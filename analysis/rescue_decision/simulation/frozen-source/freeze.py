#!/usr/bin/env python3
"""Create an exclusive plan/source freeze before any Monte Carlo execution."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sys

sys.dont_write_bytecode = True


def main():
    folder = Path(__file__).resolve().parent
    if (folder / "freeze.json").exists() or (folder / "plan.json").exists() or (folder / "frozen-source").exists():
        raise RuntimeError("existing freeze must not be overwritten")
    import numpy
    import scipy
    dependencies = {"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__}
    expected = {"python": "3.13.14", "numpy": "2.4.6", "scipy": "1.18.0"}
    if dependencies != expected:
        raise RuntimeError(f"use the authorized installed system Python: expected {expected}, got {dependencies}")
    plan = {
        "schema_version": 1, "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Declared synthetic statistical model of the efficacy interval gate only. No N1002K measurements, biological rescue, clinical calibration, complete-prototype calibration or experimental sample-size recommendation.",
        "assumed_passed": ["model qualification", "all fate and selection gates", "all exposure qualifications", "all assay and response qualifications"],
        "completed_first_divisions_per_culture": 150,
        "baseline_error_probability": 0.25,
        "cultures_per_arm": [6, 8, 12], "icc_values": [0.0, 0.05, 0.15],
        "scenario_order": ["no_benefit", "all_at_threshold", "all_strong", "mixed"],
        "truth_scenarios": {"no_benefit": [0.0, 0.0, 0.0, 0.0],
                            "all_at_threshold": [0.05, 0.05, 0.05, 0.05],
                            "all_strong": [0.15, 0.15, 0.15, 0.15],
                            "mixed": [0.0, 0.025, 0.075, 0.15]},
        "threshold_delta": 0.05, "two_sided_family_confidence": 0.95,
        "experiments_per_grid_cell": 20000, "grid_cells": 36,
        "generative_model": {
            "unit": "independent culture; equal n per arm; five arms per experiment",
            "positive_icc": "For each culture draw q ~ Beta(p*(1-rho)/rho, (1-p)*(1-rho)/rho), then errors ~ Binomial(150,q). p_control=.25 and p_treated=.25-true_benefit. The same rho applies to all arms, with independent culture q draws.",
            "zero_icc": "Exact binomial limit: errors ~ Binomial(150,p); no beta draw.",
            "dependence": "One control arm is drawn once per experiment and reused in all four contrasts. The four treatment arms and all different cultures/experiments are otherwise independent. No matched cultures or batch effects.",
            "order": "For each cell draw all 20000*n controls, then treatment candidates 1 through 4. For positive ICC each arm's full beta array is drawn before its binomial array. Both CI methods reuse exactly these draws.",
        },
        "estimator": {
            "benefit": "mean(control culture proportions)-mean(treated culture proportions)",
            "sample_variance": "Unbiased ddof=1 variance across n culture proportions, never across 150*n cells. A culture with 150 completed first divisions is one replicate.",
            "se_squared": "s_control^2/n+s_treated^2/n",
            "welch_df": "(s_control^2/n+s_treated^2/n)^2 / ((s_control^2/n)^2/(n-1)+(s_treated^2/n)^2/(n-1)); no rounding of df",
            "intervals": {"unadjusted": "estimate +/- scipy.stats.t.ppf(.975,df)*SE",
                          "bonferroni4": "estimate +/- scipy.stats.t.ppf(1-.05/(2*4),df)*SE"},
            "interval_clipping": "None; real-valued Welch intervals retained even outside [-1,1].",
            "zero_variance": "Exactly constant culture counts in an arm get exactly zero sample variance. If BOTH arms have zero variance (total SE squared=0), the contrast is indeterminate, never a candidate/rejection. One zero arm with positive total variance remains finite with df=n-1 and is counted separately.",
            "other_invalid": "Nonfinite/negative variance, nonfinite/nonpositive df, or nonfinite/reversed interval is indeterminate and counted. Invalid raw count inputs raise errors. Numerical/runtime exceptions stop execution; no substitution or silent retries.",
            "classification": "Candidate if LOWER>delta; reject if UPPER<delta; else inconclusive. Equality at either boundary is inconclusive, without rounding or epsilon. Invalid intervals are explicitly indeterminate.",
        },
        "metrics": {
            "family_false_advancement": "At least one candidate whose specified true benefit <= .05. A true benefit exactly .05 is null for advancement. No eligible contrasts is structurally inapplicable, not estimated zero risk.",
            "detection": "Per-contrast category counts and eligible detection counts; family any/all candidate among true benefit > .05. Also separately report any/per-contrast positive-benefit candidate for true benefit > 0 to avoid ambiguity about benefit below the threshold.",
            "coverage": "Per-contrast and all-four simultaneous coverage of each specified true benefit, inclusive CI endpoints. Primary coverage uses all 20000 experiments (invalid intervals count as not covering); valid-only coverage reported separately with its actual denominator. No pooling of correlated contrasts into binomial trials.",
            "candidate_count_distributions": "Raw counts for 0,1,2,3,4 candidates, all candidates and above-threshold candidates separately, each over experiments.",
            "zero_invalid": "Control, treatment, total-zero variance and other-invalid counts per contrast; any indeterminate per family.",
            "monte_carlo_uncertainty": "Two-sided 95% Wilson intervals for each applicable binary event rate, using 20000 independent simulated experiments (or explicit valid-only denominator). These pointwise Monte Carlo intervals are not simultaneous confidence intervals across grid cells/metrics and do not quantify uncertainty about the model assumptions.",
            "diagnostics": "Empirical 4x4 covariance of benefit estimates, expected off-diagonal Var(control mean)=p(1-p)*(1+149*rho)/(150*n), mean culture sample variances, and paired counts of candidates removed by Bonferroni. Continuous diagnostics have no Wilson intervals.",
        },
        "examples": "Experiment index 0 in every grid cell, all four contrasts and both methods (288 intervals). Retain culture counts only for these preselected examples; reconstruct via stdlib variance and SciPy t quantiles, and compare strict classifications with a source-hashed snapshot of existing decision.relation. Do not invoke or claim full-prototype evaluation.",
        "randomness": {"generator": "numpy.random.Generator(numpy.random.PCG64(seed))",
                       "master_seed": "MVA-rescue-sidecar-2026-10-24-frozen-v1",
                       "cell_seed": "SHA256(master_seed + '|' + plan_file_sha256 + '|' + json.dumps(cell,sort_keys=True,separators=(',',':'),allow_nan=False)); first 32 hexadecimal digits interpreted as a base-16 integer. Store the full digest, input string and integer per cell."},
        "dependencies": dependencies,
        "runtime_choice": "User explicitly authorized installed system Python 3.13.14 with SciPy 1.18.0 and NumPy 2.4.6. Bundled artifact Python lacks SciPy; no installation or global environment change. Scientific runtime is separate from statistical assumptions. No custom distribution inversion retained.",
        "stopping_and_changes": "Exactly 20000 experiments in every one of 36 cells, fixed plan and source before any simulation. No outcome-driven tuning, optional stopping, selected seeds, model replacement or cell omission. Full deterministic rerun permitted only to verify reproduction. Preserve failed execution details if any.",
        "storage": "No giant simulated individual arrays retained; store every grid-cell count/result, the 288 preselected examples, provenance, timings and diagnostics.",
        "limitations": ["Parameters and threshold are illustrative, not fitted to N1002K or any assay.",
                        "Welch t intervals are approximate for small, skewed beta-binomial culture samples. Bonferroni does not repair misspecified or under-covering marginal intervals; achieved coverage is measured.",
                        "Completed first divisions condition on completion. Attrition, death, arrest, censoring, selection, lineage, unequal denominators and informative missingness are not generated.",
                        "No batch, donor, plate, matched-pair, temporal or between-candidate correlation beyond the shared control is modeled.",
                        "All other decision gates are assumed passed. Results are not calibration of the complete prototype, clinical operating characteristics, real biological efficacy, a power guarantee or sample-size advice.",
                        "Synthetic parameter-grid comparisons do not establish comparative benefit over competing treatment proposals or prize superiority."]
    }
    plan_bytes = (json.dumps(plan, indent=2, allow_nan=False) + "\n").encode()
    (folder / "plan.json").write_bytes(plan_bytes)
    snapshot = folder / "frozen-source"
    snapshot.mkdir()
    sources = {name: folder / name for name in ("math_helpers.py", "runtime.py", "simulate.py", "freeze.py", "verify.py", "test_numeric.py", "requirements.txt", "README.md")}
    sources["decision_snapshot.py"] = folder.parent / "decision.py"
    sources["test_rescue_simulation.py"] = folder.parents[2] / "tests/test_rescue_simulation.py"
    hashes = {}
    for name, path in sources.items():
        shutil.copyfile(path, snapshot / name)
        hashes[name] = hashlib.sha256((snapshot / name).read_bytes()).hexdigest()
    receipt = {"schema_version": 1, "frozen_utc": plan["frozen_utc"],
               "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
               "source_snapshot_sha256": hashes,
               "original_source_paths": {name: str(path.resolve()) for name, path in sources.items()},
               "no_simulation_executed_before_freeze": True,
               "runtime_executable": sys.executable,
               "freeze_command_argv": [sys.executable, *sys.argv]}
    (folder / "freeze.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"plan_sha256": receipt["plan_sha256"], "source_files": len(hashes), "frozen_utc": plan["frozen_utc"]}))


if __name__ == "__main__":
    main()
