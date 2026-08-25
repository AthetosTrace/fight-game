# Board

**Updated 2026-08-23.** Deadlines: A08 **25 Aug**, A09 **27 Aug**, A10 **1 Sept** (Adrian
believes 7 Sept — unconfirmed, plan to the 1st). Internal target: playable build live
**30 Aug**.

Statuses: `todo` · `in-progress` · `blocked` · `done`

---

## NEXT UP

| Track | Task | Why this one |
|---|---|---|
| **G — Game** | **`G02`** — Verify migration + first package | `G01` is done. This is the highest-risk unknown left: nothing has ever been packaged. |
| **N — Narrative** | — | **Track complete.** Delivered in `AthetosTrace/ascendant-dm`. |
| **Q — QA** | **`Q03`** — README + triage | `Q01` and `Q02` are done; three live runs found two S1 defect classes. |

---

## G — Game (Assignment 10)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| G01 | Scope lock — GDD cut addendum, reconcile stale docs | `done` | no | — |
| G02 | Verify migration + first package smoke test | `todo` | yes | G01 |
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
| Q03 | README, and triage findings into G tasks | `todo` | no | Q02 |

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

All work happens in `C:\Users\athet\Documents\FightGame` on `main`. The `a7`, `a8` and
`a10` worktrees were removed 2026-08-24 after their work was merged.
`AscendantCapstone\fightgame-a9` is the last one standing and only until `Q03` merges.

## Blocked on a human, not on an agent

- **A10 due date** — 1 Sept or 7 Sept. Unconfirmed in writing.
- **Anthropic API key** — none on this machine at any scope. Blocks `N01`, and `G11`'s
  cost analysis needs real token counts. See `N01`.
- **Migration verification** — `G02`. Nobody has opened the migrated project yet.

## Critical path

`G01 → G02 → G03 → G04` retires the packaging risk, which is the only thing that can cap
the whole assignment at 50%. Everything in the `G05`–`G09` block is gameplay that can be
cut down if time runs short. **Do not reorder so that packaging is discovered last.**
