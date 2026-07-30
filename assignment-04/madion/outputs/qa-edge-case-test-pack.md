QUERY: How does a tester prove, repeatably and in PIE, that the five open cinematic-restoration defects (V1–V5) are fixed and that every overlay branch — failed Impact Window, failed Final Clash, death mid-overlay, repeated triggers, boss Behavior Tree resume — returns Ascendant Impact to a valid combat state?
SOURCES READ: cinematic-integration-inspection.md, combat-integration-plan.md, build-sequence.md, gdd/ascendant-impact-gdd-v0.4.md, assignment-04/shared/knowledge-base/core-canon.md
RETRIEVED TEXT:

--- from `cinematic-integration-inspection.md` §2 (V1) ---
"**Evidence:** the only documented mechanism that parks `BT_CrimsonVanguard` is the `bInClash` Blackboard bool → `BTTask_WaitIndefinite` branch, which applies to the **Final Clash only**. The Impact success branch plays "a montage pair on both fighters" for the GDD's 1–3 seconds, and row 19's acceptance condition says "after either branch … the rival BT is running" — implying it was somehow not running during the burst — but **no mechanism suspends the six-state Attack Cycle during the burst**. As specified, `BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst, fight the rival's stagger montage for the montage slot, and either desync the debug state display or strand the burst."

--- from `cinematic-integration-inspection.md` §2 (V2) ---
"the specified `RestoreCombatState()` body restores input, collision, locomotion, tags, lock-on, time dilation, rival BT, and the prompt widget — **it contains no camera-return step.** Camera return is specified only piecemeal: Clash failure step 1 ("camera back") and §8.4's routing of `LS_FinalClash` `OnStop`/`OnFinished` into restore. Meanwhile plan §2 principle 4 and the §10 checklist claim `RestoreCombatState()` "explicitly restores … camera/time dilation" — the claim **overstates the specified function**."

--- from `cinematic-integration-inspection.md` §2 (V3) ---
"`RestoreCombatState()` never disables active attack traces or clears the per-window already-hit set. The Impact Window's most common trigger — a perfect dodge — fires **while the rival's `ANS_ActiveHit` window is open**. Trace shutdown therefore relies on `Received Notify End` firing when a montage is stopped or interrupted. That is plausible engine behavior, but it is **assumed, not specified, and not on any gate checklist**. A trace left live across the handoff produces phantom hits during or after a cinematic — a direct wound to the central promise."

--- from `cinematic-integration-inspection.md` §2 (V4) ---
"explicit `Montage Stop` exists only on the Clash **failure** path (step 1). The Impact success branch assumes the burst montage pair ends naturally before restore — unstated for interruption paths. `RequestImpactWindow` refuses when "either fighter is dead," but nothing specifies what happens if the player's health reaches zero **during** a burst or Clash beat (rival damage during overlays is presumably impossible, but that presumption is also unstated). An `OnDeath` firing mid-overlay races `EndDuel(Loss)` against `RestoreCombatState()`."

--- from `cinematic-integration-inspection.md` §2 (V5) ---
"the registered tag set (plan §4 tag table) also contains `State.Dodging` and `State.CanCounter`. Neither is in the restore clear list. `State.CanCounter` clearing relies on the rival's `ANS_CounterWindow` notify-end firing when its montage is stopped — the same assumed behavior as V3. A stale `State.CanCounter` after a handoff yields a free counter, i.e., unearned spectacle."

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3 ("Impact Windows") ---
"A qualifying real-time event—such as a perfect dodge, counter, or approved combo milestone—can open one short contextual timing prompt. Success extends the exchange into a 1–3 second choreographed burst. Failure does not auto-correct the input; the game returns immediately to normal combat."
"First Impact Window | First successful perfect dodge or counter | 0.75 seconds | No cinematic extension; return to combat with no extra punishment"
"Standard Impact Window | Approved skill event after cooldown | 0.35–0.50 seconds | No extension; return to combat"
"PRESERVED — ONBOARDING RULE  The first Impact Window is intentionally wider, but it still requires the player's input and must be earned through a successful real-time defensive action. The game does not press the input for the player and does not convert a miss into success."

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3 ("Ascension Meter") ---
"PRESERVED — METER DEFINITION  Ascension Meter is a visible 0–100 resource earned only through active combat decisions. It does not fill from waiting or elapsed time."
"Light-combo finisher +5 / Perfect dodge +12 / Successful counter +15 / Impact Window success +20 / Taking damage / waiting +0"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3–4 ("Final Clash unlock rule" / "Final Clash resolution") ---
"REVISED — SINGLE GATE  The Final Clash becomes available only when BOTH conditions are true: Ascension Meter is full at 100 AND Crimson Vanguard's health is at or below 25%. If one condition is met first, the Clash remains locked until the other is met."
"Failure | Separate both fighters; preserve current health with Crimson Vanguard held at a 1 HP floor; reduce meter to 50; apply a 3-second re-trigger cooldown. | Return to Neutral; rebuild meter and try again"
"PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player automatically, or leave either fighter in a cinematic state. It creates a meaningful meter setback, restores valid combat states, and preserves a recoverable path to victory."

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("State flow and provisional timing") ---
"Idle / Reposition → Select Attack → Telegraph → Active Attack → Recover → Return to Neutral"
"Idle / Reposition 0.60–1.20 s / 0.35–0.80 s | Select Attack 0.10–0.20 s / 0.10–0.20 s | Telegraph 0.55–0.95 s / 0.40–0.75 s | Active Attack 0.18–0.45 s / 0.18–0.45 s | Recover 0.45–0.90 s / 0.35–0.75 s | Return to Neutral 0.10–0.20 s / 0.10–0.20 s"

--- from `combat-integration-plan.md` §3.1 row 27 ---
"`RestoreCombatState()` written **once** (M3-08), called by all four overlay branches and duel start: enable input; collision Query+Physics on both capsules; `Set Movement Mode (Walking)` both; clear transient tags (`State.Attacking/.Invulnerable/.PerfectWindow/.InImpactWindow/.Clashing`); restore lock-on if it was active; time dilation → 1.0 via the subsystem; rival `bInClash = false`, `CurrentState = Idle_Reposition`, BT resumes; hide `WBP_ImpactPrompt`"

--- from `combat-integration-plan.md` §3.1 row 23 ---
"The exact seven-step sequence, GDD numbers unchanged: stop montages/sequence + camera back → separate fighters (distance `OPEN` Q21, outside every `MinRange`) → preserve health → CV `MinHealthFloor = 1` (Q22 open: permanent vs Clash-only) → `Meter = 50` (the one sanctioned direct write) → 3 s re-trigger cooldown → `RestoreCombatState()`, rival BT re-enters at `Idle_Reposition`. Must NOT: restart duel, kill/damage player, leave anyone in a cinematic state"

--- from `combat-integration-plan.md` §4 (gameplay tags) ---
"`State.Attacking`, `State.Dodging`, `State.Invulnerable`, `State.PerfectWindow`, `State.CanCounter`, `State.InImpactWindow`, `State.Clashing`, `Rival.Phase2` — registered in Project Settings, no GAS"

--- from `combat-integration-plan.md` §4 (Blackboard) ---
"`BB_CrimsonVanguard` (TargetActor, CurrentState, SelectedAttack, bPhase2, DistanceToTarget, bCounteredThisAttack, bInClash)"

--- from `combat-integration-plan.md` §3.1 row 18 ---
"refuses if window open, cooldown active (`OPEN` Q26), `bInClash`, or either fighter dead; first window 0.75 s (perfect dodge/counter only), standard 0.35–0.50 s, `bFirstWindowConsumed`"

--- from `combat-integration-plan.md` §7 (vertical slice) ---
"`RestoreCombatState()` → player input, collision, locomotion, lock-on live; rival BT resumes at `Idle_Reposition` with `CurrentState` visible; meter shows 32 (+12 +20)"

--- from `cinematic-integration-inspection.md` §9 item 7 ---
"**Q22 — whether the 1 HP floor is permanent from first eligibility or Clash-attempt-only** (the most consequential open value; needed before M4-08 is final) — `OPEN — designer decides`"

--- from `assignment-04/shared/knowledge-base/core-canon.md`, "Hard constraint" ---
"The shipped game makes **no runtime AI-model calls**. Crimson Vanguard is deterministic authored Unreal gameplay AI — a state machine / Behavior Tree. No learning, no dynamically generated attacks or choreography."

---

# QA Edge-Case Test Pack — Ascendant Impact

**Type:** implementation-support QA material. Not player-facing content.
**Audience:** whoever runs the M3-GATE and M4-GATE checklists in PIE.
**Status of every number below:** carried from the GDD or `combat-integration-plan.md` **unchanged**. Provisional and pending playtest. No test in this pack resolves an open value; where a test depends on one, it says so and branches.

## What this pack is for

`cinematic-integration-inspection.md` returned `APPROVED WITH REQUIRED CHANGES`. Nine of ten hard checks passed. Hard check 7 — cinematic handoff safety — did not, producing five open defects (V1–V5) that all live in one place: the suspend/restore ownership ledger. The inspection states they are "correctable on paper before M3," and that corrections 1–5 "must be accepted by the human designer before **M3** implementation is signed off."

Paper corrections are not proof. This pack converts each defect into a test that fails loudly if the defect is still live, so the M3 gate can be signed against observed behavior instead of an edited document.

**Scope note.** These tests exercise only systems already specified in `combat-integration-plan.md`. No test requires a fifth attack, a second arena, a second rival move set, or any deferred feature. Tests that need Attack B/C/D are marked M4 because those attacks are authored at M4 per plan §6.

## How to run every test

Common preconditions, assumed by all tests unless overridden:

- `L_ShatteredRing` open in PIE.
- `WBP_DebugPanel` open with `bShowStateNames = true` and `bDrawHitTraces = true`.
- Unreal Gameplay Debugger active (apostrophe key) showing `BB_CrimsonVanguard` keys.
- A fighter selected via `WBP_CharacterSelect`. Where a test does not name one, run it once as Echo and once as Nova — plan §3.2 row 4 requires both avatars to pass identical tests.
- `bPresentationEnabled` left at its default for the main pass; QA-KS-01 re-runs with it off.

**Two independent views of state.** Plan §3.1 row 25 specifies that the drawn debug string and the Gameplay Debugger Blackboard dump are "two independent views of the same truth — if they disagree, the convention was broken." Every test below that inspects `CurrentState` must read **both**. A disagreement is itself a failure, recorded against QA-BT-03.

---

## Group 1 — The five open restoration defects (V1–V5)

### QA-V1-01 — Rival Behavior Tree does not act during the Impact burst

**Proves:** V1 (inspection §2) — no specified mechanism suspends `BT_CrimsonVanguard` during the 1–3 s burst.
**Milestone:** M3. Blocks M3 sign-off.

**Preconditions**
- Attack A authored and live (M2 complete).
- `BP_ImpactWindowDirector` live with the first-window path available; `bFirstWindowConsumed = false`.
- Rival at full health, Phase 1, `bPhase2 = false`.
- **Record `Meter` before step 1.** Plan §7's figure of 32 assumes a fresh run starting at 0; on any other run the expected value is the starting value plus the gains this test earns.

**Steps**
1. Let the rival enter `Telegraph` on Attack A. Confirm the drawn state reads `Telegraph`.
2. Dodge so the rival's `ANS_ActiveHit` trace lands while `State.PerfectWindow` is active — a perfect dodge. Confirm damage 0 and meter +12.
3. The First Impact Window opens at **0.75 s** (GDD). Press `IA_Impact` inside it.
4. During the resulting **1–3 s** burst (GDD), watch the drawn state string and the Blackboard continuously. Do not press any input.
5. Let the burst end naturally. Observe restore.

**Expected result**
Throughout step 4 the rival is playing its half of the burst montage pair and its Attack Cycle is **not** progressing. `CurrentState` does not advance into `SelectAttack` or `Telegraph` at any point during the burst. After restore, the BT is running again and `CurrentState` reads `Idle_Reposition`.

**State values to inspect**
| Value | During burst | After restore |
|---|---|---|
| `BB_CrimsonVanguard.CurrentState` | frozen at whatever state the burst began in, or an explicit parked value | `Idle_Reposition` |
| `BB_CrimsonVanguard.SelectedAttack` | unchanged during the burst | per plan, cleared/irrelevant at Neutral |
| the burst-suspension flag (see note) | set | cleared |
| rival montage slot | burst/stagger montage only | free |
| `Meter` | **starting value + 12 + 20.** Equals 32 **only if the run begins at meter 0**, which is the condition plan §7 states it under — record the starting value before step 1 rather than expecting 32 | unchanged from the burst value |

**Note on the flag name.** The inspection's correction 1 accepts either "a park flag analogous to `bInClash`, or a documented rule that the burst may only play during a state that cannot start a new attack." Which mechanism ships is `OPEN — designer decides`. This test does not assume a name: read whichever mechanism the corrected plan names. If neither exists yet, the test fails at step 4 by definition.

**Pass criteria**
- `CurrentState` never advances to `SelectAttack` or `Telegraph` during the burst, in **both** debug views.
- No second rival montage starts during the burst.
- The rival's stagger beat plays to completion without being cut off by an attack montage.
- After restore, the BT is demonstrably running (state advances again within the Phase 1 `Idle / Reposition` band of **0.60–1.20 s**, GDD).

**Fail criteria (any one)**
- The state string advances mid-burst.
- The stagger beat is visibly interrupted or replaced.
- The two debug views disagree at any frame.
- The rival attacks the player during the burst.

---

### QA-V2-01 — Camera ownership returns to the player on every branch

**Proves:** V2 — `RestoreCombatState()` has no camera-return step, while plan §2 principle 4 and the §10 checklist claim it does.
**Milestone:** M3 for the Impact branches; M4 for the Clash branches.

**Preconditions**
- `RestoreCombatState()` implemented (M3-08).
- For the Clash rows, M4 complete with `LS_FinalClash` present.

**Steps** — run once per branch, four branches total:
1. **Impact success:** earn a window, press inside it, let the burst end.
2. **Impact failure:** earn a window, press nothing, let it expire.
3. **Clash success:** reach the double gate, initiate, hit both beats.
4. **Clash failure:** reach the double gate, initiate, miss a beat.

After each, without pressing anything for two seconds: move the mouse/right stick and then move the character.

**Expected result**
In all four cases the active view target is the player's spring-arm camera, look input rotates that camera, and movement input moves the character relative to it.

**State values to inspect**
| Value | Expected after every branch |
|---|---|
| active view target | the player pawn's camera component |
| any Level Sequence camera cut | released |
| `Get Player Controller → GetViewTarget` | the player pawn |
| look input response | camera rotates |

**Pass criteria** — all four branches return camera control, and they do so **because the single restore function returns it**, not because a Level Sequence happened to finish. Verify by inspecting where the camera-return node lives: it must be inside `RestoreCombatState()`, so all branches inherit it (inspection correction 2's acceptance condition).

**Fail criteria** — any branch leaves the camera on a sequence or on the rival; or the camera returns on the Clash paths but not on the Impact paths, which indicates the step is still piecemeal rather than in the shared function.

---

### QA-V3-01 — No hit trace survives a handoff (phantom-hit test)

**Proves:** V3 — trace shutdown relies on assumed `Received Notify End` behavior on montage interrupt; nothing clears the per-window already-hit set.
**Milestone:** M3. This is the highest-value test in the pack: the inspection calls a surviving trace "a direct wound to the central promise."

**Preconditions**
- `bDrawHitTraces = true` so sweeps are visible.
- Attack A live; the perfect-dodge path live.

**Steps**
1. Provoke Attack A and perfect-dodge it. This is the deliberate hard case: per V3 the perfect dodge fires **while the rival's `ANS_ActiveHit` window is still open**, so the handoff begins mid-trace.
2. Press `IA_Impact` inside the First Impact Window (0.75 s).
3. During the burst, watch for any drawn trace belonging to the interrupted Attack A.
4. After restore, stand still inside the rival's Attack A active range for three seconds without either fighter attacking.
5. Repeat the whole test but let the window **expire** instead (failure branch), which returns control immediately per the GDD.

**Expected result**
No trace from the interrupted attack is drawn after the handoff begins. The player takes zero damage in step 4. Health is unchanged from its value at the end of step 1.

**State values to inspect**
| Value | Expected |
|---|---|
| drawn traces during/after burst | none from the interrupted `ANS_ActiveHit` |
| player `Health` | identical before burst and after step 4 |
| per-window already-hit set | empty after restore |
| `State.Invulnerable` | cleared after restore |

**Pass criteria** — zero phantom damage on both the success and failure branch; no orphan trace drawn.

**Fail criteria** — any damage in step 4; any trace drawn from the interrupted montage; or the already-hit set still holding an entry after restore (which would suppress a legitimate later hit — the opposite failure, equally real).

**Note.** The inspection permits an alternative acceptance: the notify-end-on-interrupt guarantee may be "named, tested in the sandbox or an M2 case, and added to the M3-GATE checklist." If that route is taken, this test **is** that checklist case. It does not become optional.

---

### QA-V4-01 — Montage and animation state are clean after an interrupted overlay

**Proves:** V4, first half — explicit `Montage Stop` exists only on the Clash failure path; interruption paths are unstated.
**Milestone:** M3/M4.

**Preconditions** — Impact success path live.

**Steps**
1. Earn and convert an Impact Window so the burst begins.
2. Interrupt the burst by the means the corrected plan says is possible. If the corrected plan states the burst cannot be interrupted, record that rule and instead verify it: attempt every input (`IA_Move`, `IA_Dodge`, `IA_LightAttack`, `IA_Counter`, `IA_Impact`, `IA_FinalClash`) during the burst and confirm none of them interrupts it.
3. After restore, inspect both fighters' animation state.
4. Move, attack, and dodge. Confirm each plays from a clean base pose.

**Expected result**
Neither fighter is left in a burst pose, a partially blended montage, or a frozen frame. Locomotion drives normally from `ABP_Fighter`.

**State values to inspect**
| Value | Expected after restore |
|---|---|
| player active montage | none, or normal locomotion only |
| rival active montage | none |
| both `Movement Mode` | `Walking` (plan row 27) |
| `State.Attacking` | cleared |
| visible pose | neutral idle, not a held burst frame |

**Pass criteria** — clean base pose on both fighters; the next player action plays fully and correctly.

**Fail criteria** — a held or T-pose; a montage still playing; locomotion not driving; any input from step 2 interrupting a burst the plan says is uninterruptible.

---

### QA-V4-02 — Player death during an overlay resolves to exactly one outcome

**Proves:** V4, second half — "An `OnDeath` firing mid-overlay races `EndDuel(Loss)` against `RestoreCombatState()`." The inspection lists the mid-overlay death rule as human approval item 12, `OPEN — designer decides`.
**Milestone:** M4 (needs `EndDuel` and `WBP_Result`).

**BLOCKED-UNTIL note.** This test cannot assert a specific correct outcome until the designer sets the rule. It **can** assert that the outcome is single, deterministic, and non-stranding — which is testable now and is what V4 actually endangers.

**Preconditions**
- Player health set low enough that one rival hit is lethal (exact pool is `OPEN` Q1 — read whatever `DA_TuningGlobals` holds; do not hard-code).
- An overlay reachable: Impact burst, or a Clash beat at M4.

**Steps**
1. Enter an overlay (burst or Clash beat).
2. Cause the player's health to reach zero during it, by the means the corrected plan admits. If the plan states the player cannot take damage during an overlay, verify that instead: apply every available damage source during the overlay and confirm health does not change.
3. Observe for five seconds without input.
4. Repeat five times to check determinism.

**Expected result**
One and only one of these, the same one every time:
- `EndDuel(Loss)` runs, `WBP_Result` shows Loss, and no fighter is left in a cinematic state; **or**
- damage during overlays is impossible and health is unchanged, per an explicit stated rule.

**State values to inspect**
| Value | Expected |
|---|---|
| `EndDuel` call count | exactly 0 or exactly 1 — never 2 |
| `WBP_Result` | shown once, or not at all |
| `WBP_ImpactPrompt` | hidden |
| `State.Clashing` / `State.InImpactWindow` | cleared |
| player input enabled | true, unless the Result screen owns input |
| rival `bInClash` | false |

**Pass criteria** — identical outcome on all five runs; no stranded cinematic state; `EndDuel` never fires twice; the GDD's rule that a failed Clash "does not … kill the player automatically" is not violated by a Clash-beat death that the player did not actually take damage for.

**Fail criteria** — outcome varies between runs; both `EndDuel(Loss)` and a normal restore run; a Result screen over a still-playing burst; any stranded state.

---

### QA-V5-01 — `State.Dodging` and `State.CanCounter` are clear after every handoff

**Proves:** V5 — both are registered transient tags absent from the restore clear list; a stale `State.CanCounter` "yields a free counter, i.e., unearned spectacle."
**Milestone:** M3. The inspection rates this low effort to fix.

**Preconditions** — counter path live (`ANS_CounterWindow` on Attack A).

**Steps**
1. **Dodging route:** perfect-dodge Attack A so the handoff begins during the dodge montage; convert the Impact Window; let the burst finish.
2. Immediately after restore, read the player's tag container.
3. **CanCounter route:** provoke Attack A, wait until `ANS_CounterWindow` opens (so `State.CanCounter` is granted), then trigger the handoff — press `IA_Counter` to open the window via the counter trigger, convert it, and let the burst end.
4. After restore, press `IA_Counter` once while the rival is in a state where no counter window is open.

**Expected result**
Both tags are absent after restore. The step-4 press produces nothing — no counter, no rival interrupt, no +15.

**State values to inspect**
| Value | Expected after restore |
|---|---|
| `State.Dodging` | absent |
| `State.CanCounter` | absent |
| `State.Invulnerable` | absent |
| `State.PerfectWindow` | absent |
| `State.InImpactWindow` | absent |
| `Meter` | unchanged by the step-4 press |
| rival `CurrentState` | unaffected by the step-4 press |

**Pass criteria** — both tags absent; the free-counter press is refused; meter does not move.

**Fail criteria** — either tag present after restore; the step-4 press lands a counter or grants **+15** (GDD meter table), which is exactly the unearned spectacle V5 predicts.

---

## Group 2 — Impact Window branches

### QA-IW-01 — Failed Impact Window returns control immediately with no punishment

**Proves:** GDD Page 3 — "Failure does not auto-correct the input; the game returns immediately to normal combat," and the First Window failure result "No cinematic extension; return to combat with no extra punishment."
**Milestone:** M3.

**Preconditions** — a window earnable; note whether it will be the first (**0.75 s**) or a standard one (**0.35–0.50 s**).

**Steps**
1. Earn a window by perfect dodge. Record `Meter` at that instant (it will include **+12** for the perfect dodge).
2. Press nothing. Let the window expire.
3. The instant the prompt disappears, attempt to move, dodge, and attack.
4. Record `Meter` again and compare.
5. Confirm the standard-window cooldown began (duration is `OPEN` Q26 — read the exposed variable, do not assume a value).

**Expected result**
Control is available immediately. No burst plays. Meter gained nothing for the failure (**+0** is the GDD's explicit entry for "taking damage / waiting"). No extra damage, no stun, no lockout beyond the window cooldown.

**State values to inspect**
| Value | Expected |
|---|---|
| `Meter` before vs. after expiry | identical |
| `bWindowOpen` | false |
| `WBP_ImpactPrompt` | hidden |
| player input | enabled |
| player `Health` | unchanged by the failure itself |
| window cooldown | started |
| `bFirstWindowConsumed` | true if this was the first window |

**Pass criteria** — immediate control, zero meter change, zero added punishment.

**Fail criteria** — any input delay after expiry; any meter gain; any damage attributable to the failure; a burst playing anyway (an auto-success, which also violates the GDD onboarding rule).

---

### QA-IW-02 — A press before the window opens is discarded, never queued

**Proves:** GDD onboarding rule — "The game does not press the input for the player and does not convert a miss into success." Plan §3.1 row 6 calls this the "deliberate anti-buffer."
**Milestone:** M3.

**Steps**
1. Begin a perfect dodge.
2. Press `IA_Impact` **before** the window opens — during the dodge, ahead of the prompt.
3. Do not press again. Let the window open and expire.
4. Repeat with two and three early presses.

**Expected result** — every early press is discarded. The window expires as a failure.

**State values to inspect** — `bWindowOpen` at press time (false); `Meter` unchanged; no burst; any buffer variable holding no queued Impact press.

**Pass criteria** — no early press ever converts to success, at any press count.

**Fail criteria** — a burst plays, or **+20** is granted, without a press inside the open window.

---

### QA-IW-03 — Doing nothing never succeeds

**Proves:** GDD onboarding rule; plan §3.2 row 18 acceptance "doing nothing never succeeds."
**Milestone:** M3.

**Steps** — earn ten windows across a session. On each, press nothing at all. Record outcomes.

**Expected result** — ten failures, zero bursts, zero **+20** awards.

**Pass criteria** — 10/10 failures.
**Fail criteria** — any success, which would mean an auto-success path exists.

---

### QA-IW-04 — Repeated cinematic triggers are refused, not stacked

**Proves:** Plan §3.1 row 18 — the director "refuses if window open, cooldown active (`OPEN` Q26), `bInClash`, or either fighter dead"; and row 17's rule that any second write path to `Meter` is a defect.
**Milestone:** M3, extended at M4 for `bInClash`.

**Steps**
1. Earn a window. While it is **still open**, earn a second qualifying event (e.g. land a combo finisher, or perfect-dodge a second attack if the timing allows).
2. Observe: does a second prompt open, or does the request get refused?
3. Convert the first window. During the burst, earn another qualifying event. Observe.
4. Immediately after restore, while the window cooldown is running, earn a qualifying event. Observe.
5. At M4: while `bInClash` is true (during a Clash), earn a qualifying event. Observe.
6. Record `Meter` continuously across all five steps.

**Expected result**
Exactly one window open at any time. Exactly one **+20** per converted window. Refusals are silent and harmless — no double prompt, no stacked burst, no meter double-award, no crash.

**State values to inspect**
| Value | Expected |
|---|---|
| concurrent open windows | never more than 1 |
| `+20` awards | exactly one per converted window |
| `Meter` | moves only by the five GDD values, never twice for one event |
| `WBP_ImpactPrompt` instances | one |
| refusal during `bInClash` | request denied |

**Pass criteria** — every duplicate request refused; meter arithmetic matches the GDD table exactly across the whole run.

**Fail criteria** — two prompts at once; two bursts overlapping; **+40** from one event; a refusal that strands or crashes anything.

---

## Group 3 — Final Clash

### QA-FC-01 — Failed Final Clash performs the seven-step recovery and the duel continues

**Proves:** GDD "PRESERVED — FAILED CLASH RECOVERY" and the Failure row verbatim: separate fighters, preserve health with the rival at a **1 HP floor**, meter to **50**, **3-second** re-trigger cooldown, return to neutral. Plan §3.1 row 23. The M4 gate "explicitly fails one Clash."
**Milestone:** M4. This is the single most misreadable rule in the design.

**Preconditions** — `Meter = 100` **AND** rival health ≤ **25%** (GDD single gate). Record the rival's exact health before initiating.

**Steps**
1. Initiate the Clash with `IA_FinalClash` from neutral.
2. Deliberately miss one timing beat.
3. Observe the recovery, then verify each of the seven steps in order.
4. Play on for thirty seconds. Confirm the duel is genuinely still running.
5. Rebuild meter to 100 and attempt the Clash again. Confirm a second attempt is possible.

**Expected result** — all seven steps; the duel continues; a retry is possible.

**State values to inspect**
| Value | Expected | Source |
|---|---|---|
| montages / `LS_FinalClash` | stopped; camera back to player | plan row 23 |
| fighter separation | outside every attack's `MinRange` (distance `OPEN` Q21) | plan row 23 |
| player `Health` | preserved — **unchanged** by the failure | GDD Failure row |
| rival `Health` | preserved, floored at **1 HP** | GDD Failure row |
| `Meter` | exactly **50** | GDD Failure row |
| re-trigger cooldown | **3 s** | GDD Failure row |
| rival `CurrentState` | `Idle_Reposition` | plan row 23 |
| `bInClash` | false | plan row 27 |
| `State.Clashing` | cleared | plan row 27 |
| duel state | still running; no Result screen | GDD PRESERVED note |

**The 1 HP floor is UNRESOLVED — do not assume which way it goes.** Q22 asks "whether the 1 HP floor is permanent from first eligibility or Clash-attempt-only," and the inspection calls it "the most consequential open value," needed before M4-08 is final. It is `OPEN — designer decides`.

This test therefore **records** floor behavior rather than asserting it. After the failed Clash, deal further damage to the rival and observe:
- If the rival cannot drop below 1 HP by normal damage from here on, the build has implemented the **permanent** reading.
- If the floor lifts once the Clash attempt has resolved and normal damage can finish the rival, the build has implemented the **Clash-attempt-only** reading.

Record which one the build does. **Neither is a failure of this test.** The failure is a build whose behavior matches *neither* reading, or one that is inconsistent between runs. Once the designer answers Q22, this section becomes a hard assertion; until then it is an observation with a written result.

**Pass criteria** — meter exactly 50; rival floored at 1 HP through the failure; player took no damage from the failure; 3 s cooldown observed; full control; no restart; no player death; duel continues; retry possible; floor behavior recorded and internally consistent.

**Fail criteria (any one)**
- The duel restarts — explicitly forbidden by the GDD.
- The player is killed or damaged by the failure — explicitly forbidden.
- Either fighter is left in a cinematic state — explicitly forbidden.
- Meter is any value other than 50.
- The rival dies during the failure.
- Floor behavior differs between runs.

---

### QA-FC-02 — The Clash gate is AND, never OR

**Proves:** GDD "REVISED — SINGLE GATE … only when BOTH conditions are true … If one condition is met first, the Clash remains locked until the other is met." Plan §3.1 row 21: "The AND must never soften to OR."
**Milestone:** M4.

**Steps**
1. Reach `Meter = 100` with rival health **above 25%**. Press `IA_FinalClash`. Observe.
2. Reduce rival health to ≤ 25% with meter **below 100**. Press `IA_FinalClash`. Observe.
3. Satisfy both. Press. Observe.
4. Inspect the two HUD gate indicators in all three states.
5. Attempt initiation from a non-permitted state (mid-attack, mid-dodge). Observe.

**Expected result** — locked in states 1 and 2; available only in state 3; the two indicators honestly reflect each condition separately; initiation is player-pressed only, from neutral or the post-counter window (binding/window `OPEN` Q17/Q19).

**Pass criteria** — no Clash in state 1 or 2; Clash available in state 3; never auto-triggers.
**Fail criteria** — a Clash opens on one condition; a Clash auto-triggers at meter 100; an indicator claims eligibility that the gate does not honor.

---

## Group 4 — Boss Behavior Tree resume and loop integrity

### QA-BT-01 — The rival Behavior Tree resumes at `Idle_Reposition` after every overlay

**Proves:** Plan §3.1 row 27 — restore sets "rival `bInClash = false`, `CurrentState = Idle_Reposition`, BT resumes"; and §3.2 row 19's acceptance "after either branch … the rival BT is running." This is the direct counterpart to V1.
**Milestone:** M3 for Impact branches, M4 for Clash branches.

**Steps** — for each of the four overlay branches (Impact success, Impact failure, Clash success where applicable, Clash failure):
1. Enter and exit the branch.
2. Read `CurrentState` in both debug views immediately after restore.
3. Wait and confirm the cycle advances: `Idle_Reposition` → `SelectAttack` → `Telegraph` → `ActiveAttack` → `Recover` → `ReturnToNeutral`, in that order (GDD state flow).
4. Confirm the rival actually attacks again.
5. For Clash success specifically: the rival dies, so confirm instead that the BT is not left mid-task and that restore ran **before** the Result screen (plan §3.1 row 22).

**Expected result** — after every non-terminal branch, the tree resumes at `Idle_Reposition` and completes at least two full six-state cycles.

**State values to inspect** — `CurrentState`; `bInClash` (false); `SelectedAttack`; `bCounteredThisAttack` (cleared); `bPhase2` (unchanged by the overlay); `Movement Mode` (`Walking`); the two debug views in agreement.

**Pass criteria** — resumes at `Idle_Reposition` on all applicable branches; two clean cycles; the rival attacks again.
**Fail criteria** — the tree is stopped, parked, or stuck on `BTTask_WaitIndefinite` after a non-Clash branch; `bInClash` still true; state resumes anywhere other than `Idle_Reposition`.

---

### QA-BT-02 — The six-state loop reaches Return to Neutral on every attempt

**Proves:** Plan §3.2 row 13 acceptance — "Returns to Neutral on **every** attempt incl. countered, out-of-range, idle player"; the M2 gate. Plan §3.1 row 13: "A task that never calls `Finish Execute` strands the encounter."
**Milestone:** M2, re-run at M4 with all four attacks.

**Steps** — run each provocation at least three times:
1. Let a full attack land normally.
2. Counter the rival mid-attack.
3. Walk out of range during `Telegraph`.
4. Stand completely still for two full minutes.
5. Perfect-dodge every attack for one minute.
6. At M4: repeat 1–5 in Phase 2 (`bPhase2 = true`).
7. Leave the duel running untouched for five minutes and confirm no deadlock.

**Expected result** — every attempt reaches `ReturnToNeutral`. No deadlock in any provocation.

**State values to inspect** — `CurrentState` transitions logged in GDD order; failsafe timer fires (margin `OPEN` Q18) rather than the task hanging; `bCounteredThisAttack` cleared at Neutral; state durations inside the GDD bands for the active phase.

**Pass criteria** — 100% of attempts reach Neutral; no state exceeds its band without a failsafe firing; five minutes unattended with no deadlock.

**Fail criteria** — any attempt strands; a task never finishes; a counter leaves the rival outside the cycle; the cycle stops after any interrupt. Note plan §3.1 row 9's constraint that the counter interrupt must route *through* the sequence and never via `Abort`/`Stop Logic` — a deadlock here is the predicted symptom of that rule being broken.

---

### QA-BT-03 — The drawn state can never disagree with the executing task

**Proves:** Plan §3.1 row 25 — the first-node convention makes the display "structurally truthful"; "if they disagree, the convention was broken."
**Milestone:** M2.

**Steps** — run a five-minute duel with both views visible, including at least one of every overlay branch and one Phase 2 transition. Sample both views repeatedly, especially in the first frames after each state change and after each restore.

**Expected result** — the two views agree at every sample.

**Pass criteria** — zero disagreements.
**Fail criteria** — any disagreement; specifically a `CurrentState` that lags the actual executing task, which means some `BTTask_*` does not set `CurrentState` as its first node.

---

## Group 5 — Phase 2 and the presentation kill-switch

### QA-P2-01 — Phase 2 commits only on Return to Neutral, and signals exactly once

**Proves:** Plan §3.1 row 20 — pending at `Percent <= 0.50`, "**commit only in `BTTask_ReturnToNeutral`** (never mid-telegraph/mid-active)", one-shot signal; and row 20's risk note that committing elsewhere "retimes an attack mid-read — a READ-pillar bug." GDD: "Phase 2 Begins at 50% Crimson Vanguard health; same attacks, stronger pressure."
**Milestone:** M4.

**Steps**
1. Bring the rival to just above 50% health.
2. Cross 50% **during** a `Telegraph`. Watch closely.
3. Confirm the in-flight attack finishes on **Phase 1** timing.
4. Confirm `bPhase2` flips only when `ReturnToNeutral` is reached.
5. Count the escalation signal occurrences across the rest of the duel.
6. Repeat, crossing 50% during `ActiveAttack` and during `Recover`.
7. Measure several state durations after the commit and compare against the GDD Phase 2 bands.
8. Measure the **Active Attack** window in both phases specifically.

**Expected result** — the in-flight attack keeps Phase 1 timing; `bPhase2` flips at Neutral; the signal fires exactly once; Phase 2 bands apply afterward; the **same four attacks** are used, with no fifth attack and no transformation.

**State values to inspect**
| Value | Expected | Source |
|---|---|---|
| `bPhase2Pending` | true at ≤50% | plan row 20 |
| `bPhase2` | flips only at `ReturnToNeutral` | plan row 20 |
| escalation signal count | exactly 1 | plan row 20 |
| `Idle / Reposition` | 0.60–1.20 s → 0.35–0.80 s | GDD |
| `Telegraph` | 0.55–0.95 s → 0.40–0.75 s | GDD |
| `Recover` | 0.45–0.90 s → 0.35–0.75 s | GDD |
| **`Active Attack`** | **0.18–0.45 s in BOTH phases** | GDD |
| attack row count | exactly 4 | plan row 14 |

**Pass criteria** — commit only at Neutral, on all three crossing points; signal exactly once; Phase 2 bands hold; **the active window is unchanged between phases**.

**Fail criteria** — an attack retimes mid-flight; the signal repeats; the active window shortens in Phase 2 (the GDD sets it identical in both phases deliberately); a fifth attack appears.

---

### QA-KS-01 — Disabling presentation changes zero gameplay timing

**Proves:** Plan §2 principle 5 and §3.2 row 26 — "Disabling presentation changes zero timing (verified at every gate from M1)"; GDD implementation safeguard separating gameplay timing from presentation. Also guards the M5-stays-last rule.
**Milestone:** M1 onward, re-run at every gate.

**Steps**
1. With `bPresentationEnabled = true`, record measured durations for: `Telegraph`, `ActiveAttack`, `Recover`, the First Impact Window, a standard Impact Window, and the burst.
2. Set `bPresentationEnabled = false`.
3. Re-measure all six.
4. Re-run QA-IW-01, QA-V1-01, and QA-BT-01 with presentation off.
5. Confirm the tests still pass and the numbers still match.

**Expected result** — identical timings within measurement error. All behavior tests still pass. Only visual and audio output differs.

**State values to inspect** — the six measured durations in both modes; window widths still **0.75 s** and **0.35–0.50 s**; burst still within **1–3 s**; meter awards unchanged.

**Pass criteria** — no timing differs between modes; every referenced test passes in both.
**Fail criteria** — any measured window changes; any test that passes in one mode and fails in the other. Either indicates gameplay timing is being driven through a presentation call, which plan §2 principle 5 forbids.

---

## Coverage map

| Requirement | Tests |
|---|---|
| V1 — rival AI ownership during burst | QA-V1-01, QA-BT-01 |
| V2 — camera ownership restored | QA-V2-01 |
| V3 — hitbox/trace shutdown | QA-V3-01 |
| V4 — animation cleanup; mid-overlay death | QA-V4-01, QA-V4-02 |
| V5 — two omitted transient tags | QA-V5-01 |
| Failed Impact Window | QA-IW-01, QA-IW-02, QA-IW-03 |
| Failed Final Clash recovery | QA-FC-01, QA-FC-02 |
| Death during overlay | QA-V4-02 |
| Repeated cinematic triggers | QA-IW-04 |
| Boss Behavior Tree resume | QA-BT-01, QA-BT-02, QA-BT-03 |
| Phase 2 integrity | QA-P2-01 |
| Presentation severability | QA-KS-01 |

## Gate assignment

| Gate | Tests that must pass |
|---|---|
| M2-GATE | QA-BT-02, QA-BT-03, QA-KS-01 |
| M3-GATE | QA-V1-01, QA-V2-01 (Impact branches), QA-V3-01, QA-V4-01, QA-V5-01, QA-IW-01, QA-IW-02, QA-IW-03, QA-IW-04, QA-BT-01 (Impact branches), QA-KS-01 |
| M4-GATE | all of the above plus QA-V2-01 (Clash branches), QA-V4-02, QA-FC-01, QA-FC-02, QA-BT-01 (Clash branches), QA-P2-01 |

## Open values these tests read rather than assume

None of the following is resolved here. Each test reads the exposed variable and records it.

| Tag | Value | Affects |
|---|---|---|
| **Q22** | 1 HP floor: permanent from first eligibility, or Clash-attempt-only | QA-FC-01 — the one place this pack deliberately observes instead of asserting |
| Q1 | player health pool | QA-V4-02 |
| Q18 | BT failsafe timer margin | QA-BT-02 |
| Q21 | Clash-failure separation distance | QA-FC-01 |
| Q26 | standard Impact Window cooldown | QA-IW-01, QA-IW-04 |
| Q17 / Q19 | Clash input binding and post-counter window | QA-FC-02 |
| V1 mechanism | park flag vs. can't-attack-state rule | QA-V1-01 |
| mid-overlay death rule | approval item 12 | QA-V4-02 |

## What this pack does not do

- It does not resolve any provisional value, including Q22.
- It does not repair `combat-integration-plan.md`. The inspection's corrections 1–5 are the designer's to accept; these tests verify the result.
- It does not test deferred scope. No fifth attack, no second arena, no PvP, no per-fighter move set appears anywhere.
- It does not test presentation quality. Hit-stop feel, camera choreography, VFX authoring and sound design are M5, and QA-KS-01 exists precisely to prove they can be switched off without moving a gameplay frame.
- It does not duplicate player-facing telegraph, Impact Window beat, or environmental reaction content, which is already covered in `assignment-04/shared/knowledge-base/` and the sibling output packs.
