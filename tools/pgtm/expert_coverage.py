#!/usr/bin/env python3
"""Reproduce a narrowly defined expert-assertion coverage proxy; not clinical classification."""
import argparse,csv,datetime,gzip,hashlib,json
from pathlib import Path

def compute(bulk,crosswalk):
    genes=set(); n=0
    with gzip.open(bulk,'rt',encoding='utf8') as f:
        reader=csv.DictReader(f,delimiter='\t')
        if not {'GeneSymbol','ReviewStatus'} <= set(reader.fieldnames or []):
            raise ValueError('ClinVar schema missing GeneSymbol / ReviewStatus')
        for r in reader:
            n+=1
            if r['ReviewStatus'].strip().lower() in {'reviewed by expert panel','practice guideline'}:
                genes.update(g.strip() for g in r['GeneSymbol'].split(';') if g.strip() and g.strip()!='-')
    with crosswalk.open() as f:
        reader=csv.DictReader(f)
        if not {'n_genes','genes'} <= set(reader.fieldnames or []):
            raise ValueError('Crosswalk schema missing n_genes / genes')
        rows=list(reader)
    if not n or not genes or not rows:
        raise ValueError('Empty source or zero expert genes: not a valid absence result')
    mapped=[r for r in rows if int(r['n_genes'])>0]
    if not mapped:
        raise ValueError('No mapped rows: coverage is unassessed, not zero')
    uncovered=[r for r in mapped if not(set(r['genes'].split(';')) & genes)]
    return dict(all_rows=len(rows),mapped_rows=len(mapped),unassessed_rows=len(rows)-len(mapped),
        expert_genes_global=len(genes),rows_without_qualifying_assertion=len(uncovered),
        fraction_of_mapped=len(uncovered)/len(mapped),fraction_of_all=len(uncovered)/len(rows))

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--clinvar',type=Path,required=True);p.add_argument('--crosswalk',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=compute(a.clinvar,a.crosswalk)
    result['sources']=[dict(file=x.name,sha256=digest(x),local_file_mtime_utc=datetime.datetime.fromtimestamp(x.stat().st_mtime,datetime.timezone.utc).isoformat()) for x in [a.clinvar,a.crosswalk]]
    result['interpretation']='Snapshot proxy: absence of a qualifying ClinVar record is not absence of clinical expertise, eligibility or safety.'
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
