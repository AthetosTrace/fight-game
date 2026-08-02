# Design decisions — the record

This file holds **one rule** and the log it governs. It is the permanent record of what
was decided; [`TODO.md`](../TODO.md) is the impermanent record of what is still open.
An item that gets answered is **deleted** from `TODO.md` and **appears here**.

---

## The rule

**1. The PDF is the source of truth.**
`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` (v0.4, 2026-07-24) outranks
every other document in this repository — this file, `project-brief.md`,
`design-brief.md`, `combat-integration-plan.md`, the assignment-04 knowledge base, and
anything said in a session. If any of them disagrees with the PDF, the PDF wins.

**2. `gdd/` is generated and is never hand-edited.**
`gdd/sections/`, `gdd/reference/`, `gdd/INDEX.md`, and
`gdd/ascendant-impact-gdd-v0.4.md` are all mechanically derived from the PDF. Editing
any of them by hand silently forks the source of truth and there is no way to detect it
afterwards. **To change what `gdd/` says, change the PDF and re-export.** If a
description in `gdd/reference/` is wrong, fix the description by re-reading the image —
never by writing in what you believe the art should show.

**3. Every answer recorded here gets a dated entry** naming:
- **what it resolves** — the `TODO.md` item number and its Q / V id, so the deletion
  from `TODO.md` is traceable;
- **the decision**, stated plainly enough to implement from;
- **who decided it and when**;
- **any GDD line it supersedes** — quoted, with its `gdd/sections/` file and PDF page.

**4. The moment an entry supersedes a GDD line, `TODO.md` gains an item** stating that
the GDD is out of date. **Clearing that item means Adrian updates the source PDF,
re-exports it, and re-extracts `gdd/`** — not editing `gdd/` and not leaving the two
out of step. Until the PDF is updated, the GDD remains the source of truth *and* is
known-stale, which is the worst state to be in silently and an acceptable state to be
in visibly.

**Superseding the GDD is a real act.** Most decisions will not do it. A decision that
merely fills a value the GDD never specified — which is what most of `TODO.md` is —
supersedes nothing. A decision that contradicts something the GDD actually says does,
and triggers rule 4.

---

## Status values

- **APPROVED** — a KIND A engineering item. A documented procedure exists and there was
  nothing to decide. It is settled and its `TODO.md` entry is deleted.
- **PROPOSED** — a KIND B design item. A designer dispatch researched it and recommends
  an answer. **It is not decided.** Its `TODO.md` entry stays open, marked PROPOSED,
  until the human designer approves or changes it. Only then is it deleted.

**Nothing supersedes the GDD yet, so rule 4 has not fired.**

## Log

### 2026-08-02 — Q22 · the 1 HP floor is permanent; the Final Clash is the only way to win

- **Status:** **APPROVED** — accepted as proposed by the designer of record, 2026-08-02.
  **This is now settled and binding on every downstream answer.**
- **Resolves:** TODO item 4 (Q22) · **BLOCKING** · KIND B · entry deleted from `TODO.md`
- **Dispatch:** group 01 → `design/group-01-blocking-q22.md`
- **Proposed decision:** reading **(b)**, sub-variant **(b2)** — `MinHealthFloor = 1` on
  the rival's `BP_HealthComponent` from `BeginPlay`, lowered to `0` only by
  `ClashSuccess()` immediately before it applies lethal damage.
- **Value lives in:** `HealthComponent.MinHealthFloor` (`design-brief.md` §13.2 row 50)
- **Unblocks:** M1-08 — Create the shared `BP_HealthComponent`
- **Why, in short:** the GDD's encounter-flow table lists exactly one win condition
  (Final Clash success), so reading (a) requires *adding* a win condition the GDD never
  writes down while (b) only widens the scope of a floor the GDD does state; it makes
  the double gate meaningful; it makes the meter — and therefore skill — the only route
  to the ending; and it is the cheapest, least leak-prone build.
- **Prior art cited:** Sekiro (Deathblow), Metal Gear Rising: Revengeance (Monsoon and
  Sundowner hard-stop at 10% into a mandatory QTE), Hi-Fi Rush, Sifu, God of War
  Ragnarök, Furi, Jedi: Fallen Order, Asura's Wrath as the cautionary case. Two claims
  are explicitly marked unverified in the group file.
- **Three attached conditions — carried forward as binding constraints on later groups:**
  **C1** Q9 must resolve to **no meter decay**, or the tail can become a dead end.
  **C2** the HUD must show **which gate is still locked** once the health bar visibly pins.
  **C3** Q2 must be tuned so **≤25% and meter 100 arrive close together**.
  These are not settled answers to Q9, the HUD, or Q2 — they are constraints those
  answers must satisfy.
- **Supersedes GDD:** none. This interprets the scope of the GDD's failed-Clash 1 HP
  floor; it edits no GDD number and contradicts no GDD line.
- **Developer note:** M1-08 can proceed either way — the clamp is identical. What must
  wait is the rival instance's default value and whether `BP_DuelDirector` wires a rival
  `OnDeath → EndDuel(Win)` path at all. Leave both unset rather than let a default
  silently become the design.

### Entry format

```markdown
### YYYY-MM-DD — <short title>

- **Resolves:** TODO item <n> (<Q/V id>)
- **Decision:** <the answer, stated plainly enough to implement from>
- **Decided by:** <name>
- **Supersedes GDD:** none
  <or>
- **Supersedes GDD:** "<quoted line>" — `gdd/sections/<file>.md`, PDF page <n>.
  TODO item added: GDD out of date.
```
