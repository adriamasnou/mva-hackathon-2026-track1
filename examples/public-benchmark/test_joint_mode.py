"""Focused stdlib tests for exact allele / joint best-mode evidence only."""
import copy
import unittest

from joint_mode import exact_alleles


class ExactAllelesTests(unittest.TestCase):
    def setUp(self):
        self.case = {'gene': 'TEST', 'causal_variants': [
            {'chrom': '1', 'pos': 10, 'ref': 'A', 'alt': 'G', 'genotype': '0/1'},
            {'chrom': '1', 'pos': 20, 'ref': 'C', 'alt': 'T', 'genotype': '0/1'}]}
        self.variants = [{'contigName': 'chr1', 'start': v['pos'], 'ref': v['ref'], 'alt': v['alt'],
                          'filterStatus': 'PASSED', 'contributesToGeneScore': True}
                         for v in self.case['causal_variants']]

    def mode(self, name, score, indices):
        return {'modeOfInheritance': name, 'combinedScore': score,
                'contributingVariants': [self.variants[i] for i in indices]}

    def record(self, modes):
        return {'geneSymbol': 'TEST', 'combinedScore': 0.8,
                'variantEvaluations': copy.deepcopy(self.variants), 'geneScores': modes}

    def test_global_union_and_lower_full_pair_do_not_prove_best_joint(self):
        record = self.record([self.mode('AD', .8, [0]), self.mode('XD', .8, [1]),
                              self.mode('AR', .7, [0, 1])])
        before = copy.deepcopy(record)
        result = exact_alleles([record], self.case)
        self.assertTrue(result['all_source_alleles_matched'])
        self.assertTrue(result['all_source_alleles_contributing'])
        self.assertFalse(result['all_source_alleles_in_any_best_mode'])
        self.assertFalse(result['all_source_alleles_in_every_best_mode'])
        self.assertEqual(record, before)

    def test_tied_best_any_and_every_are_distinct(self):
        result = exact_alleles([self.record([self.mode('AD', .8, [0]),
                                            self.mode('AR', .8, [0, 1])])], self.case)
        self.assertTrue(result['all_source_alleles_in_any_best_mode'])
        self.assertFalse(result['all_source_alleles_in_every_best_mode'])
        self.assertEqual(sum(m['is_best_score'] for m in result['reported_score_modes']), 2)

    def test_missing_flags_and_mode_lists_remain_unknown(self):
        record = self.record([{'modeOfInheritance': 'AR', 'combinedScore': .8}])
        for variant in record['variantEvaluations']:
            del variant['contributesToGeneScore']
        result = exact_alleles([record], self.case)
        self.assertIsNone(result['all_source_alleles_contributing'])
        self.assertIsNone(result['all_source_alleles_in_any_best_mode'])
        self.assertIsNone(result['all_source_alleles_in_every_best_mode'])
        self.assertEqual(result['mode_evidence_status'], 'incomplete')
        del record['variantEvaluations']
        self.assertIsNone(exact_alleles([record], self.case)['all_source_alleles_matched'])
        record['geneScores'][0]['contributingVariants'] = []
        self.assertFalse(exact_alleles([record], self.case)['all_source_alleles_in_any_best_mode'])

    def test_omitted_primitive_zero_mode_does_not_invalidate_best_mode(self):
        record = self.record([self.mode('AR', .8, [0, 1]), {'modeOfInheritance': 'XD'}])
        result = exact_alleles([record], self.case)
        self.assertTrue(result['all_source_alleles_in_any_best_mode'])
        self.assertEqual(result['reported_score_modes'][1]['combined_score'], 0.0)
        self.assertFalse(result['reported_score_modes'][1]['is_best_score'])
        record['geneScores'][1]['combinedScore'] = None
        with self.assertRaises(ValueError):
            exact_alleles([record], self.case)

    def test_missing_target_is_not_recovered_from_another_gene(self):
        record = self.record([self.mode('AR', .8, [0, 1])])
        record['geneSymbol'] = 'OTHER'
        result = exact_alleles([record], self.case)
        self.assertFalse(result['all_source_alleles_matched'])
        self.assertFalse(result['all_source_alleles_contributing'])
        self.assertFalse(result['all_source_alleles_in_any_best_mode'])
        self.assertEqual(result['mode_evidence_status'], 'source_gene_absent')


if __name__ == '__main__':
    unittest.main()
