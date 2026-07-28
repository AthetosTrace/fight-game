---
agent: combat-integration-architect
status: complete
artifact: combat-integration-plan.md
---

# Leave-off — Combat Integration Architect

**Date:** 2026-07-27 · Ran after the Base Framework Evaluator. Gate check passed:
`inspection.md` reports zero violations, `framework-evaluation.md` ends with a
definitive recommendation, and the human designer's approval record is on file
("APPROVED — use the Blueprint-first custom architecture recommended by
framework-evaluation.md").

## Approved foundation

`USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE` — the design-brief §2–§9 architecture on
stock UE 5.8: one shared `BP_PlayerFighter` with `DA_FighterProfile` data for Echo
and Nova, deterministic `BT_CrimsonVanguard` + `BB_CrimsonVanguard` six-state loop,
four attacks as rows in one `DT_VanguardAttacks` with paired Phase 1/Phase 2 tuning,
Anim Notify State windows, custom `BP_ImpactWindowDirector` / `BP_FinalClashDirector`
with a single `RestoreCombatState()`, and the `BP_PresentationSubsystem` kill-switch.
Plain Blueprints — not GAS, not State Tree, no marketplace template (n00dFighter and
TRUE FGE were rejected upstream). Approval status: APPROVED by the designer of record.

## Integration approach

All 28 required systems are mapped in `combat-integration-plan.md` §3 (foundation
capability, custom work, assets, inputs, outputs, risk, milestone, acceptance
condition per system), with the Unreal architecture map (§4) reusing only the names
already approved in `design-brief.md`, both data-flow chains (§5 — the player
input-to-recovery chain and the Vanguard Telegraph→Active→Recover→Neutral chain),
and a milestone contract for M1–M5 (§6) with pass conditions, git-commit rollback
points, and dependencies. M5 remains last; free proxy-asset selection is permitted
in M1–M4; every GDD number is carried verbatim and provisional; nothing was
resolved.

## Highest-risk dependency

**Animation sourcing/retargeting (R1/R4)** — above all the 6'10" Crimson Vanguard
proxy, which has no verified free asset. Fallback ladder holds: scaled Mannequin +
proxy blocks ships no matter what; a Paragon heavy swap (Q30) must land before M4
range tuning or every range value re-tunes twice. Close second: **schedule pressure
(R7)** — M4 must be functionally complete ~20 August to leave tuning time — and
**Unreal MCP instability**, mitigated by small sessions with save+commit boundaries
and a manual-execution fallback (the build sequence already names exact editor paths).

## Vertical-slice proof

Plan §7: at the M3-GATE, one unbroken PIE run — Echo proxy vs. the full six-state
rival running Attack A → readable `ANS_Telegraph` → one perfect dodge (+12) → the
earned First Impact Window (0.75 s, player-pressed) → the 1–3 s burst montage pair
with a rival stagger/knockback beat → `RestoreCombatState()` back to live combat
(meter at 32), plus the failure fork (expired prompt → immediate clean return, no
punishment). Proves the real-time-to-cinematic handoff contract without redesigning
the duel.

## Open human decisions

All listed in plan §9 as `OPEN — designer decides`: the sandbox combo-buffer test;
any purchase/plugin adoption (including Motion Warping) or external code entering
the build; asset rights review at claim time; MCP manual-fallback policy; the full
design-brief §14 set (Q1–Q31) — health/damage economy, dodge and perfect-dodge
windows, range bands and arena footprint, Clash beat widths and post-counter window,
**Q22 (1 HP floor permanent vs. Clash-only — the most consequential, needed before
M4-08 is final)**, Echo/Nova differentiation scalars (or none in Phase 1), the CV
short HUD label (Q29), the Paragon swap deadline (Q30), and whether Phase 1 ships
silent (Q31). No number was changed or resolved.

**Next:** designer answers the batched questions (Q22 and Q10/Q24/Q25 first);
Unreal MCP is established; M1-01 begins per `build-sequence.md`.
