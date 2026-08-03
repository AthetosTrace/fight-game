# Group 06 — Final Clash and meter · Q9, Q17, Q19, Q20, Q21

**Dispatched:** 2026-08-02 · designer agent, group 06 of the open-question sweep.
**Consumes:** `gdd/INDEX.md`, `gdd/sections/02`, `gdd/sections/03`, `design-brief.md`
§13.1 rows 2–4 and 11–15, §13.2 rows 37 / 45 / 47–49, §14 "Final Clash" and "Structure",
`design/decisions.md` (**Q22 APPROVED**), `design/group-01-blocking-q22.md`,
`design/group-02-combat-economy.md`, `design/group-03-defensive-timing.md`,
`design/group-04-spacing-and-arena.md`.
**Produces:** answers to **Q9, Q17, Q19, Q20, Q21** only. No other Q number is answered
here; where the reasoning leans on another group's number it is named and cited as
theirs.

> **Status of every answer in this file: `PROPOSED` — the human designer decides.**
> **The one exception is Q17, which is `APPROVED` and KIND A** — a documented Unreal
> input-binding procedure exists and there was nothing to decide.

---

## Binding context — read this before any number below

### Q22 is APPROVED, and it changes what this group is

`design/decisions.md`, entry **2026-08-02 — Q22**, status **APPROVED** by the designer of
record:

> `MinHealthFloor = 1` on the rival's `BP_HealthComponent` from `BeginPlay`, lowered to
> `0` only by `ClashSuccess()` immediately before it applies lethal damage.

**Ordinary combat damage can never kill Crimson Vanguard. The Final Clash is the only way
to win the duel.**

`design-brief.md` §14 was written before that was settled. When §14 posed Q19, Q20 and
Q21 it was describing the tuning of an *optional climax*. It is now describing **the sole
exit from the game**. Group 03 put it plainly, and this group inherits it:

> *"Q20 and Q19 tolerances tighten because they become the sole exit."*

Three consequences run through every section below:

1. **Q20 is now the hardest gate in the game.** Two response windows stand between a
   player who has fought well for three minutes and any ending at all. Group 01's
   cautionary case — **Asura's Wrath**, where reviewers found the margin for error *"so
   slim as to be nonexistent"* on progression-gating timing beats — applies directly and
   was cited against exactly this question.
2. **Q19 is on the critical path.** If the post-counter acceptance window is too short,
   the player is repeatedly denied entry to the only ending they have.
3. **Q9 is not a flavour question.** Constraint **C1** attached to the Q22 approval reads:
   *"Q9 must resolve to no meter decay, or the tail can become a dead end."* Q9 is this
   group's, and C1 is binding on it.

### GDD numbers that bind this group — cited, never edited

From `gdd/sections/03-ascension-meter-final-clash-and-encounter-flow.md` (GDD v0.4,
PDF pp. 3–4) and `gdd/sections/02-real-time-combat-and-selectable-player-roster.md`
(PDF pp. 2–3):

| Value | Number | Where it is published |
|---|---|---|
| Meter range | **0–100**, *"earned only through active combat decisions… does not fill from waiting or elapsed time"* | §03 |
| Meter gains | **+5** combo finisher · **+12** perfect dodge · **+15** counter · **+20** Impact Window · **+0** damage/waiting | §03 |
| Clash gate | Meter **100** **AND** rival health **≤ 25 %**; *"if one condition is met first, the Clash remains locked until the other is met"* | §03 |
| Clash initiation | *"the player chooses to initiate the Clash with a contextual input **during neutral or after a successful counter**"* | §03 |
| Clash success | *"Complete **both** timing beats; the finishing sequence defeats Crimson Vanguard and ends the duel."* | §03 |
| Clash failure | *"**Separate both fighters**; preserve current health with Crimson Vanguard held at a **1 HP floor**; reduce meter to **50**; apply a **3-second** re-trigger cooldown."* | §03 |
| Failed-Clash recovery | *"does not restart the duel, kill the player automatically, or leave either fighter in a cinematic state. It creates a meaningful meter setback, restores valid combat states, and preserves a recoverable path to victory."* | §03 |
| First Impact Window response | **0.75 s** | §02 |
| Standard Impact Window response | **0.35–0.50 s** | §02 |
| Impact cinematic burst | **1–3 s** | §02 |
| Failure never auto-corrects | *"Failure does not auto-correct the input"* · *"The game does not press the input for the player and does not convert a miss into success."* | §02 |
| Target session | **3–5 minutes** | §01 |

**No answer below changes any of these.** Where an answer would have, it was discarded.

### Proposed values from other groups this file reasons against

All **PROPOSED**, none decided. If any moves, the arithmetic in **"The retry loop"** must
be re-run.

| Source | Value |
|---|---|
| Group 02 (Q1 / Q2) | Player health **100**; rival health **1200** |
| Group 02 (Q3) | Rival damage **A 32 · B 25 · C 27 · D 18** |
| Group 02 (Q4 / Q5) | Combo **3 sections ≈ 1.0 s**, total **20** damage, **+5** on the finisher |
| Group 02 | Rival cycle **≈ 2.9 s** Phase 1, **≈ 2.3 s** Phase 2; **≈ 0.7 combos per cycle**; gate at **≈ 2:53** competent, **≈ 4:29** scrappy |
| Group 03 (Q6 / Q7 / Q8) | i-frames **0.28 s**; perfect dodge **0.12 s**; counter whiff lockout **0.55 s** |
| Group 03 (Q26) | Impact cooldown **7.0 s**, first window exempt; effective **+18.7** per perfect dodge |
| Group 04 (Q10) | Range bands **A 0–260 · B 90–520 · C 240–420 · D 400–840 cm** |
| Group 04 (Q24) | Arena playable floor **2400 × 1600 cm**, diagonal ≈ **2884 cm** |
| Group 04 → this group | *"supports Q21 separation of 1000–1300 cm, 1300 the guaranteed ceiling, 1200 the comfortable value, pushed along the long axis rather than the fighters' facing"* |

### Framerate convention

Every frame count quoted from a shipped game is converted at **60 fps (1 frame ≈
16.7 ms)** unless the row states otherwise, and where a source's own basis is ambiguous
that is marked. **Every value proposed in this file is authored in seconds**, never in
frames — the Clash beats are driven by `Set Timer by Event` and `Anim Notify State`
durations on a montage timeline, both of which are wall-clock and framerate-independent
by construction. A frame-counted Clash window would change the game's only win condition
depending on the player's hardware.

---

## Q9 — Does the Ascension Meter decay?

- **Kind:** B (design) · **Status:** **PROPOSED** — but see the note below: **constraint
  C1 from the APPROVED Q22 decision already binds this answer**, so the designer's real
  choice is between confirming it and overturning C1.
- **Unblocks build step:** **M3-03**
- **Value lives in:** `BP_AscensionComponent` (`design-brief.md` §13.2 row 37)
- **GDD range:** **None published. The GDD is silent on decay.** What it does publish is
  the meter's definition, verbatim (`gdd/sections/03`, PDF p. 3):
  > *"Ascension Meter is a visible 0–100 resource earned only through active combat
  > decisions. **It does not fill from waiting or elapsed time.**"*

  and the **+0** row for *"Taking damage / waiting"*, whose stated design intent is
  *"Prevent passive progress."* `design-brief.md` §14 already recommends **no decay**.

### Proposed value

> **`MeterDecayRate = 0.0` — the Ascension Meter does not decay. Ever. Not in neutral,
> not in Phase 2, not during the post-Clash cooldown, not while the rival is pinned at
> the 1 HP floor.**
>
> Implement it as a **non-existent feature, not a variable set to zero.**
> `BP_AscensionComponent` should have **no `Tick`**, no timer, and no decay float. The
> meter changes in exactly six places: the five `AddMeter(E_MeterEvent)` call sites from
> `design-brief.md` §7, plus the one sanctioned direct set in `ClashFailure()` that
> reduces it to **50**. **If there is no clock touching the meter, decay cannot be
> reintroduced by a stray default value.**

### Why — and this is now a safety argument, not a taste argument

**1. C1 makes it binding.** The Q22 approval attached three constraints, and the first is:

> **C1 — Q9 must resolve to no meter decay.** Under (b) decay is the one thing that could
> turn a slow tail into a genuine dead end.

Q22 is APPROVED. C1 came with it. This group confirms C1 rather than re-litigating it.

**2. The GDD already solved the problem decay exists to solve, and solved it better.**
Every shipped decay mechanic found in research is an **anti-passivity** device (see prior
art). Our meter's anti-passivity device is already written into the GDD: **waiting pays
+0**, and the meter *"does not fill from waiting or elapsed time."* A player who does
nothing already makes no progress. **Decay would be a second anti-passivity mechanism
layered on a design that already has one** — and because the first one is airtight, the
only behaviour the second one can still reach is the player who *is* fighting and is
simply not very good at it. **Decay does not punish the turtle. It punishes the novice.**

**3. It is the reading most faithful to the GDD's own sentence.** *"It does not fill from
waiting or elapsed time"* establishes elapsed time as **not an input to the meter**.
Decay makes elapsed time an input, in the negative direction. That is a reading, not a
prohibition — the GDD nowhere forbids decay — and it is flagged as a reading. But it is
the reading that invents least, which is the correct default under the project's rule
that the human designer owns every number.

**4. Under Q22 the meter is a win requirement, so decay is a second failure state the
GDD never authored.** The GDD lists exactly one loss condition: *"selected fighter health
reaches zero."* A decay rate that outruns a struggling player's income does not merely
slow them down — it makes the win condition unreachable while the loss condition stays
live. That is a loss condition by another name, added by a number rather than by design.

### The arithmetic — what decay would actually cost, and where it dead-ends

Using group 02's and group 03's proposed economy. Meter income for a player relying only
on the offensive route (**+5** combo finisher, the smallest gain and the only one that
does not require a defensive read):

| Player | Combos per rival cycle | Phase 2 cycle | Seconds per **+5** | **Gross income** |
|---|---|---|---|---|
| Competent (group 02's figure) | 0.70 | 2.3 s | 3.29 s | **1.52 meter/s** |
| Scrappy | 0.50 | 2.3 s | 4.60 s | **1.09 meter/s** |
| **Struggling — the case that matters** | 0.35 | 2.3 s | 6.57 s | **0.76 meter/s** |

Now apply decay to the struggling player, who is the one Q22's tail actually strands, and
measure the **time to rebuild the 50 points a failed Clash costs**:

| `MeterDecayRate` | Net income | Time to rebuild **50** | Verdict |
|---|---|---|---|
| **0.0 — proposed** | 0.76 /s | **66 s** | Slow. Finite. Recoverable. |
| 0.25 /s | 0.51 /s | **98 s** | One retry costs 1:38. Two retries exceed the entire GDD session target on their own. |
| 0.50 /s | 0.26 /s | **192 s** | One retry costs **3:12**. The duel is now longer than the GDD's maximum session before the player has done anything wrong twice. |
| **0.76 /s** | **0.00 /s** | **∞** | **Hard dead end.** The meter never moves. Rival is pinned at 1 HP and cannot die. The only reachable outcome is the loss condition, arriving after an arbitrarily long unwinnable fight. |
| 1.00 /s | −0.24 /s | never | Dead end, and the bar visibly falls while the player is landing hits. |

**A decay rate as small as 0.76 points per second — three quarters of a point — converts
this game into an unwinnable state for a real, non-hypothetical player.** That is the
whole argument. Group 01 named the standard framing for this: a softlock is *"the
interaction of the game's systems"* producing a dead end *"even though all systems are
working as intended."* Decay plus the permanent 1 HP floor is exactly that interaction.

**Note the asymmetry that makes it dangerous.** The decay rate that is invisible to a
competent player (0.25/s costs them roughly 20 % of their rebuild) is the same rate that
doubles a struggling player's rebuild. **Decay is regressive by construction** — its cost
scales inversely with skill — and under Q22 the struggling player is already the one
spending longest in the tail.

### What would break if the designer chose decay anyway

Asked for explicitly, and answered as a checklist rather than an argument. If decay is
adopted, **all of the following must be re-opened, not just Q9:**

1. **Q22's C1 is violated.** The approved decision was accepted *with* C1 attached. Decay
   means Q22 must be re-decided, and reading **(a)** — damage can kill the rival —
   becomes the safe answer, because it restores a second win path that decay cannot close.
2. **Every meter estimate in groups 02, 03 and 06 is void.** Group 03 states it directly:
   *"All fill-rate arithmetic below is cumulative. If Q9 resolves to decay, re-run every
   meter estimate in this file."* That includes group 02's *"meter 100 arrives at
   0:40–1:25"*, group 03's *"5.4 perfect dodges to fill,"* and this file's retry loop.
3. **Q26 must drop.** Group 03: *"if decay were added, a 7 s cooldown becomes a punishing
   dead zone and this number must drop."* A 7-second gap between Impact Windows with a
   draining bar is a stretch of the fight where the player is losing ground for free.
4. **A floor would have to be invented.** The only safe form of decay is one that clamps
   above zero — e.g. it can never take the meter below the 50 a failed Clash leaves. That
   is a new rule, a new number, and a new GDD-adjacent invention this group is not
   proposing.
5. **The HUD promise from C2 breaks.** C2 requires the HUD to show *which gate is still
   locked.* With decay, the meter gate can lock and unlock repeatedly while the player
   watches, which reads as instability rather than information.
6. **`BP_AscensionComponent` gains a `Tick` or a repeating timer** — the one piece of
   per-frame work the combat framework currently does not need.

### Prior art (real games, named)

| Game | Mechanism | What it actually does | Why it does **not** transfer |
|---|---|---|---|
| **Guilty Gear** (Xrd / Strive, and the series generally) | **Negative Penalty** — the closest thing in fighting games to meter decay | Sustained passive play (backdashing, walking backwards, standing still) first shows a **"DANGER"** warning while the Tension Gauge *"will slowly drain,"* then **resets Tension to 0** and cuts all Tension gain — reported as **90 % reduced gain**, i.e. a **20 % fill rate, for 10 seconds**. Explicitly *"designed to discourage a purely non-interactive playstyle,"* and **keep-away is exempt if the player is using some form of offense** | It is **conditional on passivity, not on the clock.** It never fires against a player who is attacking. Our GDD's **+0 for waiting** already achieves the same outcome with no timer at all — and unlike Negative Penalty, ours cannot misfire on an aggressive player. **Guilty Gear is evidence for the GDD's existing rule, not for decay.** |
| **Devil May Cry 3 / 4 / 5** | **Stylish Rank meter**, the genre's canonical decaying combat resource | *"Style Point decreases when enemies are not attacked at a certain period,"* and *"the higher the current grade of Style, the faster the gauge will deplete"* — decay **accelerates at S-ranks** | **Style rank is a score, not a gate.** Nothing in DMC is unwinnable because the Style meter emptied. Under Q22 our meter *is* the win condition. Copying a scoring mechanic's decay onto a progression gate is the category error. Note also that DMC's decay is **fastest when the player is doing best** — the exact opposite of what our tail needs |

> **Marked as a gap.** No shipped game was found in this pass in which a **decaying
> resource is also the only win condition of a boss fight.** That absence is itself
> informative — the combination this group is being asked about does not appear to be
> something shipped action games do — but it is an absence, not a proof, and it is
> stated as one.

### Interaction with the rest

- **Q22 (APPROVED)** — C1. This answer exists to satisfy it.
- **Q26 (group 03, proposed 7.0 s)** — the 7-second Impact cooldown is only safe because
  nothing drains during it. The two answers are joined.
- **Q19 / Q20 / Q21 (this file)** — the entire retry loop below assumes cumulative meter.
  With decay, every figure in **"The retry loop"** must be recomputed.
- **Q23 (duel timer, another group, §14 recommends none)** — decay and a duel timer are
  the same idea in two costumes: both make elapsed time hostile. If the designer wants
  time pressure, **Q23 is the honest place to put it**, because a timer is visible and a
  decaying bar is not. This group does not propose either.
- **C2 (HUD gate indicator)** — reinforced. A meter that only ever rises is a bar the
  player can trust, which is what C2 needs it to be.

**This is a recommendation. The designer decides — but overturning it also overturns C1
and therefore reopens the APPROVED Q22.**

---

## Q17 — Do the Clash beats reuse `IA_Impact`?

- **Kind:** **A** (engineering) · **Status:** **APPROVED**
- **Unblocks build step:** **M1-10**
- **Value lives in:** `IMC_Duel` (`design-brief.md` §13.2 row 45)
- **GDD range:** none published, and none needed. The GDD requires only that the Clash is
  initiated *"with a contextual input"* and resolved by *"timing beats"* — it names no
  key and no action.

**This is KIND A and there is essentially nothing to decide.** Enhanced Input has a
documented procedure for making one action mean different things in different states, and
`design-brief.md` §14 already recommends reuse *"for learned consistency."* Keeping it
short accordingly.

### The answer

> **Yes. One `IA_Impact`, in the one `IMC_Duel`, used for the Impact Window prompt and for
> both Final Clash beats. No `IA_ClashBeat`. No second Input Mapping Context. No context
> swap during the Clash.**
>
> `BP_FinalClashDirector` and `BP_ImpactWindowDirector` both listen to the same action;
> a boolean on the Clash director (`bClashBeatOpen`) decides which one consumes it.
> `design-brief.md` §9.2 already specifies the surrounding behaviour — *"Disable Input on
> normal combat actions; leave `IA_Impact` live"* — so the Clash entry disables movement,
> attack, dodge and counter and leaves exactly one action bound. **During a Clash there is
> only one live input, so there is nothing for a second context to disambiguate.**

**Why not a second mapping context.** Enhanced Input's documented pattern for
state-dependent input is to push a higher-priority `InputMappingContext` at runtime: the
subsystem *"walks through all active contexts in priority order (highest first),"* the
first context with a binding for that key fires, and *"by default, fired actions consume
the input."* That is a real, supported solution — and it is the wrong tool here, because
it exists to make **one key produce different actions**. We want the opposite: **one
action, produced by the key the player has already learned, routed to a different
listener.** A pushed context would add an add/remove pair that must be leak-proof across
montage aborts, for no behavioural gain. `design-brief.md` §9.4 step 8 already forbids
leaving the player *"with input disabled"* after a failed Clash; every context we push is
another thing that can fail to pop.

**The learned-consistency argument, which is the design half of a mostly-engineering
answer.** The GDD's Impact Window is the player's *training* for the Clash: it is the same
shape (prompt, short window, press, cinematic burst), it fires first at a deliberately
wide **0.75 s** under the onboarding rule, and by the time the Clash is reachable the
player has hit it repeatedly. **Rebinding the finish to a different key would discard that
training at the single moment it matters most** — the sole exit from the duel under Q22.

### Two developer notes attached to this answer

1. **`BP_FinalClashDirector` must never consult `BP_ImpactWindowDirector`'s cooldown.**
   Carried forward verbatim from group 03. Shared *action*, separate *gating*. The Clash
   has its own double gate; the 7 s Impact cooldown must not be able to swallow a Clash
   beat.
2. **A beat must only accept a press that *begins after* the beat opens.** Bind on the
   `Started`/pressed trigger and ignore a key already held down when `OpenClashBeat(n)`
   fires. Without this, a player holding the button through the Clash entry montage passes
   beat 1 the instant it opens, and the same physical press could satisfy both beats —
   which would be the game *"convert[ing] a miss into success,"* forbidden by the GDD's
   onboarding rule and by *"Failure does not auto-correct the input."*

> **A small question for the designer, no value proposed.** Note 2 stops a *held* button
> from passing beats, but it does not stop **mashing**. Two beats at ~0.4 s each can be
> brute-forced by a player pressing four times a second, and the GDD says nothing about
> it. The options are: accept it (mashing is a legitimate QTE strategy and the beats are
> still *earned* because reaching them required the double gate); or fail a beat on a
> press that lands **before** it opens. **Failing on an early press is the stricter and
> more readable rule, and it is the one this group would ask about first** — but it adds a
> punishment the GDD never authored, so it is surfaced rather than proposed.

---

## Q19 — Post-counter Clash-initiation window

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M4-05**
- **Value lives in:** `BP_FinalClashDirector` (`design-brief.md` §13.2 row 47)
- **GDD range:** **None published.** The GDD publishes only the permission, verbatim
  (`gdd/sections/03`, PDF p. 3): *"Once eligible, the player chooses to initiate the Clash
  with a contextual input **during neutral or after a successful counter**."* It does not
  say how long "after" lasts. `design-brief.md` §14 offers **0.5–1.5 s**.

### Proposed value

> **`PostCounterClashWindow = 1.2 s`**, opening the instant a counter is scored — i.e.
> the same event that fires the **+15** — and running for 1.2 s.
> Tuning band: **1.0–1.3 s**. **Do not go above 1.30 s** (derivation below).
>
> **The window closes early** on any of: the player pressing light attack, dodge or
> counter; the player taking damage; the player successfully initiating the Clash. It does
> **not** close when the player reaches neutral, because neutral is independently eligible
> and the two permissions simply overlap from that point.

### What this window is actually for — the structural point first

Read the GDD's sentence carefully. **Neutral is already an eligible state, and neutral is
unbounded** — an eligible player can stand still and press the input whenever they like.
So the post-counter clause **cannot be about giving the player more time**; they already
have infinite time in neutral. It is about giving them the Clash from a state that is
**not** neutral: the recovery of a counter they have just landed.

That yields a falsifiable requirement:

> **Q19 must be longer than the time it takes a successful counter to return the player to
> neutral. Otherwise the post-counter clause is dead code** — the window expires, the
> player becomes neutral-eligible a moment later, and the GDD's sentence bought nothing.

**And this is where Q19 hits a hole in the value table.** Group 03 found that
`design-brief.md` §13.2 *"lists no row for the counter's success window"* and no row for
the counter's success montage length either — only the **0.55 s whiff** (Q8). **Nobody has
proposed how long `AM_Player_Counter` takes to return control on success.** If it returns
control in ~0.5 s, then §14's lower bound of **0.5 s is exactly a no-op**, and even 0.75 s
buys only a quarter-second of extra permission.

> **Question for the designer, flagged as a dependency, no value proposed:** how long is
> the successful-counter recovery? Whatever it is, **Q19 should be authored as
> `CounterRecoveryLength + 0.6 s`, not as a bare constant**, so the two cannot drift apart
> in tuning. 1.2 s is the value that expression produces at a ~0.6 s counter recovery,
> which is the assumption used throughout this file and is **an assumption, not a number
> anyone has decided.**

### Why 1.2 s, and why 1.5 s is unsafe — the arithmetic

The upper bound is set by the rival, not by the player. After the player counters, the
rival is in **Recover**, and the earliest its next strike can land is the sum of the
remaining states at their **fastest legal GDD values**:

| State | Phase 1 floor | Phase 2 floor |
|---|---|---|
| Recover | 0.45 s | 0.35 s |
| Return to Neutral | 0.10 s | 0.10 s |
| Idle / Reposition | 0.60 s | 0.35 s |
| Select Attack | 0.10 s | 0.10 s |
| Telegraph | 0.55 s | 0.40 s |
| **Earliest next strike, from the counter** | **1.80 s** | **1.30 s** |

*(All six values are GDD-published ranges, `gdd/sections/04`, PDF p. 5, reproduced in
`design-brief.md` §13.1 rows 17–25. The floors are used because they are the worst case
for this question.)*

> **1.30 s is the hard ceiling.** At 1.2 s the post-counter window closes **0.10 s before
> the fastest legal Phase 2 attack can connect.** The Clash therefore always launches from
> a moment when the player is not under threat.
>
> **§14's own upper bound of 1.5 s exceeds that ceiling by 0.20 s.** At 1.5 s a player can
> legally initiate the Final Clash *while a Phase 2 strike is landing on them* — turning
> the game's win condition into an invulnerability button and an escape from a read they
> failed. **That is a finding against §14's stated range, and it is the reason this
> group's band tops out at 1.3 s rather than 1.5 s.** The designer may want that escape;
> it is a legitimate choice; it should be chosen deliberately, not inherited from a range.

**Why not the bottom of the band.** Under Q22 this window is on the critical path to the
only ending in the game. Group 01: *"Too short and the player is repeatedly denied the
only exit."* At 0.5 s the window is plausibly shorter than the counter recovery itself and
does nothing; at 0.75 s it demands the player recognise "counter landed → I am eligible →
press a different button" inside three quarters of a second, when the average human visual
reaction time group 03 measured against is **~250 ms** and this is a *decision*, not a
reflex. **1.2 s leaves roughly a second of thinking time after recognition.** That is the
right side of the trade when the cost of missing is a lap of the rebuild loop.

### Prior art (real games, named) — and an honest gap

**This is the weakest-sourced answer in this file and the designer should know it.** Four
searches were spent looking for a published duration on a contextual follow-up prompt in a
shipped action game. **None produced a number.** What they produced was a consistent
qualitative pattern, which is worth something but is not a measurement.

| Game | Mechanism | What is actually published | Relevance |
|---|---|---|---|
| **Sekiro: Shadows Die Twice** | Deathblow prompt after a Posture break — the closest structural analogue: a finisher offered for a limited time out of a state the player earned | *"If the player doesn't execute the deathblow within **a few seconds** after breaking an enemy's posture, the enemy will recover a small portion of their posture and the fight will continue,"* and *"you'll only have a small window of time to pull this off while they're staggered."* **No frame or second count published.** | The pattern: the window is short enough to feel urgent, long enough that a player who *sees* the prompt can act on it, and **failing it costs progress, not the run.** Our failed-window cost is even gentler — the player simply waits for neutral. |
| **God of War Ragnarök** | Stun Grab prompt after the Stun Bar fills | The enemy is *"unable to move, leaving it vulnerable for **a few seconds**."* Crucially, **the duration is upgradeable** — *"to increase your duration of Stun, you will have to upgrade your Leviathan Axe and Blades of Chaos."* **No base duration published.** | The upgrade path is the useful detail: a shipped studio treats a contextual-prompt duration as a **tuning surface players are allowed to feel**, not a fixed constant. Reinforces that Q19 is a playtest number. |
| **Bloodborne** | Visceral Attack window after a parry | Sources describe a *"window"* in which a follow-up deals double damage, and note the follow-up speed differs by firearm — Ludwig's Rifle is the slowest, Hunter Blunderbuss and Rifle Spear faster. **NOT FOUND: no duration in seconds or frames.** | Cited only for the shape — a reward window opened by a defensive read — and for the observation that **the animation you are recovering from determines whether the window is usable at all.** That is exactly the `CounterRecoveryLength` dependency above. |
| **Batman: Arkham** series | Combo meter timer — a contextual state that expires if not renewed | *"The timer is not visible and runs out in seconds,"* and if the player fails to act *"the combo indicator will go back to zero."* **NOT FOUND: no duration published in any source reached.** | Cited as a **warning, not a model.** An invisible expiring window is the standard complaint about Arkham's combo system. **Whatever Q19 resolves to, `WBP_HUD` must show it** — see below. |

> **Marked NOT FOUND.** No shipped action game reached in this pass publishes a numeric
> contextual-prompt acceptance window. Four independent sources describe theirs as *"a few
> seconds."* **1.2 s is at the low end of any reasonable reading of "a few seconds," and
> it is derived from our own GDD state ranges rather than from any of them.** Treat the
> prior art as corroborating the *shape* of the answer and not its magnitude.

### A HUD requirement that falls out of this

The Arkham row is the lesson. **A window the player cannot see is a window they will
believe is broken.** Constraint **C2** from the Q22 approval already requires `WBP_HUD` to
show which gate is locked, and group 03 already requires an Impact-readiness indicator in
**M3**. When both gates are open, the Clash prompt should be **visible in neutral and
visibly emphasised during the post-counter window** — one more state on a widget that
already exists, in M3/M4, not a new feature and not M5 work. **The styled treatment is
M5.**

### Interaction with the rest

- **Q22 (APPROVED)** — puts this window on the critical path. It is the reason the band
  sits at the generous end.
- **Q8 = 0.55 s (group 03)** — group 03 already flagged the link in the other direction:
  *"a successful counter is also the entry to the ending. That raises the value of the
  counter above its +15 and argues for keeping Q8 at the assertive end of its band."*
  Q19 and Q8 together are what a counter is worth and what it costs. **Confirmed from this
  side.**
- **The counter's success window and success-recovery length** — no Q number, no row, no
  proposal anywhere. **Q19 cannot be locked before they exist.** Group 03 already flagged
  the first as a §13.2 table defect; this group adds the second.
- **Q17 (this file)** — different input. The Clash *initiation* is `IA_FinalClash`
  (`design-brief.md` §9.1); the Clash *beats* are `IA_Impact`. Q19 governs the first, Q20
  the second. **The developer must not merge them:** a player mashing `IA_Impact` for the
  Impact Window must never accidentally start the Final Clash.
- **Q26 = 7.0 s (group 03)** — a successful counter may *also* open an Impact Window. If
  both fire on the same event, the Impact prompt and the Clash permission overlap for
  0.35–0.50 s. **`BP_FinalClashDirector` must not consult the Impact cooldown**, but the
  developer does need to decide what happens if the player presses `IA_FinalClash` while
  an Impact prompt is on screen. **The safe rule: the Impact Window resolves first, and
  the post-counter Clash window is paused, not consumed, for the duration of the Impact
  burst** — otherwise the game's biggest reward silently eats its only exit. **Surfaced
  as a developer/designer question; no timing value proposed.**

**This is a recommendation. The designer decides.**

---

## Q20 — Clash beat 1 and beat 2 response times

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M4-06**
- **Value lives in:** `BP_FinalClashDirector` (`design-brief.md` §13.2 row 48)
- **GDD range:** **None published for the Clash beats.** The GDD publishes response times
  only for Impact Windows (`gdd/sections/02`, PDF p. 3): **First Impact Window 0.75 s**,
  **Standard Impact Window 0.35–0.50 s**, with a **1–3 second** cinematic burst on
  success. It publishes for the Clash only that success requires *"complet[ing] both
  timing beats."* `design-brief.md` §14 asks the question directly: *"reuse
  `StandardWindowDuration` (0.35–0.50 s) for both, or author them separately — perhaps
  beat 2 tighter than beat 1 to make the finish feel like a real test?"*

### Proposed value

> **Both beats = 0.50 s. Identical. `ClashBeatDuration = 0.50`, one value, used twice.**
> That is **the top of the GDD's published Standard Impact Window range (0.35–0.50 s)**,
> so no number is invented — the Clash reuses a range the GDD already published and takes
> its most generous end.
> Tuning band: **0.45–0.60 s**, and **the band's floor is 0.45, not 0.35.**
>
> **Explicitly recommended against: making beat 2 tighter than beat 1.** §14 raised it as
> an option and this group is arguing the other way. Reasons below.
>
> Each beat's window is measured from the instant `OpenClashBeat(n)` fires the prompt, not
> from the start of the Clash montage.

### Why identical, and why not escalating — this is the load-bearing part

**1. §14's question was written before Q22 was approved, and Q22 inverts the answer.**
"Make the finish feel like a real test" is a good instinct for an *optional* climax. Under
the APPROVED Q22 the Clash is not the climax on top of a win — **it is the win.** A
tighter beat 2 does not make the finish feel like a test; it makes the game's only exit
harder than any other input in it, at the moment the player has the least composure. Group
01 cited **Asura's Wrath** against precisely this: a game whose progression sat behind
authored timing beats, where reviewers found *"the margin for error … is so slim as to be
nonexistent,"* and criticised the *"terrible implementation and gated content"* around an
otherwise well-liked counter-based combat system. **We now have Asura's Wrath's structure.
We must not take its tuning.**

**2. Escalating tightness makes the more expensive failure the more likely one.** Failing
beat 2 costs strictly more than failing beat 1 — the player has already spent the beat-1
montage, the beat-1 window, and the beat-2 lead-in before the failure lands, and the
setback is the same **meter to 50** either way. Estimated from the GDD's **1–3 s** burst
length:

| Where the Clash fails | Cinematic time spent before the player is back in combat | Setback |
|---|---|---|
| Beat 1 | entry montage + 0.50 s window + separation ≈ **2.5–3.0 s** | meter 100 → 50 |
| Beat 2 | the above + beat-2 montage + 0.50 s window ≈ **4.0–5.0 s** | meter 100 → 50 |

*(Both figures are **derived estimates** from the GDD's 1–3 s burst range and the proposed
0.50 s windows. **The Clash montage lengths themselves have no GDD number, no §13.2 row
and no Q number** — see the flagged gap below.)*

**A tighter beat 2 therefore charges more for the same setback, more often.** That is a
double penalty produced by a tuning choice, not by a design decision anyone made.

**3. It would discard the training the whole design spent the duel building.** Q17's
answer keeps the Clash on `IA_Impact` precisely so the player arrives fluent. The GDD's
Impact Window is the rehearsal: same prompt shape, same button, and a published window of
**0.35–0.50 s** repeated all duel. **Two beats at 0.50 s are the rehearsal, twice, at its
most forgiving setting.** A beat 2 at 0.35 s is a new, harder, unrehearsed input
introduced at the last possible moment.

**4. The GDD escalates by phase, never within an authored sequence.** Its one escalation
mechanism is **Phase 2 at 50 % health**, which re-times the *same four attacks*. Nowhere
does the GDD tighten a window inside a single authored beat sequence. **Escalating beat 2
would be a new kind of difficulty curve, and inventing one is outside what this group may
do.**

**5. It is one value, one variable, one edit.** `ClashBeatDuration` as a single float means
the designer retunes the ending in one place after a playtest. Two floats invite a drift
between them that nobody notices until a player cannot finish the game.

### Why 0.50 s and not 0.35 s

- **0.50 s is inside a GDD-published range**, so the answer invents nothing. Going below
  it would still be inside the range but would be choosing the *tight* end of a range the
  GDD wrote for a **repeatable** prompt that fires many times a duel and whose failure
  costs *"no extension; return to combat."* Our beat's failure costs 50 meter and a lap of
  the rebuild loop. **Same window, wildly different stakes — so take the generous end.**
- **Reaction time.** Group 03's reaction check uses an average human visual reaction time
  of **~250 ms**. A 0.50 s window leaves roughly 250 ms of margin after an average
  reaction; a 0.35 s window leaves ~100 ms, which is inside normal human variance. **At
  0.35 s a player of average reflexes fails the game's only exit on a bad day.**
- **The floor of the tuning band is 0.45 s, not 0.35 s**, for the same reason. If the
  designer wants the Clash tighter than the Impact Windows the player trained on, that
  should be a deliberate statement, not a slide down a range.

### An option the designer may want, with GDD precedent — not proposed, surfaced

The GDD has an authored, non-adaptive precedent for widening a window the first time a
player meets it: the **First Impact Window at 0.75 s** versus the standard **0.35–0.50 s**,
under the **PRESERVED — ONBOARDING RULE**. Group 03 called that *"the sanctioned pattern."*

> **The designer could apply the same pattern to the Clash: the very first Clash attempt
> of a duel uses 0.75 s, every subsequent attempt uses 0.50 s.** Both numbers are already
> GDD-published; nothing is invented; it is a one-shot flag (`bFirstClashAttempted`),
> structurally identical to `bFirstWindowConsumed`.

**This is the opposite of forgiveness-on-retry and must not be confused with it.** It is
**widest first and never widens again** — it cannot watch the player, cannot react to
failure, and cannot adapt. A window that *widened after failures* would be adaptive
difficulty, is **deferred future scope**, and **is not proposed anywhere in this file.**

**Surfaced, not proposed**, because it adds a rule the GDD states for Impact Windows and
does not state for the Clash. The designer decides whether the precedent carries.

### A gap this group found — the Clash beats have no lead-in specification

The response window is only half of what makes a beat fair. **The other half is the
anticipation the montage gives before the prompt opens** — the Clash's equivalent of the
rival's Telegraph state, which the GDD spends a whole readability section on for ordinary
attacks and says nothing about for the Clash.

> **Question for the designer, no value proposed.** How much readable wind-up precedes
> each Clash prompt, and does beat 2's lead-in differ from beat 1's? A window of 0.50 s
> arriving with no warning is materially harder than the same window arriving after a
> visible commit. **`AM_Clash_Beat1` / `AM_Clash_Beat2` lengths, and the notify position
> at which each prompt opens, have no GDD number, no `design-brief.md` §13.2 row and no Q
> number.** The only constraint that exists is the GDD's **1–3 s** burst length. **Flagged
> as a table gap, not resolved here.**

### Framerate — and a real shipped game that got this wrong

Every value here is authored in **seconds**, on a wall-clock timer, never in frames.
**Resident Evil 4 is the cautionary case and it is unusually literal.** When RE4 was
brought to 60 fps, *"the 60 fps conversion affected the engine logic of the game, including
QTE timing,"* and *"the rate at which you need to button mash QTEs nearly doubled … because
Resident Evil 4 was never intended to run at 60 fps."* Ascendant Impact is a PC title with
no locked framerate. **A frame-counted Clash beat would make the game's only win condition
harder or easier depending on the player's hardware.** `Set Timer by Event` and
`Anim Notify State` durations are time-based and are the correct implementation.

### Prior art (real games, named)

| Game | Mechanism | Real numbers / published behaviour | What it says about Q20 |
|---|---|---|---|
| **Hi-Fi Rush** | **Two sets of Rhythm Parries at the end of a boss's health** — structurally the closest published match to our two beats | Mimosa *"will perform two sets of Rhythm Parries at the end of her health, and they must be performed to the threshold to end the boss fight."* On failure — *"if not completed to the threshold, the enemy will either attempt another after dealing damage, or lose its enraged state."* On success a special Beat Hit *"can be performed to destroy the enemy in one hit,"* and even if that is ignored *"the enemy will still be stunned long enough to allow a counterattack"* | **This closes the claim group 01 had to mark unverified.** A failed set does **not** end the run: the player takes damage and the boss offers the sequence again. **That is our failed-Clash recovery rule, shipped.** It also shows a shipped multi-beat finisher whose two sets are the *same* difficulty, not escalating. **No frame data for the parry window was found in this pass or in group 03's** |
| **Final Fantasy XVI** | Cinematic Clash / cinematic techniques — a modern AAA answer to the same problem | *"The window to enact these prompts are forgiving, so players don't have to stress about failure."* For the Cinematic Clash specifically: *"cinematic clashes don't fail … even if you miss the timing window, the clash will still succeed."* Design philosophy: *"Final Fantasy XVI doesn't require players to press a series of buttons. All cinematic techniques rely on one button press or mashing a single button"* | **Two lessons, one of which we must refuse.** Take the input philosophy — **one button** — which is exactly Q17's answer. **Refuse the auto-success:** our GDD is explicit that *"Failure does not auto-correct the input"* and *"does not convert a miss into success."* But note what FFXVI's choice implies: a 2023 AAA studio concluded that a *failable* cinematic clash was not worth the cost. **Since we cannot take their escape hatch, we should sit at the generous end of our own published band.** This is the single strongest argument for 0.50 s over 0.35 s |
| **Resident Evil 4** (2005) | The genre's reference QTE, and the reference complaint | On Professional mode QTEs have *"a very brief button window,"* and for dodge prompts *"you have like one second to push the required button combination."* The 60 fps ports *"nearly doubled"* the required mash rate because timing was tied to engine logic | Two things: **~1 s is the community's felt figure for a QTE dodge prompt on the game's hardest setting** — which puts our 0.50 s at half of a famously unforgiving benchmark; and the **framerate lesson above**. **NOT FOUND: no frame count for the RE4 input window in any source reached** |
| **Metal Gear Rising: Revengeance** | Health-floor-plus-QTE bosses, cited by group 01 | Monsoon: *"once the boss's health bar drops below 10 %, a QTE will start, in which Raiden will deal with Monsoon after the correct buttons are pressed."* Sundowner: *"once its health bar drops to 10 %, the usual QTE sequence will start"* | Structurally near-identical to our gate, but **auto-triggered and single-gated on health**. The player is never asked to bring a second resource. **The comparison is the warning: we ask for more than MGR does before the beats even open, so the beats themselves should ask for less** |
| **Asura's Wrath** | The cautionary case, cited by group 01 against exactly this question | *"Correct inputs when prompted will advance the story while failure can cause the restart of a sequence and damage to health,"* with criticism of *"terrible implementation and gated content"* and boss fights where *"the margin for error … is so slim as to be nonexistent"* | The failure mode of a tight beat 2 under Q22, named in advance |

> **Marked NOT FOUND.** **No shipped game reached in this pass publishes a numeric QTE
> input window.** Four separate searches across RE4, FFXVI, Hi-Fi Rush and God of War
> returned qualitative descriptions only — *"forgiving," "a very brief button window,"
> "like one second," "a few seconds."* **0.50 s is therefore derived from the GDD's own
> published Standard Impact Window range, not from prior art.** The prior art establishes
> the *direction* (modern games make cinematic prompts generous, and the famous failures
> are the tight ones) and not the value.

### Interaction with the rest

- **Q22 (APPROVED)** — the reason this answer sits at the generous end. Under reading (a)
  a tighter beat 2 would have been defensible because a failing player had another way out.
  **They no longer do.**
- **Q17 (this file)** — same button, same prompt widget, same learned feel. Q20's identical
  windows are what make that training transfer.
- **Q26 = 7.0 s (group 03)** — group 03: *"the Final Clash must not be cooldown-gated …
  `BP_FinalClashDirector` must not consult `BP_ImpactWindowDirector`'s cooldown."*
  Re-stated here because Q20 shares that director's window machinery and it is the obvious
  place for the bug to enter.
- **Q19 (this file)** — Q19 gets the player *to* the beats; Q20 decides whether they get
  through them. Both were tightened in tolerance by Q22 and both are answered toward
  generosity for the same reason.
- **Q9 (this file)** — with no decay, a failed Clash is a fixed 50-point setback rather
  than a compounding one. **Q20's generosity and Q9's no-decay are the two things keeping
  the endgame recoverable**; if either is reversed the other must be reconsidered.
- **The retry loop** — Q20 is the single biggest lever on how many times the loop runs.
  See the verdict below.

**This is a recommendation. The designer decides. Of the five answers in this file, this
is the one with the greatest consequence for whether the game can be finished at all.**

---

## Q21 — Failed-Clash separation distance

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M4-08**
- **Value lives in:** `BP_FinalClashDirector` (`design-brief.md` §13.2 row 49)
- **GDD range:** **None published.** The GDD publishes the instruction and not the
  distance (`gdd/sections/03`, PDF p. 3, Failure row): *"**Separate both fighters**;
  preserve current health…"* `design-brief.md` §14 gives the requirement instead of a
  number: *"Must place both fighters outside every attack's `MinRange` (Q10) so the player
  is not immediately re-engaged while recovering."* **Group 04 has already supported a
  value from the arena side:** *"supports Q21 separation of 1000–1300 cm, 1300 the
  guaranteed ceiling, 1200 the comfortable value, pushed along the long axis rather than
  the fighters' facing."*

### Proposed value

> **`FailedClashSeparation = 1200 cm`, centre-to-centre, measured and applied **along the
> arena's long axis**, not along the fighters' facing.** Tuning band: **1100–1300 cm** —
> **group 04's band with its floor raised**, for the reason in the arithmetic below.
>
> **Placement rule:** take the midpoint of the two fighters at the moment of failure, push
> each **600 cm** along the long axis in the direction they were already nearer, clamp each
> to the playable footprint with a wall margin, and **give any clamped remainder to the
> other fighter so the total separation stays 1200 cm.**
>
> **Never swap sides.** If the push direction would put the player past the rival, keep
> each on the side of the midpoint they started on. A separation that mirrors the fighters
> reads as a teleport, and the GDD's hard rule for attack D — *"no hidden full-arena
> snap"* — is the same readability principle.

**The clamp always succeeds, and here is the proof.** Group 04's playable floor is
**2400 × 1600 cm** with the long axis on the doorway axis. Two points 1200 cm apart placed
on a 2400 cm segment leave **1200 cm of slack** to distribute between the two ends. So no
matter where in the arena the Clash failed — including with a fighter pressed against an
end wall — the redistribution rule can always deliver the full 1200 cm without either
fighter leaving the floor. **1200 cm is exactly half the long axis, which is why it is the
comfortable value and why group 04 called 1300 the guaranteed ceiling** — above about
1300 cm the wall margin starts eating the redistribution slack, and the separation the
code delivers stops matching the number the designer typed.

### The `MinRange` test is trivially passed and is not the real constraint

§14 states the requirement as *"outside every attack's `MinRange`."* Against group 04's
Q10 bands:

| Attack | `MinRange` | `MaxRange` | 1200 cm vs `MinRange` |
|---|---|---|---|
| A | 0 cm | 260 cm | outside by 1200 cm |
| **B — the largest `MinRange`** | **90 cm** | 520 cm | **outside by 1110 cm — 13.3× the value** |
| C | 240 cm | 420 cm | outside by 960 cm |
| D | 400 cm | **840 cm — the largest `MaxRange`** | outside by 800 cm |

**Any separation above 90 cm satisfies §14's stated requirement, so the requirement as
written does not constrain the answer at all.** `MinRange` is the *inner* edge of a band —
the distance below which an attack is too close to use. What actually determines whether
the player is "immediately re-engaged" is the **outer** edge: **1200 cm must sit far enough
beyond the largest `MaxRange` (D at 840 cm) that closing the gap takes real time.** That is
the test this answer is built on, and it is worked in **"Q21 against Q10"** below.

### Why 1200 and not 1000 — the arithmetic in brief

Full working is in the closing section. The short version, at the **fastest legal Phase 2
values** and using the player's proposed **600 uu/s** as a stand-in for the rival's
unspecified walk speed:

| Separation | Gap past D's 840 cm | Reposition cycles to reach D's band | **Time to the first legal telegraph** |
|---|---|---|---|
| 1000 cm | 160 cm | 1 | **≈ 0.85 s** |
| **1200 cm — proposed** | **360 cm** | **2** | **≈ 1.20 s** |
| 1300 cm | 460 cm | 3 | ≈ 1.55 s |

**0.85 s is not enough.** The player has just come out of a camera cut, a failed cinematic
and a teleport, and is reorienting. Group 03's reaction-time work puts average human visual
reaction at **~250 ms**; 0.85 s leaves roughly two reaction times to notice where the rival
is, re-acquire lock-on, and read a telegraph. **1.20 s is the smallest value in group 04's
band that buys two full reposition cycles**, which is the difference between "the rival is
walking back to me" and "the rival is already winding up."

**Why not more than 1300 cm.** Beyond the clamp problem above, the rival walking a long way
back across an empty floor is dead time in a duel with a 3–5 minute target, and it makes
the failed Clash feel like a scene change rather than a setback. **The GDD's own word is
"separate," not "reset."**

### Two checks that pass, worth recording

- **Lock-on survives.** Group 04's Q11 proposes lock-on acquire at **3000 cm** and break at
  **3300 cm**, both beyond the arena's 2884 cm diagonal. **At 1200 cm the player's lock-on
  is never broken by the separation**, so the camera does not have to re-acquire and the
  player is not disoriented. This is the single strongest practical argument for keeping
  the separation well under the break range.
- **Attack D cannot cover it in one move.** Group 04's Q13 gives D a `MaxTravelDistance` of
  **600 cm**, finishing 240 cm from the target. From 1200 cm, even if D were selectable —
  it is not, since 1200 > D's 840 cm `MaxRange` — a single D would leave the rival at
  600 cm. **No single rival action closes the separation**, which is exactly what "not
  immediately re-engaged" has to mean.

### Implementation — the Unreal-side handholds

`design-brief.md` §9.4 step 2 already specifies *"`Set Actor Location` on each, pushed
apart along the axis between them, then `Set Actor Rotation` to face each other."* Four
corrections and additions, all engineering rather than design:

1. **Push along the long axis, not "the axis between them."** Group 04's finding. The
   fighters' facing axis can be diagonal or short-axis aligned, where only 1600 cm is
   available and group 04's four **250 cm 45° chamfers** cut the corners. **The long axis
   is the only direction where 1200 cm always fits.** Read it from
   `DA_TuningGlobals.ArenaLongAxisCm` — group 04 stored it there specifically so this kind
   of derived value cannot drift from the level.
2. **`Set Actor Location` with `Teleport = true`, not with sweep.** Unreal's own
   documentation and community reports note that using sweep in `SetActorLocation` can make
   characters *"stop"* on geometry. A swept move that stops short would silently deliver a
   separation smaller than the design says, and nothing would report it. **A teleport that
   is fully hidden by the camera cut is correct here; a sweep that half-works is not.**
3. **Project the rival's target onto the NavMesh first.** `ProjectPointToNavigation`
   *"projects a point to navigation, taking parameters like the point, output location,
   extent, agent properties, and query filter"* and is the documented way to *"safely
   position AI characters on valid navigation mesh points."* The rival's Behavior Tree
   re-enters `BTTask_Idle_Reposition` immediately after the separation (§9.4 step 7); if it
   lands off the NavMesh, that task fails on the first tick and the rival stands still —
   which under Q22 is a duel that cannot end. **The projection extent is an engineering
   value, not a design one, and is not proposed here.**
4. **Order the separation before the camera returns.** §9.4 step 1 stops `LS_FinalClash`
   and returns the camera to gameplay; step 2 separates. **Do step 2 first, or on the same
   frame.** Applied under the cut, a 1200 cm teleport is invisible; applied after the
   blend, it is a pop — and §9.4 step 8 forbids leaving either fighter in a state the
   player can read as broken.

> **A dependency this group cannot close, and it is the serious one.** **The rival's
> `MaxWalkSpeed` is unspecified** — group 04 raised it as TODO item 49 and called it
> serious for a different reason: *"under the approved Q22 a rival slower than the player
> can be kited forever and the duel cannot end."* **Q21 is the other half of that vice.**
> A fast rival makes 1200 cm evaporate and the separation stops meaning anything; a slow
> rival makes the duel unendable. **Q21 cannot be validated until the rival's walk speed
> exists**, and the two should be tuned in the same session. Every timing figure in this
> section assumes **600 uu/s** — group 05's proposed *player* speed, used as a placeholder
> and **not a proposal for the rival.**

### Prior art (real games, named) — and an honest gap

| Game | Mechanism | What is published | Relevance |
|---|---|---|---|
| **Tekken 8** | Combo enders that control post-combo spacing | Community discussion of combo enders notes that some *"allow you to avoid sending your opponent 10 meters away,"* implying a standard launcher can produce roughly **10 m ≈ 1000 cm** of separation. **Marked UNVERIFIED** — a loose community figure, not frame data or an official measurement | Cited for one reason only: **1000 cm is a real, shipped, felt separation in a 1v1 fighter**, and group 04's Q21 band starts there. It is weak corroboration that a four-figure centimetre separation is not absurd in a duel. Group 04 also derived its arena footprint partly from Tekken's published stage sizes (24×24 standard, 16×24 *Midnight Siege*), so the two are consistent |
| **Hi-Fi Rush** | Failed finisher sequence → fight resumes | On a failed Rhythm Parry set *"the enemy will either attempt another after dealing damage, or lose its enraged state"* | Not a distance, but the right **shape** for the moment after: the boss is still there, still in a valid combat state, and the exchange resumes. **No repositioning is reported at all** — which is worth noting, since our GDD explicitly asks for separation and Hi-Fi Rush apparently does not need it |

> **Marked NOT FOUND, and stated as a real gap.** **No shipped game reached in this pass
> publishes a knockback or post-cinematic separation distance in world units.** The general
> sources describe knockback qualitatively — *"a short distance (perhaps one or two
> steps)"* at the low end, up to being *"knocked back a significant distance"* where the
> player *"is unable to control them until the character comes to a stop"* — and note it is
> used *"for creating space."* That is the correct *intent* for our failed Clash and it is
> all the prior art supports. **1200 cm is derived from group 04's arena footprint and
> group 04's Q10 bands, not from any shipped game.** Group 04 hit the same wall and
> recorded it the same way.

### Interaction with the rest

- **Q10 / Q13 / Q24 / Q11 (group 04)** — every check above is against their numbers. **If
  any of the four moves, re-run this section.** In particular, if D's `MaxRange` rises
  above 840 cm the separation must rise with it.
- **Q22 (APPROVED)** — group 01: *"Under (b) the player must survive and rebuild after
  every failure, so being re-engaged instantly is more punishing."* That is why the band's
  floor is raised from 1000 to 1100.
- **Q9 (this file)** — with no decay, the ~1.2 s of enforced non-combat after separation
  costs the player nothing. **With decay it would be a period of guaranteed loss the player
  cannot act against**, which is one more reason C1 is right.
- **The GDD's 3-second re-trigger cooldown** — the separation and the cooldown overlap.
  See the retry loop below: the cooldown turns out never to be the binding constraint.
- **Group 04's required advance rule** — group 04 closed the 840–2884 cm zero-coverage
  region *"by a required advance rule rather than by accident."* **Q21 puts the rival in
  that region on purpose, once per failed Clash.** So the failed Clash is the routine test
  case for that rule, and it must be exercised in M4 rather than discovered in a playtest.

**This is a recommendation. The designer decides.**

---

## The retry loop

**Under the APPROVED Q22 the retry loop is the whole endgame.** Every duel that is not a
loss ends by completing two timing beats, and every failed attempt puts the player back at
meter 50 with the rival pinned. This section models it, because nobody has yet.

**All inputs are PROPOSED values from other groups.** If any moves, this arithmetic moves.

### What one retry costs — the four components

| # | Component | Duration | Notes |
|---|---|---|---|
| 1 | Failed Clash cinematic | **≈ 2.5–3.0 s** failing at beat 1 · **≈ 4.0–5.0 s** failing at beat 2 | **Derived estimate**, from the GDD's **1–3 s** burst length plus two 0.50 s windows. The Clash montage lengths have no GDD number and no Q number |
| 2 | Re-approach after the 1200 cm separation | **≈ 1.2 s** of guaranteed non-combat | Worked in **"Q21 against Q10"** below |
| 3 | GDD 3-second re-trigger cooldown | **3.0 s**, **concurrent with components 2 and 4** | **Never binding — see below** |
| 4 | Rebuilding meter **50 → 100** | **≈ 14 s to ≈ 66 s**, depending entirely on skill | The dominant term by a wide margin |

### Component 3 is not a real constraint, and this is worth stating once

The GDD's 3-second cooldown runs from the moment of failure. The **fastest** meter rebuild
found anywhere in the model below is **13.8 s**. **The cooldown expires 4.6× sooner than
the fastest possible player can be eligible again**, and the player leaves the Clash at
meter 50 in any case, so the meter gate is already closed for far longer than 3 seconds.

> **The 3-second cooldown never gates anything in practice.** It exists to make an instant
> re-trigger structurally impossible, and it succeeds at that. **It is a GDD-fixed number,
> it must be implemented exactly as written, and nobody should spend tuning time on it.**

### Component 4 — rebuilding 50 points in Phase 2

The rival is at ≤ 25 % health, so the duel is deep in Phase 2: cycle **≈ 2.3 s**
(group 02), Impact cooldown **7.0 s** (group 03).

**Route A — offense only.** Ten **+5** combo finishers.

| Combos landed per rival cycle | Seconds per +5 | **Rebuild 50** |
|---|---|---|
| 0.70 (group 02's competent figure) | 3.29 s | **32.9 s** |
| 0.50 (scrappy) | 4.60 s | **46.0 s** |
| 0.35 (struggling) | 6.57 s | **65.7 s** |

**Route B — defensive reads.** Group 03 measured the blended value of a perfect dodge at
Q26 = 7 s, chaining into an Impact Window about a third of the time, at **+18.7**. Fifty
points is **2.67 → 3 perfect dodges.**

| Perfect-dodge hit rate | Cycles for 3 successes | **Rebuild 50** |
|---|---|---|
| 1 in 2 | 6 | **13.8 s** |
| 1 in 3 | 9 | **20.7 s** |
| 1 in 5 | 15 | **34.5 s** |

**Route C — mixed, which is what real play is.** A competent player over ~15 s of Phase 2
(≈ 6.5 cycles) plausibly lands two perfect dodges (+24), one counter (+15) and two combo
finishers (+10), with **two** Impact chains available inside 15 s at a 7 s cooldown (+40) —
comfortably past 50. **Rebuild ≈ 11–15 s.**

### One full retry cycle

| Player | Rebuild | + cinematic | + re-approach | **One retry** |
|---|---|---|---|---|
| **Strong** — chains Impact Windows | ~14 s | ~3.5 s | ~1.2 s | **≈ 19 s** |
| **Competent** — group 02's baseline | ~20 s | ~3.5 s | ~1.2 s | **≈ 25 s** |
| **Scrappy** — offense-heavy, few reads | ~40 s | ~3.5 s | ~1.2 s | **≈ 45 s** |
| **Struggling** — offense only, low hit rate | ~66 s | ~3.5 s | ~1.2 s | **≈ 71 s** |

### Against the GDD's 3–5 minute session target

Group 02's timings: a competent player reaches the ≤ 25 % gate at **≈ 2:53 (173 s)** and
has had meter 100 since **0:40–1:25**, so the first Clash attempt happens at **≈ 2:55**. A
scrappy player reaches the gate at **≈ 4:29 (269 s)**.

| Failures before success | Competent (≈ 25 s/retry) | Scrappy (≈ 45 s/retry) |
|---|---|---|
| 0 | **2:55** ✔ | **4:29** ✔ |
| 1 | **3:20** ✔ | 5:14 ✘ |
| 2 | **3:45** ✔ | 5:59 ✘ |
| 3 | **4:10** ✔ | 6:44 ✘ |
| 4 | **4:35** ✔ | 7:29 ✘ |
| 5 | **5:00** — exactly on the ceiling | — |

**A competent player can fail the Final Clash four times and still finish inside the GDD's
five-minute target.** That is a genuinely comfortable margin and it is the headline result.

### The bound nobody has stated: the loss condition caps the tail

The retry loop cannot run away, because the player is being attacked throughout it. Player
health is **100** (group 02 Q1) and Phase 2 rival damage averages **25.5** across
A 32 / B 25 / C 27 / D 18 (group 02 Q3) — **fewer than four connected hits is lethal.**

| Player | Retry length | Rival attacks faced (2.3 s cycle) | Hits taken at their plausible connect rate | Damage |
|---|---|---|---|---|
| Competent | 25 s | ~11 | ~1.1 at 10 % | ~28 |
| Scrappy | 45 s | ~20 | ~3.0 at 15 % | ~77 |
| **Struggling** | **71 s** | **~31** | **~4.6 at 15 %** | **~118 — lethal** |

> **The struggling player statistically dies during their first retry.** The competent
> player can afford roughly three to four retries on health before the loss condition
> catches them — very close to the same number the session target allows.
>
> **The GDD's single loss condition is the release valve for Q22's tail, and it is
> well-sized.** The duel self-terminates. There is no scenario in which a player grinds a
> pinned rival for ten minutes; long before that, one of the two endings arrives.

### Verdict

> **The endgame is acceptable under Q22 — at the proposed values, and with two things the
> designer must know.**

**1. The overshoot is real but pre-existing.** The scrappy player exceeds 5:00 on their
first retry. **Group 02 already flagged that the scrappy run overshoots to ~5:24 before any
Clash failure at all** (their tension #3). Clash retries widen a gap they did not create,
and the fix is the one group 02 already named: **drop Q2 from 1200 toward 1050–1100.** That
moves the health gate earlier and buys retry headroom directly. **It is the designer's
single most effective lever on this whole section.**

**2. The failed-Clash penalty is regressive, and this is the finding worth arguing about.**
The setback is a fixed **50 meter points** — the same for everyone, as the GDD specifies.
But its **cost in time is 3.7× larger for a struggling player (66 s) than for a strong one
(14 s)**, and under Q22 the struggling player is also the one most likely to fail the beats
in the first place. Combined with the health bound above, the practical shape of the
endgame is:

> **A player who cannot execute the two Clash beats does not grind their way to a win. They
> lose the duel.**

That is a coherent, defensible design — it is Sekiro's position, and the GDD's own scope
lock asks only that the player can *"reach and retry the Final Clash, and finish with a
valid win or loss."* **Both outcomes are reachable and the prototype's definition of done
is met.** But it means *"I fought well for four minutes and lost to two timing beats"* is a
reachable player experience.

> **This is the single question this file most wants the designer to answer, and it is not
> a number:** is that outcome intended? If yes, nothing changes. If no, the levers are
> listed below.

### The designer's levers, and the ones that are closed

**Available:**

| Lever | Effect |
|---|---|
| **Q2 → 1050–1100** (group 02's own proposal) | Moves the health gate earlier; buys **~20–30 s** of retry headroom for every player. **The strongest lever** |
| **Q20 generosity** — already taken at 0.50 s, identical beats | Fewer failures, so fewer laps. Already spent |
| **Q20's first-attempt 0.75 s option** (surfaced under Q20; GDD-precedented, non-adaptive) | Cuts first-attempt failures specifically, which is where the scrappy player's overshoot begins |
| **Reframe 3–5 minutes as the target for a *successful* duel** | Costs nothing. The GDD calls it a session target, not a rule; §14 Q23 already recommends **no timer**. A duel that runs to 5:30 because the player failed twice is a story, not a defect |

**Closed, and named so nobody reaches for them:**

| Lever | Why it is closed |
|---|---|
| Meter decay | **Constraint C1**, and Q9 above |
| Change the **50** meter setback | **GDD-published** |
| Change the **3 s** cooldown | **GDD-published** — and it is non-binding anyway |
| Change the gain values or the 0–100 ceiling | **GDD-published** |
| Widen the beats after failures | **Adaptive difficulty. Out of scope. Named as deferred future scope and not designed** |
| Auto-complete a beat | **GDD-forbidden** — *"Failure does not auto-correct the input"* |

---

## Q21 against Q10

The reconciliation §14 asked for, worked explicitly.

### The test as §14 states it — passes, and is not the binding test

> *"Must place both fighters outside every attack's `MinRange` (Q10) so the player is not
> immediately re-engaged while recovering."*

The largest `MinRange` among group 04's four bands is **attack B at 90 cm**. A 1200 cm
separation clears it by **1110 cm — a 13.3× margin.** **Every value in group 04's
1000–1300 cm band passes this test, and so would 200 cm.** The stated test does not
discriminate between the candidates, so it cannot be what actually decides Q21.

### The test that binds — `MaxRange`, not `MinRange`

`MinRange` is the **inner** edge of a band: below it, an attack is too close to use.
"Immediately re-engaged" is a question about the **outer** edge. The largest `MaxRange` is
**attack D at 840 cm**.

**At 1200 cm, no attack is in range at all.** The rival sits **360 cm** beyond D's outer
edge, inside group 04's identified **840–2884 cm zero-coverage region** — the region group
04 deliberately closed *"by a required advance rule rather than by accident."* The rival
must therefore advance before it can select anything.

### How long the advance takes

`BTTask_Idle_Reposition` advances for `RepositionDelay` seconds per cycle. Phase 2's
GDD-published range is **0.35–0.80 s**. Using **600 uu/s** as a placeholder for the rival's
**unspecified** walk speed (group 04 TODO item 49):

| Phase 2 reposition | Advance per cycle | Cycles to cover 360 cm | Reposition time | + Select (0.10) + Telegraph (0.40–0.75) | **First strike begins** | **+ Active (0.18)** |
|---|---|---|---|---|---|---|
| **0.35 s** (floor — worst case for the player) | 210 cm | **2** | 0.70 s | 0.50 s | **1.20 s** | **1.38 s** |
| 0.80 s (ceiling) | 480 cm | 1 | 0.80 s | 0.85 s | 1.65 s | 1.83 s |

> **The player gets a guaranteed ≈ 1.20 s in which the rival cannot legally begin an
> attack, and ≈ 1.38 s before any hit can connect — measured at the fastest legal Phase 2
> values.** That covers reorientation, lock-on confirmation, and reading the first
> telegraph, and it consumes just under half of the GDD's 3-second cooldown.

### The comparison that sets the value

| Separation | Gap past D's 840 cm | Cycles at the 0.35 s floor | **Non-threat window** | Verdict |
|---|---|---|---|---|
| 1000 cm — group 04's floor | 160 cm | **1** (210 ≥ 160) | **0.85 s** | **Too tight.** One reposition cycle only. The player is still reorienting from a camera cut |
| **1200 cm — proposed** | **360 cm** | **2** (420 ≥ 360) | **1.20 s** | **The smallest value in the band that forces two cycles** |
| 1300 cm — group 04's ceiling | 460 cm | **3** (630 ≥ 460) | 1.55 s | Safe, but the rival visibly walks, and the clamp slack starts to bind |

**The whole difference between 1000 and 1200 is one reposition cycle.** That is why the
band's floor is raised to 1100 cm: at 1100 the gap is 260 cm, still two cycles at the
0.35 s floor, so **1100 is the true minimum that preserves the guarantee.**

### The sensitivity that matters — and the threshold

The two-cycle guarantee is a function of the rival's walk speed, which **does not exist
yet**:

> **One reposition cycle at the Phase 2 floor covers 360 cm when the rival's speed reaches
> `360 / 0.35 = 1029 uu/s`.** Above roughly **1030 uu/s**, a 1200 cm separation collapses
> to a single cycle and delivers the same 0.85 s that 1000 cm would.

| Rival speed | Advance per 0.35 s cycle | Cycles to cover 360 cm | Non-threat window |
|---|---|---|---|
| 400 uu/s | 140 cm | 3 | 1.55 s |
| **600 uu/s** (placeholder) | **210 cm** | **2** | **1.20 s** |
| 800 uu/s | 280 cm | 2 | 1.20 s |
| **1030 uu/s — the threshold** | **360 cm** | **1** | **0.85 s** |
| 1200 uu/s | 420 cm | 1 | 0.85 s |

**Q21 and the rival's walk speed must be decided together.** Group 04 already named the
lower bound on that speed — *"a rival slower than the player can be kited forever and the
duel cannot end"* under Q22. **This section supplies the upper bound: above ~1030 uu/s the
failed-Clash separation stops doing its job.** That is a usable window for the designer and
it is the most concrete thing this group can contribute to a value it was not given.

### Two secondary checks, both clean

- **No single rival action closes the gap.** Attack D's `MaxTravelDistance` is **600 cm**
  (group 04 Q13), and D is not even selectable at 1200 cm. From D's own outer edge at
  840 cm, one D leaves the rival at 240 cm — by design. **From 1200 cm, nothing the rival
  owns is a one-move re-engage.**
- **Lock-on holds.** Acquire **3000 cm**, break **3300 cm** (group 04 Q11), against a
  1200 cm separation and a 2884 cm arena diagonal. **The player never loses target through
  a failed Clash**, so the separation costs no camera re-acquisition.

---

## The five answers, in one place

| Q | Kind | Status | Proposed | Lives in | Unblocks |
|---|---|---|---|---|---|
| **Q9** | B | **PROPOSED** (satisfies binding **C1**) | **No decay.** `MeterDecayRate` does not exist — no `Tick`, no timer, no float | `BP_AscensionComponent` | **M3-03** |
| **Q17** | **A** | **APPROVED** | **Yes — reuse `IA_Impact`.** One action, one `IMC_Duel`, no context swap; routed by `bClashBeatOpen`. Accept only a press that *begins after* the beat opens | `IMC_Duel` | **M1-10** |
| **Q19** | B | **PROPOSED** | **1.2 s** post-counter window (band **1.0–1.3 s**; **hard ceiling 1.30 s**). Author as `CounterRecoveryLength + 0.6 s` | `BP_FinalClashDirector` | **M4-05** |
| **Q20** | B | **PROPOSED** | **0.50 s, both beats, identical** — the top of the GDD's published 0.35–0.50 s Standard range (band **0.45–0.60 s**). **Recommended against: a tighter beat 2** | `BP_FinalClashDirector` | **M4-06** |
| **Q21** | B | **PROPOSED** | **1200 cm**, along the arena **long axis**, midpoint push with clamp-and-redistribute (band **1100–1300 cm**) | `BP_FinalClashDirector` | **M4-08** |

**All five are recommendations. Q17 is settled because there was nothing to decide. The
other four stay open in `TODO.md`, marked PROPOSED, until the human designer of record
approves or changes them.**

## Findings against `design-brief.md` §14 itself

Three places where this group's answer differs from the range or the framing §14 offered.
Recorded so the difference is visible rather than silent.

1. **Q19: §14's upper bound of 1.5 s is unsafe.** It exceeds the 1.30 s earliest-next-strike
   floor in Phase 2, which would let the player initiate the game's win condition while a
   strike is landing on them. Band capped at 1.3 s.
2. **Q20: §14's suggestion that "beat 2 tighter than beat 1" might "make the finish feel
   like a real test" is argued against**, because §14 was written before Q22 was approved
   and the Clash became the sole exit.
3. **Q21: §14's stated test — outside every attack's `MinRange` — does not discriminate
   between any candidate value.** The binding test is `MaxRange` plus reposition time, and
   that is what the answer is built on.

## Gaps found while answering — none of them this group's questions

Flagged to the commander, in the same spirit as groups 03 and 04. Each is a value the M4
build will need and which has no GDD number, no `design-brief.md` §13.2 row and no Q number.

1. **`AM_Clash_Beat1` / `AM_Clash_Beat2` montage lengths**, and the notify position at which
   each prompt opens. The Clash beats' *lead-in* is unspecified, and a 0.50 s window with no
   wind-up is a different mechanic from a 0.50 s window with one. Only the GDD's **1–3 s**
   burst constrains it.
2. **The successful-counter recovery length.** Q19 is expressed relative to it and cannot be
   locked without it. Distinct from group 03's already-flagged gap (the counter's own
   *success* window) — this is the recovery *after* success.
3. **What happens if `IA_FinalClash` is pressed while an Impact Window prompt is open.** Both
   can be live at once after a counter. Proposed rule (surfaced, not decided): the Impact
   Window resolves first and the post-counter Clash window is **paused, not consumed**.
4. **The wall margin for the Q21 clamp** — how close to the arena edge a fighter may be
   placed. Engineering-adjacent, but it changes the effective separation near the ends of
   the long axis.
5. **The rival's `MaxWalkSpeed`** — already group 04's TODO item 49. **This group supplies
   the missing upper bound: ~1030 uu/s**, above which Q21 stops working.

## Constraint check

| Constraint | How this file complies |
|---|---|
| **SCOPE LOCK** | **Two** timing beats, not three and not variable-length. **One** Final Clash — no second variant, no per-fighter Clash, no difficulty setting. One arena, four attacks, one rival. Every widening-on-failure idea is named as **deferred future scope** and is not designed |
| **No runtime AI-model calls** | Nothing here proposes an LLM, a model API call, adaptive difficulty, or a window that watches the player. The Clash is a Blueprint director with two timers; the rival remains a deterministic authored Behavior Tree, parked on `BTTask_WaitIndefinite` for the duration |
| **No auto-success** | Explicitly enforced. Q17 note 2 stops a held button from passing a beat. Q20 rejects Final Fantasy XVI's unfailable clash **by name**. The GDD's *"Failure does not auto-correct the input"* is quoted and honoured |
| **Numbers unchanged** | Meter **0–100** and **+5 / +12 / +15 / +20 / +0**; gate at **100 AND ≤ 25 %**; failure at **1 HP floor / meter to 50 / 3 s cooldown**; Impact **0.75 s** and **0.35–0.50 s**; burst **1–3 s**; session **3–5 min**. All carried through unchanged and cited. **Q20 takes 0.50 s from inside a published range rather than inventing a value** |
| **Milestone order** | Everything lands in M1 (Q17), M3 (Q9) and M4 (Q19, Q20, Q21). The one HUD note is a **functional** gray-box state in M3/M4, with the styled treatment explicitly left to **M5** |
| **This is Ascendant Impact** | Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, Shattered Ring, Ascension Meter, Impact Windows, Final Clash. Nothing from any other project appears |

## Research note

**13 of ~15 WebSearch sources used. Stopping here rather than chasing the last gaps, per
the cap.** What remains unresolved, named rather than guessed:

- **No shipped game reached in this pass publishes a numeric QTE input window.** Six
  searches across Resident Evil 4, Final Fantasy XVI, Hi-Fi Rush, Sekiro, God of War
  Ragnarök and Bloodborne returned qualitative descriptions only. **Q20's 0.50 s is derived
  from the GDD's own published Standard Impact Window range, not from prior art.**
- **No shipped game reached publishes a knockback or post-cinematic separation distance in
  world units.** Two searches, including a targeted attempt at Tekken 8. Group 04 hit the
  same wall independently. **Q21's 1200 cm is derived from group 04's arena footprint and
  Q10 bands.**
- **No contextual-prompt acceptance window was found with a number.** Four sources all say
  *"a few seconds."* **Q19 is the weakest-sourced answer in this file.**
- **Not searched at all:** motor-timing repeatability for sub-0.5 s prompts (group 03 also
  ran out of budget on the equivalent question for Q7); post-knockback recovery timing in 3D
  fighters; and whether any shipped game uses a resource that both decays and gates the only
  win condition — **Q9's key negative claim is an absence of evidence and is stated as one.**

**One prior-art claim from group 01 is now closed.** Group 01 had to mark as *unverified*
whether a failed Hi-Fi Rush Rhythm Parry set ends the fight. It does not: *"if not completed
to the threshold, the enemy will either attempt another after dealing damage, or lose its
enraged state."* **The fight continues and the sequence can be retried** — our failed-Clash
recovery rule, shipped in a real game.

## Sources

Accessed 2026-08-02.

- [Tension — Guilty Gear Wiki (Fandom)](https://guiltygear.fandom.com/wiki/Tension)
- [GGXRD/Gauges — Dustloop Wiki](https://www.dustloop.com/w/GGXRD/Gauges)
- [Stylish Rank — Devil May Cry Wiki (Fandom)](https://devilmaycry.fandom.com/wiki/Stylish_Rank)
- [Enhanced Input in Unreal Engine — UE 5.8 Documentation](https://dev.epicgames.com/documentation/unreal-engine/enhanced-input-in-unreal-engine?lang=en-US)
- [Add Mapping Context — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Input/AddMappingContext)
- [Fix: Unreal Enhanced Input Mapping Context Priority — Bugnet Blog](https://bugnet.io/blog/fix-unreal-enhanced-input-mapping-context-priority)
- [Visceral Attack — Bloodborne Wiki (Fextralife)](https://bloodborne.wiki.fextralife.com/Visceral+Attack)
- [Parry — Bloodborne Wiki (Fextralife)](https://bloodborne.wiki.fextralife.com/Parry)
- [Batman: Arkham Origins — Combat System FAQ (GameFAQs)](https://gamefaqs.gamespot.com/ps3/710576-batman-arkham-origins/faqs/68340)
- [Special Combo Moves — Arkham Wiki (Fandom)](https://arkhamcity.fandom.com/wiki/Special_Combo_Moves)
- [Deathblows — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Deathblows)
- [Posture — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Posture)
- [God Of War Ragnarok Stun Grab — How To Stun Enemies (Gamer Tweak)](https://gamertweak.com/stun-enemies-gow-ragnarok/)
- [How to Stun Enemies in God of War Ragnarok Quickly — Attack of the Fanboy](https://attackofthefanboy.com/guides/how-to-stun-enemies-in-god-of-war-ragnarok-quickly/)
- [Quick Time Event — Resident Evil Wiki (Fandom)](https://residentevil.fandom.com/wiki/Quick_Time_Event)
- [How to do 'impossible' quick time events (QTE) in Resident Evil 4 — Steam Community Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=233813344)
- [How Final Fantasy XVI Perfected the Quick-Time Event — TechRaptor](https://techraptor.net/gaming/opinions/final-fantasy-xvi-quick-time-event)
- [Quick Time Events Guide: Are There QTEs? — Final Fantasy 16 (Game8)](https://game8.co/games/Final-Fantasy-XVI/archives/415100)
- [Rhythm Parry — Hi-Fi Rush Wiki (Fandom)](https://hifi-rush.fandom.com/wiki/Rhythm_Parry)
- [Set Actor Location — UE 5.8 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Transformation/SetActorLocation)
- [ProjectPointToNavigation — UE 5.8 Documentation](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/NavigationSystem/UNavigationSystemV1/ProjectPointToNavigation?lang=en-US)
- [How to use SetActorLocation() and keep actor on ground? — Epic Developer Community Forums](https://forums.unrealengine.com/t/ue5-1-how-to-use-setactorlocation-and-keep-actor-on-ground/775096)
- [On Analyzing Tekken Moves and Strings — community document](https://docs.google.com/document/u/0/d/1I35p54rL5QhtYA2Z8Ab8io-Het8Zwe-fsTSAAcTPAOo/mobilebasic)
- [Knockback — TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/Knockback)

Prior-art claims re-used from earlier groups in this project — already sourced in their
files and not re-searched here: Sekiro's Deathblow markers, Metal Gear Rising's 10 % QTE,
Asura's Wrath, Sifu, Furi, Street Fighter 6's Perfect Parry, and the ~250 ms human visual
reaction figure (`design/group-01-blocking-q22.md`, `design/group-03-defensive-timing.md`).

---

*Every value in this file is **provisional and pending playtest**. The human designer of
record owns all of them.*
