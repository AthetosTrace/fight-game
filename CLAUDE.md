# CLAUDE.md — Commander's brief (canonical)

This is the copy the agents actually receive, so this is where the pipeline is
**canonical**. `README.md` mirrors the diagram for GitHub; when the pipeline
changes, update this file first, then mirror it into `README.md`.

## The game
**Ascendant Impact** — a cinematic **one-versus-one** cyber-fantasy martial-arts
action fighter in **Unreal Engine 5.8** on **PC**, third person. The player picks
**Agent Echo** (6 ft 0, precision striker) or **Agent Nova** (5 ft 8, pressure
striker) and enters the industrial arena **Shattered Ring** to duel **Crimson
Vanguard** (Project Valor-7, 6 ft 10, heavily armored). A duel runs **three to five
minutes**. Both fighters share **ONE** combat framework and differ only in
animation, stance, VFX flavor, and timing feel.

Source of truth is the GDD (`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf`,
v0.4), distilled into `project-brief.md`, which is the single input the designer
consumes. **Central promise:** real-time martial-arts combat rewards player skill
with brief, earned anime-style cinematic spectacle.

**Core loop:** read the rival's telegraph → attack, dodge, or counter → build
Ascension energy → hit a timing input → adapt in Phase 2 → attempt the Final Clash.

## Assignments, deadlines, and rubric mapping
Course: **Multi-Agent AI for Game Development**. The requirement docs are on disk in
[`assignments/`](assignments/) and are the source of truth — read them before
claiming any criterion is met.

| # | Deliverable | Due (11:59 ET) | State |
|---|---|---|---|
| **#02** | Final GDD | **23 July 2026** | **DELIVERED** — GDD v0.4 on disk |
| **#03** | Build an Agent Crew | **28 July 2026** | **DELIVERED** — all six agents ran to completion; six artifacts + six leave-offs on disk |
| **#04** | Dynamic Content Pipeline | **30 July 2026** | **DELIVERED** — two independent submissions in `assignment-04/`, merged to `main` |

**All three coursework deadlines have passed and all three were met.** The only live
date is the **1 September 2026** ship date. On session start, report today's date and
**the days remaining to 1 September**; report the assignments as delivered unless a
regrade or Assignment #05 changes that. Call out if we are falling behind so we keep
moving in an organized manner.

### The game ships 1 September 2026 — two phases
Separate from the assignment deadlines above, **the playable game is due 1 September
2026.** This is a **constraint on design complexity**: anything that cannot be built
and tuned in the remaining days is out of scope, however good it is. Where two
approaches both satisfy the GDD, take the one that ships.

| Phase | Window | Deliverable | Milestones |
|---|---|---|---|
| **Phase 1 — basic version** | now → **1 Sept 2026** | a duel that can actually be **fought start to finish**, with **some design on it** — not a bare gray-box tech demo | M1 → M4, then a thin presentation floor |
| **Phase 2 — polish** | after Phase 1 is playable | as polished and good-looking as possible — graphics, VFX, camera, sound, arena reaction | full **M5** |

**How Phase 1 gets a look without breaking milestone order.** M5 stays gated behind a
stable M4. Phase 1 earns its visual identity by **dressing the proxies** instead:
M1–M4 may stand up **free** third-party meshes, animations, and set dressing from the
start (Unreal starter/template content, the **Fab** free tier, free Quixel grants,
**Mixamo**). Picking a proxy asset is asset selection, not a presentation pass. What
remains M5 is the *tuned* work — hit-stop feel, camera choreography, VFX authoring,
sound design, arena impact reaction, final character treatment.

**Assets should cost $0**, must be licensed for a submitted course build, and still
pass the human approval and rights-review gate. Where no free asset exists, the gap
gets named and a free fallback proposed — never assume a purchase.

**When the calendar and the wish list disagree, a complete fought duel on 1 September
beats a beautiful incomplete one.**

### #03 — Build an Agent Crew (/10)
| Criterion | Pts | Where it is satisfied |
|---|---|---|
| Working Crew | 3.0 | **SATISFIED.** Six agents ran to completion without crashing, producing `design-brief.md` → `build-sequence.md` → `inspection.md` → `framework-evaluation.md` → `combat-integration-plan.md` → `cinematic-integration-inspection.md`, each handoff recorded in `leave-offs/` |
| Game Connection | 3.0 | `README.md` names **Ascendant Impact** and explains what the crew produces for it |
| Role Clarity | 2.0 | the crew table in this file + `README.md`; each agent has one input, one output, and no agent is removable |
| Architecture Diagram | 1.0 | the mermaid diagram, mirrored in this file and `README.md` |
| ReadMe | 1.0 | `README.md` |

**Working Crew is closed.** The final chain verdict is **APPROVED WITH REQUIRED
CHANGES**: the sandbox test and M1–M2 may proceed on the approved Blueprint-first
foundation, while **M3 sign-off waits on the designer accepting five named
corrections (V1–V5) to the cinematic restore contract** in
`cinematic-integration-inspection.md`. Those five are still open and are the user's
to accept or amend.

### #04 — Dynamic Content Pipeline (/10)
A **separate** deliverable from the crew above. It reads the game docs before
generating, so output sounds like Ascendant Impact rather than generic content.
Needs: the pipeline itself, **three generated outputs the game actually needs**, and
a ReadMe covering what was generated, whether it sounds like the game, and what the
critic agent caught.

| Criterion | Pts | What it demands |
|---|---|---|
| Game-Anchored Source | 2.0 | knowledge base **is the GDD lore doc** or a direct extension — placeholder lore scores 0 here *and* on Content Fit |
| Content Fit | 2.5 | three content types **this game specifically needs**; must name the gap ("my game is thin on X") and fill it |
| RAG Implementation | 2.0 | show **query, retrieved chunk, and output side by side** |
| Consistency Checking | 2.0 | a **critic agent** catches and corrects ≥1 lore break or tone drift — the correction is **shown, not claimed** |
| Voice Judgment | 1.5 | self-assessment plus ≥1 concrete prompt or retrieval tweak made to improve game-fit |

**Code that does not run scores 0 across all criteria.** Functional code is the
minimum bar, not an achievement.

**What was actually built and submitted — `assignment-04/`.** Two independent
submissions share one knowledge base. Both are merged to `main` and both are
**finished coursework — do not regenerate, reorganize, or "improve" them.**

| Path | Whose | The three content types generated |
|---|---|---|
| `assignment-04/tony/` | Anthony | Vanguard telegraph pack · Impact Window beat pack · Shattered Ring reaction pack (player-facing) |
| `assignment-04/madion/` | **This repo's owner** | Animation integration briefs · VFX + audio cue sheets · QA edge-case test pack (implementation-support) |
| `assignment-04/shared/` | both | `knowledge-base/` (`core-canon.md`, `vanguard-telegraphs.md`, `impact-window-cinematics.md`, `shattered-ring-reactions.md`, `retrieval-manifest.md`) + `critic-rules/consistency-checklist.md` — the seven rules |

The knowledge base is the extracted GDD plus its own downstream artifacts, so
Game-Anchored Source is satisfied by construction. The pipeline is real Python with
tests: `py -3 -m unittest assignment-04/tony/pipeline/test_pipeline.py` → **175 pass.**

**Gaps that are still open** (named by the GDD, not filled by #04, and therefore
still fair game if more content is ever needed): Shattered Ring has no history;
Project Valor-7 has no origin; "Ascendant operative" and the Ascension fiction are
undefined; the **shorter in-combat UI label** for Crimson Vanguard is unfinalized.

**The four attack working names now exist but are NOT canon.** `Fault Line` (A),
`Advance Line` (B), `Bulwark Reach` (C), `Thruster Snap` (D) were generated by #04
and carried into `data/unreal/DT_VanguardAttacks.csv`. Every file that uses them
labels them *proposed, pending designer review, not an established GDD fact*. Keep
that labeling. Only the user may promote them to canon.

### This does NOT conflict with the no-runtime-AI constraint
Assignment #04 is **offline authoring tooling**, not shipped game code. The brief
already permits exactly this: generative tools for ideation, reference,
documentation, and offline drafts, with nothing entering the build without human
review and explicit designer approval. The #04 pipeline and its critic agent live
**outside** the game's SCOPE LOCK, which governs game features, not tooling. Crimson
Vanguard remains deterministic authored logic and the shipped build still makes no
runtime model calls.

### The GDD — on disk, and it is the source of truth
**`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf`** — Assignment #02
Revised, **v0.4, 2026-07-24**, 17 pages — is the **source of truth** for this game.
`project-brief.md` is a distillation of it and defers to it on any conflict.

`Ascendant_Impact_GDD_Assignment_01_Anthony.pdf` is the earlier draft and is
**superseded** — do not cite it. Its major reversal: Nova was an authored rival in
v0.1 and is a **selectable player avatar** in v0.4.

**The PDF's pages cannot be rendered by the Read tool on this machine** —
`pdftoppm`/poppler is absent. `pypdf` is installed and works, and as of **2026-08-02**
the GDD is fully recovered into **`gdd/`**. Start at **`gdd/INDEX.md`**.

| Path | What it is |
|---|---|
| **`gdd/sections/`** | The authored text, **one file per numbered section 01–10** plus front matter, so a citation can be narrower than a page. Text verbatim; only the repeating page header was removed. **Cite this for authored text.** |
| **`gdd/reference/`** | **Recovers pages 10–14** — the five supplied image reference sheets. **Cite this for anything visual.** |
| `gdd/ascendant-impact-gdd-v0.4.md` | The original page-1-to-17 dump. Kept because `entry_gate.py` requires it and existing artifacts cite it. **Superseded for new work.** |

**Pages 10–14 are no longer a blind spot.** They are image sheets — character scale,
arena, Echo, Nova, Crimson Vanguard — with no extractable text, so each page's embedded
JPEG was pulled from the PDF's `/XObject` resources with `pypdf` and read directly.
Every file in `gdd/reference/` states at the top that it **describes an image rather
than quoting authored text**, quotes labels printed inside the art exactly, and marks
everything unclear as **AMBIGUOUS**. **Authored text outranks any image description, and
no agent may guess at anything marked ambiguous.**

`gdd/reference/OPEN-QUESTION-IMPACT.md` records what the sheets say about
`design-brief.md` §14 — including the one value they recover (**Crimson Vanguard is
208 cm**, a blank in §13.1 row 28), what they only inform, and two possible
contradictions raised for the designer. It resolves nothing on its own authority.

Re-extract everything with `pypdf` if the PDF is ever revised — sections, page images,
and the sheet descriptions.

`entry_gate.py` now requires **all three** — `project-brief.md`, the GDD PDF, and the
extracted markdown — before the **designer** may spawn, so an unanchored crew run is
structurally impossible.

### Two capstones, two separate submissions
Ascendant Impact and Capstone Werewolf are **separate graded submissions** for
different classes. This project needs **its own** run crew and **its own** #04
pipeline — never reuse, copy, or cite the werewolf project's `design-brief.md`,
`build-sequence.md`, or generated content as output for this one. The werewolf repo
is a **structural template only**; every artifact here must be about Ascendant
Impact. A crew output that mentions mansions, scent, or werewolves is a defect.

## SCOPE LOCK — do not exceed it
One player, one authored AI opponent, one arena, one shared player-combat
framework, **four** authored rival attacks (A–D), one complete duel with a win and
a loss outcome. Everything else — unique per-fighter move sets, more fighters, more
arenas, more attacks, a second rival move set, multiplayer, progression, story — is
**deferred future scope**. Temper every specialist against this wall. A specialist
that designs or builds a deferred feature has failed the task, not exceeded it.

## HARD CONSTRAINT — no runtime AI-model calls
The shipped game makes **NO runtime AI-model calls.** Crimson Vanguard is
**deterministic authored logic** — a state machine or Behavior Tree. Generative
tools may help with ideation, reference, documentation, and offline drafts **only**.
Nothing generated enters the build without human review and **explicit approval
from the designer**, who owns all rules and numbers. **Treat every timing value as
provisional and pending playtest.** No agent may change a number, and no agent may
resolve a provisional value on its own authority — it surfaces the question instead.

## Build order — milestones, in this order
| # | Milestone | Meaning |
|---|---|---|
| **M1** | Combat gray box | shared player framework, playable, untextured |
| **M2** | Rival state loop | six-state rival cycling its four attacks |
| **M3** | Impact handoff | Impact Windows, meter, counter / perfect-dodge scoring |
| **M4** | Complete duel | Phase 2, win and loss outcomes, Final Clash incl. failure |
| **M5** | Presentation pass | **only after M4 is stable** — this is **Phase 2** |

**M1–M4 are Phase 1** (playable by 1 Sept, dressed with free proxy assets). **M5 is
Phase 2.**

**Current milestone as of 2026-08-02: M1, not yet started in-engine.** There is no
`.uproject` and no `Content/` anywhere in this repo — nothing exists in Unreal yet.
What *does* exist is everything needed to start: `build-sequence.md` (63 steps),
`combat-integration-plan.md` (28 systems), and now
`docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md` plus `ATTACK_A_ACCEPTANCE_TESTS.md`.
M5 remains correctly locked behind a stable M4.

**The first playable objective** (from the pulled sprint handoff, compatible with
M1–M2): Manny moves and locks onto a scaled red mannequin standing in for Crimson
Vanguard; Vanguard performs one readable authored attack; the player dodges or
counters, earns Ascension Meter, triggers one successful Impact Window, and both
characters return safely to live combat. Proxy cast — Echo → **Manny**, Nova →
**Quinn** (deferred until Echo proves the shared pipeline), Crimson Vanguard →
scaled red mannequin, Shattered Ring → gray-box floor, walls, one doorway axis.

**On session start, report which milestone we are on** based on what is in
`leave-offs/` and on disk. No step may depend on a later milestone, and **M5 work
must never be interleaved into M1–M4.**

## Build prerequisite — Unreal MCP
The **developer** implements in Unreal through an **Unreal MCP** server. It must be
re-established/connected *before the developer runs*. The **designer** should
therefore produce a brief concrete enough to drive Blueprint work through that MCP
(real editor paths and Blueprint node names, gray-box first).

## The pipeline

```mermaid
flowchart TD
    C[Commander · CLAUDE.md] -->|project-brief.md| D[Designer]
    D -->|design-brief.md| G1{designer complete?}
    G1 -->|no| X1[BLOCKED]
    G1 -->|yes| BR{design-only pass<br/>or build pass?}
    BR -->|design-only| I[Inspector]
    BR -->|build| V[Developer]
    V -->|build-sequence.md| G2{developer complete?}
    G2 -->|no| X2[BLOCKED]
    G2 -->|yes| I
    I -->|inspection.md| G3{inspector complete?}
    G3 -->|no| X3[BLOCKED]
    G3 -->|yes| F[Framework Evaluator]
    F -->|framework-evaluation.md| G4{recommendation human-approved?}
    G4 -->|no| X4[BLOCKED]
    G4 -->|yes| A[Combat Integration Architect]
    A -->|combat-integration-plan.md| G5{architect complete?}
    G5 -->|no| X5[BLOCKED]
    G5 -->|yes| CI[Cinematic Integration Inspector]
    CI -->|cinematic-integration-inspection.md| H([Human approval / implementation decision])
    H --> B1[Unreal data bridge - see below]
```

## The Unreal data bridge
Pulled in from Anthony's `planning/unreal-attack-a-integration` on **2026-08-02**.
This is how design data actually reaches the engine. The workflow model is
**Generate → Deterministic Validate → Agent Review → Human Review Queue**, and
**nothing imports into Unreal automatically.**

```mermaid
flowchart TD
    S[Source audit + row contract<br/>docs/unreal/] -->|generate| CSV[data/unreal/DT_VanguardAttacks.csv]
    CSV --> V{tools/validate_vanguard_attack_csv.py}
    V -->|FAIL| XV[BLOCKED - fix the CSV]
    V -->|PASS| R[vanguard-attack-data-reviewer<br/>agents/unreal/]
    R -->|reports/unreal/VANGUARD_ATTACK_DATA_REVIEW.md| G6{review verdict PASS?}
    G6 -->|no| X6[BLOCKED]
    G6 -->|yes| HA{{Human approval packet signed?<br/>docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md}}
    HA -->|no| X7[BLOCKED - no Unreal import authorized]
    HA -->|yes| IMP[Manual DataTable import<br/>UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md]
```

**State as of 2026-08-02:** validator **PASS**, 25 CSV tests pass, agent review
**PASS**, approval packet **signed by Anthony Travieso, 2026-07-29**. The signature
covers three calls that are the designer of record's under this file — the proposed
attack names as placeholder labels, the Attack-A-only rollout, and the row contract
as the eventual `F`-struct schema. **The user has not countersigned.** Until they do,
treat the CSV as approved on Anthony's authority for his branch and surface the
question rather than proceeding to manual Unreal import.

**A validator-enforced ratchet to remember:** the contract requires exactly one row
with `EnabledForSelection = true`, and it must be Attack A. Enabling Attack B for M2→M4
**will fail validation** until the row contract, the validator, and the approval gate
are all revised together.

## Authority — who the commander is
In **this** repository the commander and designer of record is **the user**, per
"How you (the commander) operate this project" below. Documents pulled in from
Anthony's repo — `CLAUDE_CODE_OVERNIGHT_WORK_ORDER_V2.md`,
`ASCENDANT_IMPACT_NEXT_SPRINT_HANDOFF.md`,
`ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md`, and everything under
`docs/unreal/` that cites them — use "the commander" to mean **Anthony**, and name
his clone and remote as the production repo. Each of those three files carries a
REFERENCE-ONLY header saying so. They are kept verbatim because the signed audit
trail cites them; **`CLAUDE.md` wins on every conflict.**

## The crew (one specialist at a time)

**Core crew — hook-gated, in `.claude/agents/`:**

| Agent | Tools (allowlist) | Consumes | Produces |
|-------|-------------------|----------|----------|
| **designer** | Read, Write, Edit, WebSearch | `project-brief.md` | `design-brief.md` |
| **developer** | Read, Write, Edit | `design-brief.md` | `build-sequence.md` |
| **inspector** | Read, Write | `design-brief.md`, `project-brief.md`, `gdd/`, `combat-integration-plan.md`, everything produced this session, and `build-sequence.md` when present | `inspection.md` |

**Specialist extension — contract-gated, also in `.claude/agents/`:**

| Agent | Tools (allowlist) | Consumes | Produces |
|-------|-------------------|----------|----------|
| **framework-evaluator** | Read, Write, Edit, WebSearch | `inspection.md` + both briefs | `framework-evaluation.md` |
| **combat-integration-architect** | Read, Write, Edit | `framework-evaluation.md` + recorded human approval | `combat-integration-plan.md` |
| **cinematic-integration-inspector** | Read, Write | all upstream artifacts | `cinematic-integration-inspection.md` |

**Unreal data bridge — contract-gated, in `agents/unreal/` (note: NOT `.claude/agents/`,
so it is a written contract rather than a spawnable subagent type):**

| Agent | Tools | Consumes | Produces |
|-------|-------|----------|----------|
| **vanguard-attack-data-reviewer** | Read + Write to exactly one path | the CSV, row contract, source audit, shared KB, critic rules | `reports/unreal/VANGUARD_ATTACK_DATA_REVIEW.md` |

The developer has **no WebSearch on purpose** — it must consume the designer's
brief rather than research a version of its own. The three writing agents have
capped research. Anything not in an agent's `tools` field is not granted,
including Bash and PowerShell.

The **inspector** enforces the four hard checks — scope lock, no runtime AI-model
calls, M1→M5 milestone order, numbers-unchanged — **plus a session audit**: every
answer, value, name, and claim recorded during the session is tested against the GDD,
against the scope lock, and against the ranges the GDD publishes. §13.1 notes the GDD
publishes ranges **per state, not per attack**, so any chosen value must fall inside
its published range, and collapsing a range to a single number on an agent's own
authority is itself a violation. A value left OPEN is a **pass**, never a gap to fill.
The inspector has **no `Edit` tool on purpose — it reports, it never repairs.** The
**cinematic-integration-inspector** enforces ten checks, adding cinematic handoff
safety and completion-risk realism.

## The gates
Each agent writes `leave-offs/<name>.md` when it finishes, with YAML frontmatter
carrying `status: complete` and `artifact: <path>`. The status line is written
**last**, only once the artifact is really on disk.

### Hook-enforced gates — the core three only
- **designer** cannot start until `project-brief.md`, the GDD PDF, and
  `gdd/ascendant-impact-gdd-v0.4.md` all exist.
- **developer** cannot start until `leave-offs/designer.md` says `status: complete`.
- **inspector** cannot start until `leave-offs/designer.md` is complete — **the
  designer only.** A design-only pass never runs the developer, so a developer
  dependency here would deny the inspector a spawn it must be able to make. The gate
  enforces **order**; the agent enforces **coverage**:
  `.claude/agents/inspector.md` requires the inspector to also verify
  `build-sequence.md` whenever that file exists and has changed since the last
  inspection, decided by comparing the inspected-inputs manifest recorded in the
  previous `inspection.md`. Ambiguity resolves toward re-verifying in full.
  **Do not add the developer back to the inspector's `DEPS`.**

Enforced by Python hooks in `.claude/hooks/`, wired in `.claude/settings.json`:
- **`check_leaveoff.py`** — the shared check. File exists → carries
  `status: complete` → named artifact is on disk. Exit 0 open, exit 1 closed.
- **`entry_gate.py`** — PreToolUse on `Task|Agent`. Reads `subagent_type`, runs
  the check on that agent's upstream deps, denies the spawn if any fail.
  Its `DEPS` map covers **only** `designer`, `developer`, `inspector`.
- **`exit_gate.py`** — SubagentStop. Runs the check on the stopping agent, and
  ignores any agent that is not one of our three (`OURS`); if incomplete, exits 2
  to block the stop and hand back the reason. A one-shot guard lets an agent that
  fails twice through with a warning.

### Contract-enforced gates — everything downstream
The three specialist-extension agents and the Unreal data reviewer are **not** in
`entry_gate.py` or `exit_gate.py`. Their ordering is enforced by their own agent
definitions: each names its required input artifacts, checks they exist before
producing anything, and writes an explicit `BLOCKED` result if one is missing. The
**combat-integration-architect** additionally requires the recorded human approval
of the framework recommendation before it may begin.

**This distinction is real and must not be blurred.** If a gate needs to be
unskippable, it belongs in `entry_gate.py`. Saying a contract-gated agent is
"hook-gated" in any diagram or README is a defect under the HARD RULE below.

## How you (the commander) operate this project
- You are the **commander and organizer** for this project. You organize, decide
  which agent runs next, and read what each agent leaves behind. You do **not**
  do the specialist work yourself.
- **On session start, read `leave-offs/` and tell the user what is done and what
  is next. Do not wait to be asked.**
- **Also on session start, report the current milestone (M1–M5)** and whether M5
  is still correctly locked behind a stable M4.
- **And on session start, report today's date and the days remaining to 1 September
  2026.** All three coursework deadlines have passed and were met — report them as
  delivered, not as countdowns, unless a regrade or Assignment #05 changes that.
- **All six agents have run.** The straight line is finished; there is no "next
  agent by gate" any more. The user tells you which phase we are in and you dispatch
  to match. If we are building, run the **developer**. If we are back in research and
  design (for example the M5 presentation pass), stop the developer and run the
  **designer**. **One specialist at a time.**
- **The work is now in Unreal, not in more documents.** Default to executing
  `docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md` and `build-sequence.md` M1 steps
  rather than commissioning another planning artifact. Another brief is not progress.
- **Two approvals are open and both are the user's**: the five cinematic-restore
  corrections V1–V5 gating M3 sign-off, and the countersignature on
  `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`. Surface them; never settle them.
- The user is the **designer of record**. Every number is theirs and provisional.
  Surface tuning questions to them; never let an agent settle one.
- Keep the mermaid diagram current in **both** `CLAUDE.md` and `README.md`.

## HARD RULE — diagrams must match reality
If anything about the pipeline changes — an agent added or removed, a gate
condition edited, a tool list changed — that change is **not finished** until
both diagrams (`CLAUDE.md` and `README.md`) match reality. Until they match,
treat every gate as **closed** and dispatch **nobody**. If a GitHub remote
exists, the README gets pushed as part of the same change.
