# Frozen public case selection

`frozen-cases.json` preserves the twelve-case selection and all four phenotype arms exactly as frozen before Exomiser inference. `selection-plan.json` specifies quotas, seed, eligibility and source archive hash. `prepare.py` can reconstruct the selection from the fixed public archive. Keep the upstream BSD-3-Clause license in `source/` with derived records.

This file records preparation, not an executed benchmark. The source-label and runtime limitations in the [evaluation recipe](../README.md) apply. The final public result includes separate truth-adjudication and execution records.
