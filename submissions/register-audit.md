# What a public-register crosswalk can—and cannot—measure

**23 October 2026 · historical source snapshots, explicit denominators**

The [navigator](pgtm-navigator.html) links gene symbols to candidate conditions in the HFEA workbook dated 5 August 2026. It provides an auditable route from a gene to a regulator's condition name; it does not determine eligibility or replace variant interpretation.

## Coverage and unresolved mappings

The rebuilt crosswalk contains **2,063 condition rows**, of which **2,028** map to one or more candidate genes and **35** do not. It indexes **1,782 symbols**, with nine ClinVar/HPO disagreement rows retained. The CSV stores per-gene source and OMIM evidence; the provenance manifest records every input hash. **[OUR MEASUREMENT — `tools/pgtm/build.py`]**

**1,692/1,782 (94.9%)** indexed symbols do not occur as literal whole-word matches in their associated workbook condition names. This measures condition-name text, not the live website's full search behaviour. Prior statements that all these genes “cannot be found” overstated the experiment. **[OUR MEASUREMENT]**

## Expert-assertion coverage: a narrow proxy

Using the retained August 29 ClinVar `variant_summary.txt.gz`, define a gene as covered when at least one record has review status “reviewed by expert panel” or “practice guideline”. Deduplicate by gene symbol across assemblies. This produces **220 genes globally** under this rule. **[OUR MEASUREMENT — `tools/pgtm/expert_coverage.py`]**

Among the **2,028 mapped register rows**, **1,850 (91.2%)** have no mapped symbol with such a record. That is **1,850/2,063 (89.7%)** of all workbook rows; the **35 unmapped rows are unassessed**, not counted as lacking expert review. Rebuild instructions and a machine-readable result are supplied alongside the navigator. **[OUR MEASUREMENT]**

The proxy is deliberately limited. An expert-reviewed variant elsewhere in a gene is not expert review of the condition or variant of interest. An absent qualifying record is not proof that no expert has assessed the gene, that a condition lacks a diagnostic route, or that PGT-M is unsafe or unavailable. ClinVar coverage is not a substitute for clinical interpretation, and a gene-specific VCEP is not the only way to classify variants.

## What would establish practical impact

A next evaluation should ask clinicians and families to perform prespecified lookup tasks with and without the navigator, measuring completion, errors, time and understanding of eligibility limits. Include ambiguous, unmapped and alias cases, and ensure the warning does not disappear when a match is found. No such usability or outcomes study has been performed. **[PROPOSED EVALUATION]**

The delivered result is the working, source-traceable lookup and its reproducible coverage analysis. The effect on access to care remains a hypothesis.
