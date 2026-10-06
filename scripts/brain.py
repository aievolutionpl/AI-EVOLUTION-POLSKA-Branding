#!/usr/bin/env python3
"""Build Company Brain exports, validate metadata, or report gaps. Offline, stdlib only."""
from __future__ import annotations
import argparse
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ('identity', 'offers', 'audience', 'channels', 'voice', 'visual',
            'workflows', 'evidence', 'operations', 'governance', 'onboarding',
            'website', 'marketing', 'sales', 'seo', 'systems', 'planning')
VIEWS = {
    'docs/OFFER.md': ('offers',), 'docs/VOICE.md': ('voice', 'channels'),
    'docs/AUDIENCE.md': ('audience',), 'docs/CLIENTS.md': ('audience', 'evidence'),
    'docs/STRATEGY.md': ('identity', 'operations'), 'docs/TOOLS.md': ('operations',),
    'docs/START_HERE.md': ('onboarding',), 'docs/WEBSITE.md': ('website',),
    'docs/MARKETING.md': ('marketing', 'channels'),
    'docs/SALES.md': ('sales', 'offers', 'audience'), 'docs/SEO.md': ('seo',),
    'docs/SYSTEMS.md': ('systems',), 'docs/PLANNING.md': ('planning', 'operations'),
}
STATUSES = {'CONFIRMED', 'TO_CONFIRM', 'MISSING', 'CONFLICT', 'ARCHIVED'}
KINDS = {'offer', 'claim', 'evidence', 'cta', 'channel', 'tools', 'decision',
         'profile', 'website', 'social', 'keyword', 'campaign', 'system',
         'project', 'metric', 'research'}
SOURCE_KINDS = {'repository_snapshot', 'owner_confirmation', 'official_documentation',
                'official_page', 'measured_result', 'methodology'}
DYNAMIC = {'offer', 'cta', 'channel', 'tools', 'profile', 'website', 'social',
           'campaign', 'system', 'project', 'metric'}


def parse_day(value: object) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'Invalid ISO date: {value!r}')
    return date.fromisoformat(value)


def load(text: str) -> tuple[dict[str, str], dict]:
    pairs = re.findall(r'<!-- section:([a-z]+) -->\n(.*?)\n<!-- /section:\1 -->', text, re.S)
    sections = dict(pairs)
    if len(pairs) != len(sections) or set(sections) != set(SECTIONS):
        raise ValueError('Missing, duplicate or unknown section markers')
    if len(re.findall(r'<!-- section:([a-z]+) -->', text)) != len(pairs):
        raise ValueError('Unclosed section marker')
    blocks = re.findall(r'<!-- registry:start -->\s*```json\n(.*?)\n```\s*<!-- registry:end -->', text, re.S)
    if len(blocks) != 1 or text.count('<!-- registry:start -->') != 1 or text.count('<!-- registry:end -->') != 1:
        raise ValueError('Expected exactly one JSON registry')
    def reject_constant(value: str) -> None:
        raise ValueError(f'Non-finite JSON value: {value}')
    def unique_pairs(items: list) -> dict:
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    data = json.loads(blocks[0], parse_constant=reject_constant, object_pairs_hook=unique_pairs)
    if not isinstance(data, dict):
        raise ValueError('Registry must be an object')
    return sections, data


def outputs(text: str) -> dict[str, str]:
    """Two complete copies plus small navigation views; no second edited truth."""
    sections, data = load(text)
    result = {'BRAND.md': text, 'agent/references/COMPANY_BRAIN.md': text}
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    for path, topics in VIEWS.items():
        lines = [f'<!-- GENERATED: COMPANY_BRAIN.md | sha256:{digest} -->',
                 f'# {Path(path).stem} | indeks Company Brain', '',
                 'Nie edytuj ręcznie. To indeks, nie samodzielna baza faktów.',
                 'Pełne dane: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).',
                 'Odświeżenie: `python3 scripts/brain.py build`.', '']
        for topic in topics:
            title = re.search(r'^##\s+(.+)$', sections[topic], re.M).group(1)
            lines.append(f'- [{title}](../COMPANY_BRAIN.md#{topic})')
        records = [r for r in data['records'] if r['topic'] in topics]
        refs = sorted({s for r in records for s in r['sources']})
        lines += ['', 'Rekordy: ' + (', '.join(f'`{r["id"]}`' for r in records) or 'brak'),
                  'Źródła w rejestrze: ' + (', '.join(f'`{s}`' for s in refs) or 'brak'), '',
                  'Sprawdź status, źródło, datę i ważność przed użyciem wartości.', '']
        result[path] = '\n'.join(lines)
    return result


def publication_blockers(record: dict, sources: dict[str, dict], today: date) -> list[str]:
    """Metadata gate only. Not factual verification or authorization to act."""
    reasons = []
    if record.get('status') != 'CONFIRMED':
        reasons.append('not CONFIRMED')
    if record.get('publication_allowed') is not True:
        reasons.append('publication not approved')
    refs = record.get('sources')
    valid_refs = isinstance(refs, list) and bool(refs) and all(isinstance(s, str) and s in sources for s in refs)
    if not valid_refs:
        reasons.append('missing or unknown source')
    else:
        kinds = {sources[s].get('kind') for s in refs}
        if kinds == {'repository_snapshot'}:
            reasons.append('historical snapshot is not current confirmation')
        elif kinds <= {'repository_snapshot', 'methodology'}:
            reasons.append('methodology is not business confirmation')
        if all(sources[s].get('usable_for_facts') is False for s in refs):
            reasons.append('source is not suitable for fact confirmation')
    value = record.get('value')
    if isinstance(value, dict) and value.get('basis') in {'PROPOSED', 'HYPOTHESIS'}:
        reasons.append('proposal/hypothesis is not confirmed business fact')
    try:
        verified, review, expiry = (parse_day(record.get(k)) for k in ('verified_at', 'review_after', 'expires_at'))
        if verified is None or verified > today:
            reasons.append('missing or future verification')
        if record.get('kind') in DYNAMIC and review is None:
            reasons.append('dynamic data has no review date')
        if review is not None and review < today:
            reasons.append('review overdue')
        if expiry is not None and expiry < today:
            reasons.append('expired')
        if verified and ((review and review < verified) or (expiry and expiry < verified)):
            reasons.append('review or expiry precedes verification')
    except ValueError as exc:
        reasons.append(str(exc))
    if record.get('kind') == 'offer' and record.get('publication_allowed') is True:
        required = ('name', 'brand', 'price', 'currency', 'unit', 'price_type', 'tax_basis')
        if not isinstance(value, dict) or any(value.get(k) is None or value.get(k) == '' for k in required):
            reasons.append('offer lacks price, unit or tax context')
    return reasons


def validate_registry(data: dict, today: date) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    if data.get('schema_version') != 1:
        errors.append('Unsupported schema_version')
    if not re.fullmatch(r'\d+\.\d+\.\d+', str(data.get('version', ''))):
        errors.append('Invalid version')
    try:
        updated = parse_day(data.get('updated_at'))
        if updated is None or updated > today:
            errors.append('Missing or future updated_at')
    except ValueError as exc:
        errors.append(str(exc))
    for key in ('sources', 'records', 'assets'):
        if not isinstance(data.get(key), list) or any(not isinstance(x, dict) for x in data[key]):
            errors.append(f'{key} must be an array of objects')
    if errors:
        return errors, warnings
    seen = set()
    for item in data['sources'] + data['records'] + data['assets']:
        ident = item.get('id')
        if not isinstance(ident, str) or not re.fullmatch(r'[A-Z][A-Z0-9-]*', ident) or ident in seen:
            errors.append(f'Invalid or duplicate id: {ident!r}')
        else:
            seen.add(ident)
    sources = {s['id']: s for s in data['sources'] if isinstance(s.get('id'), str)}
    for source in data['sources']:
        if source.get('kind') not in SOURCE_KINDS or not isinstance(source.get('locator'), str) or not source['locator'].strip():
            errors.append(f'{source.get("id")}: invalid source type or locator')
        try:
            reviewed = parse_day(source.get('reviewed_at'))
            if reviewed is None or reviewed > today:
                errors.append(f'{source.get("id")}: missing or future reviewed_at')
        except ValueError as exc:
            errors.append(str(exc))
    required = {'id', 'topic', 'kind', 'status', 'value', 'sources', 'verified_at', 'review_after', 'expires_at', 'publication_allowed'}
    for record in data['records']:
        ident = record.get('id', '?')
        if not required <= record.keys():
            errors.append(f'{ident}: missing fields {sorted(required - record.keys())}')
        if record.get('status') not in STATUSES or record.get('kind') not in KINDS or record.get('topic') not in SECTIONS:
            errors.append(f'{ident}: invalid status, kind or topic')
        if not isinstance(record.get('publication_allowed'), bool):
            errors.append(f'{ident}: publication_allowed must be boolean')
        refs = record.get('sources')
        if not isinstance(refs, list) or any(not isinstance(s, str) or s not in sources for s in refs):
            errors.append(f'{ident}: invalid source references')
            continue
        for key in ('verified_at', 'review_after', 'expires_at', 'source_claimed_verified_at'):
            try:
                day = parse_day(record.get(key))
                if key in ('verified_at', 'source_claimed_verified_at') and day and day > today:
                    errors.append(f'{ident}: future {key}')
            except ValueError as exc:
                errors.append(f'{ident}: {exc}')
        blockers = publication_blockers(record, sources, today)
        if record.get('status') == 'CONFIRMED' and (not refs or record.get('verified_at') is None):
            errors.append(f'{ident}: CONFIRMED needs a source and verified_at')
        if record.get('publication_allowed') is True and blockers:
            errors.append(f'{ident}: unsafe publication approval: {", ".join(blockers)}')
        elif blockers:
            warnings.append(f'{ident}: blocked for publication ({", ".join(blockers)})')
        value = record.get('value')
        if record.get('kind') == 'offer':
            fields = {'name', 'brand', 'audience', 'problem', 'scope', 'deliverable', 'format', 'duration', 'prerequisites', 'exclusions', 'price', 'regular_price', 'currency', 'unit', 'price_type', 'tax_basis', 'availability', 'next_step', 'destination'}
            if not isinstance(value, dict) or not fields <= value.keys():
                errors.append(f'{ident}: incomplete offer schema')
            else:
                for key in ('price', 'regular_price'):
                    if value[key] is not None and not nonnegative_number(value[key]):
                        errors.append(f'{ident}: invalid {key}')
                if value['price_type'] not in {'fixed', 'from', 'promotional'} or not re.fullmatch(r'[A-Z]{3}', str(value['currency'])):
                    errors.append(f'{ident}: invalid price type or currency')
        if record.get('kind') == 'cta' and record.get('publication_allowed'):
            if not isinstance(value, dict) or not value.get('asset_path') or value.get('delivery_verified') is not True:
                errors.append(f'{ident}: CTA needs an asset and verified delivery')
    for asset in data['assets']:
        path = asset.get('path', '')
        if not isinstance(path, str) or not path or Path(path).is_absolute() or '..' in Path(path).parts or '\\' in path or ':' in path:
            errors.append(f'{asset.get("id")}: unsafe asset path')
        if not re.fullmatch(r'[0-9a-f]{40}', str(asset.get('git_blob_sha', ''))):
            errors.append(f'{asset.get("id")}: invalid asset Git hash')
    errors.extend(validate_extensions(data, today))
    return errors, warnings


def nonnegative_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value >= 0


def validate_extensions(data: dict, today: date) -> list[str]:
    errors = []
    sources = {s['id']: s for s in data['sources'] if isinstance(s.get('id'), str)}
    records = {r['id']: r for r in data['records'] if isinstance(r.get('id'), str)}
    def measured(value: dict, ident: str, fields: tuple[str, ...]) -> None:
        ref = value.get('measurement_source')
        source = sources.get(ref) if isinstance(ref, str) else None
        if not source or source.get('kind') in {'repository_snapshot', 'methodology'} or source.get('usable_for_facts') is False:
            errors.append(f'{ident}: measured values need a primary measurement source')
        try:
            day = parse_day(value.get('measured_at'))
            if day is None or day > today:
                errors.append(f'{ident}: measured values need a non-future date')
        except ValueError as exc:
            errors.append(f'{ident}: {exc}')
        if any(not value.get(k) for k in fields):
            errors.append(f'{ident}: missing measurement context')
    for record in data['records']:
        ident, kind, value = record.get('id'), record.get('kind'), record.get('value')
        if kind not in {'profile', 'website', 'social', 'keyword', 'campaign', 'system', 'project', 'metric', 'research'}:
            continue
        if not isinstance(value, dict):
            errors.append(f'{ident}: context value must be an object')
            continue
        if kind == 'keyword':
            if any(not value.get(k) for k in ('phrase', 'intent', 'target', 'basis')):
                errors.append(f'{ident}: incomplete keyword brief')
            for k in ('volume', 'difficulty', 'position'):
                if value.get(k) is not None and not nonnegative_number(value[k]):
                    errors.append(f'{ident}: invalid keyword {k}')
            if nonnegative_number(value.get('difficulty')) and value['difficulty'] > 100:
                errors.append(f'{ident}: difficulty exceeds 100')
            if nonnegative_number(value.get('position')) and value['position'] < 1:
                errors.append(f'{ident}: position must be positive')
            if any(value.get(k) is not None for k in ('volume', 'difficulty', 'position')):
                measured(value, ident, ('measured_region', 'measured_tool'))
        if kind == 'system':
            if value.get('operational_status') not in {'UNKNOWN', 'PROPOSED', 'TESTED', 'IN_USE'} or value.get('access_status') not in {'UNKNOWN', 'READ_ONLY', 'WRITE_WITH_APPROVAL'}:
                errors.append(f'{ident}: invalid system status or access')
            if value.get('operational_status') in {'TESTED', 'IN_USE'} and publication_blockers(dict(record, publication_allowed=True), sources, today):
                errors.append(f'{ident}: active system needs confirmation and verification')
            for key in ('password', 'token', 'api_key', 'admin_url', 'vault_path', 'account_id'):
                if value.get(key) is not None:
                    errors.append(f'{ident}: private access field is not allowed: {key}')
        if kind == 'campaign':
            if value.get('operational_status') not in {'PROPOSED', 'READY', 'LIVE', 'PAUSED', 'ARCHIVED'}:
                errors.append(f'{ident}: invalid campaign status')
            offer_ref = value.get('offer_id')
            offer = records.get(offer_ref) if isinstance(offer_ref, str) else None
            if not offer or offer.get('kind') != 'offer':
                errors.append(f'{ident}: campaign references an unknown offer')
            if value.get('operational_status') in {'READY', 'LIVE'}:
                if publication_blockers(dict(record, publication_allowed=True), sources, today):
                    errors.append(f'{ident}: active campaign needs current factual confirmation')
                if not all(value.get(k) is True for k in ('budget_approved', 'launch_approved', 'measurement_verified')):
                    errors.append(f'{ident}: campaign lacks launch approvals or measurement')
                if not value.get('landing_page') or record.get('status') != 'CONFIRMED':
                    errors.append(f'{ident}: campaign lacks destination or confirmation')
                if not nonnegative_number(value.get('budget')) or not re.fullmatch(r'[A-Z]{3}', str(value.get('currency'))):
                    errors.append(f'{ident}: campaign lacks a valid budget and currency')
                if offer and publication_blockers(offer, sources, today):
                    errors.append(f'{ident}: campaign offer is not publishable')
        if kind == 'metric':
            if value.get('current') is not None:
                if not nonnegative_number(value['current']):
                    errors.append(f'{ident}: invalid current metric')
                measured(value, ident, ('period', 'population', 'unit', 'formula'))
            if value.get('target') is not None and (not nonnegative_number(value['target']) or value.get('target_approved') is not True):
                errors.append(f'{ident}: numerical target needs owner approval and a valid value')
    questions = data.get('open_questions', [])
    if not isinstance(questions, list) or len(questions) > 5:
        errors.append('open_questions must contain at most five items')
    else:
        ids = set()
        for q in questions:
            if not isinstance(q, dict) or not isinstance(q.get('id'), str) or not isinstance(q.get('question'), str) or not q['question'].strip():
                errors.append('invalid open question')
                continue
            if q['id'] in ids:
                errors.append('duplicate open question')
            ids.add(q['id'])
            refs = q.get('records', [])
            if not isinstance(refs, list) or any(not isinstance(r, str) or r not in records for r in refs):
                errors.append('open question references an unknown record')
    policy = data.get('review_policy', [])
    if not isinstance(policy, list):
        errors.append('review_policy must be a list')
    else:
        for rule in policy:
            if not isinstance(rule, dict) or not rule.get('scope') or not rule.get('trigger'):
                errors.append('invalid freshness rule')
                continue
            days = rule.get('interval_days')
            if days is not None and (isinstance(days, bool) or not isinstance(days, int) or days < 1):
                errors.append('invalid freshness interval')
    return errors


def context_report(data: dict, today: date) -> str:
    sources = {s['id']: s for s in data['sources']}
    lines = ['# Company Brain | raport braków', '', f'Data raportu: {today.isoformat()}',
             'To metadane, nie research, monitoring ani potwierdzenie aktualności.', '',
             '| Rekord | Status | Weryfikacja | Kontrola po | Blokady publikacji |',
             '|---|---|---|---|---|']
    def safe(value: object) -> str:
        return str(value).replace('|', '/').replace('\n', ' ')
    for record in data['records']:
        reasons = publication_blockers(record, sources, today)
        values = (record['id'], record['status'], record.get('verified_at') or 'MISSING',
                  record.get('review_after') or 'MISSING', '; '.join(reasons) or 'brak blokad metadanych')
        lines.append('| ' + ' | '.join(safe(v) for v in values) + ' |')
    lines += ['', '## Najważniejsze pytania', '']
    for i, question in enumerate(data.get('open_questions', [])[:5], 1):
        lines.append(f'{i}. {question["question"]}')
    lines += ['', 'Raport nie zmienia plików. Zgoda na dane nie jest zgodą na kampanię.', '']
    return '\n'.join(lines)


def local_targets(text: str) -> list[str]:
    clean = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)
    return re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', clean) + re.findall(r'(?:href|src)=[\'"]([^\'"]+)[\'"]', clean)


def link_errors(root: Path, paths: set[str]) -> list[str]:
    errors = []
    for name in sorted(p for p in paths if p.endswith('.md')):
        file = root / name
        if not file.is_file():
            continue
        for target in local_targets(file.read_text(encoding='utf-8')):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file.resolve()
            try:
                rel = dest.relative_to(root.resolve()).as_posix()
            except ValueError:
                errors.append(f'{name}: link escapes repository: {target}')
                continue
            if rel not in paths:
                errors.append(f'{name}: missing target: {target}')
            elif parsed.fragment and dest.is_file() and dest.suffix == '.md':
                body, anchor = dest.read_text(encoding='utf-8'), unquote(parsed.fragment)
                if not re.search(r'(?:id|name)=[\'"]' + re.escape(anchor) + r'[\'"]', body):
                    slugs = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in re.findall(r'^#{1,6}\s+(.+)$', body, re.M)}
                    if anchor not in slugs:
                        errors.append(f'{name}: missing anchor: {target}')
    return errors


def validate(root: Path, today: date, known_paths: set[str] | None = None) -> tuple[list[str], list[str]]:
    text = (root / 'COMPANY_BRAIN.md').read_text(encoding='utf-8')
    _, data = load(text)
    errors, warnings = validate_registry(data, today)
    if errors:
        return errors, warnings
    paths = known_paths if known_paths is not None else {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
    for name, content in outputs(text).items():
        file = root / name
        if not file.is_file() or file.read_text(encoding='utf-8') != content:
            errors.append(f'Stale generated file: {name}')
    if (root / 'AGENTS.md').is_file():
        alias = root / 'agent/AGENTS.md'
        if not alias.is_file() or alias.read_bytes() != (root / 'AGENTS.md').read_bytes():
            errors.append('Stale compatibility instructions: agent/AGENTS.md')
    else:
        errors.append('Missing root AGENTS.md')
    for asset in data['assets']:
        file = root / asset['path']
        if asset['path'] not in paths:
            errors.append(f'Missing asset: {asset["path"]}')
        elif file.is_file():
            raw = file.read_bytes()
            if hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() != asset['git_blob_sha']:
                errors.append(f'Asset differs from approved hash: {asset["path"]}')
        else:
            warnings.append(f'Inventory-only asset, bytes not checked: {asset["path"]}')
    return errors + link_errors(root, paths), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'check', 'report'))
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--today', help='ISO test date; defaults to current local date')
    args = parser.parse_args()
    try:
        root, today = args.root.resolve(), parse_day(args.today) if args.today else date.today()
        text = (root / 'COMPANY_BRAIN.md').read_text(encoding='utf-8')
        _, data = load(text)
        errors, _ = validate_registry(data, today)
        if errors:
            raise ValueError('; '.join(errors))
        if args.command == 'report':
            print(context_report(data, today))
            return 0
        if args.command == 'build':
            for name, content in outputs(text).items():
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content, encoding='utf-8')
            if (root / 'AGENTS.md').is_file():
                (root / 'agent/AGENTS.md').write_bytes((root / 'AGENTS.md').read_bytes())
            print(f'Built {len(outputs(text))} exports and synced compatibility instructions.')
            return 0
        errors, warnings = validate(root, today)
        for message in warnings:
            print('WARN:', message)
        for message in errors:
            print('ERROR:', message)
        print(f'{len(errors)} errors, {len(warnings)} warnings. Structural checks only; no live fact verification.')
        return int(bool(errors))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
