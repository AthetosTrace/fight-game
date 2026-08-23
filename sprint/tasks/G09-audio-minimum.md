---
id: G09
track: G
title: Audio minimum — hit, whiff, KO, ambience
status: todo
assignment: 10
editor-required: true
depends-on: [G05]
---

## Goal

The game makes noise when things happen. Four sounds, not a soundtrack.

## Why it matters

Not in any rubric line, and that is exactly why it gets skipped. A silent fighting game
reads as broken inside the first ten seconds — the same window the playable-link gate
measures. This is the cheapest perceived-quality gain in the sprint.

The old design docs flagged this: no free sound source was ever verified, and Phase 1 was
allowed to ship silent (Q31). That permission was for a prototype. This ships to a
stranger.

## Preconditions

- `G05` complete.
- Sound files sourced under a licence that permits redistribution. **Record the source and
  licence for each file** — this ships publicly.

## Steps

1. Source four sounds: punch connects, punch whiffs, knockout, arena ambience loop.
2. Import, set up a Sound Class or two so relative levels are adjustable in one place.
3. Wire: impact on the damage event, whiff on a punch that overlaps nothing, KO on the
   knockout transition, ambience on level start.
4. Mix so nothing clips and ambience sits under the hits.
5. Write the sources and licences into `game/docs/audio-credits.md`.

## Done when

- [ ] All four sounds play at the right moments in a packaged build.
- [ ] Nothing clips; ambience does not drown the hits.
- [ ] `game/docs/audio-credits.md` lists every file, its source and its licence.

## Log

- 2026-08-23 — created.
