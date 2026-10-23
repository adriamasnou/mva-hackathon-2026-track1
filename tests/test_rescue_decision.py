"""Protocol, boundary, corruption and metamorphic tests of the research prototype.

Run only this file: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
    -p test_rescue_decision.py -v
"""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "analysis/rescue_decision"
sys.dont_write_bytecode = True
sys.path.insert(0, str(MODULE))
from casebook import load_casebook, materialize, pointer_parent, set_pointer
from decision import evaluate, loads
from mutation_checks import run_mutations
from validate_cases import build_report, decisions, naive_candidates, reason_codes

BOOK, RECEIPT = load_casebook()


def base():
    return deepcopy(BOOK["baseline"])


def first(result):
    return result["contrasts"][0]


def all_objects(value, pointer=""):
    if isinstance(value, dict):
        yield pointer, value
        for key, child in value.items():
            yield from all_objects(child, pointer + "/" + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from all_objects(child, pointer + "/" + str(index))


def numeric_leaves(value, pointer=""):
    if type(value) in (int, float):
        yield pointer
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from numeric_leaves(child, pointer + "/" + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from numeric_leaves(child, pointer + "/" + str(index))


class RescueDecisionTests(unittest.TestCase):
    def assertInvalid(self, data):
        result = evaluate(data)
        self.assertFalse(result["input_valid"], result)
        self.assertEqual(result["decision"], "INVALID_INPUT")
        self.assertEqual(result["replication_candidate_ids"], [])
        self.assertTrue(result["errors"])

    def test_frozen_expectations_and_comparators(self):
        for case in BOOK["cases"]:
            with self.subTest(case=case["id"]):
                data = materialize(BOOK, case)
                result = evaluate(data)
                self.assertEqual(decisions(result), case["expected_decisions"])
                self.assertTrue(set(case["expected_reason_codes"]) <= reason_codes(result))
                self.assertEqual(naive_candidates(data, "protein_ratio", Decimal(1)), case["expected_protein_candidates"])
                self.assertEqual(naive_candidates(data, "survivor_normal_fraction_change", Decimal(0)), case["expected_survivor_candidates"])

    def test_specification_hash_and_protocol_provenance(self):
        self.assertEqual(hashlib.sha256((MODULE / "expected-cases.json").read_bytes()).hexdigest(), RECEIPT["sha256"])
        self.assertEqual(hashlib.sha256((MODULE / "protocol-at-specification.txt").read_bytes()).hexdigest(), BOOK["protocol_sha256"])
        self.assertEqual(RECEIPT["case_count"], 40)
        self.assertEqual(len({case["id"] for case in BOOK["cases"]}), 40)

    def test_primary_ci_complete_boundary_grid(self):
        # Expected categories specified from ordered regions, not evaluator helpers.
        for lower, upper, expected in (
            ("0.049", "0.0499", "WORTHWHILE_BENEFIT_RULED_OUT"),
            ("0.049", "0.050", "INCONCLUSIVE"),
            ("0.050", "0.050", "INCONCLUSIVE"),
            ("0.050", "0.051", "INCONCLUSIVE"),
            ("0.049", "0.051", "INCONCLUSIVE"),
            ("0.050000000000000000000001", "0.051", "REPLICATION_CANDIDATE"),
        ):
            with self.subTest(lower=lower, upper=upper):
                data = base()
                data["contrasts"][0]["analysis"]["benefit_ci"] = [Decimal(lower), Decimal(upper)]
                self.assertEqual(first(evaluate(data))["decision"], expected)

    def test_fate_upper_and_lower_boundary_equality_cannot_pass(self):
        for field, value in (("division_ratio_ci", [0.8, 0.8]),
                             ("excess_death_ci", [0.05, 0.05]),
                             ("excess_arrest_ci", [0.05, 0.05]),
                             ("excess_censoring_ci", [0.05, 0.05])):
            with self.subTest(field=field):
                data = base()
                data["contrasts"][0]["fate"][field] = value
                self.assertEqual(first(evaluate(data))["decision"], "INCONCLUSIVE")

    def test_each_fate_harm_blocks_independently(self):
        for field, value in (("division_ratio_ci", [0.1, 0.2]),
                             ("excess_death_ci", [0.06, 0.07]),
                             ("excess_arrest_ci", [0.06, 0.07]),
                             ("excess_censoring_ci", [0.06, 0.07])):
            with self.subTest(field=field):
                data = base()
                data["contrasts"][0]["fate"][field] = value
                self.assertEqual(first(evaluate(data))["decision"], "DO_NOT_ADVANCE")

    def test_failed_controls_cannot_become_biological_negative(self):
        for pointer in ("/model/qualified", "/contrasts/0/assays/function_controls_qualified",
                        "/contrasts/0/assays/response_controls_qualified",
                        "/contrasts/0/exposure/measurement_qualified",
                        "/contrasts/0/fate/measurement_qualified"):
            with self.subTest(pointer=pointer):
                data = base()
                data["contrasts"][0]["analysis"]["benefit_ci"] = [-0.2, -0.1]
                set_pointer(data, pointer, False)
                row = first(evaluate(data))
                self.assertEqual(row["decision"], "TECHNICALLY_INDETERMINATE")
                self.assertNotIn("BENEFIT_UPPER_BELOW_DELTA", row["reason_codes"])
                self.assertFalse(row["criteria"]["biological_interpretation_permitted_by_declared_controls"])
                self.assertEqual(row["criteria"]["hsp_mechanism"], "UNINTERPRETABLE")

    def test_all_required_keys_missing_fail_closed(self):
        # Exhaustive schema deletion; covers controls, records and denominator fields.
        for pointer, obj in all_objects(base()):
            for key in obj:
                path = pointer + "/" + key
                with self.subTest(path=path):
                    data = base()
                    parent, child = pointer_parent(data, path)
                    del parent[child]
                    self.assertInvalid(data)

    def test_unknown_fields_rejected_at_every_object_level(self):
        for pointer, _ in all_objects(base()):
            with self.subTest(pointer=pointer):
                data = base()
                obj = data
                if pointer:
                    parent, key = pointer_parent(data, pointer)
                    obj = parent[key]
                obj["misspelled_or_unrecognized"] = True
                self.assertInvalid(data)

    def test_all_numeric_fields_reject_nonfinite_and_booleans(self):
        for pointer in numeric_leaves(base()):
            for value in (float("nan"), float("inf"), float("-inf"), True):
                with self.subTest(pointer=pointer, value=str(value)):
                    data = base()
                    set_pointer(data, pointer, value)
                    self.assertInvalid(data)

    def test_empty_records_fail_closed(self):
        for pointer in ("/model/record", "/plan/threshold_basis", "/plan/pilot_record",
                        "/plan/power_plan_record", "/contrasts/0/fate/record",
                        "/contrasts/0/exposure/record", "/contrasts/0/analysis/record"):
            with self.subTest(pointer=pointer):
                data = base()
                set_pointer(data, pointer, "  ")
                self.assertInvalid(data)

    def test_invalid_root_types_and_nonstring_api_keys_fail_closed(self):
        for data in (None, [], 1, True, "string", {1: True, "x": False}):
            with self.subTest(data=data):
                self.assertInvalid(data)

    def test_denominators_not_cells_as_replicates(self):
        row = first(evaluate(base()))
        self.assertEqual(row["denominators"]["vehicle"], {
            "independent_cultures": 3, "starting_cells": 300, "mitotic_entries": 240,
            "completed_divisions": 225, "segregation_errors": 45,
            "deaths": 15, "persistent_arrests": 15, "censored": 15})
        self.assertEqual(row["denominators"]["treated"]["segregation_errors"], 27)

    def test_deaths_and_arrests_are_not_recoded_as_segregation_errors(self):
        data = base()
        data["contrasts"][0]["observations"]["treated"][0]["deaths"] = 20
        data["contrasts"][0]["observations"]["treated"][0]["persistent_arrests"] = 20
        row = first(evaluate(data))
        self.assertEqual(row["denominators"]["treated"]["segregation_errors"], 27)
        self.assertEqual(row["denominators"]["treated"]["deaths"], 30)
        # The analyst-supplied CIs are deliberately NOT recomputed from pooled cells.

    def test_impossible_count_order_and_duplicate_cultures_rejected(self):
        for key, value in (("segregation_errors", 76), ("completed_divisions", 81),
                           ("mitotic_entries", 101), ("deaths", 101), ("censored", -1)):
            with self.subTest(key=key):
                data = base()
                data["contrasts"][0]["observations"]["treated"][0][key] = value
                self.assertInvalid(data)
        data = base()
        data["contrasts"][0]["observations"]["treated"][1]["culture_id"] = "t1"
        self.assertInvalid(data)

    def test_zero_division_culture_retained_but_empty_arm_rejected(self):
        data = base()
        zero = data["contrasts"][0]["observations"]["treated"][0]
        zero.update(completed_divisions=0, segregation_errors=0)
        result = evaluate(data)
        self.assertTrue(result["input_valid"])
        self.assertEqual(first(result)["denominators"]["treated"]["independent_cultures"], 3)
        data["contrasts"][0]["observations"]["treated"] = []
        data["contrasts"][0]["analysis"]["biological_replicates"]["treated"] = 0
        self.assertInvalid(data)

    def test_ci_range_and_confidence_mismatch_rejected(self):
        for pointer, value in (("/contrasts/0/analysis/benefit_ci", [-1.01, 0.1]),
                               ("/contrasts/0/fate/excess_death_ci", [0, 1.01]),
                               ("/contrasts/0/fate/division_ratio_ci", [-0.1, 1]),
                               ("/contrasts/0/analysis/confidence_level", 0.9),
                               ("/contrasts/0/fate/confidence_level", 0.9),
                               ("/plan/confidence_level", 1)):
            with self.subTest(pointer=pointer):
                data = base()
                set_pointer(data, pointer, value)
                self.assertInvalid(data)

    def test_nested_cells_unaccounted_for_is_indeterminate(self):
        data = base()
        data["contrasts"][0]["analysis"]["nesting_handled"] = False
        self.assertEqual(first(evaluate(data))["decision"], "TECHNICALLY_INDETERMINATE")

    def test_duplicate_and_missing_family_ids_rejected(self):
        data = base()
        data["plan"]["comparison_family"] = ["c1", "c1"]
        self.assertInvalid(data)
        data = base()
        data["contrasts"].append(deepcopy(data["contrasts"][0]))
        self.assertInvalid(data)
        data = base()
        data["plan"]["comparison_family"] = []
        self.assertInvalid(data)

    def test_family_order_does_not_change_decisions(self):
        case = next(case for case in BOOK["cases"] if case["id"] == "complete_adjusted_family_all_results")
        data = materialize(BOOK, case)
        initial = evaluate(data)
        data["contrasts"].reverse()
        data["plan"]["comparison_family"].reverse()
        reordered = evaluate(data)
        self.assertEqual({row["id"]: row for row in initial["contrasts"]},
                         {row["id"]: row for row in reordered["contrasts"]})

    def test_malformed_sibling_blocks_otherwise_positive_family(self):
        case = next(case for case in BOOK["cases"] if case["id"] == "complete_adjusted_family_all_results")
        data = materialize(BOOK, case)
        del data["contrasts"][1]["fate"]["excess_arrest_ci"]
        self.assertInvalid(data)

    def test_exploratory_results_reported_without_entering_candidate_list(self):
        data = base()
        extra = deepcopy(data["contrasts"][0])
        extra.update(id="exploratory-time", role="exploratory")
        data["contrasts"].append(extra)
        result = evaluate(data)
        self.assertEqual(result["replication_candidate_ids"], ["c1"])
        self.assertEqual(result["contrasts"][1]["decision"], "EXPLORATORY_SIGNAL")

    def test_markers_cannot_override_function_fate_or_exposure(self):
        for pointer, value in (("/contrasts/0/analysis/benefit_ci", [-0.02, 0.04]),
                               ("/contrasts/0/fate/division_ratio_ci", [0.1, 0.3]),
                               ("/contrasts/0/exposure/within_qualified_window", False)):
            data = base()
            set_pointer(data, pointer, value)
            before = evaluate(data)
            data["contrasts"][0]["assays"].update(protein_ratio=10000, survivor_normal_fraction_change=1)
            after = evaluate(data)
            self.assertEqual(decisions(before), decisions(after))
            self.assertEqual(after["replication_candidate_ids"], [])

    def test_absent_hsp_requires_investigation_not_automatic_rejection(self):
        data = base()
        data["contrasts"][0]["assays"]["hsp_response"] = "absent"
        row = first(evaluate(data))
        self.assertEqual(row["decision"], "REPLICATION_CANDIDATE")
        self.assertEqual(row["criteria"]["hsp_mechanism"], "DISCORDANT_REQUIRES_INVESTIGATION")
        data["contrasts"][0]["assays"]["hsp_response"] = "indeterminate"
        self.assertEqual(first(evaluate(data))["decision"], "TECHNICALLY_INDETERMINATE")

    def test_optional_survivor_metric_not_required_for_research_candidate(self):
        data = base()
        data["contrasts"][0]["assays"]["survivor_normal_fraction_change"] = None
        self.assertEqual(first(evaluate(data))["decision"], "REPLICATION_CANDIDATE")
        self.assertEqual(naive_candidates(data, "survivor_normal_fraction_change", Decimal(0)), [])

    def test_input_not_mutated_and_result_deterministic(self):
        data = base()
        original = deepcopy(data)
        self.assertEqual(evaluate(data), evaluate(data))
        self.assertEqual(data, original)

    def test_strict_json_duplicate_and_nonfinite_rejection(self):
        for text in ('{"x":1,"x":2}', '{"a":{"x":1,"x":2}}',
                     '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    loads(text)

    def test_decimal_json_precision_not_rounded_at_threshold(self):
        text = json.dumps(base()).replace('[0.06, 0.11]', '[0.050000000000000000000001, 0.11]')
        self.assertEqual(first(evaluate(loads(text)))["decision"], "REPLICATION_CANDIDATE")

    def run_cli(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_text(text)
            process = subprocess.run([sys.executable, str(MODULE / "decision.py"), str(path)],
                                     capture_output=True, text=True,
                                     env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False)
        self.assertEqual(process.stderr, "")
        return process.returncode, json.loads(process.stdout)

    def test_cli_well_formed_negative_exits_zero_not_positive(self):
        data = base()
        data["contrasts"][0]["analysis"]["benefit_ci"] = [-0.1, 0]
        code, result = self.run_cli(json.dumps(data))
        self.assertEqual(code, 0)
        self.assertEqual(result["replication_candidate_ids"], [])
        self.assertEqual(first(result)["decision"], "WORTHWHILE_BENEFIT_RULED_OUT")

    def test_cli_invalid_missing_and_nonfinite_fail_closed(self):
        for text in ('{}', '{', '{"x":1,"x":2}', '{"x":NaN}', '[1,2]'):
            with self.subTest(text=text):
                code, result = self.run_cli(text)
                self.assertEqual(code, 2)
                self.assertEqual(result["replication_candidate_ids"], [])
                self.assertFalse(result["input_valid"])

    def test_report_counts_cases_and_contrasts_separately(self):
        report = build_report()
        summary = report["summary"]
        self.assertEqual(summary["fixture_cases"], 40)
        self.assertEqual(summary["cases_matching_expectations"], 40)
        self.assertEqual(summary["expected_replication_candidate_contrasts"], 5)
        self.assertEqual(summary["validator_replication_candidate_contrasts"], 5)
        self.assertFalse(report["statistical_simulation"]["performed"])
        self.assertEqual(summary["naive_protein_only"]["missed_expected_candidates"], 1)
        self.assertEqual(summary["naive_survivor_only"]["missed_expected_candidates"], 1)
        valid = report["structurally_valid_comparison"]
        self.assertEqual(valid["contrast_count"], 29)
        self.assertEqual(valid["expected_replication_candidate_contrasts"], 5)
        self.assertEqual(valid["naive_protein_only"]["acceptances_not_authorized_by_expected_rules"], 24)
        self.assertEqual(valid["naive_survivor_only"]["acceptances_not_authorized_by_expected_rules"], 24)

    def test_frozen_cases_detect_deliberately_broken_decision_rules(self):
        result = run_mutations()
        self.assertEqual(result["faults_tested"], 7)
        self.assertEqual(result["faults_detected"], 7)
        for row in result["results"]:
            self.assertTrue(row["detected_by_frozen_cases"], row["deliberate_fault"])


if __name__ == "__main__":
    unittest.main()
