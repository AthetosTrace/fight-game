# Ascendant Impact — July 28 Class Transcript Alignment

## Decision

The current strategy is aligned with the instructor's guidance:

- Start with an ugly, playable prototype.
- Use Manny/Quinn or other temporary Unreal mannequins.
- Build one feature at a time.
- Keep agent work bounded and reviewable.
- Validate automatically before human review.
- Import into Unreal only after the output passes review.
- Use branches and pull requests for isolated engine changes.
- Do not rely on MCP to one-shot the entire game.
- Do not build file watchers or large autonomous infrastructure yet.

## What the transcript changes

The pre-transcript overnight work order was mostly documentation-focused.

The revised overnight target should also produce one engine-consumable artifact:

`DT_VanguardAttacks.csv`

This becomes the first bridge between the GDD/pipeline repository and Unreal.

The CSV should contain exactly four attack definitions:

- Attack A: populated and enabled
- Attack B: populated at approved metadata level, disabled
- Attack C: populated at approved metadata level, disabled
- Attack D: populated at approved metadata level, disabled

No unsupported timing values should be invented. Unknown or provisional values must remain blank or explicitly provisional according to the schema.

## First integration checkpoint

The first pipeline pass is successful only when:

1. The attack CSV passes deterministic validation.
2. A human reviews and approves it.
3. Unreal imports it into a DataTable using the matching row structure.
4. Attack A can be selected and read inside the Unreal project.
5. B–D remain unavailable for runtime selection.
6. The project opens and plays without an import or Blueprint error.

This is not yet the complete duel. It is the smallest proof that agent-produced content can cross into the engine safely.

## First playable checkpoint

After the data import works:

> Manny moves and locks onto a red Vanguard proxy. Vanguard performs Attack A. Manny dodges or counters it, earns meter, triggers the first Impact Window, and both characters return to live combat.

## Assignment 5 status

The transcript previews goal-oriented agents, but it does not provide the complete Assignment 5 brief or rubric.

Do not claim the current plan is the Assignment 5 submission until the actual brief is available.

The Attack A integration work is still a strong candidate foundation because it has:

- one concrete goal
- structured output
- deterministic validation
- human approval
- engine integration
- a pass/fail checkpoint
- a reusable workflow

## MCP decision

Use MCP experimentally and only for narrow editor operations.

Do not give MCP a whole-level or whole-game request.

Good early MCP tasks:

- create one folder
- create one Blueprint shell
- create one enum
- create one struct
- place one proxy actor
- create one DataTable from an approved CSV
- report exactly what assets changed

Every MCP task must have:

- a dedicated branch or disposable project
- an asset/change manifest
- manual inspection
- PIE verification
- a rollback path

## Blueprint versus C++

Remain Blueprint-first for the first playable slice.

C++ may later be useful for stable, testable systems or import/validation helpers, but it is not required to begin. The team needs to understand and inspect the resulting gameplay logic.

## Overnight boundary

Tonight's safe autonomous work can create:

- the attack-row schema specification
- the four-row CSV
- deterministic validators and tests
- Unreal import instructions
- Attack A implementation plan
- acceptance tests
- morning review report

It must not:

- install plugins
- create Unreal binary assets
- alter completed Assignment 4 evidence
- merge or push automatically
- invent Assignment 5 requirements
- run endless self-directed loops
