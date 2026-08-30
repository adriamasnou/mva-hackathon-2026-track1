# The answer existed and could not be found

**An audit of the infrastructure between a rare-disease diagnosis and the things a family is
entitled to — measured across the whole UK PGT-M register, not just one child.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## The thesis, and where it came from

This project began with one child's genome and the question *what causes his condition, and could
anything help?* The causal answer took a day. Everything after it kept running into the same wall,
and the wall — not the biology — turned out to be the finding.

For this child, every one of these is true:

1. **Embryo testing for his exact condition has been approved in the UK for years — and searching
   the regulator's register for his gene returns "No data to display."**
2. **His gene is classified at the highest confidence tier for gene–disease validity, and no expert
   panel has ever curated a single variant in it.**
3. **The coding system European rare-disease registries use cannot tell his condition apart from
   two others caused by different genes — one of which does not cause cancer at all.**
4. **Three published sources aimed at three different audiences give three different answers about
   his cancer surveillance, and none matches the current consensus.**

None of these is a gap in medicine. Every one is a gap in the machinery that connects medicine to
the person it exists for. **Each register is defensible on its own. The holes only appear when you
join them against each other** — and that is what this document does, for all 2,063 approved
conditions rather than for one.

---

## 1. You cannot find it by gene · **94.9%**

The HFEA register of conditions approved for preimplantation genetic testing has three columns:
condition name, status, OMIM number. **There is no gene column**, and its search matches
condition-name text — so a gene is findable only if a curator happened to write the symbol into a
condition name.

Verified live, same query form, opposite outcomes: `?condition=BRCA2` returns results (the symbol
sits inside *"…Susceptibility to, 2 (BRCA2)"*); **`?condition=BUB1B` returns "No data to display."**

> **1,688 of the 1,778 genes behind approved conditions — 94.9% — are invisible to a gene search.
> 1,892 conditions are reachable only through such a gene. Cystic fibrosis is one of them.**

Fixed here: `hfea-pgtm-gene-crosswalk.csv` and `hfea-pgtm-gene-index.json` supply the missing
index for every approved condition. Method, sources and limitations: `hfea-pgtm-gene-crosswalk.md`.

**The register is also not machine-readable in 27 rows** — including **CHIME syndrome published
under OMIM `28000`, which is not a valid OMIM number** (every MIM is six digits; the real one is
280000). The register instructs users to search by OMIM number; for that condition, following the
instruction cannot succeed.

## 2. Registries cannot tell the conditions apart · **1,068 genes**

European rare-disease registries code by ORPHA number. Orphanet groups by clinical entity, which is
right for its own purpose and wrong as a stratification key — distinct genes with **different
prognoses** collapse into one code.

Joining Orphanet's OMIM cross-references (11,645 disorders) to the register:

| | |
|---|---|
| approved conditions carrying an ORPHA code | 1,927 of 2,063 |
| **ORPHA codes covering ≥ 2 distinct genes** | **359** |
| **approved conditions sitting inside such a code** | **1,061** |
| **distinct genes made indistinguishable by the coding** | **1,068** |
| largest single collapse | **ORPHA:442835 — 41 genes, 42 approved conditions** |

**[OUR MEASUREMENT — Orphanet `en_product1.xml`, 2026-06-23, CC BY 4.0, joined to the crosswalk.]**

> ### The consequence, in this child's case
> **ORPHA:1052 covers *BUB1B*, *CEP57* and *TRIP13* as one condition.** Wilms tumour is reported in
> roughly **half** of patients with *BUB1B* variants, about **20%** with *TRIP13*, and — to current
> knowledge — **none** with *CEP57* (Hol *et al.* 2021, PMID 34134020; Nakano *et al.* 2024,
> PMID 39264246). **A registry coded by ORPHA cannot separate the children who need cancer
> surveillance from the children who do not.** The information exists. The coding discards it.

## 3. Nobody has curated the variants · **92.1%**

*BUB1B*'s gene–disease relationship is classified **Definitive** — the highest confidence tier —
and there is **no ClinGen Variant Curation Expert Panel** for it. A family can be offered embryo
selection against a gene whose variants no expert panel has ever classified.

Measured across the whole register, from ClinVar's own review-status field
(**4,490,695 GRCh38 variant records**, expert tiers = *reviewed by expert panel* and
*practice guideline*):

| | |
|---|---|
| genes anywhere in ClinVar with ≥1 expert-panel-reviewed variant | **219** |
| genes behind UK-approved PGT-M conditions | 1,778 |
| **…with ≥1 expert-panel-reviewed variant** | **141 (7.9%)** |
| **…with ZERO expert-panel-reviewed variants** | **1,637 (92.1%)** |
| **approved conditions where no causative gene has any expert curation** | **1,851 of the 2,026 gene-mappable conditions (91.4%)** — **1,851 of all 2,063 approved (89.7%)** |

> ⚠️ **DENOMINATOR DRIFT, FLAGGED NOT PATCHED — 2026-08-31.** Two bugs were fixed in
> `pipeline/hfea_crosswalk.py` today (a ClinVar `RelatedGenes` field never read, and a null `-`
> ingested as a gene — see `hfea-pgtm-gene-crosswalk.md` §6 item 5). **The shipped CSV now maps
> 2,028 conditions to at least one gene, against the 2,026 this row uses.** The **2,063** total and
> the **89.7%** figure are unaffected. **I have deliberately NOT adjusted 1,851 or 91.4%**: the
> numerator comes from a ClinVar expert-curation panel run that has not been re-executed, and
> recomputing a rate by moving only its denominator would manufacture a number neither run
> produced. **To close this properly, re-run the panel against the corrected crosswalk and restate
> both figures together.** The direction is knowable in advance — two more mappable conditions can
> only *lower* the percentage — so 91.4% is a ceiling, not a floor.

> **The UK approves embryo selection against 2,063 conditions. For 1,851 of them — 89.7% — no
> expert panel has ever classified a single variant in any causative gene.**

🔻 **CORRECTED 2026-08-30 — the numerator and the denominator were from different populations.**
This pull-quote used to read *"For 91.4% of them"*. **91.4% is 1,851 / 2,026** — a rate over the
conditions that could be mapped to a causative gene **at all** — while the sentence applies it to
the **2,063** approved conditions it names in its own first clause. Over 2,063 the figure is
**89.7%**. The ~37 unmapped conditions cannot be assessed for expert curation either way, so
**89.7% is a floor**: the true share is somewhere between 89.7% and 91.4% depending on how the
unmapped tail resolves, and the floor is the honest number to lead with. The table above keeps
1,851/2,026 = 91.4% and now says which population it is over. [OUR MEASUREMENT — arithmetic,
2026-08-30: 1851/2063 = 89.7%, 1851/2026 = 91.4%.]

***BUB1B* holds 2,472 ClinVar variants and 0 expert-panel classifications.** That is not an
outlier; it is the ordinary case.

**[OUR MEASUREMENT — ClinVar `variant_summary.txt.gz`, GRCh38 rows only, joined to the crosswalk.]**

🔻 **This number replaces a wrong one, and the failure is worth recording.** A first attempt used
ClinGen's public classification export and returned **97.2%** — and the same run returned **zero
for *BRCA2* and zero for *CFTR***, which is impossible: ENIGMA alone has classified thousands of
*BRCA2* variants. That endpoint returns a subset, not the whole set. **The result was withheld
rather than published, and re-derived from the authoritative source, where the controls now pass
(BRCA2 4,182 · CFTR 393 · PAH 816 · TP53 184).** A spectacular result that fails its own control
is not a result — and the two figures are close enough (97.2 vs 92.1) that the wrong one would
never have looked wrong. **[OUR MEASUREMENT — both runs are ours; the ClinGen export was fetched from `erepo.clinicalgenome.org/evrepo/api/classifications/all`, the authoritative counts from ClinVar `variant_summary.txt.gz`, both on 2026-08-29.]**

## 4. The guidance says different things to different readers

Three published sources, read directly on 2026-08-29:

| source | audience | interval | modality | stop age |
|---|---|---|---|---|
| **SIOP-E 2021 (PMID 34134020), re-endorsed AACR 2024 (PMID 39264246)** | consensus | 3 months | **renal** | **7th birthday** |
| clinical reference sites still in circulation | clinicians | **3–4 months** | renal | **age 5** |
| the main *BUB1B*-MVA guide written for families (2026) | **families** | 3 months ✅ | **abdominal** | **none stated** |

The superseded 2006 interval is still cited: of 56 citations to the two Wilms-surveillance
guidance papers since 2022, **16 go to the 2006 recommendation.**
⚠️ **That last figure is a weak proxy and is labelled as one** — a foundational paper is often cited
historically rather than followed. **[OUR MEASUREMENT — Europe PMC citation counts, 2026-08-29.]**

The family-facing guide is *right about the interval* and diverges in three other ways: it
recommends an **abdominal** scan where the consensus specifies **renal** (reserving full abdominal
scanning for other syndromes), states **no stopping age**, and says *"No clinical practice
guidelines for MVA1 syndrome have been published (2026)"* — so families are never directed to the
consensus that exists. **We had assumed the stale interval would be found in the family-facing
source and checked; it was in the clinician-facing ones instead.**

---

## 4b. ✅ The join that came back CLEAN — and it is here because it did

A fourth join was run and **found no meaningful hole.** It is reported for two reasons: because
selecting only the joins that found something would make the other three unreliable, and because
**what nearly happened to it is the most useful part.**

**The question:** are there conditions the UK approves embryo selection against whose gene the NHS
will not test? Joining the crosswalk to **PanelApp**, the Genomics England register of the gene
panels the NHS Genomic Medicine Service actually uses:

| | |
|---|---|
| genes behind approved conditions that are **diagnostic-grade ("green") on an NHS panel** | **1,643 / 1,778 = 92.4%** |
| not diagnostic-grade anywhere | 135 (7.6%) |
| **approved conditions where no causative gene is diagnostic-grade** | **108 of 2,026 = 5.3%** |

**And most of the residual is gene-symbol drift, not a coverage gap** — `TAFAZZIN` (was `TAZ`),
`H3-3A` (was `H3F3A`), `CDIN1` (was `C15orf41`). **Controls behave: *BUB1B*, *CFTR*, *BRCA2*, *DMD*
and *TP53* are all green.**

> ### These two NHS surfaces align. That is a real answer, and it is a negative.

### 🔴 4b.1 What nearly happened, and why it is the most instructive part of this document

**The first run of this join reported 40.6% of genes not testable and 35.8% of conditions blocked**
— a dramatic, quotable, entirely publishable-looking claim.

**It was computed on 26% of the data.** The fetcher had aborted at page 85 of 326, written 8,498 of
32,503 entries, **printed `DONE`, and exited 0.** It was caught only because the API's own declared
count did not match what was held — **by eye, not by any assertion.**

| | truncated (26%) | complete (92.9%) |
|---|---|---|
| genes not diagnostic-grade | **40.6%** | **7.6%** |
| conditions blocked | **35.8%** | **5.3%** |

**The fetcher now reads the API's declared count as a contract and exits non-zero if short**
(`pipeline/fetch_panelapp.py`). ⚠️ **The completed fetch is still 92.9% of the declared count** —
consistent with duplicate delivery under unstable pagination rather than loss, **but that cannot be
proved, so the figures above carry that caveat.**

> **A partial download that announces success is worse than one that crashes.** The three findings
> in §1–§3 are trustworthy only to the extent that this failure mode was caught in §4b — and it was
> caught once, late, by a human noticing.

**[OUR MEASUREMENT — PanelApp API, 30,190 of 32,503 declared gene-panel entries, 414 panels,
5,937 genes, retrieved 2026-08-29.]**

## 5. What this is, and what it is not

**It is not a criticism of the HFEA, Orphanet, ClinGen or any charity.** Each is doing a job well
under its own constraints, and the register's own guidance to search by OMIM number is sound advice
about its own contents. **Every failure above is an interface failure between systems that are
individually fine** — which is exactly why none of the four organisations could have found them
alone, and why they are invisible until someone joins the registers against each other.

**It is not clinical advice.** Approval is not eligibility; coding is not prognosis; a citation
count is not clinical practice. Those limits are stated at each measurement.

**It is not a claim to have fixed the problem.** One of the four is fixed — §1 ships the missing
index. §2 is measured but not fixed; fixing it is a coding-policy decision for Orphanet and the
registries. §3 is withheld pending a sound measurement. §4 is an observation about published
sources.

## 6. Why it generalises

The case that produced this is *N* = 1. **Every number above is *N* = 2,063.** The child's
situation was the instrument, not the subject: it was only by trying to get one family from a
diagnosis to the things they are entitled to that the wall became visible, and the wall is
identical for every rare disease on the register.

If one thing here outlives the hackathon, it should be the crosswalk — and the best possible
outcome is that the register grows a gene column and makes it obsolete.

---

## Reproduce

```bash
python3 pipeline/hfea_crosswalk.py --refresh     # §1, and the index that everything else joins to
```

Sources: HFEA approved-conditions workbook · Orphanet `en_product1.xml` (CC BY 4.0) · ClinVar
`gene_condition_source_id` · HPO `genes_to_disease.txt` · Europe PMC. All public, none requiring
registration. Each derived document prints the **age** of its inputs, not only their names.
