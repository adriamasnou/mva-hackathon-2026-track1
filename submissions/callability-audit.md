# Which parts of this genome can be trusted, and is the answer in one of them?

**A genome-wide MAPQ/callability audit — and the check that the causal locus is not in a dark region.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. Why this is not optional

Short-read sequencing does not cover the genome evenly. Where sequence resembles other sequence,
reads cannot be placed uniquely, and every variant call there inherits that ambiguity. **A negative
result in a dark region is not a negative result — it is an absence of information wearing the same
clothes.**

This project learned that expensively on the same day: a chromosome-scale signal that looked like
the cellular phenotype of MVA turned out to be **mismapping**, and it survived until someone asked
which sites were uniquely mapping (`F-029`). This audit is the general version of that question.

## 2. Method

Two `mosdepth` passes over the same **45× CRAM**, at 500 kb resolution: one unfiltered, one at
**MAPQ ≥ 60** (uniquely mapping). **Callability = MAPQ≥60 depth ÷ unfiltered depth** — an empirical,
per-bin measure taken from this sample's own alignments rather than from a static annotation, so it
reflects what actually happened to these reads against this reference.

## 3. The genome

| percentile of autosomal bins | callability |
|---|---|
| p1 | 0.004 |
| p5 | 0.603 |
| **p50 (median)** | **0.983** |
| p95 | 0.994 |

**Across 5,531 autosomal 500 kb bins, the median bin retains 98.3% of its depth at MAPQ ≥ 60.**
The distribution is sharply bimodal: most of the genome is essentially fully callable, and a small
tail is close to unusable.

| | bins | share of the autosome |
|---|---|---|
| **DARK** (callability < 0.50) | **238** | **4.3%** |
| **VERY DARK** (< 0.25) | 157 | 2.8% |

**[OUR MEASUREMENT — mosdepth over the merged 45× CRAM, GRCh38, 2026-08-29.]**

## 4. The dark burden is not spread evenly

| chromosome | % of bins dark | median callability |
|---|---|---|
| **chr21** | **16.0%** | 0.985 |
| **chr9** | 12.5% | 0.981 |
| **chr22** | 11.7% | 0.980 |
| chr16 | 11.4% | 0.983 |
| chr15 | 8.2% | 0.983 |
| chr18 | 8.1% | 0.984 |
| … | | |
| chr6 | 0.9% | 0.983 |
| chr19 | 0.9% | 0.980 |

Note the **median** column barely moves. The chromosomes differ not in typical quality but in **how
much unusable sequence they carry** — pericentromeric and segmentally-duplicated regions, which are
concentrated on the acrocentrics and on chr9 and chr16.

> ### This independently corroborates `F-029`.
> That finding showed the apparent mosaic-aneuploidy signal on chr20/21/22 was mismapping, from a
> completely different measurement — the fraction of *heterozygous calls* with MQ < 60 (33.8% /
> 31.0% / 33.7% against 11–13% typical). **This audit, from read depth rather than from variant
> calls, puts chr21 and chr22 first and third by dark burden.** Two independent measures, same
> answer. An 18-fold difference in dark burden between chr21 and chr19 is exactly the kind of
> structure that manufactures a chromosome-specific artefact.

## 5. ★ The question that actually matters here

A genome-wide statistic is worth little if the locus the case turns on sits in the bad tail.

> ### *BUB1B* callability: **0.990** — against a genome-wide median of 0.983.
> The locus carrying both causal variants is in **more** reliably mappable sequence than the typical
> bin, and nowhere near the 0.50 dark threshold. The same is true of *PAK6*, which shares the locus.

**The compound-heterozygote call does not rest on ambiguous alignment.** Together with the SV survey
(no structural variant of any kind at the locus) and the splice analysis (neither variant
splice-altering), this is the third independent way the finding could have failed and did not.

## 6. Limitations

1. **500 kb bins.** A fully dark exon inside a bright bin is invisible at this resolution. The
   *BUB1B* result should be read as "the locus is not in a dark region", **not** as "every base of
   *BUB1B* is callable".
2. **MAPQ ≥ 60 is aligner-specific.** It is the maximum for this aligner; another would need a
   different threshold, and the ratio is not portable across aligners.
3. **Callability is not accuracy.** A uniquely-mapping read can still be wrong. This bounds one
   failure mode, not all of them.
4. **Autosomal statistics exclude chrX and chrY**, whose copy number differs in this male sample and
   which are treated separately in the mosaicism analysis.

## 6a. ✅ Independently re-derived, 2026-08-31

**This document had never been claim-audited.** Every number in it was recomputed from
`data/derived/scans/depth{,Q60}.regions.bed.gz` on 2026-08-31, and **all of them reproduce
exactly**: 5,531 autosomal bins · p1 **0.004** · p5 **0.603** · median **0.983** · p95 **0.994** ·
DARK <0.50 **238 (4.3%)** · VERY DARK <0.25 **157 (2.8%)** · chr21 **16.0% / 0.985**, chr9
**12.5% / 0.981**, chr22 **11.7% / 0.980**, chr16 **11.4% / 0.983**, chr6 and chr19 **0.9%** ·
***BUB1B* bin 0.990**. The "18-fold" chr21-vs-chr19 ratio is 17.8. **No defect found.**
[OUR MEASUREMENT — re-derivation 2026-08-31, independent of the original run.]

## 7. Reproduce

```bash
mosdepth -Q 60 -n --by 500000 -f <ref.fa> depthQ60 <sample.cram>
mosdepth       -n --by 500000 -f <ref.fa> depth     <sample.cram>
# callability = per-bin depthQ60 / depth
```

The same track is used as the mappability covariate in `pipeline/mosaicism_pass3.py`, where adding
it moved the chrX truth anchor from 0.33% error to **0.01%** — independent evidence that the track
is measuring something real.
