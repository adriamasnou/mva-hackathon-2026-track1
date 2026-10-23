#!/usr/bin/env python3
"""Fail-closed research decision logic; no statistical fitting or medical decisions.

Only supplied, qualified, replicate-aware estimates are classified. Qualification
records and assertions are requirements, not evidence this program can authenticate.
See README.md for the narrow observation schema and scientific limitations.
"""

import argparse
from decimal import Decimal
import json
from pathlib import Path
import sys


SCOPE = "Research prototype: eligibility for independent replication only; not a medical device or biological evidence."
COUNTS = ("starting_cells", "mitotic_entries", "completed_divisions",
          "segregation_errors", "deaths", "persistent_arrests", "censored")
METHODS = ("single_prespecified_contrast", "bonferroni", "simultaneous_model",
           "other_prespecified")


class InputError(ValueError):
    """Malformed or internally inconsistent decision inputs."""


def require(condition, path, message):
    if not condition:
        raise InputError(f"{path}: {message}")


def fields(value, names, path):
    require(isinstance(value, dict), path, "must be an object")
    require(all(type(key) is str for key in value), path, "object keys must be strings")
    expected = set(names.split())
    require(set(value) == expected, path,
            f"missing fields {sorted(expected - set(value))}; unknown fields {sorted(set(value) - expected)}")


def string(value, path):
    require(isinstance(value, str) and bool(value.strip()), path, "must be a nonempty string")


def boolean(value, path):
    require(type(value) is bool, path, "must be a JSON boolean")


def number(value, path, low=None, high=None):
    require(type(value) in (int, float, Decimal), path, "must be a number, not a boolean or numeric string")
    result = Decimal(str(value))
    require(result.is_finite(), path, "must be finite")
    require(low is None or result >= Decimal(str(low)), path, f"must be >= {low}")
    require(high is None or result <= Decimal(str(high)), path, f"must be <= {high}")
    return result


def integer(value, path, minimum=0):
    require(type(value) is int and value >= minimum, path, f"must be an integer >= {minimum}")


def interval(value, path, low=None, high=None):
    require(isinstance(value, list) and len(value) == 2, path, "must be [lower, upper]")
    lower = number(value[0], path + "/0", low, high)
    upper = number(value[1], path + "/1", low, high)
    require(lower <= upper, path, "lower bound exceeds upper bound")
    return lower, upper


def member(value, choices, path):
    require(isinstance(value, str) and value in choices, path, f"must be one of {choices}")


def strings(obj, keys, path):
    for key in keys.split():
        string(obj[key], f"{path}/{key}")


def booleans(obj, keys, path):
    for key in keys.split():
        boolean(obj[key], f"{path}/{key}")


def confidence(value, path):
    require(0 < number(value, path) < 1, path, "must lie strictly between 0 and 1")


def validate(data):
    """Validate the entire submitted family before permitting any positive result."""
    fields(data, "schema_version study_id model plan contrasts", "/")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "/schema_version", "unsupported version")
    string(data["study_id"], "/study_id")
    model = data["model"]
    fields(model, "qualified record", "/model")
    boolean(model["qualified"], "/model/qualified")
    string(model["record"], "/model/record")
    plan = data["plan"]
    fields(plan, "record frozen_before_confirmation threshold_basis smallest_worthwhile_reduction "
           "confidence_level comparison_family multiplicity followup_hours division_handling "
           "incomplete_followup_record biomarker_schedule_record design_record pilot_record "
           "power_plan_record fate_boundary_rule fate_bounds", "/plan")
    strings(plan, "record threshold_basis incomplete_followup_record biomarker_schedule_record "
            "design_record pilot_record power_plan_record", "/plan")
    boolean(plan["frozen_before_confirmation"], "/plan/frozen_before_confirmation")
    require(0 < number(plan["smallest_worthwhile_reduction"], "/plan/smallest_worthwhile_reduction") < 1,
            "/plan/smallest_worthwhile_reduction", "must lie strictly between 0 and 1")
    confidence(plan["confidence_level"], "/plan/confidence_level")
    require(number(plan["followup_hours"], "/plan/followup_hours") > 0,
            "/plan/followup_hours", "must be positive")
    member(plan["division_handling"], ("first_completed_division_per_starting_cell",), "/plan/division_handling")
    member(plan["fate_boundary_rule"], ("strict_interior",), "/plan/fate_boundary_rule")
    bounds = plan["fate_bounds"]
    fields(bounds, "minimum_division_ratio maximum_excess_death maximum_excess_arrest maximum_excess_censoring", "/plan/fate_bounds")
    require(number(bounds["minimum_division_ratio"], "/plan/fate_bounds/minimum_division_ratio") > 0,
            "/plan/fate_bounds/minimum_division_ratio", "must be positive")
    for key in ("maximum_excess_death", "maximum_excess_arrest", "maximum_excess_censoring"):
        number(bounds[key], "/plan/fate_bounds/" + key, 0, 1)
    family = plan["comparison_family"]
    require(isinstance(family, list), "/plan/comparison_family", "must be an array")
    for item in family:
        string(item, "/plan/comparison_family")
    require(len(set(family)) == len(family), "/plan/comparison_family", "duplicate IDs")
    fields(plan["multiplicity"], "method record", "/plan/multiplicity")
    member(plan["multiplicity"]["method"], METHODS, "/plan/multiplicity/method")
    string(plan["multiplicity"]["record"], "/plan/multiplicity/record")
    require(len(family) <= 1 or plan["multiplicity"]["method"] != "single_prespecified_contrast",
            "/plan/multiplicity", "multiple eligible contrasts require a family coverage plan")
    contrasts = data["contrasts"]
    require(isinstance(contrasts, list) and len(contrasts) > 0, "/contrasts", "must be a nonempty array")
    ids, eligible = [], []
    for index, contrast in enumerate(contrasts):
        path = f"/contrasts/{index}"
        fields(contrast, "id role exposure assays analysis observations fate", path)
        string(contrast["id"], path + "/id")
        ids.append(contrast["id"])
        member(contrast["role"], ("confirmatory", "exploratory"), path + "/role")
        if contrast["role"] == "confirmatory":
            eligible.append(contrast["id"])
        exposure = contrast["exposure"]
        fields(exposure, "measurement_qualified within_qualified_window record compound_form active_moiety_basis matrix sampling_hours fraction binding_context", path + "/exposure")
        booleans(exposure, "measurement_qualified within_qualified_window", path + "/exposure")
        strings(exposure, "record compound_form active_moiety_basis matrix binding_context", path + "/exposure")
        number(exposure["sampling_hours"], path + "/exposure/sampling_hours", 0)
        member(exposure["fraction"], ("total", "unbound"), path + "/exposure/fraction")
        assays = contrast["assays"]
        fields(assays, "function_controls_qualified response_controls_qualified required_secondaries_complete record hsp_response protein_ratio survivor_normal_fraction_change", path + "/assays")
        booleans(assays, "function_controls_qualified response_controls_qualified required_secondaries_complete", path + "/assays")
        string(assays["record"], path + "/assays/record")
        member(assays["hsp_response"], ("present", "absent", "indeterminate"), path + "/assays/hsp_response")
        number(assays["protein_ratio"], path + "/assays/protein_ratio", 0)
        # Optional comparator observation, never an efficacy requirement. Explicit
        # null means not measured; omission is a schema error to catch typos.
        if assays["survivor_normal_fraction_change"] is not None:
            number(assays["survivor_normal_fraction_change"], path + "/assays/survivor_normal_fraction_change", -1, 1)
        analysis = contrast["analysis"]
        fields(analysis, "record unit nesting_handled multiplicity_adjusted confidence_level benefit_ci biological_replicates", path + "/analysis")
        string(analysis["record"], path + "/analysis/record")
        member(analysis["unit"], ("independent_culture",), path + "/analysis/unit")
        booleans(analysis, "nesting_handled multiplicity_adjusted", path + "/analysis")
        confidence(analysis["confidence_level"], path + "/analysis/confidence_level")
        require(number(analysis["confidence_level"], path) == number(plan["confidence_level"], path),
                path + "/analysis/confidence_level", "does not match the frozen plan")
        interval(analysis["benefit_ci"], path + "/analysis/benefit_ci", -1, 1)
        fields(analysis["biological_replicates"], "vehicle treated", path + "/analysis/biological_replicates")
        observations = contrast["observations"]
        fields(observations, "vehicle treated", path + "/observations")
        for arm in ("vehicle", "treated"):
            rows = observations[arm]
            arm_path = path + "/observations/" + arm
            require(isinstance(rows, list) and len(rows) > 0, arm_path, "must list independent cultures")
            n = analysis["biological_replicates"][arm]
            integer(n, path + "/analysis/biological_replicates/" + arm, 1)
            require(n == len(rows), arm_path, "culture count disagrees with declared biological replicates")
            culture_ids = []
            for row_index, row in enumerate(rows):
                row_path = arm_path + f"/{row_index}"
                fields(row, "culture_id " + " ".join(COUNTS), row_path)
                string(row["culture_id"], row_path + "/culture_id")
                culture_ids.append(row["culture_id"])
                for count in COUNTS:
                    integer(row[count], row_path + "/" + count, 1 if count == "starting_cells" else 0)
                require(row["segregation_errors"] <= row["completed_divisions"] <= row["mitotic_entries"] <= row["starting_cells"],
                        row_path, "first-division count ordering is inconsistent")
                for count in ("deaths", "persistent_arrests", "censored"):
                    require(row[count] <= row["starting_cells"], row_path + "/" + count, "exceeds starting cells")
            require(len(set(culture_ids)) == len(culture_ids), arm_path, "duplicate culture IDs")
            require(sum(row["completed_divisions"] for row in rows) > 0, arm_path, "conditional primary endpoint has no completed divisions")
        fate = contrast["fate"]
        fields(fate, "record measurement_qualified confidence_level coverage_qualified division_ratio_ci excess_death_ci excess_arrest_ci excess_censoring_ci selection_assessment", path + "/fate")
        string(fate["record"], path + "/fate/record")
        booleans(fate, "measurement_qualified coverage_qualified", path + "/fate")
        confidence(fate["confidence_level"], path + "/fate/confidence_level")
        require(number(fate["confidence_level"], path) == number(plan["confidence_level"], path),
                path + "/fate/confidence_level", "does not match the frozen plan")
        interval(fate["division_ratio_ci"], path + "/fate/division_ratio_ci", 0)
        for key in ("excess_death_ci", "excess_arrest_ci", "excess_censoring_ci"):
            interval(fate[key], path + "/fate/" + key, -1, 1)
        member(fate["selection_assessment"], ("excluded", "detected", "unresolved"), path + "/fate/selection_assessment")
    require(len(set(ids)) == len(ids), "/contrasts", "duplicate contrast IDs")
    require(set(eligible) == set(family), "/plan/comparison_family",
            "must match all and only supplied confirmatory contrasts; missing family members block the entire evaluation")


def relation(ci, threshold, lower_is_better=False):
    """No epsilon or rounding: equality with either endpoint is inconclusive."""
    lower, upper = (Decimal(str(value)) for value in ci)
    threshold = Decimal(str(threshold))
    if lower_is_better:
        return "pass" if upper < threshold else "fail" if lower > threshold else "inconclusive"
    return "pass" if lower > threshold else "fail" if upper < threshold else "inconclusive"


def invalid_result(message):
    return {"schema_version": 1, "scope": SCOPE, "input_valid": False,
            "errors": [message], "decision": "INVALID_INPUT",
            "reason_codes": ["INVALID_INPUT"], "replication_candidate_ids": [], "contrasts": []}


def evaluate(data):
    """Pure evaluation; never mutates input, reads files, or fits a statistical model."""
    try:
        validate(data)
    except InputError as error:
        return invalid_result(str(error))
    plan = data["plan"]
    output = {"schema_version": 1, "scope": SCOPE, "input_valid": True,
              "study_id": data["study_id"], "errors": [],
              "replication_candidate_ids": [], "contrasts": []}
    for contrast in data["contrasts"]:
        a, e, f, stats = (contrast[key] for key in ("assays", "exposure", "fate", "analysis"))
        technical = []
        for passed, code in (
            (data["model"]["qualified"], "MODEL_UNQUALIFIED"),
            (plan["frozen_before_confirmation"], "PLAN_NOT_FROZEN"),
            (e["measurement_qualified"], "EXPOSURE_MEASUREMENT_UNQUALIFIED"),
            (a["function_controls_qualified"], "FUNCTION_CONTROLS_UNQUALIFIED"),
            (a["response_controls_qualified"], "RESPONSE_CONTROLS_UNQUALIFIED"),
            (a["required_secondaries_complete"], "REQUIRED_SECONDARIES_INCOMPLETE"),
            (a["hsp_response"] != "indeterminate", "HSP_MEASUREMENT_INDETERMINATE"),
            (stats["nesting_handled"], "NESTING_NOT_ACCOUNTED_FOR"),
            (stats["multiplicity_adjusted"], "MULTIPLICITY_NOT_ACCOUNTED_FOR"),
            (f["measurement_qualified"], "FATE_MEASUREMENT_UNQUALIFIED"),
            (f["coverage_qualified"], "FATE_COVERAGE_UNQUALIFIED"),
        ):
            if not passed:
                technical.append(code)
        efficacy = relation(stats["benefit_ci"], plan["smallest_worthwhile_reduction"])
        fate_relations = {}
        blocks, uncertain = [], []
        if not e["within_qualified_window"]:
            blocks.append("OUTSIDE_QUALIFIED_EXPOSURE_WINDOW")
        for name, ci, bound, lower_better in (
            ("DIVISION", "division_ratio_ci", "minimum_division_ratio", False),
            ("DEATH", "excess_death_ci", "maximum_excess_death", True),
            ("ARREST", "excess_arrest_ci", "maximum_excess_arrest", True),
            ("CENSORING", "excess_censoring_ci", "maximum_excess_censoring", True),
        ):
            result = relation(f[ci], plan["fate_bounds"][bound], lower_better)
            fate_relations[name.lower()] = result
            if result == "fail":
                blocks.append(name + "_BOUND_FAILED")
            elif result == "inconclusive":
                uncertain.append(name + "_BOUND_INCONCLUSIVE")
        if f["selection_assessment"] == "detected":
            blocks.append("SELECTION_DETECTED")
        elif f["selection_assessment"] == "unresolved":
            uncertain.append("SELECTION_UNRESOLVED")
        reasons = technical + blocks + uncertain
        # Technical failure takes precedence over apparent positives AND negatives.
        if technical:
            decision = "TECHNICALLY_INDETERMINATE"
        else:
            if efficacy == "fail":
                reasons.append("BENEFIT_UPPER_BELOW_DELTA")
            elif efficacy == "inconclusive":
                reasons.append("BENEFIT_TOUCHES_OR_CROSSES_DELTA")
            if blocks:
                decision = "DO_NOT_ADVANCE"
            elif efficacy == "fail":
                decision = "WORTHWHILE_BENEFIT_RULED_OUT"
            elif efficacy == "inconclusive" or uncertain:
                decision = "INCONCLUSIVE"
            elif contrast["role"] == "exploratory":
                decision = "EXPLORATORY_SIGNAL"
                reasons.append("EXPLORATORY_ONLY")
            else:
                decision = "REPLICATION_CANDIDATE"
        mechanism = "UNINTERPRETABLE"
        if not technical:
            mechanism = "HSP_RESPONSE_PRESENT_NOT_CAUSAL" if a["hsp_response"] == "present" else "DISCORDANT_REQUIRES_INVESTIGATION"
            if a["hsp_response"] == "absent" and efficacy == "pass":
                reasons.append("HSP_DISCORDANT_INVESTIGATE")
        denominators = {}
        for arm, rows in contrast["observations"].items():
            denominators[arm] = {"independent_cultures": len(rows),
                                 **{key: sum(row[key] for row in rows) for key in COUNTS}}
        row = {"id": contrast["id"], "role": contrast["role"], "decision": decision,
               "reason_codes": reasons,
               "criteria": {"primary_interval_relation": efficacy,
                            "fate_interval_relations": fate_relations,
                            "exposure_measurement_qualified": e["measurement_qualified"],
                            "within_qualified_exposure_window": e["within_qualified_window"],
                            "selection_assessment": f["selection_assessment"],
                            "biological_interpretation_permitted_by_declared_controls": not bool(technical),
                            "hsp_mechanism": mechanism},
               "denominators": denominators,
               "limit": "Interval relations are arithmetic on supplied estimates. A candidate requires independent replication, not treatment; no clinical benefit, N1002K defect or causal mechanism is established."}
        output["contrasts"].append(row)
        if decision == "REPLICATION_CANDIDATE":
            output["replication_candidate_ids"].append(contrast["id"])
    return output


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "/", f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise InputError(f"Nonstandard nonfinite JSON number {value}")


def loads(text):
    """Strict JSON numbers, duplicate-key rejection, decimal boundary preservation."""
    return json.loads(text, parse_float=Decimal, parse_constant=reject_constant,
                      object_pairs_hook=no_duplicates)


def main(argv=None):
    parser = argparse.ArgumentParser(description=SCOPE)
    parser.add_argument("input", type=Path, help="Decision-input JSON; never writes or uploads inputs")
    args = parser.parse_args(argv)
    try:
        result = evaluate(loads(args.input.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as error:
        result = invalid_result(str(error))
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["input_valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
