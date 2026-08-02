# Vanguard Attack Data Review

**Reviewer:** vanguard-attack-data-reviewer (agents/unreal/vanguard-attack-data-reviewer.md)
**Date:** 2026-07-29 (re-review after correction pass)
**Reviewed CSV:** `data/unreal/DT_VanguardAttacks.csv`
(as corrected and committed in `9282c78` "Fix Vanguard attack data
validation findings" — the commit that sits directly on top of `dbde5aa`
"Add Vanguard attack data review," the commit that carried the **first**
review pass's FAIL verdict. This re-review covers the corrected CSV content
as committed in `9282c78`.)
**Reviewed contract:** `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` (no
separate version number — file path is the version reference; contract
text itself is unchanged since the first review)
**Deterministic validator status:** `tools/validate_vanguard_attack_csv.py`
reports `PASS` on this CSV. Unlike the first review pass, the validator —
also corrected and committed in `9282c78` — now enforces the row
contract's per-field **max length** rule via a `MAX_LENGTHS` table checked
against every `CONTRACT_HEADERS` field, so a validator PASS now covers
length as well as the checks it already ran.

---

## Overall verdict: **PASS**

Every row and field traces cleanly to an approved source, obeys the row
contract's type/length/allowed-values rules, contradicts nothing in core
canon, and no critic rule fires. This corrects the **FAIL** verdict from the
prior review pass (`reports/unreal/VANGUARD_ATTACK_DATA_REVIEW.md`, first
version, reviewed against commit `dbde5aa`): every finding raised there has
been resolved and committed in `9282c78` "Fix Vanguard attack data
validation findings," and no new issue was found in this pass.

**What changed since the FAIL verdict, confirmed resolved (committed in
`9282c78`):**
- Row_A `RecoveryRequirement` no longer contains "the longest recovery
  window of the four attacks per the design brief" — the unsupported,
  source-contradicting cross-attack comparison is gone. Field now reads
  "Deliberate exposed opening after the committed strike" (53 chars, under
  the 100-char limit), with no per-attack timing claim of any kind.
- `DisplayWorkingName` on all four rows is now 21–25 characters (`"Fault
  Line (proposed)"`, `"Advance Line (proposed)"`, `"Bulwark Reach
  (proposed)"`, `"Thruster Snap (proposed)"`), within the 40-char limit. The
  pending-designer-approval caveat still lives in the row contract's §2
  Notes column (which the contract explicitly permits — "caveated elsewhere
  (this contract, the CSV header comment, and the approval packet)"), so the
  shortened cell text does not present the name as finalized GDD canon.
- `Phase2Usage` on all four rows now reads "Same attack, re-timed via Phase
  2 parameters - no new moveset" (61 chars, under the 80-char limit) — the
  row contract's own suggested standard phrase (§2, `Phase2Usage` row).
- Row_B `TrackingRule` is now "Body/tracking locks at a fixed point once
  active begins; cannot curve to follow the player" (90 chars, under the
  100-char limit), preserving the same `ANS_TrackingLock` meaning as before
  in fewer words.

---

## Per-finding table

No findings. Every populated field in every row traces to an approved fact
in `ATTACK_DATA_SOURCE_AUDIT.md` or `vanguard-telegraphs.md`, stays within
its `VANGUARD_ATTACK_ROW_CONTRACT.md` §2 max length, and introduces no
number, asset path, or fact the audit did not approve:

- `IntendedRange` / `GameplayPurpose` (all rows) restate the GDD's combined
  "Range / purpose" phrase for each attack verbatim, per
  `ATTACK_DATA_SOURCE_AUDIT.md` §2.
- `TelegraphRequirement` (all rows) restates the GDD's readability
  requirement per the same table.
- `TrackingRule` is populated only for Attacks B and C and blank for A and D,
  per the row contract (§2, `TrackingRule` row) and `design-brief.md` §5.1.
- `ActiveDescription` and `RecoveryRequirement` (all rows) are qualitative,
  contain no invented timing number, and (after correction) contain no
  invented per-attack comparison either.
- `Phase2Usage` (all rows) states the attack is reused unchanged in Phase 2,
  per the row contract's required standard phrasing.
- `MontageAsset`, `TelegraphVfxAsset`, `TelegraphAudioAsset`, `HitTraceSocket`
  remain blank on all four rows, per `ATTACK_DATA_SOURCE_AUDIT.md` §5.
- `ImplementationStatus` / `EnabledForSelection` match the audit's binding
  facts exactly: Attack A `Prototype`/`true`; B, C, D `Planned`/`false`.
- Row count is exactly 4; `AttackId` set is exactly `{A, B, C, D}`; `Name`
  values are exactly `{Row_A, Row_B, Row_C, Row_D}`; CSV is UTF-8 with no
  BOM and LF line endings — all per the row contract §3 and §5.

---

## Critic-rule pass table

| # | Rule | Result | Triggering text |
|---|---|---|---|
| 1 | Nova mistaken for the AI boss | PASS | — (Nova is not mentioned anywhere in the CSV) |
| 2 | Runtime-learning or runtime-LLM behavior implied | PASS | — (no learning/adaptation/model-call language found in any field) |
| 3 | Automatic or free Impact Window success | PASS | — (the CSV does not describe Impact Windows at all) |
| 4 | Extra arenas or a fifth/altered rival attack | PASS | — (exactly 4 rows, `AttackId` set is exactly `{A, B, C, D}`, no fifth attack or arena language) |
| 5 | Altered governed numbers | PASS | — (the previously-flagged Row_A `RecoveryRequirement` cross-attack recovery-length claim has been removed; no field states or implies a per-attack timing number or comparison anywhere) |
| 6 | Cinematic sequences that fail to restore gameplay | PASS | — (not applicable; the CSV does not describe any cinematic/Impact Window restoration sequence) |
| 7 | Scope expansion beyond the single duel | PASS | — (no PvP, multiplayer, additional fighters/arenas, or other deferred-scope language found) |

---

## Closing statement

No automatic file edit occurred — this report is the sole output of this
review, and its PASS verdict awaits human review and approval per the Human
Review Queue stage of the Generate → Deterministic Validate → Agent Review
→ Human Review Queue pipeline before any Unreal import proceeds.
