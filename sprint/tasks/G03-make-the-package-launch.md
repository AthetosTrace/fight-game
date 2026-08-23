---
id: G03
track: G
title: Make the package actually launch
status: todo
assignment: 10
editor-required: true
depends-on: [G02]
---

## Goal

A packaged Windows Shipping build a person can double-click and play, with the graybox
duel in it. Not pretty — running.

## Why it matters

This is the gate. No link, or a broken link, caps the whole assignment at 50%.

## Preconditions

- `G02` complete, with its cook log on disk.

## Steps

1. **Plugin allowlists first — the most likely cause of failure.**
   `game/AscendantImpact.uproject` enables `ModelContextProtocol`, `MCPClientToolset`,
   `Terminal` and `AllToolsets` with **no `TargetAllowList`**. These are editor-side.
   `ModelingToolsEditorMode` already has `"TargetAllowList": ["Editor"]` — copy that
   pattern onto the others, or disable them for the shipping target outright.
2. Confirm Game Default Map and Editor Startup Map point at the duel level, not the
   ThirdPerson template.
3. Re-cook. Work each error to root cause; do not silence warnings to get past them.
4. Run the packaged `.exe` on this machine and play a full match.
5. Note the build size — it drives how realistic "playable in 2 minutes" is over a
   download.

## Done when

- [ ] A Shipping build cooks with no errors.
- [ ] The packaged `.exe` launches straight to the duel, with no console window and no
      editor UI.
- [ ] A full match is playable in the packaged build: move, jump, punch, take damage, KO.
- [ ] Build size recorded in the Log.
- [ ] The `.uproject` plugin changes are committed.

## Log

- 2026-08-23 — created.
