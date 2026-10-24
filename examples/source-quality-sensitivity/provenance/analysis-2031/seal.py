#!/usr/bin/env python3
"""Seal private deliverables after completed checks; no source/repo writes."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import analyze as a

def main():
    base = Path(__file__).resolve().parent
    validation = a.read(base / 'validation.json')
    tests = a.read(base / 'test-receipt.json')
    a.require(validation['valid'] and tests['success'] and tests['tests_run'] == 29,
              'Required validation/tests have not passed')
    a.require(validation['analysis_code_sha256'] == tests['code_sha256'] == a.sha(base / 'analyze.py'),
              'Tested/validated analysis code differs')
    a.check_hash(base / 'test_analysis.py', tests['tests_sha256'])
    for name, info in validation['outputs'].items():
        a.check_hash(base / name, info['sha256'])
    inputs = a.read(base / 'immutable-input-hashes.json')
    a.check_hash(base / 'immutable-input-hashes.json', validation['immutable_input_receipt_sha256'])
    a.verify_inputs(a.INPUT_ROOT, inputs)
    benchmark = validation['benchmark_verifier']
    a.check_hash(Path(benchmark['path']), benchmark['sha256'])
    rows = [json.loads(line) for line in (base / 'joined-cases.jsonl').read_text().splitlines()]
    strata = a.read(base / 'all-strata.json')
    entries = [x for c in strata.values() for d in c['source_audit_strata'].values() for x in d.values()]
    groups = strata['all_713']['source_audit_strata']
    contradicted = [r for r in rows if r['strata']['selected_packet_category'] == 'contradicted']
    findings = {'private': True, 'post_hoc': True, 'outcome_exposure': 'per_case',
                'full_cohort_case_count': len(rows), 'all_source_stratum_categories': len(entries),
                'zero_size_categories': sum(x['case_denominator'] == 0 for x in entries),
                'full_cohort_baselines': {c: {k: v for k, v in z['baseline'].items() if k != 'case_ids'}
                                          for c, z in strata.items()},
                'all_713_source_category_denominators': {d: {k: v['case_denominator'] for k, v in x.items()}
                                                        for d, x in groups.items()},
                'contradicted_selected_packets': len(contradicted),
                'phenotype_only_recorded_contradictions': sum(r['selected_raw_review']['phenotype_only_recorded_contradiction'] for r in contradicted),
                'nonphenotype_recorded_contradictions': sum(r['selected_raw_review']['recorded_nonphenotype_contradiction'] for r in contradicted),
                'interpretation': 'Source-label recovery only. Complete reading is not complete support; contradicted is not a disproved diagnosis. All favorable/adverse/empty strata retained. No inference p-values or causal claims.'}
    a.atomic(base / 'findings.json', findings)
    local = {p.name: {'path': str(p), 'bytes': p.stat().st_size, 'sha256': a.sha(p)}
             for p in sorted(base.iterdir()) if p.is_file() and p.name not in ('delivery-manifest.json', 'delivery-manifest.sha256')}
    external = []
    for p in (a.INPUT_ROOT.parent / 'benchmark-verification.json',
              a.INPUT_ROOT.parent / 'benchmark-verifier.stdout.json'):
        external.append({'path': str(p), 'bytes': p.stat().st_size, 'sha256': a.sha(p)})
    delivery = {'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'private': True,
                'status': 'validated', 'local_deliverables': local, 'external_verifier_reports': external,
                'frozen_inputs_receipt': local['immutable-input-hashes.json'],
                'frozen_input_files': len(inputs['files']),
                'frozen_input_bytes': sum(x['bytes'] for x in inputs['files']),
                'tests_passed': tests['tests_run'], 'source_snapshot_verifier_failures': 0,
                'corrected_benchmark_verifier_status': benchmark['status'],
                'changed_roots_only': [str(base), str(a.INPUT_ROOT.parent)],
                'canonical_source_or_repo_edits': False,
                'source_snapshot_manifest_sha256': a.SOURCE_MANIFEST,
                'immutable_hash_scope': 'Local byte integrity, not an external signature. All immutable copies and analysis outputs rechecked at seal.'}
    a.atomic(base / 'delivery-manifest.json', delivery)
    p = base / 'delivery-manifest.sha256'
    with p.open('w') as f:
        f.write(a.sha(base / 'delivery-manifest.json') + '  delivery-manifest.json\n')
        f.flush(); os.fsync(f.fileno())
    base.chmod(0o700)
    for p in base.iterdir():
        if p.is_file(): p.chmod(0o600)
    fd = os.open(base, os.O_RDONLY); os.fsync(fd); os.close(fd)
    print(json.dumps({'delivery_manifest': str(base / 'delivery-manifest.json'),
                      'sha256': a.sha(base / 'delivery-manifest.json'),
                      'local_files_sealed': len(local), 'tests_passed': tests['tests_run'],
                      'source_strata': len(entries), 'zero_size_categories': findings['zero_size_categories']}, indent=2))

if __name__ == '__main__':
    main()
