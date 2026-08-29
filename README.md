# MVA Hackathon 2026 — BUB1B compound heterozygote (Tracks 1 and 2)

Analysis code and submission for [Rare Disease, Real Kid: The MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/) (Track 1, variant prediction), by **adriamasnou**.

**Finding:** a candidate compound heterozygote in *BUB1B* — c.2210T>G (**p.Leu737***, ClinVar Pathogenic/Likely pathogenic for MVA1) in assumed trans with c.3006T>G (**p.Asn1002Lys**, kinase-domain missense). Methods, evidence, and limitations: [submissions/adriamasnou_track1_report.md](submissions/adriamasnou_track1_report.md).

## Contents

- `analysis/bub1b_targeted_analysis.py` — reproduces the finding from the provided VCF in one command: extracts the GRCh38 BUB1B locus, filters heterozygous PASS variants absent from dbSNP, and computes protein consequences locally against the Ensembl canonical CDS.
- `submissions/` — the ranked predictions CSV and methods report.

### For families and non-specialists

- **[Decisions you may be asked to make](submissions/family-facing-decision-aid.md)** — a patient
  decision aid built to the **International Patient Decision Aid Standards (IPDAS)**, covering the
  surveillance schedule and reproductive options. It includes a values-clarification exercise, a
  question list for the appointment, the caregiver burden counted in appointments rather than
  pounds, and **a conformance table naming the IPDAS criteria it fails** — it has not been field
  tested and has not been peer reviewed, and says so before it says anything else.
- **[What we found, in plain language](submissions/family-facing-summary.md)** — the findings
  written for a family rather than a specialist, including four things a family can actually ask
  their clinical team about, and an explicit account of what we are unsure about.

### A reusable tool: is your pipeline actually working?

- **[The canary panel](canary/README.md)** — a positive-control set for the *interpretation* layer
  of a rare-disease pipeline. Not a benchmark of accuracy: a test of **liveness**, because
  bioinformatics tools fail *closed* — they return "nothing found" — and in clinical genomics
  "nothing found" is a diagnosis. Six silent failures in one day of work motivated it, including
  one in the code written to catch them. `python3 canary/run_canary.py --self-test` proves the
  panel can go red, on a real bug rather than a synthetic one.

### The one thing here that is an object rather than a document

- **[Build specification: the *BUB1B* N1002K construct](submissions/n1002k-reagent-specification.md)**
  — no reagent carrying this child's actual variant exists anywhere, so every therapeutic claim
  about him, ours and others', is extrapolated from other people's alleles. This is the turnkey
  spec that ends that for a few hundred dollars: the edit verified from the reference sequence,
  designed and Tm-checked mutagenic primers, the destination-vector constraint the depositor warns
  about, a QC plan, and costs. **It cannot be ordered by us — it needs a laboratory.**

- **[The repurposing screen, made runnable](submissions/screen-protocol-runnable.md)** — the
  screen's own audit said 4 of 13 components done and *"we hold zero HTS methods papers"*. This
  closes the seven desk-closable ones against the NIH/NCATS **Assay Guidance Manual**'s criteria
  (Z′ ≥ 0.4, SW ≥ 2, CV ≤ 20%), names a real library, and includes an adversarial review whose
  third attack **changed the protocol**. It does not improve the odds, which remain 25–40% for a
  usable hit and under 10% for anything a child could take.

### Track 2 — beyond this one case

- **[The UK PGT-M register, indexed by gene](submissions/hfea-pgtm-gene-crosswalk.md)** — the
  UK's register of conditions approved for embryo testing has no gene column, so **1,688 of the
  1,778 genes behind approved conditions (94.9%) cannot be found by searching for the gene** —
  cystic fibrosis among them. `hfea-pgtm-gene-crosswalk.csv` and `hfea-pgtm-gene-index.json`
  supply the missing index for all 2,063 conditions; `pipeline/hfea_crosswalk.py` rebuilds them
  from public sources in one command.
- **[Does the pipeline work on a case that is not this child's?](submissions/generalisation-public-case.md)**
  — a phenotype-driven genome-wide scan run end to end on public ClinVar data with a known answer:
  run on a whole real human genome — **GIAB HG002, 4,096,123 variants**, with one pathogenic
  *FGFR2* variant spiked in. **It ranks first of 649 scored genes**, and the discrimination is
  phenotypic rather than ClinVar recognition (§3b.1). No hackathon data involved.
- **[Do either of this child's variants also disrupt splicing?](submissions/splice-prediction.md)**
  — local SpliceAI run as the model, not as lookup. Neither variant shows a splice signal
  (max delta 0.03), which is what the dose argument assumes and could have come out otherwise. The
  positive control caught a patch of ours that had silently broken the model into returning a
  plausible negative for every input.
- **[The answer existed and could not be found](submissions/register-audit.md)** — an audit of the
  infrastructure between a rare-disease diagnosis and what a family is entitled to, measured across
  all 2,063 UK-approved PGT-M conditions rather than one child: **94.9%** of causative genes are
  invisible to the register's own search, **1,068** genes are made indistinguishable by the coding
  European registries use, and **91.4%** of approved conditions have no causative gene with a
  single expert-panel-curated variant.
- **[Tiered disclosure protocol for secondary findings](submissions/secondary-findings-disclosure-protocol.md)**
  — a reusable, condition-agnostic governance template (CC BY 4.0) for any challenge that puts one
  identifiable patient's genome in front of many teams and publishes the results openly, plus an
  adoption checklist and our own application of it including what we have not done.

## Reproduce

```bash
python3 analysis/bub1b_targeted_analysis.py path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz
```

Python 3 stdlib only; `pip install truststore` if your Python does not trust your system's CA store. Only public identifiers (gene symbol, transcript ID) are sent to Ensembl REST — no proband data leaves the machine.

## Data policy

This repository contains **no hackathon data** — no sequencing data, no clinical documents, and no derived datasets. Per the hackathon's Official Rules, the gated dataset may not be redistributed and must be deleted from all environments within 30 days of hackathon close. The prediction rows in `submissions/` are hackathon results, released under CC BY 4.0 like all participant submissions.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
