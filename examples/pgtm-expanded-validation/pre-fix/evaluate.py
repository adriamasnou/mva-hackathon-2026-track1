#!/usr/bin/env python3
"""Evaluate frozen source-adjudicated expectations against shipped JavaScript.

Shared-source conformance only; not an independent clinical accuracy benchmark.
No production builders, shared tests or gates are executed or modified.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from collect_sources import collect

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE_NAMES = {"gene_condition_source_id": "ClinVar", "genes_to_disease.txt": "HPO", "mim2gene.txt": "OMIM-geneMIM"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs():
    receipt = json.loads((HERE / "expected-freeze.json").read_text())
    for filename, digest in (("expected.json", receipt["sha256"]),
                             ("source-excerpts.json", receipt["source_excerpt_sha256"]),
                             ("selection-plan.json", receipt["selection_sha256"])):
        if sha(HERE / filename) != digest:
            raise ValueError("Frozen input hash mismatch: " + filename)
    expected = json.loads((HERE / "expected.json").read_text())
    evidence = json.loads((HERE / "source-excerpts.json").read_text())
    verify_review(expected, evidence)
    return expected, evidence, receipt


def source_links(evidence, row):
    result = []
    for name, source in evidence["mapping_records"].items():
        for record in source["records"]:
            if record["mim"] in row["mims"]:
                for association in record["associations"]:
                    result.append({"gene": association["gene"], "mim": record["mim"],
                                   "source": SOURCE_NAMES[name], "file": name, "line": record["line"],
                                   "field": association["field"], "source_role": association["role"]})
    return result


def verify_review(expected, evidence):
    originals = {row["row"]: row for row in evidence["hfea_rows"]}
    reviews = {row["hfea_row"]: row for row in expected["row_reviews"]}
    if set(originals) != set(reviews) or len(reviews) != len(expected["row_reviews"]):
        raise ValueError("Incomplete or duplicate row adjudication")
    for number, review in reviews.items():
        original = originals[number]
        links = source_links(evidence, original)
        if links != review["reviewed_source_links"]:
            raise ValueError(f"Missing or altered reviewed source links: row {number}")
        if sorted({link["gene"] for link in links}) != review["expected_genes"]:
            raise ValueError(f"Manual gene set differs from source: row {number}")
        if original["mims"] != review["expected_mims"] or original["status"] != review["expected_status"]:
            raise ValueError(f"Expected identifiers/status differ from workbook: row {number}")
    for task in expected["queries"]:
        if not set(task["expected_rows"]) <= set(reviews):
            raise ValueError("Query has unreviewed expected rows: " + task["id"])


def canonical_expected(links):
    return {(item["gene"], item["source"], item["mim"]) for item in links}


def canonical_actual(row):
    evidence = json.loads(row["gene_evidence"])
    return {(gene, item["source"], item["omim"]) for gene, items in evidence.items() for item in items}


def assess_query(task, found, expected, evidence):
    errors = []
    originals = {row["row"]: row for row in evidence["hfea_rows"]}
    by_name = {row["condition"]: row["row"] for row in evidence["hfea_rows"]}
    reviews = {row["hfea_row"]: row for row in expected["row_reviews"]}
    actual_ids, row_results = [], []
    if found["query"] != task["query"]:
        errors.append("Query identity/order differs")
    if len(found["cards"]) != min(len(found["rows"]), 60):
        errors.append("Rendered card count differs")
    for index, row in enumerate(found["rows"]):
        number = by_name.get(row["condition"])
        actual_ids.append(number)
        if number is None:
            errors.append("Unreviewed returned condition: " + row["condition"])
            row_results.append({"condition": row["condition"], "reviewed": False})
            continue
        original, review = originals[number], reviews[number]
        row_errors = []
        for key, wanted in (("hfea_status", review["expected_status"]),
                            ("omim_as_published", original["omim_raw"]),
                            ("omim", ";".join(review["expected_mims"])),
                            ("clinvar_hpo", review["expected_source_agreement"]),
                            ("register_defect", review["expected_register_flags"]),
                            ("n_genes", len(review["expected_genes"]))):
            if row[key] != wanted:
                row_errors.append("Wrong " + key)
        actual_genes = row["genes"].split(";") if row["genes"] else []
        if actual_genes != review["expected_genes"]:
            row_errors.append("Incomplete/extra candidate gene set")
        wanted_links = canonical_expected(review["reviewed_source_links"])
        actual_links = canonical_actual(row)
        unsupported = sorted(actual_links - wanted_links)
        missing = sorted(wanted_links - actual_links)
        if unsupported or missing:
            row_errors.append("Per-gene source provenance differs")
        card = found["cards"][index] if index < len(found["cards"]) else []
        required = [row["condition"], review["expected_status"],
                    "Candidate gene(s): " + (", ".join(review["expected_genes"]) or "Unmapped")]
        if len(review["expected_genes"]) > 1:
            required.append("Multiple candidate genes")
        if review["expected_source_agreement"] == "differ":
            required.append("Sources disagree — review required")
        if review["expected_register_flags"]:
            required.append("Register flags: " + review["expected_register_flags"])
        missing_warnings = [text for text in required if text not in card]
        if missing_warnings:
            row_errors.append("Required card text/warning absent")
        actual_evidence = json.loads(row["gene_evidence"])
        qualifier_omissions = []
        for link in review["reviewed_source_links"]:
            if link["source_role"] not in ("POLYGENIC", "RelatedGenes"):
                continue
            rendered_gene = json.dumps(actual_evidence.get(link["gene"], []))
            if link["source_role"] not in rendered_gene:
                qualifier_omissions.append(link)
        row_results.append({"hfea_row": number, "condition": row["condition"], "reviewed": True,
                            "genes": actual_genes, "source_supported": not unsupported and not missing and not row_errors,
                            "source_unsupported_links": unsupported, "missing_source_links": missing,
                            "multiple_candidates": len(actual_genes) > 1,
                            "source_disagreement": review["expected_source_agreement"] == "differ",
                            "missing_required_card_text": missing_warnings,
                            "ambiguity_role_omissions": qualifier_omissions,
                            "errors": row_errors})
        errors.extend(f"row {number}: {error}" for error in row_errors)
    if actual_ids != task["expected_rows"]:
        errors.append("Complete returned row set/order differs from frozen expectations")
    if not task["expected_rows"] and "No match in this snapshot. Try a condition name, OMIM number or the live register." not in found["status"]:
        errors.append("No-match guidance absent")
    if task["kind"] == "alias" and "Alias BUBR1 → BUB1B." not in found["status"]:
        errors.append("Alias disclosure absent")
    literal = [number for number in task["expected_rows"]
               if task["query"].casefold() in originals[number]["condition"].casefold()]
    return {"id": task["id"], "query": task["query"], "kind": task["kind"], "stratum": task["stratum"],
            "expected_rows": task["expected_rows"], "observed_rows": actual_ids,
            "source_conformance_passed": not errors, "errors": errors,
            "literal_title_hits_among_expected_rows": literal,
            "status_text": found["status"], "row_reviews": row_results}


def run(hfea, source_dir, node):
    expected, evidence, freeze = frozen_inputs()
    if collect(hfea, source_dir) != evidence:
        raise ValueError("Original sources differ from the complete retained excerpts or selection")
    html = REPO / "submissions/pgtm-navigator.html"
    harness = REPO / "tools/pgtm/audit_query.cjs"
    # Read-only execution of the already shipped JavaScript; no builder import.
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    process = subprocess.run([str(node), str(harness), str(html)],
                             input=json.dumps([task["query"] for task in expected["queries"]]),
                             capture_output=True, text=True, check=True, timeout=30)
    found = json.loads(process.stdout)
    if len(found) != len(expected["queries"]):
        raise ValueError("Incomplete query execution")
    tasks = [assess_query(task, result, expected, evidence)
             for task, result in zip(expected["queries"], found)]
    unique_rows = {row["hfea_row"]: row for task in tasks for row in task["row_reviews"] if row["reviewed"]}
    genes = [task for task in tasks if task["kind"] == "gene"]
    positive_genes = [task for task in genes if task["expected_rows"]]
    qualifier_omissions = [{"hfea_row": number, **link} for number, row in unique_rows.items()
                           for link in row["ambiguity_role_omissions"]]
    notice = "Approval of a condition does not establish a particular variant, a family's eligibility, funding or suitability."
    static_html = html.read_text()
    if notice not in static_html or "other aliases are not inferred" not in static_html:
        raise ValueError("Required eligibility/alias limitation absent from shipped HTML")
    summary = {
        "queries": len(tasks), "source_conformance_passed": sum(task["source_conformance_passed"] for task in tasks),
        "gene_queries": len(genes), "source_expected_positive_gene_queries": len(positive_genes),
        "source_expected_no_match_gene_queries": len(genes) - len(positive_genes),
        "positive_gene_queries_retrieving_all_expected_rows": sum(task["source_conformance_passed"] for task in positive_genes),
        "literal_title_queries_retrieving_at_least_one_expected_row": sum(bool(task["literal_title_hits_among_expected_rows"]) for task in positive_genes),
        "positive_gene_query_row_instances": sum(len(task["expected_rows"]) for task in positive_genes),
        "literal_title_hits_in_those_row_instances": sum(len(task["literal_title_hits_among_expected_rows"]) for task in positive_genes),
        "unique_returned_rows_reviewed": len(unique_rows),
        "unreviewed_returned_rows": sum(not row["reviewed"] for task in tasks for row in task["row_reviews"]),
        "distinct_returned_row_gene_associations": sum(len(row["genes"]) for row in unique_rows.values()),
        "source_unsupported_links": sum(len(row["source_unsupported_links"]) for row in unique_rows.values()),
        "missing_source_links": sum(len(row["missing_source_links"]) for row in unique_rows.values()),
        "multiple_candidate_rows": sum(row["multiple_candidates"] for row in unique_rows.values()),
        "source_disagreement_rows": sum(row["source_disagreement"] for row in unique_rows.values()),
        "rows_missing_required_card_text": sum(bool(row["missing_required_card_text"]) for row in unique_rows.values()),
        "distinct_returned_row_gene_ambiguity_role_omissions": len(qualifier_omissions),
        "rows_with_ambiguity_role_omissions": len({item["hfea_row"] for item in qualifier_omissions})
    }
    return {
        "schema_version": 1, "claim_scope": "Same-developer, shared-source retrieval and ambiguity audit. Not independent clinical accuracy, eligibility, user outcomes or time savings.",
        "selection_freeze": json.loads((HERE / "selection-freeze.json").read_text()),
        "expectation_freeze": freeze, "query_execution_started_utc": started,
        "source_verification": "Whole original file hashes, original workbook cells, and complete selected/context mapping excerpts verified before queries.",
        "input_sha256": {**{name: sha(HERE / name) for name in ("selection-plan.json", "expected.json", "source-excerpts.json", "collect_sources.py", "evaluate.py")},
                         "pgtm-navigator.html": sha(html), "audit_query.cjs": sha(harness)},
        "source_review_coverage": {"primary_workbook_rows": len(evidence["hfea_rows"]),
                                   "context_workbook_rows": len(evidence["context_rows"]),
                                   "primary_mapping_records": sum(len(source["records"]) for source in evidence["mapping_records"].values()),
                                   "context_mapping_records": sum(len(source["context_records"]) for source in evidence["mapping_records"].values()),
                                   "reviewed_before_queries": True},
        "summary": summary, "ambiguity_role_omissions": qualifier_omissions,
        "clinical_promotion_assessment": {
            "independent_clinical_truth": "Unavailable for the full association set; no clinical accuracy or false-positive rate calculated.",
            "observed_static_framing": "Condition status, candidate-gene labels and explicit non-eligibility notice are retained. No explicit claim that each candidate gene/variant/family is approved was identified in reviewed template/card text.",
            "remaining_risk": "POLYGENIC and RelatedGenes qualifiers are omitted from per-gene details. Candidate genes appear alongside condition-level approval. That semantic loss can support overinterpretation; comprehension and real-world decisions were not studied.",
            "source_sharing": "Builder and audit share original snapshots; HPO and ClinVar can share upstream records. Correct transcription is not independent biological truth. Same developer authored selection, expectations and evaluation."
        },
        "tasks": tasks,
        "raw_query_results": found,
        "source_conformance_status": "PASS" if all(task["source_conformance_passed"] for task in tasks) else "FAIL",
        "overall_interpretation": "Source conformance and semantic limitations must be reported together; a retrieval pass does not close qualifier loss or clinical validity."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hfea", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--node", type=Path, default=Path("node"))
    args = parser.parse_args()
    try:
        result = run(args.hfea, args.source_dir, args.node)
    except (OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError) as error:
        print(json.dumps({"source_conformance_status": "ERROR", "error": str(error),
                          "claim_scope": "No conformance conclusion when verification/runtime fails."}, indent=2))
        sys.exit(2)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["source_conformance_status"] == "PASS" else 1)
