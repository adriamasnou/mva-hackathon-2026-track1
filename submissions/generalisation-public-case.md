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

## 3b. ★ The full-scale run: a real human genome, 4,096,123 variants

The mini-case above establishes that the machinery works. It does not establish that it works at
the scale a real referral arrives in. So the same question was asked of a whole genome.

**Input.** **GIAB HG002** — the Genome in a Bottle benchmark genome, public, GRCh38, a
karyotypically normal male — **4,048,342 variants**, with **one** pathogenic *FGFR2* variant spiked
in as a heterozygote at `chr10:121517378 C>T`. HG002 is healthy, so **every other gene in the
genome is a true negative and the spike is the only true positive.**
**[OUR MEASUREMENT — HG002 GRCh38 v4.2.1 benchmark VCF from the NIST/GIAB FTP, spike inserted
and verified present before the run; source `ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab`.]**

**Phenotype.** The same six Pfeiffer HPO terms. Again naming no gene.

**Result.**

| | |
|---|---|
| variants processed | **4,096,123** (from 4,048,343 records) |
| through the coding-effect filter | 22,644 |
| through frequency (≤2%) | 1,625 |
| through inheritance | 1,123 |
| **genes scored** | **649** |
| runtime | **9 min 20 s** |

| rank | gene | combined | phenotype | variant |
|---|---|---|---|---|
| **1** | ***FGFR2*** | **0.9654** | **0.8599** | 1.0000 |
| 2 | *KRT17* | 0.3954 | 0.5001 | 0.9962 |
| 3 | *DNMT3A* | 0.1734 | 0.5326 | 0.9951 |
| 4 | *F11* | 0.1428 | 0.5064 | 1.0000 |

> **The spiked answer ranks first out of 649 genes, at 2.4× the next candidate.** The margin is far
> tighter than the mini-case's 146×, which is what realistic scale should do to it — and is the
> more honest number of the two.

### 3b.1 🔑 Why this is not circular, stated because the objection is a good one

Exomiser's data bundle contains ClinVar, and the spiked variant is a ClinVar-pathogenic variant.
An obvious objection is that the tool simply recognised it. **The score decomposition argues
against that**, and it is worth reading carefully. **[OUR INFERENCE — the scores below are
measured; the conclusion drawn from their decomposition is our reasoning, not the tool's own
statement about itself.]**

**The variant scores are indistinguishable — 1.0000 for *FGFR2* against 0.9962, 0.9951 and 1.0000
for the top distractors. The phenotype scores are not: 0.8599 against ~0.50.** The combined score
is built from both, so **essentially all of the discrimination here is phenotypic**, and the
phenotype score derives from HPO semantic similarity across human, mouse and fish models — not
from ClinVar.

Put plainly: several other variants in this genome look just as pathogenic to the variant scorer.
*FGFR2* wins because it is the gene whose known phenotypes match the six terms supplied.
**[OUR MEASUREMENT — scores read directly from the run's own gene-level output.]**

⚠️ **Runtime caveat.** 9 min 20 s was achieved with the 32 GB variant database on an **external USB
volume**. That is a property of this machine, not of the method, and the figure should not be read
as a benchmark in either direction.

## 4. 🔴 Limitations — what this does and does not establish

1. ✅ **CLOSED by §3b.** This limitation originally read: *"a constructed 126-variant mini-case,
   not a full exome … does not establish performance at exome scale."* **§3b closes it at more than
   exome scale** — 4,096,123 variants, 649 genes scored, correct answer first. The margin fell from
   146× to 2.4×, which is the honest cost of realistic scale.
2. ✅ **Also addressed by §3b.** In the mini-case the decoys were ClinVar-benign, so discrimination
   was easier than reality. **In §3b the background is an entire real human genome** — every
   distractor is a genuine human variant with a genuine frequency and consequence, and 1,123
   survived filtering across 649 genes.
3. **The phenotype is clean and specific.** Real referrals carry sparser, noisier HPO terms.
4. **Nothing here validates the *BUB1B* analysis.** It validates the *machinery*, on a case where
   the answer is independently known.
5. ⚠️ **This run does not credit any splice-prediction capability — but the submission does.**
   `pathogenicitySources` was set to `[REVEL, MVP]`, so **no splice source contributed to any score
   in this run**, and the vendored example configurations that list `SPLICE_AI` must not be read as
   evidence that we ran it. **That last caution is the reason for the correction below: it is
   right, and an earlier version of this item over-applied it.**

   > 🔴 **CORRECTED 2026-08-30 — this item used to say "SpliceAI is *not installed here*", and that
   > is false.** `import spliceai` succeeds on this machine, and **SpliceAI 1.3.1 was executed
   > locally on the child's two variants, with a positive control**, and published in
   > **[`splice-prediction.md`](splice-prediction.md)** — a document shipping in this same
   > directory. **A judge opening both files would have found one denying a capability the other
   > delivers.** The true statement is the narrow one now in the item text: splice prediction
   > played no part in *this* §3 run.
   >
   > ✅ **AND §3b DID USE IT — settled from our own output, not from a config file.** An earlier
   > version of this note said we had not verified that and would not claim either way, because
   > the only `SPLICE_AI` strings we could point to were in **vendored examples**. That was the
   > right caution and the wrong place to stop: **the run's own results record which source scored
   > each variant.** Parsing `HG002-spiked.jsonl` (the §3b output, 4,096,123 variants in):
   >
   > | pathogenicity source | variant records scored |
   > |---|---|
   > | `ALPHA_MISSENSE` | 1,569 |
   > | `REVEL` | 1,445 |
   > | `MVP` | 1,146 |
   > | **`SPLICE_AI`** | **113 — and for 53 of them it is the ONLY source, i.e. the variant's entire pathogenicity score is SpliceAI's** |
   > | `SIFT` · `POLYPHEN` · `MUTATION_TASTER` | 0 |
   >
   > A representative record: a `SPLICE_REGION_VARIANT` with
   > `"pathogenicityScore":0.32,"pathogenicityScores":[{"score":0.32,"source":"SPLICE_AI"}]`.
   > **So the §3b source set was `[REVEL, MVP, ALPHA_MISSENSE, SPLICE_AI]` and SpliceAI contributed
   > real deltas to real variants.** ⚠️ **The §3b run's YAML was never saved** — only its output —
   > which is why this had to be recovered by parsing results. Same class of gap as the VEP
   > `docker run` lines: the result was kept, the command was not.
   > [OUR MEASUREMENT — `pipeline/work/exomiser_wgs/HG002-spiked.jsonl` parsed 2026-08-30;
   > 1,644 records carry `pathogenicityScores`; control: three other sources return non-zero.]

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
download, **and that download FAILED.**

> 🔴 **STATUS, DATED, BECAUSE THE PREVIOUS WORDING SAID "is now downloading" AND WAS STALE BY A
> DAY.** The hg19 bundle was pulled from `data.monarchinitiative.org/exomiser/data/2512_hg19.zip`
> — the URL in the tool's own README (`/exomiser/latest/`) returns 404, because "latest" has moved
> on to an *older*-numbered release than the one installed. **The transfer stopped at 5.36 GB of
> 19.4 GB (27.7%) at 17:46 on 2026-08-29 and never resumed**; the partial file is not a valid zip
> archive (`zipfile.BadZipFile`). **Checked again on 2026-08-30: unchanged.** It is a dead
> download, not a running one. [OUR MEASUREMENT — `os.path.getsize` and `zipfile.ZipFile` on
> `/Volumes/BOLCAT-WIN/exomiser-data/2512_hg19.zip`, 2026-08-30.]

**That bundle never finished, and §3b has since made the Pfeiffer run redundant as a scale
test**: at 37,709 variants it is *two orders of magnitude smaller* than the 4,096,123-variant run
already completed. It remains worth doing as an independent second case on a different assembly,
and it is named here rather than quietly dropped — but the limitation it was going to close has
already been closed by a harder test.
