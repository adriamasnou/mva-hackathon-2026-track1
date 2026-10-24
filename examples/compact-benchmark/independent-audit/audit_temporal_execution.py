#!/usr/bin/env python3
"""Independent, read-only audit of the PUBLIC 713-signature compact benchmark.

Never imports the canonical evaluator/helper/exporter or runs inference. Arithmetic
uses raw JSONL, exact allele coordinates and independently aggregated Fractions.
--self-test runs in-memory controls. Default invocation validates preparation and
returns pending (2) until execution is terminal. --write-report creates only the
two assigned, previously nonexistent reports; pending reports are never written.
--canonical and --repaired compare retained evaluations, without executing them.
The literal frozen-reader view and NON_DEFAULT-aware view remain separate.
"""
import argparse
from collections import Counter, defaultdict
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SIDE = ROOT / 'pipeline/public_validation/temporal_compact'
BASE = ROOT / 'repo/examples/public-benchmark'
WORK = Path('/Volumes/easystore/MVA-public-exomiser-2512/runs/public-temporal-compact-20261024')
REPORT = ROOT / 'dossier/sweeps/evidence-2026-10-23/rubric-repair/temporal-execution-independent-audit'
ARMS = ('original', 'none')
MODES = {'AUTOSOMAL_DOMINANT', 'AUTOSOMAL_RECESSIVE', 'X_DOMINANT', 'X_RECESSIVE', 'MITOCHONDRIAL'}
K = (1, 5, 10)
ENDPOINTS = (
    ('primary_full_source_allele_recovery', 'recovered', 'reciprocal_rank'),
    ('secondary_gene_only', 'gene_only_recovered', 'gene_only_reciprocal_rank'),
    ('secondary_joint_best_mode_recovery', 'joint_best_recovered', 'joint_best_reciprocal_rank'),
)
LIMITS = [
    'Constructed ten-hypothesis source-label recovery, not clinical accuracy, whole-genome validation, a temporal model-knowledge holdout, therapeutic benefit or competitive superiority.',
    'Our 713 signatures / 261 genes are not the authors\' unresolved 719 cases / 265 genes. The cited primary clinical papers are unadjudicated.',
    'All 713 cases and all genes remain in each arm\'s appropriate denominator, including four preparation failures. X/PAR ploidy is technical-only; phase is unasserted.',
    'Current 2512 gene/disease/HPO/ClinVar knowledge remains. Benign synthetic decoys may filter out; input hypotheses and emitted/PASSED gene universes are distinct. Top-10 can be trivial.',
    'The ledger and every prepared VCF/job are checked independently here. ClinVar source eligibility, source literature and reference normalization are not rerun; their retained preparation receipt hashes are checked.',
    'A missing PASSED-only output allele does not identify the pipeline stage or reason it disappeared. An empty hash-verified output means zero emitted genes, not a known biological cause.',
    'Raw missing contribution/whitelist flags and missing contributing-variant lists remain unknown. No union across different inheritance modes establishes joint recovery.',
    'Missing mode combinedScore is zero only in the separately identified serialization-aware view, supported by installed primitive-double bytecode and NON_DEFAULT writer configuration. Explicit null/nonfinite/bool values remain invalid. The frozen evaluator view is retained independently.',
    'Database receipt hashes and installed software are verified, not multi-gigabyte database payloads. Nothing is uploaded, altered in the frozen run, or committed by this auditor.',
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def byte_sha(data):
    return hashlib.sha256(data).hexdigest()


class Audit:
    def __init__(self):
        self.checks, self.errors = [], []

    def check(self, name, operation):
        try:
            result = operation()
            self.checks.append({'check': name, 'status': 'pass', 'details': result})
            return result
        except (ValueError, TypeError, KeyError, OSError, IndexError, subprocess.SubprocessError) as exc:
            item = {'check': name, 'status': 'error', 'error': str(exc)}
            self.checks.append(item)
            self.errors.append(item)
            return None


def key(v, source=False):
    chrom, pos = ('chrom', 'pos') if source else ('contigName', 'start')
    return str(v[chrom]).removeprefix('chr'), int(v[pos]), v['ref'], v['alt']


def number(value):
    require(type(value) in (int, float) and math.isfinite(value), 'Invalid/nonfinite score')
    return value


def tri_all(values):
    return False if False in values else None if None in values or not values else True


def tri_any(values):
    return True if True in values else None if None in values or not values else False


class ModeReadError(ValueError):
    """Preserve pre-mode diagnostics while all failure endpoints remain zero."""
    def __init__(self, error, row):
        super().__init__(str(error))
        self.row = row


def base_row(case, arm):
    row = {'case_id': case['case_id'], 'gene': case['gene'], 'arm': arm,
           'technical_X': any(key(v, True)[0] == 'X' for v in case['causal_variants']),
           'fallback': len(case['causal_variants']) == 1 and any(d['matching_tier'] != 'type_and_consequence' for d in case['decoys']),
           'pair': len(case['causal_variants']) == 2,
           'input_hypotheses': 1 + len(case['decoys']),
           'input_hypothesis_gene_count': len({case['gene'], *(d['gene'] for d in case['decoys'])}),
           'input_alleles': len(case['causal_variants']) + sum(len(d['alleles']) for d in case['decoys']),
           'status': 'pending', 'rank_min': None, 'rank_max': None,
           'all_source_alleles_passed': False, 'all_source_alleles_contribute': None,
           'all_source_alleles_in_any_best_mode': None, 'all_source_alleles_in_every_best_mode': None,
           'filtered_gene_universe': None, 'emitted_gene_universe': None,
           'source_alleles': [], 'best_modes': [], 'missing_mode_score_count': 0}
    for _, hits, rr in ENDPOINTS:
        row[hits] = {str(k): False for k in K}
        row[rr] = 0.0
    return row


def raw_result(case, arm, records, mode_zero_default=False):
    """No canonical imports. Validate all genes, then rank only PASSED genes.

    mode_zero_default=False reproduces the literal frozen reader's omission
    rejection. True is an explicitly separate, evidence-qualified correction.
    """
    row = base_row(case, arm)
    if case['blockers']:
        row['status'] = 'preparation_failed'
        return row
    sources = [key(v, True) for v in case['causal_variants']]
    require(sources and len(sources) == len(set(sources)), 'Empty/duplicate source alleles')
    seen, passed, target = set(), [], None
    for gene in records:
        symbol = gene['geneSymbol']
        require(isinstance(symbol, str) and symbol and symbol not in seen, 'Missing/duplicate gene')
        seen.add(symbol)
        number(gene['combinedScore'])
        variants = gene.get('variantEvaluations', [])
        require(isinstance(variants, list), 'Invalid variant list')
        if any(v.get('filterStatus') == 'PASSED' for v in variants):
            passed.append(gene)
        if symbol == case['gene']:
            target = gene
    row['emitted_gene_universe'], row['filtered_gene_universe'] = len(records), len(passed)
    row['gene_scores'] = [{k: g.get(k) for k in ('geneSymbol', 'combinedScore', 'priorityScore', 'variantScore')} for g in records]
    contributing = []
    for source in sources:
        matches = [v for v in (target.get('variantEvaluations', []) if target else []) if key(v) == source]
        flags = [v.get('contributesToGeneScore') for v in matches]
        require(all(v is None or type(v) is bool for v in flags), 'Invalid contribution flag')
        available = target is None or 'variantEvaluations' in target
        flag = True if True in flags else None if None in flags or not available else False
        contributing.append(flag)
        row['source_alleles'].append({'coordinate': list(source), 'match_count': len(matches),
            'passed': len(matches) == 1 and matches[0].get('filterStatus') == 'PASSED',
            'raw_matches': [{k: v.get(k) for k in ('filterStatus', 'contributesToGeneScore', 'whiteListed')} for v in matches],
            'contributes_under_some_reported_mode': flag})
    row['all_source_alleles_passed'] = all(v['passed'] for v in row['source_alleles'])
    row['all_source_alleles_contribute'] = tri_all(contributing)
    if target is None:
        row['all_source_alleles_in_any_best_mode'] = row['all_source_alleles_in_every_best_mode'] = False
    else:
        modes = target.get('geneScores', [])
        require(isinstance(modes, list), 'Invalid inheritance-mode list')
        for mode in modes:
            missing = 'combinedScore' not in mode
            row['missing_mode_score_count'] += missing
            try:
                score = number(mode.get('combinedScore', 0.0) if mode_zero_default else mode.get('combinedScore'))
                require(score <= target['combinedScore'], 'Mode score exceeds gene score')
            except ValueError as exc:
                raise ModeReadError(exc, row) from exc
            if score != target['combinedScore']:
                continue
            label = mode.get('modeOfInheritance')
            evidence = mode.get('contributingVariants')
            if 'contributingVariants' in mode:
                require(isinstance(evidence, list), 'Invalid contributing-variant list')
            if evidence is None or label not in MODES:
                joint = None
                matched = []
            else:
                require(isinstance(evidence, list), 'Invalid contributing-variant list')
                observed = {key(v) for v in evidence}
                matched = [list(s) for s in sources if s in observed]
                joint = len(matched) == len(sources)
            row['best_modes'].append({'mode': label, 'score': score, 'score_was_omitted': missing,
                                      'source_alleles': matched, 'all_source_alleles': joint})
        best = [m['all_source_alleles'] for m in row['best_modes']]
        row['all_source_alleles_in_any_best_mode'] = tri_any(best)
        row['all_source_alleles_in_every_best_mode'] = tri_all(best)
    selected = next((g for g in passed if g['geneSymbol'] == case['gene']), None)
    if selected is None:
        row['status'] = 'not_scored'
        return row
    score = selected['combinedScore']
    higher = sum(g['combinedScore'] > score for g in passed)
    equal = sum(g['combinedScore'] == score for g in passed)
    row.update(rank_min=higher + 1, rank_max=higher + equal,
               status='scored' if row['all_source_alleles_passed'] else 'source_allele_failed_or_unrepresented')
    for _, hits, rr in ENDPOINTS:
        use = hits == 'gene_only_recovered' or row['all_source_alleles_passed']
        if hits == 'joint_best_recovered':
            use = use and row['all_source_alleles_in_any_best_mode'] is True
        if use:
            row[hits] = {str(k): row['rank_max'] <= k for k in K}
            row[rr] = 1 / row['rank_max']
    return row


def score_case(case, arm, job, execution, mode_zero_default):
    row = base_row(case, arm)
    if case['blockers']:
        row['status'] = 'preparation_failed'
    elif job is None:
        row['status'] = 'missing_job'
    elif not Path(job['result_jsonl']).is_file():
        row['status'] = 'missing_output'
    else:
        try:
            path = Path(job['result_jsonl'])
            data = path.read_bytes()
            digest = byte_sha(data)
            require(execution.get('outputs', {}).get(str(path)) == digest, 'Output absent/changed in execution receipt')
            for kind in ('vcf', 'job'):
                require(sha(job[kind]) == job[kind + '_sha256'], 'Frozen ' + kind + ' changed')
            records = [json.loads(s) for s in data.decode().splitlines() if s.strip()]
            row = raw_result(case, arm, records, mode_zero_default)
            row['output_sha256'] = digest
        except (ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:
            row = base_row(case, arm)
            if isinstance(exc, ModeReadError):
                # Original adapter has populated these diagnostics before its
                # helper raises; they must not become endpoint successes.
                for name in ('all_source_alleles_passed', 'emitted_gene_universe',
                             'filtered_gene_universe', 'source_alleles', 'missing_mode_score_count'):
                    row[name] = exc.row[name]
            row.update(status='invalid_output', error=str(exc))
    return row


def summary(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['gene']].append(row)
    n, ng = len(rows), len(groups)
    out = {'case_denominator': n, 'gene_denominator': ng,
           'status_counts': dict(Counter(r['status'] for r in rows)),
           'source_alleles_all_passed_cases': sum(r['all_source_alleles_passed'] for r in rows),
           'source_alleles_all_contribute_cases': sum(r['all_source_alleles_contribute'] is True for r in rows),
           'joint_best_mode_unknown_cases': sum(r['all_source_alleles_in_any_best_mode'] is None for r in rows)}
    for name, hits, rr in ENDPOINTS:
        counts = {str(k): sum(r[hits][str(k)] for r in rows) for k in K}
        reciprocal = lambda r: Fraction(1, r['rank_max']) if r[rr] else Fraction(0)
        out[name] = {'top_k_counts': counts,
            'case_top_k_rates': {k: float(Fraction(v, n)) if n else None for k, v in counts.items()},
            'case_mrr': float(sum(map(reciprocal, rows), Fraction(0)) / n) if n else None,
            'gene_macro_top_k_rates': {str(k): float(sum((Fraction(sum(r[hits][str(k)] for r in group), len(group)) for group in groups.values()), Fraction(0)) / ng) if ng else None for k in K},
            'gene_macro_mrr': float(sum((sum(map(reciprocal, group), Fraction(0)) / len(group) for group in groups.values()), Fraction(0)) / ng) if ng else None}
    return out


def strata(rows):
    selectors = {'all_713': lambda r: True, 'primary_autosomal_681': lambda r: not r['technical_X'],
                 'technical_X_32': lambda r: r['technical_X'], 'fallback_18': lambda r: r['fallback'],
                 'without_fallback_695': lambda r: not r['fallback'], 'pairs_64': lambda r: r['pair']}
    return {name: {arm: summary([r for r in rows if r['arm'] == arm and pick(r)]) for arm in ARMS}
            for name, pick in selectors.items()}


def compare(expected, actual, where='root', subset=False):
    """Strict type-aware comparison; never equate null/false/zero."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict), where + ': expected object')
        require(set(expected) <= set(actual) if subset else set(expected) == set(actual), where + ': key set differs')
        for k, v in expected.items():
            compare(v, actual[k], where + '/' + str(k), subset)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), where + ': list length differs')
        for i, (x, y) in enumerate(zip(expected, actual)):
            compare(x, y, where + '/' + str(i), subset)
    elif type(expected) is float:
        require(type(actual) in (float, int) and math.isfinite(actual) and math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-12), where + ': number differs')
    else:
        require(type(expected) is type(actual) and expected == actual, where + ': value/type differs')


def ledger_check(cases, protocol, jobs):
    require(len(cases) == len({c['case_id'] for c in cases}) == 713, 'Case ledger cardinality')
    require(len({tuple(tuple(s) for s in c['signature']) for c in cases}) == 713, 'Duplicate source signature')
    totals, distinct = Counter(), set()
    for case in cases:
        source = [key(v, True) for v in case['causal_variants']]
        require(sorted(source) == sorted(tuple(s) for s in case['signature']), 'Source signature mismatch')
        require(len(source) in (1, 2) and len(source) == len(set(source)), 'Invalid source signature')
        row = base_row(case, 'original')
        require(row['input_hypotheses'] == case['input_candidate_hypotheses'] == 10, 'Input hypothesis count')
        require(row['input_hypothesis_gene_count'] == len(case['input_hypothesis_genes']) == 10, 'Input distinct genes')
        require({case['gene'], *(d['gene'] for d in case['decoys'])} == set(case['input_hypothesis_genes']), 'Input gene membership')
        require(row['input_alleles'] == case['input_candidate_alleles'] == 10 * len(source), 'Input allele count')
        expected = {s: v['genotype'] for s, v in zip(source, case['causal_variants'])}
        for decoy in case['decoys']:
            require(len(decoy['alleles']) == len(decoy['synthetic_genotypes']) == len(source), 'Decoy ploidy/signature size')
            for allele, gt in zip(decoy['alleles'], decoy['synthetic_genotypes']):
                k = tuple(allele['key'])
                require(k not in expected, 'Repeated input allele')
                require(allele['label'] in ('Benign', 'Likely_benign', 'Benign/Likely_benign'), 'Decoy label not benign')
                require(len(allele['genes']) == 1 and allele['genes'][0][0] == decoy['gene'], 'Decoy gene mismatch')
                expected[k] = gt
        draft = Path(case['draft_vcf'])
        require(sha(draft) == case['draft_vcf_sha256'], 'Draft VCF hash changed')
        observed = {}
        for line in draft.read_text().splitlines():
            if line and not line.startswith('#'):
                chrom, pos, ident, ref, alt, qual, filt, info, fmt, gt = line.split('\t')
                k = (chrom, int(pos), ref, alt)
                require(k not in observed and fmt == 'GT' and filt == 'PASS' and ident == info == '.', 'Unexpected VCF record/label')
                observed[k] = gt
        require(observed == expected, 'Exact draft VCF allele/genotype mismatch: ' + case['case_id'])
        distinct.update(expected)
        totals['hypotheses'] += 10
        totals['allele_occurrences'] += len(expected)
    rows = [base_row(c, 'original') for c in cases]
    measured = strata(rows)
    mapping = {'all': 'all_713', 'primary_autosomal': 'primary_autosomal_681', 'technical_X': 'technical_X_32',
               'matching_fallback': 'fallback_18', 'no_matching_fallback': 'without_fallback_695', 'two_allele': 'pairs_64'}
    for name, target in mapping.items():
        for what, expected in protocol['denominators_per_arm'][name].items():
            if what in ('cases', 'genes'):
                require(measured[target]['original'][{'cases': 'case_denominator', 'genes': 'gene_denominator'}[what]] == expected, 'Frozen denominator mismatch: ' + name)
    blocked = [c for c in cases if c['blockers']]
    require(len(blocked) == protocol['preparation_failures_per_arm'] == 4, 'Preparation failures')
    require(all(c['sex'] == 'FEMALE' and c['causal_variants'][0]['chrom'] == 'X' and c['causal_variants'][0]['genotype'] == '1' for c in blocked), 'Blocked-case context')
    allowed = {(c['case_id'], a) for c in cases if not c['blockers'] for a in ARMS}
    require(len(jobs) == len({(j['case_id'], j['arm']) for j in jobs}) == protocol['planned_jobs'] == 1418, 'Job cardinality')
    require({(j['case_id'], j['arm']) for j in jobs} == allowed, 'Jobs missing, unexpected or prepared for blocked cases')
    require(totals == Counter(hypotheses=7130, allele_occurrences=7770) and len(distinct) == 6010, 'Input universes')
    return {'cases': 713, 'case_arm_denominator': len(cases) * 2, 'genes': len({c['gene'] for c in cases}),
            'fixed_strata': {n: {'cases': s['original']['case_denominator'], 'genes': s['original']['gene_denominator']} for n, s in measured.items()},
            'blocked_cases': [{'case_id': c['case_id'], 'gene': c['gene'], 'reasons': c['blockers']} for c in blocked],
            'planned_jobs': len(jobs), **totals, 'distinct_input_alleles': len(distinct)}


def preparation_check(work, cases, jobs, protocol):
    import yaml  # existing PyYAML, used for syntax only; no project-code imports
    prep = load(work / 'preparation-receipt.json')
    hashes = {}
    for name, expected in prep['files_sha256'].items():
        hashes[name] = sha(work / name)
        require(hashes[name] == expected, 'Preparation hash: ' + name)
    require(sha(work / 'cases.json') == protocol['case_manifest_sha256'], 'Protocol case hash')
    components = {SIDE / 'evaluate_adapter.py': protocol['temporal_evaluator_sha256'],
                  SIDE.parent / 'evaluate_temporal_compact.py': protocol['joint_mode_helper_sha256']}
    components.update({BASE / p: h for p, h in protocol['reused_evaluation_sha256'].items()})
    components.update({SIDE / p: h for p, h in protocol['readiness_receipts'].items()})
    for path, digest in components.items():
        require(sha(path) == digest, 'Frozen component/receipt changed: ' + str(path))
    index = {c['case_id']: c for c in cases}
    checked = {}
    for job in jobs:
        for kind in ('job', 'vcf'):
            path = job[kind]
            if path not in checked:
                checked[path] = sha(path)
            require(checked[path] == job[kind + '_sha256'], 'Materialized hash differs: ' + path)
        case = index[job['case_id']]
        require(job['vcf_sha256'] == case['draft_vcf_sha256'], 'Materialized VCF differs from draft')
        require(job['gene'] == case['gene'] and job['variant_records'] == case['input_candidate_alleles'], 'Job metadata differs')
        document = yaml.safe_load(Path(job['job']).read_text())
        packet, analysis, output = (document[k] for k in ('phenopacket', 'analysis', 'outputOptions'))
        require(packet['subject']['sex'] == case['sex'], 'Job sex differs')
        observed = [f['type']['id'] for f in packet.get('phenotypicFeatures', [])]
        require(observed == (case['positive_hpo'] if job['arm'] == 'original' else []), 'Frozen HPO differs')
        require(not packet.get('interpretations') and not packet.get('diseases') and not packet.get('genes'), 'Label/diagnosis supplied')
        require(packet['htsFiles'][0]['uri'] == job['vcf'] and packet['htsFiles'][0]['genomeAssembly'] == 'hg38', 'Input assembly/VCF differs')
        require(analysis['analysisMode'] == 'PASS_ONLY', 'Unexpected analysis mode')
        require(sum('hiPhivePrioritiser' in s for s in analysis['steps']) == (job['arm'] == 'original'), 'Phenotype prioritiser differs')
        require(output['numGenes'] == 0 and output['outputContributingVariantsOnly'] is False, 'Truncated or contributing-only output')
        require(Path(output['outputDirectory']) / (output['outputFileName'] + '.jsonl') == Path(job['result_jsonl']), 'Result destination differs')
    require([s.split() for s in (work / 'batch.txt').read_text().splitlines() if s.strip()] == [['--analysis', j['job']] for j in jobs], 'Batch order/content differs')
    require('exomiser.hg38.use-clinvar-white-list=false' in (work / 'runtime.properties').read_text().splitlines(), 'Whitelist not disabled')
    return {'frozen_hashes': hashes, 'job_vcf_paths_verified': len(checked), 'component_receipt_hashes': {str(p): h for p, h in components.items()}}


def serialization_evidence():
    jar = ROOT / 'pipeline/exomiser/exomiser-cli-15.1.0/lib/exomiser-core-15.1.0.jar'
    javap = '/opt/homebrew/opt/openjdk@21/bin/javap'
    out = {}
    for name in ('writers.JsonResultsWriter', 'model.GeneScore'):
        command = [javap, '-p', '-c', '-classpath', str(jar), 'org.monarchinitiative.exomiser.core.' + name]
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
        out[name] = {'command': command, 'stdout_sha256': byte_sha(result.stdout.encode()), 'stdout': result.stdout}
    require('JsonInclude$Include.NON_DEFAULT' in out['writers.JsonResultsWriter']['stdout'] and 'setDefaultPropertyInclusion' in out['writers.JsonResultsWriter']['stdout'], 'Writer NON_DEFAULT evidence unavailable')
    require('private final double combinedScore;' in out['model.GeneScore']['stdout'], 'Primitive mode score evidence unavailable')
    return {'jar_sha256': sha(jar), 'bytecode': out,
            'interpretation': 'Absent primitive combinedScore is suppressed default zero. This does not make an absent contribution list a positive finding. Explicit null is not suppression.',
            'earlier_optional_probe_limit': 'An interactive JShell probe was attempted read-only: default engine blocked on local socket; local engine timed out after 40 seconds. No empirical serialization result is claimed from those probes.'}


def execution_check(work, jobs, execution):
    require(execution['status'] in ('completed', 'failed'), 'Execution still pending')
    require(execution['planned_jobs'] == len(jobs), 'Execution job denominator')
    require(execution['jobs_manifest_sha256'] == sha(work / 'jobs-manifest.json'), 'Executed manifest changed')
    require(execution['batch_sha256'] == sha(work / 'batch.txt'), 'Executed batch changed')
    require(execution['properties_sha256'] == sha(work / 'runtime.properties') and execution['properties_text'] == (work / 'runtime.properties').read_text(), 'Executed properties changed')
    require(execution['log_sha256'] == sha(work / 'execution.log'), 'Execution log changed')
    require(execution['wrapper_sha256'] == sha(BASE / 'run.py'), 'Executed launcher changed')
    require(execution['evaluation_script_sha256'] == sha(BASE / 'evaluate.py'), 'Executed base evaluator changed')
    for name in ('protocol-before-inference.json', 'preparation-receipt.json'):
        item = execution['design_records'][name]
        require(item['sha256'] == sha(work / name) and item['content'] == load(work / name), 'Design record changed: ' + name)
    frozen = datetime.fromisoformat(execution['design_records']['protocol-before-inference.json']['content']['frozen_utc'])
    require(frozen < datetime.fromisoformat(execution['started_utc']) <= datetime.fromisoformat(execution['finished_utc']), 'Invalid freeze/execution ordering')
    expected_inputs = {j[k]: j[k + '_sha256'] for j in jobs for k in ('job', 'vcf')}
    require(execution['inputs_sha256'] == expected_inputs, 'Executed input hash set differs')
    for path, digest in execution['software_sha256'].items():
        require(sha(path) == digest, 'Installed software differs: ' + path)
    for path, item in execution['data_receipts'].items():
        require(sha(path) == item['sha256'] and load(path) == item['content'], 'Database receipt differs')
    for name, item in execution.get('pre_inference_addenda', {}).items():
        require(sha(work / name) == item['sha256'] and load(work / name) == item['content'], 'Addendum differs')
    expected = {j['result_jsonl'] for j in jobs}
    present = {p for p in expected if Path(p).is_file()}
    require(set(execution['outputs']) == present and set(execution['missing_outputs']) == expected - present, 'Output/missing manifest differs')
    for path, digest in execution['outputs'].items():
        require(sha(path) == digest, 'Output hash differs: ' + path)
    if execution['status'] == 'completed':
        require(execution['exit_code'] == 0, 'Completed with nonzero exit')
    return {'execution_sha256': sha(work / 'execution.json'), 'status': execution['status'],
            'output_count': len(present), 'missing_count': len(expected - present),
            'software_files': len(execution['software_sha256']), 'data_receipts': len(execution['data_receipts']),
            'log_sha256': execution['log_sha256'], 'output_hashes': execution['outputs']}


def output_shape(jobs):
    counts = Counter({k: 0 for k in ('output_files', 'empty_output_files', 'gene_records',
        'gene_records_with_missing_top_level_score', 'source_gene_records',
        'source_modes_with_omitted_score', 'source_modes_with_explicit_null_score',
        'source_gene_outputs_with_omitted_mode_score', 'unparseable_output_files', 'invalid_schema_files')})
    source_cases, missing_top = [], []
    for job in jobs:
        path = Path(job['result_jsonl'])
        if not path.is_file():
            continue
        counts['output_files'] += 1
        try:
            records = [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
        except (ValueError, UnicodeError):
            counts['unparseable_output_files'] += 1
            continue
        if any(not isinstance(g, dict) or not isinstance(g.get('geneScores', []), list)
               or any(not isinstance(m, dict) for m in g.get('geneScores', [])) for g in records):
            counts['invalid_schema_files'] += 1
            continue
        counts['empty_output_files'] += not records
        counts['gene_records'] += len(records)
        for gene in records:
            if 'combinedScore' not in gene:
                counts['gene_records_with_missing_top_level_score'] += 1
                missing_top.append({'case_id': job['case_id'], 'arm': job['arm'], 'gene': gene.get('geneSymbol')})
            if gene.get('geneSymbol') != job['gene']:
                continue
            counts['source_gene_records'] += 1
            modes = gene.get('geneScores', [])
            absent = [m.get('modeOfInheritance') for m in modes if 'combinedScore' not in m]
            counts['source_modes_with_omitted_score'] += len(absent)
            counts['source_modes_with_explicit_null_score'] += sum('combinedScore' in m and m['combinedScore'] is None for m in modes)
            if absent:
                counts['source_gene_outputs_with_omitted_mode_score'] += 1
                source_cases.append({'case_id': job['case_id'], 'arm': job['arm'], 'gene': job['gene'], 'modes': absent})
    return {'counts': dict(counts), 'source_cases_with_omitted_mode_scores': source_cases,
            'top_level_missing_scores': missing_top}


def universe_summary(rows):
    result = {}
    for arm in ARMS:
        selected = [r for r in rows if r['arm'] == arm]
        result[arm] = {'all_cases_including_failures': len(selected),
            'input_hypothesis_distribution': dict(Counter(str(r['input_hypotheses']) for r in selected)),
            'emitted_gene_distribution': dict(Counter(str(r['emitted_gene_universe']) for r in selected)),
            'PASSED_gene_distribution': dict(Counter(str(r['filtered_gene_universe']) for r in selected)),
            'cases_with_1_to_10_PASSED_genes': sum(r['filtered_gene_universe'] is not None and 1 <= r['filtered_gene_universe'] <= 10 for r in selected),
            'scope': 'None means unavailable/invalid, not an observed zero; top-10 recovery still requires every exact source allele PASSED.'}
    return result


def hpo_check(work, cases, terminal=False):
    logs, warnings, terms = {}, [], {'HP:4000064', 'HP:0020003'}
    for filename in ('dry-run.log', 'execution.log'):
        path = work / filename
        if not path.exists():
            continue
        data = path.read_bytes()
        logs[filename] = {'sha256_of_observed_bytes': byte_sha(data), 'bytes': len(data),
                          'complete': filename == 'dry-run.log' or terminal}
        for i, line in enumerate(data.decode(errors='replace').splitlines(), 1):
            if re.search(r'unable to find current id|unknown.*HP:|HP:.*unknown|HP:.*not found|not found.*HP:', line, re.I):
                terms.update(re.findall(r'HP:\d{7}', line))
                warnings.append({'log': filename, 'line': i, 'text': line})
    affected = [{'case_id': c['case_id'], 'gene': c['gene'], 'member': c['member'],
                 'positive_hpo': c['positive_hpo'], 'unmapped_terms': sorted(set(c['positive_hpo']) & terms),
                 'execution_arm': 'original', 'frozen_list_unchanged': True}
                for c in cases if set(c['positive_hpo']) & terms]
    # Add all context lines mentioning these terms, including later scorer warnings.
    context = []
    p = work / 'execution.log'
    if p.exists():
        lines = p.read_text(errors='replace').splitlines()
        chosen = set()
        for i, line in enumerate(lines):
            if any(term in line for term in terms):
                chosen.update(range(max(0, i-2), min(len(lines), i+3)))
        context = [{'line': i+1, 'text': lines[i]} for i in sorted(chosen)]
    job_context = []
    if p.exists():
        jobs = load(work / 'jobs-manifest.json')
        affected_ids = {c['case_id'] for c in affected}
        wanted = {i+1: j for i, j in enumerate(jobs) if j['case_id'] in affected_ids and j['arm'] == 'original'}
        current = None
        for i, line in enumerate(lines, 1):
            start = re.search(r'Running job (\d+) of (\d+)', line)
            if start:
                current = int(start[1])
            if current in wanted and (start or 'WARN ' in line or any(t in line for t in terms)
                                      or 'Analysed sample' in line or 'Writing results' in line or 'HiPhivePriority' in line):
                job_context.append({'case_id': wanted[current]['case_id'], 'gene': wanted[current]['gene'],
                                    'job_number': current, 'line': i, 'text': line})
    return {'logs': logs, 'warnings': warnings, 'affected_cases': affected, 'runtime_term_context': context,
            'runtime_context_by_manifest_job': job_context,
            'qualification': 'Dry run returns the unrecognized input ID unchanged; this alone does not prove the scorer used it. Runtime handling is evidenced only by the retained lines above. Frozen HPO lists are not repaired; no replacement or exclusion from denominators.'}


def evaluation_compare(rows, path, execution_hash, case_hash):
    retained = load(path)
    require(retained['execution_sha256'] == execution_hash and retained['case_manifest_sha256'] == case_hash, 'Evaluation provenance differs')
    observed = retained['all_case_arm_results']
    require(len(observed) == len(rows) and len({(r['case_id'], r['arm']) for r in observed}) == len(rows), 'Evaluation duplicates/drops cases')
    index = {(r['case_id'], r['arm']): r for r in observed}
    compare(strata(rows), retained['all_strata'], 'all_strata')
    fields = ('case_id', 'gene', 'arm', 'technical_X', 'fallback', 'pair', 'input_hypotheses',
              'input_hypothesis_gene_count', 'input_alleles', 'status', 'rank_min', 'rank_max',
              'all_source_alleles_passed', 'all_source_alleles_contribute',
              'all_source_alleles_in_any_best_mode', 'all_source_alleles_in_every_best_mode',
              'filtered_gene_universe', 'emitted_gene_universe')
    checked = 0
    for row in rows:
        other = index[(row['case_id'], row['arm'])]
        # Frozen adapter retains some partial diagnostics when a later mode parse
        # fails. Its failure endpoints/ranks, not those stale diagnostics, govern.
        names = fields if row['status'] != 'invalid_output' else ('case_id', 'gene', 'arm', 'status', 'rank_min', 'rank_max')
        for name in (*names, *(k for _, h, rr in ENDPOINTS for k in (h, rr))):
            compare(row[name], other[name], row['case_id'] + '/' + row['arm'] + '/' + name)
            checked += 1
        if row.get('output_sha256'):
            require(row['output_sha256'] == other.get('output_sha256'), 'Evaluation output hash differs')
        if row.get('gene_scores') is not None:
            compare(row['gene_scores'], other['gene_scores'], row['case_id'] + '/gene_scores')
        if row['source_alleles']:
            source_audit = other['source_allele_audit']['source_variants']
            require(len(source_audit) == len(row['source_alleles']), 'Source allele audit length differs')
            for independent, emitted in zip(row['source_alleles'], source_audit):
                require(independent['coordinate'] == [emitted['source_coordinate'][k] for k in ('chrom', 'pos', 'ref', 'alt')], 'Source audit coordinate differs')
                require(independent['match_count'] == emitted['exact_matches_in_source_gene'], 'Source audit multiplicity differs')
                compare(independent['raw_matches'], emitted['matches'], row['case_id'] + '/source_allele_flags', subset=True)
    return {'path': str(path), 'sha256': sha(path), 'case_arms_compared': len(rows), 'row_fields_compared': checked,
            'all_fixed_strata_compared': True}


def selftests():
    """Deliberately wrong second alleles, modes, ties and denominators must fail."""
    labels = []
    def ok(name, value):
        require(value, 'SELFTEST ' + name)
        labels.append(name)
    def rejects(name, call):
        try:
            call()
        except (ValueError, KeyError, TypeError):
            labels.append(name)
            return
        raise ValueError('SELFTEST failed to reject ' + name)
    source = [{'chrom': '1', 'pos': p, 'ref': 'A', 'alt': 'G', 'genotype': '0/1'} for p in (10, 20)]
    case = {'case_id': 'fixture', 'gene': 'A', 'causal_variants': source, 'decoys': [], 'blockers': []}
    variants = [{'contigName': '1', 'start': v['pos'], 'ref': 'A', 'alt': 'G', 'filterStatus': 'PASSED', 'contributesToGeneScore': True} for v in source]
    def gene(symbol='A', score=.8, vs=None, modes=None):
        return {'geneSymbol': symbol, 'combinedScore': score, 'variantEvaluations': copy.deepcopy(variants if vs is None else vs),
                'geneScores': copy.deepcopy([{'modeOfInheritance': 'AUTOSOMAL_RECESSIVE', 'combinedScore': score, 'contributingVariants': variants}] if modes is None else modes)}
    valid = raw_result(case, 'original', [gene()], True)
    ok('positive_pair', valid['recovered']['1'] and valid['joint_best_recovered']['1'])
    wrong = gene(); wrong['variantEvaluations'][1]['filterStatus'] = 'FAILED'
    r = raw_result(case, 'original', [wrong], True)
    ok('failed_second_allele_keeps_gene_only', not r['recovered']['10'] and r['gene_only_recovered']['1'])
    wrong = gene(); wrong['variantEvaluations'].pop()
    ok('missing_second_allele', not raw_result(case, 'original', [wrong], True)['recovered']['1'])
    wrong = gene(); wrong['variantEvaluations'][1]['alt'] = 'C'
    ok('exact_alt_required', not raw_result(case, 'original', [wrong], True)['recovered']['1'])
    wrong = gene(); wrong['variantEvaluations'].append(copy.deepcopy(variants[0]))
    ok('duplicate_source_match_is_not_recovery', not raw_result(case, 'original', [wrong], True)['recovered']['1'])
    wrong = gene(); wrong.pop('geneScores')
    r = raw_result(case, 'original', [wrong], True)
    ok('unknown_mode_evidence_not_success', r['all_source_alleles_in_any_best_mode'] is None and not r['joint_best_recovered']['1'])
    wrong = gene(); wrong['geneScores'][0].pop('contributingVariants')
    r = raw_result(case, 'original', [wrong], True)
    ok('missing_contributing_list_remains_unknown', r['all_source_alleles_in_every_best_mode'] is None and not r['joint_best_recovered']['1'])
    wrong['geneScores'][0]['contributingVariants'] = None
    rejects('explicit_null_contribution_list_invalid', lambda: raw_result(case, 'original', [wrong], True))
    wrong = gene(); wrong['geneScores'][0]['modeOfInheritance'] = 'UNKNOWN'
    ok('unrecognized_mode_not_joint_success', raw_result(case, 'original', [wrong], True)['all_source_alleles_in_any_best_mode'] is None)
    modes = [{'modeOfInheritance': label, 'combinedScore': .8, 'contributingVariants': [v]} for label, v in zip(('AUTOSOMAL_DOMINANT', 'AUTOSOMAL_RECESSIVE'), variants)]
    r = raw_result(case, 'original', [gene(modes=modes)], True)
    ok('no_union_across_tied_best_modes', r['all_source_alleles_in_any_best_mode'] is False)
    modes[1]['contributingVariants'] = variants
    r = raw_result(case, 'original', [gene(modes=modes)], True)
    ok('any_and_every_tied_best_are_distinct', r['all_source_alleles_in_any_best_mode'] is True and r['all_source_alleles_in_every_best_mode'] is False)
    modes[0].pop('contributingVariants')
    r = raw_result(case, 'original', [gene(modes=modes)], True)
    ok('one_known_complete_one_unknown_mode', r['all_source_alleles_in_any_best_mode'] is True and r['all_source_alleles_in_every_best_mode'] is None)
    modes[0]['combinedScore'] = .9
    rejects('mode_score_cannot_exceed_gene', lambda: raw_result(case, 'original', [gene(modes=modes)], True))
    tied = raw_result(case, 'original', [gene(), gene('B'), gene('C', .9, vs=[])], True)
    ok('worst_ties_among_PASSED_genes_only', tied['rank_min'] == 1 and tied['rank_max'] == 2 and not tied['recovered']['1'] and tied['emitted_gene_universe'] == 3 and tied['filtered_gene_universe'] == 2)
    rejects('duplicate_gene_rejected_even_filtered', lambda: raw_result(case, 'original', [gene(), gene(vs=[])], True))
    for bad in (None, True, float('nan'), float('inf'), '0.8'):
        rejects('bad_gene_score_' + str(bad), lambda bad=bad: raw_result(case, 'original', [gene(score=bad)], True))
    missingzero = gene(); missingzero['geneScores'].append({'modeOfInheritance': 'MITOCHONDRIAL'})
    rejects('frozen_reader_rejects_omitted_zero', lambda: raw_result(case, 'original', [missingzero], False))
    ok('qualified_zero_default_preserves_positive_best', raw_result(case, 'original', [missingzero], True)['joint_best_recovered']['1'])
    missingzero['geneScores'][-1]['combinedScore'] = None
    rejects('explicit_null_mode_score_still_invalid', lambda: raw_result(case, 'original', [missingzero], True))
    empty = raw_result(case, 'original', [], True)
    ok('empty_hash_verified_output_nonrecovery', empty['status'] == 'not_scored' and empty['emitted_gene_universe'] == empty['filtered_gene_universe'] == 0 and not empty['recovered']['10'])
    blocked = copy.deepcopy(case); blocked['blockers'] = ['ploidy']; blocked['gene'] = 'B'
    fail = raw_result(blocked, 'original', [], True)
    second_fail = copy.deepcopy(empty); second_fail['case_id'] = 'second'
    s = summary([valid, second_fail, fail])
    m = s['primary_full_source_allele_recovery']
    ok('preparation_and_empty_failures_retained', s['case_denominator'] == 3 and s['gene_denominator'] == 2 and m['case_top_k_rates']['1'] == 1/3)
    ok('gene_macro_not_case_weighted', m['gene_macro_top_k_rates']['1'] == .25 and m['gene_macro_mrr'] == .25)
    missing = score_case(case, 'original', None, {}, True)
    ok('missing_job_zero_denominator_member', missing['status'] == 'missing_job' and summary([valid, missing])['primary_full_source_allele_recovery']['case_top_k_rates']['1'] == .5)
    rejects('comparison_rejects_dropped_failure_denominator', lambda: compare(s, summary([valid, second_fail])))
    rejects('comparison_distinguishes_unknown_false', lambda: compare(None, False))
    rejects('comparison_rejects_corrupt_numeric', lambda: compare(.5, .6))
    # Actual file-boundary controls use disposable /tmp files, never run inputs.
    with tempfile.TemporaryDirectory(prefix='mva-temporal-audit-') as td:
        folder = Path(td)
        output, jobpath, vcf = [folder / p for p in ('output.jsonl', 'job.yml', 'source.vcf')]
        jobpath.write_text('synthetic fixture only\n'); vcf.write_text('synthetic fixture only\n')
        omitted = gene(); omitted['geneScores'].append({'modeOfInheritance': 'MITOCHONDRIAL'})
        output.write_text(json.dumps(omitted) + '\n')
        job = {'job': str(jobpath), 'vcf': str(vcf), 'result_jsonl': str(output),
               'job_sha256': sha(jobpath), 'vcf_sha256': sha(vcf)}
        execution = {'outputs': {str(output): sha(output)}}
        strict = score_case(case, 'original', job, execution, False)
        revised = score_case(case, 'original', job, execution, True)
        ok('frozen_invalid_mode_keeps_preparsed_diagnostics', strict['status'] == 'invalid_output' and strict['all_source_alleles_passed'] and strict['filtered_gene_universe'] == 1)
        ok('frozen_invalid_mode_never_counts_success', not strict['recovered']['10'] and strict['reciprocal_rank'] == 0 and strict['rank_max'] is None)
        ok('qualified_reader_recovers_same_hash_verified_bytes', revised['recovered']['1'] and revised['output_sha256'] == execution['outputs'][str(output)])
        output.write_text('{}\n')
        ok('tampered_output_rejected', score_case(case, 'original', job, execution, True)['status'] == 'invalid_output')
        output.write_text('')
        execution['outputs'][str(output)] = sha(output)
        ok('hash_verified_empty_file_distinct_from_missing', score_case(case, 'original', job, execution, True)['status'] == 'not_scored')
        vcf.write_text('changed\n')
        ok('changed_input_rejected_even_empty_output', score_case(case, 'original', job, execution, True)['status'] == 'invalid_output')
        output.unlink()
        ok('missing_output_failure', score_case(case, 'original', job, execution, True)['status'] == 'missing_output')
    return {'status': 'pass', 'count': len(labels), 'controls': labels}


def run(args):
    audit = Audit()
    controls = audit.check('independent_negative_controls', selftests)
    cases = load(args.work / 'cases.json')['cases']
    jobs = load(args.work / 'jobs-manifest.json')
    protocol = load(args.work / 'protocol-before-inference.json')
    ledger = audit.check('full_case_ledger_and_input_VCFs', lambda: ledger_check(cases, protocol, jobs))
    preparation = audit.check('frozen_preparation_jobs_and_hashes', lambda: preparation_check(args.work, cases, jobs, protocol))
    serialization = audit.check('installed_NON_DEFAULT_primitive_zero_evidence', serialization_evidence)
    execution_path = args.work / 'execution.json'
    execution = load(execution_path) if execution_path.exists() else {}
    terminal = execution.get('status') in ('completed', 'failed')
    report = {'audit_utc': datetime.now(timezone.utc).isoformat(), 'auditor_sha256': sha(__file__),
              'work': str(args.work), 'scope': LIMITS, 'selftests': controls, 'ledger': ledger,
              'preparation': preparation, 'serialization_evidence': serialization,
              'HPO_mapping': hpo_check(args.work, cases, terminal),
              'execution_status_observed': execution.get('status', 'not_started'),
              'comparisons': {}, 'metrics': None}
    if terminal and not audit.errors:
        evidence = audit.check('execution_outputs_and_provenance', lambda: execution_check(args.work, jobs, execution))
        report['execution'] = evidence
        if evidence is not None:
            report['output_serialization_shape'] = output_shape(jobs)
            index = {(j['case_id'], j['arm']): j for j in jobs}
            views = {}
            for view, default in (('literal_frozen_reader', False), ('NON_DEFAULT_aware_independent', True)):
                rows = [score_case(c, arm, index.get((c['case_id'], arm)), execution, default) for c in cases for arm in ARMS]
                views[view] = rows
            report['metrics'] = {name: strata(rows) for name, rows in views.items()}
            report['all_case_arm_results'] = views
            report['universe_summaries'] = {view: universe_summary(rows) for view, rows in views.items()}
            changed = []
            for a, b in zip(views['literal_frozen_reader'], views['NON_DEFAULT_aware_independent']):
                if a['status'] != b['status']:
                    changed.append({'case_id': a['case_id'], 'arm': a['arm'], 'gene': a['gene'],
                        'frozen_status': a['status'], 'frozen_error': a.get('error'), 'independent_status': b['status'],
                        'missing_mode_scores': b['missing_mode_score_count']})
            report['serialization_defect'] = {'changed_case_arms': len(changed), 'details': changed,
                'interpretation': 'Independent corrected view is post-freeze interpretation, not a changed inference or an undisclosed replacement of original results.'}
            for name, path, view in (('canonical_frozen', args.canonical, 'literal_frozen_reader'),
                                     ('versioned_repaired', args.repaired, 'NON_DEFAULT_aware_independent')):
                if path is not None:
                    report['comparisons'][name] = audit.check('compare_' + name,
                        lambda path=path, view=view: evaluation_compare(views[view], path, sha(execution_path), sha(args.work / 'cases.json')))
            report['endpoint_deltas_original_minus_none'] = {}
            for view, summaries in report['metrics'].items():
                delta = {}
                for name, arms in summaries.items():
                    delta[name] = {}
                    for endpoint, _, _ in ENDPOINTS:
                        a, b = (arms[arm][endpoint] for arm in ARMS)
                        delta[name][endpoint] = {'case_top_k_rate_delta': {str(k): a['case_top_k_rates'][str(k)] - b['case_top_k_rates'][str(k)] for k in K},
                            'gene_macro_top_k_rate_delta': {str(k): a['gene_macro_top_k_rates'][str(k)] - b['gene_macro_top_k_rates'][str(k)] for k in K},
                            'case_mrr_delta': a['case_mrr'] - b['case_mrr'], 'gene_macro_mrr_delta': a['gene_macro_mrr'] - b['gene_macro_mrr']}
                report['endpoint_deltas_original_minus_none'][view] = delta
    report['checks'], report['errors'] = audit.checks, audit.errors
    report['status'] = 'ERROR' if audit.errors else 'TERMINAL_AUDITED' if terminal else 'PREPARED_EXECUTION_PENDING'
    report['comparison_status'] = 'not_requested' if not (args.canonical or args.repaired) else 'see_comparisons'
    return report


def write_report(report):
    require(report['status'] != 'PREPARED_EXECUTION_PENDING', 'Pending execution: do not create a final report')
    paths = [REPORT.with_suffix(s) for s in ('.json', '.md')]
    require(not any(p.exists() for p in paths), 'Preserve prior audit evidence; reports already exist')
    text = [f"# Independent compact benchmark audit — {report['status']}", '',
            f"Observed {report['audit_utc']}. Auditor SHA256 `{report['auditor_sha256']}`.", '',
            f"Execution status: **{report['execution_status_observed']}**. Checks: {len(report['checks'])}; errors: {len(report['errors'])}.", '',
            'The adjacent JSON retains every checked hash, all case/arm outcomes, fixed-denominator metrics, source-allele/mode details, serialization evidence and original-versus-none deltas.', '',
            'The literal frozen-reader result and independently interpreted NON_DEFAULT result are separate. The latter does not silently replace the former.', '']
    if report.get('serialization_defect'):
        text += [f"Serialization omission changes status for {report['serialization_defect']['changed_case_arms']} case/arm outputs; see the enumerated JSON ledger.", '']
    for view, strata_result in (report.get('metrics') or {}).items():
        text += [view + ':', '']
        for arm in ARMS:
            s = strata_result['primary_autosomal_681'][arm]
            m = s['primary_full_source_allele_recovery']
            text += [f"- {arm}: full-source-allele top-1/5/10 {list(m['top_k_counts'].values())} / {s['case_denominator']}; gene denominator {s['gene_denominator']}; MRR {m['case_mrr']:.6f}."]
        text += ['']
    text += ['HPO mapping qualifications:', '']
    for c in report['HPO_mapping']['affected_cases']:
        text += [f"- {c['case_id']} ({c['gene']}): {', '.join(c['unmapped_terms'])}; full unchanged HPO list and runtime context in JSON."]
    text += ['', 'Limitations:', '', *['- ' + s for s in LIMITS], '']
    if report['errors']:
        text += ['Errors (reporting them does not change the frozen evaluator):', '', *['- ' + e['check'] + ': ' + e['error'] for e in report['errors']], '']
    paths[0].write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    paths[1].write_text('\n'.join(text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=WORK)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--canonical', type=Path)
    parser.add_argument('--repaired', type=Path)
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(selftests(), indent=2))
        return 0
    result = run(args)
    if args.write_report:
        write_report(result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('all_case_arm_results', 'serialization_evidence', 'preparation', 'metrics', 'checks')}, indent=2, allow_nan=False))
    return 1 if result['errors'] else 0 if result['status'] == 'TERMINAL_AUDITED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
