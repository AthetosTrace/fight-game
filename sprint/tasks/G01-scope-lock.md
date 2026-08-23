---
id: G01
track: G
title: Scope lock — the GDD cut addendum
status: todo
assignment: 10
editor-required: false
depends-on: []
---

## Goal

Write down, once and permanently, what Ascendant Impact ships as — so every later task has
a fixed target and nobody rebuilds a descoped feature by accident.

## Why it matters

`TODO.md` still carries 66 items against the original GDD: Final Clash, Ascension Meter,
M1–M5, combos, a roster. An agent reading it cold will start building the wrong game.
Until the cut is written down and the stale docs are bannered, that trap stays armed.

## Preconditions

- None. No editor, no API key.

## Steps

1. Write `design/SCOPE-LOCK-2026-08-23.md`. State plainly: **Ascendant Impact ships as a
   2.5D boss duel in a 3D arena.** Two fighters on a constrained combat axis, a jump that
   crosses over and swaps sides, fixed duel camera, one boss, one arena, one match.
   Note this is what the systems already enforce — `BP_VanguardDuelMover` clamps the player
   to ±650 and holds the Vanguard in a depth lane; `BP_DuelCameraRig` pins the camera to
   one arena side and never flips. It is a genre decision, not a retreat.
2. List the cuts explicitly, each with one sentence of reasoning: free 3D movement;
   Ascension Meter and Final Clash; combos and multiple attacks; boss phase 2; character
   roster; story and cutscenes; multiple arenas; animation authoring (template locomotion,
   hit reactions and ragdoll accepted as-is, including the known foot-skate at 1.1 stature
   and the jump-timing mismatch at 1.9 gravity).
3. List what ships: match loop, balance, octagon arena, title screen, minimal audio,
   packaged Windows build.
4. Banner `TODO.md` at the top — superseded for this sprint, historical record only,
   pointing at the scope lock and `sprint/BOARD.md`. **Do not delete it**; it is the record
   of the design work and several graded assignments cite it.
5. Banner `leave-offs/SESSION-RESUME.md` the same way. It is from 3 August and predates the
   entire Unreal project.
6. Reconcile `game/CLAUDE.md` and `game/AGENTS.md`. They came across in the migration and
   still describe the two-repo split and the dead never-edit-Anthony's-Blueprints rule.
   Replace those sections with: one repo, `game/` under `fight-game`; assets may now be
   edited directly; the binary-conflict rule still binds absolutely, one branch at a time.

## Done when

- [ ] `design/SCOPE-LOCK-2026-08-23.md` exists and names every cut and every keep.
- [ ] `TODO.md` and `leave-offs/SESSION-RESUME.md` both carry a superseded banner pointing
      at the scope lock.
- [ ] `game/CLAUDE.md` and `game/AGENTS.md` no longer tell a reader not to edit existing
      Blueprints, and no longer describe two repos.
- [ ] Committed on `assignment-10/final-game`.

## Log

- 2026-08-23 — created.
