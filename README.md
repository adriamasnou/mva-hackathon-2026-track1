# MVA Hackathon 2026 — evidence, experiment and reusable tools

**adriamasnou · Track 2 · 23 October 2026**

We propose **arimoclomol for conditional preclinical testing** in BUB1B-MVA. The candidate must improve chromosome-segregation function at relevant exposure; more protein alone is insufficient. No drug rescue or treatment in this child has been performed.

## Start here

1. [Track 2 report (PDF)](submissions/adriamasnou_track2_report.pdf) and [editable text](submissions/adriamasnou_track2_report.md) — candidate, evidence, exposure and advancement gates.
2. [Functional rescue plan](submissions/functional-rescue-plan.md) — full-length, abundance-matched controls and explicit failure outcomes.
3. [Gene-to-condition navigator](submissions/pgtm-navigator.html) — download and open locally; no server or query transmission.
4. [Interpretation canary](canary/README.md) — portable code, measured model results and failure-injection checks.
5. [Family-facing summary](submissions/family-facing-summary.md) — research findings and questions for a clinical team.

[Methods workbook](submissions/adriamasnou_methods_description.xlsx) · [Pitch and recording kit](submissions/pitch/README.md) · [Notes for judges](submissions/notes-for-judges.md)

## Run the public checks

```sh
python3 -m unittest discover -s tests -v
python3 canary/run_canary.py --self-test
python3 analysis/exposure_check.py
python3 tools/pgtm/audit.py
python3 tools/check_package.py
```

The canary self-test tests the checker with synthetic fixtures. Actual model inference requires the listed dependencies and an indexed reference; see its README. Missing inputs return a nonzero status, never a pass. The navigator includes all 2,063 rows of a dated HFEA workbook, 35 unmapped rows and source disagreements. A match is not an eligibility or variant-classification decision. [Rebuild instructions](tools/pgtm/README.md).

## Supporting work

- [Track 1 analysis](submissions/adriamasnou_track1_report.md): two candidate BUB1B alleles; phase inferred.
- [Annotation](submissions/annotation-toolchain-vep.md), [splice prediction](submissions/splice-prediction.md), [SV/CNV assessment](submissions/sv-cnv-survey.md) and [callability](submissions/callability-audit.md).
- [Public HG002 spike-in smoke test](submissions/generalisation-public-case.md): scale demonstration, not diagnostic validation.
- [Reagent design](submissions/n1002k-reagent-specification.md), [fragment protocol](submissions/n1002k-collaboration-package.md), [assay pilot](submissions/pilot-protocol-bubr1-flow.md) and [screen design](submissions/screen-protocol-runnable.md): proposed laboratory work, subject to the functional plan's gates.
- [Literature reading record](submissions/literature-reading-record.md): exact review coverage and unresolved supplementary access.
- [Navigator task validation](submissions/pgtm-task-validation.md): eleven source-adjudicated tasks with explicit comparison limits.
- [Register audit](submissions/register-audit.md), [decision-aid draft](submissions/family-facing-decision-aid.md), [cost/access context](submissions/impact-costs-and-access.md) and [secondary-findings governance](submissions/secondary-findings-disclosure-protocol.md).

## Data and reproducibility

This repository contains code, a small number of named variant findings and public-data derivatives. It does not distribute hackathon sequencing data, clinical source documents or genotype-scale derivatives. Patient-data reruns require authorized access and local references. Public-tool checks do not require patient data. The targeted analysis accepts an authorized local VCF:

```sh
python3 analysis/bub1b_targeted_analysis.py /path/to/authorized-input.vcf.gz
```

Historical computational results are distinguished from tests performed for the current package. Proposed laboratory experiments are not represented as completed. Publication and challenge submission are separate steps; this local package does not itself establish either.
