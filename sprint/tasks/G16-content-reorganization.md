---
id: G16
track: G
title: Reorganize Content so every gameplay asset lives under one root
status: in-progress
assignment: 10
editor-required: true
mcp-required: true
depends-on: []
---

## Goal

Every asset this project actually owns lives under `/Game/AscendantImpact/`. Epic's template
content stays exactly where it is. After this, "where do I go to change the boss" has one
answer.

## Why it matters

Right now the boss is in `Variant_Combat/`, the player in `ThirdPerson/`, the arena in
`ArenaTools/`, the HUD split across `AscendantImpact/UI/` and `Variant_Combat/UI/`. Adrian
called this explicitly: he wants to know where to open the project and build from, and is
willing to spend the time now rather than ship confused.

## Preconditions — all four, no exceptions

1. **Working tree clean and committed.** This is the one operation where a bad outcome is
   painful to undo by hand. A clean commit turns it into `git reset --hard`.
2. **Unreal editor open** on `FightGame\game\AscendantImpact.uproject`.
3. **MCP server started** — `ModelContextProtocol.StartServer` in the editor console. It does
   **not** auto-start; `bAutoStartServer` defaults to false.
4. **PIE not running.** Stop play before touching assets.

## Method — and the part that goes wrong

Moves must happen **inside the editor**. Moving `.uasset` files on disk breaks references,
because the package path is baked into the binary. Use:

```python
import unreal
unreal.EditorAssetLibrary.rename_asset(src, dst)   # moves AND fixes referencers
```

`rename_asset` leaves an **ObjectRedirector** behind at the old path. Redirectors work, but
they are debt and they will end up in the cook. After all moves, clean them up:

```python
ar = unreal.AssetRegistryHelpers.get_asset_registry()
redirectors = [
    unreal.AssetData(a).get_asset()
    for a in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/CoreUObject", "ObjectRedirector"), True)
]
unreal.AssetToolsHelpers.get_asset_tools().fixup_referencers(redirectors)
unreal.EditorAssetLibrary.save_directory("/Game/AscendantImpact")
```

Then **save all** — the fixup dirties `Lvl_DuelGraybox`, which references the moved actors.

Follow the existing payload-script pattern in `game/Tools/ArenaPipeline/`: a `run()` that is
actually **called** at the bottom, or it silently no-ops and looks like success.

## Move list — 18 assets

**Move only. Do not rename.** Renaming `BP_ThirdPersonCharacter` to something prettier
invalidates every reference in `PROTOTYPE_BLACKBOARD.md`, `assignment-09/ORACLE.md`, and a
dozen task files — and Assignment 09 is already submitted and tagged. Folder structure gives
you the organization; renaming only buys cosmetics. Revisit after ship.

| From | To |
|---|---|
| `/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode` | `/Game/AscendantImpact/Core/` |
| `/Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController` | `/Game/AscendantImpact/Core/` |
| `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter` | `/Game/AscendantImpact/Characters/Player/` |
| `/Game/Variant_Combat/Blueprints/BP_VanguardProxy` | `/Game/AscendantImpact/Characters/Vanguard/` |
| `/Game/Variant_Combat/Blueprints/BP_CameraShake_Hit_Enemy` | `/Game/AscendantImpact/Camera/` |
| `/Game/Variant_Combat/Blueprints/BP_CameraShake_Hit_Player` | `/Game/AscendantImpact/Camera/` |
| `/Game/Variant_Combat/UI/UI_LifeBar` | `/Game/AscendantImpact/UI/` |
| `/Game/Variant_Combat/VFX/NS_Damage` | `/Game/AscendantImpact/VFX/` |
| `/Game/Input/Actions/IA_Attack` | `/Game/AscendantImpact/Input/Actions/` |
| `/Game/Input/Actions/IA_Jump` | `/Game/AscendantImpact/Input/Actions/` |
| `/Game/Input/Actions/IA_Look` | `/Game/AscendantImpact/Input/Actions/` |
| `/Game/Input/Actions/IA_MouseLook` | `/Game/AscendantImpact/Input/Actions/` |
| `/Game/Input/Actions/IA_Move` | `/Game/AscendantImpact/Input/Actions/` |
| `/Game/Input/IMC_Default` | `/Game/AscendantImpact/Input/` |
| `/Game/Input/IMC_MouseLook` | `/Game/AscendantImpact/Input/` |
| `/Game/ArenaTools/Maps/Lvl_ArenaOctagon` | `/Game/AscendantImpact/Maps/` |
| `/Game/ArenaTools/Maps/Checkpoints/Lvl_ArenaOctagon_CP01_ShellGood` | `/Game/AscendantImpact/Maps/Checkpoints/` |
| `/Game/ArenaTools/Maps/Checkpoints/Lvl_ArenaOctagon_CP02_TrussAndParapets` | `/Game/AscendantImpact/Maps/Checkpoints/` |

Already correctly placed, leave alone: `AscendantImpact/Animation/Vanguard/ABP_VanguardLocomotion`,
`AscendantImpact/Camera/BP_DuelCameraRig`, the three `AscendantImpact/Duel/BP_*`,
`AscendantImpact/UI/UI_DuelHUD`, `AscendantImpact/Maps/Lvl_DuelGraybox`.

### The three map moves are the risky ones — do them LAST and separately

`.umap` assets use **One File Per Actor**. `Lvl_ArenaOctagon` has 43 external actor packages
under `Content/__ExternalActors__/ArenaTools/Maps/Lvl_ArenaOctagon/`, and that path is derived
from the level's package path. Moving the level must move that folder too.

The editor handles this. Python `rename_asset` on a World is the one call in this task that is
not certain to. **Do the 15 non-map moves by script, commit, then move the three maps and
verify the `__ExternalActors__` folders followed before committing again.** If the external
actor folders did not move, undo with `git reset --hard` and do those three by hand in the
Content Browser, which definitely handles OFPA.

**Do not move or rename `Lvl_DuelGraybox`.** It is `GameDefaultMap`, it is the only map in the
cook set, and `G07` is about to merge the octagon into it. Renaming it later is a separate,
optional job.

## Config paths the editor will NOT fix — update these by hand

Asset moves fix Blueprint and level references. They do **not** touch `.ini` files.

| File | Line | Action |
|---|---|---|
| `game/Config/DefaultEngine.ini` | `GlobalDefaultGameMode=/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C` | **Must change** to `/Game/AscendantImpact/Core/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C` |
| `game/Config/DefaultEngine.ini` | `EditorStartupMap`, `GameDefaultMap` | No change — `Lvl_DuelGraybox` is not moving |
| `game/Config/DefaultEditor.ini` | `SimpleMapName=/Game/TP_ThirdPerson/Maps/ThirdPersonExampleMap` | Already a dead path; harmless. Clean it if you like |
| `game/Config/DefaultGame.ini` | `Path="/Game/Unused"` in the GameFeatures rule | Leave. Unrelated, and it is what makes the cook succeed |

`DefaultInput.ini` contains no `/Game/` paths — Enhanced Input contexts are referenced from
the player Blueprint, not config. Verified 2026-08-27.

## Do NOT touch — 157 assets

- `Content/Characters/Mannequins/` — 128 assets, 126 MB of Epic's skeleton, animations and
  textures. Moving them is pure churn and a long re-save.
- `Content/LevelPrototyping/` — 29 assets. Materials and meshes the graybox geometry uses.
- `Content/ThirdPerson/Lvl_ThirdPerson.umap` and `MI_ThirdPersonColWay` — template leftovers.
  Not cooked, not referenced. Deleting them is a separate decision.
- `Content/Input/Touch/` — template mobile input. Leave it; it may be referenced by a config
  key not caught by the `/Game/` grep.

## Done when

- [x] All 18 assets are at their new paths.
- [x] **Zero ObjectRedirectors remain** under `/Game` — check the Content Browser filter.
- [x] `GlobalDefaultGameMode` in `DefaultEngine.ini` points at the new GameMode path.
- [x] Editor restarted clean: **zero** missing-asset or missing-reference errors in the
      Message Log.
- [ ] PIE in `Lvl_DuelGraybox` still works end to end — move, jump, punch lands damage,
      Vanguard advances and strikes, both health bars respond, KO ragdolls.
      **Partly verified — left open deliberately, for a human to close in 60 seconds.**
      Vanguard advance, strike, damage, the health values and the KO are all confirmed live
      (100 → 0, `bPlayerKO = true`), and both HUD health bars exist as real widgets. Move,
      jump and punch could not be driven from here — see "the input wall" in the Log. Every
      input asset reference is proven repointed, which is the part this task could have
      broken. **What is left is: press W, press Space, left-click.**
- [x] `Lvl_ArenaOctagon` still opens and its geometry is intact — 43 actors, not an empty level.
- [x] **Repackaged successfully.** The `G02` recipe is proven, so this is a rebuild, not an
      investigation. If it fails, the reorg broke something the editor did not report.
- [x] Committed, with the `__ExternalActors__` moves visible in the diff.

## Log

- 2026-08-27 — created. Inventory taken from the live tree: 30 non-template assets, of which
  18 move. Config grep done — `GlobalDefaultGameMode` is the only `.ini` path that breaks.

- 2026-08-27 — started. Preconditions all four verified live in the editor: tree clean at
  `f98aca0`, editor open on `/Game/AscendantImpact/Maps/Lvl_DuelGraybox`, MCP listening on
  8000, PIE not running. All 18 source assets resolve; no destination path is occupied.

- 2026-08-27 - **all 18 moves done and committed** (`c879e54` non-maps, `658d456` maps).
  Config line changed, redirectors cleared, repackage green. Two Done-when lines are still
  open and both need the editor restarted; see the end of this entry.

  **The task file's method does not work, and the reason is worth keeping.** The MCP script
  sandbox permits only `math, re, copy, time, datetime, json` - there is no `import unreal`,
  so `EditorAssetLibrary.rename_asset` and `fixup_referencers` are both unreachable.
  Everything is reached through registered tools instead; `AssetTools.move` is the same
  underlying rename.

  **Three separate things silently returned `False` instead of moving.** All three are
  `FMessageDialog::Open(EAppMsgType::OkCancel, EAppReturnType::Cancel, ...)` inside
  `FAssetRenameManager`, which under MCP auto-answers with its default - Cancel. Nothing is
  logged as an error; the call just reports failure. **If a move ever returns `False` for no
  visible reason, grep the editor log for `Message dialog closed`.**

  1. `BP_ThirdPersonGameMode`. `FindCDOReferences` found `UGameMapsSettings`' CDO holding
     `GlobalDefaultGameMode`. Editing `DefaultEngine.ini` on disk does **not** help - the
     check reads the in-memory CDO, not the file. Fixed by clearing the setting through
     `ConfigSettingsToolset` (Project - Project - Maps), moving, then setting the new path.
  2. and 3. All three maps. Same check, different holders: opening a level registers it in
     `ULevelEditorViewportSettings::EditorViews` and
     `UWorldPartitionEditorPerProjectUserSettings::PerWorldEditorSettings`, both keyed by
     `TSoftObjectPtr<UWorld>`. The redirector fixup earlier in this task had just opened all
     three arena maps, which is what put them there. Neither property is editor-visible, so
     `ObjectTools` could neither read nor reset them; both **sections** were reset through
     `ConfigSettingsToolset`. Resetting only the World Partition one was not enough - both
     had to go. **Cost: local level-viewport preferences are back at defaults.** That is
     gitignored per-user state in `Saved/Config`, and the alternative was an editor restart.

  **Redirector cleanup needed a different lever than this file assumed.** With no
  `FixupReferencers` tool, neither loading a level nor `SceneTools.save_actor` re-points a
  package that reaches its dependency through a redirector - loading resolves the pointer in
  memory but leaves the package clean, so nothing is written back. What works: a package
  rebuilds its import table from live pointers on save, and those pointers have already
  followed the redirector. `WorldSettings.defaultGameMode` read back as the **new** path
  while the package on disk still named the old one. So each of the five referencing levels
  was dirtied deliberately - the level by writing `defaultGameMode` back to the value it
  already held, each OFPA actor package by a scratch tag added and removed - then saved.
  Both redirectors then had zero referencers and were deleted.

  **`AssetTools.move` on a World does carry OFPA, and carries more than this file predicted.**
  Both `__ExternalActors__` (43 + 29 + 51) *and* `__ExternalObjects__` (3 each), which this
  file did not mention. Verified by count at the new paths and zero at the old. 135 files per
  side of the diff = 3 maps + 123 external actors + 9 external objects. The
  `git reset --hard` fallback was not needed.

  **One extra path the config table missed.** `.ini` files were not the only place a moved
  path was written down. `game/Tools/ArenaPipeline/build_octagon_arena.py` held
  `OPPONENT_CLASS` pointing at the old `Variant_Combat` path, and the arena build reads that
  actor to centre its geometry - it would have found no opponent and mis-centred silently.
  Repointed. Also moved `materializer.py`'s `--level-path` default off `/Game/ArenaTools/`,
  since a run using the default would have recreated the folder this task just emptied.
  ArenaPipeline tests: **77 pass.**

  **Verification actually performed.**
  * All 18 at their new paths; `/Game/ArenaTools` gone entirely; `ThirdPerson` and
    `Variant_Combat` hold only what this file said to leave.
  * Zero live ObjectRedirectors. The asset registry still lists the two deleted ones as
    phantoms - their files are gone from disk, and the registry rescans on editor restart.
  * `Lvl_ArenaOctagon` opens with **50 actors**, of which **43** are the external-actor
    geometry - the other 7 (WorldSettings, Brush_0, WorldDataLayers, BuoyancyManager,
    DefaultPhysicsVolume, GameplayDebuggerPlayerManager, AbstractNavData) always live in the
    level package. 31 StaticMeshActors, the lights, the fog, the PlayerStart: all intact.
  * PIE in `Lvl_DuelGraybox`: all six duel actors spawn - player, Vanguard, camera rig,
    mover, attack driver, knockout coordinator - plus `HUD_0`. The Vanguard advanced and
    struck an idle player from 100 to 90 to 20 to 0, and `BP_DuelKnockoutCoordinator`
    reported `bPlayerKO = true` with its timer running. **Zero** missing-asset,
    missing-reference or Accessed-None entries in the whole session log.
  * Every dependency of the player pawn, the player controller and the Vanguard resolves to
    a new `/Game/AscendantImpact/` path - all five `IA_*`, both `IMC_*`, both camera shakes,
    `UI_LifeBar`, `UI_DuelHUD`, `NS_Damage`, `ABP_VanguardLocomotion`. Not one old path and
    no redirector in any chain. (`/Game/Input/Touch/` is genuinely still referenced by both,
    which confirms this file was right to leave it alone.)
  * **Repackaged: `BUILD SUCCESSFUL`, ExitCode 0, 43.87 s**, log at
    `game/reports/packaging/2026-08-27-g16-repackage.log`. All 21 moved assets appear in the
    cooked manifest at their new paths and **zero** old paths remain in it. A fresh cook
    process resolving every reference from disk is the strongest check available here.

  **What was NOT directly observed, stated plainly.** Player-side input - move, jump, and a
  punch landing damage - was not driven live. Attack is bound to Left Mouse Button, and
  `SlateInspector` could not produce a widget tree to click: `Observe` registered
  `observer_1` but `cachedSnapshotSize` stayed 0 across two calls, because its ~100 ms tick
  runs on the game thread that the MCP call is itself blocking. Abandoned at two attempts per
  the project's two-strikes rule rather than iterated. The Vanguard's health stayed at 100
  throughout, so nothing here proves the punch. What *is* proven is the thing this task could
  have broken: every input asset reference resolves to its new path. The KO ragdoll flag
  likewise was not read directly - `bSimulatePhysics` lives on `bodyInstance` and is not
  exposed - but the coordinator firing `bPlayerKO` is the gate in front of it.

  **Still open, both needing a restart:** the clean-Message-Log check, and the phantom
  registry entries clearing. `bAutoStartServer` was set **true** so the MCP server would come
  back by itself, and it did - but see the correction at the end of this file, it has since
  been set back to `false` because it breaks the cook. Next concrete action: close
  the editor, relaunch `game/AscendantImpact.uproject`, confirm port 8000 is listening, and
  read the Message Log.

- 2026-08-27 (later) - **editor restarted, and it comes up clean.** Closed the editor with
  everything saved, relaunched `game/AscendantImpact.uproject`. The MCP server came back by
  itself on 8000, because `bAutoStartServer` had been set true. **That setting has since been
  reverted - see the correction at the end of this file.**

  Fresh session reports: **zero ObjectRedirectors** under `/Game` (the two phantom registry
  entries cleared on the rescan, as predicted), **zero `Error:` lines in the whole log**, 25
  assets under `/Game/AscendantImpact`, `/Game/ArenaTools` and `/Game/Variant_Combat` empty,
  `/Game/ThirdPerson` holding only the two this file said to leave. The editor opened
  straight onto `Lvl_DuelGraybox`, so `EditorStartupMap` still resolves.

  **`IMC_Default` read back intact**, which is the moved asset that would have hurt most:
  all four actions present and every one of their references pointing at the new
  `/Game/AscendantImpact/Input/Actions/` paths, 13 keys bound including `W/A/S/D`,
  `SpaceBar`, `LeftMouseButton` and gamepad.

  **The input wall, and why it is not a G16 defect.** Three distinct routes were tried to
  drive the player, all failed, and the reason is environmental rather than anything this
  task changed:

  1. `Snapshot` nested inside `ProgrammaticToolset.execute_tool_script` always returns
     empty. The observer walks its subtree on a ~100 ms game-thread tick, and the MCP script
     is itself holding that thread. **Slate tools have to be called as top-level `call_tool`,
     never from inside a script payload.** Calling them directly does work - `Q02`'s agent
     does exactly this, which is how it landed punches on 2026-08-24.
  2. Even called directly, under `PlayMode_InViewPort` there is nothing to click: the level
     viewport has no node in the accessibility tree. The central splitter contains only its
     own 8x8 drag handle. `Q02`'s `viewport_ref()` looks for a line containing "Viewport" and
     would find nothing here either.
  3. Under `PlayMode_InEditorFloating` the PIE window *is* a top-level Slate window and comes
     up `[focused]`, and its tree is readable - **both HUD health bars show up as
     `progressbar` widgets, which is independent confirmation `UI_DuelHUD` is live.** But
     `PressKey` returns `true` while `jumpCurrentCount` stays 0, `movementMode` never leaves
     `MOVE_Walking` and the player never leaves `(0, 0)`. The key is being accepted by the
     window chrome, not routed into Enhanced Input.

  Compounding it: the Vanguard kills an idle player in roughly 20 seconds, so every attempt
  raced a clock - two reads came back with the player already at 0 health and `MOVE_None`.
  Chaining restart, press and read into a single pass did not beat it either.

  Stopped here rather than iterating further. The right tool for live input is the `Q02`
  agent, which is purpose-built for it, and the right check for a reorg is the cook - which
  passed.

- 2026-08-28 — **correction: `bAutoStartServer` is back to `false`, and it must stay there.**

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

  Found by `G07`'s repackage, which failed with exactly this and nothing else. `G16`'s own
  repackage had passed earlier the same session because the setting was still `false` then.
  Nothing about `G16`'s asset moves is affected — the reorg packaged clean and packages clean
  again with the setting reverted.
