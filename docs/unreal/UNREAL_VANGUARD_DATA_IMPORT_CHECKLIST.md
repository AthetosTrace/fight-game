# Unreal Vanguard Data Import Checklist — Manual Next-Day Process

**This checklist describes a manual process. No step in it has been
performed yet.** Nothing in this repository imports data into Unreal
automatically, and this document does not claim otherwise. It may only be
executed **after** `VANGUARD_ATTACK_DATA_APPROVAL.md` is signed, and it
happens in the **private Unreal production repository**, on its own
feature branch — never directly on this repository's `main`.

Per `ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md`, this is exactly the
kind of narrow, single-purpose MCP task that is safe to run: "create one
DataTable from an approved CSV," with a dedicated branch, an asset/change
manifest, manual inspection, PIE verification, and a rollback path.

---

## Preconditions (all must be true before starting)

- [ ] `VANGUARD_ATTACK_DATA_APPROVAL.md` §4 "APPROVED" box is checked and
      dated.
- [ ] `py -3 tools/validate_vanguard_attack_csv.py` currently reports PASS
      against the approved CSV.
- [ ] Unreal MCP server is connected and verified reachable, per
      `CLAUDE.md`'s build prerequisite.
- [ ] A dedicated Unreal-side feature branch exists (e.g.
      `feature/vanguard-attack-data-import`), separate from any in-progress
      Unreal work.
- [ ] The Unreal project currently opens and plays in PIE with **no**
      pre-existing errors, so any error introduced by this import is
      attributable to this change alone.

If any precondition is false, stop and do not proceed.

---

## Step 1 — Create the matching Blueprint Struct

- [ ] In the Unreal editor, create a new **Blueprint Structure** matching
      `S_VanguardAttackDef` as described in `design-brief.md` §5.3, with
      fields aligned to `VANGUARD_ATTACK_ROW_CONTRACT.md` §2 (adapt field
      names/types 1:1 — do not add fields not in the contract, do not
      invent defaults for fields the contract marks optional/blank).
- [ ] Save the struct asset under
      `/Game/AscendantImpact/Data/` (per design-brief.md §2 folder
      convention).
- [ ] Record the exact asset path in the change manifest (Step 8).

## Step 2 — Create the DataTable from the approved CSV

- [ ] Right-click in the target Content Browser folder → **Miscellaneous →
      Data Table** → select the struct from Step 1.
- [ ] Name it `DT_VanguardAttacks` per `design-brief.md` §2.
- [ ] Use the DataTable's **Import from CSV** (or **Reimport**) option and
      point it at the approved `data/unreal/DT_VanguardAttacks.csv` from
      this repository (copy or reference it — do not hand-retype values).
- [ ] Confirm the importer reports zero errors and zero warnings. If it
      reports any, stop; do not force an import past an importer warning.

## Step 3 — Verify all four rows

- [ ] Open the DataTable editor view and visually confirm exactly four
      rows exist: `Row_A`, `Row_B`, `Row_C`, `Row_D`.
- [ ] Confirm each row's `AttackId` matches its row name (A/B/C/D).
- [ ] Confirm no field silently truncated or reformatted during import
      (spot-check `DisplayWorkingName` and `Notes`, the two longest
      free-text fields).

## Step 4 — Confirm only Attack A is enabled

- [ ] Confirm `Row_A.EnabledForSelection = true`.
- [ ] Confirm `Row_B/C/D.EnabledForSelection = false`.
- [ ] Confirm `Row_A.ImplementationStatus = Prototype` and
      `Row_B/C/D.ImplementationStatus = Planned`.

## Step 5 — Read Attack A from a temporary Blueprint

- [ ] Create a small, disposable test Blueprint (e.g., a Level Blueprint
      node graph or a throwaway `BP_DataTableTest` actor) that calls
      **Get Data Table Row** on `DT_VanguardAttacks` with row name `Row_A`.
- [ ] Confirm the returned struct's fields match the CSV values exactly
      (spot-check `IntendedRange`, `TelegraphRequirement`,
      `EnabledForSelection`).
- [ ] This Blueprint is test-only. Do not wire it into any real gameplay
      class — Attack A's actual implementation is tracked separately in
      `ATTACK_A_IMPLEMENTATION_PLAN.md`.

## Step 6 — Print or display selected Attack A fields in PIE

- [ ] From the test Blueprint, use **Print String** (or a debug widget) to
      display `AttackId`, `DisplayWorkingName`, and
      `EnabledForSelection` for `Row_A` on `BeginPlay`.
- [ ] Enter PIE and confirm the printed values match the CSV.
- [ ] Confirm `Row_B/C/D` are not selectable from anywhere in the test
      (attempting to read them via `Get Data Table Row` should still
      succeed — the DataTable holds all four rows — but no gameplay-facing
      selection UI or logic may expose B/C/D as choosable; this checklist
      only proves the data loads, not that selection logic exists yet).

## Step 7 — Confirm no errors

- [ ] Unreal's Output Log shows no new errors or warnings attributable to
      this import.
- [ ] The project still opens and plays in PIE exactly as it did before
      the import (per the precondition baseline).
- [ ] The Message Log's Asset Check / Data Validation (if run) reports no
      new failures.

## Step 8 — Record screenshots and logs

- [ ] Screenshot: the DataTable editor showing all four rows.
- [ ] Screenshot: the PIE output showing Attack A's printed fields.
- [ ] Copy of the relevant Output Log excerpt (import + PIE run).
- [ ] A short **asset/change manifest**: exact list of new/changed assets
      (the struct, the DataTable, the disposable test Blueprint — noting
      the test Blueprint should be deleted or clearly marked disposable
      before this lands anywhere permanent) and their content paths.

## Step 9 — Commit Unreal changes on a separate feature branch

- [ ] Commit only in the **private Unreal production repository**, on the
      dedicated feature branch from the preconditions — never in this
      `fight-game` repository, which holds no Unreal binary content.
- [ ] Commit message should reference this repository's approval artifact
      by path (e.g., "Import DT_VanguardAttacks per fight-game
      docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md, approved <date>").
- [ ] Do not merge that feature branch into the Unreal repository's main
      line without the same human review discipline used here.
- [ ] Do not delete the disposable test Blueprint's evidence — screenshot
      it first if it will be removed.

---

## Rollback path

If any step fails: discard the Unreal-side feature branch (or `git
checkout` away the unmerged changes in the Unreal repository), leaving its
main line untouched. This repository (`fight-game`) is never touched by a
failed import — the CSV, contract, and audit here remain exactly as
approved, ready for a corrected retry.

---

## What this checklist explicitly does not authorize

- Installing any Unreal plugin.
- Wiring `Row_A`'s data into any real player-facing selection or combat
  logic (that is `ATTACK_A_IMPLEMENTATION_PLAN.md`, a separate, later,
  larger effort with its own milestone gate).
- Touching `Row_B`, `Row_C`, or `Row_D` beyond confirming they load and
  remain disabled.
- Any change to this `fight-game` repository as part of executing this
  checklist — this checklist's actions live entirely in the Unreal
  production repository.
