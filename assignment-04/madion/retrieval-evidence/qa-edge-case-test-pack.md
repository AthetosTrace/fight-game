# Retrieval Evidence — `qa-edge-case-test-pack.md`

Copy only. Full generated output: `../outputs/qa-edge-case-test-pack.md`.

---

## QUERY

> How does a tester prove, repeatably and in PIE, that the five open cinematic-restoration defects (V1–V5) are fixed and that every overlay branch — failed Impact Window, failed Final Clash, death mid-overlay, repeated triggers, boss Behavior Tree resume — returns Ascendant Impact to a valid combat state?

---

## SOURCES SELECTED — why each, and what it contributed

| Source | Why selected | What it contributed |
|---|---|---|
| `cinematic-integration-inspection.md` | It is the only document that enumerates the five open restoration/ownership defects, which are the pack's primary subject | V1–V5 verbatim evidence text; the blocking-milestone assignment per defect; Q22 as human approval item 7; the mid-overlay death rule as item 12 |
| `combat-integration-plan.md` | Holds the specified contents of `RestoreCombatState()`, the Blackboard key list, the tag list, and the director refusal checks — the concrete state a tester inspects | row 27 restore list; row 23 seven-step Clash failure; row 18 refusal checks; row 21 AND-gate; row 20 Phase 2 commit point; §4 tag and Blackboard names; §7 vertical-slice beats |
| `gdd/ascendant-impact-gdd-v0.4.md` | Source of truth for every governed number and for the preserved rules the tests assert against | 0.75 s / 0.35–0.50 s window widths; 1–3 s burst; +5/+12/+15/+20/+0; meter 0–100; 1 HP floor, meter 50, 3 s cooldown; 50% and ≤25% thresholds; six state names and all timing bands |
| `build-sequence.md` | Supplies the milestone-gate structure the tests are assigned into | M2/M3/M4 gate boundaries used in the gate-assignment table |
| `assignment-04/shared/knowledge-base/core-canon.md` | Anthony's derived layer; carries the hard constraint in citable form | the no-runtime-AI-model-calls constraint used in the pack's non-goals |

---

## RETRIEVED TEXT → GENERATED OUTPUT, side by side

### Pair 1 — V1, rival AI ownership

**RETRIEVED** (`cinematic-integration-inspection.md` §2, V1):
> "the only documented mechanism that parks `BT_CrimsonVanguard` is the `bInClash` Blackboard bool → `BTTask_WaitIndefinite` branch, which applies to the **Final Clash only**. The Impact success branch plays "a montage pair on both fighters" for the GDD's 1–3 seconds, and row 19's acceptance condition says "after either branch … the rival BT is running" — implying it was somehow not running during the burst — but **no mechanism suspends the six-state Attack Cycle during the burst**. As specified, `BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst, fight the rival's stagger montage for the montage slot, and either desync the debug state display or strand the burst."

**GENERATED** (QA-V1-01):
> "**Expected result** — Throughout step 4 the rival is playing its half of the burst montage pair and its Attack Cycle is **not** progressing. `CurrentState` does not advance into `SelectAttack` or `Telegraph` at any point during the burst. After restore, the BT is running again and `CurrentState` reads `Idle_Reposition`."
>
> "**Note on the flag name.** The inspection's correction 1 accepts either "a park flag analogous to `bInClash`, or a documented rule that the burst may only play during a state that cannot start a new attack." Which mechanism ships is `OPEN — designer decides`. This test does not assume a name: read whichever mechanism the corrected plan names. If neither exists yet, the test fails at step 4 by definition."
>
> "**Fail criteria (any one)** — The state string advances mid-burst. / The stagger beat is visibly interrupted or replaced. / The two debug views disagree at any frame. / The rival attacks the player during the burst."

---

### Pair 2 — V3, trace shutdown

**RETRIEVED** (`cinematic-integration-inspection.md` §2, V3):
> "`RestoreCombatState()` never disables active attack traces or clears the per-window already-hit set. The Impact Window's most common trigger — a perfect dodge — fires **while the rival's `ANS_ActiveHit` window is open**. Trace shutdown therefore relies on `Received Notify End` firing when a montage is stopped or interrupted. That is plausible engine behavior, but it is **assumed, not specified, and not on any gate checklist**. A trace left live across the handoff produces phantom hits during or after a cinematic — a direct wound to the central promise."

**GENERATED** (QA-V3-01):
> "1. Provoke Attack A and perfect-dodge it. This is the deliberate hard case: per V3 the perfect dodge fires **while the rival's `ANS_ActiveHit` window is still open**, so the handoff begins mid-trace."
>
> "**Fail criteria** — any damage in step 4; any trace drawn from the interrupted montage; or the already-hit set still holding an entry after restore (which would suppress a legitimate later hit — the opposite failure, equally real)."
>
> "**Note.** The inspection permits an alternative acceptance: the notify-end-on-interrupt guarantee may be "named, tested in the sandbox or an M2 case, and added to the M3-GATE checklist." If that route is taken, this test **is** that checklist case. It does not become optional."

---

### Pair 3 — the Final Clash failure rules

**RETRIEVED** (`gdd/ascendant-impact-gdd-v0.4.md` Page 4, "Final Clash resolution"):
> "Failure | Separate both fighters; preserve current health with Crimson Vanguard held at a 1 HP floor; reduce meter to 50; apply a 3-second re-trigger cooldown. | Return to Neutral; rebuild meter and try again"
> "PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player automatically, or leave either fighter in a cinematic state. It creates a meaningful meter setback, restores valid combat states, and preserves a recoverable path to victory."

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 23):
> "The exact seven-step sequence, GDD numbers unchanged: stop montages/sequence + camera back → separate fighters (distance `OPEN` Q21, outside every `MinRange`) → preserve health → CV `MinHealthFloor = 1` (Q22 open: permanent vs Clash-only) → `Meter = 50` (the one sanctioned direct write) → 3 s re-trigger cooldown → `RestoreCombatState()`, rival BT re-enters at `Idle_Reposition`. Must NOT: restart duel, kill/damage player, leave anyone in a cinematic state"

**GENERATED** (QA-FC-01 state table and fail criteria):
> "| player `Health` | preserved — **unchanged** by the failure | GDD Failure row |
> | rival `Health` | preserved, floored at **1 HP** | GDD Failure row |
> | `Meter` | exactly **50** | GDD Failure row |
> | re-trigger cooldown | **3 s** | GDD Failure row |
> | duel state | still running; no Result screen | GDD PRESERVED note |"
>
> "**Fail criteria (any one)** — The duel restarts — explicitly forbidden by the GDD. / The player is killed or damaged by the failure — explicitly forbidden. / Either fighter is left in a cinematic state — explicitly forbidden. / Meter is any value other than 50. / The rival dies during the failure. / Floor behavior differs between runs."

---

### Pair 4 — Q22, the unresolved 1 HP floor

**RETRIEVED** (`cinematic-integration-inspection.md` §9 item 7):
> "**Q22 — whether the 1 HP floor is permanent from first eligibility or Clash-attempt-only** (the most consequential open value; needed before M4-08 is final) — `OPEN — designer decides`"

**GENERATED** (QA-FC-01):
> "**The 1 HP floor is UNRESOLVED — do not assume which way it goes.** Q22 asks "whether the 1 HP floor is permanent from first eligibility or Clash-attempt-only," and the inspection calls it "the most consequential open value," needed before M4-08 is final. It is `OPEN — designer decides`.
>
> This test therefore **records** floor behavior rather than asserting it. After the failed Clash, deal further damage to the rival and observe:
> - If the rival cannot drop below 1 HP by normal damage from here on, the build has implemented the **permanent** reading.
> - If the floor lifts once the Clash attempt has resolved and normal damage can finish the rival, the build has implemented the **Clash-attempt-only** reading.
>
> Record which one the build does. **Neither is a failure of this test.** The failure is a build whose behavior matches *neither* reading, or one that is inconsistent between runs."

---

### Pair 5 — the Impact Window onboarding rule

**RETRIEVED** (`gdd/ascendant-impact-gdd-v0.4.md` Page 3):
> "PRESERVED — ONBOARDING RULE  The first Impact Window is intentionally wider, but it still requires the player's input and must be earned through a successful real-time defensive action. The game does not press the input for the player and does not convert a miss into success."

**GENERATED** (QA-IW-02 and QA-IW-03):
> "**QA-IW-02 — A press before the window opens is discarded, never queued** … 2. Press `IA_Impact` **before** the window opens — during the dodge, ahead of the prompt. … **Fail criteria** — a burst plays, or **+20** is granted, without a press inside the open window."
>
> "**QA-IW-03 — Doing nothing never succeeds** … **Steps** — earn ten windows across a session. On each, press nothing at all. Record outcomes. **Expected result** — ten failures, zero bursts, zero **+20** awards. **Pass criteria** — 10/10 failures."

---

### Pair 6 — Phase 2 commit point and the unscaled active window

**RETRIEVED** (`gdd/ascendant-impact-gdd-v0.4.md` Page 5, state timing table):
> "Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s | Active frames end"

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 20):
> "`BP_DuelDirector` sets `bPhase2Pending` at `Percent <= 0.50`; **commit only in `BTTask_ReturnToNeutral`** (never mid-telegraph/mid-active); one-shot `OnPhase2Committed` signal guarded by `bPhase2` … Committing anywhere but Return to Neutral retimes an attack mid-read — a READ-pillar bug"

**GENERATED** (QA-P2-01):
> "2. Cross 50% **during** a `Telegraph`. Watch closely. 3. Confirm the in-flight attack finishes on **Phase 1** timing. 4. Confirm `bPhase2` flips only when `ReturnToNeutral` is reached."
>
> "| **`Active Attack`** | **0.18–0.45 s in BOTH phases** | GDD |"
>
> "**Fail criteria** — an attack retimes mid-flight; the signal repeats; the active window shortens in Phase 2 (the GDD sets it identical in both phases deliberately); a fifth attack appears."

---

### Pair 7 — presentation severability

**RETRIEVED** (`combat-integration-plan.md` §2 principle 5):
> "All hit-stop, camera shake, VFX, sound, and time dilation route through `BP_PresentationSubsystem` wrappers that early-return when `bPresentationEnabled` is false. Gameplay timing is driven by montage playback and `Set Timer by Event`, never through a presentation call, so disabling presentation cannot change a frame window."

**GENERATED** (QA-KS-01):
> "**Expected result** — identical timings within measurement error. All behavior tests still pass. Only visual and audio output differs."
>
> "**Fail criteria** — any measured window changes; any test that passes in one mode and fails in the other. Either indicates gameplay timing is being driven through a presentation call, which plan §2 principle 5 forbids."

---

## POST-CRITIC CORRECTION APPLIED TO THIS OUTPUT

Finding F5 in `../critic-evidence/critic-report.md`.

**RETRIEVED** (`combat-integration-plan.md` §7):
> "meter shows 32 (+12 +20)"

**GENERATED, BEFORE:**
> "| `Meter` | 32 after the +20 lands (12 + 20, plan §7) | 32 |"

**GENERATED, AFTER:**
> "| `Meter` | **starting value + 12 + 20.** Equals 32 **only if the run begins at meter 0**, which is the condition plan §7 states it under — record the starting value before step 1 rather than expecting 32 | unchanged from the burst value |"

Plus a new precondition line:
> "**Record `Meter` before step 1.** Plan §7's figure of 32 assumes a fresh run starting at 0; on any other run the expected value is the starting value plus the gains this test earns."
