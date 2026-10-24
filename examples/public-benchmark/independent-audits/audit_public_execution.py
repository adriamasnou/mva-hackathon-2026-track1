#!/usr/bin/env python3
"""Independent read-only audit of the two frozen PUBLIC Exomiser batches.

No import of prepare/evaluate/export/compare code. Only the two assigned audit
reports are written. --inputs-only never reads raw inference outputs. A running
batch is never given a full outcome audit. Exit 0=complete/pass, 1=errors,
2=pending. --self-test exercises rejection, ties, and representation logic.
"""
import argparse
from collections import Counter, defaultdict
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'repo/examples/public-benchmark/source-selection'
PREPARED = ROOT / 'pipeline/validation-public-cases/prepared'
EXT = Path('/Volumes/easystore/MVA-public-exomiser-2512/runs')
RUNS = {
    'HG002': (ROOT / 'pipeline/work/public-validation-20261023',
              ROOT / 'pipeline/work/public-validation-cache300k-20261024'),
    'HG001': (EXT / 'public-validation-HG001-20261023',
              EXT / 'public-validation-HG001-cache300k-20261024'),
}
REPORT = ROOT / 'dossier/sweeps/evidence-2026-10-23/rubric-repair/public-execution-independent-audit'
ARMS = ('original', 'half_missing', 'swapped', 'none')
PRIMARY = {'MTOR', 'KCNJ2', 'CTCF', 'LZTR1', 'INTS11', 'BCKDHB', 'DOCK8', 'COG8', 'SLC35C1'}
LIMITS = [
    'Public synthetic spike/background ranking agreement only; no biological rescue, clinical accuracy, therapeutic benefit or competitor superiority follows.',
    'Nine primary labels retain their source qualifications. PAX4 is disputed; ZIC3/OFD1 are technical cases without an X background. No cases are replaced or dropped.',
    'Original 4/3/2 and current 4/5 source-support partitions are separate. Later visual follow-up is not retroactive pre-inference evidence.',
    'No gene or diagnosis field is supplied to inference; provenance IDs remain, and source HPO terms can themselves be disease-specific. OMIM inheritance priors and other database knowledge remain.',
    'PASS_ONLY raw output cannot establish why an absent allele disappeared. Absence after bounded representation review is not proof of a particular filter failure.',
    'An omitted per-allele whiteListed field is retained as null/unavailable, never converted into an observed false flag. Runtime bypass disabled is supported separately by the retained Loaded 0 whitelist variants log.',
    'Gene ranking is not recovery of every source allele, proof of trans phase, or independent confirmation of a published diagnosis.',
    'A true contributesToGeneScore flag means contribution under a reported inheritance mode; it does not by itself prove a joint causal configuration or biological function.',
    'Only the two completed outputs of the interrupted first attempt can be compared across JVMs. Full JSON byte reproducibility is not claimed.',
    'The cache relaunch occurred after inference began. Equality of retained scientific inputs supports an operational-only change, not a claim of external preregistration or proof of human non-inspection.',
    'Database receipt files and installed software are hashed; multi-gigabyte database payloads are not rehashed by this sidecar. Reference allele windows and FAI are checked, not the entire reference FASTA.',
    'Genotypes and all non-spike rows are compared to retained public normalized backgrounds. The GFF/exon extraction and source literature adjudications are not independently rerun here.',
]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Audit:
    def __init__(self):
        self.checks = []
        self.errors = []

    def check(self, name, operation):
        try:
            details = operation()
            self.checks.append({'check': name, 'status': 'pass', 'details': details})
            return details
        except (ValueError, TypeError, KeyError, OSError, IndexError, subprocess.SubprocessError) as exc:
            error = {'check': name, 'error': str(exc)}
            self.errors.append(error)
            self.checks.append(dict(error, status='error'))
            return None


def eligible(packet, member, excluded):
    """Re-express the written selection criteria against the original ZIP."""
    interpretations = packet.get('interpretations', [])
    if len(interpretations) != 1 or interpretations[0].get('progressStatus') != 'SOLVED':
        return None
    gis = interpretations[0].get('diagnosis', {}).get('genomicInterpretations', [])
    if len(gis) not in (1, 2):
        return None
    genes, alleles, labels, chroms = set(), set(), [], set()
    states = {'GENO:0000135': 'heterozygous', 'GENO:0000136': 'homozygous', 'GENO:0000134': 'hemizygous'}
    for gi in gis:
        v = gi.get('variantInterpretation', {}).get('variationDescriptor', {})
        gene, rec, state = v.get('geneContext', {}), v.get('vcfRecord', {}), v.get('allelicState', {})
        if gi.get('interpretationStatus') != 'CAUSATIVE' or not gene.get('symbol') or not gene.get('valueId', '').startswith('HGNC:'):
            return None
        chrom = rec.get('chrom', '').removeprefix('chr')
        try:
            pos = int(rec.get('pos', 0))
        except (ValueError, TypeError):
            return None
        ref, alt = rec.get('ref', ''), rec.get('alt', '')
        if rec.get('genomeAssembly') != 'hg38' or chrom not in {*map(str, range(1, 23)), 'X'} or pos < 1:
            return None
        if ref == alt or not all(re.fullmatch('[ACGT]{1,49}', s) for s in (ref, alt)):
            return None
        if state.get('id') not in states or states[state['id']] != state.get('label'):
            return None
        genes.add((gene['symbol'], gene['valueId']))
        alleles.add((chrom, pos, ref, alt)); chroms.add(chrom); labels.append(state['label'])
    if len(genes) != 1 or len(alleles) != len(gis) or len(chroms) != 1:
        return None
    gene = next(iter(genes))[0]
    if gene in excluded:
        return None
    sex = packet.get('subject', {}).get('sex')
    if 'X' not in chroms:
        stratum = {('heterozygous',): 'autosomal_single_heterozygous',
                   ('homozygous',): 'autosomal_homozygous',
                   ('heterozygous', 'heterozygous'): 'autosomal_two_heterozygous'}.get(tuple(labels))
    else:
        stratum = {('FEMALE', ('heterozygous',)): 'X_heterozygous_female',
                   ('MALE', ('hemizygous',)): 'X_hemizygous_male'}.get((sex, tuple(labels)))
    hpos = [set(), set()]
    for feature in packet.get('phenotypicFeatures', []):
        hp = feature.get('type', {}).get('id', '')
        if re.fullmatch(r'HP:\d{7}', hp):
            hpos[bool(feature.get('excluded', False))].add(hp)
    refs = packet.get('metaData', {}).get('externalReferences', [])
    if not stratum or len(hpos[0]) < 3 or hpos[0] & hpos[1] or not any(re.fullmatch(r'PMID:\d+', r.get('id', '')) for r in refs):
        return None
    return {'gene': gene, 'member': member, 'case_id': packet['id'], 'stratum': stratum}


def selection_check(catalog, groups):
    plan = load(SOURCE / 'selection-plan.json')
    require(catalog['selection_plan'] == plan and catalog['selection_plan_sha256'] == sha(SOURCE / 'selection-plan.json'), 'Selection plan hash/content differs')
    require(sha(SOURCE / 'frozen-cases.json') == sha(PREPARED / 'cases.json'), 'Portable and original frozen cases differ')
    archive = ROOT / 'pipeline/validation-public-cases/source/all_phenopackets-0.1.19.zip'
    require(sha(archive) == plan['archive_sha256'] and archive.stat().st_size == plan['archive_bytes'], 'Public ZIP changed')
    candidates, source_count = [], 0
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if not name.endswith('.json'):
                continue
            source_count += 1
            item = eligible(json.loads(z.read(name)), name, set(plan['excluded_genes']))
            if item:
                candidates.append(item)
        rank = lambda *parts: digest('|'.join([plan['seed'], *parts]))
        selected, used = [], set()
        for stratum, quota in plan['quotas_in_selection_order']:
            by_gene = defaultdict(list)
            for item in candidates:
                if item['stratum'] == stratum and item['gene'] not in used:
                    by_gene[item['gene']].append(item)
            for gene in sorted(by_gene, key=lambda g: (rank('gene', stratum, g), g))[:quota]:
                selected.append(min(by_gene[gene], key=lambda c: (rank('case', c['member']), c['member'])))
                used.add(gene)
        cases = catalog['cases']
        require([(s['gene'], s['member']) for s in selected] == [(c['gene'], c['source_member']) for c in cases], 'Independent ZIP selection differs')
        donors = sorted(cases, key=lambda c: (rank('donor', c['case_id']), c['case_id']))
        for i, c in enumerate(donors):
            raw = z.read(c['source_member'])
            require(hashlib.sha256(raw).hexdigest() == c['source_sha256'] == sha(SOURCE / c['local_source']), 'Source record hash differs: ' + c['gene'])
            packet = json.loads(raw)
            observed = sorted({f['type']['id'] for f in packet['phenotypicFeatures'] if not f.get('excluded', False)})
            require(c['hpo_ids'] == observed, 'Source HPO differs: ' + c['gene'])
            donor = donors[(i + 1) % len(donors)]
            expected = {'original': observed, 'none': [], 'swapped': donor['hpo_ids'],
                        'half_missing': sorted(sorted(observed, key=lambda h: (rank('drop', c['case_id'], h), h))[:(len(observed)+1)//2])}
            require(c['arms'] == expected and c['swapped_donor_case_id'] == donor['case_id'], 'Perturbation differs: ' + c['gene'])
            source_variants = []
            for gi in packet['interpretations'][0]['diagnosis']['genomicInterpretations']:
                v = gi['variantInterpretation']['variationDescriptor']; r = v['vcfRecord']
                gt = {'heterozygous': '0/1', 'homozygous': '1/1', 'hemizygous': '1'}[v['allelicState']['label']]
                source_variants.append((r['chrom'].removeprefix('chr'), int(r['pos']), r['ref'], r['alt'], gt))
            require(source_variants == [(*source_key(v), v['genotype']) for v in c['causal_variants']], 'Frozen source genotype differs: ' + c['gene'])
            require(sha(PREPARED / c['causal_only_vcf']) == c['causal_only_vcf_sha256'], 'Causal-only VCF changed: ' + c['gene'])
    require(len(cases) == len({c['case_id'] for c in cases}) == len({c['gene'] for c in cases}) == 12, 'Case cardinality')
    counts = catalog['selection_counts']
    require(source_count == counts['source_cases'] and len(candidates) == counts['eligible_cases']
            and len({c['gene'] for c in candidates}) == counts['eligible_genes']
            and dict(Counter(c['stratum'] for c in candidates)) == counts['eligible_by_stratum'], 'Independent eligibility counts differ')
    require(set(groups['primary_source_label_genes']) == PRIMARY, 'Primary membership differs')
    require(groups['frozen_inputs_manifest_sha256'] == sha(SOURCE / 'frozen-cases.json'), 'Source group input hash')
    require(groups['review']['sha256'] == sha(SOURCE / groups['review']['path']), 'Source review hash')
    for name, counts in [('original_pre_result_4_3_2', [4, 3, 2]), ('current_source_support_4_5', [4, 5])]:
        values = list(groups[name].values()); flat = [g for v in values for g in v]
        require([len(v) for v in values] == counts and len(flat) == len(set(flat)) == 9 and set(flat) == PRIMARY, 'Source group partition: ' + name)
    require({c['gene'] for c in cases} - PRIMARY == {'PAX4', 'ZIC3', 'OFD1'}, 'Separate disputed/technical cases')
    return {'source_records': source_count, 'eligible_records': len(candidates), 'eligible_genes': len({c['gene'] for c in candidates}),
            'selected': selected, 'cases': 12, 'arms_per_background': 48, 'source_variants': sum(len(c['causal_variants']) for c in cases),
            'case_manifest_sha256': sha(SOURCE / 'frozen-cases.json'), 'source_support_groups': groups}


def source_key(v):
    return (v['chrom'], int(v['pos']), v['ref'], v['alt'])


def output_key(v):
    return (v['contigName'].removeprefix('chr'), int(v['start']), v['ref'], v['alt'])


class Reference:
    def __init__(self, path):
        self.path = path
        self.index = {}
        for line in Path(str(path) + '.fai').read_text().splitlines():
            c, length, offset, bases, width, *_ = line.split('\t')
            self.index[c] = tuple(map(int, (length, offset, bases, width)))

    def get(self, chrom, start, end):
        name = chrom if chrom in self.index else 'chr' + chrom
        length, offset, bases, width = self.index[name]
        require(1 <= start <= end <= length, 'Reference bounds')
        result = bytearray()
        with self.path.open('rb') as handle:
            i = start - 1
            while i < end:
                n = min(end - i, bases - i % bases)
                handle.seek(offset + (i // bases) * width + i % bases)
                result.extend(handle.read(n)); i += n
        return result.decode().upper()


def equivalent(a, b, reference):
    """Compare resulting local haplotypes, not just stripped indel strings."""
    if a[0] != b[0] or abs(a[1] - b[1]) > 200 or len(a[3])-len(a[2]) != len(b[3])-len(b[2]):
        return False
    start = max(1, min(a[1], b[1])-2)
    end = max(a[1]+len(a[2]), b[1]+len(b[2]))+2
    window = reference.get(a[0], start, end)
    edited = []
    for _, pos, ref, alt in (a, b):
        off = pos-start
        if window[off:off+len(ref)] != ref:
            return False
        edited.append(window[:off]+alt+window[off+len(ref):])
    return edited[0] == edited[1]


def normalization_check(cases, reference):
    """Read-only normalization on stdin/stdout, never rewrite a source VCF."""
    names = [str(i) for i in range(1,23)] + ['X']
    resolved = {c:c if c in reference.index else 'chr'+c for c in names}
    lines = ['##fileformat=VCFv4.2', *['##contig=<ID='+resolved[c]+'>' for c in names],
             '##FORMAT=<ID=GT,Number=1,Type=String,Description="Public source genotype">',
             '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPUBLIC_CASE']
    original = []
    for c in cases:
        for v in c['causal_variants']:
            row = list(map(str,[resolved[v['chrom']],v['pos'],c['gene'],v['ref'],v['alt'],'.','PASS','.','GT',v['genotype']]))
            lines.append('\t'.join(row)); original.append(row)
    command = ['bcftools','norm','--no-version','-f',str(reference.path),'-c','e','-Ov','-']
    result = subprocess.run(command,input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    output = [line.split('\t') for line in result.stdout.splitlines() if line and not line.startswith('#')]
    require(Counter(tuple(r) for r in original) == Counter(tuple(r) for r in output), 'Source normalization changes allele/genotype; inspect representation before inference claims')
    return {'command':command,'input_mode':'stdin','output_mode':'stdout; source files untouched',
            'bcftools_version':subprocess.check_output(['bcftools','--version'],text=True).splitlines()[0],
            'source_alleles':len(original),'all_alleles_and_genotypes_unchanged':True,'stderr':result.stderr.strip(),
            'normalized_rows_sha256':digest('\n'.join('\t'.join(r) for r in output))}


def vcf_rows(path):
    with Path(path).open() as handle:
        for line in handle:
            if not line.startswith('#'):
                r = line.rstrip('\n').split('\t')
                require(len(r) == 10, 'Unexpected public VCF column count')
                r[0] = r[0].removeprefix('chr')
                yield r


def vcf_check(old, cases, jobs, reference):
    preparation = load(old/'preparation-receipt.json')
    public_background = Path(preparation['commands'][0][-1])
    allowed_backgrounds = {ROOT/'pipeline/work/exomiser_wgs/HG002.vcf.gz',
                           ROOT/'pipeline/work/public-validation-HG001-source/HG001.vcf.gz'}
    require(public_background in allowed_backgrounds, 'Unexpected background path: refuse unapproved inputs')
    require(sha(public_background) == preparation['background_sha256'], 'Original public background SHA256 changed')
    normalized = old / 'inputs/background-normalized.vcf'
    background = []
    for r in vcf_rows(normalized):
        require(r[0] in set(map(str, range(1, 23))), 'Unexpected non-autosomal background')
        gt = r[9].split(':')[r[8].split(':').index('GT')].replace('|', '/')
        background.append(tuple([*r[:7], '.', 'GT', gt]))
    base = Counter(background)
    checks = []
    for c in cases:
        job = next(j for j in jobs if j['case_id'] == c['case_id'])
        path = Path(job['vcf'])
        require(path == old / 'inputs' / (c['case_id']+'.vcf'), 'Unexpected VCF path: refuse unapproved inputs')
        require(sha(path) == job['vcf_sha256'], 'Input VCF hash differs: ' + c['gene'])
        loci = {(v['chrom'], str(v['pos'])) for v in c['causal_variants']}
        removed = [r for r in background if (r[0], r[1]) in loci]
        expected = base.copy()
        expected.subtract(removed)
        for v in c['causal_variants']:
            require(reference.get(v['chrom'], v['pos'], v['pos']+len(v['ref'])-1) == v['ref'], 'Source REF mismatch: ' + c['gene'])
            expected[tuple(map(str, [v['chrom'], v['pos'], '.', v['ref'], v['alt'], '.', 'PASS', '.', 'GT', v['genotype']]))] += 1
        actual = Counter(tuple(r) for r in vcf_rows(path))
        require(actual == +expected, 'Background rows/source genotype changed: ' + c['gene'])
        require(sum(actual.values()) == job['variant_records'] and job['removed_background_records'] == [list(r) for r in removed], 'Input count/collision receipt differs')
        require(len({(r[0], r[1], r[3], r[4]) for r in actual}) == sum(actual.values()), 'Duplicate allele')
        checks.append({'case_id': c['case_id'], 'gene': c['gene'], 'vcf_sha256': sha(path), 'records': sum(actual.values()),
                       'source_genotypes': [{'allele': list(source_key(v)), 'genotype': v['genotype']} for v in c['causal_variants']], 'removed_background_records': len(removed)})
    return {'public_source_path':str(public_background), 'public_source_sha256':sha(public_background),
            'normalized_background_sha256': sha(normalized), 'background_rows': len(background), 'all_non_spike_rows_and_source_genotypes_equal': True, 'cases': checks}


def jobs_check(old, new, cases, execution):
    import yaml
    before, after = load(old / 'jobs-manifest.json'), load(new / 'jobs-manifest.json')
    expected_pairs = [(c['case_id'], arm) for c in cases for arm in ARMS]
    require([(j['case_id'], j['arm']) for j in after] == expected_pairs, '48 ordered jobs differ from plan')
    require(len(before) == len(after) == 48, 'Old/new job cardinality')
    baseline = None
    template = ROOT/'repo/examples/public-case/job-template.yml'
    require(sha(template) == load(old/'preparation-receipt.json')['job_template_sha256'], 'Original public template changed')
    template_analysis = yaml.safe_load(template.read_text())['analysis']
    for a, b in zip(before, after):
        case = next(c for c in cases if c['case_id'] == b['case_id'])
        require(b['gene'] == case['gene'] and b['stratum'] == case['stratum'] and b['primary_autosomal'] == (case['gene'] in PRIMARY), 'Manifest source label/partition differs')
        require({k:v for k,v in a.items() if k not in {'job','job_sha256','result_jsonl'}} == {k:v for k,v in b.items() if k not in {'job','job_sha256','result_jsonl'}}, 'Manifest scientific content differs')
        for j, work in [(a, old), (b, new)]:
            require(Path(j['job']) == work/'jobs'/f"{j['case_id']}.{j['arm']}.yml", 'Unexpected job path')
            require(Path(j['result_jsonl']) == work/'results'/f"{j['case_id']}.{j['arm']}.jsonl", 'Unexpected result path')
            require(sha(j['job']) == j['job_sha256'], 'Job hash mismatch')
        x, y = yaml.safe_load(Path(a['job']).read_text()), yaml.safe_load(Path(b['job']).read_text())
        y_compare = copy.deepcopy(y); y_compare['outputOptions']['outputDirectory'] = x['outputOptions']['outputDirectory']
        require(x == y_compare, 'Scientific YAML changed on relaunch')
        require(set(y) == {'phenopacket', 'analysis', 'outputOptions'}, 'Unapproved job section')
        packet = y['phenopacket']
        require(set(packet) == {'id','subject','phenotypicFeatures','htsFiles','metaData'}, 'Gene/diagnosis or other unexpected phenopacket field')
        require(packet['id'] == f"{b['case_id']}.{b['arm']}", 'Unexpected identifier hint')
        require(set(packet['metaData']) == {'created','createdBy','resources','phenopacketSchemaVersion'}, 'Unexpected metadata hints')
        require(packet['metaData']['resources'] == yaml.safe_load(Path(a['job']).read_text())['phenopacket']['metaData']['resources'], 'Metadata resources changed')
        serialized = json.dumps(y,sort_keys=True)
        for source_case in cases:
            require(not re.search(r'(?<![A-Za-z0-9_])'+re.escape(source_case['gene'])+r'(?![A-Za-z0-9_])', serialized), 'Explicit selected-gene hint in YAML')
            diagnosis = source_case['source_diagnosis']
            require(all(value not in serialized for value in [diagnosis['id'],diagnosis['label']]), 'Explicit source-diagnosis hint in YAML')
        require(packet['subject'] == {'id':'PUBLIC_CASE','sex':case['sex']}, 'Subject hint/sex differs')
        require(packet['phenotypicFeatures'] == [{'type':{'id':hp}} for hp in case['arms'][b['arm']]], 'HPO arm mismatch or added annotation')
        require(packet['htsFiles'] == [{'uri':b['vcf'],'htsFormat':'VCF','genomeAssembly':'hg38'}], 'VCF route differs')
        require(y['outputOptions'] == {'outputContributingVariantsOnly':False,'numGenes':0,'outputDirectory':str(new/'results'),
                                      'outputFileName':f"{b['case_id']}.{b['arm']}",'outputFormats':['JSON','TSV_GENE']}, 'Output truncation/routing differs')
        analysis = copy.deepcopy(y['analysis'])
        require(set(analysis) == {'analysisMode','inheritanceModes','frequencySources','pathogenicitySources','steps'}, 'Unexpected analysis hint/filter')
        require(analysis['analysisMode'] == 'PASS_ONLY', 'Analysis mode differs')
        if b['arm'] == 'none':
            require(not any('hiPhivePrioritiser' in s for s in analysis['steps']), 'Phenotype present in none arm')
            analysis['steps'].append({'hiPhivePrioritiser':{}})
        if baseline is None:
            baseline = analysis
        require(analysis == baseline, 'Filters/priors differ across cases/arms')
        require(analysis == template_analysis, 'Scientific analysis differs from original hashed template')
        require([next(iter(s)) for s in analysis['steps']] == ['failedVariantFilter','variantEffectFilter','frequencyFilter','pathogenicityFilter','inheritanceFilter','omimPrioritiser','hiPhivePrioritiser'], 'Unexpected gene-list/diagnosis filter')
        require(analysis['steps'][-2:] == [{'omimPrioritiser':{}},{'hiPhivePrioritiser':{}}], 'Supplied prioritiser hints')
    require((new/'batch.txt').read_text().splitlines() == ['--analysis '+j['job'] for j in after], 'Actual batch differs')
    oldprops, newprops = (old/'runtime.properties').read_text(), (new/'runtime.properties').read_text()
    require(oldprops.count('maximumSize=60000') == 1 and oldprops.replace('maximumSize=60000','maximumSize=300000') == newprops, 'More than cache size changed')
    require('exomiser.hg38.use-clinvar-white-list=false' in newprops, 'Whitelist setting absent')
    note = load(new/'addendum-cache-only-relaunch.json')
    frozen_groups = load(new/'addendum-source-support-strata-before-inference.json')
    require(frozen_groups['source_groups'] == load(SOURCE/'source-support-groups-v3.json')
            and frozen_groups['source_groups_sha256'] == sha(SOURCE/'source-support-groups-v3.json'), 'Runtime source-support partitions differ')
    for key, p in [('prior_manifest_sha256', old/'jobs-manifest.json'), ('new_manifest_sha256', new/'jobs-manifest.json'),
                   ('prior_properties_sha256', old/'runtime.properties'), ('new_properties_sha256', new/'runtime.properties')]:
        require(note[key] == sha(p), 'Relaunch receipt changed: '+key)
    for p in [old/'protocol-before-inference.json', old/'preparation-receipt.json', *old.glob('addendum-*.json')]:
        require(sha(p) == sha(new/p.name), 'Original design/addendum changed: '+p.name)
    chronology = {'cache_relaunch_utc':note['recorded_utc'], 'source_support_freeze_utc':frozen_groups['frozen_utc'],
                  'selection_freeze_utc':load(SOURCE/'selection-plan.json')['frozen_at_utc'],
                  'scope':'Retained local timestamps, not external preregistration or proof of human non-inspection'}
    if (old/'execution.json').exists():
        prior = load(old/'execution.json')
        chronology['prior_started_utc'] = prior['started_utc']
        parse = lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
        require(parse(frozen_groups['frozen_utc']) < parse(prior['started_utc']) < parse(note['recorded_utc']), 'Frozen source groups/cache relaunch chronology differs')
    if execution:
        require(datetime.fromisoformat(note['recorded_utc']) < datetime.fromisoformat(execution['started_utc']), 'Relaunch receipt follows restart')
    if execution:
        require(execution['jobs_manifest_sha256'] == sha(new/'jobs-manifest.json'), 'Executed manifest changed')
        for j in after:
            for field in ['job', 'vcf']:
                require(execution['inputs_sha256'][j[field]] == j[field+'_sha256'], 'Executed input differs')
    return {'jobs':48, 'scientific_job_content_equal_except_output_directory':True, 'vcf_paths_and_hashes_equal':True,
            'analysis_equal_across_cases_with_prespecified_none_exception':True, 'cache_only_change':'60000 -> 300000',
            'explicit_gene_or_diagnosis_hints':False, 'provenance_ids_present':True, 'baseline_analysis':baseline, 'chronology':chronology}


def binary_check():
    libs = ROOT/'pipeline/exomiser/exomiser-cli-15.1.0/lib'
    javap = '/opt/homebrew/opt/openjdk@21/bin/javap'
    result = {}
    for jar, klass, markers in [
        ('exomiser-spring-boot-autoconfigure-15.1.0.jar','org.monarchinitiative.exomiser.autoconfigure.genome.GenomeDataSourceLoader',
         ['useClinVarWhiteList', 'Set.of:', 'VariantWhiteListReader.readVariantWhiteList', 'Set.addAll:', 'Loaded {} whitelist variants']),
        ('exomiser-core-15.1.0.jar','org.monarchinitiative.exomiser.core.writers.JsonResultsWriter', ['JsonInclude$Include.NON_DEFAULT','setDefaultPropertyInclusion']),
    ]:
        text = subprocess.check_output([javap,'-p','-c','-classpath',str(libs/jar),klass],text=True)
        require(all(marker in text for marker in markers), 'Installed runtime semantics changed: '+klass)
        result[klass] = {'jar_sha256':sha(libs/jar),'javap_sha256':digest(text),'markers':markers}
    result['interpretation'] = 'Loader log counts union of ClinVar/custom whitelist entries. JsonResultsWriter uses NON_DEFAULT omission. Raw missing per-allele whitelist fields remain null/unavailable in this audit; runtime zero-whitelist evidence is separate and is not rewritten as explicit per-allele false flags.'
    return result


def execution_check(new, ex):
    require(ex['planned_jobs'] == 48, 'Execution job count')
    for key, name in [('properties_sha256','runtime.properties'), ('batch_sha256','batch.txt'), ('jobs_manifest_sha256','jobs-manifest.json')]:
        require(ex[key] == sha(new/name), 'Execution hash mismatch: '+name)
    require(ex['properties_text'] == (new/'runtime.properties').read_text(), 'Recorded runtime property text differs')
    require('-Dspring.config.location=file:'+str(new/'runtime.properties') in ex['command'], 'Runtime did not use frozen properties')
    require(ex['command'][-2:] == ['batch', str(new/'batch.txt')], 'Runtime command mismatch')
    require(ex['wrapper_sha256'] == sha(ROOT/'repo/examples/public-benchmark/run.py'), 'Execution wrapper changed since launch')
    for group in ('design_records','pre_inference_addenda'):
        for name, record in ex[group].items():
            require(record['sha256'] == sha(new/name) and record['content'] == load(new/name), 'Design receipt differs: '+name)
    for name, h in ex['software_sha256'].items():
        p = Path(name)
        require(p.is_relative_to(ROOT/'pipeline/exomiser/exomiser-cli-15.1.0'), 'Unexpected software path')
        require(sha(p) == h, 'Installed software changed: '+name)
    for name, record in ex['data_receipts'].items():
        require(sha(name) == record['sha256'] and load(name) == record['content'], 'Database receipt differs')
    log = (new/'execution.log').read_text()
    counts = [int(n) for n in re.findall(r'Loaded (\d+) whitelist variants', log)]
    require(counts == [0], 'Runtime whitelist count not exactly zero: '+str(counts))
    started = [int(n) for n in re.findall(r'Running job (\d+) of 48', log)]
    require(started == list(range(1,len(started)+1)), 'Runtime job order/count differs')
    if ex['status'] == 'completed':
        require(ex.get('exit_code') == 0 and ex.get('missing_outputs') == [], 'Completed receipt has failures')
        require(started == list(range(1,49)), 'Not all jobs executed')
        require(sha(new/'execution.log') == ex['log_sha256'], 'Completed log hash changed')
    return {'status':ex['status'], 'started_utc':ex['started_utc'], 'finished_utc':ex.get('finished_utc'),
            'jobs_started':len(started),'runtime_whitelist_counts':counts,'software_files_hashed':len(ex['software_sha256']),
            'data_receipt_files_hashed':len(ex['data_receipts']), 'execution_receipt_sha256':sha(new/'execution.json')}


def read_raw(path):
    rows = []
    with Path(path).open() as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    require(bool(rows), 'Empty raw JSONL')
    seen = set()
    for r in rows:
        gene, score = r.get('geneSymbol'), r.get('combinedScore')
        require(isinstance(gene,str) and gene and gene not in seen, 'Missing/duplicate gene identity')
        require(not isinstance(score,bool) and isinstance(score,(int,float)) and math.isfinite(score), 'Missing/nonfinite combined score: '+gene)
        seen.add(gene)
    return rows


def ranks(rows, target):
    selected = next((r for r in rows if r['geneSymbol'] == target), None)
    if selected is None:
        return {'status':'not_scored','rank_min':None,'rank_max':None,'scored_genes':len(rows)}
    score = selected['combinedScore']
    better = sum(r['combinedScore'] > score for r in rows)
    tied = sum(r['combinedScore'] == score for r in rows)
    return {'status':'scored','rank_min':better+1,'rank_max':better+tied,'tied_genes':tied,
            'scored_genes':len(rows),'combined_score':score, 'priority_score':selected.get('priorityScore'), 'variant_score':selected.get('variantScore')}


def allele_audit(rows, case, reference):
    all_variants = [(r['geneSymbol'], v) for r in rows for v in r.get('variantEvaluations', [])]
    target = [(g,v) for g,v in all_variants if g == case['gene']]
    result = []
    for source in case['causal_variants']:
        key = source_key(source)
        matches = [(g,v,'exact') for g,v in all_variants if output_key(v) == key]
        if not matches:
            matches = [(g,v,'equivalent_local_haplotype') for g,v in all_variants if equivalent(key,output_key(v),reference)]
        detail = {'source':list(key),'input_genotype':source['genotype'],'matches':[]}
        for gene,v,kind in matches:
            detail['matches'].append({'gene':gene,'representation':kind,'output_allele':list(output_key(v)),
                'filter_status':v.get('filterStatus'), 'passed_filters':v.get('passedFilterTypes',[]), 'failed_filters':v.get('failedFilterTypes',[]),
                'contributes_to_gene_score':v.get('contributesToGeneScore'), 'white_listed':v.get('whiteListed'),
                'whitelist_flag_available':'whiteListed' in v,
                'raw_contribution_flag':v.get('contributesToGeneScore'), 'raw_whitelist_flag':v.get('whiteListed'),
                'compatible_inheritance_modes':v.get('compatibleInheritanceModes',[]),'contributing_inheritance_modes':v.get('contributingInheritanceModes',[])})
        detail['target_gene_matched'] = any(g == case['gene'] for g,_,_ in matches)
        detail['target_gene_contributing'] = any(g == case['gene'] and v.get('contributesToGeneScore',False) for g,v,_ in matches)
        if not matches:
            chrom,pos,ref,alt = key
            detail['unmatched_review'] = {'source_ref_matches_reference': reference.get(chrom,pos,pos+len(ref)-1) == ref,
                'window_start':max(1,pos-20), 'reference_window':reference.get(chrom,max(1,pos-20),pos+len(ref)+20),
                'target_gene_output_alleles':[list(output_key(v)) for _,v in target],
                'equivalence_search':'All emitted variants within 200 bases; same chromosome/length delta; REF-checked local haplotype equality.',
                'conclusion':'No exact/equivalent emitted allele found; PASS_ONLY does not preserve a reason for absence.'}
        result.append(detail)
    return result


def aggregate(results, genes):
    summary = {}
    for arm in ARMS:
        group = [r for r in results if r['gene'] in genes and r['arm'] == arm]
        require(len(group) == len(genes), 'Denominator changed')
        summary[arm] = {'denominator':len(group), 'top_k':{str(k):sum(r['status']=='scored' and r['rank_max']<=k for r in group) for k in (1,5,10)},
                        'not_scored':sum(r['status']=='not_scored' for r in group),
                        'invalid_or_missing':sum(r['status']=='invalid_or_missing' for r in group),
                        'ranked_without_all_source_alleles_contributing':[r['gene'] for r in group if r['status']=='scored' and not r['all_source_alleles_contributing']],
                        'ranked_without_any_best_mode_using_all_source_alleles':[r['gene'] for r in group if r['status']=='scored' and not r['all_source_alleles_in_any_best_mode']],
                        'ranked_with_a_best_mode_not_using_all_source_alleles':[r['gene'] for r in group if r['status']=='scored' and not r['all_source_alleles_in_every_best_mode']]}
    return summary


def mode_contributions(target, case, reference):
    modes = []
    for mode in target.get('geneScores',[]):
        contributing = [output_key(v) for v in mode.get('contributingVariants',[])]
        matched = [list(source_key(v)) for v in case['causal_variants']
                   if any(source_key(v)==key or equivalent(source_key(v),key,reference) for key in contributing)]
        modes.append({'inheritance_mode':mode['modeOfInheritance'],'combined_score':mode.get('combinedScore'),
                      'is_best_score':mode.get('combinedScore')==target['combinedScore'],
                      'contributing_source_alleles':matched,'source_allele_count':len(matched),
                      'all_source_alleles_contribute':len(matched)==len(case['causal_variants'])})
    require(any(m['is_best_score'] for m in modes),'Reported gene score has no matching best inheritance-mode score')
    return modes


def one_output_check(j, case, ex, reference):
    path = Path(j['result_jsonl']); before = sha(path)
    require(before == ex['outputs'].get(str(path)), 'Output hash mismatch/receipt missing: '+path.name)
    rows = read_raw(path)
    result = {k:j[k] for k in ['case_id','gene','arm','primary_autosomal']}
    result.update(ranks(rows,j['gene'])); result['output_sha256'] = before
    result['source_alleles'] = allele_audit(rows,case,reference)
    result['all_source_alleles_matched'] = all(v['target_gene_matched'] for v in result['source_alleles'])
    result['all_source_alleles_contributing'] = all(v['target_gene_contributing'] for v in result['source_alleles'])
    target = next((r for r in rows if r['geneSymbol']==case['gene']),None)
    reported_modes = mode_contributions(target,case,reference) if target else []
    modes = [m for m in reported_modes if m['is_best_score']]
    result['reported_score_modes'] = reported_modes
    result['best_score_modes'] = modes
    result['all_source_alleles_in_any_best_mode'] = any(m['all_source_alleles_contribute'] for m in modes)
    result['all_source_alleles_in_every_best_mode'] = bool(modes) and all(m['all_source_alleles_contribute'] for m in modes)
    variants = [v for row in rows for v in row.get('variantEvaluations',[])]
    require(all(isinstance(v[flag],bool) for v in variants for flag in ['whiteListed','contributesToGeneScore'] if flag in v), 'Invalid emitted variant boolean flag')
    result['emitted_variant_evaluations'] = len(variants)
    result['white_listed_true'] = sum(v.get('whiteListed',False) is True for v in variants)
    result['whitelist_flag_counts'] = {'explicit_true':sum(v.get('whiteListed') is True for v in variants),
        'explicit_false':sum(v.get('whiteListed') is False for v in variants),
        'unavailable':sum(v.get('whiteListed') is None for v in variants)}
    require(result['white_listed_true'] == 0, 'Whitelist bypass in emitted variant evaluations')
    # TSV_GENE is also requested by every job. The original execution wrapper
    # hashes JSONL only; independently receipt the TSV without inventing a
    # start-time or wrapper hash for it.
    tsv = path.with_name(path.stem+'.genes.tsv')
    require(tsv.exists() and tsv.stat().st_size > 0, 'Expected TSV_GENE missing/empty: '+tsv.name)
    result['tsv_gene'] = {'path':str(tsv),'sha256':sha(tsv),'receipt_scope':'Independent audit hash; execution wrapper records JSONL only'}
    require(sha(path) == before, 'Raw output changed while auditing')
    return result


def outputs_check(new, cases, groups, ex, reference, audit, sample):
    require(ex['status'] == 'completed' and ex.get('exit_code') == 0, 'Wait for completed execution receipt')
    jobs = load(new/'jobs-manifest.json')
    expected = {j['result_jsonl'] for j in jobs}
    actual = {str(p) for p in (new/'results').glob('*.jsonl')}
    audit.check(sample+' complete output membership',lambda:require(set(ex['outputs']) == expected and actual == expected,
                'Output membership differs: '+json.dumps({'missing_files':sorted(expected-actual),'extra_files':sorted(actual-expected),
                'missing_receipts':sorted(expected-set(ex['outputs'])),'extra_receipts':sorted(set(ex['outputs'])-expected)})))
    results = []
    for j in jobs:
        case = next(c for c in cases if c['case_id'] == j['case_id'])
        result = audit.check(sample+' raw '+j['case_id']+'.'+j['arm'],lambda:one_output_check(j,case,ex,reference))
        if result is None:
            result = {k:j[k] for k in ['case_id','gene','arm','primary_autosomal']}
            result.update(status='invalid_or_missing',rank_min=None,rank_max=None,scored_genes=0,
                          all_source_alleles_matched=False,all_source_alleles_contributing=False,source_alleles=[],
                          best_score_modes=[],all_source_alleles_in_any_best_mode=False,all_source_alleles_in_every_best_mode=False)
        results.append(result)
    partitions = {'primary_nine':PRIMARY,'disputed_PAX4':{'PAX4'},'X_technical':{'ZIC3','OFD1'}}
    for label in ['original_pre_result_4_3_2','current_source_support_4_5']:
        partitions.update({label+'/'+name:set(genes) for name,genes in groups[label].items()})
    evaluated = new/'evaluation.json'
    comparison = {'status':'not_yet_available'}
    if evaluated.exists() and all(r['status'] != 'invalid_or_missing' for r in results):
        external = load(evaluated)
        other = {(r['case_id'],r['arm']):r for r in external['all_case_results']}
        require(set(other) == {(r['case_id'],r['arm']) for r in results}, 'Evaluator job membership differs')
        for r in results:
            o = other[(r['case_id'],r['arm'])]
            require(all(r[k] == o.get(k) for k in ['status','rank_min','rank_max','scored_genes','output_sha256']), 'Independent rank differs from evaluator: '+r['case_id']+'.'+r['arm'])
        for arm, summary in aggregate(results,PRIMARY).items():
            require(external['primary_autosomal'][arm]['denominator'] == summary['denominator'] and external['primary_autosomal'][arm]['recovered'] == summary['top_k'], 'Evaluator aggregate differs')
        comparison = {'status':'all48_ranks_and_primary_denominators_agree','evaluation_sha256':sha(evaluated)}
    allele_observations = [(r,v) for r in results for v in r['source_alleles']]
    return {'status':'completed','jobs':len(results), 'raw_gene_rows':sum(r['scored_genes'] for r in results),
            'emitted_variant_evaluations':sum(r.get('emitted_variant_evaluations',0) for r in results),
            'white_listed_true':sum(r.get('white_listed_true',0) for r in results),
            'whitelist_flag_counts':{key:sum(r.get('whitelist_flag_counts',{}).get(key,0) for r in results) for key in ['explicit_true','explicit_false','unavailable']},
            'source_allele_summary':{'observations':len(allele_observations),
                'exact_target_gene_matches':sum(any(m['representation']=='exact' and m['gene']==r['gene'] for m in v['matches']) for r,v in allele_observations),
                'target_gene_unmatched':sum(not v['target_gene_matched'] for _,v in allele_observations),
                'target_gene_contributing':sum(v['target_gene_contributing'] for _,v in allele_observations)},
            'groups':{name:aggregate(results,genes) for name,genes in partitions.items()},'all_case_results':results,'evaluator_crosscheck':comparison}


def canon(value):
    if isinstance(value,dict):
        return {k:canon(v) for k,v in value.items()}
    if isinstance(value,list):
        return sorted((canon(v) for v in value),key=lambda x:json.dumps(x,sort_keys=True))
    return value


def cross_case_check(old, new, cases):
    """Check the fixed source-allele panel for cross-case carryover in outputs."""
    source_keys = {source_key(v) for c in cases for v in c['causal_variants']}
    background_keys = set()
    for row in vcf_rows(old/'inputs/background-normalized.vcf'):
        key = (row[0],int(row[1]),row[3],row[4])
        if key in source_keys:
            background_keys.add(key)
    checks, original_gene_sets = [], []
    for job in load(new/'jobs-manifest.json'):
        case = next(c for c in cases if c['case_id'] == job['case_id'])
        rows = read_raw(job['result_jsonl'])
        if job['arm'] == 'original':
            original_gene_sets.append({r['geneSymbol'] for r in rows})
        found = {output_key(v) for row in rows for v in row.get('variantEvaluations', [])} & source_keys
        own = {source_key(v) for v in case['causal_variants']}
        unexpected = found - own - background_keys
        require(not unexpected, 'Source alleles from another case: '+job['case_id']+'.'+job['arm']+' '+repr(unexpected))
        checks.append({'case_id':job['case_id'],'arm':job['arm'],'expected_own_source_alleles':len(own),
                       'observed_own_source_alleles':len(found & own),'unexpected_other_case_source_alleles':len(unexpected)})
    return {'jobs':len(checks),'source_alleles_in_unspiked_background':[list(k) for k in sorted(background_keys)],
            'unexpected_other_case_source_alleles':0,'common_genes_across_original_arms':len(set.intersection(*original_gene_sets)),
            'union_genes_across_original_arms':len(set.union(*original_gene_sets)), 'all_case_checks':checks,
            'scope':'Only the 14 frozen source alleles; not an assertion that all conceivable forms of contamination are excluded.'}


def repeats_check(old, new, ex):
    previous = load(old/'execution.json')
    note = load(new/'addendum-cache-only-relaunch.json')
    require(note['prior_execution_sha256'] == sha(old/'execution.json') and note['prior_completed_output_hashes'] == previous['outputs'], 'Prior receipt changed')
    require(len(previous['outputs']) == 2 and previous['status'] == 'failed', 'Interrupted first attempt shape changed')
    comparisons = []
    for oldpath, expected in previous['outputs'].items():
        a_path, b_path = Path(oldpath), new/'results'/Path(oldpath).name
        require(sha(a_path) == expected and sha(b_path) == ex['outputs'][str(b_path)], 'Repeat output hash differs from receipt')
        a, b = ({r['geneSymbol']:r for r in read_raw(p)} for p in (a_path,b_path))
        require(a.keys() == b.keys(), 'Repeat gene membership differs')
        scores = {k:sum(a[g].get(k) == b[g].get(k) for g in a) for k in ['combinedScore','priorityScore','variantScore']}
        variant_equal = sum(canon(a[g].get('variantEvaluations')) == canon(b[g].get('variantEvaluations')) for g in a)
        require(all(v == len(a) for v in scores.values()) and variant_equal == len(a), 'Repeat ranking scores/variants differ')
        comparisons.append({'file':a_path.name,'genes':len(a),'old_sha256':expected,'new_sha256':sha(b_path),'byte_equal':expected==sha(b_path),
                            'equal_score_counts':scores,'equal_variant_evaluation_gene_counts':variant_equal,
                            'changed_p_values':sum(a[g].get('pValue') != b[g].get('pValue') for g in a),
                            'changed_phenotype_model_evidence':sum(canon(a[g].get('priorityResults')) != canon(b[g].get('priorityResults')) for g in a)})
    return {'prior_status':previous['status'],'prior_exit_code':previous.get('exit_code'),'comparisons':comparisons,
            'scope':'All two completed prior outputs; exact ranking-score agreement, not full JSON byte reproducibility; no causal explanation of phenotype-model differences asserted.'}


def self_test():
    import tempfile
    passed = []
    base = [{'geneSymbol':'A','combinedScore':.8},{'geneSymbol':'B','combinedScore':.8},{'geneSymbol':'C','combinedScore':.9}]
    require(ranks(base,'A')['rank_min'] == 2 and ranks(base,'A')['rank_max'] == 3, 'Tie arithmetic')
    passed.append('ties use rank2..3, not alphabetic rank2')
    require(ranks(base,'D')['status'] == 'not_scored', 'Absent target')
    passed.append('absent target retained')
    # No fixture files persist; temporary files are outside all inputs/results.
    with tempfile.TemporaryDirectory(prefix='mva-public-audit-test-') as tmp:
        p = Path(tmp)/'raw.jsonl'
        for label, rows in [('duplicate',base+[base[0]]), ('missing score',[{'geneSymbol':'A'}]),
                            ('boolean',[{'geneSymbol':'A','combinedScore':True}]),('nan',[{'geneSymbol':'A','combinedScore':float('nan')}]),
                            ('inf',[{'geneSymbol':'A','combinedScore':float('inf')}]),('empty',[]),('empty gene',[{'geneSymbol':'','combinedScore':1}])]:
            p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            try:
                read_raw(p)
            except ValueError:
                passed.append('reject '+label)
            else:
                raise ValueError('Self-test accepted '+label)
        p.write_text(''.join(json.dumps(r)+'\n' for r in base))
        require(read_raw(p)==base,'Valid file rejected');passed.append('accept valid file')
    class TinyReference:
        def get(self, chrom, start, end):
            return 'CCAAAAAGGGGG'[start-1:end]
    require(equivalent(('1',3,'AA','A'),('1',4,'AA','A'),TinyReference()),'Repeat-shift equivalence')
    require(not equivalent(('1',3,'AA','A'),('1',4,'AA','G'),TinyReference()),'False representation match')
    passed.extend(['repeat-shift indel equivalence','reject different edited haplotype'])
    case = {'causal_variants':[{'chrom':'1','pos':3,'ref':'A','alt':'G'}, {'chrom':'1','pos':4,'ref':'A','alt':'T'}]}
    variants = [{'contigName':v['chrom'],'start':v['pos'],'ref':v['ref'],'alt':v['alt']} for v in case['causal_variants']]
    target = {'combinedScore':.8,'geneScores':[
        {'modeOfInheritance':'AUTOSOMAL_DOMINANT','combinedScore':.8,'contributingVariants':variants[:1]},
        {'modeOfInheritance':'AUTOSOMAL_RECESSIVE','combinedScore':.7,'contributingVariants':variants}]}
    modes = mode_contributions(target,case,TinyReference())
    require(not any(m['is_best_score'] and m['all_source_alleles_contribute'] for m in modes), 'Global contribution mistaken for best-mode joint contribution')
    passed.append('best score using one allele differs from lower-scoring mode using both')
    target['geneScores'][1]['combinedScore'] = .8
    best = [m for m in mode_contributions(target,case,TinyReference()) if m['is_best_score']]
    require(any(m['all_source_alleles_contribute'] for m in best) and not all(m['all_source_alleles_contribute'] for m in best), 'Tied best modes collapsed')
    passed.append('retain tied best modes with different source-allele membership')
    return {'passed':len(passed),'checks':passed}


def render(report):
    lines = ['# Independent public execution audit', '', 'Status: **'+report['status']+'**. Recorded '+report['recorded_utc']+'.', '',
             'This sidecar reads frozen public inputs and raw JSONL, recomputes ranks by direct arithmetic, and does not import the public evaluator/exporter. Shared gates, inference inputs and execution are untouched.', '',
             f"Checks: {sum(c['status']=='pass' for c in report['checks'])} passed; {len(report['errors'])} errors. Full outcome audit is recorded only for a completed execution receipt.", '']
    for name, run in report['runs'].items():
        lines += [f"## {name}", '', 'Execution: '+run['execution_status']+'.', '']
        outcome = run.get('outcomes')
        if outcome:
            valid = sum(r['status'] != 'invalid_or_missing' for r in outcome['all_case_results'])
            flags = outcome['whitelist_flag_counts']
            lines += [f"Checked {outcome['jobs']} expected jobs; {valid} passed raw-output validation. The accepted files contain {outcome['raw_gene_rows']} gene rows with unique per-job identities and finite combined scores. Per-allele whitelist fields: {flags['explicit_true']} explicit true, {flags['explicit_false']} explicit false, {flags['unavailable']} unavailable. Unavailable fields remain null; runtime zero-whitelist evidence is separate.", '']
            if (run.get('runtime') or {}).get('runtime_whitelist_counts') == [0]:
                lines += ['The retained execution log reports `Loaded 0 whitelist variants`; the recorded properties disable the ClinVar whitelist. This is runtime evidence, not an observed false flag on each allele.', '']
            alleles = outcome['source_allele_summary']
            lines += [f"Across all four arms, {alleles['exact_target_gene_matches']} of {alleles['observations']} source-allele observations match the target gene exactly; {alleles['target_gene_contributing']} are marked contributing under at least one reported mode and {alleles['target_gene_unmatched']} are unmatched. This does not mean all source alleles jointly determine the best gene score; that is audited separately below. Gene rank remains distinct from allele recovery and phase.", '']
            for arm, s in outcome['groups']['primary_nine'].items():
                lines.append(f"- {arm}: conservative top-1/5/10 = {s['top_k']['1']}/{s['top_k']['5']}/{s['top_k']['10']} of {s['denominator']}; not scored {s['not_scored']}.")
            lines += ['', 'All twelve case rows, both source-support partitions, allele flags and exact hashes are retained in the companion JSON.', '']
            exceptions = [r for r in outcome['all_case_results'] if r['status']=='scored' and not r['all_source_alleles_in_every_best_mode']]
            for r in exceptions:
                detail = '; '.join(m['inheritance_mode']+': '+str(m['source_allele_count'])+'/'+str(len(r['source_alleles']))+' source alleles' for m in r['best_score_modes'])
                lines.append(f"- {r['gene']} / {r['arm']}: rank {r['rank_min']}–{r['rank_max']}; best-scoring modes use {detail}. A gene can rank without both source alleles determining that score, even when both have a global contribution flag.")
            lines.append('')
        else:
            lines += ['Outcome audit pending; no incomplete raw output is represented as a finished benchmark.', '']
    if report.get('repeat_attempts'):
        lines += ['## Interrupted attempt and relaunch', '', 'All completed prior outputs were retained and compared; the first attempt remains interrupted after two outputs. Scientific YAML is unchanged except output directory; input VCF paths/hashes are unchanged; properties differ only in bounded cache size 60000 → 300000.', '']
        for c in report['repeat_attempts']['comparisons']:
            lines.append(f"- {c['file']}: {c['genes']} gene rows, all three ranking-score fields equal; changed p-values {c['changed_p_values']}; changed reported phenotype-model evidence {c['changed_phenotype_model_evidence']}; byte equality {c['byte_equal']}.")
        lines.append('')
    lines += ['## Errors and pending checks', '']
    lines += ['- '+e['check']+': '+e['error'] for e in report['errors']] or ['- No errors detected in executed checks.']
    if report['status'] != 'complete_pass':
        lines.append('- A complete clean outcome audit is not established until all runs and required checks pass.')
    lines += ['', '## Limits and unsupported claims', ''] + ['- '+s for s in LIMITS]
    lines += ['', '## Changed paths and reproduction', '',
              '- `pipeline/public_validation/audit_public_execution.py`',
              '- `dossier/sweeps/evidence-2026-10-23/rubric-repair/public-execution-independent-audit.md`',
              '- `dossier/sweeps/evidence-2026-10-23/rubric-repair/public-execution-independent-audit.json`', '',
              'Run `python3 pipeline/public_validation/audit_public_execution.py --self-test` for bounded negative controls; run without flags after completion for the full audit. `--inputs-only` audits inputs without reading inference outputs. Exit 2 means pending, not success. No commits, push, submission, contact, shared gates, or gated patient-data access are performed.', '']
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs-only',action='store_true')
    ap.add_argument('--self-test',action='store_true')
    args = ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test(),indent=2));return 0
    audit = Audit()
    catalog, groups = load(SOURCE/'frozen-cases.json'), load(SOURCE/'source-support-groups-v3.json')
    cases = catalog['cases']
    reference = Reference(ROOT/'pipeline/ref/GRCh38_no_alt_plus_hs38d1.fna')
    report = {'schema_version':'1.0','recorded_utc':datetime.now(timezone.utc).isoformat(), 'auditor_sha256':sha(__file__),
              'mode':'inputs_only' if args.inputs_only else 'complete_outputs_when_available', 'runs':{},'limits':LIMITS,
              'reference':{'path':str(reference.path),'fai_sha256':sha(str(reference.path)+'.fai'),'whole_fasta_hashed':False}}
    report['self_tests'] = audit.check('validator negative controls',self_test)
    report['selection'] = audit.check('original plan/ZIP/arms/source groups',lambda:selection_check(catalog,groups))
    report['runtime_code'] = audit.check('installed whitelist loader and JSON default semantics',binary_check)
    report['source_normalization'] = audit.check('all14 public source alleles/reference normalization',lambda:normalization_check(cases,reference))
    for sample,(old,new) in RUNS.items():
        ex = load(new/'execution.json') if (new/'execution.json').exists() else None
        run = {'work':str(new),'execution_status':ex['status'] if ex else 'not_started'}
        report['runs'][sample] = run
        run['jobs'] = audit.check(sample+' all48 jobs/cache-only equality/no hints',lambda:jobs_check(old,new,cases,ex))
        run['vcfs'] = audit.check(sample+' source VCF hashes/genotypes/background equality',lambda:vcf_check(old,cases,load(new/'jobs-manifest.json'),reference))
        if ex:
            run['runtime'] = audit.check(sample+' actual execution receipt/whitelist/software',lambda:execution_check(new,ex))
            if ex['status'] not in ('running','completed'):
                audit.check(sample+' execution success',lambda:require(False,'Execution failed; full audit cannot pass'))
            if ex['status'] == 'completed' and not args.inputs_only:
                run['outcomes'] = audit.check(sample+' completed raw outputs/ranks/allele review',lambda:outputs_check(new,cases,groups,ex,reference,audit,sample))
                run['cross_case_source_check'] = audit.check(sample+' source-allele cross-case carryover',lambda:cross_case_check(old,new,cases))
                if sample == 'HG002':
                    report['repeat_attempts'] = audit.check('all completed interrupted-attempt outputs vs relaunch',lambda:repeats_check(old,new,ex))
    report['checks'],report['errors'] = audit.checks,audit.errors
    complete = all(r.get('outcomes') for r in report['runs'].values())
    report['status'] = 'errors' if audit.errors else 'complete_pass' if complete else 'pending_outputs'
    REPORT.with_suffix('.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    REPORT.with_suffix('.md').write_text(render(report))
    print(json.dumps({'status':report['status'],'checks':len(audit.checks),'errors':audit.errors,
                      'runs':{k:v['execution_status'] for k,v in report['runs'].items()}},indent=2))
    return 1 if audit.errors else 0 if complete else 2


if __name__ == '__main__':
    raise SystemExit(main())
