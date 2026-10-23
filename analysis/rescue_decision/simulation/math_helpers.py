"""Standard-library culture statistics and strict threshold classification.

Independent cultures, never individual cells, determine variance and degrees of
freedom. No estimate here is a clinical threshold or a validated assay model.
"""
from decimal import Decimal
import math
from statistics import NormalDist, fmean, variance


def classify(lower, upper, threshold=0.05):
    """Strict boundaries, matching decision.relation; malformed CIs are indeterminate."""
    try:
        lo, hi, delta = (Decimal(str(v)) for v in (lower, upper, threshold))
        if not all(v.is_finite() for v in (lo, hi, delta)) or lo > hi:
            return "indeterminate"
    except Exception:
        return "indeterminate"
    return "candidate" if lo > delta else "reject" if hi < delta else "inconclusive"


def culture_summary(error_counts, completed=150):
    if type(completed) is not int or completed < 1:
        raise ValueError("positive integer completed first divisions required")
    if len(error_counts) < 2 or any(type(v) is not int or not 0 <= v <= completed for v in error_counts):
        raise ValueError("at least two valid independent culture counts required")
    proportions = [v / completed for v in error_counts]
    return {"n": len(proportions), "mean": fmean(proportions),
            "sample_variance": variance(proportions)}


def welch_components(control, treated, completed=150):
    """Returns no degrees of freedom when *total* estimated variance is zero.

    One constant arm and one variable arm have positive SE and the variable arm's
    n-1 degrees of freedom. That case is retained and separately counted.
    """
    c, t = culture_summary(control, completed), culture_summary(treated, completed)
    a, b = c["sample_variance"] / c["n"], t["sample_variance"] / t["n"]
    base = {"benefit": c["mean"] - t["mean"], "control": c, "treated": t,
            "variance_of_difference": a + b}
    if a + b == 0:
        return dict(base, status="zero_total_variance", se=None, df=None)
    return dict(base, status="valid", se=math.sqrt(a + b),
                df=(a + b) ** 2 / (a * a / (c["n"] - 1) + b * b / (t["n"] - 1)))


def tail_probability(confidence=0.95, family_size=1):
    if not 0 < confidence < 1 or type(family_size) is not int or family_size < 1:
        raise ValueError("invalid confidence or family size")
    return (1 - confidence) / (2 * family_size)


def wilson(successes, trials, confidence=0.95):
    if type(successes) is not int or type(trials) is not int or not 0 <= successes <= trials or trials <= 0:
        raise ValueError("invalid binomial Monte Carlo counts")
    z = NormalDist().inv_cdf(1 - tail_probability(confidence))
    p, zz = successes / trials, z * z
    denominator = 1 + zz / trials
    center = (p + zz / (2 * trials)) / denominator
    half = z * math.sqrt(p * (1 - p) / trials + zz / (4 * trials * trials)) / denominator
    return [max(0.0, center - half), min(1.0, center + half)]


def beta_binomial_proportion_variance(p, icc, completed=150):
    if not 0 < p < 1 or not 0 <= icc < 1 or type(completed) is not int or completed < 1:
        raise ValueError("invalid beta-binomial parameters")
    return p * (1 - p) * (1 + (completed - 1) * icc) / completed


def shared_control_covariance(p, icc, n, completed=150):
    if type(n) is not int or n < 2:
        raise ValueError("at least two cultures required")
    return beta_binomial_proportion_variance(p, icc, completed) / n


