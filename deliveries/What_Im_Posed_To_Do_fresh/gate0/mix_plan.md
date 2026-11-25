# Mix Plan: Untitled (working folder `Untitled_2026-11-25`) (Gate 0)

*Status: draft, Gate 0 only. Nothing has been processed. Every number below was measured on this song's files (scripts in `session/`, raw results in `analysis/`). No agent can hear: Kenshin's ears decide.*

Inputs: `stems.zip` from Kenshin's Dropbox, unpacked into `src/` and set read-only (sha256 in `analysis/src_sha256.txt`). The zip also had a stray `/` entry, which was skipped.

## Song facts (measured)
| | |
|---|---|
| BPM (verified to the sample) | **135.000**. Detected on the beat (alternatives 67.5 / 90). Long self-match of the beat in the 1–6 kHz band at 8–96 bars: **96-bar drift −0.01 to 0.00 samples** (corr 0.92–0.97); the 8–96 bar fit gives 135.0000. The snare is on beat 3 (half-time feel), so 67.5 is the same grid at half speed. 1 beat = 19,600 samples and 1 bar = 78,400 samples, exact at 44.1 kHz. |
| Grid T0 | **182 samples (4.1 ms)**, from the snare's 50% attack on beat 3, median of 75 full-drum bars (IQR 182–183). Correcting for detector bias puts the kick and snare at about 100–240 samples (2–5 ms). Hats were not used. Bar *n* starts at 0.0041 + (n−1)·1.77778 s. |
| Key / sung range | The note set is **F major** (relative D minor). The 808 loop is G–Bb–F–C, 2 bars per note (Gm–Bb–F–C). The tonic is **unresolved between F major and G minor (Dorian)**: beat chroma scores F major 0.83 vs G minor 0.68, and tempo_key.py scores D minor 0.813 vs F major 0.810 (low confidence). Sung notes are mostly Bb, G, A, C and F. Sung range is **F2 (87 Hz) to C3 (131 Hz)** on the leads; both BGs sit between F2/G2 and A#2. |
| Length (beat vs last vocal) | Beat 243.6 s (4:03.6). First vocal 0:42.2 (pickup into bar 25). Last vocal ends 2:53.2 (bar 98). That leaves **70.4 s (about 40 bars) of beat after the last vocal**, after a 42.2 s (24-bar) intro. |
| Stems & roles | Lead 1 and Lead 2 trade lines (call-and-response, 2 bars each), so they are **not doubles**. "Background lead" and "Background lead 2" are **not backing vocals**: they sing a 9-bar bridge on their own (bars 74–82), trading 2 bars each, with 0–1% overlap with the leads. Beat = 2-track YouTube rip. |
| Source quality | **Lossy everywhere**: the beat stops at 15.6/16.6 kHz (−40/−60 dB) and every vocal stops at 16.0–16.5 kHz. **Printed reverb on all vocals**, cut to digital silence 0.4–0.65 s after each phrase. Vocals are dual-mono (L = R exactly). No clipping, and DC is negligible. The beat is not mastered. |

### 0.1 Inventory
| Stem | SR / bits / ch | Dur s | Start / end silence s | Sample pk dBFS | TP 4× dBTP | LUFS-I | Active RMS dBFS (active %) | DC | L/R corr | Bandwidth (−40/−60 dB) Hz | Exact-zero % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Beat (Y2Mate…160k) | 44100 / 16 / 2 | 243.60 | 0.00 / 0.39 | −3.47 | −3.34 | −20.45 | −21.64 (98.9) | 9e-06 | 0.949 | 15590 / 16570 | 0.08 |
| Lead 1 | 44100 / 16 / 2 | 169.12 | 42.23 / 0.00* | −5.20 | −5.20 | −23.60 | −25.77 (29.1) | 2e-06 | 1.000 | 16015 / 16489 | 58.3 |
| Lead 2 | 44100 / 16 / 2 | 173.43 | 44.42 / 0.24 | −5.87 | −5.86 | −23.37 | −25.62 (32.3) | 2e-06 | 1.000 | 16096 / 16548 | 58.0 |
| Background lead | 44100 / 16 / 2 | 141.60 | 128.31 / 0.31 | −10.26 | −10.25 | −25.67 | −27.81 (5.1) | 1e-07 | 1.000 | 16005 / 16284 | 91.9 |
| Background lead 2 | 44100 / 16 / 2 | 145.15 | 133.32 / 0.31 | −10.62 | −10.59 | −26.00 | −28.18 (5.1) | 1e-07 | 1.000 | 16005 / 16101 | 93.9 |

\* Lead 1's file ends while the signal is still above −60 dBFS, so its last tail may be cut short by the export. Every file shares one sample rate and starts at 0 s; the vocals carry leading silence and line up with the beat grid within the timing figures below. No resampling was needed.

### 0.2 Hidden blockers
| Check | Result (numbers) | Plan impact |
|---|---|---|
| Printed FX on vocals | **Yes.** Pooled tail after phrase ends: −23 dB re the phrase at 50 ms, still −45 dB at about 600 ms (about 40 dB/s, like a 1.5 s reverb). A dry known-answer test falls 30 dB in 10 ms. Median time to −40 dB: Lead 1 530 ms, Lead 2 510 ms, BG1 640 ms, BG2 340 ms. Mono files carry no stereo FX. | Add far less space. Don't use upward compression or riders that lift the tails (ATL and Wild Side lessons). Check the tail level after every dynamics stage. |
| Dry vs gated | **Region-gated.** 58% of the leads and 92–94% of the BGs is exact digital zero. Region edges are quiet (≤ −59 dBFS), but the printed tails are cut to zero at about −45 dB re the phrase, 0.4–0.65 s after each phrase. | Edge fades in Gate 1. A tail cut to zero can sound abrupt once compressed; check it. |
| Clipping | 0 runs of 3 or more full-scale samples, and no samples ≥ 0.999 on any stem. | None |
| Lossy source | Beat cuts off at 15.6–16.6 kHz (YouTube 160k). Vocals cut off at 16.0–16.5 kHz. | Keep top-end lifts modest (they lift artifacts). Ask for the beat WAV or trackouts and for the original vocal WAVs. |
| Leaked vocals in beat | **Not tested reliably** (no separation tool). The beat's 1–4 kHz band is −17 dB re total with no anomaly, but a producer voice tag can't be ruled out. | Kenshin should check 0:00–0:43 for a tag. |
| Copy-pasted sections | **Yes.** Lead 1 + Lead 2 bars 33–41 are pasted at bars 65–73 (corr 0.95–1.00), **placed +1,023 samples (+23.2 ms) late** of an exact 32-bar repeat. Lead 1 bars 41–43 are pasted at bars 89–91 (corr 0.93–0.999), placed **−1,714 samples (−38.9 ms)**. Lead 2 bar 54 is pasted at bar 98, placed −2,868 samples (−65 ms). The beat itself is a looped arrangement (96-bar match corr 0.92–0.97 at 0.0 drift). | The real structure is A–B–B–A–bridge–B. Ask before moving anything; offsets are logged. |
| Hard-tuned vocals | Share of confident pitch frames within ±10 cents of a semitone: **Lead 1 50.7%, Lead 2 38.7%, BG1 20.3%, BG2 19.2%**. Calibration: snapped synthetic 92%, untuned 23%. Narrow 2.8–4.8 kHz spikes ≤ 3.7 dB on the leads and ≤ 5.0 dB on the BGs. | The leads look **lightly or partly tuned** and the BGs untuned. Low confidence: only about 12 s of confident pitch per lead, because most of the delivery is rap or half-sung. Don't re-tune. |
| Noise / hum / clicks / plosives | In-region noise floor median −59 to −65 dBFS. 50/60 Hz comb prominence 4–6 dB on the leads (weak) and 10–12 dB at 50 Hz on the BGs (mild, at a very low level). **0 plosive events** (<120 Hz never above −30 dBFS and over the mids). High-frequency click candidates: 12 on Lead 1, 13 on Lead 2, 1 on each BG (times in `analysis/blockers_vocals.json`). They may be consonants; verify before fixing. | Gate 1 cleanup list: check the click candidates and the BG hum only if audible. |
| Beat already mastered? | **No.** −20.45 LUFS-I, max short-term −16.9 LUFS, PLR 17.1 dB, full-section crest 16.2 dB, 0 flat-top runs, peak −3.47 dBFS. | There is headroom. Never re-limit it. |
| 808 translation | 808 notes **F1 43.7 / G1 49.1 / Bb1 58.5 / C2 65.9 Hz**, so 3 of 4 sit under 60 Hz. Sub (20–60 Hz) is −5.3 dB re total. The 100–400 Hz envelope follows the 808 only weakly (r = 0.29). Side below 120 Hz is 20.1 dB under mid. No 808 stem. | Phones will lose most 808 notes. Plan measured harmonic support in Gate 3, and ask for trackouts. |
| Licensing (not audio) | "FREE … Type Beat" from YouTube | It needs a lease or credit before release. |

## Section map
Bar numbers count from T0. "Beat energy" is measured per bar (full-drum bars about −18.5 to −21.5 dBFS RMS, drums-out bars about −26 to −29).

| Time | Bars | Section | Vocals present | Beat energy |
|---|---|---|---|---|
| 0:00.0–0:42.7 | 1–24 | Intro (instrumental) | none | 1–9 keys only (−29 to −30), 10–17 808 enters with no drums, 18–24 full drums |
| 0:42.7–1:12.9 | 25–41 | **A1** (hook candidate; pickup at 0:42.2) | Lead 1 ↔ Lead 2, 2 bars each | 25–33 full, **34–37 drums out**, 38–41 full |
| 1:12.9–1:27.1 | 42–49 | **B1** | Lead 1 ↔ Lead 2 | full |
| 1:27.1–1:39.6 | 50–56 | **B2** (same melody as B1, chroma sim 0.98) | Lead 1 ↔ Lead 2 | drums with no 808 |
| 1:39.6–2:09.8 | 57–73 | **A2** (= A1, chroma sim 0.96–0.98; bars 65–73 pasted) | Lead 1 ↔ Lead 2 | 57 no 808, **58–65 drums out**, 66–73 full |
| 2:09.8–2:25.8 | 74–82 | **Bridge** | Background lead ↔ Background lead 2, 2 bars each (no leads) | 74–81 full, 82 drums out |
| 2:25.8–2:38.2 | 83–89 | Vocal gap | none (B3 pickup in 89) | drums out |
| 2:38.2–2:54.2 | 90–98 | **B3** (B melody; 89–91 pasted from 41–43) | Lead 1 ↔ Lead 2; last vocal ends 2:53.2 | full, 98 variant |
| 2:54.2–4:03.6 | 99–137 | Outro (beat only) | none | 99–105 variant, 106–113 no hats, 114–129 full, 130–137 outro fade |

Which part is the hook is **not confirmed**. A is the 16-bar block that repeats (and was partly copy-pasted). B is an 8-bar phrase sung 3 times. Kenshin needs to say which one is the hook (see Open questions).

**Timing vs grid** (median onset offset vs the 1/16 grid). These are raw detector values: the detector read +10 ms late on a known-answer test, so subtract about 10 ms. IQRs run 25–40 ms.
| Section | Lead 1 | Lead 2 | BGs |
|---|---|---|---|
| A1 (25–41) | −7.4 ms | −7.2 ms | |
| B1 (42–49) | −15.2 | −13.4 | |
| B2 (50–57) | −11.0 | −23.9 | |
| A2 (58–73) | +10.5 | +10.7 | |
| Bridge (74–82) | | | BG1 +22.4, BG2 +32.0 |
| B3 (89–98) | −24.4 (wide) | +4.3 (wide) | |

Reading: the leads mostly **push** ahead of the grid (about 15–25 ms after bias correction) in A1 and B. A2 sits about 15–20 ms later than A1, which matches the +23.2 ms paste offset. The bridge BGs sit on the grid or slightly behind. These are natural performance or placement offsets. **Nothing gets moved without asking.**

## Reference(s)
| Track | Integrated / hook short-term LUFS | Vocal pocket delta | Notes (valid as reference?) |
|---|---|---|---|
| **Not chosen yet. Ask Kenshin for 1–3.** There is no default reference. | — | — | Use it for tone, clarity, low end and loudness only, never for BPM, key or structure. |

## Artist intent (in their words + confirmation)
- Genre / emotion: *to confirm*. The beat is tagged "Post Malone x Juice WRLD type – Hold On" (melodic rap / pain-trap tendencies; a direction only).
- What must stand out: *to confirm* (the leads; is the bridge featured?).
- Creative FX requested (exact, confirmed): **none yet. Echoes: no default; ask Kenshin how he wants them on this song** (which words, note value, repeats, level, tone, ducking).
- Things NOT to do (from LEARNINGS): no unrequested teases, chops or fills. No stacked cuts or compressors. Don't lift printed reverb. Keep BGs from getting harsh or loud. No broad "below 600 Hz" cuts on the leads. Don't move or tune any performance without asking.

## Top 3 problems (with numbers)
1. **Lossy sources plus printed, cut-off reverb on every vocal.** The beat stops at 15.6–16.6 kHz (YouTube 160k) and the vocals at 16.0–16.5 kHz. The vocal tails sit at −23 dB re the phrase at 50 ms, decay about 40 dB/s, and are then cut to digital zero 0.4–0.65 s later. Any compression or riding will lift that room (the same cause behind "not clean" on Wild Side and "too much reverb" on ATL). Air can't be restored.
2. **Box resonance on both leads at 440–520 Hz.** The harmonic envelope shows a hump peaking at **+5.6 dB (Lead 1) and +5.7 dB (Lead 2) at 480 Hz**, next to a natural dip at 560–620 Hz (−2.5 to −5.9 dB). That's the same hump-next-to-hole pattern that made "What I'm Posed To Do" sound boxy or like a tunnel. It's a preview only; Gate 1 must re-measure it per section.
3. **Low end won't translate, and the source is limited.** The 808 notes sit at 43.7, 49.1, 58.5 and 65.9 Hz (3 of 4 under 60 Hz), the 100–400 Hz envelope follows the 808 only weakly (r = 0.29), and there's no 808 or kick stem. Phones will lose most bass notes. Any fix has to be measured harmonic support, not more sub.

Also noted: copy-pasted sections placed +23.2 ms (bars 65–73) and −38.9 ms (bars 89–91) off an exact bar repeat; a 42 s intro and a 70 s instrumental tail.

## Approach per vocal (directions to test, not settings)
| Vocal | Role | Cleanup | Tone direction | Dynamics direction | Space |
|---|---|---|---|---|---|
| Lead 1 | Call-and-response lead A (2-bar turns), lightly tuned | Edge fades on region and tail cuts. Verify the 12 click candidates. No de-hum unless audible. | HPF from the measured lowest note (F2 87 Hz stable, p05 96 Hz). One bell on the measured 480 Hz hump at most; don't deepen the 560–620 Hz dip. Modest presence/air (lossy). | One stage sized to the phrase spread. Watch the printed-tail level after it (tail expander only if the tails rise). | Little added (printed reverb). |
| Lead 2 | Call-and-response lead B | Same. 13 click candidates. | Same method on its own measurements (lowest stable G2 97 Hz, p05 F2 89 Hz). The hump repeats at 480 Hz with a dip at 560 Hz. | Same. Match Lead 1's perceived level per section. | Same as Lead 1, symmetric, both centred unless Kenshin wants otherwise. |
| Background lead | Bridge vocal (bars 74–82), trades with BG2. Not a backing layer. | Edge fades. Check the 50 Hz hum (+10 dB prominence at a −65 dBFS floor). | Its level and character depend on Kenshin's answer (featured bridge vs "telephone"/distant). Don't apply the ATL "18 dB under" rule: nothing plays under it. | Light. Don't ride up the tails (ATL lesson). | Printed reverb already; add little. |
| Background lead 2 | Bridge vocal, trades with BG1 | Same (50 Hz +12 dB prominence). | Same. | Same. | Same. Pan as a pair only if Kenshin wants them treated as one group. |

## Effects plan per section
| Section | Reverb | Delays / throws | Layers | Automation |
|---|---|---|---|---|
| All | Pending: printed reverb means little or none added. Decide after the reference. | **Pending Kenshin's echo answer** (no default). Grid math is ready: 1/4 = 19,600 smp (444.444 ms), 1/8 = 9,800, dotted 1/8 = 14,700, 1/16 = 4,900, 1/32 = 2,450 (55.556 ms). | No new layers unless asked. | Pending the hook confirmation (A or B gets the lift). |
| Drums-out bars 34–37 and 58–65 (A over a break) | | Natural throw space only if Kenshin wants echoes | | The vocal will sit very exposed; measure the pocket here separately. |
| Bridge 74–82, gap 83–89 | | Gap = 12.4 s with no vocal; a candidate for throws or tails if asked | | |

## Low end & beat plan
No 808 or kick stems, so work on the 2-track only. Measure first which element drives the peaks. Harmonic support for phones goes before any clipping, and only as far as the phone proxy improves without low-mid mud. The sub is already mono (side 20 dB under mid below 120 Hz). The beat is unmastered at −20.45 LUFS with 3.5 dB of sample-peak headroom, so just gain-stage it and never re-limit it. **Best fix: ask for the beat's WAV or trackouts.**

## Loudness strategy
Choose the loudness per song: the loudest target where the limiter does ≤ 3–4 dB on the loudest 1% of hits (measured directly), compared with Kenshin's chosen reference at matched loudness. True peak ≤ −1.0 dBTP, or ≤ −2.0 dBTP if louder than −14 LUFS, with AAC margin (+0.14–0.20 dB seen on Wild Side). The song has long drums-out stretches (bars 34–37, 58–65, 82–89) and a 70 s instrumental tail, which will pull integrated LUFS down, so judge the hooks' short-term loudness. No fixed number is carried over.

## Song-specific QC thresholds (set now, before results)
Most need the reference and Kenshin's answers first. Set now: tempo drift ≤ 2 samples per 96 bars (measured 0.01). Every delay is an exact integer-sample note value at 135 BPM. Edge fades on every region cut. The tail level after dynamics must be no more than 1 dB above raw (printed reverb). Lead and BG levels, pocket, hook lift and loudness: **TBD after the reference and intent are confirmed** (left null in `mix_config_v1.json`).

## Open questions for the artist (one at a time in chat)
1. What's the song called?
2. Which 1–3 reference tracks should we match (15–30 s of a hook is enough)?
3. How do you want the echoes on this one: which words, timing, how many repeats, how loud, or none?
4. Which part is the hook: **A** (0:42–1:13, comes back at 1:40–2:10) or **B** (1:13–1:40, comes back at 2:38–2:54)?
5. The "Background lead" parts sing the 2:10–2:26 bridge on their own. Should they be featured like a lead, or sound background/distant (like the ATL telephone tone)?
6. Bars 65–73 (1:53.8–2:11.6) are a paste of bars 33–41 placed 23 ms late, and bars 89–91 (2:36.4–2:41.8) are pasted 39 ms early. Keep them as you placed them, or line them up to the grid? Default: leave them.
7. Ending: the beat runs about 70 s past your last word (2:53). End around 3:07 (bar 105) with a fade, or keep the full 4:03? And keep the full 42 s intro?
8. Can you get the beat as a WAV or trackouts, plus dry WAV exports of the vocals? Both are lossy, and the vocals have reverb printed on them.
9. Does the beat have a producer voice tag at the start?
10. Is the beat leased or licensed for release?
11. Do you want a DSP render only, or a DAW mix sheet too? Any deadline?
