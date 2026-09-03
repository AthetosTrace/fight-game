---
description: Reconnect to Ascendant Impact - preflight, plan state, and what to work on next
allowed-tools: Bash, Read, Glob, Grep, PowerShell, AskUserQuestion
---

The user has just sat down and wants to continue work on Ascendant Impact. Get them
oriented, connected, and **get the plan's record corrected** in one pass. **Do NOT start
any step work in this command** — end by recommending, and wait for them to say go.

## 1. Preflight

Run it and report what it says:

```
pwsh -File start-session.ps1
```

If it reports a blocker, **stop and walk them through fixing it**, in the script's own
order. The two that matter:

- **Nothing on port 8000** → they must type `ModelContextProtocol.StartServer` in the
  editor's Output Log `Cmd` box. Never suggest `bAutoStartServer` — it breaks the cook.
- **MCP tools missing from THIS session even though port 8000 is now listening** → the
  session was opened before the server started. MCP attaches at session start and cannot
  re-attach. Tell them plainly: `/exit` and run `claude` again. Do not work around it.

Check your own tool list. If `mcp__unreal-mcp__*` tools are not available to you, say so
explicitly rather than discovering it halfway through a step.

## 2. Read the plan

Read `FINISH-PLAN.md` — the status table, then the section for whatever is `in-progress`
or next, then the **Log** at the bottom. **That file is the only plan.** Do not go looking
for other planning documents; the stale ones were deleted on 2026-09-02 precisely so they
could not be picked up mid-task.

## 3. Reconcile the record — ASK, do not assume

**This is the part that keeps the plan honest, and it is not optional.**

Eleven of the twelve steps are `human` or `both` in the "Closed by" column, meaning the
user may have done work between sessions that nothing wrote down. Silence is not evidence
a step is still open.

Use `AskUserQuestion` when **either** is true:

- **A row is `in-progress`.** Ask whether the specific thing the Log said was outstanding
  is now done. Quote the Log's own words back — *"Step 2's log says restart wasn't wired
  yet. Still true?"*
- **The next `todo` row is `human` or `both`.** Ask whether they already did it. Name the
  actual acceptance, not the step title — *"Step 1 needs the packaged .exe run from
  Explorer, walking and punching. Have you done that?"*

Rules for asking:

- **Ask about at most two steps.** This is a check-in, not an audit. If more than two rows
  look uncertain, ask about the two nearest the front of the plan and say you'll confirm
  the rest as you reach them.
- **Ask about the acceptance, never the step in the abstract.** "Did you finish Step 5?"
  invites a yes that means nothing. "Did you play ten matches and lose at least three?"
  gets you the truth.
- **Skip the question entirely** if the Log already answers it, or if the step is
  `agent`-closed, or if the user's own message already told you.
- If they say a step is done, **update the row to `done` and append a dated Log line
  recording what they reported and that they reported it.** Attribute it: the Log must
  show this came from the user, not from a verification you performed.
- If they are unsure, leave the row as it is and say which acceptance line would settle
  it. Never upgrade a row on a maybe.

## 4. Report back, short

In this shape and no longer:

- **Connected / not connected** — one line, and the fix if not.
- **Where we left off** — the last Log line, in plain words.
- **Anything you just corrected** — one line per row you changed, and why.
- **What's next** — the next step, its one-line goal, whether it needs the editor, and
  whether it is theirs to close.
- **Blocked on a human** — a key press, an upload, a decision. Name it as theirs.
- **The one thing you'd do first**, as a recommendation. Then stop.

Do not summarise the whole plan. Do not restate the traps unless one applies to the step
about to be worked.

## 5. Then wait

They will say `work the next step`, name one, or ask something else. When they do:

- Set that step's row to `in-progress` in the status table.
- Work it one verified action at a time. Never a one-shot build.
- A step closes only when its **Done when** line is actually observed — never on "should
  work". A `human` or `both` step cannot be closed on your own say-so: **ask them to check
  it and wait for the answer.** If it cannot be verified now, it stays open with the reason
  in the Log.
- **Never commit `.uasset`, `.umap`, or anything under `Content/`.** Code, docs, config and
  scripts only. If assets need saving, tell the user to commit them by hand.
- On close: set the row to `done`, append a dated Log line saying what happened *including
  what did not work*, and commit.
