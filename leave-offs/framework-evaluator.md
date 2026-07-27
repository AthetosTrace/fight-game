---
agent: framework-evaluator
status: complete
artifact: framework-evaluation.md
---

# Framework Evaluator — leave-off

**Date:** 2026-07-27 · `framework-evaluation.md` is on disk and complete (all nine
required sections).

## Recommendation

`USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE` — the approved plan in `design-brief.md`,
executed via the inspected `build-sequence.md`. Confidence: **high**.

- **n00dFighter / NFTiny:** REJECTED — paid multiplayer-replicated versus template;
  UE 5.8 support unverified; every Ascendant-specific system (six-state boss BT,
  perfect dodge, Impact Windows, Final Clash) would still be custom on top of
  unaudited foreign code; free NFTiny repo is a skeleton that requires the paid
  plugin.
- **TRUE Fighting Game Engine:** REJECTED — paid versus template; best version
  evidence (5.0–5.7, from third-party aggregators, not the seller) excludes 5.8;
  same custom-work burden.
- **C++ scaffold:** `NOT EVALUABLE — code not supplied` (repo-wide glob found zero
  `*.cpp` / `*.h` / `*.cs` / `*.uproject` / `*.uplugin` files).
- **Minimal hybrid:** collapses into the Blueprint-first plan — the plan already uses
  every proven public pattern a hybrid would borrow.

Matrix totals: Blueprint-first 94/100 · n00dFighter 47 · TrueFGE 46 · hybrid 94.

## Highest-risk uncertainty

Not the foundation — the execution risks the design brief already flags: **animation
sourcing/retargeting for the 6'10" Crimson Vanguard proxy (R4)** and **schedule
compression (R7: M4 functionally complete ~20 August to preserve tuning time; 36 days
remain and the Unreal MCP build phase has not started)**.

## Smallest proposed test

One buffered light attack in a **disposable UE 5.8 Third Person sandbox project /
throwaway branch** (main build untouched): one montage with two sections +
`ANS_ComboLink` + `IA_LightAttack`. **Pass:** press inside the window chains to
`Light_02`; no press drops the combo; press *before* the window is discarded.
**Fail:** any behavior absent → report to the designer before M1 proceeds. Delete
the sandbox afterward; version-control history preserved.

## Decisions still requiring human approval (all `OPEN — designer decides`)

1. Approve/reject the Blueprint-first foundation before any implementation.
2. Whether to spend anything evaluating a paid template (recommendation: no purchase).
3. Licensing acceptance for every asset entering the build (rights-review gate).
4. Whether/where to run the sandbox test.
5. All provisional timing/tuning values (design-brief §13/§14 — 29+ OPEN numbers).
6. Echo/Nova character-specific data-profile values (play-rate, speed, stance).
7. Any future architecture replacement (e.g., GAS post-course) — deferred.
