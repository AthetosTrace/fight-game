# Board

**Updated 2026-08-23.** Deadlines: A08 **25 Aug**, A09 **27 Aug**, A10 **1 Sept** (Adrian
believes 7 Sept — unconfirmed, plan to the 1st). Internal target: playable build live
**30 Aug**.

Statuses: `todo` · `in-progress` · `blocked` · `done`

---

## NEXT UP

| Track | Task | Why this one |
|---|---|---|
| **G — Game** | **`G03`** — Make the package launch | `G02` is done — **the project packages**, 647 MB Win64 Shipping, after three attempts and three real defects. The exe has not been run yet. |
| **N — Narrative** | — | **Track complete.** Delivered in `AthetosTrace/ascendant-dm`. |
| **Q — QA** | **`Q03`** — README + triage | `Q01` and `Q02` are done; three live runs found two S1 defect classes. |

---

## G — Game (Assignment 10)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| G01 | Scope lock — GDD cut addendum, reconcile stale docs | `done` | no | — |
| G02 | Verify migration + first package smoke test | `done` | yes | G01 |
| G03 | Make the package actually launch | `todo` | yes | G02 |
| G04 | itch.io page + butler, upload the graybox build | `todo` | no | G03 |
| G05 | Match loop — intro, win, lose, restart | `todo` | yes | G02 |
| G06 | Balance — measure, then tune so the boss can win | `todo` | yes | G05 |
| G07 | Octagon swap — move the duel into the real arena | `todo` | yes | G05 |
| G08 | Title and controls screen | `todo` | yes | G05 |
| G09 | Audio minimum — hit, whiff, KO, ambience | `todo` | yes | G05 |
| G12 | Attack data from the A06 pipeline — DataTable + driver reads rows | `todo` | yes | G05 |
| G13 | Vanguard attack B — close-range punish | `todo` | yes | G12 |
| G14 | Vanguard attack C — advancing anti-kite | `todo` | yes | G13 |
| G15 | Player block — defensive option (**first to cut**) | `todo` | yes | G13 |
| G10 | Ship candidate — package, upload, stranger test | `todo` | yes | G04, G06, G07, G08, G09 |
| G11 | A10 submission — audit and cost analysis | `todo` | no | G10, N01 |

### How we build, by purpose — not by preference

- **Gameplay logic → Blueprints, authored through the Unreal MCP.** Fifteen milestones
  already work this way. Rewriting them in Python buys nothing and costs the animation and
  montage integration.
- **Geometry and anything parameterised → Python payload scripts** run inside the editor
  via MCP `execute_tool`. That is how the octagon was built and it is repeatable and
  tunable.
- **Tuning values → CSV to DataTable.** `G12` is the switch. It is also the cheapest way to
  make attacks B and C a row plus a branch instead of another wall of floats.

Everything runs through MCP agents either way. The distinction is where a value lives, not
which language authored it.

### Packaging constraints — learned the hard way in `G02`, and they bind every later task

- **There is no C++ toolchain on this machine.** No Visual Studio, no Windows SDK. The project
  packages only because it is genuinely Blueprint-only and can use the engine's prebuilt
  `UnrealGame-Win64-Shipping.exe`. **Enabling any plugin with a Runtime module that is not
  precompiled in the installed engine silently reclassifies the project as code-based and breaks
  packaging outright.** `GameplayStateTree` did exactly this and is now disabled. Check before
  enabling anything.
- **Dev tooling is `TargetAllowList: ["Editor"]` and must stay that way.** `ModelContextProtocol`
  has Runtime modules and would otherwise ship an MCP server inside the public build.
- **Only maps reachable from `GameDefaultMap` are cooked.** `Lvl_ArenaOctagon` is not referenced
  by anything and is **not in the current build** — `G07` owns getting it into the cook set.
- **The build is 647 MB.** Check that against itch.io's limits in `G04` before uploading.

### Cut order if the schedule slips

`G09` audio → `G15` block → `G14` attack C. Cut whole tasks, never half-build one.
`G05` and the packaging chain `G02`–`G04` are not cuttable — they are the gate.

## N — Narrative (Assignment 08, due 25 Aug) — COMPLETE

Delivered as a standalone repo, **not** in `fight-game`:
`AthetosTrace/ascendant-dm`, checked out at `C:\Users\athet\Documents\ascendant-dm`.
Three commits, clean, pushed. Engine in `dm/`, tests, and three recorded transcripts —
`betrayal-run` (7 turns), `loyal-run`, `hand-run` — with per-turn ledger snapshots.

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| N01 | API key + shared cost-instrumentation helper | `done` | no | — |
| N02 | Narrative engine — ledger and reactive DM | `done` | no | N01 |
| N03 | 5+ turn run, evidence, README | `done` | no | N02 |

**`G11` still needs this track:** pull the real token counts from
`ascendant-dm/transcripts/*/run.json` for the A10 cost analysis. Do not re-estimate them.

## Q — Adversarial QA (Assignment 09, due 27 Aug)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| Q01 | Agent design and code | `done` | no | — |
| Q02 | Run against the build, produce the report | `done` | runs | Q01 |
| Q03 | README, and triage findings into G tasks | `done` | no | Q02 |

**TRACK CLOSED 2026-08-27.** Tagged `assignment-09-submission` at `e850938`, pushed.
Submission link: `github.com/AthetosTrace/fight-game/tree/assignment-09-submission/assignment-09`
The branch was merged into `main` and deleted locally and on the remote; the tag preserves
the exact submitted state. The `fightgame-a9` worktree is gone — **no worktrees remain.**

**Three live runs landed in `e850938`** — seeds 3, 7 and 21, under
`assignment-09/evidence/runs/`. Two defect classes, both `S1`:

- **X7 — post-KO constraint loss. Reproduces on all three seeds.**
  `BP_DuelKnockoutCoordinator.StopMover` disables the mover's tick, which stops
  `ApplyConstraints` with it, so the arena clamp and the 78 cm minimum separation both stop
  being enforced. Measured: player X 599.4, Vanguard KO'd at the bound X 650, separation
  **50.6 cm against a 69 cm capsule contact**. → **`G05` owns the fix. It also gates `G07`'s
  "nothing to get stuck on or escape through" criterion**, because in the octagon this means
  walking out of the combat strip into the gallery and truss walls.
- **B3 — capsule interpenetration** at `ApplyConstraints`, and a side-ownership break at
  `UpdateSideOwnership` on seeds 7 and 21.

---

## Day by day — 24 Aug to 1 Sept

There is **no slack** in this. Every day that slips comes out of the cut list, not the end.

| Day | Tasks | Note |
|---|---|---|
| **Mon 24** | `G02` | Open the editor, verify the migration, attempt the first package. Long unattended shader compile — start it before anything else. |
| **Tue 25** | `G03`, `G04` | Make the package launch, then get it onto itch.io. **The gate is retired at the end of this day or the plan is in trouble.** |
| **Wed 26** | `G05` | Match loop. Nothing else. It is the largest single gameplay task. |
| **Thu 27** | `G12`, `Q02`, `Q03` | Attack DataTable. A09 is due today — the QA runs happen against the match loop built yesterday. |
| **Fri 28** | `G13`, `G14` | Attacks B and C. The fight becomes a fight. |
| **Sat 29** | `G06`, `G15` | Balance to a 60–70% win rate. Block only if the fight needs it. |
| **Sun 30** | `G07`, `G10` | Octagon swap, then first ship candidate live. **Target: playable link up.** |
| **Mon 31** | `G08`, `G09`, re-ship | Title screen, audio, second upload. |
| **Tue 1** | `G11` | Submission and audit. Due 11:59 PM ET. |

The octagon swap sits late on purpose: keeping the ±650 combat clamps and centring them in
the arena means spacing does not change, so attacks and balance are arena-independent and
can be built first. If that decision is reversed, `G07` moves ahead of `G06`.

## Working directory — one folder

All work happens in `C:\Users\athet\Documents\FightGame` on `main`. **No worktrees remain** —
`a7`, `a8` and `a10` went on 2026-08-24, `a9` on 2026-08-27 when the Q track closed.
Do not create new ones.

## Blocked on a human, not on an agent

- **A10 due date** — 1 Sept or 7 Sept. Unconfirmed in writing.
- **Anthropic API key** — none on this machine at any scope. Blocks `N01`, and `G11`'s
  cost analysis needs real token counts. See `N01`.
- **Migration verification** — `G02`. Nobody has opened the migrated project yet.

## Critical path

`G01 → G02 → G03 → G04` retires the packaging risk, which is the only thing that can cap
the whole assignment at 50%. Everything in the `G05`–`G09` block is gameplay that can be
cut down if time runs short. **Do not reorder so that packaging is discovered last.**
