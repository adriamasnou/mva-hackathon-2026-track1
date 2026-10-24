#!/usr/bin/env python3
"""Recompute descriptive published source summaries using the standard library."""
import hashlib
import json
import math
from pathlib import Path
import statistics


def values(observations, key='value'):
    result=[r[key] for r in observations]
    if not result or any(type(v) not in (int,float) or not math.isfinite(v) for v in result):
        raise ValueError('Missing/nonfinite/nonnumeric observation; no zero imputation permitted')
    return result


def analyse(data):
    upcp=[]
    for group in data['upcp']['fig5j']['groups']:
        v=values(group['observations'])
        if len(v)!=group['n'] or any(not 0<=x<=100 for x in v):
            raise ValueError('Invalid percentage data')
        upcp.append(dict(label=group['label'],n=len(v),mean_percent=statistics.mean(v)))
    survival=[]
    for group in data['upcp']['fig6i']['groups']:
        v=values(group['events'],'age_days')
        if len(v)!=group['n'] or any(r['event']!=1 for r in group['events']):
            raise ValueError('Unexpected count/censoring: uncensored median not valid')
        survival.append(dict(label=group['label'],n=len(v),median_days=sorted(v)[(len(v)-1)//2]))
    panels={}
    for name,groups in data['engineered_bubr1']['panels'].items():
        panels[name]=[]
        for group in groups:
            v=values(group['observations'])
            if len(v)!=group['n']:
                raise ValueError('Observation count changed')
            panels[name].append(dict(label=group['label'],n=len(v),median=statistics.median(v),units=group['units']))
    return dict(scope=data['scope'],upcp_aneuploidy=upcp,upcp_mutant_survival=survival,
                engineered_bubr1_panels=panels,
                published_source_discrepancies=data['engineered_bubr1']['discrepancies'],
                limitations=['Published experiments recomputed, not independently repeated.',
                             'No replicate nesting for pooled cells; no new inferential tests.',
                             'Song: nocodazole-arrest duration is not a direct SAC-silencing assay; cellular PLK1 dependence does not establish direct BubR1 T600/T608 phosphorylation.',
                             'WT mouse survival coding ambiguous; column excluded.',
                             'Published anatomical correction: esophagus/lamina propria, not aortic rescue.'])


if __name__=='__main__':
    source=Path(__file__).with_name('observations.json')
    result=analyse(json.loads(source.read_text()))
    result['observations_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    print(json.dumps(result,indent=2,allow_nan=False))
