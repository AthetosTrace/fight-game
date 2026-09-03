---
description: Close out an Ascendant Impact session so the next one starts cheap
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, PowerShell
---

The user is stopping. Leave the repo so the next session — theirs or someone else's —
picks up without rediscovering anything.

## 1. Log it

Append a dated line to the **Log** at the bottom of `FINISH-PLAN.md`. Write it for
someone who was not here:

- what actually happened this session, **including what did not work**
- the exact next concrete action — a file, a Blueprint node, a command, a key press
- anything you tried that failed, so they don't try it again
- any provisional value you set, so it survives a rebuild

## 2. Update the status table

Set the step's row in `FINISH-PLAN.md` to `done`, `in-progress`, or `cut`.

**Do not mark a step `done` unless its "Done when" line was actually observed.** "Should
work" is not observed. A step whose acceptance could not be verified stays
`in-progress`, with the reason in the Log.

## 3. Commit — code, docs and config only

**Never stage `.uasset`, `.umap`, or anything under `Content/`.** Check with
`git status --porcelain` before staging, and stage explicit paths — never `git add -A`.
If Blueprint assets changed, say so in your report and tell the user to commit them by
hand.

Message style — the step number first, then what really happened:

```
Step 2 - round start and win detection; restart still unwired
```

Then push, and say plainly whether it succeeded.

## 4. Report

Three lines: what landed, what is open and its next action, and what the next session
should run first. Name any changed Blueprint assets the user still needs to commit.
