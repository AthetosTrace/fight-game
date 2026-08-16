# The *Ascendant Impact* combat-copy style guide

**Scope:** every word the player reads during the duel — Impact Window prompts,
Ascension Meter feedback, the Phase 2 callout, the Final Clash unlock, the
failed-Clash recovery line, and the win/loss screens.

**Source:** `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` v0.4
(2026-07-24), extracted to `gdd/`. Every rule below cites a section and page.
Nothing here was invented for this assignment; the machine-readable copy is
[`pipeline/contracts/style_rules.json`](pipeline/contracts/style_rules.json), and
`retrieval.py` checks each citation against the extracted text on every run.

---

## The game these rules belong to

The player picks **Agent Echo** (6'0", precision and controlled timing) or
**Agent Nova** (5'8", speed and aggressive momentum) — both **Ascendant
operatives** — and enters the industrial arena called the **Shattered Ring** to
fight **Crimson Vanguard / Project Valor-7** (6'10", armor, pressure,
overwhelming force) in one complete third-person duel lasting three to five
minutes.

The operatives are there for a reason the GDD states plainly: they are
*"entering the Shattered Ring to survive a live combat evaluation against Project
Valor-7, an armored Vanguard unit designed to push enhanced fighters beyond their
operational limits."* (§01, p2)

That word — **evaluation** — is why this copy does not cheer. Nobody in the
fiction is celebrating the player. They are being assessed.

The high-concept line is the voice target:

> **Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.**
> — §01, p1

Three declaratives. No punch-up. Every rule below is downstream of that sentence.

---

## Constraint type 1 — Tone

### T1. Spectacle is earned, never granted

> Pillar 1, **Skill Creates Spectacle**: *"Readable timing and deliberate
> decisions earn the strongest visual rewards."* — §01, p1

The reward for playing well **is the spectacle**. Copy that hands out praise has
quietly changed what the game rewards — it substitutes applause for the thing
the player actually earned.

State what happened. Do not congratulate.

| Off-brand | On-brand |
|---|---|
| `Nice work! Counter landed.` | `Counter landed. Ascension rising.` |
| `Great job — Final Clash ready!` | `FINAL CLASH READY - COMMIT` |
| `Awesome! Crimson Vanguard is down.` | `Crimson Vanguard is down.` |

Banned outright: *great job, nice work, well done, good job, amazing, awesome,
incredible, fantastic, excellent, brilliant, you're crushing it, you got this,
keep it up, way to go, nailed it, impressive, wow.*

**Edge case that matters:** the loss screen. A player who just lost must not be
told they did well. This is the rule's sharpest test, and it is why T1 is
weighted above every other tone rule.

### T2. The register is clipped and declarative

> *"Choose an Ascendant operative. Survive one complete duel. Earn the
> spectacle."* — §01, p1

**Zero exclamation marks. Zero emoji.** Not "sparingly" — zero. The GDD's own
line lands three beats without one, and every exclamation mark in combat copy is
the game shouting where the fiction is measuring.

### T3. State facts, do not hedge

Combat copy is read under Phase 2 pressure. It asserts what happened or what to
do. It never suggests, softens, or asks.

Banned: *maybe, perhaps, you might want to, try to, you could, if you want,
probably, sort of, kind of.*

| Off-brand | On-brand |
|---|---|
| `Maybe try the counter.` | `Counter landed. Ascension rising.` |
| `You might want to strike now.` | `IMPACT WINDOW - STRIKE NOW` |

---

## Constraint type 2 — Vocabulary and lore

### V1. Use the game's proper nouns, not genre defaults

Every system has a name the GDD fixed. Reaching for the genre word is off-brand
by definition: a stranger reading it could not tell which game it belongs to.

| Never write | Always write | Fixed at |
|---|---|---|
| super meter, super bar, power meter, energy bar, ultimate meter | **Ascension Meter** | §03, p3 |
| QTE, quick time event, button prompt, cinematic prompt | **Impact Window** | §03, p3 |
| ultimate, ult, finisher, super move, special move | **Final Clash** | §03, p3 |
| the boss, the enemy, the opponent, the AI | **Crimson Vanguard** | §01, p1 |
| the stage, the level, the map, the arena floor | **the Shattered Ring** | §01, p1 |
| round 2, round two, stage 2, second stage | **Phase 2** | §03, p4 |
| the player, the character, the hero | **Ascendant operative** | §01, p2 |

### V2. The slot's own subject must be named

Each slot exists to tell the player about one specific system. Copy that never
names it has failed its job, however well written. `The it broke.` is a
sentence; it is not a failed-Clash line.

Required terms are listed per slot in the contract.

### L1. The Ascension Meter is earned, never passive

> *"Ascension Meter is a visible 0–100 resource earned only through active
> combat decisions. It does not fill from waiting or elapsed time."* — §03, p3

Meters in other games charge. This one does not, and copy that implies it
teaches the player a rule *Ascendant Impact* does not have.

Banned: *fills over time, charges over time, builds passively, fills
automatically, regenerates, wait for your meter, let it charge.*

### L2. A failed Final Clash does not restart the duel

> *"A failed Final Clash does not restart the duel, kill the player
> automatically, or leave either fighter in a cinematic state. It creates a
> meaningful meter setback, restores valid combat states, and preserves a
> recoverable path to victory."* — §03, p4

Failure separates both fighters, holds Crimson Vanguard at a 1 HP floor, reduces
the meter to 50, and applies a three-second cooldown. Then combat resumes.

Banned: *restart the duel, start over, from the beginning, back to the start,
the duel resets, you are dead.*

### L3. The Final Clash gate is both conditions, never one

> *"The Final Clash becomes available only when BOTH conditions are true:
> Ascension Meter is full at 100 AND Crimson Vanguard's health is at or below
> 25%. If one condition is met first, the Clash remains locked until the other
> is met."* — §03, p3

Copy presenting a full meter alone as the unlock is wrong. **This rule collides
with L4 inside the 36-character budget, and that collision is unresolved on
purpose** — see *Known conflict* below.

### L4. No numeric gameplay values in player copy

> *"Provisional gains remain subject to playtest tuning."* — §03, p3

Every meter value in the GDD is provisional. Copy that prints one promotes an
unapproved number to a shipped promise. `+15` on screen is a commitment the
designer never made.

Exempt: **Phase 2** (a name, not a value) and **Valor-7** (a designation).

This is the same restraint rule Assignment 06 enforced on the attack table,
applied to prose.

---

## Constraint type 3 — Formatting and length

### F1. Every slot has a hard character limit

> Pillar 2, **Cinematic Rhythm**: *"Brief camera, hit-stop, impact-frame, and
> VFX bursts punctuate combat without replacing it."* — §01, p1

On-screen text is bound by the same pillar. A line long enough to be *read
instead of fought* has replaced the combat rather than punctuating it.

### F2. Two shapes, and a slot may only use its own

| Shape | Rules | Used by |
|---|---|---|
| **banner** | ALL CAPS, at most 6 words, no terminal period | HUD callouts |
| **sentence** | Starts capitalised, ends with a period, at most 2 sentences | Feedback and screens |

Mixing them breaks the HUD's visual grammar and costs the reader a beat
mid-fight. Shouted prose (`THE CLASH BROKE. REBUILD ASCENSION.`) is neither
shape and is rejected as such.

### The slots

| Slot | Shape | Limit | Must name | Reference line |
|---|---|---:|---|---|
| `impact_window_prompt` | banner | 28 | Impact Window | `IMPACT WINDOW - STRIKE NOW` |
| `meter_feedback_counter` | sentence | 40 | Ascension | `Counter landed. Ascension rising.` |
| `phase2_callout` | banner | 48 | Phase 2, Crimson Vanguard | `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER` |
| `final_clash_unlock` | banner | 36 | Final Clash | `FINAL CLASH READY - COMMIT` |
| `clash_failure_recovery` | sentence | 72 | Clash, Ascension | `The Clash broke. Return to neutral and rebuild Ascension.` |
| `loss_screen` | sentence | 72 | Crimson Vanguard | `The evaluation ends here. Crimson Vanguard still stands.` |

Every reference line above scores a clean **10.0** against this guide — there is
a test that fails the build if one stops doing so.

---

## Known conflict — L3 against L4, and why it is not resolved here

Correcting a Final Clash unlock line means stating **both** gate conditions. The
health half cannot be stated inside 36 characters without printing the **25%**
threshold — and L4 forbids printing it, because §03 marks every such value
provisional.

Two rules in this guide cannot both be satisfied in that slot. Neither is wrong.

The pipeline does **not** pick a winner. It stops with
`HUMAN_REVIEW_REFINER_REFUSED` and says which decision is waiting:

> Raise the character budget, or approve 25% as shipped copy.

Both are the designer's calls. See
[`evidence/runs/final-clash-unlock-seed4/`](evidence/runs/final-clash-unlock-seed4/run.md).

---

## What this guide will not decide

Three things are open, and the pipeline refuses rather than settling them:

1. **Any meter gain, damage, timing, or threshold number** — §03 marks them all
   provisional and subject to playtest tuning.
2. **Crimson Vanguard's shorter in-combat UI label** — `CLAUDE.md` records it as
   an open gap. Inventing a short form to fit a character budget would settle it
   by accident.
3. **The Shattered Ring's history and Project Valor-7's origin** — the GDD
   defines neither. No copy in this guide needs them, and none may invent them.
