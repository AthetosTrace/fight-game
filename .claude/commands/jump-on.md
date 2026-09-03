---
description: Reconnect to Ascendant Impact - preflight, board, and what to work on next
allowed-tools: Bash, Read, Glob, Grep, PowerShell
---

The user has just sat down and wants to continue work on Ascendant Impact. Get them
oriented and connected in one pass. Do NOT start any task work in this command — end
by recommending, and wait for them to say go.

## 1. Preflight

Run it and report what it says:

```
pwsh -File sprint\start-session.ps1
```

If it reports a blocker, **stop there and walk them through fixing it**, in the script's
own order. The two that matter most:

- **Nothing on port 8000** → they must type `ModelContextProtocol.StartServer` in the
  editor's Output Log `Cmd` box. Never suggest `bAutoStartServer` — it breaks the cook.
- **MCP tools missing from THIS session even though port 8000 is now listening** → the
  session was opened before the server started. MCP attaches at session start and cannot
  be re-attached. Tell them plainly: quit with `/exit` and run `claude` again. Do not
  try to work around it.

Check your own tool list: if `mcp__unreal-mcp__*` tools are not available to you, say so
explicitly rather than discovering it halfway through a task.

## 2. Read the board

Read, in this order — and read only these:

1. `sprint/README.md` — the protocol
2. `sprint/BOARD.md` — NEXT UP and the task table
3. `sprint/HANDOFF.md` — the current briefing
4. The task file for anything `status: in-progress`, especially its **Log** block

Ignore `TODO.md` and `leave-offs/` — `sprint/README.md` explains why they are stale.

## 3. Report back, short

Give them, in this shape and nothing longer:

- **Connected / not connected** — one line, and the fix if not.
- **Where we left off** — the last Log line of each in-progress task, in plain words.
- **What's next** — the NEXT UP task, its one-line goal, and whether it needs the editor.
- **Anything blocked on a human** — a key press, an approval, a date. Name it as theirs.
- **The one thing you'd do first**, as a recommendation, then stop.

Do not summarise the whole board. Do not restate the traps unless one applies to the
task about to be worked.

## 4. Then wait

They will say `work the next task`, name a task, or ask something else. When they do,
follow the protocol in `sprint/README.md` §"The protocol" exactly — status to
`in-progress`, dated Log line, work the Steps, verify every **Done when** line, close
only on verified, move the NEXT UP pointer, commit.
