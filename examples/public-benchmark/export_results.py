#!/usr/bin/env python3
"""Export compact, verified public results without distributing genome inputs."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import shutil


def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


runner=module('run');evaluator=module('evaluate')


def allele_key(variant, source=False):
    return (str(variant['chrom' if source else 'contigName']).removeprefix('chr'),
            int(variant['pos' if source else 'start']),variant['ref'],variant['alt'])


def variant_audit(records, case):
    target=[r for r in records if r['geneSymbol']==case['gene']]
    variants=[v for gene in target for v in gene.get('variantEvaluations',[])]
    rows=[]
    for source in case['causal_variants']:
        found=[v for v in variants if allele_key(v)==allele_key(source,True)]
        rows.append({'source_coordinate':dict(zip(['chrom','pos','ref','alt'],allele_key(source,True))),
                     'exact_matches_in_source_gene':len(found),
                     'matches':[{k:v.get(k) for k in ['filterStatus','contributesToGeneScore','whiteListed',
                                                      'passedFilterTypes','failedFilterTypes','variantScore',
                                                      'compatibleInheritanceModes','contributingInheritanceModes']} for v in found]})
    return {'method':'Exact GRCh38 contig/position/REF/ALT comparison within the source-gene record. An unmatched indel requires normalization review; this audit does not prove absence from all pipeline stages or correct phase.',
            'source_gene_in_output':bool(target),'source_variants':rows}


def export(work, out, cases_path):
    if out.exists():raise FileExistsError('Preserve prior export; choose a new destination')
    manifest=work/'jobs-manifest.json';jobs=json.loads(manifest.read_text())
    receipt=work/'execution.json';execution=json.loads(receipt.read_text())
    if execution.get('status')!='completed' or execution.get('exit_code')!=0:
        raise ValueError('Export only completed successful execution; report failed runs separately')
    if execution.get('jobs_manifest_sha256')!=runner.sha(manifest):raise ValueError('Manifest changed')
    results=evaluator.evaluate(jobs,execution)
    if any(r['status'] in ('invalid_output','missing_output','execution_failed') for r in results['all_case_results']):
        raise ValueError('Some output is not verified; do not package it as complete')
    cases={c['case_id']:c for c in json.loads(cases_path.read_text())['cases']}
    out.mkdir(parents=True);(out/'jobs').mkdir();(out/'gene-scores').mkdir()
    audits=[]
    for job in jobs:
        raw=Path(job['result_jsonl']);records=[json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
        name=Path(job['job']).stem
        shutil.copyfile(job['job'],out/'jobs'/Path(job['job']).name)
        with (out/'gene-scores'/(name+'.tsv')).open('w') as stream:
            fields=['geneSymbol','combinedScore','priorityScore','variantScore']
            writer=csv.DictWriter(stream,fieldnames=fields,delimiter='\t');writer.writeheader()
            for gene in sorted(records,key=lambda r:(-r['combinedScore'],r['geneSymbol'])):
                writer.writerow({k:gene.get(k) for k in fields})
        audits.append({'case_id':job['case_id'],'arm':job['arm'],'gene':job['gene'],
                       **variant_audit(records,cases[job['case_id']])})
    for path in [manifest,receipt,work/'protocol-before-inference.json',work/'preparation-receipt.json',
                 work/'runtime.properties',work/'batch.txt',*sorted(work.glob('addendum-*.json'))]:
        if path.exists():shutil.copyfile(path,out/path.name)
    results['execution_receipt_sha256']=runner.sha(receipt)
    (out/'evaluation.json').write_text(json.dumps(results,indent=2)+'\n')
    (out/'source-variant-audit.json').write_text(json.dumps(audits,indent=2)+'\n')
    (out/'export-receipt.json').write_text(json.dumps({
        'scope':'Compact full gene-score outputs, exact executed jobs, input/runtime/output hashes and source-allele diagnostics. No genome VCF or database is included.',
        'source_cases_sha256':runner.sha(cases_path),'export_script_sha256':runner.sha(__file__),
        'execution_receipt_sha256':runner.sha(receipt),
        'file_sha256':{str(p.relative_to(out)):runner.sha(p) for p in sorted(out.rglob('*')) if p.is_file()}},indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--cases',type=Path,required=True);a=ap.parse_args()
    export(a.work.resolve(),a.out.resolve(),a.cases.resolve())
