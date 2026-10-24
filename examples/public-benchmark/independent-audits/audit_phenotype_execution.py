#!/usr/bin/env python3
"""Independently audit the frozen public phenotype-only execution.

No imports of run_phenotype, evaluator, exporter, or the genomic auditor.
Read-only inputs; writes only the two assigned phenotype audit reports.
Ranks use Decimal arithmetic on the reported TSV phenotype-score precision.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import csv

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'repo/examples/public-benchmark/source-selection'
OLD = ROOT / 'pipeline/work/public-validation-20261023/phenotype-only'
WORK = ROOT / 'pipeline/work/public-phenotype-hg38-20261024'
EXPORT = ROOT / 'repo/examples/public-benchmark/results/phenotype-only'
REPORT = ROOT / 'dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit'
FIRST_PASS = REPORT.parent / 'phenotype-independent-audit-first-pass'
PRIMARY = {'MTOR', 'KCNJ2', 'CTCF', 'LZTR1', 'INTS11', 'BCKDHB', 'DOCK8', 'COG8', 'SLC35C1'}
LIMITS = [
    'Knowledge-only source-label recovery, not genomic or clinical validation. No biological benefit or competitor superiority is inferred.',
    'The phenotype score uses existing human/model-organism/PPI knowledge. OMIM and hiPhive remain enabled; global knowledge is not disabled.',
    'Runtime loaded 287098 whitelist variants. With no VCF, no input alleles and zero filtered variants, this whitelist cannot bypass filtering of input alleles. This is not a claim that ClinVar/global knowledge was disabled.',
    'Ranks use the maximum reported phenotype score per unique gene and conservative worst ties at four-decimal TSV precision. These are not necessarily ties at internal full precision; TSV #RANK and combined-score columns are not the endpoint.',
    'This comparator scores 19192 unique gene-symbol records per case, representing 19116 distinct nonzero Entrez IDs. There are 57 shared-ID groups spanning 133 symbols. The frozen endpoint is symbol-based; shared identifiers do not establish biological synonymy or 19192 independent gene identities.',
    'Its search space differs from the filtered genomic arms; rank differences are not an isolated effect-size estimate for adding a VCF. Entrez-collapsed sensitivity is diagnostic only and does not replace the frozen symbol endpoint.',
    'Nine primary source labels retain their source qualifications; PAX4 remains disputed and ZIC3/OFD1 are separate controls. No new independent disease cases are created by another comparator.',
    'The original comparator was frozen before genomic outputs. Its native hg38 wrapper was repaired later, after genomic outcomes were known, with no phenotype outputs from the failed attempt. No external preregistration or proof of human non-inspection is claimed.',
    'Execution/script/software and extraction-receipt hashes are checked; multi-gigabyte database payloads and the Java executable are not rehashed. Native wrapper behavior is supported by exact input comparison and runtime logs, not a fresh Java bytecode review here.',
    'No repeat phenotype execution was requested; full JSON/TSV byte reproducibility across JVMs is not established.',
    'Phenotype-only ranks make no allele-recovery or phase claim. The earlier genomic COG8/SLC35C1 No-HPO best-mode limitation remains: one of two source alleles determines the best mode in each background.',
]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Audit:
    def __init__(self):
        self.checks = []
        self.errors = []

    def check(self, name, operation):
        try:
            detail = operation()
            self.checks.append({'check': name, 'status': 'pass', 'details': detail})
            return detail
        except (ValueError, TypeError, KeyError, OSError, IndexError, InvalidOperation) as exc:
            error = {'check': name, 'error': str(exc)}
            self.errors.append(error)
            self.checks.append(dict(error, status='error'))
            return None


def collapse(rows, native=False):
    """One best reported phenotype score per gene; never use TSV rank/order."""
    scores, seen = {}, set()
    identities, reverse_ids, entrez_scores = defaultdict(set), defaultdict(set), {}
    modes, variant_scores, candidate_flags, decimals = Counter(), Counter(), Counter(), Counter()
    count = 0
    for row in rows:
        gene, text = row['GENE_SYMBOL'], row['EXOMISER_GENE_PHENO_SCORE']
        require(isinstance(gene, str) and gene.strip() == gene and gene, 'Missing/invalid gene symbol')
        require(isinstance(text, str) and text.strip() == text and text, 'Missing/invalid phenotype score')
        value = Decimal(text)
        require(value.is_finite() and 0 <= value <= 1, 'Nonfinite/out-of-range phenotype score: ' + gene)
        decimals[str(value.as_tuple().exponent)] += 1
        if native:
            mode, entrez = row['MOI'], row['ENTREZ_GENE_ID']
            require(mode and entrez and entrez.isdigit(), 'Missing mode/gene ID')
            require((gene, mode) not in seen, 'Duplicate gene/mode row: ' + gene)
            require(row['ID'] == gene + '_' + mode, 'Gene/mode ID differs')
            require(re.fullmatch(r'[01]\.\d{4}', text), 'Native score is not four-decimal TSV precision')
            variant = Decimal(row['EXOMISER_GENE_VARIANT_SCORE'])
            require(variant.is_finite() and variant == 0, 'Nonzero/invalid phenotype-only variant score')
            require(row['MATCHES_CANDIDATE_GENE'] == '0', 'Candidate-gene hint flag emitted')
            identities[gene].add(entrez); reverse_ids[entrez].add(gene)
            entrez_scores[entrez] = max(entrez_scores.get(entrez, Decimal('-1')), value)
            seen.add((gene, mode)); modes[mode] += 1
            variant_scores[str(variant)] += 1; candidate_flags[row['MATCHES_CANDIDATE_GENE']] += 1
        else:
            require(gene not in scores, 'Duplicate compact gene: ' + gene)
        scores[gene] = max(scores.get(gene, Decimal('-1')), value)
        count += 1
    require(count > 0, 'Empty phenotype output')
    frequency = Counter(scores.values())
    stats = {'raw_rows': count, 'unique_gene_symbols': len(scores), 'gene_mode_counts': dict(modes),
                    'variant_score_counts': dict(variant_scores), 'candidate_flag_counts': dict(candidate_flags),
                    'decimal_exponent_counts': dict(decimals),
                    'tied_score_groups': sum(n > 1 for n in frequency.values()),
                    'genes_in_tied_groups': sum(n for n in frequency.values() if n > 1),
                    'unique_gene_symbol_set_sha256': digest('\n'.join(sorted(scores))),
                    'best_score_map_sha256': digest('\n'.join(g + '\t' + format(scores[g], '.4f') for g in sorted(scores)))}
    if native:
        shared = {key: sorted(value) for key, value in sorted(reverse_ids.items()) if len(value) > 1}
        multi = {key: sorted(value) for key, value in sorted(identities.items()) if len(value) > 1}
        stats['identifier_qualification'] = {
            'distinct_entrez_ids': len(reverse_ids), 'distinct_nonzero_entrez_ids': len(set(reverse_ids) - {'0'}),
            'symbols_with_id_zero': sorted(reverse_ids.get('0', set())),
            'shared_id_groups': len(shared), 'symbols_in_shared_id_groups': sum(len(v) for v in shared.values()),
            'shared_entrez_ids': shared, 'symbols_with_multiple_entrez_ids': multi,
            'symbol_entrez_mapping_sha256': digest('\n'.join(g + '\t' + ','.join(sorted(ids)) for g, ids in sorted(identities.items())))}
    return scores, stats, {'symbol_to_ids': identities, 'id_to_symbols': reverse_ids, 'entrez_scores': entrez_scores}


def read_scores(path, native=False):
    with Path(path).open() as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        fields = {'GENE_SYMBOL', 'EXOMISER_GENE_PHENO_SCORE'}
        if native:
            fields |= {'MOI', 'ID', 'ENTREZ_GENE_ID', 'EXOMISER_GENE_VARIANT_SCORE', 'MATCHES_CANDIDATE_GENE'}
        require(fields <= set(reader.fieldnames or []), 'Unrecognized phenotype TSV columns')
        return collapse(reader, native)


def rank(scores, target):
    if target not in scores:
        return {'status': 'not_scored', 'rank_min': None, 'rank_max': None, 'scored_genes': len(scores)}
    value = scores[target]
    greater = sum(s > value for s in scores.values())
    tied = sorted(g for g, s in scores.items() if s == value)
    return {'status': 'scored', 'rank_min': greater + 1, 'rank_max': greater + len(tied),
            'scored_genes': len(scores), 'phenotype_score': format(value, '.4f'),
            'strictly_better_genes': greater, 'tied_genes': len(tied), 'tied_gene_symbols': tied}


def self_test():
    def row(gene, score, mode='ANY', gene_id='1'):
        return {'GENE_SYMBOL': gene, 'EXOMISER_GENE_PHENO_SCORE': score, 'MOI': mode,
                'ID': gene + '_' + mode, 'ENTREZ_GENE_ID': gene_id,
                'EXOMISER_GENE_VARIANT_SCORE': '0.0000', 'MATCHES_CANDIDATE_GENE': '0'}
    fixtures = [row('A', '.8000', 'AD'), row('A', '.9000', 'AR'), row('B', '.9000', gene_id='2')]
    # Native TSV uses leading zeros; fixtures follow exactly that representation.
    for r in fixtures:
        r['EXOMISER_GENE_PHENO_SCORE'] = '0' + r['EXOMISER_GENE_PHENO_SCORE']
    scores, _, _ = collapse(fixtures, True)
    require(len(scores) == 2 and scores['A'] == Decimal('.9'), 'Best mode collapse')
    require(rank(scores, 'A')['rank_min'] == 1 and rank(scores, 'A')['rank_max'] == 2, 'Conservative ties')
    require(rank(scores, 'absent')['status'] == 'not_scored', 'Missing target')
    controls = ['collapse distinct modes to one best gene', 'worst tie crosses top1 boundary', 'absent target retained']
    bad = [('empty', []), ('duplicate gene/mode', [row('A', '0.5000')] * 2),
           ('missing gene', [row('', '0.5000')]), ('nan', [row('A', 'NaN')]),
           ('infinity', [row('A', 'Infinity')]), ('negative', [row('A', '-0.1000')]),
           ('above one', [row('A', '1.1000')]), ('missing score', [row('A', '')]),
           ('non-four-decimal', [row('A', '0.12345')]),
           ('variant score', [dict(row('A', '0.5000'), EXOMISER_GENE_VARIANT_SCORE='0.1000')]),
           ('candidate flag', [dict(row('A', '0.5000'), MATCHES_CANDIDATE_GENE='1')])]
    for label, records in bad:
        try:
            collapse(records, True)
        except (ValueError, InvalidOperation):
            controls.append('reject ' + label)
        else:
            raise ValueError('Self-test accepted ' + label)
    scores, stats, _ = collapse([row('A', '0.5000'), row('B', '0.4000')], True)
    require(len(scores) == 2 and stats['identifier_qualification']['shared_entrez_ids'] == {'1': ['A', 'B']}, 'Shared ID must be reported without changing symbol endpoint')
    controls.append('shared Entrez ID retained and reported; no silent symbol collapse')
    _, stats, _ = collapse([row('A', '0.5000', 'AD'), row('A', '0.4000', 'AR', '2')], True)
    require(stats['identifier_qualification']['symbols_with_multiple_entrez_ids'] == {'A': ['1', '2']}, 'Multiple IDs per symbol not reported')
    controls.append('multiple IDs for one symbol explicitly reported')
    _, stats, _ = collapse([row('A', '0.5000', gene_id='0')], True)
    require(stats['identifier_qualification']['symbols_with_id_zero'] == ['A'], 'ID-zero sentinel not reported')
    controls.append('ID-zero sentinel explicitly reported')
    return {'passed': len(controls), 'checks': controls}


def first_pass_check():
    expected = {'audit_phenotype_execution.py': 'e2f69b747cb235e3adf65e529e414c3c9775bb5fe54c9add1119b48689280e12',
                'phenotype-independent-audit.json': 'dd28c658b94d7c3acdcfa8e7e6c2b0ce26e076c6fbefb44054bbe106e5f7424a',
                'phenotype-independent-audit.md': '7e87cf3ec001dba34d3f7b0f207e51948ec1111643d1bcde420fbdf46c681080'}
    for name, value in expected.items():
        require(sha(FIRST_PASS / name) == value, 'First failing audit/script snapshot changed: ' + name)
    first = load(FIRST_PASS / 'phenotype-independent-audit.json')
    require(first['status'] == 'errors' and len(first['errors']) == 12
            and all(e['error'] == 'Inconsistent symbol/Entrez mapping' for e in first['errors']), 'First failing audit differs')
    return {'directory': str(FIRST_PASS), 'file_sha256': expected, 'first_failing_checks': 12,
            'reason': 'First validator imposed a one-to-one symbol/Entrez assumption not present in the frozen symbol-based endpoint. Shared IDs are now surfaced, never silently merged or treated as biological aliases.',
            'inputs_outputs_and_cases_changed': False}


def source_check(catalog, groups):
    cases = catalog['cases']
    require(sha(SOURCE / 'frozen-cases.json') == 'a69127a6c33cb66668686b446fd4d1e793422712bbd60b538a7c25ac159a61e2', 'Frozen source cases changed')
    require(len(cases) == len({c['case_id'] for c in cases}) == len({c['gene'] for c in cases}) == 12, 'Frozen case membership')
    require(set(groups['primary_source_label_genes']) == PRIMARY, 'Primary labels changed')
    require(groups['frozen_inputs_manifest_sha256'] == sha(SOURCE / 'frozen-cases.json'), 'Source-group case hash')
    require(groups['review']['sha256'] == sha(SOURCE / groups['review']['path']), 'Source review hash')
    for key in ('original_pre_result_4_3_2', 'current_source_support_4_5'):
        flat = [g for members in groups[key].values() for g in members]
        require(len(flat) == len(set(flat)) == 9 and set(flat) == PRIMARY, 'Source group partition')
    return {'cases': 12, 'primary_labels': 9, 'cases_sha256': sha(SOURCE / 'frozen-cases.json'),
            'groups_sha256': sha(SOURCE / 'source-support-groups-v3.json'), 'source_groups': groups}


def receipt_check(work, expected_status):
    ex, protocol = load(work / 'execution.json'), load(work / 'protocol-before-inference.json')
    require(ex['status'] == expected_status and ex['planned_jobs'] == len(protocol['jobs']) == 12, 'Execution state/count')
    require(ex['exit_code'] == (0 if expected_status == 'completed' else 1), 'Unexpected exit code')
    for key, name in [('protocol_sha256', 'protocol-before-inference.json'), ('batch_sha256', 'batch.txt'),
                      ('properties_sha256', 'runtime.properties'), ('log_sha256', 'execution.log')]:
        require(ex[key] == sha(work / name), 'Execution hash differs: ' + name)
    require(ex['properties_text'] == (work / 'runtime.properties').read_text(), 'Runtime property text differs')
    require(ex['script_sha256'] == sha(ROOT / 'repo/examples/public-benchmark/run_phenotype.py'), 'Execution wrapper changed')
    require((work / 'batch.txt').read_text().splitlines() == ['--analysis ' + j['job'] for j in protocol['jobs']], 'Actual batch differs')
    require(ex['command'][1:] == ['-Xmx12g', '-Dspring.config.location=file:' + str(work / 'runtime.properties'),
            '-jar', str(ROOT / 'pipeline/exomiser/exomiser-cli-15.1.0/exomiser-cli-15.1.0.jar'), 'batch', str(work / 'batch.txt')], 'Runtime command differs')
    require(set(ex['pre_inference_addenda']) == {p.name for p in work.glob('addendum-*.json')}, 'Addendum membership differs')
    for name, receipt in ex['pre_inference_addenda'].items():
        require(receipt['sha256'] == sha(work / name) and receipt['content'] == load(work / name), 'Execution addendum changed: ' + name)
    for name, expected in ex['software_sha256'].items():
        path = Path(name)
        require(path.is_relative_to(ROOT / 'pipeline/exomiser/exomiser-cli-15.1.0'), 'Unexpected software path')
        require(sha(path) == expected, 'Software hash differs: ' + name)
    for name, receipt in ex['data_receipts'].items():
        require(Path(name).parent == Path('/Volumes/easystore/MVA-public-exomiser-2512'), 'Unexpected extraction receipt path')
        require(sha(name) == receipt['sha256'] and load(name) == receipt['content'], 'Extraction receipt differs')
    log = (work / 'execution.log').read_text()
    expected = {str(work / 'results' / (j['case_id'] + '.phenotype_only.genes.tsv')) for j in protocol['jobs']}
    counts = [int(n) for n in re.findall(r'Loaded (\d+) whitelist variants', log)]
    require(counts == [287098], 'Runtime whitelist count differs')
    started = list(map(int, re.findall(r'Running job (\d+) of 12', log)))
    if expected_status == 'completed':
        require(set(ex['outputs']) == expected and ex['missing_outputs'] == [], 'Completed output receipt membership')
        require({str(p) for p in (work / 'results').iterdir() if p.is_file()} == expected, 'Output file membership')
        require(started == list(range(1, 13)), 'Completed runtime job sequence')
        require(log.count('Running analysis for proband PUBLIC_CASE without VCF') == 12, 'Runtime no-VCF evidence')
        require(log.count('Analysed sample PUBLIC_CASE with 19192 genes containing 0 filtered variants') == 12, 'Runtime gene/variant counts')
        require('Finished batch of 12 samples' in log, 'Batch completion log absent')
    else:
        require(ex['outputs'] == {} and set(ex['missing_outputs']) == expected, 'Prior failure had outputs')
        require(not list((work / 'results').iterdir()), 'Prior output directory is not empty')
        require(started == [1] and 'Assembly hg19 not supported' in log, 'Prior failure reason differs')
        require('Running analysis for proband' not in log and 'Analysed sample' not in log, 'Prior scoring appears to have run')
    return {'status': ex['status'], 'exit_code': ex['exit_code'], 'started_utc': ex['started_utc'],
            'finished_utc': ex['finished_utc'], 'started_jobs': started, 'output_receipts': len(ex['outputs']),
            'missing_outputs': len(ex['missing_outputs']), 'runtime_whitelist_counts': counts,
            'software_files_hashed': len(ex['software_sha256']), 'data_receipt_files_hashed': len(ex['data_receipts']),
            'execution_sha256': sha(work / 'execution.json'), 'log_sha256': sha(work / 'execution.log')}


def relaunch_check():
    old, new = load(OLD / 'protocol-before-inference.json'), load(WORK / 'protocol-before-inference.json')
    a, b = load(OLD / 'execution.json'), load(WORK / 'execution.json')
    note = load(WORK / 'addendum-native-sample-hg38-after-failed-attempt.json')
    for key, name in [('old_execution_sha256', 'execution.json'), ('old_log_sha256', 'execution.log'),
                      ('old_protocol_sha256', 'protocol-before-inference.json')]:
        require(note[key] == sha(OLD / name), 'Relaunch prior hash differs: ' + key)
    require(note['source_file_sha256'] == sha(ROOT / 'pipeline/public_validation/repair_phenotype_assembly.py'), 'Repair script hash differs')
    require(new['prior_protocol_sha256'] == sha(OLD / 'protocol-before-inference.json'), 'Prior protocol hash differs')
    require(new['original_frozen_utc'] == old['frozen_utc'] and old['results_seen'] is False and new['results_seen'] is True,
            'Original/repair result-visibility chronology differs')
    require(new['cases_sha256'] == old['cases_sha256'] == sha(SOURCE / 'frozen-cases.json') and new['purpose'] == old['purpose'], 'Source/endpoints changed')
    require(sha(OLD / 'runtime.properties') == sha(WORK / 'runtime.properties'), 'Runtime properties changed')
    for key in ['software_sha256', 'data_receipts', 'script_sha256', 'java_version']:
        require(a[key] == b[key], 'Runtime/software changed: ' + key)
    require([j['case_id'] for j in old['jobs']] == [j['case_id'] for j in new['jobs']], 'Job order changed')
    require(len(note['changes']) == len({c['case_id'] for c in note['changes']}) == 12, 'Repair change membership')
    for p in OLD.glob('addendum-*.json'):
        require(sha(p) == sha(WORK / p.name), 'Earlier addendum changed: ' + p.name)
    parse = datetime.fromisoformat
    require(parse(old['frozen_utc']) < parse(a['started_utc']) < parse(a['finished_utc']) < parse(new['frozen_utc'])
            <= parse(note['recorded_utc']) < parse(b['started_utc']) < parse(b['finished_utc']), 'Chronology is inconsistent')
    first_genomic = load(ROOT / 'pipeline/work/public-validation-20261023/execution.json')
    completed_genomic = {label: load(path / 'execution.json') for label, path in [
        ('HG002', ROOT / 'pipeline/work/public-validation-cache300k-20261024'),
        ('HG001', Path('/Volumes/easystore/MVA-public-exomiser-2512/runs/public-validation-HG001-cache300k-20261024'))]}
    require(parse(old['frozen_utc']) < parse(first_genomic['started_utc']), 'Original comparator freeze follows genomic execution')
    require(all(e['status'] == 'completed' and parse(e['finished_utc']) < parse(new['frozen_utc'])
                for e in completed_genomic.values()), 'Genomic outcome visibility chronology differs')
    return {'original_frozen_utc': old['frozen_utc'], 'failed_attempt_finished_utc': a['finished_utc'],
            'repair_frozen_utc': new['frozen_utc'], 'repair_started_utc': b['started_utc'],
            'repair_finished_utc': b['finished_utc'], 'results_seen_scope': new['results_seen_scope'],
            'first_genomic_started_utc': first_genomic['started_utc'],
            'completed_genomic_finished_utc': {label: e['finished_utc'] for label, e in completed_genomic.items()},
            'addendum_sha256': sha(WORK / 'addendum-native-sample-hg38-after-failed-attempt.json'),
            'properties_software_and_scoring_wrapper_unchanged': True,
            'change': 'Phenopacket without VCF (runtime hg19 default failure) to native sample with explicit hg38; output paths changed; scoring settings retained.'}


def job_check(case, catalog):
    cid = case['case_id']
    a = next(j for j in load(OLD / 'protocol-before-inference.json')['jobs'] if j['case_id'] == cid)
    b = next(j for j in load(WORK / 'protocol-before-inference.json')['jobs'] if j['case_id'] == cid)
    require({k: v for k, v in a.items() if k not in ('job', 'job_sha256')} == {k: v for k, v in b.items() if k not in ('job', 'job_sha256')}, 'Job labels/strata changed')
    require(b['gene'] == case['gene'] and b['primary_autosomal'] == (case['gene'] in PRIMARY), 'Source label/primary membership differs')
    for j, work in [(a, OLD), (b, WORK)]:
        require(Path(j['job']) == work / 'jobs' / (cid + '.phenotype_only.yml'), 'Unexpected public job path')
        require(sha(j['job']) == j['job_sha256'], 'Executed job hash differs')
    old, new = (yaml.safe_load(Path(j['job']).read_text()) for j in (a, b))
    require(set(old) == {'phenopacket', 'analysis', 'outputOptions'} and set(new) == {'sample', 'analysis', 'outputOptions'}, 'Unexpected job section/hint')
    packet = old['phenopacket']
    require(set(packet) == {'id', 'subject', 'phenotypicFeatures', 'metaData'}, 'Old phenopacket has VCF/hint field')
    require(packet['id'] == cid + '.phenotype_only' and packet['subject'] == {'id': 'PUBLIC_CASE', 'sex': case['sex']}, 'Old case/proband/sex mapping differs')
    require(packet['phenotypicFeatures'] == [{'type': {'id': hp}} for hp in case['arms']['original']], 'Old frozen positive HPO differs')
    require(new['sample'] == {'proband': packet['subject']['id'], 'sex': packet['subject']['sex'],
            'genomeAssembly': 'hg38', 'hpoIds': case['arms']['original']}, 'Native HPO/sex/proband/assembly differs or VCF/hints added')
    analysis = {'analysisMode': 'PASS_ONLY', 'inheritanceModes': {}, 'steps': [{'omimPrioritiser': {}}, {'hiPhivePrioritiser': {}}]}
    require(old['analysis'] == new['analysis'] == analysis, 'Scientific scoring settings changed')
    for value, work in [(old, OLD), (new, WORK)]:
        require(value['outputOptions'] == {'outputContributingVariantsOnly': False, 'numGenes': 0,
                'outputDirectory': str(work / 'results'), 'outputFileName': cid + '.phenotype_only', 'outputFormats': ['TSV_GENE']}, 'Output scope/naming changed')
        text = json.dumps(value, sort_keys=True)
        for source in catalog['cases']:
            require(not re.search(r'(?<![A-Za-z0-9_])' + re.escape(source['gene']) + r'(?![A-Za-z0-9_])', text), 'Explicit selected-gene hint')
            require(all(v not in text for v in [source['source_diagnosis']['id'], source['source_diagnosis']['label']]), 'Explicit source diagnosis hint')
    change = next(c for c in load(WORK / 'addendum-native-sample-hg38-after-failed-attempt.json')['changes'] if c['case_id'] == cid)
    require(change == {'case_id': cid, 'original_job_sha256': a['job_sha256'], 'new_job_sha256': b['job_sha256'],
            'hpo_identical': True, 'sex_identical': True, 'no_vcf': True, 'analysis_identical': True}, 'Repair claim differs from independently checked inputs')
    return {'case_id': cid, 'gene': case['gene'], 'old_job_sha256': a['job_sha256'], 'native_job_sha256': b['job_sha256'],
            'native_sample': new['sample'], 'hpo_order_and_membership_equal': True, 'id_and_sex_equal': True,
            'no_vcf_or_explicit_gene_diagnosis_hint': True, 'scientific_analysis_equal': True}


def output_check(case, cache):
    path = WORK / 'results' / (case['case_id'] + '.phenotype_only.genes.tsv')
    before = sha(path)
    require(load(WORK / 'execution.json')['outputs'][str(path)] == before, 'Raw output receipt/hash differs')
    scores, stats, identity = read_scores(path, True)
    require(stats['unique_gene_symbols'] == 19192 and stats['gene_mode_counts'] == {'ANY': 19192}, 'Symbol/mode count differs from runtime ledger')
    require(sha(path) == before, 'Raw output changed during audit')
    cache[case['case_id']] = scores
    target_ids = sorted(identity['symbol_to_ids'].get(case['gene'], set()))
    sensitivity = {'endpoint': 'Diagnostic maximum phenotype score per nonzero Entrez ID; not the frozen endpoint',
                   'target_entrez_ids': target_ids, 'target_shared_id_symbols': {i: sorted(identity['id_to_symbols'][i]) for i in target_ids}}
    if len(target_ids) == 1 and target_ids[0] != '0' and '0' not in identity['entrez_scores']:
        sensitivity.update(rank(identity['entrez_scores'], target_ids[0]))
        sensitivity['rank_change_from_symbol_endpoint'] = sensitivity['rank_max'] - rank(scores, case['gene'])['rank_max']
    else:
        sensitivity['status'] = 'ambiguous_identifier_mapping'
    return {'case_id': case['case_id'], 'gene': case['gene'], 'primary_autosomal': case['gene'] in PRIMARY,
            **rank(scores, case['gene']), 'output_sha256': before, 'output_path': str(path), 'tsv_statistics': stats,
            'entrez_sensitivity': sensitivity}


def summary(rows, genes):
    selected = [r for r in rows if r['gene'] in genes]
    require(len(selected) == len(genes) and len({r['gene'] for r in selected}) == len(genes), 'Missing/duplicate ledger member')
    return {'denominator': len(genes), 'recovered': {str(k): sum(r['status'] == 'scored' and r['rank_max'] <= k for r in selected) for k in (1, 5, 10)},
            'not_scored': sum(r['status'] == 'not_scored' for r in selected)}


def evaluation_check(path, rows):
    report = load(path)
    require(report['execution_receipt_sha256'] == sha(WORK / 'execution.json'), 'Evaluation receipt link differs')
    lookup = {r['case_id']: r for r in report['all_case_results']}
    require(len(lookup) == len(report['all_case_results']) == len(rows) == 12 and set(lookup) == {r['case_id'] for r in rows}, 'Evaluation job membership')
    for row in rows:
        other = lookup[row['case_id']]
        require(all(other.get(k) == row.get(k) for k in ['gene', 'primary_autosomal', 'status', 'rank_min', 'rank_max', 'scored_genes', 'output_sha256']), 'Independent rank differs: ' + row['gene'])
        if row['status'] == 'scored':
            require(Decimal(str(other['combined_score'])) == Decimal(row['phenotype_score']), 'Independent phenotype score differs')
    own = summary(rows, PRIMARY)
    require(report['primary_autosomal'] == {k: own[k] for k in ('denominator', 'recovered')}, 'Primary outcome ledger differs')
    return {'rows_agree': len(rows), 'evaluation_sha256': sha(path), 'primary': own}


def export_check(rows, cache):
    receipt = load(EXPORT / 'export-receipt.json')
    actual = {str(p.relative_to(EXPORT)) for p in EXPORT.rglob('*') if p.is_file()}
    require(actual == set(receipt['file_sha256']) | {'export-receipt.json'}, 'Export file membership differs')
    for name, expected in receipt['file_sha256'].items():
        p = (EXPORT / name).resolve()
        require(p.is_relative_to(EXPORT.resolve()) and sha(p) == expected, 'Export member hash differs: ' + name)
        if len(Path(name).parts) == 1:
            require(sha(p) == sha(WORK / name), 'Exported runtime/evaluation file differs: ' + name)
    for row in rows:
        cid = row['case_id']
        scores, _, _ = read_scores(EXPORT / 'gene-scores' / (cid + '.tsv'))
        require(scores == cache[cid], 'Exported unique-gene phenotype scores differ: ' + cid)
        job = cid + '.phenotype_only.yml'
        require(sha(EXPORT / 'jobs' / job) == sha(WORK / 'jobs' / job), 'Exported job differs')
    evaluation_check(EXPORT / 'evaluation.json', rows)
    return {'receipt_members_verified': len(receipt['file_sha256']), 'files_including_receipt': len(actual),
            'cases_verified': len(rows), 'all_unique_gene_score_maps_equal': True,
            'export_receipt_sha256': sha(EXPORT / 'export-receipt.json')}


def render(report):
    lines = ['# Independent phenotype-only execution audit', '',
             'Status: **' + report['status'] + '**. Recorded ' + report['recorded_utc'] + '.', '',
             'The validator independently reads raw TSVs and uses Decimal arithmetic; it imports no public runner, evaluator or exporter. No inference or shared gates were run.', '',
             f"Checks: {sum(c['status'] == 'pass' for c in report['checks'])} passed; {len(report['errors'])} errors. Validator controls: {(report.get('self_tests') or {}).get('passed', 0)}.", '']
    if report.get('ledger'):
        ledger = report['ledger']; primary = ledger['primary_nine']; k = primary['recovered']
        lines += [f"Primary conservative top-1/5/10: **{k['1']}/{k['5']}/{k['10']} of {primary['denominator']}**. All 12 frozen cases remain visible. Raw output: {ledger['raw_rows']} rows across 12 jobs, each with 19,192 unique gene-symbol records; all mode ANY, all variant scores zero and all candidate-gene flags zero.", '']
        for r in report['all_case_results']:
            label = 'primary' if r['primary_autosomal'] else 'disputed PAX4' if r['gene'] == 'PAX4' else 'separate X control'
            lines.append(f"- {r['gene']} ({label}): phenotype score {r.get('phenotype_score')}; conservative rank {r['rank_min']}–{r['rank_max']} of {r['scored_genes']}.")
        lines += ['', 'Ranks are rederived from each unique gene’s best reported EXOMISER_GENE_PHENO_SCORE. The native #RANK and combined-score columns are not used. Worst ties are calculated at the reported four-decimal precision.', '']
    if (report.get('first_pass') and any(c['check'] == 'identifier qualifications match all twelve raw files'
                                       and c['status'] == 'pass' for c in report['checks'])):
        lines += ['## Identifier qualification and preserved first failure', '',
                  'Each of the twelve TSVs has **19,192 unique symbols but 19,116 distinct nonzero Entrez IDs**. There are **57 shared-ID groups spanning 133 symbols**. No ID-zero sentinel occurs, no symbol maps to multiple Entrez IDs, and no target source symbol shares an ID. Examples of shared IDs include EIF3C/EIF3CL (728689) and SMN1/SMN2 (6607). These are observed shared identifiers; this audit does not adjudicate whether the symbols are synonyms, distinct loci or database mapping artifacts.', '',
                  'The frozen endpoint remains symbol-based. An explicitly separate sensitivity calculation collapses each Entrez ID to its maximum reported phenotype score: all twelve target ranks are unchanged, as is primary top-1/5/10. No cases or source records were dropped or modified. The complete shared-ID mapping is retained per case in the companion JSON.', '',
                  'The first validator incorrectly required a one-to-one symbol/Entrez mapping and failed all twelve outputs. Its exact script and both failing reports were preserved before revision in `phenotype-independent-audit-first-pass/`, with verified hashes recorded in this audit. The corrected validator reports shared-ID and sentinel anomalies, and tests these cases explicitly; the first failure is not erased.', '']
    if all(report.get(k) for k in ('old_execution', 'new_execution', 'relaunch')) and all(report.get('inputs', [])):
        lines += ['## Frozen inputs, failed attempt and runtime', '',
              'All twelve native HPO lists, subject IDs and sexes are checked against the old frozen phenopackets and the frozen source cases. The native sample adds explicit hg38 and changes output paths; eligibility, source labels, analysis steps, inheritance modes, runtime properties, software and the scoring wrapper remain unchanged.', '',
              'The old attempt failed with exit 1 on unsupported hg19 before phenotype analysis, leaving zero outputs and twelve missing outputs. Its receipts, log and empty output directory are retained. The original comparator freeze precedes genomic outputs; the native wrapper repair occurred after genomic outcomes were known, as explicitly disclosed in the new protocol/addendum.', '',
              'The completed execution log contains twelve “without VCF” analyses, twelve summaries reporting 19,192 genes and zero filtered variants, and a completed batch of twelve. The gene count in the log requires the symbol/Entrez qualification above. The log also reports **Loaded 287098 whitelist variants**. No input alleles exist for whitelist bypass to affect; this does not mean global knowledge or ClinVar was disabled. OMIM and hiPhive remain active.', '']
    if report.get('export'):
        ex = report['export']
        lines += [f"Parent export checked read-only: {ex['receipt_members_verified']} receipted members, {ex['files_including_receipt']} files including the receipt; all twelve compact unique-gene score maps equal the independently read raw TSVs. No export was modified.", '']
    lines += ['## Errors and limits', '']
    lines += ['- ' + e['check'] + ': ' + e['error'] for e in report['errors']] or ['- No audit errors detected.']
    lines += [''] + ['- ' + text for text in LIMITS]
    lines += ['', '## Changed paths and reproduction', '',
              '- `pipeline/public_validation/audit_phenotype_execution.py`',
              '- `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit.json`',
              '- `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit.md`', '',
              'The exact first failing script and JSON/Markdown reports are additionally preserved under `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit-first-pass/` at the user’s request. These are historical failure snapshots, not the current audit result.', '',
              'Run `python3 -B pipeline/public_validation/audit_phenotype_execution.py --self-test` for validator controls, or omit the flag for the complete read-only input/output audit and these two reports. Exit 0 means all executed checks passed; exit 1 means errors. No main-report, workbook, export, input, shared-gate, inference or commit operations are performed.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2)); return 0
    audit = Audit()
    catalog, groups = load(SOURCE / 'frozen-cases.json'), load(SOURCE / 'source-support-groups-v3.json')
    report = {'schema_version': '1.0', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
              'auditor_sha256': sha(__file__), 'work': str(WORK), 'old_failed_work': str(OLD), 'limits': LIMITS}
    report['self_tests'] = audit.check('independent validator controls', self_test)
    report['first_pass'] = audit.check('preserved first failing audit and script', first_pass_check)
    report['sources'] = audit.check('frozen source membership and support groups', lambda: source_check(catalog, groups))
    report['old_execution'] = audit.check('old failed execution/no outputs/receipt hashes', lambda: receipt_check(OLD, 'failed'))
    report['new_execution'] = audit.check('completed execution/no VCF/runtime/receipt hashes', lambda: receipt_check(WORK, 'completed'))
    report['relaunch'] = audit.check('native wrapper repair and chronology', relaunch_check)
    report['inputs'] = [audit.check('frozen/native input ' + c['gene'], lambda c=c: job_check(c, catalog)) for c in catalog['cases']]
    cache = {}
    rows = [audit.check('raw TSV and independent rank ' + c['gene'], lambda c=c: output_check(c, cache)) for c in catalog['cases']]
    report['all_case_results'] = [r for r in rows if r is not None]
    if len(report['all_case_results']) == 12:
        rows = report['all_case_results']
        report['evaluation_comparison'] = audit.check('recorded ranks/primary ledger comparison', lambda: evaluation_check(WORK / 'evaluation.json', rows))
        report['export'] = audit.check('parent compact export independent score/hash check', lambda: export_check(rows, cache))
        partitions = {'primary_nine': PRIMARY, 'all_twelve': {c['gene'] for c in catalog['cases']},
                      'disputed_PAX4': {'PAX4'}, 'X_controls': {'ZIC3', 'OFD1'}}
        for version in ('original_pre_result_4_3_2', 'current_source_support_4_5'):
            partitions.update({version + '/' + name: set(genes) for name, genes in groups[version].items()})
        report['ledger'] = {name: summary(rows, genes) for name, genes in partitions.items()}
        report['ledger'].update(raw_rows=sum(r['tsv_statistics']['raw_rows'] for r in rows),
                               unique_gene_symbol_observations=sum(r['scored_genes'] for r in rows),
                               planned_jobs=12, completed_jobs=12, output_receipts=12,
                               unique_gene_symbol_set_hashes=sorted({r['tsv_statistics']['unique_gene_symbol_set_sha256'] for r in rows}),
                               symbol_entrez_mapping_hashes=sorted({r['tsv_statistics']['identifier_qualification']['symbol_entrez_mapping_sha256'] for r in rows}),
                               entrez_diagnostic_rank_changes={r['gene']: r['entrez_sensitivity'].get('rank_change_from_symbol_endpoint') for r in rows})
        audit.check('same complete symbol universe and ID mapping across twelve jobs', lambda: require(
            len(report['ledger']['unique_gene_symbol_set_hashes']) == len(report['ledger']['symbol_entrez_mapping_hashes']) == 1,
            'Symbol universe or Entrez mapping differs across cases'))
        audit.check('identifier qualifications match all twelve raw files', lambda: require(all(
            r['tsv_statistics']['identifier_qualification']['distinct_nonzero_entrez_ids'] == 19116
            and r['tsv_statistics']['identifier_qualification']['shared_id_groups'] == 57
            and r['tsv_statistics']['identifier_qualification']['symbols_in_shared_id_groups'] == 133
            and not r['tsv_statistics']['identifier_qualification']['symbols_with_id_zero']
            and not r['tsv_statistics']['identifier_qualification']['symbols_with_multiple_entrez_ids']
            and all(len(symbols) == 1 for symbols in r['entrez_sensitivity']['target_shared_id_symbols'].values())
            and r['entrez_sensitivity'].get('rank_change_from_symbol_endpoint') == 0 for r in rows),
            'Identifier qualification or target sensitivity differs; inspect raw mapping'))
    report['checks'], report['errors'] = audit.checks, audit.errors
    report['status'] = 'complete_pass' if not audit.errors else 'errors'
    REPORT.with_suffix('.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    REPORT.with_suffix('.md').write_text(render(report))
    print(json.dumps({'status': report['status'], 'checks': len(audit.checks), 'errors': audit.errors,
                      'primary': report.get('ledger', {}).get('primary_nine'), 'export': report.get('export')}, indent=2))
    return 1 if audit.errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
