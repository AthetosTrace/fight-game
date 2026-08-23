# Arena pipeline run `seed2`

| | |
|---|---|
| Seed | `2` |
| Rules | v0.1.0 |
| Judge | heuristic |
| Attempts used | 3 of 3 |
| Stop reason | **CIRCUIT_BREAKER_MAX_ATTEMPTS** |

## Attempt 1 -- REFINED

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **3 violation(s)**

- `R2` obstacle 'Truss_Panel' crowds the combat bound (expected >= 500.0 cm clearance, got 485.3 cm)
- `R6` spawns are further apart than the approved opening distance (expected <= 350.0 cm, got 410.4 cm)
- `R7` not enough headroom for a jump-over (expected >= 388.0 cm, got 380.0 cm)

Refiner changed **one** field: `obstacles[Truss_Panel].x_cm` `-1160.3` -> `-1175.0` (pushed out to the minimum clearance)

## Attempt 2 -- REFINED

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **2 violation(s)**

- `R6` spawns are further apart than the approved opening distance (expected <= 350.0 cm, got 410.4 cm)
- `R7` not enough headroom for a jump-over (expected >= 388.0 cm, got 380.0 cm)

Refiner changed **one** field: `spawns.opponent.x_cm` `205.2` -> `144.8` (pulled to the widest legal opening distance)

## Attempt 3 -- CIRCUIT_BREAKER_MAX_ATTEMPTS

Decisions carried forward, pending confirmation:

- U1 resolved by us, awaiting Anthony Travieso: Not a conflict - the two values describe different things. combat_axis (+/-650, span 1300) is the FIGHTER CLAMP enforced by BP_VanguardDuelMover.ApplyConstraints. Q24's 2400x1600 is the ARENA FLOOR FOOTPRINT. The generator targets a 2400x1600 room containing a centred 1300 cm combat span.
- U2 resolved by us, awaiting Anthony Travieso: The camera corridor excludes BLOCKING GAMEPLAY GEOMETRY only. The arena's own near side wall is exempt when flagged cullable, using standard fighting-game near-wall culling.

Deterministic gate: **1 violation(s)**

- `R7` not enough headroom for a jump-over (expected >= 388.0 cm, got 380.0 cm)

---

## Human review required

This run stopped with `CIRCUIT_BREAKER_MAX_ATTEMPTS`. The pipeline did not guess a value and did not modify any Unreal asset.

