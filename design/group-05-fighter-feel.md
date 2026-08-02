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

## Item 43 — Is Echo's faceplate a visor or a light?

- **Kind:** B · **Status:** PROPOSED
- **Unblocks build step:** **M5-06** — final character treatment. *(Also read by M5-08, the
  editorial selection interface, which is the one screen that puts the face on camera.)*
- **Value lives in:** **there is no §13.2 row for any material or emissive parameter.** The
  table is complete with respect to itself and has no home for this. Proposed home, for the
  designer to accept or renumber:
  - `M_Fighter_Master` (shared master material, both fighters) — vector parameter
    **`Indicator_EmissiveColor`** and scalar parameter **`Indicator_EmissiveIntensity`**.
  - `DA_FighterProfile.IndicatorEmissiveColor` (LinearColor), sitting directly beside the
    existing `AccentColor` field in §4.2's table — so the indicator hue is data, per fighter,
    on the asset that already exists for exactly this purpose.
  - **Proposed new §13.2 row, next free number 58** — *"Echo / Nova faceplate treatment and
    indicator emissive colour."* The designer assigns the number; this file does not edit
    `design-brief.md`.

### GDD basis

**Read this qualifier first.** GDD pages 12 and 13 are supplied image reference sheets with
**no extractable authored text** beyond their captions. Everything quoted below is a *callout
printed inside the artwork*, recovered by extracting the embedded JPEG and viewing it. It is
not authored GDD prose and **authored GDD text outranks it.**

| Source | Exactly what it says |
|---|---|
| Page 12 callout (Echo) | **"Visor or Light"** — the sheet poses the question and does not answer it |
| Page 12, described | *"a smooth, entirely black full-face helmet… The face area is one continuous dark surface"*, glossy, with a specular highlight — **drawn as a dark plane, not as a lamp** |
| Page 13 callouts (Nova) | **"Helmet"**, **"Visor liast"** *(printed exactly so — a confirmed typo, intended word unknown)*, **"Light"** — **three separate callouts** |
| Page 13, described | *"a full-face helmet with a pale light-grey shell cap… and a **dark visor** across the face. A **small yellow-green indicator light** sits at the lower side of the helmet."* |
| §07 REVISED — COLOR DIRECTION (PDF p.8, authored text) | *"Echo keeps restrained orange accents. Nova's existing black, charcoal, orange, and light-gray costume design is preserved; cyan-white is reserved for combat energy, telegraphs, or selected VFX accents when separation is needed."* |
| §07 readability targets (authored text) | Echo — *"Exact timing and clear counter intent."* Nova — *"Momentum without visual noise."* |
| §07 (authored text) | Crimson Vanguard *"reads through red armor, black structure, and **red-orange systems and warning lights**."* |

**Ambiguous, and left ambiguous:**

- Whether Echo's faceplate is see-through or emissive. That is the question.
- **Nova's indicator hue.** The art shows **yellow-green**; her printed palette has four
  swatches — Matte Black, Charcoal Grey, Bright Orange, Light Grey (Helmet Cap) — and
  **yellow-green is not one of them.** Art and palette disagree on this sheet. **Not resolved
  here.**
- Echo's palette prints **three** swatches and contains no indicator colour at all.
- Whether *"Lit Orange"* (Echo) and *"Bright Orange"* (Nova) are genuinely different values.

### Proposed answer

**Resolve it as "visor AND light" for both fighters, not "visor OR light" for Echo.**

| | Echo | Nova |
|---|---|---|
| Faceplate | **Dark visor plane.** Matte black, glossy, non-emissive — exactly as page 12 draws it. Nothing changes about the art. | Dark visor across the face, as drawn. Unchanged. |
| Indicator | **One small discrete emissive element** added at the lower side of the helmet, in the same position Nova's sits | The **"Light"** her sheet already names. Unchanged. |
| Indicator colour | **"Lit Orange"** — the only accent in Echo's three-swatch palette | **OPEN.** Art says yellow-green; the palette does not list it. **Designer decides.** |
| Gameplay modulation | **None.** Constant low emissive. Identity only. | **None.** Same. |
| Cyan-white | **Not used.** Reserved for combat energy, telegraphs, and selected VFX accents | Same |

So the sheet's either/or dissolves: **Nova's board already shows a visor and a light coexisting
on one helmet**, and page 12's callout is most economically read as naming the same two parts
rather than offering a choice between them.

**And the faceplate is explicitly *not* a gameplay-state channel.** That job is item 44's, and
it lives on the back. This item hands the face to identity and takes it out of the readability
argument on purpose.

### Why

**1. It removes the inconsistency instead of deepening it.** The dispatch's own concern is that
the two fighters may currently be inconsistent with each other. Making Echo's faceplate a lamp
while Nova's stays a dark visor *is* the inconsistency, made permanent. Giving both the same
two-part structure — dark plane plus small light — costs one small emissive element on Echo and
closes the question.

**2. Camera geometry says the face is almost never on screen during the fight.** GDD §07's
opening flow requires *"The camera moves behind the selected fighter"*, and `design-brief.md`
§10.2 carries the arena's **reverse third-person framing** requirement. For the whole three-to-
five-minute duel the player is looking at the **back** of their own fighter's helmet. The face
is on camera in exactly four places, and all four are M5 or cinematic:

| Where the face is actually visible | Milestone |
|---|---|
| The editorial character-selection interface | M5-08 |
| The abbreviated arena entrance / `IntroMontage` | M4 (functional) → M5 (treated) |
| The 1–3 s Impact Window choreographed burst | M3 (functional) → M5 (camera authored) |
| The Final Clash camera cut, `LS_FinalClash` | M4 (functional) → M5 (choreographed) |

**Spending a readability channel on a surface that is off-camera for the entire duel is spending
it in the wrong place.** The faceplate is worth exactly what a face is worth: recognition on the
select screen and presence in the cinematic beats.

**3. A full emissive faceplate would be the largest single emissive area on either fighter, and
Nova has no equivalent.** Attention in a duel goes to the brightest moving thing. If Echo's face
is a lamp and Nova's is not, the two fighters are not equally legible to their own player, and
the asymmetry lands on the *head* — the region players look at first. A small indicator on both
is symmetric, and symmetric is what SCOPE LOCK asks for.

**4. It protects Nova's readability target without penalising Echo.** *"Momentum without visual
noise"* is a ceiling on how much Nova may glow. The cheap way to honour it is to lower Nova.
The correct way is to pick a channel small enough that Echo does not need to be lowered either.

**5. It keeps the player out of the rival's colour lane.** Crimson Vanguard reads through
*"red-orange systems and warning lights."* A large orange glow on Echo's face at combat distance
competes with the exact cue the player must read to survive. This produces a rule worth stating
once and applying to items 43 and 44 together:

> **The rival owns animated emissive. The player owns static or stepped emissive.**
> Flashing, pulsing, and ramping belong to `ANS_Telegraph` on Crimson Vanguard's montages.
> The player's on-body emissive holds still, or changes in discrete steps at threshold
> crossings. **Motion, not hue, is the discriminator** — which survives a colour-blind player
> and survives the two fighters sharing an orange family with the rival's red-orange.

**6. It is the cheapest thing that answers the question.** One small emissive island in the
master material and one LinearColor on a data asset that already exists.

### Prior art (real games, named)

- **Dead Space — the RIG.** Visceral put the player's state on Isaac's **back**, not his face:
  a glowing segmented spine bar for health and *"a circular Stasis bar on his back"* for the
  second resource. The stated design reason is that the third-person camera looks at the back,
  so the back is the surface that is always on screen. The face-vs-back question in Ascendant
  Impact has the same answer for the same reason, and Dead Space is the reference case for it
  at AAA scale.
- **Overwatch.** Blizzard's readability doctrine is silhouette first, then a signature colour
  palette carried across every skin so *"you're never confused about who you're fighting"*, then
  unique VFX and unique audio **per ability**. Note the split: the *character* is identified by
  silhouette and palette; the *state* is communicated by ability VFX and sound. Head-region art
  in Overwatch is a recognition anchor (Lúcio's headphones, D.Va's mech profile), not a state
  readout. That is exactly the division proposed here.
- **For Honor — Revenge.** Full-resource state is shown as *"a slight orange-yellow glow"* on
  the whole body **plus** a shield icon that fills around the edge on the HUD — two channels for
  one fact — **plus** a shimmering sound, and Ubisoft later shipped explicit colour-blind
  support for it. Not a face element in any of its three channels.

*(Destiny 2 was searched as a fourth candidate and is **not** cited: the results describe
super-ready as a HUD readout, with body glow appearing only on specific cosmetic armour
ornaments. **Unverified as a gameplay-state channel** and not used as evidence.)*

### Milestone placement

**M5-06, entirely.** Faceplate treatment, the indicator element, the emissive island in the
master material, and the indicator colour are all *final character treatment*, which is the M5
gate's own wording — and the GDD gates M5 as *"Only after M4 is stable."*

**Note to M1 — and it is a prohibition, not a task.** M1–M4 fighters are Mannequin proxies
(§12.2, §12.3). A Mannequin has no faceplate. **Do not attempt any faceplate or indicator
treatment before M5.** Phase 1 fighters carry the flat `AccentColor` that `ApplyFighterProfile`
already sets in §4.2, and nothing more. That is `design-brief.md` §11.6's line held exactly
where it is: picking a colour is asset selection, authoring an emissive element is M5.

---

## Item 44 — Are Echo's "Integrated Energy Lines" emissive at runtime?

- **Kind:** B · **Status:** PROPOSED
- **Unblocks build step:** **M5-06** — final character treatment.
- **Value lives in:** **again, no §13.2 row exists.** Proposed home:
  - `M_Fighter_Master` — one scalar parameter **`Ascension01`** (range 0–1) multiplied into the
    emissive input through a **per-fighter mask**, so the *same parameter* lights *different
    geometry* on each fighter with no logic difference.
  - `DA_FighterProfile.AscensionEmissiveCurve` (`CurveFloat` asset) — maps `Ascension01` to
    emissive intensity. **This is where "how much Nova is allowed to glow" is authored**, as a
    curve asset, without a single branch anywhere in code.
  - One function, `BP_AscensionComponent → UpdateAscensionMaterial(NewValue)`, bound to the
    **already-specified** `OnMeterChanged` delegate (§4.9), calling `Set Scalar Parameter Value`
    on a **cached** dynamic material instance.
  - **Proposed new §13.2 rows, next free numbers 59 and 60** — *59: per-fighter Ascension
    emissive curve; 60: the tier thresholds the curve steps at.* Designer assigns the numbers.

### GDD basis

Same qualifier as item 43: these are **callouts printed inside image reference sheets**, not
authored GDD prose.

| Source | Exactly what it says |
|---|---|
| Page 12 callouts (Echo) | **"Integrated Energy Lines"**, **"Backpack Power Unit Core"** |
| Page 12, described | *"the rear view shows **thin orange energy lines** tracing up the spine and across the shoulder blades, converging on a **central back unit**… low-profile and integrated, not a worn pack."* |
| Page 12, ambiguity list | **"AMBIGUOUS: whether the orange energy lines are emissive at runtime or printed trim. They are drawn flat, with no glow or bloom."** |
| Page 13 (Nova) | **No back unit and no energy lines.** Her back shows *"a large orange shoulder yoke and a charcoal spine panel."* Small **yellow-green indicator strips** sit on the chest and left ribs |
| §07 (authored) | Echo *"Controlled orange accents"* · Nova *"Cyan-white combat energy or selected telegraphs"* · CV *"Red-orange systems and warning lights"* |
| §07 REVISED — COLOR DIRECTION (authored) | cyan-white is *"reserved for combat energy, telegraphs, or selected VFX accents"* — **not a costume recolor** |
| GDD PRESERVED — METER DEFINITION (authored, via `design-brief.md` §4.9) | the meter is *"earned only through active combat decisions. It does not fill from waiting or elapsed time."* |
| `design/decisions.md` 2026-08-02 — **Q22 APPROVED** | the Final Clash is the **only** way to win; the meter is therefore the only route to the ending. Condition **C2**: the HUD must show which gate is still locked |

**Ambiguous, and left ambiguous:** whether the lines are emissive at all (the question); whether
Nova's yellow-green strips are a legitimate emissive colour for her given her four-swatch palette
does not contain yellow-green; whether "Lit Orange" and "Bright Orange" differ.

### Proposed answer

**Yes to both — with four hard constraints that keep it inside the GDD's colour rule, Nova's
readability target, and SCOPE LOCK.**

**1. Emissive at runtime: yes.** Echo's energy lines and the circular power-unit core are
authored as an emissive island in `M_Fighter_Master`, masked to Echo's geometry.

**2. Ascension-responsive: yes — and for *both* fighters, through each one's own art.** An
emissive channel that tells one fighter's player their meter state and leaves the other guessing
is a per-fighter information advantage, which is a per-fighter advantage. So:

| | Echo's channel | Nova's channel |
|---|---|---|
| Geometry | Spine **"Integrated Energy Lines"** + the circular **"Backpack Power Unit Core"** they converge on | Her existing back **orange shoulder yoke**, and the outline edge of the charcoal spine panel |
| Lit area | Larger — a literal line-and-core "charge" read | **Deliberately smaller.** Same information, less surface |
| Colour | *"Lit Orange"* — her own accent, intensity only | *"Bright Orange"* — her own accent, intensity only |
| Hue change | **Never.** Intensity only | **Never.** Intensity only |
| New geometry | None. It is already on the sheet | **None.** No back unit is added to Nova — see the tension below |

Nova gets the smaller channel *because* her readability target is *"momentum without visual
noise"*, and that is the entire mechanism by which the target is honoured while parity of
information is kept. `AscensionEmissiveCurve` is where the difference is authored: two curve
assets, one code path.

**3. Discrete tiers, not a continuous fill — and the thresholds are numbers the design already
owns.** No new number is invented here:

| Tier | Meter | Body reads | Where the number comes from |
|---|---|---|---|
| **Dim** | 0–49 | Lines dark / barely present | complement of the below |
| **Lit** | 50–99 | Lines carrying, core warm | **50** is the failed-Clash meter setback — `design-brief.md` §13.1 row 14, a GDD number |
| **Full** | 100 | Core at full, lines saturated, holds steady | **100** is the Final Clash meter gate — §13.1 row 11, a GDD number |

**The question for the designer** is not the thresholds — those are borrowed rather than
invented — it is **whether three tiers is the right count, or whether a continuous fill reads
better.** Three is proposed because a stepped read is glanceable in peripheral vision and a
continuous fill is not, and because a continuously animating body element is the thing Nova's
target forbids. **Two, three, four, or continuous are all defensible. Designer decides.**

**4. Four rules that are part of the answer, not commentary:**

- **It is never the only channel.** The `WBP_HUD` meter bar stays authoritative and Q22's
  condition **C2** — the HUD showing *which* gate is still locked — stays entirely on the HUD.
  The body says *how charged I am*. It never says *whether the Clash is available*, because
  that is a two-gate fact and the body has one dimension.
- **No animation during Telegraph, Active, or Recover.** State changes fire only on a threshold
  crossing. Any transition flash routes through
  `BP_PresentationSubsystem → RequestVFX` / `RequestHitStop` (§4.10), so the presentation
  kill-switch removes it wholesale during diagnosis **without touching the meter value**.
- **No hue change, ever.** Intensity only, in each fighter's own accent. **Cyan-white is not
  used for this channel** — it stays reserved for combat energy, telegraphs, and selected VFX
  accents, and a meter readout is none of those.
- **It reads state; it never creates state.** No damage, no meter, no timing, no collision.
  Turning it off changes nothing mechanical, which is what makes it safe to make optional.

**A consequence worth naming because it is free and good:** a failed Final Clash drops the meter
100 → 50 (§9.4 step 5). On the body that is **Full → Lit**, visible on the player's own back at
the moment it happens. The single most misreadable rule in the design — *a failed Clash is a
setback, not a restart* — gets a diegetic statement at zero cost.

### Why

**1. The back is the most on-screen surface in this game, and Echo's sheet already put the art
there.** GDD §07 requires the camera to move *"behind the selected fighter"*; §10.2 carries
**reverse third-person framing** as an arena requirement. For the entire duel the player is
looking at a spine and a shoulder line. Page 12 draws energy lines up that spine converging on a
circular core. That is not a coincidence to be admired — it is a channel the concept art already
built and the code has not yet used.

**2. It is genuinely cheap, which is the claim the TODO item makes and it holds.** One scalar
parameter on a cached MID, set from a delegate that §4.9 already specifies. No Niagara system, no
new component, no tick. Set against M5's actual VFX list — telegraph energy, thruster plumes,
warning-light systems, the Ascension language — this is the cheapest item on it by a wide margin.

**3. Under the approved Q22, meter state is the most decision-relevant number in the game.** The
Final Clash is the only win condition, so the meter is the only route to the ending. Right now
the player reads it by looking away from the fight to a HUD corner — during a duel whose entire
premise is *reading the rival's telegraph*. A second channel on the surface the camera is already
pointed at keeps the eyes where the game needs them.

**4. A hypothesis worth playtesting, offered as a hypothesis.** Group 02's open tension 2 is the
*"2-hit-and-bail"* player, who never finishes a string, earns no meter, and can reach a pinned
rival with an empty bar. A body channel that visibly **never lights** may teach that faster than
a bar the player is not looking at. **This is unproven and is not a reason to approve the item on
its own** — it is a thing to watch for in the first playtest.

**5. Nova's constraint is satisfied by area and by stillness, not by exclusion.** The wrong answer
to *"momentum without visual noise"* is to give Nova nothing. The right answer is a channel small
enough and still enough that it is legible without competing with her own animation.

### Tensions and risks — surfaced, not resolved

| # | Risk | Note |
|---|---|---|
| **1** | **Echo's orange vs the rival's red-orange warning lights.** They are neighbours on the wheel, and the rival's telegraph is the one cue the player must not miss. | Mitigated by the rule from item 43: **the rival owns animated emissive; the player owns static or stepped emissive.** Motion is the discriminator, not hue. **This does not eliminate the risk — it makes it testable.** |
| **2** | **Legibility at duel distance is unproven.** A thin spine line at 300–500 cm through a combat camera may simply not read. | This is the standing criticism of Dead Space's RIG — that diegetic readouts must be *"legible at in-world scale"* and that a back-mounted bar has *"little functional difference from a traditional corner-of-screen health bar."* **Only playtest settles it.** The redundancy rule is what makes a negative result cheap: if it does not read, nothing breaks. |
| **3** | **Nova has no back unit.** If the designer wants parity of *lit area* rather than parity of *information*, that is a change to Nova's character art. | **Out of scope for this item and for Phase 1.** Named so it is a decision rather than a drift. |
| **4** | **Nova's yellow-green indicator strips.** They are in the art and not in her printed palette. | This item deliberately does **not** use them as the Ascension channel — it uses her orange back yoke, which *is* in the palette. The yellow-green question stays open on its own. |
| **5** | **An accessibility toggle makes it non-load-bearing, which is the point.** | Doom Eternal ships its equivalent as player-disableable. Recommend the same, wired to the existing debug/presentation toggle surface rather than a new setting. Because the HUD is authoritative, disabling it removes flavour and no information. |

### Prior art (real games, named)

- **Dead Space — the RIG.** The near-exact precedent, and it maps almost part-for-part. Visceral
  put a **glowing segmented spine bar** on Isaac's back for health *and* **a circular Stasis bar
  on the same back** for the second resource. Echo's sheet has **spine lines** and **a circular
  back core**. Two more details transfer directly: the bar is **segmented** rather than smooth,
  and it steps through **discrete states** — reported as aqua-blue above 75%, green above 50%,
  yellow below 50%, blinking red below 25%. That is a stepped, glanceable read, which is the
  argument for tiers over a continuous fill. The design rationale is stated by the team: the
  ribbed suit exists partly *to* host a diegetic readout on the back, and the back is where the
  third-person camera looks. **The known criticism travels with it** and is logged as risk 2.
- **For Honor — Revenge.** Full-resource state shown as a body glow **and** a HUD shield **and**
  a sound cue. Three redundant channels for one fact, in a 1v1-focused melee game with heavy
  read-and-react combat. This is the single closest genre match to Ascendant Impact, and it does
  not make the body glow the only channel. Ubisoft also shipped colour-blind support for it.
- **Devil May Cry 5 — Devil Trigger / Sin Devil Trigger.** The Sin Devil Trigger gauge *"starts
  glowing when fully charged"* on the HUD, and when the state is active the character's **chest
  and head glow** and the body is wreathed in effects. Same pattern: **full-resource is signalled
  in both places**, and the on-body version is the loud one reserved for the moment it matters.
- **Doom Eternal — the stagger flash.** An **orange flash on the enemy body** means a Glory Kill
  is available and in range; **blue** means staggered but out of range. State communicated by
  emissive on a character body rather than a HUD element, in a fast game, and **players can
  disable the flashing glow**. Two lessons: a two-state colour read is enough to carry a real
  mechanic, and a body-emissive channel is normal to make optional.
- **Tekken 8 — Heat.** Already cited in the Q14 section above and it cuts both ways: Heat is
  signalled by a **light-blue aura on the character *and* a bar under the health bar** — the
  redundancy pattern again — while the community complaint that Tekken 8's effects volume makes
  animations harder to read is **the direct warning against Nova's target**, *"momentum without
  visual noise."*

### Milestone placement

**M5-06, entirely.** Material authoring, the emissive masks, the curve assets, the tier
thresholds, and the transition treatment are all final character treatment, and the GDD gates M5
as *"Only after M4 is stable."* No part of this is built, authored, or tuned during M1–M4.

**Note to M1 — two lines, and neither of them is M5 work.** These exist so that approving this
item at M5 does not force a rewrite of code M1 is writing anyway:

1. **`ApplyFighterProfile` (§4.2) already sets a material parameter for `AccentColor`. Make sure
   it does so through a dynamic material instance created *once* and cached**, not one created
   per call. This is a correctness fix regardless of item 44 — creating a MID repeatedly leaks a
   new material object each time, and it is the standard failure mode in this pattern. **One MID
   per mesh component per material slot, created on `BeginPlay`, stored on the component.**
2. **`BP_AscensionComponent` already broadcasts `OnMeterChanged` (§4.9).** No new delegate, no new
   event, no new component is needed at M5. **Bind nothing to it for emissive purposes before
   M5.**

That is the whole M1 note. **No emissive parameter, no mask, no curve asset, and no glow of any
kind is authored during M1–M4.** Phase 1 fighters stay at the flat `AccentColor` that
`design-brief.md` §11.6 already permits as asset selection.

---

## Item 45 — What does "SFN" stand for?

- **Kind:** B · **Status:** PROPOSED — **and the proposal is to leave it open.**
- **Unblocks build step:** **M5-08** — the editorial character-selection interface. *(A
  sub-question also touches M5-06; see below.)*
- **Value lives in:** **no §13.2 row, and this one has no natural home either** — it is a string,
  not a tunable. Proposed home, following the **Q29 precedent exactly**:
  - `WBP_CharacterSelect` — an exposed `Text` variable **`FighterUnitLine`**, **left blank by the
    developer.** §14 Q29 already establishes this discipline for Crimson Vanguard's short HUD
    label: *"The developer should expose it as a `Text` variable on `WBP_HUD` and leave it blank
    rather than inventing one."* Same rule, same reason.
  - **Proposed new §13.2 row, next free number 61** — *"Expansion of the 'SFN' unit insignia (if
    any)."* Designer assigns the number.

### GDD basis

| Source | Exactly what it says |
|---|---|
| Page 13 callout (Nova) | **"Unique 'SFN' Unit Insignia"** |
| Page 13, described | *"A **circular badge on the upper arm**, orange-outlined, carrying a stylised angular monogram… the only readable lettering identified on either fighter's sheet."* |
| Page 13, ambiguity list | **"AMBIGUOUS: what 'SFN' stands for. It is nowhere expanded in the GDD."** |
| Page 12 callout (Echo) | **"Unique Badge"** — and page 12's ambiguity list records: *"the badge carries a device but no readable lettering. Nova's equivalent badge* is *lettered; Echo's is not."* |
| Everywhere else in the GDD | **Nothing.** No expansion, no unit name, no organisation name appears in any authored section |

### Proposed answer

**It cannot be established from the GDD, and this file does not establish it. Leave it
unexpanded, and ship M5-08 without needing it.**

Three parts:

**1. The build does not need the expansion.** The insignia is a **circular badge with a stylised
angular monogram**. A unit mark reads as a unit mark whether or not the letters are expanded —
that is what unit marks are for. **M5-08 ships the badge as art.** If the editorial selection
interface wants a unit line under Nova's name, `FighterUnitLine` is exposed and **left blank**,
and the layout is authored so that a blank line collapses cleanly rather than leaving a hole.
Nothing in the game is blocked by this question, ever.

**2. Verify the three letters before anyone builds fiction on them.** Page 13 carries at least
two confirmed print errors — **"Visor liast"** and **"Two-Layer System (Technical Shirt"** with
an unclosed parenthesis — and the badge is a small, stylised, angular monogram. **A human should
confirm "SFN" against the PDF by eye before it is treated as established lettering.** This is the
same discipline `TODO` item 26 applied to the *"plasma-gauntlet weapons"* transcription, and for
the same reason: the recovered sheets are image descriptions, and a mis-read of three stylised
glyphs would propagate into every downstream artifact that quoted it.

**3. If the designer does want an expansion, it comes from assignment #04, not from here.** The
offline content pipeline reads the GDD as its knowledge base, runs a critic agent for lore and
tone consistency, and terminates in the human approval gate. `CLAUDE.md` already names *"No
UI/announcer/telegraph strings"* as one of this project's real content gaps, and this is exactly
that gap. That pipeline is **offline authoring tooling outside the game's SCOPE LOCK**; the
shipped build still makes no runtime model calls. **Nothing generated there enters the build
without the designer's explicit approval.**

**A fourth option that is legitimate and costs nothing: declare that "SFN" is never expanded.**
An unexplained unit designation on a shoulder patch is a normal and effective piece of world
texture. Choosing *not* to expand it is a real answer, not a deferral, and it is the cheapest one
on the table.

### The larger question this actually raises

**Is "SFN" Nova's unit, or the organisation both agents serve?**

Nova's badge is lettered. **Echo's is not.** If SFN is a shared unit, Echo's *"Unique Badge"*
should logically carry the same mark, and that is a **character-art change at M5-06**, not a
string decision at M5-08. If SFN is Nova's alone, the two agents belong to different units, which
is a fiction fact the GDD has never stated either way.

There is also a thread to the **undefined "Ascendant operative" fiction** — `CLAUDE.md` lists
*"'Ascendant operative' and the Ascension fiction are undefined"* as a named content gap. If a
unit fiction is ever authored, **SFN and "Ascendant" must be reconciled in one pass**, or the
project ends up with two unrelated organisational names attached to the same two characters.

**Neither of these is resolved here.** Both are handed to the designer.

### Candidate expansions — **INVENTED. NO GDD BASIS. NOT CANON.**

> **Read this label literally.** Every string below was made up by this dispatch. **None of them
> appears anywhere in the GDD, on either character sheet, or in any authored document in this
> repository.** They exist only so the designer has something concrete to reject. Approving one
> would be authoring new canon, and that is the designer's act, not this file's.

| Candidate | Invented | Note |
|---|---|---|
| *Special Forces — Nine* | yes | Reads as a military unit designation. Generic; adds no world texture |
| *Sentinel Field Network* | yes | Fits an operative-dispatch fiction and could plausibly extend to Echo |
| *Sovereign Frontier Network* | yes | Broader organisational read; would need reconciling with "Ascendant" |
| *Strike Force Nova* | yes | **Recommended against on structural grounds** — it names the unit after one selectable fighter, which makes Echo the outsider in his own shared framework and breaks any shared-unit reading |

**No research was spent on this item.** The dispatch's own instruction was that research is
unlikely to help, and it is correct: "SFN" is a three-letter mark invented for this project's
concept art. There is nothing to look up.

### Milestone placement

**M5-08** for the selection-interface string, which ships **blank** unless and until the designer
authors an expansion. **M5-06** for the separate badge-parity question — whether Echo's unlettered
badge should carry the same mark.

**Note to M1:** none. Nothing in M1–M4 displays a unit name. `WBP_CharacterSelect` at M1 is the
GDD's permitted *"simplified selection screen"* — two portrait buttons, name, one-line identity
(§10.1) — and **it must not invent a unit line to fill space.**

---

## Answering group 03's MontagePlayRate warning

**For the developer. This is the whole protection, stated as steps you can implement without
reading the rest of this file.**

Group 03 warned three times that `DA_FighterProfile.MontagePlayRate` would silently scale
**Q6 (dodge i-frames, 0.28 s)** and **Q7 (perfect dodge, 0.12 s)** into per-fighter difficulty,
because an Anim Montage's play rate is a time scalar on the entire montage and every Anim Notify
State on it is therefore scaled with it. Seven measures close it:

1. **The value is `1.000` for Echo and `1.000` for Nova.** Identical. At play rate 1.0 the
   scaling factor is unity and every notify state on every player montage occupies exactly the
   wall-clock time it was authored to occupy. **This alone is the answer; measures 2–7 are what
   stop it drifting.**

2. **The field is renamed `CosmeticMontagePlayRate`**, with a `UPROPERTY` tooltip reading
   *"Never applied to a montage that carries a gameplay notify window. See design/group-05."*

3. **It may be read by exactly four montages, and this is the complete list:**
   `AM_Fighter_SelectIdle`, `AM_Fighter_ArenaEntrance`, `AM_Fighter_Victory`,
   `AM_Fighter_Defeat`. **It is never read by** `AM_Player_LightCombo`, `AM_Player_Dodge`,
   `AM_Player_Counter`, `AM_Player_CounterWhiff`, any Impact Window burst montage, or any Final
   Clash montage.

4. **There is one call site.** A `Blueprint Function Library` node,
   `PlayFighterMontage(Montage, bCosmetic)`, is **the only place in the project** where
   `Montage_SetPlayRate` — or `Montage Play`'s `In Play Rate` pin — is given a value other than
   `1.0` on a **player** montage. Every other player montage play passes a literal `1.0`.

5. **The call site self-checks.** When `bCosmetic = true`, `PlayFighterMontage` `ensure()`s that
   the montage carries **zero** notify states of the gameplay classes `ANS_IFrame`,
   `ANS_PerfectDodge`, `ANS_ActiveHit`, `ANS_ComboLink`, `ANS_CounterWindow`. Wiring a gameplay
   montage into the cosmetic path produces an **editor warning**, not a silent balance change.

6. **Displacement never travels through play rate.** Q16's 400 cm dodge distance is delivered by
   **Motion Warping** — a warp target set from `DodgeDistance` before `Montage_Play`, consumed by
   a Motion Warping notify on the dodge montage. **Motion Warping changes how far the character
   moves and leaves the montage timeline untouched.** Q6's `[0.03, 0.31]` and Q7's `[0.03, 0.15]`
   sit at the same montage times, and therefore the same real times, at any distance.

7. **If a bespoke Nova dodge montage is ever authored**, it must use the **identical montage
   length with the notify states at identical times**, enforced by an editor validation check
   that compares the two profiles' dodge montages and **errors** if `ANS_IFrame` or
   `ANS_PerfectDodge` start or duration differ by more than one frame. Otherwise the problem
   returns through the art pipeline instead of through a data asset.

**Inspector-checkable statement:** `Montage_SetPlayRate` and any non-`1.0` `In Play Rate` on a
player montage appear in exactly **one** asset, `PlayFighterMontage`. Anywhere else is a defect.

**One scoping clarification the developer needs, or measure 5 will fire falsely.** This guard
governs the **player kit only**. The **rival's** montages legitimately use play-rate scaling:
`design-brief.md` §5.3 and §8.3 implement Phase 2 re-timing through `S_AttackPhaseTuning`'s
`TelegraphScale` and `RecoverScale`, applied as play rate over the telegraph and recover sections
of `AM_Vanguard_Attack*`. **That is the intended one data path and must not be "fixed."** Two
consequences follow, and both are correct rather than bugs:

- Scaling the telegraph section also scales any `ANS_CounterWindow` authored on it. **That is
  intended** — the counter window should move with the telegraph it is a read on.
- Because Phase 2 shortens the telegraph (**0.55–0.95 s → 0.40–0.75 s**, GDD), the counter window
  shortens with it. **That is Phase 2 pressure**, and it lands **identically on Echo and Nova**,
  which is the entire point of holding the player-side play rate at 1.0.

---

## Differentiation budget

**The question underneath Q14, Q15 and Q16 is not "what values?" — it is "how much difference
does this game still need to buy?" Here is the ledger.**

### Already bought, at no cost to the framework

The recovered sheets show Echo and Nova reading as **different people before a single scalar
moves**:

| | Echo (p.12) | Nova (p.13) |
|---|---|---|
| Palette | 3 swatches | **4** — adds "Light Grey (Helmet Cap)" |
| Helmet | Entirely black | Light-grey cap over dark visor |
| Torso | One-piece **"Segmented Body Suit"** | **"Dual-Layer System (Jacket over Vest)"** |
| Back | **"Backpack Power Unit Core"** + energy lines | Orange shoulder yoke, no back unit |
| Legs | Close-fitting, one continuous line | Cargo trousers to below the knee, then close legging |
| Carry | None | **Two named thigh pouches** |
| Footwear | Low-profile shoe | High-top **"Designed Light Sneakers"** |
| Insignia | **"Unique Badge"**, unlettered | Circular, lettered **"SFN"** |

Add the GDD's authored 10 cm height difference and §07's silhouette language — *"lean, upright
technical striker"* versus *"compact, agile layered profile"* — and the two fighters differ in
**height, outline, layer count, palette count, carried volume, leg break, footwear mass, and
insignia**. That is a full differentiation budget, spent, in the channel §02 names first:
*"animation presentation, stance and movement personality, VFX language, timing flavor."*

### How much *mechanical* differentiation is still needed

**In Phase 1: none. Zero.** The conservative reading is the right call, and it is right for four
reasons that do not depend on each other.

**1. The GDD sequences it, in its own words.** §10's Provisional Design Decisions, row *Echo /
Nova timing flavor*: *"Use the same mechanics and balance framework; **approve only
presentation-level timing flavor at first**."* The load-bearing word is **"at first"** — this is a
sequence instruction, not a permanent ban. Phase 1 is "first." §02 then names what is deferred by
category: *"Fully unique move sets, **separate balance systems**, and extensive character-specific
cinematics are deferred until the base duel is stable."* Q14, Q15 and Q16 split are all separate
balance systems in miniature: difficulty, mobility, and safety respectively.

**2. All three candidate splits turned out to be balance, not flavour.** That is the finding of
the three sections above, and it was not the expected result:

| | Looks like | Is |
|---|---|---|
| Q14 play rate | animation feel | a **9% swing in Q7**, the game's difficulty dial — plus ~**+10% DPS and meter/s** on the combo |
| Q15 walk speed | movement personality | a **published balance stat** in every fighting game that has one, and under Q22 the difference between being able to disengage and rebuild meter or not |
| Q16 dodge distance | dodge feel | a per-fighter **safety** value against attack B's multi-hit sequence |

**There was no cheap flavour split available.** Every one of the three routes into the balance
layer the GDD defers by name.

**3. The schedule decides ties, and this one is not close.** The GDD's own safeguard requires
*"Validate both selectable avatars against the same collision, targeting, reach, and
arena-boundary tests."* At identical scalars, one shared montage set, and one `ABP_Fighter`, that
is **one test pass**. Split any of the three and the M1 gate, the Q10 range bands, the Q7 window,
and the Q2 health derivation each need checking twice. With the duel due **1 September** and M4
targeted functionally complete around 20 August (R7), a second validation pass is not affordable
and buys nothing the sheets have not already delivered.

**4. Prior art says the split is not what makes characters distinct anyway.** Smash Ultimate's
Peach and Daisy have identical frame data post-patch and are still unmistakably two characters —
orange flowers versus pink hearts. Mortal Kombat's ninjas were one digitised sprite, recoloured,
and became five of the most durable identities in the genre. **Presentation carried both cases.**

### The one asymmetry that cannot be zeroed, and it is already live

**Height. 183 cm versus 173 cm, published in the GDD.** It drives capsule half-height, hurtbox
volume, attack-trace socket heights, and how the rival's `MinRange`/`MaxRange` bands read in
practice. The GDD states the requirement directly: *"The height difference must not create unfair
hidden reach or collision behavior."*

This is precisely the residual Smash could not eliminate either — the one difference that survived
Daisy's patching was that she is slightly shorter, which changes her hurtbox. And Street Fighter 6
supplies the sharper warning: **walk speed does not even predict traversal time there**, because
collision box size interacts with it — Zangief at 3.64 crosses the screen faster than JP at 3.70.
**In a game whose two avatars already have different capsules, a speed split would not produce the
clean difference the designer intends.** It would produce a difference nobody can predict.

**So the M1 gate's same-tests requirement is not boilerplate — it is the mitigation for the one
asymmetry that exists whatever Q14/Q15/Q16 resolve to.**

### Where the differentiation budget is actually spent

Nothing is being withheld. It is being routed:

| Channel | Echo | Nova | Milestone |
|---|---|---|---|
| Silhouette, palette, costume, insignia | already authored on p.12 | already authored on p.13 | M5-06 (proxies until then) |
| Locomotion **cadence** at identical 600 uu/s | longer stride, settle at the end | short, frequent, torso leading | M1 (asset selection) → M5 (tuned) |
| Dodge **pose content** at identical 400 cm / 0.28 s / 0.12 s | measured step-out, guard reforming | low lateral scramble, recovers leaning in | M1 → M5 |
| `StanceAdditivePose` (§4.2) | upright / technical | compact / layered | M1 |
| `AccentColor` | restrained orange | preserved palette; **cyan-white is not a costume recolor** | M1 |
| `IntroMontage` | abbreviated | abbreviated | M4 → M5 |
| **Items 43 / 44 emissive channel**, if approved | spine lines + back core | back yoke, smaller area | **M5-06 only** |

**The player will read Nova as quicker.** Apparent speed in third-person action is dominated by
animation cadence and camera behaviour, not by the movement component's scalar — which is exactly
why two characters with identical frame data can feel different.

### The honest counterpoint, stated so it is a decision and not a drift

**If the designer's intent is that Echo and Nova *play* differently and not merely look
differently, Phase 1 as recommended does not deliver that.** Three "identical" recommendations in
a row add up to a real design position, and it should be accepted explicitly rather than arrived
at by accumulation. The position is: *in Phase 1 Echo and Nova are one fighter with two
presentations, and mechanical differentiation is deferred until the base duel is stable* — which
is what the GDD says to do, and which the recovered sheets make affordable in a way it would not
have been without them.

**Reopening it is a Phase 2 conversation**, and it will be a better one then: Q7 will have been
playtested, Q2 will be locked, and a split can be **measured** instead of guessed.

---

*Research note: 10 sources this dispatch, against a 15-source cap. Item 45 was deliberately not
searched — per the dispatch, and because "SFN" is a mark invented for this project's concept art
and there is nothing to look up. Destiny 2 was searched as prior art for a body-mounted
resource-ready channel and is **cited as not usable** rather than stretched: the results describe
it as a HUD readout with body glow appearing only on specific cosmetic ornaments.*

*Prior art consulted for items 43 and 44: Dead Space (RIG spine + circular Stasis bar, diegetic UI
design intent and its standing criticism), For Honor (Revenge — body glow + HUD shield + audio,
plus shipped colour-blind support), Doom Eternal (orange/blue stagger flash, player-disableable),
Devil May Cry 5 (Sin Devil Trigger gauge glow at full charge; chest and head glow when active),
Overwatch (silhouette-first readability, signature palette per hero, per-ability VFX and audio),
Tekken 8 (Heat aura + bar; the effects-volume readability complaint). Unreal-side: cached dynamic
material instance + `Set Scalar Parameter Value` on a scalar emissive parameter, with the
create-once-and-cache rule.*

---
