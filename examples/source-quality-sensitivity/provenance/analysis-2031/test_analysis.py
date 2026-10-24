"""Synthetic failure-injection tests; no clinical data, network or inference."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import analyze as a


def case():
    return {'case_id': 'case-a', 'gene': 'GENE_A', 'member': 'packet-a.json', 'packet_sha256': 'a' * 64,
            'signature': [['1', 100, 'A', 'G']],
            'causal_variants': [{'chrom': '1', 'pos': 100, 'ref': 'A', 'alt': 'G'}],
            'decoys': [{'matching_tier': 'type_and_consequence'}], 'blockers': [],
            'all_matching_packets': [{'member': 'packet-a.json'}]}


def outcome(c, arm, tied=False):
    scores = [{'geneSymbol': c['gene'], 'combinedScore': 1.0}]
    if tied:
        scores.append({'geneSymbol': 'GENE_B', 'combinedScore': 1.0})
    rank = len(scores)
    return {'case_id': c['case_id'], 'gene': c['gene'], 'arm': arm, **a.tags(c), 'status': 'scored',
            'rank_min': 1, 'rank_max': rank, 'all_source_alleles_passed': True,
            'recovered': {k: rank <= int(k) for k in a.KS}, 'reciprocal_rank': 1/rank,
            'source_allele_audit': {'source_variants': [
                {'source_coordinate': v, 'exact_matches_in_source_gene': 1,
                 'matches': [{'filterStatus': 'PASSED'}]} for v in c['causal_variants']]},
            'gene_scores': scores, 'filtered_gene_universe': len(scores)}


def evaluation(c, tied=False):
    return {'all_case_arm_results': [outcome(c, arm, tied) for arm in a.ARMS]}


def source_packet(c):
    return {'case_id': c['case_id'], 'member': c['member'], 'sha256': c['packet_sha256'],
            'selected_record': True, 'phenotypicFeatures': [{'type': {'id': 'HP:TEST'}}],
            'interpretations': []}


def review_packet(c):
    source = source_packet(c)
    return {'case_id': c['case_id'], 'member': c['member'], 'packet_sha256': c['packet_sha256'],
            'role': 'selected', 'review_status': 'adjudicated', 'category': 'contradicted',
            **{f: {'status': 'supported'} for f in a.DIMENSION_FIELDS},
            'alleles': [], 'phenotypes': [
                {'pointer': '/phenotypicFeatures/0', 'snapshot': source['phenotypicFeatures'][0],
                 'snapshot_sha256': a.canonical_sha(source['phenotypicFeatures'][0]),
                 'assessment': {'status': 'contradicted'}}]}


class LinkageTests(unittest.TestCase):
    def test_valid_pair(self):
        c = case()
        self.assertEqual(len(a.validate_outcomes([c], evaluation(c))), 2)

    def test_duplicate_case_rejected(self):
        c = case()
        with self.assertRaisesRegex(ValueError, 'Duplicate case ID'):
            a.validate_outcomes([c, copy.deepcopy(c)], evaluation(c))

    def test_missing_arm_rejected(self):
        c = case(); e = evaluation(c); e['all_case_arm_results'].pop()
        with self.assertRaisesRegex(ValueError, 'Missing/unexpected outcome'):
            a.validate_outcomes([c], e)

    def test_duplicate_arm_rejected(self):
        c = case(); e = evaluation(c); e['all_case_arm_results'].append(e['all_case_arm_results'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate case/arm'):
            a.validate_outcomes([c], e)

    def test_foreign_case_rejected(self):
        c = case(); e = evaluation(c); e['all_case_arm_results'][0]['case_id'] = 'another-case'
        with self.assertRaisesRegex(ValueError, 'Missing/unexpected outcome'):
            a.validate_outcomes([c], e)

    def test_conservative_tie_top1(self):
        c = case(); e = evaluation(c, tied=True)
        rows = a.validate_outcomes([c], e)
        self.assertEqual(rows[c['case_id'], 'original']['recovered'], {'1': False, '5': True, '10': True})

    def test_conservative_tie_crosses_top5(self):
        r = {'status': 'scored', 'all_source_alleles_passed': True, 'rank_min': 5, 'rank_max': 6}
        self.assertEqual(a.primary_hits(r), {'1': False, '5': False, '10': True})

    def test_wrong_tie_rank_rejected(self):
        c = case(); e = evaluation(c, tied=True); e['all_case_arm_results'][0]['rank_max'] = 1
        with self.assertRaisesRegex(ValueError, 'Exact tie/rank mismatch'):
            a.validate_outcomes([c], e)

    def test_failed_exact_allele_rejected_as_success(self):
        c = case(); e = evaluation(c)
        e['all_case_arm_results'][0]['source_allele_audit']['source_variants'][0]['matches'][0]['filterStatus'] = 'FAILED'
        with self.assertRaisesRegex(ValueError, 'Exact PASSED evidence mismatch'):
            a.validate_outcomes([c], e)

    def test_duplicate_exact_match_cannot_pass(self):
        c = case(); e = evaluation(c)
        v = e['all_case_arm_results'][0]['source_allele_audit']['source_variants'][0]
        v['exact_matches_in_source_gene'] = 2; v['matches'] *= 2
        with self.assertRaisesRegex(ValueError, 'Exact PASSED evidence mismatch'):
            a.validate_outcomes([c], e)

    def test_both_source_alleles_required(self):
        c = case(); c['causal_variants'].append({'chrom': '1', 'pos': 200, 'ref': 'C', 'alt': 'T'})
        e = evaluation(c); e['all_case_arm_results'][0]['source_allele_audit']['source_variants'].pop()
        with self.assertRaisesRegex(ValueError, 'Missing/extra exact source allele'):
            a.validate_outcomes([c], e)

    def test_source_failure_kept_in_both_arm_denominators(self):
        c = case(); e = evaluation(c); c['blockers'] = ['preparation_blocker']
        for r in e['all_case_arm_results']:
            r.update(status='preparation_failed', reasons=c['blockers'], rank_min=None, rank_max=None,
                     all_source_alleles_passed=False, recovered=dict.fromkeys(a.KS, False), reciprocal_rank=0)
        idx = a.validate_outcomes([c], e)
        rows = [{'case_id': c['case_id'], 'gene': c['gene'],
                 'corrected_outcomes': {arm: idx[c['case_id'], arm] for arm in a.ARMS}}]
        result = a.summarize(rows)
        self.assertEqual(result['case_denominator'], 1)
        self.assertEqual(result['paired']['1']['neither_recovered'], 1)
        self.assertEqual(result['arms']['original']['status_counts'], {'preparation_failed': 1})

    def test_invalid_output_kept_failure_even_with_pass_flag(self):
        self.assertFalse(any(a.primary_hits({'status': 'invalid_output', 'all_source_alleles_passed': True,
                                            'rank_min': None, 'rank_max': None}).values()))

    def test_failed_case_cannot_be_promoted(self):
        c = case(); e = evaluation(c); c['blockers'] = ['preparation_blocker']
        with self.assertRaisesRegex(ValueError, 'Preparation failure lost'):
            a.validate_outcomes([c], e)

    def test_missing_and_changed_hash_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'input'; p.write_bytes(b'frozen'); digest = a.sha(p)
            a.check_hash(p, digest); p.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                a.check_hash(p, digest)
            p.unlink()
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                a.check_hash(p, digest)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON'):
            json.loads('{"case_id":"a","case_id":"b"}', object_pairs_hook=a.unique_object)

    def test_packet_hash_mismatch_rejected(self):
        c = case(); p = review_packet(c); p['packet_sha256'] = 'b' * 64
        with self.assertRaisesRegex(ValueError, 'packet/member/hash mismatch'):
            a.validate_packet_binding(p, source_packet(c), '00000000')

    def test_item_hash_mismatch_rejected(self):
        c = case(); p = review_packet(c); p['phenotypes'][0]['snapshot_sha256'] = 'b' * 64
        with self.assertRaisesRegex(ValueError, 'snapshot hash/content mismatch'):
            a.validate_packet_binding(p, source_packet(c), '00000000')

    def test_missing_phenotype_mapping_rejected(self):
        c = case(); p = review_packet(c); p['phenotypes'] = []
        with self.assertRaisesRegex(ValueError, 'Missing/extra source item'):
            a.validate_packet_binding(p, source_packet(c), '00000000')

    def test_duplicate_phenotype_mapping_rejected(self):
        c = case(); p = review_packet(c); p['phenotypes'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate packet item'):
            a.validate_packet_binding(p, source_packet(c), '00000000')

    def test_pending_is_unreviewed_not_raw_qualified(self):
        p = review_packet(case()); p['review_status'] = 'pending'; p['category'] = 'qualified'
        self.assertEqual(set(a.selection_annotation(p).values()), {'unreviewed'})
        self.assertEqual(p['category'], 'qualified')

    def test_phenotype_contradiction_not_genotype_or_causal_contradiction(self):
        p = review_packet(case()); s = a.selection_annotation(p)
        self.assertEqual(s['selected_packet_category'], 'contradicted')
        self.assertEqual(s['selected_phenotype_contradiction'], 'present')
        self.assertEqual(s['selected_genotype_status'], 'supported')
        self.assertEqual(s['selected_causal_confidence'], 'supported')

    def test_unresolved_without_contradiction_is_none_recorded_not_supported(self):
        p = review_packet(case()); p['phenotypes'][0]['assessment']['status'] = 'unresolved'
        self.assertEqual(a.selection_annotation(p)['selected_phenotype_contradiction'], 'none_recorded')
        self.assertEqual(p['phenotypes'][0]['assessment']['status'], 'unresolved')

    def test_empty_stratum_has_null_rates_and_explicit_zero_pairs(self):
        result = a.summarize([])
        self.assertEqual(result['arms']['original']['top_k_rates'], dict.fromkeys(a.KS))
        self.assertEqual(result['paired']['1']['paired_case_denominator'], 0)
        self.assertEqual(result['paired']['1']['none_only'], 0)

    def test_both_adverse_and_favorable_discordance_retained(self):
        rows = []
        for i, pair in enumerate([(True, False), (False, True), (False, False), (True, True)]):
            c = case(); c['case_id'] = str(i)
            outcomes = {}
            for arm, value in zip(a.ARMS, pair):
                r = outcome(c, arm); r['recovered'] = dict.fromkeys(a.KS, value); outcomes[arm] = r
            rows.append({'case_id': str(i), 'gene': c['gene'], 'corrected_outcomes': outcomes})
        result = a.summarize(rows)['paired']['1']
        self.assertEqual([result[k] for k in ('both_recovered', 'original_only', 'none_only', 'neither_recovered')], [1,1,1,1])
        self.assertEqual(result['discordant_pair_denominator'], 2)

    def test_completion_does_not_mean_supported(self):
        self.assertEqual(a.completion(2, 2, 2), 'complete')
        self.assertEqual(a.completion(2, 1, 2), 'incomplete')
        self.assertEqual(a.completion(2, 0, 0), 'unreviewed')

    def test_source_mapping_selected_hash_missing_and_duplicate(self):
        c = case(); source = source_packet(c)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'contexts/00000000').mkdir(parents=True)
            (root/'inventory.json').write_text(json.dumps({'case_manifest_sha256': a.CASE_SHA,
                                                         'papers': [{'pmid': '00000000'}]}))
            p = root/'contexts/00000000/source-context.json'
            def write(packets):
                p.write_text(json.dumps({'pmid': '00000000', 'packets': packets}))
            write([source]); a.source_indexes(root, [c], {'papers': []})
            bad = copy.deepcopy(source); bad['sha256'] = 'b'*64; write([bad])
            with self.assertRaisesRegex(ValueError, 'Selected packet member/hash'):
                a.source_indexes(root, [c], {'papers': []})
            write([source, source])
            with self.assertRaisesRegex(ValueError, 'Duplicate context mapping'):
                a.source_indexes(root, [c], {'papers': []})
            write([])
            with self.assertRaisesRegex(ValueError, 'Source/case cohort mismatch'):
                a.source_indexes(root, [c], {'papers': []})

    def test_alternate_missing_and_selected_member_mismatch(self):
        c = case(); source = source_packet(c)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'contexts/00000000').mkdir(parents=True)
            (root/'inventory.json').write_text(json.dumps({'case_manifest_sha256': a.CASE_SHA,
                                                         'papers': [{'pmid': '00000000'}]}))
            p = root/'contexts/00000000/source-context.json'
            p.write_text(json.dumps({'pmid': '00000000', 'packets': [source]}))
            c['all_matching_packets'].append({'member': 'alternate.json'})
            with self.assertRaisesRegex(ValueError, 'Missing/duplicate/extra linked packet'):
                a.source_indexes(root, [c], {'papers': []})
            c['all_matching_packets'].pop(); c['member'] = 'wrong-selected.json'
            with self.assertRaisesRegex(ValueError, 'Selected packet member/hash'):
                a.source_indexes(root, [c], {'papers': []})

    def test_multiple_selected_packets_rejected(self):
        c = case(); first = source_packet(c); second = copy.deepcopy(first)
        second['member'] = 'alternate.json'; c['all_matching_packets'].append({'member': 'alternate.json'})
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'contexts/00000000').mkdir(parents=True)
            (root/'inventory.json').write_text(json.dumps({'case_manifest_sha256': a.CASE_SHA,
                                                         'papers': [{'pmid': '00000000'}]}))
            (root/'contexts/00000000/source-context.json').write_text(json.dumps(
                {'pmid': '00000000', 'packets': [first, second]}))
            with self.assertRaisesRegex(ValueError, 'Selected mapping not unique'):
                a.source_indexes(root, [c], {'papers': []})


if __name__ == '__main__':
    unittest.main()
