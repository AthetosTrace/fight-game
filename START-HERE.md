# START HERE — how to jump on and keep working

One page. If you only read one file in this repo, read this one.

**The whole process is three commands.** Everything else in this file explains why.

```powershell
cd C:\Users\athet\Documents\FightGame
pwsh -File sprint\start-session.ps1     # preflight - fix whatever it says
claude                                  # only after preflight is GREEN
```

Then type into Claude:

```
/jump-on
```

That's it. `/jump-on` re-runs the preflight, reads the board, and tells you what
you're working on and what the last session left half-done.

---

## The five steps, spelled out

### 1. Open the Unreal project — FIRST, before the session

`C:\Users\athet\Documents\FightGame\game\AscendantImpact.uproject`

There is exactly one copy of this project. Only one editor may be open at a time —
the MCP server binds `127.0.0.1:8000` and the port has one owner.

Let it finish loading. A first open after a pull can sit on a long shader compile.

### 2. Start the MCP server — in the editor, by hand

Open **Window → Output Log**, and in the `Cmd` box at the bottom type:

```
ModelContextProtocol.StartServer
```

**This step cannot be automated away.** `bAutoStartServer` works and was tried on
2026-08-27, and it **breaks packaging** — the cook is an editor process, it loads
the plugin, it tries to bind a port the live editor already holds, and the whole
cook fails with `ExitCode=25`. Packaging is the gate that caps the assignment.
So: type the command. Every session.

### 3. Run the preflight

```powershell
pwsh -File sprint\start-session.ps1
```

It checks six things and changes nothing:

| # | Check | Why it matters |
|---|---|---|
| 1 | You're in the right folder | one repo, one folder, no worktrees |
| 2 | Git branch, uncommitted work, unpushed commits | `.uasset` files are binary and LFS-tracked; git cannot merge them |
| 3 | Exactly one editor open on this project | two editors is how work gets lost |
| 4 | Port 8000 is listening | step 2 actually happened |
| 5 | What `sprint/BOARD.md` says is NEXT UP | plus any task left `in-progress` |
| 6 | Verdict — green, or a numbered list of what to fix | re-run until green |

Green means go. Not green means fix and re-run.

### 4. Open the session — only now

```powershell
claude
```

**Order is not a preference here.** Claude Code attaches MCP servers *when the
session opens*. A session started before port 8000 is listening will not see the
Unreal tools for its whole life, and no amount of starting the server afterwards
fixes it — you have to quit and reopen. This is the single most common way a
session is wasted.

### 5. Say what you want

| Say | You get |
|---|---|
| `/jump-on` | preflight + board + what's in flight + the recommendation |
| `work the next task` | takes NEXT UP off the board and runs the protocol in `sprint/README.md` |
| `work G05` | that specific task |
| `where did we leave off` | reads the in-progress task Logs, no work started |

### 6. Before you walk away

Say **`wrap up`**. The session appends a Log line to the open task saying exactly
where it stopped and what the next concrete action is, then commits. That log line
is what makes the *next* jump-on cheap. A session that stops without one costs the
next session half an hour of rediscovery.

---

## Where the truth lives

Read these in this order and stop when you have your answer:

1. **`START-HERE.md`** — this file. The process.
2. **`sprint/README.md`** — the working protocol and the rules that bind every track.
3. **`sprint/BOARD.md`** — the task list and NEXT UP.
4. **`sprint/HANDOFF.md`** — the current briefing: what just landed, what the traps are.
5. **`sprint/tasks/<ID>-*.md`** — the one task you're working. Read it whole.

**Do not take direction from** `TODO.md`, `leave-offs/SESSION-RESUME.md`, or
`leave-offs/*.md`. They describe a larger, pre-cut version of this game and a
sprint structure that is retired. `sprint/README.md` explains why.

`CLAUDE.md` is the project's standing brief and is loaded automatically — you
don't need to read it to work, but it wins on any conflict about *what the game is*.

---

## The traps, in one place

These have each cost hours. They are not hypothetical.

- **PowerShell, not Git Bash.** Git Bash rewrites Unreal `/Game/` paths into
  Windows paths and silently corrupts asset arguments.
- **Never enable `bAutoStartServer`.** It breaks the cook. See step 2.
- **Session order is editor → server → session.** See step 4.
- **Duplicate a level to a checkpoint before changing approved geometry.**
  Checkpoints live in `/Game/AscendantImpact/Maps/Checkpoints/`.
- **One branch touches `.uasset`/`.umap` at a time.** Binary, LFS, unmergeable.
- **MCP payload scripts define `run()` and must be made to call it** — otherwise
  they silently no-op and look like success.
- **`NameError` on `execute_tool` under plain `python` is expected** — those
  scripts only run inside the editor. Don't "fix" it.
- **PIE advances in real time between MCP calls.** An idle player takes live hits
  and can be knocked out between two tool calls. Re-read health at each step.
- **Compiling a Blueprint mid-PIE kills Slate-injected input** for the rest of that
  session. Restart PIE after any mid-session compile.
- **Agent-driven player input does not currently work.** Three routes were tried
  and documented in `sprint/HANDOFF.md`. Anything needing a real key press is a
  human step — press it yourself, then tell the session what happened.
- **A move that returns `False` for no reason is a suppressed modal.** Grep the
  editor log for `Message dialog closed`.
- **Don't enable plugins with Runtime modules.** No C++ toolchain on this machine;
  the project packages only because it is genuinely Blueprint-only.

---

## Health check on the whole thing

If a session ever feels lost, the fastest reset is:

```powershell
git status                              # what's uncommitted
git log --oneline -10                   # what landed recently
pwsh -File sprint\start-session.ps1     # what's not connected
```

and then read the Log block at the bottom of whatever task is `in-progress`.
