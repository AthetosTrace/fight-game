---
id: G02
track: G
title: Verify the migration, then attempt the first package
status: done
assignment: 10
editor-required: true
depends-on: [G01]
---

## Goal

Prove the migrated project opens and plays, and find out what breaks when it is cooked —
while there is still a week to fix it.

## Why it matters

Everything to date has only ever run in PIE. Nothing has been proven in a cooked build,
and a broken playable link caps the **entire** assignment at 50%. This is the
highest-risk unknown in the project.

Do both in one sitting: cooking reuses the DerivedDataCache the editor builds, and the
worktree starts with none, so one shader compile serves both.

## Preconditions

- Nobody has an Unreal editor open on any copy of this project.
- Open **only** `fightgame-a10\game\AscendantImpact.uproject`. Never the copy sitting in
  the primary `FightGame` directory on `main`.

## Steps

1. Open the project. First open recompiles shaders from scratch — expect a long wait.
2. Open `Lvl_DuelGraybox` and PIE. Confirm: player moves and jumps, punch lands damage,
   Vanguard advances and strikes, both health bars respond, a knockout ragdolls.
3. Check the Message Log for load errors, missing references, and redirectors.
4. Set the default maps if unset (Project Settings, Maps and Modes). They almost certainly
   still point at the ThirdPerson template.
5. Attempt Platforms, Windows, Package Project — Shipping configuration.
6. Capture the full cook log whether it passes or fails. Save it under
   `game/reports/packaging/` with the date.

## Done when

- [x] The duel plays in PIE from the a10 worktree — movement, punch, damage, strike, KO.
- [x] Zero missing-asset or missing-reference errors in the Message Log.
- [x] A packaging attempt has run to completion or to a definite failure, and the log is
      saved under `game/reports/packaging/`.
- [x] The Log below records the actual outcome including every error, not a summary.

## Log

- 2026-08-23 — created. Migration verified as far as git can verify it: real byte sizes,
  zero unsmudged LFS pointers, `.uproject` present, 469 LFS objects round-tripped through
  GitHub. Engine-level verification is what this task is for. Structural risk is low —
  Unreal references are `/Game/`-relative and `/Game/` resolves to `<project>/Content/`,
  and the whole project root moved as one unit.

- 2026-08-25 — in progress. Working on `main` in the primary FightGame folder; the
  `fightgame-a10` worktree named in Steps no longer exists (removed 2026-08-24, its work
  merged), so "open only the a10 worktree" is stale — the main copy is the only copy, and
  it is the one the running editor has open.

- 2026-08-25 — **DONE. The project packages.** `game/Build/Shipping/Windows/AscendantImpact.exe`,
  647 MB archived, Win64 Shipping, IoStore + pak. It took three attempts and each failure was a
  different real defect. Whether it *launches* is `G03`; this task only had to reach a verdict.

  **PIE verification (steps 1–3).** All duel actors spawn in `Lvl_DuelGraybox` and initialise:
  `BP_VanguardDuelMover`, `BP_VanguardBasicAttackDriver`, `BP_DuelCameraRig`,
  `BP_DuelKnockoutCoordinator`, `BP_VanguardProxy`, HUD. `bDuelModeActive=true`. The Vanguard
  strike lands live — the idle player went 80 → 70 health across two MCP reads while the Vanguard
  sat at 100. Movement, punch damage and the KO ragdoll are separately evidenced by `Q02`'s three
  seeded live PIE runs (2026-08-24 21:21) against this same project copy.
  **Message Log: clean.** Five `Error:` lines in a 4,947-line editor log — two are the
  GameFeatureData pair below, two are the QA agent calling `get_current_level` during PIE, one is
  its duplicate. **Zero missing assets, zero missing references, zero redirectors.** Remaining
  warnings are all WASAPI audio-device noise (48 kHz engine vs 44.1 kHz device).

  **Step 4 — default maps were still the template, and two other things were wrong with them.**
  `EditorStartupMap` and `GameDefaultMap` both pointed at `/Game/ThirdPerson/Lvl_ThirdPerson`;
  both now point at `/Game/AscendantImpact/Maps/Lvl_DuelGraybox`. `GlobalDefaultGameMode` stays
  `BP_ThirdPersonGameMode` — that is what the graybox level actually spawns. Also fixed:
  `ProjectName` in `DefaultGame.ini` was literally `Third Person BP Game Template`, which is the
  window title of the shipped exe. Now `Ascendant Impact`.

  **Attempt 1 — FAILED, exit 6 (`OtherCompilationError`), in 2 seconds.**
  `2026-08-25-win64-shipping.log`.
  > `AscendantImpact.uproject has no code, but is being treated as a code-based project for`
  > `platforms Android, IOS, Linux, Mac, TVOS, Win64 because: GameplayStateTree plugin is enabled.`
  > `Platform Win64 is not a valid platform to build. SDK validation failed:`
  > `  Sdk: not found. Required version 10.0.19041.0.`

  This is the one worth remembering. **The project is not Blueprint-only for packaging purposes.**
  `GameplayStateTree` has a Runtime module that is not in the installed engine's prebuilt
  `UnrealGame` binaries, so enabling it silently reclassifies the project as code-based and forces
  a compile. **This machine has no C++ toolchain at all** — verified: no `vswhere`, no
  `Windows Kits\10\Include`, no `HKLM\...\Microsoft SDKs\Windows\v10.0` key. Installing Visual
  Studio would have cost most of a day out of seven.
  Instead: grepped all **433** `.uasset` files for StateTree references and found **zero**. The
  plugin was unused template baggage. Disabled it.

  **Also fixed while in there, and this one is a ship defect, not a build defect.**
  `ModelContextProtocol` declares two **Runtime** modules. Left alone it ships inside the build
  handed to strangers on itch.io — an MCP server plugin inside the game. `ModelContextProtocol`,
  `MCPClientToolset`, `AllToolsets`, `Terminal` and `ModelingToolsEditorMode` are now all
  `TargetAllowList: ["Editor"]`. **Verified in the archive: no MCP, Toolset or Terminal binary is
  present in the shipped build.** Editor targets are unaffected, so the live MCP session was never
  interrupted. Original saved at `game/AscendantImpact.uproject.bak`.

  **Attempt 2 — FAILED, exit 25 (`Error_UnknownCookFailure`), 3m 14s.**
  `2026-08-25-win64-shipping-attempt2.log`. The build step passed with no compiler, and **the cook
  itself completed** — `---- Finalisation: End ----`, `Done!`, 2m 54s — then the commandlet exited
  1 on the error summary:
  > `Failure - 2 error(s), 1 warning(s)`
  > `LogGameFeatures: Error: Asset manager settings do not include a rule for assets of type`
  > `GameFeatureData, which is required for game feature plugins to function`
  > `LoadErrors: Error: ... Add entry to PrimaryAssetTypesToScan?`

  Those two were the **only** errors in the entire cook — no missing assets, no broken references.
  Source: `AllToolsets` → `GameFeaturesToolset` → `GameFeatures`. The MCP toolchain transitively
  enables the GameFeatures plugin, which then demands an Asset Manager scan rule this project never
  had. **Restricting the toolsets to Editor targets does not dodge this, because the cook
  commandlet is itself an editor process.** It is the same error that has been sitting in the
  editor startup log at line 1736 all along — harmless in the editor, fatal to a cook.
  Fixed by adding `[/Script/Engine.AssetManagerSettings]` with the standard `GameFeatureData`
  `+PrimaryAssetTypesToScan` rule to `game/Config/DefaultGame.ini`, commented with the reason.

  **Attempt 3 — BUILD SUCCESSFUL, exit 0, 1m 1s.**
  `2026-08-25-win64-shipping-attempt3.log`. 2,473 UFS files staged, `UnrealPak` exit 0,
  `LogIoStore: Success`. Archive at `game/Build/Shipping/Windows/`:
  `AscendantImpact.exe` (172 KB launcher) + `AscendantImpact-Windows.ucas` (263 MB) +
  `.pak` (11 MB) + `.utoc`, `global.ucas`, `global.utoc`. Only `NNE` ships under
  `Engine/Plugins`. Total 647 MB — worth watching against itch.io limits in `G04`.

  **Carried into `G03`:** the exe has not been run. Shipping strips the console and most logging,
  so if it launches to a black screen, repackage as **Development** first to get a readable log —
  the toolchain-free path is proven now, so that is a one-minute rebuild, not a re-investigation.
  Note also that only maps reachable from `GameDefaultMap` were cooked; `Lvl_ArenaOctagon` is not
  referenced by anything yet and is **not in this build**. `G07` must add it to the cook set.
