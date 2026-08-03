# Design decisions — the record

This file holds **one rule** and the log it governs. It is the permanent record of what
was decided; [`TODO.md`](../TODO.md) is the impermanent record of what is still open.
An item that gets answered is **deleted** from `TODO.md` and **appears here**.

---

## The rule

**1. The PDF is the source of truth.**
`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` (v0.4, 2026-07-24) outranks
every other document in this repository — this file, `project-brief.md`,
`design-brief.md`, `combat-integration-plan.md`, the assignment-04 knowledge base, and
anything said in a session. If any of them disagrees with the PDF, the PDF wins.

**2. `gdd/` is generated and is never hand-edited.**
`gdd/sections/`, `gdd/reference/`, `gdd/INDEX.md`, and
`gdd/ascendant-impact-gdd-v0.4.md` are all mechanically derived from the PDF. Editing
any of them by hand silently forks the source of truth and there is no way to detect it
afterwards. **To change what `gdd/` says, change the PDF and re-export.** If a
description in `gdd/reference/` is wrong, fix the description by re-reading the image —
never by writing in what you believe the art should show.

**3. Every answer recorded here gets a dated entry** naming:
- **what it resolves** — the `TODO.md` item number and its Q / V id, so the deletion
  from `TODO.md` is traceable;
- **the decision**, stated plainly enough to implement from;
- **who decided it and when**;
- **any GDD line it supersedes** — quoted, with its `gdd/sections/` file and PDF page.

**4. The moment an entry supersedes a GDD line, `TODO.md` gains an item** stating that
the GDD is out of date. **Clearing that item means Adrian updates the source PDF,
re-exports it, and re-extracts `gdd/`** — not editing `gdd/` and not leaving the two
out of step. Until the PDF is updated, the GDD remains the source of truth *and* is
known-stale, which is the worst state to be in silently and an acceptable state to be
in visibly.

**Superseding the GDD is a real act.** Most decisions will not do it. A decision that
merely fills a value the GDD never specified — which is what most of `TODO.md` is —
supersedes nothing. A decision that contradicts something the GDD actually says does,
and triggers rule 4.

---

## Status values

- **APPROVED** — a KIND A engineering item. A documented procedure exists and there was
  nothing to decide. It is settled and its `TODO.md` entry is deleted.
- **PROPOSED** — a KIND B design item. A designer dispatch researched it and recommends
  an answer. **It is not decided.** Its `TODO.md` entry stays open, marked PROPOSED,
  until the human designer approves or changes it. Only then is it deleted.

**Nothing supersedes the GDD yet, so rule 4 has not fired.**

## Corrections — 2026-08-03

The cross-consistency inspection (`design/inspection-design-answers.md`) found three
process-authority violations. **It found no violation of the GDD itself.** Corrected here.

### 1. Q18 was wrongly marked APPROVED — reopened as PROPOSED

Group 07 closed Q18 at 0.35 s as a KIND A engineering item. Its own justification —
*"any value in 0.25–0.50 works; 0.35 is the middle with a documented reason"* — describes a
**designer choice**, not a documented procedure with nothing to decide. The value breaks no
range. **The authority was wrong, not the number.** `TODO.md` item 29 restored.

### 2. Q17 was wrongly marked APPROVED — reopened as PROPOSED

`design-brief.md` §14 reads *"Recommend yes, for learned consistency. **Designer confirms.**"*
The brief reserves the confirmation to the human. `TODO.md` item 6 restored.

### 3. Constraint C3 from the APPROVED Q22 is NOT satisfied

C3 requires that **≤25% rival health and meter 100 arrive close together**. At Q2 = 1200
meter 100 lands at ~0:40–1:25 and the health gate at ~2:53 — **90 to 135 seconds apart.**
Group 02 said so plainly (*"They do not arrive close together"*) and then declared C3
satisfied against a **substituted criterion** — that meter-first is the safe ordering.

**That substitution is the violation.** The argument may well be right, but a dispatch may
not amend an approved constraint's success criterion and then mark itself compliant against
the amended one. C3 came from the one decision carrying the designer's recorded approval.

**Status: OPEN, and the designer's call.** Two paths, both already on the table:
- **Accept meter-first ordering as C3's real intent** and amend C3 explicitly, on the record.
- **Take group 06's Q2 → 1050–1100**, which group 06 independently identified as the
  compliant lever and which group 02 also offered as the fix for its own ~5:24 overshoot.

Recorded as `TODO.md` item 64. **No number was changed to produce this note.**

## Log

### 2026-08-02 — Group 09 · the five cinematic corrections (V1–V5)

- **Status:** **ALL FIVE APPROVED** (KIND A engineering). Deleted from `TODO.md`. Four
  narrow carve-outs remain PROPOSED and became items 59–62.
- **Resolves:** TODO items 34 (V1), 35 (V4), 36 (V2), 37 (V3), 38 (V5)
- **Dispatch:** group 09 → `design/group-09-cinematic-corrections.md`
- **These clear hard check 7 (cinematic handoff safety), the one check
  `cinematic-integration-inspection.md` failed.**

| V | Correction | Targets |
|---|---|---|
| V1 | `bInImpactBurst` on `BB_CrimsonVanguard` as a second park key alongside `bInClash`, with a second `Selector` branch (`Observer Aborts = Lower Priority`) into the existing `BTTask_WaitIndefinite`; both released only in `RestoreCombatState()`. **Nothing is suspended while a window is merely open** — combat continues under the prompt | plan §3.1 row 19, §5.1 step 7 |
| V2 | `Set View Target with Blend` back to the possessed `BP_PlayerFighter` as an unconditional restore step, **called directly on the PlayerController, never through `BP_PresentationSubsystem`**; §2 principle 4 and §10 line 7 rewritten verbatim; §3.1 row 27 made the sole authoritative list | plan §3.1 row 27, §2, §10 |
| V3 | All hit-window state moved off the notify object onto the combat components behind a new `BPI_CombatWindows` interface, keyed by a monotonic `WindowID`; `ForceCloseOrphanedWindows()` called from restore and from the component tick. **Retires the notify-end dependency entirely** | plan §3.1 row 27, §8.4 |
| V4 | Per-branch montage-cleanup ledger; directors record `ActiveOverlayMontages` so restore's targeted `Montage Stop` covers natural completion, abort and death in one step; a single terminal `bDuelOver` rule on `BP_DuelDirector` resolves `OnDeath` during any overlay | plan §3.1 rows 19, 22, 27 |
| V5 | Blind clear replaced with `ResyncTransientTags()` over a closed seven-tag set, reading V3's window registry | plan §3.1 row 27 clear list |

**Two findings that go beyond the inspector's own text:**
1. **A latent unintended-punishment bug already present in the approved clear list.**
   Restore runs on the Impact FAILURE branch, where nothing was suspended — so a blind
   clear of `State.Invulnerable` / `State.PerfectWindow` **strips a player's i-frames
   mid-dodge** if a window expires during that dodge. **Adding `State.Dodging` literally,
   as V5's acceptance condition words it, would have widened the bug.** The resync shape
   satisfies the intent without creating it. The same reasoning forced V3's closure to be
   **orphan-scoped** rather than "close everything" — an unscoped force-close would whiff
   the player's own live combo hit.
2. **V1's "can't-attack-state rule" alternative is not actually available.**
   `AN_ComboFinisher` can open a window in any rival state, so a burst can begin
   mid-`Telegraph`. **The park flag is mandatory, not a preference.**

**Load-bearing engine fact:** `Received Notify End` is documented as **unreliable under
montage interruption**, which is what turned V3's either/or acceptance condition into a
both.

**Unresolved, left to the architect:** `BPI_CombatWindows` is a new asset, and the plan's
anti-fork rule (§2 principle 1) wants one shared class — but the player and rival have
different combat components, so an interface is the lightest way to give restore one call
path across both. The two-explicit-calls fallback is named; **choosing between them is the
architect's call when applying.**

**Supersedes GDD:** none. Burst stays 1–3 s; failed Clash stays 1 HP / meter 50 / 3 s;
Impact response stays 0.75 s and 0.35–0.50 s. No auto-success anywhere.

**These are a paper correction to `combat-integration-plan.md`. The architect must apply
them, and that is now TODO item 63. M1 and M2 may proceed now regardless — only M3 is
gated.**

### 2026-08-02 — Group 08 · asset decisions (Q30, Q31, item 20)

- **Status:** **Item 20 APPROVED** for the build action (deleted from `TODO.md`); the legal
  characterization is referred to a human. Q30 and Q31 **PROPOSED**.
- **Resolves:** TODO items 19 (Q30), 42 (Q31), 20
- **Dispatch:** group 08 → `design/group-08-assets.md`

| Item | Answer | Where it lands | Unblocks |
|---|---|---|---|
| Q30 | **YES — take `Paragon: Crunch`** (alternate `Paragon: Steel`). Decide by **2026-08-09**, import **before M2-04/M2-05 are authored**. Build the rival on **Crunch's own skeleton using Crunch's own animation cycles**, which removes the `IK Retargeter` pass from the critical path entirely | M1-23 → M2 | M1-23 |
| Q31 | **Phase 1 ships without an audio *pass* — and that must be said now, not discovered.** No M1–M4 gate names audio; only M5's does. **But not literally silent:** a capped **6–9 one-shot cue floor at ~0.5 day**, sequenced *after* M4's gate, routed through `BP_PresentationSubsystem` so it stays disable-able | M5-04 | M5-04 |
| 20 | **APPROVED — exposure is zero.** The swoosh exists only on the GDD's concept sheets, **on no asset in the build or the plan.** Manny and Quinn carry no branding. Remedy: a five-minute recorded verification at **M1-23** and a one-sentence constraint on **M5-06** art that does not exist yet | process | M1-23 |

- **Why Crunch:** it wins on the two page-14 lines that actually matter for readability —
  **fully enclosed fist with no weapon** ("the hand *is* the weapon") and **mech proportion
  with a small head**. Steel loses on the shield.
- **Day cost of Q30: ≈1.0 day, offset by ≈0.5–1.0 day returned** on M2 attack-animation
  sourcing → **net ≈0 to +0.5 days.** Retargeting Manny animations onto Crunch instead is
  **+1.0–1.5 days (do not).** Swapping *after* the attack rows are authored is
  **+2.0–3.0 days and is forbidden** — that is precisely the double-tuning §14 warned about.
- **Supersedes GDD:** none. **But Q31 supersedes `design-brief.md` §12.6's "no free sound
  source verified"** — the **Sonniss #GameAudioGDC** bundle is worldwide, non-exclusive,
  royalty-free, commercial, **no attribution**, with an **AI/ML-training prohibition that
  binds Assignment #04, not the game**. Freesound filtered to **CC0** is the right tool for
  the nine-cue floor; the CC0 filter is mandatory because every other licence there carries
  an attribution obligation.

**A defect in the brief, MEDIUM confidence — now TODO item 58.** Search results indicate
**UE Starter Content was removed from the engine in 5.7**, and `design-brief.md` §12.1 and
§12.6 both lean on it. The source is community-grade, not Epic docs. **Verify by ticking
Starter Content on a new 5.8 project — five minutes.** The asset ledger routes around it
either way.

**Gaps that could not be closed with a free source:** the rival's **back-vane/thruster
silhouette** (no free asset matches page 14 — omit in Phase 1; telegraph pose plus emissive
carries Attack D's cue; geometry is M5); a **martial-arts strike set with the intended
weight** (standing §12.6 gap); **character art matching the sheets** (standing, M5); a **UI
icon set** (text and plain bars suffice). **Music is not a Phase 1 gap** and now has a
verified free M5 option in Incompetech, at the cost of a **CC BY 4.0 credits-screen
obligation** — the paid attribution-free licence is named and explicitly not taken.

**Q31 addresses the readability tension honestly:** the GDD names sound as a Telegraph and
Phase 2 channel. Shipping the pass in M5 means that channel is absent in Phase 1, so pose,
warning lights and emissive carry the load — which is why the capped cue floor exists at all.

### 2026-08-02 — Group 07 · structure and canon (Q25, Q18, Q23, Q29, items 26, 27, 28)

- **Status:** **item 28 APPROVED** (KIND A, deleted). **Q18 was wrongly closed and is reopened as PROPOSED** — see the 2026-08-03 correction note. Q25, Q23, Q29
  and item 27 **PROPOSED**. **Item 26 is not resolved — it is blocked on a human and stays
  open.**
- **Resolves:** TODO items 25 (Q25), 29 (Q18), 5 (Q23), 32 (Q29), 27, 28
- **Dispatch:** group 07 → `design/group-07-structure-and-canon.md`

**Q25 — 26 per-attack values, all PROPOSED.** Telegraph P1 **A 0.70 · B 0.60 · C 0.80 ·
D 0.90**, P2 **0.55 / 0.48 / 0.62 / 0.70**. Active, one value for both phases, **A 0.22 ·
B 0.36 · C 0.30 · D 0.45**. Recover P1 **0.85 / 0.70 / 0.60 / 0.55**, P2 **0.68 / 0.56 /
0.48 / 0.44**. Duel-level: Reposition **0.90 / 0.55**, Select **0.15 / 0.15**, Return to
Neutral **0.15 / 0.15**. Telegraph tracks range (close = short); Recover tracks commitment
inversely (D shortest because D exists to set up A). Lives in `DT_VanguardAttacks` +
`S_AttackPhaseTuning`; unblocks M2-04.

**RANGE COMPLIANCE: 26 / 26 in range. 0 out of range. 0 GDD ranges altered or collapsed.**
One value sits on an inclusive boundary — **Attack D's Active at 0.45 s is the published
maximum**, deliberately, per group 04's mandate. **The validation check must therefore be
`Min <= Value <= Max`**, and D's Active has zero upward headroom.

Three Q25 findings the developer must not miss:
- **`ActiveSeconds` must never gain a per-phase field.** Scaling D's 0.45 s by the ~0.78
  Phase 2 ratio makes 600 cm cross at **1714 cm/s** and breaks the GDD's own no-snap rule.
  It belongs on the row, outside both phase structs.
- **Attack B's first-to-last hit notify must span ≤ 0.26 s**, or Q6's 0.28 s i-frames
  cannot cover the sequence and **B becomes unavoidable.**
- **Q5 = 3 survives independently.** Punish windows come out 1.75–2.05 s (P1) and
  1.29–1.53 s (P2) against a ~1.0 s combo, confirming group 02's rejection of 4 sections.

| Item | Answer | Lives in | Unblocks |
|---|---|---|---|
| Q18 | **PROPOSED — 0.35 s** (reopened 2026-08-03, see correction note), as `MontageLength / EffectivePlayRate + 0.35`. **Must divide by effective play rate** or it fires early on every Phase 2 telegraph | `DA_TuningGlobals` | M2-12 |
| Q23 | **No timer** — the variable should not exist. Under Q22 a clock converts group 06's bounded retry loop into a hard fail. Two terminal branches, not three | `BP_DuelDirector` | M1-09 |
| Q29 | **Recommend `VALOR-7`; ship the field blank.** Keeps Q45's build behaviour but breaks its silence, because the GDD names *this* one for finalization and an unnamed boss health bar is a visible hole | `WBP_HUD` | M3-04 |
| 27 | **Non-canonical for gameplay.** Stays in the GDD unedited, legal as #04 flavour, **forbidden as a float** | — | M2-04 |
| 28 | **APPROVED — 208 cm.** 82 in × 2.54 = 208.28, rounded as Echo's 183 and Nova's 173 are. Uniform scale only; capsule scales with the mesh; reach re-validated per GDD §07 | `BP_CrimsonVanguard` | M2-05 |

- **Q29 prior art:** Titanfall 2 (BT-7274 → "BT"), Armored Core VI (`AAP07: BALTEUS`),
  MGR (`LQ-84i`), plus a 2–16-char nameplate budget and ~30% localization buffer that puts
  `CRIMSON VANGUARD` at 16 characters with **zero headroom**.
- **Item 27's load-bearing part is the fence around MOBILITY 6/10 versus open item 49:**
  `0.6 × 600 = 360 uu/s` triggers exactly the kiting failure group 04 warned about,
  `0.6 × 1030 = 618`, and "6/10 of an unstated max" is undefined. **Three answers, so not a
  number.**
- **Item 28 caveat:** **width is still unspecified.** Do not derive a capsule radius from
  "roughly twice the shoulder width."
- **Supersedes GDD:** none. Item 28 is a transcription *from* the GDD, filling a blank in
  `design-brief.md` §13.1 row 28.

**Item 26 is correctly unresolved and stays open.** The transcription disclaims itself, so
the dispatch refused to settle a canon contradiction from low-confidence text and instead
wrote four specific questions for the designer to answer by zooming page 14. **M2-04 is
not blocked** — Attack A keeps 0–260 cm, 32 damage and its Q25 timings under every reading,
because authored §04 text outranks an image description and a reference sheet cannot add a
mechanic. The real risk named: **Assignment #04 seeding lore from a low-confidence chunk.**

**One tension carried forward: Attack A's Phase 1 cycle is 2.97 s against Q12's 3.0 s A
cooldown — 0.03 s of slack.** At 0–90 cm, where group 04's bands make A the only legal
attack, that is A every ~3.0 s at 32 damage — **10.7 dmg/s against 100 HP.** It cannot be
fixed from inside Q25; every legal choice of the six state values lands the cycle in
2.8–3.2 s. The levers belong to Q12, Q10 or Q3. **Q12 and Q25 need one joint tuning session.**

*Research note: 11/15 searches. No shipped game publishes per-attack boss telegraph or
recovery durations — the third group in a row to report that.*

### 2026-08-02 — Group 06 · Final Clash and meter (Q9, Q17, Q19, Q20, Q21)

- **Status:** **Q17 was wrongly closed and is reopened as PROPOSED** — see the 2026-08-03 correction note. Q9, Q19, Q20, Q21 **PROPOSED**.
- **Resolves:** TODO items 31 (Q9), 6 (Q17), 39 (Q19), 40 (Q20), 41 (Q21)
- **Dispatch:** group 06 → `design/group-06-final-clash.md`

| Q | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q9 | **No decay.** `MeterDecayRate` should not exist as a variable at all — no Tick, no timer, no float | `BP_AscensionComponent` | M3-03 |
| Q17 | **PROPOSED — reuse `IA_Impact`.** (reopened 2026-08-03) One action, one `IMC_Duel`, routed by a `bClashBeatOpen` bool | `IMC_Duel` | M1-10 |
| Q19 | **1.2 s**, band 1.0–1.3, authored as `CounterRecoveryLength + 0.6 s` | `BP_FinalClashDirector` | M4-05 |
| Q20 | **0.50 s, both beats, identical** — the top of the GDD's published 0.35–0.50 s Standard range | `BP_FinalClashDirector` | M4-06 |
| Q21 | **1200 cm** along the arena long axis, midpoint push with clamp-and-redistribute; band **1100**–1300 | `BP_FinalClashDirector` | M4-08 |

- **Q9 is shown falsifiably:** a decay of just **0.76 pts/s** zeroes a struggling player's
  income and makes the game unwinnable while the loss condition stays live. C1 confirmed.
- **Q19 finds a real defect in §14's own range.** §14 offers 0.5–1.5 s; **1.5 s is unsafe**
  — the earliest legal Phase 2 strike after a counter is **1.30 s**, so 1.5 s would let the
  player Clash out of an incoming hit.
- **Q20 argues against §14's "beat 2 tighter" suggestion.** Under Q22 that makes the more
  expensive failure the more likely one. Asura's Wrath is the named failure mode. Final
  Fantasy XVI's unfailable clash is rejected by name against the GDD's no-auto-success rule.
- **Q21 implementation:** `Teleport = true` not sweep, `ProjectPointToNavigation` first,
  applied **under the camera cut**.
- **Supersedes GDD:** none. Q20 takes 0.50 s from **inside** a published range rather than
  inventing a value.

**Retry-loop verdict: acceptable under Q22, with margin — but the penalty is regressive.**
One retry costs ≈19 s (strong) to ≈71 s (struggling). **The GDD's 3-second cooldown is
never binding** — the fastest possible rebuild is 13.8 s. A competent player can **fail
four times and still finish inside 5:00**. The tail cannot run away because the loss
condition bounds it: the struggling player statistically dies (~118 damage) during their
first retry.

**Three tensions carried forward:**
1. **The practical meaning of Q22 + Q20 is that a player who cannot execute the two beats
   loses the duel rather than grinding it out.** Defensible — it is Sekiro's position — but
   it makes *"I fought well for four minutes and lost to two timing beats"* reachable.
   **This is the question the file most wants the designer to answer.**
2. **Q21 cannot be validated** because the rival's `MaxWalkSpeed` does not exist (item 49).
   This group supplies the missing **upper bound ~1030 uu/s**; group 04 supplied the lower
   bound. **They must be tuned in one session.**
3. **No shipped game reached publishes a numeric QTE window or a knockback distance in
   world units** — six searches spent confirming that. Q20 and Q21 are derived from the
   GDD's own ranges and group 04's arena, not from prior art. **Q19 is the weakest-sourced
   answer in the file.**

**Bonus: group 01's unverified Hi-Fi Rush claim is now closed** — the fight continues and
the parry set can be retried, which is the GDD's failed-Clash rule shipped in a real game.

**Four more missing rows — now TODO items 54, 55, 56, 57.**

### 2026-08-02 — Group 05 · fighter feel and presentation (Q14, Q15, Q16, items 43, 44, 45)

- **Status:** **PROPOSED** — all six. The designer decides.
- **Resolves:** TODO items 7 (Q14), 8 (Q15), 9 (Q16), 43, 44, 45 · all KIND B
- **Dispatch:** group 05 → `design/group-05-fighter-feel.md`. **Ran in two parts** — the
  first dispatch was killed mid-run by an API session limit after Q14/Q15/Q16; because
  the prompt required incremental writes, those three survived on disk and were committed
  before a fresh dispatch completed items 43–45.

| Item | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q14 | `MontagePlayRate` **1.000 / 1.000, identical** | `DA_FighterProfile` | M1-12 |
| Q15 | `MaxWalkSpeed` **600 uu/s identical**; locked-on strafe **420**, backpedal **360** | `DA_FighterProfile` | M1-12 |
| Q16 | `DodgeDistance` **400 cm identical**, delivered by **Motion Warping** | `DA_FighterProfile` | M1-12 |
| 43 | Echo's faceplate is **"visor AND light", not "visor OR light"** — dark visor plane plus one small indicator in the same helmet position Nova's already occupies. **No gameplay-state modulation.** | `M_Fighter` / helmet material | M5-06 |
| 44 | Energy lines **emissive and Ascension-responsive, for both fighters** — one `Ascension01` scalar on the shared master material, per-fighter masks, stepped at **50 and 100** (thresholds the design already owns), intensity only, no hue change | shared master material | M5-06 |
| 45 | **"SFN" cannot be established and is not established here.** Ship the badge as art; expose `FighterUnitLine` **blank**, per the Q29 precedent | `WBP_CharacterSelect` | M5-08 |

- **Q14's answer is structural, not just a value.** Rename the field
  `CosmeticMontagePlayRate`; restrict consumers to a four-montage allowlist carrying no
  gameplay notify states; route every `Montage_SetPlayRate` through one library node that
  `ensure()`s the montage is notify-free. **This is the direct answer to group 03's
  warning that Q14 would silently scale Q6/Q7 into per-fighter difficulty.**
- **Scoping catch the guard needs:** the **rival's** `TelegraphScale`/`RecoverScale`
  legitimately use play rate — that is the Phase 2 one-data-path — so the guard must be
  scoped to the player kit or it fires falsely.
- **Q16 uses Motion Warping deliberately:** warping changes displacement without touching
  the montage timeline Q6 and Q7 sit on. Play rate would move both.
- **Item 43's reasoning is worth keeping:** under the GDD's reverse third-person framing
  the face is **off-camera for the entire duel** — it appears only on the select screen,
  the entrance, the Impact burst, and the Clash. So the faceplate is not a viable
  readability channel and should not be made one.
- **Item 44 respects Nova's readability target** — her lit area is deliberately smaller
  than Echo's, because *"momentum without visual noise"* limits how much may glow. The
  channel is **never the only channel**; the HUD stays authoritative and keeps C2's gate
  indicator.
- **Milestone order held.** All of 43 and 44 is placed in **M5**. The only "Note to M1" is
  two lines that add no work: cache the dynamic material instance `ApplyFighterProfile`
  already needs, and bind nothing to `OnMeterChanged` for emissive purposes before M5.
- **Supersedes GDD:** none. Prior art: Dead Space's RIG spine, For Honor's Revenge, Doom
  Eternal glory-kill states, Devil May Cry's Devil Trigger, Overwatch/TF2 readability.

**Tensions carried forward:** Echo's orange sits next to the rival's red-orange warning
lights — mitigated by a rule (**the rival owns animated emissive, the player owns static
or stepped**) that makes the risk testable, not gone. Thin-spine-line legibility at duel
distance is unproven and is the standing criticism of the Dead Space RIG it is modelled
on. **Nova's yellow-green indicator strips appear in the art but not in her printed
four-swatch palette** — routed around, not resolved. Nova has no back unit, so parity of
*information* is achievable but parity of *lit area* would be a character-art change,
declared out of scope. **"SFN" is a stylised monogram on a sheet with two confirmed
typos — a human should confirm the letters against the PDF before anyone builds fiction
on them.**

**Two more missing rows — now TODO items 52, 53:** the locked-on **strafe multiplier** and
**backpedal multiplier** have no §13.2 row and no Q number.

### 2026-08-02 — Group 04 · spacing and arena (Q24, Q10, Q12, Q13, Q11, mezzanine)

- **Status:** **PROPOSED** — all six. The designer decides.
- **Resolves:** TODO items 17 (Q24), 22 (Q10), 23 (Q12), 24 (Q13), 10 (Q11), 18 (mezzanine) · all KIND B
- **Dispatch:** group 04 → `design/group-04-spacing-and-arena.md`

| Item | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q24 | playable floor **2400 × 1600 cm (24 × 16 m)**, long axis = doorway axis, four 250 cm 45° chamfers; also stored as `ArenaLongAxisCm`/`ArenaShortAxisCm` so Q13 cannot drift | `L_ShatteredRing` + `DA_TuningGlobals` | M1-21 |
| Q10 | bands centre-to-centre **A 0–260 · B 90–520 · C 240–420 · D 400–840** cm, identical both phases | `DT_VanguardAttacks` Min/MaxRange | M2-04 |
| Q12 | P1 **A 3.0 · B 3.5 · C 3.6 · D 3.8 s** / P2 **A 2.5 · B 2.6 · C 2.7 · D 2.8 s**, **relocated into `S_AttackPhaseTuning`** so Phase 2 re-times through the existing data path | `S_AttackPhaseTuning` | M2-04 |
| Q13 | **600 cm = 0.25 × long axis**, finishing 240 cm from the target | `DT_VanguardAttacks.MaxTravelDistance` | M2-04 |
| Q11 | acquire **3000 cm**, break **3300 cm**, interp **6.0**, aim socket **140 cm** at **−8°** — both beyond the 2884 cm diagonal so lock never breaks by distance in this arena | `BP_LockOnComponent` | M1-16 |
| 18 | mezzanine is **set dressing** — no NavMesh, no blocking volume, railings `NoCollision`, underside ignores the `Camera` channel | `L_ShatteredRing` | M1-21 |

- **Footprint:** 2400 × 1600 uu, diagonal ≈ 2884 uu, ~371.5 m² walkable. Stated as **two
  dimensions**, per the recovered arena sheet showing a rectangular hall.
- **Band coverage proof delivered:** contiguous over [0, 840] with 80 cm and 120 cm
  handoff overlaps, depth ≥ 2 across the whole 100–520 cm fight zone. Exactly one
  zero-coverage region (840–2884 cm) and one depth-1 region (520–840 cm), **both resolved
  by a required advance rule rather than by accident** — which is the `BTTask_Idle_Reposition`
  loop bug §14 warned about, closed deliberately.
- **Starvation check passes in both phases** at the fastest legal cycle; tightest slack
  **+0.16 s**. Q12's legal window is narrow: **(2.94, 3.96] s in P1**, **(2.315, 2.96] s in P2**.
- **Supports Q21 (Final Clash group):** separation **1000–1300 cm**, 1300 the guaranteed
  ceiling, **1200 the comfortable value**, pushed along the long axis rather than the
  fighters' facing.
- **Handed to Q25:** author **A and B short (0.55–0.70 s), C and D long (0.75–0.95 s)** —
  group 03's counter-spam warning made spatial. And **D's Active must sit at 0.40–0.45 s**,
  or 600 cm in 0.18 s reads as the teleport the GDD forbids.
- **Supersedes GDD:** none. Prior art from Tekken's published stage sizes (24×24 standard,
  16×24 *Midnight Siege*). Souls-like arena dimensions and per-attack AI cooldowns were
  searched for and **cited as not found rather than estimated**.

**Three more gaps with no §13.2 row and no Q number — now TODO items 49, 50, 51.** One of
them is serious: **the rival's `MaxWalkSpeed` is unspecified, and under the approved Q22
a rival slower than the player can be kited forever and the duel cannot end.**

**Q12 is the weakest-sourced item in this group** — no shipped game publishes AI attack
cooldowns, so it is derived purely from the GDD's own state ranges.

*Research note: 10/15 searches.*

### 2026-08-02 — Group 03 · defensive timing (Q6, Q7, Q8, Q26, Q27, Q28)

- **Status:** **PROPOSED** — all six. The designer decides. **Q7 is BLOCKING.**
- **Resolves:** TODO items 14 (Q6), 15 (Q7), 16 (Q8), 33 (Q26), 30 (Q27), 13 (Q28) · all KIND B
- **Dispatch:** group 03 → `design/group-03-defensive-timing.md`

| Q | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q6 | i-frames **0.28 s**, spanning `[0.03, 0.31]` of `AM_Player_Dodge` | `ANS_IFrame` | M1-19 |
| Q7 | perfect dodge **0.12 s**, `[0.03, 0.15]` — front 43% of the i-frame window | `ANS_PerfectDodge` | M1-19 |
| Q8 | whiff lockout **0.55 s** | `AM_Player_CounterWhiff` | M1-20 |
| Q26 | Impact cooldown **7.0 s**, clocked on window *close*, **first window exempt** | `BP_ImpactWindowDirector` | M3-07 |
| Q27 | recover multiplier **1.0 — no bonus** | `ANS_Recover` | M2-13 |
| Q28 | combo buffer **0.25 s = 75% of a section**, stated as a ratio | `AM_Player_LightCombo` | M1-18 |

- **Q7 rationale:** 4× SF6's 2-frame Perfect Parry, tighter than Sekiro's 12-frame deflect
  and SF3's 10-frame parry. **Front-loaded so the player must press late, into the strike.**
  Playtest protocol given: **start at 0.15 s and tighten**, never the reverse.
- **Reaction check passes at the hardest legal attack:** against a 0.40 s Phase 2
  telegraph the perfect-press window `[0.25, 0.37]` opens exactly at the ~250 ms average
  human reaction time.
- **Q26 first-window exemption is not optional** — applying the cooldown to the first
  Impact Window would break the GDD's onboarding rule.
- **Supersedes GDD:** none. All six fill blanks; every cited range is unchanged.

**Q2 = 1200 SURVIVES.** At Q27 = 1.0 the scalar is unity and group 02's derivation stands
intact. Better: effective damage becomes `20 × [f×Q27 + (1−f)]`, so **1.0 removes the
unmeasurable `f` term from the model entirely.** If the designer overrides Q27:
**1.25 → Q2 ≈ 1410** (outside group 02's 1100–1400 band); **1.5 → Q2 ≈ 1620**, and at
Q2 = 1200 a strong player reaches the gate at **1:55**, below the GDD's 3-minute floor.

**Five tensions carried forward:**
1. **Q26 cannot make the meter a real second gate — no value in 3–8 s can.** Group 02's
   framing is corrected rather than answered: the meter has four faucets and Q26 gates
   one. With Impact **disabled entirely**, 20 finishers still fill the meter in ~84 s
   against a health gate at ~173 s. Every route to halving that is closed — gains are
   GDD-fixed, C1 forbids decay, the 0–100 ceiling is GDD-fixed. **The meter is an
   anti-passivity floor, not a race.** 7 s still cuts the +20 row's dominance from a
   ~2.25× speedup to ~1.67×.
2. **Q8 anti-spam fails against slow Phase 1 telegraphs (0.75–0.95 s).** Closing it needs
   ~0.95 s of lockout — outside §14's band and unplayable. Accepted as a beginner crutch
   that dies at Phase 2. **Warning to Q25: do not author all four attacks near 0.95 s.**
3. **Q27 = 1.0 does not fix group 02's scrappy ~5:24 overshoot.** 1.25 trims ~25 s while
   also shortening the competent run — net zero. Group 02's own Q2 → 1050–1100 remains
   the only fix.
4. **Q7's repeatability is unverified.** The check proves the pocket's *onset* is
   reachable; it does not prove a human can hit 0.12 s repeatably. Motor-timing precision
   was out of research budget.
5. **Q8's magnitude has no prior-art support.** No whiffed-parry recovery frame counts
   were found in any shipped game. 0.55 s is derived purely from the GDD's own telegraph
   and recover ranges. **Named as the weakest number in the file.**

**Three defects found in `design-brief.md` §13.2 — now TODO items 46, 47, 48.** The table
has no row and no Q number for the counter's own success window, for whether a dodge
cancels the light combo, or for the total length of `AM_Player_Dodge`.

**Developer notes:** `ANS_ActiveHit` and `ANS_ComboLink` overlap on the same section and
**must not be merged**; `bComboQueued` clears on next-section begin and on any montage
interruption; a successful counter must **not** play `AM_Player_CounterWhiff`;
`BP_ImpactWindowDirector` needs a `bFirstWindowConsumed` flag that skips the cooldown
check; `BP_FinalClashDirector` must never consult that cooldown. **Three separate
warnings that Q14's `MontagePlayRate` would silently scale Q6 and Q7 into per-fighter
difficulty — Q28 is the only one of the three that scales correctly.**

*Research note: 15/15 searches, cap reached.*

### 2026-08-02 — Group 02 · combat economy (Q1, Q2, Q3, Q4, Q5)

- **Status:** **PROPOSED** — all five. The designer decides.
- **Resolves:** TODO items 2 (Q1), 3 (Q2), 21 (Q3), 11 (Q4), 12 (Q5) · all KIND B
- **Dispatch:** group 02 → `design/group-02-combat-economy.md`

| Q | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q1 | Player max health **100**, identical for both fighters | `DA_TuningGlobals` | M1-05 |
| Q2 | Vanguard max health **1200** (band 1100–1400) | `DA_TuningGlobals` | M1-05 |
| Q3 | Rival damage **A 32 · B 25 · C 27 · D 18** (% of player max HP) | `DT_VanguardAttacks.Damage` | M2-04 |
| Q4 | Light hit **5**, finisher **10** (2×), combo total **20** | `AM_Player_LightCombo` notify data | M1-17 |
| Q5 | **3** sections — `S_Hit1` / `S_Hit2` / `S_Finisher`, ~1.0 s | `AM_Player_LightCombo` | M1-17 |

- **Why Q1 = 100:** makes Q3's "percentage of player health" and the Data Table integer
  the same number, so the two can never drift.
- **Why Q5 = 3, and this is the load-bearing finding:** at GDD midpoints the rival's
  cycle leaves a non-threatening window of ~1.73 s in Phase 1 and **~1.28 s in Phase 2**.
  A 4-section combo runs ~1.33 s and **does not fit Phase 2 at all**. Q5 = 4 would also
  invalidate the Q2 derivation.
- **Q2 is derived, not picked:** 1200 puts the ≤25% gate at ~2:53 for competent play and
  ~4:29 for scrappy play, against the GDD's 3–5 minute target.
- **Supersedes GDD:** none. Every value fills a blank the GDD never specified; all fixed
  GDD numbers are cited and unchanged.

**C3 IS NOT SATISFIED — see the 2026-08-03 correction note.** Group 02 wrote: — meter 100 arrives ~0:40–1:25 while the health
gate arrives ~2:53, so they do *not* converge. The ordering is meter-first, which is the
safe direction: the player spends the tail attacking and damage still progresses. The
dangerous state (1 HP, empty meter) does not occur in normal play.

**Five open tensions carried forward, none of them settled here:**
1. **Post-failed-Clash rebuild** leaves ~15–35 s of genuinely inert damage. This makes
   **C2's HUD gate indicator mandatory, not optional.**
2. **The 2-hit-and-bail player** never finishes a string, earns no meter, and can reach a
   pinned rival with an empty bar. No number in this group can close it — handed to C2,
   the onboarding Impact Window, Q28 and Q25.
3. **Scrappy worst case overshoots to ~5:24**, past the 3–5 minute target. Either accept
   it (that player may hit the loss outcome first) or drop Q2 to ~1050–1100.
4. **Q26 makes the +20 Impact row dominant** — five Impact successes fill the meter
   outright. If the meter is to be a real second gate, the lever is **Q26**, not any GDD
   gain value. Flagged to the defensive-timing group.
5. **Attack B is a "sequence."** If authored with multiple `ANS_ActiveHit` windows each
   reading `Damage = 25`, B deals 50–75% of player health in one attack and the budget is
   void. **Proposed rule: the Data Table row is *total* attack damage, split across
   notifies.** Named as the most likely way the table silently produces a broken fight.
6. **Q27 is a direct scalar on the Q2 derivation** — at §14's upper bound of 1.5 the
   45-combo count drops toward ~30. **Q27 should be resolved before Q2 is locked.**

*Research note: 13 searches. Datamined boss HP for Sekiro and Elden Ring returned nothing
reliable, so no such figure is cited. One claim about Sekiro percentage damage is marked
unverified and is not load-bearing.*

### 2026-08-02 — Q22 · the 1 HP floor is permanent; the Final Clash is the only way to win

- **Status:** **APPROVED** — accepted as proposed by the designer of record, 2026-08-02.
  **This is now settled and binding on every downstream answer.**
- **Resolves:** TODO item 4 (Q22) · **BLOCKING** · KIND B · entry deleted from `TODO.md`
- **Dispatch:** group 01 → `design/group-01-blocking-q22.md`
- **Proposed decision:** reading **(b)**, sub-variant **(b2)** — `MinHealthFloor = 1` on
  the rival's `BP_HealthComponent` from `BeginPlay`, lowered to `0` only by
  `ClashSuccess()` immediately before it applies lethal damage.
- **Value lives in:** `HealthComponent.MinHealthFloor` (`design-brief.md` §13.2 row 50)
- **Unblocks:** M1-08 — Create the shared `BP_HealthComponent`
- **Why, in short:** the GDD's encounter-flow table lists exactly one win condition
  (Final Clash success), so reading (a) requires *adding* a win condition the GDD never
  writes down while (b) only widens the scope of a floor the GDD does state; it makes
  the double gate meaningful; it makes the meter — and therefore skill — the only route
  to the ending; and it is the cheapest, least leak-prone build.
- **Prior art cited:** Sekiro (Deathblow), Metal Gear Rising: Revengeance (Monsoon and
  Sundowner hard-stop at 10% into a mandatory QTE), Hi-Fi Rush, Sifu, God of War
  Ragnarök, Furi, Jedi: Fallen Order, Asura's Wrath as the cautionary case. Two claims
  are explicitly marked unverified in the group file.
- **Three attached conditions — carried forward as binding constraints on later groups:**
  **C1** Q9 must resolve to **no meter decay**, or the tail can become a dead end.
  **C2** the HUD must show **which gate is still locked** once the health bar visibly pins.
  **C3** Q2 must be tuned so **≤25% and meter 100 arrive close together**.
  These are not settled answers to Q9, the HUD, or Q2 — they are constraints those
  answers must satisfy.
- **Supersedes GDD:** none. This interprets the scope of the GDD's failed-Clash 1 HP
  floor; it edits no GDD number and contradicts no GDD line.
- **Developer note:** M1-08 can proceed either way — the clamp is identical. What must
  wait is the rival instance's default value and whether `BP_DuelDirector` wires a rival
  `OnDeath → EndDuel(Win)` path at all. Leave both unset rather than let a default
  silently become the design.

### Entry format

```markdown
### YYYY-MM-DD — <short title>

- **Resolves:** TODO item <n> (<Q/V id>)
- **Decision:** <the answer, stated plainly enough to implement from>
- **Decided by:** <name>
- **Supersedes GDD:** none
  <or>
- **Supersedes GDD:** "<quoted line>" — `gdd/sections/<file>.md`, PDF page <n>.
  TODO item added: GDD out of date.
```
