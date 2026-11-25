# 05: Artist Feedback Dictionary (words → measurements → fixes)

Artists describe sound in feelings and pictures. **Never guess a fix from a word.** Translate the word into measurements, find which cause the numbers support, fix *that*, and show an A/B. If a note could mean two different things, ask one short multiple-choice question before rebuilding.

Rules:
- **Re-measure from the raw** when the same complaint comes back twice. A repeated complaint usually means an earlier "fix" is the cause.
- **Prefer removing processing to adding more.**
- **Change only what was asked.** Keep everything approved frozen.
- Always answer with: what you measured, what you changed, the before/after numbers, an A/B clip and the timestamps to check.

| They say | Measure | Likely causes (confirm with numbers) | Typical fix direction |
|---|---|---|---|
| **"Boxy", "in a box", "closet"** | Harmonic envelope of the lead (resonance humps); dips next to humps; reverb's and layers' 250–800 Hz share vs the dry voice; doubler delay times | Untreated resonance; a hump left standing after broad cuts; a natural dip deepened; box-heavy reverb or doubles; a room recorded into the take (test reflections on breaths/S only) | One bell on the measured hump (≤ 6 dB); undo overlapping cuts; high-pass the reverb send and doubles above the box zone; doublers within 10–20 ms |
| **"Tunnel", "tube", "phasey", "hollow"** | Comb ripple on the vocal bus; doubler delays; mono correlation; deepened dips | Short delays of the same voice (10–30 ms) at a high level; scooped mids | Lower or retime the doublers, check mono; restore the mids you cut |
| **"Dull", "muffled", "not clear", "no life"** | Consonant punch and attack (2–5 kHz) vs raw; brightness vs beat/reference; de-esser activity %; number of compressors/limiters | Over-compression (fast attack), stacked de-essers, vocal peak limiter, a dark take, too much low-mid | Strip back to one compressor with a slower attack and one de-esser; presence/air lift sized by measurement; re-check articulation |
| **"Harsh", "piercing", "sharp S"** | 2–5 kHz flare statistic vs raw; S-spike statistic; resonance peaks 2.5–5 kHz | Over-boosted presence; untreated narrow resonance; sibilance lifted by an air shelf | Dynamic cut on the measured peak; retune the de-esser; reduce the boost |
| **"Too loud", "on top", "pasted on"** | Lead vs beat in LU and in the 800 Hz–4 kHz pocket per section | Vocal level; no dynamic pocket; the beat dropping out in breakdowns | Lower the lead (all vocal layers together keep their balance); add or tune the pocket; ride breakdown sections |
| **"Buried", "can't hear the words"** | Same as above + 1–4 kHz vocal-over-music margin in phone/earbud simulations | Masking in the beat's mids; a dull vocal | Pocket the beat; brighten the vocal; then level |
| **"Too much reverb", "washy", "far away"** | Dry-to-reverb ratio while singing; pre-delay; ducking; return level; decay vs gap length | Short pre-delay, weak ducking, decay longer than the gaps, return too high | Longer pre-delay, more ducking, shorter decay, lower return |
| **"Too dry", "no space"** | Dry-to-reverb ratio in gaps; throw coverage | Reverb ducked too hard; no throws in gaps | More bloom in gaps (less ducking or a higher return), throws on line endings |
| **"Off beat", "late", "rushing"** | Onsets vs the beat grid (T0 from kick/snare) per section; P-center of added elements | Added content placed by slice start, not P-center; a copy-pasted region offset; a natural push or lay-back (may be correct!) | Fix only added content or approved regions; report natural phrasing honestly |
| **"Cut in", "chopped", "clicky"** | Edit boundaries; fade lengths; region starts | Hard edits; teases/chops starting mid-word | 5–15 ms fades; start slices at phrase onsets; remove unrequested content |
| **"Empty", "gaps feel empty"** | Gap map (vocal-free bars); arrangement density | Long instrumental stretches | Offer options: throws/echo tails, approved BG layers, ghost echoes, swells. Ask before adding content |
| **"Missing background vocals"** | Which BG stems exist and where | Ambiguous: louder existing BGs vs new layers from the lead vs echoes | **Ask** (multiple choice), then build |
| **"Weak bass on my phone"** | 808 fundamental; harmonic content; phone proxy | A sine-only 808; limiter flattening the 808 | Harmonic support before clipping; a glue sidechain high-pass; honest source limit |
| **"Not loud enough"** | Integrated vs hooks' short-term; limiter GR; references at matched loudness | A quiet arrangement lowers integrated LUFS; peaky beat | Explain normalization; raise only within the limiter-GR rule; offer a louder alternate with the trade-off stated |
| **"Pumping", "breathing"** | Glue/limiter GR vs the 808/kick envelope | A bus compressor or limiter triggered by the sub | Sidechain high-pass on the glue; lower the target; tame the sub |

## How Kenshin describes sound (keep this updated in LEARNINGS)
- "Boxy / like inside a weird tunnel" → in his songs this was a resonance at 440–520 Hz left standing, plus a deepened 600 Hz dip and box-heavy reverb.
- "Dull" → squashed consonants (consonant punch fell from 12.4 to 9.8 dB) plus a dark raw take.
- "Too loud" → he and ARMY like the lead about 0 to +0.5 LU over the beat once it's clear.
- "Slight reverb" → audible but clear: reverb about 20 dB under the dry voice, dry-to-reverb ≥ about 24 dB while singing.
- "Fill the gaps" → wants echo throws and BG layers, but **not** unasked vocal teases (they felt off-beat and "cut in").
