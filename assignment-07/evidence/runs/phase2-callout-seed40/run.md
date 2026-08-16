# Combat copy run `phase2-callout-seed40`

| | |
|---|---|
| Content type | Ascendant Impact player-facing combat copy |
| Slot | `phase2_callout` |
| Seed | `40` |
| Tone judge | `rubric` |
| Rules | v1.0.0 |
| Attempts used | 3 of 3 |
| Stop reason | **SUCCESS** |

## Before and after

| | Copy |
|---|---|
| **Before** | `it - boss fight presses harder.` |
| **After** | `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER` |

## Retrieval — what the GDD says about this slot

**Moment:** Crimson Vanguard reaches 50% health and Phase 2 begins.

**Slot source:** section 03, page 4 - 'Begins at 50% Crimson Vanguard health; same attacks, stronger pressure'

> Phase 2 Begins at 50% Crimson Vanguard health; same attacks, stronger pressure Apply learned reads under stress

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

Seeded, so this is reproducible. The evaluator does not see this list.

- `format_shape_break` — wrote a sentence where the HUD requires a banner
- `vocab_genericise` — replaced the canon term 'Crimson Vanguard' with the generic 'boss fight'
- `vocab_strip_subject` — replaced the named system 'phase 2' with a pronoun

## Attempt 1 — REFINED

**Copy:** `it - boss fight presses harder.`

```
SCORE: [5.7/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 0.00: uses the generic 'boss fight' where this game says 'Crimson Vanguard'; never names 'phase 2', which is what this slot exists to tell the player about; never names 'crimson vanguard', which is what this slot exists to tell the player about | format_length 0.70: this slot requires a banner; the copy is written as neither shape]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 0.00 | 40 | deterministic | uses the generic 'boss fight' where this game says 'Crimson Vanguard'; never names 'phase 2', which is what this slot exists to tell the player about; never names 'crimson vanguard', which is what this slot exists to tell the player about |
| `format_length` | 0.70 | 25 | deterministic | this slot requires a banner; the copy is written as neither shape |

Faults, in the order the refiner works them:

- `V1` — uses the generic 'boss fight' where this game says 'Crimson Vanguard'
- `V2` — never names 'phase 2', which is what this slot exists to tell the player about
- `V2` — never names 'crimson vanguard', which is what this slot exists to tell the player about
- `F2` — this slot requires a banner; the copy is written as neither shape

Refiner worked `V1`:

- before: `it - boss fight presses harder.`
- after: `it - Crimson Vanguard presses harder.`
- why: restored the canon term 'Crimson Vanguard' in place of 'boss fight'

## Attempt 2 — REFINED

**Copy:** `it - Crimson Vanguard presses harder.`

```
SCORE: [8.2/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 0.70: never names 'phase 2', which is what this slot exists to tell the player about | format_length 0.70: this slot requires a banner; the copy is written as neither shape]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 0.70 | 40 | deterministic | never names 'phase 2', which is what this slot exists to tell the player about |
| `format_length` | 0.70 | 25 | deterministic | this slot requires a banner; the copy is written as neither shape |

Faults, in the order the refiner works them:

- `V2` — never names 'phase 2', which is what this slot exists to tell the player about
- `F2` — this slot requires a banner; the copy is written as neither shape

Refiner worked `V2`:

- before: `it - Crimson Vanguard presses harder.`
- after: `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER`
- why: restored the canonical line so 'phase 2' is named again

## Attempt 3 — SUCCESS

**Copy:** `PHASE 2 - CRIMSON VANGUARD PRESSES HARDER`

```
SCORE: [10.0/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 1.00: uses the game's proper nouns, names 'phase 2', 'crimson vanguard', and states nothing the GDD denies | format_length 1.00: 41 of 48 characters, correctly shaped as a banner]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'phase 2', 'crimson vanguard', and states nothing the GDD denies |
| `format_length` | 1.00 | 25 | deterministic | 41 of 48 characters, correctly shaped as a banner |

