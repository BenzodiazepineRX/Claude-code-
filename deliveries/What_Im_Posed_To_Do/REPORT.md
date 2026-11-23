# "What I'm Posed To Do" — Mix & Master Report (v16)

**Status:** v16. The lead vocal chain was rebuilt from the raw takes after ARMY's review. QC: **3 rounds (24-bit, 16-bit, decoded MP3), 47/48 each.** The 1 open item is the phone-speaker 808 check, a beat limit.

## v16: what was actually holding the vocal back (answer to ARMY)
ARMY was right: the raw take isn't the problem. **My processing chain was.** Measured:
1. **Box never removed, mids hollowed.** The raw lead has one real resonance, a **440–520 Hz hump peaking at +6.3 dB at 480 Hz**. This was confirmed with a pitch-independent test: every note's harmonics were measured, about 13,000 of them, and they all pass through it. Versions up to v15 cut 300–1000 Hz in **8 places**. That lowered the whole region, left the hump sticking out (+4.9 dB in v15), and **deepened a natural dip at 600–620 Hz** with a 630 Hz cut. A hump next to a hole is a textbook "boxy/hollow" vocal.
2. **Dull = squashed consonants.** The fast 1 ms 6:1 compressor, the peak limiter and three de-essers cut consonant punch from 12.4 dB (raw) to 9.8 dB, and attack speed by 12%. My QC never measured articulation, so it couldn't see it.
3. The "Old Motorola" match reference had BandLab reverb/delay printed on it: a wet reference for a dry voice.

**v16 lead chain (rebuilt from raw, simple and surgical):**
| Stage | Setting |
|---|---|
| High-pass | 65 Hz (below his lowest note, F2) |
| **One cut** | **−5.5 dB @ 480 Hz, Q 3.5** (covers the 440–520 Hz hump; within the doc's 6 dB rule; nothing at 600 Hz+) |
| One compressor | 3:1, **15 ms attack** (consonants pass), 120 ms release, about 4.5 dB on loud phrases |
| Tone | +2.5 dB @ 3.2 kHz (broad), +4 dB shelf above 6 kHz (raw is very dark: −17.8 → −12.3 on the brightness measure) |
| One de-esser | 5–9.5 kHz, only the biggest S's (10–17% of the time) |
| Volume rider | ±3 dB phrase levelling (gain only) |
| **Removed** | fast compressor, saturation, vocal peak limiter, 2 extra de-essers, match EQ, all extra low-mid cuts |

**Measured result:** box hump +6.3 → **+3.5 dB**; 600 Hz dip −3.1 → −2.4 (not deepened); **consonant punch 12.6 = raw 12.6** (v15: 9.8); attack 96% of raw; no harsher than raw. All vocal layers were rebuilt from this lead, at the same balance you approved in v15: lead +0.5 LU over the beat, reverb 20.6 dB under (dry 23.8 dB over reverb while singing), stack 13.6 dB under, echo BGs 9.5 dB under. Master: **−14.4 LUFS, −2.4 dBTP**, limiter 4.0 dB on the loudest hits.

**ARMY:** if you can share your v1 bounce or its vocal settings, I'll measure it with these same tools and close any remaining gap to the version Kenshin already liked.

## v14–v15 (superseded by v16): the box and the dullness
**Root cause, measured:** the raw take has a **tonal bump at 500–630 Hz (+3.8 dB vs the Old Motorola raw take)** and was recorded **up to 8 dB darker at 4–5 kHz**. My earlier box cuts (350–470 Hz) missed the bump, and my +1 dB presence lift was far too small.

**Is the box "baked in" as room sound?** Tested on breaths and S/SH sounds only, which have no pitch, so any repeating pattern can only be a reflection. A sanity test detects a known 3 ms echo (0.356) and reads 0.006 with none. **No room reflections in the 2–15 ms small-box range.** There's a small 0.09 blip at about 1 ms, which the Old Motorola take shares, so it's the natural shape of those sounds. So the box is a **tonal bump in the take**, fixable by surgical EQ without thinning; it isn't room sound, which EQ couldn't fix.

| Change | Detail | Measured |
|---|---|---|
| **Reference match EQ on the lead** (linear phase) | match to the Old Motorola vocal Kenshin approved, 500 Hz–10 kHz only. **Surgical box cuts:** 500 −2.5 / 630 −2 / 800 −1.5 / 1k −1 dB. **Presence:** +1.4 to +2.3 dB at 1.6–3.2 kHz, +2.6 / +3.2 dB at 4 / 5 kHz, +0.6 / +1.2 dB at 8 / 10 kHz. **No new cuts below 500 Hz; HPF stays 65 Hz** | tone within **±1.7 dB** of the reference (box zone 0.0, presence −0.2); 300–600 Hz −2.8 dB vs raw (gentle) |
| Re-de-ess after the brightening | 5.5–9 kHz, max 6 dB, on S's only (14–21% of the time) | harsh flare-ups lower than raw (11.4 vs 13.6 dB); S-spikes 25 vs 33 dB raw |
| All vocal FX rebuilt from the corrected voice | stack, echo BGs, throws, plate | — |
| Lead −1.5 dB vs beat (ARMY) | beat +1.5 dB, every vocal layer keeps its balance | lead **+0.3 LU** (sits *in* the beat); words still **6.2 dB** clear in 1–4 kHz on phone, earbuds, car, club, laptop and mono |
| Reverb −3 dB (ARMY) | same clear plate design | **20.7 dB** under; dry over reverb **24.2 dB** while singing, 11.5 dB in gaps |
| BG stack −3 dB, **HP 600 Hz on the stack only** (not the lead) | it was the boxiest layer | 13.6 dB under the lead in hooks |
| Beat −1.5 dB @ 400 Hz | the louder beat made the mix low-mid heavy | low-mid back within limit; limiter 3.5 dB |
| Loudness | | **−14.2 LUFS**, −2.4 dBTP |

## v13: "clear, pro reverb" (feedback on v11, kept in v15 at lower level)
**Measured cause of the tunnel:** in v11 your dry voice was only **13.2 dB** above its reverb while singing. The reverb was relatively heavier in the boxy 250–600 Hz range than your voice, its short 27 ms pre-delay smeared into the words, and the BG doubles (21/29 ms) were outside the doc's doubler spec.

| | v11 | **v13** |
|---|---|---|
| Plate pre-delay | 27.78 ms (1/64) | **55.56 ms (1/32)**: the word lands, then the space blooms |
| Plate send EQ | 300 Hz–8 kHz | **600 Hz–7.5 kHz**: no low-mid box |
| Plate decay | 1.78 s (1 bar) | **1.333 s (3 beats)**: clears before the next line |
| Plate ducking | 2 dB | **6 dB** |
| Reverb level | 10.8 dB under lead | **17.8 dB under** (doc: 12–18) |
| Dry over reverb while singing | 13.2 dB | **21.1 dB** (8.3 dB in gaps, so you still hear the space) |
| Lead "box" zone 300–600 Hz | — | **−1.9 dB vs your raw take** (extra −1.5 dB @ 420 Hz) |
| BG stack | 21/29 ms, ±9 c, −6 dB, hooks + verses | **11/17 ms, ±10 c (doc spec)**, −9 dB, **hooks only**, cut below 350 Hz |
| Vocal stereo correlation | 0.82 | **0.90** |
| Lead vs beat | +1.3 LU | +1.3 LU (beat −0.5 dB to keep it after the de-boxing) |
| Loudness | −13.7 LUFS | **−14.0 LUFS**: Spotify's playback level, so it isn't turned down at all; −2.4 dBTP |

## v11: earlier feedback (intro, level, reverb, BG layers)
| You said | What I did | Measured |
|---|---|---|
| Edited vocals before the lyrics are off-beat and "cut in" | **Removed** the intro tease and the reverse swell into 0:42. The intro is clean, and your first line starts exactly as you recorded it. Your own regions are **not** chopped: every region starts softly (−47 to −58 dBFS in the first ms). | vocals before 0:42: −148 dBFS (silence) |
| Main vocals too loud | Lead −1.6 dB overall, and −3 dB in the beat breakdowns | lead vs beat: **+1.3 LU** in full sections (was +2.9); breakdowns +4.9 (was up to +9) |
| No reverb like I wanted | Plate (1 bar, 27.78 ms pre-delay) made audible: return −11.5 dB, ducking reduced to 2 dB | plate **10.8 dB under** the lead (audible but slight) |
| Missing background vocals with echo throws | **New hook stack:** 2 doubles built from your takes (±9 cents, 21/29 ms, darker, extra de-essed), 100% L/R. **New echo BGs:** the last word of **all 28 lines** repeats as a 1/4-note (444.44 ms) ping-pong echo. **Bridge BG:** wider (60%), louder, with its own 1/4-note throws on each line end | stack **6.0 dB under** in hooks, 10.9 dB in verses; echo BGs **9.7 dB under** each line; bridge BG 2.3 dB under |
| Stream ready | −13.7 LUFS integrated, −2.4 dBTP true peak (Spotify asks under −2 dBTP when louder than −14), MP3/AAC encodes stay under 0 dBTP | limiter 3.8 dB on the loudest hits |

It stays "draft, not final" until you listen and approve.

![Before / after](What_Im_Posed_To_Do_Before_After.png)

## 1. Song facts

| | |
|---|---|
| Tempo | **135.000 BPM** (verified sample-exact over 96 bars). 1 bar = 1.778 s |
| Key | D minor (relative F major); the 808 sits on B♭1 (58.5 Hz) |
| Length | 3:08.8 (the beat ran to 4:03 with no vocals after 2:53, so it now ends with an 8-bar outro and a 4-bar fade) |
| Beat | "Hold On" type beat (Post Malone × Juice WRLD type), a **160 kbps YouTube rip** |

| Time | Section | What's there |
|---|---|---|
| 0:00–0:42 | Intro | beat only, clean (v11: tease and swell removed at your request) |
| 0:42–1:11 | **Hook 1** | LEAD 1 ↔ LEAD 2 call-and-response + BG stack + echo BGs |
| 1:11–1:39 | Verse 1 | drier and closer; second half over the beat breakdown |
| 1:39–2:08 | **Hook 2** | a re-edit of Hook 1 (same melody) + BG stack + echo BGs |
| 2:08–2:24 | Bridge | BG 1 and BG 2 in a round, panned left/right |
| 2:24–2:37 | Gap | **new:** half-note throw, ghost echo of the last BG line, reverse swell |
| 2:37–2:54 | Verse 2 | |
| 2:54–3:09 | Outro | final throw on your last word, beat fades over 4 bars |

## 2. Mix plan
- **Dry vocals:** no effects were printed on the stems, so every echo and reverb was built from scratch and timed to 135 BPM.
- **Your requests:** perfect timing, echo throws and delays, make it pop, fill the empty gaps. I answered each with measured, grid-locked moves.
- **Problems found:** an extremely spiky beat (a snare/clap with 23–27 dB crest), an 808 that's a near-pure sine (phone speakers can't reproduce it), a lossy beat (nothing above 16.5 kHz), and long empty stretches (a 42 s intro, an 8-bar gap, 70 s of unused beat).

## 3. Processing

### Vocals (LEAD 1, LEAD 2: same chain fitted to each)
5 ms fades on all 27 region edges → gain to −18 dBFS RMS → **high-pass 65 Hz** (your lowest sung note is F2 at 87 Hz) → static cuts on rings that stayed fixed across sections (L1: 350 / 468 Hz; L2: 331 / 487 Hz), −1.5 dB @ 300 Hz → dynamic EQ (L1 3.5 kHz, L2 3.16 kHz; acts about 20% of the time) → fast compressor (−15 dB, 6:1) then smooth compressor (−24 dB, 2.5:1), 6.5–7.2 dB total → de-esser (5–8 kHz, S/T/CH only) → +1 dB @ 3.2 kHz, +0.5 dB air → saturation (6 dB, 25%) → second de-esser → phrase rider (spread 3.0 → 2.3 dB) → oversampled peak limiter (−7.5 dBFS, latency-compensated).
Level: about **+2.9 LU over the beat** in full sections. Hooks +1.5 dB; −1.5 dB where the beat drops out, so your voice doesn't jump out.

### BG 1 / BG 2
High-pass 150 Hz, cuts at their fixed rings (BG1 5.6k; BG2 231 / 1157 / 5566 Hz), −1.5 dB @ 3 kHz, low-pass 11 kHz, same dynamics, harder de-ess, more grit. **Panned 35% left / 35% right** so the round spreads across the speakers. Sits 2.1 dB under the lead level (they carry the bridge).

### Effects: all from 135 BPM (exact sample counts)
| Effect | Setting |
|---|---|
| Shared plate | decay **1 bar (1.78 s)**, pre-delay **1/64 = 27.78 ms**, 350 Hz–8 kHz, ducked 4 dB by the vocals; +2.5 dB in sparse sections |
| Ambience delay | **1/4 = 444.44 ms** ping-pong, **ducked 12 dB** while anyone sings, so it fills the micro-gaps between your call-and-response lines |
| BG delay | **1/8 dotted = 333.33 ms** ping-pong, ducked 10 dB |
| Throws | 1/8d at **0:46.2 / 1:43.2** (the 1-beat pocket after hook line 1, matching in both hooks); 1/2 note (**888.89 ms**) at **0:58.3** (into the break), **2:24.5** (into the gap) and **2:53.2** (final word); 1/4 at **1:55.2** |
| Hook doubler | ±7 cents, 13 / 19 ms, hard left/right, **only in the hooks**, so they open up wider |
| Intro tease | Hook 2's first line, phone-filtered (500 Hz–3.2 kHz), placed **exactly 36 bars earlier** (0:35.05), with hall and 1/4 echo |
| Ghost echo | BG 2's last line, phone-filtered, **exactly 4 bars later** (2:27.1) in the gap |
| Reverse swells | the hall tail of your entry words, reversed, rising into **0:42.23** and **2:37.47** |

### Beat
Vocal-triggered pocket (−2.5 dB @ 2.8 kHz, mid channel, only while you sing) → −1.5 dB @ 300 Hz → 808 harmonics (−7 dB) → gentle 808 compressor (<150 Hz, evens notes 6.2 → 5.2 dB) → two-band transient clip (snare/clap −6 dB, kick −2.5 dB) → outro fade.

### Bus and master
Glue 2:1 with a **sidechain high-pass at 600 Hz** so the 808 can't make it pump (1.4 dB) → mono below 120 Hz, +0.5 dB mid air → 4x-oversampled limiter (3.8 dB on the loudest 1% of hits, median 0.0) → DC block → verses −1 dB after the limiter (hook lift +1.3 LU).

## 4. Before → after
| | Rough | **Master v10** |
|---|---|---|
| Integrated | −23.3 LUFS (A/B level) | **−13.8 LUFS** |
| Max short-term | — | **−11.3 LUFS** (hooks −11.7 to −12.1) |
| True peak | — | **−2.4 dBTP** (MP3 −2.31, AAC −2.19) |
| Correlation / mono loss | — | 0.95 / −0.12 dB |

**Why −13.8 LUFS?** Louder targets made the limiter crush this beat by 7–8 dB. I tried transient clipping, 808 compression and a sidechained glue, then chose clean over loud. Spotify plays everything at −14 LUFS, so this master is barely touched there and keeps its punch. The song also has long quiet sections, which pull the integrated number down even though the hooks are about as loud as "Old Motorola"'s verses. **A louder version is possible if you want it**, with the trade-off stated.

## 5. QC
| Round | File | Result |
|---|---|---|
| Dev (v6) | 24-bit | 35/39: flagged a "30 ms timing" issue, lead too loud, 808 on phone |
| v10 (all 3 rounds) | | 39/40: you then heard the intro, level, reverb and BG issues |
| v11 (3 rounds) | | 43/44: you then heard the reverb as boxy / tunnel |
| v13 (3 rounds) | | 45/46: Kenshin heard it boxy and dull, ARMY heard it too loud with too much reverb |
| v15 dev round | | 44/46: low-mid heavy after the beat went up → beat −1.5 dB @ 400 Hz |
| v15 (3 rounds) | | 45/46: ARMY flagged that the vocal still fell short of the standard |
| **R1 (v16)** | 24-bit WAV | **47/48**: only the phone-808 check open |
| **R2 (v16)** | 16-bit WAV | **47/48** |
| **R3 (v16)** | MP3, decoded | **47/48** |

v16 adds the checks that would have caught this early: **box hump (harmonic, pitch-independent)**, **600 Hz dip not deepened** and **articulation within 1 dB of raw**. The "match Old Motorola" check is retired, because that reference was wet.

v15 replaces the old "presence +1..+3 dB vs raw" rule (this take was recorded too dark for that rule) with **"tone matches the approved Old Motorola vocal within ±2 dB"**. Lead-level and reverb ranges follow the artist's requests, and the word-clarity and dry-over-reverb checks still guard both.

v13 adds clarity checks: reverb in doc range, dry ≥ 18 dB over reverb while singing, no added boxiness. All pass.

v11 adds 4 checks from your feedback: clean intro, BG stack depth, echo BGs on every line, and audible reverb. All pass.

**Open item, source-limited: the 808 on phone speakers.** In v16, translation is 0.24 vs the original beat's 0.17 (+35%). It's still marked FAIL, not hidden. The final limiter flattens the 808 the most, and the remaining fixes (more 808 distortion, or less sub) would hurt the song on real speakers. Per the doc's rule, I stopped after 8 attempts, short of my 0.3 target. I tried 7 fixes: three enhancer strengths, sidechain at 150 / 600 / 1000 Hz, and sub clipping at 3 / 5 dB. Pushing further added low-mid mud over your voice. Fix at the source: the beat's trackout stems, or an 808 sample with more harmonics.

**About timing ("perfectly timed"):** Hook 2 is a re-edit of Hook 1 placed 23 ms later. I measured both against the beat grid before touching anything. **Hook 2 lands right on the grid (+1.8 ms) and Hook 1 pushes slightly ahead (−22 ms, a natural singer's push).** Both are natural, so per your doc I did **not** move your vocals. Every effect is grid-locked: delays are exact sample counts, and the tease and ghost moved by whole bars on a beat verified at exactly 135.000 BPM.

## 6. Honest limits
- **The beat is a 160 kbps YouTube rip**: nothing above 16.5 kHz, and some lossy smear. Buying the WAV or trackouts is the biggest upgrade.
- The 808 on phones (above).
- **I added creative content** (the intro tease, ghost echo and swells), because you asked to fill the gaps. If any of it isn't your vision, use the **No Fills** master: same everything, minus those.
- **I can't hear.** Everything was measured; your ears decide.

## 7. Even better next time
Buy the beat's WAV or trackout stems. Keep the vocals dry like you did, which was perfect for this. Send 1–3 reference songs. Tell me any lines you want throws on and I'll add them by timestamp.

## 8. Files
| File | Use |
|---|---|
| `…_Master_v16_24b-44k.wav` | **main master** for your distributor |
| `…_Master_v16_16b-44k.wav` / `…_Master_v16_320k.mp3` | 16-bit / sharing |
| `…_Master_NoFills_v16_24b-44k.wav` (+ MP3) | same master **without** the gap's ghost echo and swell |
| `…_Instrumental_v16`, `…_Acapella_v16`, `…_TV_Track_v16` (beat + all BG layers, no lead) | alternates through the identical chain (null test −88.3 dBFS) |
| `…_Unmastered_Mix_v16_24b-44k.wav` | for future remasters |
| `…_AB_VocalOnly_v15_vs_v16.mp3` | **listen first**: the vocal alone, v15 then v16, at equal loudness |
| `…_AB_Hook1_v15_vs_v16.mp3` | Hook 1 full mix, v15 then v16, at equal loudness |
| `…_Before_After.png` | song map with every fill and throw marked |
| `session/` | all scripts and settings |

**Listen for:** 0:42 (clean entry into Hook 1 with the BG stack), the echo BGs after every line (0:46, 0:51, 0:55…), 0:58 (half-note throw into the break), 2:08–2:24 (wider bridge BG with throws), 2:24–2:37 (gap fill), 2:53 (final throw).
