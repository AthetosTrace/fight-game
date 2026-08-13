# Vanguard attack row run `attackA-seed3`

| | |
|---|---|
| Content type | Crimson Vanguard attack-definition rows (DT_VanguardAttacks.csv) |
| Attack | A |
| Seed | `3` |
| Rules | v1.0.0 |
| Attempts used | 1 of 3 |
| Stop reason | **HUMAN_REVIEW_REFINER_REFUSED** |

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
- `fifth_attack` — referenced a fifth attack
- `scope_creep` — referenced deferred scope as if shipped

## Attempt 1 — HUMAN_REVIEW_REFINER_REFUSED

Deterministic gate: **3 violation(s)**

- `G1` row asserts an attack outside the authored set — expected exactly four attacks A-D, got `fifth attack`
- `G5` text references deferred scope as if it shipped — expected one duel, one arena, one rival, got `\badditional\s+arenas?\b`
- `G6` field asserts a numeric value the GDD leaves open (`IntendedRange`) — expected no damage, range, cooldown, travel cap or timing number, got `Close-range committed gauntlet force within 250 cm`

Refiner **refused**: cannot safely fix G1: the authored attack set is GDD canon (section 04, page 5). A row asserting an attack outside A-D is a canon error with no correct value to write

---

## Human review required

This run stopped with `HUMAN_REVIEW_REFINER_REFUSED`. The pipeline did not guess a value, did not write to `data/unreal/DT_VanguardAttacks.csv`, and did not touch any Unreal asset.

