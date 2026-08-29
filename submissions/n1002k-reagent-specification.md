# Build specification: the *BUB1B* N1002K construct that does not exist

**Every therapeutic claim about this child — ours and three competing teams' — is extrapolated from
other people's variants, because no N1002K reagent exists anywhere. This is the document that ends
that, for a few hundred dollars.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. The gap, stated plainly

| what exists | what it is |
|---|---|
| `GM21284` (Coriell) | a real MVA patient line — but genotype **`753X` / `R814H`**, not this child's |
| Addgene **#114052 / #114061 / #114062** | wild-type, `K795A`, `D882N` BubR1 — Kops lab, publication-linked |
| Addgene **#23858** `pDONR223-BUB1B` | full-length ORF, Gateway **entry** clone |
| **an N1002K construct** | ❌ **does not exist, anywhere** |

So the dose–response curves, the stability data, the chaperone-dependence result — all of it is
`753X/R814H`, `K795A`, or mouse. **The specific allele this child actually carries has never been
put in a tube.** Until it is, every claim about it is an argument.

## 2. The edit, verified at sequence level

| | |
|---|---|
| variant | `chr15:40,220,612 T>G` (GRCh38) · `c.3006T>G` · **p.Asn1002Lys** |
| codon | **`AAT` (Asn) → `AAG` (Lys)** — third base |
| context | `…GATTCTGAA[**T**>G]GCCAATGAT…` |

**[OUR MEASUREMENT — extracted directly from `GRCh38_no_alt_plus_hs38d1.fna` and translated; the
reference base returned `T`, matching the VCF. Not taken from an annotation.]**

## 3. Two routes, and the recommendation is the less obvious one

The protocol's route **A2** needs the **HIS₆-BubR1 (721–1,044)** pseudokinase-domain fragment —
**324 residues, 972 bp of CDS.**

### ★ Route 1 — SYNTHESISE the mutant fragment (recommended)

At ~1 kb, **synthesis is now cheaper and faster than mutagenising and subcloning**, and it arrives
**sequence-verified**. Order the 721–1,044 fragment twice — once wild-type, once carrying
`c.3006T>G` — with the flanking sites your destination vector needs.

- No template to source, no mutagenesis, no screening of colonies.
- **The WT arrives from the same synthesis run**, so the pair differ by exactly one base and share
  every other property. For a ΔTm measurement between two constructs, that matters more than cost.
- ⚠️ Codon-optimise **nothing**. A ΔTm comparison requires the two constructs to be identical
  outside the edit; optimisation would silently break that.

### Route 2 — site-directed mutagenesis from Addgene #23858

Use if a full-length ORF is wanted for cell work rather than the bacterial fragment.

**Mutagenic primer pair, designed and checked here** (QuikChange-style, complementary, mismatch
centred at position 18 of 35):

```
FWD 5'-TTTGTGCGGATTCTGAAGGCCAATGATGAGGCCAC-3'    35 nt · Tm 80.4 °C · GC 51.4%
REV 5'-GTGGCCTCATCATTGGCCTTCAGAATCCGCACAAA-3'
```

Tm exceeds the ≥78 °C the method requires; both ends terminate in C/G.

> ### 🔴 #23858 has NO STOP CODON, and the depositor says so
> Verbatim: *"The ORF has **no Stop codon**… **Do NOT use this plasmid directly for
> transfections.**"* It is a Gateway **entry** clone. After mutagenesis it **must** be recombined
> (LR) into a destination vector supplying a tag and a stop codon. **Skipping that step yields a
> read-through product**, and the protocol did not originally name it.

## 4. 🔻 An error in this document's own first draft, recorded

The first version of §3 included Sanger primers annealing **~300 bp either side of the edit,
designed against the genome.** That is wrong and would have wasted a lab's time: **the construct is
an ORF clone and contains no intron.** The CDS block holding the variant is
`chr15:40,220,564–40,220,759` — **only 48 bp of coding sequence upstream and 147 bp downstream.**
Genomic primers at ±300 bp anneal to sequence that is not in the plasmid.

**Corrected recommendation: whole-plasmid sequencing, not primer-walking.** It needs no primer
design, verifies the entire construct rather than a window, and — the reason that matters here —
**catches second-site mutations that polymerase-based mutagenesis introduces elsewhere in the
plasmid**, which a targeted amplicon cannot see.

## 5. Quality control — what must be true before the construct is used

1. **Whole-plasmid sequence**, matching the intended sequence with **exactly one difference from
   wild-type**. Not "the edit is present" — *only* the edit is present.
2. **The WT counterpart sequenced in the same run**, from the same source.
3. Expression checked by SDS-PAGE before any Tm measurement; a construct that does not express
   cannot produce a melting curve, and a flat curve would otherwise be read as a result.
4. ⚠️ **Include a construct with a published expected value** — `K795A` (Addgene **#114061**) is the
   allele the assay's own calibration comes from. **A run that cannot reproduce a published value
   cannot interpret a novel one.**

## 6. Costs

| item | estimate |
|---|---|
| synthesised fragment ×2 (WT + N1002K), ~1 kb each | **$150–400** |
| *or* Addgene #23858 + mutagenesis kit + LR reaction | ~$94 plasmid + reagents |
| Addgene control plasmids (#114052, #114061) | ~$**2 × 80–100** |
| whole-plasmid sequencing ×3 | ~$45–75 |
| **total, reagents only** | **~$400–700** |

**[OUR ESTIMATE. Addgene's $94 for #23858 is `[VERIFIED]` from the plasmid page; synthesis and
sequencing prices are current market ranges and MUST be re-quoted before ordering. Consumables,
instrument time and labour are `[NOT ESTIMATED]` and are not invented here.]**

## 7. What this does not include, and what needs a person

- 🔴 **A laboratory.** Nothing here can be ordered by us. This is a specification, not a purchase.
- Addgene plasmids are **academic/non-profit only** and need an MTA.
- Route A2's original bacterial vector (`NKI-His-3C-LIC-kan`) is an in-house vector and **is not
  deposited** — hence the recommendation to synthesise with sites for a *commercially available*
  destination vector instead, which removes a request to another lab entirely.
- **Availability and prices must be re-checked.** Every catalogue figure here has a date on it.

## 8. Why this is worth doing even if the therapeutic idea fails

**The construct outlives the argument.** Whatever the stability result says, a sequence-verified
N1002K reagent is a permanent, orderable object that any laboratory can use to ask any question
about this allele — including questions nobody has thought of, and including questions asked after
everyone involved here has moved on.

Every other output of this project is a document. **This one would be a thing.**
