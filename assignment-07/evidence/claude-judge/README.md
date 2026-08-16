# The tone judge — deterministic rubric vs Claude Opus 5

Every verdict in the `claude` column was produced by **claude-opus-5** reading the
rendered output of [`prompts/evaluator.md`](../../pipeline/prompts/evaluator.md)
verbatim, on 2026-08-16. They are replayed by the `session` backend so a
model-graded run stays reproducible offline.

| Slot | Copy | rubric | claude | Agreement |
|---|---|---:|---:|---|
| `loss_screen` | `Better luck next time. Crimson Vanguard still stands.` | 1.00 | 0.40 | **rubric misses it** |
| `clash_failure_recovery` | `The Clash broke. Shake it off and get back in there.` | 1.00 | 0.30 | **rubric misses it** |
| `meter_feedback_counter` | `Counter landed. Ascension rising.` | 1.00 | 1.00 | agree |
| `phase2_callout` | `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER` | 1.00 | 1.00 | agree |
| `impact_window_prompt` | `Well done! impact window - strike now!` | 0.20 | 0.00 | agree |
| `impact_window_prompt` | `WELL DONE IMPACT WINDOW - STRIKE NOW` | 0.50 | 0.40 | agree |
| `impact_window_prompt` | `IMPACT WINDOW - STRIKE NOW` | 1.00 | 1.00 | agree |

## The two the phrase list cannot reach

### `loss_screen` — 'Better luck next time. Crimson Vanguard still stands.'

- **rubric:** 1.00 — no banned phrase appears, no exclamation mark, no hedge.
- **claude:** 0.40 — Opens with 'Better luck next time', which consoles the player and attributes the outcome to luck; Pillar 1 makes deliberate decisions the thing that earns rewards, and the fiction frames this as a combat evaluation rather than a roll of the dice, so the consoling register is off-brand (T1).

### `clash_failure_recovery` — 'The Clash broke. Shake it off and get back in there.'

- **rubric:** 1.00 — no banned phrase appears, no exclamation mark, no hedge.
- **claude:** 0.30 — 'Shake it off and get back in there' is casual coaching in a cheerful sports-commentary register, which is warmer and chattier than the clipped declaratives the GDD's high-concept line establishes (T2 register, T1 in spirit).

This is the argument for the pluggable judge. `T1`'s phrase list catches copy
that says *"great job"*. It cannot catch copy that consoles, coaches, or
attributes the outcome to luck without ever using a listed word — and that copy
is just as off-brand for a game whose fiction frames the duel as an evaluation.

Both backends stay. The rubric is the default because committed evidence has to
be regenerable; the model is what you reach for when the phrase list runs out.
