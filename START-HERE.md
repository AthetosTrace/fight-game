# START HERE — how to jump on and keep working

One page. If you read one file in this repo, read this one.
**The plan is [`FINISH-PLAN.md`](FINISH-PLAN.md).** This file is only about getting
connected so you can work it.

**The whole process is two commands.** Everything else here explains why.

```powershell
cd C:\Users\athet\Documents\FightGame
pwsh -File start-session.ps1     # preflight - fix whatever it says
claude                            # only after preflight is GREEN
```

Then type `/jump-on`. It re-runs the preflight, reads the plan, and tells you which step
is next and what the last session left half-done.

---

## The four steps, spelled out

### 1. Open the Unreal project — FIRST, before the session

`C:\Users\athet\Documents\FightGame\game\AscendantImpact.uproject`

There is exactly one copy. Only one editor may be open at a time — the MCP server binds
`127.0.0.1:8000` and the port has one owner. Let it finish loading; a first open after a
pull can sit on a long shader compile.

### 2. Start the MCP server — in the editor, by hand

**Window → Output Log**, and in the `Cmd` box at the bottom type:

```
ModelContextProtocol.StartServer
```

**This cannot be automated away.** `bAutoStartServer` works and was tried on 2026-08-27,
and it **breaks packaging** — the cook is an editor process, it loads the plugin, it tries
to bind a port the live editor already holds, and the whole cook dies with `ExitCode=25`.
Packaging is the gate that decides the grade. So: type the command, every session.

### 3. Run the preflight

```powershell
pwsh -File start-session.ps1
```

It checks five things and changes nothing:

| # | Check | Why it matters |
|---|---|---|
| 1 | Right folder | one repo, one folder, no worktrees |
| 2 | Git state — and it separates asset changes from the rest | `.uasset` files are binary and LFS-tracked; **agents never commit them** |
| 3 | Exactly one editor on this project | two editors is how work gets lost |
| 4 | Port 8000 is listening | step 2 actually happened |
| 5 | The next step from `FINISH-PLAN.md` | plus anything left `in-progress` |

Green means go. Not green means fix and re-run.

### 4. Open the session — only now

```powershell
claude
```

**Order is not a preference.** Claude Code attaches MCP servers *when the session opens*.
A session started before port 8000 is listening will not see the Unreal tools for its
whole life, and starting the server afterwards does not fix it — you have to quit and
reopen. This is the single most common way a session gets wasted.

---

## What to say

| Say | You get |
|---|---|
| `/jump-on` | preflight + plan state + what's in flight + a recommendation |
| `work the next step` | takes the lowest `todo` step in `FINISH-PLAN.md` and works it |
| `work step 5` | that specific step |
| `where did we leave off` | reads the plan and the log, starts nothing |
| `/wrap-up` | before you walk away — logs the step, updates the table, commits |

**Say `/wrap-up` before you stop.** It writes the line that makes the next jump-on cheap.
A session that stops without one costs the next session half an hour of rediscovery.

---

## The rule that matters most

**Agents never commit Blueprint or Unreal binary assets** — no `.uasset`, no `.umap`, no
`Content/` binaries. They are LFS-tracked binaries git cannot merge, and a bad merge
silently loses a side. Agents commit code, docs, config and scripts only. **If assets
need committing, you do it by hand.** The preflight counts changed assets separately so
you always know what is sitting uncommitted.

---

## The traps, in one place

Each of these has cost hours. None is hypothetical.

- **PowerShell, not Git Bash.** Git Bash rewrites Unreal `/Game/` paths and silently
  corrupts asset arguments.
- **Never enable `bAutoStartServer`.** It breaks the cook. See step 2.
- **Session order is editor → server → session.** See step 4.
- **Duplicate a level to a checkpoint before changing approved geometry.** Checkpoints
  live in `/Game/AscendantImpact/Maps/Checkpoints/`.
- **MCP payload scripts define `run()` and must be made to call it** — otherwise they
  silently no-op and look like success.
- **`NameError` on `execute_tool` under plain `python` is expected** — those scripts only
  run inside the editor. Don't "fix" it.
- **PIE advances in real time between MCP calls.** An idle player takes live hits and can
  be knocked out between two tool calls. Re-read health at each step.
- **Compiling a Blueprint mid-PIE kills Slate-injected input** for the rest of that
  session. Restart PIE after any mid-session compile.
- **Agent-driven player input does not work.** Three routes were tried and all failed.
  Anything needing a real key press is your job — press it, then say what happened.
- **A move that returns `False` for no reason is a suppressed modal.** Grep the editor log
  for `Message dialog closed`.
- **Don't enable plugins with Runtime modules.** No C++ toolchain here; the project
  packages only because it is genuinely Blueprint-only.

---

## If a session ever feels lost

```powershell
git status                        # what's uncommitted
git log --oneline -10             # what landed recently
pwsh -File start-session.ps1      # what's not connected
```

Then read the **Log** at the bottom of `FINISH-PLAN.md`.

## Recovering anything deleted in the 2026-09-02 cleanup

The whole pre-cleanup repo is preserved at the tag `pre-cleanup-2026-09-02`:

```powershell
git checkout pre-cleanup-2026-09-02 -- <path>
```
