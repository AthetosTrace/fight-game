# Assignment 06 — A GER Pipeline for *Ascendant Impact*

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy martial-arts
action fighter. Unreal Engine 5.8, PC, Blueprint-only. The player picks Agent Echo or
Agent Nova and fights **Crimson Vanguard / Project Valor-7** in the **Shattered Ring**.
**Author:** AthetosTrace · **Repo:** `AthetosTrace/fight-game`

**Content type generated:** Crimson Vanguard **attack-definition rows** — the
seventeen-column `DT_VanguardAttacks.csv` that drives the rival's four authored attacks.

---

## Pre-Build Declaration

Committed on its own, before any pipeline code — see
[`PRE-BUILD-DECLARATION.md`](PRE-BUILD-DECLARATION.md) and commit `a2df9a4`.

**01. What content type does your game currently generate manually, inconsistently, or
not at all?**
Crimson Vanguard attack-definition rows — the seventeen-column `DT_VanguardAttacks.csv`
that drives the rival's four authored attacks in Unreal. Every row is hand-typed today.

**02. What specific rule from your GDD must every piece of that content satisfy?**
GDD §04, page 5 ("Four-attack course set"): exactly four authored attacks exist, A–D,
each carrying the GDD's stated range and purpose plus a readability requirement — a
visible wind-up and a punishable recovery. Page 6 binds Phase 2 to re-timing those same
four attacks, never a new moveset.

**03. What does a failure look like — concretely, in your game's terms?**
A row for a fifth attack, a Phase 2 row describing a new move, or an OPEN field filled
with an invented number. Imported, that hands Crimson Vanguard an attack the designer
never authored, or a tuning value nobody approved.

---

## Run it

```bash
python -m pip install pytest

# the whole loop — generate, gate, evaluate, refine, stop
python assignment-06/pipeline/orchestrator.py --attack A --seed 6

# assemble all four attacks into a full table
python assignment-06/pipeline/emit_csv.py

# check that table with the validator that already guards the shipped CSV
python tools/validate_vanguard_attack_csv.py \
    assignment-06/evidence/generated_DT_VanguardAttacks.csv

# 152 tests, no engine, no network, no API key
python -m pytest assignment-06/pipeline/tests -q
```

```
assignment-06/
├── PRE-BUILD-DECLARATION.md    committed before any code
├── pipeline/
│   ├── contracts/attack_rules.json   the rules, each citing a GDD section and page
│   ├── retrieval.py                  RAG over the GDD-cited knowledge base
│   ├── generator.py                  builds a row, then drifts it
│   ├── evaluator.py                  deterministic gate + scored rubric
│   ├── refiner.py                    one field per attempt, or a refusal
│   ├── orchestrator.py               the loop and the circuit breaker
│   ├── emit_csv.py                   assembles the full four-row table
│   └── tests/                        152 tests
└── evidence/runs/                    six committed runs
```

---

## The loop

```
attempt 1..3:
    generate (first attempt) or take the refined row
    deterministic gate  -> violations? refine one field, retry
    evaluator           -> criteria failed? refine one field, retry
    both clean          -> SUCCESS
```

| Stop reason | Meaning | Exit |
|---|---|---|
| `SUCCESS` | Gate clean and every criterion passed | 0 |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | Three attempts used, faults remain | 1 |
| `CIRCUIT_BREAKER_NO_PROGRESS` | Identical failure signature two attempts running | 1 |
| `HUMAN_REVIEW_REFINER_REFUSED` | A decision that belongs to the designer | 2 |

Two details carried over from the arena pipeline because they earned their keep.
**No-progress is measured on the failure detail, not the rule id** — clearing one of two
`G6` fields leaves `G6` still failing, and that is progress. **The refiner only runs when
an attempt remains to verify it** — applying a correction on the final attempt would end
the log on an unverified claim.

### Why the generator deliberately produces bad rows

A generator that always emitted a perfect row would make the evaluator ceremonial. So
`generator.py` builds a canon-faithful row from the GDD facts, then applies seeded
**drift** — the eight ways this content actually goes wrong: over-specifying a number
nobody approved, inflating "re-timed" into "upgraded", dropping a "(proposed)" caveat,
reaching for adaptive-AI language because that is how enemy AI is usually described.
Drift is seeded, so every defect is reproducible and traceable to the operator that
introduced it. The evaluator never sees which operators fired.

---

## What the evaluator enforces, and where it comes from

Every rule in [`contracts/attack_rules.json`](pipeline/contracts/attack_rules.json)
cites the GDD by **section and page**. A test asserts this and asserts that none of them
cite `PROTOTYPE_BLACKBOARD.md`.

| ID | Rule | GDD source |
|---|---|---|
| G1 | The attack set is exactly A–D. No fifth attack, no alternate move set | §04, p5 — "Four-attack course set" |
| G2 | Every attack shows a visible committed cue and a punishable opening | §04, p5 — readability column + "Behavioral intent" |
| G3 | Phase 2 re-times the same four attacks, never a new moveset | §04, p6 — "Phase 2 escalation" |
| G4 | No runtime learning, adaptation, or AI-model call | §04, p5 — "REVISED — RUNTIME AI BOUNDARY" |
| G5 | Scope lock — one duel, one arena, one rival | §09, p15 — "Course Scope Lock" |
| G6 | No invented damage, range, cooldown, travel cap, or timing | §04, p5 — range stated qualitatively; timings provisional |
| G7 | Attack D states a thruster cue and never a full-arena snap | §04, p5 — Attack D readability requirement |

### The retrieval layer, and the gap it closes

Assignment #04 built a manifest-driven retrieval system whose every knowledge-base chunk
ends in a `*Source: gdd/… Page N*` line. Assignment #05's arena pipeline **never called
it** — grep it and you find two passing comments and zero code paths, because its rules
trace to `PROTOTYPE_BLACKBOARD.md`, which is measured implementation rather than design.

This pipeline is the join. `retrieval.py` runs A#04's scoring over A#04's knowledge base,
pinning the *Hard constraint* and *Scope lock* chunks regardless of score, and every run
report prints the GDD pages behind the row it produced. Assignment #04's
`retrieval-manifest.md` already scoped this exact content type as **Output 1 — Crimson
Vanguard Telegraph and Readability Pack**, so the retrieval queries did not have to be
invented either.

### Two layers, doing different jobs

`gate()` asks *is this row legal?* — schema mechanics plus hard GDD canon. `evaluate()`
asks *is this a good row for Ascendant Impact?* — a weighted rubric returning a score and
a reason per criterion.

| Criterion | Weight | Asks |
|---|---|---|
| `canon_fidelity` | 30 | Does the row still say what the GDD says this attack is? |
| `telegraph_readability` | 25 | Is there a visible cue *and* a punishable opening? |
| `phase2_consistency` | 20 | Does Phase 2 read as the same attack re-timed? |
| `restraint` | 25 | Does the row avoid asserting anything the GDD leaves open? |

---

## Did the pipeline catch something I would have missed?

**Yes — and it was invisible to every check that existed before it.**

Run [`evidence/runs/attackA-seed6/`](evidence/runs/attackA-seed6/run.md). The generator
dropped the `(proposed)` caveat from Attack A's working name, leaving
`DisplayWorkingName: Fault Line`.

That row **passes the deterministic gate with zero violations.** It also passes
`tools/validate_vanguard_attack_csv.py`, the validator that guards the shipped CSV. It is
a legal string in an optional free-text column of the right length. It would import into
Unreal cleanly and sit in the DataTable looking entirely correct.

It is also **wrong**, and wrong in a way specific to this game: *the GDD names no attack.*
"Fault Line" is a working name proposed by Assignment #04's telegraph pack. Uncaveated,
the row asserts designer-approved canon that was never granted — precisely the class of
output the assignment describes as technically valid but wrong for the game.

The evaluator scored it **87.50 / 100** — comfortably above the 70 threshold — and still
failed it, because `restraint` failed and every criterion must pass:

> `restraint` **0.50** — working name 'Fault Line' is asserted as canon, but the GDD names
> no attack

The refiner then made the smallest correction that clears it — `Fault Line` →
`Fault Line (proposed)` — and the run reached SUCCESS on attempt 2.

**Why I would have missed it.** I wrote the row contract, and its §1.2 says working names
must be "explicitly caveated as pending designer approval". I then built a deterministic
validator to enforce that contract — and did not encode that clause, because it is a
sentence about honesty rather than a checkable field constraint. The rule was written
down, believed, and unenforced. A threshold-only evaluator would have missed it too: 87.5
passes.

That is the argument for the second layer. The gate checks whether the row is legal. The
evaluator checks whether it tells the truth.

---

## What the refiner will not do

It refuses rather than guesses, and a refusal is a legitimate outcome:

- **`G1`** — the authored attack set is GDD canon. A row asserting an attack outside A–D
  is a canon error with no correct value to write.
- **`G5`** — what is deferred and what ships is the scope lock, the designer's roadmap.
- **`G7`** — capping Attack D's travel means *choosing a maximum distance*. That is
  design-brief **Q13**, and it is OPEN. Inventing it is the exact failure the Pre-Build
  Declaration named. See [`evidence/runs/attackD-seed9/`](evidence/runs/attackD-seed9/run.md).

Nine OPEN values are enumerated in the rules contract, each with the reason it is open and
the document that says so. No successful run across a 4-attack × 29-seed sweep ever fills
one — there is a test for that.

---

## The committed runs

| Run | Stop reason | Shows |
|---|---|---|
| [`attackA-seed16`](evidence/runs/attackA-seed16/run.md) | `SUCCESS` (1 attempt) | A clean row, no drift |
| [`attackA-seed6`](evidence/runs/attackA-seed6/run.md) | `SUCCESS` (2) | **The evaluator catching what the gate passed** |
| [`attackA-seed2`](evidence/runs/attackA-seed2/run.md) | `SUCCESS` (3) | Two refinements, then a verified pass |
| [`attackA-seed4`](evidence/runs/attackA-seed4/run.md) | `CIRCUIT_BREAKER_MAX_ATTEMPTS` | Four drifts, three attempts, faults remain |
| [`attackA-seed3`](evidence/runs/attackA-seed3/run.md) | `HUMAN_REVIEW_REFINER_REFUSED` | A fifth-attack reference — canon, not a field |
| [`attackD-seed9`](evidence/runs/attackD-seed9/run.md) | `HUMAN_REVIEW_REFINER_REFUSED` | Attack D's travel cap is Q13, OPEN |

---

## Connecting back to the game

`emit_csv.py` runs the loop for all four attacks and assembles the full table — but only
if all four reached SUCCESS. A partial table is not a table.

The result, [`evidence/generated_DT_VanguardAttacks.csv`](evidence/generated_DT_VanguardAttacks.csv),
**passes `tools/validate_vanguard_attack_csv.py`** — a 358-line validator written months
before this pipeline existed, which knows nothing about it. That makes it a fair referee,
and the pass is asserted by a test. A second test corrupts a row and confirms the referee
still rejects it, so the pass is not the referee being asleep.

**What this pipeline does not do.** It does not write to
`data/unreal/DT_VanguardAttacks.csv`, and it does not touch Unreal. `CLAUDE.md` marks the
`S_VanguardAttackDef` / `DT_VanguardAttacks` import route **PAUSED** pending the gameplay
owner, so generated output stops in `evidence/` and waits for him. The pipeline generates
and checks; importing is his call.

---

## Two bugs the tests found while building this

Worth recording, because both were in the checking logic rather than the content, and
both would have produced silent false negatives.

1. **Negation did not cross sentence or field boundaries correctly.** The canonical
   Attack D row says *"never a full-arena snap"* — the GDD's own wording denies the very
   phrase it names. The matcher had to tell a denial from an assertion. But scoping
   negation only to commas meant `Phase2Usage`'s canonical `"- no new moveset"` reached
   across into `Notes` and laundered a planted fifth-attack reference. Fields are now
   joined on a clause boundary, and sentence-enders split clauses.
2. **Attack D's thruster-cue check read the working name.** `DisplayWorkingName` is
   *"Thruster Snap (proposed)"*, so a row with no cue anywhere in its describing fields
   still satisfied `G7`. A name is not a telegraph. The check now reads
   `ActiveDescription` and `TelegraphRequirement` only.
