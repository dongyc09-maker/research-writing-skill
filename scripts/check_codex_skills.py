#!/usr/bin/env python3
"""Read-only registration check; optional evidence from Codex skills/list."""
import argparse
import hashlib
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
    # Nature retains its independent byte/resource checks. find-skills is a
    # project-level copy: validate its pinned bytes rather than requiring a link.
    lock_path = ROOT / 'third_party/nature-skills.lock.json'
    additional = set(json.loads(lock_path.read_text())['skills']) if lock_path.exists() else set()
    find_lock = json.loads((ROOT / 'third_party/find-skills.lock.json').read_text())
    find_path = ROOT / '.agents/skills/find-skills/SKILL.md'
    additional.add('find-skills')
    if find_path.parent.is_symlink() or not find_path.is_file():
        failures.append('find-skills: missing project-level copy')
    else:
        data = find_path.read_bytes()
        meta = dict(re.findall(r'^(name|description):\s*(.+)$', data.decode(), re.M))
        if meta.get('name') != 'find-skills' or not 1 <= len(meta.get('description', '')) <= 1024:
            failures.append('find-skills: invalid metadata')
        if args.discovery_json:
            matches = [s for entry in result['data'] for s in entry['skills']
                       if s.get('name', '').rsplit(':', 1)[-1] == 'find-skills'
                       and s.get('scope') == 'repo' and s.get('enabled')]
            if len(matches) != 1 or Path(matches[0]['path']).resolve() != find_path.resolve():
                failures.append('find-skills: must be discovered exactly once, enabled, scope=repo')
        print('find-skills: metadata/project copy checked' +
              ('; Codex discovered' if find_path.resolve() in discovered else ''))
    for entry in find_lock['files']:
        path = ROOT / entry['path']
        if not path.is_file():
            failures.append(f'find-skills: missing {entry["path"]}')
            continue
        data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if digest != entry['sha']:
            failures.append(f'find-skills: pinned bytes changed: {entry["path"]}')
    cli_lock = json.loads((ROOT / 'skills-lock.json').read_text())
    if set(cli_lock['skills']) != {'find-skills'} or cli_lock['skills']['find-skills']['source'] != find_lock['repository']:
        failures.append('find-skills: unexpected CLI lock inventory/source')
    registered = {p.name for p in (ROOT / '.agents/skills').iterdir()}
    if names & additional:
        failures.append('skill name collision between research-writing and additional skills')
    if registered != names | additional:
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
