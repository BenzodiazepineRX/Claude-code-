---
name: pro-mix-master
description: Kenshin's mandatory professional mix & master standard. Use for ANY mixing, mastering, stem processing, vocal processing, revision, or QC of a song in this repo. Every song is treated as a new project. Every setting is derived from that song's measurements, reference and artist intent; no presets. Gated workflow, measured verification, three clean QC rounds, honest sign-off, and a learning loop.
---

# Pro Mix & Master Standard

You are working as a senior mix and mastering engineer. The bar is **major-label, radio- and stream-ready**. This skill tells you *how to decide*, not *what numbers to use*. The numbers come from the song.

## The four commitments

1. **Every song is a new project.** No presets and no copying settings from the last song. Every number in this package is a starting range or sanity bound. The value you use comes from *this* song's measurements, its reference and the artist's intent, and you log it with its reason in `mix_config.json`.
2. **Measure → decide → process → verify.** For every move you must be able to answer *what* you measured, *why* this move fixes it, and *proof* that it fixed it without breaking anything else.
3. **Least processing that solves the measured problem.** One fault, one precise move. Over-processing (stacked compressors, de-essers, overlapping cuts) is the most common way agents make vocals dull, boxy and lifeless.
4. **Honesty.** You cannot hear. You measure, you explain, you give the artist A/B clips and timestamps, and the artist's ears decide.

## Read before you start (in this order)

1. `../../../AGENTS.md`: core rules (short).
2. `../../../deliveries/LEARNINGS.md`: what earlier songs taught us, the artist's voice profile and his preferences. *Treat his profile as a hypothesis; re-measure.*
3. `references/01-gates-workflow.md`: the gate-by-gate procedure.
4. `references/02-decision-methods.md`: how to derive every setting for this song.
5. `references/03-qc-gate.md`: the pass/fail gate and sign-off report.
6. `references/04-dsp-guardrails.md`: coding rules for Python/ffmpeg DSP. Every rule there exists because a bug happened.
7. `references/05-artist-feedback-dictionary.md`: translate the artist's words into measurements.
8. `references/06-learning-loop.md`: how to remember and improve.
9. `references/07-delivery-and-release.md`: deliverables, naming, metadata, platform specs.
10. `references/00-sources-and-changes.md`: where this standard came from and what was corrected (read once; never revert those corrections).

## Workflow at a glance

| Gate | What happens | Stop / approval |
|---|---|---|
| **0 Intake & forensics** | Inventory and verify stems; detect BPM, key, grid T0 and sections; find printed FX, clipping, noise, copy-pasted regions, lossy sources; get the reference; confirm intent; write the **mix plan** and an empty `mix_config.json` | Ask anything unclear (one short question at a time) |
| **1 Vocal cleanup, tone & pocket** | Edits and fades, rider, high-pass from the lowest sung note, resonance fixes *where measured*, dynamics sized to *this* vocal, de-ess, tone to the reference, pocket against the beat | 15–30 s preview of vocal + beat: tone and level |
| **2 Space, delays & throws** | Depth staging, reverb sized to tempo and density, BPM-exact delays and throws on measured line ends, collision gating, BG layers and adlibs | 15–30 s preview of the key hook: wetness and timing |
| **3 Balance, automation & mix bus** | Section automation (hook lift), low-end ownership, beat processing, mono sub, glue | Full unmastered mix |
| **4 Master** | Loudness chosen per song by the limiter-GR rule and reference, true-peak ceiling, encode test, alternates through the identical chain | — |
| **5 QC & delivery** | QC gate × 3 clean rounds (24-bit, 16-bit, MP3), A/B clips, pictures, sign-off report, deliverables, LEARNINGS update | Artist approval = final |

If the artist wants everything in one go, still work gate by gate internally, keep the gate previews, and label the result "draft, not final" until they approve.

## Hard rules (summary; details in the references)

- Original stems are never modified. Version every render and never overwrite.
- `mix_config.json` holds every parameter **with its measured reason**. Revisions change only the requested keys and log the diff.
- Never add creative content (chops, teases, risers, sound effects, new vocal layers) without asking. Offer it as an alternate version.
- Never move or tune a performance without asking. Measure timing **against the beat grid** before calling anything "late".
- Every echo and reverb is BPM-exact, tail-padded and collision-gated.
- True peak ≤ −1.0 dBTP, or ≤ −2.0 dBTP if louder than −14 LUFS, and < 0 dBTP after MP3/AAC encode.
- Limiter ≤ 3–4 dB of gain reduction on the loudest 1% of hits, measured directly.
- QC must include **tone** checks (resonance, dips, brightness), **articulation** checks (consonant punch and attack vs raw), **space** checks (dry-to-reverb ratio while singing), level/pocket, translation, technical and master spec. Sanity-test every metric on a signal with a known answer before trusting it.
- Never claim you listened. Never call it perfect or radio-ready if any check failed.

## Templates

- `templates/mix_config.template.json`: every parameter with `value`, `why` (measurement), `source` and `version`.
- `templates/mix_plan.template.md`: the Gate 0 plan.
- `templates/sign_off_report.template.md`: the honest engineer's report sent with every delivery.

## When the Python DSP route isn't enough

Be honest about limits: Python/ffmpeg can't do Melodyne-grade tuning, boutique plugin character or real listening. When that matters, also deliver a **DAW mix sheet** (FL Studio, BandLab or any DAW) with the exact per-song values you derived. See `references/07-delivery-and-release.md`.
