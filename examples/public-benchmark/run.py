#!/usr/bin/env python3
"""Run an already-frozen Exomiser batch and retain execution provenance."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def check_inputs(jobs):
    checked={}
    for job in jobs:
        for name in ('job','vcf'):
            path=job[name]
            if path not in checked:
                checked[path]=sha(path)
            actual=checked[path]
            if actual!=job[name+'_sha256']:
                raise ValueError(f'Frozen {name} changed: {path}')
        if Path(job['result_jsonl']).exists():
            raise FileExistsError('Refusing to overwrite existing inference: '+job['result_jsonl'])
    return checked


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--java',type=Path,required=True)
    ap.add_argument('--jar',type=Path,required=True)
    ap.add_argument('--properties',type=Path,required=True)
    ap.add_argument('--data-receipt',type=Path,action='append',required=True)
    ap.add_argument('--heap',default='12g')
    args=ap.parse_args()
    work=args.work.resolve()
    record=work/'execution.json'
    if record.exists(): raise FileExistsError('Choose a new run; execution receipt already exists')
    jobs=json.loads((work/'jobs-manifest.json').read_text())
    inputs=check_inputs(jobs)
    jar=args.jar.resolve()
    software={str(p):sha(p) for p in [jar,*sorted((jar.parent/'lib').glob('*.jar'))]}
    command=[str(args.java.resolve()),'-Xmx'+args.heap,
             '-Dspring.config.location=file:'+str(args.properties.resolve()),
             '-jar',str(jar),'batch',str(work/'batch.txt')]
    result={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),
            'command':command,'software_sha256':software,'inputs_sha256':inputs,
            'properties_sha256':sha(args.properties),'properties_text':args.properties.read_text(),
            'data_receipts':{str(p):{'sha256':sha(p),'content':json.loads(p.read_text())} for p in args.data_receipt},
            'batch_sha256':sha(work/'batch.txt'),
            'java_version':subprocess.run([str(args.java),'-version'],capture_output=True,text=True,check=True).stderr,
            'platform':{'system':platform.system(),'release':platform.release(),'machine':platform.machine()},
            'planned_jobs':len(jobs)}
    record.write_text(json.dumps(result,indent=2)+'\n')
    began=time.monotonic()
    with (work/'execution.log').open('xb') as log:
        completed=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,cwd=work)
    result.update(status='completed' if completed.returncode==0 else 'failed',
                  exit_code=completed.returncode,elapsed_seconds=time.monotonic()-began,
                  finished_utc=datetime.now(timezone.utc).isoformat(),log_sha256=sha(work/'execution.log'))
    result['outputs']={j['result_jsonl']:sha(j['result_jsonl']) for j in jobs if Path(j['result_jsonl']).exists()}
    result['missing_outputs']=[j['result_jsonl'] for j in jobs if not Path(j['result_jsonl']).exists()]
    record.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','exit_code','elapsed_seconds','planned_jobs','missing_outputs']}))
    raise SystemExit(completed.returncode or bool(result['missing_outputs']))


if __name__=='__main__':main()
