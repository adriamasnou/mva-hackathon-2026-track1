# What we found, in plain language

**A summary for George's family, and for other MVA families**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · by adriamasnou (independent
researcher) · 2026-08-29 · CC BY 4.0*

> **How to check us.** Claims below carry their source in square brackets. A PMID is a PubMed
> identifier — paste it into pubmed.ncbi.nlm.nih.gov to read the source yourself. Where a
> conclusion is ours rather than a published result, the bracket says **OUR INFERENCE**;
> where we measured something ourselves, **OUR MEASUREMENT**. Please read those two labels as
> weaker than a citation, because that is what they mean.
>
> **This is research communication, not medical advice.** Nothing here is a recommendation to
> start, stop or change any treatment. Every medical decision belongs with the family and their
> own clinical team. Where we are unsure, we say so — there is a whole section of it below.

---

## What this document is

George's family shared his genome with researchers around the world and asked two questions:
*what exactly, in his DNA, causes his condition — and could any existing medicine help?*

Teams answered in technical language, because that is how the work gets checked. This document
says the same things in ordinary words. It is written to be read by a family, not by a
specialist, and it is meant to be shown to a doctor and argued with.

Anything below that a family could actually *act on* is marked **★ Ask your team about this**.
There are four of them, and they are the point of this document.

---

## 1. The cause, confirmed

Everyone carries two copies of a gene called *BUB1B* — one inherited from each parent. This gene
makes a protein called BubR1. BubR1 works like a safety inspector: every time a cell divides, it
checks that each new cell is getting the right number of chromosomes, and holds up the division
until the count is right.

George's two copies each carry a different change:

- **One copy is switched off.** The change puts a "stop" signal in the middle of the
  instructions, so that copy makes no working protein at all.
- **The other copy works, but imperfectly.** One building block is swapped in an important
  region of the protein.

Those two facts together are the whole story of his condition, and the second one matters more
than it first appears: because the first copy makes nothing, **every single inspector protein in
his cells is the altered kind.** There is no supply of the normal version mixed in. Most people
with one changed copy have a healthy second copy to fall back on. He does not.

With the inspector weakened, some dividing cells finish up with the wrong number of chromosomes
— and different wrong numbers in different cells. That is exactly what "mosaic variegated
aneuploidy" means: *mosaic* (only some cells), *variegated* (not the same error each time),
*aneuploidy* (the wrong chromosome count).

**This confirms, from the shared data alone, the diagnosis George's doctors had already made.**
We did not find a different answer, and we think that is worth saying plainly: the existing
diagnosis holds up under independent examination by people who had never seen it.

## 2. Can we see the condition itself in his data? — we thought so, we tested it, and no

The genetic *cause* is solid. Whether we can see its *effect* — cells with the wrong number of
chromosomes — in the data we were given is a separate question, and this section is the honest
answer to it, including the part where we were wrong.

**What we first saw.** Looking across all his chromosomes for a statistical fingerprint of cells
carrying extra copies, three of them — 20, 21 and 22 — stood out clearly, at about 1.4× the
signal of the other nineteen. It had the uneven, several-chromosomes-at-once shape that MVA
predicts. It looked like the condition made visible.

**What happened when we tried to break it.** Rather than publish that, we tried to find an
innocent explanation.

- *Is it because those chromosomes are small?* No. Chromosome 19 is smaller than chromosome 20
  and shows nothing.
- *Is it because they were read less deeply?* No — the opposite. They were read slightly more
  deeply than average, which makes the measurement more reliable, not less.
- *Is it because parts of the genome resemble each other, so the software puts reads in the
  wrong place?* **Yes. That was it.**

The genome contains regions that closely resemble other regions. Reads from them can be assigned
to the wrong location, and when that happens the software reports something that looks exactly
like an extra chromosome copy but is a filing error. Each read carries a score for how confident
the alignment is. **When we kept only the reads the software was certain about, the signal on
chromosomes 20, 21 and 22 vanished completely** — they became indistinguishable from every other
chromosome. The reason those three stood out is that about a third of their measurable sites are
in these confusing regions, against roughly one in eight for a typical chromosome.

> **So: we did not detect mosaic aneuploidy in this data, and the pattern that looked like it was
> an artefact of the analysis. We are reporting this because it is what we found, not because it
> is what we hoped for.**

**How hard did we look, and does our method work at all?** A negative result is worth nothing
unless both of those are answered.

*Does the method work?* We gave it a question we already knew the answer to. George is male, so he
has one X chromosome where the other chromosomes come in pairs — a real, known difference in copy
number, and one the method was never shown while it was being set up. **It returned 0.4999 where
the true answer is 0.5000** — an error of one part in ten thousand. It can detect a genuine change
in chromosome copy number. It then found nothing on chromosomes 20, 21 and 22.

*How hard did it look?* We tested it against simulated data containing a known amount of mosaic
change. **Had roughly 3–4% or more of his blood cells carried an extra copy, we would have
detected it.** We quote the more cautious end of that range, because different reasonable choices
in the analysis move it and we would rather understate how hard we looked than overstate it.

So the honest statement is *"not detected above roughly 4% of cells, using a method shown on this
same sample to recover a known answer"* — which is a real result. It is not *"there is nothing
there"*, which would be a claim we cannot support.

**None of this changes the diagnosis.** Mosaic variegated aneuploidy is diagnosed from cells
examined directly under a microscope, which is a far more sensitive test for this and which has
already been done for George. What we tested was whether the same phenomenon could *also* be seen
in this particular sequencing data, from blood, using this particular method. It could not. That
is a limitation of our method and this sample, and it says nothing about whether he has the
condition — he does.

## 3. ★ Ask your team about this: is the cancer surveillance plan the current one?

This is the most immediately useful thing in this document, and it is a question, not a claim.

Children with *BUB1B*-related MVA have a raised risk of Wilms tumour, a childhood kidney cancer.
Regular ultrasound scanning is recommended so that if one appears it is caught while small. There
are **two different published recommendations**, and they differ in a way that matters:

| | scan interval | continue until |
|---|---|---|
| The older UK guidance (2006) | every 3–4 months | 5th birthday |
| The current international consensus (2021, re-endorsed 2024) | **every 3 months** | **7th birthday** |

The current recommendation comes from the SIOP-Europe Host Genome Working Group
(Hol *et al.*, *European Journal of Cancer*, 2021), and it was carried forward by the American
Association for Cancer Research's childhood cancer predisposition workshop in 2024
(Nakano *et al.*, *Clinical Cancer Research*, 2024).

The difference between the two is **two extra years of scanning — about eight extra scans** —
during a period when these tumours do still occur. The newer guidance also gives its reasons:
appointments slip in practice, so a 3-month target is safer than a 3–4 month one, and these
tumours can double in size in as little as eleven days.

**The question to ask is simply: "which of these two is our surveillance plan following?"** Many
clinics will already be on the current one. But we checked what is actually in circulation, and
**three different sources aimed at three different audiences give three different answers**, none
of which matches the current consensus exactly:

| where | scan how often | which scan | until what age |
|---|---|---|---|
| the current consensus (2021, 2024) | every 3 months | **kidney** ultrasound | **7th birthday** |
| clinical reference sites still in use | every 3–4 months | kidney | age 5 |
| the main MVA guide written for families (2026) | every 3 months ✅ | **abdominal** | **no age given** |

So the older interval is still circulating — in **clinician-facing** reference sources rather than
in the family-facing guide, which we had assumed and checked. And the family-facing guide, while
right about the interval, recommends an *abdominal* scan where the consensus specifies a *kidney*
scan (it reserves full abdominal scanning for other conditions), gives **no stopping age**, and
states that no clinical practice guidelines for this condition have been published — so it does not
point families to the 2021 consensus at all.

**[OUR MEASUREMENT — the three sources were read directly on 2026-08-29. We are describing what
published sources say, not what any particular clinic does, which we have no way to know.]**

None of this means anyone has done anything wrong. It means the question is worth asking out loud,
and that it is a reasonable and easy one to answer.

One more detail from the same guidance, in case it comes up: the recommendation is for **kidney
ultrasound specifically**, not a full abdominal scan, and it applies to all forms of MVA — the
expert group was explicit that they recommend it across the board because the numbers for each
individual gene are still too small to safely separate.

## 4. ★ Ask your team about this: family planning, and a search that fails

For MVA, a changed copy is needed from each parent. Whether that is the case here can be
confirmed by a simple test on the parents, which a genetics service can arrange; our analysis of
George's data alone cannot prove it, and we have not assumed it. **If** both parents do carry a
change, then each future pregnancy carries a 1-in-4 chance of the condition — the standard
figure for this kind of inheritance.

For families who want it, embryo testing (**PGT-M** — testing embryos created by IVF before a
pregnancy begins) **is already approved in the United Kingdom for this exact condition.** It has
been approved for a while. That is the good news.

**Here is the problem, and it is the reason we are writing this paragraph.** The regulator's
public list of approved conditions is searchable by condition name and by OMIM number — but
**not by gene**. Searching that list for *BUB1B* returns "No data to display." A family, or even
a clinician, who searches the way genetics is actually discussed — by gene name — is told the
thing they are entitled to does not exist.

> **★ To find it, search the HFEA approved-conditions list for
> "Mosaic Variegated Aneuploidy Syndrome 1", or for the OMIM number 257300 — not for "BUB1B".**
> Four other forms of MVA are approved and listed there too.

We think this is a genuine failure in a public index rather than a gap in medicine, and it is
fixable by anyone who publishes the connection between the gene name and the condition name.
Doing that is one of our submissions to this hackathon.

**Two honest qualifications.** Approval of the condition is not the same as eligibility for a
particular family: the regulator's criteria require a risk of an affected pregnancy of 10% or
more, a referral from an NHS Clinical Genetics Service, and genetic counselling beforehand.
Whether any individual family qualifies is a clinical decision that we are not in a position to
make and have not made. And this is UK-specific; other countries have their own regulators and
their own lists.

## 5. ★ Ask your team about this: one thing that could actively cause harm

Most of this document is about what might help. This section is about the opposite, and it is
short because it is important.

There is a class of cancer drug called **HSP90 inhibitors**. In laboratory work on cells
carrying *BUB1B* changes very like George's, blocking HSP90 **stripped out the altered BubR1
protein while leaving the normal version largely untouched** (Suijkerbuijk *et al.*, 2010).

For most people that would be a side effect. For a child whose *entire* supply of the inspector
protein is the altered kind, it would remove the little function he has. Given that he has
already been treated for one cancer, the situation in which such a drug might be considered is
not hypothetical.

**We think HSP90 inhibitors should be regarded as relatively contraindicated in this form of
MVA.** This is our inference from published laboratory data, not an established clinical
guideline, and we state it in that form deliberately. **It is worth recording in his notes so
that the question gets asked if it ever arises.**
**[OUR INFERENCE, from Suijkerbuijk SJ et al., "Molecular causes for BUBR1 dysfunction in the
human cancer predisposition syndrome mosaic variegated aneuploidy", *Cancer Research* 2010;
PMID 20516114. The laboratory result is theirs; the clinical caution drawn from it is ours, and
we are not aware of it appearing in any guideline.]**

## 6. ★ Ask your team about this: there is no MVA registry yet, and that is a fixable problem

One reason MVA is hard to treat is that nobody has systematically collected what happens to
patients over time. Regulators call this a "natural history", and without one it is very hard to
show that any new treatment works.

**No MVA patient registry currently exists.** The MVA Society has said publicly that it hopes to
establish one and needs funding to do so. Existing European rare-disease registry networks
already have the infrastructure that such a registry would slot into.

For a family, the practical point is that **taking part in registries and natural-history studies
when they are offered is itself a contribution** — arguably one of the higher-value ones
available in a condition this rare, where the total number of described patients worldwide is
small enough that each additional documented case measurably changes the picture. It is worth
asking a genetics team what is open to enrol in.

---

## 7. What about treatment? — a testable idea, and what it is not

There is no proven treatment for MVA today. What research can realistically do at this stage is
identify *ideas worth testing properly*. Ours, in plain terms:

Laboratory studies suggest that altered BubR1 proteins of this kind are often **unstable** — the
cell makes them, then destroys too many of them. If that is what is happening, then the useful
target may not be the protein's activity at all, but its *amount*: raising the level of the
altered protein could restore a meaningful part of the inspector's function, because the altered
version is not useless, just insufficient.

**The first experiment is small and concrete.** Grow cells from a small skin sample, measure
whether the protein really is reduced, and test whether candidate compounds raise it. That
experiment either supports the idea or kills it, cheaply, before anyone goes near a patient.

**How strong is the evidence? Weaker than we would like, and we would rather say so.** One line
of work in mice, published in 2014, linked a vitamin-B3-related compound (nicotinamide riboside)
to this protein's stability. **In the twelve years since, no follow-up experiment has been
published** — not by the original authors, not by anyone. The same group's own 2024 review says
the mechanism "remains to be studied in depth". A gap that size is not evidence that the idea is
wrong, but it is not encouraging either, and anyone who presents that 2014 result as an
established basis for treatment is overstating it.
**[Sources: North BJ et al., "SIRT2 induces the checkpoint kinase BubR1 to increase lifespan",
2014, PMID 24825348 — the original mouse work; and Pun R, ... North BJ, "BubR1 and SIRT2:
Insights into aneuploidy, aging, and cancer", 2024, PMID 39490401 — the same group's review,
which is the source of the quoted phrase. The absence of follow-up is OUR MEASUREMENT, from a
literature search that returned no intervening experimental papers; an absence found by searching
is a floor, not a certainty.]**

What can be said fairly: the same compound has been given to children in a different rare
genetic condition affecting chromosome stability, at controlled doses under medical supervision,
and a regulator has granted it rare-paediatric-disease status in that condition. So a route
exists in principle.

> **What this is:** a testable hypothesis with a defined first experiment.
> **What this is not:** a treatment, a recommendation, or anything to try at home. Doses used in
> studies are not approved for children, and shop-bought supplements are neither the same thing
> nor a safe substitute for one. Anything of this kind belongs in a supervised clinical setting,
> decided together with George's own medical team.

---

## 8. What we are putting into the public record

Two changes were found in *BUB1B*. One of them is already recorded in **ClinVar**, the public
library that laboratories worldwide consult when they interpret a genetic test. **The other is
not.**

That means a laboratory somewhere else, seeing the same change in a different child tomorrow,
would find no record of it and would have to start from nothing.

We have prepared a submission to add it, with our evidence and reasoning attached.
**It has not been submitted yet** — the account registration is still awaiting approval, and we
will not file anything about this child without the family's and the organisers' agreement. We
mention it here because it is a commitment, not an achievement, and it should be readable as one.

---

## 9. What we are unsure about, and what we did not do

Families are owed straight answers about uncertainty, so, in order of how much they matter:

1. **We have not proved the protein is actually reduced in George's cells.** The whole treatment
   idea rests on it. It needs the skin-cell experiment described above. It could fail.
2. **We have not proved the two changes sit on opposite copies of the gene.** They are too far
   apart in the gene for this sequencing method to settle it. The diagnosis assumes it and the
   arrangement is by far the most likely one, but a parental test is what would confirm it.
3. **We looked for the wrong-chromosome-number pattern in this data and did not find it**, once
   an analysis artefact was removed — see section 2. We could have detected it had it involved
   roughly 4% or more of his blood cells, and we checked the method works by testing it against a
   known answer on this same sample.
4. **One feature of his condition — calcium deposits in the kidneys — is probably not caused by
   the gene.** It is common in babies born very prematurely, which is the more likely explanation
   here. We checked the rest of his genome for an alternative genetic cause and did not find one,
   but "did not find" is not the same as "is not there".
5. **We never met or contacted the family**, by design. Everything here comes from the shared
   data and from what the family has already chosen to make public. Nothing personal has been
   restated that they did not publish themselves.

Where the full report and this summary disagree, the full report is the one with the workings
in it. If anything here is wrong, we would rather be told and correct it than have it stand.

---

## Provenance

Prepared by **adriamasnou** (independent researcher) for the *Rare Disease, Real Kid: MVA
Hackathon 2026*, organised by Sage Bionetworks with the MVA Society, Hugging Face and BEACON.

Written to be readable at roughly ages 12–14, following NHS and Genomics England plain-language
guidance. Every factual claim above is sourced in the accompanying Track 2 report; the primary
sources for the surveillance interval, the PGT-M approval and the HSP90 finding are named in the
text so they can be checked directly.

Released under **CC BY 4.0** — any family, clinician, patient organisation or research team may
reuse or adapt this, including the structure, for another condition.

**This document is research communication, not medical advice. All medical decisions belong with
the family and their clinical team.**

*With thanks to the child and family whose data and whose openness made this possible.*
