# Sprint board — read this first

This directory is the operating system for the final push. If you are an agent or a
person picking this project up cold, **read this file, then `BOARD.md`, then the one task
file `BOARD.md` points at.** Nothing else. Do not read `TODO.md` — see "Stale files" below.

## Who is on this

- **Adrian Delgado** — capstone owner, the student of record.
- **Omar** — building alongside Adrian.

Either may be driving. Tasks are not assigned by person; whoever sits down takes the next
open task in whichever track they are working.

## One folder — the worktrees are gone

**Everything happens in `C:\Users\athet\Documents\FightGame` on `main`.** As of 2026-08-24
the `fightgame-a7`, `a8` and `a10` worktrees were removed; all their work was merged into
`main` first. Do not create new worktrees for this sprint.

The Unreal project is `game\AscendantImpact.uproject` in that folder and it is the only
copy, which makes the one-editor rule automatic — the MCP binds `127.0.0.1:8000` and only
one editor can hold it.

`AscendantCapstone\fightgame-a9` may still exist while the `Q` track finishes. It is the
last worktree; remove it once `Q03` merges.

## Three tracks

| Track | Prefix | Editor? | State |
|---|---|---|---|
| Game — Assignment 10 | `G` | yes | active |
| Narrative — Assignment 08 | `N` | no | **delivered**, see below |
| Adversarial QA — Assignment 09 | `Q` | runs only | active |

**Within a track, tasks are strictly ordered** — do not start `G05` while `G03` is open
unless the task file says it is independent.

**Assignment 08 is delivered and lives outside this repo**, at
`AthetosTrace/ascendant-dm`, checked out at `C:\Users\athet\Documents\ascendant-dm`.
Standalone by design, as the assignment permits. Its `transcripts/*/run.json` files carry
the real token counts `G11`'s cost analysis needs. Nothing about it merges here.

## The protocol — how to "jump on"

Say *"work the next task"* (or name one, e.g. *"work G05"*). The agent then:

1. Reads `BOARD.md`, takes the task under **NEXT UP** for that track.
2. Opens `sprint/tasks/<ID>-*.md` and reads it whole.
3. Checks **Preconditions**. If one fails, stops and says so — does not improvise around it.
4. Sets `status: in-progress` in the task frontmatter and appends a dated Log line.
5. Works the **Steps**.
6. Verifies every line under **Done when**. Any line that cannot be verified keeps the
   task open. A task is never closed on "should work".
7. Sets `status: done`, appends a closing Log entry saying what actually happened
   including what did not work, and moves the **NEXT UP** pointer in `BOARD.md`.
8. Commits on that track's branch.

**Stopping mid-task is fine and expected.** Leave `status: in-progress` and append a Log
line saying exactly where you stopped and what the next concrete action is. That log line
is the handoff — write it for someone who was not there.

## Rules that bind every track

- One branch touches `.uasset` / `.umap` at a time. They are binary and LFS-tracked; git
  cannot merge them and always loses a side.
- PowerShell, not Git Bash — Git Bash rewrites Unreal `/Game/` paths.
- Duplicate a level to a checkpoint before changing approved geometry.
- MCP payload scripts define `run()` and must be made to **call** it, or they silently
  no-op and look like success.
- `NameError` on `execute_tool` under plain `python` is expected — those scripts only run
  inside the editor.
- PIE advances in real time between MCP calls; an idle player takes live hits.
- Compiling a Blueprint mid-PIE reinstances the pawn and kills Slate-injected input.
  Restart PIE after any mid-session compile.

## Stale files — do not take direction from these

| File | Why it is stale |
|---|---|
| `TODO.md` | 66 items against the **pre-cut** GDD scope: Final Clash, Ascension Meter, M1–M5, combo system, roster. Most of it is formally descoped — see `sprint/tasks/G01`. Historical record only. |
| `leave-offs/SESSION-RESUME.md` | Written 2026-08-03. Says "M1 not started in-engine, no `.uproject`, no `Content/` anywhere." There is now a working duel and an octagon arena. |
| `leave-offs/*.md` | The old per-agent role gates (designer / developer / inspector). Not used by this sprint. |
| `game/CLAUDE.md`, `game/AGENTS.md` | Came across in the migration. Still describe the old two-repo split and the dead never-edit-Anthony's-Blueprints rule. `G01` reconciles them. |

`sprint/PLAN.md` holds the strategy and the scope cut. Read it once for context; `BOARD.md`
is what you work from day to day.
