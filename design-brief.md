# Design Brief — Ascendant Impact

**Produced by:** designer agent (research-and-planning seat)
**Consumes:** `project-brief.md` (canonical input) · `gdd/ascendant-impact-gdd-v0.4.md` (source of truth)
**Produces:** this document, for the developer agent to turn into `build-sequence.md`
**Engine / platform:** Unreal Engine 5.8 / PC, third person
**Date written:** 2026-07-25 · **Ship date:** 2026-09-01 (**38 days**)

---

## 0. How to read this document

- **Every number in here comes from the GDD or the project brief, carried through unchanged.** No number was invented, rounded, or resolved. Section 13 collects them all in one table.
- Where the GDD is genuinely **silent** on a number the build needs, this brief says so, proposes a **range as a question**, and marks it `OPEN — designer decides`. Those are collected in section 14. **The developer must not pick a value from a proposed range on its own authority; it must implement the number as a designer-exposed variable and leave it at whatever the human designer sets.**
- Every major decision names its **Unreal-side concept** and, where useful, a real editor path or Blueprint node name, so this can drive Blueprint work through the Unreal MCP server.
- **SCOPE LOCK is a wall.** Anything outside it is labelled *deferred future scope* and is not designed here.
- **The shipped game makes no runtime AI-model calls.** Crimson Vanguard is a deterministic authored Behavior Tree. Nothing in this brief proposes an LLM, a model API call, or adaptive/learning AI in the build.

### 0.1 GDD-vs-brief conflict check

I compared `project-brief.md` against `gdd/ascendant-impact-gdd-v0.4.md` line by line on every system it touches.

**No substantive conflict found.** All timing ranges, meter gains, the Final Clash double gate, the 50% Phase 2 threshold, the 1 HP floor, the meter-to-50 setback, the 3-second cooldown, the 0.75 s / 0.35–0.50 s Impact Windows, the six states, the four attacks, and the M1–M5 gates match the GDD exactly.

Three things in `project-brief.md` are **commander additions that are not in GDD v0.4**, and are not contradictions:

| Addition | Status |
|---|---|
| **The 1 September 2026 ship date and the Phase 1 / Phase 2 split** | Not in the GDD. It is a schedule constraint layered on top and it **governs this brief.** |
| **The $0 budget / free-asset constraint** | Not in the GDD. Governs section 12. |
| **"A thin presentation floor" after M4 in Phase 1** | Not in the GDD's milestone table. Reconciled in section 11.6 — it is satisfied by **asset selection**, not by pulling M5 work forward. |

One sequencing detail worth stating plainly so nobody reads it as a contradiction: **M2's gate requires all six states and *one* attack.** All four attacks A–D are required by **M4**, not M2. That is what both documents say.

Pages 10–14 of the GDD are supplied image reference sheets with no extractable text. **Nothing in this brief describes or infers their contents.** Where a visual decision would have depended on them (exact costume geometry, exact arena layout), this brief defers to the human designer and says so.

---

## 1. The Phase 1 cut line — what ships on 1 September

This is the most important section in the document. **38 days.** Read this before anything else.

### 1.1 The governing rule

> **A complete, fought duel on 1 September beats a beautiful incomplete one.** Where two approaches both satisfy the GDD, this brief picks the one that ships.

### 1.2 IN the 1 September Phase 1 build

| System | Phase 1 realization | Milestone |
|---|---|---|
| Third-person movement + camera | UE Third Person template `SpringArmComponent` + `CameraComponent`, Enhanced Input | M1 |
| Lock-on | Single-target soft lock (one enemy exists), toggle on/off | M1 |
| Light attack sequence | Montage-section combo chain, shared by both fighters | M1 |
| Dodge + perfect dodge | One directional dodge montage, `ANS_IFrame` + nested `ANS_PerfectDodge` | M1 |
| Counter | Input inside `ANS_CounterWindow` opened by rival telegraph | M1 |
| Health (both sides) | `BP_HealthComponent`, shared class | M1 |
| Fighter selection | Two-button UMG screen (GDD's "simplified selection screen" allowance) | M1 |
| Echo and Nova both playable | One Blueprint class + `DA_FighterProfile` data asset | M1 |
| Rival six-state loop | Behavior Tree, one `BTTask` per state, linear `Sequence` under `Loop` | M2 |
| Attacks A–D | Rows in one `DT_VanguardAttacks` Data Table | M2 (one attack) → M4 (all four) |
| Telegraph / Active / Recover windows | `AnimNotifyState` on each attack montage | M2 |
| Impact Windows (first + standard) | Timer + UMG prompt + Enhanced Input action, success/fail branches | M3 |
| Ascension Meter 0–100 | `BP_AscensionComponent` + `DT_MeterGains` | M3 |
| Phase 2 | Same four rows, second timing struct in the same row | M4 |
| Final Clash: double gate, two beats, success, failure recovery | Two chained Impact-Window prompts + a `Level Sequence` camera cut | M4 |
| Win screen / Loss screen | Two UMG widgets, `BP_DuelDirector` | M4 |
| Abbreviated arena entrance | Short `Level Sequence`: CV walks in from the far doorway | M4 |
| **Dressed proxies** | Free character meshes, free animations, gray-box-plus arena with free industrial materials and props — see section 12 | ongoing, **asset selection, not a presentation pass** |
| Debug: visible state names, presentation kill-switch | `Draw Debug String` + `BP_PresentationSubsystem` toggle | M1 onward |

### 1.3 DEFERRED to Phase 2 (the full M5 polish pass)

Named as deferred. Not designed here.

- Tuned hit-stop feel, impact frames, time-dilation curves.
- Camera choreography: dynamic combat camera, framing rules, per-attack camera pushes, `Camera Shake` authoring.
- Authored Niagara VFX: telegraph energy, thruster plumes, warning-light systems, Ascension energy language, Echo's orange accents vs Nova's cyan-white combat energy as *authored effects* (Phase 1 gets these as flat emissive material colors only).
- Sound design and audio mix. There is no free sound source verified in this brief — see section 12.6.
- Arena environmental reaction on major impacts.
- Final character treatment: bespoke Echo / Nova / Crimson Vanguard meshes matching the GDD reference sheets.
- The editorial character-selection interface with technical/equipment panels animating around the selected fighter (Phase 1 uses the GDD's simplified-screen allowance).
- Full-fidelity Final Clash choreography.

### 1.4 DEFERRED FUTURE SCOPE (outside SCOPE LOCK entirely — never build)

Local or online PvP · unique Echo/Nova move sets or separate balance systems · a playable Crimson Vanguard kit · multi-enemy encounters · campaign progression · additional arenas · extended gauntlets · transformations · second boss kits · additional characters, modes, weapons, or story chapters · signature per-fighter cinematic variations.

### 1.5 RED FLAGS — systems in this brief that may not be buildable *and tunable* in 38 days

I am flagging these now rather than letting the developer discover them in August.

| # | System | Risk | Proposed mitigation (designer decides) |
|---|---|---|---|
| **R1** | **Two visually distinct animation sets for Echo and Nova** | Sourcing, retargeting, and tuning two full melee anim sets is the single largest time sink in the plan. | Ship **one shared montage set** for M1–M4. Differentiate Echo and Nova by `DA_FighterProfile` scalars (play-rate, movement speed, stance additive pose, capsule scale, emissive color). This is exactly what the GDD's SHARED PLAYER-KIT SCOPE RULE permits: differences are "animation presentation, stance and movement personality, VFX language, timing flavor." **A second anim set is a Phase 2 upgrade.** |
| **R2** | **Motion Matching / Game Animation Sample locomotion** | Beautiful and free, but integrating motion matching *and* retargeting it onto non-Mannequin proxy skeletons under a 38-day clock is a real risk of eating a week. | Use the **standard Third Person `AnimBP` blendspace locomotion** for Phase 1. Treat the Game Animation Sample as a Phase 2 upgrade, or as a source of individual animation assets rather than as a whole locomotion system. |
| **R3** | **Final Clash "two timing beats"** | The GDD requires two beats and a finishing sequence. A bespoke cinematic is not affordable. | Build both beats out of the **same `WBP_ImpactPrompt` + timer machinery** already built for M3, run back to back, with one `Level Sequence` camera cut and existing montages. This costs nearly nothing extra because the prompt system already exists. Full choreography → Phase 2. |
| **R4** | **Crimson Vanguard proxy at 6'10" with red armor, gauntlets, and thrusters** | No verified free asset matches this description. Retargeting a Paragon heavy hero is possible but its skeleton is UE4-era and needs an `IK Retargeter` pass. | See section 12.4. Fallback ladder, cheapest first. **This is the single biggest asset gap.** |
| **R5** | **Motion Warping on attacks B and D** | Motion Warping is the correct tool for "committed forward pressure" and "short propulsion approach" without hidden snapping, but it is another plugin + notify-state to learn. | Phase 1 acceptable fallback: **root-motion montages with a hard distance cap**, plus a pre-attack `Move To` reposition. Motion Warping only if the schedule holds at the M2 review. Either way, attack D's travel must be **capped** — the GDD forbids a hidden full-arena snap. |
| **R6** | **Arena "environmental reaction"** | GDD lists it as a Version 1 arena requirement, but it is presentation. | It is **M5 / Phase 2.** Phase 1 ships the four *functional* arena requirements (central floor, far doorway, reverse third-person framing, side-on readability). Flagged so nobody thinks it was forgotten. |
| **R7** | **Playtest time itself** | Every number in this game is provisional and needs playtest. If M4 completes on 31 August there is no tuning time. | **Target M4 functionally complete by ~20 August**, leaving ~10 days for the human designer to tune the section-13 table. This is a schedule request, not a design decision. |

---

## 2. Architecture at a glance

```
BP_DuelDirector (GameMode / Actor)  ── owns duel state, win/loss, phase flag
   │
   ├── BP_PlayerFighter (Character)              ← ONE class. Echo and Nova are data.
   │      ├── DA_FighterProfile (Primary Data Asset)   Echo | Nova
   │      ├── BP_HealthComponent                        (shared class)
   │      ├── BP_AscensionComponent                     meter 0–100
   │      ├── BP_CombatComponent                        montages, windows, state tags
   │      └── BP_LockOnComponent                        single-target soft lock
   │
   ├── BP_CrimsonVanguard (Character)
   │      ├── BP_HealthComponent                        (same shared class)
   │      ├── BP_VanguardCombatComponent                reads DT_VanguardAttacks
   │      └── BP_VanguardController (AIController)
   │             └── BT_CrimsonVanguard + BB_CrimsonVanguard
   │
   ├── BP_ImpactWindowDirector                    opens/scores Impact Windows
   ├── BP_FinalClashDirector                      double gate, two beats, failure path
   └── BP_PresentationSubsystem (GameInstanceSubsystem)
              ↑ every hit-stop / camera / VFX / sound call routes through here
                and can be switched off wholesale during diagnosis
```

**Content root:** `/Game/AscendantImpact/`

| Folder | Contents |
|---|---|
| `/Game/AscendantImpact/Core/` | `BP_DuelDirector`, `BP_PresentationSubsystem`, enums, gameplay tag table |
| `/Game/AscendantImpact/Player/` | `BP_PlayerFighter`, components, `ABP_Fighter`, montages |
| `/Game/AscendantImpact/Rival/` | `BP_CrimsonVanguard`, `BP_VanguardController`, `BT_CrimsonVanguard`, `BB_CrimsonVanguard`, BTTasks, montages |
| `/Game/AscendantImpact/Data/` | `DT_VanguardAttacks`, `DT_MeterGains`, `DA_FighterProfile_Echo`, `DA_FighterProfile_Nova`, `DA_TuningGlobals` |
| `/Game/AscendantImpact/Notifies/` | all `AnimNotify` / `AnimNotifyState` Blueprints |
| `/Game/AscendantImpact/Arena/` | `L_ShatteredRing`, arena meshes and materials |
| `/Game/AscendantImpact/UI/` | `WBP_HUD`, `WBP_ImpactPrompt`, `WBP_CharacterSelect`, `WBP_Result`, `WBP_DebugPanel` |
| `/Game/AscendantImpact/Input/` | `IMC_Duel`, `IA_*` Input Actions |

---

## 3. Framework decision — plain Blueprints, not GAS

**Decision: build the combat framework in Blueprints with Anim Montages, Anim Notify States, Gameplay Tags, and Data Tables. Do not use the Gameplay Ability System.**

Rationale, anchored to the ship date:

- GAS is Epic's production framework and is the right call for a game that will grow ability count, needs replication, or needs cooldown/cost bookkeeping across dozens of abilities. Ascendant Impact has **one player kit** (light combo, dodge, counter, Impact input, Clash input) and **four authored rival attacks**, is **single player**, and is **scope-locked against growth**. The GAS learning curve buys nothing this project will use.
- GAS setup — `AbilitySystemComponent`, `AttributeSet` (which realistically wants C++), `GameplayEffect` authoring, ability activation policies — is measured in days before the first punch lands. With 38 days, that is the wrong trade.
- **Gameplay Tags are available without GAS.** Register tags in *Project Settings → Project → GameplayTags* and hold an `FGameplayTagContainer` on `BP_CombatComponent`. This gives clean state gating (`State.Attacking`, `State.Dodging`, `State.Invulnerable`, `State.InImpactWindow`, `State.Clashing`, `Rival.Phase2`) with `Has Matching Gameplay Tag` / `Add Gameplay Tag` nodes and no GAS dependency.

**Flag for the human designer:** if this project is ever taken past the course prototype, GAS becomes the right foundation and the combat component would be rewritten. That is a Phase 2+ conversation, explicitly **deferred**, and this brief does not design it.

**Also not used, deliberately:**

- **`AI Perception`** — there is exactly one target, it always exists, and it is never hidden. `Get Player Pawn` into a Blackboard `TargetActor` key on `BeginPlay` is correct and free. Adding `AIPerceptionComponent` with a sight config would add configuration surface and failure modes for zero gameplay benefit. *Deferred; revisit only if a future scope adds more actors, which SCOPE LOCK forbids.*
- **`State Tree`** — see section 6.1 for why Behavior Tree is the ship choice in 5.8.

---

## 4. The one shared player-combat framework

This is the core anti-fork requirement: **Echo and Nova differ only in animation, stance, VFX flavor, and timing feel, and the framework must stay single-sourced.**

### 4.1 The single-source rule

> **There is exactly one player character Blueprint: `BP_PlayerFighter`. There is no `BP_Echo` and no `BP_Nova`. There are no child Blueprints of `BP_PlayerFighter`.**
>
> Echo and Nova are two instances of `DA_FighterProfile`, a `PrimaryDataAsset`. Selecting a fighter sets which asset gets applied. **If a behavior difference cannot be expressed as a field on `DA_FighterProfile`, it is out of scope for Phase 1 and must be surfaced to the designer, not implemented as a subclass.**

This is enforced structurally: any logic difference would require either a subclass or a `Switch on Fighter` branch inside combat code. Both are defects. The inspector should treat either as a scope-lock violation of the SHARED PLAYER-KIT SCOPE RULE.

### 4.2 `DA_FighterProfile` — the only place Echo and Nova differ

Unreal concept: **Primary Data Asset** (`PrimaryDataAsset` Blueprint class, instances `DA_FighterProfile_Echo` and `DA_FighterProfile_Nova`).

| Field | Type | Echo | Nova | Notes |
|---|---|---|---|---|
| `DisplayName` | Text | "Agent Echo" | "Agent Nova" | |
| `SkeletalMesh` | `SkeletalMesh` | proxy | proxy | section 12 |
| `AnimClass` | `AnimInstance` class | `ABP_Fighter` | `ABP_Fighter` | **same AnimBP**; stance comes from the additive below |
| `CharacterHeightCm` | float | **183** (GDD) | **173** (GDD) | drives mesh scale + capsule half-height |
| `StanceAdditivePose` | `AnimSequence` | upright / technical | compact / layered | applied as an **additive** in `ABP_Fighter`; this is the whole "stance personality" mechanism |
| `MontageSet` | struct of `AnimMontage` refs | shared set (Phase 1) | shared set (Phase 1) | see R1 |
| `MontagePlayRate` | float | `OPEN` | `OPEN` | **this is "timing flavor"** — see §14 Q14 |
| `MaxWalkSpeed` | float | `OPEN` | `OPEN` | Echo deliberate, Nova faster lateral — §14 Q15 |
| `DodgeDistance` | float | `OPEN` | `OPEN` | §14 Q16 |
| `AccentColor` | LinearColor | restrained **orange** | costume palette **preserved**; **cyan-white reserved for combat energy / telegraphs / selected VFX accents only** | GDD REVISED — COLOR DIRECTION. **Cyan-white is NOT a costume recolor.** |
| `IntroMontage` | `AnimMontage` | abbreviated | abbreviated | GDD's "character introduction" difference |

**Application:** `BP_PlayerFighter → Event BeginPlay → Get Selected Profile (from BP_DuelDirector) → Set Skeletal Mesh → Set Anim Instance Class → Set Actor Scale 3D → Set Capsule Half Height → Set Max Walk Speed → Set Vector Parameter Value on Materials (AccentColor)`. One function, `ApplyFighterProfile`, called once.

**Scale note (do not treat as a committed number):** the GDD gives heights 183 cm / 173 cm / 208 cm. The correct implementation is to **measure the chosen proxy mesh's actual height in the editor and scale to the GDD height**, not to hard-code a scale factor. The GDD's hard requirement is: *"The height difference must not create unfair hidden reach or collision behavior."* That is validated by the section 11 M1 gate — **both avatars run the same collision, targeting, reach, and arena-boundary tests.**

### 4.3 Input — Enhanced Input

Unreal concept: **Enhanced Input** (`InputMappingContext` + `InputAction`), the 5.x default. `Add Mapping Context` on `Event BeginPlay` in `BP_PlayerFighter`.

`/Game/AscendantImpact/Input/IMC_Duel` mapping:

| Input Action | Purpose | Value type |
|---|---|---|
| `IA_Move` | locomotion | Axis2D |
| `IA_Look` | camera | Axis2D |
| `IA_LightAttack` | light attack / combo advance | Digital |
| `IA_Dodge` | dodge (directional from `IA_Move`) | Digital |
| `IA_Counter` | counter | Digital |
| `IA_LockOn` | toggle lock-on | Digital |
| `IA_Impact` | Impact Window response + Final Clash beats | Digital |
| `IA_FinalClash` | initiate the Clash when eligible | Digital |

**Design note for the designer:** `IA_Impact` deliberately serves both the Impact Window and both Final Clash beats. One "timing input" that the player learns once and reuses is what the GDD's core-loop step 4 ("IMPACT — choose the timing input") describes, and it removes a whole class of onboarding problem. **`OPEN` — designer confirms whether the Clash beats use `IA_Impact` or a distinct binding (§14 Q17).**

### 4.4 Lock-on

Unreal concept: `SpringArmComponent` + `CameraComponent` + a small `BP_LockOnComponent`.

Because there is exactly one opponent, this is deliberately the simplest correct thing:

1. `IA_LockOn` pressed → if not locked, and `BP_CrimsonVanguard` is within `LockOnMaxRange` and in front of the camera → set `LockedTarget`.
2. While locked, on `Event Tick`: `Find Look at Rotation` (camera → target) → `RInterp To` → `Set Control Rotation`. Interp speed is a soft-lock feel value.
3. While locked, set `Character Movement → bOrientRotationToMovement = false` and `bUseControllerDesiredRotation = true` so the fighter strafes facing the rival. This is what produces the GDD's **side-on readability** requirement during lateral exchanges.
4. Break lock on: second press, target distance > `LockOnBreakRange`, or target death.
5. `WBP_HUD` shows a lock-on reticle at the target's chest socket via `Project World to Screen`.

`LockOnMaxRange` and `LockOnBreakRange` are `OPEN` (§14 Q11). No hard-lock camera snap on attacks in Phase 1 — attack facing uses a short rotate-to-target on montage start instead, which is cheaper and less nauseating.

*Deferred to Phase 2:* dynamic combat camera framing, target switching (there is only one target), 5.8's Gameplay Camera rig work.

### 4.5 Light attack sequence

Unreal concept: **one `AnimMontage` with named `Montage Sections`**, not N separate montages.

`AM_Player_LightCombo` with sections `Light_01`, `Light_02`, `Light_03` (**combo length is `OPEN` — §14 Q5**).

- `IA_LightAttack` → if `State.Attacking` not set → `Montage Play (AM_Player_LightCombo)` at section `Light_01`, add tag `State.Attacking`.
- Each section carries an **`ANS_ComboLink`** notify state covering the window in which the next input is accepted. Input inside that window sets `bComboBuffered = true`.
- At the notify state's `Received Notify End`, if `bComboBuffered`, call `Montage Set Next Section (CurrentSection, NextSection)`. Otherwise the montage runs to its section end and returns to neutral. This is the standard, robust Unreal combo pattern and it means combo timing is authored **on the timeline**, visible in the Animation editor, retunable by dragging a notify.
- Each section carries an **`ANS_ActiveHit`** notify state (section 5.2) covering only the frames where the strike connects.
- The **final** section carries a one-shot **`AN_ComboFinisher`** notify. That notify — and only that notify — fires `BP_AscensionComponent → AddMeter(ComboFinisher)`, worth **+5**. This makes "combo finisher" a precise, authored, single point in the timeline rather than an inferred condition.

### 4.6 Dodge and perfect dodge

Unreal concept: `AM_Player_Dodge` (root-motion montage, four directional sections `Dodge_F/B/L/R`) + **two nested Anim Notify States**.

```
|--------------------- AM_Player_Dodge : Dodge_B ---------------------|
      [========== ANS_IFrame (State.Invulnerable) ==========]
            [=== ANS_PerfectDodge (State.PerfectWindow) ===]
```

- `ANS_IFrame` → `Received Notify Begin`: add tag `State.Invulnerable`. `Received Notify End`: remove it. While the tag is present, `BP_HealthComponent → ApplyDamage` returns early with 0 damage.
- `ANS_PerfectDodge` is **nested inside** `ANS_IFrame` and is tighter. It adds `State.PerfectWindow`.
- **Perfect dodge is detected on the rival's side, not the player's.** When `ANS_ActiveHit` on a Crimson Vanguard attack montage traces and hits the player, `BP_VanguardCombatComponent` calls `BP_CombatComponent → ResolveIncomingHit`. That function branches:

| Player tags at moment of hit | Result |
|---|---|
| `State.PerfectWindow` | **Perfect dodge.** Damage 0. `AddMeter(PerfectDodge)` = **+12**. Request an Impact Window. |
| `State.Invulnerable` only | Ordinary dodge. Damage 0. **No meter.** |
| neither | Hit. Damage applied. `AddMeter(DamageTaken)` = **+0** (explicit, so it is visible in the data table that damage grants nothing). |

This is why the design puts perfect-dodge detection in the hit resolution rather than in a "was the enemy attacking?" proximity test: it uses the **exact same trace that already decides damage**, so a perfect dodge can never disagree with whether you were actually about to be hit. It is one code path, one source of truth, and it is fully authored on animation timelines the designer can drag.

**`ANS_IFrame` duration and `ANS_PerfectDodge` duration are `OPEN` (§14 Q6, Q7).** The GDD gives no dodge numbers at all.

### 4.7 Counter

Unreal concept: `ANS_CounterWindow` — an Anim Notify State placed on the **rival's** attack montages, plus a player montage.

The counter is a read on the rival's telegraph, so the window is authored where the telegraph is:

1. Each Crimson Vanguard attack montage carries an `ANS_CounterWindow` notify state, authored by the designer over the frames where a counter is a legitimate read (typically overlapping the late telegraph and the early active frames).
2. `Received Notify Begin` sets `BP_VanguardCombatComponent → bCounterable = true` and broadcasts `OnCounterWindowOpen`. `BP_CombatComponent` on the player listens and sets `State.CanCounter`.
3. `IA_Counter` pressed while `State.CanCounter` is set → **successful counter**: `Montage Stop` the rival's attack montage, play `AM_Vanguard_CounterReact` on the rival, play `AM_Player_Counter` on the player, force the rival Behavior Tree straight to the **Recover** state (see §6.5 — this is the one legal external interrupt), `AddMeter(Counter)` = **+15**, and request an Impact Window.
4. `IA_Counter` pressed while `State.CanCounter` is **not** set → a short whiffed counter montage with recovery. It must be punishable; a free counter spam button destroys the READ pillar. **Whiff recovery duration is `OPEN` (§14 Q8).**

**Design pillar anchor:** this is "Skill Creates Spectacle" — the counter is only rewarded when the telegraph was actually read.

### 4.8 Health

Unreal concept: one `BP_HealthComponent` ActorComponent, **used by both the player and Crimson Vanguard**, with no subclass.

- `MaxHealth` (float), `CurrentHealth` (float), `bIsDead` (bool), `MinHealthFloor` (float, default 0).
- `ApplyDamage(Amount, Instigator)` → early-return 0 if the owner has `State.Invulnerable` → subtract → `Clamp (MinHealthFloor, MaxHealth)` → broadcast `OnHealthChanged (NewHealth, Percent)` → if `CurrentHealth <= MinHealthFloor` and `MinHealthFloor == 0`, broadcast `OnDeath`.
- **`MinHealthFloor` is the mechanism for the Final Clash 1 HP floor.** `BP_FinalClashDirector` sets Crimson Vanguard's `MinHealthFloor = 1` for the duration of the Clash and restores it to 0 afterward. No special-case branch in the damage path.
- `OnHealthChanged` on the rival is what `BP_DuelDirector` listens to for the **50% Phase 2** trigger and the **≤25%** Clash gate condition.

**All health pool values and all damage values are `OPEN`.** The GDD gives none. See §14 Q1–Q4.

### 4.9 The Ascension Meter

Unreal concept: `BP_AscensionComponent` (on the player only) + `DT_MeterGains` Data Table.

- `Meter` float, clamped **0–100**. Broadcasts `OnMeterChanged (NewValue)` → `WBP_HUD` progress bar.
- **One entry point:** `AddMeter (E_MeterEvent Event)`. It does `Get Data Table Row (DT_MeterGains, Event)` → `Meter = Clamp(Meter + Row.Gain, 0, 100)`. **Nothing else in the project may write to `Meter` directly** except `BP_FinalClashDirector`'s failure path (§9.4), which sets it explicitly to 50.
- `DT_MeterGains` (Data Table, row struct `S_MeterGain`) — **numbers carried through from the GDD unchanged:**

| Row name (`E_MeterEvent`) | `Gain` | Design intent (GDD) |
|---|---|---|
| `ComboFinisher` | **+5** | Small reward for sustained offense |
| `PerfectDodge` | **+12** | Reward a clean defensive read |
| `Counter` | **+15** | Reward converting the opening |
| `ImpactWindowSuccess` | **+20** | Reward execution during an earned cinematic beat |
| `DamageTaken` | **+0** | Prevent passive progress |

- **No time-based gain exists anywhere in the design.** There is no tick that adds meter, no regeneration timer, and no "waiting" gain. The GDD's PRESERVED — METER DEFINITION is a hard rule: *"earned only through active combat decisions. It does not fill from waiting or elapsed time."* The `DamageTaken` row is present at `+0` specifically so that this rule is **visible as data** rather than being an absence someone might later "fix."
- **Meter decay is `OPEN` and my recommendation is none.** The GDD does not mention decay. §14 Q9.

### 4.10 The presentation kill-switch (GDD implementation safeguard)

Unreal concept: **Game Instance Subsystem** (`BP_PresentationSubsystem`).

The GDD requires: *"Separate gameplay timing from cinematic presentation so hit-stop, camera, and VFX can be disabled during diagnosis."* This is how that is enforced structurally rather than by discipline:

- `BP_PresentationSubsystem` exposes `bPresentationEnabled` (default true) and the only project-legal wrappers: `RequestHitStop(Duration)`, `RequestCameraShake(Class, Scale)`, `RequestVFX(NiagaraSystem, Transform)`, `RequestSound(Sound, Location)`, `RequestTimeDilation(Scale, Duration)`.
- Each wrapper early-returns if `bPresentationEnabled` is false.
- **Hard rule for the developer: `Set Global Time Dilation`, `Set Custom Time Dilation`, `Spawn System at Location`, `Play Camera Shake`, and `Play Sound at Location` are called in exactly one asset — `BP_PresentationSubsystem`.** Anywhere else, they are a defect. The inspector can check this by search.
- **Consequence, and this is the point:** because gameplay timing never reads the clock through a presentation call, disabling presentation cannot change a single frame window. Telegraph, active, recover, i-frames, and Impact Window durations are driven by montage playback and `Set Timer by Event`, none of which route through the subsystem.
- `WBP_DebugPanel`, bound to a debug key, toggles `bPresentationEnabled`, `bShowStateNames`, and `bDrawHitTraces`.

Since almost every call into this subsystem is M5 content, in Phase 1 the subsystem exists and is **mostly empty**. That is intentional and correct: the wiring is built in M1 so that the M5 pass has somewhere to land without touching gameplay code.

---

## 5. Attack authoring, telegraph readability, and hit detection

### 5.1 The three windows are Anim Notify States, and that is the whole readability mechanism

Unreal concept: **`AnimNotifyState`** Blueprint classes, authored directly on the montage timeline in the Animation Editor.

Every Crimson Vanguard attack montage is laid out the same way:

```
|============================ AM_Vanguard_AttackA ============================|
[=== ANS_Telegraph ===][== ANS_ActiveHit ==][======= ANS_Recover =======]
        0.55–0.95 s            0.18–0.45 s              0.45–0.90 s
        (Phase 1 range, GDD)   (same both phases)       (Phase 1 range, GDD)
              [=== ANS_CounterWindow ===]
```

| Notify State | `Received Notify Begin` | During | `Received Notify End` |
|---|---|---|---|
| `ANS_Telegraph` | set Blackboard `CurrentState = Telegraph`; `RequestVFX` warning lights; set emissive **red-orange** telegraph color; broadcast `OnTelegraphStart(AttackID)` | telegraph pose holds; **no hitbox active** | clear telegraph color |
| `ANS_ActiveHit` | enable the trace; clear the previously-hit-actor set | **`Received Notify Tick`:** `Capsule Trace By Channel` from last frame's socket position to this frame's, on trace channel `AttackTrace` | disable the trace |
| `ANS_Recover` | set `CurrentState = Recover`; set `IncomingDamageMultiplier` on the rival (the punish opening) | rival cannot cancel; cannot start a new attack | restore multiplier |
| `ANS_CounterWindow` | `bCounterable = true`; broadcast `OnCounterWindowOpen` | player may counter | `bCounterable = false` |

**Why this satisfies "readable by the player and retunable by the designer without touching logic":**

- The telegraph *is* a distinct, held, visually loud animation segment with its own duration, not a blend. The player reads a pose, a color, and (in Phase 2) a sound.
- The designer retunes the entire feel of an attack by **dragging notify-state boundaries in the Animation editor** and pressing Play. No Blueprint is opened. No node is edited. No recompile of gameplay logic.
- Because the windows are on the timeline, the durations are **visible** — you can literally see that attack C's recovery is longer than attack A's.
- The `ANS_Recover` window is the physical embodiment of the GDD's behavioral intent: *"every major offense exposes a clear recovery opening."* If a designer shortens it to nothing, the attack is visibly unpunishable in the editor, before playtest.

**Readability requirements per attack, from the GDD, and how each is met:**

| Attack | GDD readability requirement | How the notify layout satisfies it |
|---|---|---|
| **A** — close-range committed gauntlet force | Distinct wind-up and punishable recovery | Long `ANS_Telegraph` with a held gauntlet pose; `ANS_Recover` is the longest window on the montage |
| **B** — committed forward-pressure sequence | Visible first beat and stable tracking limit | The first `ANS_ActiveHit` is preceded by its own telegraph; **`ANS_TrackingLock` (a fifth notify state) turns off the rival's rotate-to-target at a fixed point** so the sequence cannot curve to follow the player. "Stable tracking limit" is a *mechanic*, not a note |
| **C** — armored reach and space control | Clear body direction and visible active range | Body direction is locked before the active window by `ANS_TrackingLock`; the active-range capsule is drawn in-editor via the debug toggle so the designer can see exactly how far it reaches |
| **D** — short propulsion-assisted approach | Thruster cue before movement; **no hidden full-arena snap** | The thruster cue lives in `ANS_Telegraph`; movement is root motion (or Motion Warping) **hard-capped at `AttackD_MaxTravel`** in the data row. The cap is data, so it can never silently exceed itself |

### 5.2 Hit detection

Unreal concept: `Capsule Trace By Channel` driven from `ANS_ActiveHit → Received Notify Tick`, on a custom trace channel.

- *Project Settings → Engine → Collision*: add trace channel **`AttackTrace`** (default response: Ignore). Both fighters' meshes respond `Block`.
- The notify state traces **from the previous frame's socket location to the current frame's**, not in place. This is the standard fix for fast attacks tunnelling through a target between frames. Sockets: `hand_l` / `hand_r` for gauntlet attacks, `foot_l` / `foot_r` where relevant.
- The notify state keeps a **`Set of Actor` of already-hit actors for this window** and clears it on `Received Notify Begin`, so a single active window cannot multi-hit. Attack B, which is a sequence, uses **multiple separate `ANS_ActiveHit` states** — one per beat — which is what makes each beat individually dodgeable.
- On a hit: `Break Hit Result` → `Get Hit Actor` → `ResolveIncomingHit` (§4.6) on that actor's `BP_CombatComponent`.
- Debug: when `bDrawHitTraces` is on, pass `Draw Debug Type = For Duration`. Off in the shipped build.

The **player** uses the exact same `ANS_ActiveHit` class on its own montages. One notify state class, both fighters. This is a second place where the framework refuses to fork.

### 5.3 Attacks A–D are **data**, not four graphs

Unreal concept: one **Blueprint Structure** + one **Data Table**.

`S_VanguardAttackDef` (Blueprint Structure, `/Game/AscendantImpact/Data/`):

| Field | Type | Purpose |
|---|---|---|
| `AttackID` | `E_VanguardAttackID` (A, B, C, D) | identity |
| `DebugName` | Name | shown by the debug string, e.g. `Attack_A_GauntletForce` |
| `Montage` | `AnimMontage` | the authored animation carrying all the notify states |
| `MinRange` / `MaxRange` | float | selection gate — **`OPEN`, §14 Q10** |
| `Damage` | float | **`OPEN`, §14 Q3** |
| `Cooldown` | float | per-attack re-use lockout — **`OPEN`, §14 Q12** |
| `bUsesPropulsion` | bool | attack D |
| `MaxTravelDistance` | float | the "no hidden full-arena snap" cap — **`OPEN`, §14 Q13** |
| `bLockTrackingAtActive` | bool | the "stable tracking limit" for B and C |
| `Phase1` | `S_AttackPhaseTuning` | **see below** |
| `Phase2` | `S_AttackPhaseTuning` | **see below** |

`S_AttackPhaseTuning` (the same struct type used twice):

| Field | Type | GDD Phase 1 | GDD Phase 2 |
|---|---|---|---|
| `RepositionDelay` | float | 0.60–1.20 s | 0.35–0.80 s |
| `SelectDelay` | float | 0.10–0.20 s | 0.10–0.20 s |
| `TelegraphScale` | float | drives montage play-rate over the telegraph section so 0.55–0.95 s can be retimed to 0.40–0.75 s | " |
| `RecoverScale` | float | 0.45–0.90 s → 0.35–0.75 s | " |
| `ReturnToNeutralDelay` | float | 0.10–0.20 s | 0.10–0.20 s |
| `SelectionWeight` | float | "balanced authored selection" | "more aggressive close-range and gap-closing weight" |

`DT_VanguardAttacks` (Data Table, row struct `S_VanguardAttackDef`) — **exactly four rows: `A`, `B`, `C`, `D`.**

**This is the "one data path" requirement, and it is worth spelling out why the struct is shaped this way.** Phase 2 is not a second table, not a second set of rows, and not a duplicated montage. It is the **second member of the same row**. Every attack carries its own Phase 1 tuning and its own Phase 2 tuning side by side, sharing one montage, one range, one damage value, one cooldown. The Behavior Tree does:

```
Get Data Table Row (DT_VanguardAttacks, SelectedAttackRow)
  → Select (Blackboard bPhase2) ? Row.Phase2 : Row.Phase1
  → feeds the state tasks
```

One `Select` node. That is the entire Phase 2 mechanism at the data layer. There is no way to add a Phase 2 attack without adding a Phase 1 attack, which is exactly the guarantee the GDD's *"Same four authored attacks — no transformation rig and no second move set"* asks for.

**Active Attack duration is deliberately NOT scaled by phase** — the GDD lists it as 0.18–0.45 s in *both* phases. The active window is the part the player must dodge, and keeping it identical across phases means Phase 2 changes *pressure and rhythm* without invalidating the read the player learned in Phase 1. That is the design intent of "Apply learned reads under stress."

---

## 6. The rival state model — Crimson Vanguard

### 6.1 Behavior Tree, not State Tree

**Decision: `BT_CrimsonVanguard` (Behavior Tree) + `BB_CrimsonVanguard` (Blackboard), run from `BP_VanguardController` (AIController).**

UE 5.8 makes State Tree the default framework in new project templates and has rewritten the AI documentation around it; Behavior Tree remains fully included and supported. Both would work. Behavior Tree is the ship choice here for three concrete reasons:

1. **The Gameplay Debugger gives us the GDD's "visible debug state names" for free.** Press the apostrophe key in PIE, select the AI category, and the currently executing BT task name and every Blackboard key are drawn on screen. That is an explicit GDD implementation safeguard satisfied at zero build cost.
2. **A strict six-state linear cycle is a `Sequence` under a `Loop` decorator** — the most boring, most debuggable structure in the tool. There is no hierarchical selection problem here to justify State Tree's extra concepts.
3. **Under a 38-day clock, the depth of existing Behavior Tree material and the team's likely familiarity is worth more than being on the newer default.** Where two approaches both ship, pick the one that ships.

*State Tree is noted as the modern alternative and is **deferred**; it is not a Phase 1 risk we need to take.*

### 6.2 The Blackboard

`BB_CrimsonVanguard` keys:

| Key | Type | Notes |
|---|---|---|
| `TargetActor` | Object (Actor) | set once on `BeginPlay` from `Get Player Pawn`. No `AI Perception`. |
| `CurrentState` | Enum `E_VanguardState` | **the debug-visible state name** |
| `SelectedAttack` | Enum `E_VanguardAttackID` | set by Select Attack |
| `bPhase2` | Bool | flipped only in Return to Neutral (§8) |
| `DistanceToTarget` | Float | refreshed by `BTService_UpdateCombatData` |
| `bCounteredThisAttack` | Bool | the one legal interrupt (§6.5) |
| `bInClash` | Bool | pauses the tree during the Final Clash |

`E_VanguardState` values, **in GDD order**: `Idle_Reposition`, `SelectAttack`, `Telegraph`, `ActiveAttack`, `Recover`, `ReturnToNeutral`.

### 6.3 The tree

```
BT_CrimsonVanguard
└── ROOT
    └── Selector
        ├── [Decorator: Blackboard — bInClash Is Set]
        │   └── BTTask_WaitIndefinite            ← the Clash owns the rival; tree idles
        │
        └── Sequence  "Attack Cycle"   [Decorator: Loop (Infinite)]
            │   Services on this Sequence:
            │     • BTService_UpdateCombatData     (DistanceToTarget, face target)
            │     • BTService_DrawDebugState       (Draw Debug String, CurrentState + timer)
            │
            ├── BTTask_Idle_Reposition
            ├── BTTask_SelectAttack
            ├── BTTask_Telegraph
            ├── BTTask_ActiveAttack
            ├── BTTask_Recover
            └── BTTask_ReturnToNeutral
```

Every task is a `BTTask_BlueprintBase` subclass implementing `Receive Execute AI` and calling `Finish Execute (Success)` at its exit condition. **The first line of every task's `Receive Execute AI` is `Set Blackboard Value as Enum (CurrentState, <its own state>)`.** That single convention is what makes the debug display truthful — there is no way for the drawn state name to disagree with the executing task.

Because the six tasks sit under a `Sequence` inside an infinite `Loop`, **the tree cannot deadlock in the way M2's gate cares about**: any task that finishes advances the sequence, and the sequence completing restarts it. The only way to strand the encounter is a task that never calls `Finish Execute`. Therefore:

> **Hard rule for every BTTask in this tree: it must have a guaranteed exit. Every task that waits on a montage sets a `Set Timer by Event` failsafe of (montage length + a small margin) that calls `Finish Execute (Success)` if `On Montage Ended` never fires. This is the M2 gate — "Returns to Neutral every attempt" — implemented, not hoped for.** The failsafe margin is `OPEN` (§14 Q18).

### 6.4 The six tasks

| # | Task | What it does | Exit condition (GDD) | Phase 1 / Phase 2 duration (GDD) |
|---|---|---|---|---|
| 1 | **`BTTask_Idle_Reposition`** | `CurrentState = Idle_Reposition`. Play the neutral/strafe locomotion. `Set Focus (TargetActor)` so the rival faces the player. If `DistanceToTarget` is outside every attack's range band, `Move To Actor` with an acceptance radius; otherwise hold. Wait `RepositionDelay` from the active phase tuning. | **Valid range and line** — the task finishes when the timer elapses *and* at least one attack row's `MinRange..MaxRange` contains `DistanceToTarget` | **0.60–1.20 s** / **0.35–0.80 s** |
| 2 | **`BTTask_SelectAttack`** | `CurrentState = SelectAttack`. Filter the four rows of `DT_VanguardAttacks` to those in range and off cooldown. Pick one by `SelectionWeight` from the **active phase's** tuning. Write `SelectedAttack`. Stamp that attack's cooldown. | **Attack selected** | **0.10–0.20 s** (both phases) |
| 3 | **`BTTask_Telegraph`** | `CurrentState = Telegraph`. `Play Anim Montage (Row.Montage)`, jump to the `Telegraph` section, apply `TelegraphScale` as play rate. `ANS_Telegraph` on the montage does the pose hold, the warning-light color, and the direction cue. | **Telegraph completes** — `ANS_Telegraph → Received Notify End` | **0.55–0.95 s** / **0.40–0.75 s** |
| 4 | **`BTTask_ActiveAttack`** | `CurrentState = ActiveAttack`. Montage continues into the `Active` section. `ANS_ActiveHit` runs the trace. `ANS_TrackingLock` freezes facing where the row asks for it. For attack D, root motion / Motion Warping travel, **capped at `MaxTravelDistance`**. | **Active frames end** | **0.18–0.45 s** — *identical in both phases, by design (§5.3)* |
| 5 | **`BTTask_Recover`** | `CurrentState = Recover`. Montage runs the `Recover` section at `RecoverScale`. `ANS_Recover` raises the incoming-damage multiplier — **this is the punish opening**. No new attack may start. | **Recovery completes** | **0.45–0.90 s** / **0.35–0.75 s** |
| 6 | **`BTTask_ReturnToNeutral`** | `CurrentState = ReturnToNeutral`. **Clear every attack flag**: `SelectedAttack = None`, `bCounteredThisAttack = false`, damage multiplier restored, tracking re-enabled, `Set Movement Mode (Walking)`, montage cleared. **Then evaluate the Phase 2 commit (§8).** | **Neutral restored** | **0.10–0.20 s** (both phases) |

**Behavioral intent, restated as build rules** (GDD §04): attacks are **committed** — once `BTTask_Telegraph` starts, the cycle runs through `Recover` and only a successful player counter can shorten it. Nothing is random except which of the in-range attacks is selected, and that selection is weighted authored data. Propulsion closes short gaps explosively but is capped. Every offense exposes `ANS_Recover`.

### 6.5 The one legal interrupt

A successful player counter (§4.7) is the **only** thing outside the tree that may change the rival's state mid-attack. It is implemented as:

`BP_VanguardCombatComponent → OnCountered` → `Montage Stop` the attack montage → set `bCounteredThisAttack = true` → the currently running task's `On Montage Ended` fires → the task calls `Finish Execute (Success)` → the `Sequence` advances. If the counter landed during Telegraph or Active, `BTTask_Recover` reads `bCounteredThisAttack` and plays the counter-reaction montage instead of the normal recovery.

**Deliberately not used: `Abort Self` decorators, `Simple Parallel` aborts, or `Stop Logic`.** Every one of those is a route to a stranded state. The counter routes *through* the sequence, not around it, and the sequence's guaranteed forward motion is what keeps the M2 gate honest.

### 6.6 Visible debug state names

`BTService_DrawDebugState`, ticking on the Attack Cycle sequence, calls `Draw Debug String` above the rival's head with:

```
CV | Phase 1 | Telegraph | Attack_A_GauntletForce | 0.41s
```

Gated on `BP_PresentationSubsystem → bShowStateNames`. Plus the built-in **Gameplay Debugger** (apostrophe key) for the Blackboard dump. Two independent views of the same truth.

---

## 7. Impact Windows and the meter handoff

### 7.1 What opens a window

Unreal concept: `BP_ImpactWindowDirector` (an actor owned by `BP_DuelDirector`) + `Set Timer by Event` + `WBP_ImpactPrompt`.

A qualifying real-time event calls `RequestImpactWindow(E_ImpactTrigger)`. There are exactly three triggers, all from the GDD:

| Trigger | Fired from |
|---|---|
| Perfect dodge | `ResolveIncomingHit` → `State.PerfectWindow` branch (§4.6) |
| Successful counter | `IA_Counter` inside `ANS_CounterWindow` (§4.7) |
| Approved combo milestone | `AN_ComboFinisher` on the last combo section (§4.5) |

`RequestImpactWindow` refuses and returns immediately if: a window is already open, the standard-window cooldown has not elapsed, `bInClash` is true, or either fighter is dead.

### 7.2 The two window widths — carried through from the GDD unchanged

| Window | Trigger | **Provisional response time** | Failure result |
|---|---|---|---|
| **First Impact Window** | The **first** successful perfect dodge or counter of the duel | **0.75 s** | No cinematic extension; return to combat with **no extra punishment** |
| **Standard Impact Window** | Approved skill event after cooldown | **0.35–0.50 s** | No extension; return to combat |

Implementation: `BP_ImpactWindowDirector` holds `bFirstWindowConsumed` (false at duel start). `RequestImpactWindow` picks `FirstWindowDuration` if that bool is false **and** the trigger was a perfect dodge or a counter (per the GDD — the combo milestone does not qualify for the wider onboarding window), then sets it true. Otherwise it picks `StandardWindowDuration`.

### 7.3 The onboarding rule is a hard behavioral requirement, not a note

GDD PRESERVED — ONBOARDING RULE: *"The first Impact Window is intentionally wider, but it still requires the player's input and must be earned through a successful real-time defensive action. The game does not press the input for the player and does not convert a miss into success."*

Implemented as these three prohibitions, which the inspector should check:

1. **There is no auto-success path.** The only route to success is an `IA_Impact` `Triggered` event received while `bWindowOpen` is true. No timer, no branch, and no "assist" may set success.
2. **There is no input-buffer leniency on the window.** An `IA_Impact` press received *before* `OpenWindow` is discarded, not queued. Otherwise mashing converts a miss into a success, which the rule forbids.
3. **The wider first window changes exactly one float and nothing else.** It does not slow time, does not extend the enemy's recovery, and does not soften the failure result.

### 7.4 Scoring

```
OpenWindow(Duration):
    bWindowOpen = true
    Show WBP_ImpactPrompt
    Set Timer by Event (Duration) → OnWindowExpired

IA_Impact (Triggered) → if bWindowOpen:
    Clear and Invalidate Timer by Handle
    bWindowOpen = false
    Hide WBP_ImpactPrompt
    → SUCCESS

OnWindowExpired:
    bWindowOpen = false
    Hide WBP_ImpactPrompt
    → FAILURE
```

| Branch | What happens |
|---|---|
| **SUCCESS** | `BP_AscensionComponent → AddMeter(ImpactWindowSuccess)` = **+20**. Play the **1–3 second choreographed burst**: a montage pair on both fighters, plus a `RequestHitStop` / `RequestCameraShake` through the presentation subsystem (which is empty in Phase 1 and filled in M5). Then `RestoreCombatState()`. |
| **FAILURE** | **No cinematic extension. No meter. No extra punishment** for the first window; for standard windows, no punishment either — the GDD says only "return to combat." Then `RestoreCombatState()` immediately. Start the standard-window cooldown. |

### 7.5 `RestoreCombatState()` — the single restore function

The GDD safeguard: *"Restore input, collision, locomotion, lock-on, and AI state explicitly after every Impact Window and Final Clash branch."*

**One function, called by every branch of both systems — Impact success, Impact failure, Clash success, Clash failure.** Not four copies.

```
RestoreCombatState():
    Enable Input (PlayerController)
    Set Collision Enabled (both capsules → Query and Physics)
    Set Movement Mode (Walking) on both
    Clear all transient gameplay tags on the player combat component
        (State.Attacking, State.Invulnerable, State.PerfectWindow,
         State.InImpactWindow, State.Clashing)
    Restore lock-on if it was active before the overlay
    Set Global Time Dilation → 1.0     (via BP_PresentationSubsystem only)
    Rival: bInClash = false; CurrentState = Idle_Reposition; Behavior Tree resumes
    Hide WBP_ImpactPrompt
```

Because it is one function, a bug in restoration is one bug in one place. This is also the direct implementation of the GDD's control-model promise that overlays *"always return control to the player."*

### 7.6 Where the five meter events hook in

| Event | Hook point | Gain |
|---|---|---|
| Light-combo finisher | `AN_ComboFinisher` notify on the final combo montage section | **+5** |
| Perfect dodge | `ResolveIncomingHit`, `State.PerfectWindow` branch | **+12** |
| Successful counter | `IA_Counter` accepted inside `ANS_CounterWindow` | **+15** |
| Impact Window success | `BP_ImpactWindowDirector` SUCCESS branch | **+20** |
| Taking damage / waiting | `ResolveIncomingHit`, damage branch — calls `AddMeter(DamageTaken)` explicitly | **+0** |

All five go through `AddMeter(E_MeterEvent)` → `DT_MeterGains`. Five call sites, one table, one clamp.

---

## 8. Phase 2 — same four attacks, re-timed through one data path

### 8.1 The trigger and the commit

- `BP_DuelDirector` listens to Crimson Vanguard's `BP_HealthComponent → OnHealthChanged`.
- When `Percent <= 0.50` and `bPhase2Pending` is false → set `bPhase2Pending = true`. **Nothing else happens yet.**
- **The commit happens in `BTTask_ReturnToNeutral` and nowhere else.** Its last act, after clearing all attack flags, is: `if bPhase2Pending and not bPhase2 → Set Blackboard Value as Bool (bPhase2, true) → broadcast OnPhase2Committed → bPhase2Pending = false`.

This is exactly the GDD's REVISED — PHASE 2 rule: *"The phase change is committed on Return to Neutral."* Committing anywhere else — mid-telegraph, mid-active — would retime an attack the player is currently reading, which breaks the READ pillar and would be a bug.

### 8.2 The signal — once

`OnPhase2Committed` fires a **one-shot** presentation beat through `BP_PresentationSubsystem`: stronger thruster output, warning lights, sound, armor-energy presentation (GDD). It is guarded by the `bPhase2` bool, so it is structurally impossible to fire twice.

**Phase 1 build:** the signal is an emissive-intensity change on the rival's material plus a brief pause. **The authored VFX, the sound, and the thruster plume are M5 / Phase 2 polish** and land in the already-wired subsystem call.

### 8.3 What actually changes — and what does not

| Parameter | Phase 1 | Phase 2 | Where it lives |
|---|---|---|---|
| Reposition delay | **0.60–1.20 s** | **0.35–0.80 s** | `S_AttackPhaseTuning.RepositionDelay` |
| Telegraph | **0.55–0.95 s** | **0.40–0.75 s** | `TelegraphScale` |
| Recover | **0.45–0.90 s** | **0.35–0.75 s** | `RecoverScale` |
| Select Attack | **0.10–0.20 s** | **0.10–0.20 s** | `SelectDelay` |
| Active Attack | **0.18–0.45 s** | **0.18–0.45 s** — *unchanged* | not phase-scaled, by design |
| Return to Neutral | **0.10–0.20 s** | **0.10–0.20 s** | `ReturnToNeutralDelay` |
| Forward pressure | Measured advances | More frequent advances, shorter hesitation | emergent from the shorter `RepositionDelay` |
| Attack weighting | Balanced authored selection | More aggressive close-range and gap-closing weight | `SelectionWeight` on each row |
| Attack set | Four authored attacks | **The same four authored attacks** | one `DT_VanguardAttacks`, four rows |

**The one data path, stated for the inspector:** there is one Data Table, four rows, one montage per attack. `BTTask_SelectAttack` and every timed task read the tuning through a single `Select` node keyed on the `bPhase2` Blackboard bool. **There is no second table, no second montage set, no second Behavior Tree branch, no transformation rig, and no `Phase2` variant of any Blueprint.** Adding a Phase-2-only attack would require adding a Phase-1 row, which is precisely the guarantee the GDD asks for.

---

## 9. The Final Clash

### 9.1 The double gate

Unreal concept: `BP_FinalClashDirector`, evaluated on two events only.

```
EvaluateClashGate():                  ← called from OnMeterChanged and from CV's OnHealthChanged
    bClashEligible =
          (Meter >= 100)
      AND (CV Health Percent <= 0.25)
      AND (Clash cooldown not active)
      AND (not bInClash)
```

- **Both conditions must be true.** If only one is met, the Clash stays **locked**. `WBP_HUD` shows the gate honestly — two separate indicators, so the player can see *which* condition is still missing. That is a readability decision inside the GDD's brief, not a new feature.
- **The player chooses to initiate.** `IA_FinalClash` is only accepted when `bClashEligible` is true **and** the player is in **neutral** or **inside the post-counter success window**. The Clash never auto-triggers. This preserves the GDD control model: overlays are *"triggered by gameplay performance"* and the player *"chooses to initiate."*
- The post-counter acceptance window duration is `OPEN` (§14 Q19).

### 9.2 The two timing beats

Unreal concept: **the same `WBP_ImpactPrompt` + timer machinery from §7, run twice**, plus one `Level Sequence` camera cut. This is the R3 mitigation and it is why the Clash is affordable at all.

```
InitiateClash():
    bInClash = true                      → rival BT parks on BTTask_WaitIndefinite
    Disable Input on normal combat actions; leave IA_Impact live
    Play AM_Clash_Beat1 on both fighters
    Play LS_FinalClash (Level Sequence camera cut)
    OpenClashBeat(1)  → prompt, timer, IA_Impact
        ├─ hit  → OpenClashBeat(2) → prompt, timer, IA_Impact
        │            ├─ hit  → CLASH SUCCESS  (§9.3)
        │            └─ miss → CLASH FAILURE  (§9.4)
        └─ miss → CLASH FAILURE  (§9.4)
```

**Beat 1 and beat 2 response durations are `OPEN` (§14 Q20).** The GDD specifies the Impact Window widths but gives no numbers for the Clash beats. My question for the designer is whether they should simply reuse `StandardWindowDuration` (0.35–0.50 s) for consistency of learned feel, or be authored separately.

### 9.3 Success

> Complete **both** timing beats → the finishing sequence defeats Crimson Vanguard and ends the duel → **Win screen**.

`ClashSuccess()`: play `AM_Clash_Finisher` on both → on montage end, `BP_HealthComponent` on the rival gets `MinHealthFloor = 0` then `ApplyDamage(MaxHealth)` → `OnDeath` → `BP_DuelDirector → EndDuel(Win)` → `WBP_Result` in Win state. `RestoreCombatState()` still runs before the result screen so nothing is left in a cinematic state.

### 9.4 Failure — the exact sequence

> **A failed Final Clash never restarts the duel and never kills the player.** It is a meter setback and a recoverable path back to victory. Stated plainly here because it is the single most misreadable rule in the design.

`ClashFailure()`, in order — **all numbers from the GDD, unchanged:**

1. `Montage Stop` on both fighters; stop `LS_FinalClash`; return the camera to gameplay.
2. **Separate both fighters.** `Set Actor Location` on each, pushed apart along the axis between them, then `Set Actor Rotation` to face each other. **Separation distance is `OPEN` (§14 Q21)** — the GDD says "separate," not how far. It must place both outside every attack's `MinRange` so neither is instantly re-engaged.
3. **Preserve current health.** No health change to either fighter — except:
4. **Crimson Vanguard is held at a 1 HP floor.** `CV HealthComponent → MinHealthFloor = 1`. Since the gate required `Health <= 25%`, the rival is alive; the floor guarantees the failed Clash cannot have killed it and cannot end the duel by accident. *(Design note for the designer: the floor is what keeps the Clash the **only** way to win. §14 Q22 asks whether the floor is permanent from first eligibility or applied only during a Clash attempt.)*
5. **Reduce meter to 50.** `BP_AscensionComponent → Meter = 50` — a direct set, the one sanctioned exception to the `AddMeter`-only rule, marked with a comment saying so.
6. **Apply a 3-second re-trigger cooldown.** `Set Timer by Event (3.0) → OnClashCooldownEnd`. `bClashEligible` is forced false for the duration; `EvaluateClashGate()` re-runs when it ends.
7. **Return to Neutral.** `RestoreCombatState()` (§7.5). `bInClash = false`. The rival's Behavior Tree leaves `BTTask_WaitIndefinite` and re-enters the Attack Cycle at `Idle_Reposition`.
8. **What must NOT happen, ever:** the duel does not restart; the player is not killed or damaged; neither fighter is left in a cinematic state, with input disabled, with collision off, or with a montage playing.

The player is then at meter 50 against a rival at ≤25% health, rebuilding toward 100. Perfect dodge (+12), counter (+15), and Impact success (+20) are the fast routes back. That is a real setback with a real, skill-shaped recovery — which is exactly what the GDD's FAILED CLASH RECOVERY rule describes.

### 9.5 Loss

The **only** loss condition is the selected fighter's health reaching zero (GDD encounter flow). Player `OnDeath` → `BP_DuelDirector → EndDuel(Loss)` → `WBP_Result` in Loss state.

**There is no duel timer.** The 3–5 minute figure is a *target session length* to tune toward, not a rule. `OPEN` — §14 Q23 asks the designer to confirm.

---

## 10. Encounter flow and the arena

### 10.1 Opening flow — Phase 1 realization

GDD flow: editorial selection interface → player moves between both options → selection → technical/equipment panels animate → transition into the arena → camera behind the selected fighter → Crimson Vanguard enters through the far doorway → duel begins.

GDD course-build allowance: *"a simplified selection screen and abbreviated arena entrance are acceptable while preserving the same readable sequence."* Phase 1 takes that allowance:

| Beat | Phase 1 | Phase 2 |
|---|---|---|
| Selection | `WBP_CharacterSelect` in `L_CharacterSelect`: two portrait buttons, name, one-line identity, both `DA_FighterProfile` previews standing in a lit box. Stores the choice in the Game Instance. | Editorial layout, technical/equipment panel animation, camera moves |
| Arena transition | `Open Level (L_ShatteredRing)` with a fade | Authored transition |
| Camera behind fighter | Default spawn orientation, reverse third-person framing | Choreographed |
| CV enters through the far doorway | `LS_VanguardEntrance`: short `Level Sequence`, rival walks from the far-doorway spawn to its combat mark, fixed camera, **skippable** | Full entrance with VFX, sound, arena reaction |
| Duel begins | `RestoreCombatState()`, enable input, start the Behavior Tree | " |

The entrance sequence must be **skippable and short** — the GDD's own player-experience column says *"Establish identity and stakes without delaying play."*

### 10.2 Shattered Ring — Phase 1 arena spec

`/Game/AscendantImpact/Arena/L_ShatteredRing`. The GDD locks the established industrial Shattered Ring as the official Version 1 environment. **Pages 10–14 of the GDD are image reference sheets with no extractable text, so this brief does not describe the arena's appearance.** It specifies only the four functional requirements the GDD states in text, which is all a gray-box needs.

| GDD arena requirement | Phase 1 build |
|---|---|
| **Central combat floor** — open, readable space for spacing, lock-on, dodges, counters, Final Clash staging | A flat playable disc/rectangle, dressed with free industrial floor materials. Must be large enough that attack D's capped travel and the Clash separation both fit. **Footprint dimensions `OPEN` — §14 Q24.** |
| **Far doorway** — dedicated Crimson Vanguard entrance axis | A single large doorway opening at one end, with a `TargetPoint` named `PS_VanguardEntrance` and a second at `PS_VanguardCombatMark` |
| **Reverse third-person framing** — clear camera position behind the selected fighter | Player spawn faces the far doorway; the arena has enough headroom and backspace that the spring arm never clips through geometry at the boundary |
| **Side-on readability** — readable silhouettes and attack direction during lateral exchanges | Nothing tall or busy inside the central floor. Lighting reads silhouettes against the walls. This is a **layout** rule, enforced in the gray box, not a lighting pass |
| **Environmental reaction** — visible but controlled, **without adding gameplay hazards** | **DEFERRED to M5 / Phase 2 (R6).** The Phase 1 requirement that survives is the negative one: **the arena contains no hazards, no damage volumes, and no physics objects that can affect the duel.** |

Boundary: a `Blocking Volume` ring plus a `Kill Z` far below. The GDD's *"arena-boundary tests"* apply to **both** avatars identically.

---

## 11. Milestone contents — what "done" means

Each milestone lists **contents** (what must exist) and the **gate** (what must be demonstrated). The gates are the GDD's own. Nothing in M1–M4 may depend on M5.

### 11.1 M1 — Combat gray box
**GDD gate: playable loop with selected proxy.**

Contents:
1. `L_ShatteredRing` gray box: central floor, far doorway opening, blocking volumes, spawn points, basic lighting. Functional layout only.
2. `BP_PlayerFighter` with `SpringArmComponent` + `CameraComponent`, Enhanced Input (`IMC_Duel`, all eight `IA_*`).
3. `DA_FighterProfile_Echo` and `DA_FighterProfile_Nova`; `ApplyFighterProfile` working; `WBP_CharacterSelect` with two buttons.
4. `BP_LockOnComponent` — acquire, hold, break, strafe-facing, reticle.
5. `AM_Player_LightCombo` with sections and `ANS_ComboLink` + `ANS_ActiveHit`; combo chains and drops correctly.
6. `AM_Player_Dodge` with four directional sections, `ANS_IFrame`, nested `ANS_PerfectDodge`.
7. `IA_Counter` + whiffed-counter recovery (the rival side comes in M2).
8. `BP_HealthComponent` on both actors; `AttackTrace` collision channel; `ResolveIncomingHit` with its three-way branch.
9. `BP_PresentationSubsystem` **wired and empty**; `WBP_DebugPanel` toggling presentation, state names, and hit traces.
10. Dressed proxies in place (section 12) — asset selection, not presentation work.

**Done when:** either fighter can be selected, enters the arena, moves, locks on, chains the light combo, dodges directionally with visible i-frames, whiffs a counter, takes damage, and dies — **and both avatars pass the same collision, targeting, reach, and arena-boundary tests** (GDD safeguard). Presentation can be toggled off with no change to any timing.

### 11.2 M2 — Rival state loop
**GDD gate: all six AI states and one Crimson Vanguard attack complete without deadlock; returns to Neutral every attempt.**

Contents:
1. `BP_CrimsonVanguard`, `BP_VanguardController`, `BB_CrimsonVanguard`, `BT_CrimsonVanguard`.
2. All six `BTTask_*` Blueprints, each setting `CurrentState` first and each with a guaranteed `Finish Execute` plus its montage failsafe timer.
3. `BTService_UpdateCombatData` and `BTService_DrawDebugState`.
4. `S_VanguardAttackDef`, `S_AttackPhaseTuning`, `DT_VanguardAttacks` with **all four rows created** — even though only one attack's montage is authored at this milestone.
5. **Attack A** fully authored: montage with `ANS_Telegraph`, `ANS_ActiveHit`, `ANS_Recover`, `ANS_CounterWindow`.
6. Rival attacks connect and damage the player; the player can dodge, perfect-dodge (meter not yet wired), and counter it.
7. Counter interrupt routed through the sequence (§6.5).
8. `Draw Debug String` showing phase, state, attack name, remaining time.

**Done when:** the rival cycles Idle/Reposition → Select Attack → Telegraph → Active Attack → Recover → Return to Neutral **continuously for several minutes with no deadlock**, with visible state names, and reaches Return to Neutral on **every** attempt — including when countered mid-attack, when the player runs out of range mid-telegraph, and when the player stands still.

### 11.3 M3 — Impact handoff
**GDD gate: earned prompt, success/failure branches, restored control; no forced success and no stranded cinematic state.**

Contents:
1. `BP_ImpactWindowDirector` with `RequestImpactWindow`, `OpenWindow`, success and failure branches.
2. `WBP_ImpactPrompt`.
3. The **first window at 0.75 s** and the **standard window at 0.35–0.50 s**, with `bFirstWindowConsumed`.
4. Standard-window cooldown.
5. The **1–3 second choreographed burst** on success, as a montage pair (no authored camera or VFX yet — that is M5).
6. `BP_AscensionComponent`, `DT_MeterGains` with all five rows, `AddMeter` as the single entry point, `WBP_HUD` meter bar.
7. All five meter hooks wired: +5 combo finisher, +12 perfect dodge, +15 counter, +20 Impact success, +0 damage.
8. **`RestoreCombatState()`** written once and called by both branches.

**Done when:** a perfect dodge or a counter opens a prompt; hitting it grants +20 and plays the burst; missing it returns to combat with no punishment and no meter; **doing nothing never produces success**; an `IA_Impact` press *before* the window opens is discarded; and after either branch the player has input, collision, locomotion, and lock-on, and the rival's Behavior Tree is running.

### 11.4 M4 — Complete duel
**GDD gate: meter, Phase 2, Final Clash, failure recovery, win/loss — a start-to-finish course prototype.**

Contents:
1. **Attacks B, C, and D authored** — montages, all notify states, `DT_VanguardAttacks` rows filled including `Phase1` and `Phase2` tuning.
2. `ANS_TrackingLock` for B and C; capped travel for D.
3. Range- and cooldown-based selection across all four attacks with `SelectionWeight`.
4. Phase 2: `bPhase2Pending` at 50%, commit in `BTTask_ReturnToNeutral`, **one-shot** signal, all Phase 2 tuning live.
5. `BP_FinalClashDirector`: double gate, HUD gate indicators, `IA_FinalClash` acceptance rules, both beats, `LS_FinalClash`.
6. Clash **success** → finisher → Win.
7. Clash **failure** → the exact seven-step sequence in §9.4, verified.
8. `WBP_Result` Win and Loss states with a restart option.
9. `LS_VanguardEntrance`, skippable.

**Done when:** a player can select Echo *or* Nova, watch the abbreviated entrance, fight through Phase 1, see Phase 2 commit at 50% on Return to Neutral and signal exactly once, reach the double gate, **fail a Final Clash and recover from it** (meter 50, rival at 1 HP floor, 3 s cooldown, full control restored, duel continuing), then succeed and reach the Win screen — and separately, die and reach the Loss screen. **Both avatars complete the full duel.**

> **This is the 1 September deliverable.** Target functional completion ~20 August (R7) so the human designer has real time to tune section 13.

### 11.5 M5 — Presentation pass
**GDD gate: only after M4 is stable.** This is Phase 2 work, after 1 September.

Contents: approved character treatment for Echo, Nova, and Crimson Vanguard · arena environmental reaction · camera choreography and hit-stop tuning · authored Niagara VFX (telegraph energy, thrusters, warning lights, Ascension language, Echo orange / Nova cyan-white combat energy) · full sound design · full-fidelity Final Clash choreography · the editorial selection interface.

**M5 must not be interleaved into M1–M4.** The structural guarantee is section 4.10: all presentation lands behind `BP_PresentationSubsystem`, which exists from M1 and stays empty until M5. Filling it changes no gameplay timing.

### 11.6 Reconciling the brief's "thin presentation floor" with M5 ordering

`project-brief.md` asks Phase 1 to have *"some design on it"* so it does not read as a bare gray-box tech demo, while keeping M5 behind a stable M4. This brief satisfies that with a bright line:

| Allowed in Phase 1 — **asset selection** | Reserved for M5 — **authored/tuned work** |
|---|---|
| Choosing and importing free character meshes | Bespoke or modified character art |
| Retargeting free animations onto the proxies | Authoring or hand-keying animation |
| Applying free industrial materials to arena geometry | Lighting art pass, post-process grading |
| Setting a flat emissive accent color per fighter from `DA_FighterProfile` | Authored Niagara VFX systems |
| Placing free industrial props for the far doorway and walls | Arena environmental reaction on impact |
| A functional, legible HUD and result screens | Motion-designed UI |

**The test:** *does it cost schedule time and require iteration to feel right?* If yes, it is M5. If it is picking a file and dropping it in, it is Phase 1.

---

## 12. Free-asset sourcing — $0 budget

**Verified by WebSearch on 2026-07-25. Sources listed at the end of this document.** Availability and licensing must be re-confirmed at claim time by the human — the GDD's HUMAN APPROVAL GATE requires **rights review** on every asset before it enters the build. Nothing in this list is approved by writing it here.

### 12.1 The verified free sources

| Source | What it gives | License note | Confidence |
|---|---|---|---|
| **Engine-shipped content** — UE 5.8 Third Person template, Starter Content, UE5 Mannequins (Manny / Quinn) | Locomotion AnimBP, `SpringArm`+`Camera` rig, basic materials, two correctly-scaled humanoid characters on the **UE5 skeleton** | Ships with the engine | **High** |
| **Epic free content on Fab** (`Price > Free` filter; documented at *Free Epic Games Content for Unreal Engine*, UE 5.8 docs) | Paragon (39 characters + 1,500+ environment components), Infinity Blade collection, Soul: City, Soul: Cave | Free, licensed for use with Unreal Engine, commercial use permitted; Paragon **trademark** may not be used | **High** |
| **Paragon character packs on Fab** — e.g. *Paragon: Kallari*, *Paragon: Sevarog*, and the final free batch that included *Steel* | AAA characters with skeletons, animation cycles, skins, VFX, sound cues | As above | **High** for the program; **verify each specific hero listing on Fab before planning around it** |
| **Mixamo** (mixamo.com, free Adobe ID) | 2,000+ mocap animations, FBX, auto-rigger | Free; usable in commercial projects; **may not be redistributed as standalone assets** | **High** |
| **Game Animation Sample Project** (Epic, free; UE 5.8 docs page exists; updated in 5.7) | 500+ AAA animations, compatible with all UE Mannequins, motion-matching locomotion | Free; **licensed for use with Unreal Engine only** | **High** — but see R2 |
| **Quixel Megascans on Fab** | Photoreal metal, concrete, and industrial surfaces; props | On Fab; filter `Price > Free`. **What you acquire on Fab you keep forever** | **Medium** — the blanket "free to everyone" period ended; free/paid is now per-listing. Verify at claim time |
| **Fab "Limited-Time Free" rotation** | Rotating full packs (e.g. *Modular SciFi Station*, 147 meshes, free until 16 June 2026; *Sci-Fi Desert City Kit*, free until 14 July 2026) | Claim during the window, keep forever | **Medium** — **do not plan around any specific rotating freebie.** Both examples above have already expired. **Recommendation: someone claims the weekly Fab freebies every week from now to 1 September** — it costs a minute and may hand us the arena |

### 12.2 Agent Echo — 6'0" lean, upright technical striker, matte black/charcoal, restrained orange accents

| Option | Pros | Cons |
|---|---|---|
| **RECOMMENDED — UE5 Mannequin (Manny), scaled to 183 cm, with a recolored `Material Instance`** | Zero retargeting (native UE5 skeleton, all template animation and the Game Animation Sample work immediately). Matte dark base with an orange emissive accent parameter is a two-minute material edit and is *literally* the GDD's description. Silhouette is lean and upright | Reads as a mannequin, not a character |
| Paragon hero with a lean technical silhouette | Real character art | UE4-era skeleton → `IK Retargeter` pass; silhouettes are stylized fantasy/sci-fi hero, not "technical suit"; each hero is a large download |
| MetaHuman (free, integrated in 5.6+) | High-quality human | Heavy at runtime; clothing options do not include a technical combat suit; a schedule risk for a duel prototype |

**Decision: Mannequin-based Echo for M1–M4.** Revisit a Paragon swap only if the schedule holds at the M4 review. **Gap acknowledged: no free asset matches Echo as designed. This is a proxy, and the real Echo is Phase 2 / M5 character treatment.**

### 12.3 Agent Nova — 5'8" compact agile layered profile; black/charcoal/orange/light-gray costume **preserved**; cyan-white for **combat energy only**

**Decision: UE5 Mannequin (Quinn), scaled to 173 cm, with its own `Material Instance`.** Same reasoning as Echo, and it gives an immediate, honest silhouette contrast (compact vs. upright) at zero cost.

**Critical constraint the developer must not get wrong:** the GDD's REVISED — COLOR DIRECTION says Nova's black/charcoal/orange/light-gray costume is **preserved** and **cyan-white is reserved for combat energy, telegraphs, or selected VFX accents — it is NOT a costume recolor.** In `DA_FighterProfile_Nova`, the costume material parameters stay in the preserved palette; the cyan-white is a **separate** emissive/VFX parameter. Turning Nova cyan is a defect against the GDD.

### 12.4 Crimson Vanguard — 6'10", substantially broader armored mass, red armor over black structure, gauntlets, thrusters, red-orange warning lights

**This is the biggest gap. Flagged as R4.** No verified free asset matches this specification.

Fallback ladder, cheapest and safest first:

1. **Ships-no-matter-what (M2 baseline): UE5 Mannequin scaled to 208 cm with a widened proxy silhouette** — non-animated static-mesh shoulder/gauntlet blocks attached to bone sockets, plus a red/black `Material Instance` with red-orange emissive warning-light parameters. Ugly, honest, on the native skeleton, and it gives correct scale, correct reach, and correct readability **today**. Attached blocks are proxies, not character art, and can be deleted the moment a real mesh lands.
2. **Upgrade if the schedule holds: a free Paragon heavy hero** (the heavy/tank archetypes are in the free program — *Sevarog* and *Steel* are both confirmed free releases) retargeted with the **`IK Retargeter`** and tinted red via `Material Instance`. Budget a full day for retargeting plus proportion-driven hit-reach re-validation. Paragon heavies also ship attack animation cycles that could serve as A–D source material, which is a real saving.
3. **Fab Limited-Time Free rotation** — a free armored sci-fi character may appear before 1 September. Claim weekly; do not plan around it.

**Whichever is used, the GDD's hard requirement governs: *"The height difference must not create unfair hidden reach or collision behavior."* Capsule radius and half-height, the attack trace sockets, and every `MinRange`/`MaxRange` value must be re-validated after any mesh swap.** Building the whole game against option 1 and swapping late is exactly the risk this warns about — so **if the Paragon swap is going to happen, it must happen before the M4 range tuning**, not after.

### 12.5 Shattered Ring arena

No verified free asset is "the Shattered Ring." **Gap acknowledged.** Build it, do not buy it:

1. **Geometry first.** Author the floor, walls, and far doorway with in-editor geometry brushes or simple static meshes. The four functional requirements in §10.2 are met by **layout**, and layout is free.
2. **Surfaces.** Free Quixel Megascans on Fab (industrial concrete, scuffed metal, painted steel) plus Starter Content materials.
3. **Props.** *Soul: City* (free Epic content, industrial/urban props) and free Fab industrial kits, used sparingly and **only outside the central combat floor** — the side-on-readability requirement forbids clutter in the fight space.
4. **The far doorway** is a large framed opening with a bright backlight behind it, so the rival's entrance silhouette reads. This costs one rect light.
5. **Watch out:** many Megascans/Quixel surfaces are Nanite/high-density. On a duel prototype, prefer the lighter listings and keep the poly budget for the fighters.

### 12.6 Where no free option exists — named gaps

| Gap | Fallback | Milestone |
|---|---|---|
| Character art matching the GDD reference sheets for Echo, Nova, and Crimson Vanguard | Mannequin proxies with material differentiation (§12.2–12.4) | Real art is **M5 / Phase 2** |
| A cohesive martial-arts strike animation set with the exact weight the design wants | Mixamo combat animations retargeted with `IK Retargeter`; Paragon hero attack cycles if a hero is used. **Expect the anim set to be the schedule's tightest resource** | M1/M2 |
| Sound design — impacts, thrusters, warning lights, telegraph audio cues | **No free source verified in this pass.** Sound is M5 / Phase 2. If a Phase 1 audio floor is wanted, Starter Content has a handful of cues; otherwise ship silent and say so | M5 |
| Authored VFX — thrusters, telegraph energy, Ascension language | Phase 1 uses **emissive material parameters only**. Niagara authoring is M5 | M5 |
| Music | Not sourced. **Deferred; flagged for the designer** | M5 |

**No purchase is assumed anywhere in this plan. If the designer decides a paid asset is worth it, that is the designer's call and outside this brief.**

---

## 13. Provisional values table — every number in one place

**Every value in this table is PROVISIONAL and PENDING PLAYTEST.** The human designer owns all of them. The developer implements them as exposed variables on Data Tables, Data Assets, and Anim Notify States, and changes none of them.

### 13.1 Values carried through from the GDD — unchanged

| # | Value | GDD number | Lives in |
|---|---|---|---|
| 1 | Target session length | **3–5 minutes** | design target, not a timer (§14 Q23) |
| 2 | First Impact Window response time | **0.75 s** | `BP_ImpactWindowDirector.FirstWindowDuration` |
| 3 | Standard Impact Window response time | **0.35–0.50 s** | `BP_ImpactWindowDirector.StandardWindowDuration` |
| 4 | Impact Window cinematic burst length | **1–3 s** | clash/burst montage lengths |
| 5 | Meter range | **0–100** | `BP_AscensionComponent` clamp |
| 6 | Meter — light-combo finisher | **+5** | `DT_MeterGains.ComboFinisher` |
| 7 | Meter — perfect dodge | **+12** | `DT_MeterGains.PerfectDodge` |
| 8 | Meter — successful counter | **+15** | `DT_MeterGains.Counter` |
| 9 | Meter — Impact Window success | **+20** | `DT_MeterGains.ImpactWindowSuccess` |
| 10 | Meter — taking damage / waiting | **+0** | `DT_MeterGains.DamageTaken` |
| 11 | Final Clash gate — meter | **100** (full) | `BP_FinalClashDirector.EvaluateClashGate` |
| 12 | Final Clash gate — rival health | **≤ 25 %** | `BP_FinalClashDirector.EvaluateClashGate` |
| 13 | Failed Clash — rival health floor | **1 HP** | `HealthComponent.MinHealthFloor` |
| 14 | Failed Clash — meter setback | **set to 50** | `BP_FinalClashDirector.ClashFailure` |
| 15 | Failed Clash — re-trigger cooldown | **3 s** | `BP_FinalClashDirector.ClashCooldown` |
| 16 | Phase 2 trigger — rival health | **50 %** | `BP_DuelDirector` |
| 17 | Idle / Reposition — Phase 1 | **0.60–1.20 s** | `S_AttackPhaseTuning.RepositionDelay` (P1) |
| 18 | Idle / Reposition — Phase 2 | **0.35–0.80 s** | `S_AttackPhaseTuning.RepositionDelay` (P2) |
| 19 | Select Attack — Phase 1 & 2 | **0.10–0.20 s** | `S_AttackPhaseTuning.SelectDelay` |
| 20 | Telegraph — Phase 1 | **0.55–0.95 s** | `ANS_Telegraph` length × `TelegraphScale` |
| 21 | Telegraph — Phase 2 | **0.40–0.75 s** | as above |
| 22 | Active Attack — Phase 1 & 2 | **0.18–0.45 s** | `ANS_ActiveHit` length — *not phase-scaled* |
| 23 | Recover — Phase 1 | **0.45–0.90 s** | `ANS_Recover` length × `RecoverScale` |
| 24 | Recover — Phase 2 | **0.35–0.75 s** | as above |
| 25 | Return to Neutral — Phase 1 & 2 | **0.10–0.20 s** | `S_AttackPhaseTuning.ReturnToNeutralDelay` |
| 26 | Agent Echo height | **6'0" / 183 cm** | `DA_FighterProfile_Echo.CharacterHeightCm` |
| 27 | Agent Nova height | **5'8" / 173 cm** | `DA_FighterProfile_Nova.CharacterHeightCm` |
| 28 | Crimson Vanguard height | **6'10"** | `BP_CrimsonVanguard` mesh scale |

**Note on rows 17–25:** the GDD publishes **ranges**, and it publishes them per *state*, not per *attack*. The build needs a single float per attack per phase. **Those per-attack values are open (§14 Q25) and must fall inside the published range.** The developer should implement a Data Table validation check that flags any row whose value falls outside its GDD range — so a mistuned number is caught in the editor, not in a playtest.

### 13.2 Values the GDD does not specify — OPEN, designer decides

These appear in the build as exposed variables. Proposed ranges are **questions only** (§14).

| # | Value | Where it lives | Proposed range — **a question, not a decision** |
|---|---|---|---|
| 29 | Player max health (both fighters, identical) | `DA_TuningGlobals` | Q1 |
| 30 | Crimson Vanguard max health | `DA_TuningGlobals` | Q2 |
| 31 | Damage per rival attack A / B / C / D | `DT_VanguardAttacks.Damage` | Q3 |
| 32 | Damage per player light hit; finisher bonus | `AM_Player_LightCombo` notify data | Q4 |
| 33 | Light combo length (number of sections) | `AM_Player_LightCombo` | Q5 |
| 34 | Dodge i-frame window | `ANS_IFrame` | Q6 |
| 35 | Perfect-dodge sub-window | `ANS_PerfectDodge` | Q7 |
| 36 | Whiffed-counter recovery | `AM_Player_CounterWhiff` | Q8 |
| 37 | Meter decay | `BP_AscensionComponent` | Q9 — **recommend none** |
| 38 | Attack A/B/C/D `MinRange` / `MaxRange` | `DT_VanguardAttacks` | Q10 |
| 39 | `LockOnMaxRange` / `LockOnBreakRange` / interp speed | `BP_LockOnComponent` | Q11 |
| 40 | Per-attack cooldown | `DT_VanguardAttacks.Cooldown` | Q12 |
| 41 | Attack D max travel distance | `DT_VanguardAttacks.MaxTravelDistance` | Q13 |
| 42 | Echo / Nova montage play-rate ("timing flavor") | `DA_FighterProfile.MontagePlayRate` | Q14 |
| 43 | Echo / Nova `MaxWalkSpeed` | `DA_FighterProfile` | Q15 |
| 44 | Echo / Nova dodge distance | `DA_FighterProfile.DodgeDistance` | Q16 |
| 45 | Whether Clash beats use `IA_Impact` or a distinct binding | `IMC_Duel` | Q17 |
| 46 | BTTask montage failsafe margin | each `BTTask_*` | Q18 |
| 47 | Post-counter Clash-initiation acceptance window | `BP_FinalClashDirector` | Q19 |
| 48 | Final Clash beat 1 / beat 2 response times | `BP_FinalClashDirector` | Q20 |
| 49 | Failed-Clash separation distance | `BP_FinalClashDirector` | Q21 |
| 50 | Whether the 1 HP floor is permanent or Clash-only | `HealthComponent.MinHealthFloor` | Q22 |
| 51 | Whether a duel timer exists | `BP_DuelDirector` | Q23 — **recommend none** |
| 52 | Arena playable footprint | `L_ShatteredRing` | Q24 |
| 53 | Per-attack values inside each GDD state range | `DT_VanguardAttacks` | Q25 |
| 54 | Standard Impact Window cooldown | `BP_ImpactWindowDirector` | Q26 |
| 55 | `ANS_Recover` incoming-damage multiplier | `ANS_Recover` | Q27 |
| 56 | `ANS_ComboLink` input-buffer window | `AM_Player_LightCombo` | Q28 |
| 57 | Crimson Vanguard short in-combat UI label | `WBP_HUD` | Q29 — **GDD lists this as an open decision** |

---

## 14. Questions for the human designer

The designer agent is not permitted to resolve any of these. Ranges below are **starting points for a conversation**, drawn from what the surrounding GDD numbers imply, and are explicitly not committed values. The developer should implement each as an exposed variable and leave it at whatever the designer sets.

**Combat economy**
- **Q1 — Player max health.** No number in the GDD. Both fighters must be identical (SHARED PLAYER-KIT SCOPE RULE). Range to consider: **100–200**. Consider expressing the whole economy in "how many rival hits kill me" — a 3–5-hit budget is a common readable target for an armored-boss duel.
- **Q2 — Crimson Vanguard max health.** No number. Must be tuned against the **3–5 minute** session target and against the Phase 2 (50%) and Clash (25%) thresholds landing at satisfying moments. Range to consider: **800–2000**.
- **Q3 — Damage per rival attack A–D.** No numbers. Should differentiate the attacks: A (committed close force) heaviest; D (approach) lightest. Suggest expressing each as a **percentage of player max health** so Q1 can move independently.
- **Q4 — Player light-hit damage, and whether the finisher hits harder.** No numbers.
- **Q5 — Light combo length.** GDD says "light attack sequence" without a count. **3 hits** is the common readable default; **4** allows a heavier finisher. Designer decides.

**Defensive timing — this is where the game lives**
- **Q6 — Dodge i-frame window.** No number. Range to consider: **0.20–0.35 s**, starting near the beginning of the dodge montage.
- **Q7 — Perfect-dodge sub-window.** No number. Must be strictly narrower than Q6. Range to consider: **0.08–0.15 s**. **This single number does more to define the game's difficulty than any other in the table.** It should be the first thing tuned in playtest and the first thing revisited after any Phase 2 pass.
- **Q8 — Whiffed-counter recovery.** No number. Must be long enough that spamming counter is worse than reading the telegraph. Range to consider: **0.40–0.70 s**.
- **Q26 — Standard Impact Window cooldown.** The GDD says "approved skill event **after cooldown**" but gives no duration. Range to consider: **3–8 s**. Too short and the cinematic bursts stop feeling earned; too long and the +20 gain becomes unreachable inside a 3–5 minute duel.
- **Q27 — `ANS_Recover` incoming-damage multiplier.** No number. **1.0** (no bonus, the opening is just time) up to **~1.5**. Designer decides whether "punish opening" means extra damage or only safe access.
- **Q28 — `ANS_ComboLink` input-buffer window.** No number. Range to consider: **0.15–0.30 s** before each section ends.

**Spacing**
- **Q10 — Attack A–D range bands (cm).** No numbers. Bands should overlap enough that at least one attack is always valid at combat distance, or `BTTask_Idle_Reposition` will loop repositioning. **This is a likely early bug source — worth tuning together with Q24.**
- **Q11 — Lock-on max range, break range, camera interp speed.**
- **Q13 — Attack D max travel.** The GDD's hard rule is *"no hidden full-arena snap."* Suggest expressing it as a fraction of the arena footprint (Q24) so the two cannot drift apart.
- **Q24 — Arena playable footprint.** Must comfortably fit Q13's travel and Q21's Clash separation.

**Fighter feel**
- **Q14 / Q15 / Q16 — Echo vs Nova play-rate, walk speed, dodge distance.** These three scalars are the **entire** mechanical expression of Echo's "deliberate spacing" versus Nova's "fast lateral rhythm, forward intent" in Phase 1. The GDD's Provisional Design Decisions say to *"approve only presentation-level timing flavor at first."* **My question: does the designer want these to differ at all in Phase 1, or should they be identical until the base duel is stable?** Identical is the more conservative reading of the GDD and is the cheaper build.

**Final Clash**
- **Q17 — Do the Clash beats reuse `IA_Impact`?** Recommend yes, for learned consistency. Designer confirms.
- **Q19 — Post-counter Clash-initiation window.** The GDD permits initiation "during neutral or after a successful counter." How long does "after" last? Range to consider: **0.5–1.5 s**.
- **Q20 — Clash beat 1 and beat 2 response times.** Not in the GDD. **My question: reuse `StandardWindowDuration` (0.35–0.50 s) for both, or author them separately — perhaps beat 2 tighter than beat 1 to make the finish feel like a real test?**
- **Q21 — Failed-Clash separation distance.** Must place both fighters outside every attack's `MinRange` (Q10) so the player is not immediately re-engaged while recovering.
- **Q22 — Is the 1 HP floor permanent or Clash-only?** The GDD states the floor in the *failure* row. **Two readings:** (a) the floor applies only while a Clash is resolving, so ordinary combat damage can still kill the rival and win the duel without a Clash; (b) the floor is permanent once the rival is at low health, making the Final Clash the **only** way to win. Reading (b) makes the Clash the climax the GDD describes and makes the double gate meaningful. **Reading (a) makes it possible to finish the duel without ever seeing the Final Clash, which appears to contradict the encounter flow.** I recommend (b) but I am not permitted to decide it. **This is the single most consequential open question in the document — it changes what the game is about.**

**Structure**
- **Q9 — Does the Ascension Meter decay?** The GDD is silent. Recommend **no decay** — it is consistent with "earned only through active combat decisions" and adds no timer pressure the GDD asks for.
- **Q23 — Is there a duel timer?** The GDD lists only one loss condition (player health zero) and gives 3–5 minutes as a *target session*. Recommend **no timer**.
- **Q18 — BTTask montage failsafe margin.** An engineering safety value, not a feel value. Range to consider: **0.25–0.50 s** past montage length.
- **Q25 — Per-attack values inside each GDD state range.** Four attacks × two phases × four scaled states. The designer should fill these in the Data Table; the developer implements the range-validation check described in §13.1.
- **Q29 — Crimson Vanguard's short in-combat UI label.** The GDD explicitly lists this as unfinalized. `WBP_HUD` needs a string. Formal name is "Crimson Vanguard / Project Valor-7"; the HUD needs something shorter. **Designer decides.** The developer should expose it as a `Text` variable on `WBP_HUD` and leave it blank rather than inventing one.

**Asset decisions**
- **Q30 — Paragon heavy hero for Crimson Vanguard: yes or no, and by when?** (§12.4). If yes, it must land **before** M4 range tuning, or every range value in Q10 gets re-tuned twice.
- **Q31 — Is a silent Phase 1 build acceptable?** No free sound source was verified (§12.6). Shipping silent on 1 September and doing all audio in Phase 2 is the schedule-safe answer, but the designer should say so explicitly rather than discover it.

---

## 15. Constraint compliance statement

| Constraint | How this brief complies |
|---|---|
| **SCOPE LOCK** | One player, one authored AI rival, one arena, one shared player-combat framework, four authored attacks A–D, one duel with win and loss. Every deferred item is named as deferred in §1.3 / §1.4 and is not designed. No unique move sets, no second boss kit, no additional arena, no PvP, no progression, no transformation. |
| **No runtime AI-model calls** | Crimson Vanguard is a `BT_CrimsonVanguard` Behavior Tree with six Blueprint tasks reading a Data Table of authored values. No LLM, no model API, no learning, no adaptive difficulty, no runtime generation appears anywhere in this document. The rival's only nondeterminism is a weighted selection among in-range attacks, using designer-authored weights. |
| **Numbers unchanged** | Every GDD number is reproduced verbatim in §13.1. No number was altered, rounded, averaged, or resolved. Every missing number is listed as `OPEN` in §13.2 with a question in §14, and none is settled. |
| **Milestone order M1→M5** | §11 keeps M5 entirely behind a stable M4. §4.10's presentation subsystem is the structural mechanism preventing M5 work from leaking into M1–M4. §11.6 draws the asset-selection-vs-authored-work line. |
| **Ship 1 September / $0** | §1 is the cut line with seven named risks. §12 sources everything from verified free sources and names four gaps with free fallbacks. No purchase is assumed. |
| **This is Ascendant Impact** | Echo, Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, Ascension Meter, Impact Windows, Final Clash. No content from any other project appears in this document. |

---

## Sources

Unreal Engine implementation research, accessed 2026-07-25:

- [State Tree in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/state-tree-in-unreal-engine)
- [Overview of State Tree in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/unreal-engine/overview-of-state-tree-in-unreal-engine)
- [Unreal Engine 5.8 Release Notes — Epic Developer Community](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)
- [Unreal Engine 5.8 Preview: The Features Indie Developers Actually Care About — StraySpark](https://www.strayspark.studio/blog/unreal-engine-5-8-preview-indie-features-2026)
- [Working With Anim Notifies in Unreal Engine 5 — techarthub](https://techarthub.com/working-with-anim-notifies-in-unreal-engine-5/)
- [Animation Events & Notifies Guide — MoCap Online](https://mocaponline.com/blogs/mocap-news/animation-events-notifies-guide)
- [Precise Melee Hits: Knockouts & Hit Detection in UE5 Blueprints — Shaun Fulton](https://medium.com/@fulton_shaun/precise-melee-hits-knockouts-hit-detection-in-ue5-blueprints-11da5b2a5541)
- [Gameplay Ability System for Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine)
- [GAS Demystified: Building Scalable Combat in UE5 — StraySpark](https://www.strayspark.studio/blog/ue5-gameplay-ability-system-guide)
- [Data Assets in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine)
- [Working with Data in Unreal Engine: Data Tables, Data Assets — Epic Developer Community](https://dev.epicgames.com/community/learning/tutorials/Gp9j/working-with-data-in-unreal-engine-data-tables-data-assets-uproperty-specifiers-and-more)
- [Motion Warping in Unreal Engine — Epic Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine)
- [Motion Warping Blueprint API — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/MotionWarping)
- [Using Spring Arm Components in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-spring-arm-components-in-unreal-engine)
- [Setting Up User Inputs in Unreal Engine (Enhanced Input) — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-user-inputs-in-unreal-engine)
- [How to create a Lock-On/Targeting System on UE5 — The Indie Dev Professor](https://theindieprofessor.wordpress.com/2025/09/28/how-to-create-a-lock-on-targeting-system-on-ue5/)
- [Locomotion in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/unreal-engine/locomotion-in-unreal-engine?lang=en-US)

Free-asset sourcing research, accessed 2026-07-25:

- [Free Epic Games Content for Unreal Engine — Epic Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/free-epic-games-content-for-unreal-engine)
- [$17,000,000 of Paragon content for FREE — Unreal Engine](https://www.unrealengine.com/paragon)
- [Final Round of Free Paragon Assets Released — Unreal Engine](https://www.unrealengine.com/en-US/blog/final-round-of-free-paragon-assets-released)
- [Paragon: Kallari — Fab](https://www.fab.com/listings/ec8f2cb8-f904-4473-902f-67ade18bd225)
- [Paragon: Sevarog — Fab / Unreal Marketplace](https://www.unrealengine.com/marketplace/en-US/item-detail/4865a9dfa3a0429fafc0a099a6ad30f2)
- [Soul: City — Fab](https://www.fab.com/listings/dd77fee6-0ad2-41ce-b32c-09300c24c9f3)
- [Free Infinity Blade Collection — Unreal Engine](https://www.unrealengine.com/en-US/blog/free-infinity-blade-collection-marketplace-release/)
- [Game Animation Sample Project in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-animation-sample-project-in-unreal-engine)
- [Get over 500 free animations with the Game Animation Sample Project — Unreal Engine](https://www.unrealengine.com/blog/game-animation-sample)
- [Explore the updates to the Game Animation Sample Project in UE 5.7 — Unreal Engine](https://www.unrealengine.com/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7)
- [Quixel to Fab Transition FAQs — Fab Support](https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US)
- [Quixel on Fab: New Megascans and Megaplants — Quixel](https://quixel.com/news/quixel-on-fab-new-megascans-and-megaplants)
- [Why Mixamo Is Still a Great Animation Resource — School of Motion](https://schoolofmotion.com/blog/why-mixamo-is-still-one-of-the-best-animation-resources)
- [Free Sci-Fi Station Lands on Fab — Digital Production](https://digitalproduction.com/2026/06/11/free-sci-fi-station-lands-on-fab/)
- [Download 140+ free modular assets for building a sci-fi base — CG Channel](https://www.cgchannel.com/2026/06/download-140-free-modular-assets-for-building-a-sci-fi-base/)

---

*End of design brief. Every rule and number in this document remains the human designer's to approve, change, or reject.*
