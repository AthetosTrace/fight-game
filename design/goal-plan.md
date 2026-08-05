# Goal plan — Ascendant Impact

**Produced by:** `goal-planner` (runs first; no upstream agent dependency)
**Consumes:** `gdd/sections/`, `gdd/reference/`, `design/`, `design/decisions.md`, `TODO.md`, `build-sequence.md`
**Produces:** this document — an ordered worklist and **one** dispatch recommendation
**Date:** 2026-08-04 · **Ship date:** 2026-09-01 — **28 days remaining**
**Milestone:** **M1, not started in-engine.** No `.uproject`, no `Content/` in this repository.

> **What this document may and may not do.** It may propose and it may rank. It may
> **never** decide a design question. Every timing value, every health number, every range
> band, every naming decision, and every interpretation of an ambiguous GDD line belongs to
> the human designer, who is the designer of record. **No number in this file is new.** No
> published range is collapsed. No value marked OPEN is filled. Nothing outside this file
> was edited — the `goal-planner` has `Read` and `Write` and deliberately **no `Edit`**.

---

## 1. Inputs read

### Read directly this run

| # | Path | Lines | Why |
|---|---|---|---|
| 1 | `gdd/INDEX.md` | 79 | the map; how to cite |
| 2 | `gdd/sections/00-front-matter.md` | 17 | version, engine, revision-marker key |
| 3 | `gdd/sections/01-executive-summary.md` | 38 | high concept, **scope lock**, pillars |
| 4 | `gdd/sections/02-real-time-combat-and-selectable-player-roster.md` | 55 | control model, core loop, **shared player-kit scope rule**, Impact Window times, onboarding rule |
| 5 | `gdd/sections/03-ascension-meter-final-clash-and-encounter-flow.md` | 51 | meter 0–100 and all five gains, single gate, failed-Clash resolution |
| 6 | `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` | 52 | **the six-state timing table**, runtime-AI boundary, four-attack set, Phase 2 |
| 7 | `gdd/sections/05-gray-box-vertical-slice-and-technical-milestones.md` | 41 | **M1–M5** with required proof and gates, implementation safeguards |
| 8 | `gdd/sections/06-ai-assisted-development-architecture.md` | 30 | human approval gate, **no runtime LLM** |
| 9 | `gdd/sections/07-character-readability-scale-and-opening-flow.md` | 51 | readability table, heights 173/183/208, fair-reach rule, opening flow |
| 10 | `gdd/sections/08-visual-assets-and-official-version-1-arena.md` | 46 | arena direction, five arena requirements, sheet captions |
| 11 | `gdd/sections/09-course-scope-lock-and-future-expansion.md` | 41 | **scope lock**, deferred scope, definition of done |
| 12 | `gdd/sections/10-revision-log-and-open-design-decisions.md` | 48 | provisional-decisions list, central promise |
| 13 | `gdd/reference/page-10-character-scale-reference.md` | 93 | the 208 cm figure; width contrast; AMBIGUOUS list |
| 14 | `gdd/reference/page-11-established-arena-reference.md` | 98 | rectangular hall, zero obstacles, mezzanine, **no dimensions** |
| 15 | `gdd/reference/page-12-agent-echo.md` | 101 | 3-swatch palette; "Visor or Light" AMBIGUOUS |
| 16 | `gdd/reference/page-13-agent-nova.md` | 125 | 4-swatch palette; "SFN" AMBIGUOUS; two printed typos |
| 17 | `gdd/reference/page-14-crimson-vanguard.md` | 122 | SYSTEM STATS, "plasma-gauntlet" low-confidence transcription |
| 18 | `gdd/reference/OPEN-QUESTION-IMPACT.md` | 197 | what the sheets do and do not resolve in `design-brief.md` §14 |
| 19 | `TODO.md` | 574 | the outstanding list, its ⏳ PROPOSED index, its ranking rule |
| 20 | `design/decisions.md` | 565 | **the permanent record** — the four rules, the status vocabulary, nine dated entries, the 2026-08-03 corrections note |
| 21 | `design/inspection-design-answers.md` (pass 1) | 523 | 3 process-authority violations, 11 cross-group contradictions |
| 22 | `design/inspection-design-answers-pass2.md` (pass 2) | 341 | 6 of 7 corrections landed; N1–N7 |
| 23 | `design/inspection-design-answers-pass3.md` (pass 3) | 279 | **highest-numbered pass — read first, supersedes 1 and 2 on any disagreement.** 8 of 8 claims landed; P1–P5 |
| 24 | `build-sequence.md` | 933 | **the referee for the ranking** — steps `M1-01` … `M5-08` |
| 25 | `design-brief.md` §12.4 → end (lines 880–1091) | 1091 total | **§13.1** carried GDD values, **§13.2** rows 29–57, **§14** Q1–Q31, §15 compliance |
| 26 | `inspection.md` (Assignment #03 build-tracing pass) | 217 | no violations, no orphans, no gaps — one observation only |
| 27 | `cinematic-integration-inspection.md` | 236 | ten hard checks; **§8 corrections 1–6**; §9 human-approval items 1–12 |
| 28 | `leave-offs/SESSION-RESUME.md` | 131 | the handoff the gate files do not carry |
| 29 | `data/unreal/DT_VanguardAttacks.csv` | 5 (header + 4 rows) | §9 of this plan |
| 30 | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` | 116 | §9 — the schema |
| 31 | `tools/validate_vanguard_attack_csv.py` | 359 | §9 — the deterministic validator |
| 32 | `design/group-09-cinematic-corrections.md` (lines 1–90) | 975 total | V1–V5 status line and engine-fact ledger |
| 33 | `design/group-08-assets.md` (lines 180–219) | 492 total | Q31's "Where it lands" line — the half item 73 does not quote |

`CLAUDE.md` was supplied as project instructions rather than opened with `Read`, so it
carries no line count here. It is treated as authoritative on the pipeline, the crew, and
the two open approvals.

### Read indirectly, and named so the omission is visible

**The nine `design/group-0*.md` dispatch files were not opened in full this run.** Their
content reaches this plan through three channels that were opened in full: `design/decisions.md`
(which carries a dated log entry per group, including each group's *"tensions carried
forward"*), and inspection passes 1–3 (which read the group files directly, enumerated all
eleven cross-group contradictions, and re-verified 26/26 of Q25's values against a freshly
re-read GDD §04). Two group files were spot-read where this plan makes a new claim about
them (rows 32 and 33 above).

Line counts are carried from the pass-1 and pass-3 manifests so the next run can still
detect drift:

| Path | Lines (pass-3 manifest where recorded, else pass-1) |
|---|---|
| `design/group-01-blocking-q22.md` | **390** (was 378 at pass 1, 385 at pass 2 — see pass-3 claim 7) |
| `design/group-02-combat-economy.md` | 681 |
| `design/group-03-defensive-timing.md` | 1243 |
| `design/group-04-spacing-and-arena.md` | 1067 |
| `design/group-05-fighter-feel.md` | 1086 |
| `design/group-06-final-clash.md` | 1197 |
| `design/group-07-structure-and-canon.md` | 1162 |
| `design/group-08-assets.md` | 492 |
| `design/group-09-cinematic-corrections.md` | 975 |

**If a future run finds a different count on any of these nine, treat this plan's coverage
of that group as stale and re-open the file.**

---

## 2. What the game is

Restated only from `gdd/sections/`, each line cited. **This is the wall every item below is
held against.**

### The scope lock

> *"The course prototype remains one player, one authored AI opponent, one official arena,
> one shared player-combat framework, four authored rival attacks, and one complete duel
> with win and loss outcomes."*
> — `gdd/sections/01-executive-summary.md`, PDF p. 1

`gdd/sections/09-course-scope-lock-and-future-expansion.md` (PDF p. 15) enumerates what is
**included** — two selectable avatars on **one shared core combat framework**, one boss with
**six states, four attacks, and a parameter-based Phase 2**, one arena, one duel, complete
win/loss, Impact Window onboarding, meter, Clash unlock, failed-Clash recovery, human
approval gates — and what is **deferred**: PvP, unique Echo/Nova move sets, separate balance
systems, a playable Vanguard, multi-enemy encounters, campaign progression, additional
arenas, transformations, second boss kits, extra characters, modes, weapons, story chapters.

**The consequence that binds this plan:** Echo and Nova share one framework
(`gdd/sections/02-…`, NEW — SHARED PLAYER-KIT SCOPE RULE, PDF p. 2–3), so **any per-fighter
mechanical difference is a violation.** Their permitted differences are *"animation
presentation, stance and movement personality, VFX language, timing flavor, and character
introduction."*

### No runtime AI-model calls

> *"Crimson Vanguard is controlled by authored Unreal gameplay AI. The packaged duel makes
> no runtime LLM calls, does not learn from the player, and does not generate attacks or
> choreography dynamically."*
> — `gdd/sections/04-crimson-vanguard-authored-rival-ai.md`, PDF p. 5

Reinforced by `gdd/sections/06-ai-assisted-development-architecture.md` (PDF p. 7): runtime
opponent allowed support = **None**; *"Crimson Vanguard uses deterministic authored AI; no
runtime LLM."* Assignment #04's pipeline is offline authoring tooling and sits outside this
wall by `CLAUDE.md`'s own carve-out.

### No auto-success

> *"Failure does not auto-correct the input; the game returns immediately to normal combat."*
> and *"The game does not press the input for the player and does not convert a miss into
> success."*
> — `gdd/sections/02-real-time-combat-and-selectable-player-roster.md`, PDF p. 3

### The six-state table — the most frequently violated thing in this project

`gdd/sections/04-…` publishes **ranges, per state, not per attack** (PDF p. 5):

| State | Phase 1 | Phase 2 |
|---|---|---|
| Idle / Reposition | 0.60–1.20 s | 0.35–0.80 s |
| Select Attack | 0.10–0.20 s | 0.10–0.20 s |
| Telegraph | 0.55–0.95 s | 0.40–0.75 s |
| Active Attack | 0.18–0.45 s | 0.18–0.45 s |
| Recover | 0.45–0.90 s | 0.35–0.75 s |
| Return to Neutral | 0.10–0.20 s | 0.10–0.20 s |

Reproduced here **only** to state the wall. Choosing a value inside a published range is
what the designer does; rewriting the range, or collapsing it to a point on an agent's
authority, is a violation. Phase 2 is *"the same four authored attacks — no transformation
rig and no second move set."*

### Milestone order M1 → M5

`gdd/sections/05-gray-box-vertical-slice-and-technical-milestones.md` (PDF p. 6–7):
**M1** combat gray box · **M2** rival state loop (all six states, one attack, *"Returns to
Neutral every attempt"*) · **M3** Impact handoff (*"No forced success or stranded cinematic
state"*) · **M4** complete duel · **M5** presentation pass, gate = *"Only after M4 is
stable."* Its safeguards also bind: visible debug state names, gameplay timing separated
from presentation, **explicit restore after every Impact Window and Final Clash branch**,
both avatars validated against the same tests, and *"Treat all timing ranges, meter values,
and health thresholds as provisional until validated through playtesting and finalized by
the designer."*

`CLAUDE.md` adds the calendar shape: **M1–M4 are Phase 1**, due 1 September; **M5 is
Phase 2**. Phase 1 may dress the proxies with free third-party assets — that is asset
selection, not a presentation pass.

### Every published GDD number, carried in `design-brief.md` §13.1

Session 3–5 min (target, not a timer) · First Impact Window **0.75 s** · Standard Impact
Window **0.35–0.50 s** · burst **1–3 s** · meter **0–100** · gains **+5 / +12 / +15 / +20 /
+0** · Clash gate **meter 100 AND rival health ≤ 25 %** · failed Clash **1 HP floor /
meter to 50 / 3 s cooldown** · Phase 2 at **50 %** · the six-state ranges above · heights
**183 / 173 / 208 cm**.

**None of these may move.** Every item below either fills a blank the GDD never wrote, or
is a process/record item; **not one proposes changing a published number.**

---

## 3. What is decided

`design/decisions.md` governs status. Its vocabulary:

- **APPROVED** — a KIND A engineering item with a documented procedure and nothing to
  decide. Settled; its `TODO.md` entry is deleted.
- **PROPOSED** — a KIND B design item a dispatch researched and recommends. **Not decided.**
  Its `TODO.md` entry stays open until the human approves or changes it.
- **BLOCKED ON HUMAN** — blocked, and not unblockable by this plan.

**Trust the status field over the prose.** `design/group-07-structure-and-canon.md` still
reads `APPROVED` for Q18 at its lines 13 and 425, and `design/group-02-combat-economy.md`
line 602 still reads *"C3 is satisfied"* — both are stale (inspection pass 3, findings P3
and N6). `decisions.md` and `TODO.md` win.

### The counts

| Status | Count | What |
|---|---|---|
| **APPROVED** | **8** items, in **4** decision entries | Q22 (item 4) · V1–V5 (items 34–38) · item 20 (branding exposure) · item 28 (208 cm) |
| **PROPOSED** | **35** items across 8 group entries | the whole ⏳ index in `TODO.md` lines 28–37 |
| **BLOCKED ON HUMAN** | **1** | item 26 — the "plasma-gauntlet" canon question |
| **Untouched** | **30** | item 1, items 46–74 |
| **Total open in `TODO.md`** | **66** | header line 3, and it reconciles |

`decisions.md` holds **nine dated log entries** plus the 2026-08-03 corrections note.
**Rule 4 has not fired: nothing recorded supersedes a GDD line.** The two supersessions on
record are of `design-brief.md` — §13.1 row 28's missing cm figure (item 28) and §12.6's
*"no free sound source verified"* (group 08 Q31). Item 28 is a transcription **from** the
GDD, so it does not trigger rule 4.

### The settled decisions that bind everything downstream

**1. Q22 — the 1 HP floor is permanent; the Final Clash is the only way to win.**
APPROVED by the designer of record, 2026-08-02. `MinHealthFloor = 1` on the rival's
`BP_HealthComponent` from `BeginPlay`, lowered to `0` only by `ClashSuccess()`. Lives in
`HealthComponent.MinHealthFloor` (`design-brief.md` §13.2 row 50). Unblocks **M1-08**.
Three attached constraints bind every later answer:

- **C1** — Q9 must resolve to **no meter decay**. *(Group 06 proposes none. Satisfiable.)*
- **C2** — the HUD must show **which gate is still locked** once the health bar pins.
  *(Mandatory, not optional — group 02's post-failed-Clash inert-damage tension makes it so.)*
- **C3** — Q2 must be tuned so **≤ 25 % rival health and meter 100 arrive close together**.
  **NOT SATISFIED.** This is `TODO.md` item 64 and it is live.

**2. V1–V5 — the five cinematic-handoff corrections.** Recorded APPROVED (KIND A) in the
group 09 entry, as **drop-in specification text** for `combat-integration-plan.md`. They
clear hard check 7. **They are written and NOT APPLIED** — applying them is item 63, and it
belongs to the `combat-integration-architect`. Four narrow carve-outs were correctly left
PROPOSED and became items 59–62. *(An authority question about the APPROVED status itself is
raised as new item **N5** in §4.)*

**3. Item 20 — branding exposure is zero.** The swoosh appears only on GDD concept sheets,
on no asset in the build or the plan. Remedy: a recorded five-minute verification at
**M1-23** plus a one-sentence constraint on M5-06 art. The **legal characterization** was
referred to a human and is not settled by the item.

**4. Item 28 — Crimson Vanguard is 208 cm.** 82 in × 2.54 = 208.28, rounded exactly as 183
and 173 are. Lives in `BP_CrimsonVanguard` mesh scale (`design-brief.md` §13.1 row 28).
Unblocks **M2-05**. **Caveat that must travel with it: width is still unspecified — do not
derive a capsule radius from page 10's "roughly twice the shoulder width."**

### What the inspections settled, and what they left live

Three passes. **Zero GDD violations in all three.** Pass 1 found 3 process-authority
violations and 11 cross-group contradictions; pass 2 verified 6 of 7 corrections; pass 3
verified 8 of 8 and found no remaining violation. **Q25's 26 values re-check 26/26 in range
against a freshly re-read GDD §04**, and no published range was collapsed anywhere.

What is still live from them is carried in the list below as items 64–73 plus pass-3's P1–P5
(items **N9**, **N11** and **N13** in §4).

---

## 4. The outstanding list, ranked

**79 outstanding items: the 66 in `TODO.md` plus 13 this run found that no list holds.**
The 13 new ones are prefixed **N** so they cannot collide with `TODO.md` item numbers or with
`design-brief.md` §13.2 row numbers — the two spaces that already overlap at 58–61.

Legend. **KIND A** = engineering, a documented procedure exists. **KIND B** = design, the
human decides. **BLOCKING** = changes *what the game is*, not how it is tuned. **GB** =
*genuinely blocked* — the step's logic, branch, or structure changes with the answer, so the
step cannot be built, not merely not signed off. Everything without **GB** can be built at
its step as an exposed variable left blank (`design-brief.md` §13) and signed off later.

### M1-01 — Confirm the base project

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **1** | **Unreal MCP is not connected.** `CLAUDE.md` makes it a prerequisite *before the developer runs*. **GB — this blocks all 63 build steps.** | **A** | **M1-01** | environment / tooling; no §13 row |
| **N1** | **No manual-execution fallback policy if the Unreal MCP fails.** `cinematic-integration-inspection.md` §9 item 5, `OPEN — designer decides`. Not on any list. Contingency: blocks nothing while the MCP works. | **B** | **M1-01** | process; no §13 row |

### M1-05 — Create `DA_TuningGlobals`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **2** | **Q1 — player max health.** Both fighters identical (SHARED PLAYER-KIT SCOPE RULE). | **B** | **M1-05** | `DA_TuningGlobals.PlayerMaxHealth` — §13.2 row 29 |
| **3** | **Q2 — Crimson Vanguard max health.** | **B** | **M1-05** | `DA_TuningGlobals.CrimsonVanguardMaxHealth` — §13.2 row 30 |
| **64** | **C3 from the APPROVED Q22 is NOT satisfied.** Two recorded paths: amend C3 explicitly, or re-tune Q2. **A dispatch already tried to amend the criterion instead — that was the violation.** | **B** | **M1-05** | §13.2 row 30 + the Q22 constraint record in `design/decisions.md` |

### M1-09 — Create `BP_DuelDirector`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **5** | **Q23 — is there a duel timer?** **GB** — the answer decides whether the variable exists at all and whether there is a third terminal branch. | **B** | **M1-09** | `BP_DuelDirector` — §13.2 row 51 |

### M1-10 — Create the Enhanced Input assets

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **6** | **Q17 — do the Clash beats reuse `IA_Impact`?** Reopened 2026-08-03; §14 reserves the confirmation to the designer. **GB** — `IMC_Duel` needs a second binding if the answer is no. | **B** | **M1-10** | `IMC_Duel` — §13.2 row 45 |

### M1-12 — Create `DA_FighterProfile` + Echo and Nova instances

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **7** | **Q14 — Echo / Nova montage play-rate ("timing flavor").** | **B** | **M1-12** | `DA_FighterProfile.MontagePlayRate` — §13.2 row 42 |
| **8** | **Q15 — Echo / Nova `MaxWalkSpeed`.** | **B** | **M1-12** | `DA_FighterProfile` — §13.2 row 43 |
| **9** | **Q16 — Echo / Nova dodge distance.** | **B** | **M1-12** | `DA_FighterProfile.DodgeDistance` — §13.2 row 44 |
| **67** | **Three dispatches assume three different speeds** — 500 cm/s, 600 uu/s, and 600 uu/s used as the *rival's* speed. Invalidates two whiff/separation proofs. | **B** | **M1-12** | same rows as 8, plus item 49's missing home |

### M1-16 — Create `BP_LockOnComponent`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **10** | **Q11 — lock-on max range, break range, camera interp speed.** | **B** | **M1-16** | `BP_LockOnComponent` — §13.2 row 39 |
| **52** | **Locked-on strafe speed multiplier.** | **B** | **M1-16** | **no §13.2 row.** Proposed home `DA_FighterProfile`; consumed by `BP_LockOnComponent` strafe-facing |
| **53** | **Locked-on backpedal multiplier.** | **B** | **M1-16** | **no §13.2 row.** Same proposed home |

### M1-17 — Author `AM_Player_LightCombo`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **11** | **Q4 — player light-hit damage, and whether the finisher hits harder.** | **B** | **M1-17** | `AM_Player_LightCombo` notify data — §13.2 row 32 |
| **12** | **Q5 — light combo length (number of sections).** **GB** — you cannot author a montage's sections without knowing how many there are. | **B** | **M1-17** | `AM_Player_LightCombo` — §13.2 row 33 |

### M1-18 — Create the player combat notify states / notify

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **13** | **Q28 — `ANS_ComboLink` input-buffer window.** | **B** | **M1-18** | `AM_Player_LightCombo` / `ANS_ComboLink` — §13.2 row 56 |
| **N2** | **The approved sandbox combo-buffer test has not been run, and where to run it is undecided.** `cinematic-integration-inspection.md` §9 item 2 and §6 Proof A: one buffered light-attack chain in a disposable 5.8 project, three pass conditions, delete on completion. It is the approved *first* test and it exercises the mechanism M1-18, M3-07 and M4-06 all reuse. Not on any list. | **B** (whether/where; the procedure itself is A once decided) | **M1-18** | process; no §13 row |

### M1-19 — Author `AM_Player_Dodge` with nested i-frame notifies

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **15** | **Q7 — perfect-dodge sub-window.** §14: *"This single number does more to define the game's difficulty than any other in the table."* Must be strictly narrower than Q6. | **B · BLOCKING** | **M1-19** | `ANS_PerfectDodge` — §13.2 row 35 |
| **14** | **Q6 — dodge i-frame window.** | **B** | **M1-19** | `ANS_IFrame` — §13.2 row 34 |
| **47** | **Does a dodge cancel `AM_Player_LightCombo`?** **GB** — a branch, not a scalar. Decides whether Q28's buffer is a kindness or a Phase 2 trap. | **B** | **M1-19** | **no §13.2 row.** `BP_CombatComponent` / `ANS_ComboLink` |
| **48** | **Total length of `AM_Player_Dodge`.** **GB** — Q6 and Q7 are authored inside it and currently have no container. | **B** | **M1-19** | **no §13.2 row.** `AM_Player_Dodge` |
| **N3** | **Motion Warping plugin adoption is unapproved.** `cinematic-integration-inspection.md` §9 item 3 lists plugin adoption *including Motion Warping* as `OPEN — designer decides`, and both plans assume none. Group 05's Q16 is *delivered by Motion Warping* specifically so displacement never travels through play rate; `build-sequence.md` M4-01 names it again as R5 for Attack D. **GB** — if the answer is no, Q16's delivery mechanism and the M4-01 D-travel mechanism both change. Not on any list. | **B** | **M1-19** | plugin / project settings; no §13 row |

### M1-20 — Wire the counter input and player counter montages

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **46** | **The counter's own success window.** Q7 covers the perfect *dodge*; **nothing covers the perfect *counter*.** | **B** | **M1-20** | **no §13.2 row.** Player side of `ANS_CounterWindow` |
| **16** | **Q8 — whiffed-counter recovery.** | **B** | **M1-20** | `AM_Player_CounterWhiff` — §13.2 row 36 |
| **55** | **The successful-counter recovery length.** Q19 is authored as `CounterRecoveryLength + 0.6 s` and cannot be locked without it. **Step-id note: `TODO.md` files this at M4-05. The montage it lives on, `AM_Player_Counter`, is authored at M1-20, which is where the value first has to exist.** | **B** | **M1-20** *(TODO: M4-05)* | **no §13.2 row.** `AM_Player_Counter` |

### M1-21 — Gray-box `L_ShatteredRing`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **17** | **Q24 — arena playable footprint.** **GB** — you cannot gray-box a floor without dimensions. The recovered arena sheet fixes the *shape* (rectangular, chamfered, zero obstacles) and carries **no dimensions, no scale bar, no human figure**, so it cannot supply the number. | **B** | **M1-21** | `L_ShatteredRing` + `DA_TuningGlobals` — §13.2 row 52 |
| **18** | **Is the arena mezzanine reachable, or set dressing?** **GB** — decides whether a blocking volume and NavMesh exclusion exist at all. | **B** | **M1-21** | **no §13.2 row.** `L_ShatteredRing` |

### M1-23 — Stand up the dressed proxies

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **19** | **Q30 — Paragon heavy hero for Crimson Vanguard: yes or no, and by when?** **Deadline-bearing:** if yes it must land before M4 range tuning, or every Q10 range value re-tunes twice. Group 08 sharpens it to *before M2-04/M2-05 are authored*, calendar backstop **2026-08-09 — five days from today.** | **B** | **M1-23** | asset selection → `BP_CrimsonVanguard` mesh; §14 Q30, no §13.2 row |
| **58** | **Verify whether UE Starter Content still ships in 5.8.** MEDIUM-confidence community reporting says it was removed in 5.7; `design-brief.md` §12.1 and §12.6 both lean on it. **Near-fit KIND A** — determinate, but it is a five-minute editor check rather than an Unreal build procedure. | **A** | **M1-23** | `design-brief.md` §12.1 / §12.6; no §13 row |
| **71** | **`build-sequence.md` files the Q30 Paragon swap under M5-06; group 08 correctly places it at M1-23.** A step filed under M5 that must execute before M4 is self-contradictory as written. | **A** | **M1-23** | `build-sequence.md` M5-06 → M1-23 |

### M2-04 — Create `DT_VanguardAttacks` with all four rows

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **65** | **Telegraph and Recover are specified two incompatible ways** — absolute seconds (group 07) versus `ANS_Telegraph` length × `TelegraphScale` (§13.1 rows 20–21, 23–24; `build-sequence.md` M4-04). The four P2/P1 ratios are **0.786 / 0.800 / 0.775 / 0.778 — not uniform**, so a single scale cannot express them. **GB, and it changes the data model:** M2-04 and M4-04 cannot both be built as written. | **B · BLOCKING** | **M2-04** | `S_AttackPhaseTuning.TelegraphScale` / `.RecoverScale` — §13.1 rows 20–21, 23–24 |
| **26** | **"Plasma-gauntlet weapons" may contradict Attack A.** **⛔ BLOCKED ON HUMAN.** Step one is not a design decision — it is confirming the wording on GDD page 14 by eye, because the transcription disclaims its own confidence. Four specific questions are written out in `design/group-07-structure-and-canon.md`. | **B · BLOCKED ON HUMAN** | **M2-04** | GDD page 14; no data home |
| **22** | **Q10 — attack A–D range bands (cm).** §14 names it *"a likely early bug source — worth tuning together with Q24."* | **B** | **M2-04** | `DT_VanguardAttacks` `MinRange`/`MaxRange` — §13.2 row 38 |
| **21** | **Q3 — damage per rival attack A–D.** | **B** | **M2-04** | `DT_VanguardAttacks.Damage` — §13.2 row 31 |
| **23** | **Q12 — per-attack cooldown.** | **B** | **M2-04** | `DT_VanguardAttacks.Cooldown` — §13.2 row 40 |
| **24** | **Q13 — Attack D max travel.** GDD hard rule: *"no hidden full-arena snap."* | **B** | **M2-04** | `DT_VanguardAttacks.MaxTravelDistance` — §13.2 row 41 |
| **25** | **Q25 — per-attack values inside each GDD state range.** 26 values. The range-validation check the developer builds against them is KIND A and can proceed without the values. | **B** | **M2-04** | `DT_VanguardAttacks` + `S_AttackPhaseTuning` — §13.2 row 53 |
| **50** | **Attack B needs a `MaxTravelDistance`; row 41 names only D.** Uncapped, B is a second gap closer, which changes the four-attack spacing shape. | **B** | **M2-04** | `DT_VanguardAttacks.MaxTravelDistance` — **row 41 covers D only** |
| **51** | **`SelectionWeight` has no row and no Q number.** GDD §04 requires Phase 2 to shift weighting toward close-range and gap-closing selection, and there is no field to shift. | **B** | **M2-04** | `S_AttackPhaseTuning.SelectionWeight` — **no §13.2 row** |
| **66** | **Q25's Attack A tension was computed on a distance band group 04 proved unreachable** (0–90 cm, against a 100 cm capsule minimum). Recompute before acting on it. | **B** | **M2-04** | record only; no data home |
| **27** | **Page 14's SYSTEM STATS map to no system.** POWER 9/10, ARMOR 9/10, MOBILITY 6/10, SYSTEMS 7/10. **MOBILITY 6/10 is not a movement-speed value.** Decide they are non-canonical and record it. | **B** | **M2-04** | record only; explicitly **not** a float anywhere |
| **N4** | **The four attack working names are proposed, not canon, and only the user may promote them.** `Fault Line` (A), `Advance Line` (B), `Bulwark Reach` (C), `Thruster Snap` (D) were generated by Assignment #04 and carried into `data/unreal/DT_VanguardAttacks.csv`. Every file labels them pending; **nothing on any list asks the designer to settle them.** Naming is the designer's by the binding rule. Not on any list. | **B** | **M2-04** | `DT_VanguardAttacks.DisplayWorkingName` (CSV) → `S_VanguardAttackDef.DebugName`; **no §13.2 row** |
| **N6** | **The user has not countersigned `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`.** It is signed by Anthony Travieso, 2026-07-29, covering three calls that are the designer of record's under `CLAUDE.md`. Until the user countersigns, the CSV is approved on Anthony's authority for his branch only and **no Unreal import is authorized.** Not on any list. | **B** | **M2-04** | `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`; no §13 row |

### M2-12 — Create the six `BTTask_*` tasks

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **49** | **Crimson Vanguard's `MaxWalkSpeed` has no row and no Q number.** Under the approved Q22 a rival slower than the player **can be kited forever and the duel cannot end.** Bounded by two dispatches to roughly **[600, 1030) uu/s**; assigned by none. **Step-id note: `TODO.md` files this at M1-12, which is the *player's* profile. The rival does not exist until M2-05, and the first step whose logic reads the value is `BTTask_Idle_Reposition` at M2-12. It is nonetheless *scheduled* at M1-12 because it is coupled to Q15 — see §6, group C.** | **B · potentially BLOCKING** | **M2-12** *(TODO: M1-12; scheduled M1-12 by coupling)* | **no §13.2 row.** `BP_CrimsonVanguard` movement component |
| **29** | **Q18 — BTTask montage failsafe margin.** Reopened 2026-08-03. The recommendation's *division by effective play rate is not optional* or it fires early on every Phase 2 telegraph. | **B** | **M2-12** | `DA_TuningGlobals` / each `BTTask_*` — §13.2 row 46 |

### M2-13 — Author Attack A montage and its notify states

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **30** | **Q27 — `ANS_Recover` incoming-damage multiplier.** Designer decides whether "punish opening" means extra damage or only safe access. **It is a direct scalar on the Q2 derivation, so it should be resolved before Q2 is locked.** | **B** | **M2-13** | `ANS_Recover` — §13.2 row 55 |

### M3-03 — Create `BP_AscensionComponent`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **31** | **Q9 — does the Ascension Meter decay?** Constraint **C1** from the approved Q22 requires *no decay*. | **B** | **M3-03** | `BP_AscensionComponent` — §13.2 row 37 |

### M3-04 — Create `WBP_HUD`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **32** | **Q29 — Crimson Vanguard's short in-combat UI label.** The GDD itself lists this as unfinalized. **No short form exists anywhere in the GDD, including page 14.** The developer exposes a `Text` variable and leaves it blank. | **B** | **M3-04** | `WBP_HUD` — §13.2 row 57 |

### M3-07 — Create `BP_ImpactWindowDirector`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **N5** | **`CLAUDE.md` and `design/decisions.md` disagree about whether V1–V5 are accepted.** `decisions.md` records **ALL FIVE APPROVED (KIND A)** by the group 09 dispatch; `CLAUDE.md` says *"M3 sign-off waits on the designer accepting five named corrections (V1–V5) … Those five are still open and are the user's to accept or amend."* `cinematic-integration-inspection.md` §9 item 1 agrees with `CLAUDE.md`. This is the same shape as pass-1 Violations 1 and 2 — an item the human owns closed by a dispatch — and no inspection pass caught it. The corrections also contain judgement calls (V5 deliberately departs from the inspector's literal acceptance wording, correctly, to avoid widening a bug). **Not a claim that V1–V5 are wrong; a claim that their status field may be.** Not on any list. | **B · BLOCKING (for M3 sign-off)** | **M3-07** | `design/decisions.md` group 09 status line; `combat-integration-plan.md` §3.1 rows 19/22/27 |
| **63** | **Apply the five corrections to `combat-integration-plan.md`.** V1–V5 exist as drop-in text; **the `combat-integration-architect` must apply them.** This is what clears hard check 7 and unlocks M3 sign-off. The architect must also choose between `BPI_CombatWindows` and the two-explicit-calls fallback. **M1 and M2 may proceed now regardless.** | **A** | **M3-07** | `combat-integration-plan.md` §3.1 rows 19, 22, 27; §2; §10 |
| **33** | **Q26 — standard Impact Window cooldown.** The first-window exemption is not optional; applying the cooldown to the first window would break the GDD onboarding rule. | **B** | **M3-07** | `BP_ImpactWindowDirector` — §13.2 row 54 |
| **59** | **`CameraReturnBlendSeconds` — no value chosen.** Introduced by V2's camera-restore step. | **B** | **M3-07** | **no §13.2 row.** `RestoreCombatState()` camera step |
| **60** | **`OverlayStopBlendOutSeconds` — no value chosen.** Introduced by V4's targeted `Montage Stop`. | **B** | **M3-07** | **no §13.2 row.** `RestoreCombatState()` montage-cleanup step |
| **61** | **Should a same-frame death that races an earned `IA_Impact` press still show the burst before the Loss screen?** **GB** — a terminal branch. V4 part 4, deliberately left open. | **B** | **M3-07** | **no §13.2 row.** `BP_DuelDirector.bDuelOver` |
| **N7** | **The Impact burst montage pair has no names.** `cinematic-integration-inspection.md` §9 item 11, `OPEN — designer decides`; the plan's proposed names are cosmetic and left OPEN. Naming is the designer's. Cosmetic, but it is a real blank at M3-07. Not on any list. | **B** | **M3-07** | `BP_ImpactWindowDirector` SUCCESS branch montage refs; no §13 row |

### M3-08 — Write `RestoreCombatState()` once

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **68** | **`build-sequence.md` M3-08 still carries the two defects V2 and V5 correct**, and `build-sequence.md` is **not on item 63's apply list.** Whoever applies V1–V5 must update the build sequence too, or the developer builds the old spec. | **A** | **M3-08** | `build-sequence.md` M3-08 |
| **62** | **Is `design-brief.md` §7.5 amended in place, or annotated as superseded?** V2's omission exists upstream in the brief's pseudocode. The inspector required it be **surfaced, not silently edited**, so the process question is the user's. | **A** *(process; near fit)* | **M3-08** | `design-brief.md` §7.5 |

### M4-05 — Create `BP_FinalClashDirector` and the double gate

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **56** | **What happens if `IA_FinalClash` is pressed while an Impact Window prompt is open.** Both can be live at once after a counter. **GB** — a branch. Proposed rule surfaced, not decided. | **B** | **M4-05** | **no §13.2 row.** `BP_FinalClashDirector` initiation |
| **39** | **Q19 — post-counter Clash-initiation window.** | **B** | **M4-05** | `BP_FinalClashDirector` — §13.2 row 47 |
| **72** | **Q20's tuning band and Q19's ceiling both need a recompute.** Q20's 0.45–0.60 s band exceeds the 0.35–0.50 s range its own justification rests on; Q19's 1.30 s ceiling was computed from GDD Phase 2 *floors* and the real floor under Q25 is 1.77 s. Record-only. | **B** | **M4-05** | rows 47–48; recompute, no new home |

### M4-06 — The two timing beats + `LS_FinalClash`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **40** | **Q20 — Clash beat 1 and beat 2 response times.** | **B** | **M4-06** | `BP_FinalClashDirector` — §13.2 row 48 |
| **54** | **`AM_Clash_Beat1` / `AM_Clash_Beat2` montage lengths and prompt lead-in.** A 0.50 s window with no wind-up is a different mechanic from one with a wind-up. | **B** | **M4-06** | **no §13.2 row.** The two Clash beat montages |
| **70** | **`build-sequence.md` M4-06 names no `AM_Clash_Beat2`.** Two beats, one beat montage. | **A** | **M4-06** | `build-sequence.md` M4-06 |
| **N8** | **Acceptance of a cut-less Phase 1 Final Clash camera if the Level Sequence handoff proves fragile.** `cinematic-integration-inspection.md` §9 item 6, `OPEN — designer decides`; named as the fallback for the hardest camera transition. Contingency. Not on any list. | **B** | **M4-06** | `LS_FinalClash`; no §13 row |

### M4-08 — Clash FAILURE → the seven-step recovery

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **41** | **Q21 — failed-Clash separation distance.** Must place both fighters outside every attack's band. **Cannot be validated until item 49 exists.** | **B** | **M4-08** | `BP_FinalClashDirector` — §13.2 row 49 |
| **57** | **The wall margin for the Q21 clamp.** How close to the arena edge a fighter may be placed. Engineering-adjacent, but it changes effective separation near the ends of the long axis. | **A** | **M4-08** | **no §13.2 row.** `BP_FinalClashDirector` clamp |
| **69** | **`build-sequence.md` M4-08 step 2 pushes the fighters "along their axis"; Q21 mandates the arena long axis.** One of the two is wrong. | **A** | **M4-08** | `build-sequence.md` M4-08 step 2 |

### M5-04 — Fill `RequestSound`

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **73** | **Group 08's Q31 states two different milestone placements for the cue floor** — *"M1–M4 for the floor (asset selection), M5 for everything else"* (its lines 194–195) versus *"authored after M4's gate is met"* (its lines 302–305). **Both are legal**; the question is which side of the asset-selection / authoring line the cues fall on, and that decides whether they ship on 1 September. **See N9 — the `TODO.md` entry for this item currently states the conflict against a false premise.** | **B** | **M5-04** | `design/group-08-assets.md` Q31; `BP_PresentationSubsystem.RequestSound` |
| **42** | **Q31 — is a silent Phase 1 build acceptable?** Shipping silent and doing all audio in Phase 2 is the schedule-safe answer, **but the designer should say so explicitly rather than discover it on 31 August.** | **B** | **M5-04** | `BP_PresentationSubsystem.RequestSound`; §14 Q31, no §13.2 row |

### M5-06 — Final character treatment

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **43** | **Is Echo's faceplate a visor or a light?** Page 12's own callout reads **"Visor or Light"** and does not choose — **AMBIGUOUS, and therefore off limits to every agent.** Nova's sheet separately labels a "Light", so the two fighters may not be consistent. | **B** | **M5-06** | `M_Fighter` / helmet material; **no §13.2 row** |
| **44** | **Are the "Integrated Energy Lines" emissive at runtime, and do they respond to the meter?** Drawn flat on page 12 with no glow. **AMBIGUOUS.** | **B** | **M5-06** | shared master material; **no §13.2 row** |

### M5-08 — The editorial character-selection interface

| Item | Description | Kind | Step | Where the value lives |
|---|---|---|---|---|
| **45** | **What does "SFN" stand for?** Page 13's *"Unique 'SFN' Unit Insignia"*, the only readable lettering on either sheet. **AMBIGUOUS and never expanded in the GDD** — and page 13 carries two confirmed printed typos, so a human should confirm the letters against the PDF before anyone builds fiction on them. | **B** | **M5-08** | `WBP_CharacterSelect.FighterUnitLine`, shipped blank; **no §13.2 row** |

### Blocks no build step — these go last, by the rule

| Item | Description | Kind | Step | Where it lives |
|---|---|---|---|---|
| **74** | **The root `README.md` diagram does not show the `goal-planner`.** A knowingly-accepted HARD RULE debt: `CLAUDE.md` was updated, `README.md` was not. Until they match, the HARD RULE's literal remedy is to treat every gate as closed and dispatch nobody. **Five-minute mirror of two blocks.** | **A** | **none** | `README.md` |
| **N9** | **`TODO.md` item 73 is misfiled at M1-05 and states its premise incorrectly.** Pass-3 findings **P1** and **P2**: it sits under the M1-05 heading (filed by proximity to item 64) when Q31 is M5-04, and it calls an after-M4 audio floor *"M5 work"* when `CLAUDE.md` explicitly permits a thin presentation floor after M4 inside Phase 1. **It never quotes the `M1–M4 for the floor` half, which is the half that creates the conflict.** A designer reading item 73 alone would decide the wrong question. Not on any list. | **A** | **none** *(gates item 73's answerability at M5-04)* | `TODO.md` item 73 |
| **N10** | **The Q18 and Q17 reopenings are un-bannered in the group files.** Pass-3 **P3**: `design/group-07-structure-and-canon.md` lines 13 and 425 still read `APPROVED` for Q18 with no banner; `group-06` presumably carries the same shape for Q17 (not read by pass 3, not asserted). The correction pass established a banner convention on `group-01` and applied it once, which makes the un-bannered files *look* current. Not on any list. | **A** | **none** | `design/group-07-…md`, `design/group-06-…md` |
| **N11** | **`TODO.md`'s two descriptions of items 46–73 disagree.** Pass-3 **P4**: line 11 correctly says items 64–72 are contradictions; lines 89–92 still say items 46–73 are *"values the build needs that §13.2 has no row for at all."* Items 64–74 are corrections and record defects, not missing values. Cosmetic, in the section a future agent reads first. Not on any list. | **A** | **none** | `TODO.md` lines 89–92 |
| **N12** | **`cinematic-integration-inspection.md` §8 correction 6 has never been logged.** *"`framework-evaluation.md` §6 ledger row E12 — the Behavior-Tree-in-5.8 claim is internally cited rather than independently sourced. Acceptance: either an independent primary source is added, or the row is annotated as inherited-internal."* Corrections 1–5 became `TODO.md` items 34–38; **correction 6 became nothing.** Explicitly non-blocking, and the recommendation does not hinge on it — but it is a required correction that is not on any list. | **A** | **none** | `framework-evaluation.md` §6 ledger row E12 |
| **N13** | **`design/group-01-blocking-q22.md`'s manifest divergence is unexplained.** 378 lines at pass 1, 385 at pass 2, 390 at pass 3, with pass 3 recording a **+5 delta against a 6-line insertion** it could not reconcile without hashing. Content was verified clean line by line — **no number changed, no scope claim changed.** Named because the manifest is the only change-detection mechanism this pipeline has, and it is the file holding the only decision carrying the designer's actual approval. Not on any list. | **A** | **none** | `design/group-01-blocking-q22.md`; the manifest convention |

### Standing gates, not items

Two things are **permanent gates** rather than work items, and are recorded here so nobody
files them as tasks and then "closes" them:

- **Rights/licensing acceptance for every free asset, at claim time** —
  `cinematic-integration-inspection.md` §9 item 4 and GDD §06's HUMAN APPROVAL GATE. Item 20
  closed the *swoosh* question specifically; the per-asset gate itself never closes.
- **No agent resolves a provisional value** — `CLAUDE.md` HARD CONSTRAINT, GDD §05
  safeguard 5, GDD §06 (*"Designer approves all rules and numbers"*).
