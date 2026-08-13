# Vanguard attack row run `attackD-seed9`

| | |
|---|---|
| Content type | Crimson Vanguard attack-definition rows (DT_VanguardAttacks.csv) |
| Attack | D |
| Seed | `9` |
| Rules | v1.0.0 |
| Attempts used | 1 of 3 |
| Stop reason | **HUMAN_REVIEW_REFINER_REFUSED** |

## Retrieval — what the generator read

GDD citations behind this row:

- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Four-attack course set"); `project-brief.md`, "The four authored attacks".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Crimson Vanguard — Authored Rival AI", state flow table); `project-brief.md`, "Crimson Vanguard — authored rival AI (GDD §04)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 6 ("Phase 2 escalation"); `project-brief.md`, "Phase 2 escalation (REVISED)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("REVISED — RUNTIME AI BOUNDARY"); `project-brief.md`, "Hard constraint — no runtime AI-model calls (GDD §04, §06)".
- `gdd/ascendant-impact-gdd-v0.4.md`, Page 15 ("Course Scope Lock & Future Expansion"); `project-brief.md`, "SCOPE LOCK (GDD §01, §09) — do not exceed".

| Chunk | Score |
|---|---|
| `vanguard-telegraphs.md` :: The four authored attacks (no names in the GDD — this is the gap) | 12 |
| `vanguard-telegraphs.md` :: The six-state loop (authored, deterministic — never LLM-driven) | 11 |
| `vanguard-telegraphs.md` :: Phase 2 escalation (same four attacks, re-timed — never a new moveset) | 7 |
| `core-canon.md` :: Hard constraint | 4 |
| `core-canon.md` :: Scope lock (do not exceed in generated content) | 4 |

## Drift the generator introduced

Seeded, so this is reproducible. The evaluator does not see this list.

- `adaptive_language` — described the attack as adapting to the player at runtime
- `drop_name_caveat` — dropped the '(proposed)' caveat from the working name
- `snap_travel` — removed Attack D's travel cap and asserted a full-arena snap

## Attempt 1 — HUMAN_REVIEW_REFINER_REFUSED

Deterministic gate: **1 violation(s)**

- `G7` Attack D asserts an uncapped approach (`ActiveDescription`) — expected thruster cue, travel hard-capped by data, got `instant close`

Refiner **refused**: cannot safely fix G7: capping Attack D's travel means choosing a maximum distance. That is design-brief Q13 and it is OPEN -- inventing it is the failure this pipeline exists to prevent

---

## Human review required

This run stopped with `HUMAN_REVIEW_REFINER_REFUSED`. The pipeline did not guess a value, did not write to `data/unreal/DT_VanguardAttacks.csv`, and did not touch any Unreal asset.

