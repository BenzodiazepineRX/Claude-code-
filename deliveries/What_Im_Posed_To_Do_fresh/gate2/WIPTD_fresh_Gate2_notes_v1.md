# What I'm Posed To Do (fresh run): Gate 2 notes, v1

**Status: DRAFT, NOT FINAL** (Kenshin hasn't approved it yet). Gate 2 covers the space, the throws and the background (BG) layer. Built by Mix And Master Plugin/Effect Pro on 2026-11-25.
I can't hear. Everything below comes from measurements. Kenshin's ears make the final call.
**Exit checks: 116 pass, 3 fail.** All 3 fails are the late, quiet throw repeats (see below). None was hidden, and none was moved to a pass.

## Input
- The input is Alpha's **Gate 1 v2 DRY** stems: all four vocals are -1.5 dB vs v1, because Kenshin said the vocals were too loud and the beat was hard to hear. The beat is the Gate 1 pocket beat (untouched). The v3 leads were **not** used, because they have a lead plate printed on them.
- Every Gate 2 level is set **relative to the lead**, so it follows any later change to the lead level.
- **No reverb was added to the main lead.** The stems already have printed reverb, and stacking reverb is a known dislike.

## Word timing (there wasn't any before)
- I ran faster-whisper medium.en on each section of the summed Gate 1 vocals (`words/words_sections_medium_v1.json` and `words/words_by_section_v1.json`). The lyrics come from speech recognition, so **Kenshin needs to confirm them**.
- Accuracy check against an independent energy-onset detector: the median |ASR start − onset| is **51 ms**, p90 is 77 ms, and only 35% fall within 40 ms. So the recognition is only used to **label** the words. Every time that matters (the BG entry points, throw word starts, P-centers and line ends) comes from 10 ms envelopes of the audio.
- `analysis/words/` from AUDIO ENGINEER & DAW only held a 6-word, low-confidence lead1 file when I checked, so I didn't use it. I also didn't use `timing_vs_grid.json` (its detector reads about 10 ms late and its section averages spread 25–40 ms).

## BG layer (copy of the lead, sample-exact, 0 offset)
| Section | Entry (word) | Time |
|---|---|---|
| A1 | word 5 "these" | 0:44.867 |
| B1 | word 5 "do" | 1:13.777 |
| B2 | word 5 "do" | 1:27.997 |
| A2 | word 6 "blunts" | 1:42.187 |
| Bridge (bridge voices) | word 5 "no" | 2:10.637 |
| B3 | word 5 "do" | 2:39.067 |

- **Which word:** in each section I used whichever of words 5 and 6 has the deeper energy dip just before it. The fade-in is 10 ms and finishes at that dip.
- **How it ends:** the copy runs to the end of the section. The stem that opens the next section is cut at the dip before its first word. The other stem finishes its phrase, including the printed tail.
- **Telephone tone:** high-pass at 600 Hz and low-pass at 2.0 kHz, applied zero-phase (24 dB/oct).
  - Why 600 Hz: the box hump sits at 430–530 Hz, so 480 Hz ends up about -10.7 dB on the layer.
  - Why 2.0 kHz: the beat masks the lead most at 2.0–3.2 kHz, so the layer stays out of that range.
  - Zero-phase keeps the copy at 0 samples vs the lead (measured lag 0 at 7 spots).
- **Ducking:** 3 dB, 10 ms attack, 111 ms release (1/16 note), keyed by the dry vocals in 1–4 kHz.
- **Level under the lead:**
  - **Light:** 20.0 dB under in 1–4 kHz (24.4 dB broadband).
  - **Fuller:** 15.0 dB under in 1–4 kHz (19.4 dB broadband).
  - Why: ATL v4 at 18 dB was the last level he didn't reject, and 14 dB was still "way too loud".
- **Against the beat:** in the layer's own 600 Hz–2 kHz band, light is 12.3 dB under the beat and fuller is 7.3 dB under. So the light version will be very subtle texture.

## Dreamy reverb (on the BG copy only)
- **Type:** synthetic stereo hall.
- **Decay:** RT60 = 1 bar (1.778 s, 78,400 samples). It's long, but it's 60 dB down within one bar, so it never stacks over more than one 2-bar call-and-response turn.
- **Pre-delay:** 1/16 = 4,900 samples (111.1 ms). This lands after the printed tail's 23 dB drop.
- **Band:** 600 Hz–3 kHz (keeps it out of the box and the S zone). Its low-mid share is **7.9 dB lower** than the dry voice's, so it's not tunnel-heavy.
- **Return ducking:** 6 dB, 10 ms attack, 222 ms release (1/8 note).
- **Return level, set for clarity first:**

  | Measure | Light | Fuller |
  |---|---|---|
  | Dry-to-reverb while singing (target ≥ 24 dB) | **30.0 dB** | **25.0 dB** |
  | Reverb vs beat in the gaps | -18 dB | -13 dB |

- **Honest limit:**
  - The tail only blooms **0.8 dB** louder in the gaps than while singing, because the gaps here are only 0.1–0.5 s long.
  - On the light version the reverb is probably too quiet to be heard as "dreamy".
  - My first attempt (reverb in the gaps equal to the BG level) gave fuller only 20.2 dB dry-to-reverb, which fails. A ducking sweep from 6 to 16 dB only reached 22.7. That attempt is kept in `versions/render_attempt1/`.
  - If Kenshin wants it dreamier, the next move is a higher return on the light version only, and he has to OK the trade-off on clarity.

## Throws (timed from the word: stressed-vowel P-center + exact note value)
Only 6 line ends in the song are followed by a real gap of 0.3 s or more on the combined vocal bus. B1 and B2 have no gaps, so they get no throws.

| # | Section | Word (ASR) | P-center | vs 1/16 grid | Gap | Main note (samples) | Repeats kept | Alt note |
|---|---|---|---|---|---|---|---|---|
| 0 | A1 | "enough" (Lead 1) | 45.986 | -18.3 ms | 0.50 s | 1/4 (19,600) | 1, repeat at 46.430 | 1/8d |
| 1 | A1 | "some" (Lead 2) | 57.815 | +32.9 ms | 0.50 s | dotted 1/4 (29,400) | 1, repeat at 58.482 (tail faded before the next word) | 1/4 |
| 2 | A2 | "enough" (Lead 1) | 102.903 | +10.0 ms | 0.50 s | 1/4 (19,600) | 1, repeat at 103.348 | 1/8d |
| 3 | A2 | "some" (Lead 2) | 114.728 | -54.4 ms | 0.51 s | dotted 1/4 (29,400) | 1, repeat at 115.394 (tail faded) | 1/4 |
| 4 | Bridge | "all" (BG 2) | 143.601 | +41.3 ms | 13.7 s | dotted 1/2 (58,800) | 3: 144.934 / 146.268 / 147.601 | 1 bar |
| 5 | B3 | "Adderall" (Lead 2) | 171.487 | +38.6 ms | 70.7 s | 1 bar (78,400) | 3: 173.265 / 175.043 / 176.821 | 1 bar (only value that fits) |

- **How the note was chosen:**
  - **Short gaps (A1, A2):** I used the value whose first repeat sits most centred between the line end and the next word ("not too early, not too late").
    - "enough": a 1/4 lands 250 ms after the line end and 250 ms before the next word. A 1/8d would leave only 139 ms after the line end.
    - "some": a dotted 1/4 leaves 321 ms after and 179 ms before. A 1/4 would leave only 99 ms after the word.
  - **Long gaps:** I used the shortest value whose first repeat lands after the held word ends. A 1/2 note misses the end of "all" by 1 ms, and "Adderall" is held 1.4 s.
- **Repeat 2 in the A1/A2 gaps:** it would land on the next line, so the collision gate drops it. These throws get 1 repeat each.
- **Copy:** the whole word from its real start, never longer than one repeat interval.
- **Tone:** band-passed 600 Hz–3.6 kHz, and each later repeat is darker (LP 3.6k, then 2.55k, then 1.8k).
- **Pan:** repeat 1 is 30% L, repeat 2 is 30% R, repeat 3 is centre.
- **Levels:** repeat 1 is -12 dB re the word, then -5 dB per repeat.
- **Collision scan:** [t-0.15 s, t+len] of all dry vocals, leaving out the source word. Collisions: **0**.
- **Grid-locked A/B (clip d):** the same throws with the repeat P-center moved onto the 1/16 grid. Offsets per throw: +809, -1451, -442, +2398, -1822 and -1704 samples.

## Exit checks (`WIPTD_fresh_Gate2_exit_checks_v1.json`, thresholds set before the results)
**PASS:**
- **Format:** beat length, 24-bit, 44.1k, stereo, start at 0:00.
- **Clean files:** no clipping, DC < 1e-4.
- **Lead passthrough:** identical to the Gate 1 v2 sum (max diff 0), and no transient shift (0 samples at 6 spots).
- **BG sync:** 0 samples.
- **BG level:** light 20.0 and fuller 15.0 dB under (±1 dB).
- **Dry-to-reverb:** 30.0 / 25.0 dB.
- **Reverb low-mid share:** -7.9 dB vs the dry voice.
- **Tails:** < -60 dBFS in the padded buffers and at the song end.
- **Delay math:** exact for every throw in all 3 renders (measured lag 0 samples).
- **Throw placement:** every first repeat lands in its gap, with 0 collisions.
- **Vocal-bus mono:** correlation 0.998 (light) / 0.993 (fuller), fold loss < 0.02 dB.
- **First words dry:** the first words of each section are dry, with no copy before word 5/6.

**FAIL (3):** later throw repeats measure quieter than the beat+vocals in their band by more than the 10 dB audibility limit.
- Bridge repeat 3: -11.6 dB.
- Outro "Adderall" repeat 2: -13.0 dB.
- Outro "Adderall" repeat 3: -18.4 dB.

These fail because of the planned -5 dB/repeat fade against a full outro beat. Fix if Kenshin wants them heard: about +3 to +6 dB on those repeats.

**Note:** my first attempt also failed a "BG silent before entry" check. That was a metric bug (its window included the previous section's own last phrase, which keeps its copy by design). The check was rewritten to test the copy of the stem that opens the section, and it passes. The attempt-1 log is kept.

## Previews (A1 hook 0:42.0–1:12.0, all at **-20.0 LUFS integrated**, true peak about -2.0 dBTP, every clip uses the v2 DRY lead)
| Clip | What it is |
|---|---|
| a | light BG + throws timed from the word (main option) |
| b | fuller BG + the same throws |
| c | light BG + the alt note values (1/8d on "enough", 1/4 on "some") |
| d | light BG + the main throws **locked to the grid** |
| ref | no effects (Gate 1 v2) |

## Please check (headphones, car, phone)
1. **0:44.9 (a vs b vs ref):** the copy comes in on "these". Does the lead stay clear and on top? Light or fuller?
2. **0:46.4 and 0:58.5 (a vs c vs d):** the throws on "enough" and "some". Do they feel just right, early or late? Which of a, c or d?
3. **2:24.9–2:27.6 and 2:53.3–2:56.8 (full stems):** the bridge and outro throws fading into the gaps. Are the 2nd and 3rd repeats loud enough?

Draft, not final.
