#!/usr/bin/env python3
"""Offline Nature registration, vendored-byte and dependency checks (stdlib only)."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'third_party/nature-skills'


def metadata(text):
    """Read the two scalar fields used by this pinned upstream; Codex validates YAML."""
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('missing frontmatter')
    result = {}
    lines = match[1].splitlines()
    for i, line in enumerate(lines):
        field = re.match(r'^(name|description):\s*(.*)$', line)
        if not field:
            continue
        key, value = field.groups()
        if value in ('>-', '>', '|', '|-'):
            continuation = []
            for following in lines[i + 1:]:
                if following and not following[0].isspace():
                    break
                continuation.append(following.strip())
            value = ' '.join(continuation).strip()
        elif value.startswith('"'):
            value = json.loads(value)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--discovery-json', type=Path)
    args = parser.parse_args()
    lock = json.loads((ROOT / 'third_party/nature-skills.lock.json').read_text())
    failures = []
    expected_files = {entry['path'] for entry in lock['files']}
    actual_files = {p.relative_to(VENDOR).as_posix() for p in VENDOR.rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts
                    and '.pytest_cache' not in p.parts and p.suffix not in ('.pyc', '.pyo')}
    if actual_files != expected_files:
        failures.append(f'vendor inventory drift: missing={expected_files-actual_files}; extra={actual_files-expected_files}')
    for entry in lock['files']:
        path = VENDOR / entry['path']
        if not path.is_file():
            continue
        data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if digest != entry['sha']:
            failures.append(f'upstream bytes changed: {entry["path"]}')
        if bool(path.stat().st_mode & 0o111) != (entry['mode'] == '100755'):
            failures.append(f'upstream executable mode changed: {entry["path"]}')
    original_names = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}
    if original_names & set(lock['skills']):
        failures.append('skill name collision; do not overwrite either library')
    discovered = {}
    if args.discovery_json:
        for entry in json.loads(args.discovery_json.read_text())['data']:
            failures.extend(str(error) for error in entry.get('errors', []))
            for skill in entry['skills']:
                if skill.get('scope') == 'repo' and skill.get('enabled'):
                    # Some Codex builds namespace names as <plugin>:<frontmatter-name>.
                    discovered.setdefault(skill['name'].rsplit(':', 1)[-1], []).append(Path(skill['path']).resolve())
    resources = set()
    for name in lock['skills']:
        source = VENDOR / 'skills' / name
        link = ROOT / '.agents/skills' / name
        if not link.is_symlink() or link.readlink().is_absolute() or link.resolve() != source.resolve():
            failures.append(f'{name}: incorrect relative registration')
        try:
            text = (link / 'SKILL.md').read_text()
            meta = metadata(text)
            if meta.get('name') != name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
                failures.append(f'{name}: invalid metadata name')
            if not 1 <= len(meta.get('description', '')) <= 1024:
                failures.append(f'{name}: invalid description')
        except (OSError, ValueError) as error:
            failures.append(f'{name}: unreadable/invalid SKILL.md: {error}')
            continue
        manifest = source / 'manifest.yaml'
        material = text + ('\n' + manifest.read_text() if manifest.exists() else '')
        refs = set(re.findall(r'(?<![\w/])(?:\.\./nature-shared/|static/|references/|scripts/|assets/)[\w./-]+\.(?:md|py|R|json|yaml|csv)\b', material))
        refs.update(re.findall(r'\]\(<([^>]+)>\)', text))
        for ref in refs:
            target = (source / ref).resolve()
            if not target.is_relative_to(VENDOR.resolve()) or not target.is_file():
                failures.append(f'{name}: missing/escaping dependency {ref}')
            else:
                target.read_bytes()
                resources.add(target)
        found = discovered.get(name) == [(source / 'SKILL.md').resolve()]
        if args.discovery_json and not found:
            failures.append(f'{name}: must be discovered exactly once, enabled, scope=repo')
        print(f'{name}: metadata/link/resources checked' + ('; Codex discovered' if found else ''))
    print(f'Vendor: {len(lock["files"])} files byte/mode checked; {len(resources)} referenced resources; pinned {lock["commit"]}')
    for failure in failures:
        print('FAIL:', failure)
    if not args.discovery_json:
        print('Static checks only; actual Codex discovery NOT verified by this invocation.')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
