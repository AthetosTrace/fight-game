# Vanguard attack row run `attackA-seed2`

| | |
|---|---|
| Content type | Crimson Vanguard attack-definition rows (DT_VanguardAttacks.csv) |
| Attack | A |
| Seed | `2` |
| Rules | v1.0.0 |
| Attempts used | 3 of 3 |
| Stop reason | **SUCCESS** |

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

- `adaptive_language` — described the attack as adapting to the player at runtime
- `invent_asset_path` — invented a montage asset path

## Attempt 1 — REFINED

Deterministic gate: **2 violation(s)**

- `C_BLANK` no asset path may be invented before approval (`MontageAsset`) — expected blank, got `/Game/AscendantImpact/Animation/Vanguard/MM_Attack_A`
- `G4` text implies runtime learning, adaptation, or a model call — expected deterministic authored behaviour, got `\badapts?\s+(in\s+real\s+time|at\s+runtime|to\s+the\s+player|dynamically)\b`

Refiner changed **one** field: `MontageAsset`

- before: `/Game/AscendantImpact/Animation/Vanguard/MM_Attack_A`
- after: ``
- why: cleared -- no asset path is approved yet

## Attempt 2 — REFINED

Deterministic gate: **1 violation(s)**

- `G4` text implies runtime learning, adaptation, or a model call — expected deterministic authored behaviour, got `\badapts?\s+(in\s+real\s+time|at\s+runtime|to\s+the\s+player|dynamically)\b`

Refiner changed **one** field: `ActiveDescription`

- before: `Adapts to the player in real time, selecting the least anticipated angle`
- after: `Authored gauntlet-force hitbox trace during the committed active window; no propulsion`
- why: replaced adaptive-AI language with the authored description

## Attempt 3 — SUCCESS

Deterministic gate: **passed**

Evaluator: **SCORE 100.00 / 100**, threshold 70 — passed

| Criterion | Score | Weight | Passed | REASON |
|---|---|---|---|---|
| `canon_fidelity` | 1.00 | 30 | yes | range, purpose and readability requirement all match GDD section 04 page 5 |
| `telegraph_readability` | 1.00 | 25 | yes | readable: cue 'wind-up', recovery 'punishable' |
| `phase2_consistency` | 1.00 | 20 | yes | states the same attack re-timed for Phase 2 ('same attack') |
| `restraint` | 1.00 | 25 | yes | working name 'Fault Line (proposed)' is caveated; Notes flags the values still OPEN |

