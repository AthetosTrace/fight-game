# Combat copy run `clash-failure-recovery-seed2`

| | |
|---|---|
| Content type | Ascendant Impact player-facing combat copy |
| Slot | `clash_failure_recovery` |
| Seed | `2` |
| Tone judge | `rubric` |
| Rules | v1.0.0 |
| Attempts used | 1 of 3 |
| Stop reason | **SUCCESS** |

## Before and after

| | Copy |
|---|---|
| **Before** | `The Clash broke. Return to neutral and rebuild Ascension.` |
| **After** | `The Clash broke. Return to neutral and rebuild Ascension.` |

## Retrieval — what the GDD says about this slot

**Moment:** The player attempts the Final Clash and fails; both fighters separate and combat resumes.

**Slot source:** section 03, page 4 - 'A failed Final Clash does not restart the duel'

> PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player

| Rule | Title | GDD source | Verified |
|---|---|---|---|
| `T1` | Spectacle is earned, never granted | section 01, page 1 - Pillar 1 'Readable timing and deliberate decisions earn the strongest visual rewards' | yes |
| `T2` | The register is clipped and declarative | section 01, page 1 - 'Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.' | yes |
| `T3` | State facts, do not hedge | section 01, page 1 - 'Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.' | yes |
| `V1` | Use the game's proper nouns, not genre defaults | section 01, page 1 - 'The player selects Agent Echo or Agent Nova and enters the Shattered Ring to fight' | yes |
| `V2` | The slot's own subject must be named | section 03, page 4 - 'Readable armored pressure; onboarding Impact Window' | yes |
| `L1` | The Ascension Meter is earned, never passive | section 03, page 3 - 'It does not fill from waiting or elapsed time' | yes |
| `L2` | A failed Final Clash does not restart the duel | section 03, page 4 - 'A failed Final Clash does not restart the duel' | yes |
| `L4` | No numeric gameplay values in player copy | section 03, page 3 - 'Provisional gains remain subject to' | yes |
| `F1` | Every slot has a hard character limit | section 01, page 1 - Pillar 2 'VFX bursts punctuate combat without replacing it' | yes |
| `F2` | Two shapes, and a slot may only use its own | section 01, page 1 - Pillar 2 'VFX bursts punctuate combat without replacing it' | yes |

## Drift the generator introduced

None — this seed produced a clean line.

## Attempt 1 — SUCCESS

**Copy:** `The Clash broke. Return to neutral and rebuild Ascension.`

```
SCORE: [10.0/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 1.00: uses the game's proper nouns, names 'clash', 'ascension', and states nothing the GDD denies | format_length 1.00: 57 of 72 characters, correctly shaped as a sentence]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'clash', 'ascension', and states nothing the GDD denies |
| `format_length` | 1.00 | 25 | deterministic | 57 of 72 characters, correctly shaped as a sentence |

