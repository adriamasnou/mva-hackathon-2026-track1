# MVA Hackathon 2026 — evidence, experiment and reusable tools

**adriamasnou · Track 2 · 24 October 2026**

We propose **arimoclomol for conditional preclinical testing** in BUB1B-MVA. The candidate must improve chromosome-segregation function at relevant exposure; more protein alone is insufficient. No drug rescue or treatment in this child has been performed.

## Start here

1. [Track 2 report (PDF)](submissions/adriamasnou_track2_report.pdf) and [editable text](submissions/adriamasnou_track2_report.md) — candidate, evidence, exposure and advancement gates.
2. [Functional rescue plan](submissions/functional-rescue-plan.md) — full-length, abundance-matched controls and explicit failure outcomes.
3. [Gene-to-condition navigator](submissions/pgtm-navigator.html) — download and open locally; no server or query transmission.
4. [Interpretation canary](canary/README.md) — portable code, measured model results and failure-injection checks.
5. [Family-facing summary](submissions/family-facing-summary.md) — research findings and questions for a clinical team.

[Methods workbook](submissions/adriamasnou_methods_description.xlsx) · [Pitch and recording kit](submissions/pitch/README.md) · [Notes for judges](submissions/notes-for-judges.md)

[Reviewer walkthrough](submissions/reviewer-walkthrough.md): inspect a gene-to-condition source link, an unresolved identifier and three executable synthetic rescue-decision examples.

## Run the public checks

Use Python 3.11 or newer. The navigator audit also needs Node.js. The tests below use public fixtures and do not run the large annotation models.

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
- [Completed public multi-case evaluation](submissions/public-validation.md): 96 genomic jobs and 12 phenotype-only jobs. Original-HPO top-1/5/10 recovery is 6/7/8 on HG002 and 7/8/8 on HG001, each of the same nine primary source labels; phenotype-only gives 4/8/8 with a different candidate universe. Five labels have material source qualifications. [Paired results](examples/public-benchmark/results/paired-summary.json), [genomic exports](examples/public-benchmark/results/) and [phenotype-only export](examples/public-benchmark/results/phenotype-only/) support offline checks. This is semi-synthetic source-label recovery, not clinical accuracy or drug validation.
- [Compact public companion](submissions/compact-public-validation.md): all 1,418 jobs completed for 713 constructed source signatures. Primary top-1 is 556/681 with original HPO versus 430/681 without HPO; raw outputs, both parser versions and independent offline verification are retained. The [post-inference review snapshot](examples/compact-source-audit/README.md) adds 137 full-main-text reads, 62 complete paper reviews and 708 adjudicated packet mappings. Incomplete source review, small candidate sets and current knowledge limit interpretation; this is not clinical accuracy or demonstrated competitor superiority. **[OUR MEASUREMENT; OUR INFERENCE about scope]**
- [Reagent design](submissions/n1002k-reagent-specification.md), [fragment protocol](submissions/n1002k-collaboration-package.md), [assay pilot](submissions/pilot-protocol-bubr1-flow.md) and [screen design](submissions/screen-protocol-runnable.md): proposed laboratory work, subject to the functional plan's gates.
- [Laboratory execution readiness](submissions/laboratory-execution-readiness.md): staged full-length function/rescue study, sequence and quantity checks, public supplier prices, unresolved full costs and detailed quotation requests. Provider acceptance, project quotations and experimental results remain unresolved.
- [Literature reading record](submissions/literature-reading-record.md): exact review coverage and unresolved supplementary access.
- [Claude Science continuation plan](submissions/claude-science-continuation.md): conditional, milestone-based use of $12,000 in credits, with a separate laboratory funding dependency.
- [Expanded navigator evaluation](submissions/pgtm-expanded-validation.md): 28 frozen queries, all 47 returned row–gene pairs reviewed, source-role repair and 18 local browser checks. The earlier [11-task audit](submissions/pgtm-task-validation.md) is retained.
- [Rescue-decision prototype](submissions/rescue-decision-validation.md): 40 frozen synthetic cases exercise functional, exposure and fate criteria. This tests software decisions, not drug rescue.
- [Register audit](submissions/register-audit.md), [decision-aid draft](submissions/family-facing-decision-aid.md), [cost/access context](submissions/impact-costs-and-access.md) and [secondary-findings governance](submissions/secondary-findings-disclosure-protocol.md).

## Data and reproducibility

This repository contains code, a small number of named variant findings and public-data derivatives. It does not distribute hackathon sequencing data, clinical source documents or genotype-scale derivatives. Patient-data reruns require authorized access and local references. Public-tool checks do not require patient data. The targeted analysis accepts an authorized local VCF:

```sh
python3 analysis/bub1b_targeted_analysis.py /path/to/authorized-input.vcf.gz
```

Historical computational results are distinguished from tests performed for the current package. Proposed laboratory experiments are not represented as completed. Publication and challenge submission are separate steps; this local package does not itself establish either.
