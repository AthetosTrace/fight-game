---
description: Close out an Ascendant Impact session so the next one starts cheap
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, PowerShell
---

The user is stopping for now. Leave the repo in a state where the next session — theirs
or someone else's — can pick up without rediscovering anything.

## 1. Log the open task

For every task in `sprint/tasks/` with `status: in-progress`, append a dated line to its
**Log** block. Write it for someone who was not here:

- what actually happened this session, **including what did not work**
- the exact next concrete action — a file, a node, a command, a key press
- anything you tried that failed, so they don't try it again

Do not mark a task `done` unless every line under **Done when** was actually verified.
"Should work" is not verified. A task with an unverifiable line stays open, with the
reason in the Log.

## 2. Move the pointer

If a task closed this session, update **NEXT UP** in `sprint/BOARD.md` and its status
row. If the situation changed materially — a new blocker, a reordering, a trap worth
knowing — rewrite `sprint/HANDOFF.md` to brief the next session on the state you are
actually leaving.

## 3. Commit

Stage and commit on `main` with a message in the style of the existing log — the task id
first, then what really happened:

```
G05 - round start and win detection; restart still unwired
```

Then report whether the push succeeded, and say plainly if there are unpushed commits.

## 4. Report

Three lines, no more: what landed, what is open with its next action, and what the next
session should run first.
