---
id: G04
track: G
title: itch.io page and butler, with the graybox build on it
status: todo
assignment: 10
editor-required: false
depends-on: [G03]
---

## Goal

Prove the distribution pipe end to end by pushing the *graybox* build, long before there
is anything good to put through it.

## Why it matters

UE 5.8 has no WebGL target, so the only route to a playable link is a downloadable Windows
build. Discovering an itch.io or butler problem on submission night is the avoidable way to
fail the gate.

## Preconditions

- `G03` complete — a launching packaged build exists.

## Steps

1. Create the itch.io project page. Title, one-paragraph description, and the controls
   listed **on the page itself**, so the 2-minute rule does not depend on a readme buried
   inside the zip.
2. Install `butler`, authenticate, push the build to a channel such as `windows-beta`.
3. Set the page Public or take a shareable draft link, then confirm the download works
   from a browser that is not signed in as the owner.
4. Record the URL in `sprint/BOARD.md` and in the Log below.
5. Time it honestly: from clicking the link to being in a fight. Write that number down —
   `G11` needs it and the rubric measures it.

## Done when

- [ ] The itch.io page exists and lists the controls.
- [ ] `butler push` succeeds and the build appears on the page.
- [ ] Download and launch verified from a signed-out browser.
- [ ] Time-to-first-fight measured and recorded.

## Log

- 2026-08-23 — created.
