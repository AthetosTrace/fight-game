# Human Approval Packet — Vanguard Attack Data (DT_VanguardAttacks.csv)

**No Unreal import is authorized until this packet is signed.** This
document is the human-review gate between the generated/validated attack
data and any Unreal DataTable import, per the Generate → Deterministic
Validate → Agent Review → Human Review Queue workflow model. Nothing below
resolves an open question on its own authority — every open field is a
question for the human designer, not a default.

**Branch:** `planning/unreal-attack-a-integration`
**CSV reviewed:** `data/unreal/DT_VanguardAttacks.csv`
**Validator status at time of writing:** PASS (`py -3
tools/validate_vanguard_attack_csv.py`)
**Agent review status:** NOT YET RUN — `agents/unreal/vanguard-attack-data-reviewer.md`
defines the reviewer contract; running it and producing
`reports/unreal/VANGUARD_ATTACK_DATA_REVIEW.md` is a pending next action
(see the morning review report for the exact next step).

---

## 1. The four-row table, human-readable

| Attack | Working name (proposed, NOT approved GDD canon) | Status | Enabled? | Range/purpose (GDD) | Readability requirement (GDD) |
|---|---|---|---|---|---|
| A | "Fault Line" | Prototype | **Yes** | Close-range committed gauntlet force | Distinct wind-up and punishable recovery |
| B | "Advance Line" | Planned | No | Committed forward-pressure sequence | Visible first beat and stable tracking limit |
| C | "Bulwark Reach" | Planned | No | Armored reach and space control | Clear body direction and visible active range |
| D | "Thruster Snap" | Planned | No | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap |

All four working names come from `assignment-04/tony/outputs/vanguard-telegraph-pack-final.md`
(an Assignment 4 output that passed all seven deterministic critic rules).
They are **not** GDD facts — see question 1 below.

---

## 2. Every open or provisional field in this CSV

| Field | Rows affected | Current value | Why it's open |
|---|---|---|---|
| `DisplayWorkingName` | All four | Proposed names from Assignment 4 pack | Not in the GDD; needs explicit designer sign-off before being treated as more than a placeholder |
| Damage per attack | All four | Blank (not a CSV column in this pass) | design-brief.md §14 Q3 — no numbers exist |
| `MinRange`/`MaxRange` (cm) | All four | Blank (not a CSV column in this pass) | design-brief.md §14 Q10 — no numbers exist |
| Per-attack cooldown | All four | Blank (not a CSV column in this pass) | design-brief.md §14 Q12 — no numbers exist |
| Attack D max travel distance | D | Blank (not a CSV column in this pass) | design-brief.md §14 Q13 — GDD gives only "no hidden full-arena snap," no cap value |
| `MontageAsset` | All four | Blank | No montage assets exist yet for any attack, including A |
| `TelegraphVfxAsset` | All four | Blank | Phase 1 uses flat emissive material colors, not authored VFX (design-brief §1.3); VFX authoring is Phase 2/M5 |
| `TelegraphAudioAsset` | All four | Blank | No free sound source verified (design-brief §14 Q31); Phase 1 may ship silent |
| `HitTraceSocket` | All four | Blank | Example sockets (`hand_l`/`hand_r`/`foot_l`/`foot_r`) in design-brief §5.2 are not confirmed against a chosen proxy skeleton yet |
| Per-attack timing inside GDD state ranges | All four | Not resolved at the row level | design-brief.md §14 Q25 — the GDD publishes ranges per *state*, not per *attack*; the per-attack figure is the designer's to set once a proxy/skeleton exists |

---

## 3. Exact questions requiring your approval

1. **May the four proposed working names (Fault Line / Advance Line /
   Bulwark Reach / Thruster Snap) be used in `DisplayWorkingName` as
   placeholder labels, or should that field stay blank until you name the
   attacks directly?**
   - [ ] Approve using the proposed names as placeholders
   - [ ] Reject — leave `DisplayWorkingName` blank until I provide names
   - [ ] Approve a different set of names (specify below)

2. **Is Attack A alone being `Prototype`/enabled and B–D `Planned`/disabled
   the correct rollout for this sprint** (matching design-brief.md §1.2's
   "M2 (one attack) → M4 (all four)" sequencing)?
   - [ ] Approve
   - [ ] Reject (explain below)

3. **Do you approve the row contract itself** (`docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md`)
   as the schema to build the eventual Unreal `F`-struct and DataTable
   against?
   - [ ] Approve
   - [ ] Reject — needs a schema change (specify below)

4. **Do you want the agent reviewer** (`agents/unreal/vanguard-attack-data-reviewer.md`)
   **run before or after this approval?** (It performs no repository
   changes to reviewed files; its own report is the only file it writes.)
   - [ ] Run it before I sign — hold this approval open until its report exists
   - [ ] Approve now; run the reviewer as a parallel confirmation, not a gate

5. **Any other correction needed to the CSV, the row contract, or the source
   audit before this proceeds to Unreal import prep** (Task 7's checklist)?
   - [ ] None
   - [ ] Yes (specify below)

---

## 4. Approval

- [ ] **APPROVED** — the CSV, row contract, and source audit as they stand
  on this branch/commit are approved for the manual Unreal import steps
  described in `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`. No Unreal
  changes may occur until this box is checked and dated.
- [ ] **REJECTED** — see rejection reason below; the CSV/contract/audit must
  be revised and re-validated before resubmission.

**Rejection reason (if applicable):**

```
(designer writes here)
```

**Signature / date:**

```
Name: _______________________________
Date: _______________________________
```

---

## 5. What this approval does NOT authorize

- It does not authorize installing any Unreal plugin.
- It does not authorize creating or modifying any Unreal binary asset.
- It does not authorize merging `planning/unreal-attack-a-integration` into
  `main`.
- It does not resolve any of the open values in §2 — those remain open
  after this approval and must be filled in later, by the designer, once
  the relevant assets/systems exist.
- It authorizes exactly one thing: proceeding to the **manual** DataTable
  import steps in `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md`, on a separate
  Unreal-side feature branch, with the evidence that checklist requires.
