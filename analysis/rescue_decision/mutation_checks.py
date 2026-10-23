"""Check that frozen expectations detect deliberate faults in our own evaluator.

No repository files are modified. Only the in-memory, single-edit variants below
are executed. This is a bounded test-strength check, not comprehensive mutation
coverage and not a statistical/biological simulation.
"""

from pathlib import Path
from casebook import load_casebook, materialize


MUTATIONS = (
    ("accept_lower_ci_touching_delta", 'return "pass" if lower > threshold else "fail" if upper < threshold else "inconclusive"',
     'return "pass" if lower >= threshold else "fail" if upper < threshold else "inconclusive"'),
    ("reject_upper_ci_touching_delta", 'return "pass" if lower > threshold else "fail" if upper < threshold else "inconclusive"',
     'return "pass" if lower > threshold else "fail" if upper <= threshold else "inconclusive"'),
    ("ignore_fate_measurement_control", '(f["measurement_qualified"], "FATE_MEASUREMENT_UNQUALIFIED"),',
     '(True, "FATE_MEASUREMENT_UNQUALIFIED"),'),
    ("ignore_qualified_exposure_window", 'if not e["within_qualified_window"]:', 'if False:'),
    ("ignore_failed_fate_bounds", 'if result == "fail":', 'if False:'),
    ("discard_qualified_hsp_negative_functional_hit", '(a["hsp_response"] != "indeterminate", "HSP_MEASUREMENT_INDETERMINATE"),',
     '(a["hsp_response"] == "present", "HSP_MEASUREMENT_INDETERMINATE"),'),
    ("force_primary_benefit_to_pass", 'efficacy = relation(stats["benefit_ci"], plan["smallest_worthwhile_reduction"])',
     'efficacy = "pass"'),
)


def run_mutations():
    book, _ = load_casebook()
    source = (Path(__file__).resolve().parent / "decision.py").read_text()
    rows = []
    for name, original, replacement in MUTATIONS:
        if source.count(original) != 1:
            raise ValueError(f"Mutation anchor must match exactly once: {name}")
        namespace = {"__name__": "research_decision_deliberate_fault"}
        exec(compile(source.replace(original, replacement, 1), f"<deliberate-fault:{name}>", "exec"), namespace)
        detected_by = []
        for case in book["cases"]:
            result = namespace["evaluate"](materialize(book, case))
            observed = [row["decision"] for row in result["contrasts"]] if result["input_valid"] else ["INVALID_INPUT"]
            if observed != case["expected_decisions"]:
                detected_by.append(case["id"])
        rows.append({"deliberate_fault": name, "detected": bool(detected_by),
                     "detected_by_frozen_cases": detected_by})
    return {"scope": "Seven deliberately faulty in-memory versions of our own evaluator; no files changed. Not exhaustive mutation coverage or biological simulation.",
            "faults_tested": len(rows), "faults_detected": sum(row["detected"] for row in rows),
            "results": rows}
