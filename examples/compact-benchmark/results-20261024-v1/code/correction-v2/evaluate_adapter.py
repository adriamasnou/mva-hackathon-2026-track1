#!/usr/bin/env python3
"""Evaluate a later authorized run; this script never executes Exomiser.

Explicit post-freeze copy with one semantic correction: mode-score default zero.
The original evaluator and its literal result remain retained. Inputs, endpoints,
tie ranking, denominator and inclusion rules are unchanged. Iterate all planned cases, including preparation failures.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FROZEN_ADAPTER = HERE.parent / "evaluate_adapter.py"
FROZEN_HELPER = HERE.parent.parent / "evaluate_temporal_compact.py"
CORRECTION = HERE / "correction-receipt.json"
BASE = ROOT / 'repo/examples/public-benchmark'
ARMS = ('original', 'none')


def module(name):
    spec = importlib.util.spec_from_file_location('temporal_reuse_' + name, BASE / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


ranking = module('evaluate')
exporter = module('export_results')
runner = module('run')
HELPER = HERE / 'joint_mode.py'
helper_spec = importlib.util.spec_from_file_location('temporal_joint_mode', HELPER)
joint_mode = importlib.util.module_from_spec(helper_spec)
helper_spec.loader.exec_module(joint_mode)


def case_result(case, arm, job, execution):
    result = {'case_id': case['case_id'], 'gene': case['gene'], 'arm': arm,
              'technical_X': any(v['chrom'] == 'X' for v in case['causal_variants']),
              'fallback': any(d['matching_tier'] != 'type_and_consequence' for d in case['decoys']) if len(case['signature']) == 1 else False,
              'pair': len(case['signature']) == 2, 'input_hypotheses': case['input_candidate_hypotheses'],
              'input_hypothesis_gene_count': len(case['input_hypothesis_genes']),
              'input_alleles': case['input_candidate_alleles'], 'rank_min': None, 'rank_max': None,
              'all_source_alleles_passed': False, 'all_source_alleles_contribute': None,
              'all_source_alleles_in_any_best_mode': None,
              'all_source_alleles_in_every_best_mode': None,
              'joint_best_mode_audit': None, 'joint_best_reciprocal_rank': 0.0,
              'joint_best_recovered': {str(k): False for k in (1, 5, 10)},
              'reciprocal_rank': 0.0, 'gene_only_reciprocal_rank': 0.0,
              'recovered': {str(k): False for k in (1, 5, 10)},
              'gene_only_recovered': {str(k): False for k in (1, 5, 10)},
              'filtered_gene_universe': None, 'emitted_gene_universe': None}
    if case['blockers']:
        result.update(status='preparation_failed', reasons=case['blockers'])
        return result
    if job is None:
        result['status'] = 'missing_job'
        return result
    raw = Path(job['result_jsonl'])
    if not raw.is_file():
        result['status'] = 'missing_output'
        return result
    try:
        if execution.get('outputs', {}).get(str(raw)) != runner.sha(raw):
            raise ValueError('Output hash absent/different in execution receipt')
        for kind in ('job', 'vcf'):
            if runner.sha(job[kind]) != job[kind + '_sha256']:
                raise ValueError('Executed input changed: ' + kind)
        records = [json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
        # A hash-verified empty output may mean every input allele was filtered.
        # Retain its zero emitted universe and nonrecovery; do not invent a cause.
        # Validate all emitted scores/identities before using a passing subset.
        ranking.rank_records(records, case['gene'])
        passing = [r for r in records if any(v.get('filterStatus') == 'PASSED' for v in r.get('variantEvaluations', []))]
        ranks = ranking.rank_records(passing, case['gene'])
        result.update(ranks)
        result['emitted_gene_universe'] = len(records)
        result['filtered_gene_universe'] = len(passing)
        audit = exporter.variant_audit(records, case)
        result['source_allele_audit'] = audit
        result['all_source_alleles_passed'] = all(
            a['exact_matches_in_source_gene'] == 1 and a['matches'][0].get('filterStatus') == 'PASSED'
            for a in audit['source_variants'])
        joint = joint_mode.exact_alleles(records, case)
        result['joint_best_mode_audit'] = joint
        result['all_source_alleles_contribute'] = joint['all_source_alleles_contributing']
        for key in ('all_source_alleles_in_any_best_mode', 'all_source_alleles_in_every_best_mode'):
            result[key] = joint[key]
        if ranks['status'] == 'scored':
            worst = ranks['rank_max']
            result['gene_only_reciprocal_rank'] = 1 / worst
            result['gene_only_recovered'] = {str(k): worst <= k for k in (1, 5, 10)}
            if result['all_source_alleles_passed']:
                result['reciprocal_rank'] = 1 / worst
                result['recovered'] = {str(k): worst <= k for k in (1, 5, 10)}
                if joint['all_source_alleles_in_any_best_mode'] is True:
                    result['joint_best_reciprocal_rank'] = 1 / worst
                    result['joint_best_recovered'] = dict(result['recovered'])
            else:
                result['status'] = 'source_allele_failed_or_unrepresented'
        result['output_sha256'] = runner.sha(raw)
        result['gene_scores'] = [{k: r.get(k) for k in ('geneSymbol', 'combinedScore', 'priorityScore', 'variantScore')}
                                 for r in records]
        return result
    except (ValueError, KeyError, TypeError, OSError) as error:
        # No partial scoring of an invalid file; preserve failure in every denominator.
        result.update(status='invalid_output', error=str(error), rank_min=None, rank_max=None)
        result['recovered'] = {str(k): False for k in (1, 5, 10)}
        result['gene_only_recovered'] = {str(k): False for k in (1, 5, 10)}
        result['reciprocal_rank'] = result['gene_only_reciprocal_rank'] = 0.0
        result['joint_best_recovered'] = {str(k): False for k in (1, 5, 10)}
        result['joint_best_reciprocal_rank'] = 0.0
        result['all_source_alleles_in_any_best_mode'] = None
        result['all_source_alleles_in_every_best_mode'] = None
        result['joint_best_mode_audit'] = None
        result['all_source_alleles_contribute'] = None
        return result


def summarize(rows):
    by_gene = defaultdict(list)
    for r in rows:
        by_gene[r['gene']].append(r)
    n, g = len(rows), len(by_gene)
    result = {'case_denominator': n, 'gene_denominator': g,
              'status_counts': dict(Counter(r['status'] for r in rows)),
              'source_alleles_all_passed_cases': sum(r['all_source_alleles_passed'] for r in rows),
              'source_alleles_all_contribute_cases': sum(r['all_source_alleles_contribute'] is True for r in rows),
              'joint_best_mode_unknown_cases': sum(r['all_source_alleles_in_any_best_mode'] is None for r in rows)}
    for name, success, rr in [('primary_full_source_allele_recovery', 'recovered', 'reciprocal_rank'),
                              ('secondary_gene_only', 'gene_only_recovered', 'gene_only_reciprocal_rank'),
                              ('secondary_joint_best_mode_recovery', 'joint_best_recovered', 'joint_best_reciprocal_rank')]:
        result[name] = {
            'top_k_counts': {str(k): sum(r[success][str(k)] for r in rows) for k in (1, 5, 10)},
            'case_top_k_rates': {str(k): sum(r[success][str(k)] for r in rows) / n if n else None for k in (1, 5, 10)},
            'case_mrr': sum(r[rr] for r in rows) / n if n else None,
            'gene_macro_top_k_rates': {str(k): sum(sum(r[success][str(k)] for r in rs) / len(rs)
                                                   for rs in by_gene.values()) / g if g else None for k in (1, 5, 10)},
            'gene_macro_mrr': sum(sum(r[rr] for r in rs) / len(rs) for rs in by_gene.values()) / g if g else None}
    return result


def aggregate(rows):
    strata = {'all_713': lambda r: True, 'primary_autosomal_681': lambda r: not r['technical_X'],
              'technical_X_32': lambda r: r['technical_X'], 'fallback_18': lambda r: r['fallback'],
              'without_fallback_695': lambda r: not r['fallback'], 'pairs_64': lambda r: r['pair']}
    return {name: {arm: summarize([r for r in rows if r['arm'] == arm and include(r)]) for arm in ARMS}
            for name, include in strata.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--cases', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    out = a.out.resolve()
    if HERE not in out.parents or out.exists():
        raise ValueError('Write a new evaluation receipt only within this sidecar')
    cases = json.loads(a.cases.read_text())['cases']
    if len(cases) != 713 or len({c['case_id'] for c in cases}) != 713:
        raise ValueError('All 713 planned signatures must remain in the denominator')
    execution = json.loads((a.work / 'execution.json').read_text())
    manifest = a.work / 'jobs-manifest.json'
    if runner.sha(manifest) != execution.get('jobs_manifest_sha256'):
        raise ValueError('Executed jobs manifest differs')
    protocol = execution.get('design_records', {}).get('protocol-before-inference.json', {}).get('content', {})
    if protocol.get('case_manifest_sha256') != runner.sha(a.cases):
        raise ValueError('Full case ledger was not hashed into the execution protocol')
    correction = json.loads(CORRECTION.read_text())
    for name in ('evaluate_adapter.py', 'joint_mode.py'):
        if correction['corrected_component_sha256'][name] != runner.sha(HERE / name):
            raise ValueError('Versioned correction code differs from correction receipt')
    if correction['frozen_adapter_sha256'] != runner.sha(FROZEN_ADAPTER) or correction['frozen_helper_sha256'] != runner.sha(FROZEN_HELPER):
        raise ValueError('Original frozen evaluator/helper changed')
    if protocol.get('temporal_evaluator_sha256') != runner.sha(FROZEN_ADAPTER):
        raise ValueError('Temporal evaluator was not pinned before execution')
    if protocol.get('joint_mode_helper_sha256') != runner.sha(FROZEN_HELPER):
        raise ValueError('Joint-mode helper was not pinned before execution')
    for name in ('evaluate.py', 'export_results.py'):
        if protocol.get('reused_evaluation_sha256', {}).get(name) != runner.sha(BASE / name):
            raise ValueError('Reused evaluation component not pinned or changed')
    if execution.get('status') not in ('completed', 'failed'):
        raise ValueError('Do not evaluate a still-running/incomplete execution receipt')
    jobs = json.loads(manifest.read_text())
    index = {(j['case_id'], j['arm']): j for j in jobs}
    allowed = {(c['case_id'], arm) for c in cases if not c['blockers'] for arm in ARMS}
    if len(index) != len(jobs) or not set(index) <= allowed:
        raise ValueError('Unexpected, duplicated, or blocked-case jobs')
    results = [case_result(c, arm, index.get((c['case_id'], arm)), execution) for c in cases for arm in ARMS]
    output = {'scope': 'Constructed compact source-label recovery; not clinical accuracy, knowledge holdout or a head-to-head reproduction.',
              'analysis_version': 'post-freeze-correction-v2',
              'correction_receipt_sha256': runner.sha(CORRECTION),
              'frozen_evaluator_sha256': runner.sha(FROZEN_ADAPTER),
              'frozen_helper_sha256': runner.sha(FROZEN_HELPER),
              'corrected_helper_sha256': runner.sha(HELPER),
              'execution_status': execution['status'], 'execution_sha256': runner.sha(a.work / 'execution.json'),
              'case_manifest_sha256': runner.sha(a.cases), 'evaluator_sha256': runner.sha(__file__),
              'primary_rule': 'Conservative worst-tied source-gene rank among genes with at least one PASSED allele; every exact source allele must be represented in that gene and PASSED. No phase or joint causality claim.',
              'failure_rule': 'Preparation, missing-output, invalid-output and unrepresented/failed source-allele cases remain failures with reciprocal rank zero. Verified completed outputs from a terminal failed batch are retained alongside every missing failure.',
              'all_strata': aggregate(results), 'all_case_arm_results': results}
    out.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output['all_strata'], indent=2))


if __name__ == '__main__':
    main()
