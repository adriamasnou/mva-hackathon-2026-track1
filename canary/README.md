# The canary panel — is your rare-disease pipeline actually working?

**A positive-control set for the *interpretation* layer of a rare-disease pipeline.
Not a benchmark of how accurate your tools are — a test of whether they are running at all.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## The problem

Bioinformatics tools do not usually fail loudly. **They fail closed** — they return *nothing found*.

In one day of work on a single child's genome, we hit five instances of exactly this, and not one
of them threw an exception:

| what broke | what it returned |
|---|---|
| our patch to make SpliceAI run on numpy 2 | **0.00 for every variant** — including five canonical splice-site pathogenic variants |
| Ensembl (`1`) vs UCSC (`chr1`) contig naming, **five separate times** | **silently empty results** |
| a public API queried for "all" classifications | **a subset that looked like the whole set** |
| precomputed pathogenicity scores covering 32% of variants | **no score, indistinguishable from a benign score at the point of use** |
| a cached census advertising the provenance of its method, not the age of its data | **a confidently wrong count** |
| **our own PanelApp fetcher**, aborting at page 85 of 326 | **printed `DONE`, exited 0, wrote 26% of the data** |

Every one produced a **plausible negative.** Every one would have been reported as a clean result.

> ### 🔴 The last row is the one that should be believed.
> That fetcher was written **on the same afternoon as this panel, by the same hand, while building
> the tool to catch exactly this.** It downloaded a quarter of a dataset, announced success, exited
> zero, and a population-scale statistic was computed from it before anyone checked the page count.
> **Knowing about a failure mode does not protect you from it.** Only an assertion does — which is
> why the rewritten fetcher now reads the API's own declared `count` and exits non-zero if what it
> wrote is short. *A partial download that announces success is worse than one that crashes.*

> ### In clinical genomics, "nothing found" is a diagnosis.
> A silently broken diagnostic pipeline does not crash. It produces an undiagnosed patient and a
> family that keeps looking. Some part of the rare-disease diagnostic odyssey is not biology being
> hard — it is tooling failing closed and being believed.

## What this is, and how it differs from benchmarking

There is an established literature on **accuracy** — how well does SpliceAI predict splicing?
There is `GIAB` for **variant-calling** truth sets. We could not find an equivalent for
**liveness**: *is the tool in front of me producing real output right now?*
**[unverified-novel — one literature search, which is a floor and not a fact. If this exists, this
panel should defer to it and we would rather be told.]**

Accuracy asks *how often is the tool right?* Liveness asks *is the tool answering at all?*
**A tool with 95% accuracy and a silent failure returns the same thing as a tool with 0% accuracy:
a confident negative.**

## Design rules

1. **Every expectation must be one no reasonable person disputes.** Canonical ±1/±2 splice sites.
   A male's single X chromosome. A gene whose phenotype match is the textbook case. If an
   expectation needs an argument, it belongs in a benchmark, not a canary.
2. **Selected mechanically, never hand-picked.** The five splice variants were pulled from ClinVar
   by regex on `c.N±1/±2` plus a Pathogenic assertion — not chosen because they gave a good result.
3. **Every panel carries a NEGATIVE control.** A tool stuck at "everything is pathogenic" fails as
   surely as one stuck at "nothing found", and only a negative catches it.
4. **The answer must be checkable without the tool under test.** Published, or arithmetic.
5. **Failure must be loud.** The runner exits non-zero and names the assertion.

## The panels

### Panel 1 — splice prediction (`canary_variants.tsv`)
Five canonical splice-site Pathogenic variants, each of which **must** score ≥0.5, plus one coding
nonsense variant that **must** score <0.2.
**This panel has already caught a real, silent, total failure** — our own numpy patch, which
returned 0.00 for all six and would otherwise have been reported as "no splice signal found".
It also validates *mechanism*: the two acceptor-site variants must score acceptor-loss and the
three donor-site variants donor-loss. A tool returning large numbers on the wrong axis is broken.

### Panel 2 — copy-number / depth (no file needed; it is already in your data)
**In a male sample, chrX must return a depth ratio of 0.500 against the autosomes.**
Free, requires no download, and is a *known-truth* copy-number change present in every male genome
you will ever analyse. Our GC+mappability model returns **0.4999** (0.01% error); the same model
with one covariate removed returns 0.4991, and an earlier version returned **0.0000** because a
filter had silently dropped every chrX bin — *the filter deleted the control that validates the
method.* **If your CNV pipeline cannot recover chrX in a male, it cannot recover anything.**

### Panel 3 — phenotype-driven prioritisation
A pathogenic *FGFR2* variant spiked into a public genome, with the six HPO terms of Pfeiffer
syndrome, **must rank *FGFR2* first.** Against the GIAB HG002 benchmark genome (4,096,123 variants,
649 genes scored) it ranks 1 at a 2.4× margin — and the margin is *phenotypic*, since the variant
scores of the top candidates are indistinguishable (1.0000 vs 0.9962).

### Panel 4 — contig naming (the cheapest and most-hit trap)
Assert that a variant your annotation returns a result for in one naming convention **also**
returns one in the other, or that the mismatch **errors**. It usually does neither.
**This trap was hit five times in a single day** across three different tools, and it never once
announced itself: SpliceAI's `grch38` annotation is Ensembl-named, our alignment reference is
UCSC-named, our VCF is Ensembl-named, and our depth artefacts are UCSC-named.

## Run it

```bash
python3 canary/run_canary.py           # all panels available on this machine
python3 canary/run_canary.py --splice  # panel 1 only
```

Exit code 0 = every assertion held. Non-zero = at least one tool is not doing what you think.

## Reuse

**CC BY 4.0.** Take it, extend it, disagree with the expectations. The panel matters less than the
habit: **before you believe a negative, make the instrument prove it can produce a positive.**

## Does this panel actually work?

A control set that has only ever passed is indistinguishable from one that *cannot fail* — the same
failure mode, turned on itself. So the panel tests itself:

```bash
python3 canary/run_canary.py --self-test
```

This reintroduces the **real** bug — the encoder patch that dropped its byte substitution — into a
throwaway copy of the splice runner and asserts the panel goes red. It does: **5 of 5 positive
controls fail**, loudly, where the broken tool had reported a clean "no splice signal" for five
canonical splice-site pathogenic variants.

**A canary that has never been shown to die is decoration.**
