QUERY: For each of Crimson Vanguard's four authored attacks A–D, what does an animator need to deliver and what does an implementer need to wire, so the montage drives the six-state Behavior Tree correctly, activates and deactivates hit detection at the authored windows, respects its tracking and travel limits, and restores a valid combat state on every exit path including interruption?
SOURCES READ: combat-integration-plan.md, build-sequence.md, cinematic-integration-inspection.md, gdd/ascendant-impact-gdd-v0.4.md, assignment-04/shared/knowledge-base/core-canon.md
RETRIEVED TEXT:

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Four-attack course set") ---
"AUTHORED ATTACK | RANGE / PURPOSE | READABILITY REQUIREMENT"
"Authored attack A | Close-range committed gauntlet force | Distinct wind-up and punishable recovery"
"Authored attack B | Committed forward-pressure sequence | Visible first beat and stable tracking limit"
"Authored attack C | Armored reach and space control | Clear body direction and visible active range"
"Authored attack D | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("State flow and provisional timing") ---
"Idle / Reposition → Select Attack → Telegraph → Active Attack → Recover → Return to Neutral"
"Idle / Reposition | Face the selected fighter and maintain armored pressure | 0.60–1.20 s | 0.35–0.80 s | Valid range and line"
"Select Attack | Choose one of four authored attacks by range and cooldown | 0.10–0.20 s | 0.10–0.20 s | Attack selected"
"Telegraph | Show committed pose, warning lights, sound, and readable direction | 0.55–0.95 s | 0.40–0.75 s | Telegraph completes"
"Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s | Active frames end"
"Recover | Expose a deliberate punish opening after the committed strike | 0.45–0.90 s | 0.35–0.75 s | Recovery completes"
"Return to Neutral | Clear attack flags and restore valid locomotion | 0.10–0.20 s | 0.10–0.20 s | Neutral restored"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Behavioral intent") ---
"Crimson Vanguard advances as a large armored threat: attacks are committed rather than random, propulsion closes short gaps explosively, gauntlets communicate force, and every major offense exposes a clear recovery opening. Armor and scale may intensify presentation, but they do not remove readable counterplay."

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("REVISED — RUNTIME AI BOUNDARY") ---
"Crimson Vanguard is controlled by authored Unreal gameplay AI. The packaged duel makes no runtime LLM calls, does not learn from the player, and does not generate attacks or choreography dynamically."

--- from `build-sequence.md` M2-13 ("Author Attack A montage and its notify states") ---
"`Rival/ > Add > Animation > Animation Montage` → `AM_Vanguard_AttackA` (proxy skeleton). Lay out on the timeline (design-brief §5.1): `[ANS_Telegraph][ANS_ActiveHit][ANS_Recover]` with `ANS_CounterWindow` overlapping late telegraph / early active."
"**`ANS_Telegraph`** — Begin: `Set Blackboard CurrentState = Telegraph`, `RequestVFX` warning lights (empty in Phase 1), set emissive **red-orange** telegraph color, broadcast `OnTelegraphStart(AttackID)`; End: clear color. Attack A = long telegraph, held gauntlet pose."
"**`ANS_ActiveHit`** — reuse the M1-18 class (**same class, both fighters**)."
"**`ANS_Recover`** — Begin: `CurrentState = Recover`, raise `IncomingDamageMultiplier` (**multiplier value OPEN — §14 Q27**); Attack A = longest recover window on the montage; End: restore multiplier."
"**`ANS_CounterWindow`** — Begin: `bCounterable = true`, broadcast `OnCounterWindowOpen`; End: `bCounterable = false`."
"**Provisional GDD window ranges (*tunable, do not change*):** Telegraph **0.55–0.95 s**, Active **0.18–0.45 s**, Recover **0.45–0.90 s** (Phase 1). Per-attack float **OPEN — §14 Q25**."

--- from `build-sequence.md` M4-01 ("Author Attacks B, C, and D") ---
"`AM_Vanguard_AttackB`, `AM_Vanguard_AttackC`, `AM_Vanguard_AttackD`, each laid out like Attack A: `ANS_Telegraph`, `ANS_ActiveHit`, `ANS_Recover`, `ANS_CounterWindow`. Fill the `B/C/D` rows in `DT_VanguardAttacks` including `Phase1` and `Phase2` tuning."
"**B** (committed forward-pressure sequence) — visible first beat; **multiple separate `ANS_ActiveHit` states**, one per beat, so each beat is individually dodgeable; `ANS_TrackingLock` at a fixed point (stable tracking limit)."
"**C** (armored reach / space control) — body direction locked before active by `ANS_TrackingLock`; active-range capsule visible via the debug toggle."
"**D** (short propulsion-assisted approach) — thruster cue in `ANS_Telegraph`; root motion (or Motion Warping, **R5**) travel **hard-capped at `MaxTravelDistance`** — the cap is data, **no hidden full-arena snap**."
"**Numbers:** all window/tuning floats **OPEN — §14 Q25**, inside GDD ranges; Active window **0.18–0.45 s** *(GDD, provisional — **identical both phases, not phase-scaled**)*."

--- from `build-sequence.md` M4-02 ("Create `ANS_TrackingLock`") ---
"**Logic:** turns off the rival's rotate-to-target (facing freeze) for its duration — the "stable tracking limit" for B and C, gated by `bLockTrackingAtActive` on the row."

--- from `build-sequence.md` M2-03 ("Create `S_VanguardAttackDef`") ---
"**Fields (design-brief §5.3):** `AttackID` (`E_VanguardAttackID`), `DebugName` (Name), `Montage` (AnimMontage), `MinRange`/`MaxRange` (float — **OPEN — §14 Q10**), `Damage` (float — **OPEN — §14 Q3**), `Cooldown` (float — **OPEN — §14 Q12**), `bUsesPropulsion` (bool), `MaxTravelDistance` (float — **OPEN — §14 Q13**), `bLockTrackingAtActive` (bool), `Phase1` (`S_AttackPhaseTuning`), `Phase2` (`S_AttackPhaseTuning`)."

--- from `build-sequence.md` M2-14 ("Wire the counter interrupt through the sequence") ---
"`BP_VanguardCombatComponent → OnCountered` → `Montage Stop` the attack montage → set `bCounteredThisAttack = true` → the running task's `On Montage Ended` fires → task calls `Finish Execute (Success)` → the `Sequence` advances → `BTTask_Recover` reads `bCounteredThisAttack` and plays `AM_Vanguard_CounterReact`. Also complete the player side left open in M1-20 (stop rival montage, force rival to Recover — **the one legal external interrupt**)."

--- from `combat-integration-plan.md` §5.2 (the rival chain) ---
"**Active Attack** (0.18–0.45 s, **identical both phases by design**): `ANS_ActiveHit` sweeps sockets frame to frame; `ANS_TrackingLock` freezes facing where the row asks (B, C); attack D travels under root motion hard-capped at `MaxTravelDistance` — no hidden full-arena snap. Hits resolve through the player's `ResolveIncomingHit`."
"**Return to Neutral** (0.10–0.20 s): clear every attack flag, restore multiplier and tracking, `Set Movement Mode (Walking)`, clear montage; **then and only then** commit Phase 2 if pending (one-shot signal). The `Sequence` completes and the `Loop` restarts at step 1. Every task sets `CurrentState` first and carries a failsafe timer (Q18), so the cycle reaches Neutral on every attempt — the M2 gate."

--- from `combat-integration-plan.md` §3.1 row 16 ---
"`AttackTrace` channel (default Ignore, both meshes Block); `ANS_ActiveHit` sweeps previous-frame → current-frame socket, per-window already-hit set, one shared class for both fighters; hit → `ResolveIncomingHit` three-way branch (perfect / dodge / hit); hit reaction = shared hit-react montage in the `MontageSet` (proxy anim; tuned hit-stop feel is M5); debug draw behind `bDrawHitTraces`"

--- from `combat-integration-plan.md` §3.1 row 13 ---
"Six `BTTask_*` in GDD order (`Idle_Reposition`, `SelectAttack`, `Telegraph`, `ActiveAttack`, `Recover`, `ReturnToNeutral`); first node of every task sets `CurrentState`; every montage-waiting task carries a failsafe timer (margin `OPEN` Q18); `bInClash` branch parks the tree on `BTTask_WaitIndefinite`; no `Abort Self`, no `Simple Parallel` aborts, no `Stop Logic`"

--- from `combat-integration-plan.md` §8.2 (fallback ladder) ---
"**Fallback (ladder, cheapest first):** UE5 Mannequins on the native skeleton for both fighters (zero retargeting); Vanguard = Mannequin scaled to 208 cm + static-mesh gauntlet/shoulder proxy blocks + red/black material — ships no matter what; the Paragon heavy swap only if the schedule holds and **before** M4 range tuning."

--- from `combat-integration-plan.md` §8.7 (external plugin failure) ---
"the design's own R5 fallback is already the default — **root-motion montages with a hard distance cap** plus a pre-attack `Move To` reposition; Motion Warping is only attempted if the schedule holds at the M2 review, and only on a disposable branch first."

--- from `combat-integration-plan.md` §8.5 (attack-data mismatch) ---
"a `DT_VanguardAttacks` row and its montage drift apart — a montage missing `ANS_CounterWindow`, a `TelegraphScale` that pushes an authored window outside its GDD range, a D-row travel exceeding `MaxTravelDistance`, an active window that differs between phases."
"the check **flags, never picks**; a flagged attack is pulled from the selection filter until fixed, and the loop keeps running on the remaining rows"

--- from `cinematic-integration-inspection.md` §2 (V3, V4, V5 — restoration gaps affecting montage authoring) ---
"Trace shutdown therefore relies on `Received Notify End` firing when a montage is stopped or interrupted. That is plausible engine behavior, but it is **assumed, not specified, and not on any gate checklist**."
"explicit `Montage Stop` exists only on the Clash **failure** path (step 1)."
"`State.CanCounter` clearing relies on the rival's `ANS_CounterWindow` notify-end firing when its montage is stopped — the same assumed behavior as V3."

--- from `assignment-04/shared/knowledge-base/core-canon.md`, "The three combatants" ---
"Crimson Vanguard | Height 6'10" | Combat identity: Armor, pressure, overwhelming force | Movement: Committed advances, short propulsion | Silhouette: Substantially broader armored mass | Material family: Red armor over black structure | Energy / VFX: Red-orange systems and warning lights | Readability target: Threatening reach, obvious tells and recovery"

---

# Animation Integration Briefs — Crimson Vanguard Attacks A–D

## THIS IS A HANDOFF DOCUMENT. THE ANIMATIONS DO NOT EXIST YET.

Not one of the four montages named here has been authored. `AM_Vanguard_AttackA` is created at build step **M2-13**; `AM_Vanguard_AttackB`, `AM_Vanguard_AttackC`, and `AM_Vanguard_AttackD` at **M4-01**. Nothing in Unreal has been built at all — the project is at M1 with the build phase not yet started.

This document exists so that whoever authors those montages — animator, implementer, or both — knows the contract each one has to satisfy **before** they start, rather than discovering it at a milestone gate. Every requirement below is copied from an approved source, not invented here.

**What this document is not.** It is not a design document. It creates no attack, changes no attack, and adds no fifth attack. The four attacks, their purposes, their readability requirements, and every timing band come from the GDD; the asset names, notify classes, struct fields, and wiring come from `build-sequence.md` and `combat-integration-plan.md`. Where a value is unresolved it is marked `OPEN` with its question tag and left alone.

**Every number here is provisional and pending playtest, and belongs to the human designer.** No brief resolves one.

---

## Shared contract — applies to all four attacks

Read this section once. The per-attack briefs below only state what differs.

### The state ownership chain

Each attack is driven by three consecutive Behavior Tree tasks inside one `Sequence` under an infinite `Loop`, in GDD order:

```
BTTask_Idle_Reposition → BTTask_SelectAttack → BTTask_Telegraph
   → BTTask_ActiveAttack → BTTask_Recover → BTTask_ReturnToNeutral → (loop)
```

| Boundary | Owner | Detail |
|---|---|---|
| **Starts the attack** | `BTTask_SelectAttack` | filters `DT_VanguardAttacks` to in-range and off-cooldown rows, picks by the active phase's `SelectionWeight`, writes `SelectedAttack`, stamps cooldown |
| **Plays the montage** | `BTTask_Telegraph` | plays the row's `Montage` at `TelegraphScale` |
| **Owns active frames** | `BTTask_ActiveAttack` | the montage's `ANS_ActiveHit` window(s) do the work |
| **Owns the punish opening** | `BTTask_Recover` | `ANS_Recover` raises `IncomingDamageMultiplier` |
| **Ends the attack** | `BTTask_ReturnToNeutral` | clears every attack flag, restores multiplier and tracking, `Set Movement Mode (Walking)`, clears montage, then commits Phase 2 if pending |

**One montage spans three tasks.** This is the single most important thing for an animator to understand: the timeline is continuous, but three separate BT tasks hand off across it, and the *notify states are what tell the tree where it is*. A misplaced notify boundary is not a cosmetic error — it desynchronises the state machine.

**Convention that must not be broken:** the first node of every task sets `CurrentState`. Plan §3.1 row 25 relies on this to make the on-screen debug string "structurally truthful." Every montage-waiting task also carries a failsafe timer (margin `OPEN — Q18`).

### Notify layout, common to all four montages

Per M2-13 and M4-01, every attack montage carries the same four notify classes on one continuous timeline:

```
|<---- ANS_Telegraph ---->|<-- ANS_ActiveHit -->|<------ ANS_Recover ------>|
              |<--- ANS_CounterWindow --->|
              (overlaps late telegraph / early active)
```

| Notify | Begin does | End does |
|---|---|---|
| `ANS_Telegraph` | `CurrentState = Telegraph`; `RequestVFX` warning lights (empty until M5); set emissive **red-orange**; broadcast `OnTelegraphStart(AttackID)` | clear color |
| `ANS_ActiveHit` | **activates hit detection** — begins sweeping previous-frame → current-frame socket on the `AttackTrace` channel; opens a per-window already-hit set | **deactivates hit detection** — ends the sweep; the already-hit set closes |
| `ANS_Recover` | `CurrentState = Recover`; raise `IncomingDamageMultiplier` (`OPEN — Q27`) | restore multiplier |
| `ANS_CounterWindow` | `bCounterable = true`; broadcast `OnCounterWindowOpen` | `bCounterable = false` |

`ANS_ActiveHit` is **one class shared by both fighters** (created at M1-18, reused here). Do not author a rival-specific variant. Traces are visible in-editor behind `bDrawHitTraces`.

### Where hit detection turns on and off — and the open risk

Hit detection is activated **only** by `ANS_ActiveHit` Begin and deactivated **only** by its End. There is no separate enable call. This means:

- The animator's placement of that notify state *is* the hitbox timing. Nothing else defines it.
- The window must sit inside the GDD's **0.18–0.45 s**, and that band is **identical in Phase 1 and Phase 2 by design** — telegraph and recover are phase-scaled, the active window deliberately is not. Do not let a `TelegraphScale` or `RecoverScale` bleed onto the active section.

**Open defect V3 applies directly to this contract.** The inspection found that shutdown on an *interrupted* montage relies on `Received Notify End` firing when the montage is stopped — "plausible engine behavior, but … assumed, not specified, and not on any gate checklist." Anyone authoring these montages should treat that as unverified: if a montage stop does not fire notify-end, every attack here leaks a live trace. Test it on the first montage authored (Attack A, M2-13) rather than discovering it across four.

### Root motion, facing, and travel

| Property | Rule | Source |
|---|---|---|
| Root motion | Attacks A/B/C: authored in place or with small committed steps; the rival repositions in `Idle_Reposition` via `Move To Actor`, not inside the attack. Attack D is the only one that travels as its purpose. | GDD attack table; plan §5.2 |
| Travel cap | Enforced by `MaxTravelDistance` on the row (`OPEN — Q13`). Applies to D. "The cap is data, **no hidden full-arena snap**." | M4-01 |
| Facing | The rival rotates to target by default. `ANS_TrackingLock` **freezes facing** for its duration, gated by `bLockTrackingAtActive` on the row. Used by **B and C only**. | M4-02 |
| Motion Warping | **Not the default.** Root motion with a hard distance cap is the default; Motion Warping (R5) is optional, only if the schedule holds, only on a disposable branch first, and only with designer approval. Assume root motion. | plan §8.7 |

### Interruption and cancel behaviour — one legal interrupt, and no others

**The counter is the only legal mid-attack interrupt.** It must route *through* the `Sequence`, never via `Abort Self`, `Simple Parallel` aborts, or `Stop Logic` — plan §3.1 row 13 forbids all three, and §3.1 row 9 calls routing through the sequence the "deadlock defense."

The exact chain (M2-14):

```
OnCountered → Montage Stop (the attack montage) → bCounteredThisAttack = true
  → the running task's On Montage Ended fires → task calls Finish Execute (Success)
  → the Sequence advances → BTTask_Recover reads bCounteredThisAttack
  → plays AM_Vanguard_CounterReact instead of the normal recover
```

Consequences for authoring:

- **Every attack montage must be safely stoppable at any frame.** A counter can land during late telegraph or early active — wherever `ANS_CounterWindow` is open.
- **The montage must not be the only thing clearing state.** If `Montage Stop` fires mid-`ANS_ActiveHit`, notify-end must clear the trace (V3) and mid-`ANS_CounterWindow`, notify-end must clear `bCounterable` and the player's `State.CanCounter` (V5). Both are currently assumed, not specified.
- **No self-cancel, no attack-into-attack cancel, no dodge-cancel for the rival.** Plan §5.2 step 5: "No cancel, no new attack" during Recover. The GDD's whole readability contract is that attacks are "committed rather than random."

### What happens if the montage ends early

Three cases, all of which must leave a valid state:

| Case | What happens | Guarantee |
|---|---|---|
| **Counter interrupt** | `Montage Stop` → `On Montage Ended` → `Finish Execute (Success)` → Sequence advances to Recover → `AM_Vanguard_CounterReact` | the one legal interrupt; rival still reaches Return to Neutral |
| **Montage ends unexpectedly / notify never fires** | the task's **failsafe timer** (`OPEN — Q18`) fires and the task exits anyway | plan §3.1 row 13: "A task that never calls `Finish Execute` strands the encounter" — the failsafe is the defense, and reaching Neutral on *every* attempt is the M2 gate |
| **Overlay takes over** (Impact burst, Final Clash) | the attack is displaced by the overlay; exit runs through `RestoreCombatState()` | subject to open defects V1 and V4 — see the caveat below |

**Authoring implication:** never rely on a notify firing to clear state that matters. Anything that must be true at Return to Neutral is cleared by `BTTask_ReturnToNeutral` regardless of how the montage ended.

### How locomotion, collision, AI state, and control are restored

Two different paths, and they must not be confused.

**Normal path — `BTTask_ReturnToNeutral`** (0.10–0.20 s, both phases). Clears every attack flag, restores `IncomingDamageMultiplier` and tracking, `Set Movement Mode (Walking)`, clears the montage, then commits Phase 2 if pending as a one-shot. This is the ordinary end of every attack.

**Overlay path — `RestoreCombatState()`**, called by all four overlay branches. Per plan §3.1 row 27 it enables input, sets collision to Query+Physics on both capsules, sets `Walking` on both, clears the five listed transient tags, restores lock-on, returns time dilation to 1.0, sets rival `bInClash = false` and `CurrentState = Idle_Reposition` with the BT resuming, and hides `WBP_ImpactPrompt`.

> **Caveat carried from `cinematic-integration-inspection.md` — five open defects touch this.** `RestoreCombatState()` as specified does **not** restore camera ownership (V2), does **not** terminate active hit traces or clear the already-hit set (V3), does **not** specify montage/animation cleanup on interruption paths (V4), and omits `State.Dodging` and `State.CanCounter` from its clear list (V5). Separately, **no mechanism is specified that suspends the rival's Attack Cycle during the 1–3 s Impact burst** (V1) — meaning as currently written, `BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst and fight the stagger montage for the montage slot.
>
> Corrections 1–5 must be accepted by the human designer **before M3 sign-off**. Anyone authoring these montages before that happens should assume the restore contract is still incomplete and not design around it. The QA pack in this directory (`qa-edge-case-test-pack.md`) contains the tests that prove each one.

### Required assets and placeholders — all four attacks

**Nothing here has been claimed, downloaded, or licensed.** The `$0` budget applies and every asset passes the human rights-review gate individually at claim time.

| Need | Phase 1 placeholder (ships no matter what) | Upgrade path |
|---|---|---|
| Vanguard mesh | UE5 Mannequin **scaled to 208 cm** + static-mesh gauntlet/shoulder proxy blocks + red/black material | Paragon heavy swap — `OPEN — Q30`, and only **before** M4 range tuning |
| Attack animations | proxy clips retargeted onto the proxy skeleton; free sources only (Mixamo, Fab free tier, Paragon, UE starter content) | bespoke or higher-fidelity clips at M5-06 |
| Hit reaction | shared hit-react montage in the `MontageSet` | tuned hit-stop feel is M5 |
| Counter reaction | `AM_Vanguard_CounterReact` (also serves the burst stagger family, plan §7) | M5 |
| Trace sockets | must exist on whichever proxy skeleton is chosen — **verify before authoring**, not after | re-validate after any mesh swap |

**Scale is load-bearing, not cosmetic.** The Vanguard is **6'10"** with a "substantially broader armored mass." A late mesh swap "invalidates sockets, capsule, and every range value" (plan §8.2), and every `MinRange`/`MaxRange` re-tunes twice. Q30 must be answered before M4 range tuning or the range work is done twice.

### The data row each montage must match

Every attack is one row in `DT_VanguardAttacks` (exactly four rows, created at M2-04). Fields per `S_VanguardAttackDef`:

`AttackID` · `DebugName` · `Montage` · `MinRange`/`MaxRange` (`OPEN — Q10`) · `Damage` (`OPEN — Q3`) · `Cooldown` (`OPEN — Q12`) · `bUsesPropulsion` · `MaxTravelDistance` (`OPEN — Q13`) · `bLockTrackingAtActive` · `Phase1` (`S_AttackPhaseTuning`) · `Phase2` (`S_AttackPhaseTuning`)

An editor-time validation check flags any per-attack value outside its GDD range. It **flags, never picks** — a flagged attack is pulled from the selection filter until fixed, and the loop keeps running on the remaining rows. Plan §8.5 names row-versus-montage drift as a real risk: a montage missing `ANS_CounterWindow`, a scale pushing a window outside its band, D exceeding its cap, or an active window differing between phases.

---

## Attack A — Close-range committed gauntlet force

**Milestone:** M2 (build step M2-13). **The first montage authored, and the reference layout for B/C/D.**

### Gameplay purpose and range
Close-range committed gauntlet force. Purpose is to punish being close and to teach the read: this is the attack the player learns the fight on. Range band `MinRange`/`MaxRange` — `OPEN — Q10`, close band.

### Readability requirement (GDD, non-negotiable)
"Distinct wind-up and punishable recovery." Attack A is the clearest tell in the set and carries the **longest recover window on the montage** (M2-13). It is the attack the vertical slice uses to prove the whole handoff (plan §7).

### Window sequence
| Window | Phase 1 | Phase 2 | Notes |
|---|---|---|---|
| Telegraph | 0.55–0.95 s | 0.40–0.75 s | **long** telegraph, held gauntlet pose |
| Active | 0.18–0.45 s | 0.18–0.45 s | identical both phases |
| Recover | 0.45–0.90 s | 0.35–0.75 s | **the longest of the three windows on A's own montage** (M2-13) — the deliberate punish opening |
| Return to Neutral | 0.10–0.20 s | 0.10–0.20 s | |

Per-attack float inside each band: `OPEN — Q25`.

### State boundaries
Started by `BTTask_SelectAttack` → montage played by `BTTask_Telegraph` → active frames owned by `BTTask_ActiveAttack` → punish window owned by `BTTask_Recover` → ended by `BTTask_ReturnToNeutral`.

### Montage layout
`[ANS_Telegraph][ANS_ActiveHit][ANS_Recover]`, with `ANS_CounterWindow` overlapping late telegraph / early active. **One** `ANS_ActiveHit` state.

**On montage sections:** upstream sources specify Vanguard attacks as a continuous notify-driven timeline and do **not** define named sections for them (unlike `AM_Player_LightCombo`, which has `Light_01..N`). No section names are invented here. If the implementer wants sections for authoring convenience, that is a free choice with no system dependency — but nothing reads them, and `BTTask_Telegraph` plays the montage from the start.

### Hit detection
On at `ANS_ActiveHit` Begin; off at End. Gauntlet socket sweep. Single window, so one already-hit set, so no multi-hit.

### Root motion, facing, tracking
- Root motion: in place or a short committed step. No travel.
- `bUsesPropulsion` — expected **false**, `MaxTravelDistance` unused. *Derivation, not a quoted value:* the GDD attributes propulsion to **D only** ("Short propulsion-assisted approach"), so A/B/C read as non-propulsion. The row values themselves are the designer's to set.
- `bLockTrackingAtActive` = **false** — A does not freeze facing. It rotates to target normally.

### Interruption and cancel
Counterable during `ANS_CounterWindow` via the standard chain. No other cancel. If countered: `AM_Vanguard_CounterReact` replaces the normal recover.

### If the montage ends early
Failsafe timer (`OPEN — Q18`) exits the waiting task; Return to Neutral still runs and clears flags.

### Acceptance checks in Unreal
1. Full cycle runs Idle → Select → Telegraph → Active → Recover → Neutral with visible state names, repeatedly, no deadlock.
2. Measured telegraph, active, and recover durations fall inside their Phase 1 GDD bands.
3. Windows retune **by dragging notify boundaries only** — no logic edit required.
4. A dodge timed into `ANS_PerfectDodge` yields 0 damage and **+12** meter; an ordinary dodge yields 0 damage and no meter.
5. `IA_Counter` inside `ANS_CounterWindow` interrupts, rival plays `AM_Vanguard_CounterReact`, **+15** meter, rival still reaches Neutral.
6. `IA_Counter` outside the window does nothing.
7. Attacking during `ANS_Recover` deals increased damage (multiplier `OPEN — Q27`).
8. Traces visible with `bDrawHitTraces`; no multi-hit within one active window; no tunnelling at full play rate.
9. **V3 check:** counter mid-active and confirm no trace survives (QA-V3-01).
10. Active window measured in Phase 1 and Phase 2 is **the same**.

---

## Attack B — Committed forward-pressure sequence

**Milestone:** M4 (build step M4-01).

### Gameplay purpose and range
Committed forward-pressure sequence — a multi-beat advance that pressures the player. Range band `OPEN — Q10`; the GDD does not state B's band or rank it against the others.

### Readability requirement (GDD, non-negotiable)
"Visible first beat and stable tracking limit." Two distinct obligations:
- The **first beat must be visible** — the player must be able to identify that B has started, from the first beat, and act on it.
- The **tracking limit must be stable** — once committed, B does not keep re-aiming at the player. That is what makes a sequence of beats dodgeable rather than homing.

### Window sequence
Same GDD bands as A (Telegraph 0.55–0.95 / 0.40–0.75; Active 0.18–0.45 both; Recover 0.45–0.90 / 0.35–0.75; Neutral 0.10–0.20). Per-attack floats `OPEN — Q25`.

**Structural difference:** B carries **multiple separate `ANS_ActiveHit` states, one per beat**, so each beat is individually dodgeable (M4-01). The GDD's Active band applies per active window; the number of beats is not specified upstream and is `OPEN — designer decides`.

### State boundaries
Same three-task chain. Note that **all beats live inside `BTTask_ActiveAttack`** — the multi-beat structure is montage-side, not a second BT task. Do not add a task per beat; that would fork the state model the GDD fixes at six states.

### Montage layout
`[ANS_Telegraph][ANS_ActiveHit #1][gap][ANS_ActiveHit #2][gap][…][ANS_Recover]`, `ANS_CounterWindow` overlapping late telegraph / early active, `ANS_TrackingLock` spanning the committed portion.

### Hit detection
On/off **per beat**. Each `ANS_ActiveHit` state opens and closes its **own** already-hit set — that is what makes each beat independently dodgeable and prevents one dodge from eating the whole sequence, or one beat from hitting twice.

The gaps between beats are not decorative: they are the dodge opportunities. If the beats merge into one continuous trace, B becomes an unavoidable multi-hit and the readability requirement fails.

### Root motion, facing, tracking
- Root motion: **forward travel across the beats is inferred from the GDD's "forward-pressure" purpose, not specified upstream.** No source states that B travels, how far, or by what means. Treat the advance as a design question for the designer, and if B does travel, apply the same measured discipline as D even though the cap field is D's.
- `bUsesPropulsion` — expected **false** (propulsion is attributed to D alone). Same derivation caveat as A: the row value is the designer's.
- `bLockTrackingAtActive` = **true** — `ANS_TrackingLock` freezes facing "at a fixed point" for the committed portion. This *is* the stable tracking limit.
- If B's cumulative travel is significant, it should be measured against the same discipline as D even though `MaxTravelDistance` is D's field — plan §8.5 lists travel exceeding a cap as a drift risk.

### Interruption and cancel
Counterable during `ANS_CounterWindow` only — which sits at late telegraph / early active, i.e. **the first beat**. Later beats are past the counter window: the player's answer to those is dodging, not countering. No cancel between beats. If countered on beat 1, the whole sequence stops and `AM_Vanguard_CounterReact` plays.

### If the montage ends early
Failsafe timer exits the task. **Extra care for B:** a stop between beats must not leave a beat's trace live (V3) or the tracking freeze applied (cleared by Return to Neutral regardless).

### Acceptance checks in Unreal
1. The first beat is identifiable in play as B rather than as any other attack.
2. **Each beat is individually dodgeable** — dodge beat 1, get hit by beat 2; dodge all beats, take zero damage. Test every combination.
3. No beat hits twice; no beat's trace bleeds into the next gap.
4. Facing is frozen for the tracking-lock duration: strafe hard during the committed portion and confirm B does **not** re-aim.
5. Total forward travel is bounded and repeatable; B cannot cross the arena.
6. Countering the first beat stops the whole sequence and routes to `AM_Vanguard_CounterReact`; rival reaches Neutral.
7. A counter attempt on a later beat does nothing (window closed).
8. Active windows measured identical in Phase 1 and Phase 2; only telegraph and recover scale.
9. Row-versus-montage check passes: beat count in the montage matches whatever the row expects; validation flags nothing.

---

## Attack C — Armored reach and space control

**Milestone:** M4 (build step M4-01).

### Gameplay purpose and range
Armored reach and space control — punishes standing at what feels like a safe distance. Range band `OPEN — Q10`. The GDD gives C "armored reach and space control" but **does not rank the four range bands against each other**; do not assume C holds the longest band until Q10 is set.

### Readability requirement (GDD, non-negotiable)
"Clear body direction and visible active range." Two obligations:
- **Body direction must be clear before the active frames** — the player must be able to read *where* C is going to reach from the pose alone.
- **The active range must be visible** — the threatened space must be legible, not a surprise.

### Window sequence
Same GDD bands as A. Per-attack floats `OPEN — Q25`. C's telegraph carries the heaviest readability load in the set because its threat is spatial rather than temporal.

### State boundaries
Same three-task chain.

### Montage layout
`[ANS_Telegraph][ANS_ActiveHit][ANS_Recover]`, `ANS_CounterWindow` overlapping late telegraph / early active, `ANS_TrackingLock` beginning **before** the active window.

### Hit detection
On at `ANS_ActiveHit` Begin; off at End. The trace is the reach — a long sweep. Per M4-01, the "active-range capsule visible via the debug toggle" (`bDrawHitTraces`) is how the implementer confirms the authored reach matches the intended reach.

**Socket dependency is highest here.** C's reach is defined by which socket the trace sweeps. On a scaled proxy Mannequin with static-mesh gauntlet blocks, the socket may not sit where the visual reach appears to end. Verify the trace against the visual silhouette before tuning ranges, or C's range band will be tuned against a lie.

### Root motion, facing, tracking
- Root motion: minimal or none. C controls space; it does not travel into it.
- `bUsesPropulsion` — expected **false** (same derivation as A and B).
- `bLockTrackingAtActive` = **true** — body direction is locked by `ANS_TrackingLock` **before** the active window opens (M4-01). This one *is* sourced: M4-01 names B and C as the tracking-lock attacks. This is what makes the direction readable: it is committed while the player can still see it and move.

The ordering matters. If the lock begins at the same instant as the active window, the direction is only readable *during* the hit, which fails the requirement. The lock must precede the active frames.

### Interruption and cancel
Counterable during `ANS_CounterWindow` only. No cancel. Countered → `AM_Vanguard_CounterReact`.

### If the montage ends early
Failsafe timer exits. Tracking freeze cleared by Return to Neutral. Long trace makes the V3 leak risk more consequential here — a surviving long-reach trace covers a lot of floor.

### Acceptance checks in Unreal
1. From the telegraph pose alone, a player can identify which direction C will reach. Test with a second person who has not seen the montage.
2. The active-range capsule drawn with `bDrawHitTraces` matches the visual reach of the mesh — no invisible extra reach, no visible reach that does not hit.
3. Body direction is locked **before** the active window opens, not simultaneously — verify on the timeline and in play by strafing during late telegraph.
4. Standing just outside `MaxRange` is genuinely safe; just inside is genuinely not.
5. Counter works only inside the authored window; rival reaches Neutral after every counter.
6. Active window identical in both phases.
7. After any proxy mesh change, re-verify socket positions and re-run checks 2 and 4 — C is the attack most sensitive to a swap.

---

## Attack D — Short propulsion-assisted approach

**Milestone:** M4 (build step M4-01). **The attack with the hardest constraint in the set.**

### Gameplay purpose and range
Short propulsion-assisted approach — closes a gap explosively so that distance is not a free defence. Range band `OPEN — Q10`; D is selected from a gap its travel can actually close.

### Readability requirement (GDD, non-negotiable)
"Thruster cue before movement; no hidden full-arena snap." Two obligations, and the second is a hard structural limit:
- **The thruster cue must precede the movement** — the player sees D coming before D moves, not as it arrives.
- **No hidden full-arena snap** — D's travel is bounded and the bound is visible in data. This is repeated in the GDD, in `combat-integration-plan.md` §5.2, and in `build-sequence.md` M4-01. It is the most-repeated single constraint attached to any attack in the design.

### Window sequence
Same GDD bands as A. Per-attack floats `OPEN — Q25`. The thruster cue lives inside `ANS_Telegraph` (M4-01), which means the telegraph must both hold a readable committed pose *and* fire the propulsion cue before the active window.

### State boundaries
Same three-task chain. The travel happens inside `BTTask_ActiveAttack`.

### Montage layout
`[ANS_Telegraph (contains thruster cue)][ANS_ActiveHit][ANS_Recover]`, `ANS_CounterWindow` overlapping late telegraph / early active.

### Hit detection
On at `ANS_ActiveHit` Begin; off at End. Because D moves while active, the frame-to-frame socket sweep matters more here than anywhere else — plan §3.1 row 16 notes that "tunnelling on fast attacks is pre-solved by the sweep." D is the attack that proves it. Verify no pass-through at full travel speed.

### Root motion, facing, and the travel cap
- **Root motion is the default and expected implementation.** `bUsesPropulsion` = **true**.
- **`MaxTravelDistance` (`OPEN — Q13`) is a hard cap.** The cap is data. Travel must be measured against it, not assumed to respect it: plan §8.5 names "a D-row travel exceeding `MaxTravelDistance`" as a specific drift risk, and the fallback extends the validation check to "D's root-motion extent measured against `MaxTravelDistance`."
- `bLockTrackingAtActive` = **false** — D is not listed among the tracking-lock attacks (B and C are). D's commitment comes from its travel, not a facing freeze.
- **Motion Warping is NOT the default.** Plan §8.7: the default is "root-motion montages with a hard distance cap plus a pre-attack `Move To` reposition." Motion Warping is R5 — optional, schedule-dependent, disposable-branch-first, and requires designer approval since it is external code. **Author for root motion.** If warping is ever adopted, the early warning sign named upstream is "warp targets overshooting or ignoring the distance cap."

### Interruption and cancel
Counterable during `ANS_CounterWindow` — which sits at late telegraph / early active, i.e. **before or at the very start of the lunge**. No cancel mid-travel.

**Special care:** a counter that lands as D begins travelling stops a montage that is mid-root-motion. Confirm the rival ends at a sane location and is not left displaced, floating, or clipped into geometry. Return to Neutral's `Set Movement Mode (Walking)` is what recovers locomotion.

### If the montage ends early
Failsafe timer exits the task. **The worst case in the set:** a root-motion montage stopped mid-travel can leave the rival mid-air or intersecting the arena's blocking-volume ring. Verify `Walking` is restored and the capsule is resolved on the floor before the next cycle begins.

### Acceptance checks in Unreal
1. The thruster cue is visible and audible-in-principle **before** any movement begins. Verify on the timeline that the cue precedes the first root-motion frame, and in play that a player can react to it.
2. **Measure actual travel distance across at least twenty runs from varied starting gaps.** No run exceeds `MaxTravelDistance`. This is the single check the design repeats three times.
3. D cannot cross the arena. Attempt it from maximum separation — D closes part of the gap, not all of it.
4. No tunnelling: D at full travel speed never passes through the player without a trace hit.
5. Counter at the start of the lunge stops D cleanly; the rival ends on the floor, at a sane location, in `Walking`, and reaches Neutral.
6. Force an early montage end mid-travel: rival ends grounded, not clipped into the blocking volume or Kill Z.
7. Active window identical in both phases; only telegraph and recover scale. Note that a shorter Phase 2 telegraph means **less warning before the same lunge** — verify the thruster cue is still readable at the Phase 2 band of 0.40–0.75 s.
8. Validation check flags a D row whose travel exceeds its cap; the flagged row is pulled from the selection filter and the loop keeps running on A/B/C.

---

## Cross-attack acceptance — run after all four exist (M4)

| # | Check | Source |
|---|---|---|
| 1 | `DT_VanguardAttacks` has **exactly four rows**. No fifth attack anywhere. | scope lock |
| 2 | Selection filters to in-range **and** off-cooldown, then picks by the active phase's `SelectionWeight`. The only nondeterminism is authored weighting. | M4-03 |
| 3 | Every montage carries all four required notify classes. A montage missing `ANS_CounterWindow` is a validation failure. | plan §8.5 |
| 4 | Every attack's active window is inside **0.18–0.45 s** and **identical across phases**. | GDD |
| 5 | Telegraph and recover scale into their Phase 2 bands; nothing else does. | GDD, plan §3.1 row 15 |
| 6 | All four reach Return to Neutral on every attempt — countered, out of range, player idle, in both phases. | M2/M4 gates |
| 7 | Retuning any window requires dragging a notify or editing a table value — never a logic edit. | plan §2.2 |
| 8 | Each attack is distinguishable from the other three during its telegraph. | GDD readability column |
| 9 | Only B and C freeze facing. A and D rotate normally. | M4-01/M4-02 |
| 10 | Only D travels as its purpose, and its travel is capped in data. | GDD, M4-01 |
| 11 | Toggling `bPresentationEnabled` off changes no measured window on any attack. | plan §2.5 |
| 12 | No runtime model call anywhere in the attack path. | GDD runtime AI boundary |

---

## Open values this document does not resolve

| Tag | Value | Attacks affected |
|---|---|---|
| Q3 | per-attack damage | all |
| Q10 | range bands `MinRange`/`MaxRange` | all — tune against arena footprint Q24 |
| Q12 | per-attack cooldowns | all |
| **Q13** | **`MaxTravelDistance`** | **D — the cap the design repeats three times** |
| Q18 | BT task failsafe timer margin | all |
| Q25 | the single per-attack float inside every GDD state range | all |
| Q27 | `ANS_Recover` incoming-damage multiplier | all |
| Q30 | Paragon heavy swap and its deadline — **before M4 range tuning** | all; C most sensitive |
| — | number of beats in Attack B | B |
| — | whether Motion Warping is ever attempted (R5) | D |
| — | section naming inside Vanguard montages (no system dependency) | all |

## What this document does not do

- It does not create, remove, or modify any attack. Four attacks, exactly as the GDD defines them.
- It does not resolve a single provisional number.
- It does not duplicate the player-facing telegraph and readability content already in `assignment-04/shared/knowledge-base/vanguard-telegraphs.md`. That material describes what the player perceives; this describes what the montage and the Behavior Tree must do.
- It does not specify VFX or audio content — those are the sibling cue sheets, and the authored versions are M5.
- It does not assume the restoration contract is fixed. V1–V5 are open, and every place they touch montage authoring is flagged inline rather than glossed.
