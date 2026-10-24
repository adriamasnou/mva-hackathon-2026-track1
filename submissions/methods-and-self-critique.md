# The phenotype-blind scan, and everything we tried to break

**Retained negative findings, corrected claims and measured computational limits.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · original record 2026-08-29, updated 2026-10-24 · CC BY 4.0*

---

## 1. The phenotype-blind scan — a pre-declared failure condition, reported as one

The obvious attack on our finding is that **we found what we went looking for.** *BUB1B* was
reached with a candidate-gene prior; a prior that strong can manufacture its own confirmation.

The algorithm was re-run without phenotype or a candidate list: **no gene list, no HPO terms, no panel** — against a
filter recorded *before* this run, after the team already knew the candidate in `pipeline/recessive_scan_PREREGISTERED.md`.

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
rank.** The defensible claim is that a phenotype-blind recessive model puts *BUB1B* in approximately the top quarter of 230 candidates under a rule that does not use phenotype or a gene list. **[OUR MEASUREMENT]**, re-derived
2026-08-30 by `python3 pipeline/vep_concordance.py`, which also reproduces the 55/230 above from
the pre-registered rule. Re-annotating the same callset with **Ensembl VEP** moves *BUB1B* to
**rank 42 of 184** with its own allele counts unchanged — see
[`annotation-toolchain-vep.md`](annotation-toolchain-vep.md) §6d, which reports **four** rules
side by side — including the post-hoc arm that counts splice consequences as damaging, and which
moves *BUB1B* the other way, to rank 59 of 239. *BUB1B*'s own allele counts are identical under
all four.

**The good half.** The scan recovered the same heterozygous truncating-plus-missense pair without a phenotype or candidate-gene list in the filter:

```
chr15:40,209,701  T>G  stop_gained  0/1     (allele A)
chr15:40,220,612  T>G  missense     0/1     (allele B)
```

One truncating plus one missense, both heterozygous. **If they are in trans**, this pair is consistent with the allelic architecture reported in BUB1B-associated MVA (Hanks 2004, PMID 15475955). Hanks demonstrated opposite-parent inheritance in its families; phase here remains unconfirmed, and N1002K's residual function is unmeasured. An analyst who already knows the answer is not blinded.

> ### The bad half, which we are reporting rather than burying: **55th is not first.**
> A phenotype-blind scan does **not** independently nominate this gene. **It corroborates the
> variant-pair pattern; it does not establish phase, missense function or the priority.** Anyone claiming a blind scan validates
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
| **"neither candidate variant has a high SpliceAI prediction"** | five canonical splice-site pathogenic controls with a regression threshold ≥0.5 | 🔻 **The instrument was broken** — our own patch had it returning 0.00 for everything. Fixed; controls 5/5; low prediction scores reproduced; an experimental absence of splice effects remains unproven |
| **"the PS3 ceiling has not moved in 19 months"** | recompute from a ClinVar release newer than the finding's own, by a separate implementation | ✅ **SURVIVES.** 21.6% vs 20.7%; *BUB1B* count reproduces **exactly** (35) |
| **"no additional event was detected by these surveys"** | genome-wide SV survey; splice prediction; MAPQ callability | No SV or large splice-prediction signal detected within the analyses’ limits; callability 0.990 vs a 0.983 median. This does not exclude every additional cause. |
**[OUR MEASUREMENT — historical project runs on 2026-08-29. `pipeline/mosaicism_test.py` and `pipeline/mosaicism_pass3.py` are retained in the private working project, not distributed in this package. The package includes `pipeline/spliceai_run.py` and `canary/run_canary.py`; patient-data reruns require authorized inputs and local dependencies.]**

> **One of four claims did not survive, and it was the most quotable one we had.**

### 2.1 What the failures have in common, and why it is the useful part

Three of the four tests initially returned a **plausible negative from a broken instrument** rather
than an error — a patched encoder scoring noise, a contig-naming mismatch yielding empty output, a
data fetch that wrote 26% of a file and exited zero. **None threw.**

That pattern is the subject of `canary/`, a positive-control panel included in this local submission package,
and the practical lesson is: **we did not catch these by being careful. We caught them by demanding
that each instrument first produce a result we already knew.**

## 3. Compute footprint — measured on the runs that produced this submission, not estimated

Every figure below is read from a log or a file that the pipeline wrote (`pipeline/work/overnight.log`,
`markdup_stats.txt`, `stats_SN.txt`, the VEP and Exomiser run records); none is a projection.
**[OUR MEASUREMENT, 2026-08-27 to 2026-08-30.]**

**Historical hardware.** One laptop: Apple M3 Max, 14 cores, 36 GB RAM. Two 1 TB external USB disks (exFAT)
held the reference databases; no separately billed cloud compute is recorded. Hardware, electricity,
human time and LLM subscriptions were not apportioned to these runs; the table is not a total project-cost estimate.

| step | input | wall-clock | resources | output |
|---|---|---|---|---|
| FASTQ integrity + checksums | 8 files (4 lanes × 2 reads), 9.5–10 GiB each where logged, ≈ 80 GB compressed | minutes | `gzip -t`, `sha256sum` | `fastq.sha256` manifest; FASTQs deleted afterwards |
| Whole-genome alignment, per lane | one lane pair | **2 h 38 m – ≈ 3 h** each (L001 2:41, L002 2:44, L003 2:38, L004 ≈ 3 h); four lanes sequentially ≈ **11.3 h** | `bwa mem -t 8` → `samtools sort`, GRCh38 no-alt + hs38d1 | four sorted lane CRAMs, ≈ 5.2 GB each |
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
every file's checksum was on record. **The realignment is reproducible from the access-controlled hackathon FASTQs in
≈ 12 h on the same hardware; it is not required for any Track 2 conclusion**, which rest on the
organizers' VCF and on the literature.

**What those timings establish.** The separate alignment, annotation and public-genome analyses
completed on the stated laptop and storage. They do not measure clinical turnaround, other hardware,
independent diagnostic performance or family usability. Their logs cover different runs and must not
be combined into an unsupported end-to-end working-day claim.

**October reconstruction.** Both reconstructed FGFR2 jobs completed in **200.48 seconds including
startup**, with FGFR2 first among 2 and 471 scored genes. This newer execution used recovered public
databases on a larger external disk and retained exact configuration and outputs. The missing August
YAML was not recovered; changed candidate counts and hardware/configuration prevent treating the two
timings as a controlled speed comparison. [Executed reconstruction and offline verification](generalisation-public-case.md).
**[OUR MEASUREMENT — October execution receipt retained with the reconstructed results.]**

## 4. What this section is not

These checks address the specified failure modes and retain negative findings. They do not exhaust
possible errors. The phenotype-blind severity tie at ranks 53–61 is a limited ranking result;
unresolved phase, allele function and treatment response remain distinct biological limitations.
