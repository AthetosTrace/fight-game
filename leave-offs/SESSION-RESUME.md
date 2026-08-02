# Session resume — written 2026-08-02

Not a gate file. The gate hooks only read `designer.md`, `developer.md`, and
`inspector.md`; this file is here for the next session to read first.

**Recompute every date below on session start — they are stale the moment this file
is saved.**

## Where the project actually stands

| Thing | State |
|---|---|
| Milestone | **M1 — not yet started in-engine.** No `.uproject`, no `Content/` anywhere in the repo |
| Phase | **Phase 1** (a duel fought start to finish by 1 Sept 2026) |
| Coursework | **#02, #03, #04 all delivered and past due-date.** Nothing outstanding |
| Agent crew | **all six have run.** The straight line is finished — there is no "next agent by gate" |
| Unreal data bridge | pulled in 2026-08-02; validator PASS, 25 CSV tests PASS, agent review PASS, approval signed by Anthony |
| Git | local `main` == `origin/main`. Anthony's `tony/main` is behind us |

## What happened this session (2026-08-02)

1. **Audited `CLAUDE.md` against the repo** — found it two deliverables stale
   (claimed #03 never ran and #04 never started), listing three agents when six
   exist, with wrong designer tools and a gates section that implied the specialist
   extension was hook-gated when it is not.
2. **Confirmed Anthony never received our work.** `tony/main` is a direct ancestor
   of our `main`. Our four commits — the agent-tools fix and all of
   `assignment-04/madion/` — exist only on `origin`. The user chose to leave that
   alone for now.
3. **Pulled `tony/planning/unreal-attack-a-integration`** (15 commits, +3168 lines,
   zero conflicts, all new paths). Verified in-tree afterward: validator PASS,
   25 CSV tests, 175 assignment-04 tests, no regression. Pushed to `origin/main`.
4. **Cleanup pass** — provenance headers on the three pulled root docs, `CLAUDE.md`
   and `README.md` brought back in sync with reality, this file rewritten.

## Do this first, next session

**Stop writing documents. Start building in Unreal.** Everything needed exists:
`build-sequence.md` (63 steps, M1 first), `combat-integration-plan.md` (28 systems),
`docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md`, and
`docs/unreal/ATTACK_A_ACCEPTANCE_TESTS.md`.

The first playable objective: Manny moves and locks onto a scaled red mannequin
standing in for Crimson Vanguard; Vanguard performs one readable authored attack;
the player dodges or counters, earns Ascension Meter, triggers one successful Impact
Window, and both characters return safely to live combat.

**Unreal MCP is still not connected.** It is required before build steps are executed
in the editor.

## Still open — needs the user, and only the user

- **Five cinematic-restore corrections V1–V5** in
  `cinematic-integration-inspection.md`. M1–M2 may proceed without them; **M3
  sign-off cannot.**
- **Countersignature on `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`.** It is
  signed by Anthony Travieso (2026-07-29) and covers three designer-of-record calls:
  the proposed attack names as placeholder labels, the Attack-A-only rollout, and the
  row contract as the eventual `F`-struct schema. Until the user countersigns, treat
  it as approved on Anthony's authority for his branch only, and do not proceed to
  manual Unreal import.
- **29 provisional values** in `design-brief.md` §14. None block the build — they
  become exposed variables.
- **Whether to push our four commits to Anthony's repo.** Deferred by the user on
  2026-08-02.

## Traps worth remembering

- **Enabling Attack B will fail validation.** The row contract requires exactly one
  enabled row and it must be A. M2→M4 needs the contract, the validator, and the
  approval gate revised together.
- **The attack names are not canon.** Fault Line / Advance Line / Bulwark Reach /
  Thruster Snap came from Assignment 04 and are labeled *proposed, pending designer
  review* everywhere they appear. Keep that labeling.
- **Three root docs are Anthony's, not ours.** `CLAUDE_CODE_OVERNIGHT_WORK_ORDER_V2.md`,
  `ASCENDANT_IMPACT_NEXT_SPRINT_HANDOFF.md`, and
  `ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md` each carry a REFERENCE-ONLY
  header. In those files "the commander" means Anthony. In this repo it means the
  user. `CLAUDE.md` wins on every conflict.
