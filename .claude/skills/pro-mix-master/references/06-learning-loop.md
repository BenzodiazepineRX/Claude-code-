# 06: Learning Loop & Memory (get better every song)

Agents don't remember between sessions unless the knowledge is **written into files they load**. In this repository the memory is:

| Memory | File | Loaded how |
|---|---|---|
| Core rules | `AGENTS.md` (imported by `CLAUDE.md` and `GEMINI.md`) | Auto-loaded by Claude Code / Gemini CLI / many agents in this repo |
| Full standard | `.claude/skills/pro-mix-master/` | Claude Code project skill; other agents read it by path |
| Lessons, artist profile, preferences, scores | `deliveries/LEARNINGS.md` | **Read at the start of every job; written at the end** |
| Per-song truth | `deliveries/<Song>/REPORT.md`, `session/` (scripts, settings, QC JSON) | Read when revising that song or a similar one |

Agents in chat apps without file access: paste `AGENTS.md` (and, if space allows, `02-decision-methods.md` and `03-qc-gate.md`) into the project or custom instructions, and paste the latest `LEARNINGS.md` at the start of a job.

## Before every song
1. Read `AGENTS.md`, this skill and `deliveries/LEARNINGS.md`.
2. Pull the **artist profile** (voice range, recurring resonances, mic/room notes, level/space preferences, how he describes sound). Treat it as **hypotheses to re-measure**, not settings.
3. If the genre, reference artists or techniques are new: research reputable sources (Sound On Sound "Inside Track", iZotope Learn, FabFilter Learn, Mix Online, Production Expert, The Pro Audio Files, Mastering The Mix, AES; platform specs from official pages such as Spotify for Artists). **Adopt a technique only if two reputable sources agree, or if an A/B test on this song shows a measurable improvement.**
4. Re-check platform loudness specs at least monthly and update `07-delivery-and-release.md`.

## During the song
- Log every decision with its measurement in `mix_config.json`.
- When the artist gives feedback: translate it with `05-artist-feedback-dictionary.md`, measure, fix, and **write the translation into LEARNINGS** (his words → what was actually wrong).

## After every song (and after every round of feedback)
Write into `deliveries/LEARNINGS.md`:
1. **What worked / what failed**, with numbers.
2. **The artist's exact words** and what they turned out to mean.
3. **Settings that suited this voice or mic**, marked as "re-measure next time".
4. **Process mistakes** (yours included) and the guardrail that prevents them. Add new guardrails to `04-dsp-guardrails.md` when they're general.
5. **Scores 1–10:** vocal clarity, balance, low end, effects, loudness & translation, emotion (artist-rated if possible). Aim the next song at the lowest score.
6. **Open questions** to ask next time (for example "send dry 24-bit stems and the beat's WAV").

## Improving the standard itself
- When a rule in this standard turns out wrong for a song, don't silently ignore it. Record the case in LEARNINGS, and if it generalizes, edit the rule (with a dated note on why).
- Never delete hard-won lessons; mark them superseded instead.
- Prefer measurements and checks over adjectives. If a lesson can become a QC check, make it one. The box-hump, dip and articulation checks were added after a vocal stayed boxy and dull through 15 versions.
