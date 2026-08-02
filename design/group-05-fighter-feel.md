# Group 05 — Fighter feel and character presentation · Q14, Q15, Q16 + items 43, 44, 45

**Dispatched:** 2026-08-02 · designer agent, group 05 of the open-question sweep.
**Consumes:** `gdd/INDEX.md`, `gdd/sections/02-real-time-combat-and-selectable-player-roster.md`
(the SHARED PLAYER-KIT SCOPE RULE), `gdd/sections/07-character-readability-scale-and-opening-flow.md`,
`gdd/sections/10-revision-log-and-open-design-decisions.md`,
`gdd/reference/page-12-agent-echo.md`, `gdd/reference/page-13-agent-nova.md`,
`gdd/reference/OPEN-QUESTION-IMPACT.md` §3 and §6, `design-brief.md` §13.2 rows 42–44
and §14 "Fighter feel", `design/decisions.md` (Q22 APPROVED, groups 02, 03, 04).
**Produces:** answers to **Q14, Q15, Q16** and to the three new questions the recovered
character sheets raise — **item 43** (Echo's faceplate), **item 44** (Echo's energy
lines), **item 45** ("SFN"). Nothing else.

> **EVERY ANSWER IN THIS FILE IS `PROPOSED`, NOT DECIDED.**
> All six items are **KIND B** design items. A designer dispatch researches and
> recommends; it does not settle. The human designer of record owns every value here.
> Each entry stays open in `TODO.md`, marked PROPOSED, until the designer approves or
> changes it.

---

## The governing constraint on Q14 — group 03's warning, stated up front

`design/decisions.md`, group 03, 2026-08-02, issued this **three separate times**:

> "Three separate warnings that Q14's `MontagePlayRate` would silently scale Q6 and Q7
> into per-fighter difficulty — Q28 is the only one of the three that scales correctly."

This is the single most important input to this file, so it is stated before any answer.

**The mechanism.** Group 03 authored the dodge i-frame window (**Q6 = 0.28 s**) and the
perfect-dodge sub-window (**Q7 = 0.12 s**, spanning `[0.03, 0.15]`) as **Anim Notify
States placed on `AM_Player_Dodge`**. An Anim Montage's play rate is a **time scalar on
the entire montage**: the montage's internal timeline advances at `PlayRate × DeltaTime`,
so every notify state on it begins earlier and lasts a shorter wall-clock time. A notify
state authored to occupy 0.12 s of montage time occupies `0.12 / PlayRate` seconds of
real time.

**The consequence, in numbers.** If Echo runs `MontagePlayRate = 1.00` and Nova runs
`1.10`, then:

| Fighter | `PlayRate` | Q6 i-frames, real time | Q7 perfect dodge, real time |
|---|---|---|---|
| Echo | 1.00 | 0.280 s | 0.120 s |
| Nova | 1.10 | 0.255 s | 0.109 s |
| Nova | 1.15 | 0.243 s | 0.104 s |
| Nova | 0.90 | 0.311 s | 0.133 s |

A 10% play-rate split is a **9% swing in the hardest execution window in the game**.
Group 03 called Q7 *"the single number that does more to define the game's difficulty
than any other in the table."* Splitting it per fighter is **per-fighter difficulty**,
and the SHARED PLAYER-KIT SCOPE RULE defers *"separate balance systems"* until the base
duel is stable. **This is not a feel decision. It is a scope violation wearing a feel
decision's clothes.**

**Why the same is true of the offensive montage, which group 03 did not have to say.**
Q28 (combo input buffer) was authored as a **ratio** — 0.25 s = 75% of a section — so it
does scale correctly; the buffer stays 75% of a section at any rate. But the *combo
itself* does not. Group 02 fixed the light combo at **3 sections, ~1.0 s, 20 damage
total**. Damage per combo is fixed; combo *duration* is not. A fighter with
`PlayRate = 1.10` completes the same 20 damage and the same **+5** meter finisher in
0.91 s instead of 1.00 s — roughly **+10% damage per second and +10% meter per second**,
for free. Against Q2 = 1200 rival health that is on the order of 15–25 seconds off the
duel. That is a balance split too.

**The finding this group reaches:** there is **no montage in the player kit where play
rate is purely cosmetic.** Every player montage either carries a defensive notify window
(dodge, counter, Impact, Clash) or converts directly into damage-per-second and
meter-per-second (light combo). The answer to Q14 follows from that, and is given below.

---

## Binding context

### Q22 is APPROVED and binding

`design/decisions.md`, 2026-08-02: `MinHealthFloor = 1` on the rival from `BeginPlay`,
lowered to `0` only by `ClashSuccess()`. **The Final Clash is the only way to win, and
the Ascension Meter is therefore the only route to the ending.**

Two consequences land squarely on this group:

1. **Meter is the win condition's currency**, so anything that changes meter-per-second
   changes the length and difficulty of the duel. That is why Q14 is treated as a balance
   value here and not a flavour value.
2. **Condition C2 — the HUD must show which gate is still locked** once the health bar
   visibly pins at 1 HP. Items 43 and 44 propose putting a *second, on-character* reading
   of that same state in the player's field of view. That is a **redundant** channel, and
   the file says explicitly below that it must never be the only one.

### Values from groups 02, 03 and 04 — PROPOSED, used as inputs here

Player health **100** (identical both fighters) · rival health **1200** · combo
**3 sections, ~1.0 s, 20 damage** · i-frames **0.28 s** · perfect dodge **0.12 s** ·
counter whiff lockout **0.55 s** · combo buffer **0.25 s (75% of a section)** · arena
**2400 × 1600 cm**, diagonal ≈ 2884 cm · rival attack bands centre-to-centre
**A 0–260 · B 90–520 · C 240–420 · D 400–840 cm** · attack D travel **600 cm** ·
lock-on acquire **3000 cm** / break **3300 cm**.

If any of these move, Q15 and Q16 move with them — they are spacing values and they were
derived against group 04's footprint and bands. Q14 does not depend on any of them.

### What the GDD authorises, quoted

- **SHARED PLAYER-KIT SCOPE RULE** (§02, PDF p.2–3): Echo and Nova *"share the same
  prototype framework: movement, lock-on, light attack sequence, dodge, perfect dodge,
  counter, health, Ascension Meter, Impact Windows, and Final Clash. Their initial
  differences are animation presentation, stance and movement personality, VFX language,
  timing flavor, and character introduction. Fully unique move sets, separate balance
  systems, and extensive character-specific cinematics are deferred until the base duel
  is stable."*
- **Provisional Design Decisions** (§10, PDF p.16–17), row *Echo / Nova timing flavor*:
  *"Use the same mechanics and balance framework; approve only presentation-level timing
  flavor at first."*
- **REVISED — COLOR DIRECTION** (§07, PDF p.8): *"Echo keeps restrained orange accents.
  Nova's existing black, charcoal, orange, and light-gray costume design is preserved;
  cyan-white is reserved for combat energy, telegraphs, or selected VFX accents when
  separation is needed."*
- **Readability targets** (§07): Echo — *"Exact timing and clear counter intent."*
  Nova — *"Momentum without visual noise."*

The operative phrase for this whole group is **"presentation-level timing flavor."** The
question every answer below has to survive is: *is this presentation, or is it balance?*

---

## Q14 — Echo / Nova montage play-rate ("timing flavor")

- **Kind:** B · **Status:** PROPOSED
- **Unblocks build step:** M1-12 (author `DA_FighterProfile_Echo` / `DA_FighterProfile_Nova`)
- **Value lives in:** `DA_FighterProfile.MontagePlayRate` — `design-brief.md` §13.2 row 42
- **GDD range:** **none published.** The GDD authorises *"timing flavor"* as a category
  (§02 shared-player-kit rule; §10 *"approve only presentation-level timing flavor at
  first"*) and gives no number, no ratio, and no bound.

### Proposed value

**`MontagePlayRate = 1.000` for Echo and `1.000` for Nova. Identical. No split in
Phase 1, and no split at any point before the base duel is stable.**

Together with a structural guard, because a value of 1.0 today does not stop somebody
typing 1.1 in the editor next week:

1. **Rename the field `CosmeticMontagePlayRate`.** A name that says what it is allowed to
   touch is worth more than a comment. The developer should also add a
   `UPROPERTY` tooltip: *"Never applied to a montage that carries a gameplay notify
   window. See design/group-05."*
2. **Restrict its consumers to a named allowlist.** It may be read **only** when playing
   montages that carry **no** gameplay notify state and resolve no timing:
   - `AM_Fighter_SelectIdle` (character-select screen pose)
   - `AM_Fighter_ArenaEntrance` (the abbreviated opening, §10.1)
   - `AM_Fighter_Victory` / `AM_Fighter_Defeat` (result screens)
   That is the whole list. **It is never read by** `AM_Player_LightCombo`,
   `AM_Player_Dodge`, `AM_Player_Counter`, `AM_Player_CounterWhiff`, any Impact Window
   burst montage, or any Final Clash montage.
3. **Make the guard testable.** One `Blueprint Function Library` node,
   `PlayFighterMontage(Montage, bCosmetic)`, is the only place `Montage_SetPlayRate` is
   ever called with a value other than 1.0, and it `ensure()`s that a montage passed
   with `bCosmetic = true` carries zero notify states of the gameplay classes
   (`ANS_IFrame`, `ANS_PerfectDodge`, `ANS_ActiveHit`, `ANS_ComboLink`,
   `ANS_CounterWindow`). A designer who wires a gameplay montage into the cosmetic path
   gets an editor warning, not a silent balance change.

Even inside the allowlist, **1.000 / 1.000 is the recommended Phase 1 value.** The
allowlist exists so the field is *safe*, not so it gets used.

### Why

**Because there is no montage in the player kit where play rate is purely cosmetic.**
That is the whole argument and it is worth stating in three parts.

**1. On the defensive montages it is difficulty.** Detailed at the top of this file: a
play-rate split moves Q6 and Q7 by the same percentage, and Q7 is the number group 03
identified as the game's difficulty dial. Group 03 also warned that Q7's repeatability
by a human hand is *unverified* — the perfect-dodge pocket's onset was proven reachable
against a 0.40 s Phase 2 telegraph, but nobody has shown a player can hit 0.12 s
repeatably. **Shrinking an unverified window by 9% for one of two selectable fighters is
the worst possible place to spend the differentiation budget.** If Q7 turns out to be
too tight in playtest, a play-rate split means it is too tight *for one character*, and
the designer is then debugging two problems that look like one.

**2. On the offensive montage it is damage per second.** Group 02 fixed the light combo
at 3 sections, ~1.0 s, 20 total damage, +5 meter on the finisher. Damage and meter per
combo are constants; only the duration moves. A 1.10 play rate is therefore
approximately **+10% DPS and +10% meter/s**, and under the approved Q22 the meter is the
only route to the ending. That is a balance split, and *"separate balance systems"* are
deferred by name.

**3. There is a second, quieter failure.** Group 02's load-bearing finding is that the
rival's cycle leaves a non-threatening window of **~1.28 s in Phase 2**, and a 3-section
combo at ~1.0 s fits it with **0.28 s of slack**. A play rate below ~0.78 would push the
combo out of the Phase 2 window entirely and the slower fighter would simply lose access
to her finisher — and therefore to the **+5** meter row — for the back half of the duel.
The safe band is wide, but the failure at the bottom of it is total rather than gradual,
and it would present in playtest as "Nova feels bad in Phase 2" rather than as a number.

**Prior art says the split is not needed anyway.** See below: the strongest historical
examples of two characters reading as different people are examples where the underlying
timing was *identical* and only the presentation changed.

### Prior art (real games, named)

- **Super Smash Bros. Ultimate — Peach and Daisy.** Daisy is Nintendo's own
  "Echo Fighter": after patching, the two have **identical frame data**, and the
  differentiation is carried almost entirely by presentation — Daisy's effects are
  **orange flowers and petals** where Peach's are **pink hearts**, her Toad is a
  different colour, her Final Smash swaps the prop. Community and competitive
  consensus treats them as interchangeable, and nobody argues they look like the same
  character. This is the closest published analogue to what the GDD is asking for:
  *same framework, different presentation.*
  **One caveat that matters here more than in Smash:** the one difference that survived
  patching is **height** — Daisy is slightly shorter, which changes her hurtbox. Echo is
  183 cm and Nova is 173 cm, a **10 cm published difference**, so Ascendant Impact
  already has the exact residual asymmetry Smash could not eliminate. That is discussed
  under "Differentiation budget" below and it is a live issue for the GDD's *"must not
  create unfair hidden reach or collision behavior"* requirement.
- **Mortal Kombat (1992–93) — the palette-swap ninjas.** Scorpion, Sub-Zero, Reptile,
  Smoke and Noob Saibot were **literally the same digitised sprite recoloured** — one
  motion-capture costume, re-tinted. They are among the most durable character identities
  in the genre. The differentiation that made them distinct characters was *special moves
  and colour*, not the shared animation base. The lesson for this project is the
  converse of MK's: Ascendant Impact **cannot** differentiate via unique moves (scope
  lock), so it must differentiate via the two channels MK proved were sufficient on their
  own — **silhouette and colour** — and the recovered sheets have already done that far
  more thoroughly than a recolour.
- **Tekken 8 — Heat.** Not a play-rate case, but the relevant discipline: Heat state is
  signalled by a **light-blue aura on the character** *and* a bar under the health bar.
  Note also the community complaint the search surfaced — that Tekken 8's effects volume
  makes animations harder to read. That is a direct warning against Nova's readability
  target, *"momentum without visual noise."*

### Interaction with the rest

| Touches | Effect at the proposed value |
|---|---|
| **Q6 = 0.28 s, Q7 = 0.12 s** (group 03) | **Protected.** At 1.0 both fighters get the authored window exactly. See the dedicated closing section. |
| **Q28 = 0.25 s combo buffer** (group 03) | Unaffected either way — group 03 authored it as a **ratio** (75% of a section), which is the one of the three that scales correctly. |
| **Q4 / Q5 / Q2** (group 02) | Unaffected. Combo duration stays ~1.0 s for both, so the Q2 = 1200 derivation and the ~1.28 s Phase 2 fit both hold for Echo *and* Nova with no second set of arithmetic. |
| **Q22 (APPROVED)** | Meter is the only win route; identical play rate means both fighters reach the gate on the same schedule and C3's "meter and health gate arrive close together" only has to be checked once. |
| **M1-12** | Unblocked. Two data assets, same number, no per-fighter validation pass needed. |
| **Testing cost** | This is the quiet win. At 1.0/1.0 the GDD safeguard — *"validate gameplay collision and hit reach only after both avatars pass the same close-range tests"* — is **one** test pass, not two. At 38 days to ship that is not a small saving. |

---

## Q15 — Echo / Nova `MaxWalkSpeed`

- **Kind:** B · **Status:** PROPOSED
- **Unblocks build step:** M1-12
- **Value lives in:** `DA_FighterProfile` (`MaxWalkSpeed`, applied to
  `CharacterMovementComponent` in `ApplyFighterProfile`) — `design-brief.md` §13.2 row 43
- **GDD range:** **none published.** §07 gives movement *personality* only — Echo
  *"deliberate spacing and counters"*, Nova *"fast lateral rhythm and forward intent"* —
  and no speed value anywhere in the document.

### Proposed value

**Identical for both fighters:**

| Sub-value | Proposed | Band | Notes |
|---|---|---|---|
| `MaxWalkSpeed`, free movement (lock-on off) | **600 uu/s** | 500–650 | uu = cm, so 6.00 m/s |
| Locked-on strafe speed | **420 uu/s** (0.70 ×) | 0.65–0.75 × | **no §13.2 row exists — see gap below** |
| Locked-on backpedal | **360 uu/s** (0.60 ×) | 0.55–0.65 × | **no §13.2 row exists — see gap below** |

The UE5 Third Person template ships `MaxWalkSpeed = 500`; **600 is a deliberate 20% step
above the template default**, so the developer should expect to change it rather than
inherit it. *(The 500 figure is community-documented rather than quoted from an Epic
docs page — treat as high-confidence but verify in the editor, which takes ten seconds.)*

**Two sub-values have no row in `design-brief.md` §13.2 and no Q number: the locked-on
strafe multiplier and the backpedal multiplier.** They are named here as gaps for
`TODO.md`, not smuggled in as answers. A lock-on system that strafes at full run speed
will feel wrong regardless of what Q15 resolves to, so the designer will need them.

### Why

**Why identical.** Walk speed in a 1v1 fighter is not flavour, it is a **published
balance stat**. Street Fighter 6 lists a forward walk speed per character —
Dhalsim 2.80 at the bottom, JP 3.70 near the top — and the community reads those numbers
as a core tier consideration, with Dhalsim's slow walk understood as the deliberate
counterweight to his reach. A speed split between Echo and Nova is the same kind of
object: a balance lever, and *"separate balance systems"* are deferred by the shared-kit
rule. Under the approved Q22 it is worse than usual, because with the rival pinned at
1 HP and **no duel timer** (Q23 recommends none), mobility is the difference between a
player who can disengage to rebuild meter and one who cannot.

**Why 600 specifically.** Against group 04's 2400 × 1600 cm arena:

| Check | Number | Reading |
|---|---|---|
| Cross the long axis | 2400 / 600 = **4.0 s** | At the template's 500 it is 4.8 s, which is a long time to spend not fighting in a 3–5 minute duel |
| Cross the short axis | 1600 / 600 = **2.7 s** | |
| Distance covered in one fastest-legal Phase 2 rival cycle (2.315 s) | **~1389 cm** | The player can relocate across most of the arena inside one cycle — enough to escape, not enough to become untouchable |
| Close from mid-band (400 cm) to attack-A contact (~150 cm) | 250 / 600 = **0.42 s** | |

**And one consequence the designer should see before approving.** Group 02's Phase 2
non-threatening window is **~1.28 s**. Approach from 400 cm (0.42 s) plus a full
3-section combo (~1.0 s) is **1.42 s** — it **does not fit**. At the template's 500 uu/s
it is 1.50 s, worse. This is not a bug in the number; it is what Phase 2 escalation
*means*. The reading is: **in Phase 2 the player must already be in range when the
window opens, or take two hits instead of three.** It is a genuine consequence of
600 uu/s and it is surfaced rather than resolved. If the designer wants close-and-full-
combo to fit Phase 2, the required speed is ~890 uu/s, which is a sprint, not a
martial-arts duel — so the honest recommendation is to accept the pressure.

**Where Nova's "fast lateral rhythm" goes instead.** Into the **locomotion animation
set**, which is the channel the GDD names: *"animation presentation, stance and movement
personality."* Same `MaxWalkSpeed`, different step cadence, different foot-plant count
per metre, different weight shift. Nova's strafe cycle is authored short-and-frequent
with the torso leading; Echo's is longer-strided with a settle at the end. Both cover
420 uu/s while locked on. **The player will read Nova as quicker.** That is not a trick —
apparent speed in third-person action is dominated by animation cadence and camera
behaviour, not by the movement component's scalar, which is exactly why two characters
with identical frame data can feel different.

### Prior art (real games, named)

- **Street Fighter 6.** Per-character forward walk speeds are published and differ
  materially (Dhalsim 2.80 → JP 3.70). Crucially for this decision, EventHubs' ranking
  notes that **raw walk speed does not even predict traversal time**, because character
  collision box size interacts with it — Zangief at 3.64 crosses the screen a frame
  faster than JP at 3.70. That is a warning: in a game where the two avatars have
  **different heights and therefore different capsules**, a speed split would not produce
  the clean, predictable difference the designer intends.
- **Super Smash Bros. Ultimate — Peach / Daisy**, again. Identical movement stats; the
  characters still read as different people.
- **Mortal Kombat's ninjas.** Identical locomotion, entirely distinct identities.

### Interaction with the rest

| Touches | Effect |
|---|---|
| **Q10 bands, Q24 arena** (group 04) | 600 uu/s crosses each band quickly enough that the *"at least one attack always valid"* coverage proof is not stressed. Nothing in group 04's starvation check depends on player speed. |
| **Rival `MaxWalkSpeed` — `TODO` 49** | **This is the hard dependency and it is still open.** Group 04 already flagged it: *"a rival slower than the player can be kited forever and the duel cannot end"* under Q22. Q15 makes that concrete. **Constraint handed forward: the rival's pursuit speed must be ≥ 600 uu/s, or attack D's 600 cm closing travel must be available often enough to make up the difference.** This group cannot resolve TODO 49 — it is the rival's value, not the player's. |
| **Q11 lock-on** (group 04) | Acquire 3000 cm / break 3300 cm both exceed the 2884 cm arena diagonal, so lock never breaks by distance no matter how fast the player runs. Q15 cannot break lock-on. |
| **Q16 dodge distance** | Related but separate: dodge is a burst, walk is sustained. See Q16. |
| **M1-12, M1-16** | Unblocked. |

---

## Q16 — Echo / Nova dodge distance

- **Kind:** B · **Status:** PROPOSED
- **Unblocks build step:** M1-12 (and constrains M1-19, the dodge montage)
- **Value lives in:** `DA_FighterProfile.DodgeDistance` — `design-brief.md` §13.2 row 44
- **GDD range:** **none published.** The GDD names dodge and perfect dodge as shared kit
  and gives no displacement figure.

### Proposed value

**Identical for both fighters: `DodgeDistance = 400 cm`, band 300–450 cm**, applied to
every direction (back, left, right, forward) in Phase 1.

**Implementation matters as much as the number here.** The displacement should be
delivered by **Motion Warping** (`MotionWarpingComponent`, a warp target set from
`DodgeDistance` before `Montage_Play`, and a **Motion Warping notify** on the dodge
montage window) rather than by baked root motion or by scaling the play rate:

> **Motion Warping changes displacement while leaving the montage's timeline untouched.
> Play rate changes the timeline. That is the whole difference, and it is why
> `DodgeDistance` is a safe per-fighter scalar in principle and `MontagePlayRate` is
> not.** Q6's i-frames and Q7's perfect-dodge pocket sit at fixed montage times either
> way; warping moves the character further within the same 0.28 s.

Two things this group cannot supply:

- **The dodge montage's total length has no row and no Q number** — group 03 flagged it
  as `TODO` 48. Distance without duration is not a feel value. If the montage is ~0.50 s
  with displacement front-loaded across roughly the first 0.30 s, 400 cm is an average
  burst of ~1330 cm/s, which is in the range a dodge should feel like. **If the designer
  sets a different montage length, 400 cm means something different and should be
  re-checked.**
- **Whether a dodge cancels the light combo** — also group 03's finding, `TODO` 47, also
  unresolved. It changes how often the player dodges from a committed state.

### Why

**Why identical.** Dodge displacement decides whether a dodge *escapes the follow-up*,
and group 02 flagged attack **B as a "sequence"** — an attack authored with more than one
`ANS_ActiveHit`. Against a multi-hit attack, distance is survival: the i-frame window
covers one hit, and the distance decides whether the second one lands. A per-fighter
distance split is therefore a per-fighter **safety** split, which is per-fighter
difficulty by another route — the same failure as Q14, arriving through spacing instead
of time.

**Why 400 cm.** Checked against group 04's bands (centre-to-centre: A 0–260, B 90–520,
C 240–420, D 400–840):

| From | Back-dodge 400 cm lands at | Reads as |
|---|---|---|
| Attack-A contact, ~150 cm | **550 cm** | Out of A (max 260), out of C (max 420), out of B (max 520) — **into D's band alone** |
| Mid-band, ~300 cm | **700 cm** | Inside D only |
| Two consecutive back-dodges from 200 cm | **1000 cm** | Outside **all four** bands — deliberately triggers group 04's required-advance rule in `BTTask_Idle_Reposition` rather than an idle loop |

That is the spacing conversation the design wants: **one back-dodge trades the three
close attacks for the approach attack.** The player is never safe, only differently
threatened. At the bottom of the band (300 cm) a back-dodge from 150 cm lands at 450 cm,
still inside B and C, so the dodge buys much less; at the top (450 cm) it starts to
overshoot D's 400 cm floor from close contact, which pushes the player into the
zero-coverage region too readily.

**Where Nova's "forward intent" goes instead.** Into **which direction the dodge
animation sells**, not how far it travels. Echo's back-dodge is authored as a measured
step-out with a settle and the guard reforming — *"exact timing and clear counter
intent."* Nova's is a low lateral scramble that recovers already leaning in —
*"momentum without visual noise."* Same 400 cm, same 0.28 s of i-frames, same 0.12 s
pocket, same montage length, same notify times. **Only the pose content differs.**

**One authoring rule that makes this survive M5.** If the designer later wants a bespoke
Nova dodge animation rather than a shared one, it must be authored to the **identical
montage length with the notify states at identical times**, and the developer should add
an editor validation check that compares the two profiles' dodge montages and errors if
`ANS_IFrame` or `ANS_PerfectDodge` start/duration differ by more than a frame. Otherwise
Q14's problem returns through the art pipeline instead of through a data asset.

### Prior art (real games, named)

- **Super Smash Bros. Ultimate — Peach / Daisy.** Identical dodge and roll properties;
  the game's own first-party "same kit, different character" design does not split
  defensive displacement.
- **Street Fighter 6.** The genre convention that defensive options are **not** where
  characters are differentiated at the same tier as offence — SF6's Drive Parry and
  Perfect Parry windows are universal system mechanics with the same timing for the whole
  roster, and characters differ in walk speed and moves instead. Ascendant Impact has
  deferred the "moves" half of that trade, which leaves defensive parity as the *only*
  safe configuration.
  *(The universality of SF6's Perfect Parry window is stated here from group 03's cited
  2-frame figure; this group did not separately verify that it is identical for every
  character. **Marked unverified.**)*
- **Mortal Kombat's ninjas.** Same movement, same evasion, distinct characters.

### Interaction with the rest

| Touches | Effect |
|---|---|
| **Q6 / Q7** (group 03) | Untouched, provided displacement is delivered by Motion Warping and not by play rate. |
| **Q10 bands** (group 04) | 400 cm is tuned *to* those bands. **If Q10 moves, Q16 must be re-derived.** |
| **Attack B as a multi-hit sequence** (group 02, open tension 5) | 400 cm is the value that makes a dodge out of B's follow-up meaningful. If B's active windows end up spread over more than ~0.4 s, re-check. |
| **Q13 attack D travel = 600 cm** (group 04) | A single dodge (400 cm) does not out-distance D's closing travel (600 cm). Intended: **you cannot dodge your way out of the approach attack, only through it.** |
| **`TODO` 47, 48** | Both still open and both change what 400 cm feels like. |

---
