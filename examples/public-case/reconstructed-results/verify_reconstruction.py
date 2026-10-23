#!/usr/bin/env python3
"""Verify an extracted compact FGFR2 package offline, without source paths or dependencies."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path, PurePosixPath


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(export):
    export = Path(export).resolve()
    receipt_path = export / 'export-receipt.json'
    require(receipt_path.is_file() and not receipt_path.is_symlink(), 'Missing regular export receipt')
    receipt = json.loads(receipt_path.read_text())
    require(receipt.get('status') == 'verified_compact_export', 'Not a completed compact export')
    members = receipt['file_sha256']
    require(isinstance(members, dict) and bool(members), 'Empty member manifest')
    actual = set()
    for path in export.rglob('*'):
        require(not path.is_symlink(), 'Symlinks are not portable package members')
        if path.is_file() and path != receipt_path:
            actual.add(path.relative_to(export).as_posix())
    require(actual == set(members), 'Package member set differs from export receipt')
    for name, expected in members.items():
        relative = PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts and '\\' not in name,
                'Unsafe member path: ' + name)
        require(sha(export / name) == expected, 'Member hash mismatch: ' + name)

    def read(name):
        require(name in members, 'Required member missing: ' + name)
        return json.loads((export / name).read_text())

    def bound(name, expected):
        require(name in members and members[name] == expected, 'Receipt binding mismatch: ' + name)

    execution = read('execution.json')
    bound('execution.json', receipt.get('execution_receipt_sha256'))
    require(execution.get('status') == 'completed' and execution.get('exit_code') == 0
            and execution.get('missing_outputs') == [] and execution.get('planned_jobs') == 2,
            'Execution was not a complete successful two-job batch')
    jobs = read('jobs-manifest.json')
    require([j['case_id'] for j in jobs] == ['mini', 'genome'], 'Wrong case membership or order')
    require(all(j['gene'] == 'FGFR2' for j in jobs), 'Wrong target gene')
    bound('jobs-manifest.json', execution.get('jobs_manifest_sha256'))
    bound('runtime.properties', execution.get('properties_sha256'))
    require((export / 'runtime.properties').read_text() == execution.get('properties_text'),
            'Properties content differs from execution')
    bound('batch.txt', execution.get('batch_sha256'))
    for job in jobs:
        require(not any(c.isspace() or c in "\"'" for c in job['job']), 'Invalid batch job path')
    require((export / 'batch.txt').read_text().splitlines() == ['--analysis ' + j['job'] for j in jobs],
            'Batch differs from manifest or uses shell quoting')
    bound('execution.log', execution.get('log_sha256'))
    bound('code/run.py', execution.get('wrapper_sha256'))
    bound('code/evaluate.py', execution.get('evaluation_script_sha256'))
    require(bool(execution.get('software_sha256')), 'Missing recorded software hashes')

    designs = {name for name in ('protocol-before-inference.json', 'preparation-receipt.json') if name in members}
    require('protocol-before-inference.json' in designs, 'Missing protocol')
    if 'design_records' in execution:
        require(set(execution['design_records']) == designs, 'Design record membership mismatch')
        for name, record in execution['design_records'].items():
            bound(name, record.get('sha256'))
            require(read(name) == record.get('content'), 'Design content mismatch: ' + name)
        require(receipt.get('design_record_binding') == 'Hashes and JSON content verified against execution.design_records',
                'Incorrect design-binding label')
    else:
        require(receipt.get('design_record_binding') == 'Older receipt without design_records: current snapshots only; no execution-time binding asserted',
                'Older design snapshots must not claim execution-time binding')
    addenda = {name for name in members if PurePosixPath(name).parent == PurePosixPath('.')
               and name.startswith('addendum-') and name.endswith('.json')}
    require(set(execution.get('pre_inference_addenda', {})) == addenda, 'Addendum membership mismatch')
    for name, record in execution.get('pre_inference_addenda', {}).items():
        bound(name, record.get('sha256'))
        require(read(name) == record.get('content'), 'Addendum content mismatch: ' + name)
    require(bool(execution.get('data_receipts')), 'No database receipt binding')
    data_names = set()
    for i, (source, record) in enumerate(execution['data_receipts'].items(), 1):
        name = f'data-receipts/{i}-{PurePosixPath(source).name}'
        data_names.add(name)
        bound(name, record.get('sha256'))
        require(read(name) == record.get('content'), 'Database receipt content mismatch')
    require({n for n in members if n.startswith('data-receipts/')} == data_names, 'Database receipt membership mismatch')
    require(set(execution.get('outputs', {})) == {j['result_jsonl'] for j in jobs}, 'Output hash membership mismatch')
    require(set(execution.get('inputs_sha256', {})) == {j[k] for j in jobs for k in ('job', 'vcf')},
            'Input hash membership mismatch')
    evaluation = read('evaluation.json')['all_case_results']
    comparisons = read('historical-vs-reconstructed.json')
    require([r['case_id'] for r in evaluation] == ['mini', 'genome'], 'Evaluation case membership mismatch')
    require([r['case_id'] for r in comparisons] == ['mini', 'genome'], 'Comparison case membership mismatch')
    history = {r['case']: r for r in read('historical-result-summary.json')['results']}
    audits = read('source-variant-audit.json')
    require([r['case_id'] for r in audits] == ['mini', 'genome'], 'Variant audit case membership mismatch')
    results = []
    for job, reported, comparison in zip(jobs, evaluation, comparisons):
        case = job['case_id']
        bound('jobs/' + case + '.yml', job['job_sha256'])
        for kind in ('job', 'vcf'):
            require(execution['inputs_sha256'].get(job[kind]) == job[kind + '_sha256'],
                    'Input differs from executed manifest: ' + case + '/' + kind)
        require(reported.get('output_sha256') == execution['outputs'][job['result_jsonl']],
                'Output hash not bound to execution: ' + case)
        name = 'gene-scores/' + case + '.tsv'
        require(name in members, 'Missing gene scores: ' + case)
        with (export / name).open(newline='') as stream:
            reader = csv.DictReader(stream, delimiter='\t')
            require(reader.fieldnames == ['rank_min', 'rank_max', 'geneSymbol', 'combinedScore',
                                          'priorityScore', 'variantScore', 'pValue'], 'Unexpected score columns')
            rows = list(reader)
        require(bool(rows), 'No gene records: ' + case)
        require(all(r['geneSymbol'] for r in rows) and len({r['geneSymbol'] for r in rows}) == len(rows),
                'Missing or duplicate gene identity: ' + case)
        for row in rows:
            for key in ('combinedScore', 'priorityScore', 'variantScore', 'pValue'):
                row[key] = float(row[key]) if row[key] else None
                require((row[key] is None and key != 'combinedScore') or
                        (row[key] is not None and math.isfinite(row[key])), 'Invalid score: ' + case)
        # Independently derive intervals from every score. Do not execute packaged evaluator code.
        counts = {}
        for row in rows:
            counts[row['combinedScore']] = counts.get(row['combinedScore'], 0) + 1
        bounds, before = {}, 0
        for score in sorted(counts, reverse=True):
            bounds[score] = (before + 1, before + counts[score])
            before += counts[score]
        for row in rows:
            require((int(row['rank_min']), int(row['rank_max'])) == bounds[row['combinedScore']],
                    'Gene TSV rank/tie interval mismatch: ' + case + '/' + row['geneSymbol'])
        target = next((r for r in rows if r['geneSymbol'] == 'FGFR2'), None)
        expected = {'status': 'not_scored', 'rank_min': None, 'rank_max': None, 'scored_genes': len(rows)}
        if target:
            lo, hi = bounds[target['combinedScore']]
            expected.update(status='scored', rank_min=lo, rank_max=hi,
                            combined_score=target['combinedScore'], priority_score=target['priorityScore'],
                            variant_score=target['variantScore'])
        expected.update(case_id=case, gene='FGFR2', output_sha256=execution['outputs'][job['result_jsonl']])
        for key in ('rank_min', 'rank_max', 'scored_genes'):
            require(reported.get(key) is None or type(reported[key]) is int, 'Invalid integer result field: ' + key)
        require(reported == expected, 'FGFR2 evaluation rank/score differs from full TSV: ' + case)
        require(comparison.get('new_reconstructed') == expected, 'Historical comparison has an altered new result: ' + case)
        old = history['mini' if case == 'mini' else 'HG002-spiked']
        require(old['top'][0]['geneSymbol'] == 'FGFR2', 'Historical summary does not support rank one')
        old_expected = {'rank': 1, 'rank_basis': 'Retained August summary; only top rows bundled',
                        'scored_genes': old['gene_records'], 'source_jsonl_sha256': old['source_sha256'], **old['top'][0]}
        require(comparison.get('historical') == old_expected, 'Historical comparison differs from retained summary')
        results.append(expected)
    return {'status': 'verified_offline', 'verified_members': len(members), 'all_case_results': results,
            'limits': 'Package consistency and rank arithmetic verified without source paths. The unsigned member manifest is not authenticity proof. '
                      'Without raw JSONL/VCFs/software/databases, their recorded hashes and TSV derivation cannot be independently recomputed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', dest='export_dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.export_dir), indent=2, allow_nan=False))
