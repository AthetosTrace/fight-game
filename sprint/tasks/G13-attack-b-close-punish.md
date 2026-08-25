---
id: G13
track: G
title: Vanguard attack B — the close-range punish
status: todo
assignment: 10
editor-required: true
depends-on: [G12]
---

## Goal

A second Vanguard attack that makes standing right next to it dangerous. Faster windup,
shorter reach, less damage than A.

## Why it matters

The Vanguard has **one** attack, on a 2.5–4.0 s cooldown, with a 1.1 s telegraph. Once a
player reads it, the fight has no further content — back off, wait, punish, repeat. One
attack is a demo. Two attacks with different correct responses is a fight.

Attack B already has approved design metadata in the A06 CSV: *"Committed forward-pressure
sequence... visible first beat and stable tracking limit... each beat individually
dodgeable."*

## Preconditions

- `G12` complete — attacks come from the table, so this is a row plus a branch.

## Steps

1. Enable `Row_B` and give it values that make it a genuinely different threat:
   shorter windup (roughly 0.5–0.6 s against A's 1.1), shorter range (roughly 140 against
   A's 240), lower damage (roughly 6 against A's 10), shorter cooldown.
2. Selection: the driver picks by range band, not at random. Inside roughly 150 cm → B is
   eligible. Beyond that → A. Weight the overlap so it is not perfectly predictable.
3. Telegraph must be **visually distinct** from A. A different glyph, colour or scale —
   with a 0.5 s windup the player cannot read it any other way. This is the single most
   important detail in the task.
4. Reuse the existing impact path. Do not author a new damage system.

## Done when

- [ ] B fires only at close range, A only at longer range, with a deliberate overlap.
- [ ] B's telegraph is distinguishable from A's at a glance.
- [ ] Standing next to the Vanguard is now punished; backing off is a real decision.
- [ ] Both attacks still land damage exactly once per strike.
- [ ] All values live in the DataTable, none hardcoded.

## Log

- 2026-08-24 — created.
