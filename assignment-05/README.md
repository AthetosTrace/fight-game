# Assignment 05 — Goal-Oriented Coding Agent

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy martial-arts
action fighter. Unreal Engine 5.8, PC, Blueprint-only.
**Author:** AthetosTrace · **Repo:** `AthetosTrace/fight-game`

---

## What to look at

```
assignment-05/
├── README.md            you are here
├── agent/               the reasoning layer — ranks work, enforces goals
├── arena-pipeline/      the build layer — generates, validates, refines, emits code
└── evidence/            run logs, findings, and the audit trail behind every claim
```

Run it:

```bash
python -m pip install pytest

# the full loop: generate -> validate -> evaluate -> refine -> stop
python assignment-05/arena-pipeline/orchestrator.py --seed 8

# generate the code that builds the level in Unreal
python assignment-05/arena-pipeline/materializer.py \
    assignment-05/evidence/runs/seed8/final_plan.json \
    --allow-proposed --out-dir assignment-05/evidence/runs/seed8/generated

# 77 tests
python -m pytest assignment-05/arena-pipeline/tests -q
```

---

## How the five requirements are met

| Requirement | Where | What it does |
|---|---|---|
| **Read the GDD** | `arena-pipeline/contracts/arena_rules.json` | Every rule names the GDD or design document it came from. R1's source is the blackboard §14.1; the arena footprint is `design/group-04-spacing-and-arena.md` Q24; the landmark set comes from GDD page 11, the Shattered Ring reference sheet |
| **Scan the codebase** | `arena-pipeline/contracts/arena_rules.json`, statuses `MEASURED` | See the note below — this is a Blueprint-only project |
| **Detect gaps** | `arena-pipeline/validate_arena_plan.py` | Rules R1–R8 check a candidate arena against those requirements and report every violation with expected-vs-actual |
| **Prioritize** | `agent/goal-planner.md` and `arena-pipeline/refiner.py` | Two different ranking rules, described below |
| **Generate code** | `arena-pipeline/generator.py`, `materializer.py` | The generator writes arena plans; the materializer emits `build_level.py`, runnable Python that builds the level in Unreal |

### A note on "scan the codebase"

*Ascendant Impact* has **no source files.** It is a Blueprint-only Unreal project —
no `Source/` folder, no C++, no build. All logic lives in binary `.uasset` files
that cannot be read as text.

So "scanning the codebase" here means reading the live project rather than
parsing files. Rules marked `MEASURED` were taken from the actual shipped
Blueprints:

| Value | Read from |
|---|---|
| Combat clamp ±650 cm | `BP_VanguardDuelMover.ApplyConstraints` |
| Camera distance curve `clamp(450 + 0.8 × separation, 500, 1500)` | `BP_DuelCameraRig` |
| Jump apex ~180 cm | `CharacterMovement` `JumpZVelocity` 820 / `GravityScale` 1.9 |
| Min axis separation 78 cm | Capsule radii 35 + 34, plus margin |

The validator reproduces the camera rig's real distance curve, so a plan that
passes R4 will frame correctly in the actual rig rather than in a model of it.

---

## 1. What the agent built

**It built the arena.** Specifically, it generated a validated arena plan and
then the code that constructs that arena as a real level in Unreal.

The system has two halves.

### The reasoning layer — `agent/`

`goal-planner.md` ranks open work. Its two hooks are what make the goal real:

- **`entry_gate.py`** fires on `PreToolUse` and refuses to start an agent whose
  input files are not on disk yet.
- **`exit_gate.py`** fires on `SubagentStop` and refuses to let an agent finish
  until the artifact it promised actually exists.

The reason these are goals rather than conventions is that **the check runs
outside the agent** — a separate program reading the filesystem. An agent can be
wrong about whether it finished. The program reading the disk cannot.

### The build layer — `arena-pipeline/`

```
attempt 1..3:
    generate (first attempt) or take the refined plan
    deterministic gate  -> violations? refine one field, retry
    evaluator           -> criteria failed?  refine one field, retry
    both clean          -> SUCCESS
```

- **Generator** — parametric and seeded, so any run in a report reproduces exactly.
- **Deterministic validator** — R1–R8, checked before any judgement call is made.
- **Evaluator** — four weighted criteria, pass mark 70.
- **Refiner** — one field per attempt, with a before/after diff.
- **Circuit breaker** — stops after three attempts, or earlier on no progress.
- **Materializer** — turns a passing plan into `build_level.py` and a manifest.

Three runs are committed in `evidence/runs/`:

| Run | What it demonstrates |
|---|---|
| `seed8` | Clean pass on the first attempt — its `generated/` folder holds the emitted `build_level.py` |
| `seed4` | Two refinements, then success — the refiner working |
| `seed2` | Three attempts used, faults remain — the circuit breaker stopping |

---

## 2. Why the agent selected that feature

**Two ranking rules, both written down, neither a judgement call.**

### Which feature to build — the blocking-step rule

Every open item is ranked by **the lowest-numbered step in `build-sequence.md`
that cannot execute until it is answered.** `build-sequence.md` holds 63 ordered
Unreal editor steps and was written *before* most of these questions were asked,
which is what makes it a fair referee — it cannot be bent to justify a convenient
order.

The arena came out at **`M1-21`, gray-box `L_ShatteredRing`**, and it ranked
early for a concrete reason: **you cannot gray-box a floor without dimensions.**
Ranking it also exposed a dependency chain — Attack D's travel distance is
defined as a fraction of the arena footprint, and the failed-Clash separation has
to fit inside it, so all three had to move together or disagree.

### Which correction to make — the smallest-correction rule

Inside a run, the refiner changes **exactly one field per attempt** and records a
before/after diff. It refuses rather than guesses when a fix is not ours to make.
The clearest case is R4, camera framing: the only real fix is retuning
`BP_DuelCameraRig`, which belongs to the gameplay owner, so the refiner escalates
instead. **That refusal is enforced in code, not documented as a convention.**

The same applies to unresolved inputs. `design/group-04-spacing-and-arena.md`
opens with *"EVERY ANSWER IN THIS FILE IS PROPOSED, NOT DECIDED"*, so the
validator will not enforce a `PROPOSED` value as a requirement. It reports it for
human review and stops. The pipeline is built so it cannot invent a missing
gameplay requirement.

---

## 3. Were you able to run this in your game?

**Yes.**

The generated `build_level.py` was run against a live Unreal 5.8 editor session
over the `unreal-mcp` server. It created 12 actors and saved the level to
`/Game/ArenaTools/Maps/Lvl_ArenaGen_Seed8` — floor, ceiling, two end walls, two
side railings, four landmarks, and two spawn markers.

The result was then verified **in the engine** by ray-tracing the built geometry,
rather than by trusting the script's own output:

| Check | Measured in engine | Rule |
|---|---|---|
| Floor height across the combat span | Z = 0.0 at all 5 sample points | R3 — flat floor at Z = 0 |
| Nearest blocking geometry | 500.0 cm beyond the ±650 bound | R2 — clearance ≥ 500 cm |
| Headroom above centre | 515 cm | R7 — ≥ 388 cm for a jump-over |

### What building it revealed

Two defects survived the deterministic gate and were only caught once a level
actually existed. Both are recorded in
[`evidence/ARENA_PIPELINE_FINDINGS.md`](evidence/ARENA_PIPELINE_FINDINGS.md).

1. **Clearance was measured to obstacle centres, not faces.** An obstacle 507.7 cm
   beyond the combat bound passed R2 while its near face sat 482.7 cm out —
   legal on paper, illegal in the level. Clearance is now measured face to face.
2. **Landmarks were being placed inside each other.** Two landmarks at the same
   end share a depth plane, and their lateral positions were sampled
   independently, so 300 cm boxes overlapped on 26 of 42 passing seeds.

Both were invisible to a validator reading a plan, because a plan is
dimensionless and a level is not. That gap is the argument for building the
thing rather than only checking it.

### And a finding about the game itself

The pipeline surfaced a real constraint that nobody had multiplied out. The
arena's long axis is 2400 cm, the combat span is 1300 cm, and environment
geometry must keep 500 cm of clearance:

```
1200 (half the long axis) − 650 (combat bound) − 500 (clearance) = 50 cm
```

**Fifty centimetres of depth at each end for all environment geometry.** End
features can be shallow wall relief but not free-standing objects. That happens
to suit the landmarks already named — the doorway frame, the truss panel and the
mezzanine struts are all wall-attached — so nothing is blocked, but it constrains
environment art from here on.

---

## Honest limits

- **The mezzanine, corner chamfers and the centred doorway are not enforced.**
  The pipeline checks the arena's *dimensions* but not its *layout*. GDD page 11
  fixes the doorway centred on the far short wall and Q24 specifies 250 cm corner
  chamfers; the generator currently randomises the doorway and ignores chamfers.
  These are queued as candidate rules R9–R11, pending the designer's sign-off,
  because changing what the generator may produce is an arena-design decision.
- **The agent-judge evaluator backend is a seam, not built.** `--judge agent`
  stops for human review. The heuristic evaluator is what runs today.
- **The generated level is not the shipping arena.** `design/group-08-assets.md`
  specifies the Shattered Ring as authored in-editor by the team. The generated
  level is a rules-legal test arena that proves the constraints are satisfiable
  and buildable — not a replacement for authored environment art.
- **The pipeline also lives in the Unreal implementation repo**, where it is the
  working copy. The copy here is the snapshot submitted for this assignment; the
  two are byte-identical as of this commit.
