# Octagon merged into the duel level — 2026-08-28 (`G07`)

Evidence that the arena the pipeline generated is the arena the game ships in.
This matters for A10's Pipeline-to-Game Connection: `game/Tools/ArenaPipeline/`
produced this geometry, and it is now inside `Lvl_DuelGraybox`, which is the map
`GameDefaultMap` points at and therefore the only map in the cook.

| File | What it shows |
|---|---|
| `octagon-overhead.png` | The eight walls, gallery slabs, truss panels and parapet ramps standing in `Lvl_DuelGraybox`. Editor viewport, camera at `(-2400, -2400, 1900)`. |
| `octagon-fight-level.png` | Fight-level view down the X axis — the Vanguard on the arena floor, PlayerStart to the right, gallery overhang above. |

## What the build reported

Read from the live level, not assumed:

- spawns at PlayerStart `(0, 0, 94)` and Vanguard `(350, 0, 90)`; floor Z `0.0` by trace
- centre `(0, 0, 0)` — the **fighter clamp centre**, `CENTRE_MODE = "combat_axis"`
- `centre_to_face` **1590 cm**, grown from the 1200 cm spec by the authored
  camera-containment rule (duel rig worst case 1490 cm from centre, plus 100 cm margin)
- `flat_to_flat` **3180 cm**, floor area 838 m²
- the fighter clamp is unchanged at **±650**

## Verification

- The 30 `ArenaOct_*` actors in `Lvl_DuelGraybox` are **identical** to those in the
  reference `Lvl_ArenaOctagon` — diffed both ways, nothing on either side.
- Packaged clean afterwards: `BUILD SUCCESSFUL`, `Success - 0 error(s), 0 warning(s)`.
  `Engine/Content/BasicShapes/Cube` — the arena's only mesh — is in the staged manifest,
  and `LevelPrototyping` dropped to 5 entries once the 36 playground props came out.

## Two things this does not show

- **Lighting.** The interior is still flat-lit and the gallery overhangs read as dark
  bands. The template floor plane's ±2000 corners also stick out past the 3180 cm octagon
  and read as a floating island. `G07` step 5, not done.
- **Collision sign-off.** Gated on `X7`, which `G05` owns: after a knockout the mover's
  tick stops and takes the arena clamp with it. Invisible on a flat plane; in the octagon
  it means walking into the ramps and truss walls.
