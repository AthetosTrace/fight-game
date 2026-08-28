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

- [ ] All 18 assets are at their new paths.
- [ ] **Zero ObjectRedirectors remain** under `/Game` — check the Content Browser filter.
- [ ] `GlobalDefaultGameMode` in `DefaultEngine.ini` points at the new GameMode path.
- [ ] Editor restarted clean: **zero** missing-asset or missing-reference errors in the
      Message Log.
- [ ] PIE in `Lvl_DuelGraybox` still works end to end — move, jump, punch lands damage,
      Vanguard advances and strikes, both health bars respond, KO ragdolls.
- [ ] `Lvl_ArenaOctagon` still opens and its geometry is intact — 43 actors, not an empty level.
- [ ] **Repackaged successfully.** The `G02` recipe is proven, so this is a rebuild, not an
      investigation. If it fails, the reorg broke something the editor did not report.
- [ ] Committed, with the `__ExternalActors__` moves visible in the diff.

## Log

- 2026-08-27 — created. Inventory taken from the live tree: 30 non-template assets, of which
  18 move. Config grep done — `GlobalDefaultGameMode` is the only `.ini` path that breaks.

- 2026-08-27 — started. Preconditions all four verified live in the editor: tree clean at
  `f98aca0`, editor open on `/Game/AscendantImpact/Maps/Lvl_DuelGraybox`, MCP listening on
  8000, PIE not running. All 18 source assets resolve; no destination path is occupied.
