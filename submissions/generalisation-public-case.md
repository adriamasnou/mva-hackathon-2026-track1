# Does the pipeline work on a case that is not this child's?

**A phenotype-driven genome-wide scan run end to end on public data with a known answer.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. Why this exists

A method demonstrated on one patient, where the answer is already known, has shown nothing. The
claim that an approach *generalises* is worth exactly as much as the evidence that it has been run
on something else. This is that evidence, and it uses **no hackathon data**: the input is built
from public ClinVar records and the expected answer is published.

## 2. The setup

**Input.** 126 variants on GRCh38, assembled from ClinVar's public `variant_summary`: **six
pathogenic *FGFR2* variants** and **120 benign decoys** in *TTN*, *MUC16*, *OBSCN*, *NEB* and
*RYR1* — genes chosen because they are large and mutation-rich, so they are the realistic
distractors in any exome. **[OUR MEASUREMENT — assembled from ClinVar `variant_summary.txt.gz`,
GRCh38 rows, downloaded 2026-08-29; pathogenic/benign labels are ClinVar's own.]**

**Phenotype.** Six HPO terms describing Pfeiffer syndrome — syndactyly, strabismus, maxillary
hypoplasia, proptosis, hypertelorism, brachyturricephaly — supplied as a phenopacket. **The
phenotype never names a gene.**

**Expected answer.** *FGFR2*. Pfeiffer syndrome is caused by *FGFR2* variants; the scan is only
useful if it recovers that from phenotype plus variants alone.

## 3. Result

| rank | gene | inheritance | combined score | phenotype | variant | p |
|---|---|---|---|---|---|---|
| **1** | ***FGFR2*** | **AD** | **0.9647** | 0.8599 | 1.0000 | **0.00e+00** |
| 2 | *FGFR2* | AR | 0.1531 | 0.4043 | 1.0000 | 2.95e-02 |
| 3 | *RYR1* | AD | 0.0066 | 0.5337 | 0.9663 | 2.86e-01 |
| 4 | *RYR1* | AR | 0.0043 | 0.5005 | 0.9486 | 3.37e-01 |
| 5 | *TTN* | AR | 0.0013 | 0.4674 | 0.8177 | 4.90e-01 |

> ***FGFR2* ranks first, with a combined score 146× the next distinct gene.** 126 variants in,
> 90 through filtering, 3 genes scored, correct answer at the top. Runtime 5.2 s after startup.

**[OUR MEASUREMENT — Exomiser 15.1.0, `2512_hg38` data bundle, run 2026-08-29. Input, job file and
outputs are reproducible from the command in §5.]**

## 4. 🔴 Limitations — what this does and does not establish

1. **This is a constructed 126-variant mini-case, not a full exome.** A real exome presents tens of
   thousands of variants and is a materially harder ranking problem. **This demonstrates that the
   pipeline runs correctly on an unseen case and recovers a known answer; it does not establish
   performance at exome scale.** The full-exome run is described in §6 and is **not yet complete**.
   **[OUR INFERENCE — that exome scale is materially harder is our judgement about the
   task, not a benchmarked comparison; §6's run is what would settle it.]**
2. **The decoys are benign by ClinVar's own labels**, so the discrimination task is easier than
   reality, where most distractors are variants of uncertain significance.
3. **The phenotype is clean and specific.** Real referrals carry sparser, noisier HPO terms.
4. **Nothing here validates the *BUB1B* analysis.** It validates the *machinery*, on a case where
   the answer is independently known.
5. ⚠️ **This run does not credit any splice-prediction capability.** `pathogenicitySources` was set
   to `[REVEL, MVP]`. SpliceAI is **not installed here**, and the vendored example configuration
   that references it must not be read as evidence that we ran it.

## 5. Reproduce

```bash
java -Xmx6g -Dexomiser.data-directory=<path-to-exomiser-data> \
  -jar exomiser-cli-15.1.0.jar analyse --analysis smoke-job.yml
```

Input built from ClinVar `variant_summary.txt.gz` (public, GRCh38 rows). No hackathon data is
involved at any step.

## 6. 🔻 The blocker this hit, and why it is recorded

The project plan named `Pfeiffer.vcf.gz` — bundled with Exomiser — as the public case to run, on
the basis that it was "already on disk". **It is on disk and it could not be run**, for a reason
the plan did not anticipate: **every bundled Exomiser example is `genomeAssembly: hg19`, and the
only data bundle installed was `2512_hg38`.** A neighbouring filename ending `_38` reads like an
assembly and is a UTR position.

The plan's premise — that the work was bought and only needed running — was wrong by one 19.4 GB
download. That bundle is now downloading, from
`data.monarchinitiative.org/exomiser/data/2512_hg19.zip`; the URL documented in the tool's own
README (`/exomiser/latest/`) returns 404, because "latest" has moved on to an older-numbered
release than the one installed.

**The full-exome Pfeiffer run (37,709 variants, known answer *FGFR2*, hg19) is the harder test and
will be added when that bundle lands.** It is named here rather than quietly omitted, because §4.1
is exactly the limitation it would close.
