---
id: N02
track: N
title: Narrative engine — the ledger and the reactive DM
status: todo
assignment: 08
editor-required: false
depends-on: [N01]
---

## Goal

A virtual Dungeon Master agent that tracks what the player *does* in a JSON facts ledger
and lets that tracked state change how it narrates.

## Why it matters

Assignment 08, due **25 Aug**. Rubric: State Tracking 4.0, Reactive Dialogue 3.0,
Consistency 2.0, ReadMe 1.0.

## Preconditions

- `N01` complete — key working, usage helper importable.

## Steps

1. **Set it in the Ascendant Impact world.** The assignment permits it ("may adapt it
   later"), the GDD supplies the worldbuilding for free, and any lines it generates —
   Vanguard taunts, round callouts — become candidates for the shipped build, which
   strengthens A10's Pipeline-to-Game Connection. Cheaper and worth more.
2. Design the ledger schema first, before any prompt. Track *actions and their
   consequences*, not conversation history: what the player did, who now trusts or fears
   them, what is broken, what is owed. The rubric's example is betrayal versus loyalty —
   the ledger must be able to hold that kind of fact and act on it many turns later.
3. Ledger updates must be **automatic** — a structured extraction step after each player
   turn, not the model being asked politely to remember.
4. Narration reads the ledger as explicit context every turn. The distinction the rubric
   draws is responses changing on *ledger state*, not just on the most recent input.
   Design so that is demonstrable.
5. **Print or log the ledger every turn.** "The ledger state must be visible in the output
   or logs" is worth 4 points and is the easiest thing to lose by accident.
6. Route every call through the `N01` helper.

## Done when

- [ ] Ledger is JSON, updates automatically from player actions, and is visible in output
      or logs every turn.
- [ ] A demonstrable case where two different ledger states produce genuinely different
      narration from the same player input.
- [ ] Every API call is recorded with token counts by the `N01` helper.

## Log

- 2026-08-23 — created.
