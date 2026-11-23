# Mix & Master Lessons Notebook

Read this at the start of every job.

## Artist voice profile (Kenshin)
- Deep male voice. Most-sung notes are D3/C#3/B2, and the **lowest is B2 at 123 Hz**, so high-pass at 80 Hz (never above about 100).
- Recurring mic/room rings: **~433 Hz, ~576–579 Hz, ~1007 Hz** (lead takes) and **~253 Hz** (adlibs). Check these first on the next song.
- Style: LEAD 1 / LEAD 2 **call-and-response** (not doubles), adlibs panned left, a telephone-effect lead for bridges.
- Stems arrive with **effects printed on them** (echo about 300 ms after phrases, reverb about 1 s) and band-limited at about 16 kHz (likely a BandLab/MP3 path). Ask for dry 24-bit WAV exports.
- Even the processed vocals stay **spiky** (raw crest about 19 dB). What worked: fast stage −15 dB / 6:1, then a −7.5 dBFS oversampled peak limiter **with latency=true**.
- Presence: compression plus saturation already brighten this voice by about 1.5 dB, so keep tone EQ at **+1 dB @ 3.2 kHz and +0.5 dB air**. +2 / +1.5 measured over spec.

## Process lessons (Old Motorola, Nov 2026)
1. **Gain-stage the mix bus to −6 dBFS before any glue compressor.** Otherwise the threshold is meaningless (v1 lost about 6 dB to the glue).
2. **Measure real limiter gain reduction** (pre vs post, 10 ms peak blocks). The "LU off" estimate is skewed by quiet intros.
3. A quiet intro plus loud hooks makes the limiter squeeze hooks hardest. **Do hook-vs-verse lift as post-limiter verse attenuation.** Pre-limiter lift gets eaten (0.9 LU → 0.3 LU).
4. Asymmetric (even-harmonic) saturation makes the limiter generate DC. Use a 20 Hz high-pass before the limiter and a 12 Hz zero-phase DC block after, then ceiling −2.3 so the result lands ≤ −2.0 dBTP.
5. Check every peak limiter for latency. ffmpeg `alimiter` needs `latency=true` or it delays the signal (0.48 ms at 0.5 ms attack).
6. **808s around 40–45 Hz vanish on phones.** A harmonic enhancer (saturate <120 Hz, keep 150–900 Hz, −10 dB) moved phone translation from 0.23 to 0.37.
7. Write QC checks that compare like with like: master vs unmastered mix for clicks, vocal vs raw vocal at matched loudness for tone, 1–4 kHz for intelligibility, and the transient band for timing (low-frequency phase fakes a time shift).
8. Moving averages on 7M-sample files: use cumsum, never `np.convolve` with long windows (that turned 1 s into 30+ min).
9. Throws need real gaps. With tight call-and-response, throw only into section breaks.

## Process lessons (What I'm Posed To Do, Nov 2026)
1. **Kenshin's voice goes down to F2 (87 Hz)**: high-pass at 65 Hz on this song. Re-check the lowest note every song.
2. Dry stems are a gift: build all the space, timed to the BPM. Duck the ambience delay 12 dB by *all* vocals so it fills only the micro-gaps.
3. **Measure timing against the beat grid, not hook vs hook.** Hook 2 looked 23 ms "late" vs Hook 1, but against the grid it was on time and Hook 1 was pushing. Nothing needed moving.
4. Verify the beat tempo to the sample (a 96-bar self-match) before grid-locking fills. Then move fills by whole bars only.
5. Heavy-808 YouTube beats: the 808 rides the limiter. Use a glue **sidechain HPF at about 600 Hz** (150 Hz still hears the added harmonics) and accept a lower integrated LUFS rather than >4 dB of limiting.
6. Clip thresholds relative to the global peak miss the loud sections when the biggest hit lives in a quiet section. Check where the peak is.
7. The 808 enhancer must come **before** any clip, or its harmonics raise the peaks.
8. QC scripts must read the **actual** mix gains (a stale +1 dB made the lead look 1.5 dB too loud).
9. Don't nest heredocs in generated scripts. Pass settings through environment variables instead.
10. Run heavy QC rounds one or two at a time (three in parallel ran out of memory).

## Scores (self-assessed from measurements; replace with the artist's feedback)
| Song | Vocal clarity | Balance | Low end | Effects | Loudness & translation | Emotion |
|---|---|---|---|---|---|---|
| Old Motorola v5 | 8 | 8 | 6 (lossy beat, no 808 stem) | 7 (printed FX limit control) | 8 | **artist loved it** |
| What I'm Posed To Do v10 | 8 | 8 | 6 (sine 808, YouTube rip) | 9 (dry stems, grid-locked fills) | 7 (−13.8 LUFS to keep it clean) | needs artist's ears |

**Next song, aim at the lowest score (low end):** get the beat's trackout stems so the kick and 808 can be balanced separately.

## Artist feedback
- **Old Motorola v5:** "absolutely amazing… I loved it." Keep this approach: measured, vocal-forward, light space when FX are printed.
- **What I'm Posed To Do v10 → v11:** the intro tease sounded off-beat and "cut in" → **don't add teases/chops without asking first**. Lead too loud at +2.9 LU → **Kenshin likes the lead about +1.3 LU over the beat**, not on top. Wanted audible reverb, but at 10.8 dB under with 2 dB ducking and a 27 ms pre-delay he heard it as **boxy / "tunnel"** → his "clear pro reverb": **pre-delay 1/32 (≈55 ms), send HP 600 Hz / LP 7.5 kHz, decay about 3 beats, duck 6 dB, about 18 dB under, dry ≥ 20 dB over reverb while singing**. Wants **background vocal layers with echo throws**: build doubles from the takes (**11/17 ms, ±10 cents, HP 350, about −9 dB, hooks only**; 21/29 ms at −6 dB sounded phasey/boxy) plus a 1/4-note echo on every line end (about 10 dB under).

## Rule of thumb: synthetic doubles and reverb
- Keep doublers inside the doc spec (10–20 ms, 5–12 cents) and check stereo correlation ≥ 0.9 on the vocal bus.
- Before calling reverb "audible", measure **direct-to-reverb while singing** (aim ≥ 18–20 dB) and the reverb's 250–600 Hz share vs the dry voice. A box-heavy reverb = tunnel.

## Process lessons (What I'm Posed To Do v14–v15, with ARMY)
1. **"Boxy" or "dull" → compare the vocal tone, band by band, to an approved reference of the same voice (Old Motorola)** before adding more cuts or boosts. That found the real box bump (500–630 Hz) that three earlier versions missed.
2. **ARMY's rule: keep box fixes surgical (500–630 Hz); never cut "everything below 600" on a lead.** Broad cuts thin the voice and add dullness. Broad high-passes belong on BG layers only.
3. Ask whether the box is baked in: test for room reflections on **noise-like frames only** (breaths and S's, no pitch), with a known-echo sanity test. A tonal bump is fixable by EQ; reflections are not.
4. Kenshin's raw takes can be recorded much darker than his last session. Re-check presence every song instead of reusing the last EQ.
5. Kenshin and ARMY prefer the lead **at about 0 to +0.5 LU vs the beat** and the reverb **at about 20 dB under** (dry ≥ 24 dB over reverb while singing).
6. Raising the beat raises the mix's low-mids. Re-check mud after any beat-level change.

## The big lesson (What I'm Posed To Do v16, prompted by ARMY)
1. **Fix one measured fault with one precise move.** Eight overlapping cuts in 300–1000 Hz lowered the region, left the box hump standing out and hollowed a natural dip. A hump next to a hole = boxy.
2. **Find resonances with the pitch-independent harmonic envelope** (scripts/harmenv.py): measure every note's harmonics and look for a hump all notes share. Plain spectra and fine notches confuse melody with resonance.
3. **Measure articulation** (consonant punch and attack in 2–5 kHz vs raw). Dull = squashed consonants. Use one compressor with a 15 ms attack; no vocal peak limiter, no stacked de-essers, no saturation by default.
4. **Never use a reference that has printed FX** for tone matching.
5. **Kenshin's voice (this mic):** resonance at 480 Hz (Q 3.5, −5.5 dB), a natural dip at 600 Hz (leave it), very dark top (+2.5 dB @ 3.2k, +4 dB shelf above 6k).
6. When collaborators (ARMY) push back with measurements, re-test assumptions from the raw. Don't keep stacking fixes on a flawed chain.
