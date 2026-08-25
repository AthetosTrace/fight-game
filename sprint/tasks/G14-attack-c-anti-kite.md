---
id: G14
track: G
title: Vanguard attack C — the advancing anti-kite
status: todo
assignment: 10
editor-required: true
depends-on: [G13]
---

## Goal

An attack that closes distance, so retreating forever stops being a winning strategy.

## Why it matters

This is the hole the old design work already found. `SESSION-RESUME.md` flagged it as
items 49 and 67: a rival slower than the player **can be kited forever and the duel cannot
end.** The Vanguard advances at 300 cm/s; the player runs at 600. Right now, backing away
is unbeatable. With A and B both being stationary attacks, a patient player never loses.

Fixing it with an attack is better than raising the Vanguard's speed, because it stays
readable and it stays a decision.

## Preconditions

- `G13` complete.

## Steps

1. Enable `Row_C`. Long windup (roughly 1.3–1.5 s — it must be readable *because* it is
   dangerous), long reach, and forward travel during the active window.
2. Selection: eligible only when separation is **large** and the player has been retreating.
   A simple retreat check is enough — do not build a behaviour tree for this.
3. The travel must respect the arena clamp and the minimum separation of 78. It must not be
   able to shove the player through `CombatAxisMax`. This is the most likely bug in the
   task; test it against the wall specifically.
4. Correct response is jumping over it or moving toward it — not backing up. Verify both
   read as viable.

## Done when

- [ ] Retreating in a straight line no longer wins reliably.
- [ ] C only fires from long range and only after retreat, not at random.
- [ ] The advance cannot push either fighter out of the arena or inside min separation.
- [ ] Jumping over C works as an answer.
- [ ] Values in the DataTable.

## Log

- 2026-08-24 — created. The kiting hole is a known open item from the original design pass
  (`SESSION-RESUME.md` items 49 and 67), never closed.
