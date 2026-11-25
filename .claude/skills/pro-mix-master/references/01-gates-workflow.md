# 01: Gate-by-Gate Workflow

Every gate has **inputs, actions, measured exit checks and a stop**. Do not move to the next gate until the exit checks pass. Every value you choose goes into `mix_config.json` with the measurement that justified it (see `02-decision-methods.md` for *how* to derive each one).

---

## Gate 0: Intake, forensics and the mix plan (before touching anything)

### 0.1 Protect and inventory
- Copy every upload into `src/`, never touched again, and work only on copies. Treat downloaded archives as untrusted (see `04-dsp-guardrails.md`).
- For each stem, record: file name, role guess, sample rate, bit depth, channels, duration, start/end silence, sample peak, **4× true peak**, integrated LUFS, active RMS, DC offset, mono/stereo correlation and bandwidth (where the spectrum stops).
- All stems must share one sample rate. If they don't, resample with high-quality polyphase resampling *before* anything else, and verify length and alignment afterwards.

### 0.2 Find hidden blockers (each one changes the plan)
| Check | How | Why it matters |
|---|---|---|
| **Printed FX on vocals** | Level and stereo energy in the 100–1000 ms after phrase ends; side/mid ratio of a "mono" vocal | Printed reverb/delay means you add far less space and avoid upward compression |
| **Dry vs gated** | Gaps going to digital silence (−120 dBFS) vs a noise floor | Dry stems = full control of space; hard gates need edge fades |
| **Clipping** | Runs of ≥ 3 full-scale samples | Report; de-clip only modestly |
| **Lossy source** | Spectrum stops near 15–16.5 kHz; filenames like "Y2Mate…160k" | Air can't be restored; keep top-end lifts modest; recommend the WAV |
| **Leaked vocals in the beat** | Vocal-band energy in the beat during gaps | Masks the lead; may need separation |
| **Copy-pasted sections** | Sample-level cross-correlation of repeated sections (≥ 0.95) | Reveals the real hook structure *and* placement offsets |
| **Hard-tuned vocals** | Narrow spectral spikes 2.8–4.8 kHz; "steppy" pitch | Don't re-tune; tame artifacts dynamically and narrowly |
| **Noise, hum, clicks, plosives, harsh breaths** | Noise floor in gaps; 50/60 Hz combs; transient spikes < 120 Hz | Cleanup list for Gate 1 |
| **Beat already mastered?** | High LUFS, low crest, flat-topped peaks | Never re-limit it into distortion; just turn it down |
| **808 translation** | Does the 808 fundamental sit below ~60 Hz with weak harmonics? | Plan harmonic support for phone speakers |

### 0.3 Musical map
- **BPM:** detect on the beat or full mix, never on a vocal alone. Check half/double time. **Verify to the sample** with a long self-match of the beat (for example a 96-bar autocorrelation). A file's tempo can drift from its nominal value.
- **Grid origin T0:** from kick/snare transients only, never hi-hats.
- **Key and scale:** detection plus the sung pitch classes. Note confidence.
- **Sections:** beat energy per bar plus vocal activity per stem, giving timestamped intro / verse / pre / hook / bridge / outro. Find hooks by melodic or chroma repetition, not by guessing.
- **Vocal roles:** lead, call-and-response leads, doubles, harmonies, BGs, adlibs, telephone/FX vocals. Measure whether two "leads" overlap (doubles) or alternate (call-and-response). They are mixed very differently.
- **Range:** the lowest and highest sung notes of each vocal. The lowest note sets the high-pass.
- **Timing vs grid:** median onset offset of each section vs the 1/16 grid. Note natural "push" or "lay-back". Don't call anything late until you've measured it against the *beat*, not against another section.
- **Song length vs beat length:** if the beat runs long after the last vocal, propose an ending (outro and fade) and offer the full length as an option.

### 0.4 Reference and intent
- Ask for **1–3 commercial reference tracks** (15–30 s of the hook is enough). Measure their integrated and short-term loudness, tonal curve, low-end weight, vocal-to-beat relationship (800 Hz–4 kHz pocket delta) and stereo width. **Only use references without problems you'd copy.** A stem with printed FX is not a valid tonal reference for a dry vocal.
- No references? Use the artist's own approved past songs (see LEARNINGS), clearly labelled as such, and the genre tendencies in `02-decision-methods.md` §Archetypes.
- Confirm in plain words: genre and emotion, which vocals are featured, any creative FX the artist wants (never invent them from slang), delivery mode (full DSP render and/or DAW mix sheet), and deadline.

### 0.5 Write the mix plan (template: `templates/mix_plan.template.md`)
The song facts, the top 3 problems, the approach per vocal, the effects plan per section, the loudness *strategy* (not a fixed number) and the open questions. Every later decision must trace back to this plan.

**Exit checks:** inventory complete; BPM verified to the sample; sections mapped; blockers listed; plan written; empty `mix_config.json` created.

---

## Gate 1: Vocal cleanup, tone and pocket

Order matters: **fix problems before enhancing, and fix levels before compressing.**

1. **Edits & cleanup:** 5–15 ms raised-cosine fades on every region edge and edit; plosives and loud gasps lowered 4–8 dB (never gate breaths to digital silence); de-click and de-hum only if measured. Alignment of doubles and stacks to the lead (within about 10–15 ms) **only if asked or clearly needed**. Never move the lead without asking.
2. **Gain staging:** each vocal to a consistent working level (active RMS around −18 dBFS is a good starting point) so processors behave predictably.
3. **Phrase rider (before compression):** transparent RMS riding (window about 250–400 ms, ramps about 80–150 ms, limited range, for example ±3 dB). Verify that the phrase-to-phrase spread shrinks.
4. **High-pass:** just below the vocal's **lowest sung fundamental** (measured). Never a fixed frequency.
5. **Subtractive EQ, only where measured:**
   - Find resonances with the **pitch-independent harmonic envelope** (`02-decision-methods.md` §Resonances). It separates a real resonance (every note passes through it) from melody (harmonics of the most-sung notes).
   - One fault → one bell, centered on the measured peak, width matched to the measured width, depth ≤ 6 dB. If it needs more, the problem is elsewhere.
   - **Never stack overlapping cuts** across a region. **Never deepen a natural dip.** Re-measure after every cut.
6. **Dynamics, sized to this vocal:** start with *one* stage. Choose the ratio, attack and threshold from the vocal's measured dynamic range and the genre. Slower attacks (about 10–20 ms) preserve consonants; fast attacks (1–5 ms) catch peaks but dull articulation. Add a second stage or parallel compression **only** if the measurement shows a need. **Verify articulation** (consonant punch and attack vs raw) after compression.
7. **De-essing:** detect on the sibilance band measured for *this* voice; reduce only the sharp S/T/SH/CH moments (watch the "% of time active"). No broadband cuts above 6 kHz. One stage unless measured otherwise.
8. **Tone (additive EQ):** presence and air sized by measurement: brightness vs the beat and the reference, and the take's own darkness. Re-check sibilance and harshness *after* boosting.
9. **Saturation:** optional. Only if it measurably helps translation (phones) without adding low-mid weight or DC. Check DC afterwards.
10. **Pocket:** measure lead vs beat in the 800 Hz–4 kHz band and in LU per section. Set the level from the reference and the artist's taste, then carve a **vocal-keyed dynamic dip in the beat's mid channel** (centre, depth and speed chosen from where the beat masks the voice).
11. **Background vocals, doubles, adlibs:** their own chains (higher high-pass, harder de-ess, darker than the lead), placed by role (`02` §Layers).

**Exit checks (measured):** resonance hump reduced to the target without deepening dips; articulation within tolerance of raw; sibilance controlled with nothing harsher than raw; lead-to-beat pocket at the chosen target; phrase consistency (short-term loudness spread within the section target). Save the frozen Gate 1 stems and log everything in `mix_config.json`.

**Stop:** send a 15–30 s preview (vocal plus beat, with no space FX yet) and a vocal-only A/B vs raw at matched loudness.

---

## Gate 2: Space, delays and throws

1. **Depth plan:** front (dry lead, kick, snare, 808, all centered), middle (adlibs, doubles), back (reverb, throws). Write it down per section.
2. **Reverb:** type and size from tempo, density and genre; decay set to a note value; pre-delay a synced value that keeps the consonant ahead of the tail; return EQ that keeps the reverb out of the box zone and out of the S zone; duck under the dry vocal. **Verify the dry-to-reverb ratio *while singing*** and in the gaps. Clarity lives there.
3. **Delays:** BPM-exact ms and samples. Ambience delay (if any) ducked hard. **Throws only where a real gap exists:** detect line endings and gap lengths from the combined vocal bus, and **align each throw to the stressed vowel (P-center)**, not to the slice start.
4. **Collision gating:** before placing any repeat at time *t*, scan the dry vocals in [t − 0.15 s, t + repeat length]. Duck or omit any repeat that would cover a word.
5. **Tail padding:** every wet buffer gets clip length + 3–5 s and must decay below −60 dBFS. Verify programmatically.
6. **Layers:** doubles and synthetic doublers stay within about 10–20 ms and 5–12 cents and are mono-checked; BG layers sit under the lead (depth and level from the plan); BG pairs are panned symmetrically; adlibs are alternated or offset from center.
7. **Creative fills** (teases, ghost echoes, reverse swells) **only if the artist asked or approved**. Lock them to whole bars on the verified grid, and always offer a "no fills" alternate.

**Exit checks:** all delay times are BPM-exact; every throw lands on a measured line ending; no collisions; tails < −60 dBFS; dry-to-reverb ratio while singing meets the target; vocal-bus mono correlation is acceptable; layer depths are at their planned levels.

**Stop:** send a 15–30 s preview of the key hook, with throws.

---

## Gate 3: Balance, automation and mix bus

1. **Section automation:** the hook lifts over the verse (measure; a common target is about +1 to +3 LU unless the song is meant to stay flat). If the limiter would eat the lift, do it **after** the limiter.
2. **Low end:** one element owns the sub at a time (duck the 808 from the kick if they clash); notes even (multiband or dynamic control of the 808 if notes jump); mono below roughly 90–120 Hz (side high-pass); harmonic support for phones if the 808 is a near-pure sine. **The harmonics go *before* any clipping.**
3. **Beat processing:** mid-channel pocket, low-mid relief only if the mix measures crowded, and transient control only if peaks dominate the limiter. **Find which element drives the limiter before choosing the fix.**
4. **Mix bus:** gain-stage peaks to about −6 dBFS *before* any glue. Glue compression is light (aim for 1–2 dB GR), with a **sidechain high-pass** if heavy lows (808) would make it pump. Optional subtle saturation.
5. **Print the unmastered mix** (24-bit, peaks around −6 to −3 dBFS) for future remasters.

**Exit checks:** hook lift on target; mix-bus GR on target; no mud (low-mid vs mid within the target for this genre); sub mono; mix peaks with headroom.

---

## Gate 4: Master

1. **Analyze the mix:** loudness (integrated, short-term max, range), true peak, spectrum vs reference, correlation.
2. **Corrective EQ:** small and broad, only where measurement justifies it (in mastering, more than about 1.5–3 dB means the mix needs fixing instead).
3. **Remove DC before the limiter**, and again after it if asymmetric material makes the limiter generate DC. Use a very low, zero-phase block, then re-verify true peak.
4. **Choose the loudness for *this* song.** The loudest target where the limiter does ≤ 3–4 dB of gain reduction on the loudest 1% of hits (measure it directly; don't trust "LU taken" estimates), compared to references at matched loudness. Songs with long quiet sections legitimately measure lower in integrated LUFS. Compare their hooks' short-term loudness instead.
5. **True-peak ceiling:** ≤ −1.0 dBTP, or ≤ −2.0 dBTP when louder than −14 LUFS. Set the limiter a little lower if later stages (DC block, fades) can raise peaks.
6. **Encode test:** MP3 320 and AAC 256 must stay < 0 dBTP.
7. **Alternates** (instrumental, acapella, TV track, clean, no-fills) through the **exact same** bus and master settings. A **null test** (the main re-rendered through that fixed chain) must leave only a negligible residual.

---

## Gate 5: QC and delivery

1. Run the full QC gate (`03-qc-gate.md`) on the 24-bit WAV, the 16-bit WAV and the decoded MP3. **Three clean rounds.**
2. Make loudness-matched A/B clips (raw vs master; previous version vs new version; vocal-only when the vocal changed) and a picture (song map, waveforms, spectrograms).
3. Write the sign-off report (`templates/sign_off_report.template.md`), deliver the files (`07-delivery-and-release.md`), update `deliveries/LEARNINGS.md`, then commit and push.
4. Label everything **"draft, not final"** until the artist approves.
