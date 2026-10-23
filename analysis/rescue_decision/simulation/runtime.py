"""Optional scientific runtime, isolated from root standard-library tests."""
import numpy as np
from scipy.stats import t
from math_helpers import tail_probability


def critical_values(degrees, confidence=0.95, family_size=1):
    df = np.asarray(degrees, dtype=float)
    if np.any(~np.isfinite(df)) or np.any(df <= 0):
        raise ValueError("finite positive Welch degrees of freedom required")
    result = t.ppf(1 - tail_probability(confidence, family_size), df)
    if np.any(~np.isfinite(result)):
        raise ArithmeticError("non-finite SciPy t critical value")
    return result
