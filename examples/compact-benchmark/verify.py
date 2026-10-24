#!/usr/bin/env python3
"""Offline compact713 verification. Standard library; never imports scoring code."""
import argparse
from collections import Counter, defaultdict
import difflib
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys

ARMS = ('original', 'none')
KS = ('1', '5', '10')
CASE_SHA = '816f87efa1fc2bfcf8f0b6f3c9326cbb01f62c601f8ecaae4208d02086bd45fc'
STRATA = {
    'all_713': (713, 261), 'primary_autosomal_681': (681, 245),
    'technical_X_32': (32, 16), 'fallback_18': (18, 13),
    'without_fallback_695': (695, 257), 'pairs_64': (64, 41),
}
ENDPOINTS = {
    'primary_full_source_allele_recovery': ('recovered', 'reciprocal_rank'),
    'secondary_gene_only': ('gene_only_recovered', 'gene_only_reciprocal_rank'),
    'secondary_joint_best_mode_recovery': ('joint_best_recovered', 'joint_best_reciprocal_rank'),
}
LIMITS = [
    'Constructed 713-signature cohort, not the author-exact 719 cases.',
    'Source-case labels from 322 clinical papers remain unadjudicated; only PMID 37054711 overlaps the prior main-text reading ledger, with 321 absent from it.',
    'Different candidate universes: 10 input hypotheses can expand or shrink after mapping/filtering; top10 may be trivial.',
    'Current 2512 knowledge remains; this is not a temporal knowledge holdout.',
    'No clinical accuracy, biological benefit, therapeutic result or competitor superiority established.',
    'Exact allele matching does not establish phase, joint causality or equivalent-haplotype recovery; X cases are technical only.',
    'VCFs, Java and databases are omitted. Offline verification checks retained receipts, not absent inputs or a rerun.',
    'Local SHA256 receipt consistency is not an external signature or independent timestamp.',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'Duplicate JSON object key: ' + key)
        obj[key] = value
    return obj


def loads(text):
    return json.loads(text, object_pairs_hook=unique_object)


def read_json(path):
    return loads(Path(path).read_text(encoding='utf-8'))


def local(root, name):
    """Bundle references cannot escape, follow symlinks or use original paths."""
    require(isinstance(name, str) and bool(name), 'Empty/non-string bundle path')
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and '\\' not in name and
            all(p not in ('', '.', '..') for p in name.split('/')), 'Unsafe path: ' + name)
    path = Path(root)
    for part in parts.parts:
        path = path / part
        require(not path.is_symlink(), 'Symlink forbidden: ' + name)
    require(path.is_file(), 'Missing bundle file: ' + name)
    return path


def terminal(execution):
    require(execution.get('status') == 'completed' and execution.get('exit_code') == 0,
            'Export requires terminal completed execution with exit 0')
    require(execution.get('finished_utc') and execution.get('started_utc'), 'Missing execution times')
    require(execution.get('planned_jobs') == 1418, 'Expected 1418 planned executable jobs')
    require(execution.get('missing_outputs') == [], 'Execution has missing/unknown outputs')
    require(isinstance(execution.get('outputs'), dict) and len(execution['outputs']) == 1418,
            'Expected 1418 output receipts')


def tags(case):
    return {
        'technical_X': any(v['chrom'] == 'X' for v in case['causal_variants']),
        'fallback': len(case['signature']) == 1 and
                    any(d['matching_tier'] != 'type_and_consequence' for d in case['decoys']),
        'pair': len(case['signature']) == 2,
    }


def included(row, name):
    return {'all_713': True, 'primary_autosomal_681': not row['technical_X'],
            'technical_X_32': row['technical_X'], 'fallback_18': row['fallback'],
            'without_fallback_695': not row['fallback'], 'pairs_64': row['pair']}[name]


def ledger(cases, jobs):
    require(len(cases) == 713 and len({c['case_id'] for c in cases}) == 713, 'Need 713 unique cases')
    require(len({json.dumps(c['signature']) for c in cases}) == 713, 'Duplicate source signature')
    require(all(re.fullmatch(r'TC_[0-9a-f]{16}', c['case_id']) for c in cases), 'Invalid case ID')
    require(sum(bool(c['blockers']) for c in cases) == 4, 'Need four preparation failures per arm')
    for name, (n, g) in STRATA.items():
        group = [c for c in cases if included(tags(c), name)]
        require((len(group), len({c['gene'] for c in group})) == (n, g), 'Stratum changed: ' + name)
    papers = {r['id'] for c in cases for r in c['source_metadata'].get('externalReferences', [])
              if r['id'].startswith('PMID:')}
    require(len(papers) == 322, 'Referenced paper count changed')
    expected = {(c['case_id'], a) for c in cases if not c['blockers'] for a in ARMS}
    index = {(j['case_id'], j['arm']): j for j in jobs}
    require(len(jobs) == len(index) == 1418 and set(index) == expected,
            'Missing/duplicate/unexpected/blocked-case jobs')
    require(len({j['result_jsonl'] for j in jobs}) == 1418 and
            len({j['job'] for j in jobs}) == 1418, 'Reused output or job path')
    for c in cases:
        if c['blockers']:
            continue
        pair = [index[c['case_id'], a] for a in ARMS]
        require(len({(j['vcf'], j['vcf_sha256']) for j in pair}) == 1, 'Arms use different VCFs')
        for j in pair:
            require(j['gene'] == c['gene'] and j['primary_autosomal'] == (not tags(c)['technical_X']),
                    'Job source identity/partition mismatch')
            require(j['vcf_sha256'] == c['draft_vcf_sha256'], 'Draft/executed VCF receipt mismatch')
    return index


def score(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value),
            'Invalid/nonfinite combined score')
    return value


def key(v, source=False):
    return (str(v['chrom' if source else 'contigName']).removeprefix('chr'),
            int(v['pos' if source else 'start']), v['ref'], v['alt'])


def tri_all(values):
    return False if False in values else None if not values or None in values else True


def tri_any(values):
    return True if True in values else None if not values or None in values else False


def blank(case, arm):
    row = dict(case_id=case['case_id'], gene=case['gene'], arm=arm, **tags(case),
               input_hypotheses=case['input_candidate_hypotheses'],
               input_hypothesis_gene_count=len(case['input_hypothesis_genes']),
               input_alleles=case['input_candidate_alleles'], rank_min=None, rank_max=None,
               all_source_alleles_passed=False, all_source_alleles_contribute=None,
               all_source_alleles_in_any_best_mode=None, all_source_alleles_in_every_best_mode=None,
               filtered_gene_universe=None, emitted_gene_universe=None)
    for success, rr in ENDPOINTS.values():
        row[success] = dict.fromkeys(KS, False)
        row[rr] = Fraction(0)
    return row


def derive(case, arm, records, corrected=True, unavailable=None):
    """Direct arithmetic over raw records; returns every failure with zero RR.

    The literal-original diagnostic deliberately rejects an omitted mode score.
    No function from either recorded evaluator/helper is executed here.
    """
    row = blank(case, arm)
    if case['blockers'] or unavailable:
        row['status'] = 'preparation_failed' if case['blockers'] else unavailable
        row['reasons'] = case['blockers'] or [unavailable]
        return row
    try:
        require(isinstance(records, list), 'Raw records are not a list')
        genes = {}
        for record in records:
            symbol = record['geneSymbol']
            require(isinstance(symbol, str) and symbol and symbol not in genes, 'Missing/duplicate gene')
            score(record['combinedScore'])  # Includes excluded genes.
            genes[symbol] = record
        passing = {g: r for g, r in genes.items()
                   if any(v.get('filterStatus') == 'PASSED' for v in r.get('variantEvaluations', []))}
        row.update(emitted_gene_universe=len(genes), filtered_gene_universe=len(passing),
                   scored_genes=len(passing), status='not_scored')
        target = genes.get(case['gene'])
        if case['gene'] in passing:
            value = score(target['combinedScore'])
            greater = sum(r['combinedScore'] > value for r in passing.values())
            tied = sum(r['combinedScore'] == value for r in passing.values())
            row.update(status='scored', rank_min=greater + 1, rank_max=greater + tied,
                       combined_score=value, priority_score=target.get('priorityScore'),
                       variant_score=target.get('variantScore'))
        sources = [key(v, True) for v in case['causal_variants']]
        matches = [[v for v in target.get('variantEvaluations', []) if key(v) == s]
                   if target is not None else [] for s in sources]
        row['all_source_alleles_passed'] = all(len(vs) == 1 and vs[0].get('filterStatus') == 'PASSED'
                                              for vs in matches)
        require(sources and len(set(sources)) == len(sources), 'Empty/duplicated source allele')
        contributions = []
        row['source_observations'] = []
        for source, variants in zip(sources, matches):
            flags = [v.get('contributesToGeneScore') for v in variants]
            require(all(v is None or isinstance(v, bool) for v in flags), 'Invalid contribution flag')
            known = target is None or 'variantEvaluations' in target
            contributions.append(True if True in flags else None if None in flags or not known else False)
            row['source_observations'].append({'source': list(source), 'exact_matches': len(variants),
                'matches': [{'filterStatus': v.get('filterStatus'),
                             'contributesToGeneScore': v.get('contributesToGeneScore'),
                             'whiteListed': v.get('whiteListed')} for v in variants]})
        best_states = []
        row['mode_observations'] = []
        if target is not None:
            for mode in target.get('geneScores', []):
                mode_score = score(mode.get('combinedScore', 0) if corrected else mode.get('combinedScore'))
                require(mode_score <= target['combinedScore'], 'Mode exceeds reported best gene score')
                alleles = {key(v) for v in mode.get('contributingVariants', [])}
                state = set(sources) <= alleles if 'contributingVariants' in mode else None
                is_best = mode_score == target['combinedScore']
                row['mode_observations'].append({'mode': mode['modeOfInheritance'], 'score': mode_score,
                    'score_omitted': 'combinedScore' not in mode, 'best': is_best,
                    'all_source_alleles': state})
                if is_best:
                    best_states.append(state)
        any_best = tri_any(best_states) if target is not None else False
        row['all_source_alleles_contribute'] = tri_all(contributions)
        row['all_source_alleles_in_any_best_mode'] = any_best
        row['all_source_alleles_in_every_best_mode'] = tri_all(best_states) if target is not None else False
        if row['status'] == 'scored':
            worst = row['rank_max']
            for name, condition in [('secondary_gene_only', True),
                    ('primary_full_source_allele_recovery', row['all_source_alleles_passed']),
                    ('secondary_joint_best_mode_recovery', row['all_source_alleles_passed'] and any_best is True)]:
                success, rr = ENDPOINTS[name]
                if condition:
                    row[success] = {k: worst <= int(k) for k in KS}
                    row[rr] = Fraction(1, worst)
            if not row['all_source_alleles_passed']:
                row['status'] = 'source_allele_failed_or_unrepresented'
    except (ValueError, KeyError, TypeError, AttributeError, OverflowError) as error:
        row.update(status='invalid_output', error=str(error), rank_min=None, rank_max=None,
                   all_source_alleles_contribute=None, all_source_alleles_in_any_best_mode=None,
                   all_source_alleles_in_every_best_mode=None)
        for success, rr in ENDPOINTS.values():
            row[success], row[rr] = dict.fromkeys(KS, False), Fraction(0)
    return row


def summarize(rows):
    n = len(rows)
    groups = defaultdict(list)
    for r in rows:
        groups[r['gene']].append(r)
    g = len(groups)
    result = {'case_denominator': n, 'gene_denominator': g,
              'status_counts': dict(Counter(r['status'] for r in rows)),
              'source_alleles_all_passed_cases': sum(r['all_source_alleles_passed'] for r in rows),
              'source_alleles_all_contribute_cases': sum(r['all_source_alleles_contribute'] is True for r in rows),
              'joint_best_mode_unknown_cases': sum(r['all_source_alleles_in_any_best_mode'] is None for r in rows)}
    for name, (success, rr) in ENDPOINTS.items():
        counts = {k: sum(r[success][k] for r in rows) for k in KS}
        result[name] = {
            'top_k_counts': counts,
            'case_top_k_rates': {k: Fraction(counts[k], n) if n else None for k in KS},
            'case_mrr': sum((r[rr] for r in rows), Fraction(0)) / n if n else None,
            'gene_macro_top_k_rates': {k: sum((Fraction(sum(r[success][k] for r in rs), len(rs))
                for rs in groups.values()), Fraction(0)) / g if g else None for k in KS},
            'gene_macro_mrr': sum((sum((r[rr] for r in rs), Fraction(0)) / len(rs)
                for rs in groups.values()), Fraction(0)) / g if g else None,
        }
    return result


def aggregate(rows):
    return {name: {a: summarize([r for r in rows if r['arm'] == a and included(r, name)])
                   for a in ARMS} for name in STRATA}


def compare(expected, actual, path='root'):
    """Exact identities/counts/flags; tiny float tolerance only for calculated rates."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and set(expected) == set(actual), 'Keys differ: ' + path)
        for k, value in expected.items():
            compare(value, actual[k], path + '.' + k)
    elif isinstance(expected, Fraction):
        require(isinstance(actual, (int, float)) and not isinstance(actual, bool) and
                math.isfinite(actual) and math.isclose(float(expected), actual, rel_tol=1e-12, abs_tol=1e-12),
                'Metric differs: ' + path)
    else:
        require(type(expected) is type(actual) and expected == actual, 'Value differs: ' + path)


def checked_inventory(root):
    receipt = read_json(local(root, 'export-receipt.json'))
    require(receipt.get('schema') == 'compact713-portable-v1', 'Unknown export schema')
    inventory = receipt['file_sha256']
    require('export-receipt.json' not in inventory, 'Self-hashed receipt')
    files = set()
    for path in Path(root).rglob('*'):
        require(not path.is_symlink(), 'Symlink in bundle')
        if path.is_file() and path != Path(root) / 'export-receipt.json':
            files.add(path.relative_to(root).as_posix())
    require(files == set(inventory), 'Bundle inventory has missing or extra files')
    for name, digest in inventory.items():
        require(re.fullmatch(r'[0-9a-f]{64}', digest) is not None, 'Malformed SHA256')
        require(sha(local(root, name)) == digest, 'Bundle SHA256 mismatch: ' + name)
        require(not name.lower().endswith(('.vcf', '.vcf.gz', '.jar', '.db', '.mv.db')),
                'Forbidden inference input/binary in bundle')
    return receipt, inventory


def provenance(root, inventory):
    """Cross-link copied bytes to execution, freeze, correction, and evaluations."""
    def digest(name, expected):
        require(inventory.get(name) == expected and expected is not None, 'Provenance hash differs: ' + name)

    execution = read_json(local(root, 'execution.json'))
    terminal(execution)
    digest('jobs-manifest.json', execution['jobs_manifest_sha256'])
    for name, field in [('runtime.properties', 'properties_sha256'), ('batch.txt', 'batch_sha256'),
                        ('execution.log', 'log_sha256')]:
        digest(name, execution[field])
    require(local(root, 'runtime.properties').read_text() == execution['properties_text'], 'Property text differs')
    require(isinstance(execution.get('pre_inference_addenda'), dict), 'Missing addenda object')
    for name, record in {**execution['design_records'], **execution['pre_inference_addenda']}.items():
        digest(name, record['sha256'])
        require(read_json(local(root, name)) == record['content'], 'Embedded design content differs: ' + name)
    for name in ('protocol-before-inference.json', 'preparation-receipt.json'):
        require(name in execution['design_records'], 'Required design receipt missing: ' + name)
    protocol = read_json(local(root, 'protocol-before-inference.json'))
    prep = read_json(local(root, 'preparation-receipt.json'))
    require(protocol['state'] == 'FROZEN_BEFORE_INFERENCE' and protocol['arms'] == list(ARMS), 'Protocol changed')
    require(protocol['planned_jobs'] == 1418 and protocol['preparation_failures_per_arm'] == 4 and
            protocol['intended_case_arm_denominator'] == 1426, 'Protocol ledger differs')
    digest('cases.json', CASE_SHA)
    digest('cases.json', protocol['case_manifest_sha256'])
    for name, value in prep['files_sha256'].items():
        digest(name, value)
    require(prep['scientific_input_changes'] == [], 'Scientific preparation changes recorded')
    correction = read_json(local(root, 'correction-v2/correction-receipt.json'))
    digest('cases.json', correction['frozen_case_manifest_sha256'])
    digest('code/original/evaluate_adapter.py', protocol['temporal_evaluator_sha256'])
    digest('code/original/joint_mode.py', protocol['joint_mode_helper_sha256'])
    digest('code/original/evaluate_adapter.py', correction['frozen_adapter_sha256'])
    digest('code/original/joint_mode.py', correction['frozen_helper_sha256'])
    for name, value in protocol['reused_evaluation_sha256'].items():
        digest('code/reused/' + name, value)
    digest('code/reused/run.py', execution['wrapper_sha256'])
    digest('code/reused/evaluate.py', execution['evaluation_script_sha256'])
    for name, value in correction['corrected_component_sha256'].items():
        digest('code/correction-v2/' + name, value)
    for name, value in correction['evidence_sha256'].items():
        digest('correction-v2/' + name, value)
    probe_dir = 'correction-v2/serialization-probe/'
    probe = read_json(local(root, probe_dir + 'receipt.json'))
    require(probe['exit_code'] == 0, 'Serialization probe failed')
    digest(probe_dir + 'ModeScoreProbe.java', probe['code_sha256'])
    digest(probe_dir + 'output.txt', probe['stdout_sha256'])
    for relative, value in probe['library_sha256'].items():
        recorded = [h for p, h in execution['software_sha256'].items() if p.endswith('/' + relative)]
        require(recorded == [value], 'Probe library differs from executed software')
    for stem, name in [('adapter', 'evaluate_adapter.py'), ('helper', 'joint_mode.py')]:
        diff = ''.join(difflib.unified_diff(
            local(root, 'code/original/' + name).read_text().splitlines(keepends=True),
            local(root, 'code/correction-v2/' + name).read_text().splitlines(keepends=True),
            fromfile='frozen/' + stem, tofile='correction-v2/' + stem))
        require(diff == local(root, 'correction-v2/' + stem + '.diff').read_text(), 'Correction diff differs')
    evaluations = {}
    for version in ('original', 'corrected-v2'):
        ev = read_json(local(root, 'evaluations/' + version + '.json'))
        digest('execution.json', ev['execution_sha256'])
        digest('cases.json', ev['case_manifest_sha256'])
        require(ev['execution_status'] == 'completed', 'Evaluation not completed')
        code = 'original' if version == 'original' else 'correction-v2'
        digest('code/' + code + '/evaluate_adapter.py', ev['evaluator_sha256'])
        evaluations[version] = ev
    ev = evaluations['corrected-v2']
    require(ev['analysis_version'] == 'post-freeze-correction-v2', 'Wrong corrected evaluation version')
    digest('correction-v2/correction-receipt.json', ev['correction_receipt_sha256'])
    digest('code/original/evaluate_adapter.py', ev['frozen_evaluator_sha256'])
    digest('code/original/joint_mode.py', ev['frozen_helper_sha256'])
    digest('code/correction-v2/joint_mode.py', ev['corrected_helper_sha256'])
    return execution, evaluations


def verify_bundle(root):
    root = Path(root).resolve()
    receipt, inventory = checked_inventory(root)
    execution, evaluations = provenance(root, inventory)
    cases = read_json(local(root, 'cases.json'))['cases']
    jobs = read_json(local(root, 'jobs-manifest.json'))
    index = ledger(cases, jobs)
    crosscheck = read_json(local(root, 'source-reading-crosscheck.json'))
    require(crosscheck['case_manifest_sha256'] == inventory['cases.json'], 'Reading crosscheck cases differ')
    papers = {r['id'].removeprefix('PMID:') for c in cases
              for r in c['source_metadata'].get('externalReferences', []) if r['id'].startswith('PMID:')}
    overlap = crosscheck['existing_main_text_read_overlap']
    absent = crosscheck['source_publications_not_in_main_text_read_ledger']
    require(overlap == ['37054711'] and len(absent) == len(set(absent)) == 321 and
            not set(overlap) & set(absent) and set(overlap) | set(absent) == papers and
            crosscheck['source_publication_count'] == 322, 'Reading crosscheck PMID partition differs')
    # The prior 51-paper reading ledger is not bundled: preserve its recorded hash,
    # but do not turn this partition check into an independent paper-reading claim.
    require(re.fullmatch(r'[0-9a-f]{64}', crosscheck['reading_ledger_sha256']) is not None,
            'Missing reading ledger provenance hash')
    mapping = read_json(local(root, 'path-map.json'))
    included_paths = mapping['included']
    require(all(isinstance(k, str) and k.startswith('/') for k in included_paths), 'Expected absolute provenance paths')
    for relative in included_paths.values():
        require(relative in inventory, 'Mapped file absent from inventory')
        local(root, relative)
    omitted = mapping['omitted_vcf_sha256']
    require(omitted == {j['vcf']: j['vcf_sha256'] for j in jobs}, 'Omitted VCF ledger differs')
    require(set(omitted).isdisjoint(included_paths), 'VCF must not be bundled')
    require(set(execution['outputs']) == {j['result_jsonl'] for j in jobs}, 'Output receipt keys differ')
    expected_inputs = {j[k]: j[k + '_sha256'] for j in jobs for k in ('job', 'vcf')}
    require(execution['inputs_sha256'] == expected_inputs, 'Executed input hash ledger differs')
    batch = [line.split() for line in local(root, 'batch.txt').read_text().splitlines() if line.strip()]
    require(batch == [['--analysis', j['job']] for j in jobs], 'Batch order/content differs')
    for original, data in execution['data_receipts'].items():
        relative = included_paths[original]
        require(inventory[relative] == data['sha256'] and read_json(local(root, relative)) == data['content'],
                'Data receipt differs')
    rows = {v: [] for v in evaluations}
    expected_raw, expected_jobs = set(), set()
    for case in cases:
        for arm in ARMS:
            job = index.get((case['case_id'], arm))
            records, parse_error, output_sha = [], None, None
            if job:
                raw_name = 'raw/' + case['case_id'] + '.' + arm + '.jsonl'
                job_name = 'jobs/' + case['case_id'] + '.' + arm + '.yml'
                expected_raw.add(raw_name)
                expected_jobs.add(job_name)
                require(included_paths[job['result_jsonl']] == raw_name and
                        included_paths[job['job']] == job_name, 'Portable job mapping differs')
                output_sha = execution['outputs'][job['result_jsonl']]
                require(inventory[raw_name] == output_sha, 'Raw output differs from execution receipt')
                require(inventory[job_name] == job['job_sha256'], 'Job differs from manifest')
                try:
                    with local(root, raw_name).open(encoding='utf-8') as stream:
                        records = [loads(line) for line in stream if line.strip()]
                except (ValueError, UnicodeError) as error:
                    parse_error = str(error)
            for version in rows:
                row = derive(case, arm, records, corrected=version == 'corrected-v2',
                             unavailable='invalid_output' if parse_error else None)
                if output_sha:
                    row['output_sha256'] = output_sha
                if parse_error:
                    row['error'] = parse_error
                rows[version].append(row)
    require({p for p in inventory if p.startswith('raw/')} == expected_raw, 'Extra/missing raw files')
    require({p for p in inventory if p.startswith('jobs/')} == expected_jobs, 'Extra/missing job files')
    summaries = {}
    for version, derived in rows.items():
        ev = evaluations[version]
        retained = ev['all_case_arm_results']
        lookup = {(r['case_id'], r['arm']): r for r in retained}
        require(len(retained) == len(lookup) == 1426 and set(lookup) ==
                {(c['case_id'], a) for c in cases for a in ARMS}, 'Incomplete evaluation ledger: ' + version)
        for row in derived:
            actual = lookup[row['case_id'], row['arm']]
            fields = set(blank(next(c for c in cases if c['case_id'] == row['case_id']), row['arm'])) | {'status'}
            for extra in ('scored_genes', 'combined_score', 'priority_score', 'variant_score'):
                if extra in row:
                    fields.add(extra)
            compare({k: row[k] for k in fields}, {k: actual[k] for k in fields},
                    version + '.' + row['case_id'] + '.' + row['arm'])
            if row['status'] not in ('preparation_failed', 'invalid_output'):
                require(actual['output_sha256'] == row['output_sha256'], 'Evaluation output hash differs')
        summaries[version] = aggregate(derived)
        compare(summaries[version], ev['all_strata'], version + '.all_strata')
    affected = []
    for old, new in zip(rows['original'], rows['corrected-v2']):
        fields = ['status', 'rank_min', 'rank_max', 'all_source_alleles_contribute',
                  'all_source_alleles_in_any_best_mode', 'all_source_alleles_in_every_best_mode']
        fields += [k for values in ENDPOINTS.values() for k in values]
        changed = {k: {'original': old[k], 'corrected': new[k]} for k in fields if old[k] != new[k]}
        if changed:
            affected.append({'case_id': new['case_id'], 'arm': new['arm'], 'changes': changed})
    return {'status': 'verified', 'export_receipt_sha256': sha(root / 'export-receipt.json'),
            'files': len(inventory), 'raw_outputs': 1418, 'cases': 713, 'case_arm_rows': 1426,
            'preparation_failures_per_arm': 4, 'referenced_papers': 322,
            'all_strata': summaries, 'correction_affected_case_arms': affected,
            'all_case_arm_results': rows, 'limitations': LIMITS}


def json_default(value):
    if isinstance(value, Fraction):
        return float(value)
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--report', type=Path, help='Optional NEW report outside the immutable bundle')
    args = parser.parse_args()
    try:
        report = verify_bundle(args.bundle)
        if args.report:
            require(args.bundle.resolve() not in args.report.resolve().parents, 'Write report outside bundle')
            with args.report.open('x', encoding='utf-8') as stream:
                json.dump(report, stream, indent=2, default=json_default, allow_nan=False)
                stream.write('\n')
        print(json.dumps({k: v for k, v in report.items() if k not in ('all_case_arm_results', 'all_strata')},
                         indent=2, default=json_default, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print('VERIFICATION FAILED: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
