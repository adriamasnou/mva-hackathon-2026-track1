#!/usr/bin/env python3
"""Export source-gene raw records, or verify joint-allele evidence offline.

The full source JSONL hash is checked at export. The compact verifier checks the
retained excerpt/receipt and its scores against the main export; it cannot hash
an unavailable full original JSONL or establish biological causality/phase.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from joint_mode import exact_alleles

HERE = Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def dump(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

def export(works, out):
    if out.exists(): raise FileExistsError('Preserve prior export')
    cases_path=HERE/'source-selection/frozen-cases.json'
    cases={c['case_id']:c for c in load(cases_path)['cases']}
    rows=[]
    for label, work in works.items():
        ex=load(work/'execution.json');manifest=work/'jobs-manifest.json'
        if ex['status']!='completed' or ex['exit_code'] or ex['missing_outputs']:
            raise ValueError('Incomplete execution')
        if sha(manifest)!=ex['jobs_manifest_sha256']: raise ValueError('Changed jobs')
        for j in load(manifest):
            raw=Path(j['result_jsonl']);h=sha(raw)
            if ex['outputs'].get(str(raw))!=h: raise ValueError('Raw hash mismatch')
            found=[json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
            found=[r for r in found if r['geneSymbol']==j['gene']]
            if len(found)!=1: raise ValueError('Missing/duplicated source-gene record')
            record=found[0]
            rows.append({'background':label,'case_id':j['case_id'],'arm':j['arm'],
                         'source_jsonl_sha256':h,'source_gene_record':record,
                         'derived':exact_alleles([record],cases[j['case_id']])})
    if len(rows)!=96: raise ValueError('Expected both complete 48-job batches')
    out.mkdir(parents=True)
    dump(out/'records.json',rows)
    dump(out/'receipt.json',{'exported_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Complete source-gene records extracted from hash-verified public JSONL, plus derived allele/mode evidence. Original full files are not included.',
        'cases_sha256':sha(cases_path),'records_sha256':sha(out/'records.json'),
        'exporter_sha256':sha(__file__),'helper_sha256':sha(HERE/'joint_mode.py')})
    return verify(out)

def verify(out):
    rec=load(out/'receipt.json');cases_path=HERE/'source-selection/frozen-cases.json'
    for p,key in [(out/'records.json','records_sha256'),(cases_path,'cases_sha256'),
                  (Path(__file__),'exporter_sha256'),(HERE/'joint_mode.py','helper_sha256')]:
        if sha(p)!=rec[key]:raise ValueError('Changed evidence/component: '+str(p))
    cases={c['case_id']:c for c in load(cases_path)['cases']}
    rows=load(out/'records.json');seen=set();exceptions=[]
    expected={(bg,c,arm) for bg in ('HG002','HG001') for c in cases
              for arm in ('original','half_missing','swapped','none')}
    for row in rows:
        key=(row['background'],row['case_id'],row['arm'])
        if key not in expected or key in seen:raise ValueError('Unexpected/duplicate row')
        seen.add(key); bg,case_id,arm=key; record=row['source_gene_record']
        case=cases[case_id]; exported=HERE/'results'/bg
        ex=load(exported/'execution.json')
        stem=case_id+'.'+arm
        hashes=[h for p,h in ex['outputs'].items() if Path(p).name==stem+'.jsonl']
        if hashes!=[row['source_jsonl_sha256']]:raise ValueError('Original hash not in execution')
        with (exported/'gene-scores'/(stem+'.tsv')).open() as f:
            scores=[r for r in csv.DictReader(f,delimiter='\t') if r['geneSymbol']==case['gene']]
        if len(scores)!=1:raise ValueError('Source gene not in compact scores')
        if record['geneSymbol']!=case['gene']:raise ValueError('Wrong source gene')
        for field in ('combinedScore','priorityScore','variantScore'):
            value=float(scores[0][field]) if scores[0][field] else None
            if value!=record.get(field):raise ValueError('Excerpt score differs')
        derived=exact_alleles([record],case)
        if derived!=row['derived']:raise ValueError('Allele/mode derivation differs')
        if derived['all_source_alleles_in_any_best_mode'] is not True:
            exceptions.append({'background':bg,'gene':case['gene'],'arm':arm,
                'joint_best':derived['all_source_alleles_in_any_best_mode']})
    if seen!=expected:raise ValueError('Missing rows')
    return {'source_gene_records_verified':len(rows),'joint_best_mode_exceptions':exceptions,
            'scope':'Excerpt integrity, full-score consistency and exact-allele/mode arithmetic; no new inference or clinical validation.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--hg002',type=Path);p.add_argument('--hg001',type=Path)
    p.add_argument('--out',type=Path);p.add_argument('--verify',type=Path)
    a=p.parse_args()
    if a.verify:
        if a.hg001 or a.hg002 or a.out:p.error('Use --verify alone')
        result=verify(a.verify)
    else:
        if not (a.hg001 and a.hg002 and a.out):p.error('Export requires --hg002 --hg001 --out')
        result=export({'HG002':a.hg002.resolve(),'HG001':a.hg001.resolve()},a.out.resolve())
    print(json.dumps(result,indent=2))
