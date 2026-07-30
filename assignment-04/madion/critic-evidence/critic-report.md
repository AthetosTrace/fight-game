# Critic Report — Consistency Pass on the Three Generated Outputs

**Audited:** `outputs/qa-edge-case-test-pack.md` · `outputs/animation-integration-briefs.md` · `outputs/vfx-audio-cue-sheets.md`
**Checked against:** `gdd/ascendant-impact-gdd-v0.4.md` · `combat-integration-plan.md` · `build-sequence.md` · `cinematic-integration-inspection.md` · `assignment-04/shared/knowledge-base/` · `assignment-04/shared/critic-rules/consistency-checklist.md`
**Method:** each output was re-read against the retrieved source text as an adversarial pass — the goal was to break the outputs, not to approve them. Every finding below quotes the generated claim, quotes the conflicting source with its location, states which wins and why, and shows the corrected line. All six corrections have been **applied to the output files**.

**Result: 6 real defects found and corrected. 0 invented.** Four of the six are the same failure mode — inference presented as sourced specification. That pattern is the report's main conclusion.

---

## Checklist sweep — the seven shared checks

Run first, against `assignment-04/shared/critic-rules/consistency-checklist.md`.

| # | Check | Result |
|---|---|---|
| 1 | Nova mistaken for the AI boss | **PASS.** Nova appears only twice across all three outputs, both as a player avatar: "run it once as Echo and once as Nova" (QA pack preconditions) and "Nova: cyan-white combat energy" as a player accent. Crimson Vanguard is named the rival throughout. No output describes Nova as an opponent. |
| 2 | Runtime-learning or runtime-LLM implied | **PASS.** The animation briefs state "No runtime model call anywhere in the attack path" as cross-attack check 12, and describe selection as "the only nondeterminism is authored weighting." No output implies learning, adaptation, or a model call. |
| 3 | Automatic or free Impact Window success | **PASS, and actively enforced.** The QA pack dedicates three tests to it — QA-IW-02 (pre-open press discarded), QA-IW-03 (doing nothing never succeeds, 10/10 failures required), and QA-IW-04 (no double award). CUE-IW-OPEN explicitly refuses to fire a cue before the window opens on the grounds that it "would function as a pre-open input tell." |
| 4 | Extra arenas or a fifth/altered attack | **PASS.** Four attacks throughout; "no fifth attack" appears as an explicit non-goal in all three outputs. One arena (`L_ShatteredRing`). Cross-attack check 1 requires "exactly four rows." |
| 5 | Altered governed numbers | **PASS on every governed number** — all timing bands, meter gains, window widths, the 50%/≤25% thresholds, meter-to-50, the 3 s cooldown, and the 1 HP floor match the GDD verbatim. **But see F5**, which is a related failure: a *derived* number was stated without its precondition. |
| 6 | Cinematics that fail to restore gameplay | **PASS, and notably does not overclaim.** All three outputs carry the V1–V5 caveat rather than asserting restoration works. The animation briefs' restoration section explicitly says "do not assume restore cleans up after you." This is the behaviour check 6 asks for. |
| 7 | Scope expansion beyond the single duel | **PASS.** No PvP, no playable Vanguard, no extra fighters, no progression. Deferred items are named as deferred where mentioned at all. |

Checklist sweep found nothing. The six findings below came from the deeper pass: comparing every *specific* claim against whether a source actually says it.

---

## F1 — Attack A's recover window described as the longest of the four attacks

**Severity:** medium. Would mislead an animator into authoring B/C/D with shorter recovers than the design requires.

**Generated claim** — `animation-integration-briefs.md`, Attack A window table:
> "| Recover | 0.45–0.90 s | 0.35–0.75 s | **longest of the four** — the deliberate punish opening |"

**Conflicting source** — `build-sequence.md`, step M2-13, `ANS_Recover` bullet:
> "Attack A = longest recover window **on the montage**"

**Which wins and why.** The source wins. "On the montage" scopes the comparison to Attack A's own timeline — A's recover is the longest of A's three windows. It does not rank A's recover against B, C, or D. The reading is settled by context: M2-13 is the step that authors Attack A, and at that milestone **B, C, and D do not exist yet** (they are authored at M4-01), so a cross-attack comparison could not be what the line means. My output silently promoted an intra-montage comparison into a cross-attack ranking.

This matters because the GDD's readability requirement for A is "distinct wind-up and **punishable recovery**" — A does need a generous recover. But the other three attacks also each carry a recover inside 0.45–0.90 s, and nothing licenses making them shorter than A's.

**Corrected line, now in the file:**
> "| Recover | 0.45–0.90 s | 0.35–0.75 s | **the longest of the three windows on A's own montage** (M2-13) — the deliberate punish opening |"

---

## F2 — Attack C asserted to hold the longest range band

**Severity:** medium. Q10 is an open designer value; this pre-empted it.

**Generated claim** — `animation-integration-briefs.md`, Attack C, "Gameplay purpose and range":
> "Armored reach and space control — the long-range option that punishes standing at what feels like a safe distance. Range band `OPEN — Q10`, **the longest of the four**."

**Conflicting source** — `gdd/ascendant-impact-gdd-v0.4.md`, Page 5, "Four-attack course set". The GDD's entire range/purpose entry for C is:
> "Authored attack C | Armored reach and space control | Clear body direction and visible active range"

And `combat-integration-plan.md` §3.1 row 14 lists ranges as:
> "ranges (Q10)" — i.e. `OPEN — designer decides`

**Which wins and why.** The source wins, and the defect is sharper than it looks. The GDD gives C "armored reach" but **never ranks the four range bands against one another**. Worse, the ranking I asserted is plausibly *wrong*: Attack D is a "short propulsion-assisted approach" whose purpose is closing a gap, which implies D is selected at a distance that C might not cover. Asserting C is longest could invert the selection design.

The output correctly marked the band `OPEN — Q10` and then, in the same sentence, characterised it anyway. Marking a value open and then describing it is the same defect as filling it in.

**Corrected line, now in the file:**
> "Armored reach and space control — punishes standing at what feels like a safe distance. Range band `OPEN — Q10`. The GDD gives C 'armored reach and space control' but **does not rank the four range bands against each other**; do not assume C holds the longest band until Q10 is set."

---

## F3 — Attack B given a range band and a travel distance neither of which is sourced

**Severity:** medium. Same class as F2, plus an unsourced physical claim.

**Generated claims** — `animation-integration-briefs.md`, Attack B:
> "a multi-beat advance that pressures the player **across a short distance**. Range band `OPEN — Q10`, **mid band**."

and, under root motion:
> "Root motion: **forward travel across the beats** — this is 'forward-pressure.' Authored as root motion."

**Conflicting source** — `gdd/ascendant-impact-gdd-v0.4.md`, Page 5:
> "Authored attack B | Committed forward-pressure sequence | Visible first beat and stable tracking limit"

`build-sequence.md` M4-01 for B:
> "**B** (committed forward-pressure sequence) — visible first beat; **multiple separate `ANS_ActiveHit` states**, one per beat, so each beat is individually dodgeable; `ANS_TrackingLock` at a fixed point (stable tracking limit)."

**Which wins and why.** The sources win. Between them they specify B's beat structure, its dodgeability, and its tracking lock — and say **nothing** about a range band, nothing about distance, and nothing about root-motion travel. "Forward-pressure" is suggestive of advancing, but that is my inference, and the output stated it as authored fact in a document an animator would build from.

The distinction is not academic: `MaxTravelDistance` is a real field that exists specifically to cap travel, and it is attached to **D**, not B. If B travels meaningfully and nobody measured it, B inherits D's failure mode ("no hidden full-arena snap") with none of D's guardrails — which is exactly the row-versus-montage drift plan §8.5 warns about.

**Corrected lines, now in the file:**
> "Committed forward-pressure sequence — a multi-beat advance that pressures the player. Range band `OPEN — Q10`; the GDD does not state B's band or rank it against the others."

> "Root motion: **forward travel across the beats is inferred from the GDD's 'forward-pressure' purpose, not specified upstream.** No source states that B travels, how far, or by what means. Treat the advance as a design question for the designer, and if B does travel, apply the same measured discipline as D even though the cap field is D's."

---

## F4 — `bUsesPropulsion` stated as a settled row value for A, B, and C

**Severity:** low-medium. Correct by inference, wrong by authority.

**Generated claims** — `animation-integration-briefs.md`, three locations:
> Attack A: "`bUsesPropulsion` = **false**. `MaxTravelDistance` unused."
> Attack B: "`bUsesPropulsion` = **false** (that is D's mechanic)."
> Attack C: "`bUsesPropulsion` = **false**."

**Conflicting source** — `build-sequence.md` M2-03 lists the field without assigning per-attack values:
> "`bUsesPropulsion` (bool), `MaxTravelDistance` (float — **OPEN — §14 Q13**), `bLockTrackingAtActive` (bool)"

And the project's own governing rule, `combat-integration-plan.md` §2 principle 8:
> "No agent — including this one — resolves a provisional value."

**Which wins and why.** The source wins on authority even though my inference is almost certainly right. The GDD attributes propulsion to D alone, so `false` for A/B/C is the natural reading — but no source *states* those row values, and a document that presents them in the same typographic register as genuinely quoted values (`bLockTrackingAtActive` = true for B and C, which **is** sourced to M4-01) teaches the reader to trust both equally. That is the actual harm: mixing sourced and derived values with no visual distinction.

Note the asymmetry this exposes. `bLockTrackingAtActive` for B and C is directly sourced ("`ANS_TrackingLock` freezes facing where the row asks (B, C)"). `bUsesPropulsion` for A/B/C is not. The output presented them identically.

**Corrected lines, now in the file** — each now labels the derivation and returns authority to the designer:
> A: "`bUsesPropulsion` — expected **false**, `MaxTravelDistance` unused. *Derivation, not a quoted value:* the GDD attributes propulsion to **D only** ('Short propulsion-assisted approach'), so A/B/C read as non-propulsion. The row values themselves are the designer's to set."

> B: "`bUsesPropulsion` — expected **false** (propulsion is attributed to D alone). Same derivation caveat as A: the row value is the designer's."

> C: "`bUsesPropulsion` — expected **false** (same derivation as A and B)." — and the tracking-lock line now says explicitly "This one *is* sourced: M4-01 names B and C as the tracking-lock attacks."

---

## F5 — A derived meter total stated as a flat expected value

**Severity:** medium-high for the QA pack specifically, because a tester would record a false failure.

**Generated claim** — `qa-edge-case-test-pack.md`, QA-V1-01 state table:
> "| `Meter` | 32 after the +20 lands (12 + 20, plan §7) | 32 |"

**Conflicting source** — `combat-integration-plan.md` §7, the vertical-slice table, which states 32 **inside a specific scenario**: a single defined slice run consisting of exactly one perfect dodge and one Impact success:
> "`RestoreCombatState()` → player input, collision, locomotion, lock-on live; rival BT resumes at `Idle_Reposition` with `CurrentState` visible; meter shows 32 (+12 +20)"

And `gdd/ascendant-impact-gdd-v0.4.md` Page 3, which makes the meter cumulative and bounded:
> "Ascension Meter is a visible 0–100 resource earned only through active combat decisions."

**Which wins and why.** The source wins. 32 is arithmetic — **+12** perfect dodge plus **+20** Impact success — and it is only the expected total if the meter was at 0 when the run started. Plan §7 can state it flatly because it describes one scripted slice from a fresh start. QA-V1-01 does not; it is a test a tester may run at any point in a session, including immediately after another test that already banked meter. A tester who has run QA-IW-01 first arrives at this table with meter already above 0, sees a number other than 32, and records a failure against a system that is working correctly.

This is the subtlest of the six because the number is not *wrong* — it is right under an unstated precondition. That is precisely the failure the project's own numbers discipline exists to prevent.

**Corrected lines, now in the file** — expected value expressed as the relationship, plus a new precondition:
> "| `Meter` | **starting value + 12 + 20.** Equals 32 **only if the run begins at meter 0**, which is the condition plan §7 states it under — record the starting value before step 1 rather than expecting 32 | unchanged from the burst value |"

> Added to QA-V1-01 preconditions: "**Record `Meter` before step 1.** Plan §7's figure of 32 assumes a fresh run starting at 0; on any other run the expected value is the starting value plus the gains this test earns."

---

## F6 — An arena color palette invented, and an unsourced absence asserted

**Severity:** low for the palette, low for the dodge cue — but the palette claim is a straight fabrication and belongs in the report on principle.

### F6a — the arena palette

**Generated claim** — `vfx-audio-cue-sheets.md`, CUE-TEL-C accessibility row:
> "A red-tinted floor area is a **fail** — it becomes invisible against **a red-orange arena palette** for a protanopic player."

**Conflicting source** — `gdd/ascendant-impact-gdd-v0.4.md`, Page 9, "Official arena direction". The GDD describes Shattered Ring **functionally and gives it no colors at all**:
> "The established industrial Shattered Ring arena is locked as the official Version 1 environment."
> "Central combat floor | Open, readable space for spacing, lock-on, dodges, counters, and Final Clash staging"
> "Far doorway | Dedicated Crimson Vanguard entrance axis"
> "Environmental reaction | Visible but controlled reaction during major impacts without adding gameplay hazards"

Red-orange belongs to **Crimson Vanguard**, per `core-canon.md`: "Red-orange systems and warning lights." I transplanted the character's palette onto the arena.

**Which wins and why.** The source wins, and this is the clearest defect in the set: the GDD attaches no palette to Shattered Ring, and `CLAUDE.md` records that the arena "has no history — it is specified as a functional space." Inventing an arena color is exactly the kind of unflagged new fiction the project forbids. The accessibility *conclusion* survives — a red-on-red floor cue is still a bad idea — but it survives for a different and defensible reason: the cue would compete with the Vanguard's own red-orange warning language on the mesh in front of it.

**Corrected line, now in the file:**
> "Passes only if the range indication is shape-based. A red-tinted floor area is a **fail** — the cue would be competing with the Vanguard's own red-orange warning language on the mesh directly in front of it, and hue alone cannot separate the two for a protanopic player. Use an outline, hatch, or edge. *(The Shattered Ring's own palette is not specified by the GDD — it is described functionally as an 'industrial' arena with a central floor and far doorway. Do not author against an assumed arena color.)*"

### F6b — the ordinary dodge asserted to have no cue

**Generated claim** — `vfx-audio-cue-sheets.md`, CUE-DEF-PERFECT intensity row:
> "Deliberately louder than an ordinary dodge, which gets **no** cue and **no** meter."

**Conflicting source** — `combat-integration-plan.md` §3.2 row 8 supports half of it:
> "Detected only by the same trace that decides damage; **ordinary dodge grants no meter**"

No source addresses whether an ordinary dodge has a cue.

**Which wins and why.** The source wins on the half it covers and is silent on the rest. "No meter" is quotable. "No cue" is an assertion about a presentation decision that is M5 work and nobody has made. Asserting an absence is still asserting.

**Corrected line, now in the file:**
> "**strong**. Deliberately louder than an ordinary dodge, which grants **no meter** (plan §3.2 row 8: 'ordinary dodge grants no meter'). Whether an ordinary dodge carries any cue at all is `OPEN — designer decides` — no source says it has none. The requirement here is only that the two are unmistakably distinguishable, because that contrast is what teaches the mechanic."

---

## Things checked that turned out clean

Recorded so the pass is auditable, and so a later reader knows these were examined rather than skipped.

| Claim examined | Verdict |
|---|---|
| Active window "identical both phases" in all three outputs | **Correct.** GDD Page 5 gives Active 0.18–0.45 s in both columns; plan §5.2 says "identical both phases by design." |
| The 1 HP floor treated as unresolved in all three outputs | **Correct and required.** Q22 is `OPEN`. QA-FC-01 observes rather than asserts; CUE-FC-FAILURE authors no floor cue. This is the right handling. |
| Meter values +5/+12/+15/+20/+0 | **Correct**, GDD Page 3–4 verbatim. |
| Window widths 0.75 s and 0.35–0.50 s | **Correct**, GDD Page 3 verbatim. |
| Clash failure: meter 50, 3 s cooldown, no restart, no player death | **Correct**, GDD Page 4 verbatim. |
| Phase 2 at 50%, Clash gate at ≤25%, AND not OR | **Correct**, GDD Page 3–4 verbatim. |
| Six state names and their order | **Correct**, GDD Page 5 verbatim. |
| Counter routed through the Sequence, never `Abort`/`Stop Logic` | **Correct**, plan §3.1 row 13 and M2-14. |
| `ANS_ActiveHit` as one class shared by both fighters | **Correct**, plan §3.1 row 16. |
| Vanguard proxy at 208 cm | **Correct**, plan §8.2 ladder. Also consistent with the 6'10" figure in `core-canon.md`. |
| Motion Warping described as not-the-default | **Correct**, plan §8.7: "the design's own R5 fallback is already the default — root-motion montages with a hard distance cap." |
| Tracking lock on B and C only | **Correct**, M4-01 and M4-02. |
| B's multiple `ANS_ActiveHit` states, one per beat | **Correct**, M4-01 verbatim. |
| D's thruster cue inside `ANS_Telegraph` | **Correct**, M4-01. |
| V1–V5 descriptions and their blocking milestones | **Correct**, inspection §2 and §8. Quoted rather than paraphrased throughout. |
| No output claims restoration is fixed | **Correct** — the checklist's check 6 explicitly warns against overclaiming here, and all three outputs carry the caveat. |
| Echo 183 cm / Nova 173 cm, Echo orange / Nova cyan-white | **Correct**, `core-canon.md`. The cue sheet additionally flags the hue distinction as never load-bearing, which is a genuine accessibility improvement rather than a contradiction. |
| Contamination from the other capstone project | **Zero hits.** Grepped all three outputs for werewolf / mansion / scent / villager — nothing. |

---

## The pattern worth naming

Four of six findings — F2, F3, F4, and F6 — are the same defect: **inference presented in the same register as sourced fact.** None of the four was a wild invention; three of them are probably right. The failure was typographic and epistemic rather than factual: a document that renders `bLockTrackingAtActive = true` (sourced) and `bUsesPropulsion = false` (inferred) in identical formatting trains its reader to trust both equally, and an implementer building from it cannot tell which values they may safely change.

F1 and F5 are a second pattern: **a source claim carried out of the scope that made it true.** "Longest recover on the montage" became longest of four; "meter shows 32" in a fresh scripted slice became a flat expected value in a test runnable at any time.

Both patterns are invisible to the seven-item shared checklist, which passed cleanly. The checklist catches contradictions of canon. Neither of these was a contradiction — they were over-extensions, which is what a second adversarial read is actually for.

**The concrete process change this drove** is recorded in `../README.md` §5: every generated claim now carries a visible marker distinguishing *quoted from source*, *derived by inference*, and `OPEN — designer decides` — and where a number is derived, the derivation is shown so the reader can check it rather than trust it.

---

*End of critic report. Six defects found, six corrections applied to the output files. No defect was invented to fill the section.*
