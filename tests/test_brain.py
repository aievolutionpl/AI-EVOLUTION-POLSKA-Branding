"""Offline checks of fixtures, not tests of model behavior or business facts."""
from copy import deepcopy
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('brain', ROOT / 'scripts/brain.py')
brain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brain)
TODAY = date(2026, 10, 3)
TEXT = (ROOT / 'COMPANY_BRAIN.md').read_text(encoding='utf-8')


class BrainTests(unittest.TestCase):
    def setUp(self):
        self.sections, self.data = brain.load(TEXT)

    def synthetic_confirmed(self, kind='claim'):
        record = deepcopy(self.data['records'][0])
        record.update(kind=kind, status='CONFIRMED', verified_at='2026-10-03',
                      review_after='2026-10-04', publication_allowed=True,
                      sources=['SRC-TEST'])
        source = {'SRC-TEST': {'kind': 'official_page', 'locator': 'https://example.org/synthetic-test'}}
        return record, source

    def test_source_has_required_sections(self):
        self.assertEqual(set(self.sections), set(brain.SECTIONS))

    def test_registry_is_valid_but_unconfirmed(self):
        errors, warnings = brain.validate_registry(self.data, TODAY)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), len(self.data['records']))

    def test_no_legacy_record_is_publishable(self):
        sources = {s['id']: s for s in self.data['sources']}
        for record in self.data['records']:
            self.assertTrue(brain.publication_blockers(record, sources, TODAY))

    def test_duplicate_section_is_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT + '\n<!-- section:voice -->\nx\n<!-- /section:voice -->')

    def test_unclosed_marker_is_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT + '\n<!-- section:voice -->')

    def test_duplicate_registry_marker_is_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT + '\n<!-- registry:start -->')

    def test_missing_section_is_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT.replace('<!-- section:voice -->', '<!-- other -->'))

    def test_nonfinite_json_is_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT.replace('"price": 0', '"price": NaN', 1))

    def test_invalid_status_is_rejected(self):
        self.data['records'][0]['status'] = 'LIKELY'
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_duplicate_identifier_is_rejected(self):
        self.data['records'].append(deepcopy(self.data['records'][0]))
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_unknown_source_is_rejected(self):
        self.data['records'][0]['sources'] = ['SRC-NOT-FOUND']
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_confirmed_needs_verification(self):
        self.data['records'][0]['status'] = 'CONFIRMED'
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_historical_snapshot_does_not_unlock_publication(self):
        record, sources = self.synthetic_confirmed()
        sources['SRC-TEST']['kind'] = 'repository_snapshot'
        self.assertIn('historical snapshot is not current confirmation', brain.publication_blockers(record, sources, TODAY))

    def test_valid_synthetic_metadata_can_pass_gate(self):
        record, sources = self.synthetic_confirmed()
        self.assertEqual(brain.publication_blockers(record, sources, TODAY), [])

    def test_future_verification_is_blocked(self):
        record, sources = self.synthetic_confirmed()
        record['verified_at'] = '2026-10-04'
        self.assertTrue(brain.publication_blockers(record, sources, TODAY))

    def test_overdue_review_is_blocked(self):
        record, sources = self.synthetic_confirmed()
        record['review_after'] = '2026-10-02'
        self.assertIn('review overdue', brain.publication_blockers(record, sources, TODAY))

    def test_expired_record_is_blocked(self):
        record, sources = self.synthetic_confirmed()
        record['expires_at'] = '2026-10-02'
        self.assertIn('expired', brain.publication_blockers(record, sources, TODAY))

    def test_dynamic_record_needs_review_date(self):
        record, sources = self.synthetic_confirmed('tools')
        record['review_after'] = None
        self.assertIn('dynamic data has no review date', brain.publication_blockers(record, sources, TODAY))

    def test_ambiguous_offer_price_is_blocked(self):
        record, sources = self.synthetic_confirmed('offer')
        self.assertTrue(brain.publication_blockers(record, sources, TODAY))

    def test_malformed_dates_are_rejected(self):
        for value in ('20261003', '2026-02-30', 20261003):
            with self.subTest(value=value), self.assertRaises(ValueError):
                brain.parse_day(value)

    def test_boolean_price_is_rejected(self):
        self.data['records'][0]['value']['price'] = True
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_negative_price_is_rejected(self):
        self.data['records'][0]['value']['price'] = -1
        self.assertTrue(brain.validate_registry(self.data, TODAY)[0])

    def test_cta_without_delivery_is_blocked(self):
        record = next(r for r in self.data['records'] if r['id'] == 'CTA-ARGON')
        record['publication_allowed'] = True
        errors, _ = brain.validate_registry(self.data, TODAY)
        self.assertTrue(any('CTA needs an asset' in error for error in errors))

    def test_exports_are_deterministic(self):
        self.assertEqual(brain.outputs(TEXT), brain.outputs(TEXT))

    def test_legacy_and_skill_exports_are_self_contained(self):
        result = brain.outputs(TEXT)
        self.assertEqual(result['BRAND.md'], TEXT)
        self.assertEqual(result['agent/references/COMPANY_BRAIN.md'], TEXT)

    def test_thematic_view_contains_source_provenance(self):
        result = brain.outputs(TEXT)['docs/OFFER.md']
        self.assertIn('SRC-OFFER', result)
        self.assertIn('sha256:', result)
        self.assertNotIn('### News AI', result)

    def test_code_fence_links_are_ignored(self):
        self.assertEqual(brain.local_targets('```text\n[missing](no.md)\n```'), [])

    def test_fixture_drift_links_and_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = deepcopy(self.data)
            for asset in data['assets']:
                raw = b'synthetic asset fixture, not company artwork'
                file = root / asset['path']
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(raw)
                asset['git_blob_sha'] = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
            text = TEXT.replace(json.dumps(self.data, ensure_ascii=False, indent=2), json.dumps(data, ensure_ascii=False, indent=2))
            (root / 'COMPANY_BRAIN.md').write_text(text, encoding='utf-8')
            for name, content in brain.outputs(text).items():
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content, encoding='utf-8')
            (root / 'AGENTS.md').write_text('fixture', encoding='utf-8')
            (root / 'agent/AGENTS.md').write_text('fixture', encoding='utf-8')
            self.assertEqual(brain.validate(root, TODAY)[0], [])
            (root / 'BRAND.md').write_text('stale', encoding='utf-8')
            self.assertTrue(any('Stale generated' in x for x in brain.validate(root, TODAY)[0]))
            (root / 'README.md').write_text('[x](missing.md) [y](../escape.md) [z](COMPANY_BRAIN.md#absent)', encoding='utf-8')
            errors = brain.validate(root, TODAY)[0]
            for phrase in ('missing target', 'escapes repository', 'missing anchor'):
                self.assertTrue(any(phrase in error for error in errors))
            (root / data['assets'][0]['path']).write_bytes(b'changed')
            self.assertTrue(any('differs from approved hash' in error for error in brain.validate(root, TODAY)[0]))
            (root / data['assets'][0]['path']).unlink()
            self.assertTrue(any('Missing asset' in error for error in brain.validate(root, TODAY)[0]))

    def test_agent_scenarios_are_not_fake_success_reports(self):
        data = json.loads((ROOT / 'tests/agent_scenarios.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(data['scenarios']), 10)
        ids = [x['id'] for x in data['scenarios']]
        self.assertEqual(len(ids), len(set(ids)))
        for scenario in data['scenarios']:
            self.assertEqual(scenario['status'], 'NOT_RUN')
            self.assertIsNone(scenario['last_run'])
            self.assertTrue(scenario['criteria'])


if __name__ == '__main__':
    unittest.main()
