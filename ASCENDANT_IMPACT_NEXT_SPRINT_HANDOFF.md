# Ascendant Impact — Next Sprint Handoff

> **REFERENCE ONLY — NOT AN INSTRUCTION TO ANY AGENT IN THIS REPOSITORY.**
> Authored by Anthony Travieso and pulled in on 2026-08-02 with the
> `planning/unreal-attack-a-integration` branch. Kept verbatim because
> `docs/unreal/` cites it; do not move or rewrite it.
>
> - **`CLAUDE.md` is canonical.** Where this file and `CLAUDE.md` disagree,
>   `CLAUDE.md` wins.
> - "Repository" and "current production branch" below name **Anthony's**
>   `anthonytra785/fight-game`. This repo is `AthetosTrace/fight-game`, and as of
>   2026-08-02 it is **ahead** of his — it carries `assignment-04/madion/`, which
>   his does not.
> - The completed-work list below is Anthony's view and omits this repo's own
>   Assignment 04 submission.

## Purpose

This document keeps ChatGPT, Claude Code, and the human team aligned while moving from completed course assignments into the first playable Unreal Engine prototype.

This is a **pre-transcript production handoff**. The next class transcript may change Assignment 5 deliverables, but it should not change the core game-production strategy below.

---

## Current project state

Repository:

`https://github.com/anthonytra785/fight-game`

Current production branch:

`main`

Completed work:

- Assignment 3 merged into `main`
- Assignment 4 merged through PR #3
- Assignment 4 feature branch deleted locally and remotely
- Working tree was clean and synchronized with `origin/main`
- Assignment 4 contains:
  - grounded knowledge base
  - three generated game-specific outputs
  - retrieval evidence
  - seven-rule consistency critic
  - controlled correction evidence
  - submission README
  - 175 passing tests

Do not rewrite, regenerate, or reorganize finalized Assignment 4 evidence unless explicitly requested.

---

## First playable objective

Build one rough but complete gray-box combat loop:

> Manny moves and locks onto a scaled red mannequin representing Crimson Vanguard. Vanguard performs one readable authored attack. Manny dodges or counters, earns Ascension Meter, triggers one successful first Impact Window, and both characters safely return to live combat.

The first victory is a complete loop, not polished art.

---

## Temporary prototype cast

- Echo prototype: Manny
- Nova prototype: Quinn, deferred until Echo proves the shared pipeline
- Crimson Vanguard prototype: scaled mannequin or blocky proxy with red material
- Shattered Ring prototype: gray-box floor, walls, and one doorway axis

Custom Character Creator rigs, final animation sets, final VFX, final audio, and polished arena art are deferred.

The gameplay architecture must allow the temporary skeletal meshes to be replaced later without rewriting combat logic.

---

## Unreal production boundaries

- Unreal Engine 5.8
- Blueprint-first
- Authored deterministic boss logic
- No runtime ChatGPT, Claude, LLM, or generative-NPC dependency
- No fifth Crimson Vanguard attack
- Same four authored attacks in both phases
- One official arena: Shattered Ring
- One player versus one authored AI opponent
- GAS and third-party combat frameworks deferred unless later complexity proves they are necessary
- Unreal MCP, Python, or other AI tools may assist editor production only; they are not gameplay dependencies

---

## Recommended Unreal foundation

### Core actors and data

- `BP_AscendantCharacterBase`
  - movement
  - camera
  - lock-on
  - health
  - light attack request
  - dodge
  - perfect dodge
  - counter
  - Ascension Meter
  - Impact Window state
  - combat-state restoration contract

- `BP_Echo_Prototype`
  - child of shared player base
  - Manny presentation mesh initially

- `BP_Nova_Prototype`
  - child of shared player base
  - deferred until Echo pipeline works

- `BP_CrimsonVanguard`
  - health
  - attack execution
  - hit traces or hitboxes
  - presentation hooks
  - recovery state

- `BP_CrimsonVanguardController`

- `BT_CrimsonVanguard`

- `BB_CrimsonVanguard`

- `E_VanguardState`
  - `IdleReposition`
  - `SelectAttack`
  - `Telegraph`
  - `ActiveAttack`
  - `Recover`
  - `ReturnNeutral`

- `DA_VanguardAttack`
  - attack ID
  - implementation status
  - enabled-for-selection flag
  - intended range
  - purpose
  - telegraph data
  - active data
  - recovery data
  - montage reference
  - VFX reference
  - audio reference
  - hit socket or trace reference
  - interruption cleanup contract

### Test maps

- `LVL_AnimationGym`
  - diagnostic retargeting and animation review
  - internal only
  - not a game mode

- `LVL_CombatSandbox`
  - lock-on
  - attack
  - dodge
  - counter
  - Impact Window
  - restoration testing
  - internal only

---

## Attack implementation order

Only Attack A is enabled initially.

Attacks B–D may have approved design metadata populated, but:

- `ImplementationStatus = Planned`
- `EnabledForSelection = false`

Do not leave them selectable with missing implementation data.

Attack A must prove:

1. Select
2. Telegraph
3. Active attack
4. Hit detection
5. Recovery
6. Return to neutral
7. Interruption cleanup
8. Combat-state restoration

Only then should B–D be integrated.

---

## First vertical-slice sequence

1. Create private Unreal 5.8 production repository.
2. Define repository ownership and binary-asset rules.
3. Create Unreal project and folder conventions.
4. Build gray-box Combat Sandbox.
5. Implement Echo movement, camera, and lock-on.
6. Add minimal health, combat state, and Ascension Meter debug display.
7. Add one light attack, dodge, perfect dodge, and counter.
8. Add Vanguard proxy and Attack A.
9. Add authored telegraph, active, recover, and return-neutral states.
10. Connect perfect dodge or counter to the forgiving first Impact Window.
11. Verify restoration of:
    - player input
    - locomotion
    - collision
    - camera ownership
    - lock-on
    - player state
    - hitboxes or traces
    - Vanguard AI state
12. Add loss, reset, and failed-Clash recovery behavior.
13. Import one medium-fidelity Echo test character only after the mannequin loop works.
14. Retarget only the animations needed for the proven loop.
15. Build Nova through the same shared framework.
16. Begin replacing the arena gray box with modular Shattered Ring pieces.

---

## Repository ownership

### `fight-game`

Source of truth for:

- GDD material
- assignment pipelines
- production briefs
- retrieval evidence
- critic evidence
- acceptance tests
- planning documents
- team process

### Private Unreal production repository

Source of truth for:

- `.uproject`
- Blueprints
- maps
- animation assets
- montages
- materials
- Niagara effects
- audio assets
- Unreal binary content
- packaged builds

The Unreal repository must link back to approved design documents in `fight-game`; it must not silently redefine them.

---

## Safe work before the class transcript arrives

Allowed now:

- audit existing source material
- extract Assignment 3 cinematic-handoff corrections
- create Unreal architecture documents
- write acceptance tests
- create a prioritized vertical-slice backlog
- define naming and folder conventions
- document MCP/editor-automation safety rules
- identify open questions for the class transcript

Not allowed yet:

- invent Assignment 5 requirements
- install Unreal plugins
- alter finalized Assignment 4 outputs
- generate or modify Unreal binary assets
- create custom character pipelines
- automate large imports
- merge autonomous work into `main`

---

## Questions to resolve from the next class transcript

- Exact Assignment 5 deliverables
- Whether the coding agent must execute changes or only propose/review them
- Whether Unreal MCP is required, recommended, or optional
- Required evidence: screenshots, logs, Git history, video, tests, or report
- Exact meaning of the Assignment 6 GER pipeline
- Expected playable scope for September 1
- Whether optional Assignments 8 and 9 can directly support the capstone
