# Group 01 — BLOCKING — Q22

**Dispatched:** 2026-08-02 · **Status of every answer below: PROPOSED — the designer decides.**

## Q22 — Is the 1 HP floor permanent or Clash-only?

- **Kind:** B (design) · **BLOCKING**
- **Status:** PROPOSED
- **Unblocks build step:** M1-08 — Create the shared `BP_HealthComponent`
- **Value lives in:** `HealthComponent.MinHealthFloor` (`design-brief.md` §13.2 row 50)
- **GDD range:** not a ranged value — this is an **interpretation** of the GDD's failed-Clash rule, not a number. Nothing below edits a GDD number.

**The GDD line being interpreted**, verbatim from
`gdd/sections/03-ascension-meter-final-clash-and-encounter-flow.md` (GDD v0.4, pp. 3–4,
*Final Clash resolution* table, **Failure** row):

> Separate both fighters; preserve current health with Crimson Vanguard
> held at a 1 HP floor; reduce meter to 50; apply a 3-second re-trigger
> cooldown.

Three other GDD lines bear on the reading, and they do not all pull the same way:

- **Encounter flow, same file (p. 4):** `Win / Loss | Final Clash success / selected fighter health reaches zero | Complete duel loop`. **This table names exactly one win condition and it is Final Clash success.** "Crimson Vanguard's health reaches zero" is not listed.
- **Scope lock, `gdd/sections/09-course-scope-lock-and-future-expansion.md` (p. 15):** "The required prototype is complete when the player can … **reach and retry the Final Clash**, and finish with a valid win or loss."
- **Definition of done, same file:** `Climax | Final Clash obeys both unlock conditions and supports recovery after failure`.

Set against those: the floor is stated **inside the failure row**, which is the narrow
literal argument for scoping it to the Clash. Nowhere does the GDD say the rival can be
defeated by ordinary damage, and nowhere does it say the rival cannot. **The silence is
real, and only the designer can break it.**

---

### The two readings

| | **(a) Clash-only floor** | **(b) Permanent floor** |
|---|---|---|
| `MinHealthFloor` | Defaults `0`. Set to `1` by `BP_FinalClashDirector` for the duration of a Clash attempt only; cleared in `RestoreCombatState()`. | `1` for the duel. Only `ClashSuccess()` lowers it to `0` immediately before applying lethal damage (`design-brief.md` §9.3). |
| Can ordinary damage kill the rival? | **Yes.** Rival HP → 0 → `OnDeath` → `BP_DuelDirector.EndDuel(Win)`. | **No.** Damage clamps at 1. |
| Win paths | **Two**: damage-out, or Final Clash. | **One**: Final Clash. |
| What the double gate means | An optional, flashier route to an ending you could have got anyway. | The only ending. |
| Matches the encounter-flow table? | Adds a win condition the table does not list. | Matches it exactly. |
| Matches the failure-row wording literally? | Yes — the narrow read. | Defensible — the failure row is where the floor first *matters*, not necessarily where it first *applies*. |

**Two sub-variants of (b), because they build differently and feel different.** Both are
"permanent"; neither invents a number.

- **(b1) Floor engages at the gate threshold.** `MinHealthFloor` flips `0 → 1` the first
  time rival health crosses **≤ 25 %** — reusing the number the GDD already uses for the
  Clash gate. Nothing new to tune. Cost: a state transition to write and test, and the
  rival is unkillable across the whole last quarter of its bar.
- **(b2) Floor armed all duel; the clamp only ever bites on the killing blow.**
  `MinHealthFloor = 1` from `BeginPlay`. Nothing is observably different until the one hit
  that would have taken the rival to 0, which lands it on 1 instead. One expression —
  `Max(NewHealth, MinHealthFloor)` — no state transition anywhere, nothing to desync.
  **Cheaper and less bug-prone than (b1); behaviourally identical to the player.**

---

### Prior art — real shipped games

Researched 2026-08-02, 10 sources. Only sourced claims are stated; anything I could not
confirm is marked **unverified** rather than filled in.

#### Gate the kill behind a finisher — supports reading (b)

**Sekiro: Shadows Die Twice — Deathblow markers.** The closest real analogue, and the most
instructive. Sekiro bosses carry red **Deathblow markers** beside the Vitality bar, and
*"the only way to remove these Deathblow markers is by completely depleting the Posture or
Vitality of said Boss and then performing a deathblow."* Emptying Vitality does **not**
kill the boss; it produces the Deathblow *opportunity*, which the player must then execute.
Between Deathblows, Vitality and Posture are **fully restored**.

What Sekiro buys, and Ascendant Impact could copy: every fight ends on the same authored,
readable beat, so the climax is guaranteed. **What Sekiro does that our design does not:**
the finisher is *guaranteed available* the instant the health condition is met. There is
no second resource the player might be short of. Sekiro never puts the player in "the boss
cannot die and I cannot finish it." **Our double gate can produce exactly that state**, and
that is the entire risk in reading (b).

Second thing worth stealing: Sekiro couples the two bars — *"the lower the Vitality, the
slower the Posture recovery."* Chip damage always advances you toward the finisher even
though it can never land the kill. **Our meter has no coupling to rival health at all.**
Under the GDD's economy the only offensive gain is the light-combo finisher at **+5**, the
smallest of the five. That decoupling is the thing to look at hardest before choosing (b).

**Metal Gear Rising: Revengeance — the 10 % QTE.** Monsoon: *"once the boss's health bar
drops below 10 %, a QTE will start, in which Raiden will deal with Monsoon after the correct
buttons are pressed."* Sundowner: *"once its health bar drops to 10 %, the usual QTE sequence
will start."* Functionally this is a **health floor at 10 % plus a mandatory timing sequence**
— structurally very close to our ≤ 25 % gate — except that MGR is **single-gated on health
alone and auto-triggers**. The player is never asked to bring a second resource, and the
finisher cannot be locked out.

**Hi-Fi Rush — Rhythm Parry finisher sets.** Reported: the boss Mimosa *"will perform two
sets of Rhythm Parries at the end of her health, and they must be performed to the threshold
to end the boss fight,"* and Kale performs a Rhythm Parry set to move between phases. Again:
health floor plus mandatory timing beats — the same shape as our Final Clash's two beats.
**Unverified:** I could not confirm from a solid source what exactly happens on a failed set.
Community reporting suggests the sequence resets rather than the fight ending, which would
match our failed-Clash recovery rule, but do not treat that as established.

**Star Wars Jedi: Fallen Order — the near-zero blade lock.** Reported: *"when getting a
boss's health bar down almost to nothing, the game goes into a quicktime instance where you
lock blades with the boss."* **Unverified in detail** — I could not confirm whether the
finish is automatic or requires input. Included only because it is a third shape worth
knowing: the finisher is *triggered by damage crossing a threshold* rather than gated behind
a separate meter. That shape is not available to us — the GDD requires the player to
**choose** to initiate the Clash and to complete **two** timing beats — but it explains why
so many action games put the floor at a health threshold and nothing else.

#### Finisher optional, damage still kills — supports reading (a)

**Sifu — Structure break and Takedown.** Breaking a boss's Structure produces a Takedown,
*"however, breaking structure is not always required to finish a boss — it's simply an
efficient way to do so."* Health depletion kills. The revealing detail is in Sifu's sparing
path: to spare a boss you must break Structure twice in phase two *"without letting their
health bar get to zero, otherwise you will automatically finish them off."* Sifu's designers
had to **warn the player away from the damage route** to protect the authored ending. That is
precisely the tension reading (a) creates here: the damage route can quietly steal the
ending from the Clash, and the only fix inside the rules is asking the player not to take it.

**God of War Ragnarök — stun/stagger grab.** *"The R3 grab finisher is not mandatory — you
can continue dealing damage to stunned enemies and kill them without performing the finishing
move."* This is the standard modern action-game position and it works, but note the context:
God of War is an encounter-based game with dozens of fights, where a missed finisher costs
you flavour, not the climax. **We have exactly one fight.** A skippable climax in a
three-minute single-duel prototype is a much bigger loss than a skippable finisher in a
twenty-hour game.

**Furi — the closest genre neighbour.** A gauntlet of pure 1v1 duels built on
attack / dash / **parry**, where *"each boss in Furi possesses multiple health bars … each
health bar denotes a different phase — switching up tactics with every bar depleted,"* and
*"pull off a perfectly-timed parry, and you'll be treated to a complimentary combo for some
extra damage."* Furi is reading (a): duels end when the last bar empties. It gets away with
it because the ending cinematic is triggered *by* the damage-out — the spectacle is
guaranteed rather than gated. **If the designer picks (a), Furi is the model to study**, and
the lesson is that the reward has to be attached to the damage-out, not held behind a
separate resource.

#### The cautionary case

**Asura's Wrath.** A game whose progression is almost entirely gated behind authored timing
beats. *"Correct inputs when prompted will advance the story while failure can cause the
restart of a sequence and damage to health in a previous gameplay sequence,"* and reviewers
criticised the *"terrible implementation and gated content"* around an otherwise solid
counter-based combat system, singling out boss fights where *"the margin for error … is so
slim as to be nonexistent."* The warning for us is narrow and specific: **reading (b) makes
Q20 (Clash beat response times) the single hardest gate in the game.** If beat 2 is tuned
tight and it is the only exit, a player who can fight perfectly can still be unable to
finish. Under reading (a) that same player has another way out.

**On softlocks, generally.** The standard framing is useful here: a softlock is a state
where *"the game remains apparently playable, but further progress is impossible,"* and the
dangerous version is not a bug — it is *"the interaction of the game's systems"* creating a
dead end *"even though all systems are working as intended."* The prevention rule is
"always ensure a path forward." Reading (b) must be checked against that rule explicitly,
and it is checked below.

---

### Cost, pacing, and failure mode of each reading

#### Build cost — M1-08 `BP_HealthComponent`

The clamp expression is the same in both readings:
`NewHealth = Clamp(CurrentHealth - Damage, MinHealthFloor, MaxHealth)`. **What differs is
the default value, who owns the transitions, and whether the rival's death-by-damage path
exists at all.**

| | (a) Clash-only | (b1) engage at 25 % | (b2) armed all duel |
|---|---|---|---|
| `MinHealthFloor` default | `0` | `0`, flips to `1` at ≤ 25 % | `1` |
| Who writes it | `BP_FinalClashDirector` on `InitiateClash()` / `RestoreCombatState()` — one set/clear pair, already described in `design-brief.md` §9.4 step 4 | `BP_HealthComponent.OnHealthChanged` **and** `BP_FinalClashDirector` | `ClashSuccess()` only |
| Rival `OnDeath` from ordinary damage | must be supported and wired to `EndDuel(Win)` | never reachable | never reachable |
| Extra state to test | the set/clear pair must be leak-proof — a Clash that fails during a montage abort must not leave the floor stuck at 1, or the rival becomes silently immortal | a threshold crossing that can fire on the same frame as the Phase-2 check | none |
| Verdict | cheap, one leak risk | cheap, one extra transition | **cheapest, no transitions** |

None of the three is expensive. **Build cost is not the deciding factor and should not be
used as one.** The deciding factor is what the game is about.

#### Pacing against the 3–5 minute session target

**Reading (a).** The duel can end the moment rival HP hits 0, whenever that is. The problem
is not the duration — it is *which* player gets which ending. Look at the meter economy the
GDD fixes: light-combo finisher **+5**, perfect dodge **+12**, counter **+15**, Impact
Window **+20**, damage taken **+0**. **The only offensive gain is the smallest one.** So the
aggressive player who chains light combos deals health damage fast and builds meter slowly,
while the defensive player who reads telegraphs builds meter fast and deals damage slowly.
Under (a) those two players get different games: the aggressive one wins by attrition and
**never sees the Final Clash**; the defensive one reaches the climax. The fastest route to
victory is to ignore the meter. That inverts pillar 1, *"Skill Creates Spectacle."*

This is tunable — raise Q2 (rival max health) and lower Q4 (player light-hit damage) until
meter 100 essentially always arrives before rival HP 0 — but that is a fragile balance
relationship the designer has to keep true forever, across every future tuning pass, with
no structural guarantee behind it.

**Reading (b).** The ending is fixed: every duel ends on the Clash. The rival's health bar
stops being a race to zero and becomes a **gate timer** — its only job is to reach 25 %. The
risk moves to the tail: once the player is at the floor with meter under 100, the fight
keeps running with rival health frozen. How long that tail is depends entirely on the meter
income rate, which means **Q26 (Standard Impact Window cooldown) and Q7 (perfect-dodge
window) become the real pacing dials, not Q2.**

#### The failure mode reading (b) creates — floor reached, meter never 100

This is the case the dispatch asks about directly, so here it is precisely.

**It is a stall, not a deadlock.** The rival cannot die. The player cannot win by damage.
But:

1. **A path forward always exists.** All four gains — +5 combo finisher, +12 perfect dodge,
   +15 counter, +20 Impact success — are repeatable and **none of them depends on rival
   health**. Crimson Vanguard keeps cycling its six states and keeps exposing `ANS_Recover`
   openings forever (GDD: *"every major offense exposes a clear recovery opening"*). So the
   softlock prevention rule — always ensure a path forward — **is satisfied**, structurally,
   not by luck.
2. **The floor is worst-case slow, not blocked.** A player who cannot land a perfect dodge
   or a counter is left with +5 combo finishers only: **20 finishers from empty, 10 from the
   post-failure 50.** Slow and unglamorous, but finite and reachable.
3. **The player can still lose.** Their own health reaching zero is the GDD's only loss
   condition and remains live throughout. So the stall always resolves — one way or another.
4. **Therefore the honest description is: reading (b) can produce a long, flat tail on the
   duel for a low-skill player, in which the rival's health bar is visibly pinned and
   nothing the player does to it matters.** That is a readability problem before it is a
   balance problem, and it has a readability answer — see the recommendation's condition 2.

**Three things make that tail worse, and all three are open questions:**

- **Q9 — meter decay.** Under (a), decay is a flavour choice. **Under (b) it is
  load-bearing and dangerous:** if decay ever outruns a struggling player's income rate, the
  stall stops being finite and becomes a true dead end. `design-brief.md` §14 already
  recommends no decay; under (b) that recommendation stops being a preference.
- **Q20 — Clash beat response times.** Under (b) these are the only exit from the game.
  Asura's Wrath is the cautionary case.
- **Q26 — Standard Impact Window cooldown.** It throttles the largest gain (+20), so it
  directly sets how long the tail runs.

#### The failure mode reading (a) creates

A complete, valid playthrough in which the player never reaches the Final Clash. Concretely:

- The GDD's own scope lock says the prototype is complete when the player can *"reach and
  retry the Final Clash."* Under (a) that is possible but not guaranteed — a build can pass
  a playtest without ever demonstrating M4's headline feature.
- **Demo and grading risk.** Whoever plays the 1 September build may simply beat it by
  attrition and never see the Clash, the two beats, the failure recovery, or the meter
  paying off. The single most expensive thing in M4 becomes the thing most likely to go
  unseen.
- The central promise — *"real-time martial-arts combat rewards player skill with brief,
  earned anime-style cinematic spectacle"* — becomes optional.

---

### Recommendation

**PROPOSED: reading (b), sub-variant (b2)** — `MinHealthFloor = 1` on the rival's
`BP_HealthComponent` from `BeginPlay`, lowered to `0` only by `ClashSuccess()` immediately
before it applies lethal damage. The Final Clash is the only way to win the duel.

**Why.**

1. **It is the reading the GDD's own encounter-flow table states.** That table lists one win
   condition — Final Clash success. Reading (a) requires adding a win condition the GDD never
   writes down; reading (b) requires only that the floor's scope be wider than the row it is
   printed in. Adding a condition is the bigger interpretive leap.
2. **It makes the double gate mean something.** Under (a) the gate guards an optional bonus,
   and a gate on an optional bonus does not need two conditions. Under (b) it is the door to
   the ending, which is why it has two locks.
3. **It aligns the win condition with pillar 1.** Under (b) the only way to win is through
   the meter, and the meter is only earned by reading telegraphs, dodging perfectly,
   countering, and hitting Impact Windows. Skill creates spectacle, structurally, not by
   tuning.
4. **It is the cheapest to build and the least likely to break** — one clamp, no
   transitions, one fewer win path to wire and test, no risk of a leaked floor flag leaving
   the rival silently immortal.
5. **Prior art supports it for this exact genre shape.** Sekiro and Metal Gear Rising both
   gate the kill behind an authored finisher and both are better for it. Sifu, which does
   not, had to design *around* its own damage route to protect its authored ending.

**Three conditions I would attach — each is itself a question for the designer, not a
decision I am making:**

- **C1 — Q9 must resolve to no meter decay.** Under (b) decay is the one thing that could
  turn a slow tail into a genuine dead end. `design-brief.md` §14 already recommends none;
  under (b) I would ask the designer to make it explicit rather than default.
- **C2 — the HUD must tell the truth about the floor.** `design-brief.md` §9.1 already
  specifies two separate gate indicators so the player can see *which* condition is missing.
  Under (b) that stops being a nice-to-have: the moment the rival's health bar visibly pins
  and stops moving, the player must be able to see that the remaining lock is the meter and
  not conclude the game is broken. Exactly how that reads on screen is a designer call and I
  am not specifying it. It is a readability requirement under the GDD's existing readability
  line, not a new feature.
- **C3 — Q2 (rival max health) should be tuned so ≤ 25 % and meter 100 arrive close
  together.** Under (b), Q2's job changes from "time to kill" to "when does the gate open,"
  and the tail length is the distance between those two moments. Designer's number, as always.

**This is a recommendation. The designer decides.** If the designer's priority is instead
that the duel must always be winnable by a player who cannot execute the Clash beats, then
**(a) is the correct answer** and the mitigation is a Q2/Q4 tuning relationship that keeps
meter 100 arriving first. That is a legitimate accessibility position and I am not
dismissing it — it simply buys robustness by making the climax optional, and the designer
should choose that trade knowingly rather than inherit it from a default value.

---

### What this changes downstream

**Do not tune these before Q22 is answered.** Listed as impact only — none of them is
answered here.

| Q | Question | How Q22 changes it |
|---|---|---|
| **Q1** | Player max health | **Minor change.** Under (b) a low-skill player spends longer at the floor rebuilding meter, so total exposure to rival attacks is higher. Q1 may need to sit higher under (b) than under (a). |
| **Q2** | Crimson Vanguard max health | **Changes the most.** Under (a) it is the primary pacing dial — it sets time-to-kill and therefore session length. Under (b) it only sets *when the gate opens*; pacing moves to the meter economy. **Q2 is not tunable until Q22 is decided.** |
| **Q3** | Rival attack damage A–D | **Changes.** Under (b) the stall tail means more incoming attacks per duel, and the only loss condition can fire during a tail the player can do nothing about except keep fighting. Damage-per-attack interacts with duel length differently in each reading. |
| **Q4** | Player light-hit damage / finisher bonus | **Changes meaning entirely.** Under (a) damage wins the game. Under (b) damage's only job is to reach 25 %; past that it does nothing. Under (a), Q4 and Q2 form the balance relationship that protects the climax. |
| **Q9** | Meter decay | **Flips from optional to load-bearing.** Under (a), any answer is safe. Under (b), decay risks a genuine dead end. See condition C1. |
| **Q19** | Post-counter Clash-initiation window | **Tolerance tightens.** Under (b) this window is on the critical path to any win. Too short and the player is repeatedly denied the only exit. |
| **Q20** | Clash beat 1 / beat 2 response times | **Tolerance tightens the most.** Under (b) these two windows are the sole exit from the duel. The Asura's Wrath warning applies directly. Under (a) a player who cannot hit them still has a way to finish. |
| **Q21** | Failed-Clash separation distance | **Matters more.** Under (b) the player must survive and rebuild after every failure, so being re-engaged instantly is more punishing. Must still clear every attack's `MinRange` (Q10). |
| **Q23** | Duel timer | **New consideration under (b).** A timer would convert a stall into a loss and cap the tail — but the GDD lists exactly one loss condition, so this would be adding one. `design-brief.md` §14 recommends no timer. **Still open; not answered here.** |
| **Q26** | Standard Impact Window cooldown | **Becomes a pacing dial under (b)**, because it throttles the +20 gain that shortens the tail. |

**Not affected by Q22:** Q5–Q8, Q10–Q18, Q24, Q25, Q27–Q31.

---

### What the developer should do with M1-08 in the meantime

Not a design decision — a sequencing note, so M1-08 is not blocked longer than it has to be.

The clamp itself is identical under all three variants. `BP_HealthComponent` can be built
now with:

- `MinHealthFloor` as an exposed, editable `float` on the component;
- `ApplyDamage` clamping as `Clamp(CurrentHealth - Damage, MinHealthFloor, MaxHealth)`;
- `OnDeath` broadcast only when `CurrentHealth <= 0` — which under (b) simply never fires
  for the rival until `ClashSuccess()` lowers the floor.

**What must wait for the designer:** the default value on the rival's instance, whether
`BP_DuelDirector` wires a rival `OnDeath → EndDuel(Win)` path at all, and — under (b1) only
— a threshold transition. The developer should **leave the rival's `MinHealthFloor` default
unset/at the class default and not wire the rival damage-out win path** until Q22 is
answered, rather than pick one and have it silently become the design.

---

### Sources

Prior-art research, accessed 2026-08-02:

- [Deathblows — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Deathblows)
- [Bosses — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Bosses)
- [Sekiro: Shadows Die Twice — official web manual, mechanics (FromSoftware)](https://www.fromsoftware.jp/manual/sekiroshadowsdietwice/stadia/mechanics.html)
- [Metal Gear Rising Revengeance: Monsoon — gamepressure.com guide](https://guides.gamepressure.com/mgsrevengeance/guide.asp?ID=23780)
- [Metal Gear Rising Revengeance: Sundowner — gamepressure.com guide](https://guides.gamepressure.com/mgsrevengeance/guide.asp?ID=23781)
- [Rhythm Parry — Hi-Fi Rush Wiki (Fandom)](https://hifi-rush.fandom.com/wiki/Rhythm_Parry)
- [Sparing Bosses — Sifu Wiki (Fandom)](https://sifu.fandom.com/wiki/Sparing_Bosses)
- [How to spare bosses in Sifu and break the cycle of revenge — GamesRadar+](https://www.gamesradar.com/how-to-spare-bosses-in-sifu/)
- [God Of War Ragnarok Stun Grab — How To Stun Enemies (Gamer Tweak)](https://gamertweak.com/stun-enemies-gow-ragnarok/)
- [God of War combat guide: How to crush enemies with Kratos — Digital Trends](https://www.digitaltrends.com/gaming/god-of-war-combat-guide/)
- [Furi's merciless boss-fight gauntlet is as brilliant as it is infuriating — The A.V. Club](https://www.avclub.com/furi-s-merciless-boss-fight-gauntlet-is-as-brilliant-as-1798188323)
- [Furi Review — Nonlinear Perspectives](https://stephenamansfield.com/furi-review/)
- [Asura's Wrath — Wikipedia](https://en.wikipedia.org/wiki/Asura%27s_Wrath)
- [Review: Asura's Wrath (Part 2) — Theology Gaming](https://theologygaming.com/review-asuras-wrath-part-2/)
- [Star Wars Jedi: Fallen Order bosses — PCGamesN](https://www.pcgamesn.com/star-wars-jedi-fallen-order/bosses-all-boss-fights)
- [How to Fix a Game That Soft-Locks Players — Bugnet Blog](https://bugnet.io/blog/how-to-fix-a-game-that-soft-locks-players)
- [The Soft Lock Trap — Amini Allight](https://amini-allight.org/post/the-soft-lock-trap)

**Research budget used: 10 of ~15 WebSearch queries.** Two claims remain **unverified** and
are marked as such in-line: Hi-Fi Rush's exact failed-Rhythm-Parry behaviour, and whether
Star Wars Jedi: Fallen Order's near-zero blade lock resolves automatically or on input.
Neither is load-bearing for the recommendation.

---

**Constraint check.** No GDD number is changed anywhere above: meter stays 0–100 with
+5 / +12 / +15 / +20 / +0, Phase 2 at 50 %, the Clash gate at meter 100 AND rival health
≤ 25 %, and a failed Clash at 1 HP floor / meter to 50 / 3 s cooldown. No fifth attack, no
second phase, no second arena, no deferred feature is proposed. Nothing here involves a
runtime AI-model call — Crimson Vanguard remains a deterministic authored Behavior Tree.
No other Q number is answered. **Q22 remains PROPOSED until the human designer decides it.**
