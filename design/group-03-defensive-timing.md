# Group 03 — Defensive timing · Q6, Q7, Q8, Q26, Q27, Q28

**Dispatched:** 2026-08-02 · designer agent, group 03 of the open-question sweep.
**Consumes:** `gdd/INDEX.md`, `gdd/sections/02`, `gdd/sections/04`, `design-brief.md`
§13.1 rows 2–4 and 17–25, §13.2 rows 34–36 / 54–56, §14, `design/decisions.md` (Q22
APPROVED), `design/group-02-combat-economy.md`.
**Produces:** answers to **Q6, Q7, Q8, Q26, Q27, Q28** only. Every other Q belongs to
another group and is named as still open wherever the reasoning here leans on it.

> **EVERY ANSWER IN THIS FILE IS `PROPOSED`, NOT DECIDED.**
> All six are **KIND B** design items. A designer dispatch may research and recommend;
> it may not settle. The human designer of record owns every number here. Each entry
> stays open in `TODO.md`, marked PROPOSED, until the designer approves or changes it.

`design-brief.md` §14 titles this group **"Defensive timing — this is where the game
lives."** That is the correct framing. Nothing else in the open-question set changes
how the duel *feels* moment to moment as much as these six numbers do.

---

## Binding context

### Q22 is APPROVED and binding

`design/decisions.md`, entry **2026-08-02 — Q22**, status **APPROVED**:

> `MinHealthFloor = 1` on the rival's `BP_HealthComponent` from `BeginPlay`, lowered to
> `0` only by `ClashSuccess()` immediately before it applies lethal damage.

**Consequences for this group:**

1. **The Final Clash is the only way to win**, so **the meter is a hard win requirement,
   not a bonus.** Every defensive window in this file is therefore also a *meter faucet*.
   Q6, Q7 and Q26 are not only difficulty knobs — they are the taps that decide whether
   the player can finish the game at all.
2. **Constraint C1 is assumed true throughout: no meter decay (Q9, another group).** All
   fill-rate arithmetic below is cumulative. **If Q9 resolves to decay, re-run every
   meter estimate in this file.**
3. **Constraint C2** (HUD must show which gate is locked) is reinforced by the Q26 answer
   below, which deliberately paces the meter rather than letting it fill instantly.

### The two questions group 02 handed this group

From `design/group-02-combat-economy.md` and `design/decisions.md`:

> **4. Q26 makes the +20 Impact row dominant** — five Impact successes fill the meter
> outright. If the meter is to be a real second gate, the lever is **Q26**, not any GDD
> gain value. Flagged to the defensive-timing group.

> **6. Q27 is a direct scalar on the Q2 derivation** — at §14's upper bound of 1.5 the
> 45-combo count drops toward ~30. **Q27 should be resolved before Q2 is locked.**

Both are answered, and both get their own verdict in **"Answering group 02"** at the
end of this file.

---

## GDD numbers used here — fixed, cited, never edited

Published **per state, not per attack** (`gdd/sections/04`, PDF p.5; mirrored in
`design-brief.md` §13.1 rows 17–25). Any authored value must fall **inside** its range.

| State | Phase 1 | Phase 2 |
|---|---|---|
| Idle / Reposition | 0.60–1.20 s | 0.35–0.80 s |
| Select Attack | 0.10–0.20 s | 0.10–0.20 s |
| **Telegraph** | **0.55–0.95 s** | **0.40–0.75 s** |
| Active Attack | 0.18–0.45 s | 0.18–0.45 s (**not** phase-scaled) |
| Recover | 0.45–0.90 s | 0.35–0.75 s |
| Return to Neutral | 0.10–0.20 s | 0.10–0.20 s |

Also fixed and used below (`gdd/sections/02` p.2–3, `gdd/sections/03` p.3–4,
`gdd/sections/01` p.1):

| Value | Number |
|---|---|
| First Impact Window response time | **0.75 s** |
| Standard Impact Window response time | **0.35–0.50 s** |
| Impact Window cinematic burst | **1–3 s** |
| Meter gains | **+5** finisher · **+12** perfect dodge · **+15** counter · **+20** Impact · **+0** damage/waiting |
| Meter range | **0–100** |
| Target session | **3–5 minutes** |

**No answer below requires changing any of these.** Where an answer would have, it was
discarded.

### Framerate convention used for every frame-to-second conversion

Unless a source states otherwise, **frame counts are converted at 60 fps (1 frame =
16.7 ms)**, and where a source's own framerate basis is ambiguous, **both conversions
are given and the ambiguity is marked**. Ascendant Impact is a PC title with no locked
framerate, so **every value proposed here is authored in *seconds*, never in frames** —
`Anim Notify State` durations are time-based on the montage timeline, so they are
framerate-independent by construction. That is a deliberate implementation choice, not
an accident: a frame-counted window would change difficulty on a faster machine.

---

## Q6 — Dodge i-frame window

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-19**
- **Value lives in:** `ANS_IFrame` — an `Anim Notify State` on `AM_Player_Dodge`
  (`design-brief.md` §13.2 row 34)
- **GDD range:** **The GDD publishes no i-frame number and no range.** It publishes only
  that *dodge* and *perfect dodge* are two distinct entries in the shared control model
  (`gdd/sections/02`, PDF p.2), and that perfect dodge pays **+12** while ordinary
  survival pays **+0** (`gdd/sections/03`, PDF p.3–4) — so the GDD guarantees these are
  **two nested windows with different rewards**, and says nothing about their sizes.
  `design-brief.md` §14 offers **0.20–0.35 s**, "starting near the beginning of the
  dodge montage." The proposal below falls inside it.

### Proposed value

> **`ANS_IFrame` starts at 0.03 s into `AM_Player_Dodge` and runs for 0.28 s**, so the
> invulnerable span is **[0.03 s, 0.31 s]**.
> Identical for Agent Echo and Agent Nova — **one notify state on one shared montage.**
> Tuning band if the designer wants to move it: **0.24–0.32 s**.

**SCOPE LOCK note, stated once and applying to all six answers:** the SHARED PLAYER-KIT
SCOPE RULE (`gdd/sections/02`, PDF p.2–3) puts dodge and perfect dodge in the shared
framework. **These windows are one value, not two.** Echo's "perfect-dodge timing"
identity and Nova's "aggressive momentum" are expressed through
`DA_FighterProfile.DodgeDistance` (Q16) and `MontagePlayRate` (Q14) — **not** through a
different i-frame length. Putting `IFrameDuration` on `DA_FighterProfile` is the exact
shape a per-fighter defensive split would take later, so it must live on
`DA_TuningGlobals` or on the notify state itself, **never** on the fighter profile.

**One caution about `MontagePlayRate` (Q14, another group).** If Echo and Nova run
`AM_Player_Dodge` at different play rates, a notify state authored at 0.28 s of montage
time becomes **0.28 / PlayRate seconds of wall-clock time** — a Nova at 1.15× would get
a 0.24 s i-frame window and a harder game for free. **Recommendation to the Q14 group:
either keep `MontagePlayRate` at 1.0 for `AM_Player_Dodge` specifically, or have
`ANS_IFrame` read its duration from `DA_TuningGlobals` and compensate for play rate.**
The first is cheaper and is what this group would build.

### Why 0.28 s

1. **It sits inside the shipped-game band, at the disciplined end.** Real dodges cluster
   between ~0.22 s and ~0.47 s of invulnerability (table below). 0.28 s is a little
   above the tightest shipped example and well below the most forgiving. For a duel
   with **four** attacks the player will see dozens of times, the tighter end is right —
   the player is learning a small pattern set, not surviving an open world.
2. **It answers the GDD's Active Attack range correctly.** Active Attack is
   **0.18–0.45 s and is explicitly not phase-scaled** (`gdd/sections/04`, PDF p.5). At
   0.28 s the i-frame window **fully covers a short active window (0.18 s) with ~0.05 s
   of slack on each side**, and **cannot cover a long one (0.45 s)**. That asymmetry is
   the design: a dodge is an *answer to a specific hit*, not a blanket you throw over
   the whole attack. A player who dodges early into attack C's long active state will
   still get clipped on the way out, which is exactly the read the GDD's "clear body
   direction and visible active range" requirement is asking the player to make.
3. **It leaves room for Q7 to be meaningful.** A perfect-dodge sub-window of 0.10 s
   (Q7 below) occupies **36 %** of a 0.28 s i-frame window. That ratio is the whole
   feel of the mechanic: roughly a third of a successful dodge is a *great* dodge. At
   0.20 s the sub-window would be half the window and perfect dodge would stop feeling
   special; at 0.35 s it would be under 30 % and the +12 row would start feeling like
   a lottery.
4. **It is authored in one place and moves in one edit.** `ANS_IFrame` sets
   `bIsInvulnerable` on the shared `BP_HealthComponent` in `Notify Begin` and clears it
   in `Notify End`. Nothing else reads it.

### A dependency this group cannot answer — the dodge montage's total length

`ANS_IFrame` is a window *inside* a montage, and **`design-brief.md` §13.2 assigns no Q
number to the dodge montage's total length.** That length matters: the vulnerable tail
after the i-frames end is what makes dodge-spam cost something. Elden Ring's medium roll
is **28 i-frames followed by 16 recovery frames** — roughly a **1.75 : 1** invulnerable-
to-vulnerable ratio.

> **Question for the designer (no value proposed):** what is the total length of
> `AM_Player_Dodge`? Applying Elden Ring's ratio to a 0.28 s i-frame window starting at
> 0.03 s suggests a total in the region of **0.45–0.55 s**, leaving a **~0.15–0.25 s**
> vulnerable tail. **That is a range for conversation, not a recommendation**, and it
> should be decided alongside Q16 (dodge distance), because distance and duration
> together are what "deliberate spacing" versus "fast lateral rhythm" actually mean.

### Prior art (real games, named, with real numbers)

All conversions at **60 fps** unless the row says otherwise.

| Game | Mechanism | Real numbers | Seconds | Relevance |
|---|---|---|---|---|
| **Elden Ring** | Medium roll — the genre's reference dodge | **28 i-frames**, then **16 recovery frames**, **44 frames total** per roll; medium roll (Equip Load 30–70 %) is reported as matching fast roll on speed, distance and i-frames | **0.467 s** invulnerable, **0.267 s** vulnerable tail, **0.733 s** total | The **generous** end of the band. Justified there by an open world full of unlearnable enemies; **not** justified in a four-attack duel |
| **Dark Souls III** | Roll, i-frames barely affected by equip load | **13 i-frames** light/medium, **12** heavy. Community reporting stresses that encumbrance changes roll *speed and distance*, not i-frame count | **0.217 s** at 60 fps · **0.433 s** if the community's count is on a 30 fps basis — **AMBIGUOUS, see note** | Evidence that **distance and speed, not i-frames, are the correct per-variant lever.** This is precisely the argument for Echo/Nova differing on Q16/Q14 and **not** on Q6 |
| **Monster Hunter: World** | Base roll plus a skill that buys extra i-frames | Base evade **13 i-frames**; Evade Window levels 1–5 add **15 / 17 / 19 / 22 / 25** total i-frames. Weapon modifiers: **−3** for lance/gunlance hops, **+12** for sword-and-shield backhop, **+32** for longsword Foresight Slash | Base **0.217 s**; EW5 **0.417 s**; Foresight ≈ **0.75 s** | The clearest published *scale* of the design space: **0.22 s is a real shipped baseline dodge**, and everything above it is bought with a skill slot. Our 0.28 s is a baseline dodge with a little courtesy on top |
| **Bayonetta** (Smash Ultimate implementation, which is where the frame data is public) | Dodge with a nested reward window | Witch Time activation window **frames 8–27**; intangibility **frames 8–23**; Bat Within (the late/failed branch) **frames 24–35** | Intangible **16 frames = 0.267 s**; activation **20 frames = 0.333 s** | **The structural match for Q6 + Q7 together** — one dodge, an invulnerable span, and a nested reward branch, with an authored *late-input* fallback. Its intangible span, **0.267 s**, is within 0.02 s of the value proposed here |

> **Marked AMBIGUOUS — read carefully.** The Dark Souls III "13 i-frames" figure is
> universally quoted by the community **without stating a framerate basis**. Souls frame
> data is historically tabulated at 30 fps (the console cap of the earlier titles) while
> DS3 on PC runs at 60. The two readings differ by a factor of two and **this pass could
> not resolve which is meant.** It is cited here only as corroboration that i-frame
> counts are small and that equip load moves speed rather than invulnerability —
> **no number in this file depends on resolving it.**

> **Marked UNVERIFIED.** No source found in this pass states Bayonetta's *own* (non-Smash)
> Witch Time or dodge i-frame counts. The Smash Ultimate figures are a licensed
> reimplementation by a different studio and are **structural** evidence, not a direct
> measurement of Bayonetta's action game.

### Interaction with the other five

- **Q7 is nested inside this.** `ANS_PerfectDodge` must begin at or after 0.03 s and end
  at or before 0.31 s. The developer should author them as **two notify states on the
  same montage track region**, with an editor-time check that the perfect window is a
  strict subset. If Q6 moves, **Q7's placement moves with it** — they are one decision
  in two fields.
- **Q8 (whiffed-counter recovery) is the sibling penalty.** Dodge and counter are the two
  defensive options; if the dodge is safe and cheap while the counter is expensive to
  miss, the player will simply always dodge. **Q8's 0.55 s and the dodge's ~0.15–0.25 s
  vulnerable tail are what keep both options live**, and they should be tuned as a pair.
- **Q26 sets the value of a perfect dodge.** With the Impact Window on cooldown, a
  perfect dodge is worth **+12**; off cooldown it chains into **+20** for **+32**. Q6
  decides how often the player *gets* to that fork.
- **Q27 does not touch this.** The recover multiplier is offensive.
- **Q28 competes for the same fingers.** A player mid-combo who needs to dodge is
  cancelling the string; whether that is possible is a `Montage Stop` / branching-point
  question the developer owns, and it is **not** proposed here.
- **Open elsewhere:** **Q16** (dodge distance) and **Q14** (`MontagePlayRate`) both
  change what 0.28 s of invulnerability is *worth* — a long dodge escapes the hitbox
  spatially and barely needs i-frames, a short one needs all of them. **Q6 should be
  re-checked after Q16.** **Q25** (per-attack values inside the GDD ranges) decides
  whether any given attack's Active Attack window is 0.18 s or 0.45 s, which decides
  whether a 0.28 s dodge covers it.

**This is a recommendation. The designer decides.**

---

## Q7 — Perfect-dodge sub-window · **BLOCKING**

- **Kind:** B (design) · **Status:** **PROPOSED** · **BLOCKING**
- **Unblocks build step:** **M1-19**
- **Value lives in:** `ANS_PerfectDodge` — a second `Anim Notify State` on
  `AM_Player_Dodge` (`design-brief.md` §13.2 row 35)
- **GDD range:** **The GDD publishes no number.** It publishes the *reward* — perfect
  dodge is **+12** and is one of the two events that can open an Impact Window
  (`gdd/sections/03`, PDF p.3; `gdd/sections/02`, PDF p.3) — and it publishes the
  **PRESERVED — ONBOARDING RULE**: *"The first Impact Window is intentionally wider, but
  it still requires the player's input and must be earned through a successful real-time
  defensive action. The game does not press the input for the player and does not convert
  a miss into success."* `design-brief.md` §14 offers **0.08–0.15 s**, strictly narrower
  than Q6, and calls it *"the single number that does more to define the game's
  difficulty than any other in the table."*

### Proposed value

> **`ANS_PerfectDodge` starts at 0.03 s into `AM_Player_Dodge` — the same instant as
> `ANS_IFrame` — and runs for 0.12 s**, so the perfect span is **[0.03 s, 0.15 s]**.
> That is **the first 0.12 s of the 0.28 s invulnerable window**, or **43 %** of it.
> Identical for Echo and Nova. Tuning band: **0.10–0.15 s**.
>
> **Playtest protocol, and this matters as much as the number:** **start the first
> playtest session at the top of the band (0.15 s) and tighten toward 0.12 s / 0.10 s
> across sessions.** A too-generous first pass still produces usable data because
> players reach the mechanic and you learn what they do with it. A too-tight first pass
> produces *no* data because players never trigger it, conclude the mechanic is broken,
> and stop trying. **Tighten into a working mechanic; do not loosen into a discovered
> one.**

### Why the window sits at the *front* of the dodge

This is the load-bearing structural choice and it is more important than the duration.

`ANS_PerfectDodge` occupies the **earliest** part of the dodge, not the middle and not
the end. That means the incoming hit must arrive **just after** the player commits, which
means the player must press dodge **late — into the strike**, not early away from it.
That is the whole read the GDD's core loop asks for: *"READ Crimson Vanguard's
telegraph → RESPOND."* A player who panics and dodges at the first frame of the telegraph
gets a **plain** dodge: they survive on i-frames and earn **+0**. A player who waits,
reads the commit, and dodges into the strike gets **+12** and an Impact Window candidate.

**The reward for nerve is the mechanic.** This is Bayonetta's Witch Time structure and
Sekiro's deflect structure, and it is why both games feel like they are about courage
rather than distance.

### Why 0.12 s

1. **It is four times the competitive floor and comfortably under the classic
   benchmark.** Street Fighter 6's Perfect Parry is **2 active frames = 0.033 s**;
   Street Fighter III's parry was **10 frames = 0.167 s**. 0.12 s sits between them,
   nearer the classic. Ascendant Impact has **no** trained competitive audience, **no**
   training mode, and **no** ordinary-parry safety net underneath the perfect one — so
   it belongs above the SF6 floor by a wide margin.
2. **It is close to Sekiro's default deflect window, deliberately.** Sekiro's deflect
   window is **12 frames = 0.20 s at 60 fps** and shrinks toward **4 frames** or even
   **0** if the player spams guard. Sekiro is the closest tonal neighbour to this game
   and its window is the one most players describe as "hard but fair." 0.12 s is
   **tighter than Sekiro's default** — justified because our perfect dodge sits inside a
   **0.28 s i-frame window that already saved the player**, whereas a missed Sekiro
   deflect costs posture immediately. **Our failure state is "no bonus," Sekiro's is
   "damage."** A tighter window is affordable when failure is cheap.
3. **It is reachable by pure reaction at the GDD's worst-case telegraph.** Shown in
   full in **"Reaction-time check"** below: even at the Phase 2 telegraph floor of
   **0.40 s** with the hit landing on the first instant of Active Attack, the required
   press window is **[0.25 s, 0.37 s]** measured from telegraph onset — which straddles
   the average human visual reaction time of **~250 ms** almost exactly. **A player of
   average reflexes can perfect-dodge the hardest legal attack in the game on their
   first attempt.** Anything tighter than ~0.10 s stops being true.
4. **It makes the +12 row earnable without making it free.** Group 02's cross-check puts
   **9 perfect dodges** at a full meter. Over a duel of roughly 60 Phase 1 cycles and 25
   Phase 2 cycles, 9 successes is a modest hit rate — the player does not need to be
   good at this, only willing to try it.
5. **43 % of the i-frame window is a legible fraction.** The player's felt experience is
   "roughly the first half of a dodge is the good part." That is teachable in one
   sentence and discoverable in three attempts.

### What this number must NOT become

**A window that widens after N failures is out of scope and is not proposed.** It would
be adaptive difficulty, it would violate the project's *"deterministic authored logic"*
constraint in spirit, and it would break the GDD's own statement that the game *"does not
convert a miss into success."* **Named here as deferred future scope and deliberately not
designed.**

Note what the GDD did instead, because it is instructive: the GDD's onboarding concession
is a **wider first Impact Window (0.75 s vs 0.35–0.50 s)** — a one-shot, authored,
non-adaptive widening of a *different* window. **That is the sanctioned pattern.** If
playtest shows new players cannot find the perfect dodge, the fix is presentation
(telegraph clarity, a hit-stop cue on success, the Impact Window teaching moment) or a
flat retune of Q7 — **never a window that watches the player.**

### Prior art (real games, named, with real numbers)

All conversions at **60 fps** unless the row says otherwise.

| Game | Mechanism | Real numbers | Seconds | Relevance |
|---|---|---|---|---|
| **Sekiro: Shadows Die Twice** | Deflect — a timed guard that negates posture damage | Deflect window is **12 frames by default**, described as **0.2 s before the attack hits**; frames **1–12** deflect, frames **13–36** are ordinary block. The window **shrinks with recent guard presses — to as little as 4 frames, and to 0 if spammed** | Deflect **0.200 s**; spam-degraded **0.067 s** → **0 s** | **The single most relevant piece of prior art in this file.** Two lessons taken: (1) ~0.2 s is a shipped, beloved, "hard but fair" window; (2) **Sekiro punishes mashing by shrinking the window** — an authored, deterministic anti-spam rule. Our equivalent anti-spam rule is not window-shrinking (too opaque) but **Q8's whiffed-counter recovery** and the dodge's vulnerable tail |
| **Street Fighter 6** | Perfect Parry — the tightest window in a mainstream fighter | Triggers if Drive Parry contacts an attack **in its first two active frames**; input must land **within one frame before the hit, or on the same frame**. Defender recovers in **1 frame** and is invincible **6 frames**; the punish combo takes **50 % damage scaling** | Perfect window **0.033 s**; invincible follow-up **0.100 s** | **The floor of the design space**, and a warning. SF6 can ship 2 frames because a missed Perfect Parry still gives an ordinary Drive Parry — there is a safety net. Also note the **50 % damage scaling**: even SF6 caps the payoff of a perfect defensive read, which is direct support for **Q27 staying at 1.0** |
| **Street Fighter III: 3rd Strike** | The original parry | **10-frame** window, explicitly contrasted with SF6's 2 | **0.167 s** | The historical benchmark for "a parry a human can learn." Our 0.12 s is one notch tighter than the mechanic that produced Evo Moment 37 |
| **Bayonetta** (Smash Ultimate implementation — where the frame data is public) | Witch Time — a nested reward branch on a dodge, with an authored *late* fallback | Witch Time activation **frames 8–27**; intangibility **frames 8–23**; Bat Within (too-late branch) **frames 24–35** | Activation **0.333 s**; intangible **0.267 s**; late branch **0.200 s** | **The exact structure proposed here**: one dodge, one invulnerable span, one nested reward window sharing the same start frame. Note that Smash's activation window is *wider* than its intangibility — the reverse of our nesting. Ours is the stricter, more legible arrangement |
| **Ghost of Tsushima** | Perfect Parry, on top of an ordinary parry | Community reporting describes the perfect window as **1–2 frames** of the attack landing; practical advice is to parry *"roughly half a second after an enemy swings"* | **0.017–0.033 s** — **UNVERIFIED** | Cited only as a *second* data point that shipped perfect-parry windows go very tight when an ordinary parry sits underneath them. **We have no such underlayer**, so this is a bound we deliberately do not approach |
| **Nioh 2** | Burst Counter — three authored variants with deliberately different window shapes | Feral: leaves an afterimage that is *"only up for about half a second"* (**≈ 0.5 s**), described as the most forgiving. Phantom: *"comes out almost instantly"*, plenty of active frames, but must be at point-blank. Brute: valid *"anytime between the red glow and before their recovery frames end"* — a very wide window with a long startup | Feral ≈ **0.5 s** | Evidence that a **counter/perfect window and a spacing requirement are interchangeable difficulty levers.** Nioh buys a wide window with a hard range constraint. **We are not doing this** — SCOPE LOCK gives us one dodge — but it is worth the designer knowing the trade exists if 0.12 s proves too hard |

> **Marked UNVERIFIED.** The Ghost of Tsushima "1–2 frames" figure comes from guide and
> forum sources with no datamining behind it, and the same sources also say *"roughly
> half a second after the swing,"* which is a different kind of claim entirely. **No
> value in this file depends on it.**

> **Marked UNVERIFIED.** Hi-Fi Rush's parry window was searched for and **no frame count
> was found**. Sources describe only the mechanism — parry on the musical beat, with a
> light-blue-circle-over-pink-circle visual convergence cue. **That mechanism is worth
> more to us than the number would have been** and is cited under Q26 for its
> presentation lesson, but Hi-Fi Rush contributes **no timing data** to Q7.

### Interaction with the other five

- **Q6 is the container.** [0.03, 0.15] must stay a strict subset of [0.03, 0.31]. If the
  designer moves Q6, **Q7 does not automatically move** — it is pinned to the *start*, so
  shrinking Q6 to 0.20 s would leave Q7 at 60 % of the window and make perfect dodge feel
  cheap. **Re-check the ratio after any Q6 change.**
- **Q8 is the balancing penalty.** Perfect dodge (+12) and counter (+15) are the two
  high-value defensive reads. Counter pays more; **Q8 is what it costs to be wrong.** If
  Q7 is tight and Q8 is cheap, everyone spams counter. The pair below is tuned so that
  guessing wrong on a counter costs **~0.55 s of exposure** while guessing wrong on a
  dodge costs a **~0.15–0.25 s** tail and no meter.
- **Q26 is the multiplier on this number.** A perfect dodge off cooldown is worth
  **+12 → +32** with the Impact Window chained. Q26 decides how often the chain is live,
  and therefore how much a tight Q7 is worth. **Q7 and Q26 together set the meter's
  entire skill-sensitivity.**
- **Q27 is unaffected** — different phase of the loop.
- **Q28 competes for input attention.** A player buffering a combo link at 0.20 s before
  a section ends and a player watching for a 0.12 s dodge pocket are doing two different
  things with the same hand. **This is a real ergonomic cost and it is the argument for
  Q28 sitting at the generous end of its band.**
- **Open elsewhere:** **Q25** decides where inside Active Attack the damaging trace
  actually lands, which decides where the perfect pocket *is* for each of the four
  attacks. **Q7 is a duration; Q25 is its location.** The two must be validated together
  per attack, which is what the M3 playtest is for. **Q14** (`MontagePlayRate`) scales
  this window exactly as it scales Q6 — same warning, same fix.

**This is a recommendation. The designer decides. Of the six answers in this file, this
is the one most likely to be wrong on paper and most likely to be corrected by ten
minutes of play.**

---

## Q8 — Whiffed-counter recovery

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-20**
- **Value lives in:** `AM_Player_CounterWhiff` — the montage played when a counter is
  input and nothing is there to counter (`design-brief.md` §13.2 row 36)
- **GDD range:** **The GDD publishes no number.** It publishes that *counter* is in the
  shared control model (`gdd/sections/02`, PDF p.2), that a successful counter is worth
  **+15** — **the highest single non-Impact gain in the game** (`gdd/sections/03`, PDF
  p.3) — and that a counter is one of the two events that can open an Impact Window.
  `design-brief.md` §14 offers **0.40–0.70 s** and states the requirement plainly:
  *"must be long enough that spamming counter is worse than reading the telegraph."*

### Proposed value

> **`AM_Player_CounterWhiff` total lockout = 0.55 s** — measured from the input, covering
> the whole whiff montage (startup, empty active window, and recovery), during which the
> player **cannot move, dodge, attack, or counter again** and **takes full damage** (no
> i-frames, no damage reduction).
> Identical for Echo and Nova. Tuning band: **0.50–0.65 s**.

### Why 0.55 s — the arithmetic, not the taste

**The design requirement is falsifiable, so test it.** "Spamming counter must be worse
than reading the telegraph" means: *a counter thrown at the instant the telegraph begins
must still be in whiff recovery when the strike lands.*

The strike lands at `TelegraphLength + (offset into Active Attack)`. Taking the **worst
case for the anti-spam rule** — the shortest legal telegraph and a hit on the first
instant of Active Attack:

| Case | Telegraph | Earliest hit, from telegraph onset | Whiff lockout | Player still locked when the hit lands? |
|---|---|---|---|---|
| **Phase 2 floor** (hardest to defend) | **0.40 s** | **0.40 s** | 0.55 s | **Yes** — locked until 0.55 s ✔ |
| Phase 2 midpoint | 0.575 s | 0.575 s | 0.55 s | Marginal — recovers ~0.03 s before the hit, with no time to act ✔ |
| **Phase 1 floor** | **0.55 s** | **0.55 s** | 0.55 s | Exactly on the boundary ✔ |
| Phase 1 midpoint | 0.75 s | 0.75 s | 0.55 s | **No** — free at 0.55 s, 0.20 s to spare ✘ |
| **Phase 1 ceiling** | **0.95 s** | **0.95 s** | 0.55 s | **No** — 0.40 s to spare, a full second counter fits ✘ |

**Read that table honestly: 0.55 s defeats counter-spam against every Phase 2 telegraph
and against the fast end of Phase 1, and it does *not* defeat it against the slow end of
Phase 1.** Closing the ceiling case would need a lockout of **~0.95 s**, which is
outside §14's band, would feel dreadful, and would make the counter unusable.

**That residual is acceptable and here is why.** A slow Phase 1 telegraph is the
*tutorial* portion of the duel — the place the GDD deliberately gives the player room to
experiment. A player who discovers they can double-tap counter against attack C's long
wind-up has found a legitimate beginner crutch that **stops working the moment Phase 2
commits at 50 % health**. That is the GDD's own escalation doing its job. **Flagged, not
hidden.**

**Where the real cost lands.** The rival's Recover state — the GDD's *"deliberate punish
opening"* — is **0.45–0.90 s in Phase 1 and 0.35–0.75 s in Phase 2**. A 0.55 s whiff
lockout **consumes the entire Phase 2 punish opening and most of the Phase 1 one.** So
the cost of a wrong counter is not primarily "you get hit"; it is **"you lose the punish
you were about to get."** That is a far better teacher, it is visible on the first
mistake, and it costs the player meter (+0 instead of +5 or +15) rather than health.

**Why not 0.40 s or 0.70 s.**
- At **0.40 s** the Phase 2 anti-spam guarantee fails outright — the lockout ends exactly
  as the fastest legal strike lands, so a spammer gets a free second attempt at the
  hardest attack in the game. The whole point of the value is lost.
- At **0.70 s** the lockout exceeds even the **longest Phase 1 recover window (0.90 s)**
  by enough that a single mistimed counter costs the punish *and* leaves the player
  standing still into the next Select Attack. Combined with the Q3 damage table
  (32 % of health for attack A), that is a two-mistake death spiral off one button.
- **0.55 s is the largest value that still fits inside the shortest Phase 2 recover
  window (0.35 s)... it does not**, and that is deliberate — a whiff should cost more
  than the opening it wasted. It is the smallest value that satisfies the Phase 2
  anti-spam test with any margin at all.

### A gap this group found — the counter's own success window has no Q number

`design-brief.md` §13.2 lists **row 36 `AM_Player_CounterWhiff`** but lists **no row for
the counter's *success* window** — the span during which an incoming attack is converted
into a counter. Q7 covers the perfect *dodge*; nothing covers the perfect *counter*.
**The GDD publishes no value for it either.**

> **Question for the designer (no value proposed, and this is a genuine hole in the
> value table, not an oversight by this group).** How wide is the counter's own success
> window, and where does it sit? The structurally consistent answer is the mirror of Q7:
> a window at the **front** of `AM_Player_Counter`, **narrower than the perfect-dodge
> window** because the counter pays more (**+15** vs **+12**) and because whiffing it
> costs 0.55 s where whiffing a dodge costs a ~0.20 s tail. A band of **0.08–0.12 s**
> would preserve that ordering. **This is a range for conversation.** It also needs a
> row adding to `design-brief.md` §13.2 and a Q number of its own — **flagged to the
> commander as a table defect, not resolved here.**

### Prior art (real games, named, with real numbers)

| Game | Mechanism | Real numbers | Seconds | Relevance |
|---|---|---|---|---|
| **Devil May Cry 5** (Dante, Royalguard) | The genre's canonical high-risk counter: a tight "Just Frame" release that nullifies damage and banks it, wrapped in an ordinary block | Perfect-guard window is **exactly 6 frames** — and DMC5 kept it at **the same 6 frames** as earlier entries. What changed is the **penalty**: an ordinary Block no longer takes chip damage and is unbreakable; instead it **drains the Devil Trigger gauge**, and guard breaks only when DT empties. Perfect guard nullifies damage, raises Style rank, and fills Rage faster | Window **0.100 s** | **The most instructive row in this file.** DMC5 made Royalguard usable **not by widening the window but by softening the penalty.** That is the exact trade available to our designer: if 0.12 s (Q7) plus 0.55 s (Q8) proves too punishing, **soften Q8 before widening Q7.** Note also the penalty is a **resource**, not time — an option we do not take, because our meter is a *win requirement* under Q22 and draining it would be a second failure state |
| **Sekiro: Shadows Die Twice** | Anti-spam built into the window itself | Deflect window **12 frames** by default; **each recent guard press shrinks it**, down to **4 frames**, and to **0 frames** under fast spam | 0.200 s → 0.067 s → 0 s | The alternative anti-spam architecture, and one we **explicitly reject**. Window-shrinking is invisible: the player sees identical inputs produce different results and concludes the game is inconsistent. **A visible 0.55 s recovery animation teaches the same lesson legibly.** Cited because it is the strongest evidence that a shipped, well-regarded game considered counter-spam a problem worth engineering against |
| **Street Fighter 6** | Recovery asymmetry as the entire risk model | On a **successful** Perfect Parry the defender recovers in **1 frame** and is invincible **6 frames**, cancellable into any non-Drive attack, while the attacker cannot cancel at all | Recovery **0.017 s**; invincible **0.100 s** | The success case is nearly free — which only works because the failure case is not. Our mirror: a **successful** counter should return control immediately (no `AM_Player_CounterWhiff`, straight into the +15 and the Impact Window fork), and **only the whiff pays the 0.55 s.** The developer must not put recovery on the success path |
| **Fighting-game whiff-punish convention** (general) | Recovery frames are the universal currency of commitment across the genre | Qualitative | — | Supports the shape of the answer: the risk of a defensive option is expressed as **time you cannot act**, not as damage. This is why Q8 is a montage length and not a health penalty |

> **Marked UNVERIFIED / NOT FOUND.** No source in this pass gave a recovery-frame count
> for a **whiffed** parry in Dark Souls, Sekiro, or Street Fighter 6. Those numbers exist
> but were not located inside the research cap. **The 0.55 s proposal is therefore
> derived from the GDD's own telegraph and recover ranges — shown in the table above —
> and is corroborated by prior art only on its *shape*, not its magnitude.** The designer
> should know that this specific number has weaker external support than Q6 or Q7.

### Interaction with the other five

- **Q7 is the option this competes with.** Perfect dodge: **+12**, ~0.20 s vulnerable
  tail on failure. Counter: **+15**, **0.55 s** lockout on failure. **The counter pays
  25 % more and costs roughly 2.75× more to miss.** That ratio is the reason both options
  stay live, and it is the thing to re-check first if playtest shows players using only
  one of them. **If everyone dodges, lower Q8. If everyone counters, raise it.**
- **Q6 sets the safe alternative's price.** See above.
- **Q26 raises the stakes on both.** With the Impact Window off cooldown a counter is
  worth **+35**; on cooldown it is **+15**. **A longer Q26 makes the 0.55 s gamble worse
  on average** — the two numbers pull against each other and should be reviewed together.
- **Q27 is unaffected.**
- **Q28 is unaffected mechanically**, but note the ergonomic point from Q7: three
  different timed inputs (combo link, dodge pocket, counter pocket) is already the
  ceiling of what this control model should ask for. **No fourth timed input should be
  added anywhere.**
- **Open elsewhere:** **Q19** (post-counter Clash-initiation window) means a successful
  counter is also the *entry to the ending*. That raises the value of the counter above
  its +15 and argues for keeping Q8 at the assertive end of its band. **Q25** decides
  the actual telegraph length per attack, which decides which rows of the anti-spam table
  above are real. **The designer should not author all four attacks near 0.95 s in
  Phase 1** — doing so makes counter-spam viable for the first half of every duel.

**This is a recommendation. The designer decides.**

---

## Q26 — Standard Impact Window cooldown

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M3-07**
- **Value lives in:** `BP_ImpactWindowDirector` (`design-brief.md` §13.2 row 54)
- **GDD range:** **The GDD publishes no duration.** It publishes the trigger condition
  verbatim — Standard Impact Window: *"Approved skill event **after cooldown**"* —
  and the response time **0.35–0.50 s**, against the First Impact Window's
  *"First successful perfect dodge or counter"* at **0.75 s**
  (`gdd/sections/02`, PDF p.3). It also publishes the burst length: **1–3 seconds**.
  So **the GDD names the cooldown as a real mechanic and leaves only its duration open.**
  `design-brief.md` §14 offers **3–8 s**; the proposal below falls inside it.

### Proposed value

> **`StandardImpactCooldown = 7.0 s`** · tuning band **6.0–8.0 s**.
> **The clock starts when an Impact Window closes** — on the end of the success burst, or
> immediately on a failed/ignored prompt — **not** when it opens. Success and failure are
> spaced identically; this is a pacing rule, not a punishment, and the GDD's *"No
> extension; return to combat"* is preserved.
>
> **The First Impact Window is exempt.** Per the GDD's **PRESERVED — ONBOARDING RULE**,
> the first window fires on the first successful perfect dodge or counter of the duel at
> **0.75 s** regardless of cooldown state. `BP_ImpactWindowDirector` must hold a
> `bFirstWindowConsumed` flag and skip the cooldown check while it is false. **Applying
> the cooldown to the first window would break a GDD rule.**

### Why 7 s — and what this number is actually for

**First, the finding that reframes the question.** Group 02 asked whether Q26 could make
the meter a real second gate. **It cannot, and no value in the 3–8 s band can.** The
arithmetic is in **"Answering group 02"** below; the short version is that the meter has
**four** faucets and Q26 gates only one of them, so the meter fills from the **+5** row
alone in roughly half the time it takes the health gate to open. **Q26 is not a gate
lever.** Treating it as one would lead the designer to push it to 8 s for a benefit it
cannot deliver.

**What Q26 actually controls is cinematic pacing**, which is what §14 says it controls,
and which is a first-class concern given the project's central promise: *"real-time
martial-arts combat rewards player skill with **brief, earned** anime-style cinematic
spectacle."* Both of those adjectives are Q26's responsibility.

**The cinematic budget, shown.** One Impact event costs the fight
`response window (0.35–0.50 s) + burst (1–3 s)` ≈ **2.5 s** at midpoints. Against group
02's competent-play duel of roughly **200 s** of actual combat:

| Q26 | Min. spacing (cooldown + 2.5 s event) | Theoretical max bursts per duel | Realistic bursts (≈50 % conversion) | Realistic cinematic share of the duel |
|---|---|---|---|---|
| **3 s** | 5.5 s | ~36 | ~18 | **~23 %** |
| **5 s** | 7.5 s | ~27 | ~13 | **~16 %** |
| **7 s** | 9.5 s | ~21 | ~10 | **~13 %** |
| **8 s** | 10.5 s | ~19 | ~9 | **~11 %** |

At **3 s** a skilled player is watching a cinematic roughly **every 5.5 seconds** and
spends nearly a quarter of the duel not playing. Eighteen "earned spectacles" in one
duel is not spectacle; it is the combat loop. **That is precisely the failure §14 warns
about** — *"too short and the cinematic bursts stop feeling earned."*

**The cooldown-versus-rival-cycle threshold — the real design line.** Group 02 measured
the rival's full cycle at **≈ 2.9 s in Phase 1** and **≈ 2.3 s in Phase 2** at GDD
midpoints. So:

| Q26 | Phase 1 cycles per cooldown | Phase 2 cycles per cooldown | What the player experiences |
|---|---|---|---|
| 3 s | **1.0** | **1.3** | The cooldown never really binds — **nearly every perfect dodge chains into +20.** The Impact Window becomes a per-attack reward |
| 5 s | 1.7 | 2.2 | Binds sometimes; the player cannot predict when |
| **7 s** | **2.4** | **3.0** | **The cooldown reliably spans two to three whole attacks.** An Impact Window punctuates a *passage* of combat, not a single exchange |
| 8 s | 2.8 | 3.5 | As above, slightly further apart |

**7 s is the smallest value at which the cooldown reliably spans more than two rival
attacks in both phases.** Below that it is noise; above that the difference is
diminishing. That is the whole argument for the number.

**Why not 8 s.** 8 s is defensible and the designer may prefer it. It is not recommended
because Phase 2's cycle is shorter (2.3 s) and 8 s pushes the Phase 2 gap to **3.5
cycles** — in the phase where the GDD explicitly wants **more** pressure and where the
player's successful reads are hardest earned, going three and a half attacks between
rewards starts to feel like the game stopped paying attention. **7 s keeps Phase 2's
reward density from dropping below Phase 1's in felt terms.**

### The C2 consequence — this cooldown must be visible

A 7 s cooldown is **longer than the player's memory of when they last used it.** With no
indicator, a player who perfect-dodges and gets no prompt will read the game as
inconsistent — the same false-inconsistency problem Sekiro's window-shrinking creates
(see Q8).

> **`WBP_HUD` needs a functional Impact-readiness state as part of M3, not M5.** A
> gray-box text label or an unstyled fill bar is sufficient and is *functional HUD work*,
> not a presentation pass — the same line `design-brief.md` §11.6 draws between asset
> selection and authored presentation. **The styled treatment is M5.** This is the same
> HUD that constraint **C2** already requires for the Clash gate indicator, so it is one
> widget serving two requirements, not new scope.

Hi-Fi Rush is the useful reference for the *shape* of that cue, not its timing: its parry
is signalled by **a light-blue circle converging on a pink circle**, i.e. the game shows
the player the timing rather than expecting them to hold it in their head.

### Prior art (real games, named, with real numbers)

| Game | Mechanism | Real numbers | Relevance |
|---|---|---|---|
| **Batman: Arkham** series | Gates its cinematic finisher on **sustained performance** rather than on a clock | Special Combo moves require **8 combo multipliers** to charge, reduced to **5** with the Special Combo Boost upgrade | **The strongest alternative architecture, and the designer should know it exists.** A performance gate ("N successful reads since the last one") is self-balancing — it is impossible to see the cinematic without earning it, and it needs no HUD timer. **Not proposed here** because our meter *already* is that gate and a second performance gate would double-count the same inputs. But if playtest says a timer feels arbitrary, **"3 successful defensive reads since the last Impact Window" is the swap**, and it is roughly equivalent to 7 s at the measured cycle length |
| **DOOM Eternal** | Ships a repeatable cinematic with **no cooldown at all**, gated purely by enemy state | Glory Kills grant invulnerability **through the entire animation** plus **roughly one second** afterward, and always drop health. The **Savagery** rune exists specifically to **make glory kills faster** | **The cautionary data point, and it is unusually direct.** id shipped an uncapped cinematic and then shipped an upgrade whose entire purpose is to **shorten** it — that is a studio conceding that a repeated cinematic becomes a cost the player wants reduced. Also note the encounter timer *"doesn't stop for the glory kill duration"* in some modes: the animation is real time the player is not playing. **A 3 s Q26 walks into this** |
| **Hi-Fi Rush** | Signals the timing rather than relying on player memory | Parry is timed to the musical beat and cued by **a light-blue circle overlapping a pink circle** | Not a timing source (no frame data was found — see the Q7 unverified note), but the correct model for the **C2 readiness indicator** above |
| **Street Fighter 6** | Caps the payoff of the best defensive read rather than its frequency | A Perfect Parry punish combo takes **50 % damage scaling** | A third architecture: let the reward fire freely but **shrink it**. Rejected here because the GDD fixes the reward at **+20** and this group may not change a published GDD number |

### Interaction with the other five

- **Q7 is the input Q26 gates.** A perfect dodge is worth **+12** with Impact on cooldown
  and **+32** with it clear. At 7 s the player is in the **+12** state about **60 %** of
  the time. **Q7 and Q26 jointly set the meter's skill-sensitivity**, and Q26 is the
  gentler of the two to retune because it changes no timing the player has to execute.
- **Q8** — the counter chain is **+15 / +35** on the same split. A long Q26 makes the
  0.55 s whiff gamble worse on average, so **if Q26 goes to 8 s, consider Q8 at 0.50 s.**
- **Q6** decides how often the player reaches the fork at all.
- **Q27 / Q28** are unaffected.
- **Open elsewhere:** **Q9** (meter decay) — **C1 assumes none**; if decay were added, a
  7 s cooldown becomes a punishing dead zone and this number must drop. **Q20** (Clash
  beat response times) should probably reuse `StandardWindowDuration` rather than
  interact with this cooldown at all; **the Final Clash must not be cooldown-gated** —
  it has its own double gate. The developer must ensure `BP_FinalClashDirector` does not
  consult `BP_ImpactWindowDirector`'s cooldown.

**This is a recommendation. The designer decides.**

---

## Q27 — `ANS_Recover` incoming-damage multiplier

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M2-13**
- **Value lives in:** `ANS_Recover` — the `Anim Notify State` covering the rival's
  Recover state (`design-brief.md` §13.2 row 55)
- **GDD range:** **The GDD publishes no multiplier and never mentions one.** What it does
  publish is the *purpose* of the state: Recover — *"Expose a deliberate punish opening
  after the committed strike"* — and the behavioural rule *"every major offense exposes a
  clear recovery opening"* (`gdd/sections/04`, PDF p.5). Its duration is
  **0.45–0.90 s (Phase 1)** and **0.35–0.75 s (Phase 2)**.
  `design-brief.md` §14 offers **1.0 up to ~1.5** and frames the choice precisely:
  *"Designer decides whether 'punish opening' means extra damage or only safe access."*

### Proposed value

> **`RecoverDamageMultiplier = 1.0` — no bonus. The opening is time, not damage.**
> Authored as an exposed float on `ANS_Recover` (or on `DA_TuningGlobals` and read by it)
> so the designer can raise it without a code change, **but shipped at 1.0.**
> If the designer wants a bonus anyway, see the Q2 consequences below before choosing —
> **1.25 requires Q2 ≈ 1350 and 1.5 requires Q2 ≈ 1600.**

### Why 1.0

**1. The GDD's own words describe access, not damage.** *"Expose a deliberate punish
**opening**"* is a statement about space and time. Nowhere does the GDD say the opening
is more lethal — only that it is there. Choosing 1.0 is the reading that adds nothing the
GDD did not ask for; choosing 1.5 is the reading that invents a system. Under the
project's rule that the human designer owns every number, **the answer that invents least
is the correct default.**

**2. A window multiplier is invisible, and an invisible reward teaches nothing.** This is
the decisive argument. If the player lands the same combo, sees the same animation, hears
the same impact, and gets the same hit reaction, then a 1.5× multiplier is communicated
**only by the rival's health bar moving slightly faster** — a bar the player is not
watching mid-combo, and which under Q22 they have already been told is not the win
condition. The player cannot learn a lesson they cannot perceive.

Contrast what the recover window *already* pays, visibly:

| What the recover window gives the player at 1.0× | Visible? |
|---|---|
| Room to land the **full 3-section combo** instead of bailing after two hits | **Yes** — they see the third animation play |
| The **+5** finisher, which is the only meter the offensive route pays | **Yes** — the meter moves |
| The **2× finisher damage** from Q4, which only lands if the string completes | **Yes** — via the string completing |
| Freedom from having to dodge | **Yes** |

**The recover window is already the best place in the game to be.** It does not need a
hidden multiplier to be attractive; it needs to be *long enough to finish the string in*,
which is **Q25's** job, not Q27's.

**3. Elden Ring's critical multipliers are real prior art — for a mechanic we do not
have.** Critical attacks there deal **2.5–4× a regular attack**; a backstab is **2×
listed damage** and a riposte **3×**. But every one of those is a **distinct input at a
distinct moment producing a distinct animation** — the player presses a button they
otherwise never press and watches a unique attack play. That is a punish *action*, not a
punish *window*. **We have no riposte and SCOPE LOCK forbids adding one.** Citing Elden
Ring in favour of a passive 1.5× is citing it for the opposite of what it does.

**4. Street Fighter 6 goes the other way, and it is the closer analogue.** SF6's Perfect
Parry — the hardest, most spectacular defensive read in a modern fighter — grants a
guaranteed punish that takes **50 % damage scaling**. A shipped, heavily tuned fighting
game decided the correct payoff for a perfect defensive read is **guaranteed access at
reduced damage**. That is `1.0` with the arithmetic rounded in our favour.

**5. It protects group 02's Q2 derivation.** Full arithmetic in **"Answering group 02"**;
the conclusion is that **1.0 is the only value in §14's range at which Q2 = 1200 survives
unchanged.**

### If the designer wants a bonus anyway — the honest options

| Q27 | Effective combo damage (at a realistic ~70 % of combos landing in recover) | Q2 required to hold the 3–5 min target | Verdict |
|---|---|---|---|
| **1.0** | 20.0 | **1200** | **Recommended.** Group 02's derivation stands as written |
| 1.15 | 22.1 | ~1325 | Inside group 02's stated 1100–1400 band, barely. Effect is imperceptible to the player |
| 1.25 | 23.5 | ~1410 | **Just outside** group 02's band. Does pull the scrappy worst case from ~5:24 toward ~5:00, which is a real benefit — but it does so by widening the skill spread, since a scrappy player lands fewer combos in recover and gains less from it |
| **1.5** | 27.0 | **~1620** | **Breaks the derivation.** Outside group 02's band and near the top of §14's 800–2000. The competent run drops to **≈ 1:56** to the gate at Q2 = 1200 — **below the GDD's 3-minute floor** |

**A better-shaped alternative, if the recover window turns out to feel unrewarding.**
Do not reach for Q27. Reach for **Q25**: author the per-attack recover values toward the
**long** end of the GDD's published ranges (Phase 1 toward 0.90 s, Phase 2 toward 0.75 s)
so the full **~1.0 s** combo fits. That is visible, it stays inside the GDD ranges, it
costs no new system, and it makes the punish *feel* bigger by making it *be* bigger.
**Length is the legible lever; multipliers are the invisible one.**

### Prior art (real games, named, with real numbers)

| Game | Mechanism | Real numbers | Relevance |
|---|---|---|---|
| **Elden Ring** | Punish damage delivered as a **distinct critical action**, not a window multiplier | Critical Attacks deal roughly **2.5×–4×** a regular attack. Most weapons deal **2× listed damage on a backstab** and **3× on a riposte**; ripostes are reported as **25–30 % stronger** than backstabs. Weapon Critical stat divides by 100 for the multiplier (Miséricorde **140** → **1.4**, i.e. **+40 %**; Dagger **130**). Dagger Talisman adds a flat **+17 %** to all critical damage | The genre's canonical punish-damage numbers, and the reason they do **not** support a 1.5 on `ANS_Recover`: every one is attached to a **separate input and a separate animation**. A passive window multiplier is a different mechanic wearing the same name |
| **Street Fighter 6** | Caps punish damage after the best defensive read | Perfect Parry punish combo takes **50 % damage scaling**; defender recovers in **1 frame**, invincible **6 frames** | **Direct support for 1.0.** The reward is *guaranteed access*, and the damage is explicitly reduced to stop the read from ending rounds outright |
| **Devil May Cry 5** (Royalguard) | Banks the punish as a **separate resource and a separate release move**, not as a multiplier on ordinary attacks | Perfect guard window **6 frames**; perfect guard nullifies damage, raises Style rank, and **fills the Rage Meter faster** — the payoff is released later via a distinct move | Third confirmation of the pattern: shipped games pay a punish through a **new visible action or a resource**, never through an invisible scalar on the existing one |

### Interaction with the other five

- **Q6 / Q7 / Q8 are all defensive**; Q27 is the only offensive number in this group and
  does not touch them.
- **Q26** is unaffected — the Impact Window's **+20** is a meter gain, not damage, and is
  not scaled by anything here.
- **Q28 is quietly the most affected.** If Q27 were above 1.0, the value of *completing*
  the string inside the recover window would rise sharply, and Q28's buffer would move
  from "convenience" to "required." **At 1.0 the buffer stays a convenience, which is
  where it should be.**
- **Open elsewhere and load-bearing:** **Q2** — see below. **Q25** — the recover
  durations, which this answer explicitly nominates as the better lever. **Q4/Q5** —
  the combo payload this would have multiplied.

**This is a recommendation. The designer decides.**

---

## Q28 — `ANS_ComboLink` input-buffer window

- **Kind:** B (design) · **Status:** **PROPOSED**
- **Unblocks build step:** **M1-18**
- **Value lives in:** `AM_Player_LightCombo` — an `ANS_ComboLink` notify state on each
  montage section (`design-brief.md` §13.2 row 56)
- **GDD range:** **The GDD publishes no number and does not mention input buffering.**
  It publishes the *"light attack sequence"* in the shared control model
  (`gdd/sections/02`, PDF p.2) and the **+5 light-combo finisher**
  (`gdd/sections/03`, PDF p.3) — which together guarantee that the string has a
  **distinct final hit that must be reached** for the player to earn anything from
  offense at all. `design-brief.md` §14 offers **0.15–0.30 s** before each section ends.

### Proposed value

> **`ANS_ComboLink` occupies the final 0.25 s of every montage section** of
> `AM_Player_LightCombo`. An `IA_LightAttack` press while it is active sets
> `bComboQueued`; the section's `Notify End` reads the flag and calls
> `Montage Jump To Section` on the next section.
>
> **State it as a ratio, so it survives a Q5 change:** the buffer should be
> **≈ 75 % of one section's length**. At group 02's proposed Q5 (3 sections, ~1.0 s
> total, ~0.33 s per section) that is **0.25 s**. **If Q5 or Q14 changes the section
> length, recompute from the ratio — do not carry 0.25 s across unchanged.**
>
> Identical for Echo and Nova. Tuning band: **0.22–0.28 s**.

### Why 0.25 s / 75 %

**1. Group 02 handed this number a job, and it is the one number in this group that can
do it.** Their unclosed failure mode is *"the 2-hit-and-bail player"* — a player who
never completes a string, therefore never earns the **+5**, therefore reaches a pinned
rival with an empty meter and no way to win under Q22. They named Q28 as one of four
levers on it, with the instruction *"make finishing the string easy to **input**."*
**A 75 % buffer means the string is effectively a hold-or-mash**: the player cannot fail
to complete it by being slightly out of rhythm. Whether they *choose* to complete it —
against the rival's telegraph — stays the real decision.

**2. The risk of the combo must live in the commitment, not the execution.** Group 02's
arithmetic: the rival's non-threatening window is **≈ 1.73 s in Phase 1** and **≈ 1.28 s
in Phase 2**, against a **~1.0 s** combo. **That 0.28 s of Phase 2 margin is the risk.**
Adding input precision on top of it would be charging the player twice for one decision,
and would make Phase 2 offense collapse exactly where the GDD wants *"learned reads under
stress."*

**3. It is well above every ordinary shipped buffer, which is correct for this audience.**
Street Fighter 6's general input buffer is **4 frames** (a 5-frame window at the tightest
link) = **0.067 s**; dashes and wakeup reversals get **7 frames** (an 8-frame window) =
**0.117 s**; a quarter-circle motion gets **11 frames** = **0.183 s**. Half-circles were
**raised** from 8 to 12 frames and 360s from 25 to **32 frames (0.533 s)** — Capcom
loosening buffers post-design because tight ones were costing players inputs they had
already decided to make. **0.25 s is roughly 15 frames at 60 fps** — above SF6's most
generous ordinary buffer and far above its links. That is deliberate: our player is not a
fighting-game player, has no training mode, and is holding two other timed inputs in the
same hand (Q7's 0.12 s dodge pocket, Q8's counter).

**4. Why not 0.30 s.** At 0.30 s against a 0.33 s section the buffer covers **91 %** of
the section and leaves ~0.03 s of dead zone. Two problems: an accidental double-tap
commits the player to the full **1.0 s** string when they wanted one poke — which in
Phase 2 is a hit taken — and the string stops reading as a *chain* at all, becoming one
long button hold with no felt rhythm. **0.25 s leaves ~0.08 s of dead zone at the start
of each section, which is enough that a deliberate single tap stays a single tap.**

**5. Why not 0.15 s.** At 45 % of a section the player must actually time the link.
That is a fourth execution demand in a control model that already has three, and it
directly worsens the failure mode in point 1. **0.15 s is the value to choose only if
playtest shows players completing strings *accidentally* and getting punished for it.**

### An implementation detail the developer must not get wrong

`ANS_ComboLink` **queues** the input; it does not perform the jump. The jump happens at
section end. Two consequences:

- **The queue must be cleared** on `Notify Begin` of the next section, and on any montage
  interruption (dodge cancel, hit reaction, Impact Window entry). A stale
  `bComboQueued` that survives into the next input is the classic version of this bug and
  it produces "my character attacked when I didn't press anything."
- **`ANS_ActiveHit` and `ANS_ComboLink` overlap in time** on the same section. They are
  independent notify states doing unrelated jobs — one traces, one listens. **Do not
  merge them.** Merging is the shortcut that makes the buffer impossible to retune
  without touching hit detection, and this group's whole purpose is that every number
  here moves without touching logic.

### The `MontagePlayRate` warning, for the third time

Same as Q6 and Q7: a notify state authored at 0.25 s of **montage** time becomes
**0.25 / PlayRate** seconds of **wall-clock** time. If **Q14** gives Nova a play rate
above 1.0, **her sections are shorter *and* her buffer is shorter** — the ratio is
preserved, which is actually the correct behaviour here, unlike Q6/Q7 where the ratio
being preserved is exactly the problem. **Q28 is the one window in this group that scales
correctly with play rate.** Flagged so the developer does not "fix" it.

### Prior art (real games, named, with real numbers)

| Game | Mechanism | Real numbers | Seconds @ 60 fps | Relevance |
|---|---|---|---|---|
| **Street Fighter 6** | Tiered input buffers — precision is the skill, so the buffer is small, but Capcom sized each tier to the difficulty of the input | General buffer **4 frames** (tightest links get a **5-frame** window). Dashes and wakeup reversals **7 frames** (**8-frame** window). Quarter-circle motions **11 frames**. Half-circles raised from **8 → 12 frames**; full circles / 360s raised from **25 → 32 frames** | 0.067 / 0.117 / 0.183 / 0.200 / **0.533** | **The most useful row.** It shows (a) a shipped scale to place 0.25 s against, and (b) that the same studio **enlarged** buffers where the input was harder than the decision behind it. Our combo link is exactly that case: the decision is "commit to the string," the input should not be a second test. **Note the 360 buffer is 0.533 s — more than twice our proposal** |
| **Devil May Cry 5** (Nero, Red Queen) | A fixed-length default string designed to be chained without precision, with the *skill* expressed elsewhere (Exceed, cancels, Devil Breakers) | Combo A is a **4-hit** sword combo; Exceed multiplies Combo A–D attack power by **×1.2** | — | Structural precedent for a forgiving base string carrying no execution tax. Cited via group 02's Q4/Q5 research rather than re-searched here |
| **Batman: Arkham** series | The extreme end — a base string with essentially no timing precision at all, where the entire skill is *target selection and threat reading*, not input timing | Basic strikes build a Freeflow multiplier; a critical strike **adds 3** to the combo meter where most abilities add **1**; Special Combo moves unlock at **8** multipliers (**5** upgraded) | — | The closest match to our design intent: **the string is free, the reads are the game.** Ascendant Impact's difficulty lives in Q7 and Q8, and Q28 should stay out of the way |

> **Marked NOT FOUND.** No source in this pass gave a buffer figure for a *3D action*
> game specifically (Souls, Devil May Cry, God of War input buffer lengths). The SF6
> figures are from a fighting game, where buffers are deliberately **tighter** than in
> action games — so they function as a **floor** for our reasoning, not a target. **The
> 0.25 s proposal is therefore anchored to our own section length (75 %) rather than to
> a matched external number, and the designer should know that.**

### Interaction with the other five

- **Q7 is the ergonomic counterweight.** Three timed inputs is the ceiling. A generous
  Q28 is what makes room in the player's attention for a tight Q7. **If Q7 is tightened
  below 0.12 s, do not also tighten Q28.**
- **Q8** — see the Q7/Q8 note; the player who is buffering a combo is not watching for a
  counter pocket, and that trade-off is the intended texture of the recover window.
- **Q27 at 1.0 keeps this a convenience rather than a requirement.** If Q27 rose, Q28
  would become load-bearing for damage output as well as meter.
- **Q6 / Q26 are unaffected.**
- **Open elsewhere:** **Q5** sets the section length this ratio is taken from —
  **Q28 cannot be finalised before Q5 is approved.** **Q14** scales it correctly, as
  above. **A question with no Q number:** *can a dodge input cancel the combo, and from
  which section?* `design-brief.md` §13.2 assigns no row to this and the GDD is silent.
  **Flagged to the commander as a second table gap** (the first is the counter's success
  window, under Q8). **No value proposed** — but note that if the answer is "no cancel,"
  the ~1.0 s combo becomes a hard commitment and Q28's generosity turns into a trap in
  Phase 2's 1.28 s window.

**This is a recommendation. The designer decides.**

---

## Reaction-time check

**The question:** can a human being actually use a **0.28 s** i-frame window (Q6) and a
**0.12 s** perfect-dodge pocket (Q7) against a telegraph whose Phase 2 floor is
**0.40 s** and whose Phase 1 floor is **0.55 s**?

### The model

Let **t = 0** be the instant the Telegraph state begins — the moment the GDD's
*"committed pose, warning lights, sound, and readable direction"* becomes visible.

| Symbol | Meaning | Source |
|---|---|---|
| **T** | Telegraph length | GDD: **0.55–0.95 s** (P1), **0.40–0.75 s** (P2) |
| **h** | Offset from the start of Active Attack to the damaging trace | **Q25, open.** Active Attack is 0.18–0.45 s, so h ∈ [0, 0.45] |
| **t_hit** | When the hit lands = **T + h** | derived |
| **t_press** | When the player presses dodge | player |

From Q6 and Q7, a dodge pressed at `t_press` gives:
- invulnerable over **[t_press + 0.03, t_press + 0.31]**
- perfect over **[t_press + 0.03, t_press + 0.15]**

Inverting for the press:

```
SURVIVE  (i-frames cover the hit):  t_press ∈ [ t_hit − 0.31 , t_hit − 0.03 ]   → a 0.28 s target
PERFECT  (+12, opens Impact):       t_press ∈ [ t_hit − 0.15 , t_hit − 0.03 ]   → a 0.12 s target
```

**Human reaction band used** (from the reaction-time research cited below): elite/trained
floor **~0.10–0.12 s**; trained gamer **~0.19–0.20 s**; young adult **~0.21–0.22 s**;
general-adult average **~0.25 s**; typical adult range **0.20–0.30 s**.

### The four cases

| Case | T | h | t_hit | **SURVIVE press window** | **PERFECT press window** | Where the 0.20–0.30 s human band lands |
|---|---|---|---|---|---|---|
| **A — hardest legal attack in the game.** Phase 2 telegraph floor, trace on the first instant of Active | **0.40** | 0.00 | **0.40** | **[0.09, 0.37]** | **[0.25, 0.37]** | **Survive: the entire band is inside.** ✔ Perfect: 0.25–0.30 s is inside; 0.20–0.25 s is *early* → plain dodge |
| **B — realistic Phase 2 attack.** Phase 2 floor, trace 0.10 s into Active | 0.40 | 0.10 | 0.50 | [0.19, 0.47] | [0.35, 0.47] | Survive: entire band inside ✔. Perfect: the whole band is **0.05–0.15 s early** → the player must deliberately **wait** |
| **C — Phase 1 floor, realistic trace** | **0.55** | 0.10 | 0.65 | [0.34, 0.62] | [0.50, 0.62] | Survive: **the band is 0.04–0.14 s EARLY and the player gets HIT** ✘ — see below |
| **D — Phase 1 ceiling** | 0.95 | 0.10 | 1.05 | [0.74, 1.02] | [0.90, 1.02] | Reaction is irrelevant; pure timing, ample room |

### What the table says

**1. Q6 survives the check, decisively, at the hardest legal attack.** In Case A the
survive window is **[0.09 s, 0.37 s]** and **every** point in the human reaction band —
including a slow 0.30 s and a sluggish 0.35 s — lands inside it. **A player of any
ordinary reflex can survive the fastest attack the GDD permits, first try, on pure
reaction.** That is the property the i-frame window exists to guarantee and 0.28 s
delivers it.

**2. Q6 also passes a check nobody asked for, and this is the best evidence for 0.28 s
over anything longer.** In Case A the survive window *opens* at **0.09 s**. The elite
human reaction floor is **~0.10–0.12 s**. **It is therefore physically impossible to
react to the telegraph and dodge too early.** Dodging too early requires *pre-emptive
mashing* — dodging before the telegraph, on a guess. So the dodge's failure mode is
cleanly separated: **reaction always works, guessing does not.** A longer i-frame window
would erase that separation and make mashing viable.

**3. Case C is not a failure — it is the design, and it is why the telegraph is a read.**
Against a 0.55 s Phase 1 telegraph, a player who dodges at pure reaction speed (0.25 s)
is invulnerable over [0.28, 0.56] and the hit lands at 0.65 — **they dodge too early and
get clipped on the way out.** This is correct and intended. The GDD's core loop is
*"READ Crimson Vanguard's telegraph → RESPOND"*, not *"react to a flash."* A longer
telegraph demands a *later* press, and the player learns that by being hit twice. **The
i-frame window is a reaction tool only against the fastest attacks; against slow ones it
is a timing tool.** That is a good difficulty curve and the GDD produced it for free by
publishing a telegraph *range* rather than a single value.

**4. Q7 survives the check, and lands in an unusually pleasant place.** In Case A the
perfect pocket **[0.25 s, 0.37 s]** opens **exactly at the average human visual reaction
time of ~250 ms**. Against the hardest attack in the game, an average player perfect-
dodges by reacting as fast as they can; a *fast* player (0.20 s) has to learn to **wait**.
**At the game's hardest moment, speed stops being the skill and timing takes over.**
That is the correct shape for a game whose central promise is that spectacle is *earned*.

**5. In every other case Q7 is an anticipation skill, not a reaction skill.** Cases B, C
and D all require the player to press **later than their reflex would fire** — by 0.10 s
in B, 0.25 s in C, 0.65 s in D. **This is exactly how Sekiro's deflect works** and it is
why the GDD's telegraph requirements (*"distinct wind-up," "visible first beat," "clear
body direction," "thruster cue before movement"*) are load-bearing rather than
decorative. **If the telegraphs are not readable, Q7 is unplayable at any value.**

### The one thing this check could not verify

The check above establishes that the **onset** of the perfect pocket is reachable. It does
**not** establish that a human can hit a **0.12 s** target *repeatably* once they know
where it is — that is motor timing precision, not reaction time, and **no timing-precision
figure was researched within this run's 15-source cap.** It is named as unresolved below.
The proxy evidence is that Street Fighter III shipped a **0.167 s** parry and Sekiro
shipped a **0.20 s** deflect, both of which players demonstrably hit repeatably; **0.12 s
is tighter than both and is the single value in this file most in need of playtest.**

### Consequence for the build order

**M1-19 can be built at these values immediately.** The check shows they are not
obviously wrong, which is all a gray-box needs. **M3 is where they get tuned**, because
M3 is the first milestone where the perfect dodge has a consequence (the meter and the
Impact Window) worth measuring. **Do not spend M1 tuning Q7** — there is nothing to tune
against yet.

---

## Answering group 02

Group 02 handed this group two findings. Both are answered here, with a plain verdict.

### 1. "Q26 makes the +20 Impact row dominant" — partly fixed, and the framing needs correcting

**Their finding:** *"five Impact successes fill the meter outright. If the designer wants
the meter to be a real second gate rather than a formality, the lever is Q26, not any GDD
gain value."*

**Part one — the dominance is real, Q26 = 7 s reduces it, and it cannot be eliminated.**

An Impact Window cannot be self-started; the GDD opens it from *"a perfect dodge, counter,
or approved combo milestone."* So **+20 never arrives alone** — it arrives as a chain,
**+12 → +32** or **+15 → +35**. The question is how often the chain is *available*, and
that is precisely what Q26 sets. Against group 02's measured cycle lengths
(**2.9 s** Phase 1, **2.3 s** Phase 2):

| Q26 | Cooldown in rival cycles (P1 / P2) | Share of defensive reads that can chain | Effective meter per perfect dodge | **Perfect dodges to fill the meter** |
|---|---|---|---|---|
| Impact disabled | — | 0 % | +12.0 | **9** |
| **3 s** (§14 floor) | 1.0 / 1.3 | **~90 %** | **+30.0** | **~4** |
| 5 s | 1.7 / 2.2 | ~50 % | +22.0 | ~5 |
| **7 s — proposed** | **2.4 / 3.0** | **~33 %** | **+18.7** | **~5.4** |
| 8 s (§14 ceiling) | 2.8 / 3.5 | ~29 % | +17.8 | ~5.6 |

**Verdict on part one: Q26 = 7 s moves the Impact route from a ~2.25× speedup over
plain perfect-dodging to a ~1.67× speedup.** That is a real, meaningful reduction in
dominance. It does **not** eliminate it and **must not** — the GDD fixes **+20** as the
largest single gain in the game, so the row is *supposed* to be the best one. What 7 s
removes is the *automatic* chain, where every single defensive read paid double because
the cooldown was shorter than one rival attack.

**Part two — and this is the correction: Q26 cannot make the meter a real second gate,
and no value in §14's 3–8 s band can.**

The meter has **four** faucets and Q26 gates **one**. Take group 02's own pure-offense
measurement: **20 combo finishers at ~0.7 combos/cycle ≈ 29 cycles ≈ 84 s** to a full
meter, against a health gate at **~173 s**. **With the Impact Window disabled entirely —
Q26 = infinity — the meter still fills in roughly half the time it takes the health gate
to open.**

To make the two arrive together you would have to halve every faucet, and every route to
that is closed:

| Lever | Status |
|---|---|
| Lower the gain values +5 / +12 / +15 / +20 | **Forbidden** — GDD-published (`gdd/sections/03`, p.3–4). No agent may change a GDD number |
| Add meter decay | **Forbidden** — constraint **C1** from the APPROVED Q22 decision |
| Raise the ceiling above 100 | **Forbidden** — GDD-published meter range **0–100** |
| Lower Q2 | Moves the **health** gate *earlier* — the wrong direction |
| Raise Q26 past 8 s | Only touches one of four faucets; see the 84 s figure above |

**Verdict on part two: the meter is not a race against the health gate and cannot be made
into one inside the GDD's fixed numbers. It is an anti-passivity floor.** Its job is to
guarantee the player did *something* skilled before the ending unlocks — which is exactly
what the GDD says it is for: energy *"earned only through active combat decisions."*

**This is not a failure of the design; it is what group 02 already found and correctly
called "the safe direction."** Meter-first means the player spends the tail of the duel
attacking, which is progress. Health-first would mean farming meter in front of a rival
pinned at 1 HP, which is the C3 stall.

**The one player for whom the meter *is* an absolute gate** is group 02's 2-hit-and-bail
player, who finishes no strings and takes no defensive reads. **The right response is not
to slow the meter for everybody — it is to close that player's case**, and this group
contributes two of the four levers group 02 named for it:

- **Q28 = 0.25 s (75 % of a section)** makes the string effectively impossible to drop by
  accident, so bailing becomes a *choice* rather than a fumble.
- **The C2 HUD requirement is reinforced under Q26** — a 7 s Impact cooldown *already*
  demands a readiness indicator, so the widget that tells the player "Impact ready" is the
  same widget that tells them "meter is the gate you are missing." **One M3 widget, three
  jobs.**

### 2. "Q27 is a direct scalar on the Q2 derivation" — **Q2 = 1200 SURVIVES**

**Their finding:** *"at §14's upper bound of 1.5 the 45-combo count drops toward ~30.
Q27 should be resolved before Q2 is locked."*

**Confirmed as arithmetic, and answered: this group proposes Q27 = 1.0.**

> ## **Q2 = 1200 survives, unchanged.**
> **At Q27 = 1.0 the scalar is unity and group 02's Q2 derivation is untouched.** Every
> number in their Q2 and Q4 sections — 45 combos to the gate, 30 to Phase 2, ≈ 2:53
> competent, ≈ 4:29 scrappy — **stands exactly as written.** Group 02 may consider its
> tension #6 resolved in its own favour.

A second, quieter benefit worth naming. Effective combo damage is
`20 × [ f × Q27 + (1 − f) × 1.0 ]`, where **f** is the fraction of combos landing inside
`ANS_Recover` — a quantity **nobody has measured and nobody can measure before M3**. At
**Q27 = 1.0 the bracket equals 1.0 for every value of f.** **Q27 = 1.0 removes an
unmeasured variable from the duel-length model entirely**, which is worth something on
its own with a 1 September ship date.

**What happens if the designer overrides this group and takes a bonus anyway:**

| Q27 | Effective combo damage (f ≈ 0.7) | Combos to the ≤25 % gate | Competent time to gate | **Q2 needed to hold ≈ 2:53** | Verdict on Q2 = 1200 |
|---|---|---|---|---|---|
| **1.0** | **20.0** | **45** | **2:53** | **1200** | **SURVIVES** ✔ |
| 1.15 | 22.1 | 41 | 2:37 | ~1325 | Survives only at the top of group 02's 1100–1400 band |
| 1.25 | 23.5 | 38 | 2:27 | ~1410 | **Just outside** group 02's band |
| **1.5** | **27.0** | **33** | **2:08** | **~1620** | **DOES NOT SURVIVE.** Outside group 02's band; a strong player (f → 1.0) reaches the gate at **1:55** and finishes near **2:50 — below the GDD's 3-minute floor** |

Group 02's *"toward ~30 combos"* estimate at 1.5 is confirmed: the exact figure is
**33 at f = 0.7** and **30 at f = 1.0**.

**One thing Q27 = 1.0 does NOT fix, stated honestly.** Group 02's tension #3 — the
scrappy worst case overshooting to **~5:24** — is *not* helped by this answer. Q27 = 1.25
would trim it by roughly 25 s and it would **still** overshoot 5:00, and it would trim the
competent run further at the same time, so it buys nothing net. **Q27 is not the fix for
the scrappy tail. Group 02's own alternative — trimming Q2 toward 1050–1100 — is, and
that decision stays with the designer and with group 02's Q2 entry.**

### 3. Two feedbacks group 02 asked for without framing them as questions

- **"Tune Q7 first, then revisit Q1."** Done, in the direction they wanted. Q7 is proposed
  **mid-band at 0.12 s**, not at the tight end, and the reaction-time check shows Q6's
  0.28 s i-frame window is reachable by pure reaction across the **entire** human band at
  the hardest legal attack. **Q1 = 100 and the Q3 table (A 32 / B 25 / C 27 / D 18) hold
  as proposed.** No revision needed.
- **The "A = 34 %, 3-hit-kill" variant they offered but did not recommend.** At Q7 = 0.12 s
  it is survivable, but **do not take it before playtest.** Q7 is the number most likely
  to move, and moving A at the same time would make the resulting difficulty change
  unattributable. **Change one at a time.** Leave A at 32.

---

## The six proposed values, in one place

| Q | Value | Lives in | Unblocks | Status |
|---|---|---|---|---|
| **Q6** | Dodge i-frames **0.28 s**, spanning **[0.03 s, 0.31 s]** of `AM_Player_Dodge` (band 0.24–0.32) | `ANS_IFrame` | M1-19 | **PROPOSED** |
| **Q7** | Perfect-dodge sub-window **0.12 s**, spanning **[0.03 s, 0.15 s]** — the front 43 % of the i-frame window (band 0.10–0.15; **start playtest at 0.15 and tighten**) | `ANS_PerfectDodge` | M1-19 | **PROPOSED · BLOCKING** |
| **Q8** | Whiffed-counter lockout **0.55 s**, full damage taken, no action permitted (band 0.50–0.65) | `AM_Player_CounterWhiff` | M1-20 | **PROPOSED** |
| **Q26** | Standard Impact Window cooldown **7.0 s**, clock starting on window **close**; **first window exempt** (band 6.0–8.0) | `BP_ImpactWindowDirector` | M3-07 | **PROPOSED** |
| **Q27** | `ANS_Recover` incoming-damage multiplier **1.0** — no bonus; the opening is time, not damage | `ANS_Recover` | M2-13 | **PROPOSED** |
| **Q28** | `ANS_ComboLink` buffer = final **0.25 s** of each section ≈ **75 % of section length** (band 0.22–0.28) | `AM_Player_LightCombo` | M1-18 | **PROPOSED** |

**All six are recommendations. The human designer of record decides all six, and each
stays open in `TODO.md` marked PROPOSED until they do.**

### Two table defects found while answering, flagged to the commander

Neither is a question this group was given; both are **missing rows** in
`design-brief.md` §13.2 that the build will hit.

1. **The counter's own success window has no row and no Q number.** Q7 covers the perfect
   *dodge*; nothing covers the perfect *counter*. Suggested band for conversation:
   **0.08–0.12 s**, at the front of `AM_Player_Counter`, narrower than Q7 because the
   counter pays +15 and costs 0.55 s to miss. **No value proposed.**
2. **Whether a dodge input can cancel `AM_Player_LightCombo`, and from which section, has
   no row and no Q number.** The GDD is silent. It materially changes whether Q28's
   generosity is a kindness or a trap in Phase 2's 1.28 s window. **No value proposed.**

A third, smaller gap: **the total length of `AM_Player_Dodge`** (see Q6) has no row
either. `ANS_IFrame` is a window inside a montage whose length nobody has specified.

---

## Sources

Researched by WebSearch on 2026-08-02. **15 searches used against a 15-source cap — the
cap was reached and research was stopped.** Everything not found inside it is listed
under "What is still unresolved" below rather than guessed at.

**Dodge and i-frame windows**
- [Dodging Tips and Tricks — Elden Ring Wiki (Fextralife)](https://eldenring.wiki.fextralife.com/Dodging)
- [Elden Ring Invincibility Frame Guide: How I-Frames Work — ScreenRant](https://screenrant.com/elden-ring-invincibility-iframe-guide/)
- [Rolling — Dark Souls Wiki (Fandom)](https://darksouls.fandom.com/wiki/Rolling)
- [Dark Souls 3: Equipment Weight Thresholds — TheGamer](https://www.thegamer.com/dark-souls-3-weight-ratio-dodge-roll/)
- [Invincibility frames — DARK SOULS III General Discussions (Steam)](https://steamcommunity.com/app/374320/discussions/0/1733217528121996749/)
- [Evade Window — Monster Hunter World Wiki (Fextralife)](https://monsterhunterworld.wiki.fextralife.com/Evade+Window)
- [Evade Window — MH:World (Kiranico)](https://mhworld.kiranico.com/en/skilltrees/my39A/evade-window)

**Perfect-dodge, parry and counter windows**
- [Deflection — Sekiro Shadows Die Twice Wiki (Fextralife)](https://sekiroshadowsdietwice.wiki.fextralife.com/Deflection)
- [What's the exact timing with the parry window? — Sekiro (Steam)](https://steamcommunity.com/app/814380/discussions/0/3270186319532361490/)
- [Drive Parry — Street Fighter Wiki (Fandom)](https://streetfighter.fandom.com/wiki/Drive_Parry)
- [Street Fighter 6: How To Land Perfect Parry — eXputer](https://exputer.com/guides/street-fighter-6-perfect-parry/)
- [Witch Time — SmashWiki](https://www.ssbwiki.com/Witch_Time)
- [Bayonetta (SSBU)/Down special — SmashWiki](https://www.ssbwiki.com/Bayonetta_(SSBU)/Down_special)
- [Ghost of Tsushima: How To Perfect Parry Enemy Attacks — ScreenRant](https://screenrant.com/ghost-tsushima-perfect-parry-easy-guide/)
- [Nioh 2 Burst Counter Guide: Feral, Phantom, and Brute — GameSkinny](https://www.gameskinny.com/tips/nioh-2-burst-counter-guide-how-to-use-feral-phantom-and-brute-counters/)
- [Timing the Feral Burst Counter — Nioh 2 (Steam)](https://steamcommunity.com/app/1325200/discussions/0/3115898081230386674/)
- [Royalguard Style — Devil May Cry Wiki (Fandom)](https://devilmaycry.fandom.com/wiki/Royalguard_Style)
- [Just Frame — Devil May Cry Wiki (Fandom)](https://devilmaycry.fandom.com/wiki/Just_Frame)
- [How to parry in Hi-Fi Rush — Dot Esports](https://dotesports.com/general/news/how-to-parry-in-hi-fi-rush)
- [Hi-Fi Rush: How to Parry — NintendoSmash](https://nintendosmash.com/hi-fi-rush-how-to-parry/)

**Cinematic burst gating and pacing**
- [Special Combo Moves — Arkham Wiki (Fandom)](https://arkhamcity.fandom.com/wiki/Special_Combo_Moves)
- [Special Combo Takedown — Arkham Wiki (Fandom)](https://arkhamcity.fandom.com/wiki/Special_Combo_Takedown)
- [Glory Kill — Doom Wiki (Fandom)](https://doom.fandom.com/wiki/Glory_Kill)
- [Glory kill — The Doom Wiki at DoomWiki.org](https://doomwiki.org/wiki/Glory_kill)

**Punish-damage multipliers**
- [Critical Damage Guide — Elden Ring Wiki (Fextralife)](https://eldenring.wiki.fextralife.com/Critical+Damage)
- [Critical Attack — Elden Ring Wiki (Fandom)](https://eldenring.fandom.com/wiki/Critical_Attack)
- [Elden Ring: Best Riposte Weapons — eXputer](https://exputer.com/guides/elden-ring-best-riposte-weapon/)

**Input buffers**
- [Street Fighter 6/Game Data — SuperCombo Wiki](https://wiki.supercombo.gg/w/Street_Fighter_6/Game_Data)
- [Street Fighter 6/Offense — SuperCombo Wiki](https://wiki.supercombo.gg/w/Street_Fighter_6/Offense)
- [Here's a breakdown of why players are having trouble with Street Fighter 6's inputs — EventHubs](https://www.eventhubs.com/news/2023/jun/17/sf6-input-trouble-breakdown/)

**Human reaction time**
- [Average Reaction Time by Age, Gender & Activity (2026 data) — reaction-time-test.io](https://www.reaction-time-test.io/average-reaction-time)
- [How Fast is Human Reaction Time? — PubNub](https://www.pubnub.com/blog/how-fast-is-realtime-human-perception-and-technology/)
- [Reaction Time — IHMC (PDF)](https://www.ihmc.us/wp-content/uploads/2021/03/2021-03-Reaction-Time-2.pdf)
- [Average Reaction Time by Age (2026) — MeasureHuman](https://measurehuman.com/guides/average-reaction-time-by-age)

### What is still unresolved — the research cap was reached

**Fifteen sources were enough for Q6, Q7, Q26, Q27 and Q28, and thin for Q8.** These gaps
are named rather than filled:

1. **Whiffed-parry / failed-counter recovery frame counts in any shipped game.** Not
   found. **Q8's magnitude (0.55 s) is derived from the GDD's own telegraph and recover
   ranges, not from prior art.** Its *shape* is corroborated; its *size* is not. This is
   the weakest-supported number in the file.
2. **Hi-Fi Rush parry window frame data.** Not found. Only the mechanism (beat timing,
   converging circles) is cited, under Q26.
3. **Bayonetta's own — non-Smash — Witch Time and dodge frame data.** Not found. The
   Smash Ultimate figures are a different studio's reimplementation and are cited as
   structural evidence only.
4. **The framerate basis of Dark Souls III's "13 i-frames."** Ambiguous; the 30 fps and
   60 fps readings differ by a factor of two. **Marked AMBIGUOUS under Q6. No value in
   this file depends on resolving it.**
5. **Ghost of Tsushima's "1–2 frame" perfect parry.** **Marked UNVERIFIED.** Guide and
   forum sources only, and the same sources give a contradictory "half a second"
   description.
6. **Input buffer lengths for 3D action games** (Souls, Devil May Cry, God of War). Not
   found. Q28 is anchored to our own section length (75 %) rather than to a matched
   external number; the SF6 figures function as a floor, not a target.
7. **Human motor *timing precision* literature** — how repeatably a trained person can
   hit a known 0.12 s target. **Not searched; out of budget.** This is the missing half
   of the Q7 reaction-time check and the most valuable single thing a future research
   pass could add.
8. **Q7 shipped-comparison breadth.** Five parry windows were gathered (Sekiro, SF6,
   SF3, Smash-Bayonetta, Ghost of Tsushima). More would sharpen the recommendation but
   would not change its band.

---

## Constraint compliance

| Constraint | How this file complies |
|---|---|
| **SCOPE LOCK** | One player, one authored rival, one arena, one shared framework, four attacks A–D, one duel. **Every one of the six values is a single shared number** — Echo and Nova have identical i-frames, identical perfect-dodge windows, identical counter recovery, identical combo buffer. Per-fighter defensive timing is named as the thing **not** being designed, and Q6 states explicitly that these values must not live on `DA_FighterProfile`. No fifth attack, no second move set, no new mechanic. Two features considered and **explicitly deferred**: an adaptive perfect-dodge window (Q7) and a performance-gated Impact Window in place of a timer (Q26) |
| **No runtime AI-model calls** | Nothing here is adaptive, learned, or generated at runtime. Every value is a static duration on an `Anim Notify State`, a montage, or a Blueprint float. **Q7 explicitly rejects a window that widens after N failures**, names it as deferred future scope, and does not design it. Crimson Vanguard remains deterministic authored logic |
| **Numbers unchanged** | Every GDD number is reproduced verbatim and used as a fixed input: the six state ranges for both phases, 0.75 s / 0.35–0.50 s / 1–3 s for Impact Windows, +5 / +12 / +15 / +20 / +0, 0–100, 50 %, 100 AND ≤25 %, 1 HP / 50 / 3 s, 3–5 minutes. **None was altered.** Q26 explicitly refuses to change a GDD gain value even where doing so would have answered group 02's gate question |
| **Designer owns every number** | All six are marked **PROPOSED**, each section says so in its own words, the summary table says so again, and three genuinely missing values (dodge montage length, counter success window, combo dodge-cancel rule) are surfaced as **questions with ranges and no recommendation** rather than silently invented |
| **Q22 binding** | Every answer is reasoned inside the permanent 1 HP floor: the meter is treated as a **win requirement**, defensive windows as **meter faucets**, and C1 (no decay) is assumed and its dependency flagged. C2's HUD is reinforced as mandatory by Q26 |
| **Milestone order M1→M5** | Q6/Q7 unblock M1-19, Q8 unblocks M1-20, Q28 unblocks M1-18, Q27 unblocks M2-13, Q26 unblocks M3-07. The one HUD requirement raised (Impact readiness) is specified as **functional gray-box work in M3** with the styled treatment explicitly left to **M5**. No presentation work is designed |
| **This is Ascendant Impact** | Agent Echo, Agent Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, the Ascension Meter, Impact Windows, the Final Clash, Phase 2 at 50 %. No content from any other project appears |

---

*End of group 03. Every value here remains the human designer's to approve, change, or
reject.*
