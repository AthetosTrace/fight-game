# CLAUDE.md — inside the Unreal project

**Rewritten 2026-09-02.** The previous version described a two-repository split, pointed
at another machine's file paths, and stated the default map was `Lvl_ThirdPerson`. All
three were wrong. One repo, one folder, and the default map is `Lvl_DuelGraybox`.

**The plan is `../FINISH-PLAN.md`. The operating rules are `AGENTS.md` and `../CLAUDE.md`.**

## What this is

`AscendantImpact.uproject`, Unreal Engine **5.8**, **Blueprint-only** — no `Source/`, no
C++ build, no lint or test commands. Everything lives in binary `.uasset`/`.umap` files
under `Content/`. All editing happens through the **unreal-mcp** server against a live
editor session.

## Where the assets are

Every asset this project owns is under **`/Game/AscendantImpact/`** — 26 of them.

| Path | Contents |
|---|---|
| `Characters/Player/` | `BP_ThirdPersonCharacter` (Quinn mesh) |
| `Characters/Vanguard/` | `BP_VanguardProxy` (Manny mesh, 1.1 uniform scale) |
| `Core/` | `BP_ThirdPersonGameMode`, `BP_ThirdPersonPlayerController` |
| `Duel/` | `BP_DuelKnockoutCoordinator`, `BP_VanguardBasicAttackDriver`, `BP_VanguardDuelMover` |
| `Camera/` | `BP_DuelCameraRig`, two hit camera shakes |
| `Input/` | `IMC_Default`, `IMC_MouseLook`, five input actions |
| `Maps/` | `Lvl_DuelGraybox` (**the shipping level**), `Lvl_ArenaOctagon` (reference only, not cooked), `Checkpoints/` |
| `UI/` `VFX/` `Animation/` | `UI_DuelHUD`, `UI_LifeBar`, `NS_Damage`, `ABP_VanguardLocomotion` |

Epic's template files stay where they are. `Content/Input/Touch/` is genuinely referenced
by the player pawn and the controller — leave it alone.

**Config:** `EditorStartupMap` and `GameDefaultMap` both point at
`/Game/AscendantImpact/Maps/Lvl_DuelGraybox`. Opening the project lands you in the arena.
**Only maps reachable from `GameDefaultMap` are cooked.**

## The systems that already work

- **Player** — movement, jump with dynamic side switching, punch via `IA_Attack` playing
  `MM_Attack_01` as a dynamic slot montage, health, hit-react, camera shake.
- **Vanguard mover** (`BP_VanguardDuelMover`) — runtime-spawned by the controller.
  Preferred-range band with hysteresis, depth wander, hit-react pause, and dynamic side
  ownership with a jump-over crossing state. **Its `ApplyConstraints` is the single
  authority for all fighter position constraints**, including the ±650 arena bounds and
  the 78 cm minimum separation. Extend it there rather than adding a second clamp system.
- **Vanguard attack driver** (`BP_VanguardBasicAttackDriver`) — int-state flow of
  idle/windup/strike/recovery, a TextRender telegraph, one overlap impact per strike,
  2.5–4 s cooldowns, windup cancelled by a hit-react. **Steps 3 and 4 of the plan extend
  this with two more attacks.**
- **Knockout coordinator** (`BP_DuelKnockoutCoordinator`) — one-shot per fighter at zero
  health: cancels the driver, disables ticks, plays the death montage, ragdolls after
  1.4 s. **Known bug `X7`: disabling the mover's tick also stops `ApplyConstraints`, so
  the arena clamp dies with it. Step 2 of the plan fixes this.**
- **Duel camera** (`BP_DuelCameraRig`) — runtime-spawned, 2.5D side profile, midpoint
  tracking, separation-driven distance, mutual facing. Camera framing is coupled to the
  arena bounds: separation 1300 needs `DistancePerSeparation` 0.8 and
  `MaxCameraDistance` 1500. **Retune both together or neither.**

## The arena

`game/Tools/ArenaPipeline/` generated the octagon and its geometry now lives inside
`Lvl_DuelGraybox` — 30 `ArenaOct_*` actors. **This pipeline is the Assignment 10
deliverable. Do not modify it.** Generator order is `arena` → `detail` → `tiers`; running
`tiers` before `detail` leaves 16 stray parapet-step actors behind.

Evidence and screenshots: `reports/arena/2026-08-28-merged-into-duel/`.

## Working log

`docs/agent/PROTOTYPE_BLACKBOARD.md` is the running record of what is live in the editor
versus persisted to disk, and it carries the long-form MCP gotchas. Read it before
in-engine work; update it as work progresses.
