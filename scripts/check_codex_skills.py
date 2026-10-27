#!/usr/bin/env python3
"""Read-only registration check; optional evidence from Codex skills/list."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--discovery-json', type=Path)
    args = parser.parse_args()
    failures = []
    sources = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    names = set()
    discovered = set()
    if args.discovery_json:
        result = json.loads(args.discovery_json.read_text())
        for entry in result['data']:
            failures.extend(str(e) for e in entry.get('errors', []))
            discovered.update(Path(s['path']).resolve() for s in entry['skills']
                              if s.get('scope') == 'repo' and s.get('enabled'))
    for source in sources:
        text = source.read_text()
        match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
        meta = dict(re.findall(r'^(name|description):\s*(.+)$', match[1], re.M)) if match else {}
        name = meta.get('name', '')
        if name != source.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
            failures.append(f'{source}: invalid name')
        if name in names or not 1 <= len(meta.get('description', '')) <= 1024:
            failures.append(f'{source}: duplicate name or invalid description')
        names.add(name)
        link = ROOT / '.agents/skills' / source.parent.name
        if not link.is_symlink() or link.readlink().is_absolute() or link.resolve() != source.parent.resolve():
            failures.append(f'{name}: missing/incorrect relative registration')
        for ref in re.findall(r'`(references/[^`]+)`', text):
            if not (link / ref).is_file():
                failures.append(f'{name}: missing resource {ref}')
        for ref in re.findall(r'(?<![\w/])(?:scripts/[\w.-]+|skills/[\w.-]+/(?:SKILL\.md|templates\.md))', text):
            if not (ROOT / ref).exists():
                failures.append(f'{name}: missing repository resource {ref}')
        if args.discovery_json and source.resolve() not in discovered:
            failures.append(f'{name}: not enabled in Codex discovery')
        print(f'{name}: metadata/link/resources checked' + ('; Codex discovered' if source.resolve() in discovered else ''))
    registered = {p.name for p in (ROOT / '.agents/skills').iterdir()}
    if registered != names:
        failures.append('registration/source inventory mismatch')
    # Preserve and run the existing PS1 assertions without executing PowerShell code.
    ps = (ROOT / 'scripts/check_skill_integrity.ps1').read_text()
    required = re.search(r'\$requiredFiles = @\((.*?)\n\)', ps, re.S)[1]
    for rel in re.findall(r'"([^"]+)"', required):
        if not (ROOT / rel).is_file(): failures.append(f'missing {rel}')
    front = re.search(r'\$frontmatter = @{(.*?)\n}', ps, re.S)[1]
    assertions = re.findall(r'"([^"]+)" = "([^"]+)"', front)
    assertions += [(rel, r'description:\s*Use when') for rel, _ in assertions]
    assertions += re.findall(r'Assert-Contains "([^"]+)" [\'"](.*?)[\'"] "[^"\n]+"', ps)
    for rel, pattern in assertions:
        if not re.search(pattern, (ROOT / rel).read_text(), re.I):
            failures.append(f'original integrity assertion failed: {rel}: {pattern}')
    print(f'Original integrity checks: {len(assertions)} content assertions; {len(sources)} registered modules')
    for failure in failures: print('FAIL:', failure)
    if not args.discovery_json: print('Static checks only; actual Codex discovery NOT verified by this invocation.')
    return bool(failures)

if __name__ == '__main__':
    raise SystemExit(main())
