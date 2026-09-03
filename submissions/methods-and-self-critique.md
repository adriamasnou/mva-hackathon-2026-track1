# The phenotype-blind scan, and everything we tried to break

**Two things a submission is not obliged to include: an analysis that did not go our way, and a
record of our own claims failing.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. The phenotype-blind scan — a pre-declared failure condition, reported as one

The obvious attack on our finding is that **we found what we went looking for.** *BUB1B* was
reached with a candidate-gene prior; a prior that strong can manufacture its own confirmation.

So the analysis was re-run knowing nothing: **no gene list, no HPO terms, no panel** — against a
filter pre-registered *before* the run in `pipeline/recessive_scan_PREREGISTERED.md`.

| | |
|---|---|
| variants entering the consequence step | 313,417 |
| damaging coding consequences | 1,015 |
| genes with any damaging call | 467 |
| genes meeting the recessive model | 230 |
| ***BUB1B* rank** | **55 of 230 — but see the tie disclosure below** |

🔴 **`rank 55` is not a measurement, and we would rather say so than have it found.** Nine genes
are tied with *BUB1B* on both severity sort keys, occupying ranks **53–61**; within that block
**seven — VPS41, IGHV8-51-1, *BUB1B*, TUBB8B, PSG1, LILRB4, LBP — are tied on all three
pre-registered sort keys**, every one at mean GQ 99.0. *BUB1B*'s position among those seven is
decided by nothing the pre-registration specifies. **The honest unit is the tie block, not the
rank.** The defensible claim is that a phenotype-blind recessive model puts *BUB1B* in the top
~20% of 230 candidates with no prior knowledge of MVA. **[OUR MEASUREMENT]**, re-derived
2026-08-30 by `python3 pipeline/vep_concordance.py`, which also reproduces the 55/230 above from
the pre-registered rule. Re-annotating the same callset with **Ensembl VEP** moves *BUB1B* to
**rank 42 of 184** with its own allele counts unchanged — see
[`annotation-toolchain-vep.md`](annotation-toolchain-vep.md) §6d, which reports **four** rules
side by side — including the post-hoc arm that counts splice consequences as damaging, and which
moves *BUB1B* the other way, to rank 59 of 239. *BUB1B*'s own allele counts are identical under
all four.

**The good half.** The scan recovered the architecture exactly, with no prior:

```
chr15:40,209,701  T>G  stop_gained  0/1     (allele A)
chr15:40,220,612  T>G  missense     0/1     (allele B)
```

One truncating plus one missense, both heterozygous — the canonical MVA compound-heterozygote
architecture (Hanks 2004, PMID 15475955), reconstructed blind.

> ### The bad half, which we are reporting rather than burying: **55th is not first.**
> A phenotype-blind scan does **not** independently nominate this gene. **It corroborates the
> architecture; it does not corroborate the priority.** Anyone claiming a blind scan validates
> their candidate should say where it ranked.

**Why 55th, and why that is not a defence.** The top of the list is dominated by loci notorious in
rare-variant burden scans — of the top 25, **five are HLA genes**, three are mucins, one an
olfactory receptor, and eight more are other known-polymorphic families. They rank highly because
they are hyper-polymorphic, repetitive or VNTR-containing, not because they are disease-relevant.

**That was pre-declared**, verbatim: *"large genes and segmental-duplication regions will rank
highly for purely statistical reasons … is not evidence of anything, and will be stated rather than
filtered away post-hoc."* We could have filtered them out afterwards and reported a flattering
rank. The pre-registration exists precisely to make that unavailable.

⚠️ **A competitor's equivalent scan ranks *BUB1B* first by a 2.1× margin.** We record that too. The
difference is method, not truth, and we are not in a position to say ours is the better one.

## 2. Adversarial self-critique — four claims attacked, on the record

Rather than review by re-reading, the method is: **build the falsification test first, then run
it.** All four below were run on 2026-08-29.

| claim attacked | test built | outcome |
|---|---|---|
| **"the mosaic aneuploidy is visible in bulk WGS"** — held 3 days, already in a family-facing draft | restrict to uniquely-mapping sites; independent GC+mappability depth model with a known-truth anchor | 🔻 **FALSIFIED.** Mismapping. Replaced by a bounded negative: no gain above **~3.2% of cells** — **4.2%** on the conservative leave-one-chromosome-out variant — on a method that recovers chrX at **0.4999 against a true 0.5000**. 🔻 *(Corrected 2026-08-30: this cell read "~3.4%". **3.4% is the Pass-2 GC-only bound; 0.4999 is the Pass-3 GC+mappability anchor** — the shipped model, whose bound is 3.2%. The sentence welded one model's detection limit to a different model's truth anchor.)* |
| **"neither causal variant disrupts splicing"** | five canonical splice-site pathogenic variants, selected by regex, that **must** score ≥0.5 | 🔻 **The instrument was broken** — our own patch had it returning 0.00 for everything. Fixed; controls 5/5; claim then **confirmed** |
| **"the PS3 ceiling has not moved in 19 months"** | recompute from a ClinVar release newer than the finding's own, by a separate implementation | ✅ **SURVIVES.** 21.6% vs 20.7%; *BUB1B* count reproduces **exactly** (35) |
| **"the compound het is the whole story at this locus"** | genome-wide SV survey; splice prediction; MAPQ callability | ✅ **SURVIVES all three.** No SV at the locus, no splice signal, callability 0.990 vs a 0.983 median |
**[OUR MEASUREMENT — every row above is a run in this repository on 2026-08-29, reproducible via `pipeline/mosaicism_test.py`, `pipeline/mosaicism_pass3.py`, `pipeline/spliceai_run.py` and `canary/run_canary.py`. The verdicts are the tests' own outputs.]**

> **One of four claims did not survive, and it was the most quotable one we had.**

### 2.1 What the failures have in common, and why it is the useful part

Three of the four tests initially returned a **plausible negative from a broken instrument** rather
than an error — a patched encoder scoring noise, a contig-naming mismatch yielding empty output, a
data fetch that wrote 26% of a file and exited zero. **None threw.**

That pattern is the subject of `canary/`, a positive-control panel published with this submission,
and the honest summary is: **we did not catch these by being careful. We caught them by demanding
that each instrument first produce a result we already knew.**

## 3. Compute footprint — measured on the runs that produced this submission, not estimated

Every figure below is read from a log or a file that the pipeline wrote (`pipeline/work/overnight.log`,
`markdup_stats.txt`, `stats_SN.txt`, the VEP and Exomiser run records); none is a projection.
**[OUR MEASUREMENT, 2026-08-27 to 2026-08-30.]**

**Hardware.** One laptop: Apple M3 Max, 14 cores, 36 GB RAM. Two 1 TB external USB disks (exFAT)
held the reference databases; nothing ran in the cloud. **Cost beyond the laptop and its
electricity: none** (LLM API access aside, disclosed in the methods form).

| step | input | wall-clock | resources | output |
|---|---|---|---|---|
| FASTQ integrity + checksums | 8 files (4 lanes × 2 reads), 9.5–10 GiB each where logged, ≈ 80 GB compressed | minutes | `gzip -t`, `sha256sum` | `fastq.sha256` manifest; FASTQs deleted afterwards |
| Whole-genome alignment, per lane | one lane pair | **2 h 38 m – 2 h 44 m** each (L001 2:41, L002 2:44, L003 2:38, L004 ≈ 3 h); four lanes sequentially ≈ **11.3 h** | `bwa mem -t 8` → `samtools sort`, GRCh38 no-alt + hs38d1 | four sorted lane CRAMs, ≈ 5.2 GB each |
| Merge + duplicate marking + QC + targeted re-call + pileups | four lane CRAMs | **49 min** (20:49 → 21:38) | `samtools markdup -@ 4` streaming, no `-S` (the read-name temp for `-S` hit 46 GB with zero output in 15 min and was dropped; it does not change primary-alignment duplicate calls, measured at both causal positions) | **`WGS_EX2312012_HGWCNDSX7.markdup.cram`, 19.9 GB + index** |
| Depth per 500 kb window over the CRAM | 19.9 GB CRAM | ≈ 15 min | `mosdepth -t 4 -Q 60` | `depthQ60.regions.bed.gz` |
| VEP on the rare-variant set | 313,417 variants | **10 min 28 s** | Docker `ensemblorg/ensembl-vep:release_116.1` (1.29 GB image), `--fork 6`, 28 GB offline cache mounted **read-only** from USB | 433,168 annotation rows; count conservation asserted by `pipeline/vep_check.py` |
| Exomiser on a public whole genome (GIAB HG002) | 4,096,123 variants | **9 min 20 s** | Exomiser 15.1.0, `-Xmx6g`, 54 GB data (30 GB hg38 + 24 GB phenotype) on USB | *FGFR2* rank 1 — see `generalisation-public-case.md` |

**What the alignment produced, as a check that it is a real whole genome and not a subset:**
1,076,022,529 reads written; 1,067,610,275 mapped (99.6 %); 155.9 Gb of mapped bases, ≈ 50× over
3.1 Gb before duplicate removal; 137,794,964 duplicates marked (12.9 % of primary reads); mean read
length 149. The two causal positions were re-piled from this CRAM: 47 and 27 reads
(`overnight.log`, stage 5).

**Storage discipline, because it was the binding constraint.** The internal disk reached 95 % full
during the run. A whole-genome BAM would have been ≈ 63 GB (scaled from a measured 5.05 GB chr1
BAM); streaming lane CRAMs into a single deduplicated CRAM kept the peak near 20 GB of output, and
the FASTQs were deleted only after the merged read count matched the expected 1,076,022,529 and
every file's checksum was on record. **The realignment is reproducible from the public FASTQs in
≈ 12 h on the same hardware; it is not required for any Track 2 conclusion**, which rest on the
organizers' VCF and on the literature.

**Why this is stated.** The Scalability criterion asks whether the approach can be applied to other
individuals. A full realignment, standard annotation with the clinical toolchain, and a
phenotype-driven genome-wide rank on a 4.1-million-variant public genome all completed on one
consumer laptop in under a working day of compute, with every database offline. That is the scale
at which a rare-disease family or a single clinical group operates, and it is the scale this
submission was built at.

## 4. What this section is not

It is not a claim that the analysis is correct. It is a claim that **the specific ways we could
find to make it wrong have been tried and are recorded**, including the one that worked. Anyone
who wants to attack the finding should start at §1 — the 55th-place rank is the weakest point and
we would rather name it than have it found.
