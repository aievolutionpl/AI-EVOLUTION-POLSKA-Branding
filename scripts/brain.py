#!/usr/bin/env python3
"""Deterministic Markdown exports and offline structural checks. Standard library only."""
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
            'workflows', 'evidence', 'operations', 'governance')
VIEWS = {
    'docs/OFFER.md': ('offers',),
    'docs/VOICE.md': ('voice', 'channels'),
    'docs/AUDIENCE.md': ('audience',),
    'docs/CLIENTS.md': ('audience', 'evidence'),
    'docs/STRATEGY.md': ('identity', 'operations'),
    'docs/TOOLS.md': ('operations',),
}
STATUSES = {'CONFIRMED', 'TO_CONFIRM', 'MISSING', 'CONFLICT', 'ARCHIVED'}
KINDS = {'offer', 'claim', 'evidence', 'cta', 'channel', 'tools', 'decision'}
SOURCE_KINDS = {'repository_snapshot', 'owner_confirmation',
                'official_documentation', 'official_page', 'measured_result'}
DYNAMIC = {'offer', 'cta', 'channel', 'tools'}


def parse_day(value: object) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'Invalid ISO date: {value!r}')
    return date.fromisoformat(value)


def load(text: str) -> tuple[dict[str, str], dict]:
    pattern = r'<!-- section:([a-z]+) -->\n(.*?)\n<!-- /section:\1 -->'
    pairs = re.findall(pattern, text, flags=re.S)
    sections = dict(pairs)
    if len(pairs) != len(sections) or set(sections) != set(SECTIONS):
        raise ValueError('Missing, duplicate or unknown section markers')
    starts = re.findall(r'<!-- section:([a-z]+) -->', text)
    if len(starts) != len(pairs):
        raise ValueError('Unclosed section marker')
    blocks = re.findall(r'<!-- registry:start -->\s*```json\n(.*?)\n```\s*<!-- registry:end -->', text, re.S)
    if len(blocks) != 1 or text.count('<!-- registry:start -->') != 1 or text.count('<!-- registry:end -->') != 1:
        raise ValueError('Expected exactly one JSON registry')
    def reject_constant(value: str) -> None:
        raise ValueError(f'Non-finite JSON value: {value}')
    registry = json.loads(blocks[0], parse_constant=reject_constant)
    if not isinstance(registry, dict):
        raise ValueError('Registry must be an object')
    return sections, registry


def outputs(text: str) -> dict[str, str]:
    sections, registry = load(text)
    result = {'BRAND.md': text, 'agent/references/COMPANY_BRAIN.md': text}
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    for path, topics in VIEWS.items():
        header = (f'<!-- GENERATED: COMPANY_BRAIN.md | sha256:{digest} -->\n'
                  f'# {Path(path).stem} | widok Company Brain\n\n'
                  'Nie edytuj ręcznie. Źródło: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).\n'
                  'Wygeneruj ponownie: `python3 scripts/brain.py build`.\n\n')
        records = [r for r in registry.get('records', []) if r.get('topic') in topics]
        # Keep source provenance with each portable thematic view.
        source_ids = {s for r in records for s in r.get('sources', [])}
        data = {'records': records, 'sources': [s for s in registry.get('sources', []) if s.get('id') in source_ids]}
        body = '\n\n'.join(sections[topic] for topic in topics)
        result[path] = header + body + '\n\n## Statusy i pochodzenie danych\n\n```json\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n```\n'
    return result


def publication_blockers(record: dict, sources: dict[str, dict], today: date) -> list[str]:
    """Conservative metadata gate, not a factual verification or a model safeguard."""
    reasons = []
    if record.get('status') != 'CONFIRMED':
        reasons.append('not CONFIRMED')
    if record.get('publication_allowed') is not True:
        reasons.append('publication not approved')
    refs = record.get('sources', [])
    if not isinstance(refs, list) or not refs or any(s not in sources for s in refs):
        reasons.append('missing or unknown source')
    elif all(sources[s].get('kind') == 'repository_snapshot' for s in refs):
        reasons.append('historical snapshot is not current confirmation')
    try:
        verified = parse_day(record.get('verified_at'))
        review = parse_day(record.get('review_after'))
        expiry = parse_day(record.get('expires_at'))
        if verified is None or verified > today:
            reasons.append('missing or future verification')
        if record.get('kind') in DYNAMIC and review is None:
            reasons.append('dynamic data has no review date')
        if review is not None and review < today:
            reasons.append('review overdue')
        if expiry is not None and expiry < today:
            reasons.append('expired')
    except ValueError as exc:
        reasons.append(str(exc))
    if record.get('kind') == 'offer' and record.get('publication_allowed') is True:
        value = record.get('value')
        required_offer = ('name', 'brand', 'price', 'currency', 'unit', 'price_type', 'tax_basis')
        if not isinstance(value, dict) or any(value.get(key) is None or value.get(key) == '' for key in required_offer):
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
    for field in ('sources', 'records', 'assets'):
        if not isinstance(data.get(field), list) or any(not isinstance(x, dict) for x in data[field]):
            errors.append(f'{field} must be an array of objects')
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
        if not required.issubset(record):
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
                if key in ('verified_at', 'source_claimed_verified_at') and day is not None and day > today:
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
        if record.get('kind') == 'offer':
            value = record.get('value')
            fields = {'name', 'brand', 'audience', 'problem', 'scope', 'deliverable', 'format', 'duration', 'prerequisites', 'exclusions', 'price', 'regular_price', 'currency', 'unit', 'price_type', 'tax_basis', 'availability', 'next_step', 'destination'}
            if not isinstance(value, dict) or not fields.issubset(value):
                errors.append(f'{ident}: incomplete offer schema')
            else:
                for key in ('price', 'regular_price'):
                    amount = value[key]
                    if amount is not None and (isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0):
                        errors.append(f'{ident}: invalid {key}')
                if value['price_type'] not in {'fixed', 'from', 'promotional'} or not re.fullmatch(r'[A-Z]{3}', str(value['currency'])):
                    errors.append(f'{ident}: invalid price type or currency')
        if record.get('kind') == 'cta' and record.get('publication_allowed'):
            value = record.get('value')
            if not isinstance(value, dict) or not value.get('asset_path') or value.get('delivery_verified') is not True:
                errors.append(f'{ident}: CTA needs an asset and verified delivery')
    for asset in data['assets']:
        path = asset.get('path', '')
        if not isinstance(path, str) or not path or Path(path).is_absolute() or '..' in Path(path).parts:
            errors.append(f'{asset.get("id")}: unsafe asset path')
        if not re.fullmatch(r'[0-9a-f]{40}', str(asset.get('git_blob_sha', ''))):
            errors.append(f'{asset.get("id")}: invalid asset Git hash')
    return errors, warnings


def local_targets(text: str) -> list[str]:
    # Deliberately limited to inline Markdown and quoted HTML href/src.
    clean = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)
    targets = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', clean)
    targets += re.findall(r'(?:href|src)=[\'"]([^\'"]+)[\'"]', clean)
    return targets


def link_errors(root: Path, paths: set[str]) -> list[str]:
    errors = []
    for name in sorted(p for p in paths if p.endswith('.md')):
        file = root / name
        if not file.is_file():
            continue  # inventory-only binary/source snapshots have no local text
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
                body = dest.read_text(encoding='utf-8')
                anchor = unquote(parsed.fragment)
                if not re.search(r'(?:id|name)=[\'"]' + re.escape(anchor) + r'[\'"]', body):
                    # Conventional simple GitHub heading IDs; not a full Markdown renderer.
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
        compatibility = root / 'agent/AGENTS.md'
        if not compatibility.is_file() or compatibility.read_bytes() != (root / 'AGENTS.md').read_bytes():
            errors.append('Stale compatibility instructions: agent/AGENTS.md')
    else:
        errors.append('Missing root AGENTS.md')
    for asset in data.get('assets', []):
        if asset.get('path') not in paths:
            errors.append(f'Missing asset: {asset.get("path")}')
        elif (root / asset['path']).is_file():
            raw = (root / asset['path']).read_bytes()
            digest = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
            if digest != asset['git_blob_sha']:
                errors.append(f'Asset differs from approved hash: {asset["path"]}')
        else:
            warnings.append(f'Inventory-only asset, bytes not checked: {asset["path"]}')
    errors += link_errors(root, paths)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'check'))
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--today', help='ISO date for reproducible tests; default: local current date')
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        today = parse_day(args.today) if args.today else date.today()
        if args.command == 'build':
            text = (root / 'COMPANY_BRAIN.md').read_text(encoding='utf-8')
            _, data = load(text)
            errors, _ = validate_registry(data, today)
            if errors:
                raise ValueError('; '.join(errors))
            for name, content in outputs(text).items():
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content, encoding='utf-8')
            instruction = root / 'AGENTS.md'
            if instruction.is_file():
                (root / 'agent/AGENTS.md').write_bytes(instruction.read_bytes())
            print(f'Built {len(outputs(text))} deterministic knowledge exports and synced compatibility instructions.')
            return 0
        errors, warnings = validate(root, today)
        for message in warnings:
            print('WARN:', message)
        for message in errors:
            print('ERROR:', message)
        print(f'{len(errors)} errors, {len(warnings)} warnings. Structural checks only; no live fact verification.')
        return 1 if errors else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
