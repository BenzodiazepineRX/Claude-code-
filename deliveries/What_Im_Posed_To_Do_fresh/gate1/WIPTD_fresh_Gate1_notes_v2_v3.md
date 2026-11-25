# What I'm Posed To Do (fresh): Gate 1 v2 (level) and v3 (slight lead reverb)

**Status: DRAFT, NOT FINAL** · by Pro Mix & Master Agent Alpha · 2026-11-25 · one change per version, diff-only, v1 untouched
Kenshin's note on the v1 preview: *"This sounds really good. Just add a slight reverb and either turn the main vocals down a tad or turn the beat up. It seems kinda loud (the vocals) can't really hear the beat."*
I can't hear. Everything below is measured, and the A/B clips are for Kenshin's ears.

## v2: level only
**What changed:** all four vocal stems are at **-1.5 dB vs v1**. The beat, its pocket dip, the -6 dB bus offset and the whole vocal chain are unchanged. Because the same gain went on all four vocals, the bridge-vs-lead relationship is unchanged.

| Parameter | v1 | v2 | Why |
|---|---|---|---|
| Lead 1 / Lead 2 output gain | -0.84 dB | -2.34 dB | Kenshin: vocals kinda loud, can't hear the beat |
| BG 1 / BG 2 output gain | -0.93 dB | -2.43 dB | Same move, so the bridge stays in the same relationship to the leads |
| Lead vs beat target (range) | -1.0 LU (-1.5..-0.5) | -2.5 LU (-3.0..-2.0) | Set before the render |

**How 1.5 dB was chosen:**
- The brief allowed 1.5–2.5 dB ("a tad"). I took the largest cut that keeps every full-beat section's 800 Hz–4 kHz vocal-over-beat margin at **≥ +3 dB**. That is the Gate 1 clarity guard, set before v1.
- The tightest section was A1 at +4.63 dB in v1, so the most I could cut was 1.63 dB, which I rounded to 1.5 dB. A 2 dB cut would drop A1 to +2.6 dB, below the guard.

**References:**
- I separated each of Kenshin's three WAVs with demucs (vocals vs instrumental). I calibrated the method on our own v1 mix, where the answer is known: true -1.02 LU, separated -0.89 LU, so the bias is +0.13 LU.
- Result, lead vs beat: **WOW -0.19 LU, Fiji Falls -1.90, XXX +0.43, median -0.19 LU**. Midband (800 Hz–4 kHz) is +5.9, +9.1 and +6.4 dB.
- **The references have the vocal louder than our v1, so they do not support a cut.** I'm stating that openly. Kenshin's direct ear note, plus his history (Wild Side at -0.43 LU was "too loud", v1 at -1.0 is "kinda loud"), decides, and the clarity guard limits how far the cut goes.
- Possible reasons we hear it differently from the references: our beat is a dark, lossy YouTube rip, and the references are mastered and limited. Confidence in this comparison is low to medium.

**v2 exit checks: 70 of 75 pass.**
- v2 is exactly v1 × -1.5 dB (within 1 LSB) on every stem, and the BG-vs-lead balance is unchanged.
- The 5 fails are the same box-hump limits as v1 (Lead 1 +2.68; BG1/BG2 +3.08/+3.15). Gain doesn't change them.

**v2 lead vs beat (full-beat sections):**

| Section | LU | Midband |
|---|---|---|
| A1 | -2.90 | +3.13 |
| B1 | -2.37 | +3.60 |
| A2 | -2.63 | +3.52 |
| B3 | -2.50 | +3.65 |
| Bridge (BG) | -2.50 | +4.24 |

All PASS.

**Thin-beat sections, for Gate 3 (not ridden now):** B2 without 808 is +2.78 LU (v1 +4.28), A1 drums-out +4.77 (v1 +6.27), A2 drums-out +5.10 (v1 +6.60). The vocals still sit well over the beat there, so they need section automation in Gate 3.

## v3: v2 plus one slight reverb on the two leads
**Scope:** Lead 1 and Lead 2 share one send. The bridge voices, the beat and the Gate 2 background-copy/telephone layer are untouched.

| Setting | Value | Why |
|---|---|---|
| Type | Dark synthetic plate (stereo noise IR; highs above 4 kHz decay at 0.6×) | Brief asked for a short, dark plate. Kenshin doesn't want harsh, and the source is lossy |
| Pre-delay | **1/32 note = 55.556 ms = 2450 samples** (measured: 2450) | Keeps consonants ahead of the tail. It's Kenshin's approved value on this song (27 ms sounded boxy) |
| Decay (RT60 below 4 kHz) | **Dotted 1/8 = 333.3 ms** (measured 326.4) | Shortest option. The leads are almost continuous (median gap 70 ms) and already carry printed reverb |
| Send high-pass | **600 Hz, 24 dB/oct** | Above this voice's 440–520 Hz box zone. A 300–400 Hz HPF would feed the box zone into the reverb, which Kenshin has called a "tunnel". 600 Hz is his approved value |
| Send low-pass | **7.5 kHz, 24 dB/oct** | Below the de-essed S bands, and inside the brief's 6–8 kHz |
| Ducking | **6 dB**, attack 1/128 (13.9 ms), release 1/8 (222.2 ms), keyed by the dry lead bus | Keeps the reverb out of the words |
| Stereo | L/R correlation 0.4 | A fully decorrelated version lost 3.08 dB when summed to mono. This version loses 1.96 dB |
| Return level | **24.0 dB under the dry leads** (send -16.2 dB) | "Slight" means about 20 dB under. Printed reverb means add less. Attempt 2 at 22 dB under had dry-to-reverb only 23.0 dB |

**v3 measured:**
- Dry-to-reverb while singing is **25.0 dB** (target ≥ 24). In gaps it's 1.9 dB, so the reverb only opens up there.
- Reverb 250–600 Hz share is 5.3 dB below the dry voice's, so it isn't box-heavy.
- The tail decays to silence well inside the 4 s pad. Return peak is -34.8 dBFS.

**Decay stretch** (parent's limit ≤ +15%; Kenshin dislikes stacked reverb), median of 14 turns:

| Lead | Window | v2 | v3 | Change |
|---|---|---|---|---|
| Lead 1 | T20 | 600 ms | 600 ms | **+0%** |
| Lead 1 | T30 | 960 ms | 960 ms | +0% |
| Lead 2 | T20 | 570 ms | 570 ms | **+0%** |
| Lead 2 | T30 | 480 ms | 480 ms | +0% |

- The late window (-25 to -40 dB) shows -10.9% on Lead 1 and 0% on Lead 2. The Lead 1 figure isn't a real shortening: one more turn became measurable (13 → 14).
- Attempt 2 (1/2-note decay) had stretched the Lead 1 tail by +25%, which is why I moved to the shorter decay.

**Printed leads vs v2:**
- Turn-end tail +0.27 / +0.11 dB; room between words +0.19 / -0.06 dB.
- 2–5 kHz flare 14.31 → 14.12 and 11.70 → 11.47 (clarity unchanged).
- S-spike slightly lower.
- Punch -0.05 / -0.14 dB.
- Lead vs beat moves only +0.02 LU per section: A1 -2.88, B1 -2.35, A2 -2.62, B3 -2.48.

**v3 exit checks: 22 of 24 pass. The 2 fails are both attack vs v2:**
- Lead 1 is at **92%** and Lead 2 at **94.7%** of v2. I pre-set ≥ 95% of v2. That is stricter than the standard's ≥ 90% of raw, which both pass (92% and 95% of raw).
- **Cause (measured):** the reverb fills the very quiet frames just before word onsets. At the 100 biggest onsets, the 2–5 kHz level just before the onset rises from -70.4 to -65.2 dB.
- Ducking depth and the send low-pass don't change it. A shorter decay helps, and dotted 1/8 is the shortest I tested.
- Only "26 dB under + dotted 1/8" gets close to 95% (94% and 96%). I judged that too quiet to be the audible "slight" reverb Kenshin asked for. If he hears the words soften, the fix is to lower the return 2 dB.

**Process notes:**
- **Attempt 1:** the IR check had a bug (the dB conversion line was commented out). The files were never used and are kept in `versions/v3_attempt1_rt60_check_bug`.
- **Attempt 2:** 1/2-note decay at 22 dB under with a fully decorrelated IR. It failed dry-to-reverb, mono and attack, and stretched the decay +25%. Kept in `versions/v3_attempt2_rt60_half_note`.
- The sweeps are in `sweep_reverb_v3*.log`.

## Files (repo: `deliveries/What_Im_Posed_To_Do_fresh/`)
- **v2 stems** (`stems/v2/`): `WIPTD_fresh_G1_{Lead1,Lead2,BackgroundLead,BackgroundLead2}_v2_24b-44k.flac`. The beat is still `stems/v1/WIPTD_fresh_G1_Beat_pocket_v1_24b-44k.flac`.
- **v3 stems** (`stems/v3/`):
  - `WIPTD_fresh_G1_LeadReverbReturn_v3_24b-44k.flac`: reverb return only, stereo.
  - `WIPTD_fresh_G1_Lead1_v3_24b-44k.flac` and `..._Lead2_v3_...`: dry v2 lead plus its share of the reverb, printed.
  - The v3 files are stereo and run 4 s past the longer lead (7,824,652 samples). Use either return + v2 dry, or the printed leads, never both.
- **Previews** (`gate1/`), every clip and every A/B half at -20 LUFS:
  - `WIPTD_fresh_G1_Preview_VocalBeat_1m05-1m27_v2.mp3`
  - `WIPTD_fresh_AB_Mix_v1_vs_v2.mp3`: 0:00–0:21 v1, gap, 0:22–0:43 v2
  - `WIPTD_fresh_G1_Preview_VocalBeat_1m05-1m27_v3.mp3`
  - `WIPTD_fresh_AB_Mix_v2_vs_v3.mp3`: 0:00–0:21 v2, gap, 0:22–0:43 v3
- **Configs:** `gate1/mix_config_v2_gate1.json`, `gate1/mix_config_v3_gate1.json`. Exit checks: `gate1/gate1_exit_checks_v2.json` / `_v3.json` with raw logs. Decay: `gate1/decay_v2_v3.json`. References: `gate1/refs_pocket_v2.json`.
- **Gate 2 background copy (Plugin/Effect Pro):** build it from the **v2 dry leads** (`stems/v2/WIPTD_fresh_G1_Lead1_v2_24b-44k.flac`, `..._Lead2_v2_...`), not the v3 printed leads, so the copy doesn't carry this plate.

## Please check (headphones, car, phone)
- **v1 vs v2 A/B, 0:00 vs 0:22 (song 1:05.8–1:27.1):** can you hear the beat now? Are the words still clear? A1 is right at the clarity limit.
- **v2 vs v3 A/B:** is the reverb audible but slight? Is anything muddy or "tunnel"-like? Do the word starts still feel crisp?
- **Turn ends (e.g. the B1 entry at 1:12.9):** does the reverb make the printed tails sound longer or stacked?

## Limits
- The references disagree with the cut (they have the vocal louder). The cut follows Kenshin's ears.
- The vocals can't go down further without breaking the clarity guard in A1. A further step should be beat EQ or automation in Gate 3, not more vocal cut.
- The beat dip was keyed by the v1 vocal level. It wasn't re-keyed, to keep this a one-change version.
- The v3 attack is below my pre-set vs-v2 limit (above the standard's vs-raw limit).
- Printed reverb and lossy sources remain. The residual box humps from v1 are unchanged.
- The thin-beat sections are still +2.8 to +5.1 LU over the beat (Gate 3).

## Decisions for Kenshin
1. Is v2's level right, or should it go further? Going further would mean a Gate 3 move on the beat or automation, because the vocal cut is at the clarity limit.
2. Is the v3 reverb right as is, or should it be lower (-2 dB, crisper starts) or a bit longer or louder?
3. Still open from v1: hook A or B, bridge featured or distant, drums-out riding, dry vocal and beat WAVs, echoes, the word 5–6 entry point for the background copy, beat lease, ending.

Draft, not final.
