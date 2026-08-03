# Group 09 — Cinematic handoff corrections V1–V5

**Dispatch:** group 09 · designer seat, KIND A engineering
**Clears:** hard check 7 (cinematic handoff safety) in `cinematic-integration-inspection.md`
**Produces:** the correction text the **combat-integration-architect** will apply to
`combat-integration-plan.md`. This file **does not** edit that plan, `design-brief.md`,
or any other artifact.
**Date:** 2026-08-02 · **Ship date:** 2026-09-01

---

## 0. What this file is and is not

`cinematic-integration-inspection.md` returned **`APPROVED WITH REQUIRED CHANGES`**. Nine
of ten hard checks pass. Hard check 7 does not: five restoration/suspension steps are
**assumed rather than specified**. The inspector wrote the acceptance condition for each
and explicitly declined to repair the artifacts itself.

This file is the repair text. Each section below is **drop-in specification prose** — the
architect pastes it into the named section of `combat-integration-plan.md`. Nothing here
is advice about what should be written; it is the writing.

**Binding context carried in, not re-litigated:**

- **Q22 is APPROVED.** The Final Clash is the **only** way to win. Every one of these five
  omissions therefore sits on the only path to a victory, which is why they are worth this
  much text.
- Group 06: the Clash director **never** consults the Impact Window cooldown; a beat only
  accepts a press that **begins after** it opens; the rival is parked on
  `BTTask_WaitIndefinite` for the Clash duration; Q20 sets both beats to **0.50 s**;
  Q21 separation is **1200 cm**, `Teleport = true`, applied **under the camera cut**.
- Group 03: `BP_ImpactWindowDirector` carries `bFirstWindowConsumed`, which skips the
  cooldown check for the first window.
- Group 05: the `CosmeticMontagePlayRate` guard is **scoped to the player kit**; the
  rival's `TelegraphScale` / `RecoverScale` legitimately use play rate.

**Preserved property.** The inspector's own summary is the constraint on this file:

> *"The single-restore-function design is exactly right, which is why the omissions matter:
> one spec fix repairs every branch at once."*

Every correction below is written as **one fix inside one function**, or as one shared
mechanism both directors call. Where a per-branch statement is genuinely required (V4's
montage-cleanup ledger), it is a **declaration of existing behaviour**, not a second code
path.

**No number in this file changes a GDD number.** Impact burst stays **1–3 s**. Failed
Clash stays **1 HP floor / meter to 50 / 3 s cooldown**. Impact response stays **0.75 s**
and **0.35–0.50 s**. Where a genuinely new value is needed (a camera blend time, a montage
blend-out), it is exposed as a **designer variable at an OPEN default with a proposed
range** and is marked **PROPOSED** — never settled here.

**Milestone position, stated plainly because it is what lets the build start:** applying
these five corrections is **paper work on `combat-integration-plan.md`**. They must land
**before M3 is implemented**. They **do not block the sandbox combo-buffer test, they do
not block M1, and they do not block M2.** See §*What this does not unblock* at the end.

---

## Engine facts these corrections rest on

Three verified behaviours, because two of the five corrections exist precisely because the
plan assumed one of them.

| # | Claim | Status | Consequence |
|---|---|---|---|
| E-A | An `AnimNotifyState` is *nominally* guaranteed `Received Notify Begin` → `Received Notify Tick`* → `Received Notify End`. **That guarantee breaks under montage interruption, restart of the same montage, and same-frame cancel/replay**; community reports include the end notify being delivered *late, after* the montage has already ended, and notifies being skipped entirely when another montage starts first. | **Verified as unreliable** (Epic forums, multiple threads) | **This is the direct justification for V3 and V5.** No restoration step may depend on `Received Notify End` firing. |
| E-B | `Set View Target with Blend` is a `PlayerController` function taking `New View Target`, `Blend Time`, `Blend Func`, `Blend Exp`, `bLock Outgoing`. Returning the view to the pawn is done by calling it again with the possessed pawn as `New View Target`. | **Verified** (Epic docs, UE 5.7/5.8 Blueprint API) | **V2's mechanism.** It is a `PlayerController` call, not a presentation call. |
| E-C | UE Behavior Trees are event-driven. A `Blackboard` decorator with **`Observer Aborts = Lower Priority`** on a higher-priority `Selector` child aborts a running lower-priority branch the moment the observed key changes. This is a *higher-priority abort*, distinct from the `Abort Self` decorators, `Simple Parallel` aborts, and `Stop Logic` that plan §5.2 forbids. | **Verified** (Epic docs + UE 5.8 BT quick-start) | **V1's mechanism.** It is the same mechanism `bInClash` already relies on, so V1 adds no new engine surface. |

\* `Received Notify Tick` only fires while the owning montage is actually playing. That
property is what V5 exploits.

---

## V1 — Rival AI ownership during the Impact burst

- **Kind:** A (engineering) · **Status:** **APPROVED**
- **Target:** `combat-integration-plan.md` **§3.1 row 19** (Impact success/failure
  branches) and **§5.1 step 7** (cinematic handoff); consequential additions to **§3.1
  row 13** (six-state flow), **§3.2 row 19** (acceptance), **§4** (Blackboard key list),
  and the **M3-GATE** checklist.

### The inspector's acceptance condition, quoted

> "the plan names an explicit rival-ownership mechanism for the burst (park flag, or a
> documented can't-attack-state rule), states what is suspended when a window opens
> (including "nothing," if so decided), and routes its release through
> `RestoreCombatState()`; the mechanism appears in the M3-GATE checklist."

### Why a "can't-attack-state rule" is not available

The inspector offered two shapes. Only one survives contact with the trigger set.

`RequestImpactWindow` accepts three triggers (plan §3.1 row 18):

| Trigger | Rival state when it fires |
|---|---|
| Perfect dodge | `Active Attack` — by construction: the perfect dodge is detected *by the rival's own `ANS_ActiveHit` trace* landing during `State.PerfectWindow` |
| Successful counter | Late `Telegraph` or early `Active Attack` — the `ANS_CounterWindow` span; the rival is then forced through `Recover` |
| Combo milestone (`AN_ComboFinisher`) | **Any of the six states.** The player's combo is independent of the rival's cycle. |

The third trigger destroys the can't-attack-state rule: a combo finisher can open a window
while the rival sits in `Idle / Reposition` or `Select Attack`, and 0.75 s later the burst
can begin while the rival is mid-`Telegraph`. **An explicit park flag is therefore
mandatory.** Correction 1 takes the park-flag shape the inspector named first.

### The correction text (paste into `combat-integration-plan.md`)

> #### Rival ownership during overlays — the park contract
>
> **The rival's Behavior Tree is parked by exactly one mechanism, used by both overlay
> directors.** `BB_CrimsonVanguard` carries two independent park keys:
>
> | Blackboard key | Type | Set by | Cleared by |
> |---|---|---|---|
> | `bInClash` | Bool | `BP_FinalClashDirector.InitiateClash()` | `RestoreCombatState()` |
> | `bInImpactBurst` | Bool | `BP_ImpactWindowDirector`, on the **SUCCESS** branch only, **before** the first burst montage is played | `RestoreCombatState()` |
>
> `bInImpactBurst` is a new key and the **only** new key these corrections add. It is not a
> seventh combat state, it does not appear in `E_VanguardState`, it is never written by a
> `BTTask_*`, and it is never read anywhere except by the decorator below and by
> `RestoreCombatState()`.
>
> **`BT_CrimsonVanguard` root structure — final:**
>
> ```
> Root
> └── Selector  "Rival Root"
>     ├── [Blackboard decorator: bInClash        Is Set · Observer Aborts = Lower Priority]
>     │       BTTask_WaitIndefinite
>     ├── [Blackboard decorator: bInImpactBurst  Is Set · Observer Aborts = Lower Priority]
>     │       BTTask_WaitIndefinite
>     └── [Loop (Infinite)]
>             Sequence "Attack Cycle"
>               BTTask_Idle_Reposition → BTTask_SelectAttack → BTTask_Telegraph
>               → BTTask_ActiveAttack → BTTask_Recover → BTTask_ReturnToNeutral
>             (services: BTService_UpdateCombatData, BTService_DrawDebugState)
> ```
>
> Two park branches sharing one `BTTask_WaitIndefinite` class is deliberate: a UE
> `Blackboard` decorator observes exactly one key, and two sibling branches express the OR
> using stock nodes only. Both decorators use **`Observer Aborts = Lower Priority`**, which
> is a higher-priority abort of the Attack Cycle — **not** `Abort Self`, **not** a
> `Simple Parallel` abort, and **not** `Stop Logic`. Plan §5.2's prohibition on those three
> is unchanged and still binding.
>
> **Guaranteed-exit convention, extended.** Plan §3.1 row 13 requires every `BTTask_*` to
> set `CurrentState` as its first node and to carry a montage failsafe timer. That
> convention is hereby extended: **every `BTTask_*` must also implement `Receive Abort` and
> terminate it with `Finish Abort`**, and its abort path must clear the same per-task state
> its success path clears (unbind the `On Montage Ended` delegate, invalidate the failsafe
> timer handle). A task that is aborted by the park decorator and never calls
> `Finish Abort` strands the tree exactly as a task that never calls `Finish Execute` does.
> This is the M2 failsafe rule applied to the one interruption the design actually has.
>
> **`BTTask_WaitIndefinite` is a parking task, not a state.** It is the one exception to
> the first-node convention: it **leaves `CurrentState` untouched**, so the debug string
> keeps naming the state the rival was interrupted out of, and it sets
> `bParked = true` on `BB_CrimsonVanguard` so `BTService_DrawDebugState` appends the
> suffix `[PARKED]`. It calls neither `Finish Execute` nor any timer; it is released only
> when its decorator's observed key goes false. `bParked` is display-only and is cleared in
> the same place the park keys are.

> #### The suspension ledger — what is suspended, when, and where it is released
>
> This table is the complete ownership contract. **Every "suspend" cell has a matching
> release inside `RestoreCombatState()`; there are no other suspensions anywhere in the
> game.**
>
> | Phase | Player input | Player collision | Rival BT | Camera | Time dilation | Released by |
> |---|---|---|---|---|---|---|
> | **Impact window OPEN** (prompt showing, 0.75 s first / 0.35–0.50 s standard) | **not suspended** | **not suspended** | **not suspended** | **not taken** | **not touched** | n/a — nothing was taken |
> | **Impact burst** (SUCCESS only, 1–3 s) | suspended (`Disable Input`) | left Query+Physics; traces force-closed (see V3) | **parked** via `bInImpactBurst` | Phase 1: **not taken**. M5: taken via `BP_PresentationSubsystem` | Phase 1: untouched. M5: via subsystem | `RestoreCombatState()` |
> | **Impact FAILURE** | never suspended | never suspended | never parked | never taken | never touched | `RestoreCombatState()` still runs — see idempotency rule below |
> | **Final Clash** (both beats + finisher) | combat actions suspended; `IA_Impact` left live | suspended per plan §3.1 row 22 | **parked** via `bInClash` | taken by `LS_FinalClash` | as authored | `RestoreCombatState()` |
>
> **`NOTHING IS SUSPENDED WHILE AN IMPACT WINDOW IS MERELY OPEN.`** This is a decision, not
> an omission, and it is recorded here because the inspector asked for it explicitly. The
> GDD's Impact Window is a reaction test taken *inside* live combat: the rival keeps
> attacking, the player keeps moving, the player can still be hit, and the failure branch's
> "return to combat with no extra punishment" is only meaningful if combat never stopped.
> The prompt widget is the only thing that changes. Phase 1 has no hit-stop and no time
> dilation during the window, and M5 must not add any that alters the window's duration
> (plan §2 principle 5).
>
> **Restore is idempotent and safe to call when nothing was suspended.**
> `RestoreCombatState()` runs on the Impact FAILURE branch even though that branch suspends
> nothing. Every step in the function must therefore be written so that calling it in an
> already-restored state is a **no-op that cannot punish the player**: `Enable Input` on an
> enabled controller, `Set Collision Enabled` to the value already set, `Set Movement Mode
> (Walking)` on a Walking character, `Set View Target with Blend` to the current view
> target, and the tag resync in V5 which is defined as a *resync*, not a blind clear,
> precisely so that a live dodge is not stripped of its i-frames by a restore call it never
> needed.

### How this satisfies the acceptance condition, point by point

| Acceptance clause | Where it is satisfied |
|---|---|
| "names an explicit rival-ownership mechanism for the burst" | `bInImpactBurst` Blackboard bool + second park branch under the root `Selector`, with the exact decorator settings and BT structure written out |
| "(park flag, or a documented can't-attack-state rule)" | Park flag chosen; the can't-attack-state rule is **shown to be unavailable** because `AN_ComboFinisher` can fire in any rival state |
| "states what is suspended when a window opens (including 'nothing,' if so decided)" | The suspension ledger, row 1: **nothing**, stated as a decision with its reasoning, plus the idempotency rule that makes that decision safe |
| "routes its release through `RestoreCombatState()`" | Both park keys are cleared only in `RestoreCombatState()` (see the corrected function, §*The corrected `RestoreCombatState()` specification*) |
| "the mechanism appears in the M3-GATE checklist" | Four M3-GATE lines below |

### M3-GATE checklist lines this adds

- **M3-GATE / V1-a.** With `bShowStateNames` on, trigger an Impact Window with
  `AN_ComboFinisher` while the rival is visibly in `Telegraph`. On burst start the debug
  string shows `[PARKED]`; the rival plays **no** new montage and starts **no** new attack
  for the whole burst.
- **M3-GATE / V1-b.** During the burst, the Gameplay Debugger shows
  `bInImpactBurst = true` and the tree sitting on `BTTask_WaitIndefinite`. Within one frame
  of `RestoreCombatState()` returning, `bInImpactBurst = false` and the tree is inside the
  Attack Cycle at `Idle_Reposition`.
- **M3-GATE / V1-c.** While an Impact Window is merely **open** (prompt showing, no press
  yet), the rival's debug state **continues to advance** through its cycle and the rival can
  still land a hit on the player. Nothing is parked.
- **M3-GATE / V1-d.** Abort survival: a burst triggered mid-`Telegraph` and a burst
  triggered mid-`Active Attack` both end with the rival reaching `Return to Neutral` on the
  next cycle. Repeat ten times in one PIE run with no deadlock and no stuck montage.

---

## V2 — Camera ownership restored by the single restore function

- **Kind:** A (engineering) · **Status:** **APPROVED** for the mechanism.
  **PROPOSED** for the one new blend-time value it exposes.
- **Target:** `combat-integration-plan.md` **§3.1 row 27** (the `RestoreCombatState()`
  contents list), **§2 principle 4** (the overstated claim), **§10** acceptance checklist
  line 7 (the same overstated claim), and **§8.4** (risk text).
- **Upstream note — surfaced, not edited:** `design-brief.md` **§7.5** carries the
  identical omission. Its pseudocode block lists input, collision, locomotion, tags,
  lock-on, time dilation, rival BT and the prompt widget, and **no camera step**. That is
  the origin of the defect; the plan inherited it faithfully. **This file does not edit
  `design-brief.md`.** The designer of record should decide whether §7.5's pseudocode is
  amended in place or annotated as superseded by the corrected function in
  `combat-integration-plan.md` §3.1 row 27. Filed as a question in §*Questions for the
  designer*.

### The inspector's acceptance condition, quoted

> "an explicit camera-return step is added to the single restore function's contents, and
> the §2/§10 claims match the spec exactly."

### The engineering finding that shapes the fix

**The camera-return call must not route through `BP_PresentationSubsystem`.** Plan §2
principle 5 sends "all hit-stop, camera shake, VFX, sound, and time dilation" through
subsystem wrappers that **early-return when `bPresentationEnabled` is false**. If camera
*ownership return* were added to that list, then turning presentation off — which the
M1–M5 gates require testers to do at every gate — would leave the view target stranded on
`LS_FinalClash`'s cine camera after a Clash. The player would be alive, in control, and
looking at the wrong thing.

The distinction the plan must state:

| Camera concern | Owner | Runs when `bPresentationEnabled = false`? |
|---|---|---|
| Camera **shake**, choreography, cuts, lens work | `BP_PresentationSubsystem.RequestCameraShake` and the `LS_*` sequences | **No** — correctly suppressed |
| Camera **ownership** (which actor is the view target) | `PlayerController.Set View Target with Blend`, called directly | **Yes, always** — it is control restoration, not presentation |

This is the same class of distinction the plan already makes for time dilation, except in
the opposite direction: time dilation is *set to 1.0 through the subsystem* because the
subsystem is the only thing allowed to have moved it. Nothing but the subsystem and the
Level Sequences move the camera, but the *return* has to be unconditional.

### The correction text (paste into `combat-integration-plan.md` §3.1 row 27)

> **Camera ownership.** `RestoreCombatState()` re-asserts the player's own camera as the
> view target on every branch:
>
> ```
> Get Player Controller (0)
> → Set View Target with Blend
>       New View Target = the possessed BP_PlayerFighter
>                         (its SpringArmComponent + CameraComponent are the gameplay camera)
>       Blend Time      = DA_TuningGlobals.CameraReturnBlendSeconds   ← OPEN, designer value
>       Blend Func      = VTBlend_EaseInOut
>       Blend Exp       = 2.0
>       Lock Outgoing   = false
> ```
>
> Four rules govern this step:
>
> 1. **It is called unconditionally on every branch**, including Impact FAILURE and
>    including Phase 1 where no branch ever takes the camera. When the view target is
>    already the pawn the call is a no-op, which is what makes it safe to make
>    unconditional (V1's idempotency rule).
> 2. **It is a direct `PlayerController` call, never a `BP_PresentationSubsystem` wrapper.**
>    Camera *shake* and *choreography* remain subsystem-only per §2 principle 5; camera
>    *ownership* is control restoration and must survive `bPresentationEnabled = false`.
> 3. **It never gates control return.** `Enable Input` runs earlier in the function and does
>    not wait for the blend. The GDD requires control return on a failed standard window to
>    be immediate; the blend is cosmetic and runs concurrently with live gameplay.
> 4. **It is belt-and-braces, not the primary mechanism, for the Clash.**
>    `LS_FinalClash` is authored with its Camera Cut track's **Restore State** enabled so a
>    natural finish returns the view target by itself. Restore State is **not relied upon
>    for the `OnStop` / abort path**, which is exactly the path a Clash failure takes.
>    §8.4 already routes both `OnFinished` and `OnStop` into `RestoreCombatState()`; with
>    this step added, both paths now genuinely return the camera rather than assuming the
>    sequence did.
>
> **New designer-exposed value.** `DA_TuningGlobals.CameraReturnBlendSeconds` —
> `OPEN — designer decides`. Proposed band **0.15–0.40 s**, with **0.0** legal and meaning
> "hard cut back". Two constraints on whatever value is chosen: it must be shorter than the
> failed-Clash **3 s** re-trigger cooldown so the camera has visibly settled before the
> player can be eligible again, and it must not be so long that the player is fighting
> during a moving camera. **No value is chosen here.**

### The correction text for `combat-integration-plan.md` §2 principle 4

The current sentence overstates the spec. Replace the final clause of principle 4:

> **Current (overstated):** "…exits through the single `RestoreCombatState()` function,
> which explicitly restores player input, collision, locomotion, lock-on, camera/time
> dilation, AI state, and valid combat tags."
>
> **Corrected:** "…exits through the single `RestoreCombatState()` function, whose complete
> and enumerated contents are given in §3.1 row 27: player input, capsule collision,
> locomotion mode, director-owned overlay montages, all active hit windows and hit sets,
> transient combat tags (resynced, not blindly cleared), lock-on, **camera view target**,
> time dilation, both rival park keys, and the prompt widget. The list in §3.1 row 27 is
> authoritative; no other section may claim a restoration step that is not on it."

That last sentence is the structural fix. It makes §3.1 row 27 the single source of truth
for what restore does and turns any future §2/§10 drift into a contradiction the inspector
can catch mechanically.

### The correction text for `combat-integration-plan.md` §10 checklist line 7

> **Current:** "**All control and combat states restore after cinematics** — one
> `RestoreCombatState()` covering input, collision, locomotion, lock-on, camera/time
> dilation, AI state, tags; called by all four overlay branches (§3.1 row 27, §8.4)."
>
> **Corrected:** "**All control and combat states restore after cinematics** — one
> `RestoreCombatState()` whose enumerated contents in §3.1 row 27 cover input, collision,
> locomotion, director-owned overlay montages, hit windows and hit sets, transient tags
> (resync), lock-on, camera view target, time dilation, both rival park keys
> (`bInClash`, `bInImpactBurst`) and the prompt widget; called by all four overlay branches
> plus duel start (§3.1 row 27, §8.4). **This line asserts only what §3.1 row 27
> enumerates.**"

### How this satisfies the acceptance condition, point by point

| Acceptance clause | Where it is satisfied |
|---|---|
| "an explicit camera-return step is added to the single restore function's contents" | The `Set View Target with Blend` block above, added to §3.1 row 27 and appearing in the corrected function at the end of this file |
| "…inside the single restore function so all branches inherit it" | It is a step of `RestoreCombatState()`, unconditional; no branch has its own camera code. Clash failure's existing step 1 "camera back" becomes redundant and is re-worded to "stop `LS_FinalClash`" only, so the camera is returned in exactly one place |
| "the §2/§10 claims match the spec exactly" | Both replacement paragraphs written verbatim above, plus the new rule that §3.1 row 27 is authoritative and no other section may over-claim |
| upstream note surfaced, not silently edited | `design-brief.md` §7.5 named as the origin, left untouched, raised as a designer question |

### M3-GATE checklist lines this adds

- **M3-GATE / V2-a.** After an Impact SUCCESS burst and after an Impact FAILURE, the active
  view target is the possessed `BP_PlayerFighter` (verify with `displayall
  PlayerController ViewTarget` or a debug print of `Get View Target`), and the spring-arm
  camera responds to `IA_Look` on the next frame.
- **M3-GATE / V2-b.** Repeat V2-a with `bPresentationEnabled = false`. The camera still
  returns. (This is the test that would fail if the call were routed through the
  presentation subsystem.)
- **M4-GATE / V2-c.** Fail a Final Clash. `LS_FinalClash` is stopped mid-play by
  `ClashFailure()`, and the view target is back on the pawn with input live — proving the
  `OnStop` path does not depend on the sequence's Restore State.

---

## V3 — Hitbox and trace shutdown, specified rather than assumed

- **Kind:** A (engineering) · **Status:** **APPROVED**
- **Target:** `combat-integration-plan.md` **§3.1 row 27** (restore contents),
  **§3.1 row 16** (hit detection — where the trace state lives), **risk §8.4**, and the
  **M3-GATE** checklist.

### The inspector's acceptance condition, quoted

> "either an explicit trace-termination / hit-set-clear step in restore, **or** the
> assumption is named, tested in the sandbox or an M2 case, and added to the M3-GATE
> checklist as 'no trace survives a handoff'."

### Why the answer is "both", and why the "or" branch alone is not enough

The inspector offered a choice. Engine fact **E-A** removes it: `Received Notify End` is
**not** reliable under montage interruption, same-montage restart, or same-frame
cancel/replay, and there are reported cases of the end notify arriving *after* the montage
has already ended. Every one of those conditions occurs in this game's most common Impact
trigger: a **perfect dodge fires while the rival's `ANS_ActiveHit` window is open**, and the
burst then plays a stagger montage on the rival — interrupting the attack montage that owns
the live trace.

Naming the assumption and testing it would therefore be testing a behaviour already known
to be conditional. **The correction takes the explicit-termination branch, and additionally
carries the M3-GATE line the "or" branch asked for**, because the gate line is worth having
regardless.

The structural fix is to **stop the trace state living inside the notify object at all.**

### The correction text (paste into `combat-integration-plan.md` §3.1 row 16 and row 27)

> #### Hit windows are owned by the combat component, not by the notify
>
> `ANS_ActiveHit` holds **no** trace state. It is a thin dispatcher into whichever combat
> component owns the mesh, through a new Blueprint Interface **`BPI_CombatWindows`**,
> implemented by **both** `BP_CombatComponent` (player) and `BP_VanguardCombatComponent`
> (rival). One interface, two implementations, one `ANS_ActiveHit` class for both fighters —
> the plan's anti-fork rule (§2 principle 1) is preserved, and no new component asset is
> created.
>
> ```
> BPI_CombatWindows
>   OpenHitWindow (WindowTag, OwningMontage, StartSocket, EndSocket, Damage) → WindowID (int)
>   TickHitWindow (WindowID)
>   CloseHitWindow(WindowID)
>   ForceCloseOrphanedWindows()               ← the restoration entry point AND the tick sweep
>   ResyncTransientTags()                     ← V5's entry point
> ```
>
> - `ANS_ActiveHit.Received Notify Begin` → `OpenHitWindow(...)`, caching the returned
>   `WindowID` on the notify instance.
> - `Received Notify Tick` → `TickHitWindow(WindowID)`. The sweep
>   (`Capsule Trace By Channel` on the `AttackTrace` channel, previous-frame socket →
>   current-frame socket) and the per-window `AlreadyHitActors` set both live on the
>   **component**, keyed by `WindowID`.
> - `Received Notify End` → `CloseHitWindow(WindowID)`.
>
> **`WindowID` is a monotonically increasing integer on the component.** `CloseHitWindow`
> ignores any `WindowID` that is not currently open. This makes the system immune to the
> two documented notify-end failure modes: a **late** end notify arrives with a `WindowID`
> that has already been retired and is discarded; a **missing** end notify costs nothing
> because the window is closed by force at the next boundary.
>
> #### `ForceCloseOrphanedWindows()` — the one closure rule, used in two places
>
> **A window is orphaned when its `OwningMontage` is no longer the montage playing on that
> mesh.** The test is `Get Current Active Montage` / `Montage Is Playing (OwningMontage)` on
> the component owner's `AnimInstance`. For every orphaned window the function clears the
> `AlreadyHitActors` set, stops the sweep, retires the `WindowID`, and expires the
> `bDrawHitTraces` debug geometry on the same frame so the debug view can never show a trace
> that no longer exists. It is **idempotent** and cheap — one branch per open window.
>
> **It is deliberately scoped to orphans, and never closes a window whose montage is still
> playing.** An unscoped "close everything" would be a defect, not a fix: on the Impact
> FAILURE branch nothing is suspended and the player may legitimately be mid-combo or
> mid-dodge with a live window (see V1's suspension ledger). Killing that window would whiff
> the player's punish hit — **unintended punishment**, which hard check 6 forbids and which
> the GDD's "no extra punishment" failure rule forbids by name.
>
> **Two call sites, one function:**
>
> 1. **`RestoreCombatState()`** calls it on **both** fighters through `BPI_CombatWindows`,
>    **after** the director-owned overlay montages are stopped (V4) and **before** the tag
>    resync (V5). That ordering is what makes it work: the montage-stop step is what turns
>    an interrupted attack's window into an orphan, so by the time this step runs, exactly
>    the windows that should die are the ones marked orphaned, and the windows that should
>    live — a still-playing gameplay montage on a branch that suspended nothing — are
>    untouched. The tag resync then reads a truthful set of live windows.
> 2. **The per-component tick**, as a safety net for interrupts `RestoreCombatState()` never
>    sees. The one that actually occurs is the **successful counter**, which stops the
>    rival's attack montage mid-`ANS_ActiveHit` (plan §3.1 row 9, the one legal interrupt)
>    without any overlay being involved. The tick sweep closes it on the next frame; the
>    restore call closes its cases on the **same** frame. Both matter.
>
> Between these two call sites there is **no remaining dependency on `Received Notify End`
> anywhere in the build**. Notify-end remains the normal, fast path; it is simply no longer
> load-bearing.
>
> #### Risk §8.4 amendment
>
> Add to the fallback paragraph: *"Trace shutdown does **not** rely on
> `Received Notify End` firing on an interrupted montage — that behaviour is documented as
> unreliable under montage interruption and same-montage restart. All hit-window state lives
> on the combat components behind `BPI_CombatWindows`, keyed by a monotonic `WindowID`, and
> is closed by `ForceCloseOrphanedWindows()` from two call sites: inside
> `RestoreCombatState()` (same frame, overlay branches) and on the component tick (next
> frame, the counter interrupt). Orphan scoping is mandatory: closing a window whose montage
> is still playing would whiff a legitimate player attack and constitute unintended
> punishment."*

### How this satisfies the acceptance condition, point by point

| Acceptance clause | Where it is satisfied |
|---|---|
| "an explicit trace-termination / hit-set-clear step in restore" | `ForceCloseOrphanedWindows()` on both fighters, an enumerated step of `RestoreCombatState()`, clearing sweeps **and** `AlreadyHitActors` sets |
| "or the assumption is named" | The assumption is named **and retired** — the design no longer depends on notify-end anywhere. Engine fact E-A is written into the plan's §8.4 |
| "tested in the sandbox or an M2 case" | M2 case added below (counter-interrupt mid-`ANS_ActiveHit`) — it needs no new content and can be run at M2-GATE, ahead of M3 |
| "added to the M3-GATE checklist as 'no trace survives a handoff'" | M3-GATE / V3-a, worded in exactly those terms |
| single-function property preserved | One call in one function covers all four branches; the orphan sweep covers the non-overlay interrupt the restore function was never going to see |

### M2-GATE and M3-GATE checklist lines this adds

- **M2-GATE / V3-z** *(runs before M3, which is the point).* Counter Attack A during its
  `ANS_ActiveHit` window. With `bDrawHitTraces` on, the rival's sweep geometry disappears on
  the frame the attack montage is stopped, and the player takes **no** damage from that
  attack afterwards. Repeat five times.
- **M3-GATE / V3-a — "no trace survives a handoff".** On the frame after
  `RestoreCombatState()` returns, on either branch, **zero** hit-window sweeps are open on
  either fighter: `bDrawHitTraces` shows no geometry, and a debug print of the open-window
  count on both components reads `0`.
- **M3-GATE / V3-b.** Perfect-dodge an attack so the burst begins while the rival's
  `ANS_ActiveHit` is still open. The rival's interrupted attack deals no damage at any point
  during or after the burst — no phantom hit.
- **M3-GATE / V3-c — the orphan-scoping test, and the one most likely to be got wrong.**
  Start a light combo, let `AN_ComboFinisher` open a window, then **let it expire** while the
  combo's own `ANS_ActiveHit` is still open. The player's hit **still lands and still deals
  damage.** Restore must not have closed a window whose montage was never stopped. Repeat
  with a dodge: open a window, dodge during it, let it expire mid-`ANS_IFrame` — the player
  is still invulnerable for the remainder of the authored i-frame window.

---

## V4 — Animation-state cleanup and the death-during-overlay edge

- **Kind:** A (engineering) for parts 1–3 · **PROPOSED** for one carved-out sub-question in
  part 4.
- **Status:** **APPROVED** — the montage-cleanup ledger, the recorded-overlay-montage stop
  in restore, and the terminal-death rule. **PROPOSED** — whether a same-frame Impact
  success is shown before the Loss screen (see part 4).
- **Target:** `combat-integration-plan.md` **§3.1 rows 19, 22, 27**; **§3.2 rows 10, 19,
  22, 23**; the **M3-GATE** and **M4-GATE** checklists.

### The inspector's acceptance condition, quoted

> "each overlay branch states its montage-cleanup rule (natural completion vs. explicit
> stop), and a single stated rule resolves `OnDeath` during any overlay (surfaced to the
> designer if it needs a design decision)."

### Part 1 — the montage-cleanup ledger (declaration, not new code paths)

This table states behaviour that already exists across the branches. It is added to the plan
so that "the burst montages end naturally" stops being an unstated assumption.

> #### Overlay montage cleanup — per branch
>
> | Branch | Player-side montage | Rival-side montage | Cleanup rule | Who calls `RestoreCombatState()` |
> |---|---|---|---|---|
> | **Impact FAILURE** (window expired, or aborted) | none started by the director | none started by the director | **Nothing is stopped.** The director owns no montage on this branch, and any gameplay montage still playing is the player's own and must be left alone — stopping it would be punishment on a branch the GDD defines as unpunished | `OnWindowExpired`, immediately |
> | **Impact SUCCESS** (the 1–3 s burst) | `AM_ImpactBurst_Player` (name cosmetic, `OPEN`) | `AM_ImpactBurst_Vanguard` stagger/knockback (name cosmetic, `OPEN`) | **Natural completion is the normal path.** Before playing the pair, the director explicitly stops each fighter's in-flight *combat* montage so the burst is not fighting for the slot and the interrupted attack's hit window is orphaned (V3). Restore's recorded-montage stop then covers the abnormal path | `On Montage Ended` (Completed **or** Interrupted) of the **player's** burst montage — one authoritative end signal, not two |
> | **Clash SUCCESS** | `AM_Clash_Beat1`, then `AM_Clash_Finisher` | same pair | **Natural completion.** `LS_FinalClash` `OnFinished` and the finisher's `On Montage Ended` both route to the same handler, which is guarded so it runs once | the guarded handler, before `WBP_Result` |
> | **Clash FAILURE** | **explicit `Montage Stop`** (already plan §3.1 row 23 step 1) | **explicit `Montage Stop`** | Explicit stop of both, plus `Stop` on `LS_FinalClash`, **before** restore is called. Step 1's phrase "and camera back" is deleted — the camera is returned by restore (V2), in one place | `ClashFailure()` step 7 |
> | **Duel start** | `LS_VanguardEntrance` (skippable) | — | Sequence `OnFinished` **or** the skip input, whichever comes first; both route to the same handler | the entrance handler |

### Part 2 — the restore step that covers every abnormal exit at once

Rather than teaching restore about four branches, the directors **record what they started**
and restore closes the record. One step, one function, all branches.

> #### Director-owned overlay montages
>
> Both `BP_ImpactWindowDirector` and `BP_FinalClashDirector` maintain
> `ActiveOverlayMontages` — an array of `S_OverlayMontage { Actor, AnimMontage }` — appended
> to at the moment each overlay montage is played and **only** then. Gameplay montages
> (combo, dodge, counter, rival attacks, hit reacts) are **never** recorded.
>
> `RestoreCombatState()` step: for each entry in the combined record from both directors,
> call
>
> ```
> Get Anim Instance (Actor mesh) → Montage Stop
>       In Blend Out Time = DA_TuningGlobals.OverlayStopBlendOutSeconds   ← OPEN, designer value
>       Montage           = <the recorded AnimMontage asset>
> ```
>
> then empty the record.
>
> The `Montage` pin is the whole point. `Montage Stop` with a specific montage asset stops
> **only** that montage and only if it is the one playing; passing `None` would stop
> everything and would cancel legitimate gameplay animation on the Impact FAILURE branch.
> If the overlay montage already ended naturally — the normal case — the call is a **no-op**.
> If it is still running because of an abort or a death, it stops. **One step covers natural
> completion, abort, and death, on all four branches, with no branch-specific code.**
>
> **New designer-exposed value.** `DA_TuningGlobals.OverlayStopBlendOutSeconds` —
> `OPEN — designer decides`. Proposed band **0.0–0.15 s** (0.0 = hard cut). It affects only
> the abnormal exit, since the natural path never reaches the stop. **No value is chosen
> here.**

### Part 3 — the mid-overlay death rule

**First, the load-bearing finding: once V1 and V3 are applied, player death during a burst
or a Clash cannot occur.** This is a proof, not an assurance, and it is why the rule below
is cheap:

| Damage source during an overlay | Status |
|---|---|
| A **new** rival attack | Impossible — the rival BT is parked (`bInImpactBurst` / `bInClash`, V1) and starts no montage |
| The **in-flight** rival attack that was interrupted | Impossible — its hit window is orphaned and force-closed by `ForceCloseOrphanedWindows()` (V3) |
| Environmental damage | None exists — `design-brief.md` §10.2: the arena contains **no hazards, no damage volumes, no physics objects that can affect the duel** |
| Damage authored into the burst itself | None — plan §3.1 row 19 and the meter table grant no damage during the burst |
| Rival death mid-overlay | Impossible — under **Q22 (APPROVED)** `MinHealthFloor = 1` from `BeginPlay`, lowered to 0 only by `ClashSuccess()` immediately before it applies lethal damage |

So the remaining exposure is a **same-frame race**, not a live path: the killing hit and the
overlay start resolving in the same frame, in an order the engine does not guarantee. That is
what the rule guards.

> #### Death outranks every overlay — one rule, stated once
>
> **`BP_DuelDirector` owns duel termination and it is terminal, idempotent, and higher
> priority than any overlay.**
>
> `BP_DuelDirector` holds `bDuelOver` (bool, false at duel start). On **either** fighter's
> `OnDeath`, and on nothing else, it runs this exact order:
>
> ```
> 1  if bDuelOver → return                       (idempotent; a second OnDeath does nothing)
> 2  bDuelOver = true                            (set FIRST, before anything can re-enter)
> 3  BP_ImpactWindowDirector.AbortOverlay()
> 4  BP_FinalClashDirector.AbortOverlay()
> 5  RestoreCombatState()
> 6  EndDuel(Loss)  if the player died   |   EndDuel(Win)  if the rival died
> 7  show WBP_Result
> ```
>
> `AbortOverlay()` on either director is one shared shape: close any open window or Clash
> beat **as a non-success** (no meter, no burst, no beat 2, no finisher), invalidate its
> timer handle, hide `WBP_ImpactPrompt`, clear its park key, and leave its
> `ActiveOverlayMontages` record intact so step 5 stops those montages. It is idempotent and
> safe to call when no overlay is running.
>
> **While `bDuelOver` is true:** `RequestImpactWindow` refuses, `EvaluateClashGate` returns
> false, `IA_Impact` and `IA_FinalClash` are ignored, and no new overlay may start. This is
> one more refusal condition on checks that already exist (plan §3.1 row 18 already refuses
> when "either fighter is dead" — `bDuelOver` makes that check race-proof by latching it).
>
> **Consequences, stated so nobody has to infer them:**
> - A player death mid-burst ends the duel in **Loss**. The burst does not finish.
> - A failed Final Clash still **never** kills the player and **never** restarts the duel —
>   this rule adds no damage source and changes nothing about `ClashFailure()` (plan §3.1
>   row 23 is untouched).
> - The rival's only `OnDeath` is the one `ClashSuccess()` causes, so step 6's Win branch is
>   reachable from exactly one place. Under Q22 that is the only win in the game.

### Part 4 — the one part that is a design call, and is therefore not settled here

> **`PROPOSED — designer decides.`** Step 3 aborts an in-flight Impact success **as a
> non-success**. If the killing blow and a valid `IA_Impact` press resolve on the same
> frame, the player pressed correctly and dies without seeing the burst or receiving the
> +20.
>
> The engineering is unambiguous — death is terminal and the meter is irrelevant once the
> duel is over. What is *not* an engineering question is whether the player should
> nonetheless be **shown** their earned burst before the Loss screen. Two readings:
>
> - **(a) Abort immediately (what the rule above specifies).** Cheapest, race-proof, and
>   consistent with "the only loss condition is player health zero". Recommended default.
> - **(b) Let the burst play out, then Loss.** Honours the earned input and the central
>   promise's "earned spectacle", at the cost of a 1–3 s overlay running on a dead player
>   with all the ownership questions V1–V5 just closed reopening inside it.
>
> **This dispatch recommends (a) and does not settle it.** The frequency is near-zero given
> the proof in part 3, so the value of (b) is small and its cost is the whole restoration
> contract. Filed as a question for the designer.

### How this satisfies the acceptance condition, point by point

| Acceptance clause | Where it is satisfied |
|---|---|
| "each overlay branch states its montage-cleanup rule (natural completion vs. explicit stop)" | Part 1's five-row ledger — every branch, both fighters, plus who calls restore |
| "a single stated rule resolves `OnDeath` during any overlay" | Part 3's seven-step `bDuelOver` rule on `BP_DuelDirector`, applying to **any** overlay and **either** fighter |
| "surfaced to the designer if it needs a design decision" | Part 4 — the one genuinely discretionary slice is carved out and marked **PROPOSED**; nothing else in V4 is |
| single-function property preserved | Part 2 is **one** restore step (stop the recorded overlay montages) covering natural completion, abort and death on all four branches; part 1 adds no code paths, it documents existing ones |

### M3-GATE and M4-GATE checklist lines this adds

- **M3-GATE / V4-a.** After an Impact SUCCESS burst, neither fighter is playing any montage
  that the director started, and both are back in the locomotion state machine. After an
  Impact FAILURE, any gameplay montage that was playing when the window expired **is still
  playing and completes normally.**
- **M3-GATE / V4-b.** Force a player death during a burst (temporarily lower player max
  health, or drive `OnDeath` from the debug panel). The duel ends in **Loss** exactly once,
  the burst montages are stopped, the prompt is hidden, `bInImpactBurst` is false, and no
  overlay can be started afterwards.
- **M4-GATE / V4-c.** Force a player death during a Clash beat. Same result: Loss once,
  `LS_FinalClash` stopped, camera back, `bInClash` false, `WBP_Result` in Loss state, and
  the duel does **not** restart.
- **M4-GATE / V4-d.** Fail a Final Clash normally. Both fighters' montages are stopped,
  `LS_FinalClash` is stopped, and the seven-step recovery runs unchanged — meter 50, rival
  at the 1 HP floor, 3 s cooldown, full control, **no player damage, no restart.**

---

## V5 — `State.Dodging` and `State.CanCounter` in the restore contract

- **Kind:** A (engineering) · **Status:** **APPROVED**
- **Target:** `combat-integration-plan.md` **§3.1 row 27 clear list**; consequential note in
  **§4** (gameplay tag table); the **M3-GATE** checklist.

### The inspector's acceptance condition, quoted

> "both are added to the clear list, or a per-tag guarantee-of-clearance is documented."

And the reason it matters, which the inspector states and which this correction takes as
binding:

> "a stale `State.CanCounter` after a handoff yields a free counter, i.e., unearned
> spectacle."

Under **Q22 (APPROVED)** that free counter is worth **+15 meter** on the only path to the
only win in the game. This is the cheapest of the five defects and the one whose failure mode
lands most directly on the central promise.

### Why "add both to the clear list" is the wrong shape of fix, and what to do instead

Taking the acceptance condition literally — appending two tag names to a blind clear list —
would fix the stale-tag case and **create a new unintended-punishment bug**, because
`RestoreCombatState()` runs on the Impact FAILURE branch, where V1's ledger says **nothing
was suspended and combat is live.**

The concrete failure: a combo finisher opens a 0.35–0.50 s window; the player dodges an
incoming attack during it (legal — nothing is suspended); the window expires;
`RestoreCombatState()` blind-clears `State.Dodging`, `State.Invulnerable` and
`State.PerfectWindow` **in the middle of the player's dodge**; the rival's strike lands for
full damage. The player is punished for a missed Impact press by losing their i-frames. That
is exactly the "no extra punishment" rule the GDD attaches to Impact failure, broken by the
fix meant to harden it. **This defect already exists in the approved clear list**
(`State.Invulnerable` and `State.PerfectWindow` are already on it); adding `State.Dodging`
would widen it.

So the correction satisfies the acceptance condition's *intent* — both tags are brought
under the restore contract — by replacing the blind clear with a **resync**.

### The correction text (paste into `combat-integration-plan.md` §3.1 row 27)

> #### Transient tags are **resynced**, not blind-cleared
>
> `RestoreCombatState()` calls `ResyncTransientTags()` on **both** fighters through
> `BPI_CombatWindows` (the same interface V3 introduces). The registered transient tag set is
> **complete and closed**:
>
> `State.Attacking` · `State.Dodging` · `State.Invulnerable` · `State.PerfectWindow` ·
> `State.CanCounter` · `State.InImpactWindow` · `State.Clashing`
>
> All seven are now in the contract. `State.Dodging` and `State.CanCounter` were missing from
> the previous list and are added. `Rival.Phase2` is **not** transient — it is duel-lifetime
> state, is never cleared by restore, and is explicitly excluded here so nobody adds it later.
>
> **`ResyncTransientTags()` runs three steps, in order:**
>
> 1. **Build `DesiredTags`** = the union of the tags asserted by the component's currently
>    open windows. A window is open if it is in the component's window map and its
>    `OwningMontage` is still playing — the same authoritative registry V3 established, read
>    **after** V3's `ForceCloseOrphanedWindows()` step has already run in the same function.
> 2. **Remove** every one of the seven registered transient tags that is **not** in
>    `DesiredTags`.
> 3. **Add** every tag in `DesiredTags` that is not currently present.
>
> Because step 1 reads a registry that step V3 has just made truthful, the result is exact on
> every branch and needs no branch-specific logic:
>
> | Situation | `DesiredTags` contains | Outcome |
> |---|---|---|
> | Impact burst interrupted the rival's attack montage | nothing from that montage — its `ANS_CounterWindow` window was orphaned and closed | `State.CanCounter` **removed.** No free counter after the handoff. **This is the defect V5 exists to close.** |
> | Impact FAILURE, player mid-dodge, dodge montage still playing | `State.Dodging`, `State.Invulnerable`, and `State.PerfectWindow` if its notify is still inside its span | all three **kept.** The player keeps the i-frames they earned; no punishment |
> | Impact FAILURE, rival legitimately still counterable mid-telegraph | `State.CanCounter` | **kept.** The counter opportunity survives a failed press, which is correct — the failure branch takes nothing away |
> | Clash failure, both montages explicitly stopped | empty | **all seven removed.** Clean neutral, which is what the GDD's failed-Clash recovery asks for |
> | Any branch, nothing was ever running | empty | all seven removed; the function is a no-op on an already-clean fighter |
>
> **Belt-and-braces on the notify side.** Each tag-owning `AnimNotifyState` —
> `ANS_IFrame`, `ANS_PerfectDodge`, `ANS_CounterWindow`, `ANS_ComboLink` — re-asserts its tag
> in `Received Notify Tick` if it is missing, in addition to adding it in
> `Received Notify Begin`. `Received Notify Tick` only fires while the owning montage is
> actually playing, so this can never resurrect a tag whose montage was stopped. It costs one
> `Has Tag` branch per notify per frame and it makes the tag state self-healing against the
> notify-begin/end unreliability documented in engine fact **E-A**.
>
> **`State.Dodging`'s owner must be named.** `State.Dodging` is asserted for the **whole**
> `AM_Player_Dodge` montage, not just the i-frame span, so it needs an owning window or the
> resync will strip it: add `ANS_Dodging` spanning the full dodge montage timeline, with
> `ANS_IFrame` ⊃ `ANS_PerfectDodge` nested inside it as already specified. This is a notify
> placement, not a new mechanic, and it costs nothing at runtime. *(Related open item: the
> total length of `AM_Player_Dodge` is TODO item 48, still unanswered — `ANS_Dodging` simply
> spans whatever that length turns out to be.)*

### How this satisfies the acceptance condition, point by point

| Acceptance clause | Where it is satisfied |
|---|---|
| "both are added to the clear list" | `State.Dodging` and `State.CanCounter` are both in the now-complete seven-tag registered set that `ResyncTransientTags()` governs. Nothing is outside the contract |
| "or a per-tag guarantee-of-clearance is documented" | Also delivered: step 2 removes any registered tag with no live owning window, and the outcome table shows the guarantee holding per situation — including the exact `State.CanCounter` case the inspector called out |
| the stale-`State.CanCounter` free counter is closed | Row 1 of the outcome table; M3-GATE / V5-a below tests it directly |
| single-function property preserved | One call, one function, both fighters, all branches. The resync replaces the clear list rather than sitting beside it |
| no dependence on the assumed notify-end behaviour (the inspector links V5 to V3) | The resync reads the component window registry, not notify-end. Notify **tick** re-assertion is the only notify behaviour relied on, and it is inherently safe because tick only runs while the montage plays |

### M3-GATE checklist lines this adds

- **M3-GATE / V5-a — the free-counter test.** Trigger an Impact burst while the rival's
  `ANS_CounterWindow` is open (counter-triggered window, or a combo finisher landing during a
  rival telegraph). After `RestoreCombatState()` returns, the player does **not** hold
  `State.CanCounter`, and pressing `IA_Counter` on the next frame produces the whiff montage,
  **not** a counter and **not** +15 meter.
- **M3-GATE / V5-b — the no-punishment test.** Open a window, dodge during it, let the window
  expire mid-dodge. `State.Dodging`, `State.Invulnerable` and `State.PerfectWindow` are all
  still held for the remainder of their authored spans, and an attack landing in that
  remainder still deals **0** damage.
- **M3-GATE / V5-c.** After any overlay branch, a debug-panel dump of the seven registered
  transient tags on both fighters shows only tags whose owning notify window is verifiably
  still playing. No tag is held by an actor with no montage playing.

---

## The corrected `RestoreCombatState()` specification

This is the complete and final contents of the single restore function after V2, V3, V4 and
V5 are applied. **This is the artefact the developer builds from at M3-08.** It replaces the
body given in `combat-integration-plan.md` §3.1 row 27 and in `build-sequence.md` M3-08.

**Signature:** `RestoreCombatState()` — no parameters, on `BP_DuelDirector` (or a shared
Blueprint Function Library, as the plan already allows). **Written once. Not four copies.**

**Call sites — five, unchanged in count:** Impact SUCCESS · Impact FAILURE · Clash SUCCESS ·
Clash FAILURE · duel start. Plus, added by V4, the `bDuelOver` death handler, which is a
sixth call site and is the only addition.

**Two properties every step must satisfy:**

- **Idempotent.** Calling the function twice, or calling it when nothing was suspended, is a
  safe no-op. Required because the Impact FAILURE branch suspends nothing (V1's ledger).
- **Never punitive.** No step may cancel, shorten, or strip a legitimate in-progress gameplay
  action. This is what forces the *orphan-scoped* window closure (V3), the *recorded-montage*
  stop (V4), and the *resync* rather than blind clear (V5).

**The ordered body — order is load-bearing:**

| # | Step | Detail | Correction |
|---|---|---|---|
| 1 | **Stop director-owned overlay montages** | For each `S_OverlayMontage { Actor, AnimMontage }` in the combined `ActiveOverlayMontages` record of both directors: `Get Anim Instance → Montage Stop (In Blend Out Time = DA_TuningGlobals.OverlayStopBlendOutSeconds, Montage = <the recorded asset>)`. Then empty the record. **The `Montage` pin is never `None`** — a null pin would stop legitimate gameplay animation. Already-finished montages make this a no-op | **V4** |
| 2 | **Force-close orphaned hit windows** | `BPI_CombatWindows.ForceCloseOrphanedWindows()` on **both** fighters. Closes every window whose `OwningMontage` is no longer playing: stops the sweep, clears `AlreadyHitActors`, retires the `WindowID`, expires the debug geometry. **Scoped to orphans** — a window whose montage is still playing survives. Runs after step 1 so interrupted montages' windows are already orphaned | **V3** |
| 3 | **Resync transient tags** | `BPI_CombatWindows.ResyncTransientTags()` on **both** fighters over the closed seven-tag set — `State.Attacking`, `State.Dodging`, `State.Invulnerable`, `State.PerfectWindow`, `State.CanCounter`, `State.InImpactWindow`, `State.Clashing`. Remove any with no live owning window; add any a live window asserts. **Not a blind clear.** `Rival.Phase2` is excluded — it is duel-lifetime state | **V5** |
| 4 | **Enable input** | `Enable Input (PlayerController)`; re-enable the combat `IA_*` actions suppressed by an overlay. Runs before the camera blend and never waits for it — control return on a failed standard window must be immediate (GDD) | — |
| 5 | **Restore collision** | `Set Collision Enabled (Query and Physics)` on both capsules | — |
| 6 | **Restore locomotion** | `Set Movement Mode (Walking)` on both `CharacterMovementComponent`s | — |
| 7 | **Restore lock-on** | Re-acquire the previous target through `BP_LockOnComponent` **if lock-on was active before the overlay** (the directors record the pre-overlay lock-on target and target actor alongside `ActiveOverlayMontages`) | — |
| 8 | **Restore camera ownership** | `Get Player Controller (0) → Set View Target with Blend (New View Target = the possessed BP_PlayerFighter, Blend Time = DA_TuningGlobals.CameraReturnBlendSeconds, Blend Func = VTBlend_EaseInOut, Blend Exp = 2.0, Lock Outgoing = false)`. **A direct `PlayerController` call — never a `BP_PresentationSubsystem` wrapper**, so it survives `bPresentationEnabled = false`. Unconditional; a no-op when already on target | **V2** |
| 9 | **Restore time dilation** | `Set Global Time Dilation → 1.0` **via `BP_PresentationSubsystem` only** (unchanged — the subsystem is the only thing that ever moved it) | — |
| 10 | **Release both rival park keys** | On `BB_CrimsonVanguard`: `bInClash = false`, `bInImpactBurst = false`, `bParked = false`. Both park decorators go false, the root `Selector` falls through to the Attack Cycle, and the tree resumes | **V1** |
| 11 | **Reset the rival's displayed state** | `CurrentState = Idle_Reposition` (unchanged) | — |
| 12 | **Hide the prompt** | Hide `WBP_ImpactPrompt`; invalidate any window/beat timer handle still outstanding | — |

**What `RestoreCombatState()` must never do**, stated so the function does not grow:

- It never stops a montage it does not hold in `ActiveOverlayMontages`.
- It never closes a hit window whose owning montage is still playing.
- It never blind-clears a transient tag that a live window is still asserting.
- It never applies or removes damage, meter, or cooldown. `Meter = 50` stays where it is — in
  `ClashFailure()`, the one sanctioned direct write.
- It never decides an outcome. `EndDuel()` is `BP_DuelDirector`'s and is called *after*
  restore, never from inside it.
- It never routes camera ownership through the presentation subsystem.

---

## M3-GATE checklist additions

Every new testable line, collected. **Fourteen lines: one at M2-GATE, nine at M3-GATE, four
at M4-GATE.** The M2 line is deliberately early — it tests V3's core assumption before M3 is
implemented at all.

**M2-GATE (1 line — runs ahead of M3 on purpose)**

1. **V3-z** — Counter Attack A during its `ANS_ActiveHit` window. With `bDrawHitTraces` on,
   the rival's sweep geometry disappears on the frame the attack montage is stopped, and the
   player takes no damage from that attack afterwards. Repeat five times.

**M3-GATE (9 lines)**

2. **V1-a** — A burst triggered by `AN_ComboFinisher` while the rival is visibly in
   `Telegraph`: the debug string shows `[PARKED]`, and the rival plays no new montage and
   starts no new attack for the whole burst.
3. **V1-b** — During the burst the Gameplay Debugger shows `bInImpactBurst = true` and the
   tree on `BTTask_WaitIndefinite`. Within one frame of `RestoreCombatState()` returning,
   `bInImpactBurst = false` and the tree is at `Idle_Reposition`.
4. **V1-c** — While an Impact Window is merely **open**, the rival's debug state continues to
   advance and the rival can still hit the player. Nothing is parked.
5. **V1-d** — Ten bursts triggered mid-`Telegraph` and mid-`Active Attack` in one PIE run:
   the rival reaches `Return to Neutral` every time. No deadlock, no stuck montage.
6. **V2-a** — After both Impact branches the active view target is the possessed
   `BP_PlayerFighter` and the spring-arm camera responds to `IA_Look` on the next frame.
7. **V2-b** — Repeat V2-a with `bPresentationEnabled = false`. The camera still returns.
8. **V3-a — "no trace survives a handoff"** — On the frame after `RestoreCombatState()`
   returns, on either branch, the open-window count on both components reads `0` and
   `bDrawHitTraces` shows no geometry.
9. **V3-b** — Perfect-dodge into a burst so the rival's `ANS_ActiveHit` is open at burst
   start. The interrupted attack deals no damage during or after the burst. No phantom hit.
10. **V3-c / V5-b — the no-punishment pair** — Let a window expire while the player's own
    `ANS_ActiveHit` is open: the player's hit still lands and still deals damage. Let a window
    expire mid-dodge: `State.Dodging`, `State.Invulnerable`, `State.PerfectWindow` are all
    still held for the remainder of their authored spans and an attack in that remainder deals
    0 damage.
11. **V4-a / V4-b** — After a burst, neither fighter is playing a director-started montage;
    after an Impact FAILURE any gameplay montage still playing completes normally. Force a
    player death mid-burst: Loss fires exactly once, burst montages stopped, prompt hidden,
    `bInImpactBurst` false, no overlay can start afterwards.
12. **V5-a — the free-counter test** — Trigger a burst while the rival's `ANS_CounterWindow`
    is open. After restore the player does not hold `State.CanCounter`; `IA_Counter` on the
    next frame produces the whiff montage, not a counter and not +15.
13. **V5-c** — A debug dump of the seven registered transient tags on both fighters after any
    overlay shows only tags whose owning notify window is verifiably still playing.

**M4-GATE (4 lines)**

14. **V2-c** — Fail a Final Clash: `LS_FinalClash` is stopped mid-play and the view target is
    back on the pawn with input live, proving the `OnStop` path does not depend on the
    sequence's Restore State.
15. **V4-c** — Force a player death during a Clash beat: Loss once, `LS_FinalClash` stopped,
    camera back, `bInClash` false, `WBP_Result` in Loss, and the duel does **not** restart.
16. **V4-d** — Fail a Final Clash normally: both montages stopped, sequence stopped, and the
    seven-step recovery unchanged — meter 50, rival at the 1 HP floor, 3 s cooldown, full
    control, no player damage, no restart.
17. **V1/V5 combined** — After a failed Clash, all seven transient tags are clear on both
    fighters, both park keys are false, and the rival re-enters the Attack Cycle at
    `Idle_Reposition`.

---

## Questions for the designer

Four items this dispatch could not settle on its own authority. None blocks M1, M2, or the
sandbox test.

| # | Question | Kind | Status | Needed by |
|---|---|---|---|---|
| 1 | **`CameraReturnBlendSeconds`** — the blend time on restore's `Set View Target with Blend`. Proposed band **0.15–0.40 s**, with **0.0** legal (hard cut). Must be shorter than the failed-Clash 3 s cooldown and must not have the player fighting under a moving camera. **No value chosen here.** Needs a `TODO.md` item and a Q id assigned by the commander | B | **PROPOSED** | M3-08 |
| 2 | **`OverlayStopBlendOutSeconds`** — the blend-out on restore's recorded-montage stop. Proposed band **0.0–0.15 s** (0.0 = hard cut). Affects only the abnormal exit; the natural path never reaches the stop. **No value chosen here.** Needs a `TODO.md` item and a Q id | B | **PROPOSED** | M3-08 |
| 3 | **Same-frame death versus an earned Impact success** (V4 part 4) — abort the burst immediately, or let it play and then show Loss. This dispatch recommends **abort immediately** and does not settle it. Near-zero frequency given V4 part 3's proof | B | **PROPOSED** | M3-08, but the recommended default is safe to build against |
| 4 | **`design-brief.md` §7.5** carries the same camera omission as the plan (V2's upstream note). Amend §7.5's pseudocode in place, or annotate it as superseded by the corrected function in `combat-integration-plan.md` §3.1 row 27? **This file did not touch `design-brief.md`** | process | **OPEN** | before the inspector re-checks the chain |

---

## What this does not unblock

Stated plainly, because it is what lets the Unreal build start today.

- **This file is a paper correction.** Nothing in it has been applied. `design-brief.md`,
  `combat-integration-plan.md`, `build-sequence.md`, `inspection.md`,
  `cinematic-integration-inspection.md`, `TODO.md` and `design/decisions.md` are all
  **unmodified** by this dispatch. The only file written is
  `design/group-09-cinematic-corrections.md`.
- **The combat-integration-architect must apply these five corrections** to
  `combat-integration-plan.md` — §3.1 rows 13, 16, 19, 22, 27; §3.2 rows 10, 19, 22, 23; §2
  principle 4; §4's Blackboard key list and gameplay tag table; §5.1 step 7; §5.2's
  cross-links; §8.4; and §10 checklist line 7. Applying them is the architect's job, not
  this dispatch's. Until they are applied, hard check 7 is still failing.
- **The human designer must accept them** before M3 implementation is signed off — the
  inspector's condition, unchanged: *"corrections 1–5 must be accepted by the human designer
  before M3 implementation is signed off."*
- **M1 and M2 may proceed now, regardless.** Every mechanism above lives in M3-07 / M3-08 or
  later. The one exception cuts the right way: **M2-GATE / V3-z** is a new *test* on content
  M2 already builds, and it is worth running early precisely because it retires the
  notify-end assumption before M3 depends on it. Two forward-looking notes for the M1/M2
  builder, neither of which adds work:
  - **M2:** author the six `BTTask_*` with `Receive Abort` → `Finish Abort` from the start.
    Retrofitting abort handling onto six tasks after M3 is more expensive than writing it
    once, and V1's park decorator will abort them.
  - **M1:** when `ANS_ActiveHit` and the tag-owning notifies are first authored, put the
    window state on the combat component behind `BPI_CombatWindows` rather than on the notify
    object. Same amount of work at M1; a rewrite if it is deferred to M3.
- **The sandbox combo-buffer test is untouched** and may be run at any time.
- **Nothing here changes a GDD number.** Impact burst **1–3 s**; failed Clash **1 HP floor /
  meter to 50 / 3 s cooldown**; Impact response **0.75 s** and **0.35–0.50 s**; Clash beats
  **0.50 s** (Q20, PROPOSED); separation **1200 cm** (Q21, PROPOSED). Two new *implementation*
  values are exposed at OPEN defaults with proposed bands and are the designer's.
- **Nothing here adds a game feature.** One Blackboard bool (`bInImpactBurst`), one
  display-only bool (`bParked`), one Blueprint Interface (`BPI_CombatWindows`), one notify
  placement (`ANS_Dodging`), and one termination latch (`bDuelOver`) — all of them
  specification plumbing for behaviour the approved plan already claims to have. Scope lock
  holds: one player, one authored rival, one arena, one shared framework, four attacks,
  one duel with a win and a loss. **No runtime AI-model calls.**

---

*End of group 09. Five corrections: V1, V2, V3 and V5 **APPROVED**; V4 **APPROVED** except
for one carved-out **PROPOSED** sub-question. Two new implementation values exposed as
`OPEN — designer decides`. The single-restore-function property is preserved: one spec fix
repairs every branch at once.*
