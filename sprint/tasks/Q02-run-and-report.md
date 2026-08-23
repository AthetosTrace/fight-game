---
id: Q02
track: Q
title: Run the agent against the build and produce the report
status: todo
assignment: 09
editor-required: true
depends-on: [Q01, G05]
---

## Goal

At least one real run, against the real game, that finds at least one real bug.

## Why it matters

Findings is worth 4 of 10 points and requires the report to **name the mechanic or system**
where the problem occurred — not "collision bug" but which actor, which value, which state.

## Preconditions

- `Q01` complete.
- `G05` complete, so there is a match loop to break rather than an endless ragdoll.
- **The editor is free.** Only one editor can hold `127.0.0.1:8000`. Coordinate with
  whoever is on the `G` track — do not start a run while they are working.

## Steps

1. Agree an editor window with the `G` track and say so in the Log.
2. Run against the current duel level. Long enough to cycle every behaviour class several
   times.
3. Keep the raw log as well as the structured report — the raw log is what makes a finding
   defensible if it is questioned.
4. Triage: separate real defects from agent artefacts. A finding caused by the harness
   repositioning something impossibly is not a game bug, and claiming it as one is worse
   than finding nothing.
5. Commit the report under `assignment-09/evidence/`.

## Done when

- [ ] At least one run completed against the real game, with its seed recorded.
- [ ] At least one genuine defect, exploit or edge case found, naming the specific mechanic
      or system.
- [ ] Structured report committed with location, error type and game context per finding.
- [ ] Harness artefacts separated from real findings, and the separation explained.

## Log

- 2026-08-23 — created.
