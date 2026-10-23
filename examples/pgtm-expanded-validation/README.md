# Expanded PGT-M source evaluation

This bounded evaluation adds 28 purposively selected queries, with all associations on every returned row reviewed against original retained source records. It is a same-developer, shared-source conformance audit, not an independent clinical accuracy benchmark. See the [report](../../submissions/pgtm-expanded-validation.md) and [complete result](../../submissions/pgtm-expanded-validation.json).

The selection includes 22 gene queries and six edges. `selection-plan.json` and `selection-freeze.json` predate source adjudication. `expected.json` specifies complete row sets, gene sets, original source links/roles and review notes; `expected-freeze.json` predates navigator execution. Local hash receipts are not external preregistration. The developer had already read the implementation and prior 11-task audit. The prior record is not overwritten.

`source-excerpts.json` contains selected original HFEA cells and all mapping lines for the selected identifiers. The 45 primary workbook rows and 141 primary mapping records were read before execution; two further workbook rows and 11 context mapping records explain no-match cases. Expected row/gene sets were manually specified; coordinates and source roles were transcribed from the reviewed original records. No builder output generated expected answers. Every returned row, including additional matches beyond the original eleven tasks, is adjudicated.

## Reproduce without downloads

Supply the exact retained originals identified by the evidence hashes. Newer files require a new selection/adjudication, not changing a hash to force a pass. Python 3.9+ and Node.js are required; the recorded test runtime was Python 3.12.14. No third-party packages or network are used.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examples/pgtm-expanded-validation/evaluate.py \
  --hfea /path/to/hfea_pgtm_2026-08-05.xlsx \
  --source-dir /path/to/crosswalk-sources \
  --node /path/to/node

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s examples/pgtm-expanded-validation -p test_evaluation.py -v
```

The evaluator checks all freeze hashes, verifies whole originals and complete selected/context excerpts, then executes `tools/pgtm/audit_query.cjs` against the shipped HTML. The production builder is never imported or executed. Standard output is the new JSON result. Exit 0 means all frozen source-conformance expectations matched; **it does not mean clinical validity or absence of semantic defects**. Exit 1 means expectation mismatch; exit 2 means verification/runtime failure. The tests use the retained query output to exercise failure handling, so the shipped result must be present. The separately recorded `test-results.json` is also included in the retained submission JSON; a fresh evaluator invocation does not itself run tests or attach a new test receipt.

`collect_sources.py` is an original-source extraction aid, not an expected-answer generator or clinical oracle. It can reproduce excerpts to standard output for comparison. It includes the frozen pre-query source follow-up for GBA/ATP7B, and assumes this pinned workbook layout. All facts and generated summaries remain bounded by the exact source versions.

## Counts and interpretation

The 28 tasks contain 40 query–row instances, 35 distinct returned rows and 47 distinct returned row–gene pairs. Twenty positive gene queries retrieve all 35 expected gene-query row instances; two gene queries intentionally have no-match expectations. Literal condition-title matching finds at least one expected row in 5/20 positive gene queries. Source-link counts and candidate counts are different denominators.

Six returned rows have multiple candidate genes and one has a ClinVar/HPO disagreement; those warnings are present. The original audit found eleven row–gene associations across eight rows missing a `POLYGENIC` or `RelatedGenes` qualifier. These represented ten distinct gene–MIM qualifier facts because BRCA2/612555 occurs twice. The repair now preserves every reviewed role in both per-gene data and visible labels; the unchanged frozen queries pass the strengthened evaluation. The original result, report and hashes are retained in `pre-fix/`. A source label is not a clinical verdict or eligibility validation.

No source-unsupported links were found, but independent clinical truth was not available for the complete set. Candidate labels and the condition-level eligibility limitation remain visible; actual comprehension or decisions were not studied. Eighteen local headless Chromium layout checks passed at desktop and two mobile viewport widths, with desktop and 390-pixel captures visually reviewed. This does not establish cross-browser behaviour or user comprehension. There is no user-outcome, time-saving, usability, live-register or independent clinical-accuracy claim.

## Source sharing and terms

The audit and builder use the same HFEA, ClinVar, HPO and OMIM snapshots; ClinVar and HPO may share upstream records. Implementation-independent transcription does not create independent biological truth. Only selected excerpts are bundled. Respect source-specific terms when using or redistributing them; the OMIM file states Johns Hopkins University copyright and the [OMIM agreement](https://omim.org/help/agreement). Its gene table is not a phenotype-to-gene table. Full source files, patient data and a live external service are not part of this example.
