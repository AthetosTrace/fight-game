# Inspection — cross-consistency audit of the session's design answers

**Inspector dispatch, 2026-08-02.** This is a **cross-consistency pass over the forty-five
open items worked in nine dispatches**. It is **not** the Assignment #03 build-sequence
tracing pass. `inspection.md` in the project root is that artifact and is **untouched** by
this run. `leave-offs/inspector.md` is untouched. The only file written is this one.

**Standing rule: I report, I do not repair.** Nothing below was fixed. Every finding names
the file, the item, the value, and the rule, GDD heading, or range it meets or breaks.
**A value left OPEN or blank is a PASS, not a gap.**

---

## 1 — Inspected-inputs manifest

| # | Path | Lines | Final non-empty line (exact) |
|---|---|---|---|
| 1 | `design/decisions.md` | 530 | ` ``` ` |
| 2 | `TODO.md` | 450 | `line — the GDD had the value all along. **Do not add the GDD-out-of-date item for it.**` |
| 3 | `design/group-01-blocking-q22.md` | 378 | `---` |
| 4 | `design/group-02-combat-economy.md` | 681 | `| **This is Ascendant Impact** | Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, the Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears |` |
| 5 | `design/group-03-defensive-timing.md` | 1243 | `reject.*` |
| 6 | `design/group-04-spacing-and-arena.md` | 1067 | `**Everything in this file is the human designer's to approve, change, or reject.**` |
| 7 | `design/group-05-fighter-feel.md` | 1086 | `---` |
| 8 | `design/group-06-final-clash.md` | 1197 | `record owns all of them.*` |
| 9 | `design/group-07-structure-and-canon.md` | 1162 | `Nothing in this file supersedes a GDD line, and no GDD number or range was altered.*` |
| 10 | `design/group-08-assets.md` | 492 | `| **This is Ascendant Impact** | Echo, Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears |` |
| 11 | `design/group-09-cinematic-corrections.md` | 975 | `repairs every branch at once.*` |
| 12 | `design-brief.md` | 1091 | `*End of design brief. Every rule and number in this document remains the human designer's to approve, change, or reject.*` |
| 13 | `project-brief.md` | 388 | `LOCK as a wall, and never propose a runtime AI-model call.` |
| 14 | `build-sequence.md` | 933 | `or reject; the developer changed none and resolved none.*` |
| 15 | `combat-integration-plan.md` | 406 | `*End of combat integration plan. The approved foundation is implemented as specified; every rule and number remains the human designer's to approve, change, or reject.*` |
| 16 | `cinematic-integration-inspection.md` | 236 | `*End of cinematic integration inspection. Verdict: APPROVED WITH REQUIRED CHANGES — corrections 1–5 to the human designer before M3; the foundation, the first test, and M1–M2 may proceed.*` |
| 17 | `gdd/INDEX.md` | 79 | `` `pdftoppm` is not. Re-run the section split, re-extract the page images, and re-read `` |
| 18 | `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` | 52 | `Attack set Four authored attacks Same four authored attacks` |

**Files treated as this-session work:** `design/decisions.md`, `TODO.md`, and all nine
`design/group-0*.md` files. **`build-sequence.md`, `combat-integration-plan.md`,
`cinematic-integration-inspection.md`, `design-brief.md`, `project-brief.md` and everything
under `gdd/` were read as sources of truth and were unchanged this session.**

Partial reads: `design/group-03`, `-04`, `-05`, `-06`, `-07`, `-08`, `-09` and
`design-brief.md` were read in overlapping page ranges covering the whole file. Group 09
§V3–V5 body text (lines ~450–830) was read in summary form via its correction tables, its
`RestoreCombatState()` contents list, and its gate checklist; the five acceptance
conditions and all of its numeric claims were checked directly.

---

## 2 — Coverage statement

**The build-step tracing job did NOT run this pass.** `build-sequence.md` exists but was
**not written or edited this session** — group 09 states explicitly that
`build-sequence.md` is unmodified, and no dispatch produced a new build step. This pass is
a **design-answer cross-consistency audit**, as dispatched. `build-sequence.md` was still
read, because CHECK 3 requires knowing what the build currently says about the values the
dispatches moved; that reading produced four cross-artifact findings (§5, items F–I) which
are reported but **not** presented as step-level TRACES/ORPHAN verdicts.

---

## 3 — VIOLATIONS

Three. Each names the rule it breaks.

### VIOLATION 1 — Q18 was resolved to a number and closed by a dispatch, not by the designer

- **Where:** `design/group-07-structure-and-canon.md` §Q18; recorded as **APPROVED** in
  `design/decisions.md` (group 07 entry) and **deleted from `TODO.md`** (item 29 is absent
  from the list).
- **The value:** `MontageFailsafeMarginSeconds = 0.35 s`, as
  `MontageLength / EffectivePlayRate + 0.35`.
- **The rule broken:** `CLAUDE.md`, HARD CONSTRAINT — *"No agent may change a number, and
  **no agent may resolve a provisional value on its own authority** — it surfaces the
  question instead."* Reinforced by `design-brief.md` §0: *"The developer must not pick a
  value from a proposed range on its own authority."* `design-brief.md` **§14** lists Q18
  under *"Questions for the human designer"* with a designer-owned band of **0.25–0.50 s**,
  and §13.2 row 46 lists it as `OPEN`.
- **Precisely what is wrong:** the value is **inside** its band, so no range is broken. The
  **authority** is. Group 07's own justification concedes the point — *"Any value in
  0.25–0.50 works; 0.35 is the middle with a documented reason"* — which is the definition
  of a designer choice, not of a KIND A item with "nothing to decide." Reclassifying a §14
  question as KIND A does not remove it from §14. **The `TODO.md` deletion is the part that
  makes this a violation rather than a recommendation**: the question is now invisible to
  the designer.
- **Not fixed here.** The remedy is the designer's: either approve 0.35 s on the record, or
  restore item 29 to `TODO.md` marked PROPOSED.

### VIOLATION 2 — Q17 was confirmed and closed by a dispatch, where §14 asks the designer to confirm

- **Where:** `design/group-06-final-clash.md` §Q17; **APPROVED** in `design/decisions.md`;
  **deleted from `TODO.md`** (item 6 is absent).
- **The answer:** reuse `IA_Impact` for both Clash beats; one `IMC_Duel`; no context swap.
- **The rule broken:** `design-brief.md` **§14** — *"**Q17** — Do the Clash beats reuse
  `IA_Impact`? Recommend yes, for learned consistency. **Designer confirms.**"* The brief
  names the actor who closes this item, and it is not a dispatch. Same `CLAUDE.md` HARD
  CONSTRAINT as Violation 1.
- **Mitigating, stated plainly:** the engineering content is sound and §14 already
  recommended the same answer, so the *substance* is very unlikely to be overturned. The
  defect is procedural and identical in shape to Violation 1: an item the human owns has
  been removed from the human's list.
- **Not fixed here.**

### VIOLATION 3 — Constraint C3 from the APPROVED Q22 is not satisfied, and the acceptance criterion was rewritten instead of the failure being surfaced

- **Where:** `design/group-02-combat-economy.md` §Cross-check item 5; `design/decisions.md`
  group 02 entry — *"C3 is satisfied, but not as framed."*
- **The constraint, verbatim:** `TODO.md` header and `design/decisions.md` Q22 entry —
  *"**C3** Q2 must be tuned so ≤25 % rival health and meter 100 arrive close together."*
  `TODO.md` states these three constraints **"bind every answer below."** Q22 is the one
  item in the whole set that carries the designer of record's actual approval, so its
  attached conditions carry that approval too.
- **What was delivered:** Q2 = 1200 puts **meter 100 at ~0:40–1:25** and the **≤25 % health
  gate at ~2:53** — a separation of roughly **90 to 135 seconds**. Group 02 states outright
  *"They do **not** arrive close together"* and then argues that the ordering
  (meter-first) is the safe direction and declares C3 satisfied on that basis.
- **Why this is a violation and not a judgement call:** the argument may well be correct —
  it is a good argument — but **a dispatch may not amend an approved constraint's success
  criterion and then mark itself compliant against the amended one.** C3 says "close
  together." 90–135 s apart is not close together on any reading. The correct action was to
  surface it: *"Q2 = 1200 does not satisfy C3 as written; here is why C3 may be the wrong
  constraint; designer decides."* Group 06 independently supplies the fix that would satisfy
  C3 (**Q2 → 1050–1100**) and calls it *"the designer's single most effective lever,"* so
  the compliant path exists and was not taken.
- **Not fixed here.** The designer must either amend C3 on the record or re-tune Q2.

**No violation was found of the GDD itself.** No GDD number was altered, no published range
was collapsed, no fifth attack or second arena or second move set acquired a specification,
and nothing anywhere proposes a runtime model call, learning, or adaptive difficulty. The
three violations above are all violations of **process authority**, not of the source of
truth.

---

## 4 — Session audit

### CHECK 1 — Every value against its published range

**Q25's 26 values, verified cell by cell rather than taken on trust.** I recomputed each
against `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` (PDF p. 5), which I read
directly and which matches the range table in the dispatch brief exactly.

| Field | Values | GDD range | Verdict |
|---|---|---|---|
| Telegraph P1, A/B/C/D | 0.70 / 0.60 / 0.80 / 0.90 | 0.55–0.95 | **4/4 IN** |
| Telegraph P2, A/B/C/D | 0.55 / 0.48 / 0.62 / 0.70 | 0.40–0.75 | **4/4 IN** |
| Active (one value, both phases), A/B/C/D | 0.22 / 0.36 / 0.30 / **0.45** | 0.18–0.45 both phases | **4/4 IN**; D on the inclusive upper bound |
| Recover P1, A/B/C/D | 0.85 / 0.70 / 0.60 / 0.55 | 0.45–0.90 | **4/4 IN** |
| Recover P2, A/B/C/D | 0.68 / 0.56 / 0.48 / 0.44 | 0.35–0.75 | **4/4 IN** |
| Reposition P1 / P2 | 0.90 / 0.55 | 0.60–1.20 / 0.35–0.80 | **2/2 IN** |
| Select P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |
| Return to Neutral P1 / P2 | 0.15 / 0.15 | 0.10–0.20 | **2/2 IN** |

> **Group 07's claim of 26/26 in range is CONFIRMED by independent recomputation.**
> Zero out of range. Attack D's Active at 0.45 s is exactly the published maximum and is
> in range only under `Min <= Value <= Max`; group 07 says so and specifies the inclusive
> comparison in its Q25.9 validation spec. **That cell has zero upward headroom** and is
> the single most fragile value in the set.

**Active Attack is correctly not phase-scaled.** GDD §04 publishes 0.18–0.45 s for both
phases. Q25.5 keeps `ActiveSeconds` on the Data Table row outside both phase structs and
proves that scaling D's 0.45 s by the ~0.78 Phase 2 ratio would push a 600 cm dash to
1714 cm/s and break GDD §04's *"no hidden full-arena snap."* **CLEARED, and the reasoning
is correct.**

**Every other range-bounded value:**

| Value | Published | Chosen | Verdict |
|---|---|---|---|
| Meter range | 0–100 | unchanged everywhere | **PASS** |
| Meter gains | +5 / +12 / +15 / +20 / +0 | unchanged everywhere; group 03 explicitly refuses to change one even where doing so would have answered group 02's question | **PASS** |
| Phase 2 trigger | 50 % | unchanged | **PASS** |
| Clash gate | meter 100 **AND** rival health ≤ 25 % | unchanged | **PASS** |
| Failed Clash | 1 HP floor / meter to 50 / 3 s | unchanged in groups 01, 02, 06, 09 and in `build-sequence.md` M4-08 | **PASS** |
| First Impact Window | **0.75 s** | unchanged; group 03's Q26 first-window exemption preserves the onboarding rule | **PASS** |
| Standard Impact Window | 0.35–0.50 s | the range is preserved as a range; Q20 borrows **0.50 s** from inside it for a different mechanic | **PASS** |
| Impact burst | 1–3 s | preserved as a range; group 03 and group 06 use midpoints only in labelled estimates | **PASS** |
| Session length | 3–5 minutes | treated as a target, never a timer (Q23 = no timer, no variable) | **PASS** |
| Heights | 173 / 183 / 208 cm | item 28 = 208 cm, verified: 82 in × 2.54 = 208.28, rounded exactly as 173 and 183 are | **PASS** |

**Range-collapse sweep: no published GDD range was collapsed to a single number anywhere.**
The one thing that looks like a collapse is not one: group 07 gives Reposition, Select and
Return to Neutral **one duel-level value per phase** rather than four per-attack values.
The GDD publishes those states per *state*, not per *attack*, so a single value per phase is
the shape the GDD itself uses. **CLEARED.**

**§14 conversation bands** (the design brief's own suggestions, not GDD ranges) — every
chosen value falls inside its band: Q1 100 in 100–200 · Q2 1200 in 800–2000 · Q6 0.28 in
0.20–0.35 · Q7 0.12 in 0.08–0.15 · Q8 0.55 in 0.40–0.70 · Q18 0.35 in 0.25–0.50 · Q19 1.2 in
0.5–1.5 · Q20 0.50 in 0.35–0.50 · Q26 7.0 in 3–8 · Q27 1.0 in 1.0–1.5 · Q28 0.25 in
0.15–0.30. **All PASS.**

**HIGH finding, not a violation — Q20's stated tuning band exceeds the range it claims to
be reusing.** `design/group-06-final-clash.md` justifies 0.50 s as *"the top of the GDD's
published Standard Impact Window range (0.35–0.50 s), so no number is invented"* — and then
publishes a tuning band of **0.45–0.60 s**. The **0.50–0.60 s upper half of that band is
outside** the published range the file's own justification rests on. The Clash beats have no
published GDD range of their own, so this breaks no GDD line — but if the designer takes
0.55 or 0.60 s, the Clash beats become more generous than any window value published
anywhere in the GDD, and the file's "no number is invented" claim stops being true. **Named,
not resolved.**

**HIGH finding, not a violation — Q19's "hard ceiling 1.30 s" narrows a designer-owned
band, and its arithmetic is superseded by Q25.** Group 06 instructs *"Do not go above
1.30 s"* against §14's published 0.5–1.5 s band. The 1.30 s figure is the sum of the GDD's
**Phase 2 floors** (Recover 0.35 + Return 0.10 + Reposition 0.35 + Select 0.10 + Telegraph
0.40). Under **Q25's authored Phase 2 values** the same chain is 0.44 (D's Recover, the
shortest) + 0.15 + 0.55 + 0.15 + 0.48 (B's Telegraph, the shortest) = **1.77 s**. So the real
earliest-next-strike floor is 0.47 s later than group 06 computed, Q19 = 1.2 s has ~0.57 s of
margin rather than 0.10 s, and **§14's rejected 1.5 s would in fact be safe** under Q25. The
narrowing is conservative — it errs toward a shorter window, which is the safe direction —
but it is a directive to the designer resting on arithmetic another dispatch has superseded.
**Recompute Q19's ceiling once Q25 is approved.**

### CHECK 2 — SCOPE LOCK

| Wall | Result |
|---|---|
| One player framework | **HOLDS.** Q14 = 1.000/1.000, Q15 = 600/600, Q16 = 400/400 — all three "fighter feel" scalars resolve **identical**. Group 03 puts Q6/Q7/Q8/Q28 on shared assets and states explicitly that they *must not* live on `DA_FighterProfile`. Group 04 holds Echo's and Nova's capsule **radius** identical at 40 cm on purpose, because radius is what decides at what separation each can be struck. |
| One authored AI opponent | **HOLDS.** No second rival, no second move set, no transformation. GDD §04's *"no transformation rig and no second move set"* is honoured by Q25 (Phase 2 is a re-timing of the same four rows) and by Q30 (a **mesh** swap, not a design change). |
| One arena | **HOLDS.** Q24 specifies one `L_ShatteredRing`. Group 04's "honest alternative" (1800 × 1200) is offered as a *replacement* footprint, not a second arena. Item 18 makes the mezzanine set dressing precisely to avoid a second traversal layer. |
| Four attacks A–D | **HOLDS.** Item 26 is the pressure point and it held correctly: group 07 refused to let a low-confidence "plasma-gauntlet" transcription add a ranged option, and states *"A ranged option would be a fifth attack and is forbidden by SCOPE LOCK regardless of what the panel says."* |
| One duel, win and loss | **HOLDS.** Q23 ships **exactly two** terminal branches and refuses a third (`TimeExpired`) on the explicit ground that a timer is a second loss condition the GDD does not have. |
| No progression / multiplayer / story / difficulty setting | **HOLDS.** Three deferred features were considered and each was named as deferred rather than designed: an adaptive perfect-dodge window (group 03 Q7), a performance-gated Impact Window replacing the timer (group 03 Q26), and beats that widen after failures (group 06 Q20). |

**Two items examined closely and cleared:**

- **Group 05 items 43/44 give Echo and Nova *different* emissive geometry and different
  `AscensionEmissiveCurve` assets.** This is not a per-fighter mechanical difference: the
  channel *reads* state and never creates state, carries no damage/meter/timing/collision,
  is explicitly *"never the only channel"* with the HUD authoritative, and is placed
  entirely in **M5-06**. **CLEARED.**
- **Q30 puts the rival on Paragon Crunch's own skeleton with a foreign `AnimBP`.** The
  SHARED PLAYER-KIT SCOPE RULE binds Echo and Nova only; the rival was never in that
  framework. **CLEARED.**

**One observation, not a violation.** Group 05 item 43 proposes **adding a small emissive
indicator to Echo's helmet** — geometry page 12 does not show. The page-12 callout reads
*"Visor or Light"* and the dispatch reads it as *"visor AND light"*, which is an
interpretation of ambiguous reference art, correctly flagged as such and correctly placed in
M5-06. It is a designer call, not a scope breach. **Named so it is a decision rather than a
drift.**

### CHECK 3 — Dependent values

Every dependency the dispatch named, plus five I added. **Cleared** means I recomputed it
and it holds.

| # | Dependency | Result |
|---|---|---|
| 1 | **Q3 damage expressed against Q1 health; hits-to-kill arithmetic** | **CLEARED.** Q1 = 100 makes "% of player max HP" and the Data Table integer the same number. A 32 → 4 hits (96 < 100 ≤ 128); B 25 → **exactly 4** (100); C 27 → 4 (81 < 100 ≤ 108); D 18 → 6 (90 < 100 ≤ 108). Mean 25.5 → ~4. Matches §14's 3–5-hit budget for A/B/C; D is deliberately a 6-hit chip attack matching its GDD "approach" role. Arithmetic is correct as published. |
| 2 | **Q13's 600 cm inside Q24's 2400 × 1600 cm** | **CLEARED.** 600 = 0.25 × 2400 exactly. Fractions check: 25.0 % of the long axis, 20.8 % of the 2884 cm diagonal. GDD §04's *"no hidden full-arena snap"* is satisfied with wide margin, and stays satisfied automatically because the value is stored as a fraction of `ArenaLongAxisCm`. |
| 3 | **Q21's 1200 cm inside the arena** | **CLEARED.** Two points 1200 cm apart on a 2400 cm axis leave 1200 cm of redistribution slack, so the clamp always succeeds from anywhere in the room. The long-axis push rule is what makes this true; a facing-relative push would clamp to as little as ~700 cm. |
| 4 | **Q10 bands + Q12 cooldowns do not starve the rival** | **CLEARED, and now with much more margin than group 04 claimed.** Group 04 proved starvation-free against the GDD's *fastest legal* cycles (1.98 s P1 / 1.48 s P2), tightest slack **+0.16 s**. Re-running with **Q25's authored cycles** — P1 A 2.97 / B 2.86 / C 2.90 / D 3.10, P2 A 2.30 / B 2.25 / C 2.25 / D 2.44 — every depth-2 zone re-offers in 5.76–5.96 s (P1) and 4.55–4.69 s (P2) against longest cooldowns of 3.8 s and 2.8 s. **Slack is now +2.0 s or better everywhere. Q25 makes group 04's tightest case disappear.** |
| 5 | **Q21's separation sits outside the bands, as §14 requires** | **CLEARED, and §14's stated test is the wrong test — group 06 caught this correctly.** §14 asks for "outside every attack's `MinRange`"; the largest `MinRange` is B at 90 cm, which **any** value above 90 cm passes, so the test does not discriminate. The binding test is the largest **`MaxRange`** — D at 840 cm — and 1200 cm sits 360 cm beyond it, inside group 04's identified 840–2884 cm zero-coverage region. **No attack is selectable at 1200 cm.** |
| 6 | **Q7 strictly narrower than Q6** | **CLEARED.** [0.03, 0.15] ⊂ [0.03, 0.31]. Shares the start instant, ends 0.16 s earlier. 0.12 / 0.28 = 43 %, as claimed. |
| 7 | **Q6 and Q7 fit inside item 48's dodge montage length** | **CLEARED, and item 48 is OPEN, which is a PASS.** Q6 ends at 0.31 s of montage time. Group 03 offers 0.45–0.55 s as conversation; group 05 independently assumes "~0.50 s with displacement front-loaded across roughly the first 0.30 s" for its 400 cm / ~1330 cm/s figure (400/0.30 = 1333 ✓). **The two dispatches' working assumptions agree**, and either contains both windows with a 0.14–0.24 s vulnerable tail. No value was invented. |
| 8 | **Q20's beat windows consistent with the GDD's 0.35–0.50 s standard** | **CLEARED for the proposed value (0.50 s, both beats, identical).** See the HIGH finding above regarding the 0.45–**0.60** band. |
| 9 | **Q25's per-attack cycle vs Q12's cooldowns — the 2.97 / 3.0 s case** | **ASSESSED. The 0.03 s figure is real but is measured against a self-imposed wall, and the fight state it describes rests on an unreachable distance band.** See §5 item B — this is the most consequential contradiction in the set. |
| 10 | **Q27 = 1.0 and group 02's Q2 = 1200 derivation** | **CLEARED.** At Q27 = 1.0 the effective-damage expression `20 × [f × Q27 + (1 − f)]` equals 20 for every value of the unmeasurable `f`, so the scalar is unity and the derivation is untouched. Group 03's escalation table is correct: 1.25 → Q2 ≈ 1410 (outside group 02's 1100–1400 band); 1.5 → Q2 ≈ 1620 and a strong player reaches the gate at ~1:55, below the GDD's 3-minute floor. |
| 11 | **Q9 = no decay satisfies C1** | **CLEARED, and the proof is falsifiable, which is better than an argument.** A decay of **0.76 pts/s** exactly zeroes a struggling player's meter income (0.35 combos/cycle ÷ 2.3 s cycle × 5 = 0.76/s), producing a hard dead end with the rival pinned at 1 HP and the loss condition still live. C1 is satisfied, and the implementation — *no variable at all, no `Tick`, no timer* — is the right shape because a float that exists acquires a default and the default becomes the design. |
| 12 | **Q26 = 7.0 s does not make the +20 row unreachable in 3–5 minutes** | **CLEARED.** Minimum spacing = 7.0 s cooldown + ~2.5 s event = 9.5 s; against ~200 s of competent combat that is ~21 theoretical and ~10 realistic bursts per duel (200/9.5 = 21.05 ✓). Group 06's retry model independently finds **two Impact chains available inside 15 s** at a 7 s cooldown. The +20 row is comfortably reachable. §14's stated risk — *"too long and the +20 gain becomes unreachable"* — does not materialise at 7.0 s. |
| 13 | **Q14 = 1.000 actually protects Q6 and Q7** | **CLEARED, and the protection is structural, not just numeric.** At play rate 1.0 the montage-time scalar is unity, so `ANS_IFrame` at 0.28 s and `ANS_PerfectDodge` at 0.12 s occupy exactly the wall-clock time authored. Group 05 adds six guards on top of the value: the rename to `CosmeticMontagePlayRate`, a four-montage allowlist, a single `PlayFighterMontage` call site, an `ensure()` on gameplay notify classes, Motion Warping for Q16 displacement so distance never travels through play rate, and an editor check on any bespoke Nova dodge. **The scoping caveat is correct and necessary**: the guard binds the **player kit only**, because the rival's `TelegraphScale`/`RecoverScale` legitimately use play rate — group 07's Q18 formula correspondingly divides by the *effective* play rate, and the two dispatches agree. |
| 14 | **Q15 = 600 uu/s vs the missing rival `MaxWalkSpeed` (item 49) and group 06's ~1030 uu/s ceiling** | **CLEARED as a bound, and item 49 staying OPEN is a PASS.** Group 04's lower bound: the rival's advance speed must be **≥ the player's 600 uu/s**, or Q22 makes the duel unendable by kiting. Group 06's upper bound: above **~1030 uu/s** (= 360 cm ÷ the 0.35 s Phase 2 reposition floor) a 1200 cm separation collapses from two reposition cycles to one and delivers the same 0.85 s that 1000 cm would. **The two bounds are consistent and define a real, non-empty window of roughly [600, 1030) uu/s.** No dispatch assigned a value; group 07 additionally fences off MOBILITY 6/10 from ever being used to derive one. **This is the set's best-handled open item.** Two residual notes in §5, items D and E. |

**Five further dependencies I checked that were not on the list:**

| # | Dependency | Result |
|---|---|---|
| 15 | **Q6 = 0.28 s vs Q25's Active windows** | **CLEARED.** 0.28 s fully covers a 0.18 s active window with ~0.05 s either side and covers 62 % of D's 0.45 s window (0.28/0.45 = 0.622 ✓, matching group 04's figure). Group 03's stated asymmetry — a dodge answers *a specific hit*, not a whole attack — survives Q25's authored values. Q25.6's derived constraint (B's first-to-last hit-notify span **≤ 0.26 s**, inside a 0.36 s Active window) is correctly derived from Q6 = 0.28 s and is the right relationship to enforce at editor time. |
| 16 | **Q5 = 3 sections (~1.0 s) vs Q25's punish windows** | **CLEARED, and independently reproduced.** Q25 gives 1.75–2.05 s (P1) and 1.29–1.53 s (P2), against group 02's midpoint estimates of ~1.73 s and ~1.28 s. Q25's windows are marginally **more** generous at every attack, so a 3-section combo fits everywhere and group 02's rejection of 4 sections (≈1.33 s, does not fit post-C or post-D in Phase 2) is confirmed from a second direction. |
| 17 | **Group 05's Q15 finding that approach + full combo does not fit Phase 2** | **CLEARED as consistent, not contradictory.** Group 05: 400 cm → contact at 600 uu/s is 0.42 s, plus a ~1.0 s combo = 1.42 s against a ~1.28 s window. Group 07: post-D Phase 2 is 1.29 s against ~1.00 s. Both are true — group 07 measures from *already in range*, group 05 from *mid-band*. The reading is the same in both: **in Phase 2 the player must already be in range when the window opens.** Surfaced honestly in both files. |
| 18 | **Q16 = 400 cm against Q10's bands** | **CLEARED.** A back-dodge from ~150 cm lands at 550 cm — outside A (260), C (420) and B (520), inside D alone. Two consecutive back-dodges from 200 cm reach 1000 cm, inside group 04's 840–2884 cm zero-coverage region, deliberately exercising the required-advance rule rather than an idle loop. Consistent with group 04's own band table. And Q16's 400 cm does **not** out-distance Q13's 600 cm — group 05 states the intent plainly: *"you cannot dodge your way out of the approach attack, only through it."* |
| 19 | **Group 03's reaction check against Q25's authored telegraphs** | **CLEARED, with margin gained.** Group 03 stress-tested Q7 against a 0.40 s Phase 2 telegraph (the GDD floor), where the perfect-press window [0.25, 0.37] opens at the ~250 ms average human reaction time. Q25's **shortest** authored telegraph anywhere is **0.48 s** (B, Phase 2), 0.08 s slower than the worst legal case. **No attack in either phase sits at the reaction-time cliff.** |

### CHECK 4 — No runtime AI-model calls, and no auto-success

**HOLDS, across all nine dispatches, and it was actively defended rather than merely
asserted.**

| Evidence | Where |
|---|---|
| Rival selection is authored filtering plus authored weighting — range **and** cooldown, then a weighted pick among survivors | group 04 Q12 semantics step 3, verbatim: *"Deterministic authored filtering and weighting — no learning, no adaptation, no model call"* |
| Every Q25 value is a static constant in a Data Table read by a Behavior Tree | group 07 constraint compliance |
| An **adaptive perfect-dodge window that widens after N failures** was considered, named as deferred future scope, and **not designed** | group 03 Q7, *"What this number must NOT become"* |
| A **performance-gated Impact Window** replacing the timer was named as the available swap and **not proposed** | group 03 Q26 (Batman: Arkham row) |
| **Beats that widen after failures** are listed under "Closed, and named so nobody reaches for them" | group 06, designer's-levers table |
| Group 09's park mechanism is a **Blackboard bool + a stock `Blackboard` decorator with `Observer Aborts = Lower Priority`** — no new engine surface, no logic that watches the player | group 09 V1 |
| **Final Fantasy XVI's unfailable cinematic clash is rejected by name** against the GDD's *"Failure does not auto-correct the input"* | group 06 Q20 prior-art table |
| A press that is **already held** when a beat opens must not pass it; bind on `Started` | group 06 Q17 developer note 2 — this is the concrete anti-auto-success mechanism, and it is correct |
| The Q20 "first Clash attempt at 0.75 s" idea is **widest-first and never widens again**, explicitly distinguished from forgiveness-on-retry, and **surfaced rather than proposed** | group 06 Q20 |
| Assignment #04's generative pipeline is offline authoring outside the game's scope lock; group 07 forbids MOBILITY 6/10 becoming a float while permitting it as #04 flavour; group 08 records that Sonniss's AI/ML-training prohibition binds #04, not the build; group 08 item 20 adds a critic-agent check | groups 05, 07, 08 |

**No auto-success confirmed.** `build-sequence.md` M3-07 already records the three onboarding
prohibitions verbatim, and nothing this session weakened them. Group 06 surfaces — without
settling — the one residual: **two 0.50 s beats can be brute-forced by mashing at 4 Hz**,
and failing on an early press would be the stricter rule but adds a punishment the GDD never
authored. **Correctly surfaced, correctly left open.**

### Milestone order — M5 not pulled into M1–M4

| Item | Placement | Verdict |
|---|---|---|
| Group 05 **item 43** (faceplate + indicator) | **M5-06 entirely.** Its only M1 note is a **prohibition**: *"Do not attempt any faceplate or indicator treatment before M5."* | **PASS** |
| Group 05 **item 44** (Ascension-responsive emissive) | **M5-06 entirely.** Two M1 notes: (1) cache the dynamic material instance `ApplyFighterProfile` already creates — a genuine leak fix that is correct regardless of item 44; (2) **bind nothing to `OnMeterChanged` for emissive purposes before M5.** Neither adds work. | **PASS** — this was the item most at risk and it held |
| Group 05 **item 45** ("SFN") | M5-08, shipping **blank** | **PASS** |
| Group 03's **Impact-readiness HUD indicator** | Functional gray-box state in **M3**, styled treatment explicitly **M5** | **PASS** — `design-brief.md` §11.6's asset-selection-vs-authored-work line supports this |
| Group 06's **Clash prompt visibility** | Functional in M3/M4, styled in M5 | **PASS** |
| Group 07 **Q29** | The *string* is M3-04; *typography, plate art and animation* are M5 and "must not be pulled forward" | **PASS** |
| Group 09 **V1–V5** | M3-07 / M3-08 and later; the two forward-looking M1/M2 notes are *"same amount of work at M1, a rewrite if deferred"* | **PASS** |
| Group 08 **Q30** (Paragon swap) | M1-23 asset selection, hard-gated **before** M2-04/M2-05 | **PASS** on milestone order — but see §5 item I for a `build-sequence.md` filing conflict |
| Group 08 **Q31** (6–9 cue audio floor) | **BORDERLINE — and group 08 contradicts itself inside one file.** Its "Where it lands" line reads *"Milestone: **M1–M4 for the floor** (asset selection), M5 for everything else"*, while its sequencing paragraph reads *"the floor is authored **after M4's gate is met**, not before."* Those are two different placements. `design/decisions.md` records the second. | **PASS only under the second reading.** Under the first reading, nine authored audio cues land inside M1–M4, which is presentation content in the milestones M5 is gated behind. `CLAUDE.md`'s "thin presentation floor after M4" allowance covers the second reading and not the first. **The designer must pick one wording.** |

---

## 5 — Contradictions between groups

Nine. Ordered by consequence.

### A — Group 07 authors Telegraph/Recover as **absolute seconds**; the brief and the build sequence implement them as a **scale factor**

- `design-brief.md` §13.1 rows 20–21 and 23–24 define the values as *"`ANS_Telegraph`
  length × `TelegraphScale`"* and *"`ANS_Recover` length × `RecoverScale`."*
  `build-sequence.md` M4-04 and group 05's scoping note both describe Phase 2 as **play-rate
  scaling** over the telegraph and recover montage sections.
- Group 07's Q25 authors `Phase1.TelegraphSeconds` / `Phase2.TelegraphSeconds` and
  `Phase1.RecoverSeconds` / `Phase2.RecoverSeconds` as **absolute durations**, and its
  summary table names those fields explicitly.
- **These are two different Data Table schemas for the same value.** Group 07 is aware —
  Q25.2 notes the ratios "realized as a near-uniform ~1.28× montage play rate" and Q18
  requires dividing by the *effective* play rate — but the field shape was never reconciled.
  Note also that the ratios are **not** uniform: telegraph P2/P1 is 0.786 / 0.800 / 0.775 /
  0.778, so a single `TelegraphScale` cannot express all four; four per-attack scales can.
- **Consequence:** M2-04 and M4-04 cannot both be built as written. Whoever fills
  `DT_VanguardAttacks` must be told which the field means. **Named, not resolved.**

### B — Group 07's Q25.11 tension is computed on a distance band group 04 proved physically unreachable

- Group 07: *"at 0–90 cm, where group 04's bands make **A the only legal attack**, that is A
  every ~3.0 s at 32 damage — **10.7 dmg/s against 100 HP**."*
- Group 04's own capsule arithmetic: Echo/Nova radius 40 cm + rival radius 60 cm →
  **"the minimum achievable `DistanceToTarget` is 100 cm. The fighters physically cannot be
  closer."** Group 04's band-coverage table marks 0–90 cm and 90–100 cm **"Physically
  unreachable"**, and marks the real contact zone **100–240 cm as depth 2** — A *and* B.
- **So the fight state group 07 describes cannot occur.** At the true minimum separation, A
  and B alternate. Recomputing with Q25's cycles: A (2.97 s) + B (2.86 s) = 5.83 s per pair,
  delivering 32 + 25 = 57 damage → **~9.8 dmg/s**, not 10.7, and not A-on-repeat.
- **What survives and what does not.** The *conclusion* survives — point-blank is lethal in
  roughly ten seconds if nothing is dodged, and the designer should choose that deliberately.
  The *arithmetic that justified it* does not, and the recommendation it produced
  (*"tune Q12's A cooldown and Q25's A cycle in one session"*) is aimed at a repeat-A
  scenario the geometry forbids.
- **On the 0.03 s slack itself:** it is real but is measured against group 04's own
  **no-repeat wall** (`Cooldown > full cycle`), which is stricter than the mechanism
  requires. A's cooldown is stamped in `BTTask_ReturnToNeutral`; the next `Select Attack`
  occurs after Reposition + Select = **1.05 s** in Phase 1. The true anti-repeat requirement
  is `Cooldown > 1.05 s`, and A at 3.0 s has ~1.95 s of margin. **The 0.03 s figure is
  margin against a self-imposed conservative rule, not against a real failure.** It is
  nonetheless the correct thing to watch, because if playtest lengthens A's states past
  3.0 s the *stated* wall is crossed and someone will read that as a defect.

### C — `design/decisions.md` and group 07 both write "Q45" where they mean **item 45**

- `design/decisions.md`, group 07 entry: *"Keeps **Q45's** build behaviour but breaks its
  silence."* Group 07 §Q29: *"the **Q45** precedent."*
- **There is no Q45.** `design-brief.md` §14 ends at **Q31**. The referent is **`TODO.md`
  item 45** ("SFN"), answered by group 05.
- **Consequence:** a future agent searching §14 for Q45 finds nothing, or worse, invents it.
  **A one-character defect with a real propagation cost. Named, not fixed.**

### D — Group 04's Q21 support table and whiff arithmetic assume a **500 cm/s** player; group 05 proposes **600 uu/s**

- Group 04 uses Unreal's default `MaxWalkSpeed` of 500 cm/s in two places: the Q21 timing
  table (columns 400 / 500 / 600) and the Q10 whiff note (*"at 500 cm/s the player covers
  50–100 cm during the 0.10–0.20 s Select state"* and *"crosses 80 cm in 0.16 s"*).
- **Under Q15 = 600 uu/s** those become **60–120 cm** and **0.133 s**. The A→B handoff
  overlap is 80 cm, so the player crosses it **20 % faster** than group 04's proof assumed,
  and the Select-state displacement now **exceeds** the overlap at the top of the range.
- Separately, group 04's Q21 table columns at **400 and 500 cm/s are illegal** under group
  04's own kiting constraint once Q15 = 600 (*"the rival's advance speed must be ≥ the
  player's `MaxWalkSpeed`"*).
- **Consequence:** whiffs at the band handoffs will be more frequent than proven. Group 04's
  own remedy already applies — *"if whiffs feel excessive, widen the overlaps before touching
  any timing value."* **Re-run the two figures at 600.**

### E — Group 06's Q21 arithmetic uses 600 uu/s as the rival's speed, which is the most favourable legal value

- Group 06 substitutes group 05's *player* speed as a placeholder for the *rival's*
  unspecified speed and derives the 1.20 s non-threat window from it. 600 uu/s is exactly the
  **lower bound** of the legal window established in CHECK 3 item 14 — i.e. the case most
  favourable to the separation.
- Group 06 states this plainly and supplies the sensitivity table, so it is disclosed rather
  than hidden. But the headline claim — *"the player gets a guaranteed ≈1.20 s"* — is
  **guaranteed only at the bottom of the rival's legal speed window**; at the top (~1030) it
  is 0.85 s, which group 06 itself calls *"too tight."*
- **Consequence:** Q21 = 1200 cm and item 49 must be decided together, exactly as both
  groups say. **Cleared as disclosed; named because the word "guaranteed" is doing more work
  than the arithmetic supports.**

### F — `build-sequence.md` M3-08's `RestoreCombatState()` still carries the two defects V2 and V5 correct, and `build-sequence.md` is **not on the architect's apply list**

- `build-sequence.md` M3-08 body: *"clear all transient tags (`State.Attacking`,
  `State.Invulnerable`, `State.PerfectWindow`, `State.InImpactWindow`, `State.Clashing`)"* —
  the **blind clear** V5 replaces with `ResyncTransientTags()`, and the one group 09 shows
  *"strips a player's i-frames mid-dodge"* on the Impact FAILURE branch.
- The same step body contains **no camera-return step**, which is V2's whole subject.
- Group 09's "what this does not unblock" section lists the sections of
  `combat-integration-plan.md` the architect must edit and explicitly records
  `build-sequence.md` as **unmodified** — but does **not** add it to the apply list.
- **Consequence:** after the architect applies V1–V5 to the plan, `build-sequence.md` M3-08
  will still instruct a developer to build the uncorrected function. **A real coverage gap
  in the correction's scope. Named, not fixed.**

### G — `build-sequence.md` M4-08 step 2 pushes the fighters **"along their axis"**; Q21 mandates the **arena long axis**

- `build-sequence.md` M4-08 step 2: *"`Set Actor Location` pushed apart along their axis."*
- Group 06 Q21 implementation correction 1: *"Push along the long axis, **not** 'the axis
  between them.'"* The reason given is concrete — a facing-relative push next to a long wall
  clamps to as little as ~700 cm and silently delivers a different separation every time.
- **Consequence:** the build sequence currently specifies the behaviour Q21 was written to
  correct. Same class of gap as item F.

### H — `build-sequence.md` M4-06 names no `AM_Clash_Beat2`

- M4-06 lists `AM_Clash_Beat1`, `AM_Clash_Finisher`, `AM_Vanguard_CounterReact`. Group 06 and
  `TODO.md` item 54 both refer to **`AM_Clash_Beat1` / `AM_Clash_Beat2`** montage lengths.
- Two beats with one beat montage is either an omission in the build sequence or an
  assumption in group 06. **Named; neither file is authoritative on it yet.**

### I — Group 08 pulls the Q30 Paragon swap to **M1-23**; `build-sequence.md` still files it under **M5-06**

- `build-sequence.md` M5-06 (a presentation-pass step) carries the sentence *"If a Paragon
  heavy hero replaces the Vanguard proxy, it must land BEFORE M4 range tuning."* A step
  filed under M5 that must execute before M4 is self-contradictory as written.
- Group 08 sharpens the deadline further — **before `M2-04`/`M2-05` are authored**, calendar
  backstop **2026-08-09** — and correctly files it as **M1-23 asset selection**.
- **Consequence:** group 08's placement is the right one and is consistent with milestone
  order. `build-sequence.md` Appendix A's milestone-order claim is muddied until M5-06's
  sentence is moved to M1-23. **Named, not fixed.**

### J — Two numbering spaces have collided at 58–61

- Group 05 proposes **new `design-brief.md` §13.2 rows 58, 59, 60, 61** (faceplate treatment;
  per-fighter Ascension emissive curve; the curve's tier thresholds; the "SFN" expansion).
- **`TODO.md` items 58, 59, 60, 61 already exist and mean entirely different things** —
  Starter Content verification (group 08), `CameraReturnBlendSeconds` and
  `OverlayStopBlendOutSeconds` (group 09), and the same-frame-death question (group 09).
- Group 05 says the designer assigns the row numbers, so nothing is wrong yet — but the two
  spaces now overlap exactly, in the same repository, in files a future agent reads together.
  **"Item 59" and "row 59" are one keystroke apart and mean unrelated things. Named.**

### K — `TODO.md` states that `design/decisions.md` "holds no entries"

- `TODO.md`, "Not yet triggered": *"As of 2026-08-02 `design/decisions.md` holds **no
  entries**, so nothing supersedes the GDD yet."*
- `design/decisions.md` holds **nine dated entries** for groups 01 through 09.
- The **conclusion** is still correct — nothing supersedes a GDD line, rule 4 has not fired,
  and the two supersessions on record are of `design-brief.md`, not the GDD. **The premise is
  stale and should not be left standing, because it is the sentence a future agent will read
  to decide whether the GDD is current.**

---

## 6 — Per-step verdict

**Omitted.** The coverage statement in §2 records that the build-step tracing job did not run
this pass: no build step was written or edited this session, and `build-sequence.md` is
unchanged.

---

## 7 — Gaps

**Design-brief decisions with no implementing answer — and every one of these is a PASS.**
The dispatches were asked to research, not to close, and an OPEN value is not a gap.

- **Still OPEN and correctly so:** item 26 (the "plasma-gauntlet" canon question, blocked on
  a human zooming PDF page 14 — the refusal to settle it from a self-disclaimed
  low-confidence transcription is the single best judgement call in the set); item 46
  (counter success window); item 47 (dodge-cancels-combo); item 48 (dodge montage length);
  item 49 (rival `MaxWalkSpeed`); items 50–53 (attack B travel cap, `SelectionWeight`, strafe
  and backpedal multipliers); items 54–57 (Clash montage lengths, counter recovery length,
  `IA_FinalClash`-during-Impact, the Q21 wall margin); items 59–62 (group 09's two blend
  values, the same-frame-death rule, the §7.5 process question); item 63 (apply V1–V5).
- **Values the dispatches deliberately did not invent, named here as evidence the discipline
  held:** the rival's capsule **radius** (group 07 refuses to derive it from page 10's
  *"roughly twice the shoulder width"*); the rival's **walk speed** (three dispatches
  bounded it, none assigned it, and group 07 explicitly fenced MOBILITY 6/10 off from ever
  being used as its source); **Nova's yellow-green indicator hue** (in the art, not in her
  printed four-swatch palette — routed around, left OPEN); **"SFN"** (four candidate
  expansions offered under a literal **"INVENTED. NO GDD BASIS. NOT CANON."** label);
  **`RivalDisplayName`** (recommended `VALOR-7`, **shipped blank**).

**Genuine gaps — things that need doing and are not on anyone's list:**

1. **`build-sequence.md` is not covered by group 09's correction scope** (§5 items F, G, H).
   Three of its steps — M3-08, M4-06, M4-08 — will still instruct a developer to build
   behaviour the session corrected. No `TODO.md` item exists for this.
2. **No item exists for reconciling the Telegraph/Recover field schema** (§5 item A).
   M2-04 and M4-04 cannot both be built as currently written.
3. **No item exists for restoring Q17 and Q18 to the designer's list** (Violations 1 and 2).
4. **No item exists for resolving C3** (Violation 3) — group 02's reinterpretation is
   recorded in `design/decisions.md` as if the constraint were met.

---

## 8 — Overall verdict

> **NO — not yet.** The forty-five answers hold against the **GDD**, the **SCOPE LOCK** and
> the **published ranges** — 26/26 Q25 values verified in range by independent
> recomputation, every fixed GDD number carried through unaltered, no range collapsed, no
> fifth attack or second arena or second move set, no per-fighter mechanical difference, no
> runtime model call and no auto-success anywhere. **But they do not yet hold against the
> project's own process rules or against each other:** two §14 questions the human designer
> owns (**Q17**, **Q18**) were closed by dispatches and deleted from `TODO.md`, the approved
> Q22's binding constraint **C3** is recorded as satisfied when it is not, and eleven
> cross-group contradictions remain live — the load-bearing ones being the Telegraph/Recover
> field-schema split, group 07's Q25.11 tension computed on a distance band group 04 proved
> unreachable, and `build-sequence.md` sitting outside the scope of the session's own
> corrections.

*Nothing above was repaired. Every value in this repository remains the human designer's to
approve, change, or reject.*
