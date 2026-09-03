---
description: Reconnect to Ascendant Impact - preflight, plan state, and what to work on next
allowed-tools: Bash, Read, Glob, Grep, PowerShell
---

The user has just sat down and wants to continue work on Ascendant Impact. Get them
oriented and connected in one pass. **Do NOT start any step work in this command** — end
by recommending, and wait for them to say go.

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

Read `FINISH-PLAN.md` — the status table, then the section for whatever is
`in-progress` or next, then the **Log** at the bottom. **That file is the only plan.**
Do not go looking for other planning documents; the stale ones were deleted on
2026-09-02 precisely so they could not be picked up mid-task.

## 3. Report back, short

In this shape and no longer:

- **Connected / not connected** — one line, and the fix if not.
- **Where we left off** — the last Log line, in plain words.
- **What's next** — the next step, its one-line goal, and whether it needs the editor.
- **Blocked on a human** — a key press, an upload, a decision. Name it as theirs.
- **The one thing you'd do first**, as a recommendation. Then stop.

Do not summarise the whole plan. Do not restate the traps unless one applies to the step
about to be worked.

## 4. Then wait

They will say `work the next step`, name one, or ask something else. When they do:

- Set that step's row to `in-progress` in the status table.
- Work it one verified action at a time. Never a one-shot build.
- A step closes only when its **Done when** line is actually observed — never on
  "should work". If it cannot be verified, it stays open with the reason in the Log.
- **Never commit `.uasset`, `.umap`, or anything under `Content/`.** Code, docs, config
  and scripts only. If assets need saving, tell the user to commit them by hand.
- On close: set the row to `done`, append a dated Log line saying what happened
  *including what did not work*, and commit.
