# What I'm Posed To Do (fresh run): Gate 1 notes, v1

**Status: DRAFT, NOT FINAL** (until Kenshin approves) · Gate 1 = vocal cleanup, tone and pocket · by Pro Mix & Master Agent Alpha · 2026-11-25
QC: 65 / 70 automatic exit checks pass. All 5 fails are the same resonance (box) hump. Each one is explained below and none was forced to pass.

I can't hear. Everything below is measured. Kenshin's ears make the final call (timestamps to check are at the end).

## Files (repo paths under `deliveries/What_Im_Posed_To_Do_fresh/`)
| File | What |
|---|---|
| `stems/v1/WIPTD_fresh_G1_Lead1_v1_24b-44k.flac` | Lead 1 cleaned, full length, 24-bit/44.1k dual-mono |
| `stems/v1/WIPTD_fresh_G1_Lead2_v1_24b-44k.flac` | Lead 2 cleaned |
| `stems/v1/WIPTD_fresh_G1_BackgroundLead_v1_24b-44k.flac` | Bridge voice 1 cleaned |
| `stems/v1/WIPTD_fresh_G1_BackgroundLead2_v1_24b-44k.flac` | Bridge voice 2 cleaned |
| `stems/v1/WIPTD_fresh_G1_Beat_pocket_v1_24b-44k.flac` | Beat with the vocal-keyed 2.54 kHz mid dip (the pocket) |
| `gate1/WIPTD_fresh_G1_Preview_VocalBeat_1m05-1m27_v1.mp3` | Vocals and beat, 1:05.8–1:27.1 (bars 38–50: end of A1 → B1), -20 LUFS |
| `gate1/WIPTD_fresh_AB_VocalOnly_raw_vs_G1_v1.mp3` | Vocal only. 0:00–0:21 raw, short gap, 0:22–0:43 Gate 1. Both at -20 LUFS |
| `gate1/WIPTD_fresh_AB_Mix_raw_vs_G1_v1.mp3` | Same excerpt with the beat. Raw vocals are set to the same lead-vs-beat level (-1.12 LU) as Gate 1, so only the cleanup differs. Both at -20 LUFS |
| `gate1/mix_config_v1_gate1.json` | Every value with why / source / since |
| `gate1/gate1_exit_checks_v1.json`, `gate1/exit_checks_v1.raw.log` | Exit checks |
| `session/gate1/*.py`, `*.json`, `*.log` | Scripts, sweeps and params. The whole chain can be re-run |

FLACs are a bit-exact copy of the 24-bit WAVs (verified sample for sample). Every stem has the same length as its source and starts at 0 s. Transient lag is -1 sample (≤ 2). **All five files carry one common -6 dB bus offset** for headroom, so balance is unchanged. Gate 3 sets the bus gain.

## Gate 2 handoff: the quiet background copy of the lead (Kenshin's new request)
- **Source stems (exact): `stems/v1/WIPTD_fresh_G1_Lead1_v1_24b-44k.flac` and `stems/v1/WIPTD_fresh_G1_Lead2_v1_24b-44k.flac`.** On the box they are `/workspace/songs/Untitled_2026-11-25/gate1/WIPTD_fresh_G1_Lead1_v1_24b-44k.wav` and `..._Lead2_v1_24b-44k.wav`. SHA256 values are in `stems/v1/SHA256SUMS.txt`.
- Duplicate these stems. Don't re-process the dry lead. They are already cleaned, sample-aligned to the beat and at the pocket gain (lead gain -0.84 dB, B3 turns -0.67 dB) plus the -6 dB bus offset.
- Kenshin's brief: it comes in about 5–6 words into each verse (A1 starts 0:42.1, A2 starts 1:39.6, from the 0:42.2 pickup) and runs quietly underneath, with telephone tone, dreamy reverb and a few echo throws. Plugin/Effect Pro builds it in Gate 2.
- Set its level against `WIPTD_fresh_G1_Beat_pocket_v1_24b-44k`. That beat's mid dip is keyed by the main vocals only, not by the copy.
- Caution: the leads carry **printed reverb**, so the dreamy reverb adds to existing room. The copy is quiet and band-limited (telephone), which helps.
- The exact word-entry points have not been picked, because I have no lyric/word timing. Gate 2 or Kenshin needs to confirm where "word 5–6" falls in each verse.

## Chain (per vocal, in this order; all causal, float, sosfilt)
Edge fades → gain stage to -18 dBFS active RMS → turn rider (leads only) → HPF → one bell → one compressor → tone → one de-esser → pocket gain.

| Stage | Lead 1 | Lead 2 | BG 1 | BG 2 | Why |
|---|---|---|---|---|---|
| Edge fades | 10 ms in / 15 ms out | same | same | same | Every region and printed-tail cut ends in exact digital zero. Raised-cosine fades stop clicks. Content was not moved, pasted sections are untouched and nothing was tuned or added. |
| Gain stage | +7.40 dB | +7.39 | +9.57 | +10.10 | Brings each stem to -18 dBFS active RMS, so the compressor and de-esser thresholds are relative. |
| Turn rider | ±1.5 dB max, corrects 50% of each 2-bar turn's deviation; gain changes only inside the digital silence between turns | same | none | none | Raw turn spread was large (Lead 1 p90–p10 3.89 dB). It is changed only in silence, so tails are never lifted. |
| HPF (4th order) | 69 Hz | 72 Hz | 78 Hz | 71 Hz | Set from the lowest sung note (86.8 / 89.4 / 97.6 / 89.3 Hz): loss at that note is 0.64–0.71 dB. It also takes down the 50 Hz hum on the BGs (raw had +10 / +12 dB prominence at -65 dBFS). |
| Bell (one, RBJ peaking) | 474 Hz, Q4.2, -6 dB | 474 Hz, Q5.0, -6 dB | 450 Hz, Q3.8, -6 dB | 450 Hz, Q5.0, -6 dB | Harmonic-envelope hump: raw pooled +5.56 / +5.74 / +5.49 / +6.63 dB at 440–480 Hz. Swept through the chain at the 6 dB cap (details below). |
| Compressor (one) | thr -19.96 dBFS | -19.01 | -19.70 | -19.36 | Threshold = measured active RMS (+0 dB), 3:1, attack 10 ms, release 111.1 ms (1/16 at 135 BPM), knee 6 dB, RMS 5 ms detector, no lookahead. Average GR while singing is 1.37–1.43 dB, p95 about 3.15 dB. This was the largest crest reduction in an 18-setting sweep that kept punch within ±1 dB, attack ≥ 90% and printed room ≤ raw + 1 dB. |
| Tone | high shelf +1.5 dB @ 6 kHz (S 0.7) + bell +1 dB @ 2.8 kHz Q1 | same | same | same | The take is very dark: 5–10k vs 1–2k is -18.6 / -17.5 / -21.2 / -20.0 dB. For comparison the beat is -1.9 and Kenshin's refs are -10.1 (WOW), -2.8 (Fiji Falls) and 0.0 (XXX). The sources are lossy (16 kHz cutoff) and Kenshin dislikes harsh, scratchy sound, so the lift is modest. Presence sits at 2.8 kHz, just below the 3.6–5 kHz source hole. |
| De-esser (one, dynamic bell, after tone) | 6.0–10.1 kHz (7.78 kHz, Q1.9) | 7.1–10.1 kHz (8.49 kHz, Q2.87) | 8.5–14.3 kHz (11.0 kHz, Q1.9) | 7.1–10.1 kHz | Threshold = 97th percentile of the S-ness detector, 4:1, cap 6 dB, 1 ms / 55.6 ms (1/32). Active 10.3 / 9.3 / 13.8 / 10.8% of singing. p90 was on about 29% of the time in the sweep, which was too much. |

Pocket:
- Lead gain is -0.84 dB on both leads, BG gain -0.93 dB, and the B3 turns are trimmed -0.67 dB. B3 is sung about 2.5 dB hotter; attempt 1 put it at -0.34 LU, outside the range.
- Target is lead vs beat **-1.0 LU** (range -1.5 to -0.5) on full-beat bars, which sits inside the beat. Kenshin's last note (Wild Side, -0.43 LU) was "main vocals too loud, not clean enough".
- Beat mid dip: **2540 Hz, Q1.41, max 1.85 dB**, beat mid channel only (sides untouched), keyed by the summed vocals, attack 13.9 ms (1/128), release 222.2 ms (1/8). It is engaged more than half depth for 47% of the song.
- Why: the vocal-over-beat margin at 2–3.2 kHz was 2.2–3.3 dB, which is 2.6–3.7 dB under the median margin. The depth is half the worst deficit. 4 kHz was excluded because the vocal has a source hole there.

References: Kenshin-supplied WAVs (lossy-origin), `/workspace/wipd_refs/kenshin/`, SHA256SUMS verified: WOW (Chris Travis) -11.1 LUFS, Fiji Falls -11.8, I Don't Wanna Do This Anymore (XXXTENTACION) -9.1. They are used only loosely for tone (lossy top end). There are no vocal stems for them, so no pocket delta was taken from them.

## Exit checks (frozen files, measured at matched level)
| Check | Lead 1 | Lead 2 | BG 1 | BG 2 |
|---|---|---|---|---|
| Hump 440–520 pooled (≤ +2.5) | +5.56 → **+2.68 FAIL** | +5.74 → +2.46 PASS | +5.49 → **+3.08 FAIL** | +6.63 → **+3.15 FAIL** |
| Hump per section (≤ +3.0) | A1 2.45, B1 **2.39** (was 3.66 before refinement), B2 1.27, A2 2.69, B3 1.68: all PASS | A1 2.44, B1 0.65, B2 0.84, A2 2.77, B3 -0.15: all PASS | Bridge **3.08 FAIL** | Bridge **3.15 FAIL** |
| 560–620 dip not deepened | -1.67 → -1.52 PASS | -2.97 → -2.11 PASS | -2.57 → -1.77 PASS | -2.41 → -1.73 PASS |
| Punch ±1 dB / attack ≥ 90% | 12.95 → 12.71 / 100% | 12.33 → 12.03 / 100% | 14.66 → 14.78 / 100% | 11.01 → 10.75 / 101% |
| Harshness flare 2–5k ≤ raw + 1 | 15.53 → 14.31 | 12.50 → 11.70 | 13.36 → 11.81 | 8.50 → 8.57 |
| S-spike ≤ raw | 34.29 → 31.73 | 38.25 → 36.01 | 36.18 → 34.15 | 37.50 → 33.51 |
| Brightness (raw → G1) | -18.60 → -17.62 | -17.54 → -16.38 | -21.24 → -19.76 | -19.99 → -19.16 |
| Printed room not lifted (tail / room) | -29.58 → -28.85 / -23.14 → -23.43 | -25.34 → -29.85 / -21.05 → -22.80 | -26.97 → -33.95 / -23.14 → -23.87 | -27.33 → -30.53 / -22.02 → -23.17 |
| Turn spread p90–p10 | 3.89 → 1.00 dB | 3.04 → 0.76 | 0.33 → 0.28 | 0.28 → 0.10 |
| Peak / TP | -9.06 dBFS / -9.04 dBTP | -6.26 / -6.23 | ok | -9.46 / -9.46 |

Lead 1 tail -28.85 vs raw -29.58 is +0.73 dB, inside the +1 dB limit. It is the compressor's makeup on the cut-off printed tails. Check it by ear (see below).

**Pocket** (lead vs beat, full-beat bars, midband 800 Hz–4 kHz vocal minus beat):

| Section | LU | Midband |
|---|---|---|
| A1 | -1.40 | +4.63 |
| B1 | -0.87 | +5.10 |
| A2 | -1.13 | +5.02 |
| B3 | -1.00 | +5.15 |
| Bridge | -1.00 | +5.74 |

All PASS. Info only (the beat thins out here, so Gate 3 automation decides): B2 with no 808 is +4.28 LU, A1 drums-out +6.27, A2 drums-out +6.60. Beat: lag 0, peak -9.60 dBFS.

## The 5 FAILs: what was tried and what would fix them
- **Lead 1 pooled hump +2.68 (limit 2.5).**
  - Sweep 3 tried centre 466/474/482 × Q 3.4/4.2/5.0, through the chain, at the 6 dB cap. No setting reaches 2.5 (best about 2.67).
  - The chosen 474/Q4.2 fixes the B1 section fail (3.66 → 2.39) and keeps every section ≤ 3.0.
  - Not deepened past 6 dB (standard). No second bell was stacked. The 560–620 dip was not deepened.
- **BG 1 / BG 2 hump +3.08 / +3.15 (pooled = Bridge, limits 2.5 / 3.0).**
  - The BG checks had crashed (All-NaN: too few harmonics per bin on two short turns). The check now uses min 10 harmonics per bin and NaN counts as FAIL.
  - Once measurable, the old bells (465/Q3.8 at -4/-5 dB) read +4.33 / +4.84, so I re-swept: 430–495 Hz × Q 2.5–6.5 × 5/6 dB (`sweep_bell_bg*.log`). The best settings at the cap are 450/Q3.8 and 450/Q5.0. They were re-rendered and improved by 1.25 / 1.69 dB, but none reaches the limit.
  - The peak bin jumps between 440 and 480–500 Hz from setting to setting. With about 1.5 s of voice per stem, this measurement is **low confidence** (min 10–19 harmonics per bin).
- **What would really fix it:** dry vocal exports (no printed reverb or processing) or a different mic position or room. The harmonic envelope under-reads true bells (a 6 dB bell reads as about 3.1 dB in calibration), so the real box resonance is probably deeper than one 6 dB cut can remove.

## Honest limits and my mistakes
- **Lossy sources:** vocals stop at 16.0–16.5 kHz and the beat at 15.6–16.6 kHz (YouTube rip). The voiced vocal spectrum has a deep 3.6–5 kHz hole (about -36 dB re 1 kHz), so presence and air can't really be restored. The tone lift is kept modest on purpose.
- **Printed reverb on every vocal,** cut to digital zero 0.4–0.65 s after phrases. I can soften the cuts (edge fades) but can't remove the reverb.
- Lead 1's file ends while the signal is still above -60 dBFS, so its last tail may be cut off in the export. I didn't extend or invent anything.
- The beat dip behaves almost statically during dense call-and-response (the vocals rarely stop).
- B3 has a section trim (-0.67 dB) so it sits in the same pocket as the other sections.
- Process mistakes, all fixed (history in `gate1/versions/`):
  - Attempt 1: B3 out of range. The first trim silently failed because it looked for exact zeros in processed audio, so it now uses raw regions.
  - Attempt 2: stems clipped at 0 dBFS. Fixed with the -6 dB common offset.
  - Vocal LUFS were measured mono (3 dB low). Fixed with dual-mono measurement, which put the vocals about 3 dB lower.
  - The harmonic envelope is level-dependent, so it is now compared at matched level.
  - MP3s at -16 LUFS decoded to +1.6 dBTP, so previews now go out at -20 LUFS (decoded TP -2.2 to -2.3 dBTP).
  - The exit checks crashed on BG 1. Fixed, and that run exposed the BG hump fails (attempt 5 → final).
  - Before the bell refinement: Lead 1 B1 3.66 and Lead 2 pooled 2.77. Both are fixed.
- Nothing was moved, tuned or added. Pasted sections stay at their logged offsets (+23.2 ms bars 65–73, -38.9 ms bars 89–91, -65 ms Lead 2 bar 98).
- No reverb or delay was added (Gate 2).

## Please check (headphones, car, phone)
- **1:05–1:27** (preview and A/B): is the lead inside the beat but clear? Compare raw vs G1 in the A/B. Does the boxy 470 Hz sound go away without turning thin? Is anything harsh or spitty in the "s" sounds?
- **1:12.9–1:27.1 (B1):** Lead 1's box hump was worst here. Is it still boxy?
- **2:09.8–2:25.8 (Bridge):** BG voices are at lead level for now (-1.0 LU). Is any box tone left (the measured residual is +3 dB)?
- **2:36.4–2:54.2 (B3):** sung hotter and trimmed -0.67 dB. Does it still feel like it lifts enough?
- **Ends of turns anywhere:** the printed reverb tails are cut. Do any cuts sound abrupt after compression?
- **Thin-beat bars (A1 drums-out bars 34–37 ≈ 0:58.7–1:05.8, B2 no-808 bars 50–56 ≈ 1:27–1:41, A2 drums-out bars 58–65 ≈ 1:41–1:57):** the vocals sit +4 to +6.6 LU over the thin beat. That is left for Gate 3 automation.

## Decisions for Kenshin
1. Hook: is A or B the hook (which gets the lift)?
2. Bridge voices: featured or distant/telephone? Their final level and depth wait on this answer.
3. Drums-out and B2 sections: OK to ride the vocals down there in Gate 3?
4. Can you send dry/original vocal WAVs (no printed reverb) and the beat WAV or trackouts? That is the real fix for the box hump, the top end and the room.
5. Accept the residual box hump (Lead 1 +2.68 pooled, BGs about +3.1), or re-record / supply dry files?
6. Echoes: yes or no, and where (besides the new lead background copy). Also confirm where "word 5–6" falls in each verse for that copy.
7. Beat lease or credit (it's a "FREE … Type Beat" from YouTube).
8. Ending and length: there's a 70 s instrumental tail, and Lead 1's last tail may be cut off in the export.

Draft, not final.
