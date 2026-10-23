#!/usr/bin/env python3
"""Write a reconstructed public smoke-test input/job. Does not execute Exomiser."""
import argparse,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def prepare(out):
    with (ROOT/'clinvar-smoke-variants.tsv').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    if len(rows)!=126 or len({(r['chrom'],r['pos'],r['ref'],r['alt']) for r in rows})!=126:
        raise ValueError('Public fixture count or uniqueness check failed')
    if any(r['genotype']!='0/1' for r in rows):raise ValueError('Unexpected synthetic genotype')
    out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    vcf=out/'public-smoke.vcf';job=out/'reconstructed-job.yml'
    if vcf.exists() or job.exists():raise FileExistsError('Choose a new output directory; existing inputs will not be overwritten')
    lines=['##fileformat=VCFv4.2','##source=Public_ClinVar_subset_synthetic_heterozygous_genotypes']
    lines += [f'##contig=<ID={c}>' for c in sorted({r['chrom'] for r in rows},key=int)]
    lines += ['##FORMAT=<ID=GT,Number=1,Type=String,Description="Synthetic genotype">','#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tsmoke']
    lines += ['\t'.join([r['chrom'],r['pos'],'.',r['ref'],r['alt'],'100','PASS','.','GT',r['genotype']]) for r in rows]
    vcf.write_text('\n'.join(lines)+'\n')
    template=(ROOT/'job-template.yml').read_text().replace('__VCF__',json.dumps(str(vcf)))
    template=template.replace('outputOptions:','outputOptions:\n  outputDirectory: '+json.dumps(str(out)))
    job.write_text(template);return vcf,job
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out-dir',type=Path,required=True);a=p.parse_args()
    for x in prepare(a.out_dir):print(x)
