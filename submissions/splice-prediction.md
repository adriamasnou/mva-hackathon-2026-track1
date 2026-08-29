# Do either of this child's variants also disrupt splicing?

**Local SpliceAI, run as the model rather than as lookup — with a positive control that caught a
silent failure of our own making.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. Why this question is load-bearing

The Track 1 finding is a *BUB1B* compound heterozygote: **L737\*** (nonsense) and **N1002K**
(pseudokinase-domain missense). The Track 2 thesis rests on a specific consequence of that pair —
the nonsense allele produces no protein, so **every residual BubR1 molecule in this child is the
N1002K form.** There is no wild-type pool.

That model assumes each variant does exactly one thing. **If the missense allele also disrupted
splicing, it would produce an aberrant transcript rather than a full-length altered protein, and
the dose argument would be wrong.** Coding annotation cannot see that. This is the check.

## 2. Why the model, and not the precomputed scores

Exomiser's `2512_hg38` bundle **does** carry real SpliceAI delta scores and applies them — verified
with actual values, not merely the source name appearing in output. But in a test run only **20 of
63 variant records (32%) carried a delta.** A variant absent from the precomputed set returns no
score, and **at the point of use a missing score is indistinguishable from a benign one.** For two
variants on which an argument rests, that gap is the entire question.

Illumina's precomputed score files sit behind a BaseSpace login. **The model is pip-installable and
GPL-3.0, needs no account, and scores any variant including indels**, which the precomputed SNV set
does not cover. The login-gated artefact is the weaker one.

## 3. 🔴 The positive control, and the silent failure it caught

Five **canonical splice-site pathogenic variants** from ClinVar — positions ±1/±2 of an exon
boundary, where disruption is not in doubt — were run as a control that **must** return
non-zero. **[OUR MEASUREMENT — the five were selected mechanically from ClinVar
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
merely returning large numbers — it is returning the right *kind* of large number.

> ### 🔻 The first run of this control returned 0.00 for all five, and the cause was our own patch.
> SpliceAI 1.3.1 predates numpy 2 and calls the removed `np.fromstring`, so it installs and imports
> cleanly and then dies on the first variant. Our replacement used `np.frombuffer` on the raw
> sequence letters and **dropped the byte substitution that precedes it** (`A→\x01, C→\x02, G→\x03,
> T→\x04, N→\x00`). That substitution is not decoration — **it is the encoding.** Without it `A`
> (65 % 5 = 0) was read as `N` and `G` (71 % 5 = 1) as `A`. The model scored noise.
>
> **It did not error. It returned a plausible "no splice signal" for every input — including the
> five variants above.** We had already run the child's variants through the broken version and
> obtained the same answer we now believe to be correct, *for entirely the wrong reason.*
>
> **A negative result from an uncontrolled instrument is indistinguishable from a broken one.**

## 4. Result

| variant | gene | DS_AG | DS_AL | DS_DG | DS_DL | max | verdict |
|---|---|---|---|---|---|---|---|
| `15:40209701 T>G` (**L737\***) | *BUB1B* | 0.03 | 0.00 | 0.00 | 0.01 | **0.03** | no splice signal |
| `15:40220612 T>G` (**N1002K**) | *BUB1B* | 0.02 | 0.00 | 0.00 | 0.00 | **0.02** | no splice signal |
| `15:40220612 T>G` | *PAK6* | 0.02 | 0.00 | 0.01 | 0.00 | **0.02** | no splice signal |

All well below the high-sensitivity threshold of 0.2. **[OUR MEASUREMENT — SpliceAI 1.3.1 model,
GRCh38, ±500 bp window, run locally 2026-08-29.]**

> **Neither variant shows a splice-altering signal. The nonsense allele acts as a nonsense allele
> and the missense allele acts as a missense allele — which is exactly what the dose argument
> assumes, and it could have come out otherwise.**

The second variant overlaps *PAK6*, which shares this locus with *BUB1B*; it is unaffected too.

## 5. What this establishes, and what it does not

- ✅ **It removes a specific way the thesis could have been wrong.** An aberrant-transcript
  mechanism for N1002K is not supported.
- ❌ **It is a prediction, not an observation.** Only RNA — patient fibroblast RT-PCR or
  RNA-seq — can demonstrate what the transcripts actually are. SpliceAI is a strong predictor and
  it is still a predictor.
- ❌ **A low delta is not proof of no effect.** SpliceAI has known blind spots for deep-intronic
  and structural events, and the window here is ±500 bp.
- ❌ **This says nothing about the variants' protein-level consequences**, which are argued
  elsewhere from other evidence.

## 6. Reproduce

```bash
python3 pipeline/spliceai_run.py <variants.vcf.gz>
```

Reference: `GRCh38.primary.fa.bgz`. ⚠️ **The reference must be the Ensembl-named one.** SpliceAI's
bundled `grch38` annotation uses `1`, not `chr1`; the UCSC-named `GRCh38_no_alt` reference used by
our alignment and depth work **does not match, and mismatching produces silently empty scores
rather than an error.** This was the fifth chromosome-naming trap encountered in a single day of
work, and the runner documents it at the point of use.
