# Arena pipeline run `seed4`

| | |
|---|---|
| Seed | `4` |
| Rules | v0.1.0 |
| Judge | heuristic |
| Attempts used | 3 of 3 |
| Stop reason | **SUCCESS** |

## Attempt 1 -- REFINED

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **2 violation(s)**

- `R2` obstacle 'Doorway_Frame' crowds the combat bound (expected >= 500.0 cm clearance, got 488.6 cm)
- `R2` obstacle 'Truss_Panel' crowds the combat bound (expected >= 500.0 cm clearance, got 497.9 cm)

Refiner changed **one** field: `obstacles[Doorway_Frame].x_cm` `1163.6` -> `1175.0` (pushed out to the minimum clearance)

## Attempt 2 -- REFINED

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **1 violation(s)**

- `R2` obstacle 'Truss_Panel' crowds the combat bound (expected >= 500.0 cm clearance, got 497.9 cm)

Refiner changed **one** field: `obstacles[Truss_Panel].x_cm` `-1172.9` -> `-1175.0` (pushed out to the minimum clearance)

## Attempt 3 -- SUCCESS

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **passed**

Evaluator (`heuristic`): **85.66 / 100**, threshold 70 -- passed

| Criterion | Score | Weight | Passed | Note |
|---|---|---|---|---|
| `clear_central_floor` | 0.53 | 30 | yes | tightest blocking object sits 525 cm beyond the bound |
| `landmark_asymmetry` | 1.00 | 25 | yes | ends are distinguishable: ['Doorway_Frame', 'Mezzanine_Strut_A'] vs ['Mezzanine_Strut_B', 'Truss_Panel'] |
| `boundary_readability` | 1.00 | 25 | yes | boundary readable on both long sides |
| `staging_room` | 0.99 | 20 | yes | room is 1.85x the combat span |

