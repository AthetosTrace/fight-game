# Assignment 07 — A Style Guide Agent for *Ascendant Impact*

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy
martial-arts action fighter. Unreal Engine 5.8, PC, Blueprint-only. The player
picks Agent Echo or Agent Nova and fights **Crimson Vanguard / Project Valor-7**
in the **Shattered Ring**.
**Author:** AthetosTrace · **Repo:** `AthetosTrace/fight-game`

**Content type governed:** **player-facing combat copy** — the words the player
reads during the duel. Impact Window prompts, Ascension Meter feedback, the
Phase 2 callout, the Final Clash unlock, the failed-Clash recovery line, and the
loss screen.

Nothing in Assignments #04–#06 produced a single line of it. #04 made telegraph
packs and cue sheets, #05 the arena, #06 the attack table. Nobody had written
what the player reads, and the game ships 1 September.

---

## Pre-Build Declaration

Committed on its own, before any pipeline code — see
[`PRE-BUILD-DECLARATION.md`](PRE-BUILD-DECLARATION.md) and commit `6ad3763`.

---

## Run it

```bash
python -m pip install pytest

# the whole loop — generate, score, refine, stop
python assignment-07/pipeline/orchestrator.py --slot clash_failure_recovery --seed 69

# score one line by hand
python assignment-07/pipeline/evaluator.py meter_feedback_counter "Nice work! Ascension fills over time."

# 1200 runs, checking which stop reasons are reachable and which invariants hold
python assignment-07/pipeline/sweep.py --seeds 200

# 134 tests, no engine, no network, no API key
# -> 132 passed, 2 skipped (the two that exercise the Anthropic SDK bindings)
python -m pytest assignment-07/pipeline/tests -q
```

```
assignment-07/
├── PRE-BUILD-DECLARATION.md        committed before any code
├── STYLE-GUIDE.md                  the style guide, human-readable
├── pipeline/
│   ├── contracts/style_rules.json  the same guide as data — every rule cites a GDD section and page
│   ├── prompts/evaluator.md        the evaluator's prompt (a submitted deliverable)
│   ├── prompts/refiner.md          the refiner's prompt (a submitted deliverable)
│   ├── retrieval.py                resolves every citation against gdd/sections/ and verifies it
│   ├── generator.py                writes a canon-faithful line, then drifts it under a seed
│   ├── judge.py                    the tone judge — `rubric` (offline) or `claude` (Opus 5)
│   ├── evaluator.py                SCORE + REASON, three weighted criteria
│   ├── refiner.py                  smallest rewrite that clears one fault, or a refusal
│   ├── orchestrator.py             the loop and the circuit breaker
│   ├── sweep.py                    reachability and invariant sweep
│   └── tests/                      134 tests
└── evidence/runs/                  six committed runs + the sweep
```

---

## The loop

```
attempt 1..3:
    generate (first attempt) or take the refined line
    evaluate   -> SCORE: [X/10] + REASON
    at or above 9.6 -> SUCCESS
    otherwise       -> refine the first fault, retry
```

| Stop reason | Meaning | Exit |
|---|---|---|
| `SUCCESS` | Scored at or above the threshold | 0 |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | Three attempts used, faults remain | 1 |
| `HUMAN_REVIEW_REFINER_REFUSED` | A decision that belongs to the designer | 2 |
| `CIRCUIT_BREAKER_NO_PROGRESS` | Same failure signature twice running | 1 |

Two details carried over from Assignment 06 because they earned their keep.
**No-progress is measured on the failure detail, not the rule id** — a line that
breaks `V1` twice with one generic noun fixed is still `V1`, and that is
progress. **The refiner only runs when an attempt remains to verify it** —
applying a rewrite on the final attempt would end the log on an unverified claim.

### Why the generator deliberately writes bad copy

A generator that always emitted clean copy would make the evaluator ceremonial.
`generator.py` builds the line the GDD supports, then applies **seeded drift** —
eleven operators covering the ways this copy actually goes wrong: congratulating
the player because UI copy usually does, reaching for "ultimate" because that is
the genre word, assuming a meter charges because meters usually do, assuming
failure means starting over because it usually does. Drift is seeded, so every
defect is reproducible and traceable. **The evaluator never sees which operators
fired** — there is a test for that.

---

## How this differs from Assignment 06 — and where it deliberately doesn't

The two pipelines share a shape, and that is the point: #04 built retrieval, #05
built the loop, #06 hardened it, and this one points it at prose. `orchestrator.py`,
the circuit breaker, the no-progress fingerprint, and the negation-aware matcher
in `textcheck.py` are adapted from `assignment-06/`, each crediting its source in
a docstring — the same way #06's `retrieval.py` credits `assignment-04`.

**What is genuinely different is the verdict.**

Assignment 06 ran two layers: a deterministic `gate()` that asked *is this row
legal?* and a scored rubric that asked *is this a good row?*. A row had to clear
the gate **and** pass every criterion. That is a binary verdict, and this brief
forbids one.

So there is no gate here. **The score is the verdict.** Three criteria are
weighted and mapped onto the 1–10 scale, and nothing can veto a passing score or
rescue a failing one:

| Criterion | Weight | Asks | Backend |
|---|---:|---|---|
| `tone` | 35 | Is this the register the GDD set? | judge (`rubric` or `claude`) |
| `vocabulary_lore` | 40 | Does it use this game's words, and are its facts true? | deterministic |
| `format_length` | 25 | Will it read on a HUD mid-fight? | deterministic |

The score carries real information about severity rather than acting as a
disguised boolean — a lore break lands at **4.8**, a stray word at **9.55**:

| Fault | Score |
|---|---:|
| Three stacked lore violations | 4.8 |
| A generic noun plus a missing subject | 5.7 |
| Over-length and wrong shape | 8.2 |
| One word over the banner limit | 9.55 |
| Clean | 10.0 |

### The tone judge is pluggable, and both backends are real

Tone is the only criterion that is genuinely a judgment call. Vocabulary and
lore are lookups; length and shape are arithmetic.

- **`rubric`** (default) — deterministic, offline, no key. Scores the markers
  Pillar 1 and the GDD's register forbid.
- **`claude`** — sends [`prompts/evaluator.md`](pipeline/prompts/evaluator.md) to
  **Claude Opus 5** and reads back a structured verdict.

`rubric` is the default because **committed evidence has to be regenerable by
anyone who clones this repo** — a run report nobody can reproduce is not
evidence. To run the model-backed judge:

```bash
python -m pip install anthropic     # then set ANTHROPIC_API_KEY
python assignment-07/pipeline/orchestrator.py --slot loss_screen --seed 12 --judge claude
```

Both prompts are submitted deliverables in their own right — the assignment asks
for the evaluator's and refiner's prompts, not only their output.

---

## Before / after — three violation classes

### Example 1 — Tone

[`evidence/runs/impact-window-prompt-seed33/`](evidence/runs/impact-window-prompt-seed33/run.md)

| | |
|---|---|
| **Before** | `Well done! impact window - strike now!` |
| **Evaluator** | `SCORE: [5.7/10]` — congratulates the player, uses an exclamation mark, wrong shape, over limit |
| **After** | `IMPACT WINDOW - STRIKE NOW` — **10.0** |

Three attempts: the exclamation mark went first (`T2`), then the praise (`T1`),
then the shape resolved. Score climbed 5.7 → 7.3 → 10.0.

### Example 2 — Vocabulary and lore

[`evidence/runs/phase2-callout-seed40/`](evidence/runs/phase2-callout-seed40/run.md)

| | |
|---|---|
| **Before** | `it - boss fight presses harder.` |
| **Evaluator** | `SCORE: [5.7/10]` — uses the generic `'boss fight'` where this game says `'Crimson Vanguard'`; never names Phase 2 or Crimson Vanguard |
| **After** | `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER` — **10.0** |

A stranger could not tell what game the "before" line belongs to. That is exactly
the failure the brief scores zero for, caught and corrected.

### Example 3 — Formatting and length

[`evidence/runs/meter-feedback-counter-seed119/`](evidence/runs/meter-feedback-counter-seed119/run.md)

| | |
|---|---|
| **Before** | `COUNTER LANDED. ASCENSION RISING. READ THE TELEGRAPH, COMMIT TO THE COUNTER, AND KEEP THE PRESSURE ON CRIMSON VANGUARD THROUGH THE WHOLE EXCHANGE` |
| **Evaluator** | `SCORE: [8.2/10]` — 143 characters against a 40-character limit; shouted prose is neither shape |
| **After** | `Counter landed. Ascension rising.` — **10.0** |

### Example 4 (bonus) — Lore, the class the brief does not require

[`evidence/runs/clash-failure-recovery-seed69/`](evidence/runs/clash-failure-recovery-seed69/run.md)

| | |
|---|---|
| **Before** | `The Clash broke. Return to neutral and rebuild Ascension. Start over from the beginning (25%). Wait for your meter to charge.` |
| **Evaluator** | `SCORE: [4.8/10]` — three separate contradictions of GDD §03 |
| **After** | `The Clash broke. Return to neutral and rebuild Ascension.` — **10.0** |

This is the run worth reading. The copy is grammatical, on-register, and would
pass any generic style checker — and it teaches the player **three rules this
game does not have**: that the meter charges while you wait (§03 p3 denies it),
that a failed Clash restarts the duel (§03 p4 denies it), and that the 25%
threshold is a shipped promise (§03 p3 marks it provisional). Each was removed
with a citation to the line that denies it.

---

## Did the pipeline catch something I would have missed?

**Yes — twice, and both times it caught me rather than the copy.**

**1. The style guide broke its own rule.** `test_every_canonical_line_scores_a_clean_ten`
asserts that every reference line in the contract passes the contract. It failed
on `phase2_callout`: `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER` was counted as
seven words against a six-word banner limit, because the dash separator counted
as a word. The slot's own example failed the rule it was written to illustrate.
The measurement was wrong, not the line — a HUD separator is typography, not a
word — but I would have shipped the guide without noticing, and every banner in
the game would have inherited a limit that was silently one word tighter than
documented.

**2. Two of my own rules cannot both be satisfied.** `L3` requires a Final Clash
unlock line to state **both** gate conditions. `L4` forbids printing provisional
numbers. Inside `final_clash_unlock`'s 36-character budget, stating the health
condition requires printing **25%**. Neither rule is wrong; together they are
unsatisfiable.

I did not notice writing them. The refiner did, on the first seed that produced a
single-gate line — and it **refused** rather than picking a winner:

> `cannot safely fix L3: stating both Final Clash gate conditions requires
> printing the 25% health threshold, which L4 forbids as a provisional value
> (section 03, page 3). The character budget or the threshold has to give, and
> that is the designer's call`

See [`evidence/runs/final-clash-unlock-seed4/`](evidence/runs/final-clash-unlock-seed4/run.md).
The decision — raise the budget, or approve 25% as shipped copy — is still open
and is the designer's.

---

## The citations are load-bearing, not decorative

Every rule and slot in the contract cites a GDD section, a page, and the exact
wording it relies on. `retrieval.py` resolves each citation against
`gdd/sections/`, flattens the PDF extraction's hard wraps, and reports whether
the quoted wording is actually there. **A test fails the build if any citation
does not verify.**

That test failed on its first run. Fourteen of seventeen citations quoted wording
that was close but paraphrased — the rules were right, the quotes were not. All
seventeen now resolve to the authored line, and each run report prints the GDD
line behind the slot it generated.

---

## What the refiner will not do

It refuses rather than guesses, and a refusal is a legitimate outcome:

- **`L3`** — the rule collision above.
- **`V2`, when the required term will not fit** — the remaining fix is a shorter
  name for the system, and `CLAUDE.md` records Crimson Vanguard's shorter
  in-combat UI label as an open gap. (A guard; no seed reaches it.)
- **Any fault it cannot locate** — silence is not a correction.

Three open values are enumerated in the contract, each with the reason it is open
and the document that says so. No successful run across the 1200-run sweep fills
one.

---

## The committed runs

| Run | Stop reason | Shows |
|---|---|---|
| [`impact-window-prompt-seed33`](evidence/runs/impact-window-prompt-seed33/run.md) | `SUCCESS` (3) | **Example 1 — tone** |
| [`phase2-callout-seed40`](evidence/runs/phase2-callout-seed40/run.md) | `SUCCESS` (3) | **Example 2 — vocabulary** |
| [`meter-feedback-counter-seed119`](evidence/runs/meter-feedback-counter-seed119/run.md) | `SUCCESS` (2) | **Example 3 — format and length** |
| [`clash-failure-recovery-seed69`](evidence/runs/clash-failure-recovery-seed69/run.md) | `SUCCESS` (3) | **Example 4 — three lore breaks a style checker would pass** |
| [`final-clash-unlock-seed4`](evidence/runs/final-clash-unlock-seed4/run.md) | `HUMAN_REVIEW_REFINER_REFUSED` | Two rules that cannot both hold |
| [`clash-failure-recovery-seed2`](evidence/runs/clash-failure-recovery-seed2/run.md) | `SUCCESS` (1) | A clean line, no drift — the evaluator accepts good copy |
| [`breaker-reachability`](evidence/runs/breaker-reachability/sweep.md) | — | 1200 runs: which stops fire, and two invariants |

---

## The sweep, and one breaker that never fires

1200 runs — six slots × 200 seeds:

| Stop reason | Runs | Share |
|---|---:|---:|
| `SUCCESS` | 949 | 79.1% |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | 227 | 18.9% |
| `HUMAN_REVIEW_REFINER_REFUSED` | 24 | 2.0% |
| `CIRCUIT_BREAKER_NO_PROGRESS` | **0** | 0.0% |

Assignment 06 ended by proving its no-progress breaker unreachable rather than
leaving it merely untested. The same holds here, and structurally rather than by
luck: a run only reaches the no-progress check after a refinement was *applied*,
every applied refinement changes the text, and a fix always removes the evidence
its fault was built from. Two consecutive attempts cannot share a signature.

It stays anyway. It costs nothing, and it is the guard that would catch a future
fix that edits the copy without clearing the fault it was called for — which is
exactly the bug the `_fix_f2` word-count branch would have introduced.

The sweep also checks two invariants no single demo can show: **every `SUCCESS`
still passes when scored again from scratch** (0 failures), and **the score never
moves backwards inside a run** (0 failures). A refinement that cleared one fault
by introducing another would break the second one immediately.

---

## Pipeline connection

This Style Guide Agent runs immediately after combat copy is drafted for any HUD
slot and before that copy reaches the `UI_DuelHUD` and `UI_LifeBar` Blueprints,
so no line enters the build asserting a rule the GDD does not have or a tuning
value the designer never approved.

---

## Rubric

| Criterion | Pts | Where it is satisfied |
|---|---:|---|
| Capstone-anchored style guide | 4.5 | [`STYLE-GUIDE.md`](STYLE-GUIDE.md) and [`contracts/style_rules.json`](pipeline/contracts/style_rules.json). Eleven rules across **four** constraint types — tone, vocabulary, lore, formatting/length — against a required three. Every rule cites a GDD section, page, and verbatim wording; `retrieval.py` verifies all seventeen citations and a test fails the build otherwise. |
| Evaluator and refiner loop | 3.0 | `SCORE: [X/10]` + `REASON` from [`evaluator.py`](pipeline/evaluator.py); [`refiner.py`](pipeline/refiner.py) rewrites from the reason alone; [`orchestrator.py`](pipeline/orchestrator.py) runs it unattended with a circuit breaker. 134 tests. |
| Before / after demonstration | 2.0 | Examples 1–3 above cover tone, vocabulary, and formatting/length; Example 4 adds lore. All six runs committed under `evidence/runs/`. |
| Pipeline connection | 0.5 | The single sentence above. |

**Grading is never binary.** The evaluator's output is a score on a 1–10 scale
plus a per-criterion reason; `passed` is derived from the score and nothing else.
There is no gate that can reject a line without scoring it — this is the one
structural thing Assignment 06 did that this pipeline deliberately does not.

---

## What this does not do

It does not write to `Content/`, does not touch Unreal, and does not create a
single asset. Generated copy stops in `evidence/` and waits for the designer.
`CLAUDE.md` puts every gameplay asset under Anthony's ownership and marks the
numbers provisional; this pipeline generates and checks, and shipping is the
designer's call.
