#!/usr/bin/env python3
"""Offline integration smoke: local conversion, bundled preparation and reader QA.

Does not search, install packages, use credentials, invoke a model or draw figures.
All outputs are disposable under work/nature-smoke/.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / '.agents/skills'
OUT = ROOT / 'work/nature-smoke'


def main():
    sys.dont_write_bytecode = True
    OUT.mkdir(parents=True, exist_ok=True)
    # Follow the router's offline complete-record branch, without network preflight.
    search = (REGISTRY / 'nature-academic-search').resolve(strict=True)
    loaded = []
    for rel in ['SKILL.md', 'references/workflows/wf4-citation-file-mgmt.md',
                'references/ris-bibtex-format.md']:
        (search / rel).read_text()
        loaded.append(str((search / rel).relative_to(ROOT)))
    spec = importlib.util.spec_from_file_location('nature_local_converters', search / 'scripts/converters.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = (search / 'references/pubmed-28344011.nbib').read_text()
    fields = module.parse_medline_fields(source)
    ris = module.convert_from_medline(source, 'ris')
    bib = module.convert_from_medline(source, 'bib')
    assert ris.count('TY  - JOUR') == ris.count('ER  -') == 1
    assert ris.count('AU  - ') == len(fields['AU'])
    assert [line[6:] for line in ris.splitlines() if line.startswith('AU  - ')] == fields['AU']
    doi = module._extract_doi(fields)
    assert doi and doi in ris and doi in bib
    (OUT / 'citation.ris').write_text(ris)
    (OUT / 'citation.bib').write_text(bib)
    # Exercise the exact bundled Paper Card preparer from its registered real path.
    card = (REGISTRY / 'nature-paper-card').resolve(strict=True)
    (card / 'SKILL.md').read_text()
    for rel in ['manifest.yaml', 'static/core/principles.md', 'static/core/workflow.md',
                'static/core/output-contract.md', '../nature-shared/core/terminology-ledger.md']:
        (card / rel).read_text()
        loaded.append(str((card / rel).resolve().relative_to(ROOT)))
    fixture = {'metadata': {'title': 'Synthetic integration fixture, not a research paper'},
               'blocks': [{'id': 'S001', 'page': 1, 'text':
                           'Methods\nThis synthetic fixture checks source-map loading and preserves known page locators.'},
                          {'id': 'S002', 'text':
                           'Limitations\nThis synthetic text has no page locator and must never be assigned to page one.'}]}
    input_path = OUT / 'source_map.json'
    input_path.write_text(json.dumps(fixture))
    bundle_path = OUT / 'source_bundle.json'
    subprocess.run([sys.executable, str(card / 'scripts/prepare_paper.py'),
                    str(input_path), '--output', str(bundle_path)], check=True)
    bundle = json.loads(bundle_path.read_text())
    assert bundle['validation']['status'] in ('valid', 'valid_with_warnings')
    assert bundle['locator_summary']['verified_page_blocks'] == 1
    assert len(bundle['unlocated_blocks']) == 1
    assert 'no page locator' not in bundle['pages'][0]['text']
    # This is bundled QA, not evidence of generating a full bilingual reader.
    reader = (REGISTRY / 'nature-reader').resolve(strict=True)
    subprocess.run([sys.executable, str(reader / 'scripts/validate_reader_math.py'),
                    '--self-test'], check=True)
    result = {'network_requests': 0, 'package_installs': 0,
              'academic_search': {'workflow': 'citation-file-mgmt', 'records': 1,
                                  'authors': len(fields['AU']), 'doi_preserved': True},
              'paper_card': {'operation': 'bundled source-map preparation only',
                             'known_page_preserved': True, 'unknown_page_preserved': True},
              'reader': 'bundled math QA self-test only; no full reader generated',
              'loaded_resources': loaded,
              'limits': 'No live search, full manuscript drafting, rendering or isolated peer review was tested.'}
    (OUT / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('PASS: offline citation conversion, bundled source-map preparation, reader math QA')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
