#!/usr/bin/env python3
"""Verify a portable review snapshot, not the underlying papers or clinical truth."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root):
    root = Path(root).resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    errors = []
    for name, expected in manifest['files'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or sha(path) != expected:
            errors.append('Missing, escaped or changed file: ' + name)
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
              and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    if actual != set(manifest['files']):
        errors.append('Manifest file set differs from delivered file set')
    if errors:
        return errors
    summary = json.loads((root / 'summary.json').read_text())
    inventory = json.loads((root / 'inventory.json').read_text())
    papers = {p['pmid']: p for p in inventory['papers']}
    reports = {p['pmid']: p for p in summary['papers']}
    if len(papers) != len(inventory['papers']) or len(reports) != len(summary['papers']):
        errors.append('Duplicate PMID')
    if sha(root / 'inventory.json') != summary['inventory_sha256']:
        errors.append('Inventory binding mismatch')
    expected_cases, reviewed_cases = defaultdict(set), defaultdict(set)
    contexts = {}
    for pmid, paper in papers.items():
        path = root / 'contexts' / pmid / 'source-context.json'
        context = json.loads(path.read_text())
        contexts[pmid] = {p['member']: p for p in context['packets']}
        if context['pmid'] != pmid or len(contexts[pmid]) != len(context['packets']):
            errors.append('Invalid context identity/duplicate: ' + pmid)
        for packet in context['packets']:
            expected_cases[packet['case_id']].add((pmid, packet['member']))
        for field, selected in [('selected_case_ids', True), ('alternate_case_ids', False)]:
            ids = {p['case_id'] for p in context['packets'] if p['selected_record'] is selected}
            if ids != set(paper[field]) or ids != set(context[field]):
                errors.append('Context/inventory case mismatch: ' + pmid)
    adjudicated, categories, exposure = 0, Counter(), Counter()
    adjudicated_categories = Counter()
    for pmid, report in reports.items():
        record = json.loads((root / 'records' / (pmid + '.json')).read_text())
        exposure[record['audit']['outcome_exposure']] += 1
        if record['pmid'] != pmid or report['valid'] is not True:
            errors.append('Invalid record/report identity: ' + pmid)
        expected_bindings = {
            'inventory_sha256': sha(root / 'inventory.json'),
            'context_sha256': sha(root / 'contexts' / pmid / 'source-context.json'),
            'protocol_sha256': sha(root / 'protocol.json'),
            'case_manifest_sha256': inventory['case_manifest_sha256'],
            'packet_archive_sha256': inventory['packet_archive_sha256']}
        if record['bindings'] != expected_bindings:
            errors.append('Record input binding mismatch: ' + pmid)
        main_full = any(c['kind'] == 'main_text' and c['status'] == 'full'
                        for c in record['components'])
        if report['main_text_full'] != main_full:
            errors.append('Main-text coverage disagreement: ' + pmid)
        mappings = []
        for packet in record['packets']:
            source = contexts[pmid].get(packet['member'])
            role = 'selected' if source and source['selected_record'] else 'alternate'
            if (not source or packet['packet_sha256'] != source['sha256']
                    or packet['case_id'] != source['case_id'] or packet['role'] != role):
                errors.append('Packet source binding mismatch: ' + pmid)
            done = packet['review_status'] == 'adjudicated'
            adjudicated += done
            categories[packet['category']] += 1
            if done:
                adjudicated_categories[packet['category']] += 1
            mappings.append({'case_id': packet['case_id'], 'pmid': pmid,
                             'member': packet['member'], 'role': packet['role'],
                             'category': packet['category'], 'adjudicated': done})
            if report['complete'] and done:
                reviewed_cases[packet['case_id']].add((pmid, packet['member']))
        key = lambda x: (x['case_id'], x['member'])
        if sorted(mappings, key=key) != sorted(report['case_mappings'], key=key):
            errors.append('Record/report mapping disagreement: ' + pmid)
        if set(contexts[pmid]) != {p['member'] for p in record['packets']}:
            errors.append('Missing/extra packet mapping: ' + pmid)
        if len(record['packets']) != len(contexts[pmid]):
            errors.append('Duplicate packet mapping: ' + pmid)
        if report['packets_adjudicated'] != sum(p['adjudicated'] for p in mappings):
            errors.append('Paper packet-count disagreement: ' + pmid)
    incomplete_cases = sorted(c for c, mappings in expected_cases.items()
                              if reviewed_cases.get(c) != mappings)
    computed = {
        'papers_expected': len(papers), 'papers_valid_records': len(reports),
        'papers_complete': sum(p['complete'] for p in reports.values()),
        'papers_main_text_full': sum(p['main_text_full'] for p in reports.values()),
        'cases_expected': len(expected_cases),
        'cases_complete': len(expected_cases) - len(incomplete_cases),
        'packets_expected': sum(len(x) for x in contexts.values()),
        'packets_adjudicated': adjudicated,
        'paper_outcome_exposure_counts': dict(exposure),
        'packet_categories_valid_records': {c: categories[c] for c in
                                           ('supported', 'qualified', 'contradicted', 'unresolved')},
        'missing_or_invalid_pmids': sorted(set(papers) - set(reports), key=int),
        'incomplete_pmids': sorted((k for k, v in reports.items() if not v['complete']), key=int),
        'incomplete_case_ids': incomplete_cases}
    for field, value in computed.items():
        if summary[field] != value:
            errors.append('Summary disagreement: ' + field)
    category_file = json.loads((root / 'adjudicated-categories.json').read_text())
    if category_file['counts'] != dict(adjudicated_categories):
        errors.append('Adjudicated category-count disagreement')
    if summary['audit']['timing'] != 'post_inference' or summary['audit']['clinical_truth_established']:
        errors.append('Invalid audit scope')
    return errors


if __name__ == '__main__':
    try:
        errors = check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [str(exc)]
    for error in errors:
        print('FAIL:', error)
    print(f'Portable snapshot consistency: {len(errors)} failure(s).')
    print('Does not open source articles, certify reading/identity, rerun inference or establish clinical truth.')
    raise SystemExit(bool(errors))
