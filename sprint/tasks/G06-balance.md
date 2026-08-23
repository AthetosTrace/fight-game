---
id: G06
track: G
title: Balance — measure first, then make the boss able to win
status: todo
assignment: 10
editor-required: true
depends-on: [G05]
---

## Goal

A fight the player usually wins and sometimes loses. Target roughly a 60–70% player win
rate across honest attempts.

## Why it matters

Adrian's brief: winnable, but not so winnable that you win every time. A boss that cannot
win is a cutscene.

## Preconditions

- `G05` complete — matches can end and restart, so win rate is measurable at all.

## Steps

1. **Measure before touching anything.** Current knowns: both fighters 100 HP, both deal
   10 damage, Vanguard `AttackRange` 240, `attackDecisionChance` 0.65, player punch is an
   overlap sphere r110 at forward 120. **Player punch cadence has never been measured.**
   Get it: punches per second when spamming, and whether any cooldown or recovery exists.
2. Play ten honest matches without tuning. Record the win rate. That is the baseline and
   `G11` will want it.
3. Tune the smallest number of values that move the rate. Likely candidates, in order of
   how little they disturb proven systems: player punch cooldown or recovery window,
   Vanguard damage, `attackDecisionChance`, Vanguard attack cooldowns. **Health totals
   last** — they change match length as much as difficulty.
4. Re-measure over ten more matches after each change. One variable at a time.
5. Record every value before and after in the Log, with the win rate each produced.

## Done when

- [ ] Player punch cadence measured and written down.
- [ ] Baseline win rate over ten matches recorded before any tuning.
- [ ] Final win rate measured over at least ten matches and inside roughly 60–70%.
- [ ] The player can genuinely lose — at least two recorded losses that were not deliberate.
- [ ] Every changed value listed before and after in the Log.

## Log

- 2026-08-23 — created.
