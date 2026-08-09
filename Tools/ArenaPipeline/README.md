# Arena Pipeline

A headless generate → validate → evaluate → refine loop for Ascendant Impact
arena layouts, with a three-attempt circuit breaker.

It is a **command-line tool**. It reads and writes JSON and Markdown. It does not
open Unreal, does not touch any existing asset, and creates no binary files. See
[`OWNERSHIP.md`](OWNERSHIP.md) for the boundaries it operates under.

> **Reviewing this for the first time?** Start with
> [`docs/arena/ARENA_PIPELINE_FINDINGS.md`](../../docs/arena/ARENA_PIPELINE_FINDINGS.md)
> — a short summary of what running this pipeline revealed about the arena
> dimensions, and the two decisions still waiting on the gameplay owner.

## Status

| Stage | State |
|---|---|
| Contracts + sourced rules | done |
| Deterministic validator (R1–R8) | done |
| Generator | done |
| Evaluator (heuristic judge) | done |
| Refiner | done |
| Circuit breaker + orchestrator + logs | done |
| Unreal materializer | done — builds a graybox level via unreal-mcp |
| Evaluator (LLM judge backend) | seam exists, not built |

77 tests passing.

## Requirements

Python 3.10+ and `pytest` for the test suite. No other dependencies.

```powershell
python -m pip install pytest
```

## Run it

The whole loop — generate, validate, evaluate, refine, stop:

```powershell
python Tools/ArenaPipeline/orchestrator.py --seed 8
```

Writes `reports/arena/seed8/` containing `run.md` (readable log), `run.json`
(machine-readable) and `final_plan.json`. Add `--no-report` to print only.

Individual stages:

```powershell
python Tools/ArenaPipeline/generator.py --seed 8 --out plan.json
python Tools/ArenaPipeline/evaluator.py plan.json
```

Validate a plan:

```powershell
python Tools/ArenaPipeline/validate_arena_plan.py Tools/ArenaPipeline/examples/arena_plan.baseline.json
```

Machine-readable output for the orchestrator:

```powershell
python Tools/ArenaPipeline/validate_arena_plan.py <plan.json> --json
```

Turn a passing plan into a level:

```powershell
python Tools/ArenaPipeline/materializer.py reports/arena/seed8/final_plan.json `
    --allow-proposed --out-dir reports/arena/seed8/build
```

Run the tests:

```powershell
python -m pytest Tools/ArenaPipeline/tests -q
```

## The materializer, and why it exists

The plan is *dimensionless*. Obstacles and boundaries are points, and the
deterministic gate compares those points to the combat bounds. A level is not
dimensionless — the moment a point becomes a box it grows faces, and a face is
closer to the fighting space than the centre it was measured from.

So the materializer does not just place actors. It resolves every plan element
into a world-space box, then re-checks R2, R3 and R8 against the resulting
**faces**, and refuses to emit a build script if the realised geometry violates
a rule the plan passed. It writes no Unreal asset itself: it emits
`manifest.json`, a readable `manifest.md`, and `build_level.py`, which a human
runs against a live editor session through unreal-mcp. See
[`OWNERSHIP.md`](OWNERSHIP.md) for what that script is allowed to touch.

Extents are not design decisions. They live in the `materializer` block of
`contracts/arena_rules.json` with status `PROPOSED`, and the stage refuses to
build without `--allow-proposed`, exactly as the validator refuses to enforce a
`PROPOSED` requirement. Every run says so in its report.

**Two real defects were found by building the thing.** Both passed the
deterministic gate and both were seed-dependent, so neither was visible on
paper:

1. **Clearance was measured to obstacle centres.** An obstacle 507.7 cm beyond
   the bound passed R2 while its near face sat 482.7 cm out. R2's source says
   "nearest environment keeps >= 500 cm clearance" — a distance between real
   surfaces — so the centre-based check was the approximation, not the fix.
   Clearance is now measured face-to-face in the validator, the refiner and the
   materializer, driven by one `obstacle_extents` block the generator writes
   onto the plan. Plans that declare no footprint keep the old point behaviour,
   so archived plans stay valid.
2. **Landmarks were placed inside each other.** Both landmarks at an end share
   an X plane, and their Y positions were sampled independently, so two 300 cm
   boxes overlapped on 26 of 42 passing seeds. The generator now partitions the
   Y band per end.

Neither is caught by any rule in `contracts/arena_rules.json`, because both are
properties of geometry the plan does not describe. That is the argument for the
stage: the gate checks the plan, and the materializer checks the thing the plan
becomes. The test suite sweeps 50 seeds asserting both.

### What the arena's dimensions actually allow

Worth Anthony's attention, because it constrains environment art rather than the
pipeline: with a 2400 cm long axis, a 1300 cm combat span and R2's 500 cm
clearance, the space left for end geometry is

```
half long axis 1200 - combat bound 650 - clearance 500 = 50 cm
```

**50 cm of depth at each end.** So end landmarks can only be shallow wall
relief, not free-standing blocks — which suits `Doorway_Frame`, `Truss_Panel`
and the mezzanine struts, all wall-attached features by name. Anything deeper
needs either a longer arena or a smaller clearance, and both are his call. This
is the same 50 cm that resolution U1 noted as its margin "to spare"; it is not
spare, it is the entire budget for environment geometry.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Passed every applicable rule |
| 1 | One or more rule violations |
| 2 | **Human review required** — an unresolved input, or a PROPOSED value was needed |
| 3 | Bad usage or unreadable input |

Code 2 is not a failure. It is the pipeline refusing to proceed on information it
does not have.

Separately, a clash we resolved ourselves is reported as **decided, pending
confirmation** and does *not* block. Each such resolution must record its
decision, evidence, reversal cost, who decided it, and who confirms it — enforced
by a test. The baseline currently exits 0 with two decisions pending Anthony's
confirmation (U1 and U2 below).

## Why the rules are data, not code

`contracts/arena_rules.json` holds every threshold, and each rule carries a
`source` naming the document it came from and a `status`:

- `MEASURED` — read from the shipped build or its blackboard record
- `APPROVED` — signed off in `design/decisions.md`
- `DERIVED` — computed from the above by documented arithmetic
- `PROPOSED` — recommended by a design dispatch but **not decided**

The validator will not enforce a `PROPOSED` value as a requirement. It reports it
under *human review required* and moves on, unless `--allow-proposed` is passed.
This matters because `design/group-04-spacing-and-arena.md` opens with *"EVERY
ANSWER IN THIS FILE IS PROPOSED, NOT DECIDED"*, and `design/decisions.md` records
items that were wrongly marked approved and had to be reopened. The pipeline is
built so it cannot repeat that mistake.

## The loop, and when it stops

```
attempt 1..3:
    generate (first attempt) or take the refined plan
    deterministic gate  -> violations? refine one field, retry
    evaluator           -> criteria failed? refine one field, retry
    both clean          -> SUCCESS
```

| Stop reason | Meaning | Exit |
|---|---|---|
| `SUCCESS` | Gate clean and evaluator above threshold | 0 |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | Three attempts used, faults remain | 1 |
| `CIRCUIT_BREAKER_NO_PROGRESS` | Identical failures two attempts running | 1 |
| `HUMAN_REVIEW_REFINER_REFUSED` | A fix we are not allowed or able to make | 2 |
| `HUMAN_REVIEW_REQUIRED` | An undecided input | 2 |

Two details worth knowing:

**No-progress is measured on the failure *detail*, not the rule id.** Fixing one
of two `R2` obstacles leaves `R2` still failing — that is progress, and a
rule-id-only comparison would misread it as a stalled loop.

**The refiner only runs when an attempt remains to verify it.** Applying a
correction on the final attempt and exiting would end the log on an unverified
claim.

## What the refiner will not do

It refuses rather than guesses, and a refusal is a legitimate outcome:

- **`R4` (camera framing)** — the only fix is retuning `BP_DuelCameraRig`'s
  `DistancePerSeparation` / `MaxCameraDistance`, which the gameplay owner owns.
  The ownership boundary is enforced in code, not just documented.
- **`R8`, `landmark_asymmetry`, `staging_room`** — creative decisions.
- **Anything with no matching rule** — silence is not a correction.

## The rules

| ID | Rule | Source |
|---|---|---|
| R1 | Combat axis spans ≥ 1300 cm | blackboard §14.1 |
| R2 | Blocking geometry ≥ 500 cm beyond the combat bound | blackboard §14.1 |
| R3 | Floor at Z=0, fighting space clear | blackboard §13.2 |
| R4 | Camera frames both fighters at max separation | blackboard §14.2 |
| R5 | Camera depth corridor unoccluded | derived from §14.2 |
| R6 | Two spawns, on floor, facing, legally separated | blackboard §13.2, §15 |
| R7 | Headroom ≥ jump apex + character height | blackboard §23, decisions item 28 |
| R8 | Perimeter geometry outside the combat volume | blackboard §13.2 |

R4 reproduces `BP_DuelCameraRig`'s actual distance curve —
`clamp(450 + 0.8 × separation, 500, 1500)`, half-width ≈ distance × 0.52 — so a
plan that passes here will frame correctly in the real rig.

## Decisions we made, pending Anthony's confirmation

Tracked in the `unresolved` array of `contracts/arena_rules.json` and printed on
every run. Both are reversible by editing that one file.

**U1 — 1300 cm vs 2400 cm.** These describe different things and were never truly
in conflict. `CombatAxisMin/Max` ±650 is the *fighter clamp* in
`ApplyConstraints`; Q24's 2400 × 1600 is the *arena floor footprint*. We target a
2400 × 1600 room containing a centred 1300 cm combat span. Room half-axis 1200 −
combat bound 650 = **550 cm**, which satisfies R2's 500 cm requirement with 50 cm
to spare. *Reversal cost:* a true 2400 cm combat span needs `MaxCameraDistance`
1500 → ~2404, shrinking the fighters at FOV 55.

**U2 — camera exclusion volume.** At max separation the camera sits ~1457 cm back
(1490 × cos 12°), which is ~650 cm outside the side wall of a 1600 cm deep hall.
We treat the corridor as excluding *blocking gameplay geometry only*, and exempt
the arena's own near wall when flagged `camera.near_wall_culled` — standard
fighting-game near-wall culling. *Reversal cost:* widen the short axis to
~2915 cm, or cap fighter separation.
