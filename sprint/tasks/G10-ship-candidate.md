---
id: G10
track: G
title: Ship candidate — package, upload, stranger test
status: todo
assignment: 10
editor-required: true
depends-on: [G04, G06, G07, G08, G09]
---

## Goal

The build that gets submitted, live on itch.io, verified by someone who has not seen it.

## Why it matters

This is Deliverable 1. Target date **30 Aug**, which leaves adjustment room before the
1 Sept deadline.

## Preconditions

- Every other `G` task except `G11` is done.
- The `Q` track's findings have been triaged — see `Q03`. Anything it found that breaks a
  first-time player is fixed before this build goes up.

## Steps

1. Full Shipping package from a clean Intermediate.
2. Play it end to end yourself: title, match, win, restart, lose.
3. `butler push` to the release channel.
4. **Hand the link to someone who has not seen the game and watch without helping.** This
   is the real test of the 2-minute rule and the only way to find what the title screen
   fails to explain.
5. Fix what the watch-through exposes. Re-push.
6. Record the final URL, build size, and time-to-first-fight.
7. Record a pipeline run video for Deliverable 2 while the build is fresh — the arena
   pipeline generating the octagon, and the octagon visible in the shipped build. That
   video is what makes Pipeline-to-Game Connection verifiable.

## Done when

- [ ] The final build is live and downloadable from a signed-out browser.
- [ ] A person who had not seen it reached a fight without being told anything.
- [ ] Whatever that person got stuck on is fixed, or documented as a known limitation.
- [ ] Pipeline run video recorded.
- [ ] URL, size and time-to-first-fight recorded in the Log.

## Log

- 2026-08-23 — created.
