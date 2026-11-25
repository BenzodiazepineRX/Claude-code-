> **ARCHIVED SOURCE. Superseded by `.claude/skills/pro-mix-master/` (see `references/00-sources-and-changes.md`). Numbers below are NOT settings; derive every value from the current song.**

# DSP Code & Audio Engineering Guardrails (Anti-Bug Rules for AI Agents)

When writing Python (`numpy`, `scipy`, `soundfile`, `pydub`, `ffmpeg`) audio processing scripts, these technical guardrails are **mandatory** to prevent the exact bugs that ruin AI-rendered mixes.

---

## 1. Immutable Configuration & Diff-Only Versioning (`mix_config.json`)
- Store every numeric mix parameter (stem gains, EQ bands, de-esser thresholds, compressor settings, delay timestamps, reverb wet levels, limiter ceiling) in a versioned **`mix_config.json`** file.
- Save clean intermediate stems after Gate 1 (`gate1_lead.wav`, `gate1_adlibs.wav`, `gate1_beat_carved.wav`) so Gate 2 FX work never accidentally alters approved Gate 1 tone.
- On every revision (`v2`, `v3`, etc.), load the previous `mix_config.json`, change **only** the requested keys, and log the exact before/after diff. **Never regenerate a mixing script from scratch during a revision.**

## 2. Sample-Rate, Bit-Depth & Channel Lock
- Before any DSP math, inspect every stem's `sample_rate`, `channels`, and `duration`.
- Resample all mismatched stems to a single master working rate (e.g., `44,100 Hz` or `48,000 Hz` using high-quality polyphase resampling `scipy.signal.resample_poly`) so pitch and tempo never drift.
- Do all internal DSP math in **64-bit or 32-bit floating point (`float64`/`float32`)**, never 16-bit integer. Apply dithering/conversion to `24-bit PCM WAV` only at the final export step.

## 3. Filter Phase & Stability Discipline
- Use **second-order sections (`sos = butter(..., output='sos')` + `sosfilt`)** for all standard IIR mixing filters (HPF, LPF, shelves, peaking EQ).
- **Avoid `sosfiltfilt` on sharp bass filters or drum transients** — zero-phase bidirectional filtering creates audible pre-ringing before kicks and vocal transients.
- Verify every custom biquad filter's impulse response / gain curve isn't unstable (`np.isfinite(y).all()` and max peak sanity check) before summing stems.

## 4. Local vs. Global Timestamp Safety (Zero Silent Index Bugs)
- Never pass a **global song timestamp** (e.g., `41.40 s`) into a helper function operating on a **locally sliced clip** (`0.00 s` to `0.48 s`).
- Explicitly name variables `global_sec` vs. `local_sec` (or `global_idx` vs. `local_idx`) and assert `0 <= local_idx < len(clip)` so slice/P-center detection can never silently return an empty array.

## 5. Click-Free Edits & Crossfades
- Apply **`5–15 ms` raised-cosine (Hann) fade-ins and fade-outs** to every sliced delay throw, muted gap, breath edit, and automation gate.
- Never hard-cut a waveform at a non-zero crossing—hard cuts create audible digital clicks/pops.

## 6. Mandatory Tail Buffer Padding (Zero Cut-Off Echoes/Reverbs)
- Whenever rendering a delay throw, ping-pong echo, or reverb tail, allocate a buffer at least **`clip_len + 4.0 s`** (or full song length + `4.0 s` outro pad).
- Verify programmatically that the tail energy decays below `-60 dBFS` before the buffer ends. Never truncate a wet throw at the end of a bar or phrase slice.

## 7. True 4x-Oversampled True-Peak & EBU R128 / ITU-R BS.1770 Loudness
- **Never mistake sample peak for True Peak.** Always measure True Peak by 4x oversampling (`resample_poly(audio, 4, 1)`) and measuring `20 * log10(max(abs(oversampled)))`.
- Measure integrated LUFS using K-weighted ITU-R BS.1770-4 filtering (or `ffmpeg -filter_complex ebur128=peak=true`) so loudness numbers match real mastering meters.

## 8. Cache-Busting Output Filenames
- Every new render must use a fresh, explicit versioned filename (`TrackName_Gate1_v1.wav`, `TrackName_Gate2_Preview_v1.wav`, `TrackName_MASTER_v2_24bit.wav`) so neither the agent nor the user ever auditions a stale cached file.
