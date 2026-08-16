# Combat copy run `meter-feedback-counter-seed119`

| | |
|---|---|
| Content type | Ascendant Impact player-facing combat copy |
| Slot | `meter_feedback_counter` |
| Seed | `119` |
| Tone judge | `rubric` |
| Rules | v1.0.0 |
| Attempts used | 2 of 3 |
| Stop reason | **SUCCESS** |

## Before and after

| | Copy |
|---|---|
| **Before** | `COUNTER LANDED. ASCENSION RISING. READ THE TELEGRAPH, COMMIT TO THE COUNTER, AND KEEP THE PRESSURE ON CRIMSON VANGUARD THROUGH THE WHOLE EXCHANGE` |
| **After** | `Counter landed. Ascension rising.` |

## Retrieval — what the GDD says about this slot

**Moment:** The player converts an opening with a successful counter and the Ascension Meter rises.

**Slot source:** section 03, page 3 - 'Successful counter +15 Reward converting the opening'

> Successful counter +15 Reward converting the opening

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

- `format_overlong` — padded the line past its readability limit
- `format_shape_break` — wrote a banner where the slot requires a sentence

## Attempt 1 — REFINED

**Copy:** `COUNTER LANDED. ASCENSION RISING. READ THE TELEGRAPH, COMMIT TO THE COUNTER, AND KEEP THE PRESSURE ON CRIMSON VANGUARD THROUGH THE WHOLE EXCHANGE`

```
SCORE: [8.2/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 1.00: uses the game's proper nouns, names 'ascension', and states nothing the GDD denies | format_length 0.20: runs 145 characters against a 40-character limit; this slot requires a sentence; the copy is written as banner]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'ascension', and states nothing the GDD denies |
| `format_length` | 0.20 | 25 | deterministic | runs 145 characters against a 40-character limit; this slot requires a sentence; the copy is written as banner |

Faults, in the order the refiner works them:

- `F1` — runs 145 characters against a 40-character limit
- `F2` — this slot requires a sentence; the copy is written as banner

Refiner worked `F1`:

- before: `COUNTER LANDED. ASCENSION RISING. READ THE TELEGRAPH, COMMIT TO THE COUNTER, AND KEEP THE PRESSURE ON CRIMSON VANGUARD THROUGH THE WHOLE EXCHANGE`
- after: `Counter landed. Ascension rising.`
- why: restored the canonical wording, which fits the slot's limit

## Attempt 2 — SUCCESS

**Copy:** `Counter landed. Ascension rising.`

```
SCORE: [10.0/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 1.00: uses the game's proper nouns, names 'ascension', and states nothing the GDD denies | format_length 1.00: 33 of 40 characters, correctly shaped as a sentence]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'ascension', and states nothing the GDD denies |
| `format_length` | 1.00 | 25 | deterministic | 33 of 40 characters, correctly shaped as a sentence |

