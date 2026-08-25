# Session resume — rewritten 2026-08-23

Not a gate file. The gate hooks read `designer.md`, `developer.md` and `inspector.md`;
this file is here for the next session to read **first**.

**Recompute every date on session start.** This was written with **nine days** left to the
**1 September 2026** ship date.

> **This file replaces the 2026-08-03 version wholesale.** That version said the milestone
> was "M1, not started in-engine — no `.uproject`, no `Content/` anywhere." **That is no
> longer true and had already stopped being true.** `leave-offs/STOP-2026-08-04.md` is now
> **historical**: its lost-work incident is real and recorded, but its resume list is
> superseded by `SHIP-PLAN.md`.

## Read these three, in this order

1. **[`SHIP-PLAN.md`](../SHIP-PLAN.md)** — the nine-day plan. What we build, on which day,
   and what gets cut first if a day slips. **This is now the answer to "what next".**
2. **This file** — what changed on 2026-08-23 and what state everything is in.
3. **[`game/docs/agent/PROTOTYPE_BLACKBOARD.md`](../game/docs/agent/PROTOTYPE_BLACKBOARD.md)**
   — fifteen milestones of what is actually live in the editor, plus `game/CLAUDE.md`'s
   long list of hard-won Unreal MCP gotchas. **Read the gotchas before touching the editor.**
   They will save hours, and several of them are things that fail *silently*.

## Where the project actually stands

| Thing | State |
|---|---|
| **The game** | **Exists and runs.** `game/AscendantImpact.uproject`, UE 5.8, Blueprint-only, subtree'd into this repo 2026-08-23 with Git LFS. **Fifteen milestones** built and PIE-validated |
| Milestone | Prototype route, not the planned one. Roughly **M1–M2 complete**; M3 **deferred whole**; M4 **redefined**; M5's tuned work still correctly locked |
| Phase | **Phase 1** — a duel fought start to finish, due **1 Sept 2026** |
| Coursework | **#02 through #07 all delivered.** No requirement doc on disk for #08–#10 — **ask the user** |
| Partner | **Anthony is unresponsive.** The user is now sole commander and sole designer of record |
| Scope | **Cut on 2026-08-23** — decisions **D1–D4**, in `design/decisions.md` |

## What happened this session (2026-08-23)

Planning only. **No engine work, no assets touched, no branches cut** — the user had
agents working against the live editor and a second open project is how work gets lost.

1. **Audited the real state of the build** — the root `CLAUDE.md` was stale by fifteen
   milestones and claimed nothing existed in Unreal.
2. **Named the two gaps that actually block "playable"** (below).
3. **Took four scope decisions from the designer of record** — D1–D4.
4. **Wrote [`SHIP-PLAN.md`](../SHIP-PLAN.md)** — day-by-day to 1 September, published also
   as an artifact.
5. **Truth-passed the documentation** so no agent plans against a repo that no longer
   exists: `CLAUDE.md`, `README.md`, `TODO.md`, `design/decisions.md`, this file.

## The two gaps — this is the whole job

Both are **missing systems, not tuning.** Do not try to fix either with numbers.

1. **The player wins nearly every time.** Punch costs nothing and there is no dodge, block
   or counter — mash the attack ten times and the fight is over. Nothing asks the player to
   read anything. → `SHIP-PLAN.md` **T2** (attack commitment) and **T3** (dodge, i-frames).
2. **The Vanguard repeats one move forever.** One telegraph, one swing, one wait, at one
   range, on one timing. → **T4** (three attacks) and **T5** (pressure and punish).

**Also genuinely missing:** win/loss resolution — at zero health a body drops and *nothing
happens* — plus restart and a round timer. **T1** is the cheapest high-value task on the
list and should go first.

## Do this first, next session

1. **T1 — fight-end resolution and restart.** Half a day, highest value per hour on the
   board, and it is the thing a grader notices missing in the first ten seconds.
2. **P1 — the packaging spike, on 24 August.** This project **has never been packaged
   once**, the default map is still `Lvl_ThirdPerson`, and `ModelContextProtocol` is an
   Editor-only plugin. A first UE 5.8 package failure routinely costs a day, and the 31st
   is the one day that cannot absorb it. **Do not defer this.**
3. **T2 — player attack commitment.** Then follow `SHIP-PLAN.md` by date.

## Settled 2026-08-23 — do not re-litigate

**D1 — health zero wins the duel.** The Ascension Meter, Impact Windows and the Final
Clash are **deferred future scope**. `MinHealthFloor` stays **0**.

- **This amends Q22**, which is recorded as *settled and binding*. Q22's reasoning about
  the GDD was correct; it was amended on ship-scope grounds by the only person who could.
- **Constraints C1, C2, C3 are released. Item 64 is closed by deferral, not answered.**
- **⚠ D1 supersedes a line the GDD actually states** — the Win / Loss row in §03. **Rule 4
  has fired for the first time.** The GDD is now *known-stale on that one row* until the
  PDF is revised and re-extracted. That is **`TODO.md` item 75**, it blocks no build work,
  and **no agent may edit `gdd/` to "fix" it** — `gdd/` is generated.

**D2 — three Vanguard attacks**, Phase 2 optional. Scopes `game/AGENTS.md`'s *"only Attack
A is enabled"* to the paused DataTable route. Within the scope lock, which permits four.
**Every value stays provisional.**

**D3 — material-instance recolor** is the character look. A free Fab/Mixamo swap is
optional, attempted only from a finished duel, and is the **last** thing cut — the user
wants it and it is also the likeliest to break the validated animation path.

**D4 — the `DT_VanguardAttacks` DataTable route is paused permanently** for this ship.

## Two things that used to be blockers and are not any more

**Stop surfacing both of these.** They were real, they are closed, and raising them again
costs a day of the nine.

- **V1–V5**, the five cinematic-restore corrections gating M3 sign-off. They correct a
  cinematic restore that D1 deferred. APPROVED, unapplied, and correctly at rest.
- **The countersignature on `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`.** Anthony
  signed it for a route D4 paused. Nothing is revoked; the signature simply stands over
  work that is not being done.

## Traps that will bite whoever goes next

- **The PIE world advances in real time between MCP calls.** The Vanguard keeps striking an
  idle player while you deliberate — the player can be KO'd between two tool calls. Read
  health and flags at every step; restart PIE for clean phases.
- **Compiling a Blueprint while PIE runs silently kills Slate-injected input** for the rest
  of that session. Restart PIE after any mid-session compile before trusting an input test.
- **One editor session at a time.** The user runs agents against a live editor.
- **`.uasset` files are binary and unmergeable** — two branches editing one always loses a
  side. One branch touches assets at a time.
- **`game/CLAUDE.md` has a page of Blueprint-DSL gotchas that fail silently** — positional
  args binding to `self`, ghost UMG `Tick`/`Construct` nodes, stale per-instance component
  data, OFPA level saves. **Read them; do not rediscover them.**
- **`design-brief.md`, `combat-integration-plan.md`, `build-sequence.md` and most of
  `TODO.md` describe a LARGER game than the one shipping.** They are correct documents
  about the full GDD design. **Read them as reference.** Where they disagree with
  `SHIP-PLAN.md` about the next nine days, `SHIP-PLAN.md` wins.
- **`docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md` is no longer the thing to execute.** It
  belongs to the route D4 paused.
- **Two numbering spaces overlap.** `TODO.md` **item** numbers and `design-brief.md`
  **§13.2 row** numbers both run through the high 50s and 60s and mean unrelated things.
  Always write "item N" or "§13.2 row N", never a bare number.

## Where the work lives

| Path | What |
|---|---|
| **`SHIP-PLAN.md`** | **the plan — start here** |
| `game/` | the Unreal project (LFS) |
| `game/docs/agent/PROTOTYPE_BLACKBOARD.md` | fifteen milestones of what is live |
| `game/CLAUDE.md` | how to work in the editor + the MCP gotchas |
| `design/decisions.md` | the permanent record — D1–D4 at the top of the log |
| `TODO.md` | the old worklist, with a 2026-08-23 banner marking what is deferred |
| `gdd/INDEX.md` | the GDD — `sections/` for text, `reference/` for the image sheets |
| `leave-offs/STOP-2026-08-04.md` | historical; the lost-work incident |

**`gdd/` is generated and never hand-edited.** To change it, change the PDF and re-extract.
