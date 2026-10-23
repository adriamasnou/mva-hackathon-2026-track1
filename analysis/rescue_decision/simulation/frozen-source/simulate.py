#!/usr/bin/env python3
"""Execute only the hash-frozen synthetic efficacy-gate experiment."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True
from math_helpers import (classify, shared_control_covariance, wilson, welch_components)
from runtime import critical_values


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def check_freeze(folder):
    folder = Path(folder).resolve()
    receipt = json.loads((folder / "freeze.json").read_text())
    if sha(folder / "plan.json") != receipt["plan_sha256"]:
        raise ValueError("frozen plan changed")
    for name, digest in receipt["source_snapshot_sha256"].items():
        if sha(folder / "frozen-source" / name) != digest:
            raise ValueError(f"source snapshot changed: {name}")
    # Run the immutable copies, not a changed working-tree implementation.
    own = Path(__file__).resolve()
    if own.parent != folder / "frozen-source" or sha(own) != receipt["source_snapshot_sha256"]["simulate.py"]:
        raise ValueError("execute frozen-source/simulate.py after freeze.py")
    return receipt, json.loads((folder / "plan.json").read_text())


def derived_seed(plan, plan_sha, cell):
    message = plan["randomness"]["master_seed"] + "|" + plan_sha + "|" + canonical(cell)
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()
    return int(digest[:32], 16), digest, message


def metric(count, total, applicable=True):
    count, total = int(count), int(total)
    return {"count": count, "trials": total, "applicable": applicable,
            "estimate": count / total if applicable and total else None,
            "mc_wilson_95": wilson(count, total) if applicable and total else None}


def culture_arrays(control_counts, treatment_counts, completed):
    """E x n shared controls; E x four contrasts x n independent treatments."""
    import numpy as np
    c, t = np.asarray(control_counts), np.asarray(treatment_counts)
    if c.ndim != 2 or t.ndim != 3 or t.shape[0] != c.shape[0] or t.shape[2] != c.shape[1] or c.shape[1] < 2:
        raise ValueError("expected E x n and E x contrasts x n independent cultures")
    if type(completed) is not int or completed <= 0 or any(
            np.any(~np.isfinite(x)) or np.any(x < 0) or np.any(x > completed) or np.any(x != np.floor(x)) for x in (c, t)):
        raise ValueError("invalid culture error counts")
    cp, tp = c / completed, t / completed
    cm, tm = cp.mean(axis=1), tp.mean(axis=2)
    cv, tv = cp.var(axis=1, ddof=1), tp.var(axis=2, ddof=1)
    cz, tz = np.ptp(c, axis=1) == 0, np.ptp(t, axis=2) == 0
    # Exactly equal counts are mathematically zero variance; remove float artifacts.
    cv[cz], tv[tz] = 0, 0
    n = c.shape[1]
    a, b = cv[:, None] / n, tv / n
    v = a + b
    zero = v == 0
    with np.errstate(divide="ignore", invalid="ignore"):
        df = v * v / ((a * a + b * b) / (n - 1))
    invalid = ~np.isfinite(v) | ~np.isfinite(df) | (v <= 0) | (df <= 0)
    return {"benefit": cm[:, None] - tm, "variance": v, "df": df,
            "invalid": invalid, "zero_total_variance": zero,
            "control_zero": cz, "treatment_zero": tz,
            "control_sample_variance": cv, "treatment_sample_variance": tv,
            "control_mean": cm, "treatment_means": tm}


def intervals(stats, family_size, delta):
    import numpy as np
    valid = ~stats["invalid"]
    critical = np.full(stats["df"].shape, np.nan)
    critical[valid] = critical_values(stats["df"][valid], family_size=family_size)
    width = critical * np.sqrt(stats["variance"])
    lower, upper = stats["benefit"] - width, stats["benefit"] + width
    invalid = ~valid | ~np.isfinite(lower) | ~np.isfinite(upper) | (lower > upper)
    return {"critical": critical, "lower": lower, "upper": upper,
            "candidate": (~invalid) & (lower > delta), "reject": (~invalid) & (upper < delta),
            "inconclusive": (~invalid) & (lower <= delta) & (upper >= delta), "indeterminate": invalid}


def summarize(stats, interval, truths, delta):
    import numpy as np
    truths = np.asarray(truths)
    trials = stats["benefit"].shape[0]
    eligible, positive, null = truths > delta, truths > 0, truths <= delta
    valid = ~interval["indeterminate"]
    covered = valid & (interval["lower"] <= truths) & (interval["upper"] >= truths)
    cand = interval["candidate"]
    all_valid = valid.all(axis=1)
    family = {
        "false_advancement_true_benefit_le_delta": metric((cand & null).any(axis=1).sum(), trials, bool(null.any())),
        "any_above_threshold_candidate_true_benefit_gt_delta": metric((cand & eligible).any(axis=1).sum(), trials, bool(eligible.any())),
        "all_above_threshold_candidates_true_benefit_gt_delta": metric((cand | ~eligible).all(axis=1).sum() if eligible.any() else 0, trials, bool(eligible.any())),
        "any_positive_benefit_candidate_true_benefit_gt_zero": metric((cand & positive).any(axis=1).sum(), trials, bool(positive.any())),
        "any_indeterminate": metric((~valid).any(axis=1).sum(), trials),
        "simultaneous_coverage_all_experiments": metric(covered.all(axis=1).sum(), trials),
        "simultaneous_coverage_given_all_valid": metric(covered.all(axis=1).sum(), all_valid.sum()),
        "eligible_null_contrasts": int(null.sum()), "eligible_above_threshold_contrasts": int(eligible.sum()),
        "eligible_positive_benefit_contrasts": int(positive.sum()),
        "candidate_count_distribution": [metric((cand.sum(axis=1) == k).sum(), trials) for k in range(5)],
        "above_threshold_candidate_count_distribution": [metric(((cand & eligible).sum(axis=1) == k).sum(), trials) for k in range(5)],
    }
    per_contrast = []
    for j, truth in enumerate(truths):
        row = {"candidate_id": j + 1, "true_benefit": float(truth)}
        for category in ("candidate", "reject", "inconclusive", "indeterminate"):
            row[category] = metric(interval[category][:, j].sum(), trials)
        row["marginal_coverage_all_experiments"] = metric(covered[:, j].sum(), trials)
        row["marginal_coverage_given_valid"] = metric(covered[:, j].sum(), valid[:, j].sum())
        row["false_advancement_true_benefit_le_delta"] = metric(cand[:, j].sum() if null[j] else 0, trials, bool(null[j]))
        row["detected_true_benefit_gt_delta"] = metric(cand[:, j].sum() if eligible[j] else 0, trials, bool(eligible[j]))
        row["detected_true_benefit_gt_zero"] = metric(cand[:, j].sum() if positive[j] else 0, trials, bool(positive[j]))
        per_contrast.append(row)
    return {"family": family, "contrasts": per_contrast}


def execute_cell(plan, receipt, cell, relation):
    import numpy as np
    start, clock = utc(), time.perf_counter()
    n, rho = cell["cultures_per_arm"], cell["icc"]
    trials, completed = plan["experiments_per_grid_cell"], plan["completed_first_divisions_per_culture"]
    delta, baseline = plan["threshold_delta"], plan["baseline_error_probability"]
    truths = plan["truth_scenarios"][cell["scenario"]]
    seed, digest, seed_message = derived_seed(plan, receipt["plan_sha256"], cell)
    rng = np.random.Generator(np.random.PCG64(seed))

    def draw(p):
        if rho == 0:
            return rng.binomial(completed, p, size=(trials, n))
        concentration = (1 - rho) / rho
        probabilities = rng.beta(p * concentration, (1 - p) * concentration, size=(trials, n))
        return rng.binomial(completed, probabilities)

    control = draw(baseline)
    treated = np.stack([draw(baseline - benefit) for benefit in truths], axis=1)
    stats = culture_arrays(control, treated, completed)
    methods, examples = {}, []
    intervals_by_method = {}
    for name, family in (("unadjusted", 1), ("bonferroni4", 4)):
        ci = intervals(stats, family, delta)
        intervals_by_method[name] = ci
        methods[name] = summarize(stats, ci, truths, delta)
        # Preselected experiment zero in every cell, never chosen for its result.
        for j in range(4):
            valid = not bool(ci["indeterminate"][0, j])
            lo, hi = (float(ci[key][0, j]) if valid else None for key in ("lower", "upper"))
            classification = classify(lo, hi, delta)
            existing = relation([lo, hi], delta) if valid else None
            expected_relation = {"candidate": "pass", "reject": "fail", "inconclusive": "inconclusive"}.get(classification)
            if existing != expected_relation:
                raise AssertionError("example classification disagrees with existing decision.relation")
            # Independently reconstruct selected examples using stdlib culture variance and SciPy critical value.
            scalar = welch_components(control[0].tolist(), treated[0, j].tolist(), completed)
            scalar_bounds = None
            if valid:
                q = float(critical_values(scalar["df"], family_size=family))
                scalar_bounds = [scalar["benefit"] - q * scalar["se"], scalar["benefit"] + q * scalar["se"]]
                if max(abs(lo - scalar_bounds[0]), abs(hi - scalar_bounds[1])) > 1e-10:
                    raise AssertionError("vector CI disagrees with independent scalar reconstruction")
            examples.append({"experiment_index": 0, "candidate_id": j + 1, "method": name,
                             "control_error_counts": control[0].tolist(), "treatment_error_counts": treated[0, j].tolist(),
                             "benefit_estimate": float(stats["benefit"][0, j]),
                             "df": float(stats["df"][0, j]) if valid else None,
                             "critical_value": float(ci["critical"][0, j]) if valid else None,
                             "interval": [lo, hi] if valid else None, "scalar_reconstructed_interval": scalar_bounds,
                             "classification": classification, "existing_decision_relation": existing,
                             "zero_total_variance": bool(stats["zero_total_variance"][0, j])})
    u, b = intervals_by_method["unadjusted"], intervals_by_method["bonferroni4"]
    # Same draws and df: wider intervals cannot add candidates or rejections.
    if np.any(b["candidate"] & ~u["candidate"]) or np.any(b["reject"] & ~u["reject"]):
        raise AssertionError("multiplicity interval ordering violated")
    diagnostics = {
        "zero_control_variance_experiments": metric(stats["control_zero"].sum(), trials),
        "zero_treatment_variance_by_contrast": [metric(stats["treatment_zero"][:, j].sum(), trials) for j in range(4)],
        "zero_total_variance_by_contrast": [metric(stats["zero_total_variance"][:, j].sum(), trials) for j in range(4)],
        "other_invalid_by_contrast": [metric((stats["invalid"][:, j] & ~stats["zero_total_variance"][:, j]).sum(), trials) for j in range(4)],
        "empirical_benefit_covariance_across_experiments": np.cov(stats["benefit"], rowvar=False, ddof=1).tolist(),
        "expected_off_diagonal_shared_control_covariance": shared_control_covariance(baseline, rho, n, completed),
        "mean_control_sample_variance": float(stats["control_sample_variance"].mean()),
        "mean_treatment_sample_variance_by_contrast": stats["treatment_sample_variance"].mean(axis=0).tolist(),
        "unadjusted_candidate_removed_by_bonferroni_by_contrast": [metric((u["candidate"][:, j] & ~b["candidate"][:, j]).sum(), trials) for j in range(4)],
        "bonferroni_added_candidate_count": 0,
    }
    return {"cell": cell, "truth_benefits": truths, "seed_integer": str(seed), "seed_sha256": digest,
            "seed_material_utf8": seed_message, "started_utc": start, "finished_utc": utc(),
            "elapsed_seconds": time.perf_counter() - clock, "methods": methods,
            "diagnostics": diagnostics, "deterministically_selected_examples": examples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    folder, out = args.folder.resolve(), args.out.resolve()
    if out.parent != folder or out.exists():
        raise ValueError("output must be a new file immediately inside the sidecar folder")
    receipt, plan = check_freeze(folder)
    import numpy as np
    import scipy
    if scipy.__version__ != plan["dependencies"]["scipy"]:
        raise RuntimeError("use the pinned SciPy version")
    if np.__version__ != plan["dependencies"]["numpy"] or platform.python_version() != plan["dependencies"]["python"]:
        raise RuntimeError("use the pinned system Python and NumPy versions")
    spec = importlib.util.spec_from_file_location("frozen_decision", folder / "frozen-source/decision_snapshot.py")
    decision = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decision)
    clock, started = time.perf_counter(), utc()
    record = {"schema_version": 1, "scope": plan["scope"], "plan_sha256": receipt["plan_sha256"],
              "freeze_sha256": sha(folder / "freeze.json"), "started_utc": started,
              "command_argv": [sys.executable, *sys.argv], "working_directory": str(Path.cwd()),
              "versions": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform()},
              "thread_environment": {key: os.environ.get(key) for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
              "grid_results": []}
    for n in plan["cultures_per_arm"]:
        for rho in plan["icc_values"]:
            for scenario in plan["scenario_order"]:
                cell = {"cultures_per_arm": n, "icc": rho, "scenario": scenario}
                result = execute_cell(plan, receipt, cell, decision.relation)
                record["grid_results"].append(result)
                print(canonical({"completed_cell": cell, "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    check_freeze(folder)
    record.update(finished_utc=utc(), elapsed_seconds=time.perf_counter() - clock,
                  grid_cell_count=len(record["grid_results"]),
                  simulated_experiment_count=len(record["grid_results"]) * plan["experiments_per_grid_cell"])
    with out.open("x") as handle:
        json.dump(record, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(canonical({"output": str(out), "sha256": sha(out), "elapsed_seconds": record["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
