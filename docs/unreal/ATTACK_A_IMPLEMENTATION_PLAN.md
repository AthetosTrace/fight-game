# Attack A Implementation Plan — Crimson Vanguard

**Purpose:** the concrete, individually-testable build sequence for the
*only* enabled Vanguard attack this sprint, once `DT_VanguardAttacks` is
imported per `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`. This plan
describes Unreal-side implementation work — **it is not authorized to
begin until that import is complete and the human approval in
`VANGUARD_ATTACK_DATA_APPROVAL.md` is signed.** Nothing here invents a
timing, damage, or range number; every numeric field referenced is a
designer-exposed variable per `design-brief.md` §13.2/§14, left at
whatever the human designer sets.

**Source alignment:** this plan follows `design-brief.md` §5 (attack
authoring), §6 (rival state model), §7 (Impact Windows), and the eight-point
proof list from `ASCENDANT_IMPACT_NEXT_SPRINT_HANDOFF.md` ("Attack A must
prove: select, telegraph, active attack, hit detection, recovery, return to
neutral, interruption cleanup, combat-state restoration"). It also carries
forward the five open restoration gaps (V1–V5) named in
`cinematic-integration-inspection.md` as **known, unresolved** — this plan
does not silently assume they are fixed.

**Milestone:** M2 (one attack, all six rival states) per
`CLAUDE.md`/`project-brief.md`. Does not require M3 (Impact Window
scoring) or M4 (Phase 2, Final Clash) to be complete first, but hooks into
a minimal stub of each so the M2→M3 boundary is visible and testable.

---

## 0. Preconditions

- [ ] `DT_VanguardAttacks` DataTable exists and Attack A reads correctly in
      PIE (per `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md` Steps 5–7).
- [ ] `VANGUARD_ATTACK_DATA_APPROVAL.md` is signed.
- [ ] A proxy Crimson Vanguard mesh/skeleton exists in the Unreal project
      (mannequin or scaled proxy, per `ASCENDANT_IMPACT_NEXT_SPRINT_HANDOFF.md`).
      If not, this plan cannot proceed past Step 1 — surface that gap to
      the human designer rather than substituting an unapproved asset.
- [ ] `BT_CrimsonVanguard` / `BB_CrimsonVanguard` skeleton exists per
      `design-brief.md` §6.2/§6.3 (six Blackboard keys, `Selector` +
      `Sequence` under `Loop`), even if its tasks are currently stubs.

---

## 1. Vanguard state transitions (the six-state cycle, Attack A only)

**Test independently of any attack content:** the `Sequence` under `Loop`
advances through all six `BTTask_*` stubs and returns to
`Idle_Reposition` indefinitely, with `CurrentState` visibly changing via
`BTService_DrawDebugState` (design-brief.md §6.6).

- [ ] Implement `BTTask_Idle_Reposition`: sets `CurrentState`, holds/moves
      per `RepositionDelay` (designer-exposed, currently OPEN — §14 no
      direct Q, uses the GDD-range value the designer sets), exits when
      `DistanceToTarget` falls inside Attack A's `MinRange`/`MaxRange`
      (currently OPEN, §14 Q10 — implement as a data-driven check even
      while the value itself is unset/placeholder).
- [ ] Implement `BTTask_SelectAttack`: since only Attack A is
      `EnabledForSelection = true`, selection trivially always picks Row_A
      when in range. **Do not hardcode "always Attack A" as a special
      case** — filter `DT_VanguardAttacks` by `EnabledForSelection == true`
      and by range/cooldown, exactly as design-brief.md §6.4 #2 specifies,
      so B–D activate later with zero logic change, only a data flip.
- [ ] Implement the guaranteed-exit failsafe on every task per
      design-brief.md §6.3: `Set Timer by Event` at (montage length + a
      designer-set margin, §14 Q18, OPEN) calling `Finish Execute(Success)`
      if `On Montage Ended` never fires.

**Individually testable:** PIE with Attack A's montage temporarily muted/
skipped — confirm the cycle still completes via the failsafe timer alone,
proving the guaranteed-exit rule works independent of animation content.

---

## 2. Telegraph

- [ ] Author `AM_Vanguard_AttackA` (or reuse an existing proxy montage) with
      an `ANS_Telegraph` notify state covering the wind-up (design-brief.md
      §5.1: pose hold, no hitbox).
- [ ] `BTTask_Telegraph`: `Play Anim Montage` at the Telegraph section,
      `CurrentState = Telegraph`, exits on `ANS_Telegraph → Received Notify
      End`.
- [ ] `ANS_Telegraph → Received Notify Begin`: broadcast `OnTelegraphStart(A)`,
      apply the emissive red-orange telegraph color (flat material color in
      Phase 1, per design-brief.md §1.3 — no authored VFX yet).
- [ ] Attack A's GDD readability requirement — "distinct wind-up and
      punishable recovery" — is satisfied by this being the **longest**
      `ANS_Telegraph` window among any attack authored later; note this as
      a design constraint for whoever times the montage, not a number this
      plan sets.

**Individually testable:** in PIE, trigger Attack A and confirm the
telegraph pose holds for its full authored duration with the debug string
showing `Telegraph`, before any hitbox exists.

---

## 3. Active attack (hit detection is folded in here per design-brief §5.2)

- [ ] Add `ANS_ActiveHit` notify state on the montage's active section.
- [ ] `BTTask_ActiveAttack`: `CurrentState = ActiveAttack`; the notify's
      `Received Notify Tick` runs `Capsule Trace By Channel` on the
      `AttackTrace` custom channel (create it in *Project Settings → Engine
      → Collision* if it does not exist), tracing from the previous frame's
      socket location to the current frame's.
- [ ] `Received Notify Begin`: clear the per-window already-hit `Set of
      Actor` (prevents multi-hit within one active window, design-brief.md
      §5.2).
- [ ] `Received Notify End`: disable the trace.
- [ ] On hit: `Break Hit Result → Get Hit Actor → ResolveIncomingHit` on the
      player's `BP_CombatComponent` (this is the same function the player's
      dodge/perfect-dodge/counter detection uses — design-brief.md §4.6;
      Attack A must call it, not a parallel/duplicate hit-resolution path).
- [ ] `HitTraceSocket` for Attack A is currently **blank** in the approved
      CSV (source audit §5) — this step cannot be finished until the
      designer/animator confirms a real socket name against the chosen
      proxy skeleton. Stub with a placeholder socket only in a disposable
      test scene, never commit a guessed socket name as final.

**Individually testable:** with `bDrawHitTraces` on, confirm the trace
capsule is visually drawn only during the active window and disappears
immediately at `Received Notify End`; confirm a dodge outside the active
window takes no damage and a hit inside it does.

---

## 4. Recovery

- [ ] Add `ANS_Recover` notify state. `BTTask_Recover`: `CurrentState =
      Recover`; `Received Notify Begin` sets the rival's
      `IncomingDamageMultiplier` (punish-opening mechanism, design-brief.md
      §5.1); no new attack may start during this state (enforced structurally
      — `SelectAttack` only runs from `Idle_Reposition` in the Sequence
      order, so this is already true by the tree's shape, not an extra
      guard).
- [ ] `Received Notify End`: restore `IncomingDamageMultiplier` to its
      default.

**Individually testable:** land a hit on Crimson Vanguard during Attack A's
recovery window and confirm the multiplier is applied (visible via debug
log of the multiplier value at hit time), then confirm it reverts once
`Recover` ends.

---

## 5. Return to neutral

- [ ] `BTTask_ReturnToNeutral`: clear `SelectedAttack = None`,
      `bCounteredThisAttack = false`, restore tracking (see §6.5 note
      below), `Set Movement Mode (Walking)`, clear the montage reference.
      Evaluate the Phase 2 commit check (currently a no-op stub since Phase
      2/M4 is out of scope for this milestone — do not implement Phase 2
      logic here, just leave the hook point named and empty).
- [ ] Confirm `CurrentState = ReturnToNeutral` is visible in the debug
      string for its full authored duration before the `Sequence` loops
      back to `Idle_Reposition`.

**Individually testable:** run Attack A to completion with no player
interaction; confirm the cycle returns to `Idle_Reposition` and immediately
becomes eligible to select Attack A again (since it is the only enabled
attack) without any stranded flag.

---

## 6. Interruption cleanup (the counter path — design-brief §4.7/§6.5)

This is the one legal external interrupt and the piece most likely to
strand a flag if implemented sloppily.

- [ ] Add `ANS_CounterWindow` notify state on Attack A's montage,
      overlapping late telegraph / early active per design-brief.md §5.1.
- [ ] `Received Notify Begin`: `bCounterable = true` on
      `BP_VanguardCombatComponent`, broadcast `OnCounterWindowOpen`.
      `Received Notify End`: `bCounterable = false`.
- [ ] Player's `IA_Counter` inside the window (player-side work, out of
      this plan's scope but the hook must exist): `Montage Stop` the rival
      montage → `bCounteredThisAttack = true` → the running task's `On
      Montage Ended` fires → task calls `Finish Execute(Success)` → the
      `Sequence` advances. `BTTask_Recover` checks `bCounteredThisAttack`
      and plays the counter-reaction beat instead of normal recovery.
- [ ] **Do not use `Abort Self`, `Simple Parallel` aborts, or `Stop Logic`**
      anywhere in this path (design-brief.md §6.5 hard rule) — the counter
      routes *through* the Sequence's guaranteed forward motion, never
      around it.
- [ ] Clear `bCounteredThisAttack` back to `false` in
      `BTTask_ReturnToNeutral` (§5 above) so it never leaks into the next
      cycle.

**Individually testable:** trigger a counter mid-Telegraph and mid-Active on
separate PIE runs; confirm in both cases the montage stops cleanly, the
counter-reaction plays, `Recover` still fires and still exits normally, and
`bCounteredThisAttack` is false again by the time `Idle_Reposition` resumes.

---

## 7. Player dodge/counter interaction (perfect dodge detection)

- [ ] Confirm `ResolveIncomingHit` (§3 above) correctly branches on the
      player's tags at hit time per design-brief.md §4.6's table:
      `State.PerfectWindow` → perfect dodge, 0 damage, `+12` meter, request
      Impact Window; `State.Invulnerable` only → ordinary dodge, 0 damage,
      no meter; neither → hit applied, `+0` meter.
- [ ] This must be **the same trace/function** the player's own attacks use
      to resolve hits — no parallel hit-resolution path for "attacks
      against the player" versus "attacks against the rival."

**Individually testable:** perform a plain dodge, a perfect dodge, and no
dodge against Attack A's active window in three separate PIE runs; confirm
damage and meter gain match the table above in each case.

---

## 8. Minimal meter hook

- [ ] Confirm `BP_AscensionComponent → AddMeter(PerfectDodge)` (+12) and
      `AddMeter(Counter)` (+15) fire correctly off Attack A's own windows,
      reading from `DT_MeterGains` (design-brief.md §4.9) — no hardcoded
      meter values inside Attack A's own logic.
- [ ] Confirm `AddMeter(DamageTaken)` (+0) fires explicitly on a plain hit,
      so "no passive/damage meter gain" is visible as data, not an absence.

**Individually testable:** watch `WBP_HUD`'s meter bar (or a debug print of
`Meter`) across a perfect dodge, a counter, and a plain hit against Attack A;
confirm +12 / +15 / +0 respectively and nothing else moves the value.

---

## 9. First Impact Window hook

- [ ] Confirm a perfect dodge or successful counter against Attack A calls
      `RequestImpactWindow` (design-brief.md §7.1), and that
      `bFirstWindowConsumed` correctly selects `FirstWindowDuration`
      (0.75 s, governed) on the very first qualifying event of the duel
      and `StandardWindowDuration` (0.35–0.50 s, governed) thereafter.
- [ ] Confirm the three onboarding prohibitions from design-brief.md §7.3
      hold against Attack A specifically: no auto-success path, no
      pre-open input buffering into success, and the wider first window
      changes only the duration float (no slowed time, no softened
      failure, no altered enemy recovery).
- [ ] **Do not implement the Impact Window burst's rival-AI suspension as
      "solved."** Per `cinematic-integration-inspection.md` V1, no
      mechanism yet suspends `BT_CrimsonVanguard` during the 1–3 s burst
      outside the Final Clash's `bInClash` flag. For this Attack A slice,
      the safest interim rule (to be confirmed with the designer, not
      decided here) is: **do not allow `SelectAttack` to fire while an
      Impact Window burst is playing** — since Attack A only cycles back
      through `Idle_Reposition → SelectAttack`, gating `SelectAttack` on
      "no burst currently playing" is a minimal, targeted fix that does not
      require solving all of V1–V5 to ship this one attack safely. Flag
      this explicitly to the designer as an interim decision, not a closure
      of V1.

**Individually testable:** trigger a perfect dodge as the very first
qualifying event of a fresh PIE session; confirm the window is 0.75 s and a
second qualifying event later in the same session opens the shorter
standard window instead.

---

## 10. Debug display

- [ ] `BTService_DrawDebugState` shows, at minimum: `CV | <Phase> |
      <CurrentState> | Attack_A_GauntletForce | <elapsed time in state>`
      (design-brief.md §6.6 format), gated on
      `BP_PresentationSubsystem.bShowStateNames`.
- [ ] Confirm the built-in Gameplay Debugger (apostrophe key, AI category)
      independently shows the same Blackboard values, as a second
      cross-check per design-brief.md §6.6.

**Individually testable:** toggle `bShowStateNames` off and confirm the
custom debug string disappears while gameplay timing is unaffected (per the
presentation kill-switch's hard rule, design-brief.md §4.10) — the built-in
Gameplay Debugger remains available as an independent view regardless.

---

## 11. Completion evidence (what M2's gate needs to see)

Per `project-brief.md`'s M2 gate — "all six AI states and one Crimson
Vanguard attack complete without deadlock… returns to Neutral every
attempt" — the evidence package for Attack A is:

- [ ] A PIE recording (or screenshots per state) showing all six states
      firing in order with visible debug names, for at least 3 consecutive
      full cycles with no player interaction (proves no deadlock).
- [ ] One PIE run showing a successful dodge outcome (no damage, no meter).
- [ ] One PIE run showing a successful perfect dodge outcome (no damage,
      +12 meter, First Impact Window opens at 0.75 s).
- [ ] One PIE run showing a successful counter outcome (rival montage
      stopped cleanly, +15 meter, Impact Window requested, cycle still
      reaches `ReturnToNeutral` normally).
- [ ] One PIE run showing a plain hit outcome (damage applied, +0 meter).
- [ ] Confirmation that `bCounteredThisAttack`, `SelectedAttack`, and the
      hit-trace already-hit set are all clear at the start of every new
      cycle (no leaked state across repeated triggers).
- [ ] Output Log excerpt showing zero errors/warnings across the above runs.

This evidence maps directly onto `ATTACK_A_ACCEPTANCE_TESTS.md` (Task 9),
which defines the pass/fail rule for each of the above as a discrete test
case.

---

## Explicitly out of scope for this plan

- Attacks B, C, D's active implementation (metadata only, per the approved
  CSV).
- Phase 2 re-timing logic (M4).
- Final Clash (M4).
- Resolving `cinematic-integration-inspection.md` corrections V1–V5 in full
  — this plan names one minimal interim mitigation for V1 (§9 above) scoped
  only to keeping Attack A's single Impact Window safe, and explicitly does
  not claim the broader restoration contract is fixed.
- Any Niagara VFX, authored sound, or camera choreography (Phase 2/M5).
- Any numeric value not already governed by the GDD — every timing, damage,
  range, and cooldown figure referenced above remains a designer-exposed
  variable, per `design-brief.md` §13/§14.
