# Vanguard Attack Row Contract — Unreal DataTable Schema

**Purpose:** define the exact column schema for `DT_VanguardAttacks.csv`
(Task 3) so it imports cleanly into an Unreal `DataTable` against a matching
`F`-prefixed row struct, and so the deterministic validator (Task 4) has an
unambiguous contract to check against. Every field here traces to a fact or
an explicit gap named in `ATTACK_DATA_SOURCE_AUDIT.md`.

**Date:** 2026-07-28
**Branch:** `planning/unreal-attack-a-integration`

---

## 1. Design principles

1. **No field invents a value the source audit marked OPEN.** Fields that
   correspond to open/provisional facts (damage, range, cooldown, travel
   cap, exact timing numbers, asset paths) are defined here as **optional**
   and **blank-until-approved**, never defaulted to a guessed number.
2. **Working names are labeled, not asserted as canon.** `DisplayWorkingName`
   exists specifically to carry the Assignment 4 pack's proposed names
   (Fault Line / Advance Line / Bulwark Reach / Thruster Snap) with the
   contract itself documenting that these are proposed, not GDD fact.
3. **Enum-like strings are stable and machine-readable** so the validator
   (Task 4) can check them with exact string comparison, not fuzzy matching.
4. **The schema matches CLAUDE_CODE_OVERNIGHT_WORK_ORDER_V2.md Task 2's
   minimum field list exactly**, in the same order, with no field removed.

---

## 2. Column definitions

| Column | Type | Required | Max length | Allowed values | Notes |
|---|---|---|---|---|---|
| `Name` | string (row name) | **Required** | 40 | `Row_A`, `Row_B`, `Row_C`, `Row_D` only | This is the Unreal DataTable **row name** column (first column in any UE DataTable CSV). Distinct from `AttackId`. |
| `AttackId` | enum-like string | **Required** | 1 | `A`, `B`, `C`, `D` only — exactly one row per letter | Maps to `E_VanguardAttackID` in design-brief.md §5.3/§6.2 |
| `DisplayWorkingName` | string | Optional | 40 | Any string, OR blank | **Must be a proposed working name explicitly caveated elsewhere (this contract, the CSV header comment, and the approval packet) as pending designer approval — never presented as finalized GDD canon.** Blank is always valid. |
| `ImplementationStatus` | enum-like string | **Required** | 12 | `Prototype`, `Planned` only | `Prototype` = actively being built this sprint (Attack A only, per work order). `Planned` = approved metadata level, not yet implemented (B–D). No other status string is legal in this pass — `InProgress`, `Complete`, `Cut`, etc. are out of scope until a later contract revision. |
| `EnabledForSelection` | boolean string | **Required** | 5 | `true`, `false` only (lowercase) | Exactly one row may be `true` in this pass (Attack A). Rows B–D must be `false`. |
| `IntendedRange` | string (free text) | **Required** | 80 | Free text drawn only from the GDD's "Range / purpose" column | No numeric range (cm) may appear here — that is Q10, OPEN. This field carries the qualitative GDD phrase only, e.g. "Close-range committed gauntlet force." |
| `GameplayPurpose` | string (free text) | **Required** | 80 | Free text | Restates the GDD's stated purpose for the attack; must not introduce a purpose the GDD does not state. |
| `TelegraphRequirement` | string (free text) | **Required** | 120 | Free text | The GDD's readability requirement verbatim or a faithful restatement, e.g. "Distinct wind-up and punishable recovery." No invented timing number. |
| `TrackingRule` | string (free text) | Optional | 100 | Free text, or blank | Only Attacks B and C carry a tracking-lock rule per design-brief §5.1/§5.3 (`ANS_TrackingLock`, `bLockTrackingAtActive`). A and D leave this blank. |
| `ActiveDescription` | string (free text) | **Required** | 120 | Free text | Qualitative description of what happens during `ANS_ActiveHit` for this attack (e.g., hitbox trace, propulsion-capped movement). No exact duration number — Active Attack duration is a state-range value (0.18–0.45 s, both phases), not a per-attack invented number. |
| `RecoveryRequirement` | string (free text) | **Required** | 100 | Free text | Qualitative punish-opening description. No invented duration. |
| `Phase2Usage` | string (free text) | **Required** | 80 | Must state that the attack is reused unchanged in Phase 2 | Per GDD: same four attacks, re-timed via parameters, never a new moveset. Standard value for all four rows: `"Same attack, re-timed via Phase 2 parameters — no new moveset"` (or an equivalent faithful phrase). |
| `MontageAsset` | soft object path string | Optional | 200 | Valid `/Game/...` path, OR blank | **Must be blank in this pass** — no montage assets exist yet (source audit §5). A validator rule rejects any populated value until Task 4's exemption list is explicitly updated post-approval. |
| `TelegraphVfxAsset` | soft object path string | Optional | 200 | Valid `/Game/...` path, OR blank | **Must be blank in this pass** — Phase 1 uses flat emissive material colors, not authored Niagara VFX (design-brief §1.3). |
| `TelegraphAudioAsset` | soft object path string | Optional | 200 | Valid `/Game/...` path, OR blank | **Must be blank in this pass** — no free sound source verified (design-brief §14 Q31). |
| `HitTraceSocket` | string | Optional | 40 | A bone/socket name, OR blank | **Must be blank in this pass** — sockets named in design-brief §5.2 (`hand_l`, `hand_r`, `foot_l`, `foot_r`) are examples only, not confirmed against a chosen proxy skeleton. |
| `Notes` | string (free text) | Optional | 300 | Free text, must pass the seven-rule consistency checklist | Any additional caveats. Must not restate a governed number incorrectly, must not imply runtime learning, must not introduce a fifth attack or second arena, must not claim automatic Impact Window success, must not claim more restoration certainty than `cinematic-integration-inspection.md` supports. |

---

## 3. Row-count and identity rules

- Exactly **4** data rows, no header-only or empty file.
- `AttackId` values across the four rows must be exactly the set `{A, B, C, D}` — no duplicates, no fifth value, no omission.
- `Name` values must be exactly `{Row_A, Row_B, Row_C, Row_D}` — no duplicate row names (Unreal DataTables require unique row names).
- Exactly one row has `EnabledForSelection = true`, and it must be `AttackId = A`.
- The row with `EnabledForSelection = true` must have `ImplementationStatus = Prototype`.
- All rows with `AttackId` in `{B, C, D}` must have `ImplementationStatus = Planned` and `EnabledForSelection = false`.

---

## 4. Forbidden content (enforced by the Task 4 validator)

No field in any row may contain:

- A fifth attack identifier, or any `AttackId` outside `{A, B, C, D}`.
- Language implying Crimson Vanguard learns, adapts, or calls a runtime
  model (critic rule 2).
- Language implying an Impact Window can auto-succeed or be mashed into
  success (critic rule 3) — this schema does not describe Impact Windows
  directly, but `Notes` must not drift into that claim.
- A second arena or an off-screen duel location (critic rule 4) — not
  expected in this schema, but `Notes` is free text and must be checked.
- An altered governed number (critic rule 5) — e.g., restating Active
  Attack duration as a single invented number instead of leaving it out of
  scope for this row-level schema.
- A populated `MontageAsset` / `TelegraphVfxAsset` / `TelegraphAudioAsset` /
  `HitTraceSocket` value (see §5 of the source audit — all must be blank
  in this pass).
- Any numeric damage, cooldown, exact range-in-cm, or travel-distance value
  anywhere in the row (these are Q3/Q10/Q12/Q13 — all OPEN).

---

## 5. CSV mechanics

- Encoding: UTF-8, no BOM.
- Delimiter: comma. Fields containing commas must be double-quote wrapped
  per standard CSV escaping.
- Line endings: the repository's existing convention (LF in the working
  tree; Git may normalize to CRLF on Windows checkout, which does not affect
  Unreal's CSV importer).
- First row: header, with column names exactly as listed in §2, in that
  order.
- First column (`Name`) is what Unreal's DataTable importer uses as the row
  name — it must be the leftmost column.

---

## 6. What this contract deliberately does not do

- It does not choose exact numeric values for anything OPEN. That is the
  human designer's job, later, once assets and proxy skeletons exist.
- It does not create the Unreal `F`-struct or the `.uasset` DataTable itself
  — that is a manual Unreal-editor step described in
  `UNREAL_VANGUARD_DATA_IMPORT_CHECKLIST.md` (Task 7), performed only after
  human approval (Task 6).
- It does not resolve whether `DisplayWorkingName` should ultimately hold
  the Assignment 4 pack's proposed names or something the designer names
  directly — that question is surfaced to the human approval packet
  (Task 6), not decided here.
