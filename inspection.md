# Inspection Report — Ascendant Impact

**Produced by:** inspector agent (runs last)
**Consumes:** `design-brief.md` + `build-sequence.md` (scope questions settled against `project-brief.md`)
**Produces:** this document
**Date:** 2026-07-27

Method: every build step was traced to a named design-brief item (TRACES or ORPHAN);
the design brief was scanned for decisions no step implements (GAPS); and the four hard
checks — scope lock, no runtime AI-model calls, milestone order M1→M5, numbers unchanged
— were run against the full build sequence.

---

## Violations

**None.** All four hard checks pass. Detail below; one borderline item is recorded under
"Observations for the human designer" — it is not a violation because it faithfully
implements an explicit design-brief decision, but the human should glance at it.

### Check 1 — Scope lock: PASS
- **One player framework:** exactly one `BP_PlayerFighter` (M1-11); Echo and Nova are two
  `DA_FighterProfile` instances (M1-12), no `BP_Echo`, no `BP_Nova`, no child Blueprints,
  no `Switch on Fighter` in combat code. Matches design-brief §4.1.
- **One authored AI opponent:** one `BP_CrimsonVanguard` (M2-05). No second rival, no
  second boss kit, no playable Vanguard.
- **One arena:** one `L_ShatteredRing` (M1-21). `L_CharacterSelect` (M1-22) is a menu
  level, not a combat arena — not a second arena.
- **Four rival attacks A–D:** `DT_VanguardAttacks` has **exactly four rows A, B, C, D**
  (M2-04), B/C/D authored in M4-01. **No fifth attack anywhere.**
- **One duel, win and loss:** win path (M4-07), loss path (M4-09).
- **No deferred feature acquired a build step.** Nothing from design-brief §1.4
  (PvP, unique per-fighter move sets, second boss kit, additional arenas, progression,
  transformations) is built. R1 is honored: one shared montage set, differentiation by
  `DA_FighterProfile` scalars only (M1-12, M1-14) — no per-fighter unique move set.
  (`ANS_TrackingLock` in M4-02 is a notify state, not an attack — not a scope breach.)

### Check 2 — No runtime AI-model calls: PASS
- Crimson Vanguard is deterministic authored logic: `BT_CrimsonVanguard` + `BB_CrimsonVanguard`
  (M2-08, M2-09) run from `BP_VanguardController` (M2-07), driven by the `DT_VanguardAttacks`
  Data Table (M2-04). Six Blueprint `BTTask_*` (M2-12).
- The only nondeterminism is **authored-weighted selection among in-range attacks**
  (`SelectionWeight`, M4-03) — no model call, no learning, no adaptive difficulty, no
  runtime generation.
- No step, node, or note anywhere describes the rival as an LLM, model API, or adaptive AI.
  Confirmed by Appendix A wall 2 and Appendix B. `AIPerceptionComponent` is deliberately
  not used (M2-07).

### Check 3 — Milestone order M1→M5: PASS
- Steps are grouped strictly M1 → M2 → M3 → M4 → M5 and numbered `M<n>-NN`.
- **M5 is gated behind a stable M4** — the M5 header states "ONLY after M4 is stable …
  after 1 September," and every M5 step (M5-01…M5-08) only fills an already-wired,
  empty `BP_PresentationSubsystem` wrapper (built empty in M1-06) or swaps proxy art,
  changing no gameplay timing.
- **No M1–M4 step depends on a later milestone.** Forward references (e.g. M1-18's
  `AN_ComboFinisher` "meter wired in M3", M1-16's reticle "WBP_HUD, M3") create the asset
  in the current milestone and hook it up later; no milestone's gate requires a later
  milestone's asset. The M1 gate does not require the meter or the HUD.
- Building the empty presentation subsystem (M1-06) and the debug panel (M1-07) is
  structural wiring / kill-switch, not presentation authoring — design-brief §4.10.
- Dressed proxies (M1-23) and the minimal `LS_FinalClash` / `LS_VanguardEntrance` camera
  cuts (M4-06, M4-10) are asset selection and Phase-1 items explicitly listed IN Phase 1
  by design-brief §1.2; full choreography is correctly deferred to M5-07.

### Check 4 — Numbers unchanged: PASS
Every governed number survives verbatim, marked provisional, none resolved:
- **Meter 0–100:** M3-03 clamp.
- **+5 combo finisher / +12 perfect dodge / +15 counter / +20 Impact Window / +0 damage-or-waiting:**
  `DT_MeterGains` M3-02, hooks M3-05 (also M1-18 +5, M1-20 +15, M1-15 +0). `DamageTaken`
  kept explicit at +0 so "waiting/damage grants nothing" is visible as data.
- **Phase 2 at 50% health:** M4-04, `Percent <= 0.50`.
- **Final Clash gated on meter 100 AND rival health ≤ 25%:** M4-05,
  `(Meter >= 100) AND (CV Health Percent <= 0.25)` — the **AND** is preserved; if one
  condition only, the Clash stays locked.
- **Failed Clash:** 1 HP floor (M4-08 step 4), meter set to 50 (step 5, the one sanctioned
  exception to the `AddMeter`-only rule), 3-second cooldown (step 6), return to neutral
  (step 7), and "must NOT happen: duel restart; player killed/damaged" (explicit).
- **Impact windows:** first 0.75 s, standard 0.35–0.50 s, burst 1–3 s (M3-07). CV/state
  phase ranges (0.60–1.20 / 0.35–0.80, 0.55–0.95 / 0.40–0.75, 0.45–0.90 / 0.35–0.75,
  active 0.18–0.45 unchanged both phases) carried in M2-02, M2-13, M4-01. Heights 183/173
  (M1-12), 208 (M1-23).
- **All 29 §13.2 OPEN values + Q30/Q31** left OPEN as designer-exposed variables with their
  §14 question tags (Appendix B). No value picked from a proposed range. The M2-04 range
  check **flags** out-of-range tuning, it does not pick.

---

## Per-step verdict

Every step **TRACES**. No orphans found.

### M1 — Combat gray box
| Step | Verdict | Brief item |
|---|---|---|
| M1-01 base project | TRACES | §1.2 movement+camera; R2 (standard AnimBP locomotion) |
| M1-02 folder structure | TRACES | §2 content root / folder table |
| M1-03 gameplay tags | TRACES | §3 (tags without GAS) |
| M1-04 `AttackTrace` channel | TRACES | §5.2 |
| M1-05 `DA_TuningGlobals` | TRACES | §4.8, §13.2 rows 29–30 |
| M1-06 `BP_PresentationSubsystem` (empty) | TRACES | §4.10 kill-switch |
| M1-07 `WBP_DebugPanel` | TRACES | §4.10 |
| M1-08 shared `BP_HealthComponent` | TRACES | §4.8 (1 HP floor mechanism, 50%/≤25% reads) |
| M1-09 `BP_DuelDirector` | TRACES | §2 architecture |
| M1-10 Enhanced Input assets | TRACES | §4.3 |
| M1-11 `BP_PlayerFighter` (one class) | TRACES | §4.1 single-source rule |
| M1-12 `DA_FighterProfile` + Echo/Nova | TRACES | §4.2; R1; §12.3 color constraint |
| M1-13 `ApplyFighterProfile` | TRACES | §4.2 application + scale note |
| M1-14 `ABP_Fighter` (shared, stance additive) | TRACES | §4.2; R1; R2 |
| M1-15 `BP_CombatComponent` / `ResolveIncomingHit` | TRACES | §4.6 three-way branch |
| M1-16 `BP_LockOnComponent` | TRACES | §4.4 lock-on / side-on readability |
| M1-17 `AM_Player_LightCombo` | TRACES | §4.5 |
| M1-18 combat notifies + `AN_ComboFinisher` | TRACES | §4.5, §5.2 (shared `ANS_ActiveHit`) |
| M1-19 `AM_Player_Dodge` + nested i-frames | TRACES | §4.6 |
| M1-20 counter input + player montages | TRACES | §4.7 |
| M1-21 `L_ShatteredRing` gray box | TRACES | §10.2; §1.5 R6 (no-hazards negative req) |
| M1-22 character-select entry | TRACES | §10.1 simplified-screen allowance |
| M1-23 dressed proxies | TRACES | §12 asset selection; §11.6; R1/R4 |
| M1-GATE | TRACES | §11.1 |

### M2 — Rival state loop
| Step | Verdict | Brief item |
|---|---|---|
| M2-01 rival enums (GDD-order states, A–D) | TRACES | §6.2, §5.3 |
| M2-02 `S_AttackPhaseTuning` | TRACES | §5.3; §13.1 rows 17–25 |
| M2-03 `S_VanguardAttackDef` | TRACES | §5.3 |
| M2-04 `DT_VanguardAttacks` (four rows) | TRACES | §5.3; §11.2 item 4; range-flag check §13.1 note |
| M2-05 `BP_CrimsonVanguard` | TRACES | §2; §4.8 shared health |
| M2-06 `BP_VanguardCombatComponent` | TRACES | §4.6, §4.7, §5.1, §6.5 |
| M2-07 `BP_VanguardController` (no AI Perception) | TRACES | §6.1, §3 |
| M2-08 `BB_CrimsonVanguard` | TRACES | §6.2 |
| M2-09 `BT_CrimsonVanguard` (loop, no abort/stop) | TRACES | §6.1, §6.3, §6.5 |
| M2-10 `BTService_UpdateCombatData` | TRACES | §6.3, §6.4 task 1 |
| M2-11 `BTService_DrawDebugState` | TRACES | §6.6; §6.1 reason 1 |
| M2-12 six `BTTask_*` (guaranteed exit + failsafe) | TRACES | §6.3, §6.4; §15 no-runtime-AI |
| M2-13 Attack A montage + notify states | TRACES | §5.1; §11.2 item 5 |
| M2-14 counter interrupt through the sequence | TRACES | §6.5, §4.7 |
| M2-GATE | TRACES | §11.2 |

### M3 — Impact handoff
| Step | Verdict | Brief item |
|---|---|---|
| M3-01 meter/impact enums | TRACES | §4.9, §7.1 |
| M3-02 `S_MeterGain` + `DT_MeterGains` (5 rows) | TRACES | §4.9; §13.1 rows 6–10 |
| M3-03 `BP_AscensionComponent` (0–100, one write path) | TRACES | §4.9 |
| M3-04 `WBP_HUD` (meter/reticle/gate stub/blank label) | TRACES | §4.9, §4.4, §9.1, §14 Q29 |
| M3-05 five meter hooks | TRACES | §7.6 |
| M3-06 `WBP_ImpactPrompt` | TRACES | §7.1, §9.2 (R3 reuse) |
| M3-07 `BP_ImpactWindowDirector` (widths, onboarding prohibitions) | TRACES | §7.1–7.4 |
| M3-08 `RestoreCombatState()` (written once) | TRACES | §7.5 |
| M3-GATE | TRACES | §11.3 |

### M4 — Complete duel
| Step | Verdict | Brief item |
|---|---|---|
| M4-01 Attacks B, C, D authored | TRACES | §5.1 readability table; §11.4 items 1–2; R5 |
| M4-02 `ANS_TrackingLock` | TRACES | §5.1 (B/C), §5.3 `bLockTrackingAtActive` |
| M4-03 weighted range/cooldown selection | TRACES | §6.4 task 2; §15 no-runtime-AI |
| M4-04 Phase 2 via one data path | TRACES | §8 (trigger, commit-on-Return-to-Neutral, one-shot signal, one `Select` node) |
| M4-05 `BP_FinalClashDirector` double gate | TRACES | §9.1; §13.1 rows 11–12 |
| M4-06 two beats + `LS_FinalClash` | TRACES | §9.2; §11.4 item 5 |
| M4-07 Clash SUCCESS → Win | TRACES | §9.3 |
| M4-08 Clash FAILURE → seven-step recovery | TRACES | §9.4; §13.1 rows 13–15 |
| M4-09 Loss + `WBP_Result` (no timer) | TRACES | §9.5; §11.4 item 8 |
| M4-10 `LS_VanguardEntrance` (skippable) | TRACES | §10.1; §11.4 item 9 |
| M4-GATE | TRACES | §11.4 |

### M5 — Presentation pass (Phase 2, after 1 Sept)
| Step | Verdict | Brief item |
|---|---|---|
| M5-01 hit-stop / time-dilation | TRACES | §1.3 |
| M5-02 camera shake + choreography | TRACES | §1.3; §4.4 deferred camera |
| M5-03 authored Niagara VFX | TRACES | §1.3; §12.3 color constraint |
| M5-04 sound design + mix | TRACES | §1.3; §12.6; §14 Q31 |
| M5-05 arena environmental reaction | TRACES | §10.2; §1.5 R6 |
| M5-06 final character treatment | TRACES | §1.3; §12.4; §14 Q30 |
| M5-07 full-fidelity Clash choreography | TRACES | §1.3; §9.2 |
| M5-08 editorial selection interface | TRACES | §1.3; §10.1 Phase-2 column |

---

## Gaps

**None.** Every design-brief decision has an implementing step. Cross-check of the
design-brief §1.2 "IN Phase 1" table confirms all nineteen listed systems have a step
(movement/camera M1-01; lock-on M1-16; light combo M1-17/18; dodge+perfect M1-19;
counter M1-20/M2-14; health M1-08; selection M1-22; Echo/Nova M1-11/12; six-state loop
M2-09/12; attacks A–D M2-04/M2-13/M4-01; T/A/R windows M2-13; Impact Windows M3-07;
meter M3-03; Phase 2 M4-04; Final Clash M4-05..08; win/loss M4-09; entrance M4-10;
dressed proxies M1-23; debug M1-06/07). The three implementation safeguards (visible
debug state names, presentation separation, explicit restore) are each implemented
(M2-11, M1-06, M3-08).

Minor, not a gap: `DA_FighterProfile.IntroMontage` (M1-12) exists as data but the §10.1
Phase-1 opening flow does not wire a player intro montage to play — this matches the
design brief, which does not require it played in Phase 1, so nothing is missing.

---

## Observations for the human designer (not violations)

- **M4-04 Phase 2 signal, Phase 1 realization.** The step fires the one-shot Phase 2
  signal through `BP_PresentationSubsystem` as an "emissive-intensity change + brief
  pause." This is copied verbatim from design-brief §8.2 and is permitted by §1.3
  ("flat emissive material colors only" in Phase 1), with authored VFX/sound/thruster
  correctly deferred to M5-03/M5-04. It traces faithfully and is not milestone-order
  drift by the developer. The only element worth a designer's eye is the "brief pause"
  wording, since tuned pause/hit-stop feel is otherwise an M5 concern; the developer did
  not invent it, so this is surfaced, not flagged.

---

## Overall verdict

**Yes — the build sequence is faithful to the design brief.** All four hard checks pass,
every build step traces to a named brief decision, there are no orphans and no gaps, and
no number was altered, invented, or quietly resolved.
