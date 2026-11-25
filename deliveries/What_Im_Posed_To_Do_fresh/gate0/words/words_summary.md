# Word timestamps — What I'm Posed To Do (fresh run)

**Status:** draft measurements for Gate 2. Transcripts are **ASR**, not confirmed lyrics — Kenshin must confirm.

Agents cannot hear. Times below are measured onsets, not listened takes.

## Method

- **ASR:** faster-whisper model `medium.en` on CPU (`int8`), English, word timestamps, **VAD off**, peak-normalized section chunks, `condition_on_previous_text=False`. (`large-v3` with VAD on the full file hallucinated on this material; that run was discarded.)
- **Onset refinement:** 1-8 kHz 2nd-order bandpass, causal 2 ms RMS envelope (window ends at the sample, no look-ahead). Steepest rise in +/-60 ms of the ASR time (window clipped so it cannot jump onto a neighboring word), backtrack to 15% of (peak-floor) above the 20th-percentile floor of the 25 ms before the rise. If the ASR time lands in silence (local RMS < −48 dBFS), a forward first-crossing search (800-8 kHz, 2 ms RMS + 10 ms smooth, 15 dB above the local floor, up to 500 ms or the next word) snaps to the next energy onset and is flagged.
- **Detector bias (synthetic test):** +0.034 ms (positive = late). This bias was subtracted from every refined onset.
- **Bias definition:** median (detected - true) onset error in ms, on clean impulses and 2 ms bursts, combining exact ASR times and ASR times jittered uniformly in +/-40 ms. Positive = detector late.
- **Grid:** 44.1 kHz, 135.000 BPM, T0 = 182 samples, bar = 78400 samples, beat = 19600 samples, 1/16 = 4900 samples (111.1111 ms). `grid_offset_ms` is onset minus the nearest 1/16 line; negative means the word is ahead of the grid.
- **Sources:** Gate 1 cleaned 24-bit leads (same length/alignment as `src/`). Originals were not modified.
- **Low confidence:** ASR probability < 0.50, weak or edge-pinned onset, or local RMS below −48 dBFS (possible silent-region hallucination).

## Detector validation (known click positions)

| Condition | N | Mean error (ms) | Median (ms) | MAE (ms) | Std (ms) |
|---|---:|---:|---:|---:|---:|
| clean_exact_asr | 20 | +0.712 | +0.522 | 1.075 | 1.424 |
| clean_asr_jitter_pm40ms | 20 | +0.712 | +0.522 | 1.075 | 1.424 |
| noisy_-40dBFS_exact_asr | 20 | +0.653 | +0.522 | 1.016 | 1.320 |
| noisy_-40dBFS_asr_jitter_pm40ms | 20 | +0.653 | +0.522 | 1.016 | 1.320 |

Per kind (clean, exact ASR times):

| Kind | N | Mean (ms) | Median (ms) | MAE (ms) |
|---|---:|---:|---:|---:|
| impulse | 8 | -0.454 | -0.454 | 0.454 |
| burst_2ms | 8 | +0.522 | +0.522 | 0.522 |
| burst_8ms | 4 | +3.424 | +3.424 | 3.424 |

## Word 5 and word 6 at each verse / section start

The background copy should enter at word 5–6 of each verse. **Combined** is the time-ordered merge of the two trading stems (Lead 1 + Lead 2, or BG1 + BG2 on the bridge). Counting starts at the first *new phrase* of the section (leftover tails that cross the bar with no pause are skipped). That combined time is the one to use for the entrance. Per-stem columns use the same rule on that stem alone.

A faint signal exists on Lead 1 from 42.231 s (documented pickup 0:42.2) at about −48 dBFS; it is not a word. The first solid Lead 1 onset is the word "I've", snapped forward from an early ASR time onto the energy attack on the '3' of bar 25. Lyric note: the hook line is heard as "I've been trying everything these blunts ain't enough"; a sum-of-leads pass sometimes also hears "at all" after "enough" (not kept on Lead 1 here). "Posed" in the title is often recognized as "supposed" / "postin'". All wording is ASR and needs Kenshin's confirmation.

### Combined (use this for the BG entrance)

| Section | Bars | Word 5 | Stem | Time | Samples | Grid off. (ms) | Word 6 | Stem | Time | Samples | Grid off. (ms) | Notes |
|---|---|---|---|---|---:|---:|---|---|---|---:|---:|---|
| A1 (A) | 25–41 | `these` | lead1 | 0:44.910 | 1980534 | +17.1 | `blunts` | lead1 | 0:45.346 | 1999744 | +8.2 | — |
| B1 (B) | 42–49 | `do` | lead1 | 1:13.804 | 3254743 | +21.8 | `when` | lead1 | 1:14.069 | 3266463 | -45.8 | — |
| B2 (B) | 50–56 | `do` | lead1 | 1:28.026 | 3881966 | +22.3 | `when` | lead1 | 1:28.293 | 3893700 | -44.9 | — |
| A2 (A) | 57–73 | `these` | lead1 | 1:41.820 | 4490265 | +38.2 | `blunts` | lead1 | 1:42.247 | 4509107 | +21.0 | LOW: asr_prob=0.46<0.5 |
| Bridge (Bridge) | 74–82 | `no` | bg1 | 2:10.637 | 5761111 | -33.4 | `good` | bg1 | 2:10.978 | 5776133 | -26.1 | LOW: onset:weak_rise |
| B3 (B) | 90–98 | `do` | lead1 | 2:39.098 | 7016202 | -17.7 | `when` | lead1 | 2:39.363 | 7027922 | +25.9 | — |

First six combined words (so the 5–6 choice can be checked):

- **A1:** 1. lead1 `I've` @ 0:43.584 · 2. lead1 `been` @ 0:43.807 · 3. lead1 `trying` @ 0:43.970 · 4. lead1 `everything` @ 0:44.284 · 5. lead1 `these` @ 0:44.910 · 6. lead1 `blunts` @ 0:45.346
- **B1:** 1. lead1 `What` @ 1:12.902 [low] · 2. lead1 `I'm` @ 1:13.095 · 3. lead1 `supposed` @ 1:13.373 [low] · 4. lead1 `to` @ 1:13.578 · 5. lead1 `do` @ 1:13.804 · 6. lead1 `when` @ 1:14.069
- **B2:** 1. lead1 `What` @ 1:27.123 · 2. lead1 `I'm` @ 1:27.326 · 3. lead1 `supposed` @ 1:27.595 · 4. lead1 `to` @ 1:27.655 · 5. lead1 `do` @ 1:28.026 · 6. lead1 `when` @ 1:28.293
- **A2:** 1. lead1 `I've` @ 1:40.492 · 2. lead1 `been` @ 1:40.732 · 3. lead1 `trying,` @ 1:40.887 · 4. lead1 `everything` @ 1:41.476 · 5. lead1 `these` @ 1:41.820 [low] · 6. lead1 `blunts` @ 1:42.247
- **Bridge:** 1. bg1 `I've` @ 2:09.869 · 2. bg1 `been` @ 2:10.097 · 3. bg1 `up` @ 2:10.295 · 4. bg1 `to` @ 2:10.461 · 5. bg1 `no` @ 2:10.637 [low] · 6. bg1 `good` @ 2:10.978
- **B3:** 1. lead1 `What` @ 2:38.193 [low] · 2. lead1 `I'm` @ 2:38.325 · 3. lead1 `supposed` @ 2:38.666 [low] · 4. lead1 `to` @ 2:38.727 · 5. lead1 `do` @ 2:39.098 · 6. lead1 `when` @ 2:39.363

### Per stem

#### A1 (bars 25–41, start 0:42.671, pickup 0:42.591)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| lead1 | 45 | `these` | 0:44.910 | 1980534 | `blunts` | 0:45.346 | 1999744 | 1.I've, 2.been, 3.trying, 4.everything, 5.these, 6.blunts |
| lead2 | 47 | `with` | 0:48.508 | 2139222 | `my` | 0:48.534 | 2140366 | 1.And, 2.I, 3.been, 4.hangin', 5.with, 6.my |
| bg1 | 0 | — | — | — | — | — | — | — |
| bg2 | 0 | — | — | — | — | — | — | — |

#### B1 (bars 42–49, start 1:12.893, pickup 1:12.813)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| lead1 | 26 | `do` | 1:13.804 | 3254743 | `when` | 1:14.069 | 3266463 | 1.What, 2.I'm, 3.supposed, 4.to, 5.do, 6.when |
| lead2 | 24 | `like` | 1:17.584 | 3421468 | `myself` | 1:17.874 | 3434226 | 1.Only, 2.time, 3.I'm, 4.feeling, 5.like, 6.myself |
| bg1 | 0 | — | — | — | — | — | — | — |
| bg2 | 0 | — | — | — | — | — | — | — |

#### B2 (bars 50–56, start 1:27.115, pickup 1:27.035)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| lead1 | 27 | `do` | 1:28.026 | 3881966 | `when` | 1:28.293 | 3893700 | 1.What, 2.I'm, 3.supposed, 4.to, 5.do, 6.when |
| lead2 | 16 | `like` | 1:31.805 | 4048586 | `myself` | 1:32.103 | 4061739 | 1.Only, 2.time, 3.I'm, 4.feeling, 5.like, 6.myself |
| bg1 | 0 | — | — | — | — | — | — | — |
| bg2 | 0 | — | — | — | — | — | — | — |

#### A2 (bars 57–73, start 1:39.560, pickup 1:39.480)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| lead1 | 46 | `these` [low] | 1:41.820 | 4490265 | `blunts` | 1:42.247 | 4509107 | 1.I've, 2.been, 3.trying,, 4.everything, 5.these, 6.blunts |
| lead2 | 30 | `been` | 1:44.759 | 4619857 | `hanging` | 1:44.843 | 4623591 | 1.At, 2.all,, 3.and, 4.I've, 5.been, 6.hanging |
| bg1 | 0 | — | — | — | — | — | — | — |
| bg2 | 0 | — | — | — | — | — | — | — |

#### Bridge (bars 74–82, start 2:09.782, pickup 2:09.702)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| bg1 | 24 | `no` [low] | 2:10.637 | 5761111 | `good` | 2:10.978 | 5776133 | 1.I've, 2.been, 3.up, 4.to, 5.no, 6.good |
| bg2 | 22 | `good` | 2:14.551 | 5933683 | `hangin'` | 2:15.004 | 5953676 | 1.been, 2.up, 3.to, 4.no, 5.good, 6.hangin' |

#### B3 (bars 90–98, start 2:38.226, pickup 2:38.146)

| Stem | N words | Word 5 | Time | Samples | Word 6 | Time | Samples | First six |
|---|---:|---|---|---:|---|---|---:|---|
| lead1 | 27 | `do` | 2:39.098 | 7016202 | `when` | 2:39.363 | 7027922 | 1.What, 2.I'm, 3.supposed, 4.to, 5.do, 6.when |
| lead2 | 10 | `like` | 2:42.877 | 7182885 | `myself` | 2:43.176 | 7196044 | 1.Only, 2.time, 3.I'm, 4.feeling, 5.like, 6.myself |
| bg1 | 0 | — | — | — | — | — | — | — |
| bg2 | 0 | — | — | — | — | — | — | — |

## Line-by-line transcript by section (ASR — may contain errors)

Lines are split on a pause of ≥ 350 ms (ASR end of the previous word to the next onset). Lead 1 and Lead 2 trade about every two bars; both are listed under each section. Confirm wording with Kenshin before locking throws to a specific word.

### A1 (bars 25–41, 0:42.671–1:12.893)

**lead1** (45 lexical words, 1 low-confidence):

- L1 `0:43.584–0:46.586` (bar 25) I've been trying everything these blunts ain't enough
- L2 `0:50.680–0:54.726` (bar 29) You keep trying to run away, stop and turn around and face yours
- L3 `0:58.670–1:02.673` (bar 33) I've been up to no [?] good with all the forbidden ones
- L4 `1:05.745–1:09.453` (bar 37) Hanging with the perfect ain't been fun like too fun like at all

**lead2** (48 lexical words, 5 low-confidence):

- L1 `0:46.691–0:50.906` (bar 27) And [?] I been [?] hangin' with my demons, dancin' in the graveyard
- L2 `0:54.259–0:58.233` (bar 31) You keep tryin' to run away, stop and turn around and say some [?]
- L3 `1:02.146–1:06.033` (bar 35) I've [?] been up to no good hanging [?] with the hidden ones
- L4 `1:09.293–1:13.213` (bar 39) Most my time I spent inside the dark, I enjoyed it it all

### B1 (bars 42–49, 1:12.893–1:27.115)

**lead1** (26 lexical words, 5 low-confidence):

- L1 `1:12.902–1:17.149` (bar 42) What [?] I'm supposed [?] to do when the blunts ain't nothing [?] like that [?] at all
- L2 `1:20.095–1:23.669` (bar 46) threw back a Xan, [?] it's the only way to sleep it off

**lead2** (24 lexical words, 2 low-confidence):

- L1 `1:16.450–1:20.989` (bar 44) Only time I'm feeling like myself is out [?] this Adderall
- L2 `1:23.514–1:27.329` (bar 47) Hanging with the perfect ain't been fun like too fun Like [?] like at all

### B2 (bars 50–56, 1:27.115–1:39.560)

**lead1** (27 lexical words, 2 low-confidence):

- L1 `1:27.123–1:31.151` (bar 50) What I'm supposed to do when the blunt say nuh [?] nuh, like at all
- L2 `1:34.251–1:37.791` (bar 54) I threw back a Xan, [?] it's the only way to sleep it off

**lead2** (16 lexical words, 0 low-confidence):

- L1 `1:30.661–1:33.911` (bar 51) Only time I'm feeling like myself is out this Adderall
- L2 `1:37.742–1:39.711` (bar 55) Only time I'm feeling like myself

### A2 (bars 57–73, 1:39.560–2:09.782)

**lead1** (46 lexical words, 4 low-confidence):

- L1 `1:40.492–1:43.495` (bar 57) I've been trying, everything these [?] blunts ain't enough
- L2 `1:47.590–1:51.635` (bar 61) You keep trying to run away, stop and turn around and face yours
- L3 `1:55.582–1:59.582` (bar 66) I've I [?] been [?] up to no [?] good with all the forbidden ones
- L4 `2:02.657–2:06.722` (bar 69) Hanging with the perfect ain't been fun like too fun like at all

**lead2** (36 lexical words, 5 low-confidence):

- L1 `1:39.766–1:41.795` (bar 57) is off up the [?] cetera
- L2 `1:43.604–1:47.875` (bar 59) At [?] all, and I've been hanging with my demons, dancing in the graveyard
- L3 `1:51.164–1:55.162` (bar 63) You keep trying to run away, stop and turn around and say some [?]
- L4 `1:59.058–1:59.742` (bar 67) I [?] been [?] up
- L5 `2:09.122–2:10.157` (bar 73) it all.

**bg1** (1 lexical words, 1 low-confidence):

- L1 `2:09.417–2:10.097` (bar 73) I've [?]

### Bridge (bars 74–82, 2:09.782–2:25.782)

**bg1** (24 lexical words, 1 low-confidence):

- L1 `2:09.869–2:13.897` (bar 74) I've been up to no [?] good with all the forbidden ones
- L2 `2:16.913–2:20.697` (bar 78) Hanging with the perfect ain't been fun like too fun like at all

**bg2** (23 lexical words, 1 low-confidence):

- L1 `2:13.314–2:17.297` (bar 75) I've [?] been up to no good hangin' with the hidden ones
- L2 `2:20.465–2:24.337` (bar 80) Most my time I spent inside the dark I enjoyed it all

**lead1** (1 lexical words, 1 low-confidence):

- L1 `2:25.182–2:25.922` (bar 82) You [?]

### Gap (bars 83–89, 2:25.782–2:38.226)

**lead1** (1 lexical words, 1 low-confidence):

- L1 `2:37.465–2:38.362` (bar 89) What [?]

### B3 (bars 90–98, 2:38.226–2:54.226)

**lead1** (27 lexical words, 4 low-confidence):

- L1 `2:38.193–2:42.262` (bar 89) What [?] I'm supposed [?] to do when the blunt say nuh [?] nuh, like at all
- L2 `2:45.323–2:48.822` (bar 93) I threw back a Xan, [?] it's the only way to sleep it off

**lead2** (10 lexical words, 1 low-confidence):

- L1 `2:41.733–2:45.762` (bar 91) Only [?] time I'm feeling like myself is out this Adderall

## Confidence notes

- **lead1:** 173 ASR tokens, 173 lexical, 18 low-confidence (prob<0.5: 13; weak onset: 6; window edge: 0; silent-region: 2). Median ASR word probability 0.95. Source: `/workspace/songs/Untitled_2026-11-25/gate1/WIPTD_fresh_G1_Lead1_v1_24b-44k.wav`.
- **lead2:** 134 ASR tokens, 134 lexical, 13 low-confidence (prob<0.5: 11; weak onset: 0; window edge: 0; silent-region: 2). Median ASR word probability 0.96. Source: `/workspace/songs/Untitled_2026-11-25/gate1/WIPTD_fresh_G1_Lead2_v1_24b-44k.wav`.
- **bg1:** 25 ASR tokens, 25 lexical, 2 low-confidence (prob<0.5: 0; weak onset: 2; window edge: 0; silent-region: 1). Median ASR word probability 0.98. Source: `/workspace/songs/Untitled_2026-11-25/gate1/WIPTD_fresh_G1_BackgroundLead_v1_24b-44k.wav`.
- **bg2:** 23 ASR tokens, 23 lexical, 1 low-confidence (prob<0.5: 0; weak onset: 0; window edge: 0; silent-region: 1). Median ASR word probability 0.98. Source: `/workspace/songs/Untitled_2026-11-25/gate1/WIPTD_fresh_G1_BackgroundLead2_v1_24b-44k.wav`.

Hallucinated (silent-region) tokens should not be used for throws or BG entrances. Low-probability words may be mis-heard slang or slurred rap and need a lyric check.

## Files

- `words_lead1.json`, `words_lead2.json`, `words_bg1.json`, `words_bg2.json` — per-word ASR times, refined onsets (seconds and samples), grid offsets, confidence flags.
- `words_summary.md` — this file.
- `detector_bias.json` — full synthetic-test numbers.
- `word5_word6.json` — the word-5/6 table in machine-readable form.
- `build_word_timestamps.py` — the script that produced these.

Not pushed to GitHub and not posted anywhere.
