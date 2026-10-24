# Portable laboratory planning receipts

Start with [laboratory execution readiness](../../submissions/laboratory-execution-readiness.md). These files describe a proposed, currently unfunded programme, not completed laboratory work or provider acceptance. No cash-prize commitment is made; Claude Science credits apply only to eligible computation.

The 33-item [provider ledger](provider-evidence.json) retains official catalogue/tariff URLs, retrieved 24 October 2026, evidence classes and private capture hashes. No copyrighted full texts, provider-page copies, patient inputs or full reference record are shipped. Capture hashes identify retained source receipts; the public metadata snapshot cannot itself reconstruct those pages.

[Supplemental facility evidence](facility-supplement.json) retains seven dated official capture receipts and conditional UV/LUMC rates plus CRG access restrictions. It omits private paths and raw page copies; alternative tariffs do not establish an executable schedule or a full budget.

[Construct specifications](construct-specifications.json) contain only public-reference-derived insert designs and stated intended edits. They are not assembled vectors or complete duplex orders. [Proposed modules](proposed-modules.md) retain required controls, proposed settings, readouts, stop rules and optional branches. [Five unsent RFQs](quote-requests.md) and [official channels](rfq-channels.json) are retained unsent as reference specifications; contact was declined and no authorization is pending. An economical transient feasibility route and a stable-clone alternative are separately scoped.

Reproduce quantities, price arithmetic, layouts and prospective power scenarios locally:

```sh
python3 examples/laboratory-readiness/build_quantities.py
python3 examples/laboratory-readiness/verify.py
```

Run from the repository root. The generator has no network calls. The verifier rebuilds in a temporary directory and checks shipped hashes, sequence edits/translations, well counts, price classes and links. It does not qualify assays, invent missing quotes or test therapeutic efficacy. The [manifest](manifest.json) covers this directory and the six covered submission documents. Later edits require an explicit manifest refresh and re-review.

The 807-well matrix and 288 plate-hour scenario remain conditional. The proposed 3 min cycle would require 336 positions/672 images on each 42-well main plate; measured feasibility and counterbalanced culture scheduling are mandatory. The four-well optical preflight is development only. The RPE1 USD 6670 observation has unresolved price-tier eligibility. Complete project cost remains null.
