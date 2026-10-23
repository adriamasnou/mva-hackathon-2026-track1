#!/usr/bin/env python3
"""Report all frozen cases, conservative tie ranks and execution failures."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def rank_records(records, target):
    seen=set()
    for r in records:
        gene,score=r['geneSymbol'],r['combinedScore']
        if not gene or gene in seen: raise ValueError('Missing or duplicated gene identity')
        seen.add(gene)
        if isinstance(score,bool) or not isinstance(score,(int,float)) or not math.isfinite(score):
            raise ValueError('Invalid/nonfinite combined score')
    matches=[r for r in records if r['geneSymbol']==target]
    if not matches:return {'status':'not_scored','rank_min':None,'rank_max':None,'scored_genes':len(records)}
    score=matches[0]['combinedScore']
    return {'status':'scored','rank_min':1+sum(r['combinedScore']>score for r in records),
            'rank_max':sum(r['combinedScore']>=score for r in records),'scored_genes':len(records),
            'combined_score':score,'priority_score':matches[0].get('priorityScore'),
            'variant_score':matches[0].get('variantScore')}


def evaluate(jobs):
    results=[]
    for j in jobs:
        p=Path(j['result_jsonl'])
        result={k:j[k] for k in ['case_id','gene','stratum','arm','primary_autosomal']}
        if not p.exists():result.update(status='missing_output',rank_min=None,rank_max=None)
        else:
            try:
                records=[json.loads(line) for line in p.read_text().splitlines() if line.strip()]
                if not records:raise ValueError('Empty result file')
                result.update(rank_records(records,j['gene']))
                result['output_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
                result['top_five']=[{'gene':r['geneSymbol'],'score':r['combinedScore']} for r in sorted(records,key=lambda r:(-r['combinedScore'],r['geneSymbol']))[:5]]
            except (ValueError,KeyError,TypeError) as e:
                result.update(status='invalid_output',error=str(e),rank_min=None,rank_max=None)
        results.append(result)
    summary={}
    for arm in ('original','half_missing','swapped','none'):
        group=[r for r in results if r['arm']==arm and r['primary_autosomal']]
        summary[arm]={'denominator':len(group),'recovered':{str(k):sum(r['status']=='scored' and r['rank_max']<=k for r in group) for k in (1,5,10)},
                      'not_scored':sum(r['status']=='not_scored' for r in group),
                      'failed_or_missing':sum(r['status'] in ('missing_output','invalid_output') for r in group)}
    return {'interpretation':'Semi-synthetic source-label recovery, not clinical diagnostic accuracy. One common autosomal background. PAX4 disputed truth and both X controls excluded from primary summary but retained below.',
            'tie_policy':'Rank interval includes every exactly tied combined score; recovery uses worst tied rank.',
            'primary_autosomal':summary,'all_case_results':results}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    jobs=json.loads((a.work/'jobs-manifest.json').read_text())
    output=evaluate(jobs)
    (a.work/'evaluation.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output['primary_autosomal'],indent=2))
