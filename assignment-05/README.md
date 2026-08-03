# Assignment 05 — Goal-Oriented Agent

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy martial-arts action
fighter, Unreal Engine 5.8, PC.
**Author:** AthetosTrace · **Date:** 2026-08-03 · **Repo:** `AthetosTrace/fight-game`

> **No Assignment 05 requirement document is on disk.** `assignments/` holds only #02, #03
> and #04. This submission therefore answers the two deliverables as briefed: a complete
> runnable goal-oriented agent with its configuration, and a README answering what the agent
> built, why it selected those features, and whether it ran in the game. **If the real spec
> differs, this README is the wrong shape and should be reworked against it.**

## The deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | The agent, runnable, with configuration | [`agent/`](agent/) — and live at `.claude/agents/goal-planner.md` |
| 2 | This README | you are reading it |
| — | Evidence for every claim below | [`evidence/`](evidence/) |

```
assignment-05/
├── README.md
├── agent/
│   ├── goal-planner.md        the agent
│   ├── entry_gate.py          ordering contract — PreToolUse on Task|Agent
│   ├── exit_gate.py           completion contract — SubagentStop
│   ├── check_leaveoff.py      the shared check both gates call
│   └── settings.json          how the hooks are wired
└── evidence/
    ├── TODO.md                the worklist, as it stands now
    ├── decisions.md           the permanent record of what was decided
    ├── inspection-pass1.md    cross-consistency audit — 3 violations, 11 contradictions
    ├── inspection-pass2.md    verification — 6 of 7 corrections landed
    └── inspection-pass3.md    verification — 8 of 8 landed, no violations remain
```

The copies in `agent/` are for the grader's convenience. **The live agent runs from
`.claude/agents/goal-planner.md` and the live hooks from `.claude/hooks/`.**

---

## 1. What the agent built

The agent is the reasoning layer this project ran **by hand for one full session**, written
down so it runs on its own. That session is the evidence that the loop works, because the
loop is what produced the numbers.

### `TODO.md`, before and after

| | At the start | Now |
|---|---|---|
| Open items | **45** | **65** |
| Closed | 0 | **8** |
| PROPOSED, awaiting the designer | 0 | **35** |
| Blocked on the human | 0 | **1** |
| Untouched | 45 | **29** |

**The list got longer, and that is the result, not a failure.** 45 items in meant 43 answered
across 9 dispatches — and **28 new items (46–73)** that nobody had written down. Most are
values the build genuinely needs that `design-brief.md` §13.2 **has no row for at all**, so
they appear in no question list anywhere. The rest are cross-group contradictions the
inspection caught.

The single best example: **the rival's `MaxWalkSpeed` does not exist.** §13.2 row 43 covers
the *player's* walk speed. Nothing covers Crimson Vanguard's. With a 2400 cm arena and the
Final Clash as the only way to win, **a rival slower than the player can be kited forever and
the duel cannot end.** That is a game-breaking hole in a table that looked complete, and it
surfaced only because something walked the table against the build sequence.

### The nine dispatches

Item ids below match `evidence/TODO.md`; every answer is in `evidence/decisions.md`.

| # | Group | Items | Result |
|---|---|---|---|
| 01 | **Q22, blocking** | 1 | **APPROVED.** `MinHealthFloor = 1` from `BeginPlay`, lowered to `0` only by `ClashSuccess()`. **The Final Clash is the only way to win.** Three constraints (C1–C3) now bind everything downstream |
| 02 | Combat economy | 5 | Q1 health 100 · Q2 rival 1200 · Q3 damage A32/B25/C27/D18 as % of player HP · Q4 light 5 / finisher 10 · Q5 three combo sections |
| 03 | Defensive timing | 6 | Q6 i-frames 0.28 s · Q7 perfect dodge 0.12 s · Q8 whiff lockout 0.55 s · Q26 Impact cooldown 7.0 s · Q27 recover multiplier 1.0 · Q28 buffer 0.25 s |
| 04 | Spacing and arena | 6 | Q24 arena 2400 × 1600 cm · Q10 bands A 0–260 / B 90–520 / C 240–420 / D 400–840 · Q12 cooldowns · Q13 travel 600 cm · Q11 lock-on · mezzanine ruled set dressing |
| 05 | Fighter feel | 6 | Q14/Q15/Q16 **identical for both fighters** · Echo's faceplate · emissive energy lines · "SFN" left unexpanded |
| 06 | Final Clash and meter | 5 | Q9 no decay · Q17 reuse `IA_Impact` · Q19 1.2 s · Q20 both beats 0.50 s · Q21 separation 1200 cm |
| 07 | Structure and canon | 6 | **Q25's 26 per-attack values** · Q18 failsafe 0.35 s · Q23 no timer · Q29 `VALOR-7` · plasma-gauntlet canon · SYSTEM STATS · **208 cm APPROVED** |
| 08 | Asset decisions | 3 | Q30 **Paragon: Crunch** · Q31 Phase 1 audio · **footwear rights APPROVED, exposure zero** |
| 09 | **Cinematic corrections** | 5 | **V1–V5 all APPROVED.** These clear hard check 7 — the one check `cinematic-integration-inspection.md` failed |

Volume: **10,005 lines** across 13 files in `design/`.

### It also repaired its own inputs

Before any question could be ranked, the source had to be readable. **GDD pages 10–14 are
image reference sheets that no agent on this project had ever seen** — `pdftoppm` is absent,
so the Read tool cannot render PDF pages. The embedded JPEGs were pulled straight out of the
PDF's `/XObject` resources with `pypdf` and read directly. That recovered the visual
definition of all three characters and the arena, **1,194 lines** of description in
`gdd/sections/` and `gdd/reference/`, and it immediately paid for itself: `design-brief.md`
§13.1 row 28 had **no centimetre figure for Crimson Vanguard**, and page 10 prints
**"6'10" (208 cm)"**. The blank was never a design decision — the number was simply
unreadable.

It also fixed a gate that would have deadlocked this exact session: `entry_gate.py` made the
**inspector** depend on the **developer**, so a design-only pass could never inspect
anything. The dependency is now the designer alone, and the build-coverage requirement moved
into the agent, where it belongs.

---

## 2. Why it selected those features

**The order was not a judgment call, and that is the entire design of this agent.**

### The ranking rule

Every open item is ranked by **the lowest-numbered step in `build-sequence.md` that cannot
execute until it is answered.** Items blocking nothing go last.

`build-sequence.md` holds **63 ordered Unreal editor steps**, `M1-01` through `M5-08`. It was
written by the `developer` agent in an earlier session — **before anyone asked most of these
questions.** That is what makes it a fair referee: it cannot be bent to justify a
convenient order, because it predates the argument.

The rule, stated precisely enough to check:

> **Blocking step = the lowest-numbered step that first consumes the answer** — where a real
> value, or a decided behavior, has to exist for that step's stated outcome to be achieved.

Creating an exposed variable and leaving it blank is **not** blocked — §13 tells the developer
to do exactly that. So most scalars can be *built* at their step but not *signed off*. Items
whose **logic, branch, or structure** changes with the answer are genuinely blocked, and those
are called out.

### Three real examples, with the step id

**Q5 — light combo length → `M1-17` (Author `AM_Player_LightCombo`).** Genuinely blocked, not
merely unsigned: **you cannot author a montage's sections without knowing how many there
are.** The dispatch then found the answer was forced anyway — at GDD midpoints Phase 2 leaves
a **~1.28 s** non-threatening window, and a 4-section combo runs **~1.33 s**, so four sections
**do not fit Phase 2 at all.** Group 07 later re-derived the same conclusion independently
from punish-window arithmetic.

**Q24 — arena footprint → `M1-21` (Gray-box `L_ShatteredRing`).** You cannot gray-box a floor
without dimensions. Ranking it early also exposed a dependency chain: **Q13** (Attack D
travel) is defined as a fraction of Q24, and **Q21** (failed-Clash separation) has to fit
inside it. All three had to move together or they would disagree.

**Q7 — perfect-dodge window → `M1-19` (Author `AM_Player_Dodge` with nested i-frame
notifies).** `design-brief.md` §14 calls it *"more definitive of the game's difficulty than
any other number in the table"* — but importance is not what put it at M1-19. The montage that
contains it is.

**Q31 — silent Phase 1 → `M5-04`, so it went last.** It is a real question. It blocks nothing
until the presentation pass, so it waited, and nothing was lost by waiting.

### The exception, and why the rule allows one

**Q22 was answered first regardless of rank.** Its blocking step is `M1-08`, which is not the
lowest in the list.

It decides whether the 1 HP floor the GDD states in the failed-Clash row is **permanent** or
**Clash-only** — that is, whether the Final Clash is the **only** way to win, or whether
ordinary damage can end the duel. §14 calls it *"the single most consequential open question
in the document — it changes what the game is about."*

**Every health and damage number depends on the answer.** Under the approved reading, Q2 stops
being "time to kill" and becomes "when does the gate open" — a completely different tuning
target. Answering the economy first would have produced a coherent set of numbers for the
wrong game.

So the human overrode the ranking, deliberately, and it is recorded. **A ranking rule that
cannot be overridden by a human is a worse rule** — it would have marched a session into
tuning an economy whose purpose was still undecided. The agent's binding rule encodes this:
it ranks, and a human may reorder.

### The two-kind split

| Kind | Test | Handling | Count in `TODO.md` now |
|---|---|---|---|
| **KIND A — engineering** | A documented procedure exists; there is a right answer | Closed directly | **15** |
| **KIND B — design** | No correct answer, only better and worse | Real games that solved the same problem are researched and **named**, then the recommendation returns as **PROPOSED** for a human | **58** |

Of the 43 items answered: **8 closed**, **35 returned PROPOSED**. `evidence/decisions.md`
carries **10 APPROVED** and **16 PROPOSED** status markers across nine log entries.

KIND B answers are not opinions. Q7's 0.12 s is set against **Street Fighter 6's 2-frame
Perfect Parry, Sekiro's 12-frame deflect and Street Fighter III's 10-frame parry**, with
frame counts converted and the assumed framerate stated. Q22's reading is set against
**Sekiro's Deathblow, Metal Gear Rising's Monsoon and Sundowner hard-stopping at 10% into a
mandatory QTE, and Sifu — which does *not* gate the kill, and whose designers had to steer
players away from the damage route to protect their own ending.** Where no shipped game
publishes a number, the dispatches said so: **three separate groups reported that no game
publishes per-attack boss telegraph or recovery durations**, and **Q8's magnitude is named as
the weakest number in the whole set** because nothing was found to anchor it.

### The split is enforced, not trusted

**Two items were closed as KIND A that were actually design choices, and a cross-consistency
inspection reopened both.** Q18 was closed at 0.35 s by a dispatch whose own justification
read *"any value in 0.25–0.50 works; 0.35 is the middle with a documented reason"* — which
describes a designer's choice. Q17 was closed even though §14 reads *"Designer confirms."*
Both are open again, with the recommendation intact and the authority corrected. See
`evidence/inspection-pass1.md`.

That is the classification working. **The kinds are a claim an agent makes, and the inspector
is what tests it.**

---

## 3. How goals are enforced

**There is no goal primitive in Claude Code.** No `goal:` field, no built-in success
criterion. So the goal has to be a **machine-checked condition the agent cannot declare its
way past** — and this project already had the mechanism.

### `exit_gate.py` — the completion contract

Fires on **`SubagentStop`**. When an agent tries to finish, the hook runs
`check_leaveoff.py`, which verifies three things in order:

1. `leave-offs/<agent>.md` exists;
2. it carries `status: complete` in its YAML frontmatter;
3. **the artifact it names is genuinely on disk.**

If any fails, the hook writes the reason to stderr and **exits 2 — which blocks the stop** and
hands the reason back to the agent so it goes and finishes the work.

**The reason this is a real goal and not a convention is that the hook runs outside the
agent.** An agent cannot reason its way past it, cannot decide it is close enough, and cannot
mark itself done. The condition is checked by a separate process reading the filesystem. That
is a goal in the only sense that survives contact with a language model.

There is a one-shot guard: an agent that fails twice is let through **with an explicit
warning** rather than hanging forever. Deliberate — an infinite retry is worse than a loud
failure.

### `entry_gate.py` — the ordering contract

Fires on **`PreToolUse`** matching `Task|Agent`. It reads `subagent_type`, looks up that
agent's upstream dependencies, and **denies the spawn** if any dependency is not satisfied. A
dependency is either a file that must exist or another agent's leave-off that must be
complete.

Together they are the two halves: **`entry_gate.py` refuses to start an agent whose inputs are
not ready. `exit_gate.py` refuses to let an agent finish until its output is real.**

### Where `goal-planner` sits

It is wired into `entry_gate.py` **with no upstream agent dependency**, because it runs first
and is the thing that decides what runs next — gating it behind another agent's leave-off
would deadlock the pipeline. It is not dependency-free, though: it requires
`project-brief.md`, the extracted GDD, and `build-sequence.md`. An empty dependency list would
let it spawn against an empty repo and **produce a confident plan about nothing.**

**One honest limitation.** `exit_gate.py`'s `OURS` set is `{designer, developer, inspector}`,
and it was deliberately left unmodified for this assignment. So `goal-planner` writes
`leave-offs/goal-planner.md` **by contract in its own definition, not by hook enforcement.**
Adding it to `OURS` is a one-line change and would make its completion machine-checked like
the other three. It is stated here rather than glossed, because the section above claims hook
enforcement is what makes a goal real — and this agent does not yet have it.

### The agent's own binding rule

> **It may propose and it may rank. It may never decide a design question.**

`Read` and `Write`, **no `Edit`** — it cannot modify an artifact it is auditing. **It stops
when the top-ranked item is a design question, and stopping is a success condition.** That
rule was written because a session actually needed it: two items were closed that should not
have been, and the inspector caught them.

---

## 4. Did it run in the game?

**No.**

Nothing is built in Unreal. There is no `.uproject` and no `Content/` directory anywhere in
this repository. The project is at **M1, not yet started in-engine**, and the **Unreal MCP
server is not connected** — which is item 1 in `evidence/TODO.md` and the single item blocking
all 63 build steps.

What exists is the reasoning layer and the answers it produced: the ranked worklist, 43
answered questions with their reasoning and prior art, three inspection passes, and the
approved specification text that clears the M3 gate. **That is what the next session builds
from.** It is not a playable duel and this README does not claim it is.

---

## 5. What is still open

**Point of truth: [`evidence/TODO.md`](evidence/TODO.md)** — 65 open items, each with its
blocking step id.

**The five corrections from `cinematic-integration-inspection.md`, required before M3.** That
audit returned **APPROVED WITH REQUIRED CHANGES**: nine of ten hard checks pass, and **hard
check 7, cinematic handoff safety, does not.**

| V | Defect |
|---|---|
| **V1** | No mechanism suspends the rival's Behavior Tree during the 1–3 s Impact burst. `BTTask_SelectAttack` can fire mid-burst and strand it |
| **V2** | `RestoreCombatState()` contains **no camera-return step**, while two other sections claim it does |
| **V3** | Hitbox and trace shutdown relies on notify-end firing on interruption — which Unreal documents as **unreliable** |
| **V4** | Animation cleanup is specified only on Clash failure; **mid-overlay player death is undefined** |
| **V5** | `State.Dodging` and `State.CanCounter` are missing from the restore clear list. A stale `State.CanCounter` yields **a free counter — unearned spectacle**, which is exactly what the central promise forbids |

**All five are written and APPROVED** as drop-in specification text in
`design/group-09-cinematic-corrections.md`. **They are not yet applied** — that is item 63,
and it belongs to the `combat-integration-architect`. **M1 and M2 may proceed now regardless;
only M3 is gated.**

Writing them surfaced a defect the audit had not: because restore also runs on the Impact
*failure* branch, where nothing was suspended, **implementing V5's acceptance condition
literally would have stripped a player's i-frames mid-dodge.** The fix satisfies the intent
without creating the bug.

**Unreal MCP is not connected** — item 1, and nothing in the editor happens until it is.

**Four other items worth naming**, all in `evidence/TODO.md`:

- **Item 64** — constraint **C3 from the approved Q22 is not satisfied.** Q2 = 1200 puts meter
  100 and the health gate **90–135 s apart**, not "close together". A dispatch declared
  compliance against a criterion it had substituted for the approved one. Either amend C3 on
  the record or take Q2 → 1050–1100.
- **Item 65** — Telegraph and Recover are specified **two incompatible ways**: absolute
  seconds in one place, a scale factor in `design-brief.md` §13.1 and `build-sequence.md`
  M4-04. **`M2-04` and `M4-04` cannot both be built as written**, and the four phase ratios
  (0.786 / 0.800 / 0.775 / 0.778) are not uniform, so no single scale can express them.
- **Items 49 + 67** — the rival's missing `MaxWalkSpeed`, and three groups assuming three
  different speeds.
- **Item 26** — blocked on a human: whether page 14's *"plasma-gauntlet weapons"* contradicts
  Attack A. The transcription **disclaims its own confidence**, so the dispatch refused to
  settle canon from it and wrote four questions to answer by zooming the PDF instead.

### What held up

Across three inspection passes: **zero GDD violations.** No published number altered, no
range collapsed, no fifth attack, no second arena, no per-fighter mechanical difference, no
runtime model call, no auto-success, milestone order intact. **Group 07's claim that all 26 of
its per-attack values fall inside their published GDD ranges was independently recomputed and
confirmed twice.**

The three violations found were all **process-authority** failures — agents claiming a
decision that was the human's — and all three are corrected. That distinction is the point:
the constraint system held, and what failed was agents overstepping their remit, which is
exactly what the inspector exists to catch.
