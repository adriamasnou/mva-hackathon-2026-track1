"""Run separately with pinned scientific Python; never skipped by root discovery.

All fixtures deterministic. These tests do not execute simulated experiments.
"""
from pathlib import Path
import sys
import unittest
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy.stats import ttest_ind
from runtime import critical_values
from simulate import culture_arrays, intervals, summarize


class NumericSidecarTests(unittest.TestCase):
    def test_critical_value_order(self):
        df = np.array([5.0, 5.5, 10, 22])
        u, b = critical_values(df), critical_values(df, family_size=4)
        self.assertTrue(np.all(b > u))
        self.assertTrue(np.all(np.diff(u) < 0))
        self.assertAlmostEqual(u[0], 2.570581835636314, places=10)

    def test_welch_interval_matches_scipy_direct_sample_test(self):
        c = np.array([[5, 10, 20, 35, 55, 80]])
        t = np.array([[[0, 2, 7, 20, 30, 55], [4, 12, 21, 34, 50, 71],
                       [3, 6, 9, 20, 21, 22], [3, 3, 3, 3, 3, 3]]])
        computed = culture_arrays(c, t, 150)
        for family in (1, 4):
            observed = intervals(computed, family, .05)
            for j in range(4):
                reference = ttest_ind(c[0] / 150, t[0, j] / 150, equal_var=False)
                ci = reference.confidence_interval(confidence_level=1 - .05 / family)
                self.assertAlmostEqual(observed["lower"][0, j], ci.low, places=12)
                self.assertAlmostEqual(observed["upper"][0, j], ci.high, places=12)
                self.assertAlmostEqual(computed["df"][0, j], reference.df, places=12)

    def test_shared_control_is_reused_for_each_contrast(self):
        controls = np.array([[10, 20, 30, 40, 50, 60], [15, 25, 35, 45, 55, 65]])
        treatments = np.broadcast_to(np.array([1, 2, 3, 4, 5, 6]), (2, 4, 6)).copy()
        actual = culture_arrays(controls, treatments, 150)
        self.assertTrue(np.all(actual["benefit"][:, :1] == actual["benefit"]))
        np.testing.assert_allclose(actual["benefit"][1] - actual["benefit"][0], 5 / 150)
        expected = (controls / 150).var(axis=1, ddof=1)[:, None] / 6 + (treatments / 150).var(axis=2, ddof=1) / 6
        np.testing.assert_allclose(actual["variance"], expected, rtol=1e-14)

    def test_zero_variance_is_explicitly_indeterminate(self):
        c = np.full((2, 6), 30)
        t = np.zeros((2, 4, 6), dtype=int)
        s = culture_arrays(c, t, 150)
        for family in (1, 4):
            ci = intervals(s, family, .05)
            self.assertTrue(np.all(s["zero_total_variance"]))
            self.assertTrue(np.all(ci["indeterminate"]))
            self.assertFalse(np.any(ci["candidate"] | ci["reject"] | ci["inconclusive"]))

    def test_invalid_counts_and_degrees_rejected(self):
        for x in (float("nan"), -1, 151, .5):
            c = np.full((1, 6), x)
            with self.assertRaises(ValueError):
                culture_arrays(c, np.zeros((1, 4, 6)), 150)
        for df in (0, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                critical_values(df)

    def test_bonferroni_interval_nesting(self):
        c = np.array([[10, 15, 20, 25, 30, 35]])
        t = np.array([[[0, 2, 4, 6, 8, 10], [0, 4, 8, 12, 16, 20],
                       [10, 20, 30, 40, 50, 60], [30, 40, 50, 60, 70, 80]]])
        s = culture_arrays(c, t, 150)
        u, b = intervals(s, 1, .05), intervals(s, 4, .05)
        self.assertTrue(np.all(b["lower"] < u["lower"]))
        self.assertTrue(np.all(b["upper"] > u["upper"]))
        self.assertFalse(np.any(b["candidate"] & ~u["candidate"]))

    def test_family_events_use_experiments_and_truth_threshold(self):
        # Two fixed experiments, with a false advance in only the first.
        candidate = np.array([[True, False, True, True], [False, False, False, True]])
        lo = np.where(candidate, .06, -.1)
        hi = np.where(candidate, .2, .05)
        ci = {"candidate": candidate, "reject": np.zeros((2, 4), dtype=bool),
              "inconclusive": ~candidate, "indeterminate": np.zeros((2, 4), dtype=bool),
              "lower": lo, "upper": hi}
        result = summarize({"benefit": np.zeros((2, 4))}, ci, [0, .025, .075, .15], .05)
        family = result["family"]
        self.assertEqual(family["false_advancement_true_benefit_le_delta"]["count"], 1)
        self.assertEqual(family["false_advancement_true_benefit_le_delta"]["trials"], 2)
        self.assertEqual(family["any_above_threshold_candidate_true_benefit_gt_delta"]["count"], 2)
        self.assertEqual(family["all_above_threshold_candidates_true_benefit_gt_delta"]["count"], 1)
        self.assertEqual(family["candidate_count_distribution"][1]["count"], 1)
        self.assertEqual(family["candidate_count_distribution"][3]["count"], 1)
        self.assertFalse(result["contrasts"][1]["detected_true_benefit_gt_delta"]["applicable"])
        self.assertTrue(result["contrasts"][1]["detected_true_benefit_gt_zero"]["applicable"])
        at_threshold = summarize({"benefit": np.zeros((2, 4))}, ci, [.05] * 4, .05)
        self.assertEqual(at_threshold["family"]["false_advancement_true_benefit_le_delta"]["count"], 2)
        self.assertFalse(at_threshold["family"]["any_above_threshold_candidate_true_benefit_gt_delta"]["applicable"])

    def test_invalid_coverage_denominator_is_explicit(self):
        invalid = np.array([[True, False, False, False], [False, False, False, False]])
        ci = {"candidate": np.zeros((2, 4), dtype=bool), "reject": np.zeros((2, 4), dtype=bool),
              "inconclusive": ~invalid, "indeterminate": invalid,
              "lower": np.full((2, 4), -.1), "upper": np.full((2, 4), .2)}
        result = summarize({"benefit": np.zeros((2, 4))}, ci, [0] * 4, .05)
        self.assertEqual(result["contrasts"][0]["marginal_coverage_all_experiments"]["count"], 1)
        self.assertEqual(result["contrasts"][0]["marginal_coverage_all_experiments"]["trials"], 2)
        self.assertEqual(result["contrasts"][0]["marginal_coverage_given_valid"]["trials"], 1)
        self.assertEqual(result["family"]["simultaneous_coverage_all_experiments"]["count"], 1)
        self.assertEqual(result["family"]["simultaneous_coverage_given_all_valid"]["trials"], 1)


if __name__ == "__main__":
    unittest.main()
