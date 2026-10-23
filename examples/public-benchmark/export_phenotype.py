#!/usr/bin/env python3
"""Export or verify compact phenotype-only results, without original runtime files."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import shutil

spec=importlib.util.spec_from_file_location('phenotype_runner',Path(__file__).with_name('run_phenotype.py'))
phenotype=importlib.util.module_from_spec(spec);spec.loader.exec_module(phenotype)
sha=phenotype.runner.sha


def verify(root):
    root=root.resolve()
    receipt=json.loads((root/'export-receipt.json').read_text())
    for name,expected in receipt['file_sha256'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or sha(path)!=expected:
            raise ValueError('Export member failed verification: '+name)
    execution=json.loads((root/'execution.json').read_text())
    if execution['status']!='completed' or execution['exit_code']!=0 or execution['missing_outputs']:
        raise ValueError('Incomplete execution')
    protocol=root/'protocol-before-inference.json'
    if sha(protocol)!=execution['protocol_sha256']:raise ValueError('Protocol changed')
    report=json.loads((root/'evaluation.json').read_text())
    if report['execution_receipt_sha256']!=sha(root/'execution.json'):raise ValueError('Execution changed')
    lookup={r['case_id']:r for r in report['all_case_results']}
    jobs=json.loads(protocol.read_text())['jobs']
    if len(lookup)!=len(jobs) or len(lookup)!=len(report['all_case_results']) or set(lookup)!={j['case_id'] for j in jobs}:
        raise ValueError('Missing or duplicate case')
    for job in jobs:
        if sha(root/'jobs'/Path(job['job']).name)!=job['job_sha256']:raise ValueError('Job changed')
        rows=phenotype.phenotype_records(root/'gene-scores'/(job['case_id']+'.tsv'))
        derived=phenotype.evaluator.rank_records(rows,job['gene'])
        retained=lookup[job['case_id']]
        if any(retained.get(k)!=v for k,v in derived.items()):raise ValueError('Compact scores do not reproduce phenotype rank')
        originals=[value for name,value in execution['outputs'].items() if Path(name).name==job['case_id']+'.phenotype_only.genes.tsv']
        if originals!=[retained['output_sha256']]:raise ValueError('Original output hash differs from execution')
    return {'jobs_verified':len(jobs),'files_verified':len(receipt['file_sha256']),
            'scope':'Export hashes and conservative ranks rederived from compact four-decimal phenotype scores; no new inference.'}


def export(work,out):
    if out.exists():raise FileExistsError('Preserve prior export; choose a new destination')
    protocol=work/'protocol-before-inference.json'
    execution=json.loads((work/'execution.json').read_text())
    report=json.loads((work/'evaluation.json').read_text())
    if execution['status']!='completed' or execution['exit_code']!=0 or execution['missing_outputs']:
        raise ValueError('Only successful complete executions may be exported')
    if execution['protocol_sha256']!=sha(protocol):raise ValueError('Protocol changed')
    if report['execution_receipt_sha256']!=sha(work/'execution.json'):raise ValueError('Evaluation is stale')
    jobs=json.loads(protocol.read_text())['jobs']
    prepared=[]
    for job in jobs:
        if sha(job['job'])!=job['job_sha256']:raise ValueError('Job changed')
        source=work/'results'/(job['case_id']+'.phenotype_only.genes.tsv')
        if execution['outputs'].get(str(source))!=sha(source):raise ValueError('Output changed')
        prepared.append((job,phenotype.phenotype_records(source)))
    out.mkdir(parents=True);(out/'jobs').mkdir();(out/'gene-scores').mkdir()
    for job,rows in prepared:
        shutil.copyfile(job['job'],out/'jobs'/Path(job['job']).name)
        with (out/'gene-scores'/(job['case_id']+'.tsv')).open('w') as f:
            writer=csv.writer(f,delimiter='\t');writer.writerow(['GENE_SYMBOL','EXOMISER_GENE_PHENO_SCORE'])
            for r in sorted(rows,key=lambda r:(-r['combinedScore'],r['geneSymbol'])):
                writer.writerow([r['geneSymbol'],str(r['combinedScore'])])
    for name in ['protocol-before-inference.json','execution.json','evaluation.json','batch.txt','runtime.properties']:
        shutil.copyfile(work/name,out/name)
    for path in sorted(work.glob('addendum-*.json')):shutil.copyfile(path,out/path.name)
    (out/'export-receipt.json').write_text(json.dumps({
        'scope':'Full compact unique-gene phenotype scores and execution/configuration records, without genome or database files.',
        'script_sha256':sha(__file__),
        'file_sha256':{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()}},indent=2)+'\n')
    return verify(out)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path);parser.add_argument('--out',type=Path)
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    if args.verify:
        if args.work or args.out:parser.error('Use --verify alone')
        result=verify(args.verify)
    else:
        if not args.work or not args.out:parser.error('Export requires --work and --out')
        result=export(args.work.resolve(),args.out.resolve())
    print(json.dumps(result,indent=2))
