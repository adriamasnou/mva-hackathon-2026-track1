# Track 2 — MVA Hackathon 2026

**Status: DRAFT IN PROGRESS. NOT FOR SUBMISSION.**
Track 2 is **one shot with no resubmit**. Nothing here ships without Adrià's explicit go-ahead
(`CLAUDE.md` RED #1). Report v2 structure started 2026-09-01.

**Rubric this is written against:** Rigor 35 · Impact 25 · Innovation 25 · Scalability 15.

> **Reading note.** This report is **self-contained**: every claim it makes is stated and sourced
> here, and the companion documents in this directory are corroboration, not prerequisites. A judge
> who reads only §0 should be able to retell the argument; a judge who reads only this file should
> be able to score all four axes.

---

## §0. The answer, in one page

**The child.** Mosaic variegated aneuploidy syndrome 1 (MVA1; OMIM 257300), caused by compound
heterozygous *BUB1B*: **c.2210T>G p.(Leu737\*)** — nonsense, exon 17 of 23 — in trans with
**c.3006T>G p.(Asn1002Lys)**, a missense in the C-terminal pseudokinase domain. This is exactly the
canonical MVA1 allele architecture: a truncating allele combined with a kinase-domain missense
(**PMID 15475955**; **PMID 20516114**; **PMID 31738183**).

**The mechanism, in one sentence.** Truncating *BUB1B* alleles produce no detectable protein —
transcripts are cleared by nonsense-mediated decay (**PMID 20516114**, demonstrated for 386X and
731X, which flank residue 737; *the inference to L737\* is by analogy and has not been tested for
this allele*) — so **every BubR1 molecule in this child is N1002K**, and the disease is driven by
**low overall BUBR1 abundance** (**PMID 20516114**, the authors' own conclusion).

**The therapeutic window is known, and it is small.** In the primary data, reducing BUBR1 to **~6%**
of wild-type caused missegregation in the majority of cells, while **~13%** left segregation fidelity
*"virtually"* unaffected (**PMID 20516114**, Fig 4D). **The required correction is roughly two-fold,
not ten-fold** — which is what makes this a tractable target rather than a gene-therapy problem.

**So the mechanism-matched answer is a CLASS, not a molecule: cytosolic protein stabilisation** —
raise the abundance of the mutant protein above the threshold. Direct proof of principle exists for
exactly this move: forced overexpression of two destabilised kinase-domain mutants (I909T, L1012P —
the latter **ten residues** from this child's) **fully restored** checkpoint function (**PMID
20516114**), and a destabilising ATP-pocket mutant was rescued by nothing more than folding it at a
lower temperature (**PMID 22698286**).

**And the class is not verified for this child, because it rests on one untested premise.** A
pseudokinase-domain missense can be pathogenic two ways: by destabilising the fold (treatable by
raising abundance) or by breaking the PP2A-B56/KARD scaffolding function while the fold stays intact
(**PMID 33207204**), in which case raising abundance achieves nothing. **Q921H is the published
counter-example** — a kinase-domain-adjacent missense with wild-type protein levels (**PMID
20516114**). **N1002K has never been measured by anyone**: no functional study, no ClinVar
expert review, and no construct catalogued in Coriell or Addgene.

**Every molecule currently named for this genotype fails against it, for reasons we read out of the
primary literature** — rapamycin (**PMID 23602569**, **PMID 41820377**), NAD⁺ precursors (**PMID
24825348**, **PMID 38009412**, **PMID 36371959**), Aurora-B modulation (**PMID 16950108**), low-dose
taxol (**PMID 24670687**), senolytics (**PMID 25754370**), metformin (**PMID 35568294**), ER chemical
chaperones, proteasome inhibition, and HSP90 inhibitors, which are **relatively contraindicated here**
(**PMID 20516114**). **Each kill is stated with its own source in §2.1.** That kill list is not a
refusal; it is the result. **[OUR INFERENCE — the assembly of these results into a per-genotype
exclusion is ours; every individual result is the cited paper's.]**

**The ask.** One measurement decides which branch this child is on, and therefore whether the entire
class applies: **express WT and N1002K pseudokinase domain side by side and measure abundance and
thermal stability.** Four sequence-verified constructs including two controls, **≈ $630** at
published list prices, **~3 weeks** elapsed and ~4 days hands-on. The construct does not exist
anywhere; **the orderable sequences are printed** in `n1002k-reagent-specification.md` and the
protocol is written to *Nature Protocols* structure in `n1002k-collaboration-package.md`.

> **The sentence this submission is asking to be judged on:**
> *They identified the class the mechanism actually implies, killed every named molecule with
> measurements rather than opinion, published their own kill rate, and specified — to the base pair
> and the dollar — the one experiment that decides whether the class applies to this child.*

---

## §1. Mechanism — Rigor

### 1.1 The genotype, and why the null allele matters more than it looks

| allele | consequence | status |
|---|---|---|
| `c.2210T>G` **p.(Leu737\*)** | nonsense, exon 17 of 23 | **functionally null** — presumed NMD-competent |
| `c.3006T>G` **p.(Asn1002Lys)** | missense, pseudokinase domain (aa 721–1,044) | **the child's only source of BubR1** |

Complete BubR1 loss is embryonic lethal — mouse `BubR1^-/-` and `BubR1^H/-` are lethal, while
`BubR1^H/H` at ~10% of wild-type protein is viable (**PMID 15208629**; **PMID 31738183**). An MVA1
patient therefore *requires* one allele that makes some protein. **That allele is N1002K, and it is
the whole therapeutic surface.**

⚠️ **Stated limit.** NMD was not tested for `L737*` itself. The evidence is that 386X, 731X and
753X are undetectable in patient and parental lysates and appear only when NMD is bypassed by
plasmid-driven expression (**PMID 20516114**). **731X and 753X flank residue 737** — a strong but
indirect analogy, and it is stated as one.

### 1.2 What the pseudokinase domain actually does — and what N1002K could break

Human BUBR1 retains a catalytic triad but **putative catalysis is dispensable for error-free
chromosome segregation**; the ATP-pocket residues are required for *conformational stability*
instead (**PMID 22698286**). So **no argument here depends on N1002K abolishing catalysis**, and
none is made.

What the domain does do is non-catalytic and essential: it **promotes kinetochore PP2A-B56
recruitment, checkpoint silencing and chromosome alignment**, and mutating or removing it produces
alignment errors through an Aurora-B activity imbalance (**PMID 33207204**).

> 🔑 **This is the fork the whole therapeutic argument turns on**, and it is §0's untested premise:
> **abundance** (destabilised fold → less protein → raise it) versus **function** (fold intact →
> scaffolding broken → raising it changes nothing).
> **[OUR INFERENCE — the two-branch framing is ours, drawn from the two published mechanisms above.
> Which branch N1002K sits on is unmeasured.]**

### 1.3 Why "abundance" is the better-supported branch — and why that is still not enough

**Supporting it.** Kinase-domain substitutions in this gene destabilise: patient mutants show a
**5–10 fold decrease** in protein level, are HSP90-dependent, are cleared by the proteasome, and
turn over about twice as fast; two substitutions *away* from the kinase domain (Y155C, R550Q) do
**not** affect protein levels (**PMID 20516114**). Patient lines show **low overall BUBR1
abundance**, and ectopic BUBR1 **restored checkpoint activity** (**PMID 20516114**). Raising BubR1
is target-validated in vivo, though by transgene rather than by drug (**PMID 23242215**), and
independently by a progerin-blocking peptide that rescued BUBR1 and extended median lifespan 17% in
`Lmna^G609G/G609G` mice (**PMID 37118121**).

**Against it, and we state it rather than wait for a reviewer to.** `BubR1^H/L1002P` and `BubR1^H/H`
mice have **comparable BUBR1 levels but divergent phenotype severity** — the paper's own title is
*"BubR1 allelic effects drive phenotypic heterogeneity"* (**PMID 31738183**). **Amount is not
identity.** And **Q921H** destabilises nothing at all (**PMID 20516114**), which is precisely why
the branch must be *measured* for N1002K rather than assumed.

⚠️ **Numbering trap, stated so it cannot propagate.** The mouse allele in **PMID 31738183** is
`BubR1^L1002P`, which models **human L1012P** (offset of 10). This child's variant is **human
N1002K** — a different residue entirely.

### 1.4 What is known about this exact variant: almost nothing, and that is checkable

| source | result |
|---|---|
| published literature (PubMed, Europe PMC, OMIM, UniProt, LOVD) | **no functional or clinical data on p.Asn1002Lys** |
| UniProt O60566 natural variants | 13 listed; **none at residue 1002** |
| ClinVar | **c.3006T>G is absent.** `c.3006T>A` — same protein change — is VariationID **4600147**, **VUS, 1 star**, sole submitter, logged under *"Inborn genetic diseases"*, not MVA |
| gnomAD v4.1 `15-40220612-T-G` | **AC 1 / AN 1,461,878 · AF 6.84 × 10⁻⁷**, 0 homozygotes |
| in-silico | AlphaMissense 0.923 vs REVEL 0.472 — **they disagree**, and AlphaMissense mis-calls 2 of 4 proven MVA alleles as Benign/Ambiguous |
| provenance of every row above | **[OUR MEASUREMENT — ClinVar, gnomAD v4.1, UniProt O60566 and LOVD queried directly 2026-08-29 with the query strings recorded in `dossier/sweeps/clinvar-bub1b-2026-08-29.md`; public gene-level queries only, no patient data transmitted]** |

**[OUR MEASUREMENT — ClinVar/gnomAD/UniProt/LOVD queried directly with the query strings recorded in
`dossier/sweeps/clinvar-bub1b-2026-08-29.md`; public gene-level queries only, no patient data
transmitted.]**

**Do not write "N1002K is in ClinVar" without the T>A/T>G distinction and the 1-star VUS status.**
We nearly did.

---

## §2. The class, the gate, and why every named molecule fails it — Rigor

**This is the section that answers the brief.** The rubric asks whether a proposed repurposing
candidate is well-supported by the mechanism. Our answer is: **the mechanism supports a class
(cytosolic protein stabilisation) and a gate (is N1002K destabilising?), and it excludes every
individual molecule now being named for this child — each for a specific, cited reason.**

### 2.1 The kill table

| candidate | why it fails **for this genotype** | source |
|---|---|---|
| **Rapamycin / sirolimus** | The only in-vivo test in the flagship model was **negative**: BubR1 progeroid mice on dietary rapamycin *"developed age-related phenotypes at similar rates as mice on a control diet"* — reported by the lab that built the model, and uncontradicted since 2013. The mTORC1 evidence behind the idea is **one tissue, one *heterozygous* allele, explicitly correlative** — and the authors do not propose mTOR inhibition as a therapy. The 2026 *Drosophila* MVA model **did** rescue aneuploid neuroblast number with oral rapamycin — and **failed on brain size and neuronal output**, the organ-level endpoints. Label: **not established <13 y**, with a **boxed warning for malignancy** in a child whose syndrome already carries a high childhood-cancer risk | **Baker 2013** (**PMID 23602569**, preliminary unpublished data cited in a peer-reviewed paper) · **Sieben 2020** (**PMID 31738183**) · **González-Blanco 2026** (**PMID 41820377**) · Rapamune label rev. 10/2024 §8.4 |
| **NAD⁺ precursors (NR / NMN — the "niacin axis")** | The famous lifespan result is a **SIRT2 transgene, not a drug** (+58% median, male-driven); **NMN was never given to a BubR1 mouse**, and no NAD⁺ precursor has ever been administered to any MVA model. **NR has never been shown to raise BubR1.** The SIRT2 longevity effect **failed replication in the same transgenic line** by the original group. And there is an unresolved **oncological signal**: dietary NR at a human-equivalent dose comparable to the paediatric precedent was associated with **brain metastases in 9 of 11 animals versus 3 of 12** — counts verbatim from the paper, which **reports no p-value for them and runs no Fisher test**; two-tailed Fisher on its own counts gives ***p* = 0.012 [OUR MEASUREMENT, 2026-09-01]** | **North 2014** (**PMID 24825348**) · **Wu 2023** (**PMID 38009412**) · **Maric 2023** (**PMID 36371959**) |
| **Aurora-B modulation** | **Wrong direction of effect.** Partial Aurora inhibition at a dose with little effect on other endpoints *increased* merotelic attachments and lagging chromosomes — it is a validated method for *inducing* missegregation. No Aurora inhibitor is approved for any indication | **Cimini 2006** (**PMID 16950108**) |
| **Low-dose taxol** | Same failure mode: at clinically achievable 5–50 nM it causes missegregation on multipolar spindles — that *is* its anticancer mechanism | **Zasadil 2014** (**PMID 24670687**) |
| **Senolytics** | The BubR1 result everyone cites is a **transgene** (INK-ATTAC + a synthetic dimeriser with no clinical status), **lifespan was not extended**, and in the **late-life** arm — the arm matching a child who has already had a sarcoma — *"cataracts … remained unchanged"* and the gains *"reflect attenuated progression … rather than a reversal"*. Real senolytic drugs have **never been tested in BubR1 mice**; dasatinib carries growth-plate effects in children | **Baker 2011**, *Nature* (**PMID 22048312**) for the transgene · **Zhu 2015**, *Aging Cell* (**PMID 25754370**) for the senolytic drugs |
| **HSP90 inhibitors** | 🔴 **Not a candidate — a contraindication.** HSP90 inhibition *"severely decreased"* mutant BubR1 while barely touching wild-type. In a child whose only BubR1 is a chaperone-dependent mutant, this class should be regarded as **relatively contraindicated** | **PMID 20516114** |
| **Fisetin (OTC senolytic supplement)** | 🔴 **Not a candidate — a contraindication, and the only one here needing no prescriber.** At 30 µM in dividing human cells, fisetin cut **kinetochore BubR1 by 94%** (P < 0.001) with the structural marker Hec1 down just 4% — selective removal, not kinetochore collapse — and forced **86% (n = 42)** of prophase/prometaphase cells out of mitosis *"despite the presence of unaligned chromosomes"*. **That is this child's lesion, reproduced pharmacologically.** The authors themselves write that *"precaution should be taken when using nutritional supplements rich with fisetin"*. 🔴 **Bounded honestly: no pharmacokinetics in the source, dietary intake ≈0.4 mg/day against 30 µM in the dish, supplement content unquantified — a mechanistic contraindication with an UNMEASURED human exposure, not a demonstrated clinical hazard. Specific to fisetin; quercetin and dasatinib were not tested.** | **PMID 19395653** |
| **Metformin** | **No evidence** of any link to BubR1, the SAC or missegregation. The nearest literature is radiation clastogenesis — the wrong lesion — and high-dose metformin is itself genotoxic under low glucose | **Cheki 2016** (**PMID 27692296**) · **Lyu 2022** (**PMID 35568294**) |
| **ER chemical chaperones (4-PBA, TUDCA)** | **Excluded by compartment.** Chaperone systems are compartment-specific and BubR1 is a soluble cytosolic/nuclear protein cleared by the ubiquitin–proteasome system; 4-PBA's successes are in secretory/trafficking clients. A drug that corrects folding in the ER cannot correct a misfolded cytosolic protein | **[OUR INFERENCE — the compartment filter is ours; the compartment assignments are published]** |
| **Proteasome inhibition** | Mechanistically coherent (MG132 preserved mutant BubR1) and a **non-starter** as chronic therapy in a proliferating child | **PMID 20516114** |
| **Antioxidants / NAC** | No antioxidant has been tested in BubR1-hypomorphic mice. What is published is the **vulnerability**, not the rescue | **PMID 27815460** |

### 2.2 What survives: the class, and the one drug that is compartment-matched

The filter that kills the list also names what is left. **Cytosolic proteostasis is the only
compartment-matched axis** — BubR1 is a soluble cytosolic/nuclear protein whose mutant forms are
HSP90-dependent and proteasome-cleared (**PMID 20516114**) — and **arimoclomol** (HSF1/HSP70 axis,
approved Sept 2024, paediatric ≥2 y) is the molecule that sits in it. **[OUR INFERENCE — the
compartment filter and its application to this candidate list are ours; the compartment assignments
and the chaperone-dependence are published.]**

**We do not claim arimoclomol as our idea, and we measured that we cannot.** It appears in the
archived repositories of multiple competing teams, at least one of which ranks it first. **What we
add is the filter, the gate, and one piece of arithmetic nobody else states:**

> **Target engagement here may be unreadable.** The only human measurement of this drug hitting its
> target — PBMC HSP70 over 12 months in **Mengel et al.**'s Niemann-Pick C trial — reports **mean +1778.98 pg/mL
> with SD 1835.56** (n = 11, within-group Wilcoxon; the placebo arm was unusable because samples
> were lost). **CV = 103.2%.** **[OUR MEASUREMENT — arithmetic on the two values published by
> **Mengel et al.**, **PMID 34418116**.]** An experiment whose engagement marker did not move is therefore
> **uninterpretable, not negative** — and a gate calibrated from that trial at n = 3 would convert a
> technical failure into a false negative.

Three design consequences follow, and they apply to anyone in this field, not only to us: blot
BubR1 in the same lysate as **HSPA1A/HSP90AA1**; pre-specify the minimum detectable induction from
the **cell system's own CV**, never from the trial's; and **never normalise to GAPDH or tubulin** in
arms where HSF1 activation perturbs housekeeping proteins — the effects at stake are 20–40%.

### 2.3 Why the honest answer is the strong one

Every entry proposing a molecule on the abundance axis — including the strongest ones — is assuming
that N1002K is a destabilising allele. **That has never been measured, in this child or in anyone.**
If it is wrong, every abundance-raising proposal in this hackathon is aimed at a protein that is
present and broken rather than absent and rescuable.

**We are not asking the panel to accept a molecule. We are asking it to notice that the question
in front of the molecule is unanswered, and that answering it costs $630 and three weeks.**

### 2.4 The kill rate, published

Our literature mining ran as orchestrated subagent roles with **adversarial verifier nodes that have
no stake in the claim and are instructed to refute it**. Of **93** allegations put through that
stage, **78 were refuted and 15 survived — an 83.9% kill rate.**
**[OUR MEASUREMENT — recomputed 2026-08-31 from the three committed run JSONs, not quoted from the
reports: `dossier/sweeps/pool1-mining-2026-08-31.json`, `pool1-verify38-2026-08-31.json`,
`pool2-mining-2026-08-31.json`.]**

Separately, all **91** `NEW_NUMBER` leads — the class that asserts figures — were checked verbatim
against the primaries with a control confirming the matcher rejects the same quote with one digit
changed: **91 of 91 faithful, 0 fabricated.**

> 🔑 **Transcription fidelity and allegation validity are different quantities. The quotes are real;
> the inferences drawn from them are usually wrong.** Two of the fifteen survivors were defects in
> our own judge-visible material that no automated gate we hold could see — including the
> oncological signal against the compound we had been leading with, which we already held and had
> never cited (**PMID 36371959**).

⚠️ **The remaining 268 findings have had no adversarial pass on their substance** (177 have since
been adjudicated on substance; the other 91 are exactly the `NEW_NUMBER` class above). **Nothing in
this submission rests on an unadjudicated lead.**

---

## §3. The one experiment that changes the answer

**The gate:** express the BubR1 pseudokinase domain (aa 721–1,044) as WT and N1002K side by side,
and measure **abundance and thermal stability**. Destabilised → the class applies and the child's
disease is a dosage problem. Indistinguishable from WT → the abundance thesis is dead for this
child, every abundance-raising proposal in this competition is aimed at the wrong branch, and the
target becomes the PP2A-B56 scaffolding function instead.

| | |
|---|---|
| **what does not exist** | **no N1002K construct is catalogued in Coriell or Addgene** — both queried record by record. *(ECACC returned nothing parseable and is recorded as inconclusive, not negative.)* |
| **the edit, verified at sequence level** | `chr15:40,220,612 T>G` (GRCh38) · `c.3006T>G` · codon 1002 `AAT` → `AAG` · fragment 721–1,044 = **972 bp / 324 codons** · WT vs mutant differ at **exactly one position**, fragment position 846, no internal stop in either **[OUR MEASUREMENT — re-derived 2026-08-31 from the Ensembl CDS `ENST00000287598.11` and the GRCh38 reference FASTA; not taken from any annotation]** |
| **constructs** | **four, not two** — WT, N1002K, and two controls. A two-construct design fails the standard the protocol itself cites |
| **cost** | **≈ $630** at published list prices, itemised and dated |
| **time** | **~3 weeks** elapsed, ~4 days hands-on |
| **status** | *(external-engagement line — to be completed by the author before submission; it is deliberately left blank rather than implied)* |

The full build specification, with both 972 bp sequences printed and every price dated, is
`n1002k-reagent-specification.md`. The bench protocol, written to *Nature Protocols* structure with
timing, critical steps and a troubleshooting table, is `n1002k-collaboration-package.md`.

---

## §4. What we built that others can run — Innovation · Scalability

| artifact | what it is | why it is portable |
|---|---|---|
| **The canary panel** (`canary/`) | a positive-control set for the *interpretation* layer of a rare-disease pipeline | Bioinformatics tools **fail closed** — they return "nothing found". In one day on this genome we hit five silent failures, none of which threw an exception. The panel tests whether your pipeline is running at all |
| **The HFEA gene ↔ condition crosswalk** | 2,063 approved-condition rows joined to genes, published as CSV/JSON | The regulator's own register has **no gene column**. Anyone can now query it by gene |
| **The pipeline, on a genome that is not this child's** | GIAB HG002, public, **4,096,123 variants**, one *FGFR2* variant spiked in — **ranked first at 0.9654** | Generalisation demonstrated on public data rather than claimed |
| **The mining harness and its kill rate** | miner nodes → adversarial verifier nodes → adjudication, with typed findings and verbatim quotes | The harness is not novel and we do not claim it is. **The published kill rate is** (§2.4) |

---

## §5. Impact

**1. Embryo testing for this exact condition is already approved in the UK — and cannot be found.**
MVA1 (OMIM 257300) is on the HFEA's approved PGT-M list, alongside MVA2, MVA3, MVA5 and MVA6.
The register's columns are *condition name*, *status* and *OMIM number*: **there is no gene column,
and `BUB1B` appears in none of the 2,063 rows.** A clinician or family searching the way genetics is
actually practised — by gene — is told it does not exist. **[OUR MEASUREMENT — HFEA workbook,
2026-08-05 snapshot, 2,063 rows, parsed directly; corroborated for this condition by the regulator's
Statutory Approvals Committee minutes of 26 January 2026, applicant Aria Fertility (centre 0382),
<https://ifqlive.blob.core.windows.net/inspectiondocuments/8623.pdf>.]**
⚠️ Approval is not eligibility: HFEA criteria require a ≥10% risk of an affected pregnancy, NHS
Clinical Genetics referral and prior counselling. **Whether any individual family qualifies is a
clinical determination we do not make.**

**2. The discoverability failure is systemic, not anecdotal.** Across the whole register:
**1,688 of the 1,778 genes behind approved conditions — 94.9% — are invisible to a gene search**,
and **1,850 of all 2,063 approved conditions (89.7%) have no expert-curated variant in any causative
gene**. **[OUR MEASUREMENT — `register-audit.md`, full method and reconciliation there.]**

**3. A "Definitive" gene with zero expert-reviewed variants and no expert panel.** *BUB1B* holds
**2,493** ClinVar records and **1,426** unique missense VUS (bulk `variant_summary`, deduplicated on
`VariationID`), of which **0** are reviewed by an expert panel — and **no ClinGen VCEP exists for
the gene**. Restricted to the pseudokinase domain the assay targets: **430 uncertain missense
variants, again zero expert-reviewed.** This child's second allele sits in that bucket **not because
the evidence was weighed and found wanting, but because no mechanism exists to weigh it.**

**4. And the fix is measurable.** Under ClinGen's `OddsPath` framework (**PMID 31892348**) the
attainable evidence strength is governed by the number of **benign** controls. For *BUB1B*:
**35 benign ≥1★ gene-wide → `PS3` (strong)**, but **10 in the pseudokinase domain alone →
`PS3_moderate`**. **Whether a functional assay for this gene can deliver strong or only moderate
evidence turns entirely on whether benign controls from outside the assayed domain are admissible**
— exactly the judgement a VCEP exists to make, and for *BUB1B* there is none.
⚠️ **We do not assert which scoping is correct**; both numbers are reported so the choice is visible.

**5. Written for the family, not only for judges.** A decision aid built to **IPDAS**, including a
declaration of the criteria it **fails**; a family-facing summary carrying the same caveats as this
report — **including the oncological signal against the compound we had been leading with**; and a
reusable **CC BY 4.0** secondary-findings disclosure protocol for open single-patient challenges.

---

## §6. Limits — ours, stated before a reviewer extracts them

1. **We do not have a therapy, and nothing here will produce one for this child in this timeframe.**
   Our own odds that a screen yields any compound raising BubR1 two-fold are **25–40%**, and **well
   under 10%** that anything reaches a child. **[ESTIMATE — both figures are ours; no *BUB1B*-specific
   prior exists because no screen has been run.]**
2. **The central premise is untested.** Whether N1002K destabilises is the question §3 exists to
   answer, not something this report establishes.
3. **Amount is not identity.** Even on the abundance branch, `BubR1^H/L1002P` versus `BubR1^H/H`
   shows comparable protein levels with divergent severity (**PMID 31738183**).
4. **The NMD inference for `L737*` is by analogy**, not by measurement on this allele (§1.1).
5. **A verifier that shares the miner's blind spot cannot see it.** Verifier nodes run on the same
   model family as the miners; the independence is of *stake and context*, not of architecture.
   **[OUR INFERENCE — stated as a limitation, not measured.]**
6. **Every "no competitor has X" claim is bounded by what we could see.** Repositories may stay
   private until the close, so such statements are about **the repositories we archived on a stated
   date**, never about the field.

### What we stopped claiming

**The strongest thing in this submission is the list of things we withdrew on evidence.**

| withdrawn | why |
|---|---|
| **the ClinVar submission itself** | three of the four ACMG criteria we had claimed do not hold — `PM3` needs parental phase we do not have, `PP4` fails because MVA has ≥8 genetic causes, `PP3` is inadmissible because our in-silico predictors disagree (REVEL 0.472 vs AlphaMissense 0.923). **Only `PM2` survives. It is not being submitted.** |
| **"supplement-grade safety" for our lead compound** | an unresolved oncological signal we already held (**PMID 36371959**) |
| **"the mosaic aneuploidy is visible in bulk WGS"** | **falsified — it was mis-mapping.** Replaced with a bounded negative: no gain above ~3.2% of cells |
| **"microcephaly is *BUB1B*-specific"** | citation drift traced across three papers; the primary says **4 of 7** |
| **"an N1002K construct does not exist anywhere"** | narrowed to the two repositories actually searched — **an unresolved query is not an absence** |

> 🔑 Every row above was found by us, before submission, and each is published rather than quietly
> dropped. A reviewer can check that: the corrections are in the files, with dates and with what the
> text used to say.

---

## Appendix — companion documents

**This report does not depend on any of these.** Each is corroboration for a claim made above, listed
so coverage can be checked rather than taken on trust.

| document | what it establishes |
|---|---|
| `adriamasnou_track1_report.md` | the variant call, the phasing bound, and the alignment it rests on |
| `annotation-toolchain-vep.md` | Ensembl VEP over the full cache — 313,417 variants in, 313,417 distinct out, both patient alleles passing a known-answer control |
| `methods-and-self-critique.md` | the phenotype-blind scan, run so the answer could have come out otherwise — plus every claim of ours that failed |
| `splice-prediction.md` | local SpliceAI run as the model, not as lookup, with a positive control that caught a silent failure of our own making |
| `sv-cnv-survey.md` | genome-wide SV/CNV survey — is the compound heterozygote the complete molecular explanation? |
| `callability-audit.md` | genome-wide MAPQ/callability audit, and the check that the causal locus is not in a dark region |
| `generalisation-public-case.md` | the same pipeline, unchanged, on public data (§4) |
| `register-audit.md` | the whole-register audit behind §5's 94.9% and 89.7% |
| `hfea-pgtm-gene-crosswalk.md` · `.csv` | the gene↔condition crosswalk the regulator's own register does not provide |
| `impact-costs-and-access.md` | what surveillance actually costs, and how anything would reach this child |
| `family-facing-decision-aid.md` | built to IPDAS, including a declaration of the criteria it fails |
| `family-facing-summary.md` | the same evidence written for the family, carrying the same caveats |
| `secondary-findings-disclosure-protocol.md` | a reusable governance template for open single-patient challenges, CC BY 4.0 |
| `innovation-mechanism.md` | the compartment filter and the branch point, in full |
| `n1002k-reagent-specification.md` | the build specification, with both 972 bp sequences printed and every price dated |
| `n1002k-collaboration-package.md` | the bench protocol in *Nature Protocols* format, with timing, critical steps and troubleshooting |
| `screen-protocol-runnable.md` · `pilot-protocol-bubr1-flow.md` | the screen, and the pilot that gates it |
| `notes-for-judges.md` | the 150-word note accompanying this submission |
| `canary/` | the positive-control panel described in §4 |

---

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · adriamasnou · CC BY 4.0*
