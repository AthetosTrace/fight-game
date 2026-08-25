---
id: G15
track: G
title: Player block — the defensive option
status: todo
assignment: 10
editor-required: true
depends-on: [G13]
---

## Goal

Hold a key to reduce incoming damage while rooted in place.

## Why it matters — and why this is the cut line

With three Vanguard attacks and only movement to answer them, the fight risks reading as
unfair rather than hard.

**But be honest about whether it is needed.** The player already has two answers: retreat
against a 1.1 s telegraph, and jump-over side switching. `G13` and `G14` are deliberately
built so spacing *is* the defensive game. Block adds depth; it does not rescue anything.

**This is the first task to cut if the schedule slips.** Cut order is `G09` audio, then
`G15` block, then `G14` attack C. Say so plainly rather than half-building it.

## Preconditions

- `G13` complete, so there is something worth blocking.
- Honest answer to: does the fight already feel fair with spacing alone? If yes, skip it.

## Steps

1. New input action. Hold to block. Rooted while held — no movement, no jump, no punch.
2. Damage taken while blocking scaled down, not to zero. Zero makes holding block
   dominant.
3. Visual state so the player can see they are blocking. Even a colour change is enough at
   graybox.
4. It must not break the KO path, the crossing state or the side rule — those are all
   proven and re-validating them is the real cost here.
5. Re-run the `G05` restart check afterwards. Block state must reset with everything else.

## Done when

- [ ] Holding block reduces damage and roots the player.
- [ ] Blocking cannot be combined with movement, jump or punch.
- [ ] Block state clears on KO and on restart.
- [ ] Crossing, side ownership and knockout all still behave as before.

## Log

- 2026-08-24 — created, and marked as the intended cut if time runs short.
