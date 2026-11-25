# 07: Delivery & Release

## Deliverables (every song)
| File | Format | Use |
|---|---|---|
| Main master | WAV 24-bit, 44.1 kHz (or the session rate) | Distributor upload, hi-res stores |
| 16-bit master | WAV 16-bit, TPDF-dithered (once, last) | Stores/CDs that require 16-bit |
| MP3 | 320 kbps CBR from the 24-bit master; true peak < 0 dBTP after encoding | Sharing, quick listening |
| Clean / radio edit | Same spec as the main | Radio, clean playlists. Needs the artist's list of words to clean (timestamps); mute, reverse or replace on the beat; check BGs and adlibs too |
| Instrumental | Same chain as the main | Performances, sync |
| Acapella | Same chain as the main | Remixes |
| TV track | Beat + background layers, no lead | Live/TV |
| Alternates the artist asked for | Same chain | For example a "no fills" version |
| Unmastered mix | WAV 24-bit, peaks around −6 to −3 dBFS | Future remasters |
| Stems (optional) | WAV 24-bit, all starting at 0:00, same length | Live shows, remixes |
| A/B clips | MP3, loudness-matched | Artist listening |
| Picture | PNG song map, waveforms, spectrograms | Visual check |
| Report | `REPORT.md` (sign-off) | Record |

**All alternates go through the exact same bus and master settings** as the main (fixed gains, glue threshold, limiter gain and ceiling). Prove it with a null test of the main re-rendered through that chain.

## Naming and archiving
- `Song_Name_Master_v12_24b-44k.wav`, `Song_Name_Instrumental_v12_24b-44k.wav`, `Song_Name_AB_<what>_vA_vs_vB.mp3`.
- Current deliverables live in `deliveries/<Song_Name>/`. Older versions move to a versions folder (never silently deleted). Settings, scripts and QC JSON go in `session/`.
- Commit and push deliverables. Note large-file limits (keep each file under about 50 MB where possible).

## Platform loudness facts (as recorded Nov 2026; re-verify monthly from official sources)
| Platform | Normalizes to | Notes |
|---|---|---|
| Spotify | −14 LUFS | Asks for true peak below −1 dBTP, or below −2 dBTP if the master is louder than −14 LUFS (Spotify for Artists) |
| YouTube | about −14 LUFS | Turns down only |
| TIDAL | about −14 LUFS | Normalization on by default in mobile apps |
| Amazon Music | about −14 LUFS | Users can disable normalization |
| Deezer | about −15 LUFS | Users can disable normalization |
| Apple Music | −16 LUFS (Sound Check) | Mostly turns down |

Consequence: masters crushed far above −14 LUFS get turned down and sound smaller. Choose loudness for punch at matched loudness, within the limiter-GR rule.

## Release-readiness extras (ask the artist; agents don't invent metadata)
- Final title spelling, artist/feature credits, explicit/clean flag, ISRC (from the distributor), songwriter/producer credits, **beat license** (a "FREE … type beat" usually requires a lease or credit before commercial release; flag it), cover-art match.
- Radio edits typically run about 3:00–3:45 with a short intro. Confirm with whoever pitches the song.
- FM radio boosts highs and many radios play in mono, so sibilance control and mono compatibility are required.

## DAW mix sheet (hybrid route)
When plugin character or real tuning matters, also deliver a sheet the artist can rebuild in FL Studio, BandLab or any DAW. For each track: insert order, plugin (stock option + pro option), and **the exact values derived for this song** (Hz, dB, Q, threshold, ratio, attack, release, de-ess band, send levels, pre-delay/decay in ms, delay ms, pan %), plus the sidechain routing (vocal → beat pocket, vocal → delay and reverb ducking), bus settings and the limiter ceiling. Never fill the sheet with generic numbers.

## What to send the artist
1. A/B clips first (matched loudness), then the full song MP3, then the picture.
2. A short, plain-language summary: what changed, before → after numbers, honest limits, 2–3 timestamps to check on headphones, car and phone.
3. Where the full files are (with a simple how-to if needed).
4. An invitation for specific feedback: "timestamp + what you hear".
