# Attack Data Source Audit — Ascendant Impact

**Purpose:** establish, before any CSV row is written, exactly which Crimson
Vanguard attack facts are governed (traceable to the GDD or an approved
downstream artifact) versus provisional/open versus new authored content
that must be labeled as such. This audit is the input to
`VANGUARD_ATTACK_ROW_CONTRACT.md` (Task 2) and `DT_VanguardAttacks.csv`
(Task 3). No CSV field may be populated with a value that is not traceable
to a row in this document.

**Date:** 2026-07-28
**Branch:** `planning/unreal-attack-a-integration`

---

## 1. Authoritative sources, in order of authority

| Rank | Source | Role |
|---|---|---|
| 1 | `gdd/ascendant-impact-gdd-v0.4.md` (Assignment #02 Revised, v0.4, 2026-07-24) | Source of truth for all game facts and governed numbers |
| 2 | `project-brief.md` | Distillation of the GDD; defers to it on conflict |
| 3 | `design-brief.md` (designer agent output, human-referenced, not yet re-approved for this bridge) | Unreal-side data shape for attacks (`S_VanguardAttackDef`, `S_AttackPhaseTuning`), provisional-values table (§13), open-questions list (§14) |
| 4 | `combat-integration-plan.md` / `cinematic-integration-inspection.md` | Confirms the attack data model traces cleanly (system #14: "Four data-driven attacks — TRACES"), and flags restoration gaps (V1–V5) not directly relevant to attack *data* but relevant to any Impact Window language near this data |
| 5 | `assignment-04/shared/knowledge-base/vanguard-telegraphs.md` (Assignment 4 knowledge base, grounded in the GDD) | Restates the GDD attack facts in retrieval-ready form; explicitly marks "no names, no choreography, no telegraph copy" as a gap |
| 6 | `assignment-04/tony/outputs/vanguard-telegraph-pack-final.md` (Assignment 4 generated + critic-passed output) | Proposes **working names** and playtest-shorthand telegraph copy for A–D, each explicitly labeled as new authored content pending designer review, not an established GDD fact |
| 7 | `assignment-04/shared/critic-rules/consistency-checklist.md` | The seven rules any generated attack-adjacent text must pass (used to sanity-check CSV `Notes`/name fields, not to invent facts) |

No source above rank 1 may override the GDD. Where design-brief.md or the
Assignment 4 pack states something the GDD does not, it is marked **derived**
or **proposed**, never **governed**.

---

## 2. Approved Attack A–D facts (governed — GDD-traceable)

These are the only facts about the four attacks that exist in the GDD itself.
*Source: `gdd/ascendant-impact-gdd-v0.4.md` Page 5 ("Four-attack course set");
carried unchanged into `project-brief.md` and `vanguard-telegraphs.md`.*

| Attack | Range / purpose | Readability requirement |
|---|---|---|
| **A** | Close-range committed gauntlet force | Distinct wind-up and punishable recovery |
| **B** | Committed forward-pressure sequence | Visible first beat and stable tracking limit |
| **C** | Armored reach and space control | Clear body direction and visible active range |
| **D** | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap |

**Governed, exactly four, no fifth attack, same four attacks in both phases**
(GDD Page 15, "Course Scope Lock"; `core-canon.md`, "Scope lock"). This is a
hard wall for the CSV: row count must be exactly 4, IDs exactly A/B/C/D.

**Governed state flow** the attacks execute inside (GDD Page 5, "Crimson
Vanguard — Authored Rival AI"): `Idle/Reposition → Select Attack → Telegraph
→ Active Attack → Recover → Return to Neutral`. All Phase 1/Phase 2 state
durations in this flow are **provisional** (see §3) — not attack-row fields,
but relevant context for anyone authoring `Notes`.

**Governed telegraph mechanics** (design-brief.md §5.1, corroborated by
`vanguard-telegraphs.md` "Telegraph mechanics"): each attack montage carries,
in order, `ANS_Telegraph` (pose hold + warning lights, no hitbox),
`ANS_ActiveHit` (hitbox trace window), `ANS_Recover` (punish opening), and
`ANS_CounterWindow` (overlaps late telegraph/early active). Attack B
additionally uses `ANS_TrackingLock` for its "stable tracking limit"; Attack
D's travel is hard-capped by data (`MaxTravelDistance`) — never a hidden
full-arena snap. These are **implementation facts about the row contract's
shape**, not values to put in a CSV cell — they justify why the row contract
(Task 2) needs `TrackingRule`, `TelegraphRequirement`, etc. as free-text
fields rather than numeric ones.

**Governed implementation-status facts for this overnight scope** (from
`ASCENDANT_IMPACT_CLASS_TRANSCRIPT_ALIGNMENT.md` and
`CLAUDE_CODE_OVERNIGHT_WORK_ORDER_V2.md`, both authored by the commander this
sprint, not the GDD, but binding on this deliverable):

- Attack A: `ImplementationStatus = Prototype`, `EnabledForSelection = true`
- Attacks B, C, D: `ImplementationStatus = Planned`, `EnabledForSelection = false`

---

## 3. Governed numeric values relevant to attacks (from design-brief.md §13.1)

These are GDD-sourced numbers that bound or contextualize attack data, even
though most live on the *state* struct (`S_AttackPhaseTuning`) rather than a
flat CSV row. Carried here so nobody re-derives or rounds them later.

| Value | Phase 1 | Phase 2 | Notes |
|---|---|---|---|
| Telegraph duration | 0.55–0.95 s | 0.40–0.75 s | Per-state range, not per-attack — see design-brief §13.1 note on rows 17–25 |
| Active Attack duration | 0.18–0.45 s | **same, not phase-scaled** | Deliberately identical across phases (design-brief §5.3) |
| Recover duration | 0.45–0.90 s | 0.35–0.75 s | |
| Select Attack duration | 0.10–0.20 s | 0.10–0.20 s | |

**These ranges are not per-attack values.** The GDD publishes them per
*state*, not per *attack* — the per-attack figure inside each range is
`OPEN` per design-brief §14 Q25. **No exact per-attack timing number may be
invented for the CSV.** Per the row contract (Task 2), timing fields stay
blank or hold the GDD range as text, never a single invented number.

---

## 4. Provisional / open values that touch attack data (must remain blank)

Pulled from design-brief.md §13.2/§14, restricted to rows that would
otherwise tempt a CSV author to invent a number:

| # | Value | Design-brief ref | Status |
|---|---|---|---|
| Q3 | Damage per rival attack A/B/C/D | §14 Q3 | OPEN — no numbers exist anywhere; suggested as % of player max health, not committed |
| Q10 | Attack A–D `MinRange`/`MaxRange` (cm) | §14 Q10 | OPEN — no numbers |
| Q12 | Per-attack cooldown | §14 Q12 | OPEN — no numbers |
| Q13 | Attack D max travel distance | §14 Q13 | OPEN — GDD gives only the qualitative rule "no hidden full-arena snap," no cap value |
| Q25 | Per-attack values inside each GDD state-duration range | §14 Q25 | OPEN — the CSV/row contract must not resolve these; they are the human designer's to fill into the eventual Unreal Data Table after this bridge is approved |
| — | `MontageAsset`, `TelegraphVfxAsset`, `TelegraphAudioAsset`, `HitTraceSocket` (asset references) | design-brief §5.3 (`Montage` field), §5.2 (sockets `hand_l`/`hand_r`/`foot_l`/`foot_r`) | OPEN/BLANK — no montage, VFX, audio, or confirmed socket assets exist yet for any attack, including A. Sockets are named as *examples* in the design brief, not confirmed against a chosen proxy skeleton. **No asset path may be invented.** |

**Rule enforced downstream (validator, Task 4):** none of the above may
appear as a populated numeric or path value in the CSV. They must be blank,
or (for the range-bound state durations) may optionally carry the GDD range
as descriptive text in a free-text field — never a single invented number in
a field the row contract marks numeric.

---

## 5. Fields that must remain blank in the first CSV pass

Per the row contract (Task 2) and the facts above, these fields are
structurally required by the schema but have **no approved value yet**:

- `MontageAsset` (all four rows — no montage assets exist)
- `TelegraphVfxAsset` (all four rows — Phase 1 uses flat emissive material
  colors per design-brief §1.3, not authored VFX; VFX authoring is M5/Phase 2)
- `TelegraphAudioAsset` (all four rows — design-brief §14 Q31 flags Phase 1
  as possibly silent; no audio source verified)
- `HitTraceSocket` (all four rows — sockets are named as examples in
  design-brief §5.2, not confirmed against a selected proxy skeleton)

These fields exist in the schema so the Unreal import (Task 7) has a place
to receive them **after** a proxy skeleton and asset set are chosen — not so
this pipeline can guess at them now.

---

## 6. New authored content proposed for this pass (not GDD facts — must be labeled)

Source: `assignment-04/tony/outputs/vanguard-telegraph-pack-final.md`, which
passed all seven deterministic critic rules in its final run (per
`assignment-04/tony/submission/README.md`).

| Attack | Proposed working name | Status |
|---|---|---|
| A | "Fault Line" | Proposed, pending designer approval — not an established GDD fact |
| B | "Advance Line" | Proposed, pending designer approval — not an established GDD fact |
| C | "Bulwark Reach" | Proposed, pending designer approval — not an established GDD fact |
| D | "Thruster Snap" | Proposed, pending designer approval — not an established GDD fact |

**Decision for this audit:** these names may populate a `DisplayWorkingName`
field **only if that field is explicitly documented in the row contract as
holding proposed/unapproved working names**, never a field implying finalized
GDD canon. The row contract (Task 2) must carry that caveat verbatim so a
future reader of the CSV cannot mistake a working name for an approved one.

---

## 7. Contradictions found

**None.** `project-brief.md`, `design-brief.md`, the Assignment 4 knowledge
base, and the cinematic-integration-inspection all agree on: exactly four
attacks (A–D), the six-state cycle, the data-driven (not per-attack-graph)
implementation, and that no attack has a name, timing, damage, range, or
asset value in the GDD itself. The only apparent tension — the Assignment 4
pack's proposed working names versus the GDD's silence on names — is not a
contradiction because the pack itself labels the names as proposed, not
canon, and the critic rules were run against exactly that distinction.

---

## 8. Fields that need explicit human approval before Unreal import

Everything in §4 and §5 above, plus:

- Whether the §6 proposed working names may be used as `DisplayWorkingName`
  values at all, or whether that field should stay blank until the designer
  names the attacks directly.
- Confirmation that Attack A alone should be `Prototype`/enabled and B–D
  `Planned`/disabled (this is a work-order instruction, not yet a GDD or
  design-brief statement, though it is consistent with design-brief §1.2's
  M2-then-M4 attack rollout: "M2 (one attack) → M4 (all four)").

This audit makes no CSV-authoring decision on its own; it hands the above
forward to `VANGUARD_ATTACK_ROW_CONTRACT.md` and the human approval packet.
