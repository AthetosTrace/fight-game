# Handoff — 2026-08-28

The current briefing. Read `README.md` for the protocol and `BOARD.md` for the task list;
this file is the "start here right now" note. Rewrite it when the situation changes.

**Previous version, dated 2026-08-27, briefed `G16` then `G07`. Both are done** — each with
one or more acceptance lines left open for a reason that is written down. What follows is the
state they left behind.

---

## Starting a session that can do this work

1. **Open the project** — `C:\Users\athet\Documents\FightGame\game\AscendantImpact.uproject`
2. **Start the MCP server** in the editor console:
   ```
   ModelContextProtocol.StartServer
   ```
   **This step is still needed. Do not "fix" it by enabling `bAutoStartServer`** — that was
   tried on 2026-08-27 and it breaks packaging. See "The one trap that got worse" below.
3. **Then** open the session — MCP servers attach at session start, so a session opened
   before port 8000 is listening will not see the tools.
   ```
   cd C:\Users\athet\Documents\FightGame
   claude
   ```
4. **Commit before starting** anything that moves or deletes assets.

---

## What just landed

### `G16` — every asset this project owns is under one root

`/Game/AscendantImpact/` holds all 25 of them. The boss is in `Characters/Vanguard/`, the
player in `Characters/Player/`, the GameMode and controller in `Core/`, the whole Enhanced
Input set in `Input/`, both arena checkpoint maps in `Maps/Checkpoints/`. `ArenaTools` and
`Variant_Combat` are gone entirely. Epic's 157 template files stayed put, and so did
`Content/Input/Touch/` — which turned out to be genuinely referenced by both the player pawn
and the controller, so leaving it alone was right.

Zero ObjectRedirectors. `GlobalDefaultGameMode` repointed. Editor restarts clean with zero
`Error:` lines. Repackaged green.

**One line is open and it needs a human, not an agent:** a PIE pass driving the player. The
Vanguard half is proven live — it advances, strikes, drives the player 100 → 0, the knockout
coordinator fires — but agent-driven input does not reach the game (see below). Every input
asset reference is proven repointed and the cook resolves all of them, so this is a
verification gap rather than a suspected break. **Press W, press Space, left-click once, then
tick the box and mark `G16` done.**

### `G07` — the octagon is in the duel level

`Lvl_DuelGraybox` now holds exactly the same 30 `ArenaOct_*` actors as `Lvl_ArenaOctagon`,
diffed both ways with nothing on either side. Open the project and the arena is simply there.
Because the geometry moved into the map `GameDefaultMap` already points at, **the arena is in
the cook with no packaging config change at all** — which is the entire argument for having
reversed the merge direction, and it held.

Screenshots and the numbers the build reported are in
[`game/reports/arena/2026-08-28-merged-into-duel/`](../game/reports/arena/2026-08-28-merged-into-duel/).

**Arena size, the U1 decision, now recorded:** keep the fighter clamp at **±650** and centre
the octagon on it. No authored number was changed — that is what the generators do
unmodified. They read the live level and chose the fighter clamp centre `(0,0,0)` over the
spawn midpoint, and grew `centre_to_face` to 1590 cm by the authored camera-containment rule.

---

## The three things worth knowing before you touch anything

### 1. Generator order is `arena` → `detail` → `tiers`

Not arena → tiers → detail. `build_octagon_detail.py` places the parapets **with** blocky step
runs, and `build_octagon_tiers.py` exists to delete those and replace them with wedge ramps.
Run tiers second and it finds nothing to remove, then detail puts 16
`ArenaOct_ParapetStep_*` actors back. The checkpoint names `CP01_ShellGood` and
`CP02_TrussAndParapets` hint at the order; now it is written down.

`Lvl_DuelGraybox` also came off `PROTECTED_LEVEL_NAMES` in all three scripts. That list began
as "levels owned by Anthony" and the rule is retired. `Lvl_ThirdPerson` stays protected.

### 2. The one trap that got worse

`bAutoStartServer` **works** — set it true and the editor comes back with MCP already
listening. **It also breaks packaging.** The cook runs `UnrealEditor-Cmd.exe -run=Cook`, which
is an editor process and loads the plugin too; it tries to bind `127.0.0.1:8000`, the live
editor already holds that port, and that single bind failure fails the entire cook:

```
LogHttpListener: Error: HttpListener unable to bind to 127.0.0.1:8000
Failure - 1 error(s), 1 warning(s)
AutomationTool exiting with ExitCode=25 (Error_UnknownCookFailure)
```

Packaging with the editor open is the normal workflow here, and packaging is the gate that
caps the whole assignment if it breaks. It is back to `false`. **Type the console command.**

### 3. Two MCP rules that cost hours

- **Call `SlateInspector` tools as top-level `call_tool`, never from inside a
  `ProgrammaticToolset.execute_tool_script` payload.** Its observers walk their subtree on a
  ~100 ms game-thread tick, and a script payload holds that thread, so `Snapshot` silently
  returns an empty string. `Q02`'s agent gets this right.
- **A move that returns `False` for no visible reason is a suppressed modal.** Under MCP,
  `FMessageDialog::Open(..., EAppReturnType::Cancel, ...)` auto-answers with its default,
  which is Cancel, and logs nothing as an error. Grep the editor log for
  `Message dialog closed`. `FAssetRenameManager::FindCDOReferences` is the usual culprit: it
  serialises **every CDO** looking for soft references, so anything holding a
  `TSoftObjectPtr` to your asset blocks the rename. In `G16` that was
  `UGameMapsSettings::GlobalDefaultGameMode`, then
  `ULevelEditorViewportSettings::EditorViews` and
  `UWorldPartitionEditorPerProjectUserSettings::PerWorldEditorSettings` — the last two get
  populated just by **opening a level**. Editing the `.ini` does not help; the check reads the
  in-memory CDO. Clear it through `ConfigSettingsToolset`.

Also: agent-driven **player input does not currently work**. Three routes were tried.
`PlayMode_InViewPort` exposes no viewport node in the Slate tree to click;
`PlayMode_InEditorFloating` gives a focused window whose chrome swallows `PressKey`
(`jumpCurrentCount` stays 0 and the player never leaves `(0,0)`). The `Q02` agent is the
purpose-built tool for live input — use it rather than re-deriving this.

---

## `G05` is now the bottleneck, and it is holding three separate things

Not one. Do this next.

| Waiting on `G05` | Why |
|---|---|
| `G07`'s "full match plays start to finish" | There is no win/lose/restart, so there is no match to play through. |
| `G07`'s collision sign-off | Gated on **`X7`**: after a knockout the mover's tick stops and takes `ApplyConstraints` with it, so the arena clamp stops being enforced. Invisible on a flat plane. In the octagon it means a player who just won walks into the ramps and truss walls. |
| `G06` balance | Needs a match that can be won or lost before anything can be tuned. |

## Order after that

| Step | Task | Why |
|---|---|---|
| 1 | `G05` | Win / lose / restart. Also closes `X7`. Unblocks three things. |
| 2 | `G03` | Run the packaged exe — built many times now, never launched. Ten minutes. |
| 3 | `G12` → `G13` → `G14` | Attack DataTable, attack B, the anti-kite attack. |
| 4 | `G06` | Balance. Needs all three attacks first. |
| 5 | `G04`, `G08`, `G09`, `G10`, `G11` | itch.io, title, audio, ship, submission. |

Not blocked by anything and cuttable at any point: **`G07`'s lighting pass**. The arena
interior is flat-lit, the gallery overhangs read as dark bands, and the template floor plane's
±2000 corners stick out past the 3180 cm octagon and read as a floating island. Asset dressing
under D3, so it can happen whenever someone wants the screenshots to look better.

Adrian's four named problems still map straight onto this: **can't win or lose** is `G05`,
**backing up wins every time** is `G14`, **only one NPC attack** is `G12`–`G14`.

---

## Where everything lives

- **One repo, one folder.** `C:\Users\athet\Documents\FightGame`, branch `main`. No worktrees.
- **The game** — `game/`, with `game/AscendantImpact.uproject` the only copy.
- **Checkpoints** — `/Game/AscendantImpact/Maps/Checkpoints/` now holds three:
  `Lvl_ArenaOctagon_CP01_ShellGood`, `Lvl_ArenaOctagon_CP02_TrussAndParapets` and
  `Lvl_DuelGraybox_CP01_PreOctagon`, the last taken immediately before the merge.
- **`Lvl_ArenaOctagon` is now a reference level, not the shipping one.** It is unreferenced
  and not cooked, which is correct — its geometry lives in `Lvl_DuelGraybox`.
- **Assignment 08** lives outside this repo by design — `AthetosTrace/ascendant-dm`. Its
  `transcripts/*/run.json` files hold the only real token counts, which `G11` needs.
- **Assignment 09** is submitted, tagged `assignment-09-submission`, branch deleted.
