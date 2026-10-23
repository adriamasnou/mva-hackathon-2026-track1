#!/usr/bin/env python3
"""Prepare frozen, public semi-synthetic Exomiser cases; never execute inference.

Requires bcftools and PyYAML. Inputs are a public GIAB VCF, Ensembl GFF3,
and a separately frozen Phenopacket Store selection. No MVA input is accepted
by this project's invocation. Full provenance and commands are retained.
"""
import argparse
import collections
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ARMS = ('original', 'half_missing', 'swapped', 'none')


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')


def merged_exons(path):
    intervals = collections.defaultdict(list)
    n = 0
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            cols = line.rstrip().split('\t')
            if cols[0] in {str(i) for i in range(1,23)} and cols[2] == 'exon':
                intervals[cols[0]].append((max(0, int(cols[3])-1-20), int(cols[4])+20))
                n += 1
    if not n:
        raise ValueError('No canonical autosomal exons: refuse empty background')
    merged = []
    for chrom in sorted(intervals, key=int):
        result = []
        for start, end in sorted(intervals[chrom]):
            if result and start <= result[-1][1]:
                result[-1][1] = max(result[-1][1], end)
            else:
                result.append([start, end])
        merged.extend((chrom, start, end) for start, end in result)
    return merged, n


def coordinate(row):
    return (23 if row[0] == 'X' else int(row[0]), int(row[1]), row[3], row[4])


def spike_rows(rows, variants):
    # Keep a changed locus from becoming two conflicting records. Disclose every
    # removed background row, including alternate alleles at the same position.
    loci = {(v['chrom'], int(v['pos'])) for v in variants}
    removed = [r for r in rows if (r[0], int(r[1])) in loci]
    result = [r for r in rows if (r[0], int(r[1])) not in loci]
    for v in variants:
        result.append([v['chrom'], str(v['pos']), '.', v['ref'], v['alt'], '.',
                       'PASS', '.', 'GT', v['genotype']])
    result.sort(key=coordinate)
    if len({(r[0],r[1],r[3],r[4]) for r in result}) != len(result):
        raise ValueError('Duplicate allele after spike: fix preparation before inference')
    return result, removed


def make_job(template, case, arm, vcf, outdir, label):
    job = copy.deepcopy(template)
    packet = job['phenopacket']
    packet['id'] = label
    packet['subject'] = {'id': 'PUBLIC_CASE', 'sex': case['sex']}
    packet['phenotypicFeatures'] = [{'type': {'id': h}} for h in case['arms'][arm]]
    packet['htsFiles'] = [{'uri': str(vcf), 'htsFormat': 'VCF', 'genomeAssembly': 'hg38'}]
    packet['metaData']['created'] = datetime.now(timezone.utc).isoformat()
    packet['metaData']['createdBy'] = 'adriamasnou-public-benchmark'
    # Preserve supplied HPO identifiers; do not imply the old example's 2019
    # ontology generated these cases. The executable ontology is pinned below.
    packet['metaData']['resources'][0]['version'] = 'Exomiser-2512-bundled-HPO'
    if arm == 'none':
        job['analysis']['steps'] = [s for s in job['analysis']['steps'] if 'hiPhivePrioritiser' not in s]
    job['outputOptions'] = {'outputContributingVariantsOnly': False, 'numGenes': 0,
                            'outputDirectory': str(outdir), 'outputFileName': label,
                            'outputFormats': ['JSON', 'TSV_GENE']}
    return job


def prepare(args):
    import yaml  # Heavy-runtime preparation only; lightweight unit tests use stdlib.
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out/'inputs').mkdir(); (out/'jobs').mkdir(); (out/'results').mkdir()
    cases = json.loads(args.cases.read_text())
    template = yaml.safe_load(args.template.read_text())
    if len(cases['cases']) != 12 or len({c['gene'] for c in cases['cases']}) != 12:
        raise ValueError('Expected frozen 12-case, 12-gene selection')
    protocol = {
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'results_seen': False,
        'case_manifest_sha256': sha(args.cases), 'background_sha256': sha(args.background),
        'gff_sha256': sha(args.gff), 'job_template_sha256': sha(args.template),
        'background_rule': 'All canonical autosomal Ensembl 116 exons, any transcript/biotype, plus 20 bp flanks; merge overlapping/bookended BED intervals; bcftools view -R --regions-overlap 1. No gene/score selection.',
        'spike_rule': 'Replace any background record at each source causal position, then add source allele/genotype unphased. Record collisions. Normalise multiallelic records with bcftools norm -m -any before merging. Preserve all other observed autosomal genotypes.',
        'analysis_rule': 'Reconstructed 15.1.0 exome template unchanged across cases. Same variant sources/filters and inheritance modes. Original/half/swapped differ only in HPO list. None removes hiPhivePrioritiser and supplies no HPO; OMIM inheritance prior remains.',
        'outcomes': 'Primary: source-designated causal gene rank and top-1/5/10 over nine provisional autosomal source-label comparators, failures count as not recovered. PAX4 is separately reported as disputed truth after pre-result primary-source adjudication; its paper calls the variant VUS. Report both minimum and maximum tied rank; success uses conservative maximum rank. Keep all twelve cases and all four arms visible. Two X cases reported separately because background lacks X; ZIC3 also has unresolved source-phenotype conflict.',
        'limits': ['One common public autosomal background, synthetic combinations, not independent patient genomes.',
                   'Source-curated SOLVED labels are not independently adjudicated clinical diagnoses.',
                   'Knowledge leakage possible; no novel-gene or clinical sensitivity claim.',
                   'X background absent: two X cases are limited technical controls, not X-linked validation.',
                   'A result failure or filtered causal gene remains in denominator; no post-result replacement.',
                   'Causal gene ranking does not confirm every causal allele, phase, drug response or patient benefit.'],
        'commands': [], 'tool_version': subprocess.check_output(['bcftools','--version'],text=True).splitlines()[0]
    }
    dump(out/'protocol-before-inference.json',protocol)
    intervals,n = merged_exons(args.gff)
    bed=out/'inputs'/'all-autosomal-exons-plus20.bed'
    bed.write_text(''.join(f'chr{c}\t{s}\t{e}\n' for c,s,e in intervals))
    bcf=out/'inputs'/'background-exonic.bcf'
    commands=[['bcftools','view','--no-version','-R',str(bed),'--regions-overlap','1','-Ob','-o',str(bcf),str(args.background.resolve())],
              ['bcftools','norm','--no-version','-m','-any','-Ov','-o',str(out/'inputs'/'background-normalized.vcf'),str(bcf)]]
    for command in commands:
        subprocess.run(command,check=True)
    rows=[];background_sample=None
    for line in (out/'inputs'/'background-normalized.vcf').read_text().splitlines():
        if line.startswith('#CHROM'):
            columns=line.split('\t')
            if len(columns)!=10: raise ValueError('Exactly one public background sample required')
            background_sample=columns[9]
        if line.startswith('#'): continue
        r=line.split('\t'); r[0]=r[0].removeprefix('chr')
        gt=r[9].split(':')[r[8].split(':').index('GT')].replace('|','/')
        if not all(x in ('0','1') for x in gt.split('/')):
            raise ValueError(f'Unexpected normalized GT {gt}')
        rows.append([*r[:5],r[5],r[6],'.','GT',gt])
    if len(rows)<10000: raise ValueError('Unexpectedly sparse exonic background')
    if background_sample not in ('HG001','HG002'):
        raise ValueError('Expected the explicitly permitted public HG001/HG002 background')
    job_records=[]
    for case in cases['cases']:
        label=case['case_id']
        result,removed=spike_rows(rows,case['causal_variants'])
        vcf=out/'inputs'/f'{label}.vcf'
        header=['##fileformat=VCFv4.2','##reference=GRCh38',
                f'##source=Public_{background_sample}_autosomal_exons_plus_PhenopacketStore_causal_variants',
                *[f'##contig=<ID={c}>' for c in [*map(str,range(1,23)),'X']],
                '##FORMAT=<ID=GT,Number=1,Type=String,Description="Synthetic combination; phase unasserted">',
                '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPUBLIC_CASE']
        vcf.write_text('\n'.join(header+['\t'.join(r) for r in result])+'\n')
        for arm in ARMS:
            name=f'{label}.{arm}'
            jobpath=out/'jobs'/f'{name}.yml'
            jobpath.write_text(yaml.safe_dump(make_job(template,case,arm,vcf,out/'results',name),sort_keys=False))
            job_records.append({'case_id':label,'gene':case['gene'],'stratum':case['stratum'],
                                'arm':arm,'primary_autosomal':case['stratum'].startswith('autosomal_') and case['gene'] != 'PAX4',
                                'vcf':str(vcf),'vcf_sha256':sha(vcf),'variant_records':len(result),
                                'removed_background_records':removed,'job':str(jobpath),'job_sha256':sha(jobpath),
                                'result_jsonl':str(out/'results'/f'{name}.jsonl')})
    protocol['commands']=commands
    protocol['gff_exon_records']=n;protocol['merged_intervals']=len(intervals)
    protocol['background_exonic_records']=len(rows)
    protocol['background_sample']=background_sample
    dump(out/'preparation-receipt.json',protocol)
    dump(out/'jobs-manifest.json',job_records)
    (out/'batch.txt').write_text(''.join('analyse --analysis '+json.dumps(j['job'])+'\n' for j in job_records))
    print(json.dumps({'jobs':len(job_records),'background_records':len(rows),'out':str(out)}))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('cases','background','gff','template','out'):
        ap.add_argument('--'+key,type=Path,required=True)
    prepare(ap.parse_args())
