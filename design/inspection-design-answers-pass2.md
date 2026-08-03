# Inspection pass 2 — verification of the 2026-08-03 corrections

**Inspector dispatch, 2026-08-03.** This is a **verification pass** over the corrections the
commander applied in response to `design/inspection-design-answers.md` (pass 1, 2026-08-02).
Pass 1 found **3 process-authority violations** and **11 cross-group contradictions**.

**Files written by this run: this one only.** `inspection.md` (Assignment #03),
`design/inspection-design-answers.md` (pass 1), and `leave-offs/inspector.md` are **untouched**.
**Standing rule: I report, I do not repair.** Nothing below was fixed.

**A value left OPEN or blank is a PASS, not a gap.** The question this pass asks is not
whether the questions are answered — it is whether the **record is now accurate** and the
**authority is now correct**.

---

## 1 — Inspected-inputs manifest

Compared cell by cell against the manifest in `design/inspection-design-answers.md` §1.
**"Changed"** means the line count or the final non-empty line differs from pass 1.

| # | Path | Lines | Final non-empty line (exact) | vs pass 1 |
|---|---|---|---|---|
| 1 | `design/inspection-design-answers.md` | 523 | `approve, change, or reject.*` | new to this manifest (pass-1 output) |
| 2 | `design/decisions.md` | 566 | ` ``` ` | **CHANGED** — was 530 lines (+36; the Corrections block, lines 56–89, plus two inline status edits) |
| 3 | `TODO.md` | 551 | `line — the GDD had the value all along. **Do not add the GDD-out-of-date item for it.**` | **CHANGED** — was 450 lines (+101; banner, restored items 6 and 29, numbering bullet, items 64–72, rewritten "Not yet triggered") |
| 4 | `design/group-01-blocking-q22.md` | **385** | `No other Q number is answered. **Q22 remains PROPOSED until the human designer decides it.**` | **CHANGED / UNEXPLAINED** — pass 1 recorded **378** lines, final non-empty `---`. See Finding N1 |
| 5 | `design/group-02-combat-economy.md` | 681 | `\| **This is Ascendant Impact** \| Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, the Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears \|` | unchanged |
| 6 | `design/group-03-defensive-timing.md` | 1243 | `reject.*` | unchanged |
| 7 | `design/group-04-spacing-and-arena.md` | 1067 | `**Everything in this file is the human designer's to approve, change, or reject.**` | unchanged |
| 8 | `design/group-05-fighter-feel.md` | 1086 | `---` | unchanged |
| 9 | `design/group-06-final-clash.md` | 1197 | `record owns all of them.*` | unchanged |
| 10 | `design/group-07-structure-and-canon.md` | 1162 | `Nothing in this file supersedes a GDD line, and no GDD number or range was altered.*` | unchanged |
| 11 | `design/group-08-assets.md` | 492 | `\| **This is Ascendant Impact** \| Echo, Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears \|` | unchanged |
| 12 | `design/group-09-cinematic-corrections.md` | 975 | `repairs every branch at once.*` | unchanged |
| 13 | `design-brief.md` | 1091 | `*End of design brief. Every rule and number in this document remains the human designer's to approve, change, or reject.*` | unchanged |
| 14 | `project-brief.md` | 388 | `LOCK as a wall, and never propose a runtime AI-model call.` | unchanged |
| 15 | `build-sequence.md` | 933 | `or reject; the developer changed none and resolved none.*` | unchanged |
| 16 | `combat-integration-plan.md` | 406 | `*End of combat integration plan. The approved foundation is implemented as specified; every rule and number remains the human designer's to approve, change, or reject.*` | unchanged |
| 17 | `cinematic-integration-inspection.md` | 236 | `*End of cinematic integration inspection. Verdict: APPROVED WITH REQUIRED CHANGES — corrections 1–5 to the human designer before M3; the foundation, the first test, and M1–M2 may proceed.*` | unchanged |
| 18 | `gdd/INDEX.md` | 79 | `` `pdftoppm` is not. Re-run the section split, re-extract the page images, and re-read `` | unchanged |
| 19 | `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` | 52 | `Attack set Four authored attacks Same four authored attacks` | unchanged |

**Read in full this pass:** items 1, 2, 3, 4, 5, 10, 19, 18. **Read as tail plus targeted
sections:** items 6, 7, 8, 9, 11, 12 (constraint-compliance blocks and summary tables), 13
(§12.5–§15, covering all of §13.1, §13.2 and §14), 14, 15 (M3-05 → Appendix C, covering
M3-07, M3-08, M4-01 → M4-10, M5-01 → M5-08 and Appendices A–C), 16, 17.

**Only three files changed since pass 1: `design/decisions.md`, `TODO.md`, and — unexpectedly
— `design/group-01-blocking-q22.md`.** Every other design-answer artifact, the design brief,
the build sequence, the integration plan and the whole of `gdd/` are byte-consistent with the
pass-1 manifest.

---

## 2 — Coverage statement

**The build-step tracing job did NOT run this pass.** `build-sequence.md` exists and is
**unchanged** — 933 lines, identical final line, and its M3-08 / M4-06 / M4-08 / M5-06 bodies
are verbatim what pass 1 quoted. Per the coverage rule I carry forward the pass-1 position:
tracing was skipped there too because no build step was written or edited, and the prior
inspection I rely on is **`design/inspection-design-answers.md`, 2026-08-02, §2**.
`build-sequence.md` was still **read** this pass, because verifying claim 3 ("no number was
changed") and claims 68–71 required confirming its four stale steps are still stale.

---

## 3 — Correction verification table

| # | Claimed fix | Verdict | Evidence checked |
|---|---|---|---|
| **1** | **Violation 1 — Q18 reopened as PROPOSED; `TODO.md` item 29 restored** | **LANDED** | `design/decisions.md` §Corrections 1 (lines 61–66) states the authority was wrong, not the number, and quotes group 07's own *"any value in 0.25–0.50 works"* justification. The group-07 log entry's status line (line 187) and its Q18 table row (line 217) both now read **PROPOSED (reopened 2026-08-03)**. `TODO.md` item 29 is present under **M2-12** (lines 328–334), tagged `⏳ PROPOSED — reopened 2026-08-03`, with the recommendation and the divide-by-effective-play-rate warning preserved. The PROPOSED index (line 37) lists `**6 (Q17), 29 (Q18)** — reopened by the inspection`. `design-brief.md` §13.2 row 46 and §14 Q18 are unchanged and still carry the 0.25–0.50 s band. **The value 0.35 s was not deleted and not changed — only its authority.** Residual: see N3 |
| **2** | **Violation 2 — Q17 reopened as PROPOSED; `TODO.md` item 6 restored** | **LANDED** | `design/decisions.md` §Corrections 2 (lines 68–71) quotes §14's *"Designer confirms."* The group-06 log entry's status line (line 253) and its Q17 table row (line 260) both now read **PROPOSED (reopened 2026-08-03)**. `TODO.md` item 6 is present under **M1-10** (lines 128–134), tagged `⏳ PROPOSED — reopened 2026-08-03`, and correctly retains the *genuinely blocked* note (`IMC_Duel` needs a second binding if the answer is no). §14 Q17's wording is unchanged. Residual: see N3 |
| **3** | **Violation 3 — C3 corrected in the record only; no number changed** | **LANDED — and the "no number changed" part is CONFIRMED by independent search** | `design/decisions.md` §Corrections 3 (lines 73–89): C3 is stated **NOT satisfied**, the 90–135 s separation is stated, **the substitution is named as the violation** (*"a dispatch may not amend an approved constraint's success criterion and then mark itself compliant against the amended one"*), **both paths are recorded** (amend C3 on the record, or take group 06's Q2 → 1050–1100), status is **OPEN and the designer's call**, and it is logged as `TODO.md` item 64. The group-02 log entry (line 493) now opens **"C3 IS NOT SATISFIED — see the 2026-08-03 correction note."** `TODO.md` item 64 (lines 483–488) states it accurately. **Q2 = 1200 verified unchanged in every place it appears:** `design/group-02-combat-economy.md` lines 156 (proposed value + band 1100–1400), 199 (tuning identity), 632 (summary table); `design/decisions.md` line 477; `design/group-07-structure-and-canon.md` line 397; `TODO.md` item 3 still carries only the §14 band **800–2000** with no value chosen. **`design/group-02-combat-economy.md` is byte-identical to pass 1 (681 lines, same final line) — no group file was edited to make the problem disappear.** Residuals: N5, N6 |
| **4** | **Contradiction C — "Q45" renamed to "item 45" in `design/decisions.md`** | **NOT LANDED** | `design/decisions.md` **line 219**, group-07 log entry, Q29 row, verbatim: *"**Recommend `VALOR-7`; ship the field blank.** Keeps **Q45's** build behaviour but breaks its silence…"*. The string `Q45` is still there and still means `TODO.md` **item 45**. There is no `Q45` — `design-brief.md` §14 ends at **Q31** (verified this pass: §14's last entry is Q31, line 1031). The defect pass 1 named is unrepaired and unchanged. (`design/group-07-structure-and-canon.md` line 603, *"How this relates to the Q45 precedent"*, and line 711 also still carry it — that file was outside the claim, but the two now propagate each other) |
| **5** | **Contradiction J — item 58–61 vs §13.2 row 58–61 collision called out in `TODO.md`'s "How this file works"** | **LANDED** | `TODO.md` lines 49–54: *"**⚠ TWO NUMBERING SPACES OVERLAP.**"* It names both spaces, gives the concrete collision (group 05's proposed §13.2 rows 58–61 = faceplate, emissive curve, thresholds, "SFN"; `TODO.md` items 58–61 = Starter Content, two blend values, the death-race question), and issues the rule: *"**Always write 'item N' or '§13.2 row N' — never a bare number.**"* Correctly placed in the section a future agent reads first |
| **6** | **Contradiction K — the "holds no entries" premise rewritten, conclusion preserved** | **LANDED** | `TODO.md` lines 546–550: *"As of 2026-08-03 `design/decisions.md` holds **nine dated entries** plus a corrections note. **None of them supersedes a GDD line** … So rule 4 has still not fired."* The false premise is gone; the load-bearing conclusion (nothing supersedes the GDD; the two supersessions on record are of `design-brief.md`) survives intact, as does the item-28 carve-out. Cross-checked against `design/decisions.md` line 54, which still reads *"Nothing supersedes the GDD yet, so rule 4 has not fired."* — the two documents now agree |
| **7** | **Contradictions A, B, D, E, F, G, H, I logged as `TODO.md` items 64–72** | **LANDED — all eight present and accurately stated; none dropped.** One caveat, N7 | Mapping verified one by one against pass 1 §5. **A → item 65** (absolute seconds vs `TelegraphScale`; correctly reproduces the four non-uniform ratios **0.786 / 0.800 / 0.775 / 0.778** and the "a single scale cannot express them" consequence; correctly marked as blocking M2-04 and M4-04 from both being built as written). **B → item 66** (the 0–90 cm band is unreachable given 40 + 60 = 100 cm minimum separation; instructs recompute before acting). **D + E → item 67** (both stated: group 04's **500 cm/s** player assumption vs group 05's **600 uu/s**, and group 06's use of **600 uu/s as the rival's speed — "the most favourable legal value"**; correctly tied to open item 49 and Q21 as one tuning session). **F → item 68** (M3-08 still carries the defects V2 and V5 correct; `build-sequence.md` not on item 63's apply list). **G → item 69** ("along their axis" vs the arena long axis). **H → item 70** (no `AM_Clash_Beat2`). **I → item 71** (Q30 at M1-23 vs `build-sequence.md` M5-06). **Bonus: item 72** logs the two pass-1 HIGH findings that were not lettered contradictions — Q20's 0.45–**0.60** band overshooting the 0.35–0.50 range its justification rests on, and Q19's 1.30 s ceiling superseded by Q25's real **1.77 s** floor. All four stale build steps re-read this pass and confirmed still stale, so items 68–71 remain true statements |

**Score: 6 of 7 landed. 1 did not land (item 4, the `Q45` rename).**

---

## 4 — VIOLATIONS

### Remaining from pass 1 — **none.**

All three pass-1 violations were **process-authority** violations, and all three are now
correctly recorded:

- **Q18** is PROPOSED and back on the designer's list. The question is open, which is a **PASS**.
- **Q17** is PROPOSED and back on the designer's list. Open, **PASS**.
- **C3** is recorded as NOT satisfied, the substitution is named as the violation, both remedies
  are on the record, and it is item 64. Open, **PASS**.

No agent resolved a value on its own authority in the correction pass. No number moved.

### New violations — **none.**

The corrections add no game feature, no fifth attack, no second arena, no second rival move
set, no per-fighter mechanical difference, no runtime model call, no auto-success path, and no
M5 work inside M1–M4. Nothing in them touches a GDD line or a published range.

### Findings that are not violations, ordered by consequence

**N1 — HIGH. `design/group-01-blocking-q22.md` does not match the pass-1 manifest, and the
correction pass did not disclose an edit to it.**
Pass 1 recorded **378 lines**, final non-empty line `---`. It now measures **385 lines**, final
non-empty line *"No other Q number is answered. **Q22 remains PROPOSED until the human designer
decides it.**"* The 7-line delta corresponds exactly to the **Constraint check** block now at
lines 379–385. Two explanations exist and I cannot distinguish them: the block was appended
after pass 1, or the pass-1 manifest was inaccurate. **Per my own rule, uncertainty resolves
toward doing the work: I re-read the whole file this pass.** Result — **no number is changed**
(the block's own text confirms 0–100, +5/+12/+15/+20/+0, 50 %, 100 AND ≤ 25 %, 1 HP / 50 / 3 s),
**no scope breach**, the (b2) recommendation and constraints **C1 / C2 / C3** are worded exactly
as `TODO.md` and `design/decisions.md` quote them. **The content is clean. The undisclosed
divergence is the finding**, because the manifest is the only change-detection mechanism this
pipeline has, and a group file that moves silently defeats it.

**N2 — MEDIUM. `design/group-01-blocking-q22.md` now ends by asserting that Q22 is still
PROPOSED.** Line 385: *"**Q22 remains PROPOSED until the human designer decides it.**"* Also line
3 (*"Status of every answer below: PROPOSED"*) and line 8. But `design/decisions.md` records
Q22 as **APPROVED — accepted as proposed by the designer of record, 2026-08-02** (line 522), and
`TODO.md`'s banner reads **"SETTLED AND BINDING — Q22 (approved 2026-08-02)"**. The group file is
a dated dispatch artifact and was written before the approval, so this is staleness rather than
contradiction of authority — but it is stale in **the one file that carries the only decision on
this project with the designer's actual approval**, and its last line is the sentence a future
agent will read.

**N3 — LOW. `design/decisions.md`'s `Resolves:` lines still claim items 6 and 29 as resolved.**
Group 07's entry (line 190): *"**Resolves:** TODO items 25 (Q25), **29 (Q18)**, 5 (Q23), 32
(Q29), 27, 28"*. Group 06's entry (line 254): *"**Resolves:** TODO items 31 (Q9), **6 (Q17)**,
39 (Q19), 40 (Q20), 41 (Q21)"*. `design/decisions.md`'s own **rule 3** defines that field as
naming *"the `TODO.md` item number and its Q / V id, **so the deletion from `TODO.md` is
traceable**."* Items 6 and 29 are no longer deleted — they are restored and open. The status
lines and the value tables in both entries were corrected; the `Resolves:` lines were not.

**N4 — LOW. `TODO.md` item 64 is filed under the wrong build step.** It sits under the heading
*"### M2-04 — the one most likely to break a build"*, alongside items 65 and 66 which genuinely
are M2-04. Item 64 is about **Q2, `VanguardMaxHealth`**, which `design-brief.md` §13.2 row 30
places in `DA_TuningGlobals` and `TODO.md` item 3 itself files under **M1-05**. `TODO.md`'s own
ranking rule is *"Every item names the lowest-numbered `build-sequence.md` step that first needs
it. Work top-down and you will never be blocked by something further down this list."* Under the
current filing, a top-down worker meets the C3 question one milestone late.

**N5 — LOW. A dangling fragment in the corrected group-02 entry.** `design/decisions.md`
line 493 now reads: *"**C3 IS NOT SATISFIED — see the 2026-08-03 correction note.** Group 02
wrote: — meter 100 arrives ~0:40–1:25 while the health gate arrives ~2:53…"*. The
`Group 02 wrote: —` splice leaves the sentence without its quoted subject. Cosmetic, but it sits
in the permanent record of the one constraint that failed.

**N6 — LOW, and expected under "record only". The group-02 file itself still asserts the
opposite.** `design/group-02-combat-economy.md` §Cross-check item 5 (lines 589–614) still reads
*"**C3 is satisfied**, with two residual exposures named."* That is the correct consequence of
correcting the record and not the artifact — the dispatch file is a dated research document and
`design/decisions.md` is the record that governs it. Named only so it is a known disagreement
rather than a discovered one: a reader who opens the group file alone gets the superseded
answer, and nothing inside that file points at the correction.

**N7 — LOW. One pass-1 finding was not logged anywhere.** Pass 1's milestone-order table
recorded group 08's **Q31 self-contradiction**: its "Where this lands" line says *"Milestone:
**M1–M4 for the floor** (asset selection), M5 for everything else"* while its sequencing
paragraph says *"the floor is authored **after M4's gate is met**, not before"* — two different
placements for nine authored audio cues, with only the second surviving `CLAUDE.md`'s
"thin presentation floor after M4" allowance. Pass 1 wrote *"The designer must pick one
wording."* It was not one of the lettered contradictions A–K, so claim 7 is not broken by its
absence — but `TODO.md` item 42 (Q31) still carries only the original §14 framing and does not
mention the wording conflict, so the finding is currently held nowhere except pass 1's own
report. Both readings remain milestone-legal under the second wording; the record is silent on
which was chosen.

---

## 5 — Session audit — the four checks re-run

### CHECK 1 — every value inside its published GDD range

**Re-verified, not carried forward.** I re-read `gdd/sections/04-crimson-vanguard-authored-rival-ai.md`
(52 lines, unchanged) and re-read `design/group-07-structure-and-canon.md`'s range-compliance
tables (lines 1035–1097, unchanged) rather than trusting either pass-1 or the group's own
summary.

**The GDD's published ranges, re-read verbatim from PDF p. 5:** Idle/Reposition
**0.60–1.20 / 0.35–0.80** · Select Attack **0.10–0.20 / 0.10–0.20** · Telegraph
**0.55–0.95 / 0.40–0.75** · Active Attack **0.18–0.45 / 0.18–0.45** · Recover
**0.45–0.90 / 0.35–0.75** · Return to Neutral **0.10–0.20 / 0.10–0.20**. Phase 2 at **50 %
health**, *"same four authored attacks — no transformation rig and no second move set."*
**Identical to what pass 1 recorded. No range was edited, widened, narrowed or collapsed.**

| Field | Values | GDD range | Verdict |
|---|---|---|---|
| Telegraph P1 A/B/C/D | 0.70 / 0.60 / 0.80 / 0.90 | 0.55–0.95 | **4/4 IN** |
| Telegraph P2 A/B/C/D | 0.55 / 0.48 / 0.62 / 0.70 | 0.40–0.75 | **4/4 IN** |
| Active (one value, both phases) A/B/C/D | 0.22 / 0.36 / 0.30 / **0.45** | 0.18–0.45, **not phase-scaled** | **4/4 IN**; D on the inclusive upper bound, zero upward headroom |
| Recover P1 A/B/C/D | 0.85 / 0.70 / 0.60 / 0.55 | 0.45–0.90 | **4/4 IN** |
| Recover P2 A/B/C/D | 0.68 / 0.56 / 0.48 / 0.44 | 0.35–0.75 | **4/4 IN** |
| Reposition P1 / P2 | 0.90 / 0.55 | 0.60–1.20 / 0.35–0.80 | **2/2 IN** |
| Select P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |
| Return to Neutral P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |

> **26 / 26 IN RANGE. 0 out of range. Nothing drifted.** Attack D's Active still sits exactly on
> the published maximum and is legal only under `Min <= Value <= Max`, which group 07's Q25.9
> validation spec still specifies. It remains the single most fragile cell in the set.

**Every other range-bounded value, re-read from `design-brief.md` §13.1 (rows 1–28, unchanged):**

| Value | Published | State this pass | Verdict |
|---|---|---|---|
| Meter range | 0–100 | row 5 unchanged | **PASS** |
| Meter gains | +5 / +12 / +15 / +20 / +0 | rows 6–10 unchanged | **PASS** |
| Phase 2 trigger | 50 % | row 16 unchanged; GDD §04 unchanged | **PASS** |
| Clash gate | meter **100 AND** rival health **≤ 25 %** | rows 11–12 unchanged; `build-sequence.md` M4-05 still `(Meter >= 100) AND (Health <= 0.25)` | **PASS** |
| Failed Clash | 1 HP floor / meter to 50 / 3 s | rows 13–15 unchanged; `build-sequence.md` M4-08 steps 4–6 unchanged, still "no restart, no player death" | **PASS** |
| First Impact Window | 0.75 s | row 2 unchanged; `build-sequence.md` M3-07 unchanged | **PASS** |
| Standard Impact Window | 0.35–0.50 s | row 3 unchanged and still published **as a range** | **PASS** |
| Impact burst | 1–3 s | row 4 unchanged; group 09 line 958 still cites it as a range | **PASS** |
| Session length | 3–5 minutes | row 1 unchanged, still *"design target, not a timer"*; Q23 still proposes no timer and no variable | **PASS** |
| Heights | 173 / 183 / 208 cm | rows 26–27 unchanged (5'8"/173, 6'0"/183); row 28 still reads **6'10"** with no cm figure, and item 28's 208 cm remains a proposal against it | **PASS** |

**Range-collapse sweep: still zero.** The three duel-level states (Reposition, Select, Return to
Neutral) still carry one value per phase rather than four per attack, which is the shape the
GDD itself uses — it publishes per *state*, not per *attack*. **Not a collapse. CLEARED again.**

**§14 conversation bands re-checked** (these are the brief's suggestions, not GDD ranges) — every
chosen value still falls inside its band: Q1 100 ∈ 100–200 · Q2 **1200** ∈ 800–2000 · Q6 0.28 ∈
0.20–0.35 · Q7 0.12 ∈ 0.08–0.15 · Q8 0.55 ∈ 0.40–0.70 · Q18 0.35 ∈ 0.25–0.50 · Q19 1.2 ∈ 0.5–1.5 ·
Q20 0.50 ∈ 0.35–0.50 · Q26 7.0 ∈ 3–8 · Q27 1.0 ∈ 1.0–1.5 · Q28 0.25 ∈ 0.15–0.30. **All PASS.**
The two pass-1 HIGH findings on Q20's band and Q19's ceiling are unchanged in substance and are
now logged as item 72.

### CHECK 2 — SCOPE LOCK

| Wall | Result this pass |
|---|---|
| One player framework | **HOLDS.** Q14 1.000/1.000, Q15 600/600, Q16 400/400 still identical; group 03's six defensive values still shared and still forbidden from `DA_FighterProfile` |
| One authored AI opponent | **HOLDS.** GDD §04's *"no transformation rig and no second move set"* re-read verbatim; Q25 still re-times the same four rows, Q30 is still a mesh swap |
| One arena | **HOLDS.** One `L_ShatteredRing`; the 1800 × 1200 alternative is still a replacement footprint, not a second arena |
| Four attacks A–D | **HOLDS.** Item 26 is still **BLOCKED ON YOU** and still unresolved; group 07 still refuses the ranged reading — *"A ranged option would be a fifth attack and is forbidden by SCOPE LOCK regardless of what the panel says."* |
| One duel, win and loss | **HOLDS.** Q23 still ships exactly two terminal branches and still refuses `TimeExpired` |
| Nothing deferred acquired a design | **HOLDS.** Items 64–72 are corrections and reconciliations. None of them adds a feature, a fighter, an attack, an arena, a mode, progression or story. The three deferred ideas pass 1 tracked (adaptive dodge window, performance-gated Impact Window, beats that widen after failure) are still named-and-not-designed |

### CHECK 3 — dependent values agree, and did the corrections break anything

**The corrections changed no number, so the pass-1 dependency set is arithmetically
undisturbed.** I re-confirmed the five that the corrections could plausibly have touched:

| Dependency | Result |
|---|---|
| **Q2 = 1200 against the C3 correction** | **CLEARED.** The correction moved the *verdict*, not the *value*. Q2 is 1200 in all five places it appears; item 64 offers 1050–1100 as one of two designer paths without adopting it. Everything downstream of Q2 — the 45-combo count, the ~2:53 / ~4:29 gate timings, group 03's Q27 escalation table, group 07's "Q25 changes no damage value" note — still reads against 1200 and remains internally consistent |
| **Q18 = 0.35 s against Q25's Phase 2 play rate** | **CLEARED.** Reopening Q18 as PROPOSED did not delete the value or its formula. `MontageLength / EffectivePlayRate + 0.35` is intact in both `design/decisions.md` (line 217) and `TODO.md` item 29, and the "divide by *effective* play rate or it fires early on every Phase 2 telegraph" warning survives in both. Group 07 §Q18 and group 05's play-rate guard still agree |
| **Q17 against `IMC_Duel` and M1-10** | **CLEARED.** Reopening preserved the *genuinely blocked* flag — `IMC_Duel` needs a second binding if the answer is no — so M1-10's dependency is still visible. The anti-auto-success mechanism (bind on `Started`, a held button must not pass a beat) is untouched in group 06 |
| **Items 6 and 29 against `TODO.md`'s own bookkeeping** | **CLEARED, and the arithmetic is right.** Header claims *64 open · 8 closed · 35 PROPOSED · 1 blocked · 28 untouched*. Counted: the PROPOSED index totals **35** (5+6+6+6+4+4+2, plus items 6 and 29); blocked = item 26 = **1**; untouched = items 1, 46–63, 64–72 = **28**; 35 + 1 + 28 = **64** ✓; closed = items 4, 20, 28, 34, 35, 36, 37, 38 = **8** ✓, with 6 and 29 correctly no longer counted as closed. **The restoration did not corrupt the count** |
| **Items 64–72 against the existing numbering space** | **CLEARED.** 64–72 are new ids; no existing item was renumbered or reused; the §13.2-row collision at 58–61 is now explicitly warned about rather than silently live |

**All fourteen pass-1 dependencies plus the five I added there remain CLEARED**, because none of
their inputs moved. The two that were **ASSESSED rather than cleared** in pass 1 — Q25.11's
0.03 s A-cycle tension (pass 1 §5B) and the rival-speed knot (pass 1 §5 D/E) — are unchanged in
substance and are now items 66 and 67, which is the correct disposition for findings that need
the designer.

### CHECK 4 — no runtime AI-model calls, no auto-success, milestone order

**All three HOLD.**

- **No runtime model call.** Nothing in the Corrections block, in items 64–72, or in the
  restored items 6 and 29 proposes a model call, learning, adaptation or runtime generation.
  Re-read this pass and unchanged: GDD §04's *"The packaged duel makes no runtime LLM calls,
  does not learn from the player, and does not generate attacks or choreography dynamically"*;
  `combat-integration-plan.md` §checklist line 392 (*"Crimson Vanguard remains deterministic"*)
  and line 397; `build-sequence.md` M4-03 (*"the only nondeterminism is a weighted selection
  among in-range attacks using authored weights — no runtime model call"*) and Appendix A.
- **No auto-success.** `build-sequence.md` M3-07's three onboarding prohibitions are verbatim
  intact (no auto-success path; a pre-window press is **discarded, not queued**; the wider first
  window changes exactly one float), and M3-GATE still requires *"doing nothing never produces
  success."* Group 06's rejection of Final Fantasy XVI's unfailable clash by name is intact.
- **Milestone order.** No step was added, moved or reordered. `build-sequence.md` M5 still opens
  *"ONLY after M4 is stable … M5 must not be interleaved into M1–M4."* The four M5-placement
  judgements pass 1 examined (group 05 items 43/44 in M5-06, item 45 in M5-08, the Impact HUD
  functional-in-M3 / styled-in-M5 split, Q29's string-in-M3 / typography-in-M5 split) are
  unchanged. Items 68–71 record that `build-sequence.md` is *behind* the corrections, which is a
  staleness problem, not a milestone-order breach. The one borderline placement — group 08's Q31
  — is unchanged and still unlogged (N7).

---

## 6 — Per-step verdict

**Omitted.** §2 records that the build-step tracing job did not run: `build-sequence.md` is
unchanged since the pass-1 manifest and no build step was written or edited this session.

---

## 7 — Gaps

**Items correctly left open are a PASS and are not listed as gaps.** Everything pass 1 listed as
"still OPEN and correctly so" is still open and still correct: items 26, 46, 47, 48, 49, 50–53,
54–57, 59–63, plus the values the dispatches deliberately refused to invent (the rival's capsule
radius, the rival's walk speed, Nova's indicator hue, "SFN", `RivalDisplayName`).

**Pass-1 genuine gaps, re-checked:**

| Pass-1 gap | Status now |
|---|---|
| 1. `build-sequence.md` outside the correction scope (M3-08, M4-06, M4-08) | **CLOSED as a record gap** — items 68, 69, 70 exist and are accurate. The build steps themselves are still stale, which is what the items say |
| 2. No item for the Telegraph/Recover field schema | **CLOSED** — item 65 |
| 3. No item for restoring Q17 and Q18 | **CLOSED** — items 6 and 29 restored |
| 4. No item for resolving C3 | **CLOSED** — item 64 |

**Gaps opened or left open by this pass:**

1. **`Q45` is still written where `item 45` is meant** — `design/decisions.md` line 219 and, by
   propagation, `design/group-07-structure-and-canon.md` lines 603 and 711. No `TODO.md` item
   exists for it. This is the one claimed fix that did not land.
2. **`design/group-01-blocking-q22.md`'s divergence from the pass-1 manifest is unexplained**
   (N1), and its closing line still says Q22 is PROPOSED (N2). No item exists for either.
3. **Group 08's Q31 milestone-placement wording conflict is held nowhere but pass 1** (N7).
4. **`design/decisions.md`'s `Resolves:` lines for items 6 and 29 still imply deletion** (N3).

---

## 8 — Overall verdict

> **NOT CLEAN — but close, and clean on everything that matters most.** **Six of the seven
> claimed corrections landed and were verified against the files, not taken on trust.** The
> three pass-1 process-authority violations are properly remediated: Q17 and Q18 are back on the
> designer's list as PROPOSED with their values and warnings intact, and C3 is recorded as NOT
> satisfied with the substitution named as the violation and both remedies on the record. **The
> "no number was changed" claim is independently confirmed — Q2 is still 1200 in all five places
> it appears, `design/group-02-combat-economy.md` is byte-identical to pass 1, and 26/26 of
> Q25's values re-check IN RANGE against a freshly re-read GDD §04.** SCOPE LOCK, the
> no-runtime-AI rule, the no-auto-success rule and M1→M5 order all hold, and no new violation
> was introduced. **What stops this being CLEAN:** contradiction **C** was reported as fixed and
> is not — `design/decisions.md` line 219 still reads *"Keeps Q45's build behaviour"* — and
> `design/group-01-blocking-q22.md` has moved from **378 lines** to **385** with a different
> final line, which the correction pass did not disclose; I re-read that file in full and found
> no number changed and no scope breach, but a group file that moves silently defeats the only
> change-detection mechanism this pipeline has.

*Nothing above was repaired. Every value in this repository remains the human designer's to
approve, change, or reject.*
