#!/usr/bin/env python3
"""Reproduce deterministic protocol-conformance results; no statistical simulation."""

from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True

from casebook import load_casebook, materialize
from decision import evaluate
from mutation_checks import run_mutations


def naive_candidates(data, key, threshold):
    """Deliberately incomplete comparators, NOT competitor implementations."""
    result = []
    for contrast in data["contrasts"]:
        value = contrast["assays"].get(key)
        if type(value) not in (int, float, Decimal):
            continue
        value = Decimal(str(value))
        if value.is_finite() and value > threshold:
            result.append(contrast["id"])
    return result


def decisions(result):
    return [row["decision"] for row in result["contrasts"]] if result["input_valid"] else ["INVALID_INPUT"]


def reason_codes(result):
    return {code for row in result["contrasts"] for code in row["reason_codes"]} if result["input_valid"] else set(result["reason_codes"])


def build_report():
    book, receipt = load_casebook()
    root = Path(__file__).resolve().parent
    rows = []
    totals = {"fixture_cases": len(book["cases"]), "cases_matching_expectations": 0,
              "valid_input_cases": 0, "invalid_input_cases": 0,
              "expected_replication_candidate_contrasts": 0,
              "validator_replication_candidate_contrasts": 0,
              "naive_protein_only": {"accepted_contrasts": 0, "acceptances_not_authorized_by_expected_rules": 0, "missed_expected_candidates": 0},
              "naive_survivor_only": {"accepted_contrasts": 0, "acceptances_not_authorized_by_expected_rules": 0, "missed_expected_candidates": 0}}
    valid_comparison = {
        "scope": "Structurally valid inputs only, excluding schema and nonfinite failures. These still include declared failed controls and inconclusive results.",
        "contrast_count": 0, "expected_replication_candidate_contrasts": 0,
        "naive_protein_only": {"accepted_contrasts": 0, "acceptances_not_authorized_by_expected_rules": 0, "missed_expected_candidates": 0},
        "naive_survivor_only": {"accepted_contrasts": 0, "acceptances_not_authorized_by_expected_rules": 0, "missed_expected_candidates": 0}
    }
    for case in book["cases"]:
        data = materialize(book, case)
        result = evaluate(data)
        protein = naive_candidates(data, "protein_ratio", Decimal(1))
        survivor = naive_candidates(data, "survivor_normal_fraction_change", Decimal(0))
        observed = decisions(result)
        matched = (observed == case["expected_decisions"]
                   and set(case["expected_reason_codes"]) <= reason_codes(result)
                   and protein == case["expected_protein_candidates"]
                   and survivor == case["expected_survivor_candidates"])
        expected_ids = {contrast["id"] for contrast, expected in zip(data["contrasts"], case["expected_decisions"])
                        if expected == "REPLICATION_CANDIDATE"}
        totals["cases_matching_expectations"] += int(matched)
        totals["valid_input_cases" if result["input_valid"] else "invalid_input_cases"] += 1
        totals["expected_replication_candidate_contrasts"] += len(expected_ids)
        totals["validator_replication_candidate_contrasts"] += len(result["replication_candidate_ids"])
        for key, observed_ids in (("naive_protein_only", protein), ("naive_survivor_only", survivor)):
            totals[key]["accepted_contrasts"] += len(observed_ids)
            totals[key]["acceptances_not_authorized_by_expected_rules"] += len(set(observed_ids) - expected_ids)
            totals[key]["missed_expected_candidates"] += len(expected_ids - set(observed_ids))
            if result["input_valid"]:
                valid_comparison[key]["accepted_contrasts"] += len(observed_ids)
                valid_comparison[key]["acceptances_not_authorized_by_expected_rules"] += len(set(observed_ids) - expected_ids)
                valid_comparison[key]["missed_expected_candidates"] += len(expected_ids - set(observed_ids))
        if result["input_valid"]:
            valid_comparison["contrast_count"] += len(data["contrasts"])
            valid_comparison["expected_replication_candidate_contrasts"] += len(expected_ids)
        rows.append({"case_id": case["id"], "category": case["category"],
                     "expected_decisions": case["expected_decisions"], "observed_decisions": observed,
                     "expected_reason_codes": case["expected_reason_codes"],
                     "expectations_matched": matched,
                     "naive_protein_candidate_ids": protein, "naive_survivor_candidate_ids": survivor,
                     "validator_output": result})
    return {
        "schema_version": 1,
        "title": "Synthetic research decision-rule conformance; not biological or clinical validation",
        "scope": "Deterministic evaluator of supplied estimates and qualification assertions. Eligibility means independent research replication only.",
        "expected_case_freeze": receipt,
        "protocol_source": {"path": book["protocol"], "sha256_at_specification": book["protocol_sha256"]},
        "implementation_sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                  for name in ("decision.py", "casebook.py", "validate_cases.py", "mutation_checks.py")},
        "test_source_sha256": hashlib.sha256((root.parents[1] / "tests/test_rescue_decision.py").read_bytes()).hexdigest(),
        "comparators": {
            "naive_protein_only": "Accept any finite BubR1 protein ratio > 1; ignores function, fate, exposure, uncertainty and controls.",
            "naive_survivor_only": "Accept any finite positive change in normal-cell fraction among survivors; ignores function per division, selection, fate, exposure, uncertainty and controls.",
            "interpretation": "Illustrative failure modes only. Neither rule represents a named competitor. Case frequency is chosen, not sampled: counts do not estimate sensitivity, specificity, error rates or field superiority."
        },
        "statistical_simulation": {"performed": False, "reason": "No measured pilot variance or overdispersion is available. Invented parameters would not establish assay power or comparative benefit. Supplied CIs are synthetic fixtures, not fitted to the illustrative counts."},
        "hard_limits": [
            "Expected cases and implementation have the same author. Expectations precede implementation execution, not independent human adjudication or external preregistration.",
            "No mutant BubR1 rescue, actual N1002K defect, drug efficacy, patient benefit, causal mechanism or clinical threshold is demonstrated.",
            "All reference strings, thresholds, counts and intervals in fixtures are synthetic. Passing three example cultures is not a power calculation.",
            "The program cannot authenticate model qualification, pre-registration, exposure review, imaging, selection exclusion, statistical interval coverage, pilot records or independent culture identity.",
            "No CI estimation, hierarchical model fitting or multiplicity adjustment is performed; qualified analyst-supplied results are required.",
            "Only a first-completed-division-per-starting-cell design is supported. Repeated division data require a separately reviewed schema and analysis.",
            "Comparison-family completeness is checked against the supplied declaration; undeclared experiments or changed declarations cannot be detected.",
            "The phenotype classification / abundance-equivalence experiment is not implemented. A qualified stage-1 model is a declared prerequisite.",
            "No deployment, runtime benchmark, external validation or medical-device validation is claimed."
        ],
        "summary": totals,
        "structurally_valid_comparison": valid_comparison,
        "bounded_mutation_checks": run_mutations(),
        "cases": rows
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    stream = io.StringIO()
    suite = unittest.TestLoader().discover(str(root / "tests"), pattern="test_rescue_decision.py")
    tests = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    report = build_report()
    report["focused_test_execution"] = {
        "suite": "tests/test_rescue_decision.py",
        "tests_run": tests.testsRun,
        "failures": len(tests.failures), "errors": len(tests.errors),
        "skipped": len(tests.skipped), "successful": tests.wasSuccessful(),
        "python_version": sys.version.split()[0],
        "output_on_failure": None if tests.wasSuccessful() else stream.getvalue(),
        "scope": "Only the new rescue decision tests; no shared gates or other project suites."
    }
    print(json.dumps(report, indent=2, allow_nan=False))
    mutations = report["bounded_mutation_checks"]
    passed = (tests.wasSuccessful() and all(case["expectations_matched"] for case in report["cases"])
              and mutations["faults_detected"] == mutations["faults_tested"])
    sys.exit(0 if passed else 1)
