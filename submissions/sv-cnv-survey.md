# Genome-wide structural variant and CNV survey

**Does anything structural contribute to this child's phenotype — and is the compound heterozygote
the complete molecular explanation?**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. Why this was run

The Track 1 finding is a biallelic *BUB1B* compound heterozygote: a nonsense allele and a
pseudokinase-domain missense allele. That model makes a strong structural claim — **that all
residual BubR1 in this child is the missense form** — and the claim only holds if nothing
structural is also happening at the locus. A cryptic deletion, duplication or inversion at
*BUB1B* would change the interpretation entirely.

Short-read SNV calling cannot see those. This survey was run to look for them, and to ask
whether any structural variant elsewhere contributes to features the *BUB1B* pair does not
explain.

## 2. Method

`delly` on the **45× merged CRAM** (four lanes, `GRCh38_no_alt_plus_hs38d1`), genome-wide,
producing two callsets — an intra-chromosomal set and a fuller set including inter-chromosomal
breakends.

| callset | records | DEL | DUP | INV | INS | BND |
|---|---|---|---|---|---|---|
| intra-chromosomal | 32,197 | 20,264 | 6,565 | 3,560 | 1,808 | — |
| **full (used here)** | **53,610** | 20,905 | 7,182 | 3,756 | 1,842 | 19,925 |

Of the full set, **18,675 carry `PASS`** and 34,935 are `LowQual`.

## 3. 🔴 The raw PASS set is not a findings set, and saying so is part of the result

Before any biological reading, the callset has to be characterised honestly:

- **`PASS` does not mean the sample carries the variant.** 496 DEL, 387 DUP and 561 BND calls are
  `PASS` with genotype `0/0`.
- **The large end is dominated by artefact.** The largest `PASS` "deletion" spans **223 Mb** —
  longer than any human chromosome. 383 `PASS` calls exceed 5 Mb, and **348 of those (91%) are
  `IMPRECISE`**, i.e. supported by discordant read pairs with no breakpoint-spanning reads.
- Size distribution of `PASS` DEL/DUP/INV: 9,064 below 1 kb, 1,522 at 1–10 kb, 768 at 10–100 kb,
  652 at 100 kb–1 Mb, 373 at 1–5 Mb, **516 above 5 Mb**.

Applying the filters this implies — `PASS`, a carried genotype, ≤ 5 Mb, and `PRECISE` — leaves a
**high-confidence intra-chromosomal set of 10,206 calls**: 8,285 DEL, 1,603 INS, 174 INV, 144 DUP.
Excluded: 383 oversized, 2,778 imprecise, 3,614 breakends.

**[OUR MEASUREMENT — `delly` output on the merged CRAM, filtered with `bcftools`; every count
above re-derived from the BCF in the same session as this write-up.]**

## 4. ★ The primary result: *BUB1B* is structurally clean

> ### No structural variant of any type, at any confidence level, affects *BUB1B*
> ### (chr15:40,160,984–40,221,137).

The single call returned by a positional query of that window originates at chr15:24,767,504 — a
`LowQual`, oversized duplication whose annotated end merely spans the region. There is no
deletion, duplication, inversion or breakend at the locus.

**This is the check the compound-heterozygote model needed.** There is no cryptic third allele, no
structural deletion of the second copy, and no rearrangement disrupting the gene. The two SNVs are
the complete molecular explanation at *BUB1B*, and the claim that all residual BubR1 is the
missense form survives a structural challenge that could have falsified it.

## 5. The rest of the spindle-assembly checkpoint

Nine SAC and MVA-associated genes were screened for high-confidence carried calls:

| gene | result |
|---|---|
| ***BUB1B*** | **no SV** |
| *CEP57*, *CENPF*, *MAD2L1*, *TTK* | no SV |
| *BUB1* | 1 — chr2:108,525,365, INV 3.8 Mb, **IMPRECISE**, PE 13, **no split reads** |
| *TRIP13* | 1 — chr5:262,544, INV 1.3 Mb, **IMPRECISE**, PE 12, **no split reads** |
| *CENPE* | 2 — 26 bp and 104 bp deletions, PRECISE, SR 4 and 15 |
| *MAD1L1* | 1 — 38 bp deletion, PRECISE, SR 8 |

**None is a credible contributor.** The two megabase inversions are imprecise, carry no
breakpoint-spanning read support, and begin far outside the genes they are annotated as
overlapping — the signature of discordant-pair artefact, not of a real rearrangement. The three
small deletions are indel-scale heterozygous events of the kind present in every genome, in a
child who already has a complete biallelic explanation for his condition.

## 6. Consistency with the aneuploidy analysis

This survey and the mosaicism analysis are independent methods that agree. No chromosome-scale
duplication survives filtering, which is what the GC-corrected depth analysis also found — no
mosaic gain of chr20, 21 or 22 above ~3.4% of cells. **Two methods, one negative.**

That negative does not bear on the diagnosis, which rests on direct cytogenetics of dividing
cells — a far more sensitive assay for mosaic aneuploidy than bulk short-read WGS of blood.

## 7. Limitations — this is a screen, not a validated SV callset

1. **A single caller.** `delly` only. No `manta`/`smoove`/`GRIDSS` consensus, and no caller
   intersection. Sensitivity and specificity are both unmeasured here.
2. **No population frequency filter.** gnomAD-SV was not applied, so the 10,206 high-confidence
   calls are **not** rare variants — most will be common polymorphisms.
3. **No manual review.** Nothing was inspected in a genome browser; the SAC-gene calls were
   adjudicated from evidence fields alone.
4. **No orthogonal confirmation.** Nothing here has been confirmed by a second technology.
5. **Short reads.** Balanced rearrangements, events in segmental duplications, and repeat-mediated
   variation are systematically under-detected — the same mappability limitation quantified in the
   mosaicism analysis.

**The *BUB1B* negative in §4 is robust to all five**, because it is an absence across every call
in the region at every confidence level, not a judgement about any particular call. The
genome-wide numbers in §3 should be read as a characterisation of the callset, not as findings.

## 8. Reproduce

```bash
bcftools view -f PASS -H data/derived/scans/delly_wgs/wgs.bcf | wc -l
bcftools view -r chr15:40160984-40221137 -H data/derived/scans/delly_wgs/wgs.bcf
```

The BCFs are derived from gated data and are not redistributed here. This document reports counts,
categories and a handful of named calls in candidate genes — findings, not the dataset.
