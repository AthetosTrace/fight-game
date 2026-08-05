# Session resume — written 2026-08-03

> **2026-08-04 — read [`STOP-2026-08-04.md`](STOP-2026-08-04.md) BEFORE this file.** A task was
> interrupted mid-run, and **OneDrive rolled two files backward during a folder move, losing
> `design/goal-plan.md` sections 5–8.** That note carries the loss, the recovery options, and
> the resume list. It also supersedes two rows below: the `goal-planner` **has** now been run,
> and the working tree is **not** clean.

Not a gate file. The gate hooks read `designer.md`, `developer.md` and `inspector.md`; this
file is here for the next session to read **first**.

**Recompute every date on session start — they are stale the moment this file is saved.**

## Read these three, in this order

1. **This file** — where things stand.
2. **`TODO.md`** — 66 open items, every one carrying the `build-sequence.md` step it blocks.
3. **`design/decisions.md`** — what is settled and what is only proposed. **Trust its status
   field over any group file's prose**: an inspection reopened two items whose own sections
   still read APPROVED in places.

## Where the project actually stands

| Thing | State |
|---|---|
| Milestone | **M1 — not started in-engine.** No `.uproject`, no `Content/` anywhere |
| Phase | **Phase 1** — a duel fought start to finish, due **1 Sept 2026** |
| Coursework | **#02, #03, #04, #05 all delivered.** Nothing outstanding |
| Git | local `main` == `origin/main` == `0f762df`, clean, pushed |
| Agents | **seven exist.** The new `goal-planner` runs first and has never been run |
| Design answers | **43 questions answered** across 9 dispatches, **8 closed**, **35 PROPOSED and awaiting the designer** |
| Inspections | **3 passes.** Zero GDD violations. 3 process-authority violations found and corrected |

## The one thing that matters most

**35 items are PROPOSED and waiting on the human designer.** They are researched, sourced
against real shipped games, and cross-checked — but **not decided.** Nothing downstream should
be built on a PROPOSED value as though it were settled.

**`TODO.md`'s ⏳ PROPOSED table lists every one, grouped by dispatch.** The fastest useful
thing the next session can do is walk that table with the user and convert approvals into
deletions.

## What happened 2026-08-02 → 2026-08-03

1. **Pulled Anthony's `planning/unreal-attack-a-integration`** — 15 commits, the Unreal data
   bridge (attack CSV, validator, 25 tests, Attack A plan). Verified in-tree: validator PASS,
   25 CSV tests, 175 assignment-04 tests.
2. **Recovered GDD pages 10–14.** They are image reference sheets no agent had ever seen —
   `pdftoppm` is absent, so pages cannot be rendered. The embedded JPEGs were pulled from the
   PDF's `/XObject` resources with `pypdf` and read directly. Now in `gdd/reference/`.
   Re-split the authored text into `gdd/sections/` by the document's own numbering.
3. **Fixed a gate that would have deadlocked the work** — `entry_gate.py` made the inspector
   depend on the developer, so a design-only pass could never inspect anything.
4. **Worked the whole `TODO.md`** in 9 grouped designer dispatches. See below.
5. **Ran the inspector three times.** Corrected everything that was mine to correct.
6. **Built Assignment 05** — the `goal-planner` agent and `assignment-05/`.

## Do this first, next session

1. **Run the `goal-planner`.** It has never been run. Its gate is open (it needs only
   `project-brief.md`, the extracted GDD, and `build-sequence.md`). It produces
   `design/goal-plan.md` — a ranked worklist and one dispatch recommendation — and **stops
   when the top item is a design question.** That replaces the by-hand ranking this session
   did.
2. **Or skip it and walk `TODO.md`'s PROPOSED table with the user**, if the user wants to
   approve in a batch instead. That is the higher-value move if they have time.
3. **Then stop writing documents and start building in Unreal.** Everything needed exists:
   `build-sequence.md` (63 steps), `combat-integration-plan.md` (28 systems),
   `docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md`, `ATTACK_A_ACCEPTANCE_TESTS.md`.

## Blocked, and needs the user — not solvable by any agent

- **Unreal MCP is not connected.** `TODO.md` item 1. **This blocks all 63 build steps.**
- **Item 26** — whether GDD page 14's *"plasma-gauntlet weapons"* contradicts Attack A. The
  transcription disclaims its own confidence, so a dispatch refused to settle canon from it.
  **Clearing it means zooming page 14 by eye.** Four specific questions are written out in
  `design/group-07-structure-and-canon.md`.
- **Item 64** — constraint **C3 from the approved Q22 is not satisfied.** Q2 = 1200 puts meter
  100 and the ≤25% health gate **90–135 s apart**, not "close together". Either amend C3 on the
  record or take Q2 → 1050–1100.
- **Items 6 and 29** — Q17 and Q18, reopened by the inspection because they were closed as
  engineering when they were actually designer choices. Recommendations intact.

## Traps that will bite whoever goes next

- **Item 65 — Telegraph and Recover are specified two incompatible ways.** Absolute seconds in
  `design/group-07-structure-and-canon.md`, a scale factor in `design-brief.md` §13.1 and
  `build-sequence.md` M4-04. **`M2-04` and `M4-04` cannot both be built as written**, and the
  four phase ratios (0.786 / 0.800 / 0.775 / 0.778) are not uniform, so no single
  `TelegraphScale` can express them.
- **Items 49 + 67 — the rival's `MaxWalkSpeed` does not exist** in any table, and under the
  approved Q22 a rival slower than the player **can be kited forever and the duel cannot end.**
  Three dispatches assumed three different speeds. Tune 49, 67 and Q21 in one session.
- **Item 63 — V1–V5 are written and APPROVED but NOT APPLIED.** The
  `combat-integration-architect` has to put them into `combat-integration-plan.md`. That is
  what clears hard check 7 and unlocks **M3**. **M1 and M2 may proceed now regardless.**
- **Items 68–71 — `build-sequence.md` is stale** in four places against the new answers.
- **`ActiveSeconds` must never gain a per-phase field.** Scaling Attack D's 0.45 s by the
  Phase 2 ratio crosses 600 cm at 1714 cm/s and breaks the GDD's own no-snap rule.
- **Attack B's first-to-last hit notify must span ≤ 0.26 s**, or the 0.28 s i-frames cannot
  cover it and **B becomes unavoidable**.
- **Two numbering spaces overlap.** `TODO.md` **item** numbers and proposed `design-brief.md`
  **§13.2 row** numbers both run through the high 50s and early 60s and mean unrelated things.
  Always write "item N" or "§13.2 row N", never a bare number.
- **Item 74 — a HARD RULE debt, opened knowingly.** `CLAUDE.md`'s diagram shows the
  `goal-planner`; the root `README.md` does not, because the Assignment 05 instruction said not
  to touch it. The two diagrams disagree until someone mirrors two blocks across.

## Settled and binding — do not re-litigate

**Q22, approved by the designer of record 2026-08-02.** `MinHealthFloor = 1` on the rival from
`BeginPlay`, lowered to `0` only by `ClashSuccess()`. **The Final Clash is the only way to win
the duel.** Three constraints follow and bind every later answer:

- **C1** — Q9 must resolve to **no meter decay**. (Done; group 06 proposes none.)
- **C2** — the HUD must show **which gate is still locked** once the health bar pins.
- **C3** — Q2 must place ≤25% health and meter 100 **close together**. **NOT SATISFIED —
  item 64.**

Also settled: **item 28** — Crimson Vanguard is **208 cm**, transcribed from GDD page 10, which
filled a blank in `design-brief.md` §13.1 row 28.

## Where the work lives

| Path | What |
|---|---|
| `TODO.md` | the worklist — 66 items, each with its blocking step |
| `design/decisions.md` | the permanent record, 9 entries + a corrections note |
| `design/group-0*.md` | the reasoning behind every answer, 10,005 lines total |
| `design/inspection-design-answers*.md` | three inspection passes |
| `gdd/INDEX.md` | start here for the GDD — `sections/` for text, `reference/` for the images |
| `assignment-05/` | the goal-planner submission |
| `.claude/agents/goal-planner.md` | the live agent |

**`gdd/` is generated and never hand-edited.** To change it, change the PDF and re-extract.
