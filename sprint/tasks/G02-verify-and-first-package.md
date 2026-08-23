---
id: G02
track: G
title: Verify the migration, then attempt the first package
status: todo
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

- [ ] The duel plays in PIE from the a10 worktree — movement, punch, damage, strike, KO.
- [ ] Zero missing-asset or missing-reference errors in the Message Log.
- [ ] A packaging attempt has run to completion or to a definite failure, and the log is
      saved under `game/reports/packaging/`.
- [ ] The Log below records the actual outcome including every error, not a summary.

## Log

- 2026-08-23 — created. Migration verified as far as git can verify it: real byte sizes,
  zero unsmudged LFS pointers, `.uproject` present, 469 LFS objects round-tripped through
  GitHub. Engine-level verification is what this task is for. Structural risk is low —
  Unreal references are `/Game/`-relative and `/Game/` resolves to `<project>/Content/`,
  and the whole project root moved as one unit.
