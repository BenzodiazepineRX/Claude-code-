# 02: Deriving Every Setting From the Song

**Read this first:** the ranges below are *sanity bounds* and *starting points for a test*, **never settings**. For every parameter you set:

1. **Measure** the thing the parameter controls, on this song.
2. **Derive** a value from that measurement, the reference and the artist's intent.
3. **Process**, then **verify** with a measurement that it did what you intended, and nothing else.
4. **Log** it in `mix_config.json`: `value`, `why` (the measurement), `source` (measured / reference / artist request) and `version`.

If a derived value lands outside the sanity range, that's allowed when the measurement supports it. Write down why. If you can't justify a value, don't use it.

---

## Tempo-based values (exact math, never eyeballed)

| Value | Formula |
|---|---|
| 1/4 note | 60000 / BPM ms |
| 1/8 | 30000 / BPM |
| 1/8 dotted | 45000 / BPM |
| 1/8 triplet | 20000 / BPM |
| 1/2 | 120000 / BPM |
| 1 bar (4/4) | 240000 / BPM |
| 1/32 | 7500 / BPM |
| 1/64 | 3750 / BPM |

Convert to **samples** (ms × sr / 1000) and verify integer accuracy. BPM must be **verified to the sample** first (Gate 0). Which note value to use depends on the space in the phrasing: measure the gap lengths after line endings and choose a value whose first repeat lands inside the gap.

---

## Vocal high-pass
- **Measure:** the lowest sung fundamental of each vocal (pitch tracking over active frames, 5th percentile), plus plosive energy below about 120 Hz.
- **Derive:** set it a safe margin below the lowest fundamental (for example 15–25% below), so the chest of the lowest note survives. BG and adlib layers can go much higher (they don't need chest).
- **Sanity:** most leads land between 60 and 120 Hz. Deep voices can go lower. *Example: a voice whose lowest note was F2 (87 Hz) used 65 Hz.*
- **Verify:** the lowest note's fundamental is within about 1 dB of the unfiltered level; rumble and plosive energy are reduced.

## Resonances ("box", "honk", "ring")
- **Measure, the pitch-independent way:** for every voiced frame, detect f0, read the level of each harmonic k·f0, and plot all harmonics from all notes against frequency (a "harmonic envelope", tool: `deliveries/What_Im_Posed_To_Do/session/harmenv.py`). **A real resonance is a hump that every note passes through.** Plain long-term spectra and very narrow notches confuse melody (harmonics of the most-sung notes) with resonances.
- Also check that the hump **persists across sections** and in both takes.
- **Derive:** center = the measured hump peak; width (Q) = the measured hump width; depth = enough to bring the hump near its neighbourhood, **≤ 6 dB** (needing more means the cause is elsewhere: mic, room or an earlier process).
- **Never:** stack overlapping cuts across a region; cut into a natural dip next to the hump (it creates a hump-next-to-a-hole, which sounds boxy and hollow); use a fixed "box zone" from a chart. *Example: the chart said 180–380 Hz; the measured box was 440–520 Hz.*
- **Verify:** hump peak and mean reduced to the target; neighbouring dips not deepened; low-mid energy vs raw not thinner than intended.

## Dynamics (compression)
- **Measure:** the vocal's phrase-level spread (loud vs quiet phrases), crest factor while singing, and consonant punch and attack in 2–5 kHz (the **articulation baseline** from raw).
- **Derive:** the ratio and threshold that bring the phrase spread to the genre's consistency target, with an attack slow enough to keep consonants (verify!). Start with **one** stage. Add a fast peak stage only if peaks still measurably poke out; add parallel compression only for density the reference shows.
- **Sanity:** total average GR of a few dB per stage is typical. Large totals need justification.
- **Verify:** phrase spread reduced; **consonant punch within about 1 dB of raw and attack ≥ about 90% of raw**. If articulation drops, the vocal will sound dull. Back off attack or ratio before anything else.

## De-essing
- **Measure:** where this voice's sibilance lives (the band whose 99th-percentile spikes stand out), and how often it spikes.
- **Derive:** the detection band from that measurement; a threshold that triggers only on S/T/SH/CH; depth just enough to bring the spikes in line. Use one stage unless a later boost re-creates the problem. Then retune that stage rather than adding another.
- **Sanity:** typically active roughly 5–20% of singing time; much more means it's eating the voice.
- **Verify:** S-spike statistic reduced vs pre-de-ess; the voice is no harsher than raw; brightness not lost (no broadband cut above 6 kHz).

## Presence and air (tone)
- **Measure:** the vocal's brightness (for example 5–10 kHz vs 1–2 kHz) compared with the beat's top end, the reference and the raw take; and how dark the take was recorded.
- **Derive:** broad lifts sized to close the gap to the reference and to the "slightly at or above the beat's hi-hat brightness" idea. They can be bigger on a dark take, kept modest on a lossy source (it lifts artifacts).
- **Verify:** brightness at the target; harsh-flare statistic not above raw; sibilance re-checked after the boost.

## Lead-vs-beat pocket
- **Measure:** lead vs beat (a) in LU per section and (b) RMS in the 800 Hz–4 kHz band during active singing; the same deltas in the reference if one is available.
- **Derive:** match the reference's delta. Without a reference, start with the vocal clearly intelligible but *inside* the beat, then follow the artist's ears. *Example: Kenshin and ARMY preferred about 0 to +0.5 LU over the beat after the vocal was made clear.*
- **Dynamic pocket in the beat:** centre on where the beat's mid channel masks the vocal most (measure the overlap), with depth and speed chosen so the dip opens only while the vocal sings.
- **Verify:** the words come through in phone, earbud, car, club, laptop and mono simulations (1–4 kHz vocal-over-music margin); the artist's notes on level are respected.

## Reverb
- **Measure:** tempo, density (how much space between phrases), whether the vocals already have printed reverb, and the box zone of *this* voice.
- **Derive:** decay from a note value that clears before the next phrase; pre-delay from a synced value long enough that consonants land before the tail; a send high-pass above this voice's box zone and a low-pass below its sibilance; ducking depth that keeps the tail out of the words. Return level from the reference and the artist. If FX are printed, add far less (roughly 60–80% less).
- **Verify (clarity metric):** **dry-to-reverb ratio *while singing*** high (clear) and lower in gaps (space blooms). Check the reverb's low-mid share vs the dry voice: a box-heavy reverb sounds like a tunnel.

## Delays and throws
- **Measure:** line endings and gap lengths on the combined vocal bus; stressed-vowel P-centers of the throw words; dry vocal activity around each candidate repeat.
- **Derive:** the note value whose first repeat lands in the gap; feedback so tails clear before the next phrase; band-pass so repeats sit behind the voice; ducking depth so repeats only bloom in space.
- **Verify:** exact sample delay; no collisions; tails < −60 dBFS inside the padded buffer; throws land on measured line endings.

## Layers: doubles, BGs, adlibs
- **Measure:** whether the layers overlap or alternate with the lead; their pitch range and sibilance; their box-band share vs the lead.
- **Derive:** level under the lead by role (the reference and artist decide; hooks are usually louder than verses); higher high-pass and harder de-ess than the lead; symmetric pan for pairs; synthetic doublers within about 10–20 ms and 5–12 cents and mono-checked; a high-pass on a stack if it measures box-heavy.
- **Verify:** layer depth (dB under the lead) at the plan; vocal-bus correlation healthy; no added box.

## Low end and the 808
- **Measure:** 808 fundamental frequency and notes (key); kick/808 overlap; 808 harmonic content; phone-translation proxy (does a phone-band signal follow the 808's rhythm?).
- **Derive:** harmonic support (band-limited saturation blended under the 808) only as much as phones need without low-mid mud; kick/808 ducking if they collide; note-evening compression if notes jump.
- **Verify:** phone proxy improved; low-mid share not crowded; sub mono; the limiter isn't being driven mainly by the 808 (if it is, a sidechain high-pass on the glue, and careful sub control).

## Loudness and true peak (master)
- **Measure:** directly, the limiter's gain reduction on the loudest 1% of hits at candidate targets; short-term loudness of the hooks; references at matched loudness; the song's quiet-section share (it pulls integrated LUFS down).
- **Derive:** the loudest target with ≤ about 3–4 dB GR on the loudest hits that still sounds as punchy as the references when everything is played at −14 LUFS. If the beat is peaky or lossy, the answer may be quieter than the genre norm. That's correct; explain it.
- **Ceiling:** ≤ −1.0 dBTP; ≤ −2.0 dBTP when louder than −14 LUFS; < 0 dBTP after MP3/AAC.
- **Verify:** encode test; final integrated and true peak re-measured after DC block, automation and fades.

---

## Archetype tendencies (directions, not settings)

These describe how genres *tend* to differ. They help choose the **direction of a test**; the song and its reference choose the values.

| Archetype | Vocal tendency | Space tendency | Dynamics tendency | Loudness tendency* |
|---|---|---|---|---|
| Silky pop-R&B | Smooth, airy top, strict sibilance control | Lush pre-delayed plates, subtle hook widening, clean throws | Gentle peak control + smooth levelling | Commercial-loud if the beat allows |
| Melodic rap / pain-trap | Clear 3–5 kHz intelligibility, controlled sibilance, warmth | Moody plate/hall, wide band-passed ping-pong throws around adlibs | Firmer levelling, optional subtle saturation | Commercial-loud if the beat allows |
| Aggressive / upfront rap | Punchy chest and bite, body kept | Short rooms/slaps, little wash, dry-leaning throws | Fast peak control, optional parallel crush | Loud if the beat allows |
| Ballad / acoustic | Intimate, dynamic | Longer halls/plates | Light | Lower; dynamics matter more |

\*Always subject to the limiter-GR rule and matched-loudness comparison. *Example: "What I'm Posed To Do" landed at −14.4 LUFS integrated because its YouTube-rip beat was extremely peaky and the song has long quiet sections; louder versions crushed the drums.*

---

## Universal sanity checks for any derived value
- Is it **reversible and minimal** (the smallest move that fixes the measured problem)?
- Did it change **only** what you intended (re-measure the neighbours: frequencies, sections, other layers)?
- Is it **consistent with the artist's previous feedback** (see LEARNINGS)?
- Would a world-class engineer be able to explain why this exact value fits this exact song? If not, re-measure.
