"""Context-schema regression tests. No API calls, model runs or live business data."""
from copy import deepcopy
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('brain_v31', ROOT / 'scripts/brain.py')
brain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brain)
TEXT = (ROOT / 'COMPANY_BRAIN.md').read_text(encoding='utf-8')
TODAY = date(2026, 10, 6)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.sections, self.data = brain.load(TEXT)

    def record(self, ident):
        return next(r for r in self.data['records'] if r['id'] == ident)

    def errors(self):
        return brain.validate_registry(self.data, TODAY)[0]

    def test_template_sections_exist(self):
        self.assertTrue({'onboarding', 'website', 'marketing', 'sales', 'seo', 'systems', 'planning'} <= self.sections.keys())

    def test_new_indexes_point_to_canonical_sections(self):
        out = brain.outputs(TEXT)
        for name in ('START_HERE', 'WEBSITE', 'MARKETING', 'SALES', 'SEO', 'SYSTEMS', 'PLANNING'):
            self.assertIn(f'docs/{name}.md', out)
            self.assertIn('../COMPANY_BRAIN.md#', out[f'docs/{name}.md'])
            self.assertIn('nie samodzielna baza', out[f'docs/{name}.md'])

    def test_methodology_cannot_confirm_a_business_fact(self):
        r = self.record('SEO-TRAINING')
        r.update(status='CONFIRMED', publication_allowed=True, verified_at='2026-10-06', review_after='2026-10-07')
        self.assertTrue(any('methodology' in e for e in self.errors()))

    def test_hypothesis_does_not_become_fact_by_adding_a_source(self):
        r = self.record('SEO-TRAINING')
        r.update(status='CONFIRMED', publication_allowed=True, verified_at='2026-10-06', review_after='2026-10-07', sources=['SRC-WEBSITE-ATTEMPT'])
        self.assertTrue(any('hypothesis' in e for e in self.errors()))

    def test_partial_page_cannot_confirm_facts(self):
        r = self.record('WEBSITE-MAIN')
        r.update(status='CONFIRMED', publication_allowed=True, verified_at='2026-10-06', review_after='2026-10-07')
        self.assertTrue(any('not suitable' in e for e in self.errors()))

    def test_keyword_metrics_need_actual_measurement(self):
        self.record('SEO-TRAINING')['value']['volume'] = 1200
        self.assertTrue(any('measurement' in e for e in self.errors()))

    def test_keyword_metrics_reject_boolean_and_negative(self):
        for amount in (True, -1):
            self.record('SEO-TRAINING')['value']['volume'] = amount
            self.assertTrue(any('invalid keyword volume' in e for e in self.errors()))

    def test_keyword_bounds(self):
        self.record('SEO-TRAINING')['value'].update(difficulty=101, position=0)
        errors = self.errors()
        self.assertTrue(any('difficulty exceeds' in e for e in errors))
        self.assertTrue(any('position must be positive' in e for e in errors))

    def test_active_system_needs_confirmation(self):
        self.record('SYSTEMS-MAP')['value']['operational_status'] = 'IN_USE'
        self.assertTrue(any('active system needs' in e for e in self.errors()))

    def test_methodology_cannot_activate_a_system(self):
        r = self.record('SYSTEMS-MAP')
        r.update(status='CONFIRMED', verified_at='2026-10-06', review_after='2026-10-07', sources=['SRC-TEMPLATE'])
        r['value']['operational_status'] = 'TESTED'
        self.assertTrue(any('active system needs' in e for e in self.errors()))

    def test_private_access_fields_are_rejected(self):
        self.record('SYSTEMS-MAP')['value']['token'] = 'synthetic-not-a-real-token'
        self.assertTrue(any('private access field' in e for e in self.errors()))

    def test_live_campaign_requires_approvals_and_offer(self):
        self.record('CAMPAIGN-TRAINING')['value']['operational_status'] = 'LIVE'
        errors = self.errors()
        self.assertTrue(any('launch approvals' in e for e in errors))
        self.assertTrue(any('offer is not publishable' in e for e in errors))

    def test_campaign_requires_known_offer(self):
        self.record('CAMPAIGN-TRAINING')['value']['offer_id'] = 'NO-SUCH-OFFER'
        self.assertTrue(any('unknown offer' in e for e in self.errors()))

    def test_active_campaign_needs_factual_confirmation(self):
        self.record('CAMPAIGN-TRAINING')['value']['operational_status'] = 'READY'
        self.assertTrue(any('current factual confirmation' in e for e in self.errors()))

    def test_metric_needs_population_period_and_source(self):
        self.record('KPI-CONVERSION')['value']['current'] = 5
        self.assertTrue(any('measurement' in e for e in self.errors()))

    def test_target_needs_owner_approval(self):
        self.record('KPI-LEADS')['value']['target'] = 10
        self.assertTrue(any('target needs owner approval' in e for e in self.errors()))

    def test_questions_are_bounded(self):
        self.data['open_questions'].append(deepcopy(self.data['open_questions'][0]))
        self.assertTrue(any('at most five' in e for e in self.errors()))

    def test_questions_link_to_known_records(self):
        self.data['open_questions'][0]['records'] = ['MISSING-RECORD']
        self.assertTrue(any('unknown record' in e for e in self.errors()))

    def test_freshness_intervals_are_positive(self):
        self.data['review_policy'][0]['interval_days'] = 0
        self.assertTrue(any('freshness interval' in e for e in self.errors()))

    def test_report_is_read_only_and_repeatable(self):
        before = deepcopy(self.data)
        first = brain.context_report(self.data, TODAY)
        self.assertEqual(first, brain.context_report(self.data, TODAY))
        self.assertEqual(self.data, before)
        self.assertIn('SEO-TRAINING', first)
        self.assertIn('nie research', first)

    def test_missing_kpis_are_not_zeroes(self):
        self.assertIsNone(self.record('KPI-CONVERSION')['value']['current'])
        self.assertIsNone(self.record('KPI-LEADS')['value']['target'])

    def test_template_source_has_no_private_drive_url(self):
        source = next(s for s in self.data['sources'] if s['id'] == 'SRC-TEMPLATE')
        self.assertNotIn('drive.google.com', source['locator'])
        self.assertEqual(source['kind'], 'methodology')
        self.assertFalse(source['usable_for_facts'])

    def test_start_cannot_replace_aiep_with_another_company(self):
        self.assertIn('nie nadpisuj kontekstu AIEP', self.sections['onboarding'])

    def test_legacy_business_records_are_unchanged(self):
        # Public v3 records; hash guards prices AND all other existing fields.
        # 3.2.0 added website scope and sources; 3.3.0 added owner decisions (PRO price, routing).
        raw = json.dumps(self.data['records'][:13], ensure_ascii=False, sort_keys=True).encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), 'c45dab60f4e15b1396c09232b49628c746ff8755140316afaeae9ce9a4ceadb7')
        prices = {r['id']: (r['value']['price'], r['value']['regular_price']) for r in self.data['records'] if r['kind'] == 'offer'}
        self.assertEqual(prices, {'OFFER-FREE': (0, None), 'OFFER-PRO': (1499, 1999),
                                  'OFFER-BUSINESS': (4999, None), 'OFFER-WORKSHOPS': (2499, None)})

    def test_owner_confirmed_pro_price_and_routing(self):
        r = self.record('OFFER-PRO')
        self.assertEqual((r['status'], r['value']['price']), ('CONFIRMED', 1499))
        self.assertIn('SRC-OWNER-20261006', r['sources'])
        # Unit and tax basis are still unknown, so the offer must stay unpublished.
        self.assertFalse(r['publication_allowed'])
        self.assertIn('offer lacks price, unit or tax context',
                      brain.publication_blockers(dict(r, publication_allowed=True),
                                                 {s['id']: s for s in self.data['sources']}, TODAY))
        self.assertEqual(self.record('DECISION-BRAND-ROUTING')['status'], 'CONFIRMED')
        for ident in ('SRC-WEBSITE-SEARCH', 'SRC-SKILLS-SEARCH', 'SRC-ONLINE-SEARCH'):
            source = next(s for s in self.data['sources'] if s['id'] == ident)
            self.assertFalse(source['usable_for_facts'])

    def test_no_fabricated_live_activities(self):
        self.assertEqual(self.record('CAMPAIGN-TRAINING')['value']['operational_status'], 'PROPOSED')
        self.assertEqual(self.record('SYSTEMS-MAP')['value']['operational_status'], 'UNKNOWN')
        self.assertFalse(self.record('WEBSITE-MAIN')['value']['forms_tested'])

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            brain.load(TEXT.replace('"schema_version": 1,', '"schema_version": 1, "schema_version": 1,', 1))

    def test_additional_behavior_scenarios_are_not_run(self):
        data = json.loads((ROOT / 'tests/context_scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['scenarios']), 7)
        self.assertEqual(len({s['id'] for s in data['scenarios']}), 7)
        for s in data['scenarios']:
            self.assertEqual(s['status'], 'NOT_RUN')
            self.assertIsNone(s['last_run'])
            self.assertTrue(s['criteria'])


if __name__ == '__main__':
    unittest.main()
