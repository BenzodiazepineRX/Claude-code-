# Pro Mix & Master Standard: Core Rules for Every Agent

> **Every agent (Claude, Gemini, ChatGPT, Cursor, Copilot or any other) working in this repository MUST read and follow this file before touching audio.**
> The full standard lives in [`.claude/skills/pro-mix-master/`](.claude/skills/pro-mix-master/SKILL.md). Read `SKILL.md` and its `references/` before any mix or master.
> Then read the lessons notebook [`deliveries/LEARNINGS.md`](deliveries/LEARNINGS.md), and add to it after every song.

The goal is **radio-ready, stream-ready, major-label-quality mixes and masters, every song, every time.** "Good enough", "pretty close" and "fine for a demo" never count as finished.

## Owner corrections (2026-11-25; these override anything older)

- **Echoes: there is no default.** Echoes are different on every song. Before applying any echo, ask Kenshin how he wants them on this song (which words, timing, repeats, levels, tone). The old "last word only" rule is wrong and must not be used.
- **Reference track: picked per song.** "Top8 (Extended Network)" is not a default reference. Ask Kenshin which reference(s) to use for each song.
- **No fixed numbers carry over.** Old fixed loudness ranges and fixed vocal/adlib levels are superseded; loudness and levels come from this song's measurements, its reference and Kenshin's ears.
- **Push every version as soon as it is rendered.** Each version's notes, `mix_config.json` and QC results go to `main` right away, not when the song is done. Agent computers get refreshed and unpushed work is lost. Pull `main` before editing shared files.

---

## Rule 0: Every song is a new project

**There are no presets in this standard.** Every number written anywhere in these documents is a *starting range* or a *sanity bound*, never a setting to copy.

- Every value you use on a song (high-pass frequency, EQ cut, compressor threshold, de-esser range, reverb size, delay level, loudness target and the rest) **MUST be derived from that song's own measurements, its reference track and the artist's intent.**
- Log each value with **the measurement that justified it**, in that song's `mix_config.json`.
- A previous song's settings, even from the same artist, are only a **hypothesis to re-measure**. Mics, rooms, takes, keys and beats change.
- If you cannot say *why* a value is what it is, for *this* song, you are not allowed to use it.

> Example: on "What I'm Posed To Do" the generic "box zone 180–380 Hz" rule pointed at the wrong place. Measurement found the real box resonance at **480 Hz**. Three versions were lost to cutting where a rule said instead of where the song said.

---

## Non-negotiable rules

1. **Measure first, then decide, then verify.** Analyze before touching anything (Gate 0), and write a mix plan. After every process, measure that it did what you intended, and nothing else.
2. **Work in gates. Never one-shot a mix and master.** Gate 0 Intake & forensics → Gate 1 Vocal cleanup, tone & pocket → Gate 2 Space, delays & throws → Gate 3 Balance, automation & mix bus → Gate 4 Master → Gate 5 QC & delivery. Show the artist a short preview at each gate when they are available.
3. **One measured fault, one precise move.** Fix exactly what measurement finds, exactly where it is. Never stack overlapping cuts, compressors or de-essers "to be safe". Stacked fixes made vocals boxy *and* dull here for 15 versions.
4. **The vocal sits *inside* the beat, not pasted on top.** The level comes from the reference and the artist's ears, never from a fixed number.
5. **Protect the performance.** Keep originals untouched and work on copies. Never move, delete, replace or tune a performance, and never add creative content (vocal chops, teases, risers, sound effects), without asking first. Offer creative ideas as a separate alternate version.
6. **Every time-based effect is computed from the verified BPM** (exact ms and samples). Pad every delay and reverb tail 3–5 s so it decays below −60 dBFS. Duck or skip any echo that would collide with a dry vocal.
7. **Never let the limiter do the mixing.** The loudness target is chosen per song: the loudest it can be with ≤ 3–4 dB of limiting on the loudest hits, compared against references at matched loudness. True peak: ≤ −1.0 dBTP, or ≤ −2.0 dBTP when louder than −14 LUFS. It must stay under 0 dBTP after MP3/AAC encoding.
8. **Revisions are diff-only.** Change only what was asked, log the before/after diff, and keep approved stages frozen. Version every render (`_v1`, `_v2` and so on) and never overwrite.
9. **Nothing ships until the QC gate passes three full rounds in a row.** Run it on the 24-bit WAV, the 16-bit WAV and the decoded MP3. A check that fails because of the source is reported as FAIL with an explanation, never hidden or relabelled.
10. **Agents cannot hear.** Never claim to have listened. Report measurements, provide loudness-matched A/B clips, and give the artist specific timestamps to check on headphones, car and phone. **The artist's ears are the final judge.** Until the artist approves, everything is labelled "draft, not final".
11. **Tell the truth.** Report what you fixed, what the source limits, what you are unsure of, and your own mistakes. Never say "perfect" or "radio-ready" if any check failed.
12. **Get better every song.** Read `deliveries/LEARNINGS.md` before starting. After each song, and after every piece of artist feedback, write the lessons down: what worked, what failed, and how the artist describes sound.

---

## The artist's words → what to measure (short version)

| Artist says | Measure first | Usual real cause (verify!) |
|---|---|---|
| "Boxy", "in a box", "tunnel" | Pitch-independent harmonic envelope of the lead (find the resonance); reverb's low-mid share; doubler delays; natural dips you may have deepened | An untreated resonance, or a hump left standing next to a dip you carved; reverb with too much 250–600 Hz; doubles at 10–30 ms |
| "Dull", "not clear" | Consonant punch and attack (2–5 kHz) vs raw; brightness vs beat | Over-compression, stacked de-essers or peak limiters squashing consonants; a dark take that needs a presence lift |
| "Too loud", "on top" | Lead vs beat in the 800 Hz–4 kHz pocket and in LU, per section | The vocal level; no dynamic pocket in the beat |
| "Too much reverb" | Dry-to-reverb ratio *while singing*, pre-delay, ducking | Short pre-delay, weak ducking, return too loud |
| "Off beat", "cut in" | Onsets vs the beat grid (kick/snare T0); edit and fade boundaries | Added content not on grid; hard edits |

Full dictionary: `.claude/skills/pro-mix-master/references/05-artist-feedback-dictionary.md`.

---

## Where things are

| What | Path |
|---|---|
| Full standard (workflow skill) | `.claude/skills/pro-mix-master/SKILL.md` |
| Gate-by-gate workflow | `.claude/skills/pro-mix-master/references/01-gates-workflow.md` |
| How to derive every setting per song | `.claude/skills/pro-mix-master/references/02-decision-methods.md` |
| QC gate (pass/fail + sign-off) | `.claude/skills/pro-mix-master/references/03-qc-gate.md` |
| DSP / coding guardrails | `.claude/skills/pro-mix-master/references/04-dsp-guardrails.md` |
| Artist feedback dictionary | `.claude/skills/pro-mix-master/references/05-artist-feedback-dictionary.md` |
| Learning loop & memory | `.claude/skills/pro-mix-master/references/06-learning-loop.md` |
| Delivery & release | `.claude/skills/pro-mix-master/references/07-delivery-and-release.md` |
| Templates (`mix_config.json`, mix plan, sign-off report) | `.claude/skills/pro-mix-master/templates/` |
| Lessons notebook (read first, add after) | `deliveries/LEARNINGS.md` |
| Past songs: masters, reports, scripts, QC results | `deliveries/<Song>/` |
