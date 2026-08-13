# Vanguard attack row run `attackA-seed6`

| | |
|---|---|
| Content type | Crimson Vanguard attack-definition rows (DT_VanguardAttacks.csv) |
| Attack | A |
| Seed | `6` |
| Rules | v1.0.0 |
| Attempts used | 2 of 3 |
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

- `drop_name_caveat` — dropped the '(proposed)' caveat from the working name

## Attempt 1 — REFINED

Deterministic gate: **passed**

Evaluator: **SCORE 87.50 / 100**, threshold 70 — failed

| Criterion | Score | Weight | Passed | REASON |
|---|---|---|---|---|
| `canon_fidelity` | 1.00 | 30 | yes | range, purpose and readability requirement all match GDD section 04 page 5 |
| `telegraph_readability` | 1.00 | 25 | yes | readable: cue 'wind-up', recovery 'punishable' |
| `phase2_consistency` | 1.00 | 20 | yes | states the same attack re-timed for Phase 2 ('same attack') |
| `restraint` | 0.50 | 25 | **no** | working name 'Fault Line' is asserted as canon, but the GDD names no attack; Notes flags the values still OPEN |

Refiner changed **one** field: `DisplayWorkingName`

- before: `Fault Line`
- after: `Fault Line (proposed)`
- why: re-caveated -- the GDD names no attack, so this is proposed only

## Attempt 2 — SUCCESS

Deterministic gate: **passed**

Evaluator: **SCORE 100.00 / 100**, threshold 70 — passed

| Criterion | Score | Weight | Passed | REASON |
|---|---|---|---|---|
| `canon_fidelity` | 1.00 | 30 | yes | range, purpose and readability requirement all match GDD section 04 page 5 |
| `telegraph_readability` | 1.00 | 25 | yes | readable: cue 'wind-up', recovery 'punishable' |
| `phase2_consistency` | 1.00 | 20 | yes | states the same attack re-timed for Phase 2 ('same attack') |
| `restraint` | 1.00 | 25 | yes | working name 'Fault Line (proposed)' is caveated; Notes flags the values still OPEN |

