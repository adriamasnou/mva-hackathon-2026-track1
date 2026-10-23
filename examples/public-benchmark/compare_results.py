#!/usr/bin/env python3
"""Summarize paired backgrounds and the pre-inference source-support groups."""
import argparse
import hashlib
import json
from pathlib import Path

ARMS=('original','half_missing','swapped','none')


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def recovered(row,k):return row['status']=='scored' and row['rank_max']<=k


def summarize(rows, genes):
    summary={}
    for arm in ARMS:
        group=[r for r in rows if r['arm']==arm and r['gene'] in genes]
        if len(group)!=len(genes) or len({r['gene'] for r in group})!=len(genes):
            raise ValueError('Missing or duplicated frozen group member')
        summary[arm]={'denominator':len(group),'recovered':{str(k):sum(recovered(r,k) for r in group) for k in (1,5,10)},
                      'not_scored':sum(r['status']=='not_scored' for r in group),
                      'failed_or_missing':sum(r['status'] not in ('scored','not_scored') for r in group)}
    return summary


def verified_export(path):
    receipt=json.loads((path/'export-receipt.json').read_text())
    for name in ('evaluation.json','execution.json','jobs-manifest.json'):
        if receipt['file_sha256'].get(name)!=digest(path/name):raise ValueError('Export changed: '+name)
    return json.loads((path/'evaluation.json').read_text()),json.loads((path/'execution.json').read_text())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hg002',type=Path,required=True);ap.add_argument('--hg001',type=Path,required=True)
    ap.add_argument('--groups',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();groups=json.loads(a.groups.read_text());primary=groups['primary_source_label_genes']
    data={};out={'interpretation':'Paired source-label recovery across two public backgrounds. Nine disease labels, not eighteen independent cases; no clinical accuracy estimate.',
                 'groups_sha256':digest(a.groups),'backgrounds':{},'paired_recovery_on_both':{}}
    for label,path in [('HG002',a.hg002),('HG001',a.hg001)]:
        result,execution=verified_export(path)
        addendum=execution['pre_inference_addenda']['addendum-source-support-strata-before-inference.json']['content']
        if addendum['source_groups_sha256']!=digest(a.groups):raise ValueError('Groups differ from execution addendum')
        rows=result['all_case_results'];lookup={(r['gene'],r['arm']):r for r in rows}
        if len(rows)!=48 or len(lookup)!=48:raise ValueError('Expected twelve unique cases and four arms')
        data[label]=lookup
        strata={}
        for version in ('original_pre_result_4_3_2','current_source_support_4_5'):
            members=[g for values in groups[version].values() for g in values]
            if sorted(members)!=sorted(primary):raise ValueError('Invalid source-stratum partition')
            strata[version]={name:summarize(rows,genes) for name,genes in groups[version].items()}
        out['backgrounds'][label]={'primary':summarize(rows,primary),'source_support_sensitivity':strata,
                                  'evaluation_sha256':digest(path/'evaluation.json'),'execution_sha256':digest(path/'execution.json')}
    if set(data['HG002'])!=set(data['HG001']):raise ValueError('Backgrounds have different cases')
    for arm in ARMS:
        out['paired_recovery_on_both'][arm]={'denominator':len(primary),
           'recovered':{str(k):sum(recovered(data['HG002'][g,arm],k) and recovered(data['HG001'][g,arm],k) for g in primary) for k in (1,5,10)}}
    a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['paired_recovery_on_both'],indent=2))


if __name__=='__main__':main()
