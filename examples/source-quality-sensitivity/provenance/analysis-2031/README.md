# Private post-hoc source-audit sensitivity, frozen at 20:31

This is an outcome-linked, non-blinded descriptive analysis with explicit `per_case` exposure. It retains all 713 frozen cases and both arms, including every preparation or ranking failure. It does not change source annotations, case labels, selected packets, inference, or evaluation. `contradicted` describes source correspondence of an assertion; it does not mean a disproved diagnosis.

The exact source manifest is `ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0`: 262 main texts, 147 complete papers, 1169 adjudicated mappings, and 322 complete cases. Its entire 613-file snapshot and eight benchmark/provenance files are frozen as read-only byte copies under `/Volumes/easystore/MVA-deadline-build-20261024/sensitivity-2031/inputs`. `immutable-input-hashes.json` records every original and frozen path, size and SHA256. The original literal evaluation is retained alongside corrected v2; the analysis uses corrected v2 throughout.

`joined-cases.jsonl` has one row per frozen case, in original case order. Each retains the selected member and packet hash, every selected/alternate mapping, source-review availability and raw assessment statuses/item hashes, both corrected arm outcomes, and both literal-original outcomes. Indexes and canonical hashes point to each full unchanged evaluation row in the frozen JSON. Pending selected reviews retain their raw labels but belong to `unreviewed` strata; those labels are never counted as adjudicated support.

`all-strata.json` reports all seven named dimensions across all six frozen benchmark cohorts: 162 categories, including 15 empty categories. Each category includes its exact case IDs, denominator, top1/5/10 counts and rates, status/failure counts, ties, and paired both/original-only/none-only/neither counts with both total and discordant denominators. Empty rates are null. These are separate marginal partitions, not outcome-selected intersections. `methods.json` defines every partition. `frozen-baseline-strata.json` retains every original and corrected endpoint and aggregate, including secondary endpoints, without relabeling.

For all 713 cases, original-HPO versus no-HPO recovery counts at top1/5/10 remain 581/681/693 versus 449/677/693. Top1 paired counts are 416 both, 165 original-only, 33 no-HPO-only, and 99 neither; all 713 pairs remain. At top5 the discordant counts are 15 versus 11; top10 has no discordant pair and 20 failures in both arms. The primary 681 counts remain 556/653/665 versus 430/649/665. The technical-X 32 counts remain 25/28/28 versus 19/28/28, retaining all four preparation failures per arm.

All linked papers and packets are complete for 322 cases: top1/5/10 counts 271/310/315 versus 196/305/315, with top1 discordance 83 versus 8. The other categories remain visible: 316 incomplete cases and 75 with no linked paper review. Packet adjudication alone is complete for 601 cases, partial for 8, and absent for 104. These different definitions must not be interchanged.

Selected-packet categories are supported 0, qualified 93, contradicted 205, unresolved 308, and unreviewed 107 (77 no record, 30 pending). Genotype statuses are supported 153, qualified 408, contradicted 11, unresolved 34, and unreviewed 107. Causal-confidence statuses are supported 1, qualified 548, contradicted 48, unresolved 9, and unreviewed 107. There are 148 selected packets with a recorded phenotype-item contradiction, 458 adjudicated packets with none recorded, and 107 unreviewed. Of the 205 contradicted packets, 125 have contradictions recorded only in phenotype items/completeness; 80 have at least one nonphenotype dimension or allele contradiction. This is a classification of the frozen annotations, not a new source adjudication or diagnostic conclusion.

Adverse results are retained. At top5, no-HPO has 300/316 versus 297/316 in the incomplete-paper group, 300/308 versus 297/308 among unresolved selected packets, and 147/153 versus 146/153 among genotype-supported packets. In the fixed 64-pair cohort, no-HPO top1 is 59/64 versus 58/64. Every contrary individual pair is counted even in strata whose net difference favors original HPO.

Review availability and completion are nonrandom. Cases share genes and papers; source phenotypes, source labels and current knowledge may overlap. Top10 may be trivial in the constructed passing-gene universes. These results do not establish clinical accuracy, an effect of review or HPO, knowledge-holdout performance, or biological benefit. No inferential p-values or new reading credits are produced.

The existing source verifier passed with zero errors. The existing independent raw benchmark verifier passed for 2870 files, 1418 raw outputs, 713 cases and 1426 case/arm rows; its report is external and hashed in `validation.json`. It independently recalculates the original and corrected evaluations from retained raw outputs without rerunning inference. The linkage additionally checks exact case/member/hash correspondence, every source item snapshot, both arms, exact PASSED allele evidence, rank ties, complete-case membership, all six baseline results, and every stratum partition. `test-receipt.json` records the failure-injection tests; `validation.json` records linkage checks. `delivery-manifest.json` seals deliverables and the external verification reports.

To repeat local checks without network or inference, from this directory:

```sh
python3 -B -m unittest -v test_analysis
python3 -B analyze.py
```

The input root can be relocated with `--input-root`; keep the external `benchmark-verification.json` beside its `inputs/` directory. `freeze_inputs.py` is provenance for the one-time freeze and refuses to overwrite its destination. No canonical source, nested-repo, aggregate, release or submission file was edited.
