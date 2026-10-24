# Three-minute pitch kit

Two local versions share six base slides and a **177-second** timeline:

- `pitch-narrated.mp4`: 1080p H.264/AAC with neutral synthetic English narration (macOS Samantha) and an optional English subtitle track.
- `pitch-silent.mp4`: identical video frames without audio, ready for participant narration.
- `pitch-editable.pptx`: editable text and native candidate-comparison and credit-allocation tables, with actual local application screenshots. Slide 4 shows the first replay state.
- `pitch-slides.pdf`: six matching static base slides.
- `replay-state-1.png`, `replay-state-2.png`, `replay-state-3.png`: the three displayed demo states used within slide 4's video segment.
- [Timed recording script](../pitch-video-script.md), `storyboard.json` and `timing.json`: spoken text, slide boundaries and the exact frame of each demo transition.
- `pitch-captions.srt`: editable sentence captions aligned to individually measured speech segments. This is sentence alignment, not phoneme-level forced alignment.
- `navigator-demo.png`: actual BUB1B lookup in the current local navigator. It shows the condition-level register status and visible source descriptions. The capture changes no source data.

The script contains **394 spoken words**. Samantha uses a requested rate of 175 words per minute, with measured speech durations and padding to the fixed timeline. This is a synthetic alternative, not a recording of the participant. For the participant version, record the script while watching the silent video and keep the final export under three minutes.

## What the pitch shows

The comparison presents the different evidence strengths for arimoclomol, NMN and 4-PBA. It does not rank demonstrated MVA efficacy. The proposed experiment separates variant function, measured exposure and cell fate; laboratory acceptance, imaging qualification and complete costs remain open.

Slide 4 displays three recorded executions of the actual Python decision implementation: worthwhile benefit ruled out, do not advance, and technically indeterminate. The video changes state at the corresponding narration sentence. Open the [offline viewer](../../examples/rescue-decision-demo/replay.html) or use its [replay instructions](../../examples/rescue-decision-demo/README.md). These are existing synthetic fixtures, not additional validation cases or drug results. Their intervals are supplied, and were not fitted from the accompanying counts.

Slide 5 shows the actual navigator and its 28 selected-query/47-association developer audit, with shared-source and clinical-validity limits. The separate 713-signature benchmark measures constructed source-label recovery. Slide 6 shows the conditional $12,000 Claude Science credit allocation and concrete outputs. It commits no cash prize to research and does not fund laboratory work.

## Verification and remaining review

The working project's `dossier/sweeps/evidence-2026-10-24/deadline-review/pitch-qa.json` records checks of the exact exported deck, native tables, captions, measured speech, demo timing and encoded video streams. Six slides and all three demo states are visually reviewed during release preparation. The deck has not been tested in native PowerPoint. Audio levels and exact sentence timing cannot establish pronunciation, prosody or comprehension; a human listening pass remains advisable before choosing the synthetic version.

The files remain local and unsubmitted. No external pitch URL exists.

## Rebuild notes

The current builders are in the working project's `dossier/sweeps/evidence-2026-10-24/delivery/`: `capture-demo.mjs`, `build-pitch.mjs`, `build-pitch-video.py`, `verify-pitch-import.mjs` and `verify-pitch.py`. The previous builders are historical. The current scripts use the bundled Artifact Tool runtime, macOS Samantha, FFmpeg/FFprobe, ReportLab and the authorised external build directory `/Volumes/easystore/MVA-deadline-build-20261024/pitch/`. No patient data enters that directory.

The slide builder preserves Arial and the existing 16:9 dimensions, validates a new versioned candidate and receipt, then installs the local output. `RUNTIME_NODE_MODULES` is required by the finalizer. A new presentation authoring marker was run once for this revision. Prior immutable release archives preserve the older deck and media.
