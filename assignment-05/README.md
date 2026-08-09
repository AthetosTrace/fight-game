# Assignment 05 — Goal-Oriented Coding Agent

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy martial-arts
action fighter. Unreal Engine 5.8, PC, Blueprint-only.
**Author:** AthetosTrace · **Repo:** `AthetosTrace/fight-game`

---

## What to look at

```
assignment-05/
├── README.md            you are here
├── gap-scanner/         reads the design, scans the build, ranks what is missing
├── arena-pipeline/      generates the code for the top-ranked gap
├── agent/               the goal contract — hooks that gate start and finish
└── evidence/            the scan, the run logs, and the findings
```

Run the whole chain:

```bash
python -m pip install pytest

# 1-4. read the design, scan the build, find the gaps, rank them
python assignment-05/gap-scanner/gap_scan.py \
    --build-sequence build-sequence.md \
    --inventory assignment-05/gap-scanner/codebase-inventory.json

# 5. generate the arena, the gap it selected
python assignment-05/arena-pipeline/orchestrator.py --seed 8

# generate the code that builds it in Unreal
python assignment-05/arena-pipeline/materializer.py \
    assignment-05/evidence/runs/seed8/final_plan.json \
    --allow-proposed --out-dir assignment-05/evidence/runs/seed8/generated

# 96 tests
python -m pytest assignment-05/gap-scanner/tests assignment-05/arena-pipeline/tests -q
```

The scan defaults to a committed inventory so it runs anywhere. To scan the live
Unreal project instead, pass `--scan <path-to-unreal-repo>`.

---

## How the five requirements are met

| Requirement | Where | What it actually does |
|---|---|---|
| **Read the GDD** | `gap-scanner/gap_scan.py` → `parse_requirements()` | Parses `build-sequence.md` and extracts **63 build steps naming 178 assets** — the features and systems the design requires, as identifiers a program can check |
| **Scan the codebase** | `gap_scan.py` → `scan_codebase()` | Walks the Unreal project's `Content/` tree and finds **184 built assets**, skipping One-File-Per-Actor packages |
| **Detect gaps** | `gap_scan.py` → `detect_gaps()` | Diffs the two. **59 of 63 steps have something missing.** Output: [`evidence/gap-scan.md`](evidence/gap-scan.md) |
| **Prioritize** | `gap_scan.py` → ranking + `arena-pipeline/refiner.py` | Two rules, both described below |
| **Generate code** | `arena-pipeline/` | Produces a validated arena plan, then emits `build_level.py` — runnable code that built the level in Unreal |

### A note on "scan the codebase"

*Ascendant Impact* has **no source files.** It is a Blueprint-only Unreal project —
no `Source/` folder, no C++, no build. All logic lives in binary `.uasset` files
that cannot be read as text.

So the scanner reads the project the way this project can be read: by asset
inventory. It walks `Content/`, collects every `.uasset` and `.umap`, and skips
`__ExternalActors__` packages, whose generated hash names would drown the real
inventory. Where the design and the prototype disagree on a name, the difference
is declared in [`gap-scanner/scope.json`](gap-scanner/scope.json) **with a
reason** — the scanner will not guess that two similar names are the same asset.

The rule values the arena pipeline enforces came from the same project, measured
off the shipped Blueprints:

| Value | Read from |
|---|---|
| Combat clamp ±650 cm | `BP_VanguardDuelMover.ApplyConstraints` |
| Camera curve `clamp(450 + 0.8 × separation, 500, 1500)` | `BP_DuelCameraRig` |
| Jump apex ~180 cm | `JumpZVelocity` 820 / `GravityScale` 1.9 |
| Min axis separation 78 cm | Capsule radii 35 + 34, plus margin |

The validator reproduces the camera rig's real distance curve, so a plan that
passes will frame correctly in the actual rig rather than in a model of it.

---

## 1. What the agent built

**It built the arena** — a validated arena plan, and then the code that
constructs it as a real level in Unreal.

### The gap scanner — `gap-scanner/`

Parses the design, scans the build, diffs them, and ranks what is missing by
blocking step. Full output in [`evidence/gap-scan.md`](evidence/gap-scan.md).

### The arena pipeline — `arena-pipeline/`

```
attempt 1..3:
    generate (first attempt) or take the refined plan
    deterministic gate  -> violations? refine one field, retry
    evaluator           -> criteria failed?  refine one field, retry
    both clean          -> SUCCESS
```

Generator (seeded, reproducible) · deterministic validator R1–R8 · evaluator
(four weighted criteria, pass mark 70) · refiner (one field per attempt, with a
before/after diff) · circuit breaker (three attempts, or earlier on no progress)
· materializer (emits `build_level.py`).

Three runs are committed in `evidence/runs/`:

| Run | What it demonstrates |
|---|---|
| `seed8` | Clean pass, first attempt — its `generated/` folder holds the emitted `build_level.py` |
| `seed4` | Two refinements, then success — the refiner working |
| `seed2` | Three attempts used, faults remain — the circuit breaker stopping |

### The goal contract — `agent/`

Two hooks make the goal machine-checked rather than promised.
**`entry_gate.py`** fires on `PreToolUse` and refuses to start an agent whose
inputs are not on disk. **`exit_gate.py`** fires on `SubagentStop` and refuses to
let an agent finish until the artifact it promised actually exists.

These are goals rather than conventions because **the check runs outside the
agent** — a separate program reading the filesystem. An agent can be wrong about
whether it finished. The program reading the disk cannot.

---

## 2. Why the agent selected that feature

**Two ranking rules. Neither is a judgement call, and both are in code.**

### Which feature to build — the blocking-step rule

Every gap is ranked by **the lowest-numbered build step that cannot execute
until it is closed.** `build-sequence.md` holds 63 ordered editor steps and was
written *before* most of these questions were asked, which is what makes it a
fair referee — it cannot be bent to justify a convenient order.

The scan returns 59 open steps. The top of the ranking is **not** the arena:

| Rank | Step | Missing | Ours? |
|---|---|---|---|
| 1 | `M1-05` | `DA_TuningGlobals` | no |
| 2 | `M1-06` | `BP_PresentationSubsystem` | no |
| 3 | `M1-07` | `WBP_DebugPanel` | no |
| … | … | … | no |
| **17** | **`M1-21`** | **`L_ShatteredRing`** | **yes** |

**The arena was selected because it is the highest-ranked gap this side of the
project is allowed to build.** Everything above it — the player, the rival, the
combat components, the HUD — belongs to the gameplay owner under a work split
that exists so two people never edit the same binary Unreal asset.

Ownership is applied **after** ranking, never before, and the report always
prints the true top of the list. Filtering another owner's work out of the
*selection* is a boundary; hiding it from the *ranking* would make the tool lie
about what matters most. There is a test for exactly that.

The arena also ranked early for a concrete reason: **you cannot gray-box a floor
without dimensions.** Ranking it exposed a dependency chain — Attack D's travel
distance is defined as a fraction of the arena footprint, and the failed-Clash
separation has to fit inside it, so all three had to move together or disagree.

### Which correction to make — the smallest-correction rule

Inside a run, the refiner changes **exactly one field per attempt** and records a
before/after diff. It refuses rather than guesses when a fix is not ours. The
clearest case is R4, camera framing: the only real fix is retuning
`BP_DuelCameraRig`, which belongs to the gameplay owner, so the refiner
escalates. **That refusal is enforced in code, not documented as a convention.**

The same applies to undecided inputs. `design/group-04-spacing-and-arena.md`
opens with *"EVERY ANSWER IN THIS FILE IS PROPOSED, NOT DECIDED"*, so the
validator will not enforce a `PROPOSED` value as a requirement — it reports it
for human review and stops. The pipeline is built so it cannot invent a missing
gameplay requirement.

---

## 3. Were you able to run this in your game?

**Yes.**

The generated `build_level.py` was run against a live Unreal 5.8 editor session
over the `unreal-mcp` server. It created 12 actors and saved the level to
`/Game/ArenaTools/Maps/Lvl_ArenaGen_Seed8` — floor, ceiling, two end walls, two
side railings, four landmarks, two spawn markers.

The result was verified **in the engine** by ray-tracing the built geometry,
rather than by trusting the script's own output:

| Check | Measured in engine | Rule |
|---|---|---|
| Floor height across the combat span | Z = 0.0 at all 5 sample points | R3 — flat floor at Z = 0 |
| Nearest blocking geometry | 500.0 cm beyond the ±650 bound | R2 — clearance ≥ 500 cm |
| Headroom above centre | 515 cm | R7 — ≥ 388 cm for a jump-over |

### What building it revealed

Two defects survived the deterministic gate and were caught only once a level
existed. Both are written up in
[`evidence/ARENA_PIPELINE_FINDINGS.md`](evidence/ARENA_PIPELINE_FINDINGS.md).

1. **Clearance was measured to obstacle centres, not faces.** An obstacle 507.7 cm
   beyond the combat bound passed while its near face sat 482.7 cm out — legal on
   paper, illegal in the level.
2. **Landmarks were placed inside each other.** Two landmarks at the same end
   share a depth plane, and their lateral positions were sampled independently,
   so 300 cm boxes overlapped on 26 of 42 passing seeds.

Both were invisible to a validator reading a plan, because a plan is
dimensionless and a level is not.

### And a finding about the game itself

The pipeline surfaced a constraint nobody had multiplied out. The long axis is
2400 cm, the combat span 1300 cm, and environment geometry must keep 500 cm
clear:

```
1200 (half the long axis) − 650 (combat bound) − 500 (clearance) = 50 cm
```

**Fifty centimetres of depth at each end for all environment geometry.** End
features can be shallow wall relief but not free-standing objects. That suits the
landmarks already named — doorway frame, truss panel, mezzanine struts are all
wall-attached — so nothing is blocked, but it constrains environment art.

---

## Honest limits

- **The scanner checks that an asset exists, not that it is correct.** A gap
  closes when an asset of the right name is present. Whether its graph is right
  is a question for the inspector agent, not this scan.
- **The layout is not enforced, only the dimensions.** GDD page 11 fixes the
  doorway centred on the far short wall and Q24 specifies 250 cm corner
  chamfers; the generator randomises the doorway and ignores chamfers. Queued as
  candidate rules R9–R11, pending the designer's sign-off, because changing what
  the generator may produce is an arena-design decision.
- **The agent-judge evaluator backend is a seam, not built.** `--judge agent`
  stops for human review; the heuristic evaluator is what runs.
- **The generated level is not the shipping arena.** `design/group-08-assets.md`
  specifies the Shattered Ring as authored in-editor by the team. What the
  pipeline produces is a rules-legal test arena proving the constraints are
  satisfiable and buildable — not a replacement for authored environment art.
- **The Unreal project lives in a separate implementation repo** (Blueprints and
  maps are binary and LFS-tracked, and are split from this text-only design
  repo). The arena pipeline here is byte-identical to the working copy there;
  `gap-scanner/codebase-inventory.json` is the asset snapshot it scanned, so the
  scan reproduces without access to that repo.
