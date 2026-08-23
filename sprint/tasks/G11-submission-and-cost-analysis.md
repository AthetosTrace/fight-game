---
id: G11
track: G
title: A10 submission — pipeline audit and cost analysis
status: todo
assignment: 10
editor-required: false
depends-on: [G10, N01]
---

## Goal

The filled-in Assignment 10 form and the one-page audit.

## Why it matters

Five rubric criteria, and three of them are answered here rather than in the engine.

## Preconditions

- `G10` complete — there is a link and a video.
- `N01` complete — cost analysis needs **real** token counts. The rubric says "calculated
  from the actual content generation run, not a hypothesis."

## Steps

1. **Student and game overview** — name, title, concept brief.
2. **Deliverable 1** — the itch.io link.
3. **Deliverable 2** — repo link (`AthetosTrace/fight-game`) and the pipeline run video.
   Target engine Unreal 5.8. Describe the automated flow: the arena pipeline emits a plan,
   the materializer builds it into the level through the Unreal MCP, and the octagon that
   results is the arena the shipped match is fought in.
4. **Deliverable 3, part 1** — what the pipeline produced (the octagon and its checkpoints;
   Assignment 06's attack CSV; Assignment 07's player-facing copy if any shipped), what
   manual steps remain, what would remove them.
5. **Part 2, architectural reflection** — one decision to change and the specific
   alternative. Candidates worth considering: the match-state ownership choice recorded in
   `G05`; driving the editor through MCP payload scripts rather than a commit-time
   generator; the octagon built as a payload script rather than a data asset the pipeline
   emits.
6. **Part 3, cost analysis** — total actual run cost from the instrumented runs, the most
   expensive step, and an honest read on solo-dev sustainability.
7. **Part 4, mid-project cost reduction** — before and after, with real token counts. Pull
   from the instrumented run JSON, do not reconstruct.

## Done when

- [ ] Every field on the assignment form is filled with a real value, no placeholders.
- [ ] The audit is one page.
- [ ] Cost figures trace to specific run JSON files that exist on disk.
- [ ] The before/after cost comparison uses measured token counts, not estimates.

## Log

- 2026-08-23 — created.
