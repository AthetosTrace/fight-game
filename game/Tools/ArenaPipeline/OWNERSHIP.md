# Ownership and asset boundaries

This folder is owned by the agentic-workflow side of the project (AthetosTrace).
It exists so arena work can proceed without ever touching a file the gameplay
owner (Anthony Travieso) is editing.

## What this folder may create

New files only, all plain text:

- `Tools/ArenaPipeline/**` — the pipeline itself
- `docs/arena/**` — contracts and specs
- `reports/arena/**` — per-run logs and reports
- the **new** `/Game/ArenaTools/` Content namespace and the **new** maps under it

## The materializer and the live editor

`materializer.py` is the only stage whose output reaches Unreal, and it does so
at arm's length: it writes a manifest and a build script, and never imports an
Unreal module or opens the editor itself. A human runs the emitted script
against a live session through unreal-mcp.

Everything it creates goes into `/Game/ArenaTools/Maps/`. The generated level is
seeded by duplicating `/Engine/Maps/Templates/Template_Default`, so no project
map is read, copied or modified — in particular not `Lvl_ThirdPerson` or
`Lvl_DuelGraybox`. A test asserts the emitted script contains no path under
`/Game/ThirdPerson`, `/Game/Variant_Combat` or `/Game/AscendantImpact`, so the
boundary is checked by CI rather than by memory.

Placed actors are stock `/Engine/BasicShapes/Cube` instances plus a `PlayerStart`
and a `TargetPoint`. Nothing is imported, no plugin is installed, and no
Blueprint is created or compiled.

## What this folder must never touch

Read freely. Write never.

| Category | Assets |
|---|---|
| Player | `BP_ThirdPersonCharacter`, `BP_ThirdPersonPlayerController` |
| Vanguard | `BP_VanguardProxy`, `BP_VanguardDuelMover`, `BP_VanguardBasicAttackDriver` |
| Camera | `BP_DuelCameraRig` |
| Combat / state | `BP_DuelKnockoutCoordinator` |
| HUD / health | `UI_DuelHUD`, `UI_LifeBar` |
| Animation | `ABP_Unarmed`, `ABP_VanguardLocomotion` |
| Maps | `Lvl_ThirdPerson`, `Lvl_DuelGraybox` |

Also forbidden: renaming or moving any existing asset, reorganizing `Content/`,
editing the main gameplay map, and overwriting any existing asset with a
generated version.

## Why it is enforced this way

`.uasset` and `.umap` are binary and Git-LFS-tracked. Git cannot merge two edits
to the same one — whoever pushes second loses work or hits an unresolvable
conflict. Every rule above exists to keep that from happening.

Note that `.gitattributes` in this repo LFS-tracks **only** `*.uasset` and
`*.umap`. Everything in this folder is `.py`, `.json`, or `.md`, so it is plain
text, diffs normally, and merges normally.

## If we need something in the gameplay area

Stop and ask first, stating what we want to build, which files it would touch,
and how it connects. The agreed options are: take ownership of that feature,
split it into separate assets, build an isolated child Blueprint, take turns, or
write a new shared plan. Preference order for us is **new component, child
Blueprint, interface, data asset, or test level** — never an edit in place.
