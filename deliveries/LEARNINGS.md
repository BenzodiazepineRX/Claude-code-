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

## Scores (self-assessed from measurements; replace with the artist's feedback)
| Song | Vocal clarity | Balance | Low end | Effects | Loudness & translation | Emotion |
|---|---|---|---|---|---|---|
| Old Motorola v5 | 8 | 8 | 6 (lossy beat, no 808 stem) | 7 (printed FX limit control) | 8 | needs artist's ears |

**Next song, aim at the lowest score (low end):** get the beat's trackout stems so the kick and 808 can be balanced separately.

## Artist feedback
- (pending: add after Kenshin listens)
