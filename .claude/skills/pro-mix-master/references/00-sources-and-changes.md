# 00: Sources and What Changed

This standard merges three sources (originals archived in `../sources/`, all **superseded by this standard**):

1. **Kenshin's "Pro Mix & Master Agent: Full Instructions"** (Word doc, Nov 21 2026): professional bar, 7-pass QC × 3 clean rounds, honest reporting, learning loop, delivery set, platform table.
2. **The Gemini package** (Major-Label Engineering Playbook, Pre-Release QC Checklist, DSP Code Guardrails, and the combined "Agent Package"): gated workflow with artist stops, `mix_config.json` diff-only revisions, the vocal pocket concept, P-center throw alignment, collision gating, tail padding, a DAW mix sheet and a sign-off report.
3. **What two real songs taught us** ("Old Motorola" v1–v5, "What I'm Posed To Do" v1–v16; see `deliveries/LEARNINGS.md`).

## Kept from the Gemini package
Gates with preview stops; immutable config and diff-only revisions; frozen gate stems; vocal-inside-the-pocket; mid-channel dynamic beat pocket; P-center alignment; collision gating; 3–5 s tail padding; sosfilt and pre-ringing caution; global vs local index discipline; click-free fades; 4× true peak and BS.1770 loudness; cache-busting filenames; no unrequested sound effects; best tool for the job (DSP render vs DAW mix sheet); honest sign-off with listen-back checkpoints.

## Corrected or changed (and why)
| Gemini said | This standard says | Why |
|---|---|---|
| Fixed numbers for HPF, EQ zones, compressor ratios/attacks, de-ess bands, reverb, loudness | **Starting ranges only; every value derived from the song's measurements and logged with its reason** | Every song is different. The fixed "box zone 180–380 Hz" missed this song's real box at 440–520 Hz |
| "Always listen back" | **Agents cannot hear.** Measured checks + loudness-matched A/B + artist listen-back at timestamps | Claiming to listen is dishonest |
| True peak ≤ −0.5 (−1.0 to −0.5) dBTP | **≤ −1.0 dBTP; ≤ −2.0 dBTP when louder than −14 LUFS; < 0 after encode** | Kenshin's standard and Spotify for Artists guidance; inter-sample safety after encoding |
| Target −10.5 to −9.0 LUFS | **Loudness chosen per song by the limiter-GR rule (≤ 3–4 dB on the loudest hits) and matched-loudness reference comparison** | "Never let the limiter do the mixing." A peaky YouTube-rip beat with long quiet sections correctly landed near −14 |
| Two-stage serial compression as the default | **Start with one stage sized to this vocal; add stages only if measured; verify articulation** | Stacked fast compression, a vocal limiter and three de-essers made the vocal dull (consonant punch 12.4 → 9.8 dB) |
| Notch boxy low-mids "180–380 Hz" | **Find resonances with the pitch-independent harmonic envelope; one bell where measured; never deepen natural dips** | A hump left next to a deepened dip = boxy/hollow for 15 versions |
| Pocket "±1.5 dB of beat midrange" as a universal pass | **Pocket target set per song** (reference delta or artist preference), guarded by intelligibility checks | References and artists differ; Kenshin preferred about 0 to +0.5 LU |
| Micro-doubler 12–22 ms | **10–20 ms / 5–12 cents, mono-checked, box-band checked** | Doubles at 21/29 ms were heard as a "tunnel" |

## Added (not in either source)
- Articulation QC (consonant punch and attack vs raw), resonance-hump and dip checks, reverb-clarity metric (dry-to-reverb while singing).
- Metric sanity tests with known-answer signals; QC must read the real mix gains; no hidden FAIL summaries.
- Timing judged against the beat grid (not section vs section); sample-exact BPM verification; copy-paste region detection.
- Latency compensation for lookahead processes; DC handling around limiters; performance and memory rules.
- Artist feedback dictionary; artist profile; learning loop with scores; research-adoption rule.
- Release extras: beat-license flag, clean-edit process, alternates through an identical chain with null test.
