# The UK PGT-M register, indexed by gene

**A gene ↔ OMIM ↔ condition crosswalk for all 2,063 conditions approved for preimplantation
genetic testing in the United Kingdom — and a measurement of how many of them cannot be found
the way genetics is actually practised.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · adriamasnou · 2026-08-29 · CC BY 4.0*

| artefact | what it is |
|---|---|
| `hfea-pgtm-gene-crosswalk.csv` | every approved condition, with the gene(s) it is caused by, the OMIM number(s) as published, and any defect in how that row is published |
| `hfea-pgtm-gene-index.json` | the inverse index: gene symbol → the approved conditions it gives access to |
| `pipeline/hfea_crosswalk.py` | builds both from public sources in one command |

---

## 1. Why this exists

The HFEA publishes which conditions are approved for PGT-M in the UK. Its register has three
columns: **condition name, status, OMIM number.** **There is no gene column** — the only place a
gene symbol ever appears is inside a *condition name*, where a curator happened to write one.
🔻 *This read "no gene symbol appears anywhere in the workbook" until 2026-08-31, and §2 of this
same document falsifies it four paragraphs later: §2's entire measurement rests on symbols
appearing in condition names — its worked example is BRCA2, "the symbol sits inside
Breast-Ovarian Cancer, Familial, Susceptibility to, 2 (BRCA2)" — and the shipped index records
`_genes_findable_by_accident: 90`. **The absolute was the overstatement; the finding underneath it
is unchanged and is if anything sharper: a gene is findable only by accident.**

The register's own guidance tells users to search by OMIM number, precisely because condition
names are unstable. That advice is sound and it has a gap in the middle of it: **nothing in the
register gets you from a gene to an OMIM number.** A clinical genetics report names a gene. A
family who has been told "your child has a *BUB1B* variant" has a gene. Neither can enter the
register with what they hold.

This was found while working on a single child's case, where searching the register for *BUB1B*
returns *"No data to display"* while the condition it causes has been approved for years. The
crosswalk here is the general fix rather than the one-row one, because the missing column is
missing for every row.

## 2. The measurement

The register's search matches the **text of condition names**. So a gene is findable if, and only
if, a curator happened to write its symbol into one of its own condition names. That is not a
policy; it is an accident of prose.

**Verified live against the register on 2026-08-29**, same query form, opposite outcomes:

| query | result |
|---|---|
| `?condition=BRCA2` | returns results — the symbol sits inside *"Breast-Ovarian Cancer, Familial, Susceptibility to, 2 (BRCA2)"* |
| `?condition=BUB1B` | **"No data to display"** |

Applying that rule across the whole register:

> ### 1,688 of the 1,778 genes behind approved conditions — **94.9%** — are invisible to a gene
> ### search of the register. 1,892 conditions can be reached only through such a gene.

**Cystic fibrosis is one of them.** Searching the UK's approved-conditions register for `CFTR`
finds nothing.

The 5.1% that do work are not a designed subset. They are the genes whose symbols a curator
wrote in brackets after a condition name.

## 3. What the crosswalk contains

| | |
|---|---|
| approved-condition rows parsed | **2,063** |
| mapped to ≥1 causative gene | **2,027 (98.3%)** |
| distinct genes indexed | **1,778** |
| not mapped | 36 — every one listed in the CSV with `n_genes=0`, none silently dropped |
| ClinVar and HPO agree exactly | 2,007 |
| ClinVar and HPO name different genes | 2 — **reported, not reconciled**: locus heterogeneity is real biology, not a defect to average away |

## 4. Defects found in the register itself

Building the crosswalk required parsing the OMIM column as it actually is rather than as a number
column. **27 rows are published in a form no program can read**, and they are flagged per-row in
the CSV's `register_defect` column:

| defect | rows | example, verbatim |
|---|---|---|
| no OMIM number at all | 14 | `Chromosomal rearrangements (various)` |
| OMIM's own gene-entry prefix `*` | 5 | `*182340`, `" *620823 "` (with stray spaces) |
| several OMIM numbers in one cell | 6 | `601728, 158350, 153480, 605309`; `609307 & 193003` |
| free text where a number belongs | 1 | `ARVC/D` |
| **malformed OMIM number** | 2 | see below |

🔻 **The `rows` column above sums to 28, and the register carries 27 defective rows** — corrected
2026-08-31. **The prose total of 27 is right**; the table double-counts **one row that bears two
defects**, whose CSV value is `multi-omim(3);malformed-mim-length`. It is counted once under
*"several OMIM numbers in one cell"* and again under *"malformed OMIM number"*. The column is
labelled **rows**, so as printed it is a row count that does not sum to the row count. **Read the
column as defect-instances, not rows; the row total is 27.**

> ### 🔴 CHIME syndrome is published under OMIM `28000`. That is not an OMIM number.
> Every MIM in OMIM's own index is six digits; `28000` is five and does not exist. The correct
> identifier is **280000** (→ *PIGL*, confirmed via ClinVar). The register instructs users to
> search by OMIM number; **for this condition, following that instruction cannot succeed.**
> The crosswalk carries the corrected identifier.

## 5. Method, and the trap in it

```bash
python3 pipeline/hfea_crosswalk.py --refresh
```

Sources, all public and none requiring registration:

| source | role |
|---|---|
| HFEA approved-conditions workbook (snapshot 2026-08-05) | the register itself |
| ClinVar `gene_condition_source_id` (NCBI) | gene ↔ disease-MIM |
| HPO `genes_to_disease.txt` (Jax/Monarch) | gene ↔ OMIM disease id, independent second opinion |
| OMIM `mim2gene.txt` | **gene-MIM index only** |

**The obvious join does not work, and silently returns nothing for exactly the rows that matter.**
`mim2gene.txt` looks like the natural bridge from an OMIM number to a gene symbol. Its own header
says otherwise — *"THIS IS NOT A TABLE OF GENE-PHENOTYPE RELATIONSHIPS."* It indexes **gene**
entries; the register is keyed by **phenotype** MIMs, which carry no symbol there:

```
$ grep -P "^257300\t" mim2gene.txt
257300	phenotype
```

Anyone reaching for the intuitive file gets an empty result and may conclude the mapping cannot be
made. It can — from ClinVar and HPO, which record phenotype→gene evidence. `mim2gene.txt` is still
used here, but only for its real job: catching the five register rows that cite a **gene** MIM.

Two independent phenotype→gene sources are used deliberately rather than one, so that agreement is
a reported quantity instead of an assumption. The build prints the **age** of every input, warns
past 24 hours, and aborts rather than write a short file if any fetch fails — a truncated source
would quietly shrink every count downstream, and a wrong number is worse than a missing one.

## 6. Limitations — please read these before using it

1. **Built from the downloadable workbook, which the HFEA states is less current than its
   website.** The website is authoritative. This crosswalk is a derived index, not a substitute
   for the register, and the snapshot it was built from is named in the JSON.
2. **The 94.9% figure is computed** from the crosswalk's own gene↔condition-name mapping and
   **spot-verified live on three genes** (BRCA2 findable, BUB1B and CFTR not), not on all 1,778.
   Independent re-testing is welcome; the method is one line of the script.
3. **Approval is not eligibility.** The HFEA's criteria require a risk of an affected pregnancy of
   10% or more, referral by an NHS Clinical Genetics Service, and prior genetic counselling.
   Nothing here is a statement that any person qualifies for anything.
4. **Gene–disease attribution is inherited** from ClinVar and HPO and is only as current as they
   are. Where they disagree, both genes are listed.
5. **35 conditions are unmapped** and are in the CSV with `n_genes=0` — 14 because the register
   gives no OMIM number, 1 because it gives text, 1 because the number is malformed, and the rest
   because no public gene–disease source links that MIM to a gene. They are listed, not hidden.

   > 🔴 **IT WAS 36, AND ONE OF THEM WAS OUR BUG, NOT THE REGISTER'S — fixed 2026-08-31.**
   > **`Leigh Syndrome (LS)` (MIM 256000) shipped as a measured zero with a blank `sources` cell.**
   > ClinVar's `gene_condition_source_id` carries **48 rows** for that MIM naming **24 distinct
   > genes** (BCS1L, COX10, DLAT, DLD, LRPPRC, MTFMT, NDUFA1, …) — **but every one of those rows
   > has an empty `AssociatedGenes` field and puts the genes in `RelatedGenes`**, which is how
   > ClinVar files multi-gene phenotypes. `pipeline/hfea_crosswalk.py` read only `AssociatedGenes`,
   > so all 48 were dropped silently. **That is an absence produced by our reader, not by the
   > register** — precisely the defect this document exists to find in someone else's data.
   > **Both fields are now read.** Leigh Syndrome goes **0 → 24 genes**, and eight other multi-gene
   > phenotypes gain genuine entries: Craniosynostosis 1 (1→4), Usher Syndrome USH1 and USH1B
   > (2→5), Mitochondrial DNA Depletion Syndrome 15 (1→4), Cerebral Cavernous Malformations (3→4),
   > Phenylketonuria (1→2), Pyridoxine-Dependent Epilepsy (1→2).
   >
   > 🔴 **AND A NULL WAS PUBLISHED AS A GENE.** HPO uses `-` as its null `gene_symbol` in **10
   > rows**, two of them OMIM:176270 (Prader-Willi). `read_clinvar()` filtered `sym != "-"`;
   > **`read_hpo()` did not, and `"-"` is truthy** — so the shipped index JSON carried a literal
   > **`"-"` key** and the CSV's Prader-Willi row read `genes=-;HERC2;IPW;…` with `n_genes=11`.
   > **The same guard is now in both readers.** PWS is **11 → 10**, the `"-"` key is gone, and the
   > index goes 1,778 → 1,782 keys. **The row count is unchanged at 2,063**, so no headline
   > denominator moves.
   > **[OUR MEASUREMENT — both bugs re-derived from the source files 2026-08-31: 48 rows / 0
   > `AssociatedGenes` / 24 `RelatedGenes` for MIM 256000; 10 HPO rows with `gene_symbol == "-"`.]**
6. **UK only.** Other countries run their own registers.

## 7. Reuse

Released **CC BY 4.0**. The intended users are families, genetic counsellors, clinical genetics
services and other rare-disease teams. It may be reused, corrected, or absorbed into the register
itself — the last of those would be the best possible outcome, and would make this file obsolete.

*Built for a hackathon about one child. The missing column was never about one child.*
