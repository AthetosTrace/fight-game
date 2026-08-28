# Board

**Updated 2026-08-23.** Deadlines: A08 **25 Aug**, A09 **27 Aug**, A10 **1 Sept** (Adrian
believes 7 Sept — unconfirmed, plan to the 1st). Internal target: playable build live
**30 Aug**.

Statuses: `todo` · `in-progress` · `blocked` · `done`

---

## NEXT UP

| Track | Task | Why this one |
|---|---|---|
| **G — Game** | **`G05`** — match loop | `G16` and `G07` are both done bar checks that need something else first (see their rows). Adrian's ordering — organise the project, get the arena visible on open — is delivered. **`G05` is now the bottleneck for three separate things**: `G07`'s remaining boxes, `G06` balance, and `X7`. `G03` (run the packaged exe) is still a ten-minute job that can happen either side. |
| **N — Narrative** | — | **Track complete.** Delivered in `AthetosTrace/ascendant-dm`. |
| **Q — QA** | **`Q03`** — README + triage | `Q01` and `Q02` are done; three live runs found two S1 defect classes. |

---

## G — Game (Assignment 10)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| G01 | Scope lock — GDD cut addendum, reconcile stale docs | `done` | no | — |
| G02 | Verify migration + first package smoke test | `done` | yes | G01 |
| G16 | **Reorganize Content under one root** (18 asset moves) | `in-progress` | yes + MCP | — |
| G03 | Make the package actually launch | `todo` | yes | G02 |
| G04 | itch.io page + butler, upload the graybox build | `todo` | no | G03 |
| G05 | Match loop — intro, win, lose, restart | `todo` | yes | G02 |
| G06 | Balance — measure, then tune so the boss can win | `todo` | yes | G05 |
| G07 | Octagon swap — merge the arena into the duel level | `in-progress` | yes | G05 |
| G08 | Title and controls screen | `todo` | yes | G05 |
| G09 | Audio minimum — hit, whiff, KO, ambience | `todo` | yes | G05 |
| G12 | Attack data from the A06 pipeline — DataTable + driver reads rows | `todo` | yes | G05 |
| G13 | Vanguard attack B — close-range punish | `todo` | yes | G12 |
| G14 | Vanguard attack C — advancing anti-kite | `todo` | yes | G13 |
| G15 | Player block — defensive option (**first to cut**) | `todo` | yes | G13 |
| G10 | Ship candidate — package, upload, stranger test | `todo` | yes | G04, G06, G07, G08, G09 |
| G11 | A10 submission — audit and cost analysis | `todo` | no | G10, N01 |

**`G16` — all 18 moves done, committed and packaged. One line is open and it needs a
human, not an agent.** Seven of its eight acceptance checks passed: assets moved, zero
redirectors, config repointed, editor restarts clean, octagon geometry intact, repackage
`BUILD SUCCESSFUL`, committed. The eighth is a PIE pass. The Vanguard half is confirmed live
— it advances, strikes, drives the player 100 → 0 and the knockout coordinator fires — but
**player input could not be driven from an agent.** Under `PlayMode_InViewPort` the level
viewport has no node in the Slate accessibility tree, and under `PlayMode_InEditorFloating`
`PressKey` is swallowed by the window chrome. Every input asset reference is proven
repointed and the cook resolves all of them, so this is a verification gap, not a suspected
break. **Someone press W, Space and left-click once, then tick the box and mark `G16`
done.**

**`G07` — the octagon is merged into `Lvl_DuelGraybox` and the duel runs inside it.** Three
of its six acceptance lines are closed: the arena-size decision is recorded, the Vanguard's
per-instance overrides are confirmed live on the placed actor, and the default map needed **no
change at all** — which is exactly what reversing the merge direction bought. The level now
holds precisely the same 30 `ArenaOct_*` actors as `Lvl_ArenaOctagon`, diffed both ways. The
arena is in the cook automatically because it is inside the map `GameDefaultMap` already
points at.

**The other three lines are blocked on `G05`, not on `G07`.** There is no win/lose/restart, so
there is no "full match" to play start to finish; there is no `G05`/`G06` acceptance to
re-verify; and the collision sign-off is explicitly gated on `X7`, because after a knockout the
mover's tick stops and takes the arena clamp with it — invisible on a flat plane, but in the
octagon it means walking into the ramps and truss walls. **`G05` is now the single thing
holding three separate boxes.**

Still open inside `G07` and not blocked by anything: the **lighting pass**. The interior is
flat-lit, the gallery overhangs read as dark bands, and the template floor plane's corners
stick out past the octagon and read as a floating island. Asset dressing under D3, so it can
proceed whenever.

**Generator order is `arena` → `detail` → `tiers`.** Not arena → tiers → detail: `detail`
places the parapets with blocky step runs and `tiers` exists to replace them with wedge ramps,
so running tiers second leaves 16 stray `ArenaOct_ParapetStep_*` actors behind. Also,
`Lvl_DuelGraybox` came off `PROTECTED_LEVEL_NAMES` in all three scripts — the list began as
"levels owned by Anthony" and that rule is retired. `Lvl_ThirdPerson` stays protected.

**`bAutoStartServer` was turned on and then turned back off — do not re-enable it.** It
works, and the editor did come back with MCP listening. But the cook runs
`UnrealEditor-Cmd.exe -run=Cook`, which is an editor process and so loads the plugin too;
with auto-start on it tries to bind `127.0.0.1:8000`, the live editor already holds that
port, and that single bind failure fails the whole cook:

```
LogHttpListener: Error: HttpListener unable to bind to 127.0.0.1:8000
Failure - 1 error(s), 1 warning(s)
AutomationTool exiting with ExitCode=25 (Error_UnknownCookFailure)
```

Packaging with the editor open is the normal workflow here, and packaging is the gate that
caps the whole assignment if it breaks. So **Trap 1 stays a trap**: after opening the
project, type `ModelContextProtocol.StartServer` in the console.

**One Slate rule worth keeping**, learned the hard way in `G16`: call `SlateInspector` tools
as top-level `call_tool`, **never** from inside a `ProgrammaticToolset.execute_tool_script`
payload. Its observers walk their subtree on a ~100 ms game-thread tick, and a script payload
holds that thread, so `Snapshot` silently returns empty. `Q02`'s agent gets this right.

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
