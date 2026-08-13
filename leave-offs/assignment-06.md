---
agent: assignment-06
status: complete
artifact: assignment-06/README.md
date: 2026-08-12
recorded_by: commander
---

# Assignment 06 leave-off — the GER pipeline

**Not a gate file.** No agent by this name exists; the gate hooks read `designer.md`,
`developer.md` and `inspector.md`. The frontmatter matches their format so
`check_leaveoff.py` would pass if ever pointed here, and so this file is read the same
way as the rest.

Due **18 August 2026, 11:59 ET**. Built **12 August 2026**. Not yet submitted.

## What is on disk

`assignment-06/` — a Generator → Evaluator → Refiner → Circuit Breaker pipeline that
generates **Crimson Vanguard attack-definition rows** for `DT_VanguardAttacks.csv`.

| Check | Result |
|---|---|
| Pipeline code | 1,614 lines across 7 modules |
| Tests | **152 passing**, no engine, no network, no API key |
| Assignment 05 suite still green | **96 passing** — nothing regressed |
| GDD rules in the contract | **7**, each citing a GDD section *and* page |
| OPEN values that must never be invented | **9**, each with its reason and source |
| Committed evidence runs | **6**, covering every stop reason |
| Generated table vs `tools/validate_vanguard_attack_csv.py` | **PASS** |
| Commits | `a2df9a4` (declaration, alone), `b892e5d` (pipeline) |

## Why this is not Assignment 05's arena pipeline

Worth recording, because the obvious move was to resubmit A05 and it would have been a
mistake.

The rubric's 3.0-point criterion is *"the Evaluator enforces a specific rule from the
student's **GDD** — the rule is identifiable in the GDD."* All eight arena rules in
`assignment-05/arena-pipeline/contracts/arena_rules.json` cite
`docs/agent/PROTOTYPE_BLACKBOARD.md` — **measured implementation, not design.** Correct
for what A05 was doing; wrong for what A06 is graded on.

Separately, Assignment 04 built a real retrieval layer (`knowledge_base.py`, 377 lines)
whose every chunk carries a `*Source: gdd/… Page N*` line — and **A05 never called it.**
Grep the arena pipeline for it and you find two passing comments and zero code paths.

So A06 is the join: `assignment-06/pipeline/retrieval.py` runs A04's scoring over A04's
knowledge base, and a test asserts that **no rule cites the blackboard**. A04's
`retrieval-manifest.md` had already scoped this exact content type as *Output 1 — Crimson
Vanguard Telegraph and Readability Pack*, so the queries were not invented either.

## The catch — read this before touching the row contract

Run [`assignment-06/evidence/runs/attackA-seed6/run.md`](../assignment-06/evidence/runs/attackA-seed6/run.md).

A generated row with `DisplayWorkingName: Fault Line` **passes the deterministic gate with
zero violations** and **passes `tools/validate_vanguard_attack_csv.py`.** Legal string,
optional column, correct length. It would import into Unreal looking entirely correct.

It is wrong because **the GDD names no attack.** Uncaveated, it asserts designer approval
that was never given. The evaluator scored it **87.50 / 100** — above the 70 threshold —
and still failed it, because `restraint` failed and every criterion must pass.

**`VANGUARD_ATTACK_ROW_CONTRACT.md` §1.2 already required the caveat.** The deterministic
validator built to enforce that contract never encoded it, because it is a sentence about
honesty rather than a checkable field constraint. The rule was written down, believed, and
unenforced for months. That is the argument for the scored second layer, and it is the
ReadMe's answer to *"did the pipeline catch something you would have missed?"*

## Boundaries respected

- **Nothing was written to `data/unreal/DT_VanguardAttacks.csv`.** Generated output stops
  in `assignment-06/evidence/`.
- **Nothing in Unreal was touched.** `CLAUDE.md` marks the `S_VanguardAttackDef` /
  `DT_VanguardAttacks` import route **PAUSED** pending the gameplay owner. That pause
  holds; this pipeline only generates and checks.
- **`tools/` and `assignment-04/` were read, never modified.**

## Two bugs the tests found

Both in the checking logic, both silent false negatives. Both fixed, both in the ReadMe.

1. **Negation leaked across CSV fields.** The canonical Attack D row says *"never a
   full-arena snap"* — the GDD's own wording denies the phrase it names, so the matcher
   must tell a denial from an assertion. Scoping negation to commas alone let
   `Phase2Usage`'s canonical `"- no new moveset"` reach into `Notes` and launder a planted
   fifth-attack reference. Fields now join on a clause boundary; sentence-enders split.
2. **Attack D's thruster-cue check read the working name.** `DisplayWorkingName` is
   *"Thruster Snap (proposed)"*, so a row with no cue in any describing field still
   satisfied `G7`. A name is not a telegraph.

## What is NOT done

1. **Not submitted.** The work is committed and pushed; turning it in is the user's.
2. **Anthony has not been told this exists.** It respects the PAUSE and touches nothing of
   his, so it is not blocking — but the generated CSV is a thing he would want to know
   about before the DataTable route unpauses.
3. **`CIRCUIT_BREAKER_NO_PROGRESS` never fires on a real seed.** It is covered by a test
   that stubs a no-op refiner. Every real drift the generator produces is either fixable
   or refused, so the guard is correct but currently unexercised in the committed runs.
   Do not read the six runs as proving it.

## Handoff to Assignment 07 — Style Guide Agent

Due **20 August 2026, 11:59 PM ET**. Two days after A06.

It reuses this pass directly:

- **Architecture** — same G/E/R shape, minus the circuit breaker. A07 explicitly forbids
  human intervention, so refuse-and-escalate is **not** wanted there.
- **`assignment-04/tony/pipeline/llm_client.py`** — the Claude CLI subprocess wrapper.
  Ports essentially unchanged; mock it in tests as A04 did.
- **Content type** — Vanguard telegraph and announcer copy. `vanguard-telegraphs.md` says
  outright that the GDD gives *"no names, no choreography prose, no telegraph copy"* and
  calls that absence a real content gap. A06 took the data rows; A07 takes the prose, so
  they do not overlap.

**Two constraints A07 adds that A06 did not have:** the evaluator must emit `SCORE` +
`REASON` and **must not be binary**, which disqualifies A04's `critic_rules.py` as the
evaluator (it returns `Violation | None`) — use it as a deterministic pre-check feeding a
scored LLM judge. And it needs **three before/after demonstrations** across three distinct
violation classes.
