"""Standard-library sidecar tests; no simulation or optional dependency imports."""
import math
from pathlib import Path
import statistics
import sys
import unittest

sys.dont_write_bytecode = True
SIDE = Path(__file__).resolve().parents[1] / "analysis/rescue_decision/simulation"
sys.path.insert(0, str(SIDE))
import math_helpers as h


class RescueSimulationMathTests(unittest.TestCase):
    def test_strict_threshold_touch(self):
        for lo, hi, expected in ((.05, .08, "inconclusive"), (.01, .05, "inconclusive"),
                                 (.05, .05, "inconclusive"), (.050001, .08, "candidate"),
                                 (.01, .049999, "reject")):
            self.assertEqual(h.classify(lo, hi), expected)

    def test_decimal_boundary_has_no_tolerance(self):
        self.assertEqual(h.classify("0.05000000000000000001", "0.06"), "candidate")

    def test_invalid_interval_is_indeterminate(self):
        for lo, hi in ((.1, .0), (float("nan"), .1), (0, float("inf")), (None, .1)):
            self.assertEqual(h.classify(lo, hi), "indeterminate")

    def test_cells_are_not_independent_replicates(self):
        # Six cultures at 0 or 50% error: sample variance 0.075, mean variance .0125.
        s = h.culture_summary([0, 0, 0, 75, 75, 75])
        self.assertEqual(s["n"], 6)
        self.assertAlmostEqual(s["mean"], .25)
        self.assertAlmostEqual(s["sample_variance"], .075)
        self.assertAlmostEqual(s["sample_variance"] / s["n"], .0125)
        cell_pseudoreplicate_variance = .25 * .75 / (6 * 150)
        self.assertGreater(s["sample_variance"] / s["n"], 50 * cell_pseudoreplicate_variance)

    def test_equal_culture_proportions_not_cell_count_drive_se(self):
        a = h.welch_components([0, 15, 30, 45, 60, 75], [0, 0, 15, 15, 30, 30])
        b = h.welch_components([0, 30, 60, 90, 120, 150], [0, 0, 30, 30, 60, 60], 300)
        for key in ("benefit", "variance_of_difference", "se", "df"):
            self.assertAlmostEqual(a[key], b[key])

    def test_zero_total_variance_indeterminate(self):
        result = h.welch_components([30] * 6, [0] * 6)
        self.assertEqual(result["status"], "zero_total_variance")
        self.assertIsNone(result["se"])
        self.assertIsNone(result["df"])

    def test_one_zero_arm_still_has_finite_uncertainty(self):
        result = h.welch_components([30] * 6, [0, 10, 20, 30, 40, 50])
        self.assertEqual(result["status"], "valid")
        self.assertGreater(result["se"], 0)
        self.assertAlmostEqual(result["df"], 5)

    def test_invalid_counts_raise(self):
        for values in ([1], [-1, 3], [151, 3], [float("nan"), 3], [True, 2], [1.0, 2]):
            with self.assertRaises(ValueError):
                h.culture_summary(values)
        with self.assertRaises(ValueError):
            h.culture_summary([1, 2], 0)

    def test_welch_df_and_variance_constructed_from_cultures(self):
        result = h.welch_components([0, 15, 30, 45, 60, 75], [0, 15, 30, 45, 60, 75])
        self.assertEqual(result["benefit"], 0)
        self.assertAlmostEqual(result["df"], 10)
        self.assertAlmostEqual(result["variance_of_difference"], 2 * .035 / 6)

    def test_multiplicity_tail_order(self):
        self.assertAlmostEqual(h.tail_probability(.95, 4), .00625)
        self.assertAlmostEqual(h.tail_probability(.95, 1), .025)
        self.assertLess(h.tail_probability(.95, 4), h.tail_probability(.95, 1))

    def test_wilson_zero_all_midpoint(self):
        self.assertAlmostEqual(h.wilson(50, 100)[0], .4038315303659956, places=12)
        self.assertAlmostEqual(h.wilson(50, 100)[1], .5961684696340044, places=12)
        self.assertEqual(h.wilson(0, 100)[0], 0)
        self.assertGreater(h.wilson(0, 100)[1], 0)
        self.assertAlmostEqual(h.wilson(100, 100)[1], 1)
        for k, n in ((1, 0), (2, 1), (-1, 20)):
            with self.assertRaises(ValueError):
                h.wilson(k, n)

    def test_beta_binomial_variance_and_icc_zero(self):
        self.assertAlmostEqual(h.beta_binomial_proportion_variance(.25, 0), .25 * .75 / 150)
        self.assertAlmostEqual(h.beta_binomial_proportion_variance(.25, .05), .25 * .75 * 8.45 / 150)
        self.assertAlmostEqual(h.shared_control_covariance(.25, .05, 6), .25 * .75 * 8.45 / 900)

    def test_shared_control_covariance_exact_enumeration(self):
        # Complete Cartesian product, no random draws. Cov(C-T1,C-T2)=Var(C).
        pairs = [(c - t1, c - t2) for c in (.1, .3) for t1 in (.1, .2) for t2 in (.15, .25)]
        x, y = zip(*pairs)
        covariance = statistics.fmean((a - statistics.fmean(x)) * (b - statistics.fmean(y)) for a, b in pairs)
        self.assertAlmostEqual(covariance, .01)
        # Independent control draws would remove that covariance.
        pairs2 = [(c1 - t1, c2 - t2) for c1 in (.1, .3) for c2 in (.1, .3)
                  for t1 in (.1, .2) for t2 in (.15, .25)]
        x, y = zip(*pairs2)
        self.assertAlmostEqual(statistics.fmean((a - statistics.fmean(x)) * (b - statistics.fmean(y))
                                               for a, b in pairs2), 0)



if __name__ == "__main__":
    unittest.main()
