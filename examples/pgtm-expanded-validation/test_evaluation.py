"""Targeted failure tests for expanded source-conformance evaluation only."""
from copy import deepcopy
import datetime
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evaluate

EXPECTED, EVIDENCE, FREEZE = evaluate.frozen_inputs()
RESULT = json.loads((evaluate.REPO / "submissions/pgtm-expanded-validation.json").read_text())
PRE_FIX = json.loads((evaluate.HERE / "pre-fix/pgtm-expanded-validation.json").read_text())
spec = importlib.util.spec_from_file_location('pre_fix_evaluator', evaluate.HERE / 'pre-fix/evaluate.py')
pre_fix_evaluator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pre_fix_evaluator)


def task_and_output(query, result=RESULT):
    index = next(index for index, task in enumerate(EXPECTED["queries"]) if task["query"] == query)
    return EXPECTED["queries"][index], deepcopy(result["raw_query_results"][index])


class ExpandedEvaluationTests(unittest.TestCase):
    def test_complete_frozen_review_and_prequery_order(self):
        self.assertEqual(len(EXPECTED["queries"]), 28)
        self.assertEqual(len(EXPECTED["row_reviews"]), 45)
        self.assertEqual(sum(len(row["expected_genes"]) for row in EXPECTED["row_reviews"]), 57)
        self.assertEqual(sum(len(source["records"]) for source in EVIDENCE["mapping_records"].values()), 141)
        self.assertEqual(sum(len(source["context_records"]) for source in EVIDENCE["mapping_records"].values()), 11)
        before = datetime.datetime.fromisoformat(FREEZE["frozen_at_utc"])
        queried = datetime.datetime.fromisoformat(RESULT["query_execution_started_utc"])
        self.assertLess(before, queried)

    def test_deleted_related_gene_record_fails_even_without_hash_check(self):
        evidence = deepcopy(EVIDENCE)
        records = evidence["mapping_records"]["gene_condition_source_id"]["records"]
        evidence["mapping_records"]["gene_condition_source_id"]["records"] = [record for record in records if record["line"] != 12260]
        with self.assertRaisesRegex(ValueError, "row 1675"):
            evaluate.verify_review(EXPECTED, evidence)

    def test_incomplete_manual_gene_set_is_not_accepted_as_truth(self):
        expected = deepcopy(EXPECTED)
        row = next(row for row in expected["row_reviews"] if row["hfea_row"] == 503)
        row["expected_genes"].remove("FCGR2A")
        with self.assertRaisesRegex(ValueError, "Manual gene set differs"):
            evaluate.verify_review(expected, EVIDENCE)

    def test_source_role_changes_are_detected(self):
        evidence = deepcopy(EVIDENCE)
        record = next(record for record in evidence["mapping_records"]["genes_to_disease.txt"]["records"] if record["line"] == 873)
        record["associations"][0]["role"] = "MENDELIAN"
        with self.assertRaisesRegex(ValueError, "row 503"):
            evaluate.verify_review(EXPECTED, evidence)

    def test_target_only_match_cannot_hide_missing_additional_rows(self):
        task, found = task_and_output("DMD")
        found["rows"] = found["rows"][-1:]
        found["cards"] = found["cards"][-1:]
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertIn("Complete returned row set/order differs from frozen expectations", result["errors"])

    def test_unreviewed_extra_row_fails_closed(self):
        task, found = task_and_output("CFTR")
        extra = deepcopy(found["rows"][0])
        extra["condition"] = "UNREVIEWED SYNTHETIC CONDITION"
        found["rows"].append(extra)
        found["cards"].append(["UNREVIEWED SYNTHETIC CONDITION"])
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertFalse(result["row_reviews"][-1]["reviewed"])

    def test_same_genes_with_unsupported_source_link_fail(self):
        task, found = task_and_output("CFTR")
        links = json.loads(found["rows"][0]["gene_evidence"])
        links["CFTR"][0]["omim"] = "999999"
        found["rows"][0]["gene_evidence"] = json.dumps(links)
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertEqual(len(result["row_reviews"][0]["source_unsupported_links"]), 1)
        self.assertEqual(len(result["row_reviews"][0]["missing_source_links"]), 1)

    def test_mapping_correct_but_ambiguity_warning_missing_fails(self):
        task, found = task_and_output("CFTR")
        found["cards"][0].remove("Multiple candidate genes")
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertIn("Multiple candidate genes", result["row_reviews"][0]["missing_required_card_text"])

    def test_qualifier_loss_is_reported_despite_source_conformance(self):
        task, found = task_and_output("CFTR", PRE_FIX)
        result = pre_fix_evaluator.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertTrue(result["source_conformance_passed"])
        lost = {(item["gene"], item["source_role"]) for row in result["row_reviews"] for item in row["ambiguity_role_omissions"]}
        self.assertEqual(lost, {("FCGR2A", "POLYGENIC"), ("TGFB1", "POLYGENIC"),
                                ("CFTR", "POLYGENIC"), ("CTRC", "POLYGENIC"), ("PRSS2", "POLYGENIC")})

    def test_retained_11_pairs_and_frozen_facts_unchanged(self):
        self.assertEqual(len(PRE_FIX["ambiguity_role_omissions"]), 11)
        self.assertEqual(RESULT["before_after"]["original_11_omissions"], PRE_FIX["ambiguity_role_omissions"])
        self.assertEqual(RESULT["ambiguity_role_omissions"], [])
        self.assertEqual(RESULT["summary"]["source_conformance_passed"], 28)
        for name in ("selection-plan.json", "expected.json", "source-excerpts.json"):
            self.assertEqual(PRE_FIX["input_sha256"][name], RESULT["input_sha256"][name])
            self.assertEqual(evaluate.sha(evaluate.HERE / name), RESULT["input_sha256"][name])

    def test_pre_fix_payload_fails_new_role_and_visible_label_checks(self):
        task, found = task_and_output("CFTR", PRE_FIX)
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertFalse(result["row_reviews"][0]["source_role_metadata_matches"])
        self.assertTrue(result["row_reviews"][0]["missing_visible_source_labels"])

    def test_correct_word_on_wrong_gene_is_rejected(self):
        task, found = task_and_output("CFTR")
        links = json.loads(found["rows"][0]["gene_evidence"])
        for gene, wrong in (("FCGR2A", "MENDELIAN"), ("CFTR", "POLYGENIC")):
            next(item for item in links[gene] if item["source"] == "HPO")["association_type"] = wrong
        found["rows"][0]["gene_evidence"] = json.dumps(links)
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertEqual(result["row_reviews"][0]["source_unsupported_links"], [])
        self.assertIn("FCGR2A", {x["gene"] for x in result["row_reviews"][0]["ambiguity_role_omissions"]})

    def test_metadata_in_collapsed_details_only_does_not_pass(self):
        task, found = task_and_output("CFTR")
        next(group for group in found["geneGroups"][0] if group["gene"] == "TGFB1")["labels"] = []
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertTrue(result["row_reviews"][0]["source_role_metadata_matches"])
        self.assertEqual([x["gene"] for x in result["row_reviews"][0]["ambiguity_role_omissions"]], ["TGFB1"])

    def test_correct_visible_role_under_wrong_gene_is_rejected(self):
        task, found = task_and_output("CFTR")
        groups = {group["gene"]: group for group in found["geneGroups"][0]}
        groups["CFTR"]["labels"], groups["TGFB1"]["labels"] = groups["TGFB1"]["labels"], groups["CFTR"]["labels"]
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertTrue(result["row_reviews"][0]["source_role_metadata_matches"])
        self.assertTrue(result["row_reviews"][0]["unexpected_visible_source_labels"])
        self.assertEqual([x["gene"] for x in result["row_reviews"][0]["ambiguity_role_omissions"]], ["TGFB1"])

    def test_relatedgenes_changed_to_associatedgenes_is_rejected(self):
        task, found = task_and_output("QDPR")
        i = next(i for i, row in enumerate(found["rows"]) if row["omim"] == "261600")
        links = json.loads(found["rows"][i]["gene_evidence"])
        links["QDPR"][0]["source_field"] = "AssociatedGenes"
        found["rows"][i]["gene_evidence"] = json.dumps(links)
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertFalse(result["row_reviews"][i]["source_role_metadata_matches"])

    def test_unqualified_status_is_rejected_even_when_condition_status_exists(self):
        task, found = task_and_output("BUB1B")
        found["cards"][0].append("approved")
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertIn("Approval status is not visibly restricted to the condition", result["row_reviews"][0]["errors"])

    def test_bad_original_verification_blocks_runtime(self):
        changed = deepcopy(EVIDENCE)
        changed["selection_mims"] = []
        with patch.object(evaluate, "collect", return_value=changed), patch.object(evaluate.subprocess, "run") as runtime:
            with self.assertRaisesRegex(ValueError, "Original sources differ"):
                evaluate.run(Path("unused"), Path("unused"), Path("unused"))
            runtime.assert_not_called()

    def test_missing_runtime_does_not_return_skipped_success(self):
        with patch.object(evaluate, "collect", return_value=EVIDENCE), patch.object(evaluate.subprocess, "run", side_effect=FileNotFoundError("missing-node")):
            with self.assertRaises(FileNotFoundError):
                evaluate.run(Path("unused"), Path("unused"), Path("missing-node"))

    def test_query_identity_mismatch_fails(self):
        task, found = task_and_output("BUB1B")
        found["query"] = "WRONG QUERY"
        result = evaluate.assess_query(task, found, EXPECTED, EVIDENCE)
        self.assertFalse(result["source_conformance_passed"])
        self.assertIn("Query identity/order differs", result["errors"])


if __name__ == "__main__":
    unittest.main()
