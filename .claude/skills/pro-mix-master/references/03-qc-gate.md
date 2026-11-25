# 03: QC Gate ("Digital Forever")

Once a song is on Spotify, Apple Music and YouTube it is permanent. **Nothing ships until this gate passes three full rounds in a row:** round 1 on the 24-bit WAV, round 2 on the 16-bit WAV, round 3 on the decoded 320 kbps MP3. Any fix sends you back through every check it could affect, then three fresh rounds.

Thresholds marked **(song)** are set per song in `mix_config.json`, from the reference, the genre and the artist's documented preferences, and are written into the QC script *before* the results are seen. Changing a threshold after a failure requires a written reason (for example, "artist asked for a lower vocal") in the report. Moving a threshold just to turn a FAIL into a PASS is forbidden.

---

## 0. Before trusting any metric
- **Sanity-test every new measurement on a signal with a known answer** (for example, noise plus a known 3 ms echo must be detected, and plain noise must read near zero). Several metrics in this project were wrong until tested this way.
- QC scripts must read the **actual gains and files used in the mix**, never stale constants.
- The summary count must be computed from the same pass/fail values that are printed. Watch boolean-type pitfalls; a printed FAIL must never be summarized as "0 failed".

---

## Pass 1: Technical
| Check | Pass |
|---|---|
| No digital clipping | 0 samples ≥ 0.999; 0 runs of ≥ 3 full-scale samples |
| DC offset | < 1e-4 (and < 0.001 absolute) |
| Format | Correct sample rate, bit depth and channels; all versions sample-aligned and equal length |
| Clean start/end | No dead air at the start; tails fade below −60 dBFS; no cut-off echoes or reverbs |
| Clicks/glitches | No more transient spikes in the master than in the unmastered mix and raw stem sum (like-for-like) |

## Pass 2: Timing
| Check | Pass |
|---|---|
| Tempo verified | Long self-match of the beat shows ≤ 2 samples of drift |
| Delay math | Every delay, throw and pre-delay equals the BPM formula to the sample |
| Throws placed | Every throw sits on a measured line ending and its first repeat lands in a gap |
| No collisions | No wet repeat overlaps an active dry vocal (beyond ducked bleed) |
| No processing shift | Beat and vocal transients (1–6 kHz band) not shifted by processing (≤ 2 samples). Lookahead processes are latency-compensated |
| Creative edits | Anything added (fills, swells) shifted by whole bars on the verified grid, and **approved by the artist** |
| Performance | Vocal timing left as performed unless the artist approved a change (offset vs the beat grid documented) |

## Pass 3: Balance & space
| Check | Pass |
|---|---|
| Lead vs beat (LU per section) | Within the **(song)** range |
| Vocal pocket (800 Hz–4 kHz) | Lead vs beat midrange RMS within the **(song)** range (reference-matched when available) |
| Layer order | Lead > BGs > BG-of-BG; adlibs present but secondary; measured dB under the lead within the **(song)** ranges |
| Hook lift | Hook louder than verse by the **(song)** target (unless intentionally flat) |
| Phrase consistency | Short-term loudness spread within a section ≤ the **(song)** target |
| Reverb clarity | Dry-to-reverb ratio **while singing** ≥ the **(song)** target; reverb level within the **(song)** range |
| Echo BGs / throws | Audible in gaps at the planned depth; collision-free |
| Unrequested content | None. Every creative element is on the approved list |

## Pass 4: Tone
| Check | Pass |
|---|---|
| **Resonances** | Measured resonance hump(s) reduced to the **(song)** target (harmonic-envelope method) |
| **No hollowing** | Natural dips not deepened; no hump-next-to-hole |
| **Articulation** | Consonant punch (2–5 kHz) within ±1 dB of raw; attack ≥ 90% of raw |
| Harshness | 2–5 kHz flare statistic ≤ raw + 1 dB |
| Sibilance | S-spike statistic controlled vs raw; de-esser active only on S moments |
| Brightness | Vocal brightness at the **(song)** target vs beat/reference |
| Mud / boom | Low-mid vs mid share within the **(song)** limit; sub share sane |

## Pass 5: Translation (simulations; label them as simulations)
| System | Pass |
|---|---|
| Phone (mono, ~300 Hz–7 kHz) | Words clear (vocal-over-music margin in 1–4 kHz ≥ the **(song)** target); 808 rhythm audible via harmonics (proxy improved vs the original beat) |
| Earbuds, laptop, car (bass bump), club (sub boost) | Words clear in 1–4 kHz; low end not swamping the vocal |
| Mono fold | Loss ≤ 1 dB; full-mix correlation ≥ +0.3 (≥ +0.6 below 250 Hz); lead solid |
| Sub mono | Side energy below ~90 Hz at least 20 dB under mid |
| Very low volume (equal-loudness simulation) | Lead still above the music |

## Pass 6: Master spec
| Check | Pass |
|---|---|
| Integrated loudness | Within ±0.5 LU of the **(song)** target |
| True peak (4× oversampled) | ≤ −1.0 dBTP; ≤ −2.0 dBTP when louder than −14 LUFS |
| Encodes | MP3 320 and AAC 256 < 0 dBTP |
| Limiter load | ≤ 3–4 dB GR on the loudest 1% of hits (measured directly) |
| Short-term loudness | Reviewed; hooks vs references at matched loudness |
| Alternates | Null test of the main vs the fixed alternate chain shows a negligible residual (for example < −80 dBFS RMS) |

## Pass 7: Fresh full review
Re-analyze the final render from scratch as if someone else mixed it: no new warnings; lead-only, music-only and whole-song measurements consistent; **regression check** (every previously approved stage matches its frozen `mix_config.json` state).

---

## Artist listen-back checkpoints (mandatory: agents can't hear)
Give the artist at least three specific spots to check on **headphones, car speakers and a phone speaker**:
1. The intro and first vocal entry or drop.
2. A verse-to-hook transition with a key delay throw.
3. The outro and final tail.
Plus any spot that changed in this revision. Provide **loudness-matched A/B clips** (raw vs master; previous vs new; vocal-only when the vocal changed).

---

## Source limits
If a check still fails after about five genuine fix attempts **because of the source** (a lossy beat, a sine-only 808, a clipped take), stop looping. Deliver the best version, keep the check marked **FAIL (source-limited)** with the attempts listed, and state exactly what would fix it (for example "buy the beat's WAV/trackouts"). Never call that master "perfect" or "radio-ready". Say "meets streaming specs; one source-limited item" instead.

---

## Honest engineer's sign-off (with every delivery)
Use `templates/sign_off_report.template.md`. Minimum contents:
1. **Verified specs:** BPM (verified), key, integrated LUFS, max short-term, 4× true peak, MP3/AAC true peak, limiter GR on the loudest hits, mono correlation, lead-vs-beat pocket delta, hook lift.
2. **QC results:** each round's pass/fail count and every FAIL, with its explanation.
3. **Exact revision diff** (v2+): every parameter changed (before → after), and confirmation that everything else stayed frozen.
4. **Honest limits and your own mistakes.**
5. **Artist ear checkpoints** (timestamps; headphones/car/phone) and the A/B files.
6. Status: **"draft, not final"** until the artist approves.
