# Three-minute pitch kit

Two local versions share six visuals and a 177-second timeline:

- `pitch-narrated.mp4`: 1080p H.264/AAC with neutral synthetic English narration (macOS Samantha) and an optional English subtitle track.
- `pitch-silent.mp4`: the same video frames without audio, ready for participant narration.
- `pitch-editable.pptx`: editable text, preserved six-slide design and an actual navigator screenshot.
- `pitch-slides.pdf`: matching static visuals.
- [Timed recording script](../pitch-video-script.md), `storyboard.json` and `timing.json`: spoken text and exact slide boundaries.
- `pitch-captions.srt`: editable sentence captions. Boundaries follow individually synthesized speech segments, rather than a proportional word-count estimate. This is sentence alignment, not phoneme-level forced alignment.
- `navigator-demo.png`: actual TGFB1 lookup in the current local navigator. The cystic-fibrosis row retains condition-level approval and visible Mendelian/polygenic source descriptions. The capture changes no source data or page content.

The script contains **390 spoken words**. The synthetic version uses Samantha at a requested 175 words per minute, with measured speech durations and padding to the fixed timeline. It is a reviewable alternative, not a recording of the participant. No voice cloning is used. For the participant version, record the script while watching the silent video and keep the final export under three minutes.

Slide 3 now shows all four formal gates A–D. Slide 4 reports 28 selected queries and review of all 47 returned gene–row associations, with the shared-source developer-evaluation limit explicit. Slide 5 describes the implemented decision prototype's 40 frozen synthetic cases and retains the separate six SpliceAI controls and nine checker faults. Software verification does not establish biological rescue or clinical accuracy. The pitch makes no Exomiser result claim.

All six exported slides were rendered and visually inspected. Package, slide-count, font-policy and layout checks, caption/script consistency, encoded stream properties and measured audio checks are recorded in `dossier/sweeps/evidence-2026-10-23/delivery/pitch-rubric-qa.json` in the working project. The deck has not been opened in native PowerPoint. Automated audio checks and sentence boundaries cannot establish pronunciation quality or user comprehension; a human listening pass remains advisable before choosing the synthetic version.

The files remain local and unsubmitted. No external pitch URL exists. Final screenshot/video capture and publication are separate decisions.

## Rebuild notes

The two maintained source builders are in `dossier/sweeps/evidence-2026-10-23/delivery/`: `build-slides.mjs` edits a copy of the original deck and `build-video.py` synthesizes local speech, encodes both variants, and writes script/captions/timing plus the slide PDF. The original deck is recoverable from nested-repo commit `6e2152d`, path `submissions/pitch/pitch-editable.pptx`, with SHA-256 `2704d7f8ed1c1f7a849dcba4c83fd0b7656f78c46a369fc4d74be98d60529fb8`.

The slide builder accepts that reference as its first argument, uses the bundled Artifact Tool runtime, and requires `RUNTIME_NODE_MODULES` for the finalizer's import check. Temporary renders and speech segments use `/tmp/mva-pitch-rubric/`. The video builder needs local macOS Samantha, FFmpeg/FFprobe and ReportLab. Empty speech outputs are rejected rather than cached as success. The presentation authoring marker was run once for this revision; the parent had already registered the slide-PDF operation.
