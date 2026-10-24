# Independent compact benchmark audit — TERMINAL_AUDITED

Observed 2026-10-24T09:17:53.498417+00:00. Auditor SHA256 `b71784f394d5f36aeef8199369865c0959f0cc9927873586d50db307339a2f39`.

Execution status: **completed**. Checks: 7; errors: 0.

The adjacent JSON retains every checked hash, all case/arm outcomes, fixed-denominator metrics, source-allele/mode details, serialization evidence and original-versus-none deltas.

The literal frozen-reader result and independently interpreted NON_DEFAULT result are separate. The latter does not silently replace the former.

Serialization omission changes status for 726 case/arm outputs; see the enumerated JSON ledger.

literal_frozen_reader:

- original: full-source-allele top-1/5/10 [547, 626, 632] / 681; gene denominator 245; MRR 0.850711.
- none: full-source-allele top-1/5/10 [0, 0, 0] / 681; gene denominator 245; MRR 0.000000.

NON_DEFAULT_aware_independent:

- original: full-source-allele top-1/5/10 [556, 653, 665] / 681; gene denominator 245; MRR 0.873546.
- none: full-source-allele top-1/5/10 [430, 649, 665] / 681; gene denominator 245; MRR 0.752084.

HPO mapping qualifications:

- TC_e5bbd96c3cea24cd (NAV3): HP:4000064; full unchanged HPO list and runtime context in JSON.
- TC_ea40e72573ec996f (NLRP7): HP:0020003; full unchanged HPO list and runtime context in JSON.
- TC_c0d89254e82b7968 (NLRP7): HP:0020003; full unchanged HPO list and runtime context in JSON.
- TC_f170f73410ee740c (NLRP7): HP:0020003; full unchanged HPO list and runtime context in JSON.

Limitations:

- Constructed ten-hypothesis source-label recovery, not clinical accuracy, whole-genome validation, a temporal model-knowledge holdout, therapeutic benefit or competitive superiority.
- Our 713 signatures / 261 genes are not the authors' unresolved 719 cases / 265 genes. The cited primary clinical papers are unadjudicated.
- All 713 cases and all genes remain in each arm's appropriate denominator, including four preparation failures. X/PAR ploidy is technical-only; phase is unasserted.
- Current 2512 gene/disease/HPO/ClinVar knowledge remains. Benign synthetic decoys may filter out; input hypotheses and emitted/PASSED gene universes are distinct. Top-10 can be trivial.
- The ledger and every prepared VCF/job are checked independently here. ClinVar source eligibility, source literature and reference normalization are not rerun; their retained preparation receipt hashes are checked.
- A missing PASSED-only output allele does not identify the pipeline stage or reason it disappeared. An empty hash-verified output means zero emitted genes, not a known biological cause.
- Raw missing contribution/whitelist flags and missing contributing-variant lists remain unknown. No union across different inheritance modes establishes joint recovery.
- Missing mode combinedScore is zero only in the separately identified serialization-aware view, supported by installed primitive-double bytecode and NON_DEFAULT writer configuration. Explicit null/nonfinite/bool values remain invalid. The frozen evaluator view is retained independently.
- Database receipt hashes and installed software are verified, not multi-gigabyte database payloads. Nothing is uploaded, altered in the frozen run, or committed by this auditor.
