# Functional-rescue research decision prototype

This dependency-free Python program checks the logical application of the [functional rescue plan](../../submissions/functional-rescue-plan.md), revision 23 October 2026. It classifies supplied estimates and qualification assertions; it does not estimate treatment effects, establish an N1002K defect, demonstrate rescue or make medical decisions. **It is a research prototype, not a medical device or biological evidence.**

The strongest output is `REPLICATION_CANDIDATE`: a signal eligible for independent research replication under the supplied programme rules. It is not successful replication, clinical advancement or permission to treat anyone. The existing laboratory protocol still needs pilot data, laboratory design review and registration.

## Run locally

From the repository root, Python 3.9+ and its standard library are sufficient:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/rescue_decision/decision.py /path/to/decision-input.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_rescue_decision.py -v
PYTHONDONTWRITEBYTECODE=1 python3 analysis/rescue_decision/validate_cases.py
```

`decision.py` reads one local JSON file and prints its result. **Exit 0 means structurally valid input, even for negative or inconclusive decisions.** Exit 2 means invalid input or an unreadable file. Inspect `replication_candidate_ids` and every contrast's `decision`; never interpret the exit code as efficacy. No network, external dependencies or input-file modification is involved.

`validate_cases.py` runs only the new focused test suite and the frozen cases, prints a provenance-bearing JSON report, and exits 1 on a failed expectation or test. Seven single-edit faulty versions of our own evaluator are also executed in memory: the frozen cases must detect each fault. No source files are modified; this bounded mutation check is not comprehensive coverage. The retained result is [rescue-decision-validation.json](../../submissions/rescue-decision-validation.json). The report records hashes of the implementation, test source, protocol at specification, and expected-case file.

The `baseline` object in `expected-cases.json` is a complete **synthetic input example**, not a default laboratory protocol. Do not adopt its thresholds or its three illustrative cultures as a power calculation. The remaining cases apply documented JSON-pointer changes to that baseline. Their expected labels were specified before the evaluator existed; the freeze receipt records a preimplementation addition of explicit fate qualification checks. Expected labels were not generated from the evaluator. The same developer authored both; no independent human adjudication or trusted external timestamp is claimed.

`protocol-at-specification.txt` retains the exact protocol bytes used when the casebook was frozen, recovered from local commit `ad435c8` and checked against the original hash. The current protocol later added native-RNA, comparative-compound and tissue-output considerations without changing these bounded decision rules. The report retains both hashes. The initial provenance test incorrectly required the evolving document to retain its historical hash; it now verifies the immutable snapshot instead, leaving every expected decision unchanged.

## Decision contract

Δ is the reduction in segregation-error probability versus vehicle, in absolute probability units. δ must be supplied by a registered, pilot-justified programme plan; there is no default. For the supplied multiplicity-accounted-for CI [L,U], **L > δ** passes the functional-benefit criterion, **U < δ** rules out the programme's worthwhile benefit at the tested exposure, and either boundary touching δ or an interval crossing it is inconclusive. Comparisons use decimal values without tolerance or rounding; JSON decimal precision is retained. Already-rounded upstream results cannot be recovered.

The four fate intervals are separate from efficacy: treated/vehicle division-rate ratio, treated-minus-vehicle excess death, excess persistent arrest, and excess censoring. A ratio must lie wholly above its minimum; each excess-risk interval must lie wholly below its maximum. Whole intervals on the harmful side fail. Touching or crossing a bound is inconclusive. **This strict-interior fate convention is a conservative implementation choice**, explicitly named in the input plan, not a clinically validated threshold or an additional empirical finding in the protocol. Other conventions require a separately reviewed version. Selection must be explicitly assessed as excluded; detected selection blocks, unresolved selection is inconclusive.

Decisions have the following meaning and precedence:

1. `INVALID_INPUT`: a missing, malformed or inconsistent input anywhere blocks the whole evaluation. No candidate is returned, including when a sibling contrast is malformed. This is a conservative software rule, not biological evidence of no effect.
2. `TECHNICALLY_INDETERMINATE`: an unqualified model, unfrozen plan, failed measurement/control, uncollected required secondary, unresolved HSP measurement, unaccounted nesting/multiplicity or unqualified fate coverage prevents interpretation. Failed controls cannot produce a biological negative. Raw interval relations are retained as arithmetic only.
3. `DO_NOT_ADVANCE`: qualified inputs show a failed fate/selection gate or an exposure outside the independently qualified window. This does not establish that the molecule or class is ineffective.
4. `WORTHWHILE_BENEFIT_RULED_OUT`: qualified functional inputs have U < δ. This is specific to the supplied programme threshold, exposure, system and window. Other uncertain fate findings remain visible.
5. `INCONCLUSIVE`: efficacy touches/crosses δ or a required fate/selection criterion is unresolved.
6. `EXPLORATORY_SIGNAL`: all numerical and qualification gates pass for an explicitly exploratory contrast. It cannot enter the replication-candidate list as a confirmatory finding.
7. `REPLICATION_CANDIDATE`: a supplied confirmatory contrast passes all declared gates. Independent replication and interpretation are still required.

A qualified absent HSP response with positive function remains eligible for replication and receives `HSP_DISCORDANT_INVESTIGATE`. Present HSP response is labelled `HSP_RESPONSE_PRESENT_NOT_CAUSAL`. Neither establishes HSP-mediated rescue. A BubR1 rise or improved fraction of normal survivors never overrides efficacy, exposure, selection or fate checks.

## Input semantics and provenance

The complete structural template is the baseline JSON; unknown fields, duplicate JSON keys, numeric strings, numeric booleans, NaN and infinities are rejected. All required records must be nonempty. Qualification flags must be actual JSON booleans. These are explicit assertions the caller must substantiate; the program does **not** inspect referenced records or decide whether a pharmacology review, control or pilot is adequate.

- `model` supplies laboratory qualification of the full-length model and controls. The Stage 1 abundance-matching / functional-equivalence classification is **outside this program**; neither abundance-limited nor function-limited N1002K is assigned. Domain membership or protein abundance cannot supply that classification.
- `plan` declares the frozen eligible comparison family, δ, confidence level, follow-up window, observation handling, biomarker schedule, design/exclusion records, pilot/power records and separate fate bounds. Every contrast eligible to trigger advancement must be listed. The supplied confirmatory contrast IDs must match that family exactly; all results are returned. An omitted declared member blocks evaluation. An undeclared experiment or dishonest declaration cannot be detected.
- `multiplicity` identifies a prespecified single contrast, Bonferroni, simultaneous-model or other documented interval-coverage method. More than one eligible contrast cannot use the single-contrast method. `analysis.multiplicity_adjusted=true` declares that family coverage has been accounted for (including no adjustment required for one prespecified contrast). **The validator does not perform or verify the adjustment.** Fate interval coverage has its own `coverage_qualified` assertion and record; appropriate coverage for the joint decision must be established by the analyst.
- `exposure` records measurement qualification separately from being within the reviewed exposure window. Both are needed. Compound form, active-moiety basis, matrix, sampling time, total/unbound status and binding context must be declared. The quantitative exposure/pharmacology review belongs in the referenced record. No serum-to-intracellular conversion or universal concentration cutoff is inferred by this program.
- `assays` declares function-control qualification, independent response-control qualification, completion of **all** required secondary measures and their acceptance records. The single completion assertion covers alignment/checkpoint/mitotic duration, BubR1 abundance/localisation, viability/apoptosis, division and cell-cycle measures; it is not evidence those experiments occurred. `protein_ratio` is a nonnegative measured ratio; the optional comparator-only `survivor_normal_fraction_change` can be `null` if unmeasured. Neither selects candidates.
- `analysis` provides an already fitted, replicate-aware CI, its confidence level and independent-culture counts. `nesting_handled` must cover both functional and fate analyses. The confidence levels for primary and fate intervals must equal the frozen plan. No variance, sample-size adequacy or model correctness is inferred from culture counts.
- `observations` retains every independent culture per arm, including zero-division cultures. The schema supports only the first completed division per starting cell: `mitotic_entries` is the number of starting cells with at least one entry, `completed_divisions` the number completing the prespecified first division, and `segregation_errors` the number of those divisions with at least one prespecified error. Thus errors ≤ completed divisions ≤ entrants ≤ starting cells. Death, persistent-arrest and censoring counts each use starting cells as denominator, may overlap according to the registered observation definitions, and are not summed into a partition or recoded as segregation errors. An arm with no completed divisions has no conditional primary endpoint and is rejected. Actual repeated-division event counts are unsupported and require another reviewed design.
- `fate` provides separate measurement qualification, interval coverage, confidence level, fate estimates and selection assessment. Counts are reported beside these estimates; the program does not recompute hierarchical estimates by pooling cells or verify consistency between model outputs and source images. Record links must supply that traceability for real use.

Three illustrative cultures, any finite CI, and a nonempty pilot-record string do not establish power or honest analysis. A qualified Stage 1 model remains an asserted prerequisite. Actual model, assay, exposure and selection qualification, statistical review and independent replication require laboratory work.

## Comparator limits

The two deliberately incomplete rules accept protein ratio > 1 or a positive change in normal-cell fraction among survivors. They represent failure modes, **not named competitors' software or complete proposals**. The report separates all-input counts from a comparison restricted to structurally valid inputs, so malformed-input cases do not inflate the latter comparison. The fixed case collection deliberately overrepresents failures and boundaries. Its counts are protocol conformance results, not biological false-positive rates, sensitivity, specificity, expected clinical impact or evidence of comparative dominance.

No statistical simulation is included. Without measured baseline variance, overdispersion and usable divisions per independent culture, a claimed assay operating characteristic would depend on invented pilot assumptions. The illustrative intervals are input fixtures, not intervals fitted from their illustrative counts. This deliverable adds executable decision discipline; it does not close the experimental efficacy gap.
