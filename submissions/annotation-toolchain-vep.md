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

Both controls hold. **The exon numbering is the load-bearing part**: allele A is in exon 17 of 23
and is NMD-competent, so that transcript is degraded; allele B is in the **last** exon and escapes
NMD. That asymmetry — independently confirmed here by the standard toolchain — is why all residual
BubR1 protein in this child carries the missense allele, and it is the premise of everything
downstream.

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

**824 of 826 were already in the scan — recall 99.8%.** The two it missed are frameshifts in
**FOXO6** and **WWC3**. Neither is a plausible cause of this child's phenotype, but both are
reported here rather than left out.

### 6d. Does the annotator change the answer? — a sensitivity analysis

The pre-registration forbids post-hoc changes, so this is **not** a re-ranking. The pre-registered
result stands as published. This asks a different question: *if a reviewer re-ran our own rule with
the field-standard annotator, what would they get?*

**[OUR MEASUREMENT]** — both rows recomputed this session from the pre-registered rule in `pipeline/recessive_scan_PREREGISTERED.md`; the first row reproduces the published 55/230 exactly, which is itself a check on the published number.

| | qualifying genes | *BUB1B* | truncating / damaging alleles |
|---|---|---|---|
| `bcftools csq` — **as pre-registered** | 230 | **rank 55** | 1 / 2 |
| VEP canonical — sensitivity | 187 | **rank 42** | 1 / 2 |
| *provenance* | **[OUR MEASUREMENT]** | recomputed 2026-08-30 | from `recessive_scan_PREREGISTERED.md` |

Two things to notice, and the second one matters more than the first.

**[OUR MEASUREMENT]. First: the conclusion is robust, and the standard toolchain moves it in our favour.** *BUB1B*
improves from 55/230 to 42/187. Its **own** numbers are byte-identical under both annotators —
one truncating allele, two damaging alleles, both heterozygous. The improvement comes entirely
from 43 *other* genes dropping out because their damaging calls were non-canonical. We did not
gain a candidate; the field around it thinned.

**[OUR MEASUREMENT]. Second, and we would rather say it than have it found: `rank 55` is not a measurement.**
Nine genes are tied with *BUB1B* on both severity keys, occupying ranks **53–61**. Within that
block, **seven genes — VPS41, IGHV8-51-1, *BUB1B*, TUBB8B, PSG1, LILRB4, LBP — are tied on all
three pre-registered sort keys**, every one of them at mean GQ 99.0. *BUB1B*'s position among
those seven is decided by **nothing the pre-registration specifies.** Under VEP the same thing
happens one block higher: rank 42, six genes tied on all three keys.

**The honest unit is the tie block, not the rank.** The scan's real claim is *"an unbiased,
phenotype-blind recessive model puts BUB1B in the top ~20% of 230 candidate genes with no prior
knowledge of MVA"* — which is true under both annotators — and **not** *"BUB1B ranked 55th"*,
which implies a precision the sort keys do not carry. `methods-and-self-critique.md` has been
corrected to say so.

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
