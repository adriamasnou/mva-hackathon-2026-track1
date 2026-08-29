# A tiered disclosure protocol for secondary findings in open, single-patient data challenges

**A reusable governance template — CC BY 4.0 — with the worked example that produced it.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · adriamasnou · 2026-08-29*

> **This document is written to be taken and used by someone else.** Part A is the template and
> is deliberately condition-agnostic, organiser-agnostic and contest-agnostic. Part B is our own
> application of it, including what we have *not* done. If you only want the reusable thing,
> read Part A and the checklist in §A.5 and stop.

---

## The problem this exists to solve

A growing class of research event puts **one real patient's genome in front of many teams** and
publishes the results openly. The format works: it is fast, it is generous, and it gets a family
answers that a clinical pathway alone might take years to reach.

It also creates a hazard that the format's own rules usually do not address.

Such challenges typically (a) **welcome** secondary or incidental findings — extra rows in a
submission, reviewed qualitatively, with no scoring penalty — and (b) require submissions to be
**public and openly licensed**. Each is reasonable alone. Together they mean that a team that
does exactly what it was invited to do can create **permanent, public, individual-level health
information about an identifiable child, concerning conditions nobody asked about.**

The asymmetry is the point:

| | consented? | published? |
|---|---|---|
| the **causal** finding | yes — it is the question the family asked the world | appropriate |
| an **incidental** finding | no — never sought, never discussed | **permanent and public** |

A cancer-predisposition variant unrelated to the primary condition, a carrier state, a
pharmacogenomic result: each is legal to publish under most such rules, useful to somebody, and
wrong to place in a public repository attached to a named child who cannot consent and will one
day be an adult.

**Precedent does not settle it.** CAGI6-RGP instructed teams *not* to return incidental findings
(Stenton *et al.* 2024). This hackathon explicitly invites them. Neither addresses the difference
between finding something and publishing it.

The resolution is not to refuse the findings. It is to **separate what is discovered from what is
made public**, and to route the difference somewhere useful.

---

# PART A — THE TEMPLATE

## A.1 The tiers

**Tier 0 — the causal finding.** The answer the challenge exists to produce.
→ **Published in full.** This is what the family asked for.

**Tier 1 — findings relevant to the primary condition.** A modifier, a second hit, or a
variant explaining an otherwise unexplained core feature of the presenting phenotype.
→ **Published as named variants only if the evidence is strong** and the assertion criteria are
stated. Otherwise summarised at gene or category level. The test is *"does this help interpret
the condition the family already knows about?"*

**Tier 2 — actionable findings unrelated to the primary condition.** Secondary-findings-list
territory: unrelated cancer predisposition, cardiac, metabolic; carrier status; pharmacogenomics.
→ **Never published as named variants.** The public report states **category and count only**
(*"the screen identified N variants meeting reporting criteria in [list] genes"*). The specifics
go to the organisers through their sanctioned private channel, for transmission to the family
**via their own clinical team**, mirroring how the Rare Genomes Project returns findings through
a local clinician after CLIA confirmation — and honouring any no-recontact rule, because the
research team never contacts the family directly.

**Tier 3 — uncertain, unactionable, or weakly predispositional.**
→ **Not reported anywhere**, except as an aggregate count in methods. Publishing these
transfers anxiety without transferring information.

## A.2 Cross-cutting rules

1. **Direct evidence before tier assignment.** No tier is assigned from an annotation alone.
2. **Never restate what the family has not already made public.** Sex, ages, locations, treatment
   details, school, region — out, unless the family published them themselves.
3. **A research assay is not a clinical assay.** Every Tier 1/2 statement carries the caveat that
   clinical confirmation is required before any use.
4. **Deletion obligations bind the data, not the governance.** Where a challenge requires data
   deletion after close, this protocol's outputs are category-level text and reconstruct nothing.
5. **State the tier counts publicly.** A reader must be able to check that you did what you said.
   A protocol whose application cannot be audited is a statement of intent, not a control.
6. 🔴 **The absence of a finding is not the same as not having looked.** If a tier was never
   screened, say "not screened" — never let silence read as a clean result.

## A.3 What this deliberately does NOT do

- It does not withhold anything from the family. Everything useful reaches them, through the
  route their own clinicians can act on.
- It does not refuse the organisers the value they wanted from secondary findings.
- It does not require the research team to make clinical judgements. Tier 2 is a *routing*
  decision, not an interpretation.
- **It does not survive being applied after the fact.** Tiering must be pre-specified. Deciding
  what to publish once you know what you found is how the harm happens.

## A.4 Why tiers rather than a blanket rule

A blanket "publish everything" makes the child's unrelated risks permanently public.
A blanket "publish nothing" wastes findings the family would want and the organisers invited.
Tiering keeps the value and drops the harm, and it is cheap: the classification takes minutes
once the categories are fixed in advance.
**[OUR INFERENCE. This is a design argument, not an empirical finding. We are not aware of a
study comparing disclosure regimes in open single-patient challenges, and we did not find one;
if the trade-off has been measured somewhere, this section should defer to that measurement.]**

## A.5 Adoption checklist

For an **organiser** writing rules, or a **team** with no rules to follow:

- [ ] State in the rules whether secondary findings are invited. Ambiguity defaults to teams
      guessing, and they will guess differently from each other.
- [ ] Name a **private channel** for Tier 2 before the event opens. Without one, the tiering
      collapses and teams face publish-or-discard.
- [ ] Say who transmits to the family, and confirm it is a clinician.
- [ ] Require public reports to state **tier counts**, so compliance is checkable.
- [ ] Require tiers to be **pre-specified** in the methods, not chosen after results.
- [ ] Decide whether "not screened" must be declared. It should be.
- [ ] Check the public-licence clause against the tiering — an open licence applied to a Tier 2
      variant cannot be withdrawn later.

This checklist is the part most worth copying. The tiers are easy; **the private channel and the
pre-specification are what make them real.**

---

# PART B — OUR APPLICATION, AND WHAT WE HAVE NOT DONE

*Status as of 2026-08-29. Written to be falsifiable: every claim below is either an executed
action or an explicit "not done".*

**Tier 0 — done and published.** The biallelic causal pair is published in full, in the Track 1
submission and report, with evidence and limitations.

**Tier 1 — screen executed, findings NOT yet derived.** A pre-specified 30-gene panel relating to
an unexplained clinical feature (nephrocalcinosis) was run genome-wide. **Its output is a raw
pre-filter variant extraction — not a findings list**, and no variant in it has been curated,
evidence-assessed, or assigned a disclosure tier. It is held only in the gated working area and
nothing derived from it appears in this repository. **We are not reporting a count of findings,
because we do not have one**; reporting the raw extraction size as though it were a findings count
would be exactly the overstatement this protocol exists to prevent.

Separately, and on the literature rather than the genome: the same clinical feature is **not
reported in any published MVA case**, and the more likely explanation remains extreme prematurity.
That is a published negative and it belongs in the report, not here.

**Tier 2 — SCREENED 2026-08-29. Result below, reported under this document's own rules.**

*(This section previously read "NOT SCREENED", stated so that its absence could not read as a clean
result. The screen has since been run: `pipeline/acmg_sf_screen.py`.)*

**Method.** All 81 genes of **ACMG SF v3.2** (enumerated from NCBI, 2026-08-29), plus — because the
proband is a UK child — **the NHS Genomic Medicine Service's own age-stratified "additional
findings" panels** from Genomics England PanelApp. Classification is **ClinVar's, not ours**: a
variant counts as reportable only where ClinVar records it Pathogenic or Likely pathogenic at ≥1★.
We assert no pathogenicity ourselves.
**[OUR MEASUREMENT — gene list from `ncbi.nlm.nih.gov/clinvar/docs/acmg/` and NHS panels from
PanelApp, both retrieved 2026-08-29; classifications from ClinVar `variant_summary.txt.gz`
of the same date. ⚠️ The NCBI page's prose states 73 genes while enumerating 81; the
enumeration was used and the discrepancy is recorded rather than reconciled away.]**

| screened against | genes | variants meeting reporting criteria |
|---|---|---|
| ACMG SF v3.2 — cancer | 28 | **0** |
| ACMG SF v3.2 — cardiovascular | 39 | **0** |
| ACMG SF v3.2 — metabolic / other | 14 | **0** |
| **NHS additional findings — children** | **7** | **0** |
| NHS additional findings — adult-specific | 6 | **0** |
| NHS additional findings — full health-related | 14 | **0** |

**10,895 PASS variants fall inside the ACMG SF genes; none meets reporting criteria. There is
nothing to disclose, and therefore no Tier 2 transmission to request.**

> ### 🔴 This negative is only worth stating because the join was controlled first.
> A zero from an unverified lookup is indistinguishable from a broken one. **Controls, run before
> the result was believed:** 1,851 of the proband's chr15 variants match ClinVar records, so the
> join works; and the proband's **own** truncating allele is **found** in ClinVar while his
> missense allele is **absent** — exactly as expected, since the latter is novel. A screen that
> cannot find the variant we already know about would not be evidence of anything.

### 🔑 What the NHS comparison shows, and why it belongs in a protocol document

**The NHS returns seven genes to a child where ACMG recommends eighty-one.** *BRCA1*, *BRCA2* and
the Lynch-syndrome genes sit on the **adult-specific** panel and would **not** be returned to him
now — they are held until he can decide for himself.

That is **age-stratified return of results already operating in a national health service**, and it
is the same principle as Part A's tiering, arrived at independently by people with statutory
responsibility for it. Our Tier 2 rule says specifics go to the family through their clinicians
rather than into a public repository; the NHS goes further and withholds adult-onset findings from
the child entirely until adulthood. **A protocol proposing restraint is on firmer ground when it can
point at a health service already practising more of it than the protocol demands.**

⚠️ **A null result is not a clean bill of health.** It means no variant in these genes met these
criteria in this callset — not that none exists. Coverage gaps, structural variants, and variants
ClinVar has not yet classified are all outside what this screen can see, and roughly 1–3% of
individuals are expected to carry a reportable secondary finding, so **zero is the ordinary outcome
rather than a reassuring one.**

**Tier 3 — nothing to report**, consistent with Tier 1 not yet being curated.

### What this protocol cost us, stated plainly

Following it means our public submission will contain **fewer named variants** than the rules
permit, in a contest where extra rows are invited and carry no penalty. We think that is the
right trade and we would rather it be visible than quietly absorbed.

---

## Provenance and reuse

Developed for the *Rare Disease, Real Kid: MVA Hackathon 2026* (Sage Bionetworks, the MVA Society,
Hugging Face, BEACON), where the proband is a real, identifiable, publicly-known child and
submissions are openly licensed — the exact combination this protocol addresses.

**Released under CC BY 4.0.** Any organiser, team, patient organisation or challenge may adopt,
adapt or absorb it, in whole or in part, with or without attribution to us. Part A contains
nothing specific to this condition, this child, or this contest, and that is deliberate: the
hazard belongs to the format, not to the case.

**Reference for the returned-findings route:** Stenton *et al.*, on the Rare Genomes Project's
practice of returning findings via a local clinician after clinical confirmation.
