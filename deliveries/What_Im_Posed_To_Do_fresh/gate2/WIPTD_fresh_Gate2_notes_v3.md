# What I'm Posed To Do (fresh run): Gate 2 notes, v3

**Status: DRAFT, NOT FINAL.** Built by Mix And Master Plugin/Effect Pro on 2026-11-26 (America/Chicago). I can't hear. Everything below is measured.

**Request:** Kenshin picked the 13 dB-under ladder rung, then said "turn 13 up a little more."

**What changed:** the dry BG copy went up 2 dB from that 13 version, to **11.0 dB under the lead** in 1–4 kHz. The reverb return was **not** raised with it. The 13 version sat at 23.0 dB dry-to-reverb, below the 24 dB floor, so the return was lowered 1.25 dB (smallest 0.25 dB step that clears 24 dB). Duck, timing, telephone band, entry points, throws, and the v2 dry lead (no reverb on the lead) are unchanged.

## Measurements (pass/fail)

| Check | Hook (0:42–1:12) | Whole song | Floor | Result |
|---|---|---|---|---|
| BG vs beat, 600 Hz–2 kHz | −3.76 dB | −3.25 dB | (info; v2 audibility floor was −10) | clearly above the old −10 dB floor |
| Lead vs beat+BG, 800 Hz–4 kHz | 3.94 dB | 4.10 dB | ≥ 3.0 dB | **PASS** |
| Dry-to-reverb while singing | 24.58 dB | 24.25 dB (all singing) / 24.17 dB (BG sections) | ≥ 24.0 dB | **PASS** |

11 dB under passed clarity, so that is the level used (not a quieter fallback). Broadband the copy is 15.35 dB under the lead. Preview: −20.0 LUFS, encoded true peak −2.01 dBTP.

## Files
- Preview: `gate2/WIPTD_fresh_G2_Preview_BGup_11dBunder_0m42-1m12_v3.mp3` (+ 24-bit WAV)
- Stems: `gate2/WIPTD_fresh_G2_BGLayer_11dBunder_v3_24b-44k.wav`, `gate2/WIPTD_fresh_G2_ReverbBus_11dBunder_v3_24b-44k.wav`
- Dry lead and throws are still the v1 files.

## Exit checks
**57 pass / 3 fail.** The three fails are the same late throw repeats as v1 and v2 (throws were not changed): bridge repeat 3 at −11.6 dB, outro "Adderall" repeat 2 at −13.0 dB, and repeat 3 at −18.4 dB.

Draft, not final.
