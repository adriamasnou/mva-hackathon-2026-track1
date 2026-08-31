# The standard annotation toolchain: Ensembl VEP, run offline, and what it says about our own result

**One line:** we re-annotated the child's entire 313,417-variant rare callset with **Ensembl VEP
116.1 against a local offline GRCh38 cache**, proved nothing was dropped, proved the toolchain
answers correctly on two known variants, and then used it to **audit our own pre-registered scan**
— which it reproduces, corrects in two places, and moves *in our favour* without changing a single
one of the child's alleles.

The point of this document is not that we ran the field-standard tool. It is that **running it
was an opportunity to attack our own result, and we took it.**

---

## 1. Why this exists, and what we were doing before

The genome-wide recessive scan in `methods-and-self-critique.md` was annotated with
**`bcftools csq`** — a real, published, peer-reviewed consequence caller, and the honest choice at
the time, because Ensembl VEP's Perl API does not run on this machine. That limitation was stated
in our submitted Track 1 report rather than papered over.

It is also a genuine weakness. `bcftools csq` gives **consequence terms only**. It has no
pathogenicity predictors, no population frequencies, no ClinVar cross-reference, and no HGVS
nomenclature. Every one of those is standard in clinical variant interpretation, and their absence
shaped how our scan had to rank genes.

**This document closes that gap and then spends the new capability on ourselves.**

---

## 2. The run

| | |
|---|---|
| Tool | **Ensembl VEP 116.1** (`ensemblorg/ensembl-vep:release_116.1`) |
| Mode | `--cache --offline` — no network call, fully reproducible |
| Cache | `homo_sapiens/116_GRCh38`, 28 GB, mounted **read-only** |
| Assembly | GRCh38.p14 · GENCODE 50 · dbSNP 156 · **gnomAD v4.1** (e and g) · ClinVar 202509 · SIFT 6.2.1 · PolyPhen 2.2.3 |
| Input | the child's filtered rare callset, **313,417 variants** |
| Output | **433,168 annotation rows**, **313,417 distinct variants** |
| Command | `bash pipeline/vep_run.sh data/derived/rare_csq4.vcf.gz rare_csq4 --fork 6` |

**Why Docker, not the Perl API.** `Bio::DB::HTS::Tabix` will not load on this host — re-verified
while writing this document (`Can't locate Bio/DB/HTS/Tabix.pm in @INC`). Everything above it in
`Bio::EnsEMBL::IO` therefore fails. The container sidesteps the host's Perl entirely. We report the
route we actually used, not the one we wished we had.

**The command is committed, not just described.** An earlier version of this run existed as
`docker run` lines typed into a shell: the *result* was recorded and the *command* was not, which
makes a run **recoverable but not executable** by anyone else. `pipeline/vep_run.sh` closes that.

---

## 3. Proof that nothing was silently dropped

A cache-backed annotator's characteristic failure is **returning fewer rows quietly**, not
erroring. An exit code of 0 is not evidence. So the runner asserts count conservation and fails if
it breaks:

```
input:  313,417 variant lines
output: 433,168 rows, 313,417 distinct variants
✅ 313,417 in == 313,417 distinct out
```

(433,168 > 313,417 because `--pick_allele_gene` emits one row per allele **per gene**, and
overlapping genes are common.)

---

## 4. Proof that the annotation is *right*, not merely present

Count conservation cannot detect a cache or assembly mismatch, which returns a full-length file of
**wrong or empty** annotations without erroring. `pipeline/vep_check.py` is a known-answer control
on the child's two alleles. Every expected value was recorded in our own notes **before VEP was
ever run here**, so this is a control and not a tautology.

**[OUR MEASUREMENT]** — every cell below is read from our own VEP run this session and asserted by `python3 pipeline/vep_check.py pipeline/work/vep/rare_csq4.vep.tsv`, which exits non-zero if any of them changes.

| | allele A | allele B |
|---|---|---|
| Locus (GRCh38) | chr15:40,209,701 T>G | chr15:40,220,612 T>G |
| Transcript | ENST00000287598 (**canonical**) | ENST00000287598 (**canonical**) |
| Consequence | `stop_gained`, **HIGH** | `missense_variant`, MODERATE |
| Exon | **17 / 23** | **23 / 23** (last exon) |
| HGVS | `c.2210T>G` · `p.Leu737Ter` | `c.3006T>G` · `p.Asn1002Lys` |
| SIFT / PolyPhen | — (not applicable to a nonsense) | **deleterious (0.01)** / **probably damaging (0.997)** |
| dbSNP | rs759242053 | not catalogued |
| gnomAD v4.1 exomes / genomes | **7.867 × 10⁻⁵** / 3.286 × 10⁻⁵ | **VEP returns nothing — see §7** |
| ClinVar | **pathogenic, likely pathogenic** | no assertion for this nucleotide change |
| *provenance* | **[OUR MEASUREMENT]** · asserted by `pipeline/vep_check.py` | **[OUR MEASUREMENT]** · asserted by `pipeline/vep_check.py` |

Both controls hold. **The exon numbering is load-bearing for allele A, and the asymmetry is real —
but it is not an NMD asymmetry, and this passage stated it wrongly until 2026-08-31.**

- **Allele A — `p.Leu737Ter`, exon 17 of 23 — IS an NMD substrate.** It creates a premature
  termination codon **~748 nt and 6 exon–exon junctions upstream** of the final exon–exon junction,
  far beyond the 50–55 nt rule, so the transcript is predicted to be degraded. ⚠️ **Predicted, not
  measured** — no RNA was sequenced, and NMD efficiency cannot be derived from DNA.
- **Allele B — `p.Asn1002Lys` — is NOT an NMD substrate and never was.** A **missense creates no
  premature termination codon**, so the surveillance pathway is **never engaged** and the exon it
  falls in is **irrelevant to transcript stability**. The transcript is normal-length and translated.

> 🔴 **CORRECTED 2026-08-31 — CATEGORY ERROR.** This passage read: *"allele B is in the **last** exon
> and **escapes NMD**."* **A missense does not "escape" NMD; NMD is not applicable to it.** The
> last-exon fact is true and is useful elsewhere — it is why `p.Leu1012Pro`, the closest
> functionally characterised MVA allele, sits **29 bp away in the same exon** — but it does **no
> work** in the NMD argument, and presenting it as the reason allele B survives implies a mechanism
> that does not exist.
>
> ✅ **THE CONCLUSION IS UNCHANGED, and now rests on the right premise:** allele A's transcript is
> predicted to be degraded, and allele B's is a normal-length transcript that was never at risk —
> **so the residual BubR1 protein in this child is predicted to be N1002K.** The asymmetry is
> *"one allele is destroyed, the other is untouched"*, **not** *"both were at risk and one escaped"*.
>
> ⚠️ **And "the premise of everything downstream" was too strong** — it inherits allele A's
> prediction-not-measurement caveat, and Suijkerbuijk 2010 records that *"it is unclear what the
> status of 194X, 483X or 753X is in patient cells"*, i.e. **BUB1B truncations are not uniformly
> null once NMD is bypassed.** Stated as a prediction, not a premise.
>
> *How this was found: the error was surfaced by an internal field-intelligence sweep noting that a
> competitor had publicly withdrawn the identical formulation from their own report. **The
> correction here rests on the molecular biology and on our own allele-A analysis, not on their
> document** — per this project's standing rule that a claim sourced from a competitor repository is
> an observation about a competitor, never evidence about the biology.*

---

## 5. What VEP added that our previous annotator could not

**[OUR MEASUREMENT]** — the columns present in our own output header (`head -30 pipeline/work/vep/rare_csq4.vep.tsv`):
SIFT and PolyPhen scores · gnomAD exome and genome frequencies · ClinVar significance · dbSNP
identity · HGVS c. and p. nomenclature · canonical/MANE transcript flags · exon numbering.

All of it now sits on the child's whole callset, not on the two variants we already knew about.

---

## 6. Turning the new tool on ourselves

This is the part that matters. `python3 pipeline/vep_concordance.py` prints every number below.

### 6a. Do the two annotators agree?

All **1,015** damaging calls in the pre-registered scan matched a VEP record — **0 unmatched**.

**[OUR MEASUREMENT]**, `python3 pipeline/vep_concordance.py`, 2026-08-30:

| | |
|---|---|
| Identical Sequence Ontology term at VEP's canonical pick | **834 / 1,015 = 82.2%** |
| Scan says protein-altering, canonical pick does not | **181** |
| *provenance* | **[OUR MEASUREMENT]** · `pipeline/vep_concordance.py`, 2026-08-30 |

An 82% agreement is not a result on its own — it is a question. So we asked it.

### 6b. Why they differ — settled by experiment, not by argument

We re-ran **exactly those 181 variants** through VEP again with `--all-transcripts`
(`bash pipeline/vep_run.sh pipeline/work/vep/discordant.vcf disc --all-transcripts`), which
reports every transcript instead of one pick:

**[OUR MEASUREMENT]**, same tool, on the re-run output:

| | |
|---|---|
| Protein-altering on **at least one** transcript | **179 / 181 = 98.9%** |
| Protein-altering on the **canonical** transcript | **0 / 181 = 0.0%** |
| Protein-altering on **no transcript at all** | **2** |
| *provenance* | **[OUR MEASUREMENT]** · `pipeline/vep_concordance.py`, 2026-08-30 |

**[OUR MEASUREMENT] and the inference drawn from it.** **The discordance is not a disagreement about biology. It is a disagreement about which transcript
to report**, and it is now measured rather than assumed: `bcftools csq` reports the most severe
consequence across all transcripts; VEP with `--pick_allele_gene` uses a canonical-first pick
order. On this callset the two rules diverge on 17.8% of damaging calls, and in **every single
case** the scan's call was supported by *some* transcript.

The only two genuine disagreements are **PAPLN** and **ZNF302**, both of which VEP calls
`stop_retained_variant` — a stop codon changed to a different stop codon, which does not truncate
a protein. **Those two are our errors, and they are the correct kind of error to find: the scan
was too permissive, not too generous to our own candidate gene.**

### 6c. What the scan missed

**[OUR MEASUREMENT]**, `python3 pipeline/vep_concordance.py`. Running the comparison in the other direction: VEP's canonical picks contain **826** calls in the
three classes the pre-registration declared damaging (nonsense, frameshift, missense — `stop_lost`
and `start_lost` are out of scope *by design*, and counting them as misses would score the scan
against a rule it never adopted).

**824 of 826 were already in the scan — recall 99.8%.** Two were missed, and because "why not
100%?" is the right question to ask a recall figure, here is the whole answer.

| | FOXO6 | WWC3 |
|---|---|---|
| Locus | chr1:41,382,200 | chrX:10,015,674 |
| Change | **200 bp insertion** (not a multiple of 3) | **1 bp insertion** |
| VEP, canonical | `frameshift_variant` + `splice_acceptor_variant` | `frameshift_variant` |
| `bcftools csq` | `synonymous&splice_donor`, `splice_acceptor` | `synonymous&splice_donor`, `splice_region` |
| Zygosity | homozygous | homozygous |
| *provenance* | **[OUR MEASUREMENT]** · `BCSQ` read from the input VCF, VEP from our own run | same |

**Both misses are the same thing, and it is a rule we wrote down in advance, not a bug.** At a
splice junction the two annotators disagree about which consequence dominates: `bcftools csq`
reports the **splice** term and calls the coding half *synonymous*; VEP reports the **frameshift**.
The pre-registration lists exactly three damaging classes — nonsense, frameshift, missense — and
**explicitly excludes `splice_donor`/`splice_acceptor`**, with the reason recorded at the time:
adding splice later would be a post-hoc change. So the scan saw both variants, classified both,
and excluded both **by its own stated rule**. That is the pre-registration working, not failing.

It is still a real limitation, so we bound it. Both variants are homozygous, and the pre-registered
recessive model qualifies a gene on a single homozygous damaging allele — so had they been counted,
each would have added a gene. We recomputed the ranking with both inserted as homozygous
frameshifts: **230 genes → 232, and *BUB1B* stays at rank 55.** FOXO6 and WWC3 land at 79 and 80,
below *BUB1B*, because the first sort key is truncating-allele count and the second is total
damaging count, on which they score 1/1 against *BUB1B*'s 1/2. **[OUR MEASUREMENT]**, 2026-08-30.

**A frame-shifting 200 bp insertion called synonymous is worth saying out loud**, whatever the
splice-junction context. And rather than leave it there, §6d runs the scan **with splice counted
as damaging** — rule B — so the excluded class is measured rather than merely disclosed. It costs
us four rank places, and it is reported anyway.

### 6d. Does the answer depend on the two choices we made before running? — four rules, side by side

Two choices were fixed before the scan ran: **which annotator**, and **whether splice consequences
count as damaging**. The pre-registration excluded splice deliberately, and §6c showed that
exclusion has a cost. So we measured both choices instead of arguing about them —
`python3 pipeline/scan_sensitivity.py`.

**Rebuilt from the callset, not from the scan's own output.** The scan's variant table holds only
what it already called damaging, so any re-ranking built on it can drop a gene but never add one —
one-sided in exactly the direction that matters here. This rebuild reads all **313,417** variants
with their genotypes and both annotators' calls. **Rule A reproduces the published 230 genes and
*BUB1B* rank 55 exactly**, which is the acid test that the rebuild is faithful; the tool refuses to
report the other three arms if it fails. *(An earlier draft of this document said "187 genes" for
rule C. That figure came from the one-sided route and is superseded by the 184 below.)*

| rule | annotator | splice damaging? | qualifying genes | *BUB1B* | its own alleles |
|---|---|---|---|---|---|
| **A** | `bcftools csq` | no — **AS PRE-REGISTERED** | **230** | **rank 55** | 1 truncating / 2 damaging |
| B | `bcftools csq` | **yes** (post-hoc) | 239 | rank **59** | 1 / 2 |
| C | VEP canonical | no (post-hoc) | 184 | rank **42** | 1 / 2 |
| D | VEP canonical | **yes** (post-hoc) | 191 | rank **43** | 1 / 2 |
| *provenance* | **[OUR MEASUREMENT]** | 2026-08-30 | `pipeline/scan_sensitivity.py` | acid test passed | |

🔴 **A is the result. B, C and D are declared post-hoc arms and must never be quoted as if they
were the pre-registered finding.** A post-hoc rule change that improves your own candidate is the
most suspect move available in this kind of analysis, which is why all four are printed together —
including when they help.

**Three things this settles.**

**[OUR MEASUREMENT]. First, the rule change we were tempted to make would have made us look
WORSE, not better.** Counting splice as damaging moves *BUB1B* from 55/230 to **59/239** under the
pre-registered annotator, and from 42/184 to 43/191 under VEP. The pre-registered exclusion was
not a choice that flattered our own candidate — and now we can say that with a number instead of
an assurance. **Rule B is the honest home for the FOXO6 and WWC3 misses in §6c**: including them
costs us four places, and we are reporting it anyway.

**[OUR MEASUREMENT]. Second, *BUB1B*'s own evidence is invariant.** One truncating allele, two
damaging alleles, both heterozygous — **identical under all four rules**. Every movement in the
table is other genes entering or leaving the list around it. We did not gain a candidate under any
arm; the field around it thinned or thickened.

**[OUR MEASUREMENT]. Third, and we would rather say it than have it found: `rank 55` is not a
measurement.** Nine genes are tied with *BUB1B* on both severity keys, at ranks **53–61**. Within
that block, **seven — VPS41, IGHV8-51-1, *BUB1B*, TUBB8B, PSG1, LILRB4, LBP — are tied on all
three pre-registered sort keys**, every one at mean GQ 99.0. *BUB1B*'s position among those seven
is decided by **nothing the pre-registration specifies**, and the same is true in every other arm
(9 tied under B, 6 under C and D).

**The honest unit is the tie block, not the rank.** The scan's real claim is *"an unbiased,
phenotype-blind recessive model puts BUB1B in the top ~20–25% of candidate genes with no prior
knowledge of MVA"* — true under **all four rules** — and **not** *"BUB1B ranked 55th"*, which
implies a precision the sort keys do not carry. `methods-and-self-critique.md` has been corrected
to say so.

---

## 7. Limitations, stated plainly

1. **🔴 VEP returning nothing for allele B's frequency is NOT a measurement of absence.** VEP's
   gnomAD columns are empty for `chr15:40,220,612 T>G`. That means *this nucleotide substitution
   is not in the annotation source as queried* — it does **not** mean the allele is absent from
   gnomAD. A direct gnomAD v4.1 lookup returns **AC = 1, AN = 1,461,878, AF = 6.84 × 10⁻⁷** (gnomAD v4.1, https://gnomad.broadinstitute.org — recorded in our own `track2-verified-claims.md`).
   Both alleles are therefore ultra-rare rather than absent; ACMG **PM2** ("absent *or* at
   extremely low frequency") holds for both, and no classification moves. We record this
   prominently because we made exactly this error once, in the other direction, and a competing
   team has published a self-correction for the same mistake on the same variant.
2. **ClinVar's silence on allele B is allele-level and correct.** ClinVar holds
   `NM_001211.6(BUB1B):c.3006T>A (p.Asn1002Lys)` — the same protein change by a **different**
   nucleotide substitution. The child's `T>G` is the novel part. Protein-level novelty and
   nucleotide-level novelty are different claims and we keep them apart.
3. **No plugins were run.** This run has SIFT, PolyPhen and gnomAD, but **no CADD, REVEL,
   AlphaMissense or SpliceAI plugin layer**. Splice prediction is reported separately in
   `splice-prediction.md` (SpliceAI 1.3.1, run locally). Where this document says "VEP says
   nothing", it means only that.
4. **`--pick_allele_gene` is one row per allele per gene, not per transcript.** Every canonical-pick
   number in §6 inherits VEP's pick order. §6b exists precisely because that choice is
   consequential, and it quantifies how consequential.
5. **The sensitivity analysis in §6d is one-sided by construction.** It reclassifies the variants
   the pre-registered scan already carried; it cannot add a gene the scan never saw. §6c bounds
   that gap at two variants.
6. **Single sample, no parents.** Nothing here establishes phase. Our phase claim is *inferred*,
   and is reported as inferred everywhere it appears.
7. **Pinned versions.** Cache release 116 with image `release_116.1`; a different pairing will
   produce different `Existing_variation` and frequency columns. The runner asserts the match.

---

## 8. Reproducing all of it

```bash
bash pipeline/vep_run.sh data/derived/rare_csq4.vcf.gz rare_csq4 --fork 6   # annotate + prove nothing was dropped
python3 pipeline/vep_check.py pipeline/work/vep/rare_csq4.vep.tsv           # known-answer control
python3 pipeline/vep_concordance.py --emit-discordant                       # extract the discordant set
bash pipeline/vep_run.sh pipeline/work/vep/discordant.vcf disc --all-transcripts
python3 pipeline/vep_concordance.py                                         # every number in §6
```

Requires Docker and the GRCh38 release-116 VEP cache. **Every VEP output stays in
`pipeline/work/vep/`, which is gitignored and never enters this repository** — this document
reports counts, gene symbols and two already-public variants, which are findings, not the dataset.
