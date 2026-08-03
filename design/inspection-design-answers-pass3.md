# Inspection pass 3 — narrow verification of the N2–N7 + contradiction-C corrections

**Inspector dispatch, 2026-08-03.** This is a **bounded verification pass**, not a re-audit.
It checks the eight claims named in the dispatch against the files, then runs the bounded
re-check the dispatch specified. Pass 1 (`design/inspection-design-answers.md`) found 3
process-authority violations and 11 contradictions; pass 2
(`design/inspection-design-answers-pass2.md`) confirmed 6 of 7 corrections and raised N1–N7
plus the un-landed contradiction **C**.

**Files written by this run: this one only.** `inspection.md`,
`design/inspection-design-answers.md`, `design/inspection-design-answers-pass2.md` and
`leave-offs/inspector.md` are **untouched**. **Standing rule: I report, I do not repair.**
Nothing below was fixed.

**A value left OPEN or blank is a PASS, not a gap.** The question this pass asks is whether the
**record is now accurate** and the **authority correct**.

---

## 1 — Inspected-inputs manifest

Only the files the dispatch named were read. Everything else in the repository was **not read
this pass** and is listed at the end of this section so the omission is visible rather than
implied.

| # | Path | Lines | Final non-empty line (exact) | vs pass 2 |
|---|---|---|---|---|
| 1 | `design/inspection-design-answers-pass2.md` | 340 | `approve, change, or reject.*` | new to this manifest (pass-2 output) |
| 2 | `TODO.md` | **557** | `line — the GDD had the value all along. **Do not add the GDD-out-of-date item for it.**` | **CHANGED** — was 551 (+6: item 73, the renamed M1-05 heading, the header recount) |
| 3 | `design/decisions.md` | **566** | ` ``` ` | **line count UNCHANGED**; three inline edits at lines 190, 219, 254, 493. The count holding at 566 is itself evidence the edits were surgical rather than rewrites |
| 4 | `design/group-01-blocking-q22.md` | **390** | `No other Q number is answered. **Q22 remains PROPOSED until the human designer decides it.**` | **CHANGED** — pass 2 recorded 385. Delta **+5**. See claim 7 |
| 5 | `design/group-02-combat-economy.md` | 681 | `\| **This is Ascendant Impact** \| Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, the Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears \|` | unchanged |
| 6 | `design/group-05-fighter-feel.md` | 1086 | `---` | unchanged (tail + item-45 section only) |
| 7 | `design/group-07-structure-and-canon.md` | 1162 | `Nothing in this file supersedes a GDD line, and no GDD number or range was altered.*` | **line count UNCHANGED**; two inline edits at lines 603 and 711 |
| 8 | `design/group-08-assets.md` | 492 | `\| **This is Ascendant Impact** \| Echo, Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears \|` | unchanged |
| 9 | `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` | 52 | `Attack set Four authored attacks Same four authored attacks` | unchanged |
| — | `build-sequence.md` | **not read this pass** | — | see §2 |

**Read in full:** items 1, 2, 3, 4, 7, 8, 9. **Read as targeted sections:** item 5 (lines
140–214 for Q2 and its derivation; 585–681 for the C3 cross-check, the summary table and the
constraint-compliance block), item 6 (lines 860–1086, the item-45 answer and the tail).

**NOT read this pass, and therefore not certified unchanged by me:** `inspection.md`,
`design/inspection-design-answers.md`, `design-brief.md`, `project-brief.md`,
`build-sequence.md`, `combat-integration-plan.md`, `cinematic-integration-inspection.md`,
`design/group-03`, `group-04`, `group-06`, `group-09`, `gdd/INDEX.md`, the rest of `gdd/`.
Where a check below depends on one of those, it is explicitly **carried forward from pass 2**
and named as such.

---

## 2 — Coverage statement

**The build-step tracing job did NOT run this pass, and `build-sequence.md` was not read.**
This was a narrow verification dispatch that named its inputs; the build sequence was not
among them and no build step was written or edited. Per the coverage rule I carry forward the
position recorded in **`design/inspection-design-answers-pass2.md` §2**, which itself carried
forward **`design/inspection-design-answers.md` §2**. **I cannot certify `build-sequence.md`
as unchanged this pass** — I did not open it. If it has moved since pass 2, the next
inspection must re-run tracing in full.

---

## 3 — Verification table — the eight claims

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| **1** | **Contradiction C — `Q45` → `item 45`** in `decisions.md` **and** `group-07` | **LANDED** at all three known sites | `design/decisions.md` **line 219** now reads *"Keeps **item 45's** build behaviour but breaks its silence…"* — the `Q45` string is gone. `design/group-07-structure-and-canon.md` **line 603** now reads *"### How this relates to the **item 45** precedent, and why it differs"*, and **line 711** reads *"\| **Item 45 (group 05)** \|"*. All three sites pass 1 and pass 2 named are repaired. **Scope caveat, stated rather than glossed:** I have no `Grep` and no shell, so I cannot run a repository-wide string search. "Zero occurrences anywhere in `design/`" is verified only across the files I read — which include **all three known sites**, plus `group-08` in full and `group-05`'s item-45 section (lines 860–889, where the string would most plausibly have propagated; it does not appear). `group-03`, `group-04`, `group-06`, `group-09` and pass 1's own report were not searched |
| **2** | **N2 — `group-01` carries an APPROVED status banner** | **LANDED** | `design/group-01-blocking-q22.md` **lines 3–7**, immediately under the title, before any other text: *"**STATUS UPDATE — 2026-08-02: this proposal was APPROVED by the designer of record.** The closing line of this file still reads "Q22 remains PROPOSED", which was true when it was written. It is no longer. Q22 is **SETTLED AND BINDING** — see `design/decisions.md` and the banner in `TODO.md`. This file is preserved as the reasoning behind the decision, not as its current status."* It names the stale line explicitly, so line 390 can no longer be read as current. Placed where a future agent reads first |
| **3** | **N3 — `Resolves:` lines no longer claim items 6 and 29** | **LANDED** | `decisions.md` **line 190** (group 07): *"**Resolves:** TODO items 25 (Q25), 5 (Q23), 32 (Q29), 27, 28. **Item 29 (Q18) was reopened 2026-08-03 and is NOT resolved.**"* — `29 (Q18)` removed from the list and the reopening stated. **Line 254** (group 06): *"**Resolves:** TODO items 31 (Q9), 39 (Q19), 40 (Q20), 41 (Q21). **Item 6 (Q17) was reopened 2026-08-03 and is NOT resolved.**"* — `6 (Q17)` removed likewise. Both now satisfy rule 3's own definition (the field traces a *deletion* from `TODO.md`), and both agree with `TODO.md` items 6 and 29, which are present and tagged `⏳ PROPOSED — reopened 2026-08-03` |
| **4** | **N4 — item 64 moved from M2-04 to M1-05** | **LANDED** | `TODO.md` **line 120** heading: *"### M1-05 — the one most likely to break a build"*, with item 64 at **lines 122–127**. It now sits directly beneath the M1-05 block that holds item 2 (Q1) and item 3 (Q2) — which is where `VanguardMaxHealth` actually lives (`design-brief.md` §13.2 row 30 / `DA_TuningGlobals`). Items 65 and 66, which genuinely are M2-04, remain under the separate *"### M2-04 — the one most likely to break a build"* heading at **line 495**. A top-down worker now meets the C3 question at the same step as Q2 rather than a milestone late |
| **5** | **N5 — dangling group-02 fragment repaired** | **LANDED** | `decisions.md` **line 493** now reads: *"**C3 IS NOT SATISFIED — see the 2026-08-03 correction note.** Group 02's own text **reads:** meter 100 arrives ~0:40–1:25 while the health gate arrives ~2:53, so they do *not* converge."* The `Group 02 wrote: —` splice is gone; the sentence has its subject and parses. The following two sentences (meter-first ordering, the dangerous state not occurring) are unchanged, so the correction added no new claim while fixing the grammar |
| **6** | **N7 — group 08's Q31 milestone contradiction logged as item 73** | **LANDED** (logged), **with a wording defect named below** | `TODO.md` **lines 129–132**: *"**73. Group 08's Q31 contradicts itself on milestone placement.** · **KIND B** — Raised in the pass-1 inspection and not logged at the time. Q31 says Phase 1 ships without an audio pass, then specifies a 6–9 cue floor *sequenced after M4's gate* — which is M5 work described as a Phase 1 deliverable. Decide which it is."* The finding is on the record and asks the designer to choose, which is the correct disposition. **Two problems with how it is written — see P1 and P2 in §4** |
| **7** | **N1 — `group-01` line count re-recorded; only the banner changed** | **LANDED** | **New count: 390 lines**, final non-empty line at 390. Verified against pass 2's own quotes, cell by cell: the **(b2)** recommendation is intact (lines 264–266, *"`MinHealthFloor = 1` … lowered to `0` only by `ClashSuccess()`"*); **C1 / C2 / C3** are worded exactly as `TODO.md`'s banner and `decisions.md` quote them (lines 291–303, C3 verbatim *"Q2 (rival max health) should be tuned so ≤ 25 % and meter 100 arrive close together"*); the **Constraint check** block (lines 385–390) still reads 0–100, +5/+12/+15/+20/+0, Phase 2 at 50 %, gate at meter 100 AND ≤ 25 %, failed Clash 1 HP / 50 / 3 s, *"No fifth attack … no second arena"*, *"deterministic authored Behavior Tree"*. **No number changed. No scope claim changed. Only the banner was added.** Bookkeeping residual P5: the delta is **+5** where a 5-line banner plus its blank separator implies +6. Most likely pass 2 counted a trailing blank line that is now absent. I cannot hash files, so I record the discrepancy rather than explain it away — the *content* is verified clean line by line |
| **8** | **`TODO.md` header figures are internally consistent** | **LANDED** | Header (line 3): *"**65 open items** — **8 closed · 35 PROPOSED · 1 blocked on you · 29 untouched.**"* Counted by hand from the body: **65 numbered items present** (ids 1, 2, 3, 5–19, 21–27, 29–33, 39–42, 43–73 as present below). **35 + 1 + 29 = 65** ✓. The PROPOSED index (lines 30–37) totals **35** (5+6+6+6+4+4+2, plus the reopened `6, 29`) ✓. Blocked = item **26** = 1 ✓. Untouched = item 1 plus 46–73 = 1 + 28 = **29** ✓. Closed = the eight ids absent from the body: **4, 20, 28, 34, 35, 36, 37, 38** = 8 ✓. *"Twenty-eight new items (46–73)"* (line 11) = 73 − 46 + 1 = **28** ✓, and all 28 ids are present. **The addition of item 73 did not corrupt the count** |

> **8 of 8 claims LANDED.** Every one was checked against the file, not taken on trust.

---

## 4 — VIOLATIONS

### Remaining from passes 1 and 2 — **none.**

All three pass-1 violations were **process-authority** violations, and the record now states
each correctly: **Q17** and **Q18** are PROPOSED and on the designer's list with their values
and warnings intact; **C3** is recorded as NOT satisfied, with the substitution named as the
violation and both remedies on the record as item 64. All three are **OPEN**, which is a
**PASS**. The one un-landed pass-2 item, contradiction **C**, is now landed at every site
pass 2 named.

### New violations — **none.**

The corrections add no game feature, no fifth attack, no second arena, no second rival move
set, no per-fighter mechanical difference, no runtime model call, no auto-success path and no
M5 work inside M1–M4. No number moved. No GDD line and no published range is touched.

### Findings that are not violations — but two of them are record defects this pass found

**P1 — LOW, newly introduced. Item 73 is filed under the wrong step, in the opposite
direction from N4.** It sits under *"### M1-05 — the one most likely to break a build"*
(`TODO.md` line 120), alongside item 64. Item 73 is about **Q31**, whose own entry is item 42
under **M5-04** (line 462), and the audio floor it concerns is sequenced *after M4's gate*.
Nothing at M1-05 consumes it. `TODO.md`'s ranking rule is *"Every item names the lowest-numbered
`build-sequence.md` step that first needs it"* — item 73 now surfaces roughly four milestones
early. Fixing N4 was correct; item 73 appears to have been filed by proximity to it.

**P2 — LOW, newly introduced, and the one thing this pass found materially wrong. Item 73
states the contradiction against a premise that is itself incorrect.** Item 73 says the 6–9
cue floor *"sequenced after M4's gate"* is **"M5 work described as a Phase 1 deliverable."**
That is not what pass 1 found and it is not what `CLAUDE.md` says. `CLAUDE.md` explicitly
permits *"a thin presentation floor"* after M4 inside **Phase 1**, so *"after M4's gate"* is
**legal Phase 1 sequencing**, not M5 work — and pass 2 said so in N7 (*"only the second
surviving `CLAUDE.md`'s 'thin presentation floor after M4' allowance"*). The actual
contradiction is between two **placement statements inside group 08**, and item 73 quotes only
one of them:

- `design/group-08-assets.md` **lines 194–195**, Q31's "Where this lands": *"**Milestone:
  M1–M4 for the floor (asset selection), M5 for everything else.**"*
- `design/group-08-assets.md` **lines 302–305**, Q31's sequencing paragraph: *"the floor is
  authored **after M4's gate is met**, not before … it is the *last* thing in Phase 1."*

Both are still live in group 08, which is correct for a dated dispatch artifact under the
record-only convention. But **item 73 does not name the `M1–M4 for the floor` half**, which is
the half that creates the conflict, and it mislabels the other half as an M5 breach. A designer
reading item 73 alone would be deciding the wrong question against a false premise. **This is a
record-precision defect, not a violation** — it breaks no GDD line, no range, no scope lock and
no authority, and it does still route the question to the designer.

**P3 — LOW. The N2 remedy was applied to one dispatch file only, and the same staleness
survives elsewhere without a banner.** `group-01` now carries a banner. But
`design/group-07-structure-and-canon.md` **line 13** (status table) and **line 425** (the Q18
section header block) both still read **`APPROVED`** for Q18, with no banner anywhere in that
file pointing at the 2026-08-03 reopening. `design/group-06-final-clash.md` presumably carries
the same shape for Q17 — **not read this pass, so not asserted.** This is the same category as
N6 (a dated dispatch artifact versus the governing record) and the same disposition applies:
`decisions.md` governs, so it is staleness rather than a contradiction of authority. Named
because the correction pass established a banner convention and then applied it once, which
makes the remaining un-bannered files *look* current by comparison.

**P4 — LOW. `TODO.md`'s two descriptions of items 46–73 now disagree slightly.** Line 11
correctly says *"Items 64–72 are the contradictions"*; lines 89–92 still say *"**Items 46–73
are** values the build needs that §13.2 has **no row for at all**."* Items 64–73 are
corrections and reconciliations, not missing values. Cosmetic, in the section a future agent
reads first.

**P5 — LOW, bookkeeping only.** The `group-01` line-count delta is +5 against a 6-line
insertion (claim 7). Content verified clean; the arithmetic is unresolvable without hashing.

**Carried forward from pass 2, unchanged and correctly so:**

- **N6.** `design/group-02-combat-economy.md` **line 602** still reads *"**C3 is satisfied**,
  with two residual exposures named."* Re-read this pass and confirmed still present. This is
  the expected consequence of correcting the *record* and not the *artifact*; `decisions.md`
  line 493 governs it. Still a known disagreement rather than a discovered one.
- **Group 08's Q31 internal conflict** is still live in group 08 (P2), by the same convention.

---

## 5 — Bounded re-check

### Q25 — 26 / 26 still in range

Re-verified, not carried forward. `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` was
re-read in full (52 lines, unchanged) and the published ranges transcribed from it verbatim:
Idle/Reposition **0.60–1.20 / 0.35–0.80** · Select Attack **0.10–0.20 / 0.10–0.20** ·
Telegraph **0.55–0.95 / 0.40–0.75** · Active Attack **0.18–0.45 / 0.18–0.45** · Recover
**0.45–0.90 / 0.35–0.75** · Return to Neutral **0.10–0.20 / 0.10–0.20**; Phase 2 at **50 %
health**, *"same four authored attacks—no transformation rig and no second move set."*
**Identical to what passes 1 and 2 recorded. No range altered, widened, narrowed or
collapsed.** Values re-read from `group-07` §Q25.1–Q25.3 and its range-compliance tables
(lines 1027–1096), cross-checked against `decisions.md` lines 193–197.

| Field | Values | GDD range | Verdict |
|---|---|---|---|
| Telegraph P1 A/B/C/D | 0.70 / 0.60 / 0.80 / 0.90 | 0.55–0.95 | **4/4 IN** |
| Telegraph P2 A/B/C/D | 0.55 / 0.48 / 0.62 / 0.70 | 0.40–0.75 | **4/4 IN** |
| Active, one value both phases, A/B/C/D | 0.22 / 0.36 / 0.30 / **0.45** | 0.18–0.45, not phase-scaled | **4/4 IN**; D on the inclusive upper bound, zero upward headroom |
| Recover P1 A/B/C/D | 0.85 / 0.70 / 0.60 / 0.55 | 0.45–0.90 | **4/4 IN** |
| Recover P2 A/B/C/D | 0.68 / 0.56 / 0.48 / 0.44 | 0.35–0.75 | **4/4 IN** |
| Reposition P1 / P2 | 0.90 / 0.55 | 0.60–1.20 / 0.35–0.80 | **2/2 IN** |
| Select P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |
| Return to Neutral P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |

> **26 / 26 IN RANGE. 0 out of range. 0 ranges collapsed.** Attack D's Active remains legal
> only under `Min <= Value <= Max`, which `group-07` §Q25.9 step 2 still specifies. It is still
> the most fragile cell in the set. The three duel-level states still carry one value per
> phase rather than four per attack — the shape the GDD itself uses. **Not a collapse.**

### No number changed to make a problem disappear

| Value | Required | Found this pass |
|---|---|---|
| **Q2** | **1200** | `group-02` line 156 (**1200**, band 1100–1400), line 199 (tuning identity *"1200 → ~2:53"*), line 632 (summary table); `decisions.md` lines 477 and 488; `group-07` line 397; `TODO.md` item 3 still carries only the §14 band **800–2000** with **no value chosen**. `group-02` remains **681 lines with an identical final line** — the file was not edited. **CONFIRMED 1200** |
| **Q1** | **100** | `decisions.md` line 476; `group-02` line 631; `group-07` line 45. **CONFIRMED** |
| **Q7** | **0.12 s** | `decisions.md` line 411 (`[0.03, 0.15]`, front 43 % of the i-frame window); `group-07` lines 43 and 392. **CONFIRMED** |
| **Q24** | **2400 × 1600 cm** | `decisions.md` line 367; `group-08` ledger row 9 (line 454). **CONFIRMED** |
| **Q21** | **1200 cm** | `decisions.md` line 263 (band 1100–1300, along the arena long axis). **CONFIRMED** |
| Item 28 | 208 cm | `group-07` lines 967–985 and `decisions.md` line 221, arithmetic unchanged (82 × 2.54 = 208.28). **CONFIRMED** |

**Nothing was resolved on an agent's authority this pass.** Item 64 still offers Q2 → 1050–1100
as *one of two designer paths* without adopting it; C3's status is still **OPEN and the
designer's call**.

### The four hard checks

- **SCOPE LOCK — HOLDS.** GDD §04's *"Same four authored attacks—no transformation rig and no
  second move set"* re-read verbatim (line 43–44, 51). `group-07`'s constraint block (lines
  50–52) and `group-08`'s (line 486) both still state one arena, one rival, four attacks, two
  avatars on one framework; `group-02`'s (line 675) states one shared health value and combo.
  `group-07` line 806 still refuses the ranged reading of item 26 — *"A ranged option would be
  a fifth attack and is forbidden by SCOPE LOCK regardless of what the panel says."* Items 64
  and 73 add no feature.
- **No runtime AI-model calls — HOLDS.** GDD §04 lines 12–14 re-read: *"The packaged duel makes
  no runtime LLM calls, does not learn from the player, and does not generate attacks or
  choreography dynamically."* `group-01` line 389, `group-07` lines 53–54, `group-02` line 676
  and `group-08` line 487 all still state it. `group-08` additionally records two *licence*
  constraints that bind Assignment #04's offline tooling only (Sonniss AI/ML prohibition; the
  brand-mark description must not enter a generated art brief) — correctly scoped outside the
  game.
- **No auto-success — HOLDS on the files read.** `group-01` lines 219–229 still require every
  meter gain to be earned and still state the loss condition stays live. **Carried forward from
  pass 2 for `build-sequence.md` M3-07 / M3-GATE and `design-brief.md`, which I did not read
  this pass.**
- **Milestone order — HOLDS.** `group-08` line 488 still places every tuned thing in M5 and
  keeps Q30 as asset selection; `group-05` lines 879–887 and 1049 still place items 43/44/45 in
  M5-06/M5-08 with *"Note to M1: none"*; `group-07` line 714 still splits Q29's string (M3) from
  its typography (M5). No step was added, moved or reordered. **The one borderline placement is
  Q31, and it is now logged — imperfectly (P2).**

### Still-open items are still open

| Item | Required state | Found |
|---|---|---|
| **64** (C3) | open, designer's call | `TODO.md` lines 122–127, **YOUR CALL**, two paths, neither taken; `decisions.md` line 84 *"Status: OPEN, and the designer's call."* **OPEN** |
| **65** (Telegraph representation) | open | `TODO.md` lines 497–504, still *"Blocks M2-04 and M4-04 from both being built as written"*, ratios 0.786 / 0.800 / 0.775 / 0.778 intact. **OPEN** |
| **6** (Q17) | reopened, PROPOSED | `TODO.md` lines 142–148, `⏳ PROPOSED — reopened 2026-08-03`, *genuinely blocked* note retained. **OPEN** |
| **29** (Q18) | reopened, PROPOSED | `TODO.md` lines 342–348, `⏳ PROPOSED — reopened 2026-08-03`, `MontageLength / EffectivePlayRate + 0.35` and the divide-by-effective-play-rate warning both intact. **OPEN** |
| **26** | blocked on the human | `TODO.md` lines 320–331, `⛔ BLOCKED ON YOU`; `group-07` line 720 *"BLOCKED ON HUMAN CONFIRMATION — deliberately not resolved here"*, four questions intact. **OPEN** |

Nothing was quietly closed. No PROPOSED item became APPROVED. The closed set is still the same
eight ids (4, 20, 28, 34, 35, 36, 37, 38).

---

## 6 — Per-step verdict

**Omitted.** §2 records that the build-step tracing job did not run and that
`build-sequence.md` was not read.

---

## 7 — Overall verdict

> **CLEAN on the record and the authority — all eight claims landed, and one new record defect
> is named.** Every one of the eight corrections is on disk and was verified against the file:
> `Q45` is gone from all three sites pass 2 named, `group-01` carries an APPROVED banner ahead
> of its stale closing line, `decisions.md`'s `Resolves:` fields no longer claim items 6 and 29,
> item 64 is filed at M1-05 where Q2 lives, the group-02 fragment parses, group 08's Q31
> conflict is logged as item 73, `group-01` measures 390 lines with **no number and no scope
> claim changed**, and `TODO.md`'s header arithmetic reconciles exactly (35 + 1 + 29 = 65, eight
> closed ids absent, 46–73 = 28). **No violation remains and no new violation was introduced.
> No number moved — Q2 is still 1200 in all six places it appears, Q1 100, Q7 0.12 s, Q24
> 2400 × 1600, Q21 1200 cm — and Q25 re-checks 26 / 26 IN RANGE against a freshly re-read GDD
> §04.** SCOPE LOCK, the no-runtime-AI rule, no-auto-success and M1→M5 order all hold. **What is
> not clean is item 73's wording (P2):** it states the Q31 contradiction against a false premise
> — calling an after-M4 audio floor *"M5 work"* when `CLAUDE.md` explicitly permits a thin
> presentation floor after M4 inside Phase 1 — and it never quotes the `M1–M4 for the floor`
> half that is the actual conflict, so a designer reading it alone would decide the wrong
> question. That plus item 73's misfiling under M1-05 (P1), the un-bannered Q18 staleness in
> `group-07` (P3), and two cosmetic bookkeeping residuals (P4, P5) are the whole remaining list.
> **Two scoping limits on this verdict, stated so nobody over-reads it:** I have no search tool,
> so "zero `Q45` anywhere in `design/`" is verified only across the files I read; and
> `build-sequence.md` was not opened, so pass 2's tracing and no-auto-success positions are
> carried forward, not re-established.

*Nothing above was repaired. Every value in this repository remains the human designer's to
approve, change, or reject.*
