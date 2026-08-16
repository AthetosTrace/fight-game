# Circuit-breaker reachability sweep

1200 runs — 6 slots x 200 seeds, tone judge `rubric`, rules v1.0.0.

| Stop reason | Runs | Share | First seen |
|---|---:|---:|---|
| `SUCCESS` | 973 | 81.1% | `clash_failure_recovery` seed 1 |
| `CIRCUIT_BREAKER_MAX_ATTEMPTS` | 227 | 18.9% | `clash_failure_recovery` seed 3 |
| `HUMAN_REVIEW_REFINER_REFUSED` | 0 | 0.0% | **never** |
| `CIRCUIT_BREAKER_NO_PROGRESS` | 0 | 0.0% | **never** |

## Refusals, by the rule that caused them

None.

## Unreached stop reasons

- `HUMAN_REVIEW_REFINER_REFUSED`
- `CIRCUIT_BREAKER_NO_PROGRESS`

`CIRCUIT_BREAKER_NO_PROGRESS` is unreachable, and structurally so rather than by luck. A run only reaches the no-progress check after a refinement was *applied*, every applied refinement changes the text, and the fix for a fault always removes that fault's evidence — which is what the signature is built from. Two consecutive attempts therefore cannot share a signature.

It is kept anyway. It costs nothing, and it is the guard that would catch a future fix that edits the copy without clearing the fault it was called for.

## Invariants checked across every run

| Invariant | Failures |
|---|---:|
| Every `SUCCESS` still passes when scored again from scratch | 0 |
| The score never moves backwards inside a run | 0 |


## Per-slot breakdown

| Slot | `SUCCESS` | `CIRCUIT_BREAKER_MAX_ATTEMPTS` | `HUMAN_REVIEW_REFINER_REFUSED` | `CIRCUIT_BREAKER_NO_PROGRESS` |
|---|---:|---:|---:|---:|
| `clash_failure_recovery` | 161 | 39 | 0 | 0 |
| `final_clash_unlock` | 172 | 28 | 0 | 0 |
| `impact_window_prompt` | 161 | 39 | 0 | 0 |
| `loss_screen` | 158 | 42 | 0 | 0 |
| `meter_feedback_counter` | 161 | 39 | 0 | 0 |
| `phase2_callout` | 160 | 40 | 0 | 0 |

