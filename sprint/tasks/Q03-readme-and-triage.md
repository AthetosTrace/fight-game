---
id: Q03
track: Q
title: ReadMe, and triage the findings into G tasks
status: todo
assignment: 09
editor-required: false
depends-on: [Q02]
---

## Goal

Close out Assignment 09, and turn its findings into fixes that actually reach the shipped
build.

## Preconditions

- `Q02` complete.

## Steps

1. Write the ReadMe. Two questions, answered directly: **what did the agent find**, and
   **were you surprised.** An honest "no, it found exactly what we expected" is a fine
   answer if it is true — but say which finding was the exception, because there usually is
   one.
2. Triage every finding into one of three buckets:
   - **Breaks a first-time player** — must be fixed before `G10`. Add it to `BOARD.md` as
     a new `G` task and say so in the Log.
   - **Real but survivable** — record as a known limitation for the `G11` audit.
   - **Not a defect** — harness artefact or intended behaviour. Say why.
3. Update `sprint/BOARD.md` with anything that became a `G` task.

## Done when

- [ ] ReadMe answers both rubric questions directly.
- [ ] Every finding is in exactly one of the three buckets, with a reason.
- [ ] Anything that breaks a first-time player exists as a `G` task on the board.
- [ ] Committed on `assignment-09/adversarial-qa`.

## Log

- 2026-08-23 — created.
