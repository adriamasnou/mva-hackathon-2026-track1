#!/usr/bin/env python3
"""Verify a compact export and rederive every source-gene rank offline."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path


spec = importlib.util.spec_from_file_location('benchmark_evaluator', Path(__file__).with_name('evaluate.py'))
evaluator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluator)
spec = importlib.util.spec_from_file_location('export_provenance', Path(__file__).with_name('export_provenance.py'))
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    root = root.resolve()
    receipt = json.loads((root/'export-receipt.json').read_text())
    for name, expected in receipt['file_sha256'].items():
        path = (root/name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or sha(path) != expected:
            raise ValueError('Export member failed verification: '+name)
    jobs = json.loads((root/'jobs-manifest.json').read_text())
    execution = json.loads((root/'execution.json').read_text())
    if sha(root/'execution.json') != receipt['execution_receipt_sha256']:
        raise ValueError('Export execution receipt changed')
    provenance.verify(root,execution)
    if execution['status'] != 'completed' or execution['exit_code'] != 0:
        raise ValueError('Execution did not complete successfully')
    if sha(root/'jobs-manifest.json') != execution['jobs_manifest_sha256']:
        raise ValueError('Exported manifest differs from execution')
    results = json.loads((root/'evaluation.json').read_text())['all_case_results']
    lookup = {(r['case_id'], r['arm']): r for r in results}
    if len(lookup) != len(results) or len(results) != len(jobs) or set(lookup) != {(j['case_id'],j['arm']) for j in jobs}:
        raise ValueError('Missing or duplicate evaluated job')
    for job in jobs:
        name = Path(job['job']).stem
        if sha(root/'jobs'/Path(job['job']).name) != job['job_sha256']:
            raise ValueError('Executed job changed: '+name)
        with (root/'gene-scores'/(name+'.tsv')).open() as stream:
            records = list(csv.DictReader(stream, delimiter='\t'))
        for record in records:
            for key in ('combinedScore', 'priorityScore', 'variantScore'):
                record[key] = float(record[key]) if record[key] else None
        derived = evaluator.rank_records(records, job['gene'])
        retained = lookup[job['case_id'], job['arm']]
        if any(retained.get(k) != v for k, v in derived.items()):
            raise ValueError('Compact scores do not reproduce rank: '+name)
        if retained['output_sha256'] != execution['outputs'].get(job['result_jsonl']):
            raise ValueError('Original output hash differs from execution: '+name)
    return {'jobs_verified': len(jobs), 'files_verified': len(receipt['file_sha256']),
            'scope': 'Local export integrity and ranks from every compact gene-score table. Original genome inputs, databases and raw inference are not rerun.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export', type=Path)
    print(json.dumps(verify(parser.parse_args().export), indent=2))
