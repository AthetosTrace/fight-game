# Critic evidence — Controlled regression fixture - runtime-learning violation (rule #2)  
**CONTROLLED REGRESSION FIXTURE — NOT A REAL GENERATED OUTPUT**

## Per-rule results (all seven checked)

| Rule | Status |
|---|---|
| 1 | clean |
| 2 | FLAGGED |
| 3 | clean |
| 4 | clean |
| 5 | clean |
| 6 | clean |
| 7 | clean |

## Rule 2 — Runtime-learning or runtime-LLM behavior implied

**Before (flagged):**
> Over the course of the fight, Crimson Vanguard learns from the player's patterns and adapts its attacks in real time, favoring whichever of its four strikes the fight has shown to be least anticipated.

**Why it's flagged:** Text implies runtime learning/adaptive/model-driven behavior via the phrase 'learns from the player'. The shipped game makes no runtime AI-model calls; Crimson Vanguard is deterministic authored logic.

**Ground truth:** core-canon.md, "Hard constraint"

**After (corrected):**
> Crimson Vanguard uses an authored state machine to select among four fixed attacks by range and cooldown; it does not learn from the player or adapt at runtime.

