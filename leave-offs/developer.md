---
agent: developer
status: complete
artifact: build-sequence.md
---

# Developer leave-off

`build-sequence.md` is on disk in the project root — an ordered, buildable sequence of
Unreal Engine 5.8 editor steps grouped strictly by milestone **M1 → M2 → M3 → M4 → M5**.
It contains **63 build steps** (M1: 23, M2: 14, M3: 8, M4: 10, M5: 8), each with an
editor path / menu action, the specific Blueprint / asset / node names, what it
produces, and the named design-brief decision it implements. A gate-verification block
closes each milestone, restating that milestone's GDD "Done when".

## What I produced, against the three walls

- **SCOPE LOCK held.** One `BP_PlayerFighter` (Echo/Nova as `DA_FighterProfile` data),
  one `BP_CrimsonVanguard`, one `L_ShatteredRing`, one shared framework, four rows A–D
  in one `DT_VanguardAttacks`, one duel with Win and Loss. Nothing from design-brief
  §1.3 (Phase-2/M5 deferred) or §1.4 (outside SCOPE LOCK) got a build step in M1–M4.
- **No runtime AI-model calls.** The rival is `BT_CrimsonVanguard` + Data Table; the
  only nondeterminism is authored-weighted attack selection. No step calls a model.
- **Numbers unchanged.** All GDD values carried verbatim and marked provisional/tunable
  (0.75 s / 0.35–0.50 s windows, +5/+12/+15/+20/+0 meter, meter 100 & CV ≤25% gate,
  1 HP floor, meter→50, 3 s cooldown, Phase 2 at 50%, all six state ranges, three
  heights, active window unscaled across phases).
- **Milestone order not interleaved.** Every M5 step fills the empty
  `BP_PresentationSubsystem` wired in M1-06 and changes no gameplay timing; no M1–M4
  step depends on a later milestone.

## OPEN values preserved without resolving

All **29** open values from design-brief §13.2 (Q1–Q29), plus the two asset decisions
Q30–Q31, are implemented as designer-exposed variables and left OPEN with their §14
question tag. I picked **none** from any proposed range. Appendix B of the artifact
lists all of them.

## Gaps in the brief I had to flag (Appendix C of the artifact)

- GDD pages 10–14 are image reference sheets with no extractable text — no step guesses
  arena appearance or costume geometry; proxy art stands in until M5-06.
- Crimson Vanguard has no verified free asset (R4/§12.4) — M1-23 uses the option-1
  Mannequin-plus-proxy-blocks fallback; a Paragon swap (Q30), if chosen, must precede
  M4 range tuning.
- No free sound source verified (§12.6) — Phase 1 may ship silent (Q31); music
  unsourced; all audio is M5-04.
- Per-attack tuning floats inside the GDD state ranges (Q25) are unfilled — M2-04 adds
  an editor-time range-validation check that flags out-of-range values, never picks one.
- Arena footprint / range bands / attack-D travel (Q24/Q10/Q13) interlock and are a
  likely early bug source; left OPEN and cross-referenced.

Handoff: the inspector's gate is now open. It consumes `design-brief.md` +
`build-sequence.md` and produces `inspection.md`, enforcing scope lock, no-runtime-AI,
M1→M5 order, and numbers-unchanged.
