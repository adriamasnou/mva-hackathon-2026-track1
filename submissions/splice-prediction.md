# Do either of this child's variants also disrupt splicing?

**Local SpliceAI, run as the model rather than as lookup — with a positive control that caught a
silent failure of our own making.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. Why this question is load-bearing

The Track 1 finding is an inferred *BUB1B* compound heterozygote: **L737\*** (nonsense) and **N1002K**
(pseudokinase-domain missense). The Track 2 thesis rests on a specific consequence of that pair —
the nonsense allele may undergo nonsense-mediated decay and N1002K may supply residual full-length protein. **Phase, transcript decay and protein abundance are unmeasured**, so this is a conditional model, not an established protein inventory.

Coding annotation does not exclude an additional RNA effect. **A splice alteration could change
the amount or composition of full-length transcript and therefore change the abundance/function
hypothesis.** Aberrant and normally spliced transcripts could coexist, with effects depending on
transcript and cell context. The analysis below tests the model's prediction for the queried
annotations; it does not measure RNA or establish the protein inventory.

## 2. Why the model, and not the precomputed scores

Exomiser's `2512_hg38` bundle **does** carry real SpliceAI delta scores and applies them — verified
with actual values, not merely the source name appearing in output. But in a test run only **20 of
63 variant records (32%) carried a delta.** A variant absent from the precomputed set returns no
score. **A missing score must remain missing, not be interpreted as a benign result.** Running the
model supplies a prediction for supported inputs; it does not turn a low score into evidence that
splicing is normal.

Illumina's precomputed score files sit behind a BaseSpace login. **The model is pip-installable and
GPL-3.0, needs no account, and can score supported variants including indels**, which the precomputed SNV set
does not cover. The login-gated artefact is the weaker one.

## 3. 🔴 The positive control, and the silent failure it caught

Five **canonical splice-site variants with Pathogenic assertions** in ClinVar — positions ±1/±2
of an exon boundary — were run as positive controls for an expected model response.
**[OUR MEASUREMENT — the five were selected mechanically from ClinVar
`variant_summary.txt.gz` (GRCh38) by matching `c.N±1/±2` in the variant name with a
Pathogenic assertion; they were not hand-picked for a good result.]**

| variant | gene | DS_AG | DS_AL | DS_DG | DS_DL | max |
|---|---|---|---|---|---|---|
| `c.25-2A>G` | *WDR35* | 0.37 | **0.81** | 0.00 | 0.01 | **0.81** |
| `c.76-1G>T` | *WDPCP* | 0.02 | **0.84** | 0.00 | 0.82 | **0.84** |
| `c.636+1G>C` | *UROD* | 0.01 | 0.28 | 0.46 | **0.90** | **0.90** |
| `c.894+1G>A` | *LIPA* | 0.00 | 0.70 | 0.13 | **0.94** | **0.94** |
| `c.427+2T>G` | *TCN2* | 0.00 | 0.23 | 0.38 | **0.92** | **0.92** |

**5 of 5 flagged, and each on the correct mechanism**: the two acceptor-site variants (`-1`, `-2`)
score acceptor-loss; the three donor-site variants (`+1`, `+2`) score donor-loss. The model is not
merely returning large numbers — the largest changes match the expected splice-site class in
these controls. This small selected set tests pipeline behaviour; it does not estimate clinical
sensitivity, specificity or the negative predictive value of a low score in this case.

> ### 🔻 The first run of this control returned 0.00 for all five, and the cause was our own patch.
> SpliceAI 1.3.1 predates numpy 2 and calls the removed `np.fromstring`, so it installs and imports
> cleanly and then dies on the first variant. Our replacement used `np.frombuffer` on the raw
> sequence letters and **dropped the byte substitution that precedes it** (`A→\x01, C→\x02, G→\x03,
> T→\x04, N→\x00`). That substitution is not decoration — **it is the encoding.** Without it `A`
> (65 % 5 = 0) was read as `N` and `G` (71 % 5 = 1) as `A`. The model scored noise.
>
> **It did not error. It returned a plausible "no splice signal" for every input — including the
> five variants above.** The child's variants had also received low scores from that broken
> version. Similar low scores after repairing the encoding do not retrospectively validate the
> broken run or establish that the child's splicing is unaffected.
>
> **A negative result from an uncontrolled instrument is indistinguishable from a broken one.**

## 4. Result

| variant | gene | DS_AG | DS_AL | DS_DG | DS_DL | max | model result |
|---|---|---|---|---|---|---|---|
| `15:40209701 T>G` (**L737\***) | *BUB1B* | 0.03 | 0.00 | 0.00 | 0.01 | **0.03** | low predicted delta |
| `15:40220612 T>G` (**N1002K**) | *BUB1B* | 0.02 | 0.00 | 0.00 | 0.00 | **0.02** | low predicted delta |
| `15:40220612 T>G` | *PAK6* | 0.02 | 0.00 | 0.01 | 0.00 | **0.02** | low predicted delta |

All are below the model's reported high-sensitivity operating cutoff of 0.2. **This is a model
threshold, not a clinically validated boundary for normal splicing or benignity in this case.**
**[OUR MEASUREMENT — SpliceAI 1.3.1 model, GRCh38, bundled `grch38` annotation, ±500 bp
score-aggregation distance, run locally 2026-08-29.]**

> **No high-scoring splice effect was predicted for the queried annotations under this model and
> configuration. These low scores do not establish protein-only action or exclude an RNA
> mechanism. Transcript effects remain unmeasured.**

The second variant also received a low predicted delta for the overlapping *PAK6* annotation.
That prediction does not establish that *PAK6* transcripts or function are unaffected.

## 5. What this establishes, and what it does not

- **The queried annotations have low predicted deltas.** This computational result leaves an
  aberrant-transcript mechanism unresolved; it does not remove that possible failure of the
  abundance/function hypothesis.
- **It is a prediction, not an RNA observation.** Appropriate RNA measurements could test
  transcript effects, with tissue, expression, transcript selection and assay sensitivity taken
  into account. Such measurements have not been performed here.
- **A low delta is not proof of no effect.** The result is conditional on the model, reference,
  annotation and scoring configuration; it does not exclude effects outside the assessed scope.
- **A local distance comparison reproduced the same maxima.** Jaganathan 2019 (PMID 30661751)
  defines its variant delta using the largest prediction change within 50 nt of the variant.
  That score-aggregation distance is distinct from the model's input sequence context. The
  paper's benchmark operating characteristics do not automatically calibrate our wider setting.
  **Re-run at 50 nt
  (2026-08-31): every reported maximum is identical — L737\* 0.03, N1002K *BUB1B* 0.02, N1002K
  *PAK6* 0.02.** Two non-maximal components fall to zero (L737\* `DS_DL` 0.01 → 0.00, N1002K/*PAK6*
  `DS_DG` 0.01 → 0.00). Those components are shown in the ±500 bp table above; the equal maxima
  establish robustness to this tested setting change, not absence of an RNA effect.
  **[OUR MEASUREMENT — same model, same reference, `dist` argument 50 instead of 500.]**
- **This does not establish the variants' protein-level consequences**, which are considered
  elsewhere from other evidence.

## 5a. Local numerical rerun, 2026-08-31

**This document had never been claim-audited.** The result table was **re-run from scratch** on
2026-08-31 — `python3 pipeline/spliceai_run.py` against a freshly written two-variant VCF — and
**every value reproduces exactly**: L737\* *BUB1B* `0.03 / 0.00 / 0.00 / 0.01`, max **0.03**;
N1002K *BUB1B* `0.02 / 0.00 / 0.00 / 0.00`, max **0.02**; N1002K *PAK6* `0.02 / 0.00 / 0.01 /
0.00`, max **0.02**. The tool prints three operating cutoffs (0.2 / 0.5 / 0.8).
**This historical rerun confirmed numerical reproducibility of the local calculation. It was
not an independent model validation or a clinical calibration, and it did not validate the
earlier biological interpretation of a low score.**

*The byte-encoding arithmetic in §3 also checks out: `A`=65, 65 mod 5 = **0** (read as `N`);
`G`=71, 71 mod 5 = **1** (read as `A`) — exactly the corruption described.* And 20/63 = **31.7%**,
consistent with the "32%" in §2.

## 6. Reproduce

```bash
python3 pipeline/spliceai_run.py <variants.vcf.gz>
```

Reference: `GRCh38.primary.fa.bgz`. ⚠️ **The reference must be the Ensembl-named one.** SpliceAI's
bundled `grch38` annotation uses `1`, not `chr1`; the UCSC-named `GRCh38_no_alt` reference used by
our alignment and depth work **does not match, and mismatching produces silently empty scores
rather than an error.** This was the fifth chromosome-naming trap encountered in a single day of
work, and the runner documents it at the point of use.
