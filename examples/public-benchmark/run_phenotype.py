#!/usr/bin/env python3
"""Execute and evaluate the frozen phenotype-only knowledge comparator."""
import argparse
import csv
from datetime import datetime, timezone
import importlib.util
import json
import math
from pathlib import Path
import platform
import subprocess
import time


def sibling(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


runner=sibling('run');evaluator=sibling('evaluate')


def phenotype_records(path):
    """Collapse modes by best reported phenotype score, retaining TSV precision."""
    genes={}
    with Path(path).open() as stream:
        rows=csv.DictReader(stream,delimiter='\t')
        if not {'GENE_SYMBOL','EXOMISER_GENE_PHENO_SCORE'}<=set(rows.fieldnames or []):
            raise ValueError('Unrecognised gene TSV header')
        for row in rows:
            gene=row['GENE_SYMBOL'];score=float(row['EXOMISER_GENE_PHENO_SCORE'])
            if not gene or not math.isfinite(score) or not 0<=score<=1:
                raise ValueError('Invalid phenotype score or gene')
            genes[gene]=max(genes.get(gene,0),score)
    if not genes:raise ValueError('Empty phenotype result')
    return [{'geneSymbol':gene,'combinedScore':score} for gene,score in genes.items()]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--java',type=Path,required=True)
    ap.add_argument('--jar',type=Path,required=True)
    ap.add_argument('--data-receipt',type=Path,action='append',required=True)
    a=ap.parse_args();work=a.work.resolve();receipt=work/'execution.json'
    if receipt.exists():raise FileExistsError('Preserve prior execution; choose a new documented run')
    protocol=work/'protocol-before-inference.json'
    jobs=json.loads(protocol.read_text())['jobs']
    runner.check_batch(work/'batch.txt',jobs)
    outputs={j['case_id']:work/'results'/(j['case_id']+'.phenotype_only.genes.tsv') for j in jobs}
    if any(p.exists() for p in outputs.values()):raise FileExistsError('Pre-existing inference output')
    for j in jobs:
        if runner.sha(j['job'])!=j['job_sha256']:raise ValueError('Frozen job changed')
    properties=work/'runtime.properties';jar=a.jar.resolve()
    command=[str(a.java.resolve()),'-Xmx12g','-Dspring.config.location=file:'+str(properties),
             '-jar',str(jar),'batch',str(work/'batch.txt')]
    record={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),
            'command':command,'script_sha256':runner.sha(__file__),
            'protocol_sha256':runner.sha(protocol),'batch_sha256':runner.sha(work/'batch.txt'),
            'properties_sha256':runner.sha(properties),'properties_text':properties.read_text(),
            'software_sha256':{str(p):runner.sha(p) for p in [jar,*sorted((jar.parent/'lib').glob('*.jar'))]},
            'data_receipts':{str(p):{'sha256':runner.sha(p),'content':json.loads(p.read_text())} for p in a.data_receipt},
            'java_version':subprocess.run([str(a.java),'-version'],capture_output=True,text=True,check=True).stderr,
            'platform':platform.platform(),'planned_jobs':len(jobs)}
    receipt.write_text(json.dumps(record,indent=2)+'\n');start=time.monotonic()
    with (work/'execution.log').open('xb') as log:
        proc=subprocess.run(command,cwd=work,stdout=log,stderr=subprocess.STDOUT)
    record.update(status='completed' if proc.returncode==0 else 'failed',exit_code=proc.returncode,
                  finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start,
                  log_sha256=runner.sha(work/'execution.log'))
    record['outputs']={str(p):runner.sha(p) for p in outputs.values() if p.exists()}
    record['missing_outputs']=[str(p) for p in outputs.values() if not p.exists()]
    receipt.write_text(json.dumps(record,indent=2)+'\n')
    results=[]
    for job in jobs:
        row={k:job[k] for k in ('case_id','gene','primary_autosomal')};path=outputs[job['case_id']]
        if proc.returncode:row.update(status='execution_failed',rank_min=None,rank_max=None)
        elif not path.exists():row.update(status='missing_output',rank_min=None,rank_max=None)
        else:
            try:
                row.update(evaluator.rank_records(phenotype_records(path),job['gene']))
                row['output_sha256']=runner.sha(path)
            except (ValueError,KeyError,TypeError) as err:
                row.update(status='invalid_output',error=str(err),rank_min=None,rank_max=None)
        results.append(row)
    primary=[r for r in results if r['primary_autosomal']]
    report={'interpretation':'Knowledge-only original-HPO comparator; no VCF or variant score. Not diagnostic validation.',
            'score':'Best EXOMISER_GENE_PHENO_SCORE across modes for each unique gene; four-decimal TSV precision.',
            'tie_policy':'Conservative worst tied rank at the exported precision; does not imply exact full-precision ties.',
            'execution_receipt_sha256':runner.sha(receipt),'all_case_results':results,
            'primary_autosomal':{'denominator':len(primary),'recovered':{str(k):sum(r['status']=='scored' and r['rank_max']<=k for r in primary) for k in (1,5,10)}}}
    (work/'evaluation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['primary_autosomal']))
    raise SystemExit(proc.returncode or any(r['status'] in ('missing_output','invalid_output','execution_failed') for r in results))


if __name__=='__main__':main()
