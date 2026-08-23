---
id: G08
track: G
title: Title and controls screen
status: todo
assignment: 10
editor-required: true
depends-on: [G05]
---

## Goal

The build teaches itself in ten seconds. Game title, the controls, one key to start.

## Why it matters

The gate says *without setup instructions*. That means the instructions live inside the
game, not in a readme the stranger will not open.

## Preconditions

- `G05` complete — there is a match to start.

## Steps

1. A simple widget: title, the four controls (move, jump, punch, restart), one prompt to
   begin. No menu tree, no options screen.
2. Wire it as the first thing the build shows, then hand off to the match.
3. Keep the control list truthful — if `G06` changed a binding, this screen changes with it.
4. Verify in a packaged build, not just PIE.

## Done when

- [ ] The build opens to the title screen, not straight into a fight.
- [ ] Every control the player needs is on screen before they play.
- [ ] One key starts the match.
- [ ] Verified in a packaged build.

## Log

- 2026-08-23 — created.
