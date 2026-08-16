# Combat copy run `impact-window-prompt-seed33`

| | |
|---|---|
| Content type | Ascendant Impact player-facing combat copy |
| Slot | `impact_window_prompt` |
| Seed | `33` |
| Tone judge | `rubric` |
| Rules | v1.0.0 |
| Attempts used | 3 of 3 |
| Stop reason | **SUCCESS** |

## Before and after

| | Copy |
|---|---|
| **Before** | `Well done! impact window - strike now!` |
| **After** | `IMPACT WINDOW - STRIKE NOW` |

## Retrieval — what the GDD says about this slot

**Moment:** An Impact Window opens during the duel and the player must execute the timing input.

**Slot source:** section 03, page 3 - 'Impact Window success +20 Reward execution during an earned cinematic beat'

> Impact Window success +20 Reward execution during an earned cinematic beat

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

- `tone_congratulate` — prepended praise the player did not earn
- `format_shape_break` — wrote a sentence where the HUD requires a banner
- `tone_exclaim` — swapped the terminal period for an exclamation mark

## Attempt 1 — REFINED

**Copy:** `Well done! impact window - strike now!`

```
SCORE: [5.7/10]
REASON: [tone 0.20: congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause; uses 2 exclamation mark(s); the GDD's register allows 0 | vocabulary_lore 1.00: uses the game's proper nouns, names 'impact window', and states nothing the GDD denies | format_length 0.20: runs 38 characters against a 28-character limit; this slot requires a banner; the copy is written as neither shape]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 0.20 | 35 | rubric | congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause; uses 2 exclamation mark(s); the GDD's register allows 0 |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'impact window', and states nothing the GDD denies |
| `format_length` | 0.20 | 25 | deterministic | runs 38 characters against a 28-character limit; this slot requires a banner; the copy is written as neither shape |

Faults, in the order the refiner works them:

- `T2` — congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause; uses 2 exclamation mark(s); the GDD's register allows 0
- `F1` — runs 38 characters against a 28-character limit
- `F2` — this slot requires a banner; the copy is written as neither shape

Refiner worked `T2`:

- before: `Well done! impact window - strike now!`
- after: `WELL DONE IMPACT WINDOW - STRIKE NOW`
- why: removed the exclamation marks -- the GDD's register is declarative

## Attempt 2 — REFINED

**Copy:** `WELL DONE IMPACT WINDOW - STRIKE NOW`

```
SCORE: [7.3/10]
REASON: [tone 0.50: congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause | vocabulary_lore 1.00: uses the game's proper nouns, names 'impact window', and states nothing the GDD denies | format_length 0.50: runs 36 characters against a 28-character limit]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 0.50 | 35 | rubric | congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'impact window', and states nothing the GDD denies |
| `format_length` | 0.50 | 25 | deterministic | runs 36 characters against a 28-character limit |

Faults, in the order the refiner works them:

- `T1` — congratulates the player ('well done') -- Pillar 1 makes the spectacle the reward, not applause
- `F1` — runs 36 characters against a 28-character limit

Refiner worked `T1`:

- before: `WELL DONE IMPACT WINDOW - STRIKE NOW`
- after: `IMPACT WINDOW - STRIKE NOW`
- why: removed 'well done' -- the spectacle is the reward, not applause

## Attempt 3 — SUCCESS

**Copy:** `IMPACT WINDOW - STRIKE NOW`

```
SCORE: [10.0/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 1.00: uses the game's proper nouns, names 'impact window', and states nothing the GDD denies | format_length 1.00: 26 of 28 characters, correctly shaped as a banner]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 1.00 | 40 | deterministic | uses the game's proper nouns, names 'impact window', and states nothing the GDD denies |
| `format_length` | 1.00 | 25 | deterministic | 26 of 28 characters, correctly shaped as a banner |

