#!/usr/bin/env python3
"""Synthetic controls only; no inference, mounted outputs or shared project gates."""
from collections import Counter, defaultdict
import copy
import difflib
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import export
import verify as v


def source(pos=1, chrom='1'):
    return dict(chrom=chrom, pos=pos, ref='A', alt='T', genotype='0/1')


def allele(pos=1, passed=True):
    return dict(contigName='1', start=pos, ref='A', alt='T',
                filterStatus='PASSED' if passed else 'FAILED', contributesToGeneScore=True)


def case(pair=False, blocked=False):
    variants = [source(1), source(2)] if pair else [source(1)]
    return dict(case_id='TC_0000000000000000', gene='TARGET', causal_variants=variants,
                signature=[[x['chrom'], x['pos'], x['ref'], x['alt']] for x in variants],
                blockers=['synthetic_failure'] if blocked else [], decoys=[],
                input_candidate_hypotheses=10, input_hypothesis_genes=['TARGET'] + ['D' + str(i) for i in range(9)],
                input_candidate_alleles=20 if pair else 10)


def mode(value=0.5, variants=None, name='AUTOSOMAL_RECESSIVE'):
    return dict(combinedScore=value, modeOfInheritance=name,
                contributingVariants=[allele()] if variants is None else variants)


def gene(name='TARGET', value=0.5, variants=None, modes=None):
    return dict(geneSymbol=name, combinedScore=value,
                variantEvaluations=[allele()] if variants is None else variants,
                geneScores=[mode(value)] if modes is None else modes)


class ArithmeticControls(unittest.TestCase):
    def test_worst_tie_crosses_top1_and_top5(self):
        rows = [gene('TARGET')] + [gene('D' + str(i)) for i in range(5)]
        r = v.derive(case(), 'original', rows)
        self.assertEqual((r['rank_min'], r['rank_max']), (1, 6))
        self.assertEqual(r['recovered'], {'1': False, '5': False, '10': True})
        self.assertEqual(r['reciprocal_rank'], Fraction(1, 6))

    def test_only_passed_gene_universe(self):
        r = v.derive(case(), 'original', [gene(), gene('FILTERED', 1, [allele(passed=False)])])
        self.assertEqual((r['emitted_gene_universe'], r['filtered_gene_universe'], r['rank_max']), (2, 1, 1))

    def test_excluded_gene_still_requires_finite_score(self):
        r = v.derive(case(), 'original', [gene(), gene('BAD', float('nan'), [])])
        self.assertEqual(r['status'], 'invalid_output')
        self.assertEqual(r['gene_only_reciprocal_rank'], 0)

    def test_duplicate_symbol_invalidates_whole_output(self):
        r = v.derive(case(), 'original', [gene(), gene()])
        self.assertEqual(r['status'], 'invalid_output')

    def test_missing_gene_scalar_is_not_default_zero(self):
        g = gene()
        del g['combinedScore']
        self.assertEqual(v.derive(case(), 'original', [g])['status'], 'invalid_output')

    def test_empty_completed_output_is_nonrecovery(self):
        r = v.derive(case(), 'original', [])
        self.assertEqual((r['status'], r['emitted_gene_universe']), ('not_scored', 0))
        self.assertFalse(r['all_source_alleles_in_any_best_mode'])

    def test_preparation_failure_stays_in_ledger(self):
        r = v.derive(case(blocked=True), 'none', [gene()])
        self.assertEqual(r['status'], 'preparation_failed')
        self.assertIsNone(r['all_source_alleles_in_any_best_mode'])
        self.assertEqual(r['reciprocal_rank'], 0)

    def test_missing_output_is_not_an_empty_output(self):
        r = v.derive(case(), 'none', [], unavailable='missing_output')
        self.assertEqual(r['status'], 'missing_output')
        self.assertIsNone(r['emitted_gene_universe'])
        self.assertIsNone(r['all_source_alleles_in_any_best_mode'])

    def test_failed_second_allele_keeps_gene_only(self):
        r = v.derive(case(True), 'original', [gene(variants=[allele(), allele(2, False)])])
        self.assertEqual(r['gene_only_reciprocal_rank'], 1)
        self.assertEqual(r['reciprocal_rank'], 0)
        self.assertEqual(r['status'], 'source_allele_failed_or_unrepresented')

    def test_duplicate_exact_match_does_not_pass(self):
        r = v.derive(case(), 'original', [gene(variants=[allele(), allele()])])
        self.assertFalse(r['all_source_alleles_passed'])

    def test_no_union_across_best_modes(self):
        g = gene(variants=[allele(), allele(2)], modes=[mode(variants=[allele()]), mode(variants=[allele(2)], name='AUTOSOMAL_DOMINANT')])
        r = v.derive(case(True), 'original', [g])
        self.assertEqual(r['reciprocal_rank'], 1)
        self.assertTrue(r['all_source_alleles_contribute'])
        self.assertFalse(r['all_source_alleles_in_any_best_mode'])
        self.assertEqual(r['joint_best_reciprocal_rank'], 0)

    def test_lower_mode_with_both_alleles_cannot_rescue(self):
        g = gene(variants=[allele(), allele(2)], modes=[mode(), mode(.4, [allele(), allele(2)])])
        self.assertFalse(v.derive(case(True), 'original', [g])['all_source_alleles_in_any_best_mode'])

    def test_any_best_is_distinct_from_every_best(self):
        g = gene(variants=[allele(), allele(2)], modes=[mode(), mode(variants=[allele(), allele(2)])])
        r = v.derive(case(True), 'original', [g])
        self.assertTrue(r['all_source_alleles_in_any_best_mode'])
        self.assertFalse(r['all_source_alleles_in_every_best_mode'])
        self.assertEqual(r['joint_best_reciprocal_rank'], 1)

    def test_missing_contribution_evidence_is_unknown(self):
        g = gene()
        del g['geneScores'][0]['contributingVariants']
        del g['variantEvaluations'][0]['contributesToGeneScore']
        r = v.derive(case(), 'original', [g])
        self.assertIsNone(r['all_source_alleles_contribute'])
        self.assertIsNone(r['all_source_alleles_in_any_best_mode'])
        self.assertEqual(r['joint_best_reciprocal_rank'], 0)

    def test_absent_modes_unknown(self):
        self.assertIsNone(v.derive(case(), 'original', [gene(modes=[])])['all_source_alleles_in_any_best_mode'])

    def test_omitted_zero_mode_original_invalid_corrected_valid(self):
        g = gene()
        g['geneScores'].append({'modeOfInheritance': 'ANY', 'contributingVariants': []})
        self.assertEqual(v.derive(case(), 'original', [g], corrected=False)['status'], 'invalid_output')
        self.assertEqual(v.derive(case(), 'original', [g])['reciprocal_rank'], 1)

    def test_omitted_zero_can_be_best_at_zero_gene_score(self):
        g = gene(value=0)
        del g['geneScores'][0]['combinedScore']
        self.assertEqual(v.derive(case(), 'none', [g])['joint_best_reciprocal_rank'], 1)

    def test_explicit_null_bool_nonfinite_mode_remain_invalid(self):
        for bad in (None, True, float('inf'), float('nan')):
            with self.subTest(value=bad):
                g = gene(modes=[mode(bad)])
                self.assertEqual(v.derive(case(), 'original', [g])['status'], 'invalid_output')

    def test_mode_above_reported_best_is_invalid(self):
        self.assertEqual(v.derive(case(), 'none', [gene(modes=[mode(.9)])])['status'], 'invalid_output')

    def test_absent_variant_evidence_unknown(self):
        g = gene()
        del g['variantEvaluations']
        r = v.derive(case(), 'none', [g])
        self.assertIsNone(r['all_source_alleles_contribute'])
        self.assertEqual(r['gene_only_reciprocal_rank'], 0)

    def test_failed_only_gene_in_gene_macro(self):
        good = v.derive(case(), 'original', [gene()])
        failure = v.derive(case(blocked=True), 'original', [])
        failure['gene'] = 'OTHER'
        result = v.summarize([good, copy.deepcopy(good), failure])
        endpoint = result['primary_full_source_allele_recovery']
        self.assertEqual(endpoint['case_mrr'], Fraction(2, 3))
        self.assertEqual(endpoint['gene_macro_mrr'], Fraction(1, 2))
        self.assertEqual(result['gene_denominator'], 2)


class IntegrityControls(unittest.TestCase):
    def test_running_failed_or_missing_terminal_receipt_rejected(self):
        good = dict(status='completed', exit_code=0, planned_jobs=1418, started_utc='start', finished_utc='end',
                    missing_outputs=[], outputs={str(i): 'x' for i in range(1418)})
        v.terminal(good)
        for change in ({'status': 'running'}, {'status': 'failed', 'exit_code': 1},
                       {'missing_outputs': ['x']}, {'outputs': {}}, {'finished_utc': None}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                v.terminal(dict(good, **change))

    def test_path_escape_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a').write_text('ok')
            (root / 'link').symlink_to(root / 'a')
            self.assertEqual(v.local(root, 'a'), root / 'a')
            for name in ('../a', '/a', 'link', './a', 'x/../a', 'x\\a'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    v.local(root, name)

    def test_changed_hash_extra_missing_files_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'raw').write_bytes(b'original\n')
            (root / 'export-receipt.json').write_text(json.dumps({
                'schema': 'compact713-portable-v1', 'file_sha256': {'raw': v.sha(root / 'raw')}}))
            v.checked_inventory(root)
            (root / 'raw').write_bytes(b'changed\n')
            with self.assertRaises(ValueError):
                v.checked_inventory(root)
            (root / 'raw').write_bytes(b'original\n')
            (root / 'extra').write_text('extra')
            with self.assertRaises(ValueError):
                v.checked_inventory(root)
            (root / 'extra').unlink()
            (root / 'raw').unlink()
            with self.assertRaises(ValueError):
                v.checked_inventory(root)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            v.loads('{"geneSymbol":"A","geneSymbol":"B"}')

    def test_metric_and_boolean_tampering_rejected(self):
        v.compare({'mrr': Fraction(1, 3)}, {'mrr': 1 / 3})
        for actual in ({'mrr': .34}, {'mrr': True}):
            with self.assertRaises(ValueError):
                v.compare({'mrr': Fraction(1, 3)}, actual)
        with self.assertRaises(ValueError):
            v.compare({'count': 1}, {'count': True})

    def test_export_guard_creates_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work, out = root / 'work', root / 'out'
            work.mkdir()
            (work / 'execution.json').write_text('{"status":"running"}')
            args = (work, out, root, root / 'cases', root / 'old', root / 'new', root / 'correction')
            for ready in (False, True):
                with self.assertRaises(ValueError):
                    export.export_bundle(*args, parent_ready=ready)
                self.assertFalse(out.exists())
            out.mkdir()
            (out / 'sentinel').write_text('keep')
            with self.assertRaises(ValueError):
                export.export_bundle(*args, parent_ready=True)
            self.assertEqual((out / 'sentinel').read_text(), 'keep')


def synthetic_cases():
    """Independent fixed-denominator fixture; these are not real cohort records."""
    specifications = [(f'A{i}', False, True, False) for i in range(41)]
    specifications += [(f'A{i}', False, True, False) for i in range(23)]
    specifications += [(f'A{i}', False, False, True) for i in range(41, 45)]
    specifications += [(f'A{i}', False, False, False) for i in range(45, 245)]
    specifications += [(f'A{i}', False, False, True) for i in (45, 45, 46, 46, 47, 47, 48)]
    specifications += [(f'A{45 + i % 200}', False, False, False) for i in range(406)]
    for i, count in enumerate([3, 3, 2, 2, 2] + [2] * 9 + [1] * 2):
        specifications += [(f'X{i}', True, False, j < (2 if i < 2 else 1 if i < 5 else 0)) for j in range(count)]
    result = []
    for i, (symbol, x, pair, fallback) in enumerate(specifications):
        c = case(pair)
        c.update(case_id=f'TC_{i:016x}', gene=symbol,
                 causal_variants=[source(10 * i + j + 1, 'X' if x else '1') for j in range(2 if pair else 1)],
                 decoys=[{'matching_tier': 'type_only' if fallback else 'type_and_consequence'}],
                 source_metadata={'externalReferences': [{'id': 'PMID:' + ('37054711' if i % 322 == 0 else str(i % 322))}]})
        c['signature'] = [[a['chrom'], a['pos'], a['ref'], a['alt']] for a in c['causal_variants']]
        c['blockers'] = ['synthetic_failure'] if i >= 709 else []
        result.append(c)
    return result


def manual_evaluation(cases, raw_hashes):
    """Known-answer fixture: every executable target ranks 1; four cases fail.

    Does not call verifier ranking or aggregation to construct the expected metrics.
    """
    rows = []
    for c in cases:
        for arm in ('original', 'none'):
            good = not c['blockers']
            row = dict(case_id=c['case_id'], gene=c['gene'], arm=arm,
                       technical_X=c['causal_variants'][0]['chrom'] == 'X', pair=len(c['signature']) == 2,
                       fallback=c['decoys'][0]['matching_tier'] == 'type_only',
                       input_hypotheses=10, input_hypothesis_gene_count=10,
                       input_alleles=c['input_candidate_alleles'], rank_min=1 if good else None,
                       rank_max=1 if good else None, all_source_alleles_passed=good,
                       all_source_alleles_contribute=True if good else None,
                       all_source_alleles_in_any_best_mode=True if good else None,
                       all_source_alleles_in_every_best_mode=True if good else None,
                       filtered_gene_universe=1 if good else None, emitted_gene_universe=1 if good else None,
                       status='scored' if good else 'preparation_failed')
            for success, rr in [('recovered', 'reciprocal_rank'), ('gene_only_recovered', 'gene_only_reciprocal_rank'),
                                ('joint_best_recovered', 'joint_best_reciprocal_rank')]:
                row[success] = {'1': good, '5': good, '10': good}
                row[rr] = float(good)
            if good:
                row.update(scored_genes=1, combined_score=0.5, priority_score=None, variant_score=None,
                           output_sha256=raw_hashes[c['case_id'], arm])
            rows.append(row)
    selectors = {'all_713': lambda r: True, 'primary_autosomal_681': lambda r: not r['technical_X'],
                 'technical_X_32': lambda r: r['technical_X'], 'fallback_18': lambda r: r['fallback'],
                 'without_fallback_695': lambda r: not r['fallback'], 'pairs_64': lambda r: r['pair']}
    strata = {}
    for name, select in selectors.items():
        strata[name] = {}
        for arm in ('original', 'none'):
            selected = [r for r in rows if r['arm'] == arm and select(r)]
            groups = defaultdict(list)
            for r in selected:
                groups[r['gene']].append(r['status'] == 'scored')
            n, count = len(selected), sum(r['status'] == 'scored' for r in selected)
            macro = sum(Fraction(sum(values), len(values)) for values in groups.values()) / len(groups)
            summary = dict(case_denominator=n, gene_denominator=len(groups),
                           status_counts=dict(Counter(r['status'] for r in selected)),
                           source_alleles_all_passed_cases=count, source_alleles_all_contribute_cases=count,
                           joint_best_mode_unknown_cases=n-count)
            for endpoint in ('primary_full_source_allele_recovery', 'secondary_gene_only', 'secondary_joint_best_mode_recovery'):
                summary[endpoint] = dict(top_k_counts={k: count for k in ('1', '5', '10')},
                    case_top_k_rates={k: count / n for k in ('1', '5', '10')}, case_mrr=count / n,
                    gene_macro_top_k_rates={k: float(macro) for k in ('1', '5', '10')}, gene_macro_mrr=float(macro))
            strata[name][arm] = summary
    return dict(all_case_arm_results=rows, all_strata=strata)


def fixture(root):
    """Full 713/1418 portable fixture with synthetic provenance and no external data."""
    root = root.resolve()
    project, work = root / 'project', root / 'public/runs/test'
    temporal = project / 'pipeline/public_validation/temporal_compact'
    correction_dir = temporal / 'correction-v2'
    reused = project / 'repo/examples/public-benchmark'

    def put(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, indent=2) + '\n' if not isinstance(content, str) else content)
        return v.sha(path)

    cases, jobs, raw_hashes, inputs, outputs = synthetic_cases(), [], {}, {}, {}
    for c in cases:
        c['draft_vcf_sha256'] = put(work / 'inputs' / (c['case_id'] + '.vcf'), 'synthetic public fixture\n')
        if c['blockers']:
            continue
        variants = [dict(contigName=a['chrom'], start=a['pos'], ref=a['ref'], alt=a['alt'],
                         filterStatus='PASSED', contributesToGeneScore=True) for a in c['causal_variants']]
        for arm in ('original', 'none'):
            stem = c['case_id'] + '.' + arm
            job_path, raw_path = work / 'jobs' / (stem + '.yml'), work / 'results' / (stem + '.jsonl')
            job_sha = put(job_path, 'synthetic job\n')
            raw_sha = put(raw_path, json.dumps(gene(c['gene'], variants=variants,
                                                   modes=[mode(variants=variants)])) + '\n')
            raw_hashes[c['case_id'], arm] = raw_sha
            j = dict(case_id=c['case_id'], gene=c['gene'], arm=arm,
                     primary_autosomal=c['causal_variants'][0]['chrom'] != 'X',
                     job=str(job_path), job_sha256=job_sha, result_jsonl=str(raw_path),
                     vcf=str(work / 'inputs' / (c['case_id'] + '.vcf')), vcf_sha256=c['draft_vcf_sha256'])
            jobs.append(j)
            outputs[str(raw_path)] = raw_sha
            inputs.update({j['job']: job_sha, j['vcf']: j['vcf_sha256']})
    case_path = temporal / 'draft-01/cases.planned.json'
    case_hash = put(case_path, {'state': 'SYNTHETIC', 'cases': cases})
    put(work / 'cases.json', case_path.read_text())
    manifest_hash = put(work / 'jobs-manifest.json', jobs)
    codes = {}
    for name in ('evaluate.py', 'export_results.py', 'run.py', 'export_provenance.py'):
        codes[name] = put(reused / name, '# synthetic provenance only: ' + name + '\n')
    old_adapter = put(temporal / 'evaluate_adapter.py', '# original adapter\n')
    old_helper = put(temporal.parent / 'evaluate_temporal_compact.py', '# original helper\n')
    new_adapter = put(correction_dir / 'evaluate_adapter.py', '# corrected adapter\n')
    new_helper = put(correction_dir / 'joint_mode.py', '# corrected helper\n')
    for stem, old, new in [('adapter', temporal / 'evaluate_adapter.py', correction_dir / 'evaluate_adapter.py'),
                           ('helper', temporal.parent / 'evaluate_temporal_compact.py', correction_dir / 'joint_mode.py')]:
        put(correction_dir / (stem + '.diff'), ''.join(difflib.unified_diff(old.read_text().splitlines(True),
            new.read_text().splitlines(True), fromfile='frozen/' + stem, tofile='correction-v2/' + stem)))
    evidence = {name: put(correction_dir / name, 'synthetic bytecode evidence\n') for name in ('installed-GeneScore-javap.txt', 'installed-JsonResultsWriter-javap.txt')}
    corr_hash = put(correction_dir / 'correction-receipt.json', dict(frozen_adapter_sha256=old_adapter,
        frozen_helper_sha256=old_helper, frozen_case_manifest_sha256=case_hash,
        corrected_component_sha256={'evaluate_adapter.py': new_adapter, 'joint_mode.py': new_helper}, evidence_sha256=evidence))
    probe = correction_dir / 'serialization-probe'
    probe_code = put(probe / 'ModeScoreProbe.java', '// synthetic probe\n')
    probe_output = put(probe / 'output.txt', 'synthetic probe result\n')
    put(probe / 'receipt.json', dict(exit_code=0, code_sha256=probe_code, stdout_sha256=probe_output,
                                   library_sha256={'pipeline/example.jar': 'a' * 64}))
    put(temporal / 'source-reading-crosscheck.json', dict(case_manifest_sha256=case_hash,
        reading_ledger_sha256='b' * 64, source_publication_count=322, existing_main_text_read_overlap=['37054711'],
        source_publications_not_in_main_text_read_ledger=[str(i) for i in range(1, 322)]))
    protocol = dict(state='FROZEN_BEFORE_INFERENCE', arms=['original', 'none'], planned_jobs=1418,
        preparation_failures_per_arm=4, intended_case_arm_denominator=1426, case_manifest_sha256=case_hash,
        temporal_evaluator_sha256=old_adapter, joint_mode_helper_sha256=old_helper,
        reused_evaluation_sha256={name: codes[name] for name in ('evaluate.py', 'export_results.py')})
    put(work / 'protocol-before-inference.json', protocol)
    put(work / 'runtime.properties', 'synthetic=true\n')
    put(work / 'batch.txt', ''.join('--analysis ' + j['job'] + '\n' for j in jobs))
    prep = dict(scientific_input_changes=[], files_sha256={name: v.sha(work / name) for name in
        ('cases.json', 'jobs-manifest.json', 'runtime.properties', 'batch.txt', 'protocol-before-inference.json')})
    put(work / 'preparation-receipt.json', prep)
    log_hash = put(work / 'execution.log', 'synthetic completion\n')
    data_path = work.parents[1] / 'data-receipt.json'
    put(data_path, {'synthetic': True})
    execution = dict(status='completed', exit_code=0, started_utc='start', finished_utc='finish',
        planned_jobs=1418, missing_outputs=[], outputs=outputs, inputs_sha256=inputs, jobs_manifest_sha256=manifest_hash,
        wrapper_sha256=codes['run.py'], evaluation_script_sha256=codes['evaluate.py'],
        design_records={name: dict(sha256=v.sha(work/name), content=v.read_json(work/name)) for name in
                        ('protocol-before-inference.json', 'preparation-receipt.json')},
        pre_inference_addenda={}, properties_sha256=v.sha(work/'runtime.properties'), properties_text='synthetic=true\n',
        batch_sha256=v.sha(work/'batch.txt'), log_sha256=log_hash,
        software_sha256={str(project/'pipeline/example.jar'): 'a'*64},
        data_receipts={str(data_path): dict(sha256=v.sha(data_path), content=v.read_json(data_path))})
    exec_hash = put(work / 'execution.json', execution)
    evaluation = manual_evaluation(cases, raw_hashes)
    evaluation.update(execution_status='completed', execution_sha256=exec_hash, case_manifest_sha256=case_hash,
                      evaluator_sha256=old_adapter)
    old_path = temporal / 'evaluation-20261024.json'
    put(old_path, evaluation)
    evaluation.update(evaluator_sha256=new_adapter, analysis_version='post-freeze-correction-v2',
        correction_receipt_sha256=corr_hash, frozen_evaluator_sha256=old_adapter,
        frozen_helper_sha256=old_helper, corrected_helper_sha256=new_helper)
    new_path = correction_dir / 'evaluation-20261024.json'
    put(new_path, evaluation)
    return (work, root / 'bundle', project, case_path, old_path, new_path, correction_dir), case_hash


class FullBundleControl(unittest.TestCase):
    def test_synthetic_full_ledger_export_move_verify_and_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args, case_hash = fixture(root)
            with patch.object(v, 'CASE_SHA', case_hash):
                result = export.export_bundle(*args, parent_ready=True)
                self.assertEqual((result['raw_outputs'], result['case_arm_rows']), (1418, 1426))
                with self.assertRaises(ValueError):
                    export.export_bundle(*args, parent_ready=True)
                bundle = args[1]
                relocated = root / 'relocated'
                bundle.rename(relocated)
                # Original paths no longer resolve: verification must stay offline.
                args[0].rename(root / 'hidden-work')
                verified = v.verify_bundle(relocated)
                self.assertEqual(verified['correction_affected_case_arms'], [])
                self.assertEqual(verified['all_strata']['corrected-v2']['all_713']['original']
                                 ['primary_full_source_allele_recovery']['case_mrr'], Fraction(709, 713))
                for name in ('raw/TC_0000000000000000.original.jsonl', 'jobs-manifest.json',
                             'correction-v2/serialization-probe/output.txt', 'evaluations/corrected-v2.json'):
                    path = relocated / name
                    before = path.read_bytes()
                    path.write_bytes(before + b' ')
                    with self.subTest(file=name), self.assertRaises(ValueError):
                        v.verify_bundle(relocated)
                    path.write_bytes(before)
                # Rehashed raw tampering still fails the original execution SHA link.
                raw = relocated / 'raw/TC_0000000000000000.original.jsonl'
                raw.write_bytes(raw.read_bytes() + b' ')
                receipt = v.read_json(relocated / 'export-receipt.json')
                receipt['file_sha256'][raw.relative_to(relocated).as_posix()] = v.sha(raw)
                (relocated / 'export-receipt.json').write_text(json.dumps(receipt))
                with self.assertRaisesRegex(ValueError, 'Raw output differs'):
                    v.verify_bundle(relocated)

    def test_duplicate_and_missing_jobs_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            args, _ = fixture(Path(directory))
            cases = v.read_json(args[3])['cases']
            jobs = v.read_json(args[0] / 'jobs-manifest.json')
            v.ledger(cases, jobs)
            for changed in (jobs[:-1], jobs[:-1] + [jobs[0]]):
                with self.assertRaises(ValueError):
                    v.ledger(cases, changed)


if __name__ == '__main__':
    unittest.main()
