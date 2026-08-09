# Arena pipeline — first working version

**From:** AthetosTrace (agent orchestration + arena pipeline)
**For:** Anthony Travieso
**Branch:** `feature/agent-arena-pipeline`, cut from `feature/duel-jump-feel-polish`
**Date:** 2026-08-09

Everything in the "first working version" list is built and running. This
document covers what was delivered, what we found while building it, and the
short list of things that need a decision from you.

Nothing here is blocked. The pipeline runs today.

---

## 1. Requirements coverage

| What you asked for | Status | Where |
|---|---|---|
| A generator that creates an arena plan or arena data | Done | `Tools/ArenaPipeline/generator.py` |
| Deterministic checks for required measurements and rules | Done | `validate_arena_plan.py` — rules R1–R8 |
| An evaluator with game-specific criteria | Done | `evaluator.py` — 4 weighted criteria, pass mark 70 |
| A refiner that applies the smallest correction | Done | `refiner.py` — one field per attempt, before/after diff |
| A three-attempt circuit breaker | Done | `orchestrator.py` — `MAX_ATTEMPTS = 3`, plus a no-progress stop |
| Clear logs showing what happened during each attempt | Done | `reports/arena/<run>/run.md` and `run.json` |
| A README explaining how to run and test it | Done | `Tools/ArenaPipeline/README.md` |
| Stop and request human review rather than invent requirements | Done | exit code 2; see §2 |

Your rules checklist is covered as follows:

| Your wording | Rule |
|---|---|
| arena size | R1 — combat axis spans at least the maximum legal separation |
| combat space | R2 clearance, R3 flat and clear floor |
| camera safety areas | R4 framing at max separation, R5 corridor |
| spawn areas | R6 — two spawns, on floor, facing, legally separated |
| boundaries | R8 — perimeter outside the combat volume |
| "and other requirements" | R7 — jump-over headroom |

Every threshold is sourced. Each rule in `contracts/arena_rules.json` names the
document it came from and carries a status: `MEASURED`, `APPROVED`, `DERIVED`,
or `PROPOSED`.

**Three example runs are committed as evidence:**

| Run | What it shows |
|---|---|
| `reports/arena/seed8/` | Clean pass on the first attempt |
| `reports/arena/seed4/` | Two refinements, then success — the refiner working |
| `reports/arena/seed2/` | Three attempts used, faults remain — the circuit breaker stopping |

77 automated tests pass.

---

## 2. It refuses rather than guesses

You asked that it not invent missing gameplay requirements. Three mechanisms
enforce that, and all three are tested:

1. **A `PROPOSED` value is never enforced as a requirement.** `group-04` opens
   with "EVERY ANSWER IN THIS FILE IS PROPOSED, NOT DECIDED", so the validator
   reports those under human review and moves on unless explicitly waived.
2. **The refiner refuses fixes that are not ours to make.** R4 camera framing is
   the clearest case — the only fix is retuning `BP_DuelCameraRig`'s
   `DistancePerSeparation` / `MaxCameraDistance`, which is yours. The refusal is
   in code, not just in documentation. R8 and the creative criteria refuse too.
3. **A failure with no matching rule is a refusal, not a silent pass.**

---

## 3. What we found while building it

We ran the pipeline against a live editor session and built a graybox test level
from a passing plan — `/Game/ArenaTools/Maps/Lvl_ArenaGen_Seed8`, a separate
arena test map as you asked for. Building it surfaced things that reading the
plan could not.

### 3.1 The arena has 50 cm of depth at each end for environment geometry

This is the one that affects your design work.

Three of your numbers are individually fine and jointly very tight:

| Value | Source |
|---|---|
| Arena floor 2400 × 1600 cm | `design/group-04-spacing-and-arena.md` Q24 |
| Combat span 1300 cm (fighter clamp ±650) | `PROTOTYPE_BLACKBOARD.md` §14.1 |
| Environment clearance ≥ 500 cm beyond the bound | `PROTOTYPE_BLACKBOARD.md` §14.1 |

```
1200 (half the long axis)
-  650 (combat bound)
-  500 (required clearance)
=   50 cm
```

**Fifty centimetres at each end.** That is the whole budget between where
environment geometry may start and where the end wall is.

In practice: end features can be shallow wall relief, set into or bolted onto
the end wall. They cannot be free-standing objects you would walk around. That
suits the landmarks already named — `Doorway_Frame`, `Truss_Panel` and the
mezzanine struts are all wall-attached features — so nothing is blocked today.
It does constrain environment art going forward.

Note: resolution U1 previously described this 50 cm as clearance satisfied "with
50 cm to spare." That reading was too optimistic and we are correcting it here.
It is not spare margin. It is the entire budget.

**Your options:** accept it (this is what the pipeline assumes today), lengthen
the arena past 2400 cm, or reduce the 500 cm clearance if that figure was a
comfort margin rather than a measured constraint.

### 3.2 We now measure clearance to the face of geometry, not its centre

Our validator used to measure from the combat bound to an obstacle's centre
point. It now measures to the obstacle's nearest surface.

§14.1 says the nearest environment "keeps >= 500 cm clearance." Clearance
between real surfaces is a face-to-face distance, so checking centres was an
approximation that let geometry through. We had an obstacle whose centre was
507.7 cm clear while its actual near face was 482.7 cm clear — it passed on
paper and violated the rule in the level.

**Your 500 cm number is unchanged.** We are measuring it the way it was always
meant to be measured. Nothing you approved was reinterpreted.

### 3.3 Two bugs on our side, both fixed

Listed for completeness. Neither is in your code.

1. **Landmarks were placed inside each other.** Both landmarks at one end share
   a depth plane, and we picked their side-to-side positions independently, so
   two 3 m boxes overlapped on 26 of 42 passing runs. Fixed by partitioning the
   width into lanes.
2. **The centre-versus-face error above also affected the refiner**, which
   "corrected" clearance violations to a position that was still short by half a
   footprint. Fixed.

Both were invisible until a level was actually built from a plan. That is the
argument for having built one.

---

## 4. Open items — these need you

None of these block the pipeline. All are things you listed as yours to provide.

### 4.1 Camera exclusion areas have never been written down (U2)

You listed "camera exclusion areas" among the things you provide. There is no
spec for it, so we made a provisional call and flagged it.

At maximum separation the camera sits about 1457 cm back, roughly 650 cm outside
the side wall of a 1600 cm deep hall. We treat the camera corridor as excluding
**blocking gameplay geometry only**, and exempt the arena's own near wall using
standard fighting-game near-wall culling.

*If that is wrong:* the short axis has to widen to about 2915 cm, or fighter
separation has to be capped.

### 4.2 Is the arena 1300 cm or 2400 cm? (U1)

We concluded these were never in conflict. 1300 is the **fighter clamp**
(`BP_VanguardDuelMover.ApplyConstraints`, ±650). 2400 × 1600 is the **floor
footprint** from Q24. We build a 2400 × 1600 room containing a centred 1300 cm
combat span.

*If that is wrong:* a true 2400 cm combat span needs `MaxCameraDistance` raised
from 1500 to about 2400, which shrinks the fighters noticeably at FOV 55.

### 4.3 Should your locked layout become enforced rules?

You own arena design and you supplied the reference. Right now the pipeline
enforces your **dimensions** but not your **layout**. Three specifics from GDD
page 11 and Q24 are not currently checked:

| Your spec | Pipeline today |
|---|---|
| "One bright doorway **centred** on the far short wall" — Q24, p.11 panel 1, §08 | The generator randomises the doorway's position along the wall |
| "Four corners chamfered at 45° with a **250 cm leg**" — Q24, called "a gameplay feature, not decoration" | Not modelled. The value `corner_chamfer_leg_cm: 250.0` is already in our contract file, unused |
| Truss panel "set into the concrete band" on the mezzanine | Placed at floor level |

The mezzanine itself is correctly absent — dispatch 04 ruled it set dressing.

**Ask:** do you want these encoded as hard rules (R9, R10, R11)? That is
squarely our job — you provide the requirement, we build the check. We did not
add them unilaterally because they change what the generator is allowed to
produce, and that is arena design.

### 4.4 Smaller items

- **The closed roof is our choice, not yours.** The plan carries a ceiling
  *height* for the R7 headroom check; we built it as a solid slab to make the
  limit visible. Your reference calls overhead skylights "the dominant lighting
  signature of the space." Easy to change — it is one flag in the materializer.
- **The agent-judge evaluator backend is a seam, not built.** `--judge agent`
  currently stops for human review. The heuristic evaluator is what runs today.
- **Suggested one-line addition to `.gitignore`:** `.pytest_cache/`. We did not
  edit your `.gitignore` — running the test suite from the repo root creates
  that folder.

---

## 5. What we did not touch

- No existing Blueprint, map, or asset was opened for edit.
- **This PR contains no binary files.** Only `.py`, `.json` and `.md`, so
  nothing goes through Git LFS and nothing can conflict with your work.
- The generated test level is **not committed**. It is reproducible output — one
  command rebuilds it — and committing generated `.umap` files into LFS is how
  merge conflicts start.
- The level was seeded from the stock **engine** template, not from
  `Lvl_ThirdPerson` or `Lvl_DuelGraybox`. Placed actors are engine cubes plus a
  `PlayerStart` and a `TargetPoint`. Nothing imported, no plugins, no Blueprints
  created or compiled.
- This is enforced by a test, not just by policy: the emitted build script is
  checked for any path under `/Game/ThirdPerson`, `/Game/Variant_Combat` or
  `/Game/AscendantImpact`, and the test fails if one appears.

---

## 6. Proof it runs

Built in a live editor session, then measured **in the engine** by ray-tracing
the actual geometry rather than trusting our own output:

| Check | Measured | Requirement |
|---|---|---|
| Floor height across the combat span | Z = 0.0 at all 5 sample points | R3: flat at Z = 0 |
| Nearest blocking geometry | 500.0 cm beyond the ±650 bound | R2: ≥ 500 cm |
| Headroom above centre | 515 cm | R7: ≥ 388 cm |

To reproduce:

```powershell
python Tools/ArenaPipeline/orchestrator.py --seed 8
python Tools/ArenaPipeline/materializer.py reports/arena/seed8/final_plan.json `
    --allow-proposed --out-dir reports/arena/seed8/build
python -m pytest Tools/ArenaPipeline/tests -q
```

The materializer writes `build_level.py`, which is what gets run against a live
editor session through unreal-mcp. See
[`Tools/ArenaPipeline/OWNERSHIP.md`](../../Tools/ArenaPipeline/OWNERSHIP.md).

---

## 7. What we need from you

1. **§3.1** — accept the 50 cm end budget, or tell us to lengthen the arena or
   lower the clearance requirement.
2. **§4.1 and §4.2** — confirm or reject our provisional calls on the camera
   exclusion area and the 1300/2400 reading.
3. **§4.3** — tell us whether the centred doorway, the 250 cm chamfers and the
   truss placement should become enforced rules.

Everything else is informational. Each provisional decision is reversible by
editing one file, `Tools/ArenaPipeline/contracts/arena_rules.json`.
