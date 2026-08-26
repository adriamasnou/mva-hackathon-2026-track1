# MVA Hackathon 2026 — Track 1: BUB1B compound heterozygote

Analysis code and submission for [Rare Disease, Real Kid: The MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/) (Track 1, variant prediction), by **adriamasnou**.

**Finding:** a candidate compound heterozygote in *BUB1B* — c.2210T>G (**p.Leu737***, ClinVar Pathogenic/Likely pathogenic for MVA1) in assumed trans with c.3006T>G (**p.Asn1002Lys**, kinase-domain missense). Methods, evidence, and limitations: [submissions/adriamasnou_track1_report.md](submissions/adriamasnou_track1_report.md).

## Contents

- `analysis/bub1b_targeted_analysis.py` — reproduces the finding from the provided VCF in one command: extracts the GRCh38 BUB1B locus, filters heterozygous PASS variants absent from dbSNP, and computes protein consequences locally against the Ensembl canonical CDS.
- `submissions/` — the ranked predictions CSV and methods report.

## Reproduce

```bash
python3 analysis/bub1b_targeted_analysis.py path/to/WGS_EX2312012_HGWCNDSX7.vcf.gz
```

Python 3 stdlib only; `pip install truststore` if your Python does not trust your system's CA store. Only public identifiers (gene symbol, transcript ID) are sent to Ensembl REST — no proband data leaves the machine.

## Data policy

This repository contains **no hackathon data** — no sequencing data, no clinical documents, and no derived datasets. Per the hackathon's Official Rules, the gated dataset may not be redistributed and must be deleted from all environments within 30 days of hackathon close. The prediction rows in `submissions/` are hackathon results, released under CC BY 4.0 like all participant submissions.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
