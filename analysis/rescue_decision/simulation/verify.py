#!/usr/bin/env python3
"""Offline stdlib audit; optional exact comparison with a full seeded rerun."""
import argparse
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from math_helpers import classify, wilson, welch_components


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def verify(folder, results_path):
    receipt = json.loads((folder / "freeze.json").read_text())
    plan = json.loads((folder / "plan.json").read_text())
    assert sha(folder / "plan.json") == receipt["plan_sha256"], "plan hash"
    for name, digest in receipt["source_snapshot_sha256"].items():
        assert sha(folder / "frozen-source" / name) == digest, f"snapshot hash {name}"
    results = json.loads(results_path.read_text())
    assert results["freeze_sha256"] == sha(folder / "freeze.json"), "freeze hash"
    assert results["plan_sha256"] == receipt["plan_sha256"], "result plan hash"
    assert results["started_utc"] >= receipt["frozen_utc"], "run preceded freeze"
    assert results["grid_cell_count"] == 36 and results["simulated_experiment_count"] == 720000
    assert len(results["grid_results"]) == 36
    expected_cells = [{"cultures_per_arm": n, "icc": rho, "scenario": scenario}
                      for n in plan["cultures_per_arm"] for rho in plan["icc_values"] for scenario in plan["scenario_order"]]
    spec = importlib.util.spec_from_file_location("frozen_decision", folder / "frozen-source/decision_snapshot.py")
    decision = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decision)
    checked_metrics, examples = 0, 0

    def check_metrics(node):
        nonlocal checked_metrics
        if isinstance(node, dict):
            if set(("count", "trials", "applicable", "estimate", "mc_wilson_95")) <= set(node):
                k, n = node["count"], node["trials"]
                assert type(k) is int and type(n) is int and 0 <= k <= n, "counts invalid"
                expected_ci = wilson(k, n) if node["applicable"] and n else None
                assert node["mc_wilson_95"] == expected_ci, "Wilson interval mismatch"
                assert node["estimate"] == (k / n if node["applicable"] and n else None), "estimate mismatch"
                checked_metrics += 1
            for child in node.values():
                check_metrics(child)
        elif isinstance(node, list):
            for child in node:
                check_metrics(child)

    for result, expected in zip(results["grid_results"], expected_cells):
        assert result["cell"] == expected, "cell omitted/reordered"
        truth = plan["truth_scenarios"][expected["scenario"]]
        assert result["truth_benefits"] == truth
        seed_text = plan["randomness"]["master_seed"] + "|" + receipt["plan_sha256"] + "|" + canonical(expected)
        digest = hashlib.sha256(seed_text.encode()).hexdigest()
        assert result["seed_material_utf8"] == seed_text and result["seed_sha256"] == digest
        assert result["seed_integer"] == str(int(digest[:32], 16)), "seed mismatch"
        check_metrics(result)
        for method in ("unadjusted", "bonferroni4"):
            rows = result["methods"][method]["contrasts"]
            assert len(rows) == 4
            for j, row in enumerate(rows):
                assert row["candidate_id"] == j + 1 and row["true_benefit"] == truth[j]
                assert sum(row[k]["count"] for k in ("candidate", "reject", "inconclusive", "indeterminate")) == 20000
                assert all(row[k]["trials"] == 20000 for k in ("candidate", "reject", "inconclusive", "indeterminate"))
                assert row["marginal_coverage_given_valid"]["trials"] == 20000 - row["indeterminate"]["count"]
                assert row["marginal_coverage_given_valid"]["count"] == row["marginal_coverage_all_experiments"]["count"]
            family = result["methods"][method]["family"]
            for key in ("candidate_count_distribution", "above_threshold_candidate_count_distribution"):
                assert sum(item["count"] for item in family[key]) == 20000
            assert family["simultaneous_coverage_given_all_valid"]["trials"] == 20000 - family["any_indeterminate"]["count"]
        u, b = (result["methods"][m] for m in ("unadjusted", "bonferroni4"))
        for j in range(4):
            assert b["contrasts"][j]["candidate"]["count"] <= u["contrasts"][j]["candidate"]["count"]
            assert b["contrasts"][j]["reject"]["count"] <= u["contrasts"][j]["reject"]["count"]
            assert u["contrasts"][j]["candidate"]["count"] - b["contrasts"][j]["candidate"]["count"] == result["diagnostics"]["unadjusted_candidate_removed_by_bonferroni_by_contrast"][j]["count"]
        assert len(result["deterministically_selected_examples"]) == 8
        seen = set()
        for example in result["deterministically_selected_examples"]:
            assert example["experiment_index"] == 0
            key = (example["method"], example["candidate_id"])
            assert key not in seen
            seen.add(key)
            scalar = welch_components(example["control_error_counts"], example["treatment_error_counts"])
            assert abs(scalar["benefit"] - example["benefit_estimate"]) < 1e-12
            interval = example["interval"]
            if interval is None:
                assert example["classification"] == "indeterminate"
                assert scalar["status"] == "zero_total_variance"
            else:
                assert abs(scalar["df"] - example["df"]) < 1e-10
                scalar_ci = [scalar["benefit"] - example["critical_value"] * scalar["se"],
                             scalar["benefit"] + example["critical_value"] * scalar["se"]]
                assert max(abs(x - y) for x, y in zip(scalar_ci, interval)) < 1e-10
                category = classify(*interval, plan["threshold_delta"])
                reference = decision.relation(interval, plan["threshold_delta"])
                assert category == example["classification"]
                assert reference == example["existing_decision_relation"] == {"candidate": "pass", "reject": "fail", "inconclusive": "inconclusive"}[category]
            examples += 1
    return results, {"status": "pass", "grid_cells": 36, "experiments": 720000,
                     "metrics_checked": checked_metrics, "examples_checked": examples,
                     "result_sha256": sha(results_path), "plan_sha256": receipt["plan_sha256"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    results, audit = verify(args.folder, args.results)
    if args.compare:
        second, second_audit = verify(args.folder, args.compare)
        for a, b in zip(results["grid_results"], second["grid_results"]):
            strip = lambda v: {k: item for k, item in v.items() if k not in ("started_utc", "finished_utc", "elapsed_seconds")}
            assert strip(a) == strip(b), "scientific outputs differ on deterministic rerun"
        audit.update(exact_scientific_output_reproduction=True, reproduced_sha256=second_audit["result_sha256"])
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
