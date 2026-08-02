# Attack A Acceptance Tests — Crimson Vanguard

**Purpose:** the pass/fail rule set for `ATTACK_A_IMPLEMENTATION_PLAN.md`.
These are manual PIE test cases (no Unreal automated-testing framework is
assumed to exist yet) to be executed by a human once Attack A is built.
None of these tests may be marked passed by an agent — evidence must be
observed in PIE, per the "Evidence required" field on each test.

**Scope:** Attack A only. Attacks B–D are not implemented this sprint and
have no acceptance tests here — confirming they load as disabled rows is
covered by `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md` Step 4, not by a
gameplay test.

---

## Test format

Each test specifies: **ID**, **Preconditions**, **Steps**, **Expected
result**, **State to inspect**, **Evidence required**, **Pass/fail rule**.

---

### AA-01 — Valid DataTable load

- **Preconditions:** `DT_VanguardAttacks` imported per
  `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`.
- **Steps:** Open the DataTable editor; call `Get Data Table Row` for
  `Row_A` from a test Blueprint at `BeginPlay`.
- **Expected result:** all four rows are present; `Row_A`'s fields exactly
  match `data/unreal/DT_VanguardAttacks.csv`.
- **State to inspect:** DataTable editor grid; printed struct fields in
  PIE.
- **Evidence required:** screenshot of the DataTable editor; screenshot or
  log of the printed `Row_A` struct.
- **Pass/fail rule:** PASS only if all 4 rows exist and `Row_A`'s fields
  match the CSV byte-for-byte on every populated field. Any mismatch is a
  FAIL.

### AA-02 — Invalid or missing row handling

- **Preconditions:** AA-01 passed.
- **Steps:** Call `Get Data Table Row` with a row name that does not exist
  (e.g. `Row_E`).
- **Expected result:** the call returns a failure/invalid result (per
  Unreal's standard `Get Data Table Row` behavior) rather than crashing or
  silently returning a zeroed/garbage struct treated as valid.
- **State to inspect:** the Blueprint's success/failure output pin;
  Output Log for any error/warning.
- **Evidence required:** screenshot of the failed lookup branch executing.
- **Pass/fail rule:** PASS if the failure is handled gracefully (no crash,
  no silent fallback treated as real data). FAIL if the game crashes or
  proceeds as if a nonexistent row were valid data.

### AA-03 — Only Attack A selectable

- **Preconditions:** `BT_CrimsonVanguard` running with `DT_VanguardAttacks`
  imported.
- **Steps:** Run several full Idle→SelectAttack cycles in PIE; observe
  `SelectedAttack` via the debug string/Gameplay Debugger each time.
- **Expected result:** `SelectedAttack` is always `A`; `B`/`C`/`D` are
  never selected, because `BTTask_SelectAttack` filters on
  `EnabledForSelection == true`.
- **State to inspect:** `BB_CrimsonVanguard.SelectedAttack` (Gameplay
  Debugger); debug string.
- **Evidence required:** a PIE log/recording covering at least 5 selection
  cycles.
- **Pass/fail rule:** PASS only if `SelectedAttack == A` on every one of
  the observed cycles. Any occurrence of B/C/D is a FAIL.

### AA-04 — Telegraph appears before active attack

- **Preconditions:** Attack A montage authored with `ANS_Telegraph` and
  `ANS_ActiveHit`.
- **Steps:** Trigger Attack A; observe `CurrentState` transition order and
  whether the hit trace is active during `Telegraph`.
- **Expected result:** `CurrentState` reads `Telegraph` first, with no
  active hit trace, then transitions to `ActiveAttack` only after
  `ANS_Telegraph → Received Notify End`.
- **State to inspect:** debug string; `bDrawHitTraces` visualization.
- **Evidence required:** PIE recording/screenshots showing the state order
  and the absence of a drawn trace capsule during Telegraph.
- **Pass/fail rule:** PASS only if the trace is never visible before
  `CurrentState == ActiveAttack`. Any hit registered during Telegraph is a
  FAIL.

### AA-05 — Hit trace enables and disables correctly

- **Preconditions:** AA-04 passed.
- **Steps:** With `bDrawHitTraces` on, observe the capsule trace visual
  across one full Attack A cycle.
- **Expected result:** trace capsule appears only between `ANS_ActiveHit`'s
  `Received Notify Begin` and `Received Notify End`; the already-hit set is
  empty at the start of each new window.
- **State to inspect:** trace visualization; a debug print of the
  already-hit `Set of Actor` size at notify begin.
- **Evidence required:** PIE recording showing the trace window's start
  and end frames.
- **Pass/fail rule:** PASS only if the trace is invisible outside the
  notify window and the already-hit set is empty at each new window's
  start. FAIL if the trace persists after `Received Notify End` or a
  second hit registers within the same window (multi-hit).

### AA-06 — Dodge success

- **Preconditions:** Player has a working dodge with `ANS_IFrame`.
- **Steps:** Trigger Attack A; player dodges with only `State.Invulnerable`
  active (outside the tighter perfect-dodge sub-window) during the active
  trace.
- **Expected result:** 0 damage taken; no meter gained; no Impact Window
  requested.
- **State to inspect:** `BP_HealthComponent.CurrentHealth`;
  `BP_AscensionComponent.Meter`; whether `RequestImpactWindow` fired
  (should not have).
- **Evidence required:** before/after health and meter values.
- **Pass/fail rule:** PASS only if health is unchanged, meter is unchanged,
  and no Impact Window opened. Any change to any of the three is a FAIL.

### AA-07 — Perfect-dodge success

- **Preconditions:** Player's `ANS_PerfectDodge` sub-window is authored and
  nested inside `ANS_IFrame`.
- **Steps:** Trigger Attack A; player dodges such that the rival's
  `ANS_ActiveHit` trace lands while `State.PerfectWindow` is active.
- **Expected result:** 0 damage; `+12` meter (`DT_MeterGains.PerfectDodge`);
  an Impact Window is requested; if this is the first qualifying event of
  the duel, it opens at 0.75 s, otherwise 0.35–0.50 s.
- **State to inspect:** `Meter` before/after; `RequestImpactWindow` call
  and the resulting window duration; `bFirstWindowConsumed`.
- **Evidence required:** before/after meter values; screenshot of the
  Impact Window prompt with its observed duration.
- **Pass/fail rule:** PASS only if meter increases by exactly +12, an
  Impact Window opens, and its duration matches the expected
  first-vs-standard rule. Any deviation is a FAIL.

### AA-08 — Counter success

- **Preconditions:** `ANS_CounterWindow` authored on Attack A's montage;
  player has a working `IA_Counter` + `AM_Player_Counter`.
- **Steps:** Trigger Attack A; press `IA_Counter` while `State.CanCounter`
  is set (during the `ANS_CounterWindow`).
- **Expected result:** rival montage stops immediately; counter-reaction
  montage plays on the rival; `bCounteredThisAttack = true`;
  `BTTask_Recover` plays the counter-reaction branch, not the normal
  recovery; `+15` meter; an Impact Window is requested; the cycle still
  reaches `ReturnToNeutral` normally afterward.
- **State to inspect:** `bCounteredThisAttack`; `Meter`; `CurrentState`
  sequence after the counter; whether the cycle deadlocks.
- **Evidence required:** PIE recording from counter press through
  `ReturnToNeutral`; before/after meter values.
- **Pass/fail rule:** PASS only if the cycle reaches `ReturnToNeutral`
  without stranding, meter increases by exactly +15, and
  `bCounteredThisAttack` is cleared again by the next `Idle_Reposition`.
  A stranded state or a leaked `bCounteredThisAttack` flag into the next
  cycle is a FAIL.

### AA-09 — Recovery is punishable

- **Preconditions:** `ANS_Recover` authored with the incoming-damage
  multiplier hook.
- **Steps:** Land a player hit on Crimson Vanguard during `CurrentState ==
  Recover`.
- **Expected result:** the hit applies with `IncomingDamageMultiplier`
  active (a visibly different damage-application path than a hit outside
  Recover — the exact multiplier value is designer-set and not asserted
  here, only that the multiplier mechanism engages).
- **State to inspect:** `IncomingDamageMultiplier` value at the moment of
  the hit; damage applied.
- **Evidence required:** a log line or debug print showing the multiplier
  was non-default at hit time during Recover, and default outside it.
- **Pass/fail rule:** PASS only if the multiplier is measurably applied
  during Recover and reverted immediately after `ANS_Recover → Received
  Notify End`. FAIL if the multiplier never engages or never reverts.

### AA-10 — Interruption cleanup

- **Preconditions:** AA-08 passed at least once.
- **Steps:** Repeat AA-08's counter twice in a row on two separate full
  cycles (not consecutively without a `ReturnToNeutral` in between).
- **Expected result:** both cycles complete identically; no flag,
  cooldown, or state from the first counter leaks into the second.
- **State to inspect:** `bCounteredThisAttack`, `SelectedAttack`, hit-trace
  already-hit set, all confirmed clear at the start of the second cycle.
- **Evidence required:** side-by-side comparison (log or screenshots) of
  both cycles' starting state.
- **Pass/fail rule:** PASS only if the second cycle's starting state is
  identical to the first's. Any residual flag is a FAIL.

### AA-11 — Return to neutral

- **Preconditions:** none beyond a working Attack A cycle.
- **Steps:** Let Attack A run to completion with zero player interaction.
- **Expected result:** cycle reaches `ReturnToNeutral`, clears all attack
  flags, restores `Walking` movement mode, and loops back to
  `Idle_Reposition`.
- **State to inspect:** `CurrentState` sequence; `SelectedAttack`;
  character movement mode.
- **Evidence required:** PIE recording of one full untouched cycle.
- **Pass/fail rule:** PASS only if the cycle reaches `ReturnToNeutral` and
  restarts `Idle_Reposition` with no manual intervention. A stall at any
  state is a FAIL.

### AA-12 — AI resumes (guaranteed-exit failsafe)

- **Preconditions:** the montage-length failsafe timer is implemented per
  `ATTACK_A_IMPLEMENTATION_PLAN.md` §1.
- **Steps:** Temporarily break or skip `On Montage Ended` firing for one
  state (e.g. mute the montage or force an early stop without the normal
  completion event) and observe whether the task still exits.
- **Expected result:** the failsafe `Set Timer by Event` fires
  `Finish Execute(Success)` and the `Sequence` still advances.
- **State to inspect:** `CurrentState` continues to progress; no permanent
  stall.
- **Evidence required:** PIE recording showing the state advancing via
  timeout rather than the normal montage-end event.
- **Pass/fail rule:** PASS only if the cycle never permanently stalls, even
  with the normal exit path broken. A permanent stall is a FAIL and blocks
  the M2 gate outright ("Returns to Neutral every attempt").

### AA-13 — Lock-on remains valid

- **Preconditions:** player lock-on implemented per design-brief.md §4.4.
- **Steps:** Lock on to Crimson Vanguard; run it through a full Attack A
  cycle including a counter and a plain hit exchange.
- **Expected result:** lock-on target reference remains valid and camera
  tracking continues throughout every state transition; lock-on does not
  break unless the player explicitly breaks it or the target dies.
- **State to inspect:** `BP_LockOnComponent.LockedTarget`; camera
  behavior.
- **Evidence required:** PIE recording showing continuous lock-on framing
  across the full cycle.
- **Pass/fail rule:** PASS only if lock-on persists through every state and
  every branch (dodge, perfect dodge, counter, hit). Any unexplained break
  is a FAIL.

### AA-14 — Player input and locomotion restore

- **Preconditions:** a counter or perfect dodge has been triggered
  (exercises the restore path, even though the full
  `RestoreCombatState()` cinematic-burst contract is only partially
  specified per V1–V5).
- **Steps:** After a perfect dodge or counter completes and returns to live
  combat, attempt to move the player and issue a light attack.
- **Expected result:** player input (movement, light attack, dodge) is
  fully responsive immediately after the exchange — no lingering
  `State.Attacking`/`State.Invulnerable`/other stale tag blocks a new
  action.
- **State to inspect:** player's `FGameplayTagContainer` state immediately
  after the exchange; responsiveness of the next input.
- **Evidence required:** PIE recording showing an immediate, successful
  player action right after the exchange resolves.
- **Pass/fail rule:** PASS only if the player can act immediately with no
  frame of unresponsive input beyond the intended animation lock of their
  own action. A stuck/ignored input is a FAIL.

### AA-15 — Repeated trigger protection

- **Preconditions:** none beyond a working cycle.
- **Steps:** Attempt to trigger a second Impact Window request while one is
  already open (e.g., perfect-dodge twice in rapid succession).
- **Expected result:** `RequestImpactWindow` refuses the second request
  per design-brief.md §7.1 ("a window is already open" refusal condition).
- **State to inspect:** whether a second `WBP_ImpactPrompt` opens or the
  first is disturbed.
- **Evidence required:** PIE recording showing the second request refused.
- **Pass/fail rule:** PASS only if the second request is cleanly refused
  with the first window's timer undisturbed. A second window opening, or
  the first window's timer resetting, is a FAIL.

### AA-16 — Reset and replay

- **Preconditions:** a full AA-01 through AA-15 pass has been completed
  once.
- **Steps:** Without restarting PIE, repeat the entire Attack A cycle
  (including a counter and a perfect dodge) a second time end to end.
- **Expected result:** identical behavior to the first pass — no
  degradation, no leaked state, no growing error count in the Output Log.
- **State to inspect:** Output Log error/warning count before and after;
  all state flags at the start of the second pass.
- **Evidence required:** Output Log excerpt spanning both passes.
- **Pass/fail rule:** PASS only if the second pass behaves identically to
  the first with zero new errors/warnings. Any regression is a FAIL.

---

## Overall Attack A acceptance

Attack A is considered acceptance-complete for M2 only when **all 16 tests
above PASS** in the same PIE session (or a documented equivalent sequence
of sessions with no reset-losing intermediate evidence) and the completion
evidence package from `ATTACK_A_IMPLEMENTATION_PLAN.md` §11 exists. A
single FAIL blocks the M2 gate for Attack A; it does not block the CSV,
contract, or documentation work already committed on this branch.
