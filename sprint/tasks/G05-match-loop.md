---
id: G05
track: G
title: Match loop — intro, win, lose, restart
status: todo
assignment: 10
editor-required: true
depends-on: [G02]
---

## Goal

A match that starts, ends, tells you which way it ended, and lets you play again without
quitting.

## Why it matters

**This outranks every art task in the sprint.** Right now someone ragdolls and nothing
happens, forever. A stranger plays thirty seconds and is stuck. A pretty build a stranger
cannot finish fails the gate; an ugly build with win, lose and restart passes it.

## Preconditions

- `G02` complete — the project opens and PIE runs.
- No other branch is touching `.uasset` or `.umap`. Coordinate with the `Q` track.

## Steps

1. Checkpoint the level before touching it — duplicate to
   `Lvl_DuelGraybox_CP_PreMatchLoop`.
2. Decide where match state lives. `BP_DuelKnockoutCoordinator` already detects both
   knockouts and is the natural owner; a new `BP_MatchDirector` is the alternative if the
   coordinator gets crowded. Record the choice and why in the Log — `G11` asks for one
   architectural decision and its alternative.
3. **Round start:** brief "Round 1 — Fight" beat before input unlocks. Freeze both fighters
   for the count so the player is not hit before they have their bearings.
4. **End detection:** on either fighter reaching 0, stop the mover and the attack driver,
   let the ragdoll play, then show the result.
   **Fix X7 here — the QA agent found it and it reproduces on every seed.**
   `BP_DuelKnockoutCoordinator.StopMover` disables the mover's tick, which also stops
   `ApplyConstraints` running. All position enforcement dies with it: the arena clamp and
   the 78 cm minimum separation both stop applying. Measured evidence — player at X 599.4,
   Vanguard KO'd against the bound at X 650, separation **50.6 cm against a 69 cm capsule
   contact distance**. The player walks into and through the body.
   Either keep constraints ticking after a KO, or lock player input at match end. The
   input lock is the natural fix because the result screen needs it anyway — but make it a
   deliberate choice and record which, since `G11` wants an architectural decision.
5. **Result screen:** distinct win and lose states. Different words, not just a colour.
6. **Restart:** a key that resets both healths, positions, side sign, crossing state and
   the driver's cooldowns. The §22/§23 regression evidence shows PIE restart already
   resets everything correctly — mirror that reset path rather than reloading the level if
   it is cheaper.
7. Confirm restart is genuinely clean across at least five consecutive matches, alternating
   win and lose.

## Done when

- [ ] A match begins with a visible start beat and locked input.
- [ ] Beating the Vanguard shows a win result; being beaten shows a distinct lose result.
- [ ] Restart returns both fighters to full health, correct positions, side sign `+1`,
      `bCrossingActive` false, driver values from the CDO.
- [ ] Five consecutive matches run without state leaking between them — verified, not
      assumed.
- [ ] **X7 closed:** after a KO the player cannot walk inside 69 cm of the body or past the
      arena bound. Re-run the QA agent on seeds 3, 7 and 21 to confirm — those are the three
      that caught it.
- [ ] Works in PIE **and** in a packaged build.

## Log

- 2026-08-23 — created.
