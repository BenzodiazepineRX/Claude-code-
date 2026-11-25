> **ARCHIVED SOURCE. Superseded by `.claude/skills/pro-mix-master/` (see `references/00-sources-and-changes.md`). Numbers below are NOT settings; derive every value from the current song.**

# Major-Label Pre-Release QC Audit Checklist ("Digital Forever" Gate)

Run this full audit **before delivering any final mix or master**. Once a track hits Spotify, Apple Music, and YouTube, it is permanent—if any gate fails, fix it with a surgical diff and re-verify before shipping.

---

## 1. Automated Technical Pass/Fail Gates

| Check | Pass Standard | Fail Action |
| :--- | :--- | :--- |
| **4x Oversampled True Peak** | `<= -0.5 dBTP` (ideally `-1.0` to `-0.5 dBTP`) | Lower limiter ceiling; never ship `>= 0.0 dBTP` |
| **Zero Digital Clipping** | `0` clipped samples (`>= 0.9999`) | Reduce limiter drive or pre-limiter transient spikes |
| **Integrated Loudness (LUFS)** | Within `±1.0 LU` of target (`-10.5 to -9.0 LUFS` for hip-hop/trap/R&B) | Adjust limiter input gain without pumping the beat |
| **Vocal-to-Beat Midrange Pocket** | Lead `800 Hz – 4 kHz` RMS within `-1.5` to `+1.5 dB` of beat midrange (or matched to reference) | Rebalance lead fader + beat dynamic Mid pocket |
| **Sub-Bass Mono Integrity** | Side-channel energy `< 90 Hz` is `> 20 dB` below Mid-channel | Tighten Side HPF at `90 Hz` |
| **Mono Phase Correlation** | Full-mix correlation `> +0.3` (and `> +0.6` `< 250 Hz`); lead vocal stays full in mono | Reduce stereo widener/Haas spread or fix phase |
| **DC Offset** | `< 0.001` | Apply DC removal / HPF at Gate 1 |
| **Tail & Fade Integrity** | Zero cut-off echo/reverb tails (`< -60 dBFS` decay verified); clean intro/outro fades | Pad tail buffer `3–5 s` and re-render |
| **Sample-Rate & Sync Lock** | All stems verified at identical sample rate; zero tempo drift across full song | Polyphase-resample mismatched stems and re-align |

---

## 2. Multi-System Translation Diagnostics (Car / Phone / Club / Streaming)

Verify how the master translates across real-world playback systems:
- **Phone Speakers (`200 Hz – 6 kHz` dominant):** Is the vocal clear without sounding piercing, and is the 808/bass line still audible via `80–220 Hz` upper harmonics?
- **Car Audio (Heavy Sub + Mid-Bass):** Is `40–100 Hz` tight and mono without drowning the vocal or making the limiter pump when the 808 hits?
- **Headphones / Earbuds (Wide Stereo Detail):** Are adlibs crisp (not boxy/muffled), are breaths natural, and are there zero edit clicks, pops, or harsh "s" spikes?
- **Streaming Normalization (Spotify `-14 LUFS`, Apple Music `-16 LUFS`, YouTube `-14 LUFS`):** Does `-1.0 to -0.5 dBTP` headroom prevent AAC/Ogg codec distortion when platforms turn the track down?

---

## 3. Mandatory Listen-Back Spot Check (At Least 3 Checkpoints)

Listen back to (1) **Intro & First Drop**, (2) **Verse-to-Hook Transition + Key Delay Throws**, and (3) **Outro**:
- [ ] **Pocket & Glue:** Vocal sits *inside* the beat like a commercial release—not pasted on top.
- [ ] **Delay Groove & Tails:** Every throw's stressed vowel hits on-grid, and every tail decays smoothly to silence.
- [ ] **Zero Collisions:** No wet echo collides with a dry adlib or smears the next vocal phrase.
- [ ] **Tone & Sibilance:** "S/t/ch" sounds are smooth without dulling vocal air; adlibs remain alive and clear.
- [ ] **Zero Artifacts / Unrequested FX:** No clicks, pops, pre-ringing, or unapproved synthetic sound effects.
- [ ] **Revision Regression Check (`v2+`):** Every previously approved stage matches its frozen `mix_config.json` state.

---

## 4. Honest Engineer's Sign-Off Report (Mandatory With Every Final Delivery)

Always include this concise readout with every final master:
1. **Verified Specs:** BPM, Integrated LUFS, 4x True Peak (dBTP), Mono Correlation, and Vocal-to-Beat midrange pocket delta.
2. **Exact Revision Diff (if `v2+`):** Exact parameter changes made—confirming all approved stages remained frozen.
3. **Artist Ear Checkpoints:** 1–2 specific timestamps or balance calls to audition on **headphones, car speakers, and a phone speaker** before distributor upload.
