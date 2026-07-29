# Claude Code — Overnight Work Order V2

## Mission

Create the first safe, engine-consumable bridge from the Ascendant Impact design repository into Unreal Engine 5.8.

The overnight deliverable is not a complete game and not an Unreal binary project.

The deliverable is a validated Vanguard attack-data package, implementation plan, and acceptance-test set that a human can review and import into Unreal the next day.

## Repository

`C:\Users\Tonys ProArt\Documents\fight-game`

## Source branch

Start from the current synchronized `main`.

## Work branch

Create:

`planning/unreal-attack-a-integration`

If it exists, create a timestamped variant.

Do not push, merge, delete branches, rewrite history, or force-push.

## Required reading

Read before writing:

- current Ascendant Impact GDD/project brief
- Assignment 3 cinematic-integration inspection
- `assignment-04/shared/knowledge-base/`
- `assignment-04/shared/critic-rules/`
- `assignment-04/tony/submission/README.md`
- `ASCENDANT_IMPACT_NEXT_SPRINT_HANDOFF.md`, if present
- `ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md`, if present

## Hard constraints

- Unreal Engine 5.8
- Blueprint-first prototype
- temporary mannequins are approved
- no runtime generative AI
- one arena
- one player versus one authored AI rival
- exactly four Vanguard attacks
- the same four attacks in Phase 2
- Attack A is the only enabled implementation target
- B–D remain disabled
- unknown or provisional numbers must not be invented
- completed Assignment 4 artifacts are immutable

## Workflow model

Use:

`Generate -> Deterministic Validate -> Agent Review -> Human Review Queue`

Do not import into Unreal automatically.

## Task 1 — Source audit

Create:

`docs/unreal/ATTACK_DATA_SOURCE_AUDIT.md`

Record:

- authoritative sources
- approved Attack A–D facts
- governed values
- provisional or open values
- contradictions
- fields that must remain blank
- fields that need human approval

Commit:

`Document Vanguard attack data sources`

## Task 2 — Unreal row contract

Create:

`docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md`

Define a compact Unreal-friendly row schema.

At minimum include:

- `Name`
- `AttackId`
- `DisplayWorkingName`
- `ImplementationStatus`
- `EnabledForSelection`
- `IntendedRange`
- `GameplayPurpose`
- `TelegraphRequirement`
- `TrackingRule`
- `ActiveDescription`
- `RecoveryRequirement`
- `Phase2Usage`
- `MontageAsset`
- `TelegraphVfxAsset`
- `TelegraphAudioAsset`
- `HitTraceSocket`
- `Notes`

Rules:

- use stable machine-readable enum-like strings
- define maximum lengths
- define required versus optional fields
- define allowed Boolean values
- define allowed implementation statuses
- do not invent asset paths
- leave Unreal asset-reference fields blank until assets exist

Commit:

`Define Unreal Vanguard attack row contract`

## Task 3 — Generate the CSV

Create:

`data/unreal/DT_VanguardAttacks.csv`

Requirements:

- exactly four rows: A, B, C, D
- Attack A: `ImplementationStatus=Prototype`
- Attack A: `EnabledForSelection=true`
- Attacks B–D: `ImplementationStatus=Planned`
- Attacks B–D: `EnabledForSelection=false`
- use only approved game facts and clearly labeled working names
- no fifth attack
- no extra arena
- no runtime learning language
- no invented exact timings
- no invented asset paths

Commit:

`Add Unreal Vanguard attack DataTable source`

## Task 4 — Deterministic validator

Create:

`tools/validate_vanguard_attack_csv.py`

The validator must fail when:

- CSV is missing
- headers do not match the contract
- row count is not four
- IDs are not exactly A, B, C, D
- more than one attack is enabled
- Attack A is disabled
- B, C, or D is enabled
- an unsupported status appears
- required fields are blank
- duplicate IDs or row names exist
- a fifth attack appears
- runtime-learning language appears
- forbidden scope-expansion language appears
- numeric values appear in fields that are required to remain unspecified
- an Unreal asset path is invented before approval

Return nonzero on failure.

Create tests under:

`tools/tests/test_validate_vanguard_attack_csv.py`

Include positive and negative fixtures.

Commit:

`Add deterministic Vanguard attack CSV validation`

## Task 5 — Agent review prompt

Create:

`agents/unreal/vanguard-attack-data-reviewer.md`

The reviewer must compare:

- source audit
- row contract
- generated CSV
- core canon
- critic rules

It must return a bounded report with:

- PASS or FAIL
- exact row and field
- source violated
- required correction
- no automatic file edits

Create the expected report location:

`reports/unreal/VANGUARD_ATTACK_DATA_REVIEW.md`

Commit:

`Add Vanguard attack data reviewer contract`

## Task 6 — Human approval packet

Create:

`docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md`

Include:

- a four-row human-readable table
- all open or provisional fields
- exact questions requiring approval
- approval checkboxes
- rejection reason field
- signature/date placeholders
- statement that no Unreal import is authorized until approved

Commit:

`Add human approval gate for attack data`

## Task 7 — Unreal import checklist

Create:

`docs/unreal/UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`

Describe the manual next-day process:

1. Create the matching Blueprint Struct.
2. Create/import the DataTable from the approved CSV.
3. Verify all four rows.
4. Confirm only A is enabled.
5. Read Attack A from a temporary Blueprint.
6. Print or display selected Attack A fields in PIE.
7. Confirm no errors.
8. Record screenshots and logs.
9. Commit Unreal changes on a separate feature branch.

Do not pretend the import has occurred.

Commit:

`Document Unreal attack DataTable import checkpoint`

## Task 8 — Attack A implementation plan

Create:

`docs/unreal/ATTACK_A_IMPLEMENTATION_PLAN.md`

Cover:

- Vanguard state transitions
- telegraph
- active attack
- hit detection
- recovery
- return neutral
- interruption cleanup
- player dodge/counter interaction
- minimal meter hook
- first Impact Window hook
- debug display
- completion evidence

Keep every step individually testable.

Commit:

`Plan the first Vanguard attack implementation`

## Task 9 — Acceptance tests

Create:

`docs/unreal/ATTACK_A_ACCEPTANCE_TESTS.md`

Include tests for:

- valid DataTable load
- invalid or missing row handling
- only Attack A selectable
- telegraph appears before active attack
- hit trace enables and disables
- dodge success
- perfect-dodge success
- counter success
- recovery is punishable
- interruption cleanup
- return to neutral
- AI resumes
- lock-on remains valid
- player input and locomotion restore
- repeated trigger protection
- reset and replay

Each test needs:

- ID
- preconditions
- steps
- expected result
- state to inspect
- evidence required
- pass/fail rule

Commit:

`Add Attack A integration acceptance tests`

## Task 10 — Morning review report

Create:

`reports/unreal/OVERNIGHT_ATTACK_A_REVIEW.md`

Include:

- branch name
- commits
- files created
- validation commands
- test results
- agent review result
- assumptions
- unresolved questions
- human decisions required
- exact next Unreal action
- stop reason, if incomplete

Run:

`py -3 tools/validate_vanguard_attack_csv.py`

Run the validator test suite.

Run the existing Assignment 4 test suite:

`py -3 -m unittest assignment-04/tony/pipeline/test_pipeline.py -v`

Record results honestly.

Commit:

`Add overnight Attack A integration review`

## Parallelism rule

Tasks may run in parallel only when they write to separate files and do not depend on each other's output.

The following are sequential:

1. Source audit
2. Row contract
3. CSV
4. Validator
5. Review
6. Approval
7. Import checklist
8. Implementation plan
9. Acceptance tests
10. Final report

Do not create a blind infinite loop.

## Stop conditions

Stop immediately if:

- the working tree is dirty before branch creation
- source facts conflict without an authority
- the validator cannot be made deterministic
- required data would have to be invented
- a task requires Unreal binary assets
- a task requires plugin installation
- existing unrelated tests fail
- Git behaves unexpectedly
- all tasks are complete

Leave the branch unmerged for human review.
