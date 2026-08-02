# Group 04 — Spacing and arena · Q24, Q10, Q12, Q13, Q11 + the mezzanine question

**Dispatched:** 2026-08-02 · designer agent, group 04 of the open-question sweep.
**Consumes:** `gdd/INDEX.md`, `gdd/sections/04-crimson-vanguard-authored-rival-ai.md`,
`gdd/sections/08-visual-assets-and-official-version-1-arena.md`,
`gdd/reference/page-11-established-arena-reference.md`,
`gdd/reference/OPEN-QUESTION-IMPACT.md` §2, `design-brief.md` §12.4, §13.2 rows 38–41
and 52, §14 "Spacing", `design/decisions.md` (Q22 APPROVED, groups 02 and 03).
**Produces:** answers to **Q24, Q10, Q12, Q13, Q11** and to the new **mezzanine
reachability** question raised by the recovered arena sheet. Nothing else.

> **EVERY ANSWER IN THIS FILE IS `PROPOSED`, NOT DECIDED.**
> All six items are **KIND B** design items. A designer dispatch researches and
> recommends; it does not settle. The human designer of record owns every number here.
> Each entry stays open in `TODO.md`, marked PROPOSED, until the designer approves or
> changes it.

---

## Binding context

### Q22 is APPROVED and binding

`design/decisions.md`, 2026-08-02: `MinHealthFloor = 1` on the rival from `BeginPlay`,
lowered to `0` only by `ClashSuccess()`. **The Final Clash is the only way to win.**

Consequence for spacing: the duel has a mandatory tail in which the rival is pinned at
1 HP and the player is farming meter. **Spacing must stay interesting when damage has
stopped mattering.** A range layout that lets the player park at one distance and win
by attrition is not a risk here — attrition cannot win — but a layout that lets the
player park *out of reach* and stall is, because the duel then has no clock (Q23
recommends no timer) and no way to end. This drives two of the answers below: the
arena's long axis is bounded, and `BTTask_Idle_Reposition` is required to advance
rather than idle when nothing is eligible.

### Values from groups 02 and 03, PROPOSED and used as inputs here

Player health **100** · rival health **1200** · rival damage **A 32 / B 25 / C 27 /
D 18** (% of player health) · player combo **3 sections, ~1.0 s** · i-frames **0.28 s**
· perfect dodge **0.12 s** · counter whiff lockout **0.55 s**. If any of these move,
nothing in this file breaks — spacing is largely orthogonal to the damage economy —
but the telegraph note in Q10 below depends on the 0.55 s lockout.

### The warning group 03 handed this group

> "**Do not author all four attacks near 0.95 s**" — a slow Phase 1 telegraph lets
> counter-spam beat the 0.55 s whiff lockout.

Telegraph durations themselves are **Q25 and belong to another group.** But range bands
decide *which* attacks the player meets *most often*, so the bands and the telegraph
spread interact. That interaction is written out at the end of the Q10 section as a
constraint handed forward to Q25. It is not a Q25 answer.

---

## What the recovered arena sheet settled, and what it did not

`gdd/reference/page-11-established-arena-reference.md` was recovered from the PDF's
embedded JPEG on **2026-08-02**. No previous agent had it.

**Settled — the build may rely on these:**

| Constraint | Source |
|---|---|
| Plan shape is **broadly rectangular, longer than wide**, corners chamfered not square | p.11 geometry table |
| **One flat concrete floor.** No elevation change, no stairs into play, no pits | p.11 geometry table |
| **Zero obstacles** on the central floor — no crates, columns, or props | p.11 panel 1 |
| **No hazards**, consistent with GDD §08 "without adding gameplay hazards" | p.11 + §08 |
| **One bright doorway centred on the far short wall** — the Vanguard entrance axis | p.11 panel 1, §08 |
| Opposite short end is a **closed wall** landmarked by an X-braced steel truss | p.11 panel 2 |
| Solid concrete boundary on all sides; **orange railings mark the floor perimeter** | p.11 geometry table |
| A **mezzanine ring** above the floor with **no visible route into the play space** | p.11 geometry table |

**Not settled — and the sheet cannot settle it:**

> "**AMBIGUOUS — no dimensions are printed anywhere.** There is no scale bar, no
> measurement, and no human figure in any of the three views. **The playable footprint
> cannot be read off this sheet.**"

So **Q24 is still a design decision, not a transcription.** Anyone who claims to have
measured the arena from the art is guessing.

**The one thing the sheet does change about how Q24 must be answered:** the hall is
rectangular, so centre-to-short-wall and centre-to-long-wall are different distances.
**Any single "arena radius" is wrong.** Every footprint statement below is **two
dimensions**.

### Character scale — GDD-published, fixed, not open

| Fighter | Height | Source |
|---|---|---|
| Agent Nova | **5'8" / 173 cm** | GDD §07 |
| Agent Echo | **6'0" / 183 cm** | GDD §07 |
| Crimson Vanguard | **6'10" / 208 cm** | GDD p.10, recovered 2026-08-02 |

And the rule every number in this file has to survive:

> "The height difference **must not create unfair hidden reach or collision behavior**."
> — GDD §07

### Units

**Unreal units are centimetres. 1 uu = 1 cm; 100 uu = 1 m.** This is the engine default
and every value below is stated in centimetres with the metre equivalent in brackets.
([Level Design Book — Metrics](https://book.leveldesignbook.com/process/blockout/metrics),
[techarthub — Scale and Measurement Inside Unreal Engine](https://techarthub.com/scale-and-measurement-inside-unreal-engine/),
[World of Level Design — UE5 Player Scale and Environment Dimensions](https://www.worldofleveldesign.com/categories/ue5/guide-to-scale-dimensions-proportions.php))

---

## Q24 — Arena playable footprint

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-21** — gray-box `L_ShatteredRing`. This is a genuine
  block: a floor cannot be blocked out without dimensions.
- **Value lives in:** `L_ShatteredRing` (`design-brief.md` §13.2 row 52). Recommended to
  *also* live as two floats on `DA_TuningGlobals` — `ArenaLongAxisCm`,
  `ArenaShortAxisCm` — because **Q13 is defined as a fraction of the long axis** and the
  two must not be able to drift apart.
- **GDD range:** **the GDD publishes none.** §08 specifies the arena entirely in
  *function* — "open, readable space for spacing, lock-on, dodges, counters, and Final
  Clash staging" — and page 11 carries no scale bar. There is no number to carry through
  and nothing here supersedes anything.

### Proposed value

> **Playable floor: 2400 cm × 1600 cm (24 m × 16 m), rectangular, long axis = the
> doorway axis. Four corners chamfered at 45° with a 250 cm leg.**

| Property | Value | In metres |
|---|---|---|
| Long axis (doorway → truss wall), **X** | **2400 cm** | 24.0 m |
| Short axis (side wall → side wall), **Y** | **1600 cm** | 16.0 m |
| Corner chamfer, each of 4 corners | **250 cm** leg, 45° | 2.5 m |
| Centre → short (end) wall | **1200 cm** | 12.0 m |
| Centre → long (side) wall | **800 cm** | 8.0 m |
| Corner-to-corner diagonal (uncut) | **≈ 2884 cm** | 28.84 m |
| Net walkable area | ≈ **371.5 m²** (384 − 4 × 3.125) | — |
| Wall height to mezzanine underside | **≥ 450 cm** (provisional, camera-driven — see Item 18) | 4.5 m |

**Definition:** the playable footprint is the **NavMesh-walkable rectangle between the
inside faces of the wall shells**. The orange perimeter railings sit **on** that line,
so the railing the player sees *is* the boundary they collide with. There is one
boundary, not two.

### Why

1. **It is the shape the art shows, at a size a 1v1 fighting game actually uses.**
   Tekken's *standard* stage is **24 × 24 in-game metres**; Tekken 8 ships stages from
   **16 × 24** (*Midnight Siege*) up to **32 × 24** (*Elegant Palace*), with walls on all
   but a handful. **24 × 16 m is Tekken's smaller walled stage, rotated.** That is a
   directly relevant precedent: a walled, hazard-free, flat, one-versus-one duel floor.
   ([Wavu Wiki — Stage](https://wavu.wiki/t/Stage),
   [VideoGamer — Tekken 8 stages](https://www.videogamer.com/guides/tekken-8-stages/))
2. **It satisfies the two things §14 says it has to fit.** Q13's travel is 25% of the
   long axis (600 cm) and Q21's separation has 1000–1300 cm of guaranteed room. Both
   arithmetic checks are in the closing sections.
3. **Longer than wide serves the doorway.** The rival's entrance walk (`LS_VanguardEntrance`,
   M4) runs the full 2400 cm long axis, which is a real entrance rather than three steps.
   The GDD assigns the far doorway as the "dedicated Crimson Vanguard entrance axis" —
   that axis wants length.
4. **16 m across serves side-on readability.** GDD §08 requires "readable silhouettes
   and attack direction during lateral exchanges." At 800 cm from centre to a side wall,
   a lateral exchange has 16 m of lane and the camera is never jammed against geometry
   during a strafe. A narrower hall would pin the spring arm on the side walls.
5. **371 m² of empty floor is defensible against the "no obstacles" finding.** With zero
   cover, every square metre is fight space. A cluttered arena of the same footprint
   would play much smaller; this one does not.
6. **The chamfers are a gameplay feature, not decoration.** A 250 cm 45° cut removes the
   90° pocket where a player can wedge themselves so the rival's approach vector and the
   camera both fail. It matches what the art shows and it deletes a known third-person
   combat bug for free.

### Prior art (real games, named)

| Source | Number | Note |
|---|---|---|
| **Tekken 7 / 8** — standard stage | **24 × 24 m** | Walled 1v1 duel floor |
| **Tekken 8** — *Midnight Siege* | **16 × 24 m** | The closest published analogue to this proposal |
| **Tekken 8** — *Elegant Palace* | **32 × 24 m** | Upper bound of "normal" |
| **Tekken 8** — *Arena* | **24 × 24 m**, octagonal caged | Chamfered/angled boundary precedent |
| **Unreal / World of Level Design** | player base scale **180 cm = 180 uu** | Confirms 1 uu = 1 cm and the humanoid reference height |
| **Souls-likes (Sekiro, Elden Ring)** | **no figure found** | Searched; FromSoftware arena dimensions are not published or reliably datamined. **Cited as not found rather than estimated.** |

### Interaction with the rest

- **Q13** is expressed as a fraction of `ArenaLongAxisCm`. Change the arena and D's dash
  changes with it, by construction.
- **Q21 (not mine)** — see the closing section. 2400 × 1600 supports a separation of
  **1000–1300 cm**, with 1300 cm the largest value achievable from anywhere in the room.
- **Q10** — the longest attack band (D, 840 cm) is **35% of the long axis**, so the rival
  threatens roughly a third of the room's length from a standing start. That is the
  pressure level "armored pressure" implies without making the floor decorative.
- **Q11** — the 2884 cm diagonal is the number lock-on has to beat. It does; see Q11.
- **A gap this exposes, and it is not one of my six.** `design-brief.md` §13.2 has **no
  row and no Q number for Crimson Vanguard's `MaxWalkSpeed` / reposition speed.** With a
  2400 cm long axis and Unreal's default player `MaxWalkSpeed` of 500 cm/s, **a rival
  slower than the player can be kited indefinitely** — the player runs, the rival never
  arrives, and Q22 guarantees there is no other way for the duel to end.
  **Constraint, stated for whoever owns it:** the rival's *advance* speed must be
  **≥ the player's `MaxWalkSpeed` (Q15)**, or the long axis must shrink. Recommended
  new TODO item. **I am not assigning it a value or a Q number.**
- Lock-on strafing usually runs at a reduced speed. If the player's locked-on strafe
  speed is lower than their free-run speed, the kite hole only opens when the player
  **breaks lock and runs**, which the HUD can make legible. Worth knowing; still not a
  substitute for the rival being fast enough.

### The honest alternative, if the designer wants a tighter fight

**1800 × 1200 cm (18 × 12 m).** Pressure goes up, kiting shrinks, camera work gets
easier, and the entrance walk gets weaker. The cost is Q21: a 1200 cm separation would
be **67% of the long axis** and would routinely clamp against a wall. If the designer
picks this, **Q21 must come down to roughly 700–900 cm** and Q13 to 450 cm (same 25%
fraction). I recommend 2400 × 1600 but the smaller room is a coherent package, not a
worse one.

---

## Q10 — Attack A–D range bands (cm)

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** **M2-04** — populate `DT_VanguardAttacks`.
- **Value lives in:** `DT_VanguardAttacks` → `S_VanguardAttackDef.MinRange` /
  `.MaxRange` (`design-brief.md` §13.2 row 38).
- **GDD range:** **the GDD publishes none.** §04's four-attack table gives *purpose*
  only — A "close-range committed gauntlet force", B "committed forward-pressure
  sequence", C "armored reach and space control", D "short propulsion-assisted
  approach". Those four phrases are the entire authored constraint, and the bands below
  are built to express exactly them and nothing more.

### First: how distance is measured, because the bands are meaningless without it

**`DistanceToTarget` = horizontal (Z-zeroed) distance between the two capsule
centres**, written each tick by `BTService_UpdateCombatData` into the blackboard.

```
FVector D = RivalActor->GetActorLocation() - TargetActor->GetActorLocation();
D.Z = 0.f;
Blackboard->SetValueAsFloat("DistanceToTarget", D.Size());
```

Three reasons this is the definition and not `GetDistanceTo`:

1. **`GetDistanceTo` is 3-D and the rival's origin sits higher.** With the capsule
   half-heights proposed below, the rival's actor origin is 12.5 cm above Echo's and
   17.5 cm above Nova's. At 200 cm horizontal separation the 3-D distances are 200.39 cm
   and 200.76 cm — **a 0.37 cm difference between the two player characters.** That is
   sub-centimetre and will never be felt, so this is not a scare story; but zeroing Z
   costs one line and removes the only mechanism by which the height difference could
   leak into range selection at all. GDD §07 asks for exactly that assurance.
2. The floor is flat and hazard-free (page 11), so Z carries no information.
3. Capsule-centre to capsule-centre is the number the developer can actually read off a
   `DrawDebugLine` in the editor, which matters for tuning.

**Capsule sizing, proposed, and it is load-bearing for the bands:**

| Actor | Capsule radius | Capsule half-height | Note |
|---|---|---|---|
| Agent Echo (183 cm) | **40 cm** | **91.5 cm** | |
| Agent Nova (173 cm) | **40 cm** | **86.5 cm** | **Radius identical to Echo, deliberately** |
| Crimson Vanguard (208 cm) | **60 cm** | **104 cm** | Broad: p.10 shows ~2x the centre figure's shoulder width |

**The radius must be identical for Echo and Nova.** Range is a horizontal measurement,
so radius — not height — is what decides at what separation each fighter can be struck.
Giving Nova a smaller radius would make every one of the bands below behave differently
against her, which is precisely the "unfair hidden reach or collision behavior" GDD §07
forbids. Height may differ; radius may not. (Unreal's own default character capsule is
**radius 34 / half-height 88**, for reference —
[Set Capsule Half Height, UE 5.8 docs](https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/Components/Capsule/SetCapsuleHalfHeight?lang=en-US).)

**Therefore the minimum achievable `DistanceToTarget` is 40 + 60 = 100 cm.** The
fighters physically cannot be closer. Any band whose `MinRange` exceeds 100 cm is
unselectable at contact — which is the single most common way a melee AI ends up
standing inside the player doing nothing.

### Proposed value

| Attack | GDD purpose | `MinRange` | `MaxRange` | Band width |
|---|---|---|---|---|
| **A** | Close-range committed gauntlet force | **0 cm** | **260 cm** | 260 |
| **B** | Committed forward-pressure sequence | **90 cm** | **520 cm** | 430 |
| **C** | Armored reach and space control | **240 cm** | **420 cm** | 180 |
| **D** | Short propulsion-assisted approach | **400 cm** | **840 cm** | 440 |

In metres: A 0–2.6 · B 0.9–5.2 · C 2.4–4.2 · D 4.0–8.4.

**These are identical in Phase 1 and Phase 2.** Phase 2 re-times the same four attacks;
GDD §04 changes *weighting*, not reach. Range lives in `S_VanguardAttackDef` (per
attack), **not** in `S_AttackPhaseTuning` (per attack per phase). One value, one place.

### Why each number

- **A `MinRange` = 0, not 100.** A is the contact attack and must be legal at contact.
  Setting it to 0 rather than to the theoretical 100 cm floor means the band survives any
  future capsule change — a Paragon heavy swap (Q30, §12.4) will move the rival's radius,
  and A must not silently become unselectable when it does.
- **A `MaxRange` = 260.** A 208 cm figure with an oversized gauntlet, stepping into the
  swing: 60 cm of own capsule + roughly 160 cm of arm-and-step reach + 40 cm of target
  capsule ≈ 260. It is a strike, not a lunge.
- **B `MinRange` = 90, below the 100 cm contact floor.** This is the most deliberate
  number in the table. It makes **A and B both eligible at every distance from contact
  out to 260 cm** — see the cooldown starvation check. B is a *sequence* that advances,
  so it is legitimately usable point-blank; the first beat lands, the rest presses
  forward.
- **B `MaxRange` = 520.** The outer edge at which a committed forward sequence can still
  close and connect. At 520 the sequence must cover roughly 270 cm across its beats.
  **See the note below about `MaxTravelDistance` for B.**
- **C 240–420, the narrowest band.** C is "space control" — a long, committed reach that
  is *specifically* the wrong answer at contact and the wrong answer at gap-closer range.
  A narrow band is what makes C read as a distinct spacing tool rather than a second A.
  Its `MinRange` of 240 is what gives the player a real reason to close: **stepping
  inside 240 cm removes C from the rival's options entirely.**
- **D 400–840.** The gap closer. Its `MaxRange` of 840 is **derived, not chosen** — it is
  Q13's 600 cm travel cap plus the 240 cm at which D finishes (see Q13). Below 400 there
  is nothing to close, and a gap closer fired at 300 cm is a whiff by design.

### Prior art (real games, named)

Honest statement of what the research found and did not:

- **No shipped game publishes its enemy attack-range table in centimetres.** I searched
  for it; it is not available. Nothing below is presented as a datamined figure.
- **Unreal's own AI convention** is the usable anchor: melee behaviour-tree examples
  cluster around a **150 uu (1.5 m)** attack radius, versus **2000 uu (20 m)** for a
  ranged archetype, with the range held as a blackboard/config value rather than
  hard-coded. ([Gaetano Tonzuso — Behavior Tree Services and Blackboard Keys in UE5 C++](https://medium.com/@gaetano.tonzuso/expanding-the-ai-brain-behavior-tree-services-and-blackboard-keys-in-unreal-engine-5-c-97f7784f74d1),
  [Unreal Engine 4 Scripting with C++ Cookbook — AI for a Melee Attacker](https://www.oreilly.com/library/view/unreal-engine-4/9781785885549/ch10s09.html))
  **A's 260 cm sits above that 150 uu norm and should — Crimson Vanguard is 208 cm with
  oversized gauntlets, not a 180 cm human with a sword.**
- **Root-motion melee travel in Unreal practice runs around 400 uu (4 m) per attack**,
  shortened by Motion Warping when the target is nearer. That is the documented pattern
  Elden-Ring-style attack tracking is built on, and it is the direct precedent for B's
  advance and D's dash. ([Epic — Motion Warping in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine),
  [Quod Soler — How to Use Motion Warping in UE5](https://www.quodsoler.com/blog/motion-warping-character-attacks-using-blueprints-no-c-required))
- **500 uu (5 m) is the commonly used "nearby actor" detection radius** in the same
  tutorials — which is roughly where B's 520 cm outer edge lands. Not a coincidence
  worth much, but it is the same order of magnitude as working practice.

### Interaction with the rest

**1. Range is evaluated once, at Select Attack, and then the attack commits.** After
`BTTask_SelectAttack` writes `SelectedAttackRow`, **nothing re-checks range.** If the
player leaves the band during Telegraph, the attack whiffs. This is not a concession —
GDD §04 says "attacks are committed rather than random," and every recover window in the
game exists because attacks can miss. **The developer must not add a range re-validation
decorator to the Telegraph or Active tasks.** Doing so would delete the punish loop.

The magnitude: at 500 cm/s the player covers 50–100 cm during the 0.10–0.20 s Select
state alone, which is comparable to the 80 cm A→B overlap. Attacks will whiff regularly.
That is the game.

**2. Handed forward to Q25 — this is group 03's warning, made spatial.** Group 03
established that the 0.55 s counter whiff lockout (Q8) fails to punish counter-spam
against telegraphs near the Phase 1 maximum of 0.95 s, and warned Q25 not to author all
four attacks slow. The band layout says **which** attacks that warning binds hardest:

> The player spends most of the duel inside 260 cm, because that is where their own
> combo reaches. **A and B are therefore the attacks they see most often, and are the
> attacks counter-spam would exploit most.** So **A and B should carry the *short* end of
> the GDD telegraph range (0.55–0.70 s in Phase 1) and C and D the long end
> (0.75–0.95 s)** — the slow, readable telegraph belongs to the attacks that come from
> across the room and have travel time of their own to sell them.

That is a constraint on Q25, not an answer to it. **Q25's owner decides the four
numbers.** The spread it should preserve: fast at close range, slow at long range.

**3. Attack B needs a travel cap and §13.2 has no row for one.** Row 41 /
`MaxTravelDistance` is written as *"Attack D max travel distance."* But B is a
forward-pressure **sequence** with a 430 cm band, so at its outer edge it must advance
roughly 270 cm to connect. Uncapped, B becomes a second gap closer and the "no hidden
full-arena snap" rule leaks. **Recommendation: make `MaxTravelDistance` a column every
row uses, with A and C at 0 or a small step value.** I am **not** proposing B's number —
that is a new open item, adjacent to Q13 but not covered by it.

**4. Attack B's damage split.** Group 02 flagged that if B is authored with several
`ANS_ActiveHit` windows each reading `Damage = 25`, B deals 50–75% of player health in
one attack. The 430 cm band makes B the most-used attack in the table, which raises the
stakes on that rule. Group 02's proposed fix — the Data Table row is *total* damage,
split across notifies — still stands and matters more given this layout.

**5. Phase 2 weighting has no Q number and I am not inventing one.** GDD §04 requires
Phase 2 to use "more aggressive close-range and gap-closing weight," which in this
layout means A and D weighted up and C weighted down. `SelectionWeight` appears in
`design-brief.md` §11.4 but has **no row in §13.2 and no Q number**. Recommended as a
new TODO item. The bands are neutral to whatever the weights become.

---

## Q12 — Per-attack cooldown

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** **M2-04** — populate `DT_VanguardAttacks`.
- **Value lives in:** `DT_VanguardAttacks.Cooldown` (`design-brief.md` §13.2 row 40).
  **Proposed relocation: put it inside `S_AttackPhaseTuning`, not `S_VanguardAttackDef`**
  — see "one data path" below.
- **GDD range:** **the GDD publishes none.** §04 states only that Select Attack chooses
  "by range and cooldown," which is what establishes that a cooldown exists at all. No
  duration is given anywhere.

### The cycle arithmetic everything below rests on

Summing the GDD's six state ranges (§04), with Active Attack **not** phase-scaled:

| | Reposition | Select | Telegraph | Active | Recover | Neutral | **Full cycle** |
|---|---|---|---|---|---|---|---|
| **P1 fastest legal** | 0.60 | 0.10 | 0.55 | 0.18 | 0.45 | 0.10 | **1.98 s** |
| **P1 midpoint** | 0.90 | 0.15 | 0.75 | 0.315 | 0.675 | 0.15 | **2.94 s** |
| **P1 slowest legal** | 1.20 | 0.20 | 0.95 | 0.45 | 0.90 | 0.20 | **3.90 s** |
| **P2 fastest legal** | 0.35 | 0.10 | 0.40 | 0.18 | 0.35 | 0.10 | **1.48 s** |
| **P2 midpoint** | 0.575 | 0.15 | 0.575 | 0.315 | 0.55 | 0.15 | **2.315 s** |
| **P2 slowest legal** | 0.80 | 0.20 | 0.75 | 0.45 | 0.75 | 0.20 | **3.15 s** |

Every cooldown has to live between two walls:

- **No-repeat wall (lower).** `Cooldown > midpoint cycle`, or the same attack can fire
  twice in a row. Two identical attacks back to back is the failure mode that makes an
  authored rival read as random. → **P1 > 2.94 s · P2 > 2.315 s**
- **No-starvation wall (upper).** In a zone where exactly **N** attacks are in band,
  strict round-robin re-offers each attack every `N × cycle` seconds. So
  `Cooldown ≤ N × fastest legal cycle`. At **N = 2** → **P1 ≤ 3.96 s · P2 ≤ 2.96 s**

**That is the whole finding, and it is tighter than it looks:** the GDD's own state
ranges leave a legal cooldown window only **1.02 s wide in Phase 1** and **0.645 s wide
in Phase 2**, given two-deep range coverage. There is not much room to be wrong here.

### Proposed value

| Attack | **Phase 1** | **Phase 2** | In P1 window (2.94, 3.96] | In P2 window (2.315, 2.96] |
|---|---|---|---|---|
| **A** — gauntlet force | **3.0 s** | **2.5 s** | yes | yes |
| **B** — forward pressure | **3.5 s** | **2.6 s** | yes | yes |
| **C** — reach / space control | **3.6 s** | **2.7 s** | yes | yes |
| **D** — propulsion approach | **3.8 s** | **2.8 s** | yes | yes |

Ordering is deliberate: **the cheapest, most repeatable attack has the shortest
cooldown, the biggest commitment has the longest.** A is the bread-and-butter pressure
tool; D is the spectacle.

### Semantics — exactly how the clock runs

1. `LastUsedTime[Attack]` is a float map on `BP_VanguardController`, initialised to a
   large negative number at `BeginPlay` so **all four attacks are eligible on the first
   selection**.
2. The stamp is written in **`BTTask_ReturnToNeutral`**, not at Telegraph or Active. The
   cooldown therefore measures *time since the attack finished*, which is the only
   definition that stays stable if Q25 re-times the states.
3. `BTTask_SelectAttack` filters on
   `(Now - LastUsedTime[Row]) >= Row.PhaseTuning[CurrentPhase].Cooldown`
   **and** `MinRange <= DistanceToTarget <= MaxRange`, then does the authored weighted
   pick among survivors. **Deterministic authored filtering and weighting — no learning,
   no adaptation, no model call.**
4. If the survivor set is **empty**, `BTTask_SelectAttack` fails and the tree returns to
   `BTTask_Idle_Reposition`. **See the advance rule, below — this is not allowed to be a
   no-op.**

### One data path — and this is why it belongs in `S_AttackPhaseTuning`

`design-brief.md` §13.2 row 40 puts `Cooldown` on the attack. Phase 2 needs shorter
cooldowns (the cycle is ~21% faster at midpoints, so a Phase 1 cooldown starves the
rival in Phase 2 — proven in the closing section). There are two ways to get that:

- **Rejected:** add a `Phase2CooldownMultiplier`. A second mechanism, a second thing to
  forget, a second thing to validate.
- **Proposed:** move `Cooldown` into **`S_AttackPhaseTuning`**, the per-attack-per-phase
  struct the brief already defines for the Phase 2 re-timing. Then the cooldown re-times
  through **the exact same data path as Telegraph and Recover**, is edited in the same
  Data Table row, and is validated by the same range-check the brief asks for in §13.1.

This also produces a free safety property: **P2 cooldowns are uniformly shorter than P1
cooldowns, so crossing into Phase 2 can only ever make more attacks eligible, never
fewer. The phase transition cannot starve the rival.**

### Prior art (real games, named)

- **This is the weakest-sourced item in the file, and I will say so plainly.** No shipped
  action game publishes per-attack AI cooldowns, and none were found. The values above
  are derived entirely from the GDD's own published state ranges by the two-wall
  argument, not imported from anywhere.
- The only real prior art is structural: Unreal's standard melee-AI pattern is
  *"if within `AttackRadius` of the opponent, damage them every `AttackCooldown`
  seconds"* — i.e. cooldown and range are the two authored filters, exactly as used here.
  ([UE4 Scripting with C++ Cookbook — AI for a Melee Attacker](https://www.oreilly.com/library/view/unreal-engine-4/9781785885549/ch10s09.html))
- Fighting-game move recovery is not a usable analogue — a human player's "cooldown" is
  their own recovery frames, which the GDD already models separately as the Recover
  state. Cooldown here is a *repetition governor*, a different thing.

### Interaction with the rest

- **The advance rule is a hard dependency, not a nicety.** With four attacks, two range
  walls each, and cooldowns, there will be moments when zero attacks are eligible. §14
  names this: *"or `BTTask_Idle_Reposition` will loop repositioning."* The fix is to make
  that loop **purposeful**:

  > **`BTTask_Idle_Reposition` never idles in place when the eligible set is empty.**
  > `BTService_UpdateCombatData` writes a blackboard float `DesiredRange` = the midpoint
  > of the band of the **nearest attack that is off cooldown**. Reposition moves toward
  > `DesiredRange` (a `MoveTo` with an acceptance radius, or direct steering) and only
  > strafes/holds when `DistanceToTarget` is already inside an eligible band.

  With that rule the rival at 700 cm with D on cooldown **walks in to B's band** instead
  of shuffling. The reposition loop §14 warns about becomes the intended behaviour rather
  than a bug, and it is still fully deterministic authored logic.
- **Q26 (Impact cooldown, 7.0 s, group 03) is a completely separate clock** and must not
  be merged with these. Different owner (`BP_ImpactWindowDirector`), different purpose.
- **Q18 (BTTask montage failsafe margin)** interacts: if a montage failsafe fires and
  aborts an attack early, `BTTask_ReturnToNeutral` must **still stamp the cooldown**, or
  a repeatedly-failsafed attack becomes spammable.
- **Countered attacks.** Group 03 routes a successful counter as an interrupt through the
  sequence to Return to Neutral. Since the stamp lives in that task, **a countered attack
  still goes on cooldown**, which is correct: the player earned the reprieve.

---

## Q13 — Attack D max travel distance

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** **M2-04** — populate `DT_VanguardAttacks`.
- **Value lives in:** `DT_VanguardAttacks.MaxTravelDistance` (`design-brief.md` §13.2
  row 41). **Proposed: store the *fraction* on `DA_TuningGlobals` and compute the
  centimetre value** — see below.
- **GDD range:** **the GDD publishes no number, but it publishes a hard rule.** §04,
  Attack D readability requirement:
  > "Thruster cue before movement; **no hidden full-arena snap**."

  That sentence is the whole constraint, and it is a constraint on *fraction of the
  arena*, not on centimetres — which is exactly why §14 asks for it as a fraction.

### Proposed value

> **`AttackD_TravelFractionOfLongAxis = 0.25`** on `DA_TuningGlobals`
> **→ `MaxTravelDistance` = 0.25 × 2400 = 600 cm (6.0 m).**

The Data Table's `MaxTravelDistance` is **computed from the fraction at load**, or the
authored 600 is validated against `0.25 × ArenaLongAxisCm` by the same editor
range-check `design-brief.md` §13.1 already asks for. **The two cannot drift apart,
which is what §14 asked for.**

### Arena-fraction check — is 600 cm a "full-arena snap"?

| Against | Value | D's 600 cm as a fraction |
|---|---|---|
| Long axis (doorway axis) | 2400 cm | **25.0%** |
| Short axis | 1600 cm | 37.5% |
| Corner-to-corner diagonal | 2884 cm | 20.8% |
| Max on-axis separation, capsules deducted | ≈ 2300 cm | 26.1% |

**The rival cannot cross the room, cannot cross half the room, and cannot cross a
quarter of the diagonal.** At the very most it covers a quarter of the doorway axis. The
GDD's rule is satisfied with a wide margin, and it stays satisfied automatically if the
arena changes size.

### How the travel is realised, and where it stops

**Motion Warping** (`MotionWarpingComponent`), which is the documented Unreal mechanism
for exactly this: an attack montage carries root motion, and the warp shortens it when
the target is closer than the authored distance.
([Epic — Motion Warping in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine))

- **`FinishOffset = 240 cm`** — the separation D aims to end at.
- Warp target set at the **start** of `ANS_ActiveHit`:
  `TargetLocation = PlayerLocation + (RivalToPlayer_Normalised * -1 * 240)`, Z locked to
  the floor plane.
- **Actual travel = `clamp(DistanceToTarget - 240, 0, 600)`.**
- A second, independent **hard clamp inside the notify state** re-clamps the accumulated
  translation to `MaxTravelDistance`. Belt and braces: if the warp target is ever
  mis-set, the worst outcome is a short dash, never a teleport across the arena.

**This is where D's `MaxRange` of 840 comes from:** 600 + 240 = 840. At D's outer edge the
clamp is exactly reached; beyond it, D would fall short and is therefore not offered.
**Q10 and Q13 are two views of one number** — if the designer changes the fraction, D's
`MaxRange` must move with it.

**Where D lands is also deliberate:** 240 cm is inside A's band (0–260) and at C's inner
edge (240–420). So the attack that closes the gap deposits the rival exactly where its
close-range options open. The follow-up pressure is a property of the geometry, not of
any scripted combo.

### The readability problem this creates, handed to Q25

600 cm of travel has to happen inside the Active Attack state, which the GDD fixes at
**0.18–0.45 s in both phases**:

| Active duration | Implied dash speed | Reads as |
|---|---|---|
| 0.18 s (GDD minimum) | **3333 cm/s** = 33.3 m/s | a teleport |
| 0.30 s (midpoint) | 2000 cm/s = 20 m/s | very fast, marginal |
| 0.45 s (GDD maximum) | **1333 cm/s** = 13.3 m/s ≈ 48 km/h | fast, readable, sells thrust |

> **Constraint handed to Q25 (not an answer to it): Attack D's Active Attack value
> should be authored at the top of the GDD range — 0.40–0.45 s.** At the bottom of the
> range, a 600 cm dash *is* the "hidden snap" the GDD forbids, even though the distance
> passes the fraction test. The alternative, if the designer wants a short Active for D,
> is to lower the travel fraction below 0.25.

Two supporting requirements, both straight from the GDD line:

1. **The thruster cue lives in `ANS_Telegraph`, before any movement.** GDD: "Thruster cue
   before movement." Page 14 gives it something real to key off — the rear vanes and
   louvred amber vents.
2. **No movement at all during Telegraph.** If D drifts forward during its wind-up, the
   player's read of the distance is wrong and the dodge timing they learned stops
   working.

### Prior art (real games, named)

- **Unreal root-motion melee attacks are commonly authored around 400 uu (4 m) of
  travel**, warped shorter when the target is nearer — the pattern developers explicitly
  describe as "Elden Ring type movement" on melee attacks. **600 cm is above that norm,
  which is correct for a dedicated gap closer on a 208 cm armoured figure rather than a
  standard swing.** ([Epic Developer Community — correct way to add movement to melee attacks](https://forums.unrealengine.com/t/whats-the-correct-way-to-add-movement-to-melee-attacks/2081223),
  [Quod Soler — Motion Warping in UE5](https://www.quodsoler.com/blog/motion-warping-character-attacks-using-blueprints-no-c-required))
- **500 uu (5 m)** is the customary nearby-actor detection radius in the same tutorials —
  the same order of magnitude, which suggests 600 cm is a normal-sized dash and not an
  outlier.
- **No shipped game's gap-closer distance was found published in metres.** Not cited,
  because it does not exist in the sources I could reach.

### Interaction with the rest

- **Q24** — 600 cm is defined *as* 25% of the long axis. The two move together by
  construction. At the 1800 cm alternative arena, D becomes 450 cm and `MaxRange` 690.
- **Q10** — D's `MaxRange` = 600 + 240. Not independent.
- **Q21 (not mine)** — the separation must exceed **840 cm**, D's `MaxRange`, or the
  rival can dash the player down the instant the failed Clash ends. See the closing
  section.
- **Q6/Q7 (group 03)** — a 0.45 s Active window against a 0.28 s i-frame window means a
  correctly-timed dodge covers 62% of D's active frames. The player must dodge *into* the
  dash rather than early. That is consistent with group 03's front-loaded perfect-dodge
  design and needs no change here.
- **Attack B** also travels and has no cap (see Q10 note 3). Same column, value still
  open.

---

## Q11 — Lock-on max range, break range, camera interp speed

- **Kind:** B · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-16** — build `BP_LockOnComponent`.
- **Value lives in:** `BP_LockOnComponent` → `LockOnMaxRange`, `LockOnBreakRange`,
  `CameraInterpSpeed` (`design-brief.md` §13.2 row 39).
- **GDD range:** **the GDD publishes none.** §08 requires lock-on to be supported by the
  central floor and requires "reverse third-person framing — clear camera position behind
  the selected fighter." `design-brief.md` §1.2 fixes the architecture as a **single-target
  soft lock, toggle on/off**, because exactly one enemy exists.

### Proposed value

| Variable | Proposed | In metres | Tuning band |
|---|---|---|---|
| `LockOnMaxRange` (acquire) | **3000 cm** | 30.0 m | 2000–3200 |
| `LockOnBreakRange` (retain) | **3300 cm** | 33.0 m | must be ≥ 1.1 × acquire |
| `CameraInterpSpeed` | **6.0** | — | 4.0–8.0 |
| `TargetSocketHeight` (aim point on the rival) | **140 cm** above floor | 1.4 m | 120–160 |
| Lock-on camera pitch offset | **−8°** | — | −5 to −12 |

### Why — and the headline is deliberate

> **Both range values are set beyond the arena's 2884 cm diagonal, so inside
> `L_ShatteredRing` lock-on can never break because of distance.** It breaks only on
> player toggle, on either fighter's death, or when `BP_FinalClashDirector` takes the
> camera.

That is a design position, not an oversight, and here is the argument:

1. **There is exactly one target.** Lock-on acquisition in a multi-enemy game is a
   *search* — range narrows the candidate set. Here it is a *validity check*. Range has
   no selection work to do.
2. **Distance-based break is a punishment with no upside.** The only way to exceed
   2884 cm is to be in opposite corners, which is already the least interesting state of
   the duel. Dropping lock there takes the camera off the rival at the exact moment the
   player most needs to see it turn and start advancing.
3. **Souls-likes are widely criticised for lock dropping**, and the community complaints
   are specifically about lock-on range being too short or breaking at inconvenient
   moments. There is no equivalent body of complaint about lock being too sticky in a
   one-enemy fight.
   ([Dark Souls III — Adjusting the Lock-on Distance](https://steamcommunity.com/app/374320/discussions/0/351660338718061241/),
   [Improving Elden Ring's Lock-On Experience — Nik Jeleniauskas](https://www.jeleniauskas.com/writing/improving-elden-ring's-lock-on-experience))
   **Note: no published maximum lock-on distance in metres exists for any Souls title.
   I looked. The qualitative complaint is the finding; the number is not available.**
4. **The variables still exist and still do their job.** They are part of the shared
   player-combat framework and must not be hard-coded away. They are simply tuned out of
   the way for the one V1 arena. A second arena — deferred future scope — would tune them
   down.
5. **The hysteresis gap stays.** Break is 10% above acquire (3000 / 3300) so that even if
   the designer later drops both, the acquire/retain pair cannot chatter at the boundary.

**The alternative, if the designer wants distance to matter:** `LockOnMaxRange = 2000`,
`LockOnBreakRange = 3000`. Lock then breaks only at corner-to-corner distance and cannot
be re-acquired until the player closes to 20 m. This makes fleeing cost something —
which, given Q22 makes the Final Clash the only win, is a *legible* way to discourage
stalling. It is a real option and I have not ruled it out; I recommend the sticky version
because a camera that fights the player during a boss duel is a worse failure than a
player who runs away with the camera still pointed at the boss.

### Camera interp speed — the arithmetic

`RInterpTo` is exponential: the remaining angular error after `t` seconds is
approximately `e^(−S·t)`, where `S` is the interp speed.

| `CameraInterpSpeed` | Time to close 95% of the error | Feel |
|---|---|---|
| 2.0 | **1.50 s** | The value used in the common UE5 lock-on tutorial. **Too floaty here** — the rival crosses D's 600 cm dash in under half a second and the camera would still be catching up when the hit lands |
| 4.0 | 0.75 s | Smooth, slightly behind fast lateral motion |
| **6.0 (proposed)** | **0.50 s** | Settles inside one Telegraph window (0.55–0.95 s P1), so the frame is stable before the strike |
| 8.0 | 0.37 s | Crisp, begins to feel snappy/jittery on strafes |

The 2.0 figure is the documented tutorial default
([The Indie Dev Professor — How to create a Lock-On/Targeting System on UE5](https://theindieprofessor.wordpress.com/2025/09/28/how-to-create-a-lock-on-targeting-system-on-ue5/)),
and is the right starting point for a slow exploration game. **The binding requirement
here is that the camera must be settled before the telegraph resolves**, which is what
picks 6.0.

### The aim point, and why it is a fairness issue rather than a framing preference

The rival is **208 cm**; the players are **183 cm** and **173 cm**. If lock-on aims the
control rotation at the rival's **actor origin**, the camera pitches up at a 208 cm
target and the player's own body sits low in frame — and it sits *differently low* for
Echo and Nova, because their capsule half-heights differ by 5 cm.

**Proposed: aim at a named socket on the rival's chest at ~140 cm above the floor, with
a fixed −8° pitch offset**, so the two-shot frames both fighters and frames them the
same way regardless of which avatar was picked. That is the concrete camera-side
satisfaction of GDD §07's "must not create unfair hidden reach or collision behavior" —
a player who cannot see the telegraph clearly has a hidden-reach problem even if the
hitboxes are honest.

**Both fighters must use the same aim point and the same offsets.** Nothing in the
lock-on component reads `DA_FighterProfile`. Single-sourced.

### Interaction with the rest

- **Q24** — 3000 cm beats the 2884 cm diagonal. If the designer takes the 1800 × 1200
  alternative arena (2163 cm diagonal), these values still work unchanged; they are
  deliberately over-provisioned.
- **Q15 (Echo/Nova walk speed, not mine)** — if lock-on applies a strafe-speed multiplier,
  that multiplier is a *shared framework* value and must not differ per fighter unless
  Q15 resolves to differing speeds.
- **Spring arm.** `TargetArmLength` 400 (UE Third Person template default) against an
  800 cm centre-to-side-wall distance leaves the camera clear during lateral exchanges.
  The one place the probe will collapse is a player backed flat into a wall — the
  mezzanine collision note in Item 18 addresses the worst of it. **Disable camera lag
  while locked on**; lag plus interp is two smoothers fighting each other.
- **`BP_FinalClashDirector`** must take and return camera control cleanly. Group 03's
  `RestoreCombatState()` should re-assert lock-on if it was active before the Clash,
  rather than leaving the player unlocked at 1 HP.

---

## Item 18 — Is the arena mezzanine reachable, or set dressing?

- **Kind:** B · **Status:** **PROPOSED** · raised by the arena sheet recovered 2026-08-02
- **Unblocks build step:** **M1-21** — gray-box `L_ShatteredRing` (collision and NavMesh
  setup).
- **Value lives in:** `L_ShatteredRing` collision and navigation setup; no Data Table row.
- **GDD range:** **the GDD says nothing about the mezzanine at all.** §08 lists five arena
  requirements and **every one of them is a floor-level requirement** — central combat
  floor, far doorway, reverse third-person framing, side-on readability, environmental
  reaction. Verticality is never mentioned.

### Proposed answer

> **Set dressing. Not reachable. No route in, no route out, no NavMesh, no blocking
> volume.**

### Why

1. **The art shows no route.** `gdd/reference/page-11-...` records a full upper tier with
   "**no visible route into the play space**", and marks reachability **AMBIGUOUS**. This
   is a **KIND B read of reference art, and the rule for that is: do not invent what the
   art does not show.** Proposing a stair or ramp would be authoring new arena geometry
   from nothing. Proposing *decoration* adds nothing that is not already drawn.
2. **The recovered sheet states the play surface is "one flat concrete floor, no
   elevation change."** A reachable tier contradicts the only geometry statement the
   source material makes.
3. **GDD §08 forbids adding gameplay hazards.** A reachable upper tier is a fall, a ledge,
   and an edge case in every one of Impact Window, counter, dodge, and Final Clash
   staging. Even if a fall dealt no damage, "rival on the floor, player on the balcony"
   is a state the six-state rival AI has no authored answer for.
4. **SCOPE LOCK.** One arena, one shared combat framework. A second traversal layer needs
   ledge handling, a second nav layer, rival pathing up a ramp, camera occlusion work, and
   a rule for what the rival does when it cannot reach you — all of it new systems, none
   of it in the scope list, none of it buildable and tunable by 1 September.
5. **It costs nothing to keep.** As decoration the mezzanine still does real work: it
   gives the hall its scale, it holds the X-braced truss landmark that distinguishes the
   two ends, and it carries the orange paint-drip accent. The GDD's "environmental
   reaction ... without adding gameplay hazards" is *easier* to author on a tier nobody
   can stand on.

### Build consequences — the concrete part

| Thing | Setting | Reason |
|---|---|---|
| Arena collision boundary | **The wall shells at the railing line.** No extra `BlockingVolume` | One boundary, not two. The railing the player sees is the wall they hit |
| Orange railing meshes | `Collision Presets = NoCollision` | Two colliders at nearly the same place is the classic "player snags on the rail" bug |
| Mezzanine deck, struts, truss panel | `Can Ever Affect Navigation = false` | Stops nav generation spilling onto a surface nobody uses |
| Mezzanine underside | **Ignore the `Camera` trace channel** | The third-person spring-arm probe must not collide with the overhang when the player backs into a wall. This is the single most likely camera bug in the room |
| Mezzanine underside height | **≥ 450 cm** above the floor (provisional) | Above the spring arm's working envelope |
| `NavMeshBoundsVolume` | Sized to **2400 × 1600 × ~400 cm**, floor level only | Nav cannot generate anywhere the design did not intend. Cheap insurance |
| Ceiling / roof | A camera-blocking plane only if the spring arm ever escapes upward | Skylights are lighting, not geometry the player interacts with |

**Nothing here is presentation work.** It is collision and navigation setup, which is
M1 gray-box, and it does not touch M5.

### Raised, not answered — the far doorway

Page 11 also marks **AMBIGUOUS** whether the far doorway "is a functional volume or a lit
backdrop." **That is not my item and I am not deciding it.** But it interacts with mine:
`LS_VanguardEntrance` (M4) walks the rival in through that doorway, so at minimum the
doorway must be *passable during the entrance sequence* and must not be a hole the player
can walk out of afterwards. **Recommended new TODO item for whoever owns the entrance
sequence.** My footprint assumes the doorway is **sealed at the wall line once the duel
begins**, so the 2400 cm long axis is the true playable extent.

---

## Band coverage proof

**The claim being proved:** at every distance the two fighters can actually be at, either
at least one attack is selectable, **or** the rival repositions **on purpose** — and the
"on purpose" case is one identifiable region, not scattered gaps.

Bands: **A [0, 260] · B [90, 520] · C [240, 420] · D [400, 840]**.
Range of possible `DistanceToTarget`: **100 cm** (capsule contact, 40 + 60) to
**2884 cm** (corner-to-corner diagonal).

| Distance (cm) | A | B | C | D | **Depth** | What happens |
|---|:-:|:-:|:-:|:-:|:-:|---|
| 0 – 90 | ✓ | | | | 1 | **Physically unreachable** (min 100 cm). Covered anyway, so a future capsule change cannot open a hole |
| 90 – 100 | ✓ | ✓ | | | 2 | Also unreachable. Covered |
| **100 – 240** | ✓ | ✓ | | | **2** | Contact / point-blank. A and B alternate |
| **240 – 260** | ✓ | ✓ | ✓ | | **3** | The richest band. Player's own combo range |
| **260 – 400** | | ✓ | ✓ | | **2** | Mid. B and C alternate |
| **400 – 420** | | ✓ | ✓ | ✓ | **3** | Transition into gap-closer range |
| **420 – 520** | | ✓ | | ✓ | **2** | B and D alternate |
| **520 – 840** | | | | ✓ | **1** | **Only D.** See below |
| **840 – 2884** | | | | | **0** | **The one deliberate gap.** Rival advances |

### The gaps, named

**Gap 1 — the depth-0 region, 840 to 2884 cm (35% to 100% of the long axis).**
No attack is selectable. This is intentional and it is the *only* zero-coverage region.
The rival's answer is `BTTask_Idle_Reposition` moving toward `DesiredRange`. Because
there is exactly one region and it is the far half of the room, a player who sees the
rival walking rather than attacking is reading a true signal — "you are out of range" —
rather than watching a bug.

**Gap 2 — the depth-1 region, 520 to 840 cm.**
Only D. If D is on cooldown here, the eligible set is empty and the rival advances toward
B's band. Two reasons this does not become the reposition loop §14 warns about:

- The advance rule sends the rival to `DesiredRange` — the midpoint of the nearest
  off-cooldown band — so it **leaves** the depth-1 region rather than shuffling inside it.
- **After D executes, the rival is at 240 cm**, which is depth 3. D's cooldown therefore
  almost never expires while the rival is still in D's own band. The depth-1 zone is
  transient by construction.

### Contiguity, stated formally

`A ∪ B ∪ C ∪ D = [0, 840]` with **no interior gap**:

- A ends at 260, B starts at 90 → overlap **80 cm**  (A→B handoff)
- B ends at 520, C spans 240–420 entirely inside B → C adds depth, never bridges
- B ends at 520, D starts at 400 → overlap **120 cm** (B→D handoff)

**Every handoff overlaps.** The two handoff overlaps, 80 cm and 120 cm, are the numbers
to watch in playtest: at 500 cm/s the player crosses 80 cm in 0.16 s, which is within the
0.10–0.20 s Select Attack window. **That does not create a hole** — range is evaluated
once at selection and the attack commits (Q10, interaction note 1) — but it does mean the
handoffs are where whiffs cluster. If whiffs feel excessive, **widen the overlaps before
touching any timing value.**

---

## Cooldown starvation check

**The claim being proved:** in every zone with **two or more** attacks in band, the rival
always has at least one eligible attack, in **both** phases, even at the fastest cycle the
GDD permits.

**Method.** Worst case is strict round-robin at the **fastest legal cycle** — the rival
fires as often as possible, so cooldowns have the least real time to expire. In a zone of
depth **N**, each attack is re-offered every `N × cycle` seconds. Starvation-free requires
`Cooldown ≤ N × cycle`.

### Phase 1 — fastest legal cycle **1.98 s**

| Zone (cm) | Depth | Attacks and cooldowns | Re-offer period | Longest CD | Slack | Result |
|---|:-:|---|---|---|---|---|
| 100 – 240 | 2 | A 3.0, B 3.5 | 2 × 1.98 = **3.96 s** | 3.5 | **+0.46 s** | **PASS** |
| 240 – 260 | 3 | A 3.0, B 3.5, C 3.6 | 3 × 1.98 = **5.94 s** | 3.6 | +2.34 s | **PASS** |
| 260 – 400 | 2 | B 3.5, C 3.6 | **3.96 s** | 3.6 | +0.36 s | **PASS** |
| 400 – 420 | 3 | B 3.5, C 3.6, D 3.8 | **5.94 s** | 3.8 | +2.14 s | **PASS** |
| 420 – 520 | 2 | B 3.5, D 3.8 | **3.96 s** | 3.8 | **+0.16 s** | **PASS — tightest in the file** |
| 520 – 840 | 1 | D 3.8 | 1.98 s | 3.8 | −1.82 s | **Starves by design** → advance rule |

At the Phase 1 **midpoint** cycle of 2.94 s every depth-2 period becomes 5.88 s and the
slack is 2.1–2.4 s everywhere. The table above is the pessimistic case.

### Phase 2 — fastest legal cycle **1.48 s**

| Zone (cm) | Depth | Attacks and cooldowns | Re-offer period | Longest CD | Slack | Result |
|---|:-:|---|---|---|---|---|
| 100 – 240 | 2 | A 2.5, B 2.6 | 2 × 1.48 = **2.96 s** | 2.6 | +0.36 s | **PASS** |
| 240 – 260 | 3 | A 2.5, B 2.6, C 2.7 | **4.44 s** | 2.7 | +1.74 s | **PASS** |
| 260 – 400 | 2 | B 2.6, C 2.7 | **2.96 s** | 2.7 | +0.26 s | **PASS** |
| 400 – 420 | 3 | B 2.6, C 2.7, D 2.8 | **4.44 s** | 2.8 | +1.64 s | **PASS** |
| 420 – 520 | 2 | B 2.6, D 2.8 | **2.96 s** | 2.8 | **+0.16 s** | **PASS** |
| 520 – 840 | 1 | D 2.8 | 1.48 s | 2.8 | −1.32 s | **Starves by design** → advance rule |

### The Phase 2 trap the dispatch asked about, quantified

**Keeping Phase 1 cooldowns in Phase 2 breaks the rival.** Phase 2's fastest cycle is
1.48 s, so a depth-2 zone re-offers every **2.96 s** — but three of the four Phase 1
cooldowns exceed that:

| Attack | P1 cooldown | P2 depth-2 re-offer period | Starves? | Dead time per cycle |
|---|---|---|---|---|
| A | 3.0 s | 2.96 s | **yes, marginally** | ~0.04 s |
| B | 3.5 s | 2.96 s | **yes** | ~0.54 s |
| C | 3.6 s | 2.96 s | **yes** | ~0.64 s |
| D | 3.8 s | 2.96 s | **yes** | ~0.84 s |

In the 420–520 cm B/D zone that is roughly **0.84 s of the rival standing with no legal
attack, every other cycle** — precisely at the moment the GDD says Phase 2 should feel
like *more* pressure, not less. **This is why `Cooldown` belongs inside
`S_AttackPhaseTuning`.** Put it on the attack instead of on the attack-per-phase and the
build has a silent Phase 2 regression that will read as "Phase 2 feels slower" and be
blamed on the telegraph values.

### No-repeat check

An attack can fire twice in a row only if its cooldown is shorter than one cycle. Against
the **midpoint** cycle:

| | Midpoint cycle | Shortest cooldown | Repeat possible? |
|---|---|---|---|
| Phase 1 | 2.94 s | A at 3.0 s | **No** — margin 0.06 s |
| Phase 2 | 2.315 s | A at 2.5 s | **No** — margin 0.185 s |

**Phase 1's margin is 0.06 s and that is thin.** If Q25 authors any attack's states near
the *slow* end, the cycle lengthens and the margin grows — safe direction. If Q25 authors
near the *fast* end, the cycle shortens and the margin grows too. The 0.06 s figure is the
worst point on the curve, not a cliff. **But if the designer raises A's cooldown for
safety, it must stay ≤ 3.96 s or the depth-2 starvation wall is crossed.** The legal
window for A in Phase 1 is **(2.94, 3.96] seconds** and that is the whole room there is.

### What this does not prove

- It assumes the rival fires an attack every cycle. In real play the player interrupts
  with counters, which sends the tree to Return to Neutral early and **shortens** the
  cycle — pushing toward the fastest-cycle column, which is the column tested. Good.
- It assumes `DistanceToTarget` stays inside one zone across consecutive cycles. In real
  play the distance moves constantly, which only ever **adds** eligible attacks relative
  to the single-zone model. The proof is conservative.
- It says nothing about whether the resulting attack *sequence* feels good. That is
  `SelectionWeight`, which has no Q number (Q10, interaction note 5).

---

## What this footprint supports for Q21

**Q21 — the failed-Clash separation distance — belongs to the Final Clash group. I am not
setting it.** What follows is what a 2400 × 1600 cm arena and the Q10 bands *permit*, so
that group can choose inside real walls.

### The floor Q10 imposes

> **Separation must exceed 840 cm** — Attack D's `MaxRange`.

Below that, the rival can select D and dash the player down the instant the failed Clash
resolves, which defeats the entire purpose of separating them. §14's own wording asks for
the fighters to be placed "outside every attack's `MinRange`"; against this band layout
the operative number is the **largest `MaxRange`**, not any `MinRange`, because D reaches
furthest.

### The ceiling Q24 imposes

| If the separation is applied... | Room available | Largest value achievable **from anywhere** in the arena |
|---|---|---|
| Along an arbitrary axis (fighters' facing), clamped to walls | as little as the short axis, 1600 cm | **1300 cm** (1600 − 2 × 150 cm wall clearance) |
| Along the **arena long axis (X)**, clamped | 2400 cm everywhere | **2100 cm** (2400 − 2 × 150 cm) |

**Recommendation to the Q21 group: apply the push along the arena's long axis, not along
the fighters' facing.** A facing-relative push next to a long wall clamps to as little as
~700 cm and silently produces a *different* separation every time the Clash fails — which
would make the recovery beat feel inconsistent for reasons no playtester could name. A
long-axis push has 2400 cm available from every point in the room.

### What each candidate value buys, in time

Time before the rival can select D again = `(Separation − 840) / RivalAdvanceSpeed`.

| Separation | At 400 cm/s | At 500 cm/s | At 600 cm/s |
|---|---|---|---|
| 900 cm | 0.15 s | 0.12 s | 0.10 s |
| 1000 cm | 0.40 s | 0.32 s | 0.27 s |
| **1200 cm** | **0.90 s** | **0.72 s** | **0.60 s** |
| 1300 cm | 1.15 s | 0.92 s | 0.77 s |
| 1600 cm | 1.90 s | 1.52 s | 1.27 s |

**This table cannot be finished, and the reason is the gap Q24 exposed:** the rival's
advance speed has no row in §13.2 and no Q number. The three columns are placeholders
around Unreal's default player `MaxWalkSpeed` of 500 cm/s.

### The recommendation, stated as support rather than as an answer

> **A 2400 × 1600 cm arena comfortably supports a failed-Clash separation of
> 1000–1300 cm, with 1300 cm the largest value guaranteed achievable from every point in
> the room. 1200 cm is the value the geometry is most comfortable with** — it is 50% of
> the long axis, 43% above D's 840 cm reach, and it leaves ~0.7–0.9 s before the player
> can be dashed again.

### One thing the Final Clash group should know before it picks

**The 3 second failed-Clash cooldown is a Clash *re-trigger* cooldown, not a combat
pause.** GDD §03's failure resolution separates the fighters, floors the rival at 1 HP,
sets the meter to 50, and returns to neutral — the rival's Behavior Tree resumes
immediately. So **the separation distance is the only breathing room the player gets, and
at any value the geometry allows it buys under one second.**

If the designer wants a failed Clash to feel like a genuine reset rather than a stumble,
separation alone cannot deliver it — the lever would be a brief authored rival recovery
beat on the failure path. **That is the Final Clash group's call, not mine, and I am
raising it rather than proposing it.**

### And the easy one

Q13's 600 cm travel fits the footprint trivially: **25% of the long axis, with the rival
finishing 240 cm from the player and 1200+ cm from either end wall in the typical case.**
There is no interaction between D's dash and the arena boundary that needs handling
beyond the standard capsule collision — D's Motion Warping target is derived from the
*player's* location, and the player is always inside the arena.

---

## Research note

**10 WebSearch sources used, under the cap.** Searching stopped early because the two
remaining gaps proved to be genuine absences rather than things I had not found yet:

1. **No shipped third-person action game publishes its boss-arena dimensions in metres.**
   Searched for Sekiro and Elden Ring specifically; no reliable datamined figure exists in
   reachable sources. **Tekken's published stage sizes are used instead**, and they are
   arguably better prior art anyway — walled, flat, hazard-free, one-versus-one.
2. **No shipped game publishes per-attack AI cooldowns or enemy attack-range tables in
   centimetres.** Q12 in particular is derived entirely from the GDD's own state ranges,
   and it is named as the weakest-sourced number in this file.

Everything cited above is either an Unreal documentation/convention figure or a published
game figure with its source named. Nothing is presented as measured when it was estimated.

---

## Summary — all six, PROPOSED

| Item | Proposed | Lives in | Unblocks |
|---|---|---|---|
| **Q24** | Playable floor **2400 × 1600 cm** (24 × 16 m), long axis = doorway axis, 250 cm 45° corner chamfers | `L_ShatteredRing` + `DA_TuningGlobals.ArenaLongAxisCm` / `ArenaShortAxisCm` | M1-21 |
| **Q10** | **A 0–260 · B 90–520 · C 240–420 · D 400–840 cm**, identical both phases | `DT_VanguardAttacks` `MinRange` / `MaxRange` | M2-04 |
| **Q12** | P1 **A 3.0 · B 3.5 · C 3.6 · D 3.8 s**; P2 **A 2.5 · B 2.6 · C 2.7 · D 2.8 s** | **`S_AttackPhaseTuning.Cooldown`** (relocated from `S_VanguardAttackDef`) | M2-04 |
| **Q13** | **600 cm = 0.25 × long axis**, finishing 240 cm from the target | `DA_TuningGlobals.AttackD_TravelFractionOfLongAxis` → `DT_VanguardAttacks.MaxTravelDistance` | M2-04 |
| **Q11** | Acquire **3000 cm** · break **3300 cm** · interp **6.0** · aim socket **140 cm**, pitch **−8°** | `BP_LockOnComponent` | M1-16 |
| **Item 18** | Mezzanine is **set dressing** — no NavMesh, no blocking volume, underside ignores the `Camera` channel | `L_ShatteredRing` collision / nav setup | M1-21 |

**Everything in this file is the human designer's to approve, change, or reject.**

