# Board

**Updated 2026-08-23.** Deadlines: A08 **25 Aug**, A09 **27 Aug**, A10 **1 Sept** (Adrian
believes 7 Sept — unconfirmed, plan to the 1st). Internal target: playable build live
**30 Aug**.

Statuses: `todo` · `in-progress` · `blocked` · `done`

---

## NEXT UP

| Track | Task | Why this one |
|---|---|---|
| **G — Game** | **`G02`** — Verify migration + first package | `G01` is done. This is the highest-risk unknown left: nothing has ever been packaged. |
| **N — Narrative** | — | **Track complete.** Delivered in `AthetosTrace/ascendant-dm`. |
| **Q — QA** | **`Q01`** — Agent design + code | In progress. Declaration and oracle written 24 Aug. |

---

## G — Game (Assignment 10)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| G01 | Scope lock — GDD cut addendum, reconcile stale docs | `done` | no | — |
| G02 | Verify migration + first package smoke test | `todo` | yes | G01 |
| G03 | Make the package actually launch | `todo` | yes | G02 |
| G04 | itch.io page + butler, upload the graybox build | `todo` | no | G03 |
| G05 | Match loop — intro, win, lose, restart | `todo` | yes | G02 |
| G06 | Balance — measure, then tune so the boss can win | `todo` | yes | G05 |
| G07 | Octagon swap — move the duel into the real arena | `todo` | yes | G05 |
| G08 | Title and controls screen | `todo` | yes | G05 |
| G09 | Audio minimum — hit, whiff, KO, ambience | `todo` | yes | G05 |
| G10 | Ship candidate — package, upload, stranger test | `todo` | yes | G04, G06, G07, G08, G09 |
| G11 | A10 submission — audit and cost analysis | `todo` | no | G10, N01 |

## N — Narrative (Assignment 08, due 25 Aug) — COMPLETE

Delivered as a standalone repo, **not** in `fight-game`:
`AthetosTrace/ascendant-dm`, checked out at `C:\Users\athet\Documents\ascendant-dm`.
Three commits, clean, pushed. Engine in `dm/`, tests, and three recorded transcripts —
`betrayal-run` (7 turns), `loyal-run`, `hand-run` — with per-turn ledger snapshots.

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| N01 | API key + shared cost-instrumentation helper | `done` | no | — |
| N02 | Narrative engine — ledger and reactive DM | `done` | no | N01 |
| N03 | 5+ turn run, evidence, README | `done` | no | N02 |

**`G11` still needs this track:** pull the real token counts from
`ascendant-dm/transcripts/*/run.json` for the A10 cost analysis. Do not re-estimate them.

## Q — Adversarial QA (Assignment 09, due 27 Aug)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| Q01 | Agent design and code | `in-progress` | no | — |
| Q02 | Run against the build, produce the report | `todo` | runs | Q01, G05 |
| Q03 | README, and triage findings into G tasks | `todo` | no | Q02 |

---

## Working directory — one folder

All work happens in `C:\Users\athet\Documents\FightGame` on `main`. The `a7`, `a8` and
`a10` worktrees were removed 2026-08-24 after their work was merged.
`AscendantCapstone\fightgame-a9` is the last one standing and only until `Q03` merges.

## Blocked on a human, not on an agent

- **A10 due date** — 1 Sept or 7 Sept. Unconfirmed in writing.
- **Anthropic API key** — none on this machine at any scope. Blocks `N01`, and `G11`'s
  cost analysis needs real token counts. See `N01`.
- **Migration verification** — `G02`. Nobody has opened the migrated project yet.

## Critical path

`G01 → G02 → G03 → G04` retires the packaging risk, which is the only thing that can cap
the whole assignment at 50%. Everything in the `G05`–`G09` block is gameplay that can be
cut down if time runs short. **Do not reorder so that packaging is discovered last.**
