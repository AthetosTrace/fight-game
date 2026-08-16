# Circuit-breaker reachability sweep

Which stop reasons can the generator's output actually produce?

| | |
|---|---|
| Seeds per attack | 25000 |
| Attacks | A, B, C, D |
| Attempt budgets | 3, 12 |
| **Total runs** | **200000** |

## Stop reasons observed

Two budgets, because they answer different questions. Budget 3 is what
the pipeline ships with. The widened budget removes MAX_ATTEMPTS as a
confound, so a run that still does not resolve is genuinely stuck
rather than merely out of tries.

| Stop reason | budget 3 | budget 12 |
|---|---|---|
| `SUCCESS` | 47808 | 53372 |
| `HUMAN_REVIEW_REFINER_REFUSED` | 43217 | 46628 |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | 8975 | **0** |
| `CIRCUIT_BREAKER_NO_PROGRESS` | **0** | **0** |

## Did the sweep cover the whole reachable space?

Drift is seeded, so the generator has a finite set of reachable
outputs. If the last *new* drift combination appears far inside the
seed range, the sweep saturated that space rather than sampling it.

| Attack | Distinct drift combinations | Last new one at seed | Margin |
|---|---|---|---|
| A | 128 | 12489 | 12510 seeds |
| B | 128 | 12489 | 12510 seeds |
| C | 128 | 12489 | 12510 seeds |
| D | 252 | 14924 | 10075 seeds |

## Finding

**`CIRCUIT_BREAKER_NO_PROGRESS` never fires on generator output.**

Not a sampling gap -- it is structural. The no-progress guard trips
only when the refiner *applies* a change that leaves the failure
signature identical. The refiner has no such path: every branch
either restores a field from the canonical GDD facts, which always
moves the signature, or it refuses, which ends the run as
`HUMAN_REVIEW_REFINER_REFUSED` instead. A no-op-but-applied
refinement does not exist, so the guard cannot be reached from here.

`test_no_applied_refinement_ever_leaves_the_signature_unchanged`
asserts that invariant directly, and the guard keeps its unit
coverage through a stubbed stalling refiner.

The guard stays. It is cheap, and it is the correct protection if a
future refiner branch ever gains a partial-fix path. But the six
single-seed runs should not be read as proving it fires, and this
sweep is the reason that claim is not made.

## Reproduce

```bash
python assignment-06/pipeline/sweep_reachability.py --seeds 25000
```

