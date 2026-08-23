# Board

**Updated 2026-08-23.** Deadlines: A08 **25 Aug**, A09 **27 Aug**, A10 **1 Sept** (Adrian
believes 7 Sept — unconfirmed, plan to the 1st). Internal target: playable build live
**30 Aug**.

Statuses: `todo` · `in-progress` · `blocked` · `done`

---

## NEXT UP

| Track | Task | Why this one |
|---|---|---|
| **G — Game** | **`G01`** — Scope lock | No editor needed. Writes down what ships and what is cut, so every later task has a fixed target. |
| **N — Narrative** | **`N01`** — API key + cost instrumentation | Hard blocker for A08 *and* for A10's cost analysis. Nothing in this track moves until it lands. |
| **Q — QA** | **`Q01`** — Agent design + code | Text-only, no editor contention. Can start immediately. |

---

## G — Game (Assignment 10)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| G01 | Scope lock — GDD cut addendum, reconcile stale docs | `todo` | no | — |
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

## N — Narrative (Assignment 08, due 25 Aug)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| N01 | API key + shared cost-instrumentation helper | `todo` | no | — |
| N02 | Narrative engine — ledger and reactive DM | `todo` | no | N01 |
| N03 | 5+ turn run, evidence, README | `todo` | no | N02 |

## Q — Adversarial QA (Assignment 09, due 27 Aug)

| ID | Task | Status | Editor | Depends on |
|---|---|---|---|---|
| Q01 | Agent design and code | `todo` | no | — |
| Q02 | Run against the build, produce the report | `todo` | runs | Q01, G05 |
| Q03 | README, and triage findings into G tasks | `todo` | no | Q02 |

---

## Blocked on a human, not on an agent

- **A10 due date** — 1 Sept or 7 Sept. Unconfirmed in writing.
- **Anthropic API key** — none on this machine at any scope. Blocks `N01`, and `G11`'s
  cost analysis needs real token counts. See `N01`.
- **Migration verification** — `G02`. Nobody has opened the migrated project yet.

## Critical path

`G01 → G02 → G03 → G04` retires the packaging risk, which is the only thing that can cap
the whole assignment at 50%. Everything in the `G05`–`G09` block is gameplay that can be
cut down if time runs short. **Do not reorder so that packaging is discovered last.**
