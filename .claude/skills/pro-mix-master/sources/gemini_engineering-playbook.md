> **ARCHIVED SOURCE. Superseded by `.claude/skills/pro-mix-master/` (see `references/00-sources-and-changes.md`). Numbers below are NOT settings; derive every value from the current song.**

# Major-Label Mixing & Mastering Engineering Playbook

Comprehensive technical reference modeled on commercial R&B, Pop-R&B, Melodic Rap, and Atlanta Trap engineering standards. Calibrate every parameter to the raw stems and the artist's commercial reference track.

---

## 1. Vocal-to-Beat Pocket Calibration (The #1 Pro vs. Amateur Separator)

Amateur mixes sit vocals **on top** of the beat; major-label mixes lock vocals **inside** the beat.

- **Midrange Pocket Target:** Measure the beat's RMS in the vocal intelligibility band (`800 Hz – 4 kHz`) during active vocal sections. Seat the processed lead vocal within **-1.5 dB to +1.5 dB** of the beat's midrange (or matched to the reference's vocal-to-beat spectral delta)—NEVER `+4 to +6 dB` hotter on top.
- **Dynamic Beat Carving (Mid Channel Only):** Instead of turning the vocal fader up to fight a busy synth/guitar/piano beat, apply sidechain dynamic EQ to the beat's **Mid channel**:
  - Center frequency: `1.5 kHz – 3.2 kHz` (wide Q `0.8–1.2`)
  - Max dip: `1.0 – 2.5 dB` keyed to the lead vocal (`attack 5–10 ms`, `release 60–120 ms`).
  - Result: The beat hits full force in every pause and opens an invisible pocket the instant the artist sings/raps.
- **Printed-FX Stem Rule:** If vocal stems already have reverb, delay, or compression printed on them, reduce added reverb by **60–80%**, avoid heavy upward compression (which pulls up printed room noise), and limit serial compression to `1.5–3 dB` GR max.

---

## 2. Pre-Compression Prep: Clip-Gain Riding & Cleanup

Elite vocals sound effortless because dynamics are tamed *before* hitting the first compressor:
1. **DC Offset & Headroom:** Strip DC offset (`< 20 Hz` HPF) and gain-stage raw vocal peaks to `-12 to -6 dBFS`.
2. **Phrase-Level Vocal Rider:** Apply slow, transparent RMS envelope riding (`window 250–400 ms`, max `±3 dB` adjustment, smooth `80–150 ms` ramp) so quiet ends of phrases come up and shouted words come down before compression.
3. **Breath & Plosive Control:** Attenuate harsh plosives (`< 120 Hz` transient spikes) and overly loud gasps by `4–8 dB`—NEVER hard-gate breaths to dead digital silence (natural breaths preserve human emotion).
4. **Auto-Tune / Pitch Artifact Cleanup:** If stems have hard Auto-Tune printed, inspect `2.8–4.8 kHz` for narrow metallic resonant spikes and tame them dynamically (`-1.5 to -3 dB`, narrow Q `4–6`). If vocals need tuning, advise printing Auto-Tune/Melodyne/NewTone in FL Studio first before final mixing.

---

## 3. Genre & Vocal Archetype Matrix

Match processing style to the record's musical identity instead of using one generic chain:

| Archetype | High-Pass | Presence / Air Focus | Compression Style | Space & Width | Target Loudness |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Silky Pop-R&B (Chris Brown style)** | `85–100 Hz` | Smooth `2.5–3.5 kHz` control; silky high-shelf `+1.5 to +2.5 dB` at `12–16 kHz`; strict de-ess `6–8.5 kHz` | Gentle 1176 (`2–3 dB`) → smooth LA-2A (`3–4 dB`) + subtle parallel sheen | Lush pre-delayed bright plate (`30–45 ms` pre-delay), subtle micro-chorus/widener on hooks, clean ducked `1/4` or `1/8d` throws | `-10.0 to -9.0 LUFS` (`-1.0 dBTP`) |
| **Atlanta Pain-Trap / Melodic Rap** | `90–110 Hz` | Clean `200–350 Hz` mud notch; crisp `3–5 kHz` intelligibility; controlled `6–8 kHz` sibilance | Tighter 1176 (`3–5 dB`) → LA-2A (`2–3 dB`) + subtle tape/tube warmth | Moody hall/plate (`25–35 ms` pre-delay), wide bandpass ping-pong throws (`400 Hz – 4.5 kHz`) ducked cleanly around adlibs | `-10.5 to -9.0 LUFS` (`-0.5 to -1.0 dBTP`) |
| **Aggressive / Upfront Rap** | `80–95 Hz` | Punchy `1.5–3 kHz` chest/bite; keep `120–200 Hz` body intact; fast de-ess | Fast peak tamer (`4–6 dB`) + parallel vocal crush (`-12 to -15 dB` blend) | Tight room/short slap (`15–25 ms` pre-delay), minimal long reverb wash, punchy dry-leaning throws | `-9.5 to -8.5 LUFS` (`-0.5 to -1.0 dBTP`) |

---

## 4. Lead Vocal Surgical Processing Order

1. **Subtractive EQ (Fix Problems First):**
   - HPF `80–100 Hz` (`18 dB/oct`; `70 Hz` for deep baritones).
   - Boxy/mud zone `180–380 Hz`: narrow-to-medium cut (`-1.5 to -4 dB`, Q `1.8–3.0`) only where measured.
   - Nasal/honk zone `600–1,100 Hz`: `-1 to -2.5 dB` only if resonant.
   - Harsh bite `2.5–4.2 kHz`: dynamic attenuation rather than huge static cuts.
2. **Split-Band / Envelope De-Essing:**
   - Detect and attenuate `5.5–8.5 kHz` (`2–5 dB` GR on sharp "s/t/sh/ch" transients only).
   - **Anti-Lisp Rule:** Never broadband-cut above `6 kHz`; leave `10–16 kHz` open for vocal air.
3. **Two-Stage Serial Compression:**
   - *Stage 1 (Fast Peak Tamer):* `4:1`, attack `1–5 ms`, release `40–70 ms`, `2–4 dB` GR.
   - *Stage 2 (Smooth Leveler):* `2:1–3:1`, attack `10–20 ms`, release `100–180 ms`, `2–4 dB` GR.
   - *Optional Parallel Crush:* Heavy compression (`8:1–10:1`) + subtle saturation blended `-12 to -18 dB` under the lead.
4. **Harmonic Saturation & Air Sheen:**
   - Subtle even/odd harmonic warmth (low drive) to glue the vocal into the beat.
   - High-shelf air lift (`+1.0 to +2.5 dB` above `10–12 kHz`) *only after* de-essing is clean.

---

## 5. 3D Depth Staging, Adlibs & Vocal Stacks

Major-label records feel wide and 3D because every element occupies its own spatial lane:

- **Front Center (Dry & Anchored):** Lead vocal, kick, snare/clap, 808/sub-bass. Keep `100%` centered and phase-coherent.
- **Mid-Depth & Mid-Width (`±35% to ±70%`):**
  - **Adlibs:** High-pass `120–160 Hz`, keep `2–5 kHz` presence alive so they NEVER sound dull or boxy, seat `4–8 dB` under the lead unless featured in an open call-and-response gap.
  - **Hook Doubles & Harmonies:** High-pass higher (`140–180 Hz`), **de-ess harder (`-6 to -8 dB`)** than the lead so stacked "s" sounds don't splash across the stereo field, and pan symmetrically (`±50–80%`).
  - **Micro-Doubler / Chorus (Hooks Only):** Subtle L/R micro-pitch (`±6–9 cents`) or `12–22 ms` Haas spread mixed `-14 to -18 dB` underneath, checked in mono for zero hollowing.
- **Back & Wide Layer (`±75% to ±100%`):**
  - **Reverb Send:** Plate/hall with `25–45 ms` pre-delay, HPF `250–350 Hz`, LPF `6–8 kHz`, sidechain-ducked `-4 to -8 dB` under the dry lead.
  - **Delay Throws:** Bandpass-filtered (`400 Hz – 5 kHz`) ping-pong echoes so repeats sit *behind* the vocal without competing with lead vocal air.

---

## 6. Tempo-Synced Delay Math & P-Center Alignment

- **Exact Delay Times:** `1/4 = 60,000 / BPM ms` | `1/8 = 30,000 / BPM ms` | `1/8d = 45,000 / BPM ms` | `1/2 = 120,000 / BPM ms`.
- **Beat Grid Lock (`T0`):** Derive `T0` strictly from kick/snare transients (`< 250 Hz` and `1–3 kHz`), NEVER from `> 7 kHz` 16th-note/triplet hi-hats.
- **Vowel P-Center Alignment:** Words beginning with unstressed syllables or soft consonants (*"a-wake"*, *"a-way"*, *"stay"*) sound late if aligned by slice start. Detect the stressed vowel energy peak (`300–3,500 Hz`) and lock *that* P-center to `T0 + n * beat_sec`.
- **Collision Gating:** Before placing any repeat at time `t`, scan the dry adlib stem and next lead phrase in `[t - 0.15s, t + clip_len]`. Duck or omit any repeat that overlaps an active dry vocal.
- **Tail Padding:** Zero-pad every throw and reverb send by **3–5 seconds** so tails decay smoothly below `-60 dBFS` with zero abrupt cut-offs.

---

## 7. Low-End Translation & Stereo Bus Mastering

1. **808 / Phone-Speaker Translation Check:** Pure sub-bass (`35–60 Hz`) disappears on iPhone/laptop speakers. If the beat's 808 lacks upper harmonics, apply gentle parallel/band-limited saturation in `80–220 Hz` on the Mid channel so the bass line translates on small speakers without muddying the vocal.
2. **Sub-Bass Mono Centering:** High-pass the Side (`L - R`) channel at `90 Hz` (`18–24 dB/oct`). Never widen below `150 Hz`.
3. **Bus Glue Compression:** `1.5:1–2:1` ratio, slow attack (`20–30 ms` to let kicks/snares punch through), fast/auto release (`50–100 ms`), **max `1.0–2.0 dB` GR**.
4. **Reference-Matched Tonal Polish:** Broad gentle moves only (`±0.5 to ±1.5 dB`).
5. **4x-Oversampled Lookahead True-Peak Limiting:**
   - Integrated loudness matched to genre/reference (`-10.5 to -9.0 LUFS` for hip-hop/trap/R&B).
   - True Peak strictly capped at **-1.0 to -0.5 dBTP** so Spotify (`-14 LUFS`), Apple Music (`-16 LUFS` Sound Check), and YouTube (`-14 LUFS`) AAC/Ogg encoders never clip inter-sample peaks.
6. **Final Export:** `24-bit / 44.1 kHz WAV` distributor master + `320 kbps CBR MP3` audition copy.

---

## 8. Hybrid FL Studio Translation Blueprint

When boutique plugin tone outperforms raw Python DSP, provide exact **FL Studio Mixer Routing**:
- **Cleanup & Surgical EQ:** Fruity Parametric EQ 2 (exact measured Hz, dB, Q).
- **Vocal Dynamics:** Fruity Limiter (Comp tab) or Maximus (or Waves RVox/MV2, FabFilter Pro-C 2) with exact threshold/ratio/attack/release.
- **Dynamic Beat Pocket:** Sidechain Lead Vocal → Beat bus via Fruity Peak Controller or Trackspacer/Pro-Q (`1.5–3.2 kHz`, `1–2.5 dB` dip).
- **Ducked Delay Send:** Fruity Delay 3 (`100%` wet, `0%` dry, exact ms, bandpass `400 Hz – 5 kHz`) → Fruity Limiter sidechained from Lead Vocal.
- **Pre-Delayed Reverb Send:** Fruity Reeverb 2 (or Valhalla VintageVerb), pre-delay `30–45 ms`, low-cut `300 Hz`, high-cut `7 kHz`, sidechain-ducked under Lead Vocal.
- **Master Bus:** Patcher Mid/Side split (mono `< 90 Hz`), subtle bus glue, and Maximus/Pro-L 2 ceiling at `-0.5` to `-1.0 dBTP`.
