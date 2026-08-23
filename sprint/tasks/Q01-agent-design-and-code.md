---
id: Q01
track: Q
title: Adversarial QA agent — design and code
status: todo
assignment: 09
editor-required: false
depends-on: []
---

## Goal

An agent that runs inside the game and actively tries to break it, with a clear written
definition of what "broken" means.

## Why it matters

Assignment 09, due **27 Aug**. Rubric: Findings 4.0, Agent Logic 3.0, Structured Report
2.0, ReadMe 1.0. "Agent Logic" is explicitly about *trying to break the game rather than
playing it*, with a stated strategy.

And it is not a detour — this is Assignment 10's QA pass. Whatever it finds feeds `Q03`
and gets fixed before `G10` ships.

## Preconditions

- None for the code. Runs need the editor and are scheduled in `Q02`.
- **Text-only track.** Do not touch `.uasset` or `.umap` from this branch; `G` owns the
  editor and the assets.

## Steps

1. Write the oracle first — what counts as broken — before any driving code. Concrete
   targets, drawn from the measured constants in
   `game/docs/agent/PROTOTYPE_BLACKBOARD.md`:
   - **Boundary:** arena clamp ±650, min separation 78, side deadzone 20, crossing
     threshold 50, Vanguard depth lane.
   - **Stuck states:** landing inside min-separation, a crossing that never closes,
     ragdoll settling through the floor.
   - **Exploits:** punch-spam cadence, damage applied to an already-ragdolled fighter,
     `bCrossingActive` collision-ignore leaking after a knockout.
   - **Logic violations:** health below 0, both fighters knocked out, telegraph cancelled
     mid-windup, side sign flipping more than once per crossing.
2. Drive PIE over the Unreal MCP at `127.0.0.1:8000` — the same path the §22/§23 validation
   used. Real input injection where possible; scripted repositioning where it is not, and
   **say which is which in the report**.
3. Cycle behaviours continuously: move, jump, punch, probe boundaries, idle, spam.
   Randomise with a recorded seed so any finding can be reproduced.
4. Emit JSON per finding with at least `location`, `error_type`, `game_context` — plus
   seed and reproduction steps, because a report another developer can act on immediately
   is the actual bar.
5. Account for the known gotchas: PIE advances in real time between MCP calls, so an idle
   agent takes live hits; compiling a Blueprint mid-PIE kills Slate-injected input.

## Done when

- [ ] The oracle is written down before the driving code, and committed.
- [ ] The agent cycles behaviours continuously without hand-holding.
- [ ] Findings serialise to JSON with location, error type, game context, seed, and repro
      steps.
- [ ] Committed on `assignment-09/adversarial-qa`. No asset files touched.

## Log

- 2026-08-23 — created.
