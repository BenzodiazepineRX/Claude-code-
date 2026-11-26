# What I'm Posed To Do (fresh run): Gate 2 notes, v2

**Status: DRAFT, NOT FINAL.** Gate 2 v2 is a one-change revision of v1 clip a. Built by Mix And Master Plugin/Effect Pro on 2026-11-25 (America/Chicago).
I can't hear. Everything below comes from measurements. Kenshin's ears make the final call.

**Request (his words):** "The background vocals can be a lil louder. I can't really hear em." He didn't name a clip, so clip a (light BG, 20 dB under the lead in 1–4 kHz, word-timed throws) is the base.

**What changed:** only the BG copy level. The reverb return stays in the same dB relation to that copy, so it went up 3.00 dB with it. Throws, the 600 Hz–2 kHz telephone band, the entry points, the ducker, and the v2 dry lead (no reverb on the lead) are unchanged.

## Level ladder (A1 hook 0:42.0–1:12.0)
Every clip uses the Gate 1 v2 dry lead and the v1 word-timed throws. Target loudness is **−20.0 LUFS**. Encoded true peak is at or below **−2.0 dBTP**. The 20 and 17 dB clips landed at **−20.03 LUFS**; another +0.03 dB would have pushed their encoded true peak over −2.0 dBTP. The 15, 13 and 11 dB clips are −20.0 LUFS.

Clarity floor used here: lead vs beat+BG in 800 Hz–4 kHz during singing stays at or above **3.0 dB** (the Gate 1 pocket lower bound). Without the BG, that margin is 5.01 dB on the hook and 5.21 dB on the whole song.

Audibility floor used here: BG vs the beat in its own 600 Hz–2 kHz band stays at or above **−10 dB** (the same floor as the v1 throw-audibility check). Clip a measured −12.8 dB on the hook, and Kenshin could not hear the layer.

| Rung | 1–4 kHz under the lead (hook / song) | Lead vs beat+BG, 800 Hz–4 kHz (hook / song) | Margin drop vs no BG (hook) | Dry-to-reverb while singing (hook / song) | BG vs beat, 600–2 kHz (hook / song) | Mono corr (hook) | Collisions | Notes |
|---|---|---|---|---|---|---|---|---|
| **20 (old clip a)** | 19.98 / 20.00 | 4.85 / 5.05 | 0.15 | 30.33 / 30.00 | −12.76 / −12.25 | 0.998 | 0 | Below the audibility floor (matches "I can't really hear em") |
| **17 (recommended)** | 16.98 / 17.00 | 4.71 / 4.90 | 0.30 | 27.33 / 27.00 | −9.76 / −9.25 | 0.996 | 0 | Quietest rung that meets all three rules. +3 dB = "a little louder" |
| **15** | 14.98 / 15.00 | 4.55 / 4.73 | 0.46 | 25.33 / 25.00 | −7.76 / −7.25 | 0.994 | 0 | Also meets every rule. This was v1 "fuller". Next step if 17 is still too quiet |
| **13** | 12.98 / 13.00 | 4.30 / 4.48 | 0.71 | **23.33 / 23.00** | −5.76 / −5.25 | 0.990 | 0 | Dry-to-reverb falls below 24 dB (reverb is locked to the copy). Lead clarity still OK |
| **11** | 10.98 / 11.00 | 3.94 / 4.10 | 1.07 | **21.33 / 21.00** | −3.76 / −3.25 | 0.985 | 0 | Same dry-to-reverb fail, larger. Lead margin still above 3.0 dB |

No rung dropped the lead below the 3.0 dB clarity floor. I did not change the reverb design on 13 or 11; those rungs are in the ladder only, and I am not recommending them.

## Recommendation: 17 dB under the lead
It is the quietest rung that is audible over the beat in its own band, keeps the lead's 800 Hz–4 kHz margin well above 3.0 dB (only 0.30 dB of the hook margin is lost), and keeps dry-to-reverb at 27.0 dB.

**Honest limit:** on the hook the BG sits 9.76 dB under the beat in 600 Hz–2 kHz, only 0.24 dB over the audibility floor. Under the words, against beat+lead in that same band, it is still 17.3 dB down. If 17 still feels too quiet, **15** also passes every rule and is 2 dB louder. 13 and 11 would need a lower reverb return to stay at or above 24 dB dry-to-reverb, and that would break the fixed relation I was asked to keep.

## Files
Previews, all under `/workspace/songs/Untitled_2026-11-25/gate2/`:
- `WIPTD_fresh_G2_Preview_BGup_ref_clipA_20dBunder_0m42-1m12_v2.mp3` (+ WAV)
- `WIPTD_fresh_G2_Preview_BGup_17dBunder_0m42-1m12_v2.mp3` (+ WAV)
- `WIPTD_fresh_G2_Preview_BGup_15dBunder_0m42-1m12_v2.mp3` (+ WAV)
- `WIPTD_fresh_G2_Preview_BGup_13dBunder_0m42-1m12_v2.mp3` (+ WAV)
- `WIPTD_fresh_G2_Preview_BGup_11dBunder_0m42-1m12_v2.mp3` (+ WAV)

Full-length v2 stems (24-bit 44.1k, beat length, start at 0:00), recommended rung only:
- `WIPTD_fresh_G2_BGLayer_17dBunder_v2_24b-44k.wav`
- `WIPTD_fresh_G2_ReverbBus_17dBunder_v2_24b-44k.wav`

The dry lead and the word-timed throws bus are still the v1 files (`WIPTD_fresh_G2_VocalsDry_passthrough_v1_24b-44k.wav`, `WIPTD_fresh_G2_ThrowsBus_Main_v1_24b-44k.wav`).

## Exit checks (`WIPTD_fresh_Gate2_exit_checks_v2.json`)
**57 pass / 3 fail.** Thresholds were set before the results. The v2 stems are a measured +3.00 dB scale of the v1 light BG and reverb (relation unchanged). BG is 17.0 dB under the lead in 1–4 kHz (21.35 dB broadband). Dry-to-reverb while singing is 27.0 / 26.92 dB. Lead vs beat+BG in 800 Hz–4 kHz is 4.9 dB. Sync is 0 samples. Mono correlation is 0.996. First words stay dry. No clipping or DC. Tails are below −60 dBFS.

**FAIL (3, carried from v1, throws were not changed):**
- Bridge repeat 3: −11.6 dB vs beat+dry in-band
- Outro "Adderall" repeat 2: −13.0 dB
- Outro "Adderall" repeat 3: −18.4 dB

These fail the −10 dB audibility floor because of the planned −5 dB/repeat fade against a full outro beat. Same numbers as v1.

## Please check (headphones, car, phone)
1. **0:44.9 (17 vs the old clip a, and vs 15):** the copy comes in on "these". Can you hear it now, and is the lead still clear and on top?
2. **0:46.4 and 0:58.5:** the throws are unchanged. Does the louder copy get in their way?
3. **If 17 is still too quiet, compare 15.** If it is too loud, say so and we can sit between 20 and 17, or go back.

Draft, not final.
