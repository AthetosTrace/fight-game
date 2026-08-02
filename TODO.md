# TODO — Ascendant Impact

**50 open items** — **1 closed · 17 PROPOSED · 33 untouched.** Last worked 2026-08-02.
> Six new items so far (46–51) were found by the dispatches themselves: real gaps in
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

## How this file works

- **Completed items are DELETED, not ticked.** This file only ever shows what is
  outstanding. If you want a record of what was decided, that goes in
  [`design/decisions.md`](design/decisions.md), not here.
- **PROPOSED is not closed.** A KIND B item that a designer dispatch has researched
  stays here, marked ⏳ PROPOSED, until the human designer approves or changes it. Only
  an approved item is deleted. KIND A items are APPROVED on delivery and deleted at once.
- **Item numbers are stable ids, not positions.** Deletions leave gaps. That is correct —
  a gap means something got finished.
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

**The reverse is not true, and that is the interesting part.** Items 46–51 are
values the build needs that §13.2 has **no row for at all**. The table is complete with
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

### M1-09 — Create `BP_DuelDirector`

**5. Q23 — Is there a duel timer?** · **KIND B**
**Recommend none.** Reason given: the GDD lists only one loss condition (player health
zero) and gives 3–5 minutes as a *target session*, not a timer.

### M1-10 — Create the Enhanced Input assets

**6. Q17 — Do the Clash beats reuse `IA_Impact`?** · **KIND A**
**Recommend yes, for learned consistency.** Designer confirms. *Genuinely blocked:*
`IMC_Duel` needs a second binding if the answer is no.

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

**20. Footwear branding on both fighter sheets is a rights-review item.** · **KIND A**
*(Closest fit — this is a rights check, not an Unreal procedure.)* Raised by the
recovered character sheets: Echo and Nova both wear athletic sneakers carrying a
swoosh-style side mark. `CLAUDE.md` requires rights review for anything entering a
submitted course build. Applies to proxies now and to final character treatment at
M5-06.

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

**26. "Plasma-gauntlet weapons" may contradict Attack A.** · **KIND B**
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

### M2-05 — Create `BP_CrimsonVanguard`

**28. Record Crimson Vanguard's height in centimetres — 208 cm.** · **KIND A**
`design-brief.md` §13.1 row 28 lists **6'10" with no cm figure**, while rows 26 and 27
give Echo 183 cm and Nova 173 cm. The blank was never a design decision — the number was
simply unreadable until page 10 was recovered on 2026-08-02, where it is printed as
**"6'10" (208 cm)"**. This is a transcription from the GDD, not an invention. Needs the
designer's acceptance, then a dated entry in `design/decisions.md`.
**This supersedes a `design-brief.md` line, not a GDD line** — so it does *not* trip the
GDD-out-of-date rule.

### M2-12 — Create the six `BTTask_*` tasks

**29. Q18 — BTTask montage failsafe margin.** · **KIND A**
Range to consider: **0.25–0.50 s** past montage length. Reason given: an engineering
safety value, not a feel value.

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

**34. V1 — Rival AI ownership during the Impact burst is assumed, not specified.** · **KIND A**
The only documented mechanism that parks `BT_CrimsonVanguard` is the `bInClash`
Blackboard bool → `BTTask_WaitIndefinite` branch, which is **Clash-only**. Nothing
suspends the six-state Attack Cycle during the 1–3 s Impact burst. As specified,
`BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst, fight the stagger montage
for the montage slot, and either desync the debug state display or strand the burst.
**Acceptance:** `combat-integration-plan.md` names an explicit rival-ownership mechanism
for the burst (a park flag analogous to `bInClash`, or a documented can't-attack-state
rule), states what is suspended when a window opens — including "nothing", if that is
the decision — routes its release through `RestoreCombatState()`, and adds the
mechanism to the M3-GATE checklist.

**35. V4 — Animation-state cleanup and the death-during-burst edge are unspecified.** · **KIND A**
Animation cleanup is specified only on Clash failure; **mid-overlay player death is
undefined**. **Acceptance:** each overlay branch states its montage-cleanup rule
(natural completion vs explicit stop), and a single stated rule resolves `OnDeath`
during any overlay. *The `OnDeath` rule may need a design decision — surface it rather
than settling it.*

### M3-08 — Write `RestoreCombatState()` once

**36. V2 — Camera ownership is not restored by the single restore function.** · **KIND A**
The specified body restores input, collision, locomotion, tags, lock-on, time dilation,
rival BT and the prompt widget — **it contains no camera-return step** — yet plan §2
principle 4 and the §10 checklist both claim it restores camera. The claim overstates
the spec. **Acceptance:** an explicit camera-ownership restoration step (e.g.
`Set View Target with Blend` back to the player's spring-arm camera) is added inside the
single restore function so every branch inherits it, and the §2/§10 claims are aligned
to match the spec exactly. *Upstream note: `design-brief.md` §7.5 has the same omission
— surface to the designer, do not silently edit.*

**37. V3 — Hitbox/trace shutdown on restoration is assumed engine behavior.** · **KIND A**
Trace termination relies on notify-end firing when a montage is stopped.
**Acceptance:** either an explicit trace-termination / hit-set-clear step in restore, or
the assumption is named, tested in the sandbox or an M2 case, and added to the M3-GATE
checklist as "no trace survives a handoff".

**38. V5 — Two transient tags are omitted from the restore clear list.** · **KIND A**
`State.Dodging` and `State.CanCounter` are registered transient tags absent from the
clear list. `State.CanCounter` clearing relies on the same assumed notify-end behavior
as V3 — **a stale `State.CanCounter` after a handoff yields a free counter, i.e.
unearned spectacle**, which is precisely what the central promise forbids.
**Acceptance:** both are added to the clear list, or a per-tag guarantee-of-clearance is
documented.

> The single-restore-function design is exactly right, which is why these omissions
> matter: **one spec fix repairs every branch at once.**

---

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

## M5 — Presentation pass (Phase 2)

### M5-04 — Fill `RequestSound`

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

## Not yet triggered

**The GDD-out-of-date item is armed but has not fired.** The rule in
[`design/decisions.md`](design/decisions.md) says that the moment a recorded decision
**supersedes a GDD line**, an item gets added here stating the GDD is out of date and
that clearing it means Adrian updates the source PDF, re-exports and re-extracts.

As of 2026-08-02 `design/decisions.md` holds **no entries**, so nothing supersedes the
GDD yet. Item 28 (the 208 cm height) supersedes a **`design-brief.md`** line, not a GDD
line — the GDD had the value all along. **Do not add the GDD-out-of-date item for it.**
