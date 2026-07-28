# Combat Integration Plan — Ascendant Impact

**Produced by:** combat-integration-architect agent
**Consumes:** `project-brief.md` · `design-brief.md` · `build-sequence.md` · `inspection.md` · `framework-evaluation.md` · `gdd/ascendant-impact-gdd-v0.4.md` · `CLAUDE.md`
**Date:** 2026-07-27 · **Ship date:** 2026-09-01 (**36 days remaining**)
**Gate check:** `inspection.md` reports **no violations**; `framework-evaluation.md` ends with a definitive recommendation (**USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE**, confidence high); the human designer of record has approved that recommendation (approval record relayed 2026-07-27: *"APPROVED — use the Blueprint-first custom architecture recommended by framework-evaluation.md."*). Not blocked; integration planning proceeds.

This document does not choose a foundation — that decision is made and approved. It maps every required Ascendant Impact system onto the approved foundation so a human developer or a later Unreal implementation agent can build it without reinterpreting the game design. Every number in this document is carried from the GDD or design brief unchanged, is **provisional and pending playtest**, and belongs to the human designer. Every missing value is `OPEN — designer decides` with its design-brief §14 question tag.

---

## 1. Approved foundation

### 1.1 The recommendation, verbatim

`framework-evaluation.md` §1 / §9: **`USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE`** — the architecture already specified in `design-brief.md` §2–§9 and decomposed into the inspected `build-sequence.md`:

- one shared `BP_PlayerFighter` Character class with Echo and Nova as `DA_FighterProfile` data assets (no subclasses, no per-fighter branches);
- a deterministic authored `BT_CrimsonVanguard` Behavior Tree + `BB_CrimsonVanguard` Blackboard run from `BP_VanguardController`, six `BTTask_*` states in a linear `Sequence` under an infinite `Loop`;
- four attacks A–D as rows in one `DT_VanguardAttacks` Data Table, each row carrying paired `Phase1` / `Phase2` tuning structs;
- Anim Notify State windows (`ANS_Telegraph` / `ANS_ActiveHit` / `ANS_Recover` / `ANS_CounterWindow` / `ANS_ComboLink` / `ANS_IFrame` / `ANS_PerfectDodge` / `ANS_TrackingLock`) authored on montage timelines;
- custom `BP_ImpactWindowDirector` and `BP_FinalClashDirector` overlays with a single `RestoreCombatState()` return path;
- the `BP_PresentationSubsystem` kill-switch separating gameplay timing from all presentation;
- plain Blueprints with Gameplay Tags — deliberately **not** GAS, not State Tree, not AI Perception, and not any marketplace fighting-game template.

### 1.2 Approval status

**APPROVED.** The human designer of record approved the recommendation on 2026-07-27 (record relayed verbatim by the commander: *"APPROVED — use the Blueprint-first custom architecture recommended by framework-evaluation.md."*). This plan implements that approval and nothing else. No purchase, plugin adoption, license acceptance, or installation is authorized by this document.

### 1.3 Evidence supporting it (from `framework-evaluation.md`)

- The design exists on disk, fully decomposed (M1-01 → M4-GATE) and inspected with zero violations, zero orphans, zero gaps.
- Every technique used is stock, long-supported UE functionality present in 5.8 (montage sections, notify states, Behavior Tree + Blackboard + Gameplay Debugger, Data Tables, Enhanced Input, Gameplay Tags without GAS, Level Sequences, UMG) — evaluation matrix score 94/100.
- Both external candidates (n00dFighter, TRUE FGE) were **REJECTED**: unverified UE 5.8 support, versus/multiplayer-centric architecture against a no-PvP scope lock, paid against a $0 budget, more integration work than the approved plan, core claims unverifiable without purchase (47/100 and 46/100).
- The systems the central promise depends on — perfect-dodge detection in hit resolution, the earned Impact Window with its onboarding prohibitions, the double-gated recoverable Final Clash, the six-state readable rival — are custom under **every** candidate; no template removes any of them.
- A repository-wide glob found zero Unreal project or C++ files: there is no pre-existing scaffold to integrate with. This plan is a green-field map onto stock UE 5.8.

### 1.4 Assumptions still open

| Assumption | Status |
|---|---|
| UE 5.8 Third Person template behaves as assumed (Enhanced Input default rig, montage-section API, `SpringArm` + `Camera`) | Unverified in a live project; the framework evaluation's §8 sandbox test (one buffered light-attack chain in a disposable project) proves it first. **Whether/when to run it: `OPEN — designer decides`** |
| The Unreal MCP server can be established and can reliably drive the editor for the full M1–M4 sequence | Untested; CLAUDE.md names it a build prerequisite. See risk §8.6 |
| Free proxy assets (UE5 Mannequins, Mixamo, Fab free tier, Paragon heavies) pass the human rights-review gate at claim time | Nothing is approved by being listed; every asset passes the gate individually |
| All 29+ `OPEN` tuning values will be supplied by the human designer during the build, not after | Late answers stall milestones (evaluation risk 3, brief R7) |
| The 6'10" Crimson Vanguard proxy resolves via the design-brief §12.4 fallback ladder | R4 — the single biggest free-asset gap; option 1 (scaled Mannequin + proxy blocks) ships no matter what |

---

## 2. Integration principles

These rules keep the architecture single-sourced, data-driven, deterministic, testable, reversible, and inside course scope. They are restated here as build law; the inspector already enforces most of them.

1. **Single-sourced player framework.** Exactly one `BP_PlayerFighter`. No `BP_Echo`, no `BP_Nova`, no child Blueprints, no `Switch on Fighter` in combat code. Every Echo/Nova difference is a field on `DA_FighterProfile`; a difference that cannot be a data field is out of Phase 1 scope and is surfaced to the designer, never subclassed. The same anti-fork rule applies to shared classes: one `BP_HealthComponent` for both fighters, one `ANS_ActiveHit` class for both fighters' traces.
2. **Data-driven attacks, one path.** `DT_VanguardAttacks` has exactly four rows (A, B, C, D). Telegraph, active, recover, movement caps, hitbox windows, and presentation hooks live on each row's montage timeline and struct fields — editable by dragging notify boundaries and typing table values, never by editing four unrelated logic graphs. Phase 2 is the second member of the same row read through one `Select` node on `bPhase2`; there is no second table, second montage set, second BT branch, or transformation rig.
3. **Deterministic authored rival.** Crimson Vanguard is `BT_CrimsonVanguard` + `BB_CrimsonVanguard` running six Blueprint tasks. The only nondeterminism is authored-weighted selection among in-range, off-cooldown attacks. No runtime LLM or model call, no learning, no adaptive difficulty, no runtime generation — in the shipped build, ever. (Offline generative tooling for assignment #04 lives outside the game's scope lock and never enters the build without the human approval gate.)
4. **Gameplay before spectacle.** Impact Windows and the Final Clash open only from earned real-time events (perfect dodge, counter, approved combo milestone; the double gate for the Clash). No auto-success, no input pressed for the player, no buffered press converted into a success. Every cinematic branch — Impact success, Impact failure, Clash success, Clash failure — exits through the single `RestoreCombatState()` function, which explicitly restores player input, collision, locomotion, lock-on, camera/time dilation, AI state, and valid combat tags.
5. **Presentation is severable.** All hit-stop, camera shake, VFX, sound, and time dilation route through `BP_PresentationSubsystem` wrappers that early-return when `bPresentationEnabled` is false. Gameplay timing is driven by montage playback and `Set Timer by Event`, never through a presentation call, so disabling presentation cannot change a frame window. The subsystem is wired (empty) in M1 so all M5 work lands without touching gameplay code. M5 remains last.
6. **Testable at every state.** Visible debug state names (`BTService_DrawDebugState` + Gameplay Debugger), `WBP_DebugPanel` toggles (`bPresentationEnabled`, `bShowStateNames`, `bDrawHitTraces`), guaranteed-exit BT tasks with montage failsafe timers, and per-milestone gates that are demonstrable in PIE.
7. **Reversible.** Every milestone ends in a git commit on the build branch that is a known-good rollback point; risky experiments (sandbox tests, retarget trials, Motion Warping) happen on disposable branches or throwaway projects and never touch the main build until proven. A proxy-asset swap is a data-asset field change, revertible in one edit.
8. **Human-owned values.** Every GDD number is carried verbatim and marked provisional. Every missing number is a designer-exposed variable left `OPEN — designer decides` with its §14 tag. No agent — including this one — resolves a provisional value.
9. **Course scope is a wall.** One player, one authored rival, one arena, one shared framework, four attacks, one duel with win and loss. Nothing in design-brief §1.3 (M5/Phase-2 deferred) or §1.4 (outside scope lock — PvP, unique move sets, second boss kit, more arenas, progression, transformations) gets integration work here.

---

## 3. Foundation-versus-custom matrix

### 3.1 The matrix — all 28 required systems

"Provided by foundation" means stock UE 5.8 capability (the approved foundation is stock UE plus the approved custom design; no external framework exists to provide anything).

| # | Game system | Provided by foundation (stock UE 5.8) | Custom Ascendant work | Integration boundary (assets involved) | Risk | Milestone |
|---|---|---|---|---|---|---|
| 1 | Third-person movement | Third Person template: `CharacterMovementComponent`, `SpringArmComponent` + `CameraComponent`, blendspace locomotion AnimBP, Enhanced Input plumbing | `IMC_Duel` mapping; `DA_FighterProfile.MaxWalkSpeed` applied per fighter (value `OPEN` Q15); strafe-facing flags flipped by lock-on | `BP_PlayerFighter`, `ABP_Fighter`, `IMC_Duel`, `IA_Move`/`IA_Look` | Template assumptions unverified until the sandbox test; Motion Matching deliberately NOT used (R2) | M1 |
| 2 | Camera and lock-on | Spring-arm follow camera, `Find Look at Rotation`, `RInterp To`, control rotation | `BP_LockOnComponent`: single-target soft lock, acquire/hold/break, strafe-facing (`bOrientRotationToMovement=false`, `bUseControllerDesiredRotation=true`), HUD reticle via `Project World to Screen`; ranges/interp `OPEN` Q11 | `BP_LockOnComponent`, `WBP_HUD`, `IA_LockOn` | Camera fighting the Level Sequence cuts at Impact/Clash handoff — see risk §8.4; hard camera work is M5 | M1 |
| 3 | Character selection | UMG, Game Instance persistence, `Open Level` | `WBP_CharacterSelect` (two portraits, name, one-line identity), stores chosen `DA_FighterProfile` in Game Instance; `L_CharacterSelect` menu level | `WBP_CharacterSelect`, `L_CharacterSelect`, `BP_DuelDirector` (reads selection) | Low; GDD's simplified-screen allowance applies. Editorial interface is M5-08 | M1 |
| 4 | Shared Echo/Nova fighter data | `PrimaryDataAsset`, material vector parameters, capsule/scale APIs | `DA_FighterProfile` class + `DA_FighterProfile_Echo` / `DA_FighterProfile_Nova`; `ApplyFighterProfile()` called once at BeginPlay; heights 183/173 cm (GDD, provisional); measure-then-scale rule; Nova's cyan-white is a separate combat-energy parameter, **not** a costume recolor | `DA_FighterProfile`, `BP_PlayerFighter.ApplyFighterProfile`, `ABP_Fighter` (stance additive) | Fork temptation — any behavior difference must be a data field or be surfaced; scale must not create hidden reach (M1 gate tests both avatars) | M1 |
| 5 | Light attack sequence | Anim Montage with named sections, `Montage Play` / `Montage Set Next Section` | `AM_Player_LightCombo` sections `Light_01..N` (count `OPEN` Q5); `ANS_ComboLink` accept window per section; `AN_ComboFinisher` on final section only (the +5 meter point); `ANS_ActiveHit` per section | `AM_Player_LightCombo`, `ANS_ComboLink`, `AN_ComboFinisher`, `ANS_ActiveHit`, `BP_CombatComponent`, `IA_LightAttack` | Free anim sourcing/retargeting (R1) — the schedule's tightest resource | M1 |
| 6 | Input buffering | Enhanced Input `Triggered` events | Combo buffering ONLY inside `ANS_ComboLink` (`bComboBuffered`, window `OPEN` Q28); **deliberate anti-buffer** on `IA_Impact`: a press before a window opens is discarded, never queued (onboarding prohibition 2) | `ANS_ComboLink`, `BP_CombatComponent`, `BP_ImpactWindowDirector` | The two buffering policies are opposites and must not share code — see risk §8.3 | M1 (combo) / M3 (discard rule) |
| 7 | Dodge | Root-motion montage sections, notify states | `AM_Player_Dodge` sections `Dodge_F/B/L/R`, direction from `IA_Move` at press; `ANS_IFrame` adds/removes `State.Invulnerable` (window `OPEN` Q6); `DodgeDistance` per profile (`OPEN` Q16) | `AM_Player_Dodge`, `ANS_IFrame`, `BP_CombatComponent`, `IA_Dodge` | Root-motion distance vs. arena footprint (Q24) interplay | M1 |
| 8 | Perfect dodge | Notify-state nesting on the same timeline | `ANS_PerfectDodge` nested strictly inside `ANS_IFrame`, adds `State.PerfectWindow` (window `OPEN` Q7 — the single most difficulty-defining number); detection happens on the **rival's hit trace**, in `ResolveIncomingHit`, so a perfect dodge can never disagree with an actual incoming hit | `ANS_PerfectDodge`, `BP_CombatComponent.ResolveIncomingHit` | If detection ever moves to a proximity test it will desync from damage — the one-code-path rule is the defense | M1 (window) / M2 (first real detection vs. Attack A) |
| 9 | Counter | Notify states on the rival's montages, event dispatchers | `ANS_CounterWindow` authored on each Vanguard attack montage → `bCounterable` + `OnCounterWindowOpen` → player `State.CanCounter`; success: stop rival montage, `AM_Vanguard_CounterReact`, `AM_Player_Counter`, +15 meter, Impact request, rival forced through Recover (the one legal interrupt); whiff: `AM_Player_CounterWhiff` punishable recovery (`OPEN` Q8) | `ANS_CounterWindow`, `AM_Player_Counter`, `AM_Player_CounterWhiff`, `AM_Vanguard_CounterReact`, `BP_VanguardCombatComponent`, `IA_Counter` | Interrupt must route *through* the BT sequence, never via `Abort`/`Stop Logic` — deadlock defense | M1 (player half) / M2 (rival half) |
| 10 | Player health | ActorComponent pattern, event dispatchers | Shared `BP_HealthComponent` (one class, no subclass): `ApplyDamage` early-returns 0 on `State.Invulnerable`, clamps to `MinHealthFloor`, broadcasts `OnHealthChanged`/`OnDeath`; pool `OPEN` Q1 in `DA_TuningGlobals` (identical for Echo and Nova) | `BP_HealthComponent`, `DA_TuningGlobals`, `WBP_HUD` | Low — deliberately boring | M1 |
| 11 | Rival health | Same shared class | Same `BP_HealthComponent` instance on `BP_CrimsonVanguard`; `MinHealthFloor` is the Final Clash 1 HP floor mechanism (no special-case damage branch); `OnHealthChanged` feeds the 50% Phase 2 trigger and ≤25% Clash gate; pool `OPEN` Q2 | `BP_HealthComponent`, `BP_CrimsonVanguard`, `BP_DuelDirector`, `BP_FinalClashDirector` | Q22 (floor permanent vs. Clash-only) changes what the game is about — designer must answer before M4-08 is final | M2 (mounted) / M4 (floor + thresholds live) |
| 12 | Crimson Vanguard controller | `AIController`, `Run Behavior Tree`, Blackboard | `BP_VanguardController`: runs `BT_CrimsonVanguard`, sets `TargetActor` from `Get Player Pawn` at BeginPlay; **no AI Perception** (one target, always exists) | `BP_VanguardController`, `BB_CrimsonVanguard` | Low | M2 |
| 13 | Six-state rival flow | Behavior Tree editor, `Sequence` + `Loop` decorator, Gameplay Debugger (apostrophe key) | Six `BTTask_*` in GDD order (`Idle_Reposition`, `SelectAttack`, `Telegraph`, `ActiveAttack`, `Recover`, `ReturnToNeutral`); first node of every task sets `CurrentState`; every montage-waiting task carries a failsafe timer (margin `OPEN` Q18); `bInClash` branch parks the tree on `BTTask_WaitIndefinite`; no `Abort Self`, no `Simple Parallel` aborts, no `Stop Logic` | `BT_CrimsonVanguard`, `BB_CrimsonVanguard`, `BTTask_*` ×6 + `BTTask_WaitIndefinite`, `BTService_UpdateCombatData`, `BTService_DrawDebugState` | A task that never calls `Finish Execute` strands the encounter — the failsafe rule is the M2 gate implemented | M2 |
| 14 | Four data-driven attacks | Data Table + Blueprint Structure, `Get Data Table Row` | `S_VanguardAttackDef` + `S_AttackPhaseTuning`; `DT_VanguardAttacks` with exactly four rows (all four created at M2, montages B/C/D authored at M4); per-row: montage, ranges (Q10), damage (Q3), cooldown (Q12), propulsion cap (Q13), tracking lock, paired Phase1/Phase2 tuning; editor-time range-validation check that **flags** (never picks) out-of-GDD-range values | `DT_VanguardAttacks`, `S_VanguardAttackDef`, `S_AttackPhaseTuning`, `AM_Vanguard_AttackA/B/C/D`, `ANS_TrackingLock` | Attack-data mismatch (row vs. montage) — see risk §8.5; range bands vs. arena footprint is the likely early bug source (Q10 × Q24) | M2 (A + table) / M4 (B, C, D) |
| 15 | Telegraph / active / recover windows | AnimNotifyState authored on montage timelines, Animation editor | `ANS_Telegraph` (pose hold, warning color, `OnTelegraphStart`), `ANS_ActiveHit` (swept trace), `ANS_Recover` (punish multiplier, `OPEN` Q27), `ANS_CounterWindow` overlay; GDD ranges carried verbatim: Telegraph 0.55–0.95 s P1 / 0.40–0.75 s P2, Active 0.18–0.45 s **both phases**, Recover 0.45–0.90 s P1 / 0.35–0.75 s P2; per-attack floats `OPEN` Q25; retuned by dragging notify boundaries, no logic edits | montages + `ANS_*` classes in `/Notifies/`, `TelegraphScale`/`RecoverScale` in the row structs | Play-rate scaling must cover only telegraph/recover sections — the active window is deliberately not phase-scaled | M2 (A) / M4 (B–D, Phase 2 scaling) |
| 16 | Hit detection and hit reaction | `Capsule Trace By Channel`, custom trace channels, sockets | `AttackTrace` channel (default Ignore, both meshes Block); `ANS_ActiveHit` sweeps previous-frame → current-frame socket, per-window already-hit set, one shared class for both fighters; hit → `ResolveIncomingHit` three-way branch (perfect / dodge / hit); hit reaction = shared hit-react montage in the `MontageSet` (proxy anim; tuned hit-stop feel is M5); debug draw behind `bDrawHitTraces` | `ANS_ActiveHit`, `BP_CombatComponent.ResolveIncomingHit`, `BP_VanguardCombatComponent`, collision settings | Tunnelling on fast attacks is pre-solved by the sweep; socket names must exist on whichever proxy skeleton is chosen | M1 (player-side) / M2 (rival-side) |
| 17 | Ascension Meter | ActorComponent + Data Table | `BP_AscensionComponent` (player only), `Meter` clamped 0–100; single entry point `AddMeter(E_MeterEvent)` reading `DT_MeterGains`: +5 finisher / +12 perfect dodge / +15 counter / +20 Impact success / +0 damage-or-waiting (explicit, so "waiting grants nothing" is visible data); **no time-based gain anywhere**; decay `OPEN` Q9 (brief recommends none); one sanctioned direct write: Clash failure sets 50 | `BP_AscensionComponent`, `DT_MeterGains`, `WBP_HUD` | Any second write path to `Meter` is a defect | M3 |
| 18 | Impact Window trigger | `Set Timer by Event`, UMG, Enhanced Input | `BP_ImpactWindowDirector.RequestImpactWindow(E_ImpactTrigger)` from exactly three earned events (perfect dodge via `ResolveIncomingHit`, counter via `ANS_CounterWindow`, combo milestone via `AN_ComboFinisher`); refuses if window open, cooldown active (`OPEN` Q26), `bInClash`, or either fighter dead; first window 0.75 s (perfect dodge/counter only), standard 0.35–0.50 s, `bFirstWindowConsumed` | `BP_ImpactWindowDirector`, `WBP_ImpactPrompt`, `IA_Impact` | Onboarding prohibitions: no auto-success, no pre-open buffering, wider first window changes exactly one float | M3 |
| 19 | Impact success / failure branches | Montage pair playback, timers | SUCCESS: +20 meter, 1–3 s (GDD, provisional) choreographed burst as a montage pair on both fighters, presentation via subsystem wrappers (empty until M5), then `RestoreCombatState()`. FAILURE: no extension, no meter, no extra punishment, `RestoreCombatState()` immediately, start cooldown | `BP_ImpactWindowDirector`, burst montage pair, `RestoreCombatState()` (M3-08), `BP_PresentationSubsystem` | Stranded-cinematic-state risk — killed by the single restore function; see risk §8.4 | M3 |
| 20 | Phase 2 at 50% rival health | Blackboard bool, event dispatch | `BP_DuelDirector` sets `bPhase2Pending` at `Percent <= 0.50`; **commit only in `BTTask_ReturnToNeutral`** (never mid-telegraph/mid-active); one-shot `OnPhase2Committed` signal guarded by `bPhase2` (Phase 1 realization: emissive change + brief pause; authored VFX/sound M5); every timed task reads tuning via one `Select` on `bPhase2` — same four attacks, active window unchanged | `BP_DuelDirector`, `BTTask_ReturnToNeutral`, `BB_CrimsonVanguard.bPhase2`, `DT_VanguardAttacks` Phase2 structs | Committing anywhere but Return to Neutral retimes an attack mid-read — a READ-pillar bug | M4 |
| 21 | Final Clash eligibility gate | Event-driven evaluation | `BP_FinalClashDirector.EvaluateClashGate()` on `OnMeterChanged` and CV `OnHealthChanged` only: `(Meter >= 100) AND (CV Health <= 25%) AND (no cooldown) AND (not bInClash)`; both conditions or locked; `WBP_HUD` shows two honest gate indicators; `IA_FinalClash` accepted only in neutral or the post-counter window (`OPEN` Q19); never auto-triggers | `BP_FinalClashDirector`, `WBP_HUD`, `IA_FinalClash` | The AND must never soften to OR | M4 |
| 22 | Final Clash success | Level Sequence, montages, reused prompt machinery | Two timing beats = the same `WBP_ImpactPrompt` + timer machinery run twice (beat widths `OPEN` Q20; binding reuse of `IA_Impact` `OPEN` Q17); `bInClash = true` parks the rival BT; `AM_Clash_Beat1`, `LS_FinalClash` (one camera cut in Phase 1; full choreography M5-07); both beats hit → `AM_Clash_Finisher` → floor to 0, `ApplyDamage(MaxHealth)` → `OnDeath` → `EndDuel(Win)`; `RestoreCombatState()` runs before the result screen | `BP_FinalClashDirector`, `LS_FinalClash`, `AM_Clash_Beat1`, `AM_Clash_Finisher`, `WBP_ImpactPrompt`, `WBP_Result` | Camera/control restoration after the sequence — risk §8.4 | M4 |
| 23 | Final Clash failure recovery | Timers, transform APIs | The exact seven-step sequence, GDD numbers unchanged: stop montages/sequence + camera back → separate fighters (distance `OPEN` Q21, outside every `MinRange`) → preserve health → CV `MinHealthFloor = 1` (Q22 open: permanent vs Clash-only) → `Meter = 50` (the one sanctioned direct write) → 3 s re-trigger cooldown → `RestoreCombatState()`, rival BT re-enters at `Idle_Reposition`. Must NOT: restart duel, kill/damage player, leave anyone in a cinematic state | `BP_FinalClashDirector.ClashFailure()`, `BP_HealthComponent.MinHealthFloor`, `BP_AscensionComponent`, `RestoreCombatState()` | The single most misreadable rule in the design — verified explicitly at the M4 gate | M4 |
| 24 | Win and loss handling | Event dispatchers, UMG | Win: Clash success only path above. Loss: the **only** loss condition is player health zero → `OnDeath` → `EndDuel(Loss)`. `WBP_Result` Win/Loss states + restart. No duel timer (`OPEN` Q23, brief recommends none; 3–5 min is a session target, not a rule) | `BP_DuelDirector.EndDuel`, `WBP_Result` | Low | M4 |
| 25 | Debug-state visibility | Gameplay Debugger (free Blackboard/task dump), `Draw Debug String` | `BTService_DrawDebugState`: `CV | Phase | State | AttackDebugName | time` above the rival, gated on `bShowStateNames`; task convention (first node sets `CurrentState`) makes the display structurally truthful; `bDrawHitTraces` draws the attack sweeps | `BTService_DrawDebugState`, `WBP_DebugPanel`, `BP_PresentationSubsystem` bools | Two independent views of the same truth — if they disagree, the convention was broken | M2 (rival) / M1 (panel) |
| 26 | Presentation kill-switch | GameInstanceSubsystem | `BP_PresentationSubsystem`: `bPresentationEnabled` + the ONLY legal wrappers (`RequestHitStop`, `RequestCameraShake`, `RequestVFX`, `RequestSound`, `RequestTimeDilation`), each early-returning when disabled; hard rule: the five raw engine calls appear in exactly this one asset; wired empty in M1, filled only in M5 | `BP_PresentationSubsystem`, `WBP_DebugPanel` | The structural guarantee that M5 changes no gameplay timing; searchable by the inspector | M1 (wired empty) / M5 (filled) |
| 27 | Clean return to gameplay | One function, project-wide | `RestoreCombatState()` written **once** (M3-08), called by all four overlay branches and duel start: enable input; collision Query+Physics on both capsules; `Set Movement Mode (Walking)` both; clear transient tags (`State.Attacking/.Invulnerable/.PerfectWindow/.InImpactWindow/.Clashing`); restore lock-on if it was active; time dilation → 1.0 via the subsystem; rival `bInClash = false`, `CurrentState = Idle_Reposition`, BT resumes; hide `WBP_ImpactPrompt` | `RestoreCombatState()` on `BP_DuelDirector` (or shared library) | One bug lives in one place — never four copies | M3 (written) / M4 (Clash branches call it) |
| 28 | Save, test, and version-control boundaries | Git repo (exists), UE editor save/package, PIE | Milestone-gate commits on the build branch as rollback points; sandbox/experiment work on disposable branches (e.g. `sandbox/combo-buffer-test`) or throwaway projects, deleted after the result is recorded; the M2-04 editor-time range-validation check; each M-GATE is a scripted PIE checklist demonstrated before the commit; Unreal MCP drives the editor but **every MCP session ends with saved assets and a commit** so an MCP failure never loses more than one session | git branches, `M<n>-GATE` checklists in `build-sequence.md`, MCP session discipline | MCP instability (risk §8.6); binary `.uasset` merges are impossible — one-writer discipline, commit small and often | M1 onward (discipline, not a feature) |

### 3.2 Inputs, outputs, and acceptance per system

| # | System | Input dependency | Output produced | Acceptance condition |
|---|---|---|---|---|
| 1 | Third-person movement | `IA_Move` / `IA_Look` via `IMC_Duel` | Locomotion + camera follow in `L_ShatteredRing` | Either fighter moves and looks in PIE; boundary tests pass for both avatars; toggling presentation changes nothing (M1-GATE) |
| 2 | Camera and lock-on | `IA_LockOn`; `BP_CrimsonVanguard` existing | `LockedTarget`, strafe-facing, HUD reticle | Acquire, hold through lateral movement (side-on readability), break on press/range/death |
| 3 | Character selection | Player click in `WBP_CharacterSelect` | Selected `DA_FighterProfile` in Game Instance; level open | Either avatar enters the same complete duel (GDD definition of done) |
| 4 | Shared fighter data | Selection from #3 | Applied mesh, scale, capsule, speed, accent color | No subclass, no fighter branch; both avatars pass identical collision/targeting/reach tests |
| 5 | Light attack sequence | `IA_LightAttack`; `State.Attacking` gate | Combo chain, hits via #16, +5 at finisher notify | Chains inside `ANS_ComboLink`, drops outside it; finisher fires exactly once per completed chain |
| 6 | Input buffering | `IA_LightAttack` inside `ANS_ComboLink`; `IA_Impact` timing | `bComboBuffered` (combo only); discarded pre-window `IA_Impact` presses | Sandbox test three-way pass (chain / drop / discard); M3 gate confirms pre-open Impact press is discarded |
| 7 | Dodge | `IA_Dodge` + `IA_Move` direction | Directional root-motion dodge, `State.Invulnerable` during `ANS_IFrame` | Visible i-frames: an attack during the window deals 0 |
| 8 | Perfect dodge | Rival `ANS_ActiveHit` trace landing during `State.PerfectWindow` | Damage 0, +12 meter, Impact Window request | Detected only by the same trace that decides damage; ordinary dodge grants no meter |
| 9 | Counter | `IA_Counter` during `State.CanCounter` (from rival `ANS_CounterWindow`) | Rival interrupt → Recover, +15 meter, Impact request; whiff → punishable recovery | Counter works only during the authored window; rival returns to Neutral after every counter (M2-GATE) |
| 10 | Player health | `ApplyDamage` from rival hits | `OnHealthChanged` → HUD; `OnDeath` → Loss | Invulnerable early-return works; death ends duel in Loss exactly once |
| 11 | Rival health | `ApplyDamage` from player hits (× `ANS_Recover` multiplier) | `OnHealthChanged` → Phase 2 pending, Clash gate; `OnDeath` → Win (via Clash) | 50% and 25% thresholds fire once each; 1 HP floor holds during Clash failure |
| 12 | Vanguard controller | `BeginPlay`; player pawn exists | Running `BT_CrimsonVanguard` with `TargetActor` set | Tree starts and ticks; Gameplay Debugger shows keys |
| 13 | Six-state flow | Blackboard keys; montage notify ends; failsafe timers | Continuous state cycle, `CurrentState` always truthful | Cycles for several minutes, no deadlock; Returns to Neutral on **every** attempt incl. countered, out-of-range, idle player (M2-GATE) |
| 14 | Four data-driven attacks | `DT_VanguardAttacks` rows; `DistanceToTarget`; cooldown stamps | `SelectedAttack` + montage playback per row | Exactly four rows; selection is weighted, in-range, off-cooldown, deterministic logic; D's travel never exceeds `MaxTravelDistance` |
| 15 | T/A/R windows | Montage playback; phase tuning scales | Readable telegraph → hitbox frames → punish opening | Windows retunable by dragging notifies only; active window identical in both phases |
| 16 | Hit detection/reaction | `ANS_ActiveHit` tick; sockets; `AttackTrace` channel | `ResolveIncomingHit` branch result; hit-react montage | No multi-hit per window; no tunnelling; traces visible with `bDrawHitTraces` |
| 17 | Ascension Meter | `AddMeter(E_MeterEvent)` from the five hooks | `Meter` 0–100, `OnMeterChanged` → HUD + Clash gate | All five gains match the table verbatim; no time-based gain exists; only sanctioned writes |
| 18 | Impact trigger | The three earned events; director refusal checks | Open window (0.75 s first / 0.35–0.50 s standard) + prompt | First window only on first perfect dodge/counter; refusals all work; doing nothing never succeeds (M3-GATE) |
| 19 | Impact branches | `IA_Impact` during `bWindowOpen`, or expiry | SUCCESS (+20, burst, restore) / FAILURE (restore, cooldown) | After either branch: input, collision, locomotion, lock-on restored; rival BT running |
| 20 | Phase 2 | CV health ≤ 50%; Return to Neutral reached | `bPhase2` true, one-shot signal, Phase2 tuning live | Commits only on Return to Neutral; signals exactly once; same four attacks; active window unchanged (M4-GATE) |
| 21 | Clash gate | `OnMeterChanged` + CV `OnHealthChanged` | `bClashEligible`; two HUD indicators; `IA_FinalClash` acceptance | AND-gate holds; player-initiated only, in neutral or post-counter window |
| 22 | Clash success | Both beats hit | Finisher, rival death, `EndDuel(Win)`, Win screen | Both beats required; restore runs before the result screen |
| 23 | Clash failure | Any beat missed | Seven-step recovery, duel continues | Meter 50, CV at 1 HP floor, 3 s cooldown, full control, no restart, no player damage (M4-GATE explicitly fails one Clash) |
| 24 | Win/loss | `EndDuel(Win/Loss)` | `WBP_Result` + restart | Both outcomes reachable by both avatars, start to finish |
| 25 | Debug visibility | `bShowStateNames`; Gameplay Debugger | On-screen state string + Blackboard dump | The drawn state can never disagree with the executing task (first-node convention) |
| 26 | Kill-switch | `WBP_DebugPanel` toggle | Presentation on/off wholesale | Disabling presentation changes zero timing (verified at every gate from M1) |
| 27 | Clean return | Every overlay branch end | Restored full combat state | No stranded cinematic state anywhere; one function, four call sites (five with duel start) |
| 28 | Save/test/VC | Milestone gates; MCP sessions | Gate commits, sandbox branches, PIE checklists | Every milestone has a known-good rollback commit; no experiment touches the main build unproven |

---

## 4. Unreal architecture map

All names are the ones already approved in `design-brief.md` §2 and used throughout `build-sequence.md`. Nothing is renamed. Content root: `/Game/AscendantImpact/`.

```
BP_DuelDirector (Actor, Core/) ── duel state, selected profile, phase flags, EndDuel(Result)
   │
   ├── BP_PlayerFighter (Character, Player/)          ← the ONE player class; Echo/Nova are data
   │      ├── DA_FighterProfile (PrimaryDataAsset, Data/)   → DA_FighterProfile_Echo / _Nova
   │      ├── BP_HealthComponent (shared class)
   │      ├── BP_AscensionComponent (meter 0–100, M3)
   │      ├── BP_CombatComponent (tags, ResolveIncomingHit, combo buffer)
   │      ├── BP_LockOnComponent (single-target soft lock)
   │      └── ABP_Fighter (one AnimBP; stance via additive from the profile)
   │
   ├── BP_CrimsonVanguard (Character, Rival/)
   │      ├── BP_HealthComponent (same shared class)
   │      ├── BP_VanguardCombatComponent (reads DT_VanguardAttacks; bCounterable;
   │      │        IncomingDamageMultiplier; OnCounterWindowOpen / OnCountered)
   │      └── BP_VanguardController (AIController)
   │             ├── BT_CrimsonVanguard  (Selector: [bInClash → BTTask_WaitIndefinite]
   │             │        | Sequence "Attack Cycle" under Loop(Infinite):
   │             │          BTTask_Idle_Reposition → BTTask_SelectAttack → BTTask_Telegraph
   │             │          → BTTask_ActiveAttack → BTTask_Recover → BTTask_ReturnToNeutral;
   │             │        services: BTService_UpdateCombatData, BTService_DrawDebugState)
   │             └── BB_CrimsonVanguard  (TargetActor, CurrentState, SelectedAttack,
   │                      bPhase2, DistanceToTarget, bCounteredThisAttack, bInClash)
   │
   ├── BP_ImpactWindowDirector (Actor, Core/)   ← opens/scores Impact Windows
   ├── BP_FinalClashDirector  (Actor, Core/)    ← double gate, two beats, seven-step failure
   └── BP_PresentationSubsystem (GameInstanceSubsystem, Core/)
              ← ALL hit-stop / camera-shake / VFX / sound / time-dilation calls; kill-switch
```

| Category | Assets |
|---|---|
| Player character | `BP_PlayerFighter` (`Player/`) — no `BP_Echo`, no `BP_Nova`, no children |
| Shared combat component | `BP_CombatComponent` — `State.*` tag container, `ResolveIncomingHit`, `bComboBuffered` |
| Fighter profile data | `DA_FighterProfile` + `DA_FighterProfile_Echo` / `DA_FighterProfile_Nova` (`Data/`) |
| Health component | `BP_HealthComponent` — one class on both fighters; `MinHealthFloor` = Clash 1 HP mechanism |
| Ascension component | `BP_AscensionComponent` + `DT_MeterGains` (`S_MeterGain`, five rows) |
| Lock-on component | `BP_LockOnComponent` |
| Rival character | `BP_CrimsonVanguard` (`Rival/`) + `BP_VanguardCombatComponent` |
| Rival controller | `BP_VanguardController` (AIController; no AI Perception) |
| Behavior assets | `BT_CrimsonVanguard`, `BB_CrimsonVanguard`, `BTTask_Idle_Reposition`, `BTTask_SelectAttack`, `BTTask_Telegraph`, `BTTask_ActiveAttack`, `BTTask_Recover`, `BTTask_ReturnToNeutral`, `BTTask_WaitIndefinite`, `BTService_UpdateCombatData`, `BTService_DrawDebugState` |
| Attack data | `S_VanguardAttackDef`, `S_AttackPhaseTuning`, `DT_VanguardAttacks` (exactly four rows A–D), `DA_TuningGlobals`, enums `E_VanguardState`, `E_VanguardAttackID`, `E_MeterEvent`, `E_ImpactTrigger` |
| Impact Window director | `BP_ImpactWindowDirector` |
| Final Clash director | `BP_FinalClashDirector` + `LS_FinalClash`, `AM_Clash_Beat1`, `AM_Clash_Finisher` |
| Duel director | `BP_DuelDirector` + `LS_VanguardEntrance` (skippable) |
| UI widgets | `WBP_HUD` (meter bar, reticle, two Clash gate indicators, CV short label left BLANK — Q29), `WBP_ImpactPrompt` (reused for both Clash beats), `WBP_CharacterSelect`, `WBP_Result` (Win/Loss + restart), `WBP_DebugPanel` |
| Debug & presentation controls | `BP_PresentationSubsystem` (`bPresentationEnabled`, `bShowStateNames`, `bDrawHitTraces`, the five wrappers), `WBP_DebugPanel`, `BTService_DrawDebugState`, Gameplay Debugger |
| Player animation | `ABP_Fighter`, `AM_Player_LightCombo`, `AM_Player_Dodge`, `AM_Player_Counter`, `AM_Player_CounterWhiff`, shared hit-react montage in the profile `MontageSet` |
| Rival animation | `AM_Vanguard_AttackA/B/C/D`, `AM_Vanguard_CounterReact` |
| Notifies (`Notifies/`) | `ANS_Telegraph`, `ANS_ActiveHit` (one class, both fighters), `ANS_Recover`, `ANS_CounterWindow`, `ANS_ComboLink`, `ANS_IFrame`, `ANS_PerfectDodge`, `ANS_TrackingLock`, `AN_ComboFinisher` |
| Input (`Input/`) | `IMC_Duel`; `IA_Move`, `IA_Look`, `IA_LightAttack`, `IA_Dodge`, `IA_Counter`, `IA_LockOn`, `IA_Impact`, `IA_FinalClash` |
| Levels (`Arena/`) | `L_ShatteredRing` (the one arena; central floor, far doorway, `PS_VanguardEntrance`, `PS_VanguardCombatMark`, blocking-volume ring, Kill Z, no hazards), `L_CharacterSelect` (menu level, not an arena) |
| Gameplay tags | `State.Attacking`, `State.Dodging`, `State.Invulnerable`, `State.PerfectWindow`, `State.CanCounter`, `State.InImpactWindow`, `State.Clashing`, `Rival.Phase2` — registered in Project Settings, no GAS |

The Impact success burst is "a montage pair on both fighters" (design-brief §7.4 / build step M3-07); the pair's asset names are not fixed upstream — proposed `AM_ImpactBurst_Player` / `AM_ImpactBurst_Vanguard`, final naming `OPEN — designer decides` (cosmetic, no system effect).

---

## 5. Data flow

### 5.1 The player chain

`Player input → shared combat framework → combat result → Ascension event → Impact Window eligibility → prompt resolution → cinematic handoff → recovery → normal gameplay`

1. **Player input.** `IMC_Duel` maps hardware to `IA_*` actions. `BP_PlayerFighter` receives `Triggered` events; `BP_CombatComponent` gates them with `State.*` tags (e.g. no new attack while `State.Attacking`).
2. **Shared combat framework.** The action plays a montage from the profile's shared `MontageSet` (`AM_Player_LightCombo` section, `AM_Player_Dodge` direction, `AM_Player_Counter`/`_CounterWhiff`). Notify states on the timeline open and close every window: `ANS_ComboLink` (buffer accept), `ANS_ActiveHit` (player hit frames), `ANS_IFrame` ⊃ `ANS_PerfectDodge` (defense). Echo vs. Nova changes only profile data (mesh, scale, stance additive, play rate, speed, accent color) — never the path taken.
3. **Combat result.** All incoming rival hits resolve through one function: rival `ANS_ActiveHit` trace → `BP_CombatComponent.ResolveIncomingHit` → perfect dodge (0 dmg) / ordinary dodge (0 dmg, no meter) / hit (`BP_HealthComponent.ApplyDamage`). Player hits on the rival run the same `ANS_ActiveHit` class → rival `ApplyDamage` (× the `ANS_Recover` punish multiplier when open). Counter success is the one legal rival interrupt, routed through the BT sequence.
4. **Ascension event.** The result calls `BP_AscensionComponent.AddMeter(E_MeterEvent)` — five hooks, one table (`DT_MeterGains`), one clamp: +5 / +12 / +15 / +20 / +0. `OnMeterChanged` updates `WBP_HUD` and re-evaluates the Clash gate.
5. **Impact Window eligibility.** Perfect dodge, counter, or `AN_ComboFinisher` calls `BP_ImpactWindowDirector.RequestImpactWindow(trigger)`. The director refuses if a window is open, the cooldown (Q26) is running, `bInClash` is true, or either fighter is dead. Otherwise it opens the first window (0.75 s, first perfect dodge/counter only) or a standard window (0.35–0.50 s).
6. **Prompt resolution.** `WBP_ImpactPrompt` shows; a `Set Timer by Event` runs. `IA_Impact` while `bWindowOpen` → SUCCESS. Expiry → FAILURE. A press before the window opened was discarded — never queued.
7. **Cinematic handoff.** SUCCESS: +20 meter, the 1–3 s burst montage pair on both fighters; hit-stop/shake/VFX requested **through `BP_PresentationSubsystem`** (empty until M5, so in Phase 1 the burst is the montage pair alone). FAILURE: no extension, no meter, no punishment.
8. **Recovery.** Both branches end in the single `RestoreCombatState()`: input, collision, locomotion, transient tags, lock-on, time dilation, rival BT, prompt hidden.
9. **Normal gameplay.** The rival's Attack Cycle continues; the loop repeats. At `Meter = 100` AND CV ≤ 25%, `IA_FinalClash` (neutral or post-counter) enters the same shape at larger scale: two chained prompt beats → `AM_Clash_Finisher`/Win or the seven-step failure recovery → back to this chain.

### 5.2 The rival chain

`Crimson Vanguard selection → Telegraph → Active Attack → Recover → Return to Neutral`

1. **Idle / Reposition** (0.60–1.20 s P1 / 0.35–0.80 s P2): face target (`Set Focus`), `Move To Actor` if no attack row's range band contains `DistanceToTarget` (refreshed by `BTService_UpdateCombatData`); exits on timer **and** valid range.
2. **Select Attack** (0.10–0.20 s): filter the four `DT_VanguardAttacks` rows to in-range and off-cooldown; weighted pick by the **active phase's** `SelectionWeight` (one `Select` node on `bPhase2`); write `SelectedAttack`; stamp cooldown. Deterministic authored logic — the only randomness is the authored weighting.
3. **Telegraph** (0.55–0.95 s P1 / 0.40–0.75 s P2): play the row's montage at `TelegraphScale`; `ANS_Telegraph` holds the committed pose, sets the red-orange warning color (VFX via subsystem, empty until M5), broadcasts `OnTelegraphStart(AttackID)`; `ANS_CounterWindow` opens over late telegraph/early active. The attack is now committed.
4. **Active Attack** (0.18–0.45 s, **identical both phases by design**): `ANS_ActiveHit` sweeps sockets frame to frame; `ANS_TrackingLock` freezes facing where the row asks (B, C); attack D travels under root motion hard-capped at `MaxTravelDistance` — no hidden full-arena snap. Hits resolve through the player's `ResolveIncomingHit`.
5. **Recover** (0.45–0.90 s P1 / 0.35–0.75 s P2): `ANS_Recover` raises `IncomingDamageMultiplier` — the deliberate punish opening. No cancel, no new attack. If `bCounteredThisAttack`, `AM_Vanguard_CounterReact` plays instead.
6. **Return to Neutral** (0.10–0.20 s): clear every attack flag, restore multiplier and tracking, `Set Movement Mode (Walking)`, clear montage; **then and only then** commit Phase 2 if pending (one-shot signal). The `Sequence` completes and the `Loop` restarts at step 1. Every task sets `CurrentState` first and carries a failsafe timer (Q18), so the cycle reaches Neutral on every attempt — the M2 gate.

Cross-links into the player chain: `ANS_CounterWindow` → `State.CanCounter`; a successful counter forces this chain from wherever it is into Recover (the one legal interrupt); `bInClash` parks this chain on `BTTask_WaitIndefinite` until `RestoreCombatState()` releases it.

---

## 6. Milestone implementation map

The step-by-step build is `build-sequence.md` (M1-01 … M5-08); this map states each milestone's integration contract. Free proxy-asset **selection** is allowed throughout M1–M4; tuned presentation is M5 only. Rollback points are git commits on the build branch at each gate.

### M1 — Combat gray box
- **Inputs:** approved foundation (this plan §1); UE 5.8 Third Person template project; Unreal MCP connected; sandbox combo-buffer test result recorded (if the designer runs it); free proxy assets identified per design-brief §12.
- **Implementation tasks:** build steps M1-01 → M1-23 — project + folders + tags + `AttackTrace`; `BP_PresentationSubsystem` wired **empty** + `WBP_DebugPanel`; shared `BP_HealthComponent`; `BP_DuelDirector`; Enhanced Input; `BP_PlayerFighter` + `DA_FighterProfile` ×2 + `ApplyFighterProfile` + `ABP_Fighter`; `BP_CombatComponent` (`ResolveIncomingHit`); `BP_LockOnComponent`; `AM_Player_LightCombo` + `AM_Player_Dodge` + counter montages with all player notify states; gray-box `L_ShatteredRing`; `WBP_CharacterSelect` + `L_CharacterSelect`; dressed proxies.
- **Artifact outputs:** the entire Player/, Core/, Input/, UI/ foundation; playable one-sided combat sandbox.
- **Pass condition (M1-GATE):** either fighter selected → enters arena → moves, locks on, chains combo, dodges with visible i-frames, whiffs a counter, takes damage, dies; **both avatars pass the same collision, targeting, reach, and arena-boundary tests**; presentation off changes no timing.
- **Rollback point:** git commit `M1-GATE` (plus a pre-M1 commit of the empty project).
- **Dependencies:** none on later milestones. MCP availability. No designer numbers strictly required (all M1 `OPEN` values exist as exposed variables at placeholder-neutral defaults the designer will set).

### M2 — Rival state loop
- **Inputs:** M1-GATE commit; the Crimson Vanguard proxy from the §12.4 fallback ladder (option 1 ships regardless).
- **Implementation tasks:** M2-01 → M2-14 — enums; `S_AttackPhaseTuning` + `S_VanguardAttackDef` + `DT_VanguardAttacks` (all four rows created, only A authored) + range-validation check; `BP_CrimsonVanguard` + `BP_VanguardCombatComponent` + `BP_VanguardController` + `BB_CrimsonVanguard` + `BT_CrimsonVanguard`; both BT services; six `BTTask_*` with the first-node convention and failsafe timers; `AM_Vanguard_AttackA` with `ANS_Telegraph`/`ANS_ActiveHit`/`ANS_Recover`/`ANS_CounterWindow`; counter interrupt routed through the sequence.
- **Artifact outputs:** the entire Rival/ tree; Attack A live; visible debug state names.
- **Pass condition (M2-GATE):** rival cycles all six states continuously for several minutes with no deadlock and reaches Return to Neutral on **every** attempt — countered mid-attack, player out of range mid-telegraph, player standing still; player can dodge, perfect-dodge, and counter Attack A.
- **Rollback point:** git commit `M2-GATE`.
- **Dependencies:** M1 only. Q10/Q24 (range bands vs. arena footprint) flagged as the likely early bug source — surfaced to the designer during this milestone, not after.

### M3 — Impact handoff
- **Inputs:** M2-GATE commit (a real rival attack must exist to earn a window against).
- **Implementation tasks:** M3-01 → M3-08 — meter/impact enums; `DT_MeterGains` (five GDD rows verbatim); `BP_AscensionComponent` (one write path); `WBP_HUD`; all five meter hooks; `WBP_ImpactPrompt`; `BP_ImpactWindowDirector` (two widths, `bFirstWindowConsumed`, refusal checks, the three onboarding prohibitions); `RestoreCombatState()` written once.
- **Artifact outputs:** the earned real-time-to-cinematic handoff, both branches, the single restore path.
- **Pass condition (M3-GATE):** perfect dodge or counter opens a prompt; hit → +20 and the burst; miss → return with no punishment and no meter; doing nothing never succeeds; a pre-open `IA_Impact` press is discarded; after either branch the player has input, collision, locomotion, lock-on and the rival BT is running.
- **Rollback point:** git commit `M3-GATE`.
- **Dependencies:** M1 + M2. This gate is also the **vertical-slice proof** (§7).
- **Q26** (standard-window cooldown) needed from the designer here.

### M4 — Complete duel
- **Inputs:** M3-GATE commit; designer answers trending in for Q1–Q4 (health/damage economy), Q10/Q12/Q13 (ranges/cooldowns/travel), Q19–Q22 (Clash specifics — **Q22 before M4-08 is finalized**), Q25 (per-attack floats); Paragon-swap decision Q30 **before** range tuning if it is ever going to happen.
- **Implementation tasks:** M4-01 → M4-10 — attacks B, C, D authored on the same data path; `ANS_TrackingLock`; weighted selection across four rows; Phase 2 (pending at 50%, commit on Return to Neutral, one-shot signal, one `Select` node); `BP_FinalClashDirector` (double gate, HUD indicators, initiation rules, two reused prompt beats, `LS_FinalClash`); Clash success → Win; the exact seven-step failure recovery; `WBP_Result`; skippable `LS_VanguardEntrance`.
- **Artifact outputs:** the start-to-finish course prototype — **the 1 September deliverable**.
- **Pass condition (M4-GATE):** select Echo **or** Nova → entrance → Phase 1 → Phase 2 commits at 50% on Return to Neutral and signals exactly once → double gate → **fail a Final Clash and recover** (meter 50, 1 HP floor, 3 s cooldown, full control, duel continuing) → succeed → Win; separately die → Loss. Both avatars complete the full duel.
- **Rollback point:** git commit `M4-GATE`. Target functional completion **~20 August** (R7) to leave real tuning days.
- **Dependencies:** M1–M3. Late designer numbers are the schedule risk here, not engineering.

### M5 — Presentation pass (Phase 2 — only after M4 is stable; after 1 September)
- **Inputs:** stable M4-GATE commit; designer approvals for character treatment, VFX language, sound plan (Q31), Paragon/bespoke swaps (Q30).
- **Implementation tasks:** M5-01 → M5-08 — fill the already-wired `BP_PresentationSubsystem` wrappers (hit-stop/time-dilation, camera shake + choreography, authored Niagara, sound + mix); arena environmental reaction (still no hazards); final character treatment (re-validate capsule, sockets, ranges after any mesh swap); full-fidelity Clash choreography (gameplay beat logic unchanged); editorial selection interface.
- **Artifact outputs:** the polished game — camera, VFX, sound, arena reaction, final characters.
- **Pass condition:** every M5 change lands behind the subsystem or as swapped art; toggling `bPresentationEnabled` off still changes zero gameplay timing; the M4-GATE checklist still passes end to end.
- **Rollback point:** the M4-GATE commit — by construction, deleting all M5 content returns a working duel.
- **Dependencies:** all of M1–M4 stable. **M5 remains last; no M5 work is interleaved into M1–M4.**

---

## 7. One vertical-slice proof

This is the GDD's own PRESERVED gray-box vertical slice, stated as an integration-contract test. It is **not** a redesign of the duel; it proves the real-time-to-cinematic handoff once, end to end, with the minimum content. It falls out of the build naturally at the **M3-GATE** — no extra assets beyond what M1–M3 already produce.

| Element | Realization |
|---|---|
| One selected fighter | Echo proxy (`DA_FighterProfile_Echo` on `BP_PlayerFighter`) — Nova is validated separately at the milestone gates; the slice needs one |
| One Crimson Vanguard attack | Attack A (`AM_Vanguard_AttackA`, row A of `DT_VanguardAttacks`) driven by the full six-state loop |
| One readable telegraph | `ANS_Telegraph` on Attack A: held gauntlet pose + red-orange emissive, 0.55–0.95 s (Phase 1 range, per-attack float Q25) |
| One perfect dodge or counter | A perfect dodge: `IA_Dodge` timed so Attack A's `ANS_ActiveHit` trace lands during `State.PerfectWindow` → damage 0, +12 meter |
| One earned Impact Window | The perfect dodge fires `RequestImpactWindow(PerfectDodge)` → **First Impact Window, 0.75 s**, `WBP_ImpactPrompt` shown; the input is pressed by the player, never for them |
| One short cinematic extension | On `IA_Impact` inside the window: +20 meter and the 1–3 s burst montage pair on both fighters (presentation subsystem calls present but empty — Phase 1) |
| One knockback or stagger | The rival half of the burst pair is a stagger/knockback montage beat (reuses the `AM_Vanguard_CounterReact` stagger family); the rival is visibly displaced/reeled, then recovers |
| One clean return to gameplay | `RestoreCombatState()` → player input, collision, locomotion, lock-on live; rival BT resumes at `Idle_Reposition` with `CurrentState` visible; meter shows 32 (+12 +20) |

**Pass:** all eight beats occur in one unbroken PIE run, with `bShowStateNames` on, and the run also demonstrates the failure fork (a second attempt where the prompt expires → immediate return, no punishment, no meter). **Fail:** any stranded state, any auto-success, any timing change when `bPresentationEnabled` is toggled off. The slice result is recorded and committed before M4 begins.

---

## 8. Risks and fallback paths

### 8.1 Framework incompatibility (UE 5.8 assumptions)
- **Risk:** a stock-UE assumption fails in 5.8 — Third Person template rig differences, montage-section API behavior, notify-tick ordering.
- **Early warning sign:** the framework evaluation's §8 sandbox test (buffered light-attack chain) fails any of its three conditions; or M1-01 finds the template missing an assumed piece.
- **Fallback:** the design uses only long-supported stock features, so the fallback is local substitution (e.g., manual timer-driven combo advance instead of section-next if the section API misbehaves) — never a framework change; findings go to the designer before M1 proceeds.
- **Scope effect:** none; possibly a few days of M1 schedule.
- **Human decision required:** whether/when to run the sandbox test, and acceptance of any substitution. `OPEN — designer decides`.

### 8.2 Animation retargeting (R1/R4)
- **Risk:** sourcing and retargeting free melee animations — and above all the 6'10" Crimson Vanguard proxy — eats weeks; a late mesh swap invalidates sockets, capsule, and every range value.
- **Early warning sign:** IK Retargeter cleanup on the first Mixamo/Paragon clip exceeds ~a day; trace sockets missing on a candidate skeleton; reach tests failing after a scale change.
- **Fallback (ladder, cheapest first):** UE5 Mannequins on the native skeleton for both fighters (zero retargeting); Vanguard = Mannequin scaled to 208 cm + static-mesh gauntlet/shoulder proxy blocks + red/black material — ships no matter what; the Paragon heavy swap only if the schedule holds and **before** M4 range tuning.
- **Scope effect:** none on systems; visual fidelity deferred to M5-06.
- **Human decision required:** Q30 (Paragon swap yes/no and by when); rights review on every asset at claim time. `OPEN — designer decides`.

### 8.3 Input-buffer conflict
- **Risk:** the combo buffer (presses inside `ANS_ComboLink` are queued) and the Impact/Clash anti-buffer (presses before a window opens are discarded) get implemented through one shared input path, and one policy leaks into the other — mashing then converts an Impact miss into a success, violating the GDD onboarding rule.
- **Early warning sign:** mashing `IA_Impact` before a window ever succeeds; or a combo press inside the link window fails to chain after Impact code lands.
- **Fallback:** keep the two policies in separate components with no shared buffer variable (`bComboBuffered` lives in `BP_CombatComponent` and is read only by `ANS_ComboLink`; `BP_ImpactWindowDirector` accepts `IA_Impact` only while `bWindowOpen` and holds no queue at all); add both cases to the M3-GATE checklist.
- **Scope effect:** none.
- **Human decision required:** Q28 (combo buffer width), Q17 (whether Clash beats share `IA_Impact`). `OPEN — designer decides`.

### 8.4 Camera/control restoration after cinematic branches
- **Risk:** an Impact burst, `LS_FinalClash`, or `LS_VanguardEntrance` ends with the player input disabled, collision off, time dilation ≠ 1, lock-on lost, or the rival BT parked — a stranded cinematic state.
- **Early warning sign:** any post-overlay frame where the debug panel shows a lingering transient tag, the Gameplay Debugger shows the BT still on `BTTask_WaitIndefinite`, or the camera does not return to the spring arm.
- **Fallback:** the single `RestoreCombatState()` is the design's own defense — every branch must end in it, including sequence-abort paths (Level Sequence `OnStop`/`OnFinished` both route there); if a Level Sequence camera cut proves fragile under MCP-built content, the Phase 1 fallback is **no camera cut at all** (montage pair on the gameplay camera), which loses nothing gameplay-tests care about.
- **Scope effect:** none; a cut-less Clash is visually plainer in Phase 1 and is restored in M5-07.
- **Human decision required:** acceptance of a cut-less Phase 1 Clash if it comes to that. `OPEN — designer decides`.

### 8.5 Attack-data mismatch (row vs. montage)
- **Risk:** a `DT_VanguardAttacks` row and its montage drift apart — a montage missing `ANS_CounterWindow`, a `TelegraphScale` that pushes an authored window outside its GDD range, a D-row travel exceeding `MaxTravelDistance`, an active window that differs between phases.
- **Early warning sign:** the M2-04 editor-time range-validation check flags a row; an attack is un-counterable in playtest; attack D crosses more arena than its cap.
- **Fallback:** extend the validation check to structural assertions (every attack montage must carry exactly the required notify classes; D's root-motion extent measured against `MaxTravelDistance`) — the check **flags, never picks**; a flagged attack is pulled from the selection filter until fixed, and the loop keeps running on the remaining rows (the tree cannot deadlock on a filtered set as long as one row stays valid — if zero remain, `BTTask_SelectAttack`'s failsafe exits and Reposition resumes).
- **Scope effect:** none — four rows remain four rows.
- **Human decision required:** the per-attack floats themselves (Q25, Q10, Q12, Q13, Q3). `OPEN — designer decides`.

### 8.6 Unreal MCP instability
- **Risk:** the MCP server that drives the editor drops mid-session, corrupts an asset write, or cannot express an editor action the sequence needs — the build stalls or loses work.
- **Early warning sign:** the first M1 session cannot complete a simple asset-create/save round trip; repeated disconnects; assets on disk not matching what the session reported.
- **Fallback:** MCP session discipline from §3.1 row 28 — small sessions, save + git commit at each step group, so a failure loses at most one session; anything the MCP cannot drive is written up as an exact manual editor instruction (the build sequence already names paths, menus, and node names for precisely this reason) and executed by the human.
- **Scope effect:** none on the game; schedule effect if large parts fall back to manual execution.
- **Human decision required:** whether the human executes manual steps or waits for MCP repair. `OPEN — designer decides`.

### 8.7 External plugin failure
- **Risk:** an optional plugin the plan touches misbehaves in 5.8 — realistically only **Motion Warping** (R5, considered for attacks B/D) since the approved foundation adopts no marketplace framework, no GAS, no AI Perception, no State Tree.
- **Early warning sign:** warp targets overshooting or ignoring the distance cap in a disposable test; retarget interactions with the chosen proxy skeleton.
- **Fallback:** the design's own R5 fallback is already the default — **root-motion montages with a hard distance cap** plus a pre-attack `Move To` reposition; Motion Warping is only attempted if the schedule holds at the M2 review, and only on a disposable branch first. No other external code enters the build without the human gate.
- **Scope effect:** none — the cap is data either way; D can never full-arena snap.
- **Human decision required:** whether Motion Warping is attempted at all; whether any external code ever enters the course build. `OPEN — designer decides`.

### 8.8 Schedule pressure (R7)
- **Risk:** 36 days remain; if M4 completes on 31 August there is zero tuning time and every provisional number ships untested.
- **Early warning sign:** any milestone gate slipping more than ~3 days past its internal target; open designer questions (especially Q1–Q4, Q10, Q22, Q25) unanswered when their milestone starts.
- **Fallback:** the cut order is already law — a complete fought duel beats a beautiful incomplete one. Cuts come from asset fidelity (stay on Mannequin proxies, cut-less Clash camera, silent build per Q31) never from systems inside the scope lock; M4 targets functional completion **~20 August**; designer questions are batched to the designer at each gate rather than trickled.
- **Scope effect:** Phase 1 visual floor only; M1–M4 systems are not cuttable.
- **Human decision required:** the tuning-time trade itself, Q31 (silent build), and every batched value. `OPEN — designer decides`.

---

## 9. Open human decisions

None of these are resolved in this document. All carry through from design-brief §14 / build-sequence Appendix B, plus the integration-level decisions this plan adds. Every one is `OPEN — designer decides`.

**Foundation & process**
1. Run the framework-evaluation §8 sandbox test (buffered combo chain), and on which machine/branch — `OPEN — designer decides`
2. Whether any external code, plugin (incl. Motion Warping), or paid product ever enters the course build; all purchases and plugin adoptions — `OPEN — designer decides` (this plan assumes none)
3. Final framework installation details (project location, branch layout for the Unreal project itself) — `OPEN — designer decides`
4. Licensing/rights acceptance for every free asset at claim time (Mannequins, Mixamo, Fab, Paragon) — `OPEN — designer decides`
5. Manual-execution fallback policy if the Unreal MCP fails (§8.6) — `OPEN — designer decides`
6. Acceptance of a cut-less Phase 1 Final Clash camera if the Level Sequence handoff proves fragile (§8.4) — `OPEN — designer decides`
7. Names for the Impact burst montage pair (proposed `AM_ImpactBurst_Player`/`_Vanguard`; cosmetic) — `OPEN — designer decides`

**Timing and tuning (design-brief §14, carried unchanged)**
8. Q1 player max health · Q2 CV max health · Q3 per-attack damage A–D · Q4 player light-hit damage/finisher bonus — `OPEN — designer decides`
9. Q5 combo length · Q6 dodge i-frame window · Q7 perfect-dodge sub-window · Q8 whiffed-counter recovery · Q28 combo-link buffer window — `OPEN — designer decides`
10. Q9 meter decay (brief recommends none) · Q23 duel timer (brief recommends none) · Q26 standard Impact-Window cooldown · Q27 `ANS_Recover` damage multiplier — `OPEN — designer decides`
11. Q10 range bands · Q11 lock-on ranges/interp · Q12 per-attack cooldowns · Q13 attack-D max travel · Q24 arena footprint · Q25 per-attack floats inside every GDD state range · Q18 BTTask failsafe margin — `OPEN — designer decides`
12. Q17 whether Clash beats reuse `IA_Impact` · Q19 post-counter Clash window · Q20 Clash beat 1/2 response times (within/near the approved 0.35–0.50 s question — not resolved here) · Q21 failed-Clash separation distance · **Q22 whether the 1 HP floor is permanent or Clash-only (the single most consequential open question — needed before M4-08 is final)** — `OPEN — designer decides`

**Character differentiation and presentation**
13. Q14/Q15/Q16 Echo vs Nova play-rate, walk speed, dodge distance — including whether they differ **at all** in Phase 1 — `OPEN — designer decides`
14. Final animation set (shared set for Phase 1 per R1; any second set is a Phase 2 upgrade) — `OPEN — designer decides`
15. Final character differentiation beyond profile scalars, and any signature cinematic variation (GDD: deferred until the base duel is stable) — `OPEN — designer decides`
16. Final cinematic lengths beyond the approved ranges (Impact burst stays within the GDD's 1–3 s; entrance stays short and skippable) — `OPEN — designer decides`
17. Q29 Crimson Vanguard's short in-combat UI label (GDD lists it unfinalized; HUD field stays blank) · Q30 Paragon heavy swap and its deadline (before M4 range tuning) · Q31 whether Phase 1 ships silent — `OPEN — designer decides`

---

## 10. Acceptance checklist

This plan passes only if every line below holds. Self-audit against the documents on disk:

- [x] **Every required system maps to the approved foundation** — all 28 systems in §3.1/§3.2 map to stock UE 5.8 capability plus the approved custom design; every one names its assets, inputs, outputs, risk, milestone, and acceptance condition; no system requires an unapproved framework.
- [x] **Echo and Nova remain one shared framework** — one `BP_PlayerFighter`, two `DA_FighterProfile` instances, one `ABP_Fighter`, one `MontageSet` in Phase 1; no subclass, no fighter branch anywhere in this plan (§2.1, §3.1 rows 4–9).
- [x] **Crimson Vanguard remains deterministic** — `BT_CrimsonVanguard` + Blackboard + Data Table; only authored-weighted selection; no runtime LLM/model call, no learning, no adaptive behavior (§2.3, §3.1 rows 12–14, §5.2).
- [x] **Attacks remain four and data-driven** — exactly four rows in one `DT_VanguardAttacks`, one reusable data path, Phase 2 as the second struct in the same row; no fifth attack anywhere (§3.1 row 14, §5.2).
- [x] **Impact Windows remain earned** — three earned triggers only; no auto-success, no pre-open buffering, wider first window changes exactly one float (§3.1 rows 18–19, §5.1 steps 5–6).
- [x] **Final Clash rules remain unchanged** — meter 100 AND ≤25% double gate; two beats; success → win; failure → 1 HP floor, meter to 50, 3 s cooldown, seven-step recovery, no restart, no player death (§3.1 rows 21–23).
- [x] **All control and combat states restore after cinematics** — one `RestoreCombatState()` covering input, collision, locomotion, lock-on, camera/time dilation, AI state, tags; called by all four overlay branches (§3.1 row 27, §8.4).
- [x] **No runtime model calls are introduced** — none anywhere in this plan; assignment #04 tooling is offline authoring outside the game build (§2.3).
- [x] **M5 remains last** — §6 keeps M5 behind a stable M4; the empty-until-M5 `BP_PresentationSubsystem` is the structural guarantee; proxy-asset selection in M1–M4 is asset selection, not presentation work.
- [x] **Every open value remains human-owned** — every GDD number carried verbatim and marked provisional; all 29+ §14 values plus this plan's seven integration-level decisions listed as `OPEN — designer decides` in §9; nothing resolved.

Quality-failure self-check: this plan does not change the framework recommendation; assumes no marketplace template is installed (none is); invents no plugin behavior (Motion Warping is optional with its fallback already the default); converts nothing to PvP; forks nothing by fighter; changes no meter value, health threshold, timing range, or Final Clash recovery rule; adds no fifth attack; treats Unreal MCP as a build conduit, not the combat foundation; treats editor automation as execution, not design proof (the milestone gates and the §7 slice are the proof); and every system traces to a milestone and an acceptance condition.

---

*End of combat integration plan. The approved foundation is implemented as specified; every rule and number remains the human designer's to approve, change, or reject.*
