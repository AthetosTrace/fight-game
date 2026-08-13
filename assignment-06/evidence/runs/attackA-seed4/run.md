# Vanguard attack row run `attackA-seed4`

| | |
|---|---|
| Content type | Crimson Vanguard attack-definition rows (DT_VanguardAttacks.csv) |
| Attack | A |
| Seed | `4` |
| Rules | v1.0.0 |
| Attempts used | 3 of 3 |
| Stop reason | **CIRCUIT_BREAKER_MAX_ATTEMPTS** |

## Retrieval — what the generator read

GDD citations behind this row:

- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Crimson Vanguard — Authored Rival AI", state flow table); `project-brief.md`, "Crimson Vanguard — authored rival AI (GDD §04)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Four-attack course set"); `project-brief.md`, "The four authored attacks".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 6 ("Phase 2 escalation"); `project-brief.md`, "Phase 2 escalation (REVISED)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("REVISED — RUNTIME AI BOUNDARY"); `project-brief.md`, "Hard constraint — no runtime AI-model calls (GDD §04, §06)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 15 ("Course Scope Lock & Future Expansion"); `project-brief.md`, "SCOPE LOCK (GDD §01, §09) — do not exceed".

| Chunk | Score |
|---|---|
| `vanguard-telegraphs.md` :: The six-state loop (authored, deterministic — never LLM-driven) | 11 |
| `vanguard-telegraphs.md` :: The four authored attacks (no names in the GDD — this is the gap) | 11 |
| `vanguard-telegraphs.md` :: Phase 2 escalation (same four attacks, re-timed — never a new moveset) | 7 |
| `core-canon.md` :: Hard constraint | 4 |
| `core-canon.md` :: Scope lock (do not exceed in generated content) | 3 |

## Drift the generator introduced

Seeded, so this is reproducible. The evaluator does not see this list.

- `embellish_numeric` — added an unapproved numeric range to IntendedRange
- `phase2_upgrade` — restated Phase 2 as a new moveset
- `invent_asset_path` — invented a montage asset path
- `drop_name_caveat` — dropped the '(proposed)' caveat from the working name

## Attempt 1 — REFINED

Deterministic gate: **3 violation(s)**

- `C_BLANK` no asset path may be invented before approval (`MontageAsset`) — expected blank, got `/Game/AscendantImpact/Animation/Vanguard/MM_Attack_A`
- `G3` Phase 2 described as a new or upgraded moveset (`Phase2Usage`) — expected the same four attacks, re-timed, got `upgraded moveset`
- `G6` field asserts a numeric value the GDD leaves open (`IntendedRange`) — expected no damage, range, cooldown, travel cap or timing number, got `Close-range committed gauntlet force within 250 cm`

Refiner changed **one** field: `MontageAsset`

- before: `/Game/AscendantImpact/Animation/Vanguard/MM_Attack_A`
- after: ``
- why: cleared -- no asset path is approved yet

## Attempt 2 — REFINED

Deterministic gate: **2 violation(s)**

- `G3` Phase 2 described as a new or upgraded moveset (`Phase2Usage`) — expected the same four attacks, re-timed, got `upgraded moveset`
- `G6` field asserts a numeric value the GDD leaves open (`IntendedRange`) — expected no damage, range, cooldown, travel cap or timing number, got `Close-range committed gauntlet force within 250 cm`

Refiner changed **one** field: `Phase2Usage`

- before: `Phase 2 grants an upgraded moveset with a new finisher`
- after: `Same attack, re-timed via Phase 2 parameters - no new moveset`
- why: restored the GDD's Phase 2 statement -- same attacks, re-timed

## Attempt 3 — CIRCUIT_BREAKER_MAX_ATTEMPTS

Deterministic gate: **1 violation(s)**

- `G6` field asserts a numeric value the GDD leaves open (`IntendedRange`) — expected no damage, range, cooldown, travel cap or timing number, got `Close-range committed gauntlet force within 250 cm`

---

## Human review required

This run stopped with `CIRCUIT_BREAKER_MAX_ATTEMPTS`. The pipeline did not guess a value, did not write to `data/unreal/DT_VanguardAttacks.csv`, and did not touch any Unreal asset.

