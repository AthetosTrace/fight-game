# Arena build manifest `gen-seed8`

| | |
|---|---|
| Seed | `8` |
| Rules | v0.1.0 |
| Extents status | PROPOSED |
| Placements | 12 |
| Realised violations | 0 |

**Human review / waivers:**

- materializer extents used from a PROPOSED value under --allow-proposed; every placed actor is graybox-only and carries no design authority

## Placements

| Actor | Role | Location (cm) | Size (cm) |
|---|---|---|---|
| `Arena_Floor` | floor | 0, 0, -10 | 2400 x 1600 x 20 |
| `Arena_Ceiling` | ceiling | 0, 0, 530 | 2400 x 1600 x 20 |
| `Wall_DoorwayEnd` | wall | 1220, 0, 260 | 40 x 1600 x 520 |
| `Wall_TrussEnd` | wall | -1220, 0, 260 | 40 x 1600 x 520 |
| `Railing_North` | railing | 0, 810, 60 | 2400 x 20 x 120 |
| `Railing_South` | railing | 0, -810, 60 | 2400 x 20 x 120 |
| `Doorway_Frame` | obstacle | 1175, -456, 150 | 50 x 300 x 300 |
| `Truss_Panel` | obstacle | -1175, -470, 150 | 50 x 300 x 300 |
| `Mezzanine_Strut_A` | obstacle | 1175, 500, 150 | 50 x 300 x 300 |
| `Mezzanine_Strut_B` | obstacle | -1175, 375, 150 | 50 x 300 x 300 |
| `Spawn_Player` | spawn | -125, 0, 94 | marker |
| `Spawn_Opponent` | spawn | 125, 0, 90 | marker |

