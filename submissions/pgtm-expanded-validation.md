# PGT-M navigator: expanded source and ambiguity evaluation

**The source-qualifier defect is repaired. The unchanged 28 frozen queries pass after the repair, with all 47 returned row–gene pairs reviewed. The 11 pre-fix `POLYGENIC`/`RelatedGenes` omissions across eight rows are now zero in both the per-gene payload and text outside collapsed details.** This is a same-developer, shared-source conformance result, not independent clinical accuracy or a measure of user benefit.

The [exact pre-fix result](../examples/pgtm-expanded-validation/pre-fix/pgtm-expanded-validation.json), [pre-fix report](../examples/pgtm-expanded-validation/pre-fix/pgtm-expanded-validation.txt), builder/template and SHA-256 manifest remain retained. The [current JSON result](pgtm-expanded-validation.json) explicitly records both summaries, the original 11 omissions, every query/card, exact source-role comparisons, hashes and the targeted test receipt. Frozen selection, source excerpts and expected answers are unchanged. The prior [11-task record](pgtm-task-validation.md) is also unchanged; its existing audit passes against the repaired navigator.

Before repair, 28/28 queries passed retrieval and gene/source/MIM-link checks while qualifier loss was reported separately. After repair, 28/28 also pass the added exact source-field/type checks and require each source label outside collapsed details. These are different levels of assertion, not an increase in clinical accuracy. There are zero source-role metadata mismatches and zero missing visible source labels among the 35 returned rows. All 41 targeted tests pass (22 navigator tests, including the existing 11-task audit, and 19 expanded-evaluation tests).

The builder now retains the original HPO `association_type` and source field per gene/MIM. The actual ClinVar mapping columns are `AssociatedGenes` and `RelatedGenes`, **not `GeneSymbol`**; neither supplies a separate association-type value, so the raw payload records null. Visible descriptions distinguish “ClinVar: associated gene” from “ClinVar: related gene” without repeating an absent type. HPO's symbol field is `gene_symbol`. OMIM gene identifiers retain `entry_type: gene` and visibly say they are not phenotype evidence. Distinct roles/fields for the same gene are preserved, without choosing one as clinical truth. Exact duplicate records are deduplicated.

Each card now says **“Condition status: approved”**, with no gene-level approval badge. Each gene has a separate heading and a short list of source descriptions with the relevant OMIM identifier. Visible wording includes “ClinVar: associated gene,” “ClinVar: related gene,” “HPO: Mendelian association,” “HPO: polygenic association” and “OMIM: gene identifier only.” Unknown HPO types remain literal and marked as unrecognized; blank types say they were not supplied. Exact raw fields and types remain in expandable JSON. The descriptions are explicitly distinguished from clinical classifications or gene-level approvals. A missing or renamed HPO `association_type` header now stops the build instead of silently discarding it.

## Selection frozen before execution

The 28-query selection was frozen at **21:41:07 UTC on 23 October 2026**. After source review, explicit expected row sets and complete gene sets were frozen at **21:46:43 UTC**. The first selected navigator execution began at **21:49:05 UTC**. Both freezes have local SHA-256 receipts; neither is a trusted external timestamp or independent preregistration.

The purposive strata contain 22 gene queries and six edge cases:

- MVA: BUB1B, CEP57, TRIP13.
- Classical disorders and inheritance diversity: CFTR, DMD, FMR1, HBB, HBA1, SMN1.
- Cancer predisposition, gene identifiers and multiple identifiers: BRCA1, BRCA2, CHEK2, TP53.
- Metabolic disease and symbol handling: PAH, GAA, GBA, ATP7B.
- Pleiotropic/neurodevelopmental conditions: NF1, TSC2, SCN1A.
- Explicit source-role ambiguity: TGFB1, QDPR.
- Edges: BUBR1 alias, CHIME malformed identifier, SIX2 missing identifier, `28000`, whitespace/lowercase `cftr`, and a synthetic unmatched token.

Selection was not random or blinded. The same AI developer had read the previous evaluation and implementation. No queries were removed or substituted after selection. Expected answers came from the original source cells and records, not builder outputs or navigator results. The review read **45 primary workbook rows and all 141 mapping records for their 42 identifiers**, including condition-title-only candidates that exact gene matching should exclude. It also read two context workbook rows and all 11 context mapping records explaining the GBA/ATP7B cases. All expected source sets were frozen before the actual JavaScript queries; no post-query additions were needed.

## Retrieval and complete association review

Twenty of the 22 gene queries had source-derived positive expectations; the other two had explicit no-match expectations. All 20 positive queries retrieved all expected rows. Literal case-insensitive substring search of those condition titles found at least one expected row for **5/20 queries**, and **5/35 expected query–row instances**. These are different denominators. The navigator retrieved all 35 positive gene query–row instances.

This comparison demonstrates functionality on selected source-defined tasks. It is not a comparison with the live HFEA search service, an independently assessed clinical reference standard, or a population performance estimate. Literal substring search can also find unrelated text fragments, such as DMD inside other abbreviations; those text-only candidate rows were reviewed separately and were not promoted into source-gene associations.

Across all 28 queries, there were 40 query–row instances but only 35 distinct returned rows. All **47 distinct returned row–gene associations**, including genes other than the query, have original source locators and review notes. The six multiple-candidate rows are cystic fibrosis, hereditary pancreatitis, phenylketonuria, SMA type III, tuberous sclerosis 2 and Wilms tumour 1. All six displayed the multiple-candidate warning. Phenylketonuria displayed the expected ClinVar/HPO disagreement warning. No returned row remained unreviewed.

## Ambiguity and unsupported promotion

The following **pre-fix** omitted source distinctions remain fully enumerated in the retained evidence and current before/after JSON; all are now preserved and displayed:

- Cystic fibrosis, HFEA row 503: HPO marks **FCGR2A and TGFB1 `POLYGENIC`**, while CFTR is `MENDELIAN` (HPO lines 872–874).
- Hereditary pancreatitis, row 1648: **PRSS2, CFTR and CTRC are `POLYGENIC`**, while PRSS1 and SPINK1 are `MENDELIAN` (lines 281–285).
- SMA III, row 1900: **SMN2 is `POLYGENIC`**, while SMN1 is `MENDELIAN` (lines 3677–3678).
- Breast-ovarian susceptibility, rows 177, 178 and 182: HPO labels **BRCA1 or BRCA2 `POLYGENIC`** (lines 1231 and 5940). This source label is not a clinical reclassification or a reason to dismiss these genes.
- Phenylketonuria, row 1675: **QDPR occurs in ClinVar `RelatedGenes`**, not HPO's gene set for this MIM (ClinVar line 12260). The separate QDPR condition at row 975 was also reviewed.
- Tuberous sclerosis 2, row 2012: **IFNG is `POLYGENIC`**, while TSC2 is `MENDELIAN` (HPO lines 5066–5067).

These were **11 row–gene omissions**, representing ten distinct gene–MIM qualifier facts: the BRCA2/612555 fact appears on two register rows. Repair restores these source distinctions; matching gene sets across sources still do not establish matching clinical roles. **[OUR MEASUREMENT — source-row audit above and linked JSON]**

No source-unsupported gene/source/MIM links were found. The reviewed template and card text retain “Candidate gene(s)” and explicitly state that condition approval does not establish variant suitability or family eligibility. No explicit assertion that every displayed gene, variant or family is approved was identified. However, even with qualifiers restored and condition status explicitly labelled, candidate lists can still be overinterpreted. This evaluation did not measure comprehension or decisions. It **cannot classify all candidates as clinically true or false**.

The scoped repair changes the builder, template and generated navigator without adding or deleting any candidate-gene associations. All 2,063 rows have identical non-evidence columns before/after, and the generated gene index is byte-identical. The nine whole-snapshot ClinVar/HPO gene-set disagreements remain; one appears in this selected evaluation. Gene-set agreement is not role agreement. The clinical meaning of `POLYGENIC`, `RelatedGenes` and the six-gene Wilms tumour row remains unadjudicated beyond the original snapshot records.

## No-match and identifier limits

`GBA` has no exact association or title match in the held snapshots. The context review found `GBA1` on the Gaucher II/III rows 853–854. General alias inference is not implemented, and equivalence was not independently adjudicated here. `ATP7B` has records for Wilson disease MIM 277900 and gene MIM 606882, but neither identifier appears in the held HFEA workbook. Neither no-match result establishes ineligibility or the live register's current contents.

CHIME's five-digit identifier remains flagged and unmapped; SIX2's blank identifier remains unmapped despite successful text retrieval. HBB also retrieves a row whose original XML cell C886 stores `141900.00380000001` in General format. The navigator flags malformed fragments and maps the six-digit prefix. This is stored numeric text, not a verified displayed allele identifier. The existing flag does not establish variant-specific eligibility.

## Sources, tests and hard limits

The exact [5 August HFEA workbook](https://www.hfea.gov.uk/media/ssapbtyc/2026-08-05-pgt-m-full-approved-condition-list.xlsx), [ClinVar mapping](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id), [HPO association file](https://purl.obolibrary.org/obo/hp/hpoa/genes_to_disease.txt) and [OMIM gene-identifier file](https://omim.org/static/omim/data/mim2gene.txt) were verified against retained whole-file hashes before querying. Mapping snapshots were retained on 29 August; file dates do not establish current clinical knowledge. Selected excerpts and locators are retained, not full source redistributions. Source-specific terms, including [OMIM's agreement](https://omim.org/help/agreement), still apply.

The 22 navigator tests include ten role/presentation tests and the existing parser and 11-task audit tests. They check original field names, multiple roles on one gene, blank/unknown HPO labels, fail-closed header handling, gene identifiers, per-gene visible labels and condition-only status. The 19 expanded-evaluation tests retain the pre-fix loss finding and reject swapped gene roles in both raw metadata and visible gene groups, `RelatedGenes` promoted to `AssociatedGenes`, qualifiers present only in collapsed JSON, unqualified status, incomplete expected/output sets, unsupported source links, missing ambiguity warnings, bad source verification and missing runtime. The actual shipped JavaScript was executed through the minimal DOM adapter, extended to capture text and per-gene group structure outside `<details>`. Tests reject a correct role label displayed under the wrong gene, retain the complete raw JSON, and check unknown/blank HPO labels.

Actual local headless Chrome rendering also passed **18 checks**: CFTR, QDPR, BRCA1, BRCA2, CHEK2 and HBB at **1440×1000, 390×844 and 320×740**. This includes a six-gene card. Checks covered DOM source-role groups against the frozen-source evaluation, visible role text with raw JSON collapsed, unchanged raw evidence, condition-level status, JSON expansion, and absence of clipped text or horizontal overflow. No page JavaScript errors or attempted page HTTP requests were observed. Desktop and 390-pixel CFTR renderings were visually inspected; final presentation capture remains separate. The [browser receipt](../examples/pgtm-expanded-validation/browser-check-results.json) pins the navigator and check-script hashes. This is one local browser engine with resized viewports, not physical-device, cross-browser, accessibility or user-comprehension validation.

**Independent clinical truth for the complete expanded set is unavailable.** Builder and audit share source snapshots; ClinVar and HPO may share upstream evidence; selection, adjudication and evaluation share a developer. Database agreement, an HPO category or an OMIM gene entry does not independently establish causality, variant validity or PGT-M eligibility. No user outcomes, time savings, clinical accuracy, live-register completeness or competitive superiority are claimed.

## Scoped changed paths and reproduction

Product files: `tools/pgtm/build.py`, `tools/pgtm/template.html`, `tools/pgtm/audit_query.cjs`; generated `submissions/hfea-pgtm-gene-crosswalk.csv`, `submissions/hfea-pgtm-provenance.json` and `submissions/pgtm-navigator.html`. The gene index was regenerated but is byte-identical. `submissions/expert-coverage.json` has only its crosswalk hash/mtime refreshed: every input column used by its coverage calculation was verified identical across all rows, so its estimates are unchanged; this was not a new bulk analysis. The [rebuild receipt](../examples/pgtm-expanded-validation/rebuild-checks.json) records that check.

Tests: `tests/test_pgtm.py` and `tests/test_pgtm_audit.py` only update HPO fixtures for the required original role column; new `tests/test_pgtm_roles.py` contains the role/presentation regressions. Evaluation changes are confined to this Markdown/JSON pair and `examples/pgtm-expanded-validation/` (evaluator, targeted tests, local browser check, receipts and pre-fix archive). No shared gates, commits, README/main-report edits or external actions were performed by this repair.

From the submission repo, with Python 3 and Node available:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_pgtm*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/pgtm-expanded-validation -p test_evaluation.py -v
PYTHONDONTWRITEBYTECODE=1 python3 examples/pgtm-expanded-validation/evaluate.py --hfea ../data/derived/hfea_pgtm_2026-08-05.xlsx --source-dir ../data/derived/crosswalk-sources --node node
```

The last command prints a fresh result without overwriting the retained result. For browser verification, run `node examples/pgtm-expanded-validation/browser-check.cjs` with Playwright and its Chromium available, or supply local installation paths through `PGTM_PLAYWRIGHT_PATH` and `PGTM_CHROMIUM_PATH`. No dependency download is performed by that script. Original source files are required for whole-file verification. The pre-fix evaluator/tests are retained as historical evidence, not a second live test suite. The expanded directory README and this report describe the current repair; the exact original report remains archived as plain text with unchanged bytes and its original hash.
