---
id: G12
track: G
title: Wire the Assignment 06 attack CSV into the game as a DataTable
status: todo
assignment: 10
editor-required: true
depends-on: [G05]
---

## Goal

The Vanguard's attack values come from a DataTable built from
`assignment-06/evidence/generated_DT_VanguardAttacks.csv`, not from hardcoded variables on
the driver. Attack A behaves **exactly as it does today** when this is finished.

## Why it matters

Two reasons, and the second is worth points.

1. **It makes every later attack cheap.** Adding attack B or C becomes a new row plus a
   behaviour branch, instead of another wall of hardcoded floats.
2. **It is pipeline-produced content in the shipped build.** A10's Pipeline-to-Game
   Connection is 3 points and currently rests entirely on the octagon. Assignment 06 built
   a validated generator *and* a CSV validator for exactly this table — and **the output
   was never wired into the game.** No `DT_*` asset exists anywhere in `game/Content`.
   Wiring it in means two independent pipelines demonstrably feed the build.

The blackboard §10.3 recorded why it stalled: creating the row struct was a manual blocker
at the time. That blocker is worth paying now.

## Preconditions

- `G05` complete. Do not refactor the driver while the match loop is still moving.
- Editor free. This touches `.uasset`.

## Steps

1. Create the row struct matching the CSV columns. Only the fields the driver actually
   needs become gameplay values — the rest (`GameplayPurpose`, `Notes`) are documentation
   and can ride along as strings.
2. Add the numeric columns the CSV does not carry yet, because A06 deliberately left every
   timing and damage value OPEN: `WindupDuration`, `StrikeImpactDelay`, `StrikeDuration`,
   `RecoveryDuration`, `AttackRange`, `ImpactForwardOffset`, `ImpactRadius`,
   `ImpactDepthTolerance`, `AttackDamage`, `CooldownMin`, `CooldownMax`, `SelectionWeight`.
3. Seed **Row_A with today's measured values** so behaviour is unchanged:
   windup 1.1, impact delay 0.3, strike 0.6, recovery 1.0, range 240, offset 100,
   radius 90, depth tolerance 55, damage 10, cooldown 2.5–4.0.
4. Import as a DataTable at `/Game/AscendantImpact/Data/DT_VanguardAttacks`.
5. Change `BP_VanguardBasicAttackDriver` to read the active row instead of its own
   variables. Keep the variables as the fallback if the table is missing, so a bad import
   cannot brick the fight.
6. Extend `Tools/` with the CSV-to-DataTable step so a regenerated CSV lands in the engine
   without hand editing — that is what "output lands in the engine without manual
   reformatting" means on the rubric.

## Done when

- [ ] `DT_VanguardAttacks` exists in `game/Content` and is populated from the A06 CSV.
- [ ] The driver reads Row_A from the table; the fight is **indistinguishable** from before.
- [ ] Changing a value in the CSV and re-importing changes the fight, with no hand editing.
- [ ] A full match still plays: telegraph, strike, damage, KO.

## Log

- 2026-08-24 — created. Confirmed no `DT_*` asset exists anywhere in `game/Content`, and
  `assignment-06/evidence/generated_DT_VanguardAttacks.csv` carries approved metadata for
  rows A, B, C and D with every numeric value still OPEN.
