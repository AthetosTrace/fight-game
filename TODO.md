# TODO — Ascendant Impact

**65 open items** — **8 closed · 35 PROPOSED · 1 blocked on you · 29 untouched.**
Last worked 2026-08-03.

> **INSPECTED 2026-08-03.** A cross-consistency pass over all nine dispatches
> (`design/inspection-design-answers.md`) found **3 process-authority violations and 11
> cross-group contradictions**, and **zero GDD violations**. Group 07's 26/26 in-range
> claim was independently recomputed and **CONFIRMED**. Items 6 and 29 were wrongly
> closed and are **restored below**. Items 64–72 are the contradictions.
> Twenty-eight new items (46–73) were found by the dispatches and the inspection: real gaps in
> `design-brief.md` §13.2 that have no row and no Q number. The list grew because the
> work found holes, which is the list working.

> **SETTLED AND BINDING — Q22 (approved 2026-08-02).** The 1 HP floor is **permanent**;
> `MinHealthFloor = 1` from `BeginPlay`, lowered to `0` only by `ClashSuccess()`.
> **The Final Clash is the only way to win the duel.** Three constraints follow and bind
> every answer below: **C1** Q9 must resolve to *no meter decay*; **C2** the HUD must
> show which gate is still locked once the health bar pins; **C3** Q2 must be tuned so
> ≤25% rival health and meter 100 arrive close together. See `design/decisions.md`.

## ⏳ PROPOSED — awaiting your approval

These items have a researched recommendation on disk and are **not closed**. Approve or
change them and they get deleted. Kept as an index here so the entries below stay in
build order rather than being rewritten every group.

| Items | Group | Answer file |
|---|---|---|
| 2 (Q1), 3 (Q2), 21 (Q3), 11 (Q4), 12 (Q5) | 02 — combat economy | `design/group-02-combat-economy.md` |
| 14 (Q6), **15 (Q7 · BLOCKING)**, 16 (Q8), 33 (Q26), 30 (Q27), 13 (Q28) | 03 — defensive timing | `design/group-03-defensive-timing.md` |
| 17 (Q24), 22 (Q10), 23 (Q12), 24 (Q13), 10 (Q11), 18 (mezzanine) | 04 — spacing and arena | `design/group-04-spacing-and-arena.md` |
| 7 (Q14), 8 (Q15), 9 (Q16), 43, 44, 45 | 05 — fighter feel and presentation | `design/group-05-fighter-feel.md` |
| 31 (Q9), 39 (Q19), 40 (Q20), 41 (Q21) | 06 — Final Clash and meter | `design/group-06-final-clash.md` |
| 25 (Q25), 5 (Q23), 32 (Q29), 27 | 07 — structure and canon | `design/group-07-structure-and-canon.md` |
| 19 (Q30), 42 (Q31) | 08 — asset decisions | `design/group-08-assets.md` |
| **6 (Q17), 29 (Q18)** — reopened by the inspection | 06 / 07 | see those group files |

## How this file works

- **Completed items are DELETED, not ticked.** This file only ever shows what is
  outstanding. If you want a record of what was decided, that goes in
  [`design/decisions.md`](design/decisions.md), not here.
- **PROPOSED is not closed.** A KIND B item that a designer dispatch has researched
  stays here, marked ⏳ PROPOSED, until the human designer approves or changes it. Only
  an approved item is deleted. KIND A items are APPROVED on delivery and deleted at once.
- **Item numbers are stable ids, not positions.** Deletions leave gaps. That is correct —
  a gap means something got finished.
- **⚠ TWO NUMBERING SPACES OVERLAP.** `TODO.md` **item** numbers and proposed new
  `design-brief.md` **§13.2 row** numbers both currently run through the high 50s and
  early 60s and mean unrelated things. Group 05 proposes §13.2 **rows** 58–61 (faceplate
  treatment, Ascension emissive curve, its thresholds, the "SFN" expansion); `TODO.md`
  **items** 58–61 are Starter Content, two blend values and the death-race question.
  **Always write "item N" or "§13.2 row N" — never a bare number.**
- **Ranked by build order, not by importance.** Every item names the lowest-numbered
  `build-sequence.md` step that first needs it. Work top-down and you will never be
  blocked by something further down this list.
- **Nothing here is decided by an agent.** Ranges are the design brief's suggestions,
  carried verbatim with the reason given. The human designer owns every one.

### The ranking rule

**Blocking step = the lowest-numbered step that first consumes the answer** — where a
real value, or a decided behavior, has to exist for that step's stated outcome to be
achieved.

Creating an exposed variable and leaving it blank is **not** blocked; `design-brief.md`
§13 explicitly tells the developer to do exactly that. So most scalar items can be
*built* at their blocking step but cannot be *signed off* there. Items whose **logic,
branch, or structure** changes with the answer are genuinely blocked, and they are
marked as such in the note.

### Tags

- **KIND A — engineering.** A documented procedure exists. Someone competent can go do
  it. Two items are marked KIND A by closest fit but are not Unreal procedures; each
  says so.
- **KIND B — design.** No correct answer, only better and worse. The designer decides.
- **BLOCKING** — changes *what the game is*, not how it is tuned. Two items carry this,
  both flagged by `design-brief.md` §14 itself.

### Coverage note

Every row in `design-brief.md` §13.2 that has no number maps to a Q number in §14 —
rows 29–57 are Q1–Q29 with no remainder. They are therefore listed once, under their Q
number, and not double-counted. §13.1 is fully specified by the GDD and contributes no
open items, with one exception now recorded below (row 28).

**The reverse is not true, and that is the interesting part.** Items **46–63** are values
the build needs that §13.2 has **no row for at all**. Items **64–73** are different — they
are cross-group contradictions and record defects found by the inspections, not missing
rows. The table is complete with
respect to itself and incomplete with respect to the game. Expect more of these as the
groups run.

---

## M1 — Combat gray box

### M1-01 — Confirm the base project

**1. Unreal MCP is not connected.** · **KIND A**
The developer implements in Unreal through an Unreal MCP server, and `CLAUDE.md` makes
connecting it a prerequisite *before the developer runs*. Nothing in this milestone —
or any milestone — can be executed in the editor until it is up. **This is the single
item blocking all 63 build steps.** Note the 28 July class guidance recorded in
`ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md`: use MCP for individual reviewed
steps, not to one-shot the game.

### M1-05 — Create `DA_TuningGlobals`

**2. Q1 — Player max health.** · **KIND B**
Range to consider: **100–200**. Both fighters must be identical (SHARED PLAYER-KIT
SCOPE RULE). Reason given: consider expressing the whole economy as "how many rival
hits kill me" — a 3–5-hit budget is a common readable target for an armored-boss duel.

**3. Q2 — Crimson Vanguard max health.** · **KIND B**
Range to consider: **800–2000**. Reason given: must be tuned against the 3–5 minute
session target and against the Phase 2 (50%) and Clash (25%) thresholds landing at
satisfying moments.

### M1-05 — the one most likely to break a build

**64. C3 from the approved Q22 is NOT satisfied.** · **KIND B** · **YOUR CALL**
C3 requires ≤25% rival health and meter 100 to arrive **close together**. At Q2 = 1200 they
are **90–135 s apart**. Group 02 said so and then passed itself against a substituted
criterion (meter-first ordering is safe). **A dispatch may not amend an approved
constraint's success criterion and then mark itself compliant against the amended one.**
Two paths: amend C3 explicitly on the record, or take group 06's **Q2 → 1050–1100**.

### M1-09 — Create `BP_DuelDirector`

**5. Q23 — Is there a duel timer?** · **KIND B**
**Recommend none.** Reason given: the GDD lists only one loss condition (player health
zero) and gives 3–5 minutes as a *target session*, not a timer.

### M1-10 — Create the Enhanced Input assets

**6. Q17 — Do the Clash beats reuse `IA_Impact`?** · **KIND B** ·
**⏳ PROPOSED — reopened 2026-08-03**
Reopened by the inspection: group 06 closed this as KIND A, but `design-brief.md` §14 reads
*"Recommend yes, for learned consistency. **Designer confirms.**"* — the brief reserves the
confirmation to you. The recommendation stands: reuse `IA_Impact`, one action, one
`IMC_Duel`, routed by a `bClashBeatOpen` bool. See `design/group-06-final-clash.md`.
*Genuinely blocked:* `IMC_Duel` needs a second binding if the answer is no.

### M1-12 — Create `DA_FighterProfile` + Echo and Nova instances

**7. Q14 — Echo / Nova montage play-rate ("timing flavor").** · **KIND B**
**8. Q15 — Echo / Nova `MaxWalkSpeed`.** · **KIND B**
**9. Q16 — Echo / Nova dodge distance.** · **KIND B**
No ranges. These three scalars are the **entire** mechanical expression of Echo's
"deliberate spacing" versus Nova's "fast lateral rhythm, forward intent" in Phase 1.
The GDD says to *"approve only presentation-level timing flavor at first."* The brief's
question: **should they differ at all in Phase 1, or be identical until the base duel
is stable?** Identical is the more conservative reading and the cheaper build.
*New evidence, 2026-08-02:* the recovered character sheets show the differentiation
budget is already heavily spent on presentation — Nova has a 4-swatch palette to Echo's
3, layered jacket vs one-piece suit, thigh pouches, high-tops, a lettered insignia.
They read as different people before a single scalar moves. See
`gdd/reference/OPEN-QUESTION-IMPACT.md` §3.

### M1-12 — additional gap found 2026-08-02

**49. Crimson Vanguard's `MaxWalkSpeed` has no row and no Q number.** · **KIND B** ·
**Potentially BLOCKING — flagged for your attention**
Found by the group 04 dispatch. §13.2 row 43 covers the *player's* walk speed (Q15);
nothing covers the rival's. With a 2400 cm long axis and **Q22 making the Final Clash
the only way to win**, a rival slower than the player **can be kited forever and the duel
cannot end.** The dispatch refused to assign a value. It also blocks Q21's separation
arithmetic, which needs a closing speed.

### M2-04 — additional gaps found 2026-08-02

**50. Attack B needs a `MaxTravelDistance`; §13.2 row 41 names only D.** · **KIND B**
Found by the group 04 dispatch. B advances ~270 cm at its outer edge. Uncapped, it is a
second gap closer, which changes the four-attack spacing shape. No number proposed.

**51. `SelectionWeight` has no row and no Q number.** · **KIND B**
Found by the group 04 dispatch. GDD §04 requires Phase 2 to shift attack weighting toward
"more aggressive close-range and gap-closing selection", but there is no field to shift.

### M1-16 — additional gaps found 2026-08-02

Found by the group 05 dispatch while answering Q15. §13.2 row 43 covers free-movement
walk speed only; a lock-on system that strafes at full run speed feels wrong regardless
of what Q15 resolves to.

**52. Locked-on strafe speed multiplier has no row and no Q number.** · **KIND B**
Group 05 used 0.70× (420 uu/s) as a working value and flagged it as a gap rather than
smuggling it in as an answer.

**53. Locked-on backpedal multiplier has no row and no Q number.** · **KIND B**
Group 05 used 0.60× (360 uu/s), same caveat.

### M1-16 — Create `BP_LockOnComponent`

**10. Q11 — Lock-on max range, break range, camera interp speed.** · **KIND B**
No ranges given.

### M1-17 — Author `AM_Player_LightCombo`

**11. Q4 — Player light-hit damage, and whether the finisher hits harder.** · **KIND B**
No numbers.

**12. Q5 — Light combo length (number of sections).** · **KIND B**
GDD says "light attack sequence" without a count. **3 hits** is the common readable
default; **4** allows a heavier finisher. *Genuinely blocked:* you cannot author a
montage's sections without knowing how many there are.

### M1-18 — Create the player combat notify states / notify

**13. Q28 — `ANS_ComboLink` input-buffer window.** · **KIND B**
Range to consider: **0.15–0.30 s** before each section ends.

### M1-19 — Author `AM_Player_Dodge` with nested i-frame notifies

**14. Q6 — Dodge i-frame window.** · **KIND B**
Range to consider: **0.20–0.35 s**, starting near the beginning of the dodge montage.

**15. Q7 — Perfect-dodge sub-window.** · **KIND B** · **BLOCKING**
Range to consider: **0.08–0.15 s**. Must be strictly narrower than Q6. §14:
**"This single number does more to define the game's difficulty than any other in the
table."** It should be the first thing tuned in playtest and the first thing revisited
after any Phase 2 pass.

### M1-19 — additional gaps found 2026-08-02

Found by the group 03 dispatch: `design-brief.md` §13.2 has **no row and no Q number**
for any of these three. They are real holes in the provisional-values table, not
oversights in this file. Ranges were offered for conversation; **no values proposed.**

**47. Does a dodge cancel `AM_Player_LightCombo`?** · **KIND B**
Decides whether Q28's 0.25 s buffer is a kindness or a Phase 2 trap — a buffered combo
input that cannot be dodge-cancelled locks the player into a string during the ~1.28 s
Phase 2 window.

**48. Total length of `AM_Player_Dodge`.** · **KIND B**
`ANS_IFrame` (Q6, 0.28 s) and `ANS_PerfectDodge` (Q7, 0.12 s) are both authored *inside*
this montage. Its length is unspecified, so the windows have no container.

### M1-20 — Wire the counter input and player counter montages

**46. The counter's own success window has no row and no Q number.** · **KIND B**
Q7 covers the perfect *dodge*. **Nothing covers the perfect *counter*.** `ANS_CounterWindow`
exists in the rival's montage spec, but the player-side success window it is judged
against is unspecified. Found by the group 03 dispatch.

**16. Q8 — Whiffed-counter recovery.** · **KIND B**
Range to consider: **0.40–0.70 s**. Reason given: must be long enough that spamming
counter is worse than reading the telegraph.

### M1-21 — Gray-box `L_ShatteredRing`

**17. Q24 — Arena playable footprint.** · **KIND B**
No number. Reason given: must comfortably fit Q13's travel and Q21's Clash separation.
*Genuinely blocked:* you cannot gray-box a floor without dimensions.
*New evidence, 2026-08-02:* the recovered arena sheet carries **no dimensions, no scale
bar, and no human figure** — it cannot supply the number. It does fix the shape:
broadly **rectangular** with chamfered corners, one flat floor, **zero obstacles**, no
hazards, one doorway on the far short wall, orange railings marking the perimeter.
Because the hall is rectangular, **any downstream "arena radius" assumption is wrong.**

**18. Is the arena mezzanine reachable, or set dressing?** · **KIND B**
Raised by the recovered arena sheet. It shows a full upper tier ringing the floor with
**no visible route into the play space**. If it is decoration, the collision boundary is
simply the walls and no blocking volume is needed for it. Confirm before building one.

### M1-23 — Stand up the dressed proxies

**19. Q30 — Paragon heavy hero for Crimson Vanguard: yes or no, and by when?** · **KIND B**
Reason given (§12.4): if yes, it must land **before** M4 range tuning, or every range
value in Q10 gets re-tuned twice.
*New evidence, 2026-08-02:* page 14 now gives a concrete silhouette to judge candidates
against — mech proportion, small head relative to torso, oversized rounded pauldrons,
back vanes, fully enclosed fists.

---

### M1-23 — additional gap found 2026-08-02

**58. Verify whether UE Starter Content still ships in 5.8.** · **KIND A**
Found by the group 08 dispatch, **MEDIUM confidence**: search results indicate Starter
Content was **removed from the engine in 5.7**, and `design-brief.md` §12.1 and §12.6 both
lean on it — for basic materials and as the audio fallback. The source is community-grade,
not Epic documentation. **Clearing this is five minutes: tick Starter Content on a new 5.8
project and see.** The group 08 asset ledger routes around it either way.

---

## M2 — Rival state loop

### M2-04 — Create `DT_VanguardAttacks` with all four rows

**21. Q3 — Damage per rival attack A–D.** · **KIND B**
No numbers. Reason given: should differentiate the attacks — A (committed close force)
heaviest, D (approach) lightest. Suggest expressing each as a **percentage of player
max health** so Q1 can move independently.

**22. Q10 — Attack A–D range bands (cm).** · **KIND B**
No numbers. Reason given: bands should overlap enough that at least one attack is
always valid at combat distance, or `BTTask_Idle_Reposition` will loop repositioning.
**A likely early bug source — worth tuning together with Q24.**

**23. Q12 — Per-attack cooldown.** · **KIND B**
No numbers.

**24. Q13 — Attack D max travel.** · **KIND B**
The GDD's hard rule is *"no hidden full-arena snap."* Suggest expressing it as a
fraction of the arena footprint (Q24) so the two cannot drift apart.

**25. Q25 — Per-attack values inside each GDD state range.** · **KIND B**
Four attacks × two phases × four scaled states. The designer fills these in the Data
Table. The **range-validation check** the developer builds against them (§13.1) is
KIND A and can proceed without the values.

**26. "Plasma-gauntlet weapons" may contradict Attack A.** · **KIND B** ·
**⛔ BLOCKED ON YOU — four specific questions in `design/group-07-structure-and-canon.md`**
The group 07 dispatch correctly refused to settle a canon contradiction from a
low-confidence transcription. **Clearing this means zooming GDD page 14 by eye and
confirming the wording.** M2-04 is not blocked meanwhile.
Raised by page 14. Its UNITS DESCRIPTION panel reads *"powerful, integrated
plasma-gauntlet weapons"*, while GDD §04 describes Attack A only as **"Close-range
committed gauntlet force"** and the sheet's own gauntlet panel shows an enclosed fist
with **no emitter, barrel, or muzzle**. **Step one is not a design decision — it is
confirming the wording against the PDF by eye**, because that panel is low-contrast and
the transcription is explicitly low-confidence. Only if it reads as transcribed is there
a canon question.

**27. Page 14's SYSTEM STATS map to no system.** · **KIND B**
POWER 9/10, ARMOR 9/10, **MOBILITY 6/10**, SYSTEMS 7/10 appear on the rival sheet and
are consumed by nothing in the GDD, `design-brief.md`, or `combat-integration-plan.md`.
Probably concept-art flavour — but they are numbers in the source of truth and a future
agent will find them. Decide whether they are non-canonical and record it.
**MOBILITY 6/10 is not a movement-speed value.**

### M2-12 — Create the six `BTTask_*` tasks

**29. Q18 — BTTask montage failsafe margin.** · **KIND B** ·
**⏳ PROPOSED — reopened 2026-08-03**
Reopened by the inspection: group 07 closed this as KIND A, but its own justification —
*"any value in 0.25–0.50 works; 0.35 is the middle with a documented reason"* — describes a
designer choice. The value breaks no range; the authority was wrong. Recommendation stands:
**0.35 s**, expressed as `MontageLength / EffectivePlayRate + 0.35` — **the division by
effective play rate is not optional**, or it fires early on every Phase 2 telegraph.

### M2-13 — Author Attack A montage and its notify states

**30. Q27 — `ANS_Recover` incoming-damage multiplier.** · **KIND B**
**1.0** (no bonus, the opening is just time) up to **~1.5**. Designer decides whether
"punish opening" means extra damage or only safe access.

---

## M3 — Impact handoff

> **`cinematic-integration-inspection.md` returned APPROVED WITH REQUIRED CHANGES.**
> Nine of ten hard checks pass. **Hard check 7 — cinematic handoff safety — does not.**
> Several restoration steps are *assumed rather than specified*, and one ownership
> transition has no documented mechanism at all. These are specification defects in
> `combat-integration-plan.md`, not foundation defects. **All five must be corrected
> before M3 is implemented. None of them block the sandbox test, M1, or M2.**

### M3-03 — Create `BP_AscensionComponent`

**31. Q9 — Does the Ascension Meter decay?** · **KIND B**
**Recommend no decay.** Reason given: consistent with "earned only through active
combat decisions", and it adds no timer pressure the GDD asks for.

### M3-04 — Create `WBP_HUD`

**32. Q29 — Crimson Vanguard's short in-combat UI label.** · **KIND B**
The GDD explicitly lists this as unfinalized. Formal name is "Crimson Vanguard /
Project Valor-7"; the HUD needs something shorter. The developer exposes it as a `Text`
variable and **leaves it blank rather than inventing one.**
*Checked 2026-08-02:* page 14 offers only the formal title treatment. **No short form
exists anywhere in the GDD.**

### M3-07 — Create `BP_ImpactWindowDirector`

**33. Q26 — Standard Impact Window cooldown.** · **KIND B**
Range to consider: **3–8 s**. Reason given: too short and the cinematic bursts stop
feeling earned; too long and the +20 gain becomes unreachable inside a 3–5 minute duel.

**63. Apply the five corrections to `combat-integration-plan.md`.** · **KIND A**
V1–V5 are written and APPROVED as drop-in specification text in
`design/group-09-cinematic-corrections.md`. **The `combat-integration-architect` must
apply them** — the designer dispatch deliberately did not edit the architect's artifact.
**This is what actually clears hard check 7 and unlocks M3 sign-off. M1 and M2 may proceed
now regardless.** The architect must also choose between `BPI_CombatWindows` and the
two-explicit-calls fallback.

**59. `CameraReturnBlendSeconds` — no value chosen.** · **KIND B**
Proposed band **0.15–0.40 s**, 0.0 legal. Introduced by V2's camera-restore step.

**60. `OverlayStopBlendOutSeconds` — no value chosen.** · **KIND B**
Proposed band **0.0–0.15 s**. Introduced by V4's targeted `Montage Stop`.

**61. Should a same-frame death that races an earned `IA_Impact` press still show the
burst before the Loss screen?** · **KIND B**
V4 part 4, deliberately left open. The dispatch recommends aborting immediately but did
not settle it.

**62. Is `design-brief.md` §7.5 amended in place, or annotated as superseded?** · **KIND A**
V2's omission exists upstream in the design brief's pseudocode too. The inspector required
that it be **surfaced, not silently edited** — so the process question is yours.

## M4 — Complete duel

### M4-05 — Create `BP_FinalClashDirector` and the double gate

**39. Q19 — Post-counter Clash-initiation window.** · **KIND B**
Range to consider: **0.5–1.5 s**. The GDD permits initiation "during neutral or after a
successful counter" — how long "after" lasts is unspecified.

### M4-06 — The two timing beats + `LS_FinalClash`

**40. Q20 — Clash beat 1 and beat 2 response times.** · **KIND B**
Not in the GDD. The brief's question: **reuse `StandardWindowDuration` (0.35–0.50 s) for
both, or author them separately — perhaps beat 2 tighter than beat 1 to make the finish
feel like a real test?**

### M4-08 — Clash FAILURE → the exact seven-step recovery

**41. Q21 — Failed-Clash separation distance.** · **KIND B**
No number. Reason given: must place both fighters outside every attack's `MinRange`
(Q10) so the player is not immediately re-engaged while recovering.

---

### M4-05 / M4-06 / M4-08 — additional gaps found 2026-08-02

Found by the group 06 dispatch. Each is a value the M4 build needs that has no GDD
number, no §13.2 row and no Q number.

**54. `AM_Clash_Beat1` / `AM_Clash_Beat2` montage lengths and prompt lead-in.** · **KIND B**
A 0.50 s window with no wind-up is a different mechanic from a 0.50 s window with one.
Only the GDD's 1–3 s burst constrains it.

**55. The successful-counter recovery length.** · **KIND B**
Q19 is expressed as `CounterRecoveryLength + 0.6 s` and cannot be locked without it.
Distinct from item 46, which is the counter's *success* window; this is the recovery
*after* success.

**56. What happens if `IA_FinalClash` is pressed while an Impact Window prompt is open.** · **KIND B**
Both can be live at once after a counter. Proposed rule, surfaced not decided: the Impact
Window resolves first and the post-counter Clash window is **paused, not consumed**.

**57. The wall margin for the Q21 clamp.** · **KIND A**
How close to the arena edge a fighter may be placed. Engineering-adjacent, but it changes
the effective separation near the ends of the long axis.

---

## M5 — Presentation pass (Phase 2)

### M5-04 — Fill `RequestSound`

**73. Group 08's Q31 states two different milestone placements for the cue floor.** · **KIND B**
Raised in the pass-1 inspection, logged late, and **restated 2026-08-03 because the first
wording was wrong.** The conflict is internal to `design/group-08-assets.md`: §Q31 says
*"Milestone: M1–M4 for the floor (asset selection), M5 for everything else"* (L194–195) but
later says the cues are *"authored after M4's gate is met"* (L302–305). **Both can be legal
— `CLAUDE.md` permits a thin presentation floor after M4 *inside* Phase 1 — so this is not
an M5-interleaving violation. It is an ambiguity about which side of the asset-selection /
authoring line the cues fall on**, and that decides whether they ship on 1 September.

**42. Q31 — Is a silent Phase 1 build acceptable?** · **KIND B**
No free sound source was verified (§12.6). Reason given: shipping silent on 1 September
and doing all audio in Phase 2 is the schedule-safe answer, **but the designer should
say so explicitly rather than discover it.**

### M5-06 — Final character treatment

**43. Is Echo's faceplate a visor or a light?** · **KIND B**
Raised by page 12, whose own callout reads **"Visor or Light"** and does not choose.
This is not an art detail — an emissive faceplate is a readability channel during
telegraphs and Impact Windows. Nova's sheet separately labels a "Light", so the two
fighters may not currently be consistent.

**44. Are Echo's "Integrated Energy Lines" emissive at runtime?** · **KIND B**
Raised by page 12. They are drawn flat with no glow. Whether they light up — and
whether they respond to the Ascension Meter — is unstated, and would be a cheap, strong
readability win if they do.

### M5-08 — The editorial character-selection interface

**45. What does "SFN" stand for?** · **KIND B**
Raised by page 13's **"Unique 'SFN' Unit Insignia"** — the only readable lettering on
either fighter's sheet. The GDD never expands it. If UI, announcer, or selection-screen
strings ever need a unit name, this is the thread to pull.

---

---

## Found by the cross-consistency inspection, 2026-08-03

Full detail in [`design/inspection-design-answers.md`](design/inspection-design-answers.md).

### M2-04 — the one most likely to break a build

**65. Telegraph and Recover are specified two incompatible ways.** · **KIND B** ·
**Blocks M2-04 and M4-04 from both being built as written**
Group 07 authors them as **absolute seconds** (`Phase1.TelegraphSeconds`);
`design-brief.md` §13.1 rows 20–21 and `build-sequence.md` M4-04 implement them as a
**scale factor** (`ANS_Telegraph` length × `TelegraphScale`). Worse: group 07's four P2/P1
ratios are **0.786 / 0.800 / 0.775 / 0.778 — not uniform**, so a single `TelegraphScale`
cannot express them. Either the data model moves to per-attack absolute seconds, or Q25 is
re-authored as scales.

**66. Q25's Attack A tension was computed on an unreachable distance band.** · **KIND B**
Group 07's 2.97 s-vs-3.0 s finding rests on the 0–90 cm band, which group 04's own capsule
arithmetic (40 + 60 = 100 cm minimum separation) marks **physically unreachable**. The
tension may be smaller than reported, or absent. Recompute before acting on it.

### M1-12 / M4-08 — the rival speed knot

**67. Groups 04, 05 and 06 assume three different player/rival speeds.** · **KIND B**
Group 04's Q21 support table and whiff arithmetic assume a **500 cm/s** player; group 05
proposes **600 uu/s**. Group 06's Q21 arithmetic uses **600 uu/s as the rival's speed** —
the most favourable legal value. All three interact with open **item 49** (the rival's
`MaxWalkSpeed`, which has no row at all). **Items 49, 67 and Q21 must be tuned in one
session.**

### M3-08 / M4-06 / M4-08 — `build-sequence.md` is stale

**68. `build-sequence.md` M3-08 still carries the two defects V2 and V5 correct.** · **KIND A**
And `build-sequence.md` is **not on the architect's apply list** for item 63. Whoever
applies V1–V5 must update the build sequence too, or the developer builds the old spec.

**69. `build-sequence.md` M4-08 step 2 pushes the fighters "along their axis".** · **KIND A**
Q21 mandates the **arena long axis**. One of the two is wrong.

**70. `build-sequence.md` M4-06 names no `AM_Clash_Beat2`.** · **KIND A**
Q20 specifies two beats at 0.50 s each; the build step names only one montage.

**71. Group 08 pulls the Q30 Paragon swap to M1-23; `build-sequence.md` files it under M5-06.** · **KIND A**
Asset selection at M1-23 is legitimate under the dressed-proxies rule. The build sequence
has not caught up.

### Not blocking anything — record only

**72. Q20's tuning band and Q19's ceiling both need a recompute.** · **KIND B**
**Q20:** its band is **0.45–0.60 s** while its justification claims it reuses the GDD's
**0.35–0.50 s** Standard range — the top half sits outside the range it rests on.
**Q19:** its "hard ceiling 1.30 s" was computed from GDD Phase 2 *floors*; under Q25's
authored values the real floor is **1.77 s**, so the ceiling is over-tight and §14's
rejected **1.5 s would in fact be safe**.


## Not yet triggered

**The GDD-out-of-date item is armed but has not fired.** The rule in
[`design/decisions.md`](design/decisions.md) says that the moment a recorded decision
**supersedes a GDD line**, an item gets added here stating the GDD is out of date and
that clearing it means Adrian updates the source PDF, re-exports and re-extracts.

As of 2026-08-03 `design/decisions.md` holds **nine dated entries** plus a corrections
note. **None of them supersedes a GDD line** — the two supersessions on record are of
`design-brief.md` (§13.1 row 28's missing cm figure, and §12.6's "no free sound source
verified"), not of the GDD. So rule 4 has still not fired. Item 28 (the 208 cm height) supersedes a **`design-brief.md`** line, not a GDD
line — the GDD had the value all along. **Do not add the GDD-out-of-date item for it.**
