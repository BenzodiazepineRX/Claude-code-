# 04: DSP & Code Guardrails (every rule here exists because a bug happened)

Mandatory for any agent rendering audio with Python (numpy, scipy, soundfile, pyloudnorm) and ffmpeg.

## 1. Configuration & versioning
- **`mix_config.json` is the single source of truth.** Every gain, EQ band, compressor, de-esser, delay time and timestamp, reverb level, automation range, loudness target and ceiling, each with `why` + `source` + `version` (template in `templates/`).
- Freeze approved intermediate stems per gate (for example `gate1_lead1.wav`). Later gates read them; they never re-process approved stages.
- **Revisions:** load the previous config, change only the requested keys, write the before/after diff into the report. Never regenerate a working chain from scratch during a revision unless the artist's problem measurably originates there. In that case say so and A/B old vs new.
- Every render gets a fresh versioned filename (`Song_Master_v7_24b-44k.wav`). Never overwrite. Move superseded files to `versions/`. Never delete them silently.

## 2. Format discipline
- Inspect sample rate, channels and duration of every stem first. Resample mismatches with polyphase resampling; verify alignment after.
- Do all DSP in float (32/64-bit). Convert to 24-bit PCM (or 16-bit with TPDF dither, **dither once, last**) only at export.
- Keep mono stems as mono content; when converting to stereo for panning, use explicit pan laws.

## 3. Filters and phase
- Prefer second-order sections (`butter(..., output='sos')` + `sosfilt`) for mixing filters.
- **Zero-phase (`sosfiltfilt`, linear-phase FIR) creates pre-ringing.** Avoid it on steep low filters and on drum/vocal transients. If you use it (for analysis, gentle slopes, M/S splitting or DC blocking), say why and check transients.
- Linear-phase FIR EQ must be latency-compensated (trim (taps−1)/2) and checked for pre-ringing on transients.
- Check every custom filter for stability: `np.isfinite(y).all()`, plus a peak sanity check against the input.

## 4. Latency and alignment
- **Every lookahead process (limiter, de-esser with lookahead, FIR) must be latency-compensated.** An uncompensated vocal limiter once delayed the vocal by 0.48 ms; it was caught by measuring transient alignment vs the source.
- After any process chain, measure the alignment of transients (1–6 kHz band cross-correlation) vs the source: ≤ 2 samples.
- Broadband cross-correlation can show fake "shifts" caused by low-frequency phase. Judge timing in the transient band.

## 5. Indexing safety
- Name variables `global_sec`/`global_idx` vs `local_sec`/`local_idx`; assert `0 <= local_idx < len(clip)`.
- Mixed-length arrays: pad or trim explicitly before arithmetic. A one-sample mismatch crashed several analyses here.
- Guard every window against running past the end of a file. An empty window gave a silent `nan` that propagated into a "pass".

## 6. Click-free edits and fades
- 5–15 ms raised-cosine fades on every slice, mute, gate, throw, region edge and ending.
- Never hard-cut away from a zero crossing.

## 7. Tails
- Every wet buffer is clip length + 3–5 s (or song + 4 s); verify the tail decays below −60 dBFS before the buffer ends; then trim the final master with a short fade after the last audible tail.

## 8. Loudness and peak measurement
- True peak = 4× oversampled peak (`resample_poly(x, 4, 1)`), never the sample peak.
- Loudness = ITU-R BS.1770 / EBU R128 (pyloudnorm or ffmpeg `ebur128=peak=true`).
- **Limiter load: measure directly** (pre-limiter signal × gain vs post-limiter, per 10 ms block, top 1%). Loudness-difference estimates are skewed by quiet sections.
- ffmpeg `alimiter`: set `level=disabled`, oversample around it, and set `latency=true` when timing matters.
- Asymmetric saturation plus limiting creates DC. Block DC before *and*, if needed, after the limiter, then re-check true peak (a DC block can raise peaks slightly, so leave margin in the ceiling).

## 9. Performance and resources
- **Never** run `np.convolve` with long windows on full-length audio (O(N·w)). Use cumulative sums for moving averages, or FFT convolution. One rider took 30+ minutes until rewritten.
- Run heavy analyses one or two at a time. Three parallel QC runs ran out of memory and a process was killed.
- Long jobs: run in the background, then check results. Never assume they finished.

## 10. Measurement validity
- Sanity-test new metrics on synthetic signals with known answers.
- Use **pitch-independent** methods for vocal tone (harmonic envelope). Long-term spectra mix melody with resonances.
- Never measure a vocal's tempo; measure the beat. Never measure "lateness" between two sections; measure each against the beat grid.
- When comparing processed vs raw, **match loudness first**.

## 11. Shell and file safety
- Downloaded archives: list contents before extracting; extract into a new empty directory; read with `python -I`; never run code from inside them.
- Never use `rm` with an unguarded shell variable path. Move superseded files to a versions folder instead of deleting.
- Don't nest heredocs inside generated scripts; pass settings through environment variables or JSON.
- Check every pipeline step's output. A step that "printed nothing" may have failed. A `| head` can break a pipe after the file was written; verify the files instead.

## 12. Reproducibility
- Save every script, the `mix_config.json`, the limiter settings JSON and the QC JSON per version into `deliveries/<Song>/session/`.
- The main master must be reproducible: re-render it through the fixed alternate chain and null-test it.
