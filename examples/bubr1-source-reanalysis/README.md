# Published BubR1 rescue: source-data reanalysis

Run offline with Python 3, without extra packages:

```sh
python3 examples/bubr1-source-reanalysis/analyse.py
```

The observations retain workbook cell addresses, source URLs and hashes. The
experiments are the authors' experiments. We independently recomputed selected
summaries and checked the key observations against the original workbooks with a
second extraction. This is not new biological replication.

- **Zhang 2023, PMID 37118121**, DOI [10.1038/s43587-023-00361-w](https://doi.org/10.1038/s43587-023-00361-w):
  in HGPS fibroblasts, mean aneuploid-metaphase percentages reproduce as 31.67
  (mock), 17.67 (UPCP) and 25.33 (UPCP plus BUBR1 knockdown), from three reported
  experimental percentages per group. Underlying metaphase counts are absent.
  Mutant-mouse survival medians reproduce as 100 and 117 days, with 17 and 15
  events. The WT column has ambiguous coding and is excluded. The correction
  [10.1038/s43587-023-00427-9](https://doi.org/10.1038/s43587-023-00427-9) relabels
  Fig. 7a/e/f as esophagus and the Fig. 7f measurement as lamina propria. Some
  source attachments retain the old aorta/adventitia labels; those panels do
  not demonstrate aortic rescue.
- **Song 2024, PMID 39516273**, DOI [10.1038/s42003-024-07205-2](https://doi.org/10.1038/s42003-024-07205-2):
  Figure 3e medians reproduce as approximately 40 minutes for WT, 80 for the
  engineered T600A/T608A construct, and 40 for either enhanced Plk1- or B56-binding
  rescue construct. The seven groups retain all 271 supplied cell observations.
  All seven printed counts and rounded medians agree. Cells are not independent
  biological replicates; replicate nesting is unavailable.

Song's peer-review responses acknowledge that a strict SAC-silencing assay was
not performed. Nocodazole-arrest duration must not be relabelled as silencing
kinetics, and cellular PLK1 dependence does not establish direct PLK1
phosphorylation of BubR1 T600/T608.

Other inspected panels retain discrepancies: Fig. 1b WT median approximately
50 versus printed 40; Fig. 1e WT 685 versus printed 690; S4b siBubR1 41 values
versus printed 43; Fig. 3c 2A+WDR47 165 kinetochores versus printed 150.
The five-minute difference may reflect rounding. We do not silently remove
observations or run new significance tests on pooled cells.

A separate whole-workbook audit found 149 source values rather than the stated
150 in Fig. 2b T620A and 2E and Fig. 2d ΔKARD+2E. In S1f, WT mean is 1.128875
and median 1, despite the legend's mean-normalization description. These panels
are not bundled in this executable example; their normalization provenance
remains unresolved. These discrepancies do not change the Fig. 3e timing
medians reported above.

These results strengthen the choice of functional controls and comparators.
UPCP acts in a progerin-associated context with endogenous BUB1B, and the genetic
rescue uses different engineered residues. Neither tests N1002K, arimoclomol,
comparative MVA efficacy or patient benefit. No result here estimates an MVA
treatment effect. See the [functional protocol](../../submissions/functional-rescue-plan.md).
