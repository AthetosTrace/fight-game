# Group 07 — Structure and canon

**Dispatch date:** 2026-08-02
**Dispatch:** designer, group 07 of the open-item sweep
**Scope:** seven items — **Q25, Q18, Q23, Q29** from `design-brief.md` §14, plus **items 26, 27, 28**, three canon questions raised by the GDD reference sheets recovered on 2026-08-02.
**Produces:** this file only. It does **not** modify `design-brief.md`, `TODO.md`, `design/decisions.md`, or anything under `gdd/`.

## Status per item

| Item | Kind | Status | Unblocks | Value lives in |
|---|---|---|---|---|
| **Q25** — per-attack values inside each GDD state range | B | **PROPOSED** | M2-04 | `DT_VanguardAttacks` (§13.2 row 53) |
| **Q18** — BTTask montage failsafe margin | A | **APPROVED** | M2-12 | each `BTTask_*` (§13.2 row 46) |
| **Q23** — is there a duel timer? | B | **PROPOSED** | M1-09 | `BP_DuelDirector` (§13.2 row 51) |
| **Q29** — Crimson Vanguard short in-combat UI label | B | **PROPOSED** | M3-04 | `WBP_HUD` (§13.2 row 57) |
| **Item 26** — "plasma-gauntlet weapons" vs Attack A | B | **BLOCKED ON HUMAN CONFIRMATION** | M2-04 | nothing yet — see below |
| **Item 27** — page 14 "SYSTEM STATS" map to no system | B | **PROPOSED** (non-canonical) | M2-04 | nothing — that is the proposal |
| **Item 28** — Vanguard height in centimetres | A | **APPROVED** | M2-05 | `BP_CrimsonVanguard` mesh scale (§13.1 row 28) |

## Binding context this group had to honour

**Q22 is APPROVED and settled: the Final Clash is the only way to win.** The 1 HP floor on
`BP_CrimsonVanguard.HealthComponent.MinHealthFloor` is permanent from `BeginPlay` and is
lowered to 0 only by `ClashSuccess()`. Every answer below assumes the duel ends by Clash,
not by attrition — which is why **duel length is a real constraint** (Q23) and why the
rival's cycle time has to leave the player enough income to reach meter 100 (Q25).

**The two Q25 constraints handed down by earlier groups, quoted:**

1. **Group 03 (defensive timing):** *"Q8's anti-spam holds against all of Phase 2 and the
   fast end of Phase 1, and fails against slow Phase 1 telegraphs (0.75–0.95 s). **Warning
   to Q25: do not author all four attacks near 0.95 s.**"*
2. **Group 04 (spacing and arena):** *"Handed to Q25: author **A and B short (0.55–0.70 s)
   and C and D long (0.75–0.95 s)** — group 03's counter-spam warning made spatial. And
   **D's Active must sit at 0.40–0.45 s**, or 600 cm in 0.18 s reads as the teleport the
   GDD forbids."*

**Both are honoured in full.** A = 0.70, B = 0.60 (short band); C = 0.80, D = 0.90 (long
band, and neither is at 0.95); D's Active = 0.45.

**Other proposed values reasoned against, not changed:** range bands A 0–260 · B 90–520 ·
C 240–420 · D 400–840 cm (Q10); cooldowns P1 A 3.0 · B 3.5 · C 3.6 · D 3.8 s / P2 A 2.5 ·
B 2.6 · C 2.7 · D 2.8 s (Q12); Attack D travel 600 cm (Q13); perfect dodge 0.12 s (Q7);
dodge i-frames 0.28 s (Q6); counter whiff lockout 0.55 s (Q8); no meter decay (Q9); light
combo 3 sections ≈ 1.0 s (Q5); player HP 100 (Q1); rival damage A 32 · B 25 · C 27 · D 18
(Q3).

## Constraint compliance

- **SCOPE LOCK.** Four attacks A–D, the same four in both phases. No fifth attack, no
  transformation, no second move set. Phase 2 is a re-timing of the same four rows through
  the same struct.
- **No runtime AI-model calls.** Everything below is authored constants in a Data Table
  read by a Behavior Tree. Attack selection stays authored weighting by range and cooldown.
- **No GDD number is changed and no published range is collapsed.** Every Q25 value is a
  proposal *inside* a published range, cited per cell, with the range printed next to it.
  The ranges themselves are reproduced verbatim and remain the published ranges.
- **Every value below is PROVISIONAL and PENDING PLAYTEST.** The human designer owns all
  of them.

---

## Q25 — Per-attack values inside each GDD state range

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** M2-04 — populate `DT_VanguardAttacks`
- **Value lives in:** `DT_VanguardAttacks` (`design-brief.md` §13.2 row 53), realized as two
  `S_AttackPhaseTuning` structs per row (`Phase1`, `Phase2`)
- **GDD range — cited, per state, verbatim from `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` (PDF p. 5):**

| State | Phase 1 | Phase 2 |
|---|---|---|
| Idle / Reposition | **0.60–1.20 s** | **0.35–0.80 s** |
| Select Attack | **0.10–0.20 s** | **0.10–0.20 s** |
| Telegraph | **0.55–0.95 s** | **0.40–0.75 s** |
| Active Attack | **0.18–0.45 s** | **0.18–0.45 s** *(identical — not phase-scaled)* |
| Recover | **0.45–0.90 s** | **0.35–0.75 s** |
| Return to Neutral | **0.10–0.20 s** | **0.10–0.20 s** |

Mirrored in `design-brief.md` §13.1 rows 17–25, whose note is the whole reason this item
exists: *"the GDD publishes **ranges**, and it publishes them per *state*, not per *attack*.
The build needs a single float per attack per phase."*

### Q25.0 — Which states are per-attack, and which are not

This has to be settled before any number is authored, because §14 says "four attacks × two
phases × four scaled states" and the GDD table has six states. The six do not all belong to
an attack:

| State | Per-attack? | Why |
|---|---|---|
| Idle / Reposition | **No — duel-level, per phase** | It runs **before** `Select Attack`. No attack has been chosen yet, so there is no row to read from. One value per phase. |
| Select Attack | **No — duel-level, per phase** | Same reason: it *is* the selection. Also invisible; nothing about it is per-attack. |
| **Telegraph** | **Yes** | The readability requirement in GDD §04 is written per attack ("distinct wind-up", "visible first beat", "clear body direction", "thruster cue before movement"). |
| **Active Attack** | **Yes** | Hitbox live time. Differs per attack by construction — a single gauntlet impact and a 600 cm propulsion approach cannot share one number. |
| **Recover** | **Yes** | GDD §04: *"Expose a deliberate punish opening after the committed strike."* The size of the opening is the attack's commitment cost. |
| Return to Neutral | **No — duel-level, per phase** | Bookkeeping: *"Clear attack flags and restore valid locomotion."* Nothing about it is per-attack. |

So Q25 authors **20 per-attack values** — Telegraph 4 attacks × 2 phases = 8, Recover
4 × 2 = 8, and Active **4 × 1 = 4** because Active is not phase-duplicated (Q25.5) — plus
**6 duel-level values** (three states × two phases). **Twenty-six numbers in total**, every one
of them checked against its published range in the compliance table at the end of this file.

**Structural note for the developer, not a change to any number.** `design-brief.md` §13.1
lists rows 17–19 and 25 as living in `S_AttackPhaseTuning`. That is fine if the struct is
embedded per row — group 04 relocated Q12's cooldowns there for exactly that reason. But
Reposition / Select / Return-to-Neutral are **one value per phase, not four**, so if they
sit in a per-row struct there are four copies of each and they will drift. Two acceptable
homes, developer's choice:
- **(a) preferred** — `DA_TuningGlobals` gains `RepositionDelay_P1/P2`, `SelectDelay_P1/P2`,
  `ReturnToNeutralDelay_P1/P2`, and `S_AttackPhaseTuning` carries only the per-attack
  fields (`TelegraphSeconds`, `ActiveSeconds`, `RecoverSeconds`, `Cooldown`);
- **(b)** they stay in `S_AttackPhaseTuning` and the range-validation check (below) is
  extended to `ensure()` that all four rows carry **identical** values for those three
  fields.
Either satisfies the design. (a) makes the drift impossible instead of merely detected.

### Q25.1 — The per-attack table, Phase 1

Attack identity is quoted from GDD §04's four-attack course set. Damage is group 02's Q3;
range band is group 04's Q10.

| Attack | GDD identity | Band (Q10) | Dmg (Q3) | **Telegraph P1** | range | **Active** | range | **Recover P1** | range |
|---|---|---|---|---|---|---|---|---|---|
| **A** | "Close-range committed gauntlet force" — *distinct wind-up and punishable recovery* | 0–260 cm | 32 | **0.70 s** | 0.55–0.95 | **0.22 s** | 0.18–0.45 | **0.85 s** | 0.45–0.90 |
| **B** | "Committed forward-pressure sequence" — *visible first beat and stable tracking limit* | 90–520 cm | 25 | **0.60 s** | 0.55–0.95 | **0.36 s** | 0.18–0.45 | **0.70 s** | 0.45–0.90 |
| **C** | "Armored reach and space control" — *clear body direction and visible active range* | 240–420 cm | 27 | **0.80 s** | 0.55–0.95 | **0.30 s** | 0.18–0.45 | **0.60 s** | 0.45–0.90 |
| **D** | "Short propulsion-assisted approach" — *thruster cue before movement; no hidden full-arena snap* | 400–840 cm | 18 | **0.90 s** | 0.55–0.95 | **0.45 s** | 0.18–0.45 | **0.55 s** | 0.45–0.90 |

### Q25.2 — The per-attack table, Phase 2

**Active Attack is deliberately identical to Phase 1. It is not re-authored, not scaled, and
not present in this table** — see Q25.5 for why that is the right call and not an oversight.

| Attack | **Telegraph P2** | range | ratio vs P1 | **Recover P2** | range | ratio vs P1 |
|---|---|---|---|---|---|---|
| **A** | **0.55 s** | 0.40–0.75 | 0.786 | **0.68 s** | 0.35–0.75 | 0.800 |
| **B** | **0.48 s** | 0.40–0.75 | 0.800 | **0.56 s** | 0.35–0.75 | 0.800 |
| **C** | **0.62 s** | 0.40–0.75 | 0.775 | **0.48 s** | 0.35–0.75 | 0.800 |
| **D** | **0.70 s** | 0.40–0.75 | 0.778 | **0.44 s** | 0.35–0.75 | 0.800 |

The ratios cluster at **0.775–0.800**. That is deliberate: it means Phase 2's re-timing is
realized as a **near-uniform ~1.28× montage play rate**, so the animation distorts by the
same amount on every attack and no single attack looks sped-up relative to the others. It
also means a designer who later wants "Phase 2 harder" has one obvious global lever as well
as twenty-four local ones.

### Q25.3 — The duel-level states

| State | **Phase 1** | range | **Phase 2** | range | Note |
|---|---|---|---|---|---|
| Idle / Reposition | **0.90 s** | 0.60–1.20 | **0.55 s** | 0.35–0.80 | The only state whose *range* shifts hard between phases. GDD §04's Phase 2 table: *"More frequent advances and shorter hesitation."* |
| Select Attack | **0.15 s** | 0.10–0.20 | **0.15 s** | 0.10–0.20 | Invisible bookkeeping. Identical by phase because the GDD publishes one range for both. |
| Return to Neutral | **0.15 s** | 0.10–0.20 | **0.15 s** | 0.10–0.20 | Same. Also the state GDD §04 commits the Phase 2 transition on. |

**If the fight ever feels sluggish in playtest, `SelectDelay` is the safest 0.05 s in the
whole design to reclaim** — it is the only state with no animation, no readability duty and
no player-facing meaning. Reposition is *not* safe to cut for the same purpose: it is where
the rival's "armored pressure" and the player's breathing room both live.

### Q25.4 — Why these numbers

**Telegraph — the readability spine, and the one place the GDD writes per-attack rules.**

The distribution is two short, two long, exactly as group 04 asked, and the split is not
arbitrary — **it tracks range**. A and B are the attacks the player meets while standing
inside the rival's reach, where there is no room to retreat and the read has to be fast.
C and D are thrown across 240–840 cm, where the player has space and where the GDD demands
a *spatial* read ("clear body direction", "thruster cue before movement"), which takes
longer to present.

- **A = 0.70 s**, the top of group 04's short band. A is the heaviest hit in the game (32 of
  the player's 100 HP) and the GDD asks for a "distinct wind-up", so it gets the longest
  telegraph of the two close-range attacks. At 0–260 cm the player has no space, so the
  read must be pure timing.
- **B = 0.60 s**, the fastest telegraph in the game. The GDD asks only that B's *first beat*
  be visible, not that the whole sequence be pre-announced, which is a licence to make B
  quick. B is also the attack whose band (90–520 cm) covers the most ground, so it is the
  rival's default pressure tool and should be the one the player learns to fear first.
- **C = 0.80 s.** Space control that must show "visible active range" before it commits —
  the player is being asked to read *where* the hitbox will be, not just *when*.
- **D = 0.90 s**, the longest, and **not 0.95 s**. D carries the GDD's single hardest
  readability rule — *"thruster cue before movement; no hidden full-arena snap"* — and it is
  the only attack whose telegraph has to sell an *incoming 600 cm of travel* before the
  travel starts. It is also the lightest hit (18), which is the right trade: the most warning
  for the least damage. Holding it at 0.90 leaves 0.05 s of headroom inside the range if
  playtest says the thruster cue is not landing.

**How this satisfies group 03's warning, concretely.** Q8's whiff lockout is 0.55 s. A
player who mashes counter at telegraph start recovers at 0.55 s and gets a second press. So
the mash beats a telegraph long enough to contain two presses, and loses to one that is not:

| Attack | Telegraph P1 | Mash beaten in P1? | Telegraph P2 | Mash beaten in P2? |
|---|---|---|---|---|
| A | 0.70 s | **yes** (second press lands at 0.55, active at 0.70 — pressed early, still lands, but the window is one press wide) | 0.55 s | **yes** |
| B | 0.60 s | **yes** | 0.48 s | **yes** |
| C | 0.80 s | no — a beginner crutch | 0.62 s | **yes** |
| D | 0.90 s | no — a beginner crutch | 0.70 s | marginal |

Two of four resist the mash in Phase 1 and **they are the two the player meets at close
range**, which is where the fight lives. All four are at or inside the boundary in Phase 2 —
**every Phase 2 telegraph is strictly below 0.75 s**, the value group 03 named as the point
where the lockout starts failing. Group 03 accepted the Phase 1 crutch explicitly; this
distribution confines it to the two attacks the player can also just walk away from.

**Reaction-time floor holds with margin.** Group 03's check was *"against a 0.40 s Phase 2
telegraph the perfect-press window [0.25, 0.37] opens exactly at the ~250 ms average human
reaction time."* The shortest telegraph anywhere in this proposal is **0.48 s** (B, Phase 2),
which is 0.08 s slower than the worst legal case group 03 stress-tested. **No attack in
either phase sits at the reaction-time cliff.**

**Active Attack — hitbox live time.**

- **A = 0.22 s.** One committed gauntlet impact. Short on purpose: a 32-damage hit should be
  a single crisp moment the 0.28 s i-frame window (Q6) can cleanly cover, not a long smear
  that punishes a slightly early dodge.
- **B = 0.36 s.** The only attack the GDD calls a *"sequence"*, so its active state has to
  contain more than one beat. **This is the value most likely to break the fight, and it
  comes with a hard constraint — see Q25.6.**
- **C = 0.30 s.** Long enough that the swept "visible active range" reads as an arc the
  player can see the extent of.
- **D = 0.45 s**, the top of both group 04's mandated 0.40–0.45 band and the GDD's own range.
  Taking the top rather than the middle is deliberate: 600 cm (Q13) in 0.45 s is **1333 cm/s**,
  against 1500 cm/s at 0.40 s. The top of the band is the slowest, most readable, least
  teleport-like value available, and this is the attack under the GDD's no-snap rule.

**Recover — the punish opening, and the attack's price.**

Recovery is authored **inversely to range**, which is the opposite of telegraph, and that is
the point: the two dimensions differentiate the four attacks along different axes instead of
making them four copies at four speeds.

- **A = 0.85 s**, the longest. A is maximally committed, lands closest, and hits hardest, so
  it pays the most. This is the player's primary damage window in the whole duel.
- **B = 0.70 s.** A committed sequence, but one that has already established pressure.
- **C = 0.60 s.** A spacing tool. If C's recovery were long, the rival could not use it to
  hold space, which is its whole stated purpose.
- **D = 0.55 s**, the shortest. **D exists to set up A.** Group 04 authored D to finish
  240 cm from the target — inside A's 0–260 cm band and B's 90–520 cm band. If D's recovery
  were long, the approach would arrive and immediately become free food, and the rival would
  have no way to close distance at all. Short recovery is what makes D a threat rather than
  a gift.

### Q25.5 — Why Active Attack must not be phase-scaled, restated as a proof

The GDD publishes Active as **0.18–0.45 s in both phases**, alone among the timed states.
It does not say why. Here is the reason, and it is load-bearing rather than stylistic:

Phase 2's re-timing ratio in this proposal is **~0.78**. Apply it to Attack D's Active and
0.45 s becomes **0.35 s**. Attack D travels **600 cm** (Q13). 600 cm in 0.35 s is
**1714 cm/s**, against 1333 cm/s in Phase 1 — a **29% increase in apparent travel speed for
the one attack the GDD explicitly forbids from reading as a snap**. Phase-scaling Active
would make Phase 2 violate GDD §04's own readability requirement for Attack D.

**So the GDD's non-scaling of Active is a correctness constraint, not a convenience.** The
developer must not add an `ActiveScale` field to `S_AttackPhaseTuning` "for symmetry" with
`TelegraphScale` and `RecoverScale`. If a field exists, someone will eventually set it.
**Recommendation: `ActiveSeconds` lives on the `DT_VanguardAttacks` row itself, outside both
phase structs, so there is physically no per-phase copy of it to diverge.** That is also the
cleanest possible statement of "Phase 2 is a re-timing of the same four attacks."

### Q25.6 — The constraint Attack B's Active window imposes, which no group has stated yet

Group 02 flagged this as *"the most likely way the table silently produces a broken fight"*:
B is a *sequence*, so it will be authored with **more than one `ANS_ActiveHit` notify**, and
its Data Table `Damage = 25` is the **total** split across them, not per notify.

Q25 adds the timing half of that rule, which group 02 could not state without an Active
value to reason from:

> **B's first hit notify and its last hit notify must be separated by no more than Q6's
> i-frame duration (0.28 s), with margin — author the span at ≤ 0.26 s.**

**Why.** A dodge grants 0.28 s of invulnerability (`ANS_IFrame`, group 03's Q6, spanning
`[0.03, 0.31]` of `AM_Player_Dodge`). If B's beats are spread across the full 0.36 s active
window — say beats at 0.04 and 0.34 — then **no single dodge can avoid both**, and B becomes
an attack that always deals at least half its damage no matter how well the player reads it.
That is not "a committed sequence"; it is an unavoidable hit, and it silently makes B the
rival's best attack at every range it is legal at (90–520 cm — the widest band in the game).

With a 0.36 s active window and a ≤ 0.26 s notify span, a legal authoring is beats at
**0.05 s and 0.29 s**, and a dodge entered ~0.02 s before the first beat covers both. Tight,
readable, and beatable — which is the design.

**This constraint is not a new number the designer must approve. It is a relationship
between two numbers the designer already owns (B's Active and Q6), and the developer should
implement it as an editor-time check, not trust it to authoring discipline.**

### Q25.7 — Derived cycle times, and what they prove

Full cycle = Reposition + Select + Telegraph + Active + Recover + Return to Neutral.

| Attack | **Phase 1 cycle** | **Phase 2 cycle** | Cooldown P1 (Q12) | Cooldown P2 (Q12) |
|---|---|---|---|---|
| A | 0.90+0.15+0.70+0.22+0.85+0.15 = **2.97 s** | 0.55+0.15+0.55+0.22+0.68+0.15 = **2.30 s** | 3.0 s | 2.5 s |
| B | 0.90+0.15+0.60+0.36+0.70+0.15 = **2.86 s** | 0.55+0.15+0.48+0.36+0.56+0.15 = **2.25 s** | 3.5 s | 2.6 s |
| C | 0.90+0.15+0.80+0.30+0.60+0.15 = **2.90 s** | 0.55+0.15+0.62+0.30+0.48+0.15 = **2.25 s** | 3.6 s | 2.7 s |
| D | 0.90+0.15+0.90+0.45+0.55+0.15 = **3.10 s** | 0.55+0.15+0.70+0.45+0.44+0.15 = **2.44 s** | 3.8 s | 2.8 s |

**Every cooldown exceeds its own attack's cycle time in both phases.** That is the healthy
direction — it means the rival can never chain an attack into itself with zero stall, so
variation is forced by the data rather than by a "don't repeat" rule in the Behavior Tree.
Slack in Phase 1: A +0.03 s, B +0.64, C +0.70, D +0.70. In Phase 2: A +0.20, B +0.35,
C +0.45, D +0.36.

**Player punish window per attack** = Recover + Return to Neutral + Reposition + Select
(the span from the end of active frames to the start of the next telegraph):

| Attack | Punish window P1 | Punish window P2 |
|---|---|---|
| A | 0.85 + 1.20 = **2.05 s** | 0.68 + 0.85 = **1.53 s** |
| B | 0.70 + 1.20 = **1.90 s** | 0.56 + 0.85 = **1.41 s** |
| C | 0.60 + 1.20 = **1.80 s** | 0.48 + 0.85 = **1.33 s** |
| D | 0.55 + 1.20 = **1.75 s** | 0.44 + 0.85 = **1.29 s** |

**Group 02's Q5 = 3 sections survives Q25 intact, and this is the strongest confirmation in
the file.** Group 02 derived a 3-section combo (≈ 1.0 s) from GDD midpoints giving a
non-threatening window of *"~1.73 s in Phase 1 and ~1.28 s in Phase 2"*. The authored values
here give **1.75–2.05 s in Phase 1** and **1.29–1.53 s in Phase 2** — marginally more
generous than group 02's midpoint estimate at every attack, so the combo fits everywhere.
And group 02's rejection of a 4-section combo is independently confirmed: a 4-section string
runs ≈ 1.33 s, which **does not fit after C (1.33 s, zero margin) or D (1.29 s) in Phase 2**.

The tightest case in the game is **post-D Phase 2 at 1.29 s against a ~1.00 s combo —
0.29 s of margin**, which is roughly one human reaction time. That is intentional and worth
saying plainly: **after D, the correct play is a partial punish, not a full combo.** D is
the rival's approach; the player who greedily commits three hits after every D will
eventually eat A.

### Q25.8 — Prior art

Direct prior art for per-attack boss timing values is thin, and this file says so rather
than dressing up an estimate.

- **Sekiro: Shadows Die Twice.** The published, community-verified figure is the **12-frame
  (0.20 s at 60 fps) deflect window** — which group 03 already used to justify Q7's 0.12 s.
  Boss *attack* startup and recovery frames are not published by FromSoftware; the available
  material is per-attack video frame-counting by players, not a table. What it does establish
  as a design principle is the one Q25 is built on: **each attack is learned as its own
  timing**, and phase transitions are the largest free punish windows.
  ([Sekiro frame-data playlist](https://www.youtube.com/playlist?list=PLPjQJT7BCKSUXcqsmKc9RZhCpMvxKwJHt), [Sekiro-like boss design writeup](https://medium.com/@menardisaac/making-a-sekiro-like-combat-design-boss-3f2909c6487d))
- **Fighting-game frame data as the authoring convention.** The industry standard is 60 fps
  and one frame = 1/60 s, with attacks decomposed into **startup / active / recovery** — the
  exact three-part split GDD §04 uses under different names (Telegraph / Active Attack /
  Recover). This is why authoring in seconds and validating against ranges is safe: the model
  is the established one. ([Dustloop — Using Frame Data](https://www.dustloop.com/w/Using_Frame_Data), [Understanding Frame Data](https://fightinggameguide.com/framedata.html))
  At 60 fps the Phase 1 values above convert as: **A 42 / 13.2 / 51 frames, B 36 / 21.6 / 42,
  C 48 / 18 / 36, D 54 / 27 / 33.** Ten of the twelve land exactly on a frame boundary. **The
  two that do not are A's and B's Active windows** (0.22 s and 0.36 s), and the designer may
  prefer to snap them to **0.2167 s / 13 frames** and **0.35 s / 21 frames** respectively —
  both still inside the GDD's 0.18–0.45 s range, and 0.35 s still satisfies the Q25.6 span
  constraint. **This is a tidiness question, not a correctness one:** Unreal evaluates anim
  notify states in seconds against a variable frame rate, so a non-integer frame count does not
  break anything. It is flagged because a fighting-game designer will want the numbers to read
  as frames.
- **Not found, and not estimated.** No shipped 3D action game publishes a per-attack table of
  boss windup and recovery durations in seconds. Group 04 reported the same for AI cooldowns
  and group 06 for QTE windows. **The Q25 values are derived from the GDD's own ranges, the
  attacks' stated identities, and the already-proposed Q6/Q7/Q8/Q12/Q13 values — not from a
  shipped comparable.** Treat the *relationships* as the argument and the absolute numbers as
  provisional.

### Q25.9 — The range-validation check the developer must build

`design-brief.md` §13.1 asks for this and it is worth specifying exactly, because it is the
mechanism that lets the designer retune freely without being able to break the GDD:

1. A `UDataAsset` or hardcoded const table holds the **six GDD ranges verbatim**, per state,
   per phase. This is the only place the GDD's numbers appear in code.
2. `UDataTable`'s row-validation path (or an `EditorUtilityBlueprint` run on save) walks every
   `DT_VanguardAttacks` row and, for each of `TelegraphSeconds`, `ActiveSeconds`,
   `RecoverSeconds` in each phase struct, checks `Min <= Value <= Max`.
3. A violation logs an **error with the row name, field name, value, and the range it broke**,
   and fails the check. It does not clamp — clamping would silently produce a fight nobody
   authored.
4. It additionally asserts the three cross-checks this group found:
   **(i)** `ActiveSeconds` has exactly one copy per row and no per-phase variant (Q25.5);
   **(ii)** B's first-to-last hit-notify span ≤ 0.26 s (Q25.6);
   **(iii)** for every row and phase, `Cooldown > full cycle time` (Q25.7) — the anti-chain
   guarantee.
5. If the developer chooses home **(b)** in Q25.0, it also asserts that all four rows carry
   identical Reposition / Select / Return-to-Neutral values.

**This is the deliverable that makes Q25 retunable.** The designer changes a float in a Data
Table; the editor tells them immediately whether they have left the GDD.

### Q25.10 — Interaction with the rest

| Interacts with | How |
|---|---|
| **Q5 / Q4 (combo, group 02)** | Confirmed. 3 sections fit every punish window in both phases; 4 do not fit post-C or post-D in Phase 2. Q25 independently reproduces group 02's finding. |
| **Q6 / Q7 (i-frames, perfect dodge, group 03)** | Q6 = 0.28 s **binds B's Active authoring** (Q25.6). Q7's 0.12 s pocket has more headroom than group 03's stress case — shortest telegraph here is 0.48 s, not 0.40. |
| **Q8 (whiff lockout, group 03)** | Group 03's warning honoured: two of four Phase 1 telegraphs resist the mash, and they are the close-range two. All Phase 2 telegraphs are below 0.75 s. |
| **Q10 (range bands, group 04)** | Telegraph length tracks range band: close = short, far = long. D finishing at 240 cm inside A's band is why D's recovery is shortest. |
| **Q12 (cooldowns, group 04)** | **One real tension — see below.** All eight cooldowns exceed their cycle, but A's Phase 1 slack is only **+0.03 s**. |
| **Q13 (D travel 600 cm, group 04)** | D's Active = 0.45 s gives 1333 cm/s. Also the basis of the Q25.5 proof that Active must never be phase-scaled. |
| **Q2 (rival HP 1200, group 02)** | Untouched. Q25 changes no damage value, so the ~2:53 competent / ~4:29 scrappy gate timings stand. |
| **Q26 (Impact cooldown 7.0 s, group 03)** | Untouched. Note the fastest legal cycle here is 2.25 s, so an Impact opportunity every 7.0 s means roughly **one Impact per three rival cycles** in Phase 2. |
| **Q22 (Clash is the only win, APPROVED)** | Q25's punish windows are the player's meter income. Wider windows than group 02 assumed means meter 100 arrives at or before group 02's ~0:40–1:25, so C3's convergence problem is not made worse. |
| **Q23 (below)** | The cycle times here are the reason a duel timer is unnecessary — see Q23. |

### Q25.11 — The tension this group could not resolve

**A's Phase 1 cooldown (3.0 s, Q12) exceeds A's Phase 1 cycle (2.97 s) by 0.03 s.** In
practice that means: at 0–90 cm, where group 04's bands make **A the only legal attack**, the
rival throws A essentially every 3.0 s, forever, with a 0.03 s stall. At 32 damage that is
**10.7 damage per second against a 100 HP player** if nothing is dodged — death in ~9.4 s.

This is not obviously wrong. It is arguably exactly what "close-range committed armored
pressure" should mean, and A has the longest close-range telegraph (0.70 s) and the longest
recovery (0.85 s) in the game, so the counterplay is present and generous. But it is a fight
state the designer should choose rather than discover, and **it cannot be fixed from inside
Q25** — every legal choice of the six state values puts the full cycle in the 2.8–3.2 s band,
which is within ±0.2 s of Q12's 3.0 s no matter what. The levers are Q12's A cooldown, Q10's
A `MinRange`, or Q3's A damage, all owned by other groups.

**Recommendation to the designer: tune Q12's A cooldown and Q25's A cycle in one session,
and decide deliberately whether point-blank should be a place the player can stand.**

---

## Q18 — BTTask montage failsafe margin

> **REOPENED 2026-08-03 by the cross-consistency inspection.** This section was written as
> KIND A / APPROVED, but its own justification — *"any value in 0.25–0.50 works; 0.35 is the
> middle with a documented reason"* — describes a **designer choice**, not a procedure with
> nothing to decide. **The value breaks no range; the authority was wrong.** Status is now
> **PROPOSED** and `TODO.md` item 29 is restored. The recommendation below stands unchanged.

- **Kind:** ~~A~~ **B** — reclassified 2026-08-03; see the note above
- **Status:** ~~APPROVED~~ **PROPOSED**
- **Unblocks build step:** M2-12 — the `BTTask_*` montage-completion failsafe
- **Value lives in:** each `BTTask_*` (`design-brief.md` §13.2 row 46), as a single shared
  const so there are not six copies
- **GDD range — cited:** **none.** The GDD does not mention a failsafe. It is an artefact of
  the Behavior Tree implementation, not a design surface. `design-brief.md` §14 supplies the
  band to consider: **0.25–0.50 s past montage length.**

### Proposed value

> **`MontageFailsafeMargin = 0.35 s`**, applied as
> `FailsafeTimeout = MontageLength / EffectivePlayRate + 0.35 s`.

**One value, one place.** Put it on `DA_TuningGlobals` as `MontageFailsafeMarginSeconds` and
have every `BTTask_*` read it. Six local copies of an engineering constant is how one of them
ends up at 0.35 and the others at 0.5.

### Why

This is the timer that lets a `BTTask` finish if `OnMontageEnded` / `OnMontageBlendingOut`
never fires — because the montage was interrupted, the mesh was hidden, the anim instance was
reinitialized, or the task was aborted mid-blend. It is a **deadlock breaker**, and the only
two things it must be are: **long enough never to fire on a healthy montage**, and **short
enough that a genuine hang does not read as the rival freezing.**

- **Lower bound.** The rival's own re-timing already changes montage duration: Phase 2 runs
  Telegraph and Recover at roughly **1.28× play rate** (Q25.2), and `Montage_SetPlayRate` plus
  blend-out means the observed end time is not exactly `MontageLength`. A margin below ~0.25 s
  risks firing on a legitimately slow blend-out. **0.25 s is the floor, not a target.**
- **Upper bound.** 0.50 s of a frozen rival is visible. The shortest state in the design is
  0.15 s and the shortest attack cycle is 2.25 s (Q25.7), so half a second of nothing is
  roughly a quarter of a Phase 2 cycle — a player would notice and misread it as a telegraph.
- **0.35 s** sits above the noise floor by 0.10 s and below the visibility ceiling by 0.15 s,
  slightly toward safety-from-false-firing, which is the right bias: a failsafe that fires
  spuriously turns a working rival into a stuttering one, whereas a failsafe that fires 0.1 s
  late costs nothing.

**There is nothing to decide here, which is why this is KIND A.** Any value in 0.25–0.50 works;
0.35 is the middle with a documented reason. If the developer's blend-out settings push
observed montage end past +0.35 s in practice, they should **raise it and log why**, not
silence the failsafe.

### Implementation notes

- The failsafe must **log a warning with the task name and montage name** every time it fires.
  A silent failsafe hides the bug it exists to survive. If it fires in normal play, that is a
  defect to fix, not a margin to widen.
- It must be a **`SetTimer` cleared on the real `OnMontageEnded`**, not a Tick comparison.
- It must **not** be used as the normal exit path for any state. Every `BTTask_*` finishes on
  its notify or its montage delegate; the failsafe only ever finishes a task that failed.
- `BTTask_Idle_Reposition`, `BTTask_SelectAttack` and `BTTask_ReturnToNeutral` have no montage
  to wait on — they run on the Q25.3 delays and need no failsafe at all. The margin applies to
  **`BTTask_Telegraph`, `BTTask_ActiveAttack`, `BTTask_Recover`** only.

### Interaction with the rest

Q18 touches nothing else. It is the only value in this group that is not visible to the player
in any circumstance where the game is working correctly. It does interact with **Q14's
play-rate guard** (group 05): because the rival legitimately uses `Montage_SetPlayRate` for its
Phase 2 re-timing, the failsafe must divide by the **effective** play rate rather than assume
1.0, or it will fire early on every Phase 2 telegraph.

---

## Q23 — Is there a duel timer?

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** M1-09 — `BP_DuelDirector` duel-state setup
- **Value lives in:** `BP_DuelDirector` (`design-brief.md` §13.2 row 51)
- **GDD range — cited:** the GDD gives **"3–5 minutes"** as the *session* figure
  (`gdd/sections/01-executive-summary.md`, PDF p. 1–2, carried into `design-brief.md` §13.1
  row 1 as *"design target, not a timer"*). GDD §03's encounter flow lists exactly **one loss
  condition — player health reaching zero.** There is no time-out row, no draw state, no
  sudden-death, and no clock anywhere in the document.

### Proposed value

> **No duel timer. `BP_DuelDirector` has no countdown, no `RemainingTime` float, no
> `TimeExpired` outcome, and `WBP_HUD` has no clock.** The 3–5 minute figure is a tuning
> target measured in playtest, not a rule enforced at runtime.

**The variable should not exist**, on the same reasoning group 06 gave for Q9's
`MeterDecayRate`: a float that exists gets a default, a default becomes the design, and
nobody remembers deciding it.

### Why

**1. Adding a timer would add a loss condition the GDD does not have.** This is the same
structural argument the designer of record already approved in Q22, pointed the other way.
Q22 was approved *because* the GDD's encounter-flow table lists exactly one win condition, so
reading (a) would have required inventing one. The table also lists exactly one **loss**
condition. A time-out is a second loss condition, and adding it is the same category of act
that Q22 rejected.

**2. Under Q22, a timer is actively dangerous.** Q22 makes the Final Clash the only way to
win. Group 06 established that a failed Clash costs **≈19 s (strong play) to ≈71 s (struggling
play)** to rebuild the meter, and that a competent player can **fail four times and still
finish inside 5:00**. A timer set anywhere near the 3–5 minute target would convert group 06's
carefully-bounded retry loop into a hard fail — *"I fought well, executed the Clash, missed
beat 2, rebuilt the meter, and the clock killed me"* — which is the single worst outcome the
whole Q22 discussion was trying to avoid. **The retry margin group 06 measured only exists
because there is no clock.**

**3. The loss condition already bounds duel length.** This is the load-bearing point and it is
quantitative. With no timer, the pathological case is a player who never dies and never
progresses. Q22's 1 HP floor means they cannot win by attrition — but they also cannot stall,
because **the rival never stops attacking.** Q25.7 gives Phase 1 cycles of 2.86–3.10 s and
Phase 2 cycles of 2.25–2.44 s, and group 02 measured a passive player taking **~118 damage
during a single meter rebuild** against 100 HP (Q1). A player who refuses to engage loses to
the rival, on the rival's clock, without any timer needing to exist. **The duel is bounded by
the rival's aggression, which is authored, which means it is tunable — a timer would be a
second, blunter bound on the same thing.**

**4. It costs schedule.** A timer is UI (clock widget), a state (`TimeExpired`), an outcome
(a third end-of-duel branch alongside win and loss), and tuning. The scope lock names *"one
complete duel with a win and a loss outcome"* — **two** outcomes. A time-out is a third, and
building it is scope creep on a 1 September date.

### Prior art

The prior art here is a **split, and it splits along exactly the line this game sits on.**

- **Timers belong to competitive round-based fighters.** Street Fighter, Tekken and Mortal
  Kombat run 60–99 second rounds because a clock is the anti-turtling device in a
  **symmetric, human-versus-human** contest, where without one a defensive player can refuse
  to engage indefinitely and the *other human* has no authored pressure to force them.
  Ascendant Impact is asymmetric single-player against authored logic, so the rival itself is
  the anti-turtling device.
- **Timers also appear as an authored dramatic device**, not a fairness device — the
  *Time-Limit Boss* pattern, where the clock is the *content* (Persona 5's turn limits,
  Kingdom Hearts' Phantom counting down on Big Ben). ([TV Tropes — Time-Limit Boss](https://tvtropes.org/pmwiki/pmwiki.php/Main/TimeLimitBoss))
  Ascendant Impact's authored dramatic device is already chosen and it is the Final Clash. A
  clock would compete with it.
- **Skill-mastery duels do not use timers.** The soulslike/character-action lineage the GDD's
  core loop actually descends from — read the telegraph, punish the recovery, learn the
  pattern — runs on unbounded encounters, because the design premise is that the player
  **repeats until they master the pattern**, and a clock punishes the learning the game is
  built to teach. FromSoftware boss design is explicitly built around extending the learning
  curve across phases rather than compressing it.
  ([Boss design overview](https://gamedesignskills.com/game-design/game-boss-design/), [soulslike boss design](https://gamerant.com/soulslikes-worth-playing-boss-fights/))
  **Marked as a genre-pattern claim rather than a sourced per-game fact:** I did not find a
  developer statement explaining the absence of timers in these games, and the search returned
  discussion of boss-fight philosophy rather than a citable design rationale. The absence
  itself is easily verified by anyone who has played them; the *stated reason* is not
  published.

### Interaction with the rest

| Interacts with | How |
|---|---|
| **Q22 (APPROVED)** | Q23 = none is the setting that keeps Q22's retry loop survivable. If the designer ever *does* want a timer, Q22's retry economics must be re-derived first. |
| **Q9 (no meter decay, group 06)** | Same family of answer for the same reason — no ambient clock pressure anywhere in the design. A timer would reintroduce through the front door exactly what C1 closed at the back. |
| **Q2 (rival HP 1200, group 02)** | This is where the 3–5 minute target is actually enforced: **by health tuning, not by a clock.** Group 02's ~5:24 scrappy overshoot is a Q2 question, and Q23 = none means the overshoot is a pacing note rather than a loss. |
| **Q25 (above)** | The cycle times are the mechanism that bounds duel length in place of a timer. |
| **M4 outcomes** | `BP_DuelDirector` ships exactly **two** terminal branches: `EndDuel(Win)` from `ClashSuccess()` and `EndDuel(Loss)` from player health reaching zero. No third branch. |

**What the designer might still want, and it is not a timer:** an **elapsed-time readout**
recorded for playtest — logged to file or shown on the debrief screen, never counting down and
never affecting the duel. That measures the 3–5 minute target without enforcing it. It is a
**developer instrumentation** item, and it belongs in M4's playtest tooling, not in the HUD.

---

## Q29 — Crimson Vanguard's short in-combat UI label

- **Kind:** B · **Status:** **PROPOSED** — a recommendation with a shortlist, not a decision
- **Unblocks build step:** M3-04 — the rival health bar and name plate on `WBP_HUD`
- **Value lives in:** `WBP_HUD` (`design-brief.md` §13.2 row 57), as
  `RivalDisplayName : Text`, **shipping blank**
- **GDD range — cited:** this is the one item in this group the GDD **explicitly leaves open
  and explicitly asks to be closed.** `gdd/sections/10-revision-log-and-open-design-decisions.md`
  (PDF p. 16–17), Provisional Design Decisions table, verbatim:
  > *"Crimson Vanguard display name — Use "Crimson Vanguard / Project Valor-7" formally;
  > finalize the shorter in-combat UI label."*

  There is no range and no candidate list. The formal string is fixed; the short form is a
  blank the GDD asks the designer to fill.

### How this relates to the item 45 precedent, and why it differs

Group 05 answered item 45 by shipping `FighterUnitLine` **blank** rather than inventing a
meaning for the "SFN" monogram, and cited Q29 as its precedent. **Q29 should keep half of that
precedent and break the other half**, and the distinction is worth stating precisely because a
future agent will otherwise flatten the two:

| | Item 45 ("SFN") | **Q29 (short rival label)** |
|---|---|---|
| Is there a readable source string? | **No.** A stylised monogram on a sheet with two confirmed typos; group 05 could not establish the letters. | **Yes.** *"Crimson Vanguard / Project Valor-7"*, printed in authored GDD text, fully legible. |
| Does the GDD ask for it to be finalized? | **No.** The GDD never mentions it. | **Yes**, by name, in the Provisional Design Decisions table. |
| Can the build ship without it? | **Yes.** A badge is art; a blank line is invisible. | **No.** A boss health bar with no name is a visible hole in the HUD at M3-04. |
| Correct answer | Ship blank. Invent nothing. | **Ship blank in code, but hand the designer a shortlist and a recommendation** — because the GDD asked for one, and because an unanswered Q29 blocks a visible HUD element rather than an optional flourish. |

So the **build behaviour is identical to item 45** — `RivalDisplayName` is exposed, defaults to
empty, and the developer does not fill it. What differs is that this file does its job and
brings a candidate forward, because *"the designer decides"* is not a useful answer to a
question the source document specifically asked the designer to decide.

### Proposed value

> **Recommendation: `VALOR-7`** (7 characters, upper case, no prefix).
> Full formal name *"Crimson Vanguard / Project Valor-7"* stays on the character-select /
> arena-entrance card and the debrief, so the short form is **taught before it is used**.

Shortlist, with the reasoning that separates them:

| Candidate | Chars | Assessment |
|---|---|---|
| **`VALOR-7`** | **7** | **Recommended.** Unique in the fiction, alphanumeric so it is effectively locale-invariant, comfortably inside the HUD nameplate budget, and it reads as a *unit designation* — which is what the rival is. |
| `CRIMSON VANGUARD` | 16 | The evocative name, and it sits **exactly at the ceiling** of the common 2–16-character nameplate budget before any localization buffer — so it is over budget in practice. Also the weaker read: "Crimson Vanguard" is what the *project* is called, and the HUD is labelling a *unit*. |
| `PROJECT VALOR-7` | 15 | Same width problem, and "PROJECT" carries no information the player needs mid-duel. Better on the entrance card. |
| `VANGUARD` | 8 | Short and clean, but **collides with a role word.** GDD page 14's unit description uses "vanguard" as a job — *"optimized for front-line vanguard operations"* — so "VANGUARD" as a name is ambiguous with "vanguard" as a function. Also a heavily used word elsewhere in the genre. |
| `V-7` | 3 | Too terse. Loses the fiction entirely and reads as a placeholder. |

### Why `VALOR-7`

**1. It is what shipped games in this exact situation do.** The pattern — a machine antagonist
with a formal alphanumeric designation and a spoken name — is well established, and the HUD
consistently carries the **designation**, not the poetry:

- **Titanfall 2 — the closest structural match.** BT-7274's full designation is
  *"Bravo-Tango-Seven-Two-Seven-Four"*; the in-game display and every character in the game use
  **"BT"**. The full designation is established once, then the short form carries the rest of
  the campaign. That is precisely the split the GDD asks for: formal name once, short label
  thereafter. ([Titanfall 2 Wiki — BT-7274](https://titanfall2.fandom.com/wiki/BT-7274), [Titanfall Wiki — BT-7274](https://titanfall.fandom.com/wiki/BT-7274))
- **Armored Core VI.** Boss units are displayed as designation-plus-name:
  **"AAP07: BALTEUS"**, **"IA-13: SEA SPIDER"**, **"IB-01: CEL 240"** — the designation is
  never dropped, because for a machine it *is* the name.
  ([AC6 Wiki — AAP07: BALTEUS](https://armoredcore6.wiki.fextralife.com/AAP07:_BALTEUS), [TV Tropes — AC6 bosses](https://tvtropes.org/pmwiki/pmwiki.php/Characters/ArmoredCoreVIEnemiesAndBosses))
- **Metal Gear Rising: Revengeance.** The unit is formally *"IF Prototype LQ-84i"* and is
  referred to throughout as **LQ-84i**, with "Blade Wolf" as the earned name that arrives
  later. ([Metal Gear Rising Wiki — Blade Wolf / LQ-84i](https://metal-gear-rising.fandom.com/wiki/Blade_Wolf/LQ-84i))
  **Marked unverified:** I did not find a source stating which string appears on that game's
  boss health bar specifically. The designation-forward naming is confirmed; the exact HUD
  string is not.

**2. It fits the width budget, and it is the only candidate that fits it safely.** The common
working range for a HUD nameplate is **2–16 characters**, and localization guidance is to
budget **~30% extra width** for European languages (German routinely needs 30–40% more than
English). `CRIMSON VANGUARD` is 16 — at the ceiling with zero headroom. `VALOR-7` is 7, which
leaves room even if the project later grows a prefix. And because it is an alphanumeric
designation rather than a phrase, **it is the candidate least likely to be translated at all**,
which removes the width risk instead of budgeting for it. Truncation with an ellipsis is the
one outcome to avoid outright — it hides information the player needs.
([Character limits in game localization](https://sandvox.io/glossary/character-limit-localization/), [length limits for UI localization](https://www.smartcat.com/blog/target-length-limit/), [Unreal UIs and localization](https://unreal-garden.com/tutorials/ui-localization/))

**3. It is consistent with what the recovered art actually says the rival is.** Page 14's
unit description calls it *"a high-end, heavily armored tactical mech unit"* (transcription
low-confidence, see item 26), and page 10's own caption for the figure is the generic
**"Villain"** — the sheets carry no character name at all. A unit designation is the label the
source material supports; a proper name is the label it does not.

### The honest counter-argument

`CRIMSON VANGUARD` is the better *title*. It is what the game's own documentation, this
repository, and the player's memory of the select screen will all say. A player who picks a
fighter, watches an entrance titled "Crimson Vanguard", and then sees "VALOR-7" over the
health bar may not immediately connect them.

**The mitigation is the Titanfall mechanism, and it costs nothing:** put the full string
*"CRIMSON VANGUARD / PROJECT VALOR-7"* on the arena-entrance card, which the GDD already
specifies as a beat, and let the combat HUD carry the short form. The player learns the
mapping in the one place there is screen room and no time pressure. **If the designer is not
willing to spend that entrance beat on the full name, then `CRIMSON VANGUARD` is the correct
answer and the width problem has to be solved in the widget instead** — smaller font, or a
two-line plate.

### Implementation notes

- `WBP_HUD` exposes **`RivalDisplayName : Text`**, `BlueprintReadWrite`, **default empty**,
  marked in its tooltip: *"Q29 — pending designer approval. Do not fill in."* Per
  `design-brief.md` §14: *"The developer should expose it as a `Text` variable on `WBP_HUD` and
  leave it blank rather than inventing one."*
- Use **`Text`**, not `String` or `Name`, so it is localizable by default.
- The name plate's `TextBlock` should have **`Auto Wrap Text` off** and a fixed width sized to
  16 characters at the chosen font. Then a too-long candidate fails **visibly in the editor**
  rather than silently at runtime.
- **Nothing else should read this variable.** The formal name belongs on the select screen,
  the entrance card and the debrief; those are separate strings and must not be derived from
  this one, or shortening the HUD label will silently shorten the title card too.
- C2 (from Q22) requires the HUD to show **which Clash gate is still locked**. That indicator
  sits next to this name plate, so both should be laid out in the same M3-04 pass.

### Interaction with the rest

| Interacts with | How |
|---|---|
| **Item 45 (group 05)** | Same build behaviour (ship blank), different reasoning (see the table above). The two should be recorded together so nobody later "fixes" one to match the other. |
| **GDD §10** | This is the only item in group 07 whose resolution would let a line be **struck from the GDD's own open-decisions table.** When the designer approves a label, `design/decisions.md` rule 4 fires: the GDD becomes known-stale and a `TODO.md` item is needed for the PDF re-export. |
| **Assignment #04 content pipeline** | `CLAUDE.md` names this exact gap — *"the **shorter in-combat UI label** for Crimson Vanguard is unfinalized"* — as a candidate Content Fit gap. **A generated candidate is fine as ideation; it does not become the label without designer approval, and nothing in the shipped build reads a generated string.** |
| **M3-04 / M5** | The *string* is M3. The *typography, plate art and animation* are M5 and must not be pulled forward. |

---

## Item 26 — "Plasma-gauntlet weapons" may contradict Attack A

- **Kind:** B · **Status:** **BLOCKED ON HUMAN CONFIRMATION** — deliberately not resolved here
- **Affects build step:** M2-04 — `DT_VanguardAttacks` row A. **Current assessment: no change
  required to M2-04 under any reading.** See below.
- **Value lives in:** nothing yet. There is no variable to set. If the confirmed wording ever
  demands a change it would land in Attack A's VFX (M5) rather than in its data.
- **GDD text — cited, both sides:**
  - **Authored text, `gdd/sections/04-crimson-vanguard-authored-rival-ai.md` (PDF p. 5),
    verbatim:** Attack A is *"Close-range committed gauntlet force"*, readability requirement
    *"Distinct wind-up and punishable recovery"*. The Active Attack state's purpose is
    *"Apply authored movement, gauntlet force, hitbox, reach, or short propulsion."*
    **No ranged or projectile behaviour appears anywhere in GDD §04.**
  - **Image description, `gdd/reference/page-14-crimson-vanguard.md` (PDF p. 14), UNITS
    DESCRIPTION panel, transcription explicitly marked low-confidence:** *"Known for unmatched
    durability and powerful, integrated **plasma-gauntlet weapons**."*
  - **Same file, the gauntlet panel:** *"A **fully enclosed armored fist** … There is no
    visible weapon barrel, blade, or muzzle: the hand *is* the weapon."*

### Step one is not a design decision — it is confirming the wording

`gdd/reference/page-14-crimson-vanguard.md` says so itself, twice:

> *"**Treat this transcription as low-confidence.** Individual words may be misread. It is the
> **only in-world prose about the rival anywhere in the GDD**, so it matters — but it should be
> confirmed against the PDF by a human before being quoted as canon."*

> *"**AMBIGUOUS:** whether "plasma-gauntlet weapons" implies a ranged or energy component. GDD
> §04 describes Attack A only as "close-range committed gauntlet force", and the art shows no
> emitter."*

**So there may be no contradiction at all — there may only be a misread word.** Resolving a
canon conflict from a transcription that the transcription itself disclaims would be inventing
canon, which this file will not do.

### What confirmation is needed, and by whom

**Who:** Adrian, the human designer of record. No agent can do this — the panel is
low-contrast grey-on-pale at a size the extraction pipeline could not read reliably, and the
only remedy is a human looking at the PDF.

**What, precisely — four questions, in order:**

1. Open `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` at **page 14**, zoom the
   **bottom-right "UNITS DESCRIPTION:" panel**, and read the final sentence.
2. **Confirm or correct the two words "plasma-gauntlet".** Plausible misreads at that contrast
   include *plasma / plated / plate*, and *gauntlet / gauntlets*. The word that matters is
   **"plasma"**.
3. **Confirm or correct "Crimson Valor color scheme"** in the same paragraph — flagged
   separately as AMBIGUOUS, and directly relevant to Q29 if it turns out to be a distinct
   in-world term.
4. **Confirm or correct the "REF: Screenshots 2026-07-23 (All timestamps)" line** above the
   stat block, which bears on item 27.

Then record the confirmed sentence in `design/decisions.md` — **not** by editing
`gdd/reference/`, which rule 2 forbids by hand. If the transcription proves wrong, the fix is
to re-read the image and regenerate the description, per rule 2's own instruction.

### The reading that would dissolve the tension — offered, not adopted

There is a reading in which nothing conflicts, and the designer should see it before treating
this as a problem:

> **A "plasma-gauntlet" is plausibly a gauntlet that delivers plasma on contact** — an
> energy-augmented melee weapon — rather than a gauntlet that fires plasma. Under that reading
> *"powerful, integrated plasma-gauntlet weapons"* and *"close-range committed gauntlet force"*
> describe the same thing at different levels of abstraction, and the art agrees: an enclosed
> fist with **two amber indicator lights on the wrist cuff** and a **bright amber-white chest
> core** is exactly what an energy-augmented fist looks like. No emitter is missing, because
> none is needed.

**This is a candidate reading and this file does not adopt it.** It is offered because it is
the cheapest possible resolution and because it would let the designer close the item with a
sentence rather than a redesign.

### What is true regardless of the outcome

**Authored GDD text outranks any image description.** `gdd/INDEX.md`: *"Authored GDD text
outranks any description in these files."* `design/decisions.md` rule 2 says the same about
never writing into `gdd/` what you believe the art should show. So **even if "plasma-gauntlet
weapons" is confirmed verbatim, GDD §04 still governs what Attack A does**, and GDD §04 gives
Attack A no ranged component. A reference sheet cannot add a mechanic.

Concretely, and this is the part the developer needs:

- **Attack A's data does not change under any reading.** Row A keeps `MinRange = 0`,
  `MaxRange = 260` (Q10), `Damage = 32` (Q3), and the Q25 timings above. **M2-04 is not
  blocked by item 26.** Build it.
- **No fifth attack.** A ranged option would be a fifth attack and is forbidden by SCOPE LOCK
  regardless of what the panel says. If the designer ever wants a plasma projectile, it is
  **deferred future scope**.
- **The only thing that could change is presentation, and it is M5.** If "plasma" is confirmed,
  Attack A's impact VFX gains an amber-plasma flash on the gauntlet and the telegraph's warning
  lights read as a charging core. That is an M5 authoring note, gated behind a stable M4, and
  it costs nothing to defer because it changes no timing and no hitbox.
- **It matters most to Assignment #04, not to the game.** This paragraph is the *only in-world
  prose about the rival in the entire GDD*, so the offline content pipeline will lean on it
  hard. **A low-confidence transcription must not become the seed of generated lore.** Confirm
  it before it is used as a retrieval chunk.

### Interaction with the rest

| Interacts with | How |
|---|---|
| **Q25 (above)** | None. A's telegraph 0.70 / active 0.22 / recover 0.85 are unaffected. |
| **Q10 / Q3** | None. A stays a 0–260 cm, 32-damage melee attack. |
| **Q29** | Shares a dependency: question 3 above ("Crimson Valor color scheme") could introduce a fourth naming candidate. Confirm both in one sitting. |
| **Item 27** | Same panel region, same low-contrast problem, same human confirmation pass. **Bundle items 26 and 27 into one five-minute PDF check.** |
| **M5 VFX (group 05 items 43/44)** | Group 05 fixed the rule that *"the rival owns animated emissive, the player owns static or stepped."* A plasma-gauntlet flash sits comfortably inside that rule. |

---

## Item 27 — Page 14's "SYSTEM STATS" map to no system

- **Kind:** B · **Status:** **PROPOSED — non-canonical for gameplay**
- **Affects build step:** M2-04 (as a prohibition, not as a value). Also **item 49**, the
  rival's unspecified `MaxWalkSpeed` — which is the actual trap.
- **Value lives in:** **nothing, and that is the proposal.** No variable, no Data Asset field,
  no Data Table column derives from these four numbers.
- **GDD text — cited:** `gdd/reference/page-14-crimson-vanguard.md` (PDF p. 14), "SYSTEM STATS"
  panel, quoted exactly in that file: **POWER 9/10 · ARMOR 9/10 · MOBILITY 6/10 · SYSTEMS
  7/10**, *"rendered as red-to-orange gradient bars against a dark track."* The same file flags:
  > *"**AMBIGUOUS:** whether "SYSTEM STATS" are intended as gameplay values or as flavour.
  > Nothing in the GDD's authored text references them, and they do not map to any system in
  > `design-brief.md`."*

### Proposed value

> **The four SYSTEM STATS are non-canonical as gameplay values.** They are concept-art
> presentation on a character board. **No number in the build may be derived from them, scaled
> by them, or justified by citing them.** They remain in the GDD, unedited, as art.

### Why

**1. Nothing consumes them, and four separate documents were checked.** They appear in
`gdd/reference/` only. They are referenced by **zero** lines of authored GDD text — GDD §04
(the rival's own section) does not mention POWER, ARMOR, MOBILITY or SYSTEMS; nor does §07
(readability and scale). They map to **no field** in `design-brief.md` §13.1 or §13.2, and to
nothing in `combat-integration-plan.md`. A number that nothing reads is not a specification.

**2. There is no system for three of the four to attach to.** This is the decisive point, and
it is checkable rather than a matter of taste:

| Stat | Would attach to | Does that system exist? |
|---|---|---|
| POWER 9/10 | rival attack damage | **No mapping.** Damage is authored **per attack** — A 32 · B 25 · C 27 · D 18 (Q3). There is no single "power" scalar for 9/10 to be a scalar *of*. |
| ARMOR 9/10 | damage reduction / toughness | **The system does not exist.** The rival has `MaxHealth = 1200` (Q2) and no damage-reduction, resistance, poise or stagger system anywhere in the design. There is nothing for 9/10 to modify. |
| MOBILITY 6/10 | movement speed | **No mapping — see the warning below.** |
| SYSTEMS 7/10 | ? | **Attaches to nothing at all.** There is no "systems" concept in the design. This one is unambiguously flavour, which is strong evidence about the other three. |

**SYSTEMS 7/10 is the tell.** If the four bars were gameplay values, the designer would have
had to have a "systems" mechanic in mind and then never mention it in seventeen pages. The
simpler and far likelier explanation is that all four are the same kind of thing.

**3. That kind of thing has a name.** GDD page 14 is a **character board / model sheet** — a
document whose purpose is *standardizing a character's appearance, poses and gestures* across
production. Its own panel titles say so: HEAD / OPTICS, CHEST / POWER CORE, ORTHOGRAPHIC VIEWS,
ACTION VIGNETTES. **Stat bars on a model sheet are a visual-language convention** — they tell
an artist "this thing should look powerful, armored and not very agile", which is guidance the
sheet's silhouette already delivers. ([Model sheet](https://en.wikipedia.org/wiki/Model_sheet), [character design sheets for video games](https://retrostylegames.com/blog/character-design-sheets-video-game/))
**Marked as an inference:** I found no source stating that stat bars on character boards are
conventionally non-mechanical. The *model-sheet purpose* is sourced; the specific claim about
stat bars is my reading of it.

**4. As art direction they are correct and useful — so keep them.** POWER 9 / ARMOR 9 /
MOBILITY 6 is a precise description of what page 10 shows: a figure *"massively broader than
both others — roughly twice the shoulder width"* whose *"dominance reads as width, not just
height."* And MOBILITY 6/10 is a genuinely good note for whoever animates the rival: **the
rival is not slow, but it is not agile** — which is exactly why the GDD gives it Attack D's
thruster-assisted approach as its *only* explosive movement.

### The warning that matters — MOBILITY 6/10 is not a movement-speed value

**This is the real reason item 27 needed answering, and it is a live risk today.**

**Item 49 is open: the rival's `MaxWalkSpeed` is unspecified.** Group 04 found it and called it
serious — *"under the approved Q22 a rival slower than the player can be kited forever and the
duel cannot end."* Group 04 supplied a lower bound; group 06 supplied an upper bound of
**~1030 uu/s**. There is a missing number, and forty lines away in the source of truth there is
a number labelled MOBILITY.

A future agent will connect them. It must not.

**Every derivation from MOBILITY 6/10 is invention wearing a citation:**

- `0.6 × 600` (player `MaxWalkSpeed`, Q15) = **360 uu/s** — this makes the rival 40% slower than
  the player and **directly triggers the kiting failure group 04 warned about**, which is the
  worst possible outcome, arrived at by the most natural-looking arithmetic.
- `0.6 × 1030` (group 06's ceiling) = **618 uu/s** — arithmetically identical in form, gives a
  completely different answer, and neither is more justified than the other.
- `6/10 of some unstated maximum` — the maximum is unstated, so the calculation has a free
  parameter and can produce anything.

**The stat has no units, no scale, and no stated maximum.** Three different plausible readings
give 360, 618, and undefined. **A number that produces three answers is not a number.**

> **Rule for every downstream agent: item 49 must be resolved from the arena footprint (Q24),
> the range bands (Q10), the cycle times (Q25.7) and the player's own speed (Q15) — the same
> way group 04 and group 06 bounded it. MOBILITY 6/10 is not evidence and must not appear in
> the justification.**

### What "recording it" means, procedurally

**The GDD is not edited.** `design/decisions.md` rule 2: *"`gdd/` is generated and is never
hand-edited… To change what `gdd/` says, change the PDF and re-export."* Item 27 does not want
the GDD changed at all — the sheet is correct as art, and its own file already flags the
ambiguity honestly. What is needed is a **decision recorded outside it**:

1. **`design/decisions.md`** gains an entry (written by the human, not by an agent) stating that
   the four SYSTEM STATS are non-canonical as gameplay values and naming the MOBILITY → item 49
   trap explicitly. That is the file a future agent reads for settled questions.
2. **No `TODO.md` item is created for the GDD being stale**, because rule 4 does not fire — this
   supersedes no GDD line. The GDD says the stats exist, which is true, and says nothing about
   what they mean, which is what is being filled in.
3. **They stay legal as fiction.** The Assignment #04 offline pipeline may use "POWER 9/10,
   ARMOR 9/10, MOBILITY 6/10, SYSTEMS 7/10" as *flavour* in generated unit-dossier or lore text
   — that is the sheet's own register and it reads as authentic. **What is forbidden is a
   gameplay constant.** Flavour in a document, never a float in the build.
4. **Item 26's confirmation pass covers this too:** question 4 there (the "REF: Screenshots"
   line, directly above the stat block) is in the same low-contrast region. If a human is
   already zooming that corner of page 14, they can confirm the four stat values read as
   transcribed while they are there.

### Interaction with the rest

| Interacts with | How |
|---|---|
| **Item 49 (rival `MaxWalkSpeed`)** | **The whole point.** MOBILITY 6/10 is fenced off so item 49 gets derived properly. |
| **Q2 (rival HP 1200)** | ARMOR 9/10 does **not** justify raising it. Q2 is derived from the 3–5 minute session target; group 02 owns it. |
| **Q3 (per-attack damage)** | POWER 9/10 does **not** justify raising it. Damage is per attack and budgeted against player HP 100 (Q1). |
| **Q25 (above)** | MOBILITY 6/10 does **not** justify slowing the rival's states. Every Q25 value is inside a published GDD range and derived from the attacks' stated identities. |
| **Item 26** | Same panel, same page, same human confirmation pass. Bundle them. |
| **Assignment #04** | Legal as flavour, forbidden as a constant. The critic agent is the natural place to enforce that line. |

---

## Item 28 — Crimson Vanguard's height in centimetres

- **Kind:** **A** — a transcription from the GDD, not an invention
- **Status:** **APPROVED**
- **Affects build step:** M2-05 — spawn and scale `BP_CrimsonVanguard`
- **Value lives in:** `BP_CrimsonVanguard` mesh scale (`design-brief.md` §13.1 row 28)
- **GDD text — cited:** `gdd/reference/page-10-character-scale-reference.md` (PDF p. 10)
  records the printed height caption on the right-hand figure, quoted exactly:
  **`"6'10" (208 cm)"`**. GDD §07 authored text supplies the name mapping
  (*"Crimson Vanguard stands 6'10""*).

### Proposed value

> **`208 cm`.** `design-brief.md` §13.1 row 28 becomes **6'10" / 208 cm**, matching the form of
> rows 26 (Echo, 6'0" / 183 cm) and 27 (Nova, 5'8" / 173 cm).

### Why — there was never a decision here

Row 28's blank was **not** a design question. The centimetre figure was printed in the GDD all
along, on page 10, and was simply unreadable until the page-14/page-10 image recovery on
2026-08-02. Nothing is being chosen.

The arithmetic confirms the transcription and confirms it rounds the same way as the other two:

| Character | Feet/inches | Inches | × 2.54 | Printed | Consistent? |
|---|---|---|---|---|---|
| Nova | 5'8" | 68 | 172.72 | **173 cm** | yes |
| Echo | 6'0" | 72 | 182.88 | **183 cm** | yes |
| **Vanguard** | **6'10"** | **82** | **208.28** | **208 cm** | **yes** |

All three round to the nearest centimetre. 208 is not an approximation someone made — it is
the correct conversion, printed on the sheet, in the same style as the other two.

### Implementation notes

- `design-brief.md` §12.4's M2 baseline is *"UE5 Mannequin scaled to 208 cm"*, so this value
  was already the intended target; it just had no cited source until now. **Uniform scale
  only** — non-uniform scaling breaks the retarget and distorts reach.
- **Scale the capsule by the same factor as the mesh.** `CapsuleHalfHeight` and
  `CapsuleRadius` must both move, or the collision will not match the silhouette.
- **Then re-validate reach.** GDD §07's requirement is a hard rule: *"The height difference
  must not create unfair hidden reach or collision behavior."* Attack trace sockets and every
  `MinRange`/`MaxRange` in Q10 are measured **centre-to-centre**, so they survive a scale
  change — but the *visual* reach at 208 cm must still agree with them. §12.4 says this
  re-validation is required after **any** mesh swap, and a scale change is a mesh change.
- Page 10 prints **height only**. There is no width or depth measurement anywhere in the GDD —
  the sheet's own file flags that as AMBIGUOUS. So **capsule radius is still unspecified**, and
  page 10's *"roughly twice the shoulder width of the centre figure"* is a description, not a
  measurement. **Do not derive a radius from it.** That is a separate open value and it belongs
  with item 49's cluster of missing rival numbers.

### Interaction with the rest

| Interacts with | How |
|---|---|
| **§13.1 rows 26/27** | Row 28 now matches their form. The three-way scale comparison in GDD §07 becomes checkable in centimetres. |
| **Q10 (range bands)** | Bands are centre-to-centre, so they do not change. Visual reach must be eyeballed against them once at M2-05. |
| **Q11 (lock-on, group 04)** | Group 04's aim socket at **140 cm, −8°** was authored for the rival. At 208 cm total height, 140 cm is roughly two-thirds up the body — chest-core height, which is where page 14 puts the brightest emissive point. **Consistent; no change needed.** |
| **Item 49 / capsule radius** | Height is now known; **width is still not.** Those belong to the same tuning session. |

---

## Range compliance table

**Purpose: let an inspector check Q25 without reconstructing anything.** Every one of the
twenty-six values proposed in Q25 appears below, next to the GDD range it must fall inside,
with an explicit verdict. The ranges are quoted verbatim from
`gdd/sections/04-crimson-vanguard-authored-rival-ai.md` (PDF p. 5) and are **unchanged** — this
group proposes values inside them and rewrites none of them.

**Comparison rule: inclusive on both ends — `Min <= Value <= Max`.** This matters for exactly
one cell (Attack D's Active at 0.45 s, the published upper bound) and is called out again below.

### Per-attack — Telegraph

| Attack | Phase | Value | GDD range | Verdict | Headroom below / above |
|---|---|---|---|---|---|
| A | 1 | 0.70 s | **0.55–0.95 s** | **IN RANGE** | −0.15 / +0.25 |
| B | 1 | 0.60 s | **0.55–0.95 s** | **IN RANGE** | −0.05 / +0.35 |
| C | 1 | 0.80 s | **0.55–0.95 s** | **IN RANGE** | −0.25 / +0.15 |
| D | 1 | 0.90 s | **0.55–0.95 s** | **IN RANGE** | −0.35 / +0.05 |
| A | 2 | 0.55 s | **0.40–0.75 s** | **IN RANGE** | −0.15 / +0.20 |
| B | 2 | 0.48 s | **0.40–0.75 s** | **IN RANGE** | −0.08 / +0.27 |
| C | 2 | 0.62 s | **0.40–0.75 s** | **IN RANGE** | −0.22 / +0.13 |
| D | 2 | 0.70 s | **0.40–0.75 s** | **IN RANGE** | −0.30 / +0.05 |

### Per-attack — Active Attack (one value per attack, both phases)

The GDD publishes **0.18–0.45 s for Phase 1 and Phase 2 identically**. Q25.5 proposes there be
only one stored copy per attack, so each row below is simultaneously the Phase 1 and the
Phase 2 value and is checked against both published ranges — which are the same range.

| Attack | Phase | Value | GDD range | Verdict | Headroom below / above |
|---|---|---|---|---|---|
| A | 1 & 2 | 0.22 s | **0.18–0.45 s** | **IN RANGE** | −0.04 / +0.23 |
| B | 1 & 2 | 0.36 s | **0.18–0.45 s** | **IN RANGE** | −0.18 / +0.09 |
| C | 1 & 2 | 0.30 s | **0.18–0.45 s** | **IN RANGE** | −0.12 / +0.15 |
| D | 1 & 2 | **0.45 s** | **0.18–0.45 s** | **IN RANGE — on the inclusive upper bound** | −0.27 / **+0.00** |

**The one boundary value in the whole proposal, and it is deliberate.** Attack D's Active sits
exactly at the published maximum, 0.45 s, because group 04 mandated 0.40–0.45 s and 0.45 is the
slowest — therefore most readable — legal crossing of Q13's 600 cm. It is **in range under an
inclusive comparison** and would be out of range under a strict one, so the validation check
(Q25.9) must use `Min <= Value <= Max`. **It has zero upward tuning headroom:** if playtest says
D still reads as a teleport, the lever is Q13's 600 cm travel distance, not this value.

### Per-attack — Recover

| Attack | Phase | Value | GDD range | Verdict | Headroom below / above |
|---|---|---|---|---|---|
| A | 1 | 0.85 s | **0.45–0.90 s** | **IN RANGE** | −0.40 / +0.05 |
| B | 1 | 0.70 s | **0.45–0.90 s** | **IN RANGE** | −0.25 / +0.20 |
| C | 1 | 0.60 s | **0.45–0.90 s** | **IN RANGE** | −0.15 / +0.30 |
| D | 1 | 0.55 s | **0.45–0.90 s** | **IN RANGE** | −0.10 / +0.35 |
| A | 2 | 0.68 s | **0.35–0.75 s** | **IN RANGE** | −0.33 / +0.07 |
| B | 2 | 0.56 s | **0.35–0.75 s** | **IN RANGE** | −0.21 / +0.19 |
| C | 2 | 0.48 s | **0.35–0.75 s** | **IN RANGE** | −0.13 / +0.27 |
| D | 2 | 0.44 s | **0.35–0.75 s** | **IN RANGE** | −0.09 / +0.31 |

### Duel-level states — one value per phase, not per attack

| State | Phase | Value | GDD range | Verdict | Headroom below / above |
|---|---|---|---|---|---|
| Idle / Reposition | 1 | 0.90 s | **0.60–1.20 s** | **IN RANGE** | −0.30 / +0.30 |
| Idle / Reposition | 2 | 0.55 s | **0.35–0.80 s** | **IN RANGE** | −0.20 / +0.25 |
| Select Attack | 1 | 0.15 s | **0.10–0.20 s** | **IN RANGE** | −0.05 / +0.05 |
| Select Attack | 2 | 0.15 s | **0.10–0.20 s** | **IN RANGE** | −0.05 / +0.05 |
| Return to Neutral | 1 | 0.15 s | **0.10–0.20 s** | **IN RANGE** | −0.05 / +0.05 |
| Return to Neutral | 2 | 0.15 s | **0.10–0.20 s** | **IN RANGE** | −0.05 / +0.05 |

### Verdict

| Check | Result |
|---|---|
| Values proposed | **26** |
| **IN RANGE** | **26 / 26** |
| **OUT OF RANGE** | **0** |
| On an inclusive boundary | **1** — Attack D Active, 0.45 s = published max (deliberate; see above) |
| GDD ranges altered | **0** |
| GDD ranges collapsed to a single number | **0** — every published range is reproduced intact and remains the range |
| Active Attack phase-scaled | **No.** One value per attack, identical in both phases, per the GDD |
| Values sitting below a range minimum | **0** |
| Values sitting above a range maximum | **0** |

**Group-03 and group-04 constraint compliance, restated for the inspector:**

| Constraint | Required | Delivered | Pass |
|---|---|---|---|
| Group 04 — A and B short | 0.55–0.70 s | A **0.70**, B **0.60** | **yes** |
| Group 04 — C and D long | 0.75–0.95 s | C **0.80**, D **0.90** | **yes** |
| Group 04 — D's Active | 0.40–0.45 s | **0.45** | **yes** |
| Group 03 — not all four telegraphs near 0.95 s | spread, not clustered | 0.60 / 0.70 / 0.80 / 0.90 — spread across 0.30 s, one attack above 0.85 | **yes** |
| Group 03 — Phase 2 telegraphs below the 0.75 s lockout-failure point | < 0.75 s | 0.48 / 0.55 / 0.62 / 0.70 — all below | **yes** |

### Every number in this group, in one list — all PROVISIONAL and PENDING PLAYTEST

| Item | Field | Value | Home | Range it sits in |
|---|---|---|---|---|
| Q25 | `Phase1.TelegraphSeconds` A / B / C / D | 0.70 / 0.60 / 0.80 / 0.90 s | `DT_VanguardAttacks` | GDD 0.55–0.95 |
| Q25 | `Phase2.TelegraphSeconds` A / B / C / D | 0.55 / 0.48 / 0.62 / 0.70 s | `DT_VanguardAttacks` | GDD 0.40–0.75 |
| Q25 | `ActiveSeconds` A / B / C / D (both phases) | 0.22 / 0.36 / 0.30 / 0.45 s | `DT_VanguardAttacks`, **row-level, no phase copy** | GDD 0.18–0.45 |
| Q25 | `Phase1.RecoverSeconds` A / B / C / D | 0.85 / 0.70 / 0.60 / 0.55 s | `DT_VanguardAttacks` | GDD 0.45–0.90 |
| Q25 | `Phase2.RecoverSeconds` A / B / C / D | 0.68 / 0.56 / 0.48 / 0.44 s | `DT_VanguardAttacks` | GDD 0.35–0.75 |
| Q25 | `RepositionDelay` P1 / P2 | 0.90 / 0.55 s | `DA_TuningGlobals` (preferred) | GDD 0.60–1.20 / 0.35–0.80 |
| Q25 | `SelectDelay` P1 / P2 | 0.15 / 0.15 s | `DA_TuningGlobals` (preferred) | GDD 0.10–0.20 |
| Q25 | `ReturnToNeutralDelay` P1 / P2 | 0.15 / 0.15 s | `DA_TuningGlobals` (preferred) | GDD 0.10–0.20 |
| Q25.6 | B first-to-last hit-notify span | **≤ 0.26 s** (constraint, not a free value) | `AM_Vanguard_AttackB` | bounded by Q6 = 0.28 s |
| Q18 | `MontageFailsafeMarginSeconds` | **0.35 s** | `DA_TuningGlobals` | §14 band 0.25–0.50 |
| Q23 | duel timer | **none — no variable** | `BP_DuelDirector` | GDD has no clock |
| Q29 | `RivalDisplayName` | **blank in build**; recommended `VALOR-7` | `WBP_HUD` | GDD asks for finalization |
| 27 | SYSTEM STATS as gameplay constants | **none — non-canonical** | nowhere | — |
| 28 | Crimson Vanguard height | **208 cm** | `BP_CrimsonVanguard` mesh scale | GDD-printed, 6'10" |

---

## Research note

**11 of 15 searches used.** Budget spent as instructed, on Q25 and Q29.

**What the searches did and did not establish.** Q29 is the best-sourced item in the file:
Titanfall 2, Armored Core VI and Metal Gear Rising all confirm the designation-forward naming
pattern, and the HUD width and localization-buffer figures are sourced. Q25's *model* is
sourced — startup / active / recovery at 60 fps is the established authoring convention — but
**no shipped 3D action game publishes a per-attack table of boss telegraph and recovery
durations in seconds**, which is now the third group in a row to report that (group 04 for AI
cooldowns, group 06 for QTE windows). **The Q25 absolute values are therefore derived from the
GDD's own ranges and the already-proposed Q3/Q6/Q8/Q10/Q12/Q13 values, not from a comparable.**
Item 27's "stat bars on a character board are conventionally flavour" is explicitly marked as
my inference from the sourced definition of a model sheet, not as a sourced claim. Q23's
"skill-mastery duels do not use timers" is marked as a genre pattern rather than a cited
developer rationale.

**Four unresolved things, named rather than closed:**

1. **Attack A's Phase 1 cycle (2.97 s) and Q12's A cooldown (3.0 s) differ by 0.03 s**, which
   makes point-blank a place where A repeats almost every cycle at 32 damage. It cannot be fixed
   from inside Q25 — every legal cycle lands in 2.8–3.2 s. **Q12 and Q25 must be tuned together.**
2. **Item 26 cannot be resolved by any agent.** It needs a human to zoom page 14 of the PDF.
   Bundle it with item 27's stat-block confirmation — one five-minute check answers four
   questions.
3. **Q29's recommendation trades evocativeness for width.** `VALOR-7` is the safe engineering
   answer; `CRIMSON VANGUARD` is the better title and needs a widget solution. The designer is
   choosing between those two, not between five.
4. **Attack D's Active has zero upward headroom** at 0.45 s. If D still reads as a snap in
   playtest, the only remaining lever is Q13's 600 cm — which belongs to group 04.

*Every value above is provisional and pending playtest. The human designer owns all of them.
Nothing in this file supersedes a GDD line, and no GDD number or range was altered.*
