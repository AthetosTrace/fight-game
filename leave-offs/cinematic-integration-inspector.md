---
agent: cinematic-integration-inspector
status: complete
artifact: cinematic-integration-inspection.md
---

# Leave-off — Cinematic Integration Inspector

**Date:** 2026-07-27 · Ran last in the specialist extension, after the framework-evaluator and the combat-integration-architect. All eight required inputs were present on disk; not blocked.

## Verdict

**`APPROVED WITH REQUIRED CHANGES`.** The Blueprint-first custom architecture recommendation is evidence-supported, human-approved, scope-safe, and preserves the defining experience. Nine of ten hard checks pass cleanly (scope lock, no runtime AI-model calls, framework evidence, shared Echo/Nova framework, deterministic six-state rival flow, real-time gameplay preservation, numbers unchanged, milestone order, buildability). Hard check 7 — cinematic handoff safety — surfaced five specification violations.

## Blocking violations (block M3 sign-off only; not the sandbox test, M1, or M2)

- **V1** — no specified mechanism suspends the rival's Behavior Tree during the 1–3 s Impact burst (`bInClash` parks it for the Clash only).
- **V2** — `RestoreCombatState()` contains no camera-ownership restoration step, while plan §2/§10 claim it does.
- **V3** — hitbox/trace shutdown across the handoff relies on assumed notify-end-on-interrupt engine behavior, untested and unlisted on any gate.
- **V4** — animation-state cleanup is specified only on Clash failure; player death during an overlay is undefined.
- **V5** — `State.Dodging` and `State.CanCounter` are omitted from the restore clear list.

All five live in one place — the restore/suspend contract — and are correctable on paper via corrections 1–5 (inspection §8) before M3 implementation. No scope expansion, no runtime model calls, no altered numbers, no milestone-order drift, no unsupported framework claims accepted.

## Approved first test

The framework-evaluation §8 sandbox test: one buffered light-attack chain (montage sections + `ANS_ComboLink` + `IA_LightAttack`) in a disposable UE 5.8 Third Person project on a throwaway branch. Three pass conditions (chain inside window / clean drop / pre-window press discarded); delete the sandbox afterward; the main build is never touched.

## Top risk

**Schedule compression (R7)** — 36 days remain, M4 must be functionally complete ~20 August to leave tuning time, and the Unreal MCP build phase has not started. Close behind: the V1–V5 handoff-restoration gaps (a stranded cinematic state fails the M3 gate at the heart of the central promise) and the 6'10" Crimson Vanguard proxy gap (R4, guaranteed-ship fallback: scaled Mannequin + proxy blocks).

## Open human decisions

Twelve consolidated items in inspection §9, all `OPEN — designer decides`: acceptance of corrections 1–5; the sandbox test run; any purchase/plugin/external code; per-asset rights review; MCP manual fallback; cut-less Clash camera acceptance; **Q22 (1 HP floor permanent vs. Clash-only — needed before M4-08)**; the full Q1–Q31 tuning set; Echo/Nova differentiation scalars; Q29 CV HUD label / Q30 Paragon swap deadline / Q31 silent Phase 1; burst montage names; the mid-overlay death rule.

## Assignment 3 role-clarity conclusion

The extension is a real dependency chain: framework-evaluator → combat-integration-architect → cinematic-integration-inspector, each with a unique role, one named input set, and one named output; each downstream artifact gate-checks and quotes its upstream; removing any one breaks the pipeline; every output is specific to Ascendant Impact (four attack rows, 0.75 s first window, meter-100-AND-≤25% gate, 1 HP floor, `RestoreCombatState()`). The six-agent submission accurately demonstrates collaboration — all six artifacts exist on disk, and this inspector's independence is evidenced by finding and blocking real defects rather than rubber-stamping. A rubric-ready README paragraph is included at the end of `cinematic-integration-inspection.md`.

**Next:** commander presents corrections 1–5 and the §9 decision list to the human designer; on acceptance, run the sandbox test, then M1-01 via the Unreal MCP.
