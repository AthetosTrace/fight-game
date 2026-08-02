# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Ascendant Impact is an Unreal Engine **5.8** PC project, **Blueprint-only** — there is no `Source/` folder, no C++ build, and no traditional lint/test commands. All implementation lives in binary `.uasset`/`.umap` files under `Content/`.

Scope is a single-duel prototype: the player (Echo or Nova) fights Crimson Vanguard, who uses authored, deterministic AI. Design/planning source of truth is the separate `fight-game` repository (locally at `C:\Users\Tonys ProArt\Documents\fight-game`); this repo is the Unreal implementation only.

## Operating rules (from AGENTS.md — binding)

- Blueprint-first; do not add C++ without approval.
- Do not directly edit binary Unreal assets on the filesystem, and never import assets or install plugins/frameworks without explicit human approval.
- Only Attack A is enabled until its complete loop passes; Attacks B–D stay planned and disabled. No runtime LLM/generative-NPC behavior. No scope beyond the single-duel prototype (no PvP, multiplayer, extra fighters/arenas, progression).
- Report planned changes before modifying project architecture.
- Never commit `Binaries/`, `DerivedDataCache/`, `Intermediate/`, `Saved/`, `.vs/`, or plugin-local generated folders (already in `.gitignore`).

## How to work on this project

All editing happens through the **unreal-mcp** MCP server against the live editor session (the editor must be open). Start with `mcp__unreal-mcp__list_toolsets`, then `describe_toolset` for schemas, then `call_tool`. Key toolsets:

- `editor_toolset.toolsets.blueprint.BlueprintTools` — Blueprint graph editing (DSL read/write, nodes, variables, compile).
- `editor_toolset.toolsets.object.ObjectTools` — **always** `list_properties` before `get/set_properties`; property names cannot be guessed and wrong names fail silently.
- `editor_toolset.toolsets.scene.SceneTools`, `asset.AssetTools`, `data_table.DataTableTools`, `UMGToolSet` — level, assets, DataTables, widgets.
- `EditorToolset.EditorAppToolset` — PIE start/stop, viewport capture, selection.
- `AutomationTestToolset` — the closest thing to a test runner: `DiscoverTests()` → `ListTests()` → `RunTests()` → `GetTestResults()`.

Validation standard: `compile_blueprint(warnings_as_errors=true)` must come back clean after every Blueprint change, then save the asset via MCP. There is no MCP asset-validation tool; suggest the human run **Tools → Validate Assets** for final sign-off. Functional verification is a human PIE pass — write test instructions rather than assuming success.

### Known tooling gotchas (hard-won; see docs/agent/PROTOTYPE_BLACKBOARD.md §6 and §11.9 for detail)

- **Git**: `.git` is owned by a different Windows user; every git command must be invoked as `git -c safe.directory="E:/UnrealProjects/Production/AscendantImpact" ...` (do not modify global git config).
- **OFPA level saves**: `Lvl_ThirdPerson` uses One-File-Per-Actor. Newly placed actors cannot be saved to disk via MCP (`save_actor` fails with "Asset does not exist") — a human Ctrl+S in the editor is required to persist them.
- **Stale per-instance component data**: actors placed in the level *before* a component was added/configured on their Blueprint class keep a frozen snapshot that overrides both `set_properties` and `reset_properties`. Fix by deleting and re-placing the instance.
- **Blueprint DSL quirks**: `(event ...)` sugar can't create Enhanced-Input events or match existing custom events — place nodes with `add_event`/`create_node` (find real type ids via `find_node_types`) and wire with `connect_pins`. Function graphs cannot contain latent nodes (`Delay`); use event-graph contexts. Array input pins reject literal defaults — feed them a `MakeArray` node. Bool variables drop the `b` prefix in accessor names (`bIsAttacking` → `Get/SetIsAttacking`), and variable accessor type ids include the variable's category (`Variables|DuelCamera|GetDuelModeActive`, not `Variables|Default|…`). `SpawnActorFromClass`'s `SpawnTransform` by-ref pin also rejects literal defaults — wire a `MakeTransform` node. Type ids containing parentheses (`Math|Float|Clamp(Float)`) break the S-expression parser — use `select` ternaries / component math instead. Own-function calls need keyword args (`:Param val`) or positional args may bind to `self`. `get_node_type_pins` instantiates a probe node in the graph — delete it afterward.
- **UserDefinedStruct/Enum assets cannot be created via MCP** — that is a manual editor step for the human.
- `CaptureViewport` with a manual transform is unreliable during PIE; verify changes by reading graphs/properties back, not screenshots.

## Architecture and current state

- **Player**: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter` (Quinn mesh + `ABP_Unarmed`). Attack input `IA_Attack` (LMB, mapped in `/Game/Input/IMC_Default`) plays `MM_Attack_01` via `PlaySlotAnimationAsDynamicMontage` on `DefaultSlot` — no Montage assets are authored; slot-based dynamic montages are the pattern. Hit detection is a delayed `SphereOverlapActors` → native `ApplyDamage`.
- **Enemy proxy**: `/Game/Variant_Combat/Blueprints/BP_VanguardProxy` (Manny mesh, same `ABP_Unarmed`). Handles `ReceiveAnyDamage` → health decrement, `NS_Damage` VFX, camera shake, hit-react montage, and a screen-space `WidgetComponent` health bar (`UI_LifeBar`) initialized via an `EnsureHealthBarWidget` function — never `AddToViewport`.
- **Attack data (PAUSED)**: the `S_VanguardAttackDef` struct / `DT_VanguardAttacks` DataTable route under `/Game/AscendantImpact/Data/` is on hold — do not continue it until the human unpauses it. When it resumes: import verbatim from the fight-game repo's approved CSV (`data/unreal/DT_VanguardAttacks.csv`) and never invent values marked OPEN in `fight-game/docs/unreal/ATTACK_DATA_SOURCE_AUDIT.md`.
- **Feedback assets** live under `/Game/Variant_Combat/` (`UI_LifeBar`, `NS_Damage`, `BP_CameraShake_Hit_*`).
- **Not yet built (gated)**: Vanguard AI (`BT_CrimsonVanguard`, `BB_CrimsonVanguard`, AI controller), Impact Windows, Ascension Meter, dodge/counter, death-at-zero-health. The Attack A AI plan (`ATTACK_A_IMPLEMENTATION_PLAN.md` in fight-game) is gated on human sign-off documents there — confirm preconditions before starting it.

## Current milestone: camera-first graybox (Duel Camera)

Approved decision (2026-08-01): remain **Blueprint-only** for this milestone. Do not add a C++ module, C++ class, build target, or `Source/` folder — the goal is visual validation, not architectural conversion.

The Duel Camera is to be implemented with clean Blueprint functions/components with these behaviors:
- Constrained 2.5D side-profile framing.
- Midpoint tracking between the player and Vanguard.
- Smooth distance adjustment based on fighter separation.
- Stable combat-axis side — no live-control axis crossing.
- No mouse free-look.
- Limited depth movement.
- Both fighters facing each other.
- Later (not first pass): smooth height, offset, push-in, and limited-angle dominance bias.

**First implementation is limited to the stable profile camera and basic movement.** Dominance bias is deferred until the base framing is human-approved in PIE.

**Status: first pass implemented (see blackboard §11).** `/Game/AscendantImpact/Camera/BP_DuelCameraRig` is a runtime-spawned rig activated by `BP_ThirdPersonPlayerController` (gated by its `bEnableDuelCamera` bool, default true) via `SetViewTargetWithBlend` — no level placement, original third-person camera bypassed reversibly, all tuning exposed on the rig's class defaults. Awaiting human PIE approval before any dominance-bias work.

For reviewability, every camera work pass must document: exact Blueprint assets and functions; relevant variables with provisional defaults; graph descriptions; compile results; PIE acceptance criteria; human test results; and the exact Git file manifest.

## Working log

`docs/agent/PROTOTYPE_BLACKBOARD.md` is the running agent blackboard: current state, decisions, failures/fixes, and pending manual steps. Read it at the start of a session and update it as work progresses — it is the authoritative record of what is live in the editor vs. persisted to disk.
