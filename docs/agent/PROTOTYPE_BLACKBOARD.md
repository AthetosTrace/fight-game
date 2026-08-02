# Ascendant Impact — Gray-box Combat Prototype Blackboard

Branch history: §1–§10 were built on `feature/graybox-combat-sandbox`; §11 onward on `feature/duel-camera-graybox`.
Scope for this run: smallest playable punch-and-damage checkpoint (per the active `/goal`), **not** the full approved Attack A AI plan (`ATTACK_A_IMPLEMENTATION_PLAN.md`), which requires `DT_VanguardAttacks` import + human sign-off (`VANGUARD_ATTACK_DATA_APPROVAL.md`) before it may begin. That plan is untouched and still gated.

## 1. Current project state (before this run)

Read from the live project via Unreal MCP:

- Third Person template foundation present and functional: `BP_ThirdPersonCharacter`, `BP_ThirdPersonPlayerController`, `BP_ThirdPersonGameMode`, Enhanced Input (`IMC_Default`, `IA_Move`, `IA_Look`, `IA_MouseLook`, `IA_Jump`).
- Manny (`SKM_Manny_Simple`) and Quinn (`SKM_Quinn_Simple`) meshes present; player character (`BP_ThirdPersonCharacter`) uses Quinn + `ABP_Unarmed`.
- `ABP_Unarmed` anim graph already contains an `AnimGraphNode_Slot 'DefaultSlot'` feeding into the ControlRig/output chain — confirmed by inspecting the AnimGraph node list, not assumed.
- Unarmed attack animations (`MM_Attack_01/02/03`, `MM_ChargedAttack`), dash (`MM_Dash`), death (`MM_Death_*`), and Rifle hit-react animations (`MM_HitReact_*`) exist as plain `AnimSequence` assets — no notifies authored, no Montage assets exist yet.
- Approved feedback assets present under `/Game/Variant_Combat/`: `UI_LifeBar` (exposes `SetLifePercentage(Percent)` and `SetBarColor(Color)` custom events), `NS_Damage` (Niagara System), `BP_CameraShake_Hit_Enemy`, `BP_CameraShake_Hit_Player`.
- No Vanguard proxy, no health/combat component, and no HUD wiring existed anywhere in the project (`HUDClass` on the GameMode was still the base engine `HUD`).
- `DT_VanguardAttacks`, `BT_CrimsonVanguard`, `BB_CrimsonVanguard` — none exist yet (full Attack A plan precondition, correctly out of scope here).

## 2. Missing-feature inventory and priority scoring

Scored on: dependency importance / Sunday-prototype value / how much is already built / implementation risk / scope penalty (higher total = do first).

| Feature | Dependency | Prototype value | Already built | Risk | Scope penalty | Priority |
|---|---|---|---|---|---|---|
| Light-attack input + animation | High | High | Input system present, just needs 1 action | Low | None (explicitly in scope) | **Selected — done** |
| Vanguard proxy + health + damage feedback | High | High | Nothing built | Low-Med (needs new BP) | None (explicitly in scope) | **Selected — done** |
| Hit detection (attack → damage once) | High | High | Nothing built | Med (array-pin/latent-node DSL quirks, resolved) | None | **Selected — done** |
| Vanguard AI state machine / Attack A telegraph loop | High (for full duel) | Low for *this* checkpoint (explicitly deferred) | Nothing built | High (BT + DataTable + notifies) | Large — explicitly out of scope this run | Deferred to next run |
| Impact Windows / Ascension Meter / Final Clash | Med | None for this checkpoint | Nothing built | High | Large — explicitly out of scope | Deferred |
| Dodge / counter | Med | None for this checkpoint | Nothing built | Med | Explicitly out of scope | Deferred |

Selection: the three "Selected" rows form one coherent smallest slice — a working input→animation→hit→damage→feedback loop — and were built together since they are mutually dependent (an attack with no target, or a target with no attack, proves nothing).

## 3. Why this feature first

The GDD's own vertical-slice definition (design-brief M1/M2 lineage) and this run's explicit target both name "one player defensive/offensive action landing on a proxy rival with visible health feedback" as the proof-of-concept that everything else (AI telegraph loops, Impact Windows, Ascension Meter) builds on top of. Building the Vanguard AI state machine first would have nothing to react to; building the attack first would have nothing to hit. They had to land in the same checkpoint.

## 4. Assets created or modified

**Created:**
- `/Game/Input/Actions/IA_Attack` — duplicated from `IA_Jump` (same Digital/bool `ValueType`).
- `/Game/Variant_Combat/Blueprints/BP_VanguardProxy` — `Character` Blueprint, mesh = `SKM_Manny_Simple`, `AnimClass` = `ABP_Unarmed` (visually distinct from the Quinn-skinned player, shares the same skeleton/DefaultSlot so hit-react montages work).
- `docs/agent/PROTOTYPE_BLACKBOARD.md` (this file).

**Modified:**
- `/Game/Input/IMC_Default` — added a mapping: `IA_Attack` → Left Mouse Button.
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter` — added `bIsAttacking` (bool) variable; added an `EnhancedInputActionIA_Attack` event (its `Triggered` exec pin wired directly into the attack logic — see §6 for why a Custom-Event indirection was abandoned) that:
  1. Guards against re-trigger while already attacking.
  2. Plays `MM_Attack_01` via `PlaySlotAnimationAsDynamicMontage` on the mesh's AnimInstance, slot `DefaultSlot` (no Montage asset had to be authored).
  3. Waits 0.3 s (approximating the swing's impact frame), then does a single `SphereOverlapActors` (110 cm radius, 120 cm in front of the actor, Pawn channel, class-filtered to `BP_VanguardProxy_C`).
  4. Calls native `ApplyDamage` (10.0, `/Script/Engine.DamageType`) on every actor found — since the overlap only fires once per attack and the array is built once, damage cannot double-apply within one swing.
  5. Waits an additional 0.5 s then clears the attacking flag.
- Vanguard proxy `EventGraph`:
  - `EventBeginPlay`: calls `EnsureHealthBarWidget()` then, if `LifeBarWidget` is valid, initializes the bar to 100%. (Originally this called `CreateWidget`+`AddToViewport` directly, then later a one-shot `GetUserWidgetObject`+cast — both superseded, see §7a and §7d.)
  - `ReceiveAnyDamage` (found via `list_events`, added via `add_event`, populated as `Game|Damage|EventAnyDamage` in the DSL): subtracts damage from `Health` (floored at 0 via `Math|Float|Max`), prints `"Vanguard Health: <value>"` to screen/log, spawns `NS_Damage` at chest height, plays `BP_CameraShake_Hit_Enemy` on the local player controller (still gated inside the `Damage > 0.0` branch), plays `MM_HitReact_Front_Med_01` via dynamic montage on `DefaultSlot`, then calls `EnsureHealthBarWidget()` again and updates the life bar under an `IsValid` guard (see §7d).
  - **`EnsureHealthBarWidget`** (new plain Function, added in §7d): if `LifeBarWidget` isn't valid, explicitly creates a `UI_LifeBar` widget, assigns it to the `HealthBarWidget` component via `SetWidget`, casts it, and stores the reference — a no-op if `LifeBarWidget` is already valid.
  - `Health` (float) default = 100 set on the class default object.
  - **`HealthBarWidget`** — new `WidgetComponent` (added after the first failed PIE test, see §7a): `Space = World`, `WidgetClass = UI_LifeBar_C`, `DrawSize = (200, 24)`, `RelativeScale3D = (0.5, 0.5, 0.5)` (≈100×12 cm physical size), `RelativeLocation = (0, 0, 220)` (attached to the capsule root, above the head), parent = `CollisionCylinder`.
- Player Blueprint: added a `Development|PrintString "Attack Triggered"` node spliced between the attack Branch's `then` pin and the `SetIsAttacking true` node (temporary debug aid, per request).
- **Level `Lvl_ThirdPerson`**: `BP_VanguardProxy` instance repositioned twice after the first failed test (see §7a) — now at `(350, 0, 288)`, facing the player start (yaw 180°). Ground height at that X was measured with `SceneTools.trace_world` (200 world units, not 210 as at the player start — the arena has a gentle staircase after roughly X=400) and the actor's Z was set to `groundZ + CapsuleHalfHeight(88)`. **This placement is still live in the open editor session only — see §7, it has not persisted to disk.**

## 5. Compile / validation results

- `BP_ThirdPersonCharacter`: `compile_blueprint(warnings_as_errors=true)` → clean, no errors or warnings.
- `BP_VanguardProxy`: `compile_blueprint(warnings_as_errors=true)` → clean, no errors or warnings.
- Confirmed via `LogBlueprint` output log entries: the two most recent compiles for both Blueprints have no `Warning:`/`Error:` lines following them (earlier lines in the log are from mid-session mistakes that were fixed — see §6).
- Assets saved to disk and confirmed via `git status` / file mtimes: `IA_Attack.uasset` (new), `IMC_Default.uasset` (modified), `BP_ThirdPersonCharacter.uasset` (modified), `BP_VanguardProxy.uasset` (new).
- After the §7a fixes: both Blueprints recompiled with `warnings_as_errors=true` a second time — still clean, zero errors/warnings. Re-saved `BP_ThirdPersonCharacter` and `BP_VanguardProxy` to disk.
- After the §7b fixes: `BP_VanguardProxy` recompiled a third time with `warnings_as_errors=true` — clean, zero errors/warnings. Re-saved to disk. `BP_ThirdPersonCharacter` untouched this round.
- After the §7d fix (LifeBarWidget Accessed-None): `BP_VanguardProxy` recompiled a fourth time with `warnings_as_errors=true` — clean, zero errors/warnings. Only `BP_VanguardProxy` saved; `BP_ThirdPersonCharacter` untouched.
- No dedicated "asset validation" MCP tool was found in the available toolsets (`list_toolsets`/`describe_toolset` surveyed); compile-with-warnings-as-errors plus the output-log check is the evidence substitute. This gap is worth a human validating with **Editor → Tools → Validate Assets** before the checkpoint is considered fully closed.

## 6. Failures and fixes (for Assignment #5 evidence)

- **`AddEvent|EnhancedInputActionIA_Attack` / `AddEvent|ReceiveAnyDamage` do not exist**: `write_graph_dsl`'s `(event Name ...)` sugar only resolves names through an internal `AddEvent|...` registry keyed by the *exact* DSL-friendly alias, and that registry does **not** include Enhanced-Input-action nodes or plain custom events already placed in the graph. Fix: use `add_event`/`create_node` to place the actual node first (discovering the enhanced-input node's real type id, `Input|EnhancedActionEvents|IA_Attack`, via `find_node_types`), then either match it in the DSL by its exact reflected name (worked for the native override `ReceiveAnyDamage`, whose reflected DSL name turned out to be `Game|Damage|EventAnyDamage`) or, when the DSL still refuses to match (true for the Enhanced Input node), fall back to wiring pins by hand with `connect_pins`.
- **Custom events cannot host latent nodes if attempted as plain Function graphs**: first attempt put the attack logic in an `add_function_graph` because a Custom Event created via the DSL wasn't matchable. That failed to compile — Blueprint Function graphs cannot contain `Delay` (latent nodes require an Event-graph-rooted context). Fix: removed the function graph, used a Custom Event instead (which does support latent nodes), then discovered Custom Events aren't discoverable as `CallFunction|Name` node types either — so the final wiring skips the Custom Event indirection entirely and connects the Enhanced Input node's `Triggered` exec pin straight into the logic chain's first node.
- **Bool member variables strip their `b` prefix in generated accessor names**: `bIsAttacking`'s getter/setter are `Variables|Default|GetIsAttacking`/`SetIsAttacking`, not `GetbIsAttacking`. Found by probing `find_node_types` with a narrower filter after the first guess failed.
- **Array-typed pins (`SphereOverlapActors`'s `ObjectTypes`) reject literal/default-value assignment outright**: compiling reported *"Array inputs...must have an input wired into them (try connecting a MakeArray node)"*. Fix: explicitly created a `Utilities|Array|MakeArray` node, connected its output to the `ObjectTypes` pin, then set the single array element's value to `ObjectTypeQuery3` (the project's default Pawn object-type channel) via `set_pin_value`.
- **Stray/duplicate nodes from abandoned attempts**: two dead-end custom-event nodes were created and left in `BP_ThirdPersonCharacter`'s EventGraph during iteration; both were found via `find_nodes`/`get_node_infos` and removed with `delete_node` before the final compile.
- **Git `dubious ownership` on every `git` invocation**: this repo's `.git` is owned by a different Windows user than the current session. Worked around per-invocation with `git -c safe.directory=... status` rather than touching global git config (per operating rules, global config is never modified).

## 7a. Failed manual PIE test #1 and fixes applied

The human ran the checkpoint in PIE and rejected it. Observed problems and root causes, found by inspecting the live Blueprint/UMG state via MCP (not by re-guessing):

1. **"A giant solid red rounded UI shape fills nearly the entire screen."** Root cause, confirmed via `UMGToolSet.GetWidgets` on `UI_LifeBar`: its root widget is an `Overlay` containing a `Border` (background) wrapping the `ProgressBar`. `EventBeginPlay` was calling `CreateWidget` + `AddToViewport` directly — `AddToViewport`'s default `CanvasPanelSlot` anchors span the full screen (0,0)–(1,1), and the `Border`'s default fill alignment stretches to match, so the widget's background rendered as a full-screen block. **Fix:** removed `CreateWidget`/`AddToViewport` from `EventBeginPlay` entirely. Added a `WidgetComponent` (`HealthBarWidget`) instead — world-space, small draw size, mounted above the Vanguard's head (see §4). `EventBeginPlay` now only fetches that component's auto-created widget instance via `GetUserWidgetObject` + `CastToUI_LifeBar` and stores the reference; nothing is ever added to the player's screen-space viewport.
2. **"The camera jumps/collides strangely while moving."** Root cause: the Vanguard proxy was originally placed only 200 cm from the player start. Capsule radii (35 + 34 = 69 cm) left very little real clearance, and the player's `CameraBoom` (`TargetArmLength = 400`, `bDoCollisionTest = true`) reacts to any nearby blocking capsule — at that distance the boom's collision probe was interacting with the Vanguard's capsule almost immediately on spawn/approach. **Fix:** moved the Vanguard to 350 cm away (see §4), clear of immediate spawn-time interference while still a short, obvious walk for testing. (Camera-boom adjustment *while standing next to the Vanguard to actually land a punch* is expected, normal SpringArm behavior, not a bug — it will still visibly react at true melee range, which is correct.)
3. **"The Vanguard proxy appears extremely close to the PlayerStart."** Same root cause and fix as #2.
4. **"Left-click does not produce an observable successful attack/damage result."** Most likely explained by #1 — a full-screen UMG widget sitting over the game viewport captures mouse focus/clicks in many UMG configurations, which would prevent `IA_Attack` (bound to Left Mouse Button) from ever reaching the game input stack. Verified independently that the input path itself is intact and unrelated to this bug:
   - `IMC_Default.defaultKeyMappings` still contains the `IA_Attack → LeftMouseButton` entry (re-checked via `ObjectTools.get_properties` after all edits — unchanged since it was added).
   - `BP_ThirdPersonPlayerController`'s `EventBeginPlay` calls `Input|AddMappingContext` on `IMC_Default` whenever `IsLocalPlayerController()` is true — confirmed present and untouched via `read_graph_dsl`, so `IA_Attack` is active at runtime through the same path as the working `IA_Move`/`IA_Jump` mappings.
   - Added a `Development|PrintString "Attack Triggered"` node on the player's attack Branch (fires the instant the input is accepted, before the montage/hit-check) so the human can now see in the PIE screen/log whether the click is reaching Blueprint logic at all, isolating "input never arrived" from "input arrived but the hit trace/damage failed."

**Diagnostic note:** I attempted to visually confirm the fix myself by starting PIE and using `EditorAppToolset.CaptureViewport`, but two capture attempts (once with an empty `captureTransform`, once with a manually-computed "behind the player" transform) both produced renders that didn't match the expected in-game view (one appeared to originate from world origin looking up through the floor; the other appeared to be extremely close to/inside a large green-highlighted capsule, with editor actor icons visible despite `bShowUI: false`). Per the two-strikes failure policy this screenshot-verification path was abandoned rather than iterated further — it looks like `CaptureViewport`'s manual `captureTransform` does not behave as simple "camera at this world pose" during `PlayMode_InViewPort` PIE, and/or still renders editor-only actor icons and selection highlights. The structural fixes above were instead verified by directly reading back the Blueprint graphs/widget tree/component properties (all confirmed in place, all Blueprints compile clean), not by trusting these screenshots. **A real human PIE pass is still required to confirm the visual/input fixes actually resolve the reported symptoms.**

## 7b. Manual PIE retest #2 (partial pass) and fixes

The human retested after §7a's fixes. **Confirmed working:** no full-screen overlay, movement fine, "Attack Triggered" prints on click, punch animation plays, "Vanguard Damaged" printed on confirmed close-range hits — i.e. the whole input → attack → overlap → `ApplyDamage` → `ReceiveAnyDamage` chain is proven functional end to end.

**Remaining issues and fixes, found by inspecting live component properties via MCP:**

1. **Spring-arm camera clips into the player at melee range.** Root cause, confirmed via `ObjectTools.get_properties`: `CameraBoom`'s `ProbeChannel` is `ECC_Camera`. The Vanguard's `CollisionCylinder` (capsule) was on the `Pawn` collision profile with only `Visibility` overridden to Ignore — `Camera` still fell back to the profile default (`Block`), so the camera probe treated the Vanguard's capsule as solid geometry once the player got close enough to attack. Its `CharacterMesh0` was on the `CharacterMesh` profile (overrides: `Pawn`/`Visibility`/`Vehicle` all Ignore) — `Camera` was **not** overridden there either, and that profile's default for `Camera` is also `Block`, so the mesh itself would still clip the camera even after fixing the capsule. **Fix:** added a `Camera → ECR_Ignore` response override to both `CollisionCylinder.bodyInstance.collisionResponses` and `CharacterMesh0.bodyInstance.collisionResponses`, keeping every other channel/response (and the `Pawn`/`CharacterMesh` profiles themselves) untouched. Pawn-vs-pawn blocking (movement collision) and the attack's `SphereOverlapActors` (which queries the `Pawn` **object type**, unrelated to trace-channel responses) are both unaffected — verified by re-reading the full `bodyInstance` back after the edit.
2. **Health bar not clearly visible/readable.** The `HealthBarWidget` `WidgetComponent` was `Space = World` at `DrawSize 200×24` scaled to `0.5` (≈100×12 world cm) — small and, since it doesn't billboard, often edge-on or foreshortened relative to the camera. **Fix:** switched `Space` to `Screen` (still a `WidgetComponent`, never `AddToViewport` — it projects only at the actor's own screen position, not full-screen) and reset `DrawSize` to `150×20` px / `RelativeScale3D` to `(1,1,1)` (screen-space widgets size in screen pixels, not world units, so the old world-space scale hack no longer applies). It stays anchored above the Vanguard's head (`RelativeLocation.Z = 220`, unchanged) and now always faces the camera by construction.
3. **Damage debug output didn't show the actual number.** `EventAnyDamage`'s `PrintString` said `"Vanguard Damaged"`. **Fix:** rewrote it to build `"Vanguard Health: " + ToString(newHealth)` via `Utilities|String|Append` + `Utilities|String|ToString(Float)`, so each landed hit now prints the exact resulting health value (e.g. `"Vanguard Health: 90.0"`), giving direct visible proof of the exact −10-per-swing decrement.
4. **`NS_Damage` spawn point too low/obscured.** It was spawning at `GetActorLocation()` — the capsule's own origin, which sits low on the body. **Fix:** now spawns at `GetActorLocation() + (0, 0, 80)`, roughly chest height, clear of the lower body/ground clutter.
5. **Hit-reaction montage slot check.** Re-confirmed (not changed in logic) that `ABP_Unarmed`'s `AnimGraph` has a real `AnimGraphNode_Slot 'DefaultSlot'` feeding the output chain (same check as §1's original finding — the Vanguard uses this same AnimBP), and that `PlaySlotAnimationAsDynamicMontage(..., SlotNodeName="DefaultSlot", ...)` is still called unconditionally inside the `Damage > 0.0` branch, immediately after the camera shake. Tightened `BlendInTime` from `0.1` → `0.05` so the reaction reads a little snappier/more visible.

Only `BP_VanguardProxy` was touched this round (no changes needed in `BP_ThirdPersonCharacter`). Recompiled with `warnings_as_errors=true` — clean, zero errors/warnings. Re-saved to disk.

## 7c. Manual PIE retest #3 (passed, with two follow-ups) and level-save blocker resolved

The human ran retest #3 after the §7b fixes.

**Confirmed working:**
- Normal movement and camera.
- Camera remains stable at melee range (the §7b `Camera → Ignore` collision-response fix holds).
- Left-click triggers the punch animation.
- Vanguard receives exactly 10 damage per landed swing.
- Debug health values visibly progressed 90 → 80 → 70 and continued down to 0 (direct, exact confirmation of the per-swing damage amount and that it never double-applies).
- Chest-height `NS_Damage` VFX and the Vanguard hit-reaction animation were visible.
- The Vanguard proxy's level placement is now **persisted to disk** — the human pressed Ctrl+S per the standing instruction, and `git status` now shows a new untracked external-actor package (`Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/3/I5/`) alongside the (still-unchanged) `Lvl_ThirdPerson.umap`, exactly the OFPA behavior anticipated in this section. **The manual save blocker below is therefore resolved as of this retest — no more Ctrl+S reminder is needed for this actor.**

**Not yet confirmed (carried forward as open items, not failures of this checkpoint):**
1. **Health-bar widget visibility.** The screen-space `HealthBarWidget` from §7b was not clearly visible in the human's recording, despite the exact health values being independently confirmed via the debug `PrintString`. This needs a follow-up pass (e.g. checking actual screen position/anchor behavior of a `Screen`-space `WidgetComponent`, contrast/size, or whether it's being drawn behind other UI) before the life bar itself can be called "confirmed working" — the *data* driving it (`Health`, `SetLifePercentage`) is proven correct even though the *readable on-screen bar* is not yet proven visible.
2. **Vanguard death behavior at 0 health.** Not implemented — this was explicitly out of scope for this checkpoint (see the original `/goal` scope: only "Vanguard health visibly decreases," not defeat/death handling). Health correctly floors at 0 (confirmed by the debug progression reaching 0) but nothing currently happens when it gets there (no death animation, no disabling collision, no win condition). This is expected, correctly-deferred behavior, not a bug — it belongs with a later milestone (win/loss handling).

No Unreal assets, Blueprints, or debug nodes were touched to produce this update — this section only records the human's retest #3 report.

## 7d. Runtime error found in Message Log and fix (LifeBarWidget Accessed-None)

After retest #3, the Unreal Message Log showed a repeated runtime error during PIE:

> `Accessed None trying to read property LifeBarWidget` — Blueprint: `BP_VanguardProxy`, Node: `Set Life Percentage`

**Diagnosis (root cause, confirmed by reading the actual graph back, not guessed):** `EventBeginPlay` computed `LifeBarWidget` in one shot — `GetUserWidgetObject` on the `HealthBarWidget` component, cast to `UI_LifeBar_C`, store — with no failure handling. `UWidgetComponent::GetUserWidgetObject()` only returns a non-null widget if the component has already internally initialized one; it does **not** lazily create it on demand. If that internal initialization hadn't happened yet at the moment the actor's own `EventBeginPlay` ran (component initialization order isn't guaranteed to have completed a full widget construction by then), `GetUserWidgetObject` silently returned `None`, `CastToUI_LifeBar(None)` silently returned `None` too (casting `None` never fails loudly, it just produces `None`), and `LifeBarWidget` was permanently set to `None` for the rest of the actor's life — every subsequent `ReceiveAnyDamage` then called `SetLifePercentage` on a `None` object, producing this error on **every landed hit**, which matches what the Message Log showed (repeated, not one-off).

**Fix — explicit initialization instead of relying on lazy auto-creation, plus a safe reacquire/guard:**
- Added a new plain Blueprint function, **`EnsureHealthBarWidget`** (no latent nodes, so — unlike the very first attempt in §6 — a plain Function graph is fine here): if `LifeBarWidget` is not valid, it explicitly calls `CreateWidget(Class=UI_LifeBar_C, OwningPlayer=GetPlayerController(0))`, casts the result to `UI_LifeBar_C`, calls `HealthBarWidget.SetWidget(...)` to explicitly assign that exact widget instance to the component (this is the "explicitly initialize the WidgetComponent" step — it no longer depends on the component's own implicit lazy-init timing at all), and stores the cast result in `LifeBarWidget`. If `LifeBarWidget` is already valid, the function is a no-op.
- `EventBeginPlay` now just calls `EnsureHealthBarWidget()`, then an `IsValid` guard around the initial `SetLifePercentage(1.0)` call.
- `ReceiveAnyDamage` now calls `EnsureHealthBarWidget()` again right before updating the bar (the "reacquire it safely" requirement — if `LifeBarWidget` somehow went invalid or was never set, this call fixes it in place before use, at negligible cost when it's already valid), and the `SetLifePercentage` call for the damage update is itself wrapped in an `IsValid` guard as a final safety net — if the widget is still somehow invalid after the reacquire attempt, the health-bar update is silently skipped for that one hit instead of throwing an Accessed-None error. All other effects (health value, debug print, VFX, camera shake, hit-reaction montage) do not depend on `LifeBarWidget` and are unaffected either way.
- `AddToViewport` is still never used anywhere in this Blueprint (confirmed via `read_graph_dsl`); the health bar remains a small, actor-attached, screen-space `WidgetComponent` as established in §7b.
- Recompiled `BP_VanguardProxy` with `warnings_as_errors=true` — clean, zero errors/warnings. Only `BP_VanguardProxy` was saved; nothing else was touched.

## 7e. Manual PIE retest #4 (LifeBarWidget fix confirmed) and giant-oval health-bar bug

**Confirmed working after the §7d fix:** attacks/damage still function, no more Accessed-None errors — the health widget now successfully calls `SetLifePercentage` every hit, and the human visually confirmed the red fill portion decreasing.

**Remaining bug:** the actor-attached health bar rendered as an enormous red-and-black circular/oval shape covering most of the viewport, instead of a small horizontal bar above the Vanguard's head.

**Diagnosis (found by directly inspecting the live component instance, not guessed):**
- First checked `UI_LifeBar`'s widget hierarchy via `UMGToolSet.GetWidgetDescription`: `Overlay_0 → Border_0 (RoundedBox, HAlign/VAlign Fill, no SizeBox, no explicit width/height) → Bar (ProgressBar, RoundedBox fill, red)`. **No hardcoded size, anchor, or render-transform issue exists in the widget asset itself** — a `Fill`-aligned `Border` with no `SizeBox` correctly takes on whatever size its container (the `WidgetComponent`'s render target) gives it, which is exactly the desired behavior. `UI_LifeBar` was not modified.
- Then checked the `HealthBarWidget` **component's class defaults** (`BP_VanguardProxy_C:HealthBarWidget_GEN_VARIABLE`) via `ObjectTools.get_properties`: `Space=Screen`, `DrawSize=(150,20)`, `bDrawAtDesiredSize=false`, `WidgetClass=UI_LifeBar_C` — all correct, exactly as set in §7b.
- Then checked the **live level actor instance's** `HealthBarWidget` component directly (`.../PersistentLevel.BP_VanguardProxy_C_UAID_...HealthBarWidget`) — and found it was completely stale: `Space=World`, `DrawSize=(500,500)` (Unreal's raw engine default for a brand-new `WidgetComponent`), `WidgetClass=None`, `RelativeLocation=(0,0,0)`. This placed actor had been in the level since *before* the `HealthBarWidget` component was added to the Blueprint class (all the way back in the first checkpoint pass) — its per-instance component data was captured at the moment the component was first added, before any of the §7b/§7c property fixes were ever applied to the class, and that stale snapshot was never refreshed. The giant red/black oval was Unreal's fallback rendering for a `WidgetComponent` with `WidgetClass=None`, rendered at the raw 500×500 default in `World` space at the actor's feet — not `UI_LifeBar` at all.
- Confirmed this diagnosis directly: `ObjectTools.set_properties` on the live instance only partially applied (`Space`/`RelativeScale3D` took, `DrawSize`/`WidgetClass`/`RelativeLocation` silently reverted back to the stale snapshot on the next read), and `ObjectTools.reset_properties` on the same properties reverted **everything** back to the identical stale snapshot — confirming a frozen per-instance component-data cache was overriding both direct edits and "reset to default," rather than either genuinely re-syncing to the current class archetype.

**Fix:** removed the stale placed actor (`SceneTools.remove_from_scene`) and re-added a fresh `BP_VanguardProxy` instance at the same transform (`SceneTools.add_to_scene_from_asset`, `(350, 0, 288)`, yaw 180°) — a newly-spawned instance has no stale per-instance component cache and inherits the component straight from the (correct) class defaults. Verified immediately: the new instance's `HealthBarWidget` reads `Space=Screen`, `DrawSize=(150,20)`, `bDrawAtDesiredSize=false`, `WidgetClass=UI_LifeBar_C`, `RelativeLocation=(0,0,220)` — exactly the intended small, screen-space, actor-attached, non-full-screen configuration. No changes were made to `UI_LifeBar` or to any Blueprint graph logic this round (the percentage-update logic from §7d is untouched and preserved). `WidgetComponent`s are non-interactive/cannot capture game input by default (they only receive input if explicitly configured for it, which this one never was), and `AddToViewport` is still never used anywhere in the project.
- `BP_VanguardProxy` recompiled with `warnings_as_errors=true` — clean (no logic changed, this was a pure level-content fix). No Blueprint asset needed saving this round.
- **Level save note:** the new actor instance has the same OFPA save limitation documented in §7 — `SceneTools.save_actor(...)` on it failed with the same *"Asset does not exist"* error as before, since it's a brand-new external-actor package. **A human Ctrl+S in the editor is required again** to persist this replacement actor (the level in memory is correct right now for PIE testing; only the on-disk copy needs the manual save). The old actor's now-orphaned external-actor package file may remain on disk as an inert leftover until the next proper level save cleans it up — this is expected OFPA behavior, not something to hand-delete.

## 7. Manual actions required — active again (new actor replaced in §7e)

`Lvl_ThirdPerson` uses One-File-Per-Actor (OFPA) — its `__ExternalActors__` folder holds every actor as its own package. Saving a *new* actor to disk has never been possible through the available MCP tools (`AssetTools.save_assets` on the level package is a no-op for new actors; `SceneTools.save_actor` on the actor directly fails with *"Asset does not exist"* for a package that hasn't been created by a full editor "Save Level" pass yet) — this was true for the original placement (resolved once via human Ctrl+S after retest #3) and is true again now that §7e replaced that actor with a fresh instance (new GUID, new external package, never yet saved).

**A human Ctrl+S in the editor is required once more** to persist the current (fixed) Vanguard proxy placement. The actor is correct and live in the currently-open editor session right now, so PIE testing works immediately without this step — it only matters for keeping the placement across an editor restart. The previous placement's now-orphaned external-actor package (`Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/3/I5/...`) may remain on disk as an inert leftover until the next proper level save cleans it up; it is not referenced by the level anymore and was not hand-deleted (per the rule against filesystem-editing `.uasset` files).

## 8. Next recommended step

With the punch-and-damage loop proven (including retest #3's exact-damage confirmation), two small open items from §7c are worth closing before or alongside the next milestone:
- Make the `HealthBarWidget` reliably visible on screen (its underlying data is already proven correct).
- Decide, with the human designer, when/how Vanguard death-at-zero-health should be handled — correctly out of scope for this checkpoint, but likely needed before or during the next milestone below.

Beyond that, the next-smallest slice toward the Sunday goal is **M2 from `ATTACK_A_IMPLEMENTATION_PLAN.md`**: the six-state Vanguard state machine (`BT_CrimsonVanguard`/`BB_CrimsonVanguard`) driving Attack A's Telegraph → Active Attack → Recover → Return-to-Neutral loop — but that plan is explicitly gated on the `DT_VanguardAttacks` import and `VANGUARD_ATTACK_DATA_APPROVAL.md` sign-off, neither of which this run touched. Confirm those preconditions with the human designer before starting it.

## 9. Assignment #5 evidence summary

- **Found missing**: everything needed for a punch-and-damage loop — no attack input, no Vanguard proxy/health, no hit detection, no HUD wiring — while the movement/camera/feedback-asset foundation was already solid.
- **Selected**: the smallest coherent slice that makes "the player can land a hit and see the rival's health drop" true, per the scoring table in §2.
- **Generated**: 1 new Input Action, 1 modified Input Mapping Context, 1 new Character Blueprint (Vanguard proxy) with health/damage/feedback logic, 1 modified player Blueprint with attack input/animation/hit-detection logic, 1 level actor placement (now persisted to disk, see §7c).
- **Compiled**: yes — both Blueprints compile with zero errors and zero warnings (`warnings_as_errors=true`).
- **Human PIE test**: attempt #1 failed (full-screen UI overlay, camera jitter from too-close spawn, no observable attack result — see §7a). Attempt #2 partially passed — the whole input→attack→damage chain proven working, but camera clipping, health-bar readability, VFX placement, and exact-health proof still needed fixes (see §7b). **Attempt #3 passed** — camera stable at melee range, exactly 10 damage per swing directly confirmed via the debug health readout (90→80→70→...→0), chest-height VFX and hit-reaction visible, and the Vanguard's level placement is now persisted to disk (see §7c). Two follow-up items remain open (not failures of this checkpoint): the health-bar widget's on-screen visibility needs a further pass, and Vanguard death-at-zero-health behavior is correctly unimplemented/deferred to a later milestone.

---

## 10. Milestone 2 — Crimson Vanguard Attack A data prep

**Scope of this run (per the active `/goal`):** verify the approved Attack A data, create the smallest Blueprint-friendly struct + `DataTable` for exactly four Vanguard attacks (A enabled, B–D disabled placeholders), and stop — no Behavior Tree, no AI Controller, no damage-to-player logic, no extra attacks. This is a data-prep step only.

### 10.1 Approved source verified

Read from `C:\Users\Tonys ProArt\Documents\fight-game` (not guessed):

- `docs/unreal/ATTACK_DATA_SOURCE_AUDIT.md` — establishes that only the four attacks' qualitative range/purpose/readability facts are GDD-governed; every numeric value (damage, min/max range, cooldown, Attack D max travel distance) and every asset reference (montage, VFX, audio, hit-trace socket) is explicitly **OPEN** and must stay blank — inventing any of them is forbidden.
- `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md` — **signed**: "APPROVED" checked, Tony Travieso, 2026-07-29. This authorizes exactly one thing: proceeding to the manual/CSV-driven Unreal DataTable import steps in `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`. It does **not** authorize the Behavior Tree, damage-to-player logic, or resolving any OPEN value.
- `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` — the approved schema (question 3 of the approval packet explicitly approves this contract, not `design-brief.md` §5.3's more speculative numeric struct). 17 columns; the first (`Name`) is the DataTable's row-name key, not a struct field.
- `data/unreal/DT_VanguardAttacks.csv` — the actual approved data: exactly 4 rows (`Row_A/B/C/D`), `AttackId` A–D, only `Row_A.EnabledForSelection = true` (`Prototype`), `Row_B/C/D.EnabledForSelection = false` (`Planned`). `MontageAsset`/`TelegraphVfxAsset`/`TelegraphAudioAsset`/`HitTraceSocket` are blank on every row, exactly as required.
- `design-brief.md` §5.3's `S_VanguardAttackDef` (with numeric `MinRange`/`Damage`/`Cooldown`/`Phase1`/`Phase2` tuning fields) is the **later**, forward-looking gameplay struct for once those numbers are actually approved — it is explicitly not what's approved for import right now (every one of those numeric fields is listed OPEN in the source audit). Building it now would mean inventing values. **Not built this pass — noted as future work in §10.4.**

### 10.2 Existing-asset inventory (nothing to reuse)

Confirmed via `AssetTools.find_assets` and `DataTableTools.search_row_structs` — none of the following exist anywhere in the project: `S_VanguardAttackDef` (or any struct matching `*Vanguard*`), `DT_VanguardAttacks`, `BT_CrimsonVanguard`, `BB_CrimsonVanguard`, or any `E_VanguardAttackID`/`E_VanguardState` enum. The only pre-existing `*Vanguard*` asset is `BP_VanguardProxy` (the gray-box proxy Character from the combat checkpoint, §4 — unrelated to attack data, not touched this run). Created `/Game/AscendantImpact/Data/` (the folder `design-brief.md` §2 specifies for this content) — empty, ready to receive the struct and table.

### 10.3 Genuine manual blocker — creating the row struct

**No tool in any available MCP toolset can create a new `UserDefinedStruct` (Blueprint Structure) or a new `UserDefinedEnum` asset.** Confirmed by reviewing every registered toolset (`list_toolsets` — no struct/enum toolset exists) and every tool on the closest candidates:
- `DataTableTools.create` / `.import_file` both **require** an existing struct asset as their `schema` argument — they cannot create one.
- `BlueprintTools.add_variable`/`add_struct_variable` add a variable *to a Blueprint*, not a field *inside* a struct asset — `add_variable`'s `blueprint` argument is typed to `/Script/Engine.Blueprint`, which a `UserDefinedStruct` is not.
- `DataAssetTools.create` makes `DataAsset` instances from an existing class, not struct definitions.
- `search_row_structs` confirms no existing struct (native or user-defined) matches; only irrelevant engine structs exist (`GameplayTagTableRow`, `MirrorTableRow`, etc.).

A `UserDefinedStruct`'s field list lives in editor-only data (`FStructureEditorUtils`) that isn't exposed as a plain settable property, so `ObjectTools.set_properties` cannot touch it either. The only way to author one is the editor's own Blueprint Structure editor UI. I deliberately did **not** attempt this through `SlateInspectorToolset`'s low-level UI-automation — reliably adding 16 typed fields through raw Slate click/type events has a high chance of an unreliable, hard-to-verify result for a lot of tool calls, which is exactly the kind of rabbit hole the operating rules say to stop and ask about rather than push through. This is a genuine one-time manual gate, not a failure of implementation effort — everything downstream (the `DataTable` itself, the CSV import, row verification, compile) is fully scriptable via MCP once the struct exists, and will be done in the very next pass.

Per the "smallest Blueprint-friendly structure" instruction, the struct is intentionally flat — no `E_VanguardAttackID` enum, no nested `S_AttackPhaseTuning` (those are `design-brief.md`'s later, numeric-tuning-bearing design; premature here since every number they'd carry is OPEN). `AttackId` is a plain string, matching the row contract's own description of it as an "enum-like string" checked by exact string comparison, not a native enum. The three asset-reference fields (`MontageAsset`/`TelegraphVfxAsset`/`TelegraphAudioAsset`) are typed as plain `String` rather than typed Soft Object References for the same reason — they are guaranteed blank in every row this pass, so the stronger typing has zero present value and only adds friction to the one-time manual step; §10.4 flags upgrading them once real assets exist.

**Manual step required — create exactly this struct, then hand back to continue:**

1. In the Content Browser, navigate to `/Game/AscendantImpact/Data/` (already created).
2. Right-click → search "Blueprint Structure" (some UE versions file it under **Miscellaneous**, some under **Blueprints** — the create-asset menu's search box finds it either way) → create it.
3. Name it exactly **`S_VanguardAttackDef`**.
4. Open it and add exactly these 16 variables (name, type — in this order, matching `VANGUARD_ATTACK_ROW_CONTRACT.md` §2 minus its `Name` row-key column):

   | # | Field name | Type |
   |---|---|---|
   | 1 | `AttackId` | String |
   | 2 | `DisplayWorkingName` | String |
   | 3 | `ImplementationStatus` | String |
   | 4 | `EnabledForSelection` | Boolean |
   | 5 | `IntendedRange` | String |
   | 6 | `GameplayPurpose` | String |
   | 7 | `TelegraphRequirement` | String |
   | 8 | `TrackingRule` | String |
   | 9 | `ActiveDescription` | String |
   | 10 | `RecoveryRequirement` | String |
   | 11 | `Phase2Usage` | String |
   | 12 | `MontageAsset` | String |
   | 13 | `TelegraphVfxAsset` | String |
   | 14 | `TelegraphAudioAsset` | String |
   | 15 | `HitTraceSocket` | Name |
   | 16 | `Notes` | String |

5. Save (`Ctrl+S`) the struct asset.
6. Report back — the next pass will create `DT_VanguardAttacks` against this struct, import the approved CSV (`data/unreal/DT_VanguardAttacks.csv`) verbatim (no hand-retyping), verify all four rows and that only `Row_A` is enabled, and compile/validate.

### 10.4 Deferred / future work (not this pass)

- Upgrade `MontageAsset`/`TelegraphVfxAsset`/`TelegraphAudioAsset` from `String` to proper typed Soft Object References once real assets are chosen and these fields actually get populated.
- The numeric gameplay-tuning struct (`design-brief.md` §5.3's fuller `S_VanguardAttackDef` with `MinRange`/`Damage`/`Cooldown`/`Phase1`/`Phase2`) once the designer resolves the OPEN values (§14 Q3/Q10/Q12/Q13/Q25) — this bridge struct is deliberately not that struct.
- `E_VanguardAttackID` / `E_VanguardState` enums, `BB_CrimsonVanguard`, `BT_CrimsonVanguard`, `BP_VanguardController` — all explicitly out of scope for this pass; tracked in `ATTACK_A_IMPLEMENTATION_PLAN.md` M2.
- No combat-checkpoint asset (`BP_ThirdPersonCharacter`, `BP_VanguardProxy`, `IMC_Default`, `IA_Attack`) was touched this run.

---

## Manual PIE test instructions (retest #3, after fixes in §7b)

1. In the already-open Unreal Editor, press **Play** (Alt+P) to start PIE in the `Lvl_ThirdPerson` map.
2. Confirm the screen is normal on entering PIE — no full-screen overlay.
3. Confirm normal Third-Person movement (WASD + mouse look) works smoothly.
4. Walk toward the Vanguard proxy mannequin and get close enough to throw a punch (melee range). **Confirm the camera no longer clips/goes black or shows interior geometry as you close the distance** — it should stay smoothly behind the player.
5. Confirm the Vanguard's health readout (small screen-space bar anchored above its head) is clearly visible and readable now that you're close to it.
6. Left-click (or press the mapped `IA_Attack` key — Left Mouse Button) to throw a light attack. Confirm:
   - **"Attack Triggered"** prints on click.
   - The punch animation plays once per click, no spamming mid-swing.
   - On a confirmed close-range hit: the debug print now reads **"Vanguard Health: 90.0"** (then 80.0, 70.0, ...) — read the exact number each swing to confirm it drops by exactly 10 and never double-applies.
   - The health bar visibly drops to match.
   - `NS_Damage` sparks are now visibly at chest height on the Vanguard, not obscured near its feet.
   - The camera shake fires only at the instant of this confirmed hit (not before, not continuously, not on a miss).
   - The Vanguard visibly plays its hit-reaction animation on every confirmed hit.
   - Clicking out of range should show "Attack Triggered" but no health-drop message — that's correct.
7. Stop PIE (Esc or the Stop button).
8. **Press Ctrl+S to save the level** if you want the Vanguard proxy placement/component changes to persist after closing the editor (see §7 — this is a required manual step; it is not automated).

The two temporary debug `PrintString` nodes ("Attack Triggered", "Vanguard Health: X") are intentionally left in for this retest so the exact per-swing damage value is directly readable. Remove them once the loop is fully confirmed, on request.

---

## 11. Milestone 3 — Duel Camera graybox first pass (2026-08-01/02, branch `feature/duel-camera-graybox`)

**Scope delivered:** first visually playable 2.5D duel camera slice per the approved camera-first milestone — stable side-profile camera, midpoint tracking, separation-based distance, arena-relative movement with a clamped depth lane, mutual fighter facing, mouse free-look disabled. Blueprint-only (decision of 2026-08-01 honored). No dominance bias, hit-driven camera moves, or cinematics (explicitly deferred). No combat logic was expanded, redesigned, or removed.

### 11.1 Architecture chosen and why

A **runtime-spawned camera rig actor** (`BP_DuelCameraRig`), spawned by the existing `BP_ThirdPersonPlayerController` at BeginPlay and made the view target via `SetViewTargetWithBlend`. Chosen because:

- No new level actor means no OFPA "human must Ctrl+S" blocker (the §7 problem) and no stale-per-instance-data risk (§7e problem). Nothing in `Lvl_ThirdPerson` was placed or modified this pass.
- The original third-person camera (`CameraBoom`/`FollowCamera` on the player) is **bypassed, not removed** — the rig simply becomes the view target. Setting the controller's new `bEnableDuelCamera` bool to false restores stock behavior entirely (spawn + view-target switch + duel movement mode are all gated on it).
- Movement became arena-relative with **zero changes to the `Move` function**: the rig pins the controller's control rotation each tick to the yaw perpendicular to the combat axis (pointing from the camera side into the lane), so the template's existing control-rotation-relative movement math *is* arena-relative while the rig runs. W/S = depth, A/D = along the combat axis, always screen-correct for the configured camera side.

Combat axis for this level: **world X** (PlayerStart at (0,0,302) yaw 0; Vanguard placed at (350,0,288) yaw 180). Depth = world Y, lane centered on Y=0.

### 11.2 Assets created / modified (exact Git manifest)

**Created:**
- `Content/AscendantImpact/Camera/BP_DuelCameraRig.uasset` — Actor Blueprint, root scene component + `DuelCamera` (`CameraComponent`, FOV **55**, Perspective projection — the only component-template edit).

**Modified:**
- `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` — added bool `bDuelModeActive` (category "Duel Camera"); added function `SetDuelMovementMode(bActive)`; inserted a Branch gate in `Aim` (mouse look). Nothing else touched — `Move`, the attack chain, and `bIsAttacking` logic are untouched.
- `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` — added `bEnableDuelCamera` (bool, instance-editable, default **true**) and `DuelCameraRig` (object ref) in category "Duel Camera"; BeginPlay's existing Sequence node got a **third output pin** (existing wiring untouched): `then_2 → Branch(bEnableDuelCamera) → SpawnActor BP_DuelCameraRig (identity transform via MakeTransform) → Set DuelCameraRig → SetViewTargetWithBlend(rig, BlendTime 0.75)`.
- `docs/agent/PROTOTYPE_BLACKBOARD.md` — this section.

**Explicitly not touched:** `BP_VanguardProxy`, `IA_Attack`, `IMC_Default`, `IMC_MouseLook`, `UI_LifeBar`, all `/Game/Variant_Combat/` feedback assets, `Lvl_ThirdPerson` and its external actors, `Config/DefaultEditorPerProjectUserSettings.ini` (personal config, left unstaged).

### 11.3 BP_DuelCameraRig — functions, events, variables

**Event graph:** `EventTick(DeltaSeconds)` → `ResolveFighters()` → nested IsValid guards on both fighter refs (fail-safe: if either is missing this tick, nothing runs, no errors) → one-shot `ActivateDuelMode()` (guarded by `bDuelActivated`) → `UpdateDuelCamera(DeltaSeconds)`.

**Functions (all plain function graphs, no latent nodes):**
- `ResolveFighters()` — calls `ResolvePlayer()` + `ResolveVanguard()`. Each early-outs when its ref is already valid, so **no global searches happen after initialization** (`GetPlayerPawn`/`GetActorOfClass` run only while a ref is unresolved).
- `ResolvePlayer()` — `GetPlayerPawn(0)` → cast `BP_ThirdPersonCharacter` → store `PlayerFighter`.
- `ResolveVanguard()` — `GetActorOfClass(BP_VanguardProxy_C)` → store `VanguardFighter`; if none found and `bAutoSpawnVanguard` and the player is valid, spawns one at player location + (VanguardSpawnDistance, 0, 0) (fallback only — never triggers in `Lvl_ThirdPerson`, which already has the placed Vanguard; fallback spawn offset assumes CombatAxisYaw near 0, documented limitation).
- `ActivateDuelMode()` — calls player's `SetDuelMovementMode(true)` (sets `bDuelModeActive`, sets `CharacterMovement.bOrientRotationToMovement = false` so facing control doesn't fight movement orientation); snaps `SmoothedMidpoint`/`SmoothedDistance` to current values (no first-frame lurch); sets `bDuelActivated`.
- `UpdateDuelCamera(DeltaSeconds)` — per tick:
  1. Midpoint = (P+V)/2 (component-wise); separation = 2D distance (XY).
  2. Desired distance = clamp(BaseCameraDistance + separation × DistancePerSeparation, Min, Max) — clamps done with `select` ternaries.
  3. `VInterpTo`/`FInterpTo` smooth midpoint and distance into `SmoothedMidpoint`/`SmoothedDistance`.
  4. Camera offset yaw = CombatAxisYaw + CameraSideSign × (90 − SideAngleDegrees) → camera position = smoothed midpoint + offset dir × smoothed distance, raised by CameraHeightOffset; rotation = `FindLookAtRotation` to midpoint + LookHeightOffset (slight down-pitch, **roll always 0**, no orbit possible — one fixed side of the axis by construction, no live crossing).
  5. `SetControlRotation(yaw = CombatAxisYaw − CameraSideSign × 90)` on the player controller every tick — pins movement axes (this is what makes `Move` arena-relative and also neutralizes any residual look input).
  6. Player depth clamp: world Y clamped to DepthLaneCenter ± DepthLaneHalfWidth via `SetActorLocation` (X/Z untouched).
  7. Facing: both fighters `RInterpTo` yaw-only toward each other (`SetActorRotation`, yaw only — pitch/roll untouched; does not touch animation, montages, collision, or damage handling).

**Exposed tuning variables (all instance-editable, ALL VALUES PROVISIONAL):**

| Category | Variable | Default | Meaning |
|---|---|---|---|
| Targets | `bAutoSpawnVanguard` | true | Spawn fallback Vanguard if none in level |
| Targets | `VanguardSpawnDistance` | 350 | Fallback spawn offset (cm, +X) |
| Combat Axis | `CombatAxisYaw` | 0 | Combat axis yaw (0 = world X) |
| Combat Axis | `CameraSideSign` | **+1** | Which side of the axis the camera sits (+1 = +Y side → player appears screen-left; −1 mirrors) |
| Framing | `SideAngleDegrees` | 12 | Degrees off perfectly-flat side profile (spec range 5–20) |
| Framing | `CameraHeightOffset` | 60 | Camera height above fighter midpoint (≈ chest/eye line) |
| Framing | `LookHeightOffset` | 20 | Look-target height above midpoint (creates slight down-angle) |
| Distance | `BaseCameraDistance` | 450 | Distance at zero separation |
| Distance | `DistancePerSeparation` | 0.6 | Extra distance per cm of fighter separation |
| Distance | `MinCameraDistance` | 500 | Distance floor |
| Distance | `MaxCameraDistance` | 900 | Distance ceiling |
| Smoothing | `MidpointInterpSpeed` | 5 | Midpoint tracking speed |
| Smoothing | `DistanceInterpSpeed` | 3 | Zoom response speed |
| Smoothing | `FacingInterpSpeed` | 8 | Fighter turn-to-face speed |
| Movement Constraints | `DepthLaneCenter` | 0 | Lane center (world Y) |
| Movement Constraints | `DepthLaneHalfWidth` | 180 | Max depth excursion each way (cm) |

Internal (not editable): `PlayerFighter`, `VanguardFighter`, `SmoothedMidpoint`, `SmoothedDistance`, `bDuelActivated`. Camera FOV 55 lives on the `DuelCamera` component template. A `bShowDebug` var was added then removed (no debug path was implemented; a dead toggle would mislead).

### 11.4 Compile & save results

- `BP_DuelCameraRig`, `BP_ThirdPersonCharacter`, `BP_ThirdPersonPlayerController`: all `compile_blueprint(warnings_as_errors=true)` → **clean** (final pass ran all three back-to-back).
- All three saved to disk via `AssetTools.save_assets`; git confirms exactly the three expected content changes + docs.
- One transient compile failure during authoring (fixed): `SpawnActorFromClass` requires `SpawnTransform` to be **wired** (by-ref pin) — literal defaults are not accepted; fed it a `MakeTransform` node. Same gotcha family as the MakeArray rule.
- No MCP asset-validation tool exists (unchanged from §5); recommend the human run **Tools → Validate Assets** on the three Blueprints for final sign-off.

### 11.5 Tool-assisted validation (evidence, PIE via MCP)

Two full PIE sessions were started/stopped via `EditorAppToolset.StartPIE/StopPIE`, and runtime state was read from the live PIE world (`UEDPIE_0_` actors) via MCP:

- **Duel Camera becomes the active view:** `PlayerCameraManager`'s transform was identical to the rig's transform (session 1: pos (312.3, −645.7, 361.1) yaw 102°; session 2 after side flip: (312.3, +645.7, 361.1) yaw −102°). Blend-in from `SetViewTargetWithBlend(0.75s)`.
- **Both fighters resolve:** `PlayerFighter` → PIE player pawn, `VanguardFighter` → the existing placed Vanguard (fallback spawn correctly did NOT trigger).
- **Activation:** `bDuelActivated=true`, player `bDuelModeActive=true`, player `bOrientRotationToMovement=false`, controller `DuelCameraRig` ref set.
- **Midpoint + distance math:** `SmoothedMidpoint` (175, 0, 301) = exact midpoint of the two fighters; `SmoothedDistance` 660.1 = exactly clamp(450 + 350×0.6, 500, 900) for the 350 cm spawn separation.
- **Stable side / no roll:** camera roll ~0 (1e-8), fixed side (sign of Y offset matches `CameraSideSign` in both sessions; flipping the default mirrored it exactly).
- **Fighters face each other:** at rest, player yaw 0 (toward Vanguard at +X), Vanguard yaw 180 (toward player).
- **No runtime errors:** output-log sweep for `Accessed None` / Blueprint runtime errors during both PIE sessions → zero hits (only the three already-fixed authoring-time tool errors appear, timestamped before PIE).
- **Visual check:** `CaptureEditorImage` screenshots (kept in the session scratchpad, deliberately not committed) show clean side-profile framing, both fighters fully readable, player screen-left / Vanguard screen-right after the side flip.
- `CaptureViewport` now requires `captureTransform` even for a current-view capture (tool schema quirk); `CaptureEditorImage` is the reliable capture path during PIE.
- **Side default flipped after session 1:** with `CameraSideSign=-1` the player read as the right-side fighter; flipped default to `+1` for fighting-game convention (player left). One CDO float, re-verified in PIE session 2.

### 11.6 PENDING HUMAN PIE (not claimable via tools)

- Feel of midpoint tracking / zoom smoothing while actually moving (interp speeds are provisional).
- A/D actually closes/retreats and reads screen-correct; W/S depth feel and the ±180 lane clamp behavior at the boundary (clamp is positional — expect a firm invisible wall, not a soft push).
- Mouse movement does nothing (free-look gated + control rotation pinned) — verify no residual camera twitch.
- Punch loop regression: LMB attack, damage prints, health bar, VFX, hit-react all still work at melee range under the new camera (logic untouched, but the new camera angle changes what you see; also strafing animation will look like forward-run while side-stepping — known cosmetic limitation, `ABP_Unarmed` has no strafe blendspace wiring).
- Jump under the duel camera (deliberately unchanged this pass).
- Camera behavior when fighters get very close (min-distance clamp) and very far (max-distance + framing at lane extremes).

### 11.7 Human test instructions (PIE)

1. Open `Lvl_ThirdPerson`, press Play (in-viewport PIE).
2. Expect a ~0.75 s blend from behind-the-shoulder to the side-profile duel view; player on the **left**, Vanguard on the **right**.
3. **A/D** = retreat/close along the duel axis. **W/S** = limited depth movement (stops at the lane edges). **Mouse** = should do nothing. **Space** = jump (stock). **LMB** = punch (stock combat checkpoint).
4. Walk into melee range and confirm the whole §7 punch loop still behaves (Attack Triggered print, health decrement prints, bar, sparks, hit-react).
5. To compare against stock behavior, set `bEnableDuelCamera` default to false in `BP_ThirdPersonPlayerController` (or flip `CameraSideSign` on `BP_DuelCameraRig` to −1 to mirror the stage). All tuning values live on `BP_DuelCameraRig` class defaults under Targets / Combat Axis / Framing / Distance / Smoothing / Movement Constraints.

### 11.8 Known limitations (accepted for first pass)

- Depth clamp and fallback-spawn offset assume the combat axis is world-X aligned (`CombatAxisYaw` near 0); generalizing the clamp to arbitrary axis yaw is future work if arenas ever rotate.
- Depth clamp is a hard positional clamp (SetActorLocation), not a movement-input constraint — functional but blunt at the lane edge.
- Strafe animation: side-stepping plays the forward locomotion pose (no strafe blendspace in `ABP_Unarmed`); cosmetic only.
- Vanguard facing is driven externally by the rig each tick (no AI added, per scope); if a future hit-react needs rotational freedom, gate the facing write.
- `SmoothedMidpoint.Z` follows capsule centers; jumping bobs the framing slightly (midpoint interp at speed 5 damps it). Height smoothing/refinement is explicitly a later pass per the milestone.
- Deferred per milestone: dominance bias, push-in, offset framing, smooth height handling.

### 11.9 Failures and fixes this run

- `get_node_type_pins` **instantiates a probe node** in the target graph — it must be deleted afterward or it lingers as a stray (one `K2Node_VariableSet_0` was created and removed in `SetDuelMovementMode`).
- Bool-var accessor names strip the `b` prefix AND include the variable's category in the DSL type id: `bDuelModeActive` in category "Duel Camera" → `Variables|DuelCamera|Get/SetDuelModeActive` (a bare `Variables|Default|…` guess fails).
- Type ids containing parentheses (`Math|Float|Clamp(Float)`, `Math|Vector|Distance2D(Vector)`, `Utilities|String|ToString(Float)`) are risky in the S-expression DSL — avoided entirely via `select` ternary clamps and component-wise math (sqrt of dx²+dy²).
- DSL positional args can mis-bind to the `self` pin on own-function calls (`CallFunction|UpdateDuelCamera DeltaSeconds` tried to feed DeltaSeconds into `self`); keyword form `:DeltaSeconds DeltaSeconds` fixes it.
- `SpawnActorFromClass`'s `SpawnTransform` by-ref pin rejects literal defaults — must wire a `MakeTransform` (compile error otherwise; see §11.4).
- `ProgrammaticToolset` scripts: `dict.get(key, default)` is unsupported (`_StrictDict`), and helper kwargs that shadow positional args raise TypeErrors — use plain `[]` access and dict-style args.
- `PlayerCameraManager.ViewTarget` and controller `ControlRotation` are not readable via `ObjectTools.get_properties`; proving the active view target was done by comparing the camera manager's actor transform to the rig's (identical ⇒ rig is the view target).

---

## 12. Milestone 4 — Movement-only Vanguard duel behavior (2026-08-02, branch `feature/vanguard-duel-movement`)

**Scope delivered:** the Vanguard now moves like a passive second fighter — approaches when far, retreats when crowded, holds a preferred range, drifts in depth at controlled intervals, pauses while hit-reacting, and can never trade screen sides with the player. No attacks, no damage changes, no Behavior Tree, no combat AI. Movement-and-camera stress test only.

### 12.1 Architecture chosen and why

A **self-contained runtime-spawned actor**, `/Game/AscendantImpact/Duel/BP_VanguardDuelMover`, spawned by `BP_ThirdPersonPlayerController` immediately after the Duel Camera rig, behind its own instance-editable toggle **`bEnableVanguardMover`** (default true, nested inside the `bEnableDuelCamera` branch — camera off implies mover off). Rationale:

- `BP_VanguardProxy`'s combat/feedback graph stays untouched (zero graph edits there — see 12.2 for the one property-default change).
- Locomotion is driven externally through **`AddMovementInput` on the unpossessed-looking Character** — which works because Character defaults (`AutoPossessAI=PlacedInWorld`, `AIControllerClass=AIController`) mean the placed Vanguard is already possessed by a stock AIController in PIE, so CharacterMovement consumes input normally. No AIController asset or Behavior Tree was added; `ActivateMover` calls `SpawnDefaultController` only as a fallback if no controller exists (e.g. for a runtime-spawned Vanguard).
- Real CMC-driven movement means real velocity → the locomotion animation plays, capsule collision stays authoritative, and acceleration/braking provide smoothing for free.
- Facing remains owned solely by `BP_DuelCameraRig` (one facing system, unchanged).

### 12.2 Assets created / modified (exact Git manifest)

**Created:**
- `Content/AscendantImpact/Duel/BP_VanguardDuelMover.uasset` — Actor Blueprint, logic only (no components beyond the default root).

**Modified:**
- `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` — added `bEnableVanguardMover` (bool, instance-editable, default true) + `VanguardMover` (object ref), category "Duel Camera"; appended `Branch → SpawnActor BP_VanguardDuelMover → Set VanguardMover` after the SetViewTargetWithBlend node inside the existing duel-camera branch. No existing wiring disturbed.
- `Content/Variant_Combat/Blueprints/BP_VanguardProxy.uasset` — **one class-default change, no graph edits**: `bUseControllerRotationYaw` true → **false**. The raw-Character default (true) let the auto-possessing stock AIController's control rotation drive the actor yaw, silently fighting the Duel Camera's facing writes (invisible until now only because the spawn yaw 180 happened to be the correct facing). False matches the third-person template characters.
- `docs/agent/PROTOTYPE_BLACKBOARD.md` — this section. `CLAUDE.md` — durable architecture/gotcha updates.

**Not touched:** `BP_ThirdPersonCharacter`, `BP_DuelCameraRig`, level/external actors, all input assets, `UI_LifeBar`/VFX/camera-shake assets, `Config/DefaultEditorPerProjectUserSettings.ini`.

### 12.3 BP_VanguardDuelMover — logic, functions, variables

**Event graph:** `EventTick(DeltaSeconds)` → `ResolveFighters()` → nested IsValid guards (stops safely if either fighter is invalid) → one-shot `ActivateMover()` → `UpdateDuelMovement(DeltaSeconds)`. Same fail-safe pattern as the camera rig; global searches (`GetPlayerPawn`/`GetActorOfClass`) run only while a reference is unresolved. The mover does **not** spawn Vanguards (the camera rig keeps that single authority).

**`ActivateMover()`** (one-shot): stores `OriginalMaxWalkSpeed` (600) / `OriginalMaxAcceleration` (2048) from the Vanguard's CMC for reversibility, then applies `VanguardMoveSpeed` (180) and `VanguardAcceleration` (600); forces `bUseControllerRotationYaw=false` on the Vanguard pawn at runtime (belt-and-braces — the already-loaded level instance does not pick up the new class default this editor session); seeds `CurrentDepthTarget` with the Vanguard's current depth and randomizes the first decision interval; `SpawnDefaultController` only if the Vanguard has no controller.

**`UpdateDuelMovement(DeltaSeconds)`** per tick: runs the depth-decision timer, computes signed combat-axis separation (world X), updates intent, then applies movement inputs **only if no montage is playing on the Vanguard's AnimInstance** (`IsAnyMontagePlaying` — this is the hit-react movement pause, read-only on animation state), and always applies constraints.

**`UpdateMovementIntent(SepAbs)`** — three-state int with hysteresis (no enum asset): `0` hold, `1` advance, `2` retreat. From hold: advance when separation > Preferred+DeadZone (360), retreat when < Preferred−DeadZone (240). Advance/retreat each end only on reaching Preferred (300) — the hysteresis prevents threshold jitter and produces advance → settle → hold behavior.

**`UpdateDepthDecision(DeltaSeconds)`** — accumulates time; every `NextDecisionInterval` (random 1.5–3.5 s) either holds current depth (probability `DepthHoldChance` 0.4) or picks a random depth target within ±`MaxDepthTarget` (150) around `DepthLaneCenter`, then re-randomizes the interval.

**`ApplyMovementInputs()`** — axis: `AddMovementInput(world X, ±1)` toward/away from the player per intent (direction from the *signed* separation, so it stays correct even if geometry ever flips). Depth: if farther than `DepthArriveTolerance` (15) from the depth target, `AddMovementInput(world Y, ±DepthMoveScale)` — scale 0.5 while holding range, ×0.4 further reduction while actively correcting range ("pause depth while aggressively correcting").

**`ApplyConstraints()`** — three gentle position clamps (violations in normal play are ≤ one frame of movement, ~10 cm, so no visible teleporting): Vanguard depth clamped to the same lane the camera uses (±180); Vanguard X clamped to ≥ player X + `MinimumAxisSeparation` (110); player X clamped to ≤ Vanguard X − 110. The last one is the **player-side no-crossing safeguard** — capsule collision alone would let the player circle through the depth lane and swap sides. Ordering (player low-X / Vanguard high-X) matches the P1-left / P2-right screen rule for the current `CameraSideSign=+1`, `CombatAxisYaw=0` setup.

**Exposed tuning variables (instance-editable, ALL PROVISIONAL):**

| Category | Variable | Default |
|---|---|---|
| Range | `PreferredDistance` | 300 |
| Range | `RangeDeadZone` | 60 |
| Speeds | `VanguardMoveSpeed` | 180 |
| Speeds | `VanguardAcceleration` | 600 |
| Speeds | `DepthMoveScale` | 0.5 |
| Depth | `DepthDecisionIntervalMin` | 1.5 |
| Depth | `DepthDecisionIntervalMax` | 3.5 |
| Depth | `MaxDepthTarget` | 150 |
| Depth | `DepthHoldChance` | 0.4 |
| Depth | `DepthArriveTolerance` | 15 |
| Separation | `MinimumAxisSeparation` | 110 |
| Lane | `DepthLaneCenter` | 0 |
| Lane | `DepthLaneHalfWidth` | 180 |

Lane values must match `BP_DuelCameraRig`'s (they are duplicated, not shared — see limitations). Internal (not editable): `PlayerFighter`, `VanguardFighter`, `MovementIntent`, `CurrentDepthTarget`, `DepthDecisionTimer`, `NextDecisionInterval`, `bMoverActivated`, `OriginalMaxWalkSpeed`, `OriginalMaxAcceleration`.

### 12.4 Compile & save results

`BP_VanguardDuelMover`, `BP_ThirdPersonPlayerController`, `BP_VanguardProxy` — all `compile_blueprint(warnings_as_errors=true)` → **clean**. All saved via `AssetTools.save_assets`. No MCP asset-validation tool exists; human **Tools → Validate Assets** recommended for sign-off.

### 12.5 Tool-assisted runtime validation (two PIE sessions via MCP)

All numbers read from the live PIE world:

- **Mover spawns and activates:** `bMoverActivated=true`; originals stored (600/2048); Vanguard CMC live values 180/600. Duel Camera unaffected — rig spawned, camera manager tracking it (their transforms differ only by millisecond sampling skew while the camera was actively moving with the fighters, i.e. midpoint/zoom respond to both movers).
- **Advance:** player teleported to X=−400 → intent flipped to 1, Vanguard walked 350 → −53 → −122 (avg ~161 cm/s vs MaxWalkSpeed 180), stopping at separation 278 (≤ Preferred 300) with intent back to 0. It correctly *followed the player across the world origin* while keeping ordering (player −400 < Vanguard −122).
- **Retreat:** player teleported to 150 cm away → intent 2, Vanguard backed off to separation 325, intent back to 0.
- **No pass-through / side swap:** player teleported to 30 cm gap → constraint restored ≥110 immediately; after every teleport stress, player X < Vanguard X held. (Note: a *teleporting* player causes a visible one-time Vanguard shove from the clamp — normal-speed play only ever violates by ~10 cm/frame.)
- **Depth wander:** `CurrentDepthTarget` observed changing across samples (69 → 22.3 → 19.3 → 22.3, includes hold-rolls); Vanguard Y actually traveled (78.9 → −7.2 → 22.3 → 78.3); all values inside the ±180 lane.
- **Mutual facing while offset:** with Vanguard at (350.8, 78.3) and player at (23.5, 0), Vanguard yaw −166.55° = the exact look-at bearing; player yaw mid-interpolation toward its matching bearing. The §12.2 yaw-flag fix verified live: `bUseControllerRotationYaw=false` on the PIE instance after activation.
- **Never attacks:** structurally impossible — the mover's only outputs are `AddMovementInput`/`SetActorLocation`; `BP_VanguardProxy` still contains no attack logic.
- **No runtime errors:** log sweep for Accessed None / Blueprint runtime errors across both sessions → zero hits.
- **Screenshots:** `CaptureEditorImage` failed both attempts this session ("Failed to capture any editor windows" — the editor window was likely minimized; it captures the OS desktop window). Validation rests on the runtime numbers; visual confirmation folds into the human PIE pass.

### 12.6 PENDING HUMAN PIE

- Overall movement **feel**: cautious-probing quality, hesitation, no hyperactivity or jitter (all interval/speed/deadzone defaults are provisional).
- Approach/retreat readability at player-controlled speeds (validation used teleports, not walked approaches).
- Depth offsets reading as deliberate "circling" rather than drift.
- The min-separation clamp feel when deliberately shoving into the Vanguard.
- Hit-react pause: punch the Vanguard and confirm it doesn't slide during the reaction, and that damage/health-bar/VFX/hit-react all still work (logic untouched).
- Camera framing quality with both fighters moving, near min and max distance.
- Whether the Vanguard walking backward at 180 cm/s while retreating looks acceptable with the forward-run animation (known cosmetic limit).

### 12.7 Human PIE acceptance test

1. Press Play. Duel camera blends in; player left, Vanguard right.
2. **Stand still**: Vanguard should settle near ~300 cm and mostly hold, occasionally drifting in depth, never rushing.
3. **Walk toward it (W is depth — use A/D for axis)**: press **D** to close — it should retreat before you overlap; try to push through — you should be held ~110 cm apart with no side swap.
4. **Retreat (A)**: it should follow calmly (it is slower than you: 180 vs 600), settling back near preferred range.
5. **Move in depth (W/S)**: watch for occasional Vanguard depth offsets within the lane.
6. **Try to run around it** through the depth lane — screen roles must not swap.
7. **Punch it (LMB)** several times: damage prints, health bar, sparks, hit reaction all as before; Vanguard should pause movement during the reaction and never retaliate.
8. Toggles: `bEnableVanguardMover=false` on `BP_ThirdPersonPlayerController` restores the static Vanguard; all movement tuning is on `BP_VanguardDuelMover` class defaults.

### 12.8 Known limitations

- Lane bounds and axis assumptions are duplicated between rig and mover (both hard-assume world-X axis / world-Y depth, like the rig's own §11.8 limitation); they must be tuned in tandem.
- No combat-axis arena bounds: the pair can walk arbitrarily far along X (e.g. onto the staircase area past X≈400, where ground height changes).
- Backward retreat and sideways depth movement play the forward locomotion animation (no strafe/backpedal blendspace) — accepted cosmetic limit.
- The hit-react pause stops *input*, not momentum; a tick of residual deceleration slide can remain (braking 2048 stops it in <0.1 s).
- A teleporting player (debug scenario only) makes the min-separation clamp shove the Vanguard visibly; unreachable in normal play.
- The mover assumes single-player (player index 0), consistent with the prototype scope.

### 12.9 Failures and fixes this run

- **`BP_VanguardProxy` had `bUseControllerRotationYaw=true`** (raw-Character default; the template characters override it, this BP never did) — combined with auto-possession this could override external facing writes. Fixed at the class default AND enforced at runtime in `ActivateMover`, because the already-loaded level instance kept the old value for the session (same instance-staleness family as §7e, milder form: in-memory instances don't re-sync CDO edits).
- `Controller` and `ViewTarget` are not readable via `ObjectTools.get_properties` (same family as §11.9's ControlRotation) — possession was proven empirically (CMC consumed `AddMovementInput`, so a controller must exist).
- `CaptureEditorImage` fails outright when the editor window isn't visible on the desktop ("Failed to capture any editor windows") — new tooling observation.
- `time.sleep` inside `ProgrammaticToolset` scripts works and enables multi-sample runtime observation during PIE — first use of this technique; very effective for movement validation.

---

## 13. Milestone 5 — Duel-readability polish: jog retune + flat test arena (2026-08-02, branch `feature/duel-arena-polish`)

Two deliverables: (1) retuned `BP_VanguardDuelMover` so the Vanguard visibly closes distance with purposeful combat-jog movement, and (2) a clean flat test level `Lvl_DuelGraybox` for camera/locomotion evaluation. No logic changes anywhere — Goal 1 is pure class-default tuning; Goal 2 is level content only. `Lvl_ThirdPerson` is untouched.

### 13.1 Vanguard movement retune (class defaults only, no graph edits)

| Variable | Old | New | Effect |
|---|---|---|---|
| `PreferredDistance` | 300 | **240** | settles into a closer, more readable fighting distance |
| `RangeDeadZone` | 60 | **50** | advance triggers beyond 290 (was 360) — at the 350 cm spawn spacing the Vanguard now advances immediately instead of standing |
| `VanguardMoveSpeed` | 180 | **300** | slow walk → combat jog |
| `VanguardAcceleration` | 600 | **1000** | shorter, more purposeful starts/stops |
| `DepthMoveScale` | 0.5 | **0.4** | restrained depth drift (120 cm/s) |

Unchanged: `MinimumAxisSeparation` 110, depth decision intervals 1.5–3.5 s, `DepthHoldChance` 0.4, `MaxDepthTarget` ±150, lane 0 ± 180, `DepthArriveTolerance` 15. Hysteresis band is now advance >290 / retreat <190 / exits at 240. `compile_blueprint(warnings_as_errors=true)` clean; asset saved.

### 13.2 Lvl_DuelGraybox — clean flat duel arena

**Created `/Game/AscendantImpact/Maps/Lvl_DuelGraybox`** by duplicating `Lvl_ThirdPerson` via `AssetTools.duplicate` + `save_assets` — this **fully persisted the OFPA level from MCP alone** (66 fresh external-actor packages written to `Content/__ExternalActors__/AscendantImpact/Maps/Lvl_DuelGraybox/` + 2 under `__ExternalObjects__` + the `.umap`). The §7 "new actors need human Ctrl+S" blocker does not apply to the duplication path, because every package is created fresh by the asset-level duplicate.

**Removed (17 actors — the raised central platform assembly that both fighters used to spawn on):** `SM_Cylinder` (the 700 cm disc top at Z≈200), `SM_QuarterCylinder5–12` (platform sides/skirt), `SM_Cube13–16` (platform body), `SM_Ramp9–12` (the four lane-adjacent ramps). **Kept:** the 4000×4000 `Floor`, all perimeter walls (`SM_Cube2/3/4/5/17/18/19/20` at ±1800–2000), the distant corner pillars/cubes/ramps at |X|≥1200 (visual boundary, outside the duel space), lighting/sky/fog/post-process.

**Repositioned:** `PlayerStart` (0, 0, 302→**94**) yaw 0; `BP_VanguardProxy` (350, 0, 288→**90**) yaw 180 — both now on the flat floor (top at exactly Z=0, verified by `trace_world` at both spawn columns). GameMode: inherited project default (no per-level override was needed or added).

**Persistence proof:** deletions flushed 66→49 external-actor packages on disk after `save_assets([])` (save-all-dirty); then a full level round-trip (load `Lvl_ThirdPerson`, reload `Lvl_DuelGraybox` from disk) confirmed spawn positions, deleted platform, and kept geometry all persisted. **No human Ctrl+S is required for this level.**

### 13.3 Runtime validation (PIE in Lvl_DuelGraybox via MCP)

- Player spawns at (0,0,92), Vanguard at (350,0,90) — same flat ground, player screen-left / Vanguard screen-right (camera side unchanged).
- **Advance at spawn spacing:** by the first sample (~2 s in) the Vanguard had already jogged from 350 cm to 231 cm separation and settled to hold — exactly the "closes distance instead of standing" goal.
- **Jog speed measured:** teleported the player 750 cm away → intent 1, sampled axis speed 236 then **302 cm/s** (target 300), settled at separation 231.7 with a clean stop — three consecutive motionless samples, i.e. **no jitter/oscillation** at the band edge.
- Depth wander active (settled depth offset −124.4 matching `CurrentDepthTarget`), inside the lane.
- Camera: rig transform == camera-manager transform (live view target), `SmoothedDistance` 607.4 = exactly clamp(450 + 0.6 × 262) for the measured 262 cm 2D separation — midpoint/zoom tracking both fighters on the new map.
- View unobstructed: the only geometry between/around the fighters is the flat floor (obstruction candidates deleted; verified by the remaining-actor sweep).
- Log sweep: zero Accessed None / Blueprint runtime errors (only the known 2026-08-01 authoring-time entries remain in the session log).
- Punch/damage chain untouched this pass (no Blueprint graph was modified anywhere); regression is part of the human PIE list.

### 13.4 PENDING HUMAN PIE

- Whether 300 cm/s reads as a purposeful jog (vs. slide-y) with the existing forward-run locomotion blend, and overall cautious-probing feel under the new closer spacing.
- Retreat feel when crowding it at player speeds; min-separation shove feel.
- Depth shifts reading as restrained (0.4 scale).
- Punch loop regression on the new map (damage, health bar, VFX, hit-react, hit-react movement pause).
- Framing quality at 240 cm preferred distance (fighters are now closer → camera nearer MinCameraDistance more often).
- Open the editor on `Lvl_DuelGraybox` (File → Open Level) or PIE directly from it; the project default map is still `Lvl_ThirdPerson` — switching the default was deliberately not done.

### 13.5 Known limitations

- `Lvl_DuelGraybox` inherits the template's look (checker floor, distant clutter at |X|≥1200) — evaluation arena, not environment design.
- The editor session is left with `Lvl_DuelGraybox` open; the human should expect that on return.
- Fighters can still wander along ±X to the distant geometry (~±1500) — no combat-axis bounds yet (same as §12.8).
- Camera-facing/lane values remain duplicated between rig and mover.

### 13.6 Tooling discoveries this run

- **`AssetTools.duplicate` + `save_assets` persists an entire OFPA level** (map + all external actor/object packages) with no human save.
- **`save_assets([])` (empty list = all dirty) flushes OFPA actor deletions and modifications to disk** — the map-path-only save does not; the save-all sweep is required for external packages. This supersedes the assumption that all OFPA edits need human Ctrl+S: only *newly added* actors in an existing level still have that limitation (untested whether save-all would fix those too — next time a new actor is placed, try `save_assets([])` before asking the human).
- Level round-trip (`load_level` away and back) is a reliable, cheap persistence proof.

### 13.7 Git manifest

Modified: `Content/AscendantImpact/Duel/BP_VanguardDuelMover.uasset` (tuning defaults), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. Added: `Content/AscendantImpact/Maps/Lvl_DuelGraybox.umap`, 49 packages under `Content/__ExternalActors__/AscendantImpact/Maps/Lvl_DuelGraybox/`, 2 under `Content/__ExternalObjects__/AscendantImpact/Maps/Lvl_DuelGraybox/`. `Lvl_ThirdPerson` and its external actors: zero changes. `Config/DefaultEditorPerProjectUserSettings.ini`: untouched/unstaged.

---

## 14. Milestone 6 — Arena containment + base camera framing finalization (2026-08-02, branch `feature/duel-camera-containment`)

**Scope delivered:** exposed combat-axis bounds keep both fighters inside the central flat portion of `Lvl_DuelGraybox` (no more drifting into perimeter walls or the green clutter), and the camera's distance curve was retuned so the *widest legal separation* keeps both fighters framed — the one clear issue the stress math demonstrated. No new systems, no level edits, no animation changes.

### 14.1 Architecture and boundary values

Containment lives in **`BP_VanguardDuelMover.ApplyConstraints`** — the function that already owned min-separation and lane clamps, so all fighter position constraints have a single authority (no third value set was introduced). Two new instance-editable floats, category **Arena Bounds**:

- `CombatAxisMin` = **−650**, `CombatAxisMax` = **+650** (provisional). Max legal separation 1300 cm; nearest environment geometry starts at |X|≈1200, so fighters keep ≥500 cm clearance from everything.

The clamp is a **single deterministic pass**: player X → [Min, Max−MinSep]; then Vanguard X → [clampedPlayerX+MinSep, Max]; Vanguard depth → lane (unchanged). This guarantees bounds + ordering + min-separation simultaneously (player can never be pushed out of bounds by the ordering rule). Corrections are gentle (≤ one frame of movement in normal play, no teleporting; player correction only fires on actual violation). Additionally, **`ApplyMovementInputs` suppresses retreat input once the Vanguard is within 5 cm of `CombatAxisMax`** so it doesn't run-in-place against the invisible bound. Player-side boundary behavior is walk-in-place at the edge (input suppression for the player pawn would require touching `Move` — deliberately not done).

### 14.2 Camera changes (and what was deliberately left unchanged)

**The demonstrated issue:** with FOV 55, screen half-width ≈ distance × 0.52. The old curve (0.6 × separation, max 900) frames at most ~940 cm of separation — far less than the 1300 cm the bounds allow; both fighters would leave the screen at wide spacings. **Changed on `BP_DuelCameraRig` class defaults:**

- `DistancePerSeparation` 0.6 → **0.8**
- `MaxCameraDistance` 900 → **1500**

At S=1300 steady state: distance 1490 → half-width 776 cm vs. the 700 needed (fighter at 650 + ~50 body) — framed with ~10% margin at the absolute worst case. At the settled fighting range (~285 cm separation, incl. depth offset) distance ≈ 680 → fighters occupy the central ~55% of the screen — no large empty framing. At min separation (110): distance 538, above the 500 floor.

**Left unchanged, with reasoning:** `MinCameraDistance` 500, `BaseCameraDistance` 450, FOV 55, `SideAngleDegrees` 12, height/look offsets, all smoothing speeds. `DistanceInterpSpeed` 3 was examined for zoom lag at maximum separation-growth rate (~240 cm/s of distance target change → ~80 cm steady-state lag ≈ 42 cm of half-width): borderline but not a demonstrated problem in normal play, and the measured zoom behavior shows clean monotone settling — kept per the "only adjust on demonstrated issue" rule. No dominance bias, arcs, or hit-driven motion added.

### 14.3 Compile / save / PIE evidence

`BP_VanguardDuelMover` + `BP_DuelCameraRig` compile clean (`warnings_as_errors=true`); both saved. PIE stress in `Lvl_DuelGraybox` (runtime numbers from the live PIE world):

- **Axis bounds:** player teleported to −2000 → clamped to exactly **−650.0**. Vanguard teleported to +2000 → clamped to 650, then correctly advanced (sampled at 379 mid-jog toward the player). No fighter can reach walls (±1800) or clutter (±1200).
- **Depth bounds:** player teleported to Y=+2000 → exactly **180.0**; Vanguard to −2000 → clamped then drifting to its depth target (−137.7), inside the lane.
- **Ordering:** player X < Vanguard X after every stress case; min-separation still enforced — and in the crowd test the Vanguard *retreated by behavior* (settled gap 285.7) before the hard clamp was ever needed.
- **Zoom stability:** SmoothedDistance samples after crowding: 554.7 → 681.2 → 682.1 → 682.1 → 682.1 → 682.1 — monotone settle, **zero pulsing/oscillation**. Camera roll −3.9e-08 (no roll, no axis crossing; side fixed at +Y).
- **Wide-case camera:** during the max-separation transient the distance was mid-interpolation at 1194 → target ~1490, confirming the new curve engages.
- **Visual:** PIE screenshot shows both fighters fully framed on flat ground, player left / Vanguard right, facing each other, perimeter geometry background-only, view unobstructed.
- **Log:** zero Accessed None / Blueprint runtime errors (only the known 2026-08-01 authoring entries).
- `WorldPosToScreenCoords` proved to use the **editor** viewport camera even during PIE (returned off-screen values) — not usable for PIE framing checks; framing was verified geometrically + by screenshot instead.

### 14.4 PENDING HUMAN PIE

- Boundary feel when walking into the axis edges (player walks in place at the invisible bound — acceptable?).
- Framing quality across the full legal range in motion, especially the zoom-out toward 1490 during max-range chases.
- Whether the wider `DistancePerSeparation` 0.8 pullback feels right at mid ranges.
- Punch/damage/health-bar/VFX/hit-react regression (logic untouched since §12; still unverified by hand on this map).
- Overall duel-readability sign-off of the base camera (gates the deferred dominance-bias work).

### 14.5 Known limitations

- Vanguard gait: moves at 300 cm/s while `ABP_Unarmed` displays whatever its existing locomotion blend chooses — no walk/jog/run state matching was added (out of scope). **Multi-speed locomotion + animation matching is a later presentation task.**
- Player boundary is a positional clamp (walk-in-place at edges), not input suppression.
- Bounds assume the world-X combat axis, consistent with rig/mover (§11.8/§12.8).
- `Lvl_ThirdPerson` still has no arena bounds (the mover's defaults apply there too if played — bounds ±650 also happen to fit that map's central area, but it retains its platform/stairs; `Lvl_DuelGraybox` is the evaluation map).

### 14.6 Git manifest

Modified: `Content/AscendantImpact/Duel/BP_VanguardDuelMover.uasset` (2 new vars + 2 rewritten functions), `Content/AscendantImpact/Camera/BP_DuelCameraRig.uasset` (2 tuning defaults), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. No level, input, character, controller, or combat assets touched. `Config/DefaultEditorPerProjectUserSettings.ini` untouched/unstaged.

---

## 15. Milestone 7 — Close-contact duel spacing (2026-08-02, branch `feature/duel-close-contact`)

**Problem fixed:** close range felt like an invisible wall — retreat began at 190 cm and `MinimumAxisSeparation` 110 left a ~40 cm air gap between capsule surfaces. Goal: fighting-game near-contact without capsule overlap, pass-through, or side exchange.

### 15.1 Measured collision dimensions (inspected, not assumed)

- `BP_ThirdPersonCharacter` capsule: radius **35**, half-height 90.
- `BP_VanguardProxy` capsule: radius **34**, half-height 88.
- Capsule contact therefore occurs at **69 cm** center-to-center.

### 15.2 Tuning changes (all on `BP_VanguardDuelMover` class defaults; one graph edit)

| Value | Old | New | Rationale |
|---|---|---|---|
| `MinimumAxisSeparation` | 110 | **78** | 69 cm contact + 9 cm safety margin — meshes read as nearly touching (meshes are inset from capsules), capsules can never overlap |
| `PreferredDistance` | 240 | **180** | closer readable fighting distance |
| `RangeDeadZone` | 50 | **45** | retreat now begins under **135 cm** (was 190), advance beyond 225; both exit at 180 |
| `RetreatSpeedScale` | — (new, Speeds, editable) | **0.5** | retreat runs at half input scale (~150 cm/s vs player 600) so the Vanguard **yields ground under pressure instead of escaping it** |

Graph edit: `ApplyMovementInputs` retreat branch multiplies its input scale by `RetreatSpeedScale` (the CMC analog-input modifier scales max speed, so this genuinely halves retreat speed). Everything else — advance behavior, depth wander + 0.4 combat-jog scale, decision intervals, arena bounds ±650, boundary retreat suppression, `ApplyConstraints` as sole constraint authority, camera values — unchanged.

### 15.3 PIE validation (Lvl_DuelGraybox, runtime evidence)

- **Settle from spawn:** Vanguard approaches and settles at 171 cm (≈ preferred 180) — no more standing at a large gap.
- **Yield under crowding:** player placed at 100 cm → Vanguard backed off at a measured **83 cm/s** average (vs 300 advance speed), settling at 182.9 — retreat is slow and stops at preferred; it does not flee to the old 240+ gap.
- **Sustained near-contact under pursuit:** a 10-step chase loop (player re-pressed to 85 cm behind the Vanguard every 0.35 s) locked the gap at a constant **85 cm** for 8 consecutive samples — including after the Vanguard was pushed all the way to the arena bound (x = 650), i.e. the corner-pressure case holds. Minimum gap ever seen 85; the constraint floor is 78; capsule overlap (< 69) **never occurred**; player-left/Vanguard-right ordering held throughout.
- **Violation recovery:** teleporting the player to a 40 cm gap was corrected within a frame and normal behavior resumed (ordering intact).
- **Camera at close spacing:** SmoothedDistance 602 at the settled range; at the 78–85 cm contact floor the distance formula gives ~515–520, above the 500 minimum — framing stays readable; roll −5e-08.
- **Screenshot:** fighters visually near body-contact, no interpenetration, no visible empty gap, both framed, correct sides.
- **Log:** zero Blueprint runtime / Accessed None errors (only the known 2026-08-01 authoring entries).
- Compile: `BP_VanguardDuelMover` clean with `warnings_as_errors=true`; asset saved.

### 15.4 PENDING HUMAN PIE

- Whether 78 cm reads as proper fighting-game contact with these meshes in motion (margin can be tightened toward ~72 or widened via the exposed value).
- Punch → damage → health bar → VFX → hit-react at the new contact distance by hand (structurally unaffected: the attack's overlap sphere is 110 cm radius at 120 cm forward, easily covering an 85 cm gap; no combat logic touched since §12).
- Whether the slow-yield retreat (0.5 scale) feels like "holding ground under pressure" vs. sluggishness.
- Static-crowding note: a player who walks to contact and then *stands still* will see the Vanguard slowly back off toward 180 — that is the retreat model working; confirm it reads as intentional spacing behavior.

### 15.5 Git manifest

Modified: `Content/AscendantImpact/Duel/BP_VanguardDuelMover.uasset` (one new var, one function edit, four default changes), `docs/agent/PROTOTYPE_BLACKBOARD.md`. No other assets touched. `Config/DefaultEditorPerProjectUserSettings.ini` untouched/unstaged.

---

## 16. Milestone 8 — First telegraphed Vanguard strike (2026-08-02, branch `feature/vanguard-basic-strike`)

**Scope delivered:** the first two-sided combat exchange — a single, readable, fair, telegraphed Vanguard punch with one impact check, hit/whiff based on the player's actual position at impact, clean recovery, cooldowns that prevent spam, windup interruption on being hit, and a minimal reversible player damage receiver. This is a **disposable graybox prototype strike**, not the gated Attack A design (which remains untouched and gated).

### 16.1 Architecture

**`/Game/AscendantImpact/Duel/BP_VanguardBasicAttackDriver`** — a separate runtime-spawned logic actor (fourth in the controller's spawn chain: camera rig → mover → attack driver), gated by new instance-editable **`bEnableVanguardBasicAttack`** (default true, nested inside the duel-camera gate). Chosen so `BP_VanguardDuelMover` stays a pure movement controller; the driver coordinates through one tiny interface instead of merging state machines. The driver caches `PlayerFighter`/`VanguardFighter`/`VanguardMover` refs (resolve-only-while-invalid, same pattern as the rig/mover — no repeated global searches). The driver actor doubles as the **telegraph**: it carries a `TelegraphText` TextRenderComponent (big red "!", world size 150, centered), starts hidden, and during wind-up positions itself above the Vanguard's head (+140) facing the camera side (yaw 90).

**Movement-lock interface added to `BP_VanguardDuelMover`:** `bExternalMovementLocked` + `SetExternalMovementLocked(bLocked)`. While locked, `UpdateDuelMovement` skips depth decisions, intent updates, and movement inputs but **still runs `ApplyConstraints`** (bounds/ordering/min-separation/lane stay enforced). The driver locks during wind-up/strike/recovery, unlocks on finish/cancel — one movement system, no competition.

**Player damage receiver in `BP_ThirdPersonCharacter`** (smallest reversible prototype): `MaxHealth` 100 / `CurrentHealth` vars; `InitHealth()` called from a new `BeginPlay` event; `ReceiveAnyDamage` → `HandleDamage(DamageAmount)`: clamps health at 0 (`Max(0, h−d)`), prints "Player Health: N" (orange, 3 s), plays the previously unused **`BP_CameraShake_Hit_Player`**, and plays `MM_HitReact_Front_Med_01` as a dynamic montage on `DefaultSlot` (the project-standard pattern). Events were added by node surgery (add_event + 3 pin connections), not graph rewrite — the attack chain is untouched. No death/respawn/HUD/knockdown/i-frames. The receiver cannot trigger the player's own attack logic (it only touches health/print/shake/montage), and the player's punch cannot self-damage (its overlap is class-filtered to the Vanguard).

### 16.2 Attack state flow (int `AttackState`, no enum asset)

`0 idle` → (cooldown expires → `TryStartAttack`: axis-separation ≤ AttackRange AND vanguard not montage-playing AND ordering intact AND decision roll passes; else retry in `RetryDelay`) → `BeginWindup` (`1`: lock mover, show telegraph, telegraph follows Vanguard each tick; **if the Vanguard's AnimInstance starts playing any montage during wind-up — i.e. its existing hit-react from a player punch — `CancelAttack`** hides the telegraph, unlocks, re-rolls cooldown, applies no damage) → after `WindupDuration` → `BeginStrike` (`2`: hide telegraph, play `MM_Attack_02` via `PlaySlotAnimationAsDynamicMontage` on `DefaultSlot`, blend 0.1/0.2) → at `StrikeImpactDelay` exactly one `PerformImpactCheck` (guarded by `bImpactDone`) → after `StrikeDuration` → `BeginRecovery` (`3`) → after `RecoveryDuration` → `FinishAttack` (`0`, cooldown = random(min,max), unlock mover).

**Impact geometry:** single `SphereOverlapActors` at Vanguard location + forward × `ImpactForwardOffset` (forward = its live facing, which the camera rig keeps aimed at the player), radius `ImpactRadius`, Pawn object type, **class-filtered to `BP_ThirdPersonCharacter_C`**, one `ApplyDamage(10)` per overlap result (the filter makes that at most one). Max reach = offset 100 + radius 90 + player capsule 35 = **225 cm** — deliberately matched to the mover's hold band (below). No hit occurs merely because the attack started in range; position at the impact moment decides.

### 16.3 Provisional values (all instance-editable on the driver)

Attack Conditions: `AttackRange` **240** · `InitialAttackDelay` 1.5 · `AttackCooldownMin` 2.5 / `Max` 4.0 · `AttackDecisionChance` 0.65 · `RetryDelay` 0.6. Timing: `WindupDuration` 0.7 · `StrikeImpactDelay` 0.3 · `StrikeDuration` 0.6 · `RecoveryDuration` 1.0. Impact: `ImpactForwardOffset` 100 · `ImpactRadius` 90 · `AttackDamage` 10. Telegraph: `TelegraphHeightOffset` 140. Animation: **`MM_Attack_02`** (1.0 s, same skeleton/DefaultSlot; visually distinct from the player's `MM_Attack_01`; no Montage asset authored; `ABP_Unarmed` untouched).

### 16.4 Failures and fixes this run (design-relevant)

1. **Attack range vs. mover hold band mismatch** (first PIE): range check originally used 2D distance ≤ 190, but the mover legally holds axis separation up to 225 and wanders ±150 in depth — after the first strike the Vanguard settled at 209 axis / larger 2D and **never attacked again**. Fix: the range gate now uses **combat-axis separation ≤ 240** (covers the whole hold band); hit/whiff still depends on true geometry at the impact moment, and impact reach was retuned to 225 so in-band strikes can connect while depth-dodges still whiff.
2. **`SetActorHiddenInGame` positional arg silently bound to the `self` pin** — telegraph never toggled (visible "!" parked in the world). Same family as the known own-function positional gotcha: **nodes whose first data pin is `self` need keyword args** (`:bNewHidden true`). All four call sites rewritten.
3. `Utilities|Array|MakeArray` cannot be typed via DSL for enum-array pins (wildcard mismatch) — created via `create_node`, connected to `ObjectTypes` (wildcard resolves on connect), element set to `ObjectTypeQuery3`. Same-script immediate compile after graph surgery can report stale errors — recompile in a fresh call before trusting a failure.
4. Paren-containing type ids (`Math|Float|Max(Float)`, `Utilities|String|ToString(Float)`) **do parse** in the DSL (confirmed against the §7 vanguard graph and used in `HandleDamage`) — §11.9's avoidance was over-cautious; both approaches work.

### 16.5 Compile / save / validation evidence

All four touched Blueprints compile clean (`warnings_as_errors=true`) and are saved: driver, mover, character, controller. PIE (Lvl_DuelGraybox), observed via live state sampling:

- Driver spawns, activates, resolves all three refs; telegraph hidden at start; camera and mover activate normally.
- **Hit cycle:** windup observed (state 1) with telegraph visible and mover locked; player stood ground → exactly **−10 health**, telegraph hidden afterward, mover unlocked, cooldown re-rolled.
- **Whiff cycle:** on the next windup the player retreated to 500 cm → strike whiffed, **zero damage**.
- **Re-engage cycle:** subsequent windup after cooldown → hit for exactly −10 again.
- No spam: attacks separated by the 2.5–4 s cooldown (plus 0.6 s retry rolls); over the long debug session health stepped 100→…→0 in clean −10 increments and **clamped at 0** (no death, as scoped).
- Vanguard health remained 100 (its damage graph untouched); ordering, arena bounds, depth lane, live camera (rig==camera-manager), and zero roll all verified after the cycles.
- Log sweep: **zero Accessed None / runtime errors** for the entire session (the pattern including old authoring entries now returns empty because the session log rotated — checked with the full historic pattern too).

### 16.6 PENDING HUMAN PIE

- Telegraph readability (is the red "!" clear enough, 0.7 s windup fair?).
- **Interruption by hand**: punch the Vanguard during a windup — expect telegraph to vanish, no strike damage, movement resuming after its hit-react (tool-validated only by graph logic: montage-during-windup → cancel; no MCP path can simulate a real punch).
- Player hit feedback feel (print + `BP_CameraShake_Hit_Player` + hit-react montage under the duel camera).
- Whiff fairness at various angles/depths; whether reach 225 feels honest.
- Full punch-loop regression by hand (Vanguard health bar, sparks, shake, hit-react — logic untouched).
- Strike-phase trades: being punched during the 0.6 s strike (after windup) does NOT cancel the strike — both hits can land ("trade"). Confirm it reads acceptably (documented limitation, montage-signal ambiguity makes clean strike-cancel out of scope).

### 16.7 Known limitations

- Player health has no regen/reset UI — restart PIE to reset (health floors at 0 and further strikes print 0; no death by design).
- Trades during the strike phase (above). Interruption works only during wind-up.
- The telegraph "!" yaw is fixed to the +Y camera side (correct for `CameraSideSign=+1`; flip needs the driver's yaw updated — one value in `ActivateDriver`).
- The Vanguard attacks whenever conditions pass, including while the player punches — no politeness system (out of scope).
- Player "alive/damageable" gate is trivially true (no death state exists to check).

### 16.8 Human PIE test

1. Open `Lvl_DuelGraybox`, press Play. 2. Stand near the Vanguard; watch for the red "!" above its head. 3. Stay put once: one strike hits, "Player Health: 90" prints with a small shake and player hit-react. 4. On the next "!", dash away (A) or into depth (W/S): the strike whiffs, no damage. 5. Close to contact and pressure it — attacks should come at readable intervals, never back-to-back. 6. Punch (LMB) during a "!" — the attack should cancel with its hit reaction; movement resumes after. 7. Confirm recovery pauses it after each swing. 8. Confirm your punch loop (Vanguard health bar/sparks/reaction) still works. 9. Kill switches: `bEnableVanguardBasicAttack` (controller) removes only the attack; tuning lives on `BP_VanguardBasicAttackDriver` class defaults.

### 16.9 Git manifest

Created: `Content/AscendantImpact/Duel/BP_VanguardBasicAttackDriver.uasset`. Modified: `Content/AscendantImpact/Duel/BP_VanguardDuelMover.uasset` (movement-lock interface), `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` (health receiver), `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` (toggle + spawn chain), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. Untouched: camera rig, Vanguard proxy, levels, input, animation assets. `Config/DefaultEditorPerProjectUserSettings.ini` untouched/unstaged.

---

## 17. Milestone 9 — Strike fairness polish + first Duel HUD (2026-08-02, branch `feature/duel-hud-strike-polish`, from checkpoint 7097474)

**Delivered:** a fairer, clearer Vanguard strike (longer telegraph, smaller indicator, pre-impact interrupt window, honest depth dodging, restrained player-hit shake) and the first fighting-game top-screen Duel HUD with both health bars driven by the authoritative health values. Blueprint-only; no blocking/dodging systems, death, rounds, meters, or Attack A.

### 17.1 Strike fairness changes (`BP_VanguardBasicAttackDriver` + telegraph + shake)

| Aspect | Old | New |
|---|---|---|
| `WindupDuration` | 0.7 s | **1.1 s** |
| Telegraph "!" `worldSize` | 150 | **75** (50% smaller, still above the head at +140) |
| Interrupt window | wind-up only (montage signal) | **any player hit from telegraph start until the impact check fires** — implemented by caching `WindupStartVanguardHealth` at `BeginWindup` and cancelling in states 1 AND 2 (pre-impact) when the Vanguard's `Health` drops below it. Post-impact hits do not retroactively cancel. The montage-based wind-up check was replaced by this strictly more precise health signal. |
| Depth dodge | 90-radius sphere alone (hits up to ~90 cm depth offset) | sphere kept as candidate detection + **`ImpactDepthTolerance` = 55 cm** gate: damage only if |playerY − vanguardY| ≤ 55 at impact. Meaningful W/S sidesteps whiff; incidental jitter (<55) doesn't grant immunity. |
| Cooldowns / initial delay / decision chance | unchanged (2.5–4.0 / 1.5 / 0.65) — no spam introduced | same |

Impact geometry final: forward offset 100, sphere radius 90, class-filtered to the player, one check per strike (`bImpactDone`), depth gate 55. Cancelled attacks hide the telegraph, unlock movement (the mover's own montage pause covers the remaining hit-react time), apply no damage, and reroll the full cooldown. **Remaining trade window:** only same-frame punch-vs-impact ordering (~1 frame), documented.

**Player-hit camera shake** (`BP_CameraShake_Hit_Player`, WaveOscillator pattern — asset is independent of the enemy shake, which is untouched): Duration 0.35→**0.18**, BlendOut 0.1→0.08, amplitudes X/Y 1→0.5, Z 3→1.2, Pitch 1→0.6, Yaw 1→0.4, **Roll 1→0** (no roll wobble at all). Frequencies unchanged.

### 17.2 UI_DuelHUD (named per the project's existing `UI_` widget convention, at `/Game/AscendantImpact/UI/`)

**Hierarchy:** `RootCanvas` (CanvasPanel) → `PlayerHealthBar` (ProgressBar, anchors (0,0), pos (40,42), 480×26, green fill, LeftToRight — drains from the center-facing end), `VanguardHealthBar` (ProgressBar, anchors (1,0), alignment (1,0), pos (−40,42), 480×26, red fill, **RightToLeft** — mirrored drain), `PlayerLabel` "PLAYER" (40,12), `VanguardLabel` "VANGUARD" (−40,12, right-justified). Both bars are widget variables.

**Health sources (authoritative, no duplicates):** player = `CurrentHealth / MaxHealth` (the §16 receiver); Vanguard = `Health / 100` (matching `BP_VanguardProxy`'s own hardcoded max — its graph divides by 100 identically).

**Update path:** `Construct → SetTimerByFunctionName("TimerUpdate", 0.05 s, looping)`. `TimerUpdate` → resolve refs (only while invalid — no per-frame global searches after init; on first Vanguard resolve it also hides the world-space bar, see 17.3) → `UpdateHealthBars(WorldDeltaSeconds)`: reads both health values immediately, `FInterpTo`s `DisplayedPlayerPct`/`DisplayedVanguardPct` at `HealthBarInterpSpeed` 8 (~0.3 s visual settle), `SetPercent` on both bars. Values are inherently 0–1 (health floors at 0, caps at max), so bars clamp cleanly.

**Creation:** `BP_ThirdPersonPlayerController` gained `bEnableDuelHUD` (instance-editable, default true) + `DuelHUD` ref; the BeginPlay duel chain (inside the IsLocalPlayerController branch — never for non-local) appends `CreateWidget(UI_DuelHUD, OwningPlayer=self) → AddToPlayerScreen → save ref`. Single creation point, no duplicates.

### 17.3 World-space Vanguard bar

Not deleted, logic untouched: when the HUD resolves the Vanguard it calls `SetVisibility(false)` on the `HealthBarWidget` component — runtime-only and fully reversible (with `bEnableDuelHUD=false` the HUD never spawns, nothing hides the world bar, the §7 checkpoint look returns). Verified live: component `bVisible=false` with HUD on.

### 17.4 Failures and fixes this run (tooling-relevant)

1. **`bEnableDuelHUD` default silently stayed false** — the first wiring script errored (bad anchor search) *before* its set-default step ran; the HUD never spawned in the first validation PIE. Lesson: when a multi-step script dies, explicitly re-run the tail steps.
2. **`CreateWidget` without `OwningPlayer` → `AddToPlayerScreen` no-ops** (widget existed, ref stored, never on screen). The template's own call passes `self`; wired the chain's existing `K2Node_Self_0` into the pin.
3. **UMG template ghost nodes:** the widget's stock `Tick`/`Construct` nodes are disabled placeholder ("ghost") nodes — `add_event` returns them, connections compile, but they generate nothing. Even a freshly created Tick event did not fire for this widget (suspected stale `bHasScriptImplementedTick`). **Robust pattern: delete the ghost `Construct`, create it fresh via `add_event`, and drive updates with `SetTimerByFunctionName` looping instead of widget Tick.** Verified firing (marker print observed, then removed).
4. `Class|ProgressBar|SetPercent`'s data pin is `Percent` (not `InPercent`) — the DSL's pin-name error listing is exact and trustworthy.
5. Widget component variables live under `Variables|<WidgetName>|Get...` (e.g. `Variables|UI_DuelHUD|GetPlayerHealthBar`), not `Variables|Default|…`.

### 17.5 Compile / save / validation evidence

All five touched Blueprints compile clean (`warnings_as_errors=true`): attack driver, UI_DuelHUD, controller, player-hit shake, (mover untouched this run). Saved. PIE evidence (Lvl_DuelGraybox, live sampling + screenshot):

- **TEST A (hit):** wind-up observed (1.1 s tuning confirmed live), telegraph visible during wind-up, standing in range → exactly −10; top-left bar tracked (displayed 0.800→0.700 after a later hit, always matching health/100).
- **TEST B (retreat whiff):** retreat during wind-up → zero damage.
- **TEST C (depth whiff):** 130 cm depth offset at 150 cm axis range → zero damage (tolerance 55 verified live in tuning read).
- **TEST D (interrupt):** health-drop cancel logic verified by graph readback; runtime interruption requires a real punch — PENDING HUMAN (same MCP limitation as §16).
- **TEST E (vanguard bar):** right bar reads the proven `Health` value through the identical update path as the player bar (which was validated live); visual confirmation of a punch-driven drain is PENDING HUMAN.
- **TEST F (zero/reset):** health floors at 0 (§16 evidence stands); fresh PIE resets to 100 → bars full (verified: new session read 100 → stepped −10s; displayed matched exactly).
- **HUD on screen:** screenshot shows PLAYER (green, ~70%, drained toward center) top-left, VANGUARD (red, full) top-right, labels readable, safe margins, no world-space bar over the Vanguard, fighters/camera/ordering intact.
- **Regressions:** ordering/bounds/lane/camera checks passed in-session; zero Accessed None / runtime errors in the log across all PIE sessions.
- Debug scaffolding (marker prints, dead Tick path) removed before commit; final widget event graph is exactly `Construct → timer`.

### 17.6 PENDING HUMAN PIE

- Telegraph readability at the smaller 75 size and 1.1 s pacing.
- Interrupt-by-hand: punch during the wind-up AND early strike (pre-impact) — both should cancel; a punch after the hit lands should not retro-cancel.
- Depth-dodge feel (is 55 cm fair?), retreat whiff feel.
- Player-hit shake: restrained but noticeable?
- Vanguard bar draining visually on punches; smooth ~0.3 s bar interpolation feel.
- HUD readability across viewport sizes.
- Full regression sweep by hand (punch loop, hit-react, sparks, close-contact spacing, boundaries).

### 17.7 Known limitations

- Same-frame punch/impact trade (~1 frame) remains.
- Vanguard max health hardcoded as 100 in both its own graph and the HUD divisor (single source would need proxy surgery — deferred).
- No death/round/reset at 0 health (intentional); bars sit empty, fight continues.
- The world-space bar hide is HUD-driven: disabling the mover/attack but keeping the HUD still hides it (acceptable).
- Telegraph yaw still fixed to the +Y camera side.

### 17.8 Git manifest

Created: `Content/AscendantImpact/UI/UI_DuelHUD.uasset`. Modified: `Content/AscendantImpact/Duel/BP_VanguardBasicAttackDriver.uasset` (fairness), `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` (HUD toggle/chain), `Content/Variant_Combat/Blueprints/BP_CameraShake_Hit_Player.uasset` (restrained shake), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. Untouched: mover, camera rig, Vanguard proxy, character, levels, input, anims. `Config/DefaultEditorPerProjectUserSettings.ini` untouched/unstaged.

---

## 18. Milestone 10 — Assignment 5: goal-agent-selected knockout state (2026-08-02, branch `feature/assignment5-knockout`, from checkpoint fbb6487)

**Context:** this milestone was selected by the Assignment 5 goal-oriented coding agent (fight-game repo, `assignment-05/`, branch `assignment/goal-oriented-coding-agent`). The deterministic scanner read the tracked GDD (`gdd/ascendant-impact-gdd-v0.4.md`), design brief, this blackboard, CLAUDE.md, the .uproject, the Git manifest, and an MCP-produced Blueprint inventory; scored nine candidate gaps on six dimensions with penalties; and selected **"Zero-health knockout / visible fight-end state" (score 30/30, no penalties)** — GDD evidence: "one complete duel with win and loss", "Win / Loss … selected fighter health reaches zero — Complete duel loop". Gated candidates (Attack A pipeline, Phase 2) correctly scored negative and were rejected in writing.

### 18.1 Implementation — BP_DuelKnockoutCoordinator

**`/Game/AscendantImpact/Duel/BP_DuelKnockoutCoordinator`** — fifth runtime-spawned actor in the controller chain, gated by new instance-editable **`bEnableKnockout`** (default true). Per tick (with the standard resolve-while-invalid ref pattern for player/vanguard/mover/driver):

- If a fighter's authoritative health (`BP_VanguardProxy.Health` / `BP_ThirdPersonCharacter.CurrentHealth`) reaches ≤ 0 and that fighter is not already KO'd (one-shot flags `bVanguardKO`/`bPlayerKO`):
  1. `StopDuelSystems()`: attack driver `CancelAttack()` (hides any active telegraph, aborts wind-up/strike state) then `SetActorTickEnabled(false)`; mover `SetActorTickEnabled(false)`. The duel brain stops for good — no more attacks or movement decisions in either KO direction.
  2. Defeated fighter: `CharacterMovement.DisableMovement` (MOVE_None — player input and mover input both dead at the movement layer); player-KO additionally sets `bIsAttacking=true` so the punch input chain's re-entry guard permanently blocks attacks.
  3. Fall: `MM_Death_Front_01` via the project-standard `PlaySlotAnimationAsDynamicMontage` on `DefaultSlot` (blend-out 0 so it can't return to idle).
  4. After `RagdollDelay` (1.4 s, editable): capsule collision → NoCollision, mesh collision profile → Ragdoll, mesh `SetSimulatePhysics(true)` — the fighter crumples from the fall pose and **stays down permanently**; the camera rig's facing writes become invisible on a simulated mesh, and the disabled capsule means no further punch overlaps can hit the corpse (no post-KO damage events).

The camera rig and HUD deliberately keep running: the camera stays framed on both actors; the HUD keeps showing the empty bar. No rounds, rematch, victory UI, respawn, cinematics, or scoring — exactly the packet scope.

**Also modified:** `BP_ThirdPersonPlayerController` (toggle + spawn chain append after the HUD). **Minimal metadata change:** `BP_VanguardProxy.Health` and `BP_ThirdPersonCharacter.CurrentHealth` marked instance-editable — zero graph/behavior changes; needed because `ObjectTools.set_properties` on runtime instances only accepts instance-editable properties (new tooling gotcha), and it doubles as a designer tuning affordance.

### 18.2 Validation evidence (PIE, Lvl_DuelGraybox)

All modified Blueprints compile clean (`warnings_as_errors=true`). Live-state evidence across three PIE sessions:

- **TEST A (Vanguard KO):** health→0 ⇒ `bVanguardKO=true`, driver state 0 with telegraph hidden and tick disabled, Vanguard `MOVE_None`, mesh `bSimulatePhysics=true` after the 1.4 s delay, HUD vanguard bar exactly 0.000, camera roll −5e-08, state unchanged over a 3 s stays-down watch. **Player untouched by the Vanguard's KO** (clean-trace: player `MOVE_Walking`, KO flag false, attack flag false).
- **TEST B (Player KO):** `bPlayerKO=true`, `bIsAttacking=true` (attack input blocked), `MOVE_None`, ragdolled, HUD player bar 0.000. **Bonus organic validation:** in the long first validation session the player reached 0 purely from real Vanguard strikes and the coordinator KO'd them through the genuine damage path — not only via the test lever.
- **TEST C (Reset):** PIE restart ⇒ healths reset (player already re-taking real strikes: 100→70 during the sampling window — the duel loop restarts by itself), both fighters `MOVE_Walking`, all four KO/ragdoll flags false, attack flag false. No stale state.
- **TEST D (Regression):** pre-KO in the same sessions: Vanguard moving (200+ cm sampled), attack cycles running (state/cooldown live), strikes landing for exact −10 steps, HUD tracking, ordering/camera stable.
- **Log:** zero Accessed None / Blueprint runtime errors across all sessions. Screenshot captured (empty VANGUARD bar, standing player, downed opponent) and copied into the assignment evidence folder.
- KO detection was triggered via direct health writes (the damage-to-zero path was already proven in §16/§17 and organically in TEST B); punch-driven Vanguard KO by hand is PENDING HUMAN.

### 18.3 PENDING HUMAN PIE

- Visual quality of fall + ragdoll handoff (1.4 s `RagdollDelay` tunable); death-anim choice (`MM_Death_Front_01`) vs. direction of the killing blow.
- Punch the Vanguard to 0 by hand (10 punches) and confirm the KO fires from real damage; then let the Vanguard win a fresh round.
- Camera framing feel while one fighter is a ragdoll (midpoint uses capsule positions; the simulated mesh can drift from its capsule).
- HUD/interrupt/whiff regression sweep by hand.

### 18.4 Known limitations

- The ragdolled mesh may slide slightly from its capsule position; the camera frames capsules (graybox-acceptable).
- Post-KO the surviving player can still walk/jump/punch the air freely — intentional (no victory state yet).
- The Vanguard's world-space life bar stays hidden by the HUD as before; at KO the head position is on the ground.
- Player KO leaves mouse/keyboard live but movement-dead and attack-blocked; Esc/PIE restart is the only reset (by scope).

### 18.5 Git manifest (this milestone)

Created: `Content/AscendantImpact/Duel/BP_DuelKnockoutCoordinator.uasset`. Modified: `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` (toggle + chain), `Content/Variant_Combat/Blueprints/BP_VanguardProxy.uasset` + `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` (instance-editable health metadata only), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. `Config/DefaultEditorPerProjectUserSettings.ini` untouched/unstaged.

---

## 19. Milestone 11 — Knockout fall-transition polish (2026-08-02, branch `feature/knockout-transition-polish`, from 64f97f5)

**Problem:** the §18 knockout read as hit → upright reset → canned fall: the final hit-react bent the fighter, the mesh blended back toward the standing pose, `MM_Death_Front_01` restarted from standing, and ragdoll only took over 1.4 s later.

**Fix (BP_DuelKnockoutCoordinator only):**

- **Old sequence:** KO → stop systems → DisableMovement → play `MM_Death_Front_01` (blend-out 0) → ragdoll at `RagdollDelay` **1.4 s**.
- **New sequence:** KO → stop systems (attack cancel + driver/mover ticks off) → DisableMovement (+ player attack block) → the already-playing final **hit-reaction montage remains the visible pose** → ragdoll at `ImpactToRagdollDelay` **0.2 s** (exposed, provisional 0.15–0.25 band) directly from the mesh's currently evaluated pose: capsule collision off, mesh profile Ragdoll, `SetSimulatePhysics(true)`, **`WakeAllRigidBodies`** (new). No impulse. No death montage in the default path.
- **Why `MM_Death_Front_01` was bypassed:** dynamic slot montages always start from their authored standing pose, guaranteeing the visible reset; physics inheriting the live mid-hit-react pose collapses from exactly where the hit left the fighter.
- **No sync step needed:** `SetSimulatePhysics` starts from the current evaluated pose and the capsule is never written — measured capsule displacement across the KO→ragdoll transition was **0.0 cm** for both fighters.

**Assets changed:** `Content/AscendantImpact/Duel/BP_DuelKnockoutCoordinator.uasset` only (`RagdollDelay` removed, `ImpactToRagdollDelay` added at 0.2; `KnockoutVanguard`/`KnockoutPlayer`/`ApplyRagdoll`/`UpdateKnockout` rewritten). Compile clean with `warnings_as_errors=true`; saved.

**PIE evidence (Lvl_DuelGraybox):** both KOs — flags one-shot, ragdoll simulating within the 0.7 s sample window, capsule moved 0.0 cm, driver stopped with telegraph hidden, stays down over 2.5 s+, HUD bars exactly 0.000, camera roll −6e-08, player KO blocks attack (`bIsAttacking=true`) and movement (`MOVE_None`); PIE restart resets all flags/health/movement; zero runtime/Accessed-None errors.

**Remaining limitations:** ragdoll settle behavior depends on the template physics assets (no per-bone tuning); the 0.2 s window means the fall pose depends on which hit-react frame it lands on (variance is intentional but PENDING HUMAN for feel); no impulse means low-energy collapses — an optional small directional impulse is a documented future knob, deliberately not added.

---

## 20. Milestone 12 — Vanguard directional locomotion presentation (2026-08-02, branch `feature/vanguard-locomotion-presentation`, from f89cf38)

**Root cause of the sliding (measured, not assumed):** the template already ships full directional locomotion — `BS_Idle_Walk_Run` is a 2D blendspace (Direction −180..180 with 8-way walk@300/jog@600 samples + idle@0) and `ABP_Unarmed` computes an UNCLAMPED `Direction` whenever `bOrientRotationToMovement` is false (exactly the Vanguard's configuration). Live PIE sampling of the anim instance proved direction worked (advance dir≈0 @300, retreat dir≈±175 @150, lateral dir≈118 @120). The actual defect was **`ShouldMove = GroundSpeed > 0.01 AND CurrentAcceleration ≠ 0`** — authored for held player keys. On the AI-driven Vanguard, every braking window and input gap (hold-band stops, decision gaps, montage pauses) zeroed acceleration while speed was still 200+ cm/s, snapping the state machine to Idle mid-slide (captured live: `speed 205, ShouldMove false`). §12.8/§14.5's "no strafe/backpedal blendspace" notes were wrong and are superseded by this measurement.

**Architecture: Option B (minimal form), player untouched.** `AssetTools.duplicate` of `ABP_Unarmed` → **`/Game/AscendantImpact/Animation/Vanguard/ABP_VanguardLocomotion`**; only its EventGraph was rewritten: identical logic except `ShouldMove = GroundSpeed > 3.0` (speed-only; braking 2048 zeroes speed in ~0.15 s so idle onset stays snappy without mid-slide idling), plus an `IsValid(MovementComponent)` guard around the update (the DSL rewrite replaces the template's silently-null-tolerant PropertyAccess nodes with hard variable reads, which spammed Accessed-None in editor-preview contexts until guarded — new gotcha). Assigned via the mesh `animClass` on the proxy CDO **and** on the placed level instance (the §7e stale-instance gotcha struck again: the instance kept `ABP_Unarmed_C` after the CDO change), persisted with `save_assets([])`. No new blendspace was needed; no playback-rate scaling was needed (the blendspace's speed axis already matches foot speed to velocity: advance 300 = pure walk sample; retreat 150 and depth ~120 blend idle↔walk at matching rates). `AnimGraph`, `DefaultSlot`, and the Locomotion/Main-States machines are untouched duplicates — montage compatibility by construction.

**Movement-animation mapping (all in-place, no root motion):** stationary → `MM_Idle`; advance 300 → `MF_Unarmed_Walk_Fwd` (±diagonals); retreat ~150 → idle↔`MF_Unarmed_Walk_Bwd` blend; depth ~120 → idle↔`MF_Unarmed_Walk_Left/Right` blend; diagonals blend via the 8-way samples. Vanguard keeps facing the player (rig-driven); direction comes from velocity vs. facing.

**Validation (PIE, Lvl_DuelGraybox):** compile clean (`warnings_as_errors=true`) on the new ABP and proxy. TEST A idle: four consecutive stable `speed 0 / move false` samples. TEST B advance: `speed 300, dir −3..+6, move true` throughout. TEST C/D: retreat and lateral (dir 97.7 @ 120) engaged with correct directions; **zero occurrences of the glide signature (speed>50 with move=false) across all sampling**. TEST E: player health dropped to 70 from real strikes → `MM_Attack_02` plays and impacts through the new anim instance (DefaultSlot path proven end-to-end). TEST G: knockout ragdolls (simulate=true) and stays down — locomotion never resumes over ragdoll. TEST H: PIE restart → new ABP live on the instance, flags reset, health 100, physics off, locomotion running. Log: the only Accessed-None entries are pre-guard (timestamped before the fix); both validation sessions clean. Incidental: `save_assets([])` re-saved `ABP_Unarmed` with zero logical change (graph/vars verified identical, compiles clean) — restored from git so the shared player ABP remains untouched in the manifest.

**PENDING HUMAN PIE:** overall gait feel and foot-slide quality at 300/150/120 cm/s; hit-reaction visual override and return to locomotion (structurally unchanged; damage path proven); whether walk-speed advance should look more like a combat jog (that would need speed-axis or gameplay-speed tuning — deliberately not done); idle "combat stance" flavor (MM_Idle is a relaxed idle — asset-authoring question, out of scope).

**Git manifest:** NEW `Content/AscendantImpact/Animation/Vanguard/ABP_VanguardLocomotion.uasset`; MODIFIED `Content/Variant_Combat/Blueprints/BP_VanguardProxy.uasset` (mesh animClass), one `Lvl_DuelGraybox` external-actor package (instance animClass), `docs/agent/PROTOTYPE_BLACKBOARD.md`, `CLAUDE.md`. Player ABP untouched. Personal editor config unstaged.
