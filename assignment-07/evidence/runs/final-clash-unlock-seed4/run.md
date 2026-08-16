# Combat copy run `final-clash-unlock-seed4`

| | |
|---|---|
| Content type | Ascendant Impact player-facing combat copy |
| Slot | `final_clash_unlock` |
| Seed | `4` |
| Tone judge | `rubric` |
| Rules | v1.0.0 |
| Attempts used | 1 of 3 |
| Stop reason | **HUMAN_REVIEW_REFINER_REFUSED** |

## Before and after

| | Copy |
|---|---|
| **Before** | `METER FULL - CLASH READY Read the telegraph, commit to the counter, and keep the pressure on Crimson Vanguard through the whole exchange.` |
| **After** | `METER FULL - CLASH READY Read the telegraph, commit to the counter, and keep the pressure on Crimson Vanguard through the whole exchange.` |

## Retrieval — what the GDD says about this slot

**Moment:** Ascension Meter is full at 100 AND Crimson Vanguard is at or below 25% health.

**Slot source:** section 03, page 3 - 'The Final Clash becomes available only when BOTH conditions are true'

> REVISED — SINGLE GATE  The Final Clash becomes available only when BOTH conditions are true: Ascension

| Rule | Title | GDD source | Verified |
|---|---|---|---|
| `T1` | Spectacle is earned, never granted | section 01, page 1 - Pillar 1 'Readable timing and deliberate decisions earn the strongest visual rewards' | yes |
| `T2` | The register is clipped and declarative | section 01, page 1 - 'Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.' | yes |
| `T3` | State facts, do not hedge | section 01, page 1 - 'Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.' | yes |
| `V1` | Use the game's proper nouns, not genre defaults | section 01, page 1 - 'The player selects Agent Echo or Agent Nova and enters the Shattered Ring to fight' | yes |
| `V2` | The slot's own subject must be named | section 03, page 4 - 'Readable armored pressure; onboarding Impact Window' | yes |
| `L1` | The Ascension Meter is earned, never passive | section 03, page 3 - 'It does not fill from waiting or elapsed time' | yes |
| `L2` | A failed Final Clash does not restart the duel | section 03, page 4 - 'A failed Final Clash does not restart the duel' | yes |
| `L3` | The Final Clash gate is both conditions, never one | section 03, page 3 - 'The Final Clash becomes available only when BOTH conditions are true' | yes |
| `L4` | No numeric gameplay values in player copy | section 03, page 3 - 'Provisional gains remain subject to' | yes |
| `F1` | Every slot has a hard character limit | section 01, page 1 - Pillar 2 'VFX bursts punctuate combat without replacing it' | yes |
| `F2` | Two shapes, and a slot may only use its own | section 01, page 1 - Pillar 2 'VFX bursts punctuate combat without replacing it' | yes |

## Drift the generator introduced

Seeded, so this is reproducible. The evaluator does not see this list.

- `tone_hedge` — softened a direct instruction into a suggestion
- `lore_single_gate` — presented a full meter alone as the Final Clash unlock
- `format_overlong` — padded the line past its readability limit

## Attempt 1 — HUMAN_REVIEW_REFINER_REFUSED

**Copy:** `METER FULL - CLASH READY Read the telegraph, commit to the counter, and keep the pressure on Crimson Vanguard through the whole exchange.`

```
SCORE: [5.3/10]
REASON: [tone 1.00: clipped, declarative, and claims no reward the player did not earn | vocabulary_lore 0.20: the final clash gate is both conditions, never one -- the copy asserts 'meter full - clash ready'; never names 'final clash', which is what this slot exists to tell the player about | format_length 0.20: runs 137 characters against a 36-character limit; this slot requires a banner; the copy is written as sentence]
```

| Criterion | Score | Weight | Backend | Reason |
|---|---|---|---|---|
| `tone` | 1.00 | 35 | rubric | clipped, declarative, and claims no reward the player did not earn |
| `vocabulary_lore` | 0.20 | 40 | deterministic | the final clash gate is both conditions, never one -- the copy asserts 'meter full - clash ready'; never names 'final clash', which is what this slot exists to tell the player about |
| `format_length` | 0.20 | 25 | deterministic | runs 137 characters against a 36-character limit; this slot requires a banner; the copy is written as sentence |

Faults, in the order the refiner works them:

- `L3` — the final clash gate is both conditions, never one -- the copy asserts 'meter full - clash ready'
- `V2` — never names 'final clash', which is what this slot exists to tell the player about
- `F1` — runs 137 characters against a 36-character limit
- `F2` — this slot requires a banner; the copy is written as sentence

Refiner **refused**: cannot safely fix L3: stating both Final Clash gate conditions requires printing the 25% health threshold, which L4 forbids as a provisional value (section 03, page 3). The character budget or the threshold has to give, and that is the designer's call

---

## Human review required

This run stopped with `HUMAN_REVIEW_REFINER_REFUSED`. The pipeline did not invent a value, did not settle an open design question, and wrote nothing into the game.

