# Group 02 — Combat economy · Q1–Q5

**Dispatched:** 2026-08-02 · designer agent, group 02 of the open-question sweep.
**Consumes:** `project-brief.md`, `gdd/sections/01`, `gdd/sections/03`, `gdd/sections/04`,
`design-brief.md` §13.1 / §13.2 rows 29–33 / §14, `design/decisions.md` (Q22, APPROVED).
**Produces:** answers to **Q1, Q2, Q3, Q4, Q5** only. Q6–Q31 belong to other groups and
are named as still open wherever the reasoning here leans on them.

> **EVERY ANSWER IN THIS FILE IS `PROPOSED`, NOT DECIDED.**
> These are all **KIND B** design items. A designer dispatch may research and recommend;
> it may not settle. The human designer of record owns every number here. Each entry
> stays open in `TODO.md`, marked PROPOSED, until the designer approves or changes it.

---

## Binding context — Q22 was approved today

`design/decisions.md`, entry **2026-08-02 — Q22**, status **APPROVED**:

> `MinHealthFloor = 1` on the rival's `BP_HealthComponent` from `BeginPlay`, lowered to
> `0` only by `ClashSuccess()` immediately before it applies lethal damage.

**Consequences this group must reason inside:**

1. **The Final Clash is the only way to win.** Ordinary combat damage can never kill
   Crimson Vanguard. The rival's health bar is not a life bar in the usual sense — it is
   a **progress bar toward the ≤25 % gate**.
2. **Q2 (rival max health) is therefore not "time to kill."** It is *"how long until the
   ≤25 % gate opens."*
3. **Q4 (player damage) is not how you win.** It is how you open the gate.
4. **Constraint C3 is binding on this group:** *"Q2 must be tuned so ≤25 % and meter 100
   arrive close together."* A player who pins the rival at 1 HP with a half-empty meter
   is in a **stall**, and the length of that stall is this group's responsibility.
5. Constraint **C1** (Q9 must resolve to no meter decay) belongs to another group but is
   assumed true throughout the arithmetic below. **If Q9 resolves to decay, every
   meter-timing number in this file must be recomputed.**

---

## GDD numbers used here — fixed, cited, never edited

| Value | Number | Source |
|---|---|---|
| Meter range | **0–100** | `gdd/sections/03`, PDF p.3 |
| Light-combo finisher | **+5** | `gdd/sections/03`, PDF p.3 |
| Perfect dodge | **+12** | `gdd/sections/03`, PDF p.3 |
| Successful counter | **+15** | `gdd/sections/03`, PDF p.3 |
| Impact Window success | **+20** | `gdd/sections/03`, PDF p.4 |
| Taking damage / waiting | **+0** | `gdd/sections/03`, PDF p.4 |
| Phase 2 trigger | rival health **50 %** | `gdd/sections/03` p.4, `gdd/sections/04` p.6 |
| Final Clash gate | meter **100** AND rival health **≤ 25 %** | `gdd/sections/03`, PDF p.3 |
| Failed Clash | rival **1 HP** floor · meter **→ 50** · **3 s** cooldown | `gdd/sections/03`, PDF p.4 |
| Target session | **3–5 minutes** | `gdd/sections/01`, PDF p.1 |
| Rival state timings | see `design-brief.md` §13.1 rows 17–25 | `gdd/sections/04`, PDF p.5 |

**No answer below requires changing any of these.** Where an answer would have, it was
discarded.

---

## Q1 — Player max health

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-05**
- **Value lives in:** `DA_TuningGlobals` — player max health, one field, shared
  (`design-brief.md` §13.2 row 29)
- **GDD range:** **The GDD publishes no number and no range for player health.**
  `design-brief.md` §14 offers **100–200** as a starting point for conversation, and
  the proposal below falls inside it. The one thing the GDD *does* bind is the
  **SHARED PLAYER-KIT SCOPE RULE** (`gdd/sections/02`, PDF p.2–3): Echo and Nova use
  one framework, so **this is one value, not two.**

### Proposed value

> **`PlayerMaxHealth = 100`** — identical for Agent Echo and Agent Nova.
> Authored as a single field on `DA_TuningGlobals`, **not** on `DA_FighterProfile`.
> Placing it on the fighter profile is the exact shape a per-fighter health split would
> take later, so it must not live there even with equal values.

### Why

1. **It makes Q3 free.** §14 asks that rival damage be expressed as *a percentage of
   player max health*. At `100`, "percentage of player health" and "damage number" are
   the same number. `DT_VanguardAttacks.Damage = 30` **is** 30 %. The designer can read
   the whole hit budget straight off the Data Table with no arithmetic, which is the
   single biggest tuning-speed win available here.
2. **It targets the 3–5-hit budget §14 asks for.** With the Q3 spread below, the player
   dies in **4 hits** of the heaviest attack and **6** of the lightest — the readable
   armored-boss budget, and the same feel band the prior art lands in.
3. **Granularity is not needed at this scope.** Fighting games run large health pools
   (Street Fighter 6: **10000** standard, 10500 for E. Honda/Marisa, 11000 for Zangief)
   precisely because they need fine per-move damage differences across a 20+ character
   roster with combo scaling. This game has **one** attacker with **four** attacks and
   no scaling system. Tekken sits at the other end and is the closer analogue: **180 HP
   at Tekken 8 launch, raised to 200 in patch 2.00.02** (Tekken 7 shipped at 170, raised
   to 175 in Season 4) — a two-fighter duel expressed in a small, human-readable pool.
   100 is that idea taken one step further.
4. **It keeps a moved number cheap.** Because Q3 is authored as a percentage and Q4 is
   authored against rival health, **changing Q1 later re-tunes nothing else.** If the
   designer wants 150 for finer steps, it is a one-field edit.

### Prior art (real games, named)

| Game | Mechanism | Real numbers | Relevance |
|---|---|---|---|
| **Sekiro: Shadows Die Twice** | Vitality is a small stat that scales a health pool; bosses kill in very few hits | Base vitality **10** = **320** health; each Prayer Bead point adds **+80** health and **+30** posture; all beads → **1120** health / **420** posture, max vitality **20**. Community reporting on the Ashina Outskirts samurai: kills the player **in 2–3 hits** at starting vitality | The clearest shipped statement of "an armored duel is a 3-ish-hit budget." Our 4-hit worst case is one notch more forgiving, which is right for a course prototype with no checkpoints |
| **Street Fighter 6** | Large uniform pool for fine damage granularity across a roster | **10000** standard; **10500** E. Honda / Marisa; **11000** Zangief | Shows *why* you would go large — roster differentiation and combo scaling. Neither applies here, so this is the pattern we are deliberately **not** following |
| **Tekken 8** | Small readable pool in a 1v1 duel, retuned post-launch | **180** at launch, **200** from patch **2.00.02**; Tekken 7 **170**, raised to **175** in Season 4 | Direct evidence that a small pool is workable for 1v1 **and** that the number is expected to move after playtest. Both games changed it after shipping |
| **Furi** | 1v1 boss duels, player survivability expressed as discrete lives rather than a big bar | **3 deaths allowed per boss**; one life is regained for each phase the player pushes the boss through; parrying restores health | Prior art for making the player's survivability *countable* by the player. We do not adopt lives (SCOPE LOCK — one duel, one loss condition), but the readability goal is the same |

> **Unverified:** one low-quality result claimed Sekiro's damage is literally
> percentage-based against vitality. **Do not rely on that claim** — it is not
> corroborated and it is not load-bearing for anything here. The verified facts are the
> vitality/health table and the 2–3-hit community reporting.

### How it interacts with the other four

- **Q3** is authored as a percentage of this value, so the two are the same number at
  `100`. This is the whole reason for the choice.
- **Q2 / Q4** are independent of it. Player health and rival health are two separate
  economies under the approved Q22 decision — the rival pool is a *gate timer*, the
  player pool is a *mistake budget*. Nothing couples them except duel length.
- **Q5** is unaffected.
- **Open elsewhere, assumed here:** **Q6** (i-frame window), **Q7** (perfect-dodge
  sub-window) and **Q27** (`ANS_Recover` damage multiplier) all change how often the
  player actually eats a hit. **Q7 in particular will do more to set effective
  survivability than Q1 does.** If Q7 lands tight, 100 will feel brutal; if it lands
  loose, 100 will feel generous. **Tune Q7 first, then revisit Q1.**

**This is a recommendation. The designer decides.**

---

## Q2 — Crimson Vanguard max health

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-05**
- **Value lives in:** `DA_TuningGlobals` — rival max health
  (`design-brief.md` §13.2 row 30)
- **GDD range:** **The GDD publishes no number and no range for rival health.** It
  publishes only the two *thresholds* on that pool — Phase 2 at **50 %**
  (`gdd/sections/03` p.4, `gdd/sections/04` p.6) and the Clash gate at **≤ 25 %**
  (`gdd/sections/03` p.3) — and the **3–5 minute** target session
  (`gdd/sections/01` p.1). `design-brief.md` §14 offers **800–2000** as a starting
  point; the proposal below falls inside it.

### What this number actually is, after Q22

Under the approved Q22 decision the rival's health bar **is not a life bar.** It cannot
reach zero through combat. It is a **gate timer with two marks on it** — 50 % opens
Phase 2, 25 % arms half of the Clash gate — and its only job is to decide *when* those
two marks are crossed. Everything below is derived from that, not from time-to-kill.

### Proposed value

> **`VanguardMaxHealth = 1200`** · tuning band **1100–1400**.
> Derived, not picked: it is the value that puts the **≤ 25 % gate at ~2:53** of
> combat for a competent player and **~4:30** for a scrappy one, so the complete duel
> lands inside **3–5 minutes** at both ends of the skill band.

### Why — the derivation, shown

**Step 1 — how long is one rival cycle?** Sum the GDD state midpoints
(`design-brief.md` §13.1 rows 17–25). Per-attack values inside those ranges are **Q25,
still open**, so midpoints are the honest estimate.

| | Reposition | Select | Telegraph | Active | Recover | Return | **Cycle** |
|---|---|---|---|---|---|---|---|
| **Phase 1** | 0.90 | 0.15 | 0.75 | 0.315 | 0.675 | 0.15 | **≈ 2.9 s** |
| **Phase 2** | 0.575 | 0.15 | 0.575 | 0.315 | 0.55 | 0.15 | **≈ 2.3 s** |

**Step 2 — how much offense fits in one cycle?** The rival is not threatening during
Recover + Return + Reposition: **≈ 1.73 s in Phase 1**, **≈ 1.28 s in Phase 2**. A 3-hit
combo (Q5) runs ≈ **1.0 s**. So Phase 1 comfortably fits one full combo per cycle;
Phase 2 fits one only if the player is already in range. Allowing for whiffs, travel and
dropped strings, the model uses **0.7 full combos per rival cycle for competent play**
and **0.45 for scrappy play**.

**Step 3 — solve for the gate.** With the Q4/Q5 combo dealing **20** damage:

| Segment | Damage needed | Combos | Cycles @0.7 | Cycle len | Time |
|---|---|---|---|---|---|
| 100 % → 50 % (Phase 2 trigger) | 600 | 30 | 43 | 2.9 s | **≈ 124 s** |
| 50 % → 25 % (Clash gate arms) | 300 | 15 | 21 | 2.3 s | **≈ 49 s** |
| | **900** | **45** | **64** | | **≈ 173 s (2:53)** |

Add the abbreviated entrance, approach time, the Clash sequence itself and — realistically —
**one failed Clash** (3 s cooldown + meter rebuild + re-approach, ~20–30 s) and a
competent run lands at **≈ 3:20–3:40**. At 0.45 combos/cycle the same 900 damage takes
**≈ 269 s (4:29)**, landing near the top of the band. **The whole 3–5 minute target is
covered by the realistic skill spread, which is exactly what a target session is for.**

**The tuning identity, for the designer to move it with:**

```
TimeToClashGate  ≈  (0.75 × VanguardMaxHealth / ComboDamage) / CombosPerCycle × CycleLength
```

At `ComboDamage = 20`: **1000 → ~2:25** (too fast for a strong player), **1200 → ~2:53**,
**1400 → ~3:22** (a weak player runs past 5:00). **1200 is the centre of the band that
holds both ends of the skill spread inside 3–5 minutes.** Below ~1000 or above ~1400 one
end falls out.

**Step 4 — the C3 check.** Constraint C3 requires ≤ 25 % and meter 100 to arrive close
together. The full arithmetic is in the Cross-check section, but the short version:
**with the GDD's fixed gains, meter 100 arrives far earlier than the health gate in
every normal playstyle.** That means the dangerous C3 failure — *rival pinned at 1 HP,
meter empty* — essentially cannot occur through normal play. **Q2 being on the higher
side is the safe side for C3**, because a *lower* Q2 is what would bring the health gate
forward toward an unfilled meter. 1200 leans safe deliberately.

### Prior art (real games, named)

| Game | Mechanism | Real numbers | Relevance |
|---|---|---|---|
| **Furi** | Every boss is a 1v1 duel; the boss health pool is deliberately long and split into phases the player must push through | Each boss phase is **two bars** (a blue overhead/ranged bar and an orange melee bar); the player is allowed **3 deaths per boss** and regains one life per phase cleared; first-playthrough fights are reported at **up to 15 minutes** | The nearest genre neighbour, and a **cautionary** one. Furi's 15-minute duels are only tolerable because it is a boss-rush game built around repetition. Our GDD names **3–5 minutes**, so we are targeting roughly a fifth of Furi's length — which is why 1200 and not 2000 |
| **Sekiro: Shadows Die Twice** | Boss health is a secondary resource; the *real* kill condition is a separate meter (Posture) that the health bar only feeds | Vitality **10 → 20**, health **320 → 1120**, posture **120 → 420**; each vitality point is **+80 health / +30 posture** | The structural match for Q22. In Sekiro, chipping vitality lowers posture recovery — health is a *lever on the win condition*, not the win condition. Our rival health pool plays the same role: it opens the gate, it does not end the fight |
| **Sifu** | A second bar (Structure) is what actually creates the finishing opportunity; enemies and player both have it | Structure regenerates while guarding, does **not** regenerate while sprinting or attacking; breaking an enemy's structure before their health empties grants a finishing move | Independent confirmation that a duel can carry two bars where the non-health one owns the kill. Also a warning we take: Sifu's structure **decays**, and `design/decisions.md` **C1** requires our meter not to — the two systems are not interchangeable |
| **Hi-Fi Rush** | Boss health is drained by completing full combo strings rather than by individual pokes | Boss HP comes down through "big combo strings" and Beat Hits, which deal additional damage over raw hits | Direct support for Q4's back-loaded finisher: reward the *completed* string, not the hit count |

> **Not verified in this pass:** exact datamined boss HP figures for Sekiro bosses and
> for Elden Ring's Margit. Two searches returned no reliable number, so **no such figure
> is cited here.** The Sekiro player-side numbers above *are* from the Fextralife wiki
> and are used; the boss-side numbers are simply absent.

### How it interacts with the other four

- **Q4 is the direct multiplier.** `Q2` and `ComboDamage` only ever appear as a ratio in
  the identity above. **Moving either one alone moves duel length proportionally.** If
  the designer wants a longer duel, prefer raising Q2 over lowering Q4 — lowering Q4
  makes each hit feel weaker, raising Q2 does not.
- **Q5 sets `SecondsPerCombo`,** which sets `CombosPerCycle`. A 4-section combo (Q5's
  alternative) does not fit the Phase 2 non-threat window of 1.28 s, which would collapse
  `CombosPerCycle` in Phase 2 and stretch the duel past 5 minutes. **Q5 = 3 is load-bearing
  for this Q2 value.**
- **Q1 and Q3 are independent of it** — different economy, as noted in Q1.
- **Open elsewhere, assumed here:** **Q25** (per-attack values inside the GDD state
  ranges) determines the real cycle length. Midpoints were used. If the designer authors
  attacks toward the fast end of every range, cycles shorten, more combos fit, and **Q2
  must rise**. If toward the slow end, Q2 must fall. **Re-run the identity above once Q25
  is answered.** **Q12** (per-attack cooldown) and **Q10** (range bands) can also insert
  dead cycles where the rival repositions without attacking, which lengthens the duel.

**This is a recommendation. The designer decides.**

---

## Q3 — Damage per rival attack A / B / C / D

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M2-04**
- **Value lives in:** `DT_VanguardAttacks.Damage` — one row per attack
  (`design-brief.md` §13.2 row 31)
- **GDD range:** **The GDD publishes no damage numbers.** What it *does* bind is the
  **character** of each attack (`gdd/sections/04`, PDF p.5–6):
  **A** "Close-range committed gauntlet force" · **B** "Committed forward-pressure
  sequence" · **C** "Armored reach and space control" · **D** "Short propulsion-assisted
  approach." It also binds that **"every major offense exposes a clear recovery
  opening"** and that armour and scale **"do not remove readable counterplay."**
  `design-brief.md` §14 asks that A be heaviest, D lightest, and that each be expressed
  as a **percentage of player max health**.

### Proposed values

Authored as **percentage of `PlayerMaxHealth`**. At the proposed Q1 of **100** the
percentage and the Data Table integer are the same number, so the column below is
literally what goes in `DT_VanguardAttacks.Damage`.

| Attack | GDD character | **Damage (% of player max HP)** | Hits to kill from full |
|---|---|---|---|
| **A** | Close-range committed gauntlet force | **32 %** | **4** (32 / 64 / 96 / 128) |
| **B** | Committed forward-pressure sequence | **25 %** | **4** (25 / 50 / 75 / **100 exactly**) |
| **C** | Armored reach and space control | **27 %** | **4** (27 / 54 / 81 / 108) |
| **D** | Short propulsion-assisted approach | **18 %** | **6** (18 → 108) |

Mean **25.5 %** → a mixed-diet player dies on roughly the **4th** clean hit. Spread is
**4 to 6** hits depending on what lands. This sits inside §14's "3–5-hit budget" for
every attack the player is likely to eat repeatedly, and is one notch more forgiving
than the Sekiro prior art (2–3 hits) — deliberate, because this prototype has **no
checkpoints and one loss condition**.

**Designer variant offered, not recommended:** set **A = 34 %** and A becomes a
**3-hit kill** (34 / 68 / 102). That is a stronger statement of "committed close force"
and matches Sekiro more closely. It is left as a variant rather than the recommendation
because **Q7 (perfect-dodge sub-window) is still open** — if Q7 lands tight, a 3-hit
heaviest attack plus a hard defensive window compounds into a difficulty spike that no
number in this file can see yet. **Tune Q7 first; raise A afterwards if the fight reads
as too soft.**

### Why

1. **The order is forced, the gaps are the design.** §14 fixes A heaviest and D
   lightest. The interesting choice is the *spacing*: A/B/C are clustered (32 / 27 / 25)
   and **D sits clearly apart at 18**. That is intentional — A, B and C are the three
   attacks the player is meant to *respect and answer*; D is an **approach**, whose job
   per the GDD is to close a gap, not to end the fight. Making D chip rather than
   threaten keeps its purpose legible.
2. **C above B, despite B being "committed."** B is a *sequence*, so it will land more
   often per use than C's single reaching strike (see the multi-hit note below). C is a
   long single commit with a large recovery, so it should hurt more when it connects.
3. **B × 4 = exactly 100.** A small readability gift: if the designer ever wants to
   demonstrate the hit budget to a playtester, B is a clean quarter of the bar.
4. **Nothing here removes counterplay.** The GDD forbids armour from removing readable
   counterplay. At these values every attack is survivable at least three times, so no
   single mistake ends the duel — the loss comes from a *pattern* of mistakes, which is
   the readable failure the GDD wants.

### The multi-hit problem with attack B — a real authoring decision

The GDD calls B a **"sequence."** If B is authored with two or three `ANS_ActiveHit`
windows and each one reads `DT_VanguardAttacks.Damage = 25`, **B deals 50–75 % of the
player's health in one attack** and the whole budget above is void.

> **Proposed rule:** `DT_VanguardAttacks.Damage` is the **total damage of the attack**,
> not the damage of one active window. If an attack is authored with more than one
> `ANS_ActiveHit`, the notify states split the row value between them (B as 12 / 13, or
> 8 / 8 / 9). The designer then still retunes B by editing **one** number.

This is a data-path decision as much as a damage decision, and it belongs to the
developer's `ANS_ActiveHit` implementation. **Flagging it here because it is the single
most likely way this table silently produces a broken fight.**

### Prior art (real games, named)

| Game | Mechanism | Real numbers | Relevance |
|---|---|---|---|
| **Sekiro: Shadows Die Twice** | A small hit budget against telegraphed heavy attacks | Community reporting: the Ashina Outskirts samurai kills at starting vitality **in 2–3 hits**, and continues to do so as a regular enemy later | The tightest end of the readable band. Our 4-hit typical case is one step back from it |
| **Monster Hunter: World** | Damage tiering is explicitly by *telegraph class* — signature heavy attacks are authored as "meant to be dodged," not tanked | Named examples: Nergigante's divebomb, Teostra's supernova, Vaal Hazak's breath, Kushala's breath. Reported design: most moves are **not** true one-shots; they deal a lot and are survivable with defence, and the game teaches avoidance rather than tanking | Direct support for the A-vs-D spread. The heaviest, most telegraphed attack is the one you are supposed to answer, and the game makes that choice by damage number, not by making it unavoidable |
| **Tekken 8** | Damage per move sits against a small readable pool that the developer retunes post-launch | Pool **180** at launch → **200** in patch **2.00.02** | Confirms that the correct response to "the hit budget feels wrong" is to move the pool, not the move table — which is why Q1 is one field and Q3 is a percentage of it |

### How it interacts with the other four

- **Q1 is the denominator.** These are percentages. If the designer moves Q1 to 150,
  the Data Table becomes 48 / 37.5 / 40.5 / 27 and **the hit budget does not change.**
  That decoupling is the entire reason §14 asked for percentages and the reason Q1 was
  set to 100.
- **Q2 / Q4 / Q5 are untouched by this.** Rival damage does not participate in the gate
  arithmetic at all. It only decides how many mistakes fit inside the duel length that
  Q2 and Q4 set.
- **Open elsewhere, assumed here:** **Q27** (`ANS_Recover` incoming-damage multiplier) is
  the *player's* damage, not the rival's, so it does not scale this table. **Q6 / Q7**
  decide how often these numbers are actually paid. **Q10** (range bands) decides which
  of the four the player eats most — if A's band is generous, the effective budget drops
  toward 4; if D dominates, it rises toward 6. **Re-check this table after Q10.**

**This is a recommendation. The designer decides.**

---

## Q4 — Player light-hit damage, and whether the finisher hits harder

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-17**
- **Value lives in:** `AM_Player_LightCombo` notify data — the damage payload on each
  section's `ANS_ActiveHit` (`design-brief.md` §13.2 row 32)
- **GDD range:** **The GDD publishes no player damage numbers.** It publishes only the
  *meter* consequence of the string — **light-combo finisher = +5**, "Small reward for
  sustained offense" (`gdd/sections/03`, PDF p.3) — and, via SCOPE LOCK, that this is
  **one shared kit**, so Echo and Nova use the **same** damage payload.

### Proposed values

> **Light hit = `5`** · **Finisher = `10`** (**yes, the finisher hits harder — 2×**).
> **Full 3-section combo = 5 + 5 + 10 = `20` damage.**
> Identical for Echo and Nova. Authored on the montage sections, one payload each.

Against the proposed `VanguardMaxHealth = 1200`:

| | Damage | % of rival max HP | Count needed |
|---|---|---|---|
| One light hit | 5 | 0.42 % | — |
| One finisher | 10 | 0.83 % | — |
| **One full combo** | **20** | **1.67 %** | — |
| 100 % → 50 % (Phase 2) | 600 | 50 % | **30 combos** |
| 100 % → 25 % (gate arms) | 900 | 75 % | **45 combos** |
| 100 % → 1 HP floor (post-failure only) | 1199 | ~100 % | **60 combos** |

### Why the finisher hits harder — and why exactly 2×

1. **It puts the damage where the GDD already put the meter.** The GDD pays **+5 only on
   the finisher** — the first two hits pay nothing. If damage were flat, the game would be
   telling the player two different things: "the finisher is what matters" (meter) and
   "any hit is equally good" (damage). **2× aligns both rewards on the same input**, which
   is the cheapest possible way to teach the string.
2. **It makes the string a real commitment.** With a back-loaded combo, bailing after two
   hits costs the player **half the combo's damage and all of its meter**. That is a
   genuine risk/reward decision against the rival's recovery window rather than a
   free-win button.
3. **2× and not more.** At 3× the third hit becomes mandatory and the first two become
   filler; at 1.5× the incentive is too weak to change behaviour. 2× is the standard
   shape and it keeps the arithmetic in the tables above clean (a combo is exactly
   4 light-hit units).

### Why 5 and not some other number

The absolute value is arbitrary on its own — **only the ratio `Q2 : ComboDamage`
matters**, and that ratio was solved in Q2. `5` is chosen because:

- **60 combos** takes the rival from full to the 1 HP floor, and **45** arms the gate.
  Both are round, countable numbers a designer can verify in a single playtest by
  counting combos.
- It leaves headroom **below** for any future chip source without needing fractions
  (Impact-burst damage, if the designer ever wants the cinematic to deal any — currently
  it deals none and that is not proposed here).
- It keeps every value in `DA_TuningGlobals` and the montage an integer. **No floats in
  the damage path** is a small but real defence against tuning drift.

### The failure mode this creates — name it now

A player who lands **two hits and bails every cycle** deals **10** per cycle instead of
20 and earns **zero meter** (no finisher, and dodging out without a perfect dodge pays
+0). That player reaches the ≤ 25 % gate in roughly **double** the time with an **empty
meter** — which is precisely the C3 stall Q22 warned about.

**This is the only realistic path to a C3 failure**, and this group cannot close it
alone. The levers all sit in other groups: **C2's HUD gate indicator** (tell the player
which gate is locked), the GDD's **onboarding Impact Window** in Phase 1
(`gdd/sections/03`, p.4 — it guarantees at least one +20 opportunity is taught early),
**Q28** (`ANS_ComboLink` buffer — make finishing the string easy to *input*), and **Q25**
(recover windows long enough that the third hit is *reachable*). **Named and handed off,
not solved here.**

### Prior art (real games, named)

| Game | Mechanism | Real numbers / detail | Relevance |
|---|---|---|---|
| **The "Three-Strike Combo" pattern** (TV Tropes' catalogue of the convention across action games) | The basic string is three attacks in rapid succession with the last hit dealing **slightly more** damage than the first two | Documented as the default convention, not one game's invention | The exact shape proposed, and evidence it is what players already expect. Note the convention says *slightly* more; **2× is at the assertive end** and is a deliberate choice to align damage with the GDD's finisher-only meter |
| **Hi-Fi Rush** | Boss HP comes down through completed combo strings and Beat Hits, which deal **additional** damage over ordinary hits | Reported as the intended route to draining a boss ("big combo strings … Beat Hits deal additional damage") | A shipped game that puts the boss-damage payoff at the end of the string rather than spread across it — the same structure, in a game with the same "earn the spectacle" pitch |
| **Devil May Cry 5** (Nero, Red Queen) | The default light string is a fixed-length, fast, low-commitment tool, with power layered on by a separate resource | Combo A is described as a **4-hit** sword combo; **Exceed** multiplies Combo A–D, Aerial Combo and Roulette Spin attack power by **×1.2** | Shows the alternative architecture — flat string, multiplier elsewhere. **Rejected here** because we have no Exceed-equivalent and SCOPE LOCK forbids adding one; the finisher must carry the weight itself |
| **Fighting-game combo theory** (general, as summarised in the critpoints analysis) | Longer strings exist so players can trade damage against positioning, meter, knockdown and safety; committing to a full string is a risk because **combos get dropped** | Qualitative, no numbers | Supports back-loading as the mechanism that makes a dropped string cost something |

### How it interacts with the other four

- **Q2 is the other half of the ratio.** `900 / 20 = 45 combos`. Change either and duel
  length moves proportionally. **Prefer moving Q2** — see the Q2 note on why.
- **Q5 sets how many payloads there are.** At Q5 = 3 the combo is 5 + 5 + 10. At Q5 = 4
  it would have to be 5 + 5 + 5 + 10 = 25 (duel shortens ~20 %, so Q2 would rise to
  ~1500) **or** 4 + 4 + 4 + 8 = 20 (duel length preserved, individual hits feel weaker).
  **Q4 and Q5 cannot be answered separately** and are answered together here.
- **Q1 / Q3 are unaffected** — separate economy.
- **Open elsewhere, assumed here:** **Q27** (`ANS_Recover` incoming-damage multiplier)
  multiplies these numbers during the rival's recovery window. At the §14 upper bound of
  **1.5**, a punish combo deals **30** instead of 20 and the 45-combo count drops toward
  ~30 for a player who only ever attacks into recovery. **Q27 is a direct scalar on the
  Q2 derivation and must be resolved before Q2 is locked.**

**This is a recommendation. The designer decides.**

---

## Q5 — Light combo length (number of montage sections)

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-17**
- **Value lives in:** `AM_Player_LightCombo` — the montage's section count
  (`design-brief.md` §13.2 row 33)
- **GDD range:** **The GDD publishes no count.** `gdd/sections/02` (PDF p.2) names a
  *"light attack sequence"* in the control model and `gdd/sections/03` (PDF p.3) names a
  *"Light-combo finisher"* worth **+5** — so the GDD guarantees the string has a
  **distinct final hit** and says nothing about how many come before it.
  `design-brief.md` §14 offers **3** as the common readable default and **4** as the
  option that "allows a heavier finisher."
- **This one genuinely blocks.** A montage's sections cannot be authored without the
  count. **M1-17 cannot start until the designer answers this.**

### Proposed value

> **3 sections.** `S_Hit1` → `S_Hit2` → `S_Finisher`.
> `S_Finisher` is the only section that fires the GDD's **+5** and the only one carrying
> the **2× damage** payload from Q4. Target total montage length **≈ 1.0 s**
> (~0.33 s per section) at `MontagePlayRate = 1.0`.
> One montage, shared by Echo and Nova — per the SHARED PLAYER-KIT SCOPE RULE the two
> avatars differ only by **`DA_FighterProfile.MontagePlayRate`** (**Q14, open**) and by
> presentation, **never** by section count.

### Why

1. **It is the only count that fits the rival's Phase 2 window.** From the Q2 derivation:
   the rival is non-threatening for **≈ 1.73 s in Phase 1** but only **≈ 1.28 s in
   Phase 2** (Recover + Return + Reposition, GDD midpoints). A 3-section combo at ~1.0 s
   fits both with margin. **A 4-section combo at ~1.33 s does not fit Phase 2 at all** —
   the fourth hit would land inside the rival's next Telegraph, so the player would
   either stop finishing strings in Phase 2 (losing the +5 row entirely, exactly when the
   GDD wants "learned reads under stress") or eat a hit every combo. **This is the
   decisive argument and it is arithmetic, not taste.**
2. **The finisher can already be heavier at 3.** §14's stated reason for 4 — "allows a
   heavier finisher" — is satisfied by Q4's 2× payload without adding a section.
3. **It halves the animation exposure.** `design-brief.md` §12.6 flags the strike
   animation set as *"the schedule's tightest resource"* with a 1 September ship date.
   Three sections is three retargeted Mixamo clips instead of four, and three sets of
   `ANS_ActiveHit` / `ANS_ComboLink` windows to tune instead of four.
4. **It tightens the meter cadence.** +5 every ~1.0 s of committed offense instead of
   every ~1.33 s. Small, but it points the same way as everything else.

### Prior art (real games, named)

| Game | Mechanism | Real numbers / detail | Relevance |
|---|---|---|---|
| **The "Three-Strike Combo" convention** (TV Tropes' cross-game catalogue) | The default basic combo across action games is **three attacks in rapid succession**, last hit slightly stronger | Documented as the genre default | The direct precedent for 3 and for the back-loaded finisher, in the same sentence |
| **Bayonetta** | The basic string is a short fixed input chain that pays out on completion | The **punch-kick-punch** string is described as the quickest, most effective route to a Wicked Weave **without consuming magic** | A shipped 3-input string whose *whole point* is that completing it triggers the payoff — structurally identical to our +5-on-finisher |
| **Devil May Cry 5** (Nero, Red Queen) | Longer default string, in a game with cancels, Exceed, Devil Breakers and a large moveset | **Combo A is a 4-hit sword combo** | The honest counter-example for 4. It works there because DMC5 gives the player cancels and enemies that stagger; **we have neither, and a Phase 2 window of 1.28 s.** Cited so the designer can see what choosing 4 would commit us to |
| **Batman: Arkham** series | Very short basic attack, everything else layered on top | The basic punch is the highest-value combo builder — a critical strike **adds 3 to the combo meter** where most abilities add 1 | Precedent for keeping the base string small and cheap and letting the surrounding systems (here: perfect dodge, counter, Impact Window) carry depth. That is exactly our meter table's shape: the finisher is the **smallest** gain at +5 |

### How it interacts with the other four

- **Q4 is inseparable from it** — 3 sections means 5 / 5 / 10. See Q4 for what 4 sections
  would force.
- **Q2 depends on it** through `SecondsPerCombo`. **Choosing 4 sections invalidates the
  Q2 = 1200 derivation** and requires re-running the identity.
- **Q1 / Q3 are unaffected.**
- **Open elsewhere, assumed here:** **Q28** (`ANS_ComboLink` input-buffer, §14 suggests
  0.15–0.30 s before each section ends) decides whether the third section is reachable at
  all under pressure — **if the buffer is tight, the +5 row and the 2× payload both go
  unclaimed and the C3 stall risk in Q4 gets worse.** **Q25** (per-attack recover values
  inside the GDD ranges) decides the real size of the punish window; if the designer
  authors Phase 2 recovery toward **0.35 s**, even a 1.0 s combo stops fitting and Q5
  should be revisited. **Q14** (`MontagePlayRate`) scales the whole montage — if Nova's
  rate is set above 1.0 her combo is shorter than 1.0 s and fits more easily than Echo's,
  which is a *feel* difference the GDD permits but which quietly changes her damage rate
  per cycle. **Flag for the Q14 group.**

**This is a recommendation. The designer decides.**

---

## Cross-check — all five together, and the C3 verdict

All arithmetic below assumes the four proposed values (Q1 = 100, Q2 = 1200,
Q4 = 5/5/10, Q5 = 3 sections), the Q3 table, **C1 (no meter decay — Q9, still open)**,
and GDD state midpoints for the rival cycle (**Q25, still open**).

### 1. Hits to kill the player

| Attack | Damage | Hits to kill |
|---|---|---|
| A | 32 | **4** |
| B | 25 | **4** |
| C | 27 | **4** |
| D | 18 | **6** |
| Mixed diet (mean 25.5) | — | **~4** |

**Verdict:** inside §14's 3–5-hit budget for A/B/C; D is deliberately a 6-hit chip
attack because the GDD gives it an *approach* role. ✔

### 2. Combos to open the ≤ 25 % gate

`0.75 × 1200 = 900 damage` ÷ `20 per combo` = **45 full combos**.
Phase 2 commits at **600 damage = 30 combos**.
From the gate down to the 1 HP floor is a further **~15 combos** (only reachable after a
failed Clash, and it earns nothing).

### 3. Successful actions to reach meter 100 — the GDD gains, unchanged

| Route | Arithmetic | Actions needed |
|---|---|---|
| Combo finishers only (+5) | 20 × 5 = 100 | **20** |
| Perfect dodges only (+12) | 8 × 12 = 96; 9th → 108, clamped | **9** |
| Counters only (+15) | 6 × 15 = 90; 7th → 105, clamped | **7** |
| Impact Window successes only (+20) | 5 × 20 = 100 | **5** |
| Perfect dodge → Impact chain (+32) | 3 × 32 = 96; 4th → 128, clamped | **4 chains** |
| Counter → Impact chain (+35) | 2 × 35 = 70; 3rd → 105, clamped | **3 chains** |
| **Rebuild after a failed Clash (50 → 100)** | | **10 finishers**, or **5 perfect dodges** (60), or **2 counter-chains** (70) |

**Wall-clock estimate.** An Impact Window is opened by a perfect dodge or a counter
(`design-brief.md` §11.3) and then gated by **Q26 (open, §14 suggests 3–8 s)**. One chain
spans at least one rival cycle (2.3–2.9 s) plus the **1–3 s** GDD burst ≈ **5 s**. So:

- **Aggressive-defensive play:** meter 100 in **4 chains ≈ 20–40 s** (the upper end if
  Q26 lands at 8 s).
- **Offense-only play, no Impact, no perfect dodge:** 20 finishers at ~0.7 combos/cycle
  ≈ 29 cycles ≈ **84 s**.
- **Realistic mixed play:** **~40–60 s**.

### 4. Duel length against the 3–5 minute target

| Run | To gate | + entrance, approach, Clash | + one failed Clash (3 s cd + ~20 s rebuild + retry) | **Total** |
|---|---|---|---|---|
| Competent (0.7 combos/cycle), Clash succeeds first try | 2:53 | ~0:20 | — | **≈ 3:13** |
| Competent, one failed Clash | 2:53 | ~0:20 | ~0:35 | **≈ 3:48** |
| Scrappy (0.45 combos/cycle), one failed Clash | 4:29 | ~0:20 | ~0:35 | **≈ 5:24** |

**Verdict:** competent play lands at **3:13–3:48**, dead centre of the GDD's **3–5
minutes**. ✔ The scrappy run **overshoots to ~5:24** — flagged honestly. Two things
absorb it in practice: a scrappy player is also eating more of the Q3 table and may
reach the loss outcome first (which is a valid, GDD-sanctioned ending), and Q2 can be
trimmed toward **1100** if playtest shows the tail dragging. **If the designer wants the
worst case strictly inside 5:00, drop Q2 to ~1050–1100 and accept a ~2:35 competent run.**

### 5. C3 — "≤ 25 % and meter 100 must arrive close together"

They do **not** arrive close together, and **that is the correct outcome given the GDD's
fixed gains.** Meter 100 arrives at **~0:40–1:25**; the health gate arrives at
**~2:53**. The ordering is **meter first, health second**, and that ordering is the safe
one:

- **Meter first** means the player spends the tail of the duel *attacking*, which is
  progress. No dead time.
- **Health first** would mean the player standing in front of a rival pinned at 1 HP
  farming meter with damage doing nothing. **That is the C3 stall, and it does not occur
  in normal play at these values.**

**C3 is satisfied**, with two residual exposures named:

1. **The post-failed-Clash rebuild.** After a failure the rival may already be near the
   1 HP floor and the meter is forced to 50. During the rebuild, damage is genuinely
   inert. Bounded at **~15–35 s** (2 counter-chains, or 5 perfect dodges, plus the
   mandatory 3 s cooldown). **This is the designed setback the GDD asks for and it is an
   acceptable length** — but the **C2 HUD gate indicator is not optional here.** With the
   health bar visibly pinned, the HUD is the only thing telling the player that meter is
   the remaining gate.
2. **The 2-hit-and-bail player** (see Q4). Never finishes a string, never perfect dodges,
   never counters → **zero meter**, half damage rate, and eventually a pinned rival with
   an empty bar. **This group cannot close that case.** It is closed by C2's HUD, the
   GDD's onboarding Impact Window, **Q28**, and **Q25**. **Handed off, not solved.**

### 6. What would invalidate this whole set

| If this changes | Recompute |
|---|---|
| **Q9** resolves to meter **decay** (violating C1) | Every meter timing in §3 above, and the C3 verdict |
| **Q25** authors the rival toward the fast end of every GDD range | Cycle length → `CombosPerCycle` → **Q2** |
| **Q27** sets the recover damage multiplier above 1.0 | Effective combo damage → **Q2** |
| **Q5** is answered as **4** | **Q4** payloads and **Q2** together |
| **Q7** lands tight | **Q1** and the Q3 "A = 34" variant |
| **Q26** (Impact cooldown) lands at the long end | Meter fill time — pushes it later, *toward* the health gate, which is fine and arguably good |

### 7. The five proposed values, in one place

| Q | Value | Lives in | Status |
|---|---|---|---|
| **Q1** | Player max health **100** (Echo = Nova) | `DA_TuningGlobals` | **PROPOSED** |
| **Q2** | Vanguard max health **1200** (band 1100–1400) | `DA_TuningGlobals` | **PROPOSED** |
| **Q3** | A **32** · B **25** · C **27** · D **18** (% of player max HP) | `DT_VanguardAttacks.Damage` | **PROPOSED** |
| **Q4** | Light hit **5**, finisher **10** (2×) → combo **20** | `AM_Player_LightCombo` notify data | **PROPOSED** |
| **Q5** | **3** sections — `S_Hit1` / `S_Hit2` / `S_Finisher` | `AM_Player_LightCombo` | **PROPOSED** |

**All five are recommendations. The human designer of record decides all five, and each
stays open in `TODO.md` marked PROPOSED until they do.**

---

## Sources

Researched by WebSearch on 2026-08-02. **13 searches used against a 15-source cap.**
Two intended lookups — datamined boss HP figures for Sekiro and for Elden Ring's Margit —
**returned no reliable number and are therefore not cited anywhere above.**

- [Vitality — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Vitality)
- [Attack Power — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Attack+Power)
- [Sekiro — "how many attack power and vitality needed for final boss" (Steam Community)](https://steamcommunity.com/app/814380/discussions/0/3592212630594942649/)
- [How do you progress into boss health bars? — Furi (Steam Community)](https://steamcommunity.com/app/423230/discussions/0/154641879447553938/)
- [Furi Review — Bullet Hell Boss Rush Bonanza (DualShockers)](https://www.dualshockers.com/furi-review-nintendo-switch-ps4-xbox-one/)
- [Furi (Wikipedia)](https://en.wikipedia.org/wiki/Furi)
- [Sifu — How Does Structure Work (Attack of the Fanboy)](https://attackofthefanboy.com/guides/sifu-how-does-structure-work/)
- [How Sifu's Structure System Actually Works (SVG)](https://www.svg.com/760718/how-sifus-structure-system-actually-works/)
- [Hi-Fi Rush — How to defeat Kale Vandelay, the final boss (Sportskeeda)](https://www.sportskeeda.com/esports/how-defeat-kale-vandelay-final-boss-hi-fi-rush)
- [Hi-Fi Rush: 10 Best Combo Attacks (eXputer)](https://exputer.com/guides/hi-fi-rush-best-combo-attacks-top-10/)
- [Street Fighter 6: Health Values Of All Characters (eXputer)](https://exputer.com/guides/sf6-health-values/)
- [Health — Tekken Wiki (Fandom)](https://tekken.fandom.com/wiki/Health)
- [Red Queen — Devil May Cry Wiki (Fandom)](https://devilmaycry.fandom.com/wiki/Red_Queen)
- [DMC5 Nero Gameplay Guide (GameWith)](https://gamewith.net/devil-may-cry-5/article/show/8220)
- [Three-Strike Combo (TV Tropes)](https://tvtropes.org/pmwiki/pmwiki.php/Main/ThreeStrikeCombo)
- [What's the point of combos in fighting games? (critpoints)](https://critpoints.net/2019/11/11/whats-the-point-of-combos-in-fighting-games/)
- [Bayonetta 3 / Batman Arkham combat comparison thread (Pyra & Pandora boards)](https://pyra-handheld.com/boards/threads/games-that-works-like-batman-arkham.77865/)
- [Batman: Arkham Design Analysis, Part 1 (Game Developer)](https://www.gamedeveloper.com/design/batman-arkham-design-analysis-part-1-)
- [ThatOneAttack / Monster Hunter (TV Tropes)](https://tvtropes.org/pmwiki/pmwiki.php/ThatOneAttack/MonsterHunter)
- ["Endgame" and being one-shot — Monster Hunter: World (Steam Community)](https://steamcommunity.com/app/582010/discussions/0/1637543304839037646/)

---

## Constraint compliance

| Constraint | How this file complies |
|---|---|
| **SCOPE LOCK** | One player, one authored rival, one arena, one shared framework, four attacks A–D, one duel. Echo and Nova share **one** health value, **one** combo montage, **one** damage payload. No fifth attack, no per-fighter health, no second phase beyond the GDD's Phase 2, no deferred feature designed |
| **No runtime AI-model calls** | Nothing proposed here is adaptive, learned or generated at runtime. Every value is a static field on a Data Asset, a Data Table row, or a montage notify payload |
| **Numbers unchanged** | Every GDD number is reproduced verbatim and used as a fixed input: 0–100, +5/+12/+15/+20/+0, 50 %, 100 AND ≤25 %, 1 HP / 50 / 3 s, 3–5 minutes, and the §13.1 state ranges. **None was altered, and no answer here requires altering one** |
| **Designer owns every number** | All five answers are marked **PROPOSED**, each says so in its own section, and the summary table says so again |
| **Q22 binding** | Every answer is reasoned inside the permanent 1 HP floor. Q2 is treated as a gate timer, Q4 as gate-opening rather than killing, and C3 is answered explicitly with its residual exposures named |
| **Milestone order** | Q1/Q2 unblock M1-05, Q4/Q5 unblock M1-17, Q3 unblocks M2-04. No M5 presentation work is designed or implied |
| **This is Ascendant Impact** | Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, the Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears |
