# Compartment matching, and the branch point a therapy proposal has to choose

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. The branch point

A pseudokinase-domain missense can be pathogenic in **two mechanistically distinct ways**, and a
therapeutic proposal is only coherent once it commits to one:
1. **Destabilise the fold** → less total protein → a *quantitative* deficit. Treatable in principle
   by anything that raises the amount of protein.
2. **Break a scaffolding interaction** while leaving the fold intact → a *qualitative* defect.
   Raising the amount of a protein that cannot do its job achieves nothing.
**[OUR INFERENCE — the two-branch framing is ours, drawn from the published observation that kinase-domain missense variants in this family act both by destabilisation and by loss of scaffolding contacts. Which branch THIS variant sits on is unmeasured, and that is the point of §1.]**

**This child's variant has not been assigned to a branch**, and that assignment — not the choice of
drug — is the decision the whole therapeutic argument turns on. The experiment that settles it is
cheap, and it is specified in the wet-lab protocol accompanying this work.

## 2. Compartment matching — why most chaperone proposals are aimed at the wrong place

If the lesion is branch 1, the obvious move is a chaperone-axis drug. But **chaperone systems are
compartment-specific**, and BubR1 is a soluble cytosolic/nuclear protein.

| agent | compartment it acts on | matched to BubR1? |
|---|---|---|
| **arimoclomol** (HSF1/HSP70 axis; FDA-approved Sept 2024, paediatric ≥2 y) | **cytosolic** | ✅ **yes** |
| TUDCA, 4-PBA | endoplasmic reticulum | ❌ no |

**A drug that corrects folding in the ER cannot correct a misfolded cytosolic protein**, however
good its safety record. That single filter removes most of the chaperone-axis candidates that
appear in rare-disease repurposing lists.

> This is a *screening* argument, not a treatment recommendation. It says which candidates are
> **not worth testing**, which is the cheaper half of a therapeutic programme.

## 3. 🔻 What we are NOT claiming, because we measured it

**This is not novel to us.** Re-measured at the 50-archived-owner denominator:
**`arimoclomol` appears in 6 of 50 competitor repositories**, and at least one team ranks it **#1**,
justified as *"mechanism matched exactly to the temperature-rescuable folding defect"*. One entire
competing submission is built on the same abundance-rescue question.

**[OUR MEASUREMENT — grep over `archive/competitors/`, every hit read by hand, 2026-08-29.
An observation about competitors' documents, never evidence about the biology.]**

**Our contribution here is the compartment filter and the branch point, not the drug.** Several
teams arrive at the same molecule; the argument we can defend is *why most of its neighbours are
excluded* and *what experiment decides whether any of them could work at all*.

## 4. The honest position

The therapeutic branch of this work is the **weakest** part of it, and the numbers say so: 25–40%
that a screen yields any compound raising BubR1 two-fold, **well under 10%** that anything reaches
a child. It is included because a mechanism actively tested and found wanting is a different
epistemic state from one never examined — and because the branch point is a real, cheap,
decidable question that nobody has answered.
