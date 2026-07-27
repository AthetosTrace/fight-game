# Build Sequence — Ascendant Impact

**Produced by:** developer agent
**Consumes:** `design-brief.md` (the one input)
**Produces:** this document, for the inspector agent to check against `design-brief.md`
**Engine / platform:** Unreal Engine 5.8 / PC, third person
**Execution surface:** Unreal MCP server driving the UE 5.8 editor. Writing this
sequence does not require the MCP; running it does (per CLAUDE.md build prerequisite
and the designer leave-off handoff).

---

## 0. How to read this build sequence

- Steps are grouped by milestone **M1 → M2 → M3 → M4 → M5, in that order**, and are
  numbered `M<n>-NN`. **No step depends on a later milestone**, and **no M5
  presentation work is interleaved into M1–M4** (design-brief §11, §4.10).
- Each step names its **editor path / menu action**, the **Blueprint / asset / node
  names** involved, **what it produces**, and the **design-brief decision it
  implements, by name**, so the inspector can trace it.
- **Every number is the human designer's and is provisional/tunable.** Carried GDD
  values are reproduced verbatim from design-brief §13.1 and marked *(GDD, provisional
  — tunable, do not change)*. Missing values are implemented as designer-exposed
  variables and left **`OPEN — designer decides`** with their §14 question tag. **No
  step picks a value from a proposed range** (design-brief §0.1, §13, §14).
- **SCOPE LOCK holds:** one player (`BP_PlayerFighter`, Echo/Nova as data), one
  authored rival (`BP_CrimsonVanguard`), one arena (`L_ShatteredRing`), one shared
  combat framework, four authored attacks A–D, one duel with a win and a loss. Nothing
  in design-brief §1.3 (Phase-2/M5 deferred) or §1.4 (outside SCOPE LOCK) gets a build
  step in M1–M4.
- **No runtime AI-model calls.** The rival is `BT_CrimsonVanguard` + Data Table
  (design-brief §3, §6, §15). No step calls a model at runtime.
- **Content root:** `/Game/AscendantImpact/` (design-brief §2). All paths below are
  relative to `/Game/AscendantImpact/` unless the full `/Game/...` path is written out.

---

# M1 — Combat gray box

> **GDD gate (design-brief §11.1):** either fighter can be selected, enters the arena,
> moves, locks on, chains the light combo, dodges directionally with visible i-frames,
> whiffs a counter, takes damage, and dies — **and both avatars pass the same
> collision, targeting, reach, and arena-boundary tests**. Presentation can be toggled
> off with no change to any timing.

This milestone stands up the **one shared player-combat framework** (design-brief §4)
untextured but playable, plus the project foundation the whole build rests on.

### M1-01 — Confirm the base project
- **Action:** Open/confirm a UE **5.8** project created from the **Third Person**
  template (Blueprint). Verify the shipped `SpringArmComponent` + `CameraComponent`
  rig, Enhanced Input, and the standard Third Person `AnimBP` blendspace locomotion.
- **Produces:** a running third-person project to build onto.
- **Implements:** design-brief §1.2 "Third-person movement + camera"; **R2 mitigation**
  — use the standard Third Person `AnimBP` blendspace locomotion for Phase 1 (Motion
  Matching / Game Animation Sample deferred to Phase 2).

### M1-02 — Create the content-root folder structure
- **Path:** `Content Browser > /Game >` right-click `> New Folder`, create
  `AscendantImpact/` and inside it `Core/`, `Player/`, `Rival/`, `Data/`, `Notifies/`,
  `Arena/`, `UI/`, `Input/`.
- **Produces:** the folder layout in design-brief §2.
- **Implements:** design-brief §2 "Content root / folder table".

### M1-03 — Register the gameplay tags
- **Path:** `Project Settings > Project > GameplayTags > Add Tag` (or a tag source
  table in `Core/`). Add: `State.Attacking`, `State.Dodging`, `State.Invulnerable`,
  `State.PerfectWindow`, `State.CanCounter`, `State.InImpactWindow`, `State.Clashing`,
  `Rival.Phase2`.
- **Produces:** the tag set used for state gating with `Has Matching Gameplay Tag` /
  `Add Gameplay Tag` / `Remove Gameplay Tag`, **no GAS dependency**.
- **Implements:** design-brief §3 "Gameplay Tags are available without GAS" (framework
  decision: plain Blueprints, **not** GAS).

### M1-04 — Add the `AttackTrace` collision channel
- **Path:** `Project Settings > Engine > Collision > New Trace Channel...` → name
  `AttackTrace`, **Default Response = Ignore**. Set both fighters' meshes to respond
  **Block** to `AttackTrace`.
- **Produces:** the dedicated trace channel all hit detection uses.
- **Implements:** design-brief §5.2 "add trace channel `AttackTrace` (default response:
  Ignore); both fighters' meshes respond Block".

### M1-05 — Create `DA_TuningGlobals`
- **Path:** `Content Browser > Data/ > Add > Blueprint Class > Data Asset` (or a
  `PrimaryDataAsset` subclass) → `DA_TuningGlobals`.
- **Fields (all designer-exposed, left OPEN):** `PlayerMaxHealth`
  (**OPEN — designer decides, §14 Q1**), `CrimsonVanguardMaxHealth`
  (**OPEN — Q2**). Both fighters' player health identical per SHARED PLAYER-KIT SCOPE
  RULE.
- **Produces:** the single home for the two health-pool numbers.
- **Implements:** design-brief §13.2 rows 29–30; §4.8 "All health pool values are
  OPEN".

### M1-06 — Create `BP_PresentationSubsystem` (wired and EMPTY)
- **Path:** `Content Browser > Core/ > Add > Blueprint Class > GameInstanceSubsystem`
  → `BP_PresentationSubsystem`.
- **Variables:** `bPresentationEnabled` (bool, default **true**), `bShowStateNames`
  (bool), `bDrawHitTraces` (bool).
- **Functions (the ONLY project-legal presentation wrappers), each early-returns if
  `bPresentationEnabled` is false, each BODY LEFT EMPTY in Phase 1:**
  `RequestHitStop(Duration)`, `RequestCameraShake(Class, Scale)`,
  `RequestVFX(NiagaraSystem, Transform)`, `RequestSound(Sound, Location)`,
  `RequestTimeDilation(Scale, Duration)`.
- **Hard rule recorded for the inspector:** `Set Global Time Dilation`,
  `Set Custom Time Dilation`, `Spawn System at Location`, `Play Camera Shake`, and
  `Play Sound at Location` may appear in **exactly one asset — this one**. Anywhere
  else is a defect.
- **Produces:** the presentation kill-switch and the empty landing pad for all M5 work.
- **Implements:** design-brief §4.10 "the presentation kill-switch"; §11.5 structural
  guarantee that M5 changes no gameplay timing.

### M1-07 — Create `WBP_DebugPanel`
- **Path:** `UI/ > Add > User Interface > Widget Blueprint` → `WBP_DebugPanel`. Bind to
  a debug key.
- **Content:** toggles for `BP_PresentationSubsystem.bPresentationEnabled`,
  `.bShowStateNames`, `.bDrawHitTraces`.
- **Produces:** the in-PIE presentation/debug toggle surface.
- **Implements:** design-brief §4.10 "`WBP_DebugPanel` ... toggles"; §1.2 debug row.

### M1-08 — Create the shared `BP_HealthComponent`
- **Path:** `Player/ ` (shared) `> Add > Blueprint Class > ActorComponent` →
  `BP_HealthComponent`. **One class, used by BOTH the player and Crimson Vanguard — no
  subclass.**
- **Variables:** `MaxHealth` (float), `CurrentHealth` (float), `bIsDead` (bool),
  `MinHealthFloor` (float, **default 0**).
- **Function `ApplyDamage(Amount, Instigator)`:** early-return 0 if owner has
  `State.Invulnerable` → subtract → `Clamp (MinHealthFloor, MaxHealth)` → broadcast
  `OnHealthChanged (NewHealth, Percent)` → if `CurrentHealth <= MinHealthFloor` **and**
  `MinHealthFloor == 0`, broadcast `OnDeath`.
- **Events:** `OnHealthChanged`, `OnDeath` (dispatchers).
- **Produces:** shared health with the Final-Clash 1 HP floor as a plain data path (no
  special-case branch).
- **Implements:** design-brief §4.8 "Health"; the 1 HP floor mechanism (§9.4 step 4);
  the 50% Phase 2 / ≤25% Clash health reads (§8.1, §9.1).

### M1-09 — Create `BP_DuelDirector`
- **Path:** `Core/ > Add > Blueprint Class > Actor` → `BP_DuelDirector`. Set as the
  duel's owning actor (spawned by the level / GameMode).
- **Responsibilities (stubs wired now, filled across milestones):** holds duel state,
  the selected `DA_FighterProfile`, `bPhase2Pending`/`bPhase2` flags, `EndDuel(Result)`
  (M4), and subscribes to the rival's `OnHealthChanged` (M2+).
- **Produces:** the top-of-tree owner in the design-brief §2 architecture diagram.
- **Implements:** design-brief §2 "BP_DuelDirector — owns duel state, win/loss, phase
  flag".

### M1-10 — Create the Enhanced Input assets
- **Path:** `Input/ > Add > Input > Input Action` ×8, and
  `Add > Input > Input Mapping Context` → `IMC_Duel`.
- **Input Actions (value types from design-brief §4.3):** `IA_Move` (Axis2D),
  `IA_Look` (Axis2D), `IA_LightAttack` (Digital), `IA_Dodge` (Digital), `IA_Counter`
  (Digital), `IA_LockOn` (Digital), `IA_Impact` (Digital), `IA_FinalClash` (Digital).
- **Note carried forward:** `IA_Impact` is intended to serve the Impact Window **and**
  both Final Clash beats; **whether the Clash beats reuse `IA_Impact` or a distinct
  binding is OPEN — designer decides, §14 Q17.** Wire `IA_Impact` for both by default
  but keep the binding designer-swappable.
- **Produces:** the input layer.
- **Implements:** design-brief §4.3 "Input — Enhanced Input".

### M1-11 — Create `BP_PlayerFighter` (the ONE player class)
- **Path:** `Player/ > Add > Blueprint Class > Character` → `BP_PlayerFighter`.
  **There is no `BP_Echo`, no `BP_Nova`, and no child Blueprints of this class.**
- **Components:** confirm inherited `SpringArmComponent` + `CameraComponent`; add
  `BP_HealthComponent`, and (created below) `BP_CombatComponent`,
  `BP_AscensionComponent` (M3), `BP_LockOnComponent`.
- **`Event BeginPlay`:** `Add Mapping Context (IMC_Duel)`; then call
  `ApplyFighterProfile` (M1-13).
- **Produces:** the single-source player character.
- **Implements:** design-brief §4.1 "The single-source rule"; §2 architecture.

### M1-12 — Create `DA_FighterProfile` + Echo and Nova instances
- **Path:** `Data/ > Add > Blueprint Class > PrimaryDataAsset` → `DA_FighterProfile`;
  then create instances `DA_FighterProfile_Echo` and `DA_FighterProfile_Nova`.
- **Fields (design-brief §4.2):** `DisplayName` (Text: "Agent Echo" / "Agent Nova"),
  `SkeletalMesh`, `AnimClass` (= `ABP_Fighter` **for both**), `CharacterHeightCm`
  (float: **183** Echo / **173** Nova *(GDD, provisional — tunable, do not change)*),
  `StanceAdditivePose` (AnimSequence: upright-technical / compact-layered), `MontageSet`
  (struct of `AnimMontage` refs — **shared set for both in Phase 1, R1**),
  `MontagePlayRate` (**OPEN — §14 Q14**), `MaxWalkSpeed` (**OPEN — Q15**),
  `DodgeDistance` (**OPEN — Q16**), `AccentColor` (LinearColor: Echo restrained
  **orange**; Nova costume palette **preserved**, cyan-white reserved for combat energy
  only — **not a costume recolor**), `IntroMontage` (AnimMontage, abbreviated).
- **Produces:** the only place Echo and Nova differ.
- **Implements:** design-brief §4.2 "`DA_FighterProfile`"; **R1** (one shared montage
  set, differentiate by profile scalars); §12.3 critical color constraint (Nova
  cyan-white is combat energy, not a recolor).

### M1-13 — Implement `ApplyFighterProfile`
- **Where:** function on `BP_PlayerFighter`, called once from `BeginPlay`.
- **Nodes, in order (design-brief §4.2 "Application"):** `Get Selected Profile` (from
  `BP_DuelDirector`) → `Set Skeletal Mesh` → `Set Anim Instance Class` → `Set Actor
  Scale 3D` → `Set Capsule Half Height` → `Set Max Walk Speed` → `Set Vector Parameter
  Value on Materials (AccentColor)`.
- **Scale rule (design-brief §4.2 scale note):** **measure the chosen proxy mesh's
  actual height in-editor and scale to the `CharacterHeightCm` GDD height — do not
  hard-code a scale factor.** Validated by the M1 gate (both avatars run the same
  collision/targeting/reach/boundary tests).
- **Produces:** data-driven fighter application with no subclassing.
- **Implements:** design-brief §4.1, §4.2; GDD "height difference must not create unfair
  hidden reach or collision behavior".

### M1-14 — Create `ABP_Fighter` (shared AnimBP with stance additive)
- **Path:** `Player/ > Add > Animation > Animation Blueprint` (skeleton = proxy
  skeleton) → `ABP_Fighter`. **Same AnimBP for Echo and Nova.**
- **Graph:** standard Third Person blendspace locomotion (R2); apply
  `StanceAdditivePose` from the active `DA_FighterProfile` as an **additive** pose over
  locomotion (this is the entire "stance personality" mechanism); montage slot for the
  combat montages.
- **Produces:** shared animation with per-fighter stance flavor via additive only.
- **Implements:** design-brief §4.2 (`AnimClass` same for both; `StanceAdditivePose`);
  **R1**, **R2**.

### M1-15 — Create `BP_CombatComponent`
- **Path:** `Player/ > Add > Blueprint Class > ActorComponent` → `BP_CombatComponent`.
- **State:** an `FGameplayTagContainer` for `State.*` tags; `bComboBuffered` (bool);
  helpers `AddTag` / `RemoveTag` / `HasTag`.
- **Function `ResolveIncomingHit(Instigator)`** — the three-way branch (design-brief
  §4.6): if player has `State.PerfectWindow` → **Perfect dodge**: damage 0,
  `AddMeter(PerfectDodge)` (M3), `RequestImpactWindow` (M3); else if
  `State.Invulnerable` only → ordinary dodge: damage 0, no meter; else → **Hit**:
  `ApplyDamage`, `AddMeter(DamageTaken)` = +0 (explicit).
- **Function `OnCounterWindowOpen` listener:** sets `State.CanCounter` (wired in M2 to
  the rival broadcast).
- **Produces:** the single hit-resolution source of truth shared by all defensive
  reads.
- **Implements:** design-brief §4.6 "Perfect dodge is detected on the rival's side ...
  one code path, one source of truth"; §5.2 "the player uses the exact same
  `ANS_ActiveHit` class".

### M1-16 — Create `BP_LockOnComponent`
- **Path:** `Player/ > Add > Blueprint Class > ActorComponent` → `BP_LockOnComponent`.
- **Logic (design-brief §4.4):** `IA_LockOn` pressed → if not locked and
  `BP_CrimsonVanguard` within `LockOnMaxRange` and in front of camera → set
  `LockedTarget`. While locked, `Event Tick`: `Find Look at Rotation` → `RInterp To` →
  `Set Control Rotation`; set `bOrientRotationToMovement = false` and
  `bUseControllerDesiredRotation = true` (strafe-facing → side-on readability). Break
  on: second press, distance > `LockOnBreakRange`, or target death. `WBP_HUD` reticle
  (M3) via `Project World to Screen` at target chest socket.
- **Variables (designer-exposed, OPEN):** `LockOnMaxRange`, `LockOnBreakRange`, interp
  speed — **OPEN — §14 Q11**.
- **Attack facing note:** no hard-lock camera snap on attacks in Phase 1; use a short
  rotate-to-target on montage start.
- **Produces:** single-target soft lock-on with strafe facing.
- **Implements:** design-brief §4.4 "Lock-on"; the GDD side-on readability requirement.

### M1-17 — Author `AM_Player_LightCombo`
- **Path:** `Player/ > Add > Animation > Animation Montage` (proxy skeleton) →
  `AM_Player_LightCombo`. Create named **Montage Sections** `Light_01`, `Light_02`,
  `Light_03` — **combo length (number of sections) is OPEN — §14 Q5.**
- **Per-section notify states (created in M1-18):** `ANS_ComboLink` (input-accept
  window), `ANS_ActiveHit` (hit frames). **Final section only:** one-shot
  `AN_ComboFinisher`.
- **Produces:** the combo chain as a single montage with timeline-authored windows.
- **Implements:** design-brief §4.5 "one `AnimMontage` with named Montage Sections".

### M1-18 — Create the player combat notify states / notify
- **Path:** `Notifies/ > Add > Blueprint Class >` `AnimNotifyState` (or `AnimNotify`).
- **`ANS_ComboLink` (AnimNotifyState):** `Received Notify` sets acceptance window;
  input inside sets `bComboBuffered = true`; on `Received Notify End`, if
  `bComboBuffered`, `Montage Set Next Section (Current, Next)`. **Input-buffer window
  OPEN — §14 Q28.**
- **`ANS_ActiveHit` (AnimNotifyState):** `Received Notify Begin` enables trace + clears
  the per-window hit set; `Received Notify Tick` runs `Capsule Trace By Channel`
  (previous socket → current socket, channel `AttackTrace`); `Received Notify End`
  disables trace. Keeps a `Set of Actor` already-hit set. On hit: `Break Hit Result` →
  `Get Hit Actor` → `ResolveIncomingHit`. Debug draw when `bDrawHitTraces`.
- **`AN_ComboFinisher` (AnimNotify, one-shot):** fires `BP_AscensionComponent →
  AddMeter(ComboFinisher)` = **+5** (meter wired in M3).
- **Produces:** the reusable player notify classes; `ANS_ActiveHit` is the shared
  class both fighters use.
- **Implements:** design-brief §4.5 (combo link + finisher notify); §5.2 (hit
  detection); the +5 combo-finisher meter hook (§7.6, wired M3).

### M1-19 — Author `AM_Player_Dodge` with nested i-frame notifies
- **Path:** `Player/ > Add > Animation > Animation Montage` → `AM_Player_Dodge`
  (root-motion), sections `Dodge_F`, `Dodge_B`, `Dodge_L`, `Dodge_R`. Direction from
  `IA_Move` at press.
- **Notify states (in `Notifies/`):** `ANS_IFrame` (AnimNotifyState) — Begin adds
  `State.Invulnerable`, End removes it; while present, `BP_HealthComponent.ApplyDamage`
  returns 0. `ANS_PerfectDodge` (AnimNotifyState) — **nested inside** `ANS_IFrame`,
  tighter, adds `State.PerfectWindow`.
- **Durations (designer-exposed, OPEN):** `ANS_IFrame` window **OPEN — §14 Q6**;
  `ANS_PerfectDodge` sub-window **OPEN — §14 Q7** (must be strictly narrower than Q6).
- **Produces:** directional dodge with visible i-frames and a nested perfect-dodge
  window authored on the timeline.
- **Implements:** design-brief §4.6 "Dodge and perfect dodge".

### M1-20 — Wire the counter input and player counter montages
- **Path:** `Player/ > Add > Animation > Animation Montage` → `AM_Player_Counter` and
  `AM_Player_CounterWhiff`.
- **Logic (design-brief §4.7):** `IA_Counter` while `State.CanCounter` set → successful
  counter (rival-side effects wired in M2: stop rival montage, `AM_Vanguard_CounterReact`,
  force rival to Recover, `AddMeter(Counter)` +15, request Impact Window — meter/impact
  land in M3). `IA_Counter` while `State.CanCounter` **not** set → play
  `AM_Player_CounterWhiff` with punishable recovery. **Whiff recovery duration OPEN —
  §14 Q8.**
- **Produces:** the player half of the counter (rival half comes in M2); the whiff
  punish exists so counter-spam is worse than reading the telegraph.
- **Implements:** design-brief §4.7 "Counter" and its "Skill Creates Spectacle" pillar
  anchor. (Note per §11.1 M1 item 7: rival side comes in M2.)

### M1-21 — Gray-box `L_ShatteredRing`
- **Path:** `Arena/ > Add > Level` → `L_ShatteredRing`. Build with geometry brushes /
  simple static meshes.
- **Functional requirements only (design-brief §10.2):** (1) a **central combat floor**
  — flat disc/rectangle large enough for attack-D capped travel and Clash separation
  (**footprint OPEN — §14 Q24**); (2) a **far doorway** opening with `TargetPoint`
  `PS_VanguardEntrance` and `PS_VanguardCombatMark`; (3) **reverse third-person
  framing** — player spawn faces the far doorway, headroom/backspace so the spring arm
  never clips at the boundary; (4) **side-on readability** — nothing tall/busy inside
  the central floor. Add a `Blocking Volume` boundary ring and a `Kill Z` far below.
- **Negative Phase-1 requirement (R6):** **no hazards, no damage volumes, no physics
  objects** that can affect the duel. Environmental reaction is **M5**.
- **Produces:** the playable gray-box arena.
- **Implements:** design-brief §10.2 "Shattered Ring — Phase 1 arena spec"; §1.5 R6.

### M1-22 — Character-select entry
- **Path:** `UI/ > Add > Widget Blueprint` → `WBP_CharacterSelect`; `Arena/ ` (or a
  dedicated menu folder) `> Add > Level` → `L_CharacterSelect`.
- **Content (design-brief §10.1 Phase-1 row):** two portrait buttons (Echo / Nova),
  name, one-line identity, both `DA_FighterProfile` previews in a lit box; store the
  choice in the Game Instance; `Open Level (L_ShatteredRing)` with a fade.
- **Produces:** the GDD "simplified selection screen" allowance realization.
- **Implements:** design-brief §10.1 "Opening flow — Phase 1 realization"; §1.2 fighter
  selection.

### M1-23 — Stand up the dressed proxies (asset selection, NOT presentation)
- **Action (design-brief §12):** import free proxies and assign into
  `DA_FighterProfile` / arena. **Echo** = UE5 Mannequin (Manny) scaled to 183 cm with a
  recolored `Material Instance` (orange emissive accent). **Nova** = UE5 Mannequin
  (Quinn) scaled to 173 cm, own `Material Instance`, **costume palette preserved,
  cyan-white as a separate combat-energy parameter only**. **Crimson Vanguard proxy**
  (used from M2) = §12.4 fallback ladder option 1 (Mannequin scaled to 208 cm with
  attached static-mesh shoulder/gauntlet proxy blocks + red/black material). Arena
  surfaces = free Quixel/Starter materials. **All licensing re-confirmed by the human
  at claim time (GDD rights-review gate); nothing here is approved by listing it.**
- **Produces:** a gray-box-plus that reads as a duel, via file-drop asset selection.
- **Implements:** design-brief §12; §11.6 asset-selection-vs-authored-work line;
  R1/R4. **Real character art is M5** (§12.6).

### M1-GATE — Verify M1
- Select either fighter → enter arena → move, lock on, chain the light combo, dodge
  directionally with visible i-frames, whiff a counter, take damage, die. **Run both
  avatars through the same collision, targeting, reach, and arena-boundary tests.**
  Toggle `bPresentationEnabled` off and confirm **no timing changes**.
- **Implements:** design-brief §11.1 "Done when".

---

# M2 — Rival state loop

> **GDD gate (design-brief §11.2):** all six AI states and one Crimson Vanguard attack
> complete without deadlock; **returns to Neutral every attempt** — including when
> countered mid-attack, when the player leaves range mid-telegraph, and when the player
> stands still. Visible state names throughout.

**M2 requires all six states and ONE attack (Attack A). All four attacks are required
by M4, not M2** (design-brief §0.1).

### M2-01 — Create the rival enums
- **Path:** `Data/ ` (or `Core/`) `> Add > Blueprint > Enumeration`.
- **`E_VanguardState`** (values **in GDD order**): `Idle_Reposition`, `SelectAttack`,
  `Telegraph`, `ActiveAttack`, `Recover`, `ReturnToNeutral`.
- **`E_VanguardAttackID`:** `A`, `B`, `C`, `D`.
- **Produces:** the state and attack-identity enums.
- **Implements:** design-brief §6.2 "`E_VanguardState` values, in GDD order"; §5.3
  `AttackID`.

### M2-02 — Create `S_AttackPhaseTuning`
- **Path:** `Data/ > Add > Blueprint > Structure` → `S_AttackPhaseTuning`.
- **Fields (design-brief §5.3):** `RepositionDelay` (float), `SelectDelay` (float),
  `TelegraphScale` (float), `RecoverScale` (float), `ReturnToNeutralDelay` (float),
  `SelectionWeight` (float).
- **Provisional GDD ranges (per state; *tunable, do not change*):** Reposition
  **0.60–1.20 s** P1 / **0.35–0.80 s** P2; Select **0.10–0.20 s** both; Telegraph
  **0.55–0.95 s** P1 / **0.40–0.75 s** P2; Recover **0.45–0.90 s** P1 / **0.35–0.75 s**
  P2; Return-to-Neutral **0.10–0.20 s** both. **The single per-attack float inside each
  range is OPEN — §14 Q25.**
- **Produces:** the reused phase-tuning struct.
- **Implements:** design-brief §5.3 `S_AttackPhaseTuning`; §13.1 rows 17–25 and their
  note.

### M2-03 — Create `S_VanguardAttackDef`
- **Path:** `Data/ > Add > Blueprint > Structure` → `S_VanguardAttackDef`.
- **Fields (design-brief §5.3):** `AttackID` (`E_VanguardAttackID`), `DebugName`
  (Name), `Montage` (AnimMontage), `MinRange`/`MaxRange` (float — **OPEN — §14 Q10**),
  `Damage` (float — **OPEN — §14 Q3**), `Cooldown` (float — **OPEN — §14 Q12**),
  `bUsesPropulsion` (bool), `MaxTravelDistance` (float — **OPEN — §14 Q13**),
  `bLockTrackingAtActive` (bool), `Phase1` (`S_AttackPhaseTuning`), `Phase2`
  (`S_AttackPhaseTuning`).
- **Produces:** the one struct that makes attacks data, not four graphs.
- **Implements:** design-brief §5.3 "Attacks A–D are data, not four graphs".

### M2-04 — Create `DT_VanguardAttacks` with all four rows
- **Path:** `Data/ > Add > Miscellaneous > Data Table` → row struct
  `S_VanguardAttackDef` → `DT_VanguardAttacks`. Create **exactly four rows: `A`, `B`,
  `C`, `D`** now, even though only Attack A's montage is authored this milestone (M4
  authors B/C/D).
- **Row-validation check:** add an editor-time check that flags any per-attack tuning
  value falling **outside its GDD range** (design-brief §13.1 note) — so a mistuned
  number is caught in-editor, not in playtest. The check **flags**, it does not pick.
- **Produces:** the single attack data path.
- **Implements:** design-brief §5.3 "`DT_VanguardAttacks` — exactly four rows"; §11.2
  item 4 (all four rows created at M2).

### M2-05 — Create `BP_CrimsonVanguard`
- **Path:** `Rival/ > Add > Blueprint Class > Character` → `BP_CrimsonVanguard`.
- **Components:** the **shared** `BP_HealthComponent` (same class as the player, no
  subclass); mesh responds `Block` to `AttackTrace`; the Vanguard proxy from M1-23.
- **Produces:** the one authored rival actor.
- **Implements:** design-brief §2 architecture; §4.8 shared health.

### M2-06 — Create `BP_VanguardCombatComponent`
- **Path:** `Rival/ > Add > Blueprint Class > ActorComponent` →
  `BP_VanguardCombatComponent`.
- **Responsibilities:** reads `DT_VanguardAttacks`; owns `bCounterable`,
  `IncomingDamageMultiplier`; broadcasts `OnCounterWindowOpen`, `OnCountered`; calls the
  player's `ResolveIncomingHit` when `ANS_ActiveHit` connects.
- **Produces:** the rival combat brain that the notify states and BT tasks drive.
- **Implements:** design-brief §4.6 (calls `ResolveIncomingHit`), §4.7 (counterable),
  §5.1 (`ANS_Recover` multiplier), §6.5 (`OnCountered`).

### M2-07 — Create `BP_VanguardController` (AIController)
- **Path:** `Rival/ > Add > Blueprint Class > AIController` → `BP_VanguardController`.
- **`Event BeginPlay`:** `Run Behavior Tree (BT_CrimsonVanguard)`; set Blackboard
  `TargetActor` from `Get Player Pawn`. **No `AIPerceptionComponent`** (design-brief
  §3, §6.2 — one target, always exists).
- **Produces:** the controller running the tree.
- **Implements:** design-brief §6.1 "run from `BP_VanguardController`"; §3 "Also not
  used: AI Perception".

### M2-08 — Create `BB_CrimsonVanguard` (Blackboard)
- **Path:** `Rival/ > Add > Artificial Intelligence > Blackboard` → `BB_CrimsonVanguard`.
- **Keys (design-brief §6.2):** `TargetActor` (Object/Actor), `CurrentState`
  (`E_VanguardState`, the debug-visible name), `SelectedAttack` (`E_VanguardAttackID`),
  `bPhase2` (Bool), `DistanceToTarget` (Float), `bCounteredThisAttack` (Bool),
  `bInClash` (Bool).
- **Produces:** the Blackboard.
- **Implements:** design-brief §6.2 "The Blackboard".

### M2-09 — Build `BT_CrimsonVanguard`
- **Path:** `Rival/ > Add > Artificial Intelligence > Behavior Tree` →
  `BT_CrimsonVanguard`, using `BB_CrimsonVanguard`.
- **Structure (design-brief §6.3):**
  `ROOT → Selector`:
  - branch 1: **Decorator `Blackboard — bInClash Is Set`** → `BTTask_WaitIndefinite`
    (the Clash owns the rival; tree idles);
  - branch 2: **Sequence "Attack Cycle"** with **Decorator `Loop (Infinite)`**, and two
    services attached: `BTService_UpdateCombatData` and `BTService_DrawDebugState`.
    Children in order: `BTTask_Idle_Reposition`, `BTTask_SelectAttack`,
    `BTTask_Telegraph`, `BTTask_ActiveAttack`, `BTTask_Recover`,
    `BTTask_ReturnToNeutral`.
- **Deliberately NOT used:** `Abort Self` decorators, `Simple Parallel` aborts,
  `Stop Logic` (design-brief §6.5 — each is a route to a stranded state).
- **Produces:** the strict six-state linear loop.
- **Implements:** design-brief §6.1 (BT not State Tree), §6.3 (the tree).

### M2-10 — Create `BTService_UpdateCombatData`
- **Path:** `Rival/ > Add > Blueprint Class > BTService_BlueprintBase` →
  `BTService_UpdateCombatData`.
- **Logic:** refresh `DistanceToTarget`; keep the rival facing the target
  (`Set Focus`).
- **Produces:** live combat data on the Blackboard.
- **Implements:** design-brief §6.3 services list; §6.4 task 1 range logic.

### M2-11 — Create `BTService_DrawDebugState`
- **Path:** `Rival/ > Add > Blueprint Class > BTService_BlueprintBase` →
  `BTService_DrawDebugState`.
- **Logic:** `Draw Debug String` above the rival's head, e.g.
  `CV | Phase 1 | Telegraph | Attack_A_GauntletForce | 0.41s`, gated on
  `BP_PresentationSubsystem.bShowStateNames`. Plus rely on the built-in **Gameplay
  Debugger** (apostrophe key) for the Blackboard dump.
- **Produces:** the GDD "visible debug state names" (two independent views).
- **Implements:** design-brief §6.6; §6.1 reason 1.

### M2-12 — Create the six `BTTask_*` tasks
- **Path:** `Rival/ > Add > Blueprint Class > BTTask_BlueprintBase` ×6, each implements
  `Receive Execute AI` and calls `Finish Execute (Success)` at its exit condition.
- **Universal conventions (design-brief §6.3):** the **first node** of every task's
  `Receive Execute AI` is `Set Blackboard Value as Enum (CurrentState, <its own
  state>)`. Every task that waits on a montage sets a `Set Timer by Event` **failsafe**
  of (montage length + margin) that calls `Finish Execute (Success)` if
  `On Montage Ended` never fires. **Failsafe margin OPEN — §14 Q18.**
- **The six (design-brief §6.4):**
  1. **`BTTask_Idle_Reposition`** — play neutral/strafe locomotion; `Set Focus`; if
     `DistanceToTarget` outside every attack range band, `Move To Actor`; wait
     `RepositionDelay` (active phase); exit when timer elapses **and** at least one
     row's `MinRange..MaxRange` contains `DistanceToTarget`.
  2. **`BTTask_SelectAttack`** — filter the four rows to in-range **and** off-cooldown;
     pick one by `SelectionWeight` (active phase); write `SelectedAttack`; stamp that
     attack's cooldown. Wait `SelectDelay`.
  3. **`BTTask_Telegraph`** — `Play Anim Montage (Row.Montage)`, jump to `Telegraph`
     section, apply `TelegraphScale` as play rate; exit on `ANS_Telegraph → Received
     Notify End`.
  4. **`BTTask_ActiveAttack`** — montage continues into `Active`; `ANS_ActiveHit`
     traces; `ANS_TrackingLock` freezes facing where the row asks (B/C, M4); attack D
     travel capped at `MaxTravelDistance` (M4); exit when active frames end.
  5. **`BTTask_Recover`** — montage runs `Recover` at `RecoverScale`; `ANS_Recover`
     raises `IncomingDamageMultiplier` (the punish opening); no new attack; exit on
     recovery complete. If `bCounteredThisAttack`, play the counter-reaction montage
     instead (§6.5).
  6. **`BTTask_ReturnToNeutral`** — clear all attack flags (`SelectedAttack = None`,
     `bCounteredThisAttack = false`, restore damage multiplier, re-enable tracking,
     `Set Movement Mode (Walking)`, clear montage); then evaluate the Phase 2 commit
     (M4 fills the commit body).
- **Hard rule recorded for the inspector:** every task has a **guaranteed exit** — this
  is the M2 gate "Returns to Neutral every attempt", implemented not hoped for.
- **Produces:** the six state tasks, deterministic, no runtime model call.
- **Implements:** design-brief §6.3, §6.4; §15 no-runtime-AI compliance.

### M2-13 — Author Attack A montage and its notify states
- **Path:** `Rival/ > Add > Animation > Animation Montage` → `AM_Vanguard_AttackA`
  (proxy skeleton). Lay out on the timeline (design-brief §5.1):
  `[ANS_Telegraph][ANS_ActiveHit][ANS_Recover]` with `ANS_CounterWindow` overlapping
  late telegraph / early active.
- **Notify states (in `Notifies/`):**
  - **`ANS_Telegraph`** — Begin: `Set Blackboard CurrentState = Telegraph`,
    `RequestVFX` warning lights (empty in Phase 1), set emissive **red-orange**
    telegraph color, broadcast `OnTelegraphStart(AttackID)`; End: clear color. Attack A
    = long telegraph, held gauntlet pose.
  - **`ANS_ActiveHit`** — reuse the M1-18 class (**same class, both fighters**).
  - **`ANS_Recover`** — Begin: `CurrentState = Recover`, raise
    `IncomingDamageMultiplier` (**multiplier value OPEN — §14 Q27**); Attack A =
    longest recover window on the montage; End: restore multiplier.
  - **`ANS_CounterWindow`** — Begin: `bCounterable = true`, broadcast
    `OnCounterWindowOpen`; End: `bCounterable = false`.
- **Provisional GDD window ranges (*tunable, do not change*):** Telegraph
  **0.55–0.95 s**, Active **0.18–0.45 s**, Recover **0.45–0.90 s** (Phase 1). Per-attack
  float **OPEN — §14 Q25**.
- **Produces:** Attack A, fully authored, readable and retunable by dragging notifies.
- **Implements:** design-brief §5.1 (the three windows are notify states; Attack A
  readability row); §11.2 item 5.

### M2-14 — Wire the counter interrupt through the sequence
- **Path (design-brief §6.5):** `BP_VanguardCombatComponent → OnCountered` →
  `Montage Stop` the attack montage → set `bCounteredThisAttack = true` → the running
  task's `On Montage Ended` fires → task calls `Finish Execute (Success)` → the
  `Sequence` advances → `BTTask_Recover` reads `bCounteredThisAttack` and plays
  `AM_Vanguard_CounterReact`. Also complete the player side left open in M1-20 (stop
  rival montage, force rival to Recover — **the one legal external interrupt**).
- **Produces:** the only legal mid-attack interrupt, routed **through** the sequence.
- **Implements:** design-brief §6.5 "The one legal interrupt"; §4.7 counter success.

### M2-GATE — Verify M2
- Rival cycles Idle/Reposition → Select → Telegraph → Active → Recover → Return to
  Neutral **continuously for several minutes, no deadlock**, visible state names, and
  reaches Return to Neutral on **every** attempt — including countered mid-attack,
  player out of range mid-telegraph, and player standing still. Player can dodge,
  perfect-dodge (meter not yet wired), and counter Attack A.
- **Implements:** design-brief §11.2 "Done when".

---

# M3 — Impact handoff

> **GDD gate (design-brief §11.3):** earned prompt, success/failure branches, restored
> control; **no forced success and no stranded cinematic state.**

### M3-01 — Create the meter/impact enums
- **Path:** `Data/ (or Core/) > Add > Blueprint > Enumeration`.
- **`E_MeterEvent`:** `ComboFinisher`, `PerfectDodge`, `Counter`,
  `ImpactWindowSuccess`, `DamageTaken`.
- **`E_ImpactTrigger`:** `PerfectDodge`, `Counter`, `ComboMilestone`.
- **Produces:** the meter-event and impact-trigger enums.
- **Implements:** design-brief §4.9, §7.1.

### M3-02 — Create `S_MeterGain` + `DT_MeterGains` (five rows)
- **Path:** `Data/ > Add > Blueprint > Structure` → `S_MeterGain` (field `Gain`,
  float). Then `Add > Data Table` (row struct `S_MeterGain`) → `DT_MeterGains`.
- **Rows — GDD numbers verbatim (*provisional — tunable, do not change*):**
  `ComboFinisher` **+5**, `PerfectDodge` **+12**, `Counter` **+15**,
  `ImpactWindowSuccess` **+20**, `DamageTaken` **+0** (explicit, so "damage grants
  nothing" is visible as data).
- **Produces:** the single meter-gain table.
- **Implements:** design-brief §4.9 `DT_MeterGains`; §13.1 rows 6–10.

### M3-03 — Create `BP_AscensionComponent`
- **Path:** `Player/ > Add > Blueprint Class > ActorComponent` →
  `BP_AscensionComponent` (on the player only).
- **State:** `Meter` (float, clamped **0–100** *(GDD, provisional)*); dispatcher
  `OnMeterChanged (NewValue)`.
- **Single entry point `AddMeter(E_MeterEvent Event)`:** `Get Data Table Row
  (DT_MeterGains, Event)` → `Meter = Clamp(Meter + Row.Gain, 0, 100)` → broadcast
  `OnMeterChanged`. **Nothing else may write `Meter` directly** except
  `BP_FinalClashDirector`'s failure path (M4, sets 50).
- **No time-based gain anywhere** (no tick/timer/regen) — GDD METER DEFINITION.
- **Meter decay: OPEN — §14 Q9 (brief recommends none; developer leaves it OPEN).**
- **Produces:** the 0–100 meter with one write path.
- **Implements:** design-brief §4.9 "The Ascension Meter".

### M3-04 — Create `WBP_HUD` (meter bar + reticle + gate indicators stub)
- **Path:** `UI/ > Add > Widget Blueprint` → `WBP_HUD`.
- **Content:** meter progress bar bound to `OnMeterChanged`; lock-on reticle at the
  target chest socket via `Project World to Screen` (from M1-16); the two Final-Clash
  gate indicators (filled M4); a **`Text` variable for Crimson Vanguard's short
  in-combat label, left BLANK — OPEN — §14 Q29** (do not invent a name).
- **Produces:** the functional HUD.
- **Implements:** design-brief §4.9 (meter bar), §4.4 (reticle), §9.1 (honest gate
  indicators), §14 Q29.

### M3-05 — Wire all five meter hooks
- **Hooks (design-brief §7.6), all through `AddMeter(E_MeterEvent)`:** `AN_ComboFinisher`
  → `ComboFinisher` (+5); `ResolveIncomingHit` `State.PerfectWindow` branch →
  `PerfectDodge` (+12); `IA_Counter` accepted inside `ANS_CounterWindow` → `Counter`
  (+15); `BP_ImpactWindowDirector` SUCCESS → `ImpactWindowSuccess` (+20);
  `ResolveIncomingHit` damage branch → `DamageTaken` (+0, explicit).
- **Produces:** five call sites, one table, one clamp.
- **Implements:** design-brief §7.6 "Where the five meter events hook in".

### M3-06 — Create `WBP_ImpactPrompt`
- **Path:** `UI/ > Add > Widget Blueprint` → `WBP_ImpactPrompt`.
- **Content:** the timing-input prompt shown while a window is open; no auto-anything.
- **Produces:** the Impact/Clash prompt widget (reused for both Clash beats in M4).
- **Implements:** design-brief §7.1, §9.2 (R3 reuse).

### M3-07 — Create `BP_ImpactWindowDirector`
- **Path:** `Core/ > Add > Blueprint Class > Actor` → `BP_ImpactWindowDirector` (owned
  by `BP_DuelDirector`).
- **`RequestImpactWindow(E_ImpactTrigger)`** — refuses/returns immediately if a window
  is already open, standard-window cooldown not elapsed, `bInClash` true, or either
  fighter dead. The three triggers (design-brief §7.1): perfect dodge, successful
  counter, approved combo milestone.
- **Window width selection (design-brief §7.2):** hold `bFirstWindowConsumed` (false at
  duel start); pick `FirstWindowDuration` if false **and** trigger was perfect dodge or
  counter (combo milestone does **not** qualify for the wider onboarding window), then
  set it true; otherwise `StandardWindowDuration`.
- **Durations — GDD verbatim (*provisional — tunable, do not change*):**
  `FirstWindowDuration` = **0.75 s**; `StandardWindowDuration` = **0.35–0.50 s**.
  **Standard-window cooldown OPEN — §14 Q26.**
- **Scoring (design-brief §7.4):**
  - `OpenWindow(Duration)`: `bWindowOpen = true`; show `WBP_ImpactPrompt`;
    `Set Timer by Event (Duration) → OnWindowExpired`.
  - `IA_Impact (Triggered)` while `bWindowOpen`: `Clear and Invalidate Timer by Handle`;
    `bWindowOpen = false`; hide prompt → **SUCCESS**.
  - `OnWindowExpired`: `bWindowOpen = false`; hide prompt → **FAILURE**.
- **SUCCESS branch:** `AddMeter(ImpactWindowSuccess)` +20; play the **1–3 s** *(GDD,
  provisional)* choreographed burst as a **montage pair** on both fighters, plus
  `RequestHitStop` / `RequestCameraShake` **through the subsystem (empty in Phase 1)**;
  then `RestoreCombatState()`.
- **FAILURE branch:** **no cinematic extension, no meter, no extra punishment**; then
  `RestoreCombatState()`; start the standard-window cooldown.
- **The three onboarding prohibitions (design-brief §7.3), recorded for the inspector:**
  (1) no auto-success path — success only from `IA_Impact Triggered` while
  `bWindowOpen`; (2) no input-buffer leniency — an `IA_Impact` press **before**
  `OpenWindow` is **discarded, not queued**; (3) the wider first window changes exactly
  one float — it does not slow time, extend recovery, or soften failure.
- **Produces:** the earned Impact Window with success/fail and the two GDD widths.
- **Implements:** design-brief §7.1–7.4; §7.3 ONBOARDING RULE.

### M3-08 — Write `RestoreCombatState()` once
- **Where:** one function (on `BP_DuelDirector` or a shared library), called by **every
  branch of both systems** — Impact success, Impact failure, Clash success (M4), Clash
  failure (M4). **Not four copies.**
- **Body (design-brief §7.5):** `Enable Input`; `Set Collision Enabled` (both capsules →
  Query and Physics); `Set Movement Mode (Walking)` on both; clear all transient tags
  (`State.Attacking`, `State.Invulnerable`, `State.PerfectWindow`,
  `State.InImpactWindow`, `State.Clashing`); restore lock-on if it was active;
  `Set Global Time Dilation → 1.0` **(via `BP_PresentationSubsystem` only)**; rival
  `bInClash = false`, `CurrentState = Idle_Reposition`, Behavior Tree resumes; hide
  `WBP_ImpactPrompt`.
- **Produces:** the single restore path — one bug lives in one place.
- **Implements:** design-brief §7.5 "the single restore function"; GDD "always return
  control to the player".

### M3-GATE — Verify M3
- A perfect dodge or counter opens a prompt; hitting it grants +20 and plays the burst;
  missing it returns to combat with no punishment and no meter; **doing nothing never
  produces success**; an `IA_Impact` press before the window opens is **discarded**;
  after either branch the player has input, collision, locomotion, and lock-on and the
  rival's Behavior Tree is running.
- **Implements:** design-brief §11.3 "Done when".

---

# M4 — Complete duel

> **GDD gate (design-brief §11.4):** meter, Phase 2, Final Clash, failure recovery,
> win/loss — a start-to-finish course prototype. **This is the 1 September deliverable**
> (target functional completion ~20 August, R7).

### M4-01 — Author Attacks B, C, and D
- **Path:** `Rival/ > Add > Animation > Animation Montage` ×3 → `AM_Vanguard_AttackB`,
  `AM_Vanguard_AttackC`, `AM_Vanguard_AttackD`, each laid out like Attack A:
  `ANS_Telegraph`, `ANS_ActiveHit`, `ANS_Recover`, `ANS_CounterWindow`. Fill the
  `B/C/D` rows in `DT_VanguardAttacks` including `Phase1` and `Phase2` tuning.
- **Per-attack readability (design-brief §5.1 table):**
  - **B** (committed forward-pressure sequence) — visible first beat; **multiple
    separate `ANS_ActiveHit` states**, one per beat, so each beat is individually
    dodgeable; `ANS_TrackingLock` at a fixed point (stable tracking limit).
  - **C** (armored reach / space control) — body direction locked before active by
    `ANS_TrackingLock`; active-range capsule visible via the debug toggle.
  - **D** (short propulsion-assisted approach) — thruster cue in `ANS_Telegraph`; root
    motion (or Motion Warping, **R5**) travel **hard-capped at `MaxTravelDistance`** —
    the cap is data, **no hidden full-arena snap**.
- **Numbers:** all window/tuning floats **OPEN — §14 Q25**, inside GDD ranges; Active
  window **0.18–0.45 s** *(GDD, provisional — **identical both phases, not
  phase-scaled**)*.
- **Produces:** the full four-attack set.
- **Implements:** design-brief §5.1 readability table; §11.4 items 1–2; R5.

### M4-02 — Create `ANS_TrackingLock`
- **Path:** `Notifies/ > Add > Blueprint Class > AnimNotifyState` → `ANS_TrackingLock`.
- **Logic:** turns off the rival's rotate-to-target (facing freeze) for its duration —
  the "stable tracking limit" for B and C, gated by `bLockTrackingAtActive` on the row.
- **Produces:** tracking-limit mechanic (not a note).
- **Implements:** design-brief §5.1 (B/C rows), §5.3 `bLockTrackingAtActive`.

### M4-03 — Range- and cooldown-based selection across all four attacks
- **Where:** `BTTask_SelectAttack` (M2-12), now exercising all four rows.
- **Logic:** filter to in-range **and** off-cooldown; pick by `SelectionWeight` from the
  **active phase's** tuning; stamp cooldown. The only nondeterminism is a **weighted
  selection among in-range attacks using authored weights** — **no runtime model call.**
- **Range bands OPEN — §14 Q10** (tune with arena footprint Q24 — likely early bug
  source).
- **Produces:** authored, weighted, deterministic attack selection over A–D.
- **Implements:** design-brief §6.4 task 2; §11.4 item 3; §15 no-runtime-AI.

### M4-04 — Phase 2 via the one data path
- **Trigger (design-brief §8.1):** `BP_DuelDirector` listens to CV
  `OnHealthChanged`; when `Percent <= 0.50` *(GDD, provisional)* and `bPhase2Pending`
  false → set `bPhase2Pending = true`. **Nothing else happens yet.**
- **Commit (design-brief §8.1):** in `BTTask_ReturnToNeutral` and **nowhere else**, as
  its last act after clearing flags: `if bPhase2Pending and not bPhase2 → Set Blackboard
  Value as Bool (bPhase2, true) → broadcast OnPhase2Committed → bPhase2Pending = false`.
- **One-shot signal (design-brief §8.2):** `OnPhase2Committed` fires **one**
  presentation beat through `BP_PresentationSubsystem` (Phase 1 = emissive-intensity
  change + brief pause; authored VFX/sound/thruster are **M5**), guarded by `bPhase2`
  so it cannot fire twice.
- **Data path (design-brief §5.3 / §8.3):** every timed task reads tuning via **one
  `Select` node keyed on `bPhase2`**: `Row.Phase2 : Row.Phase1`. **No second table, no
  second montage set, no second BT branch, no transformation rig.** Active window stays
  unscaled.
- **Produces:** re-timed Phase 2 on the same four attacks.
- **Implements:** design-brief §8 "Phase 2 — same four attacks, re-timed through one
  data path"; §11.4 item 4.

### M4-05 — Create `BP_FinalClashDirector` and the double gate
- **Path:** `Core/ > Add > Blueprint Class > Actor` → `BP_FinalClashDirector` (owned by
  `BP_DuelDirector`).
- **`EvaluateClashGate()`** — called from `OnMeterChanged` and CV `OnHealthChanged`
  only (design-brief §9.1): `bClashEligible = (Meter >= 100) AND (CV Health Percent <=
  0.25) AND (Clash cooldown not active) AND (not bInClash)`. **Both** meter-100 and
  ≤25% health *(GDD, provisional)* required; if only one, the Clash stays **locked**.
- **HUD honesty:** `WBP_HUD` shows **two separate gate indicators** so the player sees
  which condition is missing.
- **Initiation (design-brief §9.1):** `IA_FinalClash` accepted only when `bClashEligible`
  **and** the player is in **neutral** or inside the **post-counter success window**
  (window duration **OPEN — §14 Q19**). **Never auto-triggers.**
- **Produces:** the double gate and player-initiated Clash entry.
- **Implements:** design-brief §9.1 "The double gate"; §13.1 rows 11–12.

### M4-06 — The two timing beats (reuse §7 machinery) + `LS_FinalClash`
- **Assets:** `Arena/ (or UI cinematics) > Add > Cinematics > Level Sequence` →
  `LS_FinalClash`; montages `AM_Clash_Beat1`, `AM_Clash_Finisher`,
  `AM_Vanguard_CounterReact` (if not already present).
- **`InitiateClash()` (design-brief §9.2):** `bInClash = true` (rival BT parks on
  `BTTask_WaitIndefinite`); disable normal combat input, leave `IA_Impact` live; play
  `AM_Clash_Beat1` on both; play `LS_FinalClash` (one camera cut); `OpenClashBeat(1)`
  using the **same `WBP_ImpactPrompt` + timer machinery from M3** → hit →
  `OpenClashBeat(2)` → hit → **SUCCESS**; any miss → **FAILURE**.
- **Beat durations OPEN — §14 Q20** (brief asks: reuse `StandardWindowDuration`
  0.35–0.50 s, or author separately — do not decide).
- **Produces:** the affordable Clash (R3 mitigation).
- **Implements:** design-brief §9.2 "The two timing beats"; §11.4 item 5.

### M4-07 — Clash SUCCESS → Win
- **`ClashSuccess()` (design-brief §9.3):** play `AM_Clash_Finisher` on both → on
  montage end, rival `BP_HealthComponent` `MinHealthFloor = 0` then
  `ApplyDamage(MaxHealth)` → `OnDeath` → `BP_DuelDirector → EndDuel(Win)` → `WBP_Result`
  in Win state. **`RestoreCombatState()` runs before the result screen.**
- **Produces:** the win path.
- **Implements:** design-brief §9.3 "Success"; §11.4 item 6.

### M4-08 — Clash FAILURE → the exact seven-step recovery
- **`ClashFailure()` in order (design-brief §9.4), all numbers GDD-verbatim:**
  1. `Montage Stop` both; stop `LS_FinalClash`; return camera to gameplay.
  2. **Separate both fighters** — `Set Actor Location` pushed apart along their axis,
     `Set Actor Rotation` to face each other. **Separation distance OPEN — §14 Q21**;
     must place both outside every attack's `MinRange`.
  3. **Preserve current health** — no health change (except step 4).
  4. **Rival held at a 1 HP floor** — `CV HealthComponent → MinHealthFloor = 1`.
     **Whether the floor is permanent from first eligibility or Clash-only is OPEN —
     §14 Q22** (brief flags this as the single most consequential open question; do not
     decide).
  5. **Reduce meter to 50** — `BP_AscensionComponent → Meter = 50` *(GDD, provisional)*,
     the **one sanctioned exception** to the `AddMeter`-only rule, commented as such.
  6. **3-second re-trigger cooldown** — `Set Timer by Event (3.0) → OnClashCooldownEnd`
     *(GDD, provisional)*; `bClashEligible` forced false; `EvaluateClashGate()` re-runs
     when it ends.
  7. **Return to Neutral** — `RestoreCombatState()`; `bInClash = false`; rival BT leaves
     `BTTask_WaitIndefinite` and re-enters at `Idle_Reposition`.
- **Must NOT happen:** duel restart; player killed/damaged; anyone left in a cinematic
  state (input off, collision off, montage playing).
- **Produces:** the recoverable failure path — never a restart, never a player death.
- **Implements:** design-brief §9.4 "Failure — the exact sequence"; §13.1 rows 13–15.

### M4-09 — Loss condition and `WBP_Result`
- **Path:** `UI/ > Add > Widget Blueprint` → `WBP_Result` with **Win** and **Loss**
  states and a **restart** option.
- **Loss (design-brief §9.5):** the **only** loss is the selected fighter's health
  reaching zero → player `OnDeath` → `BP_DuelDirector → EndDuel(Loss)` → `WBP_Result`
  Loss. **No duel timer** — the 3–5 minute figure is a target session length, not a rule
  (**OPEN — §14 Q23, brief recommends none; leave OPEN**).
- **Produces:** win and loss result screens.
- **Implements:** design-brief §9.5 "Loss"; §11.4 item 8.

### M4-10 — `LS_VanguardEntrance` (abbreviated, skippable)
- **Path:** `Arena/ > Add > Cinematics > Level Sequence` → `LS_VanguardEntrance`.
- **Content (design-brief §10.1):** rival walks from `PS_VanguardEntrance` to
  `PS_VanguardCombatMark`, fixed camera, **short and skippable**; then
  `RestoreCombatState()`, enable input, start the Behavior Tree.
- **Produces:** the abbreviated arena entrance (GDD simplified allowance).
- **Implements:** design-brief §10.1 (CV enters through the far doorway); §11.4 item 9.

### M4-GATE — Verify M4
- Select Echo **or** Nova → watch the abbreviated entrance → fight Phase 1 → see Phase 2
  commit at 50% **on Return to Neutral** and signal **exactly once** → reach the double
  gate → **fail a Final Clash and recover** (meter 50, rival at 1 HP floor, 3 s
  cooldown, full control restored, duel continuing) → then succeed → Win screen; and
  separately, die → Loss screen. **Both avatars complete the full duel.**
- **Implements:** design-brief §11.4 "Done when"; the 1 September Phase 1 deliverable.

---

# M5 — Presentation pass (Phase 2 — ONLY after M4 is stable)

> **GDD gate (design-brief §11.5):** only after M4 is stable. This is Phase 2, after
> 1 September. **M5 must not be interleaved into M1–M4.** The structural guarantee is
> §4.10: everything here lands **inside the already-wired `BP_PresentationSubsystem`
> wrappers** (built empty in M1-06) and **changes no gameplay timing**.

Each step fills an existing subsystem wrapper or adds authored content behind it; none
edits a gameplay window, a Data Table tuning value, or a notify-state duration.

### M5-01 — Fill `RequestHitStop` / `RequestTimeDilation` (hit-stop & time-dilation tuning)
- **Where:** `BP_PresentationSubsystem` only. Author hit-stop feel, impact frames,
  time-dilation curves.
- **Implements:** design-brief §1.3 "Tuned hit-stop feel, impact frames, time-dilation";
  §11.5.

### M5-02 — Fill `RequestCameraShake` + camera choreography
- **Where:** `BP_PresentationSubsystem`; author `Camera Shake` classes; dynamic combat
  camera, framing rules, per-attack camera pushes (and the 5.8 Gameplay Camera rig work
  deferred in §4.4).
- **Implements:** design-brief §1.3 "Camera choreography"; §4.4 deferred camera.

### M5-03 — Fill `RequestVFX` with authored Niagara systems
- **Where:** `BP_PresentationSubsystem`; author telegraph energy, thruster plumes,
  warning-light systems, Ascension energy language, **Echo orange vs Nova cyan-white
  combat energy as authored effects** (Phase 1 had flat emissive only; **Nova's costume
  stays preserved — cyan-white is combat energy, not a recolor**).
- **Implements:** design-brief §1.3 authored Niagara; §12.3 color constraint.

### M5-04 — Fill `RequestSound` + full sound design and mix
- **Where:** `BP_PresentationSubsystem`; impacts, thrusters, warning lights, telegraph
  audio cues, music. **No free sound source was verified (§12.6)** — a silent Phase 1
  build is the schedule-safe answer; **whether Phase 1 ships silent is OPEN — §14 Q31;
  music is a named gap.**
- **Implements:** design-brief §1.3 sound; §12.6; §14 Q31.

### M5-05 — Arena environmental reaction (R6)
- **Where:** `L_ShatteredRing`; visible-but-controlled reaction on major impacts, **no
  gameplay hazards / damage volumes / physics objects** (the Phase-1 negative
  requirement still holds).
- **Implements:** design-brief §10.2 environmental-reaction row; §1.5 R6.

### M5-06 — Final character treatment for Echo, Nova, Crimson Vanguard
- **Where:** swap the proxy meshes/materials in `DA_FighterProfile` / `BP_CrimsonVanguard`
  for bespoke art matching the GDD reference sheets. **If a Paragon heavy hero replaces
  the Vanguard proxy, it must land BEFORE M4 range tuning (§12.4, Q30) — otherwise every
  `MinRange`/`MaxRange` re-tunes twice.** Re-validate capsule, sockets, and ranges after
  any mesh swap.
- **Implements:** design-brief §1.3 final character treatment; §12.4; §14 Q30.

### M5-07 — Full-fidelity Final Clash choreography
- **Where:** replace the M4 minimal `LS_FinalClash` cut with authored choreography; the
  **prompt/timer gameplay logic and beat timings are unchanged** (still §7/§9 machinery).
- **Implements:** design-brief §1.3 full-fidelity Final Clash; §9.2 R3 (choreography →
  Phase 2).

### M5-08 — The editorial character-selection interface
- **Where:** replace `WBP_CharacterSelect` with the GDD's editorial layout — technical/
  equipment panels animating around the selected fighter, camera moves.
- **Implements:** design-brief §1.3 editorial selection interface; §10.1 Phase-2 column.

---

## Appendix A — Traceability of the four scope-lock walls

| Wall | Where honored in this sequence |
|---|---|
| **SCOPE LOCK** | One `BP_PlayerFighter` (M1-11, Echo/Nova as `DA_FighterProfile` data, M1-12); one `BP_CrimsonVanguard` (M2-05); one `L_ShatteredRing` (M1-21); four rows A–D in one `DT_VanguardAttacks` (M2-04, filled M4-01); one duel with Win (M4-07) and Loss (M4-09). Nothing from §1.3/§1.4 is built. |
| **No runtime AI-model calls** | Rival is `BT_CrimsonVanguard` + `DT_VanguardAttacks` (M2-09, M2-12); only nondeterminism is authored-weighted selection (M4-03). No step invokes a model at runtime. |
| **Milestone order M1→M5** | Sections are in strict order; every M5 step fills the empty `BP_PresentationSubsystem` wired in M1-06 and changes no timing. No M1–M4 step depends on a later milestone. |
| **Numbers unchanged** | All GDD numbers carried verbatim and marked provisional (M1-05, M2-02, M2-13, M3-02, M3-03, M3-07, M4-04, M4-05, M4-08). All missing numbers implemented as designer-exposed variables and left `OPEN` with their §14 question tag; **no value was picked from a proposed range.** |

## Appendix B — OPEN values preserved (not resolved), by §14 question

Q1 player max health · Q2 CV max health · Q3 per-attack damage A–D · Q4 player light-hit
damage / finisher bonus · Q5 light combo length · Q6 dodge i-frame window · Q7
perfect-dodge sub-window · Q8 whiffed-counter recovery · Q9 meter decay · Q10 attack
range bands · Q11 lock-on ranges / interp speed · Q12 per-attack cooldown · Q13 attack D
max travel · Q14 Echo/Nova play-rate · Q15 Echo/Nova walk speed · Q16 Echo/Nova dodge
distance · Q17 Clash beats binding · Q18 BTTask failsafe margin · Q19 post-counter Clash
window · Q20 Clash beat 1/2 response times · Q21 failed-Clash separation · Q22 1 HP floor
permanent vs Clash-only · Q23 duel timer · Q24 arena footprint · Q25 per-attack values
inside GDD ranges · Q26 standard Impact-Window cooldown · Q27 `ANS_Recover` damage
multiplier · Q28 `ANS_ComboLink` buffer window · Q29 CV short UI label · Q30 Paragon
Vanguard swap (asset) · Q31 silent Phase-1 build acceptable (asset).

**All 29 §13.2 open values plus the two asset decisions (Q30, Q31) are implemented as
exposed variables and left at whatever the human designer sets. The developer resolved
none.**

## Appendix C — Gaps flagged in the brief that constrain the build

- **Pages 10–14 of the GDD are image reference sheets with no extractable text** — no
  step guesses arena appearance or exact costume geometry (design-brief §0.1, §10.2).
  Proxy art stands in until M5-06.
- **Crimson Vanguard has no verified free asset (R4/§12.4)** — M1-23 uses the option-1
  Mannequin-plus-proxy-blocks fallback; a Paragon swap, if chosen (Q30), must precede
  M4 range tuning.
- **No free sound source verified (§12.6)** — M5-04; Phase 1 may ship silent (Q31);
  music unsourced.
- **Per-attack tuning floats inside GDD state ranges (Q25)** are unfilled — M2-04 adds an
  editor-time range-validation check that flags, never picks.
- **No arena footprint, range bands, or attack-D travel numbers (Q24/Q10/Q13)** — these
  interlock and are a likely early bug source; left OPEN and cross-referenced.

---

*End of build sequence. Every number remains the human designer's to approve, change,
or reject; the developer changed none and resolved none.*
