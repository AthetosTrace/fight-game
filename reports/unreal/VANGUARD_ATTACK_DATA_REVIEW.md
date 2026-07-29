# Vanguard Attack Data Review

**Reviewer:** vanguard-attack-data-reviewer (agents/unreal/vanguard-attack-data-reviewer.md)
**Date:** 2026-07-29
**Reviewed CSV:** `data/unreal/DT_VanguardAttacks.csv`
(last modified in commit `d9cc113` "Add Vanguard attack data..."; repo HEAD at
review time: `caec94e`, branch `planning/unreal-attack-a-integration`)
**Reviewed contract:** `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` (no
separate version number — file path is the version reference)
**Deterministic validator status:** `tools/validate_vanguard_attack_csv.py`
reports `PASS` on this CSV. Note: that validator does not check the row
contract's per-field **max length** rule at all (confirmed by reading
`tools/validate_vanguard_attack_csv.py` — it has no length check of any
kind), so a validator PASS does not clear the length findings below.

---

## Overall verdict: **FAIL**

At least one row/field violates the row contract and one critic rule fires
(see tables below).

---

## Per-finding table

| Row | Field | Source violated | Required correction |
|---|---|---|---|
| Row_A | RecoveryRequirement | `design-brief.md` §5.1 ("you can literally see that attack C's recovery is longer than attack A's"); `docs/unreal/ATTACK_DATA_SOURCE_AUDIT.md` §3–§4 (Q25: "the per-attack figure inside each range is OPEN... No exact per-attack timing number may be invented for the CSV") | Remove the clause "the longest recovery window of the four attacks per the design brief." No source establishes Attack A as having the longest recovery of the four; the cited design-brief line (§5.1, row A) says `ANS_Recover` is the longest **notify window on Attack A's own montage** (an intra-attack comparison against A's own Telegraph/Active/etc.), not the longest recovery **across the four attacks**. A separate design-brief line (§5.1, "you can literally see that attack C's recovery is longer than attack A's") directly contradicts the CSV's claim. Leave the per-attack recovery comparison out entirely — it is OPEN per Q25. |
| Row_A | RecoveryRequirement | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `RecoveryRequirement` row (max length 100) | Field is 123 characters, 23 over the 100-character limit. Shorten to fit within 100 characters (removing the invented cross-attack comparison per the finding above will also resolve most of the overage). |
| Row_A | DisplayWorkingName | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `DisplayWorkingName` row (max length 40) | Field is 61 characters ("Fault Line (proposed working name, pending designer approval)"), 21 over the 40-character limit. The contract states the pending-approval caveat may live "elsewhere (this contract, the CSV header comment, and the approval packet)" rather than inside the cell — shorten the cell value (e.g., to the bare working name) and rely on the contract/approval packet for the caveat, or otherwise bring the value under 40 characters. |
| Row_B | DisplayWorkingName | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `DisplayWorkingName` row (max length 40) | Field is 63 characters ("Advance Line (proposed working name, pending designer approval)"), 23 over the 40-character limit. Same correction as Row_A. |
| Row_C | DisplayWorkingName | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `DisplayWorkingName` row (max length 40) | Field is 64 characters ("Bulwark Reach (proposed working name, pending designer approval)"), 24 over the 40-character limit. Same correction as Row_A. |
| Row_D | DisplayWorkingName | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `DisplayWorkingName` row (max length 40) | Field is 64 characters ("Thruster Snap (proposed working name, pending designer approval)"), 24 over the 40-character limit. Same correction as Row_A. |
| Row_A | Phase2Usage | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `Phase2Usage` row (max length 80) | Field is 160 characters, 80 over the 80-character limit. Shorten to the contract's own suggested standard phrasing ("Same attack, re-timed via Phase 2 parameters — no new moveset," ~62 characters) or an equivalent faithful phrase that fits within 80 characters; move the extra detail about which windows scale (Select/Telegraph/Recover, Reposition delay) and the "Active Attack duration unchanged" note to `Notes` if it needs to be kept. |
| Row_B | Phase2Usage | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `Phase2Usage` row (max length 80) | Field is 109 characters, 29 over the 80-character limit. Shorten to the contract's suggested standard phrase or move the "Active Attack duration unchanged across phases" clause to `Notes`. |
| Row_C | Phase2Usage | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `Phase2Usage` row (max length 80) | Field is 109 characters, 29 over the 80-character limit. Same correction as Row_B. |
| Row_D | Phase2Usage | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `Phase2Usage` row (max length 80) | Field is 109 characters, 29 over the 80-character limit. Same correction as Row_B. |
| Row_B | TrackingRule | `docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md` §2, `TrackingRule` row (max length 100) | Field is 141 characters, 41 over the 100-character limit. Shorten while preserving the "locks at a fixed point / cannot curve to follow the player" content, e.g. by moving elaboration to `Notes`. |

---

## Critic-rule pass table

| # | Rule | Result | Triggering text |
|---|---|---|---|
| 1 | Nova mistaken for the AI boss | PASS | — (Nova is not mentioned anywhere in the CSV) |
| 2 | Runtime-learning or runtime-LLM behavior implied | PASS | — (no learning/adaptation/model-call language found in any field) |
| 3 | Automatic or free Impact Window success | PASS | — (the CSV does not describe Impact Windows at all) |
| 4 | Extra arenas or a fifth/altered rival attack | PASS | — (exactly 4 rows, `AttackId` set is exactly `{A, B, C, D}`, no fifth attack or arena language) |
| 5 | Altered governed numbers | **FAIL** | Row_A `RecoveryRequirement`: *"the longest recovery window of the four attacks per the design brief"* — presents an OPEN, per-attack timing comparison (Q25) as an established fact, and contradicts `design-brief.md` §5.1's own statement that "attack C's recovery is longer than attack A's." |
| 6 | Cinematic sequences that fail to restore gameplay | PASS | — (not applicable; the CSV does not describe any cinematic/Impact Window restoration sequence) |
| 7 | Scope expansion beyond the single duel | PASS | — (no PvP, multiplayer, additional fighters/arenas, or other deferred-scope language found) |

---

## Closing statement

No automatic file edit occurred — this report is the sole output of this
review, and every finding above awaits human review and correction per the
Human Review Queue stage of the Generate → Deterministic Validate → Agent
Review → Human Review Queue pipeline.
