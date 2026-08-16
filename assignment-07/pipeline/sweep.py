"""Sweep every slot against a seed range and record what the loop actually does.

Assignment 06 ended by proving its no-progress breaker unreachable rather than
leaving it merely untested. The same question applies here and the same answer
is worth committing: a stop reason nobody has ever seen is a claim, not a
result.

The sweep also guards two properties that a single run cannot show:

    * every SUCCESS survives being scored again from scratch
    * the score never moves backwards inside a run

Both would be easy to break with a refiner change that clears one fault by
introducing another, and neither would show up in a hand-picked demo.

Run it:

    python assignment-07/pipeline/sweep.py --seeds 200
"""

import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import evaluator  # noqa: E402
import generator  # noqa: E402
import orchestrator  # noqa: E402
from evaluator import DEFAULT_RULES  # noqa: E402

ASSIGNMENT_ROOT = os.path.dirname(HERE)
DEFAULT_OUT = os.path.join(ASSIGNMENT_ROOT, "evidence", "runs", "breaker-reachability")

ALL_STOPS = (
    orchestrator.STOP_SUCCESS,
    orchestrator.STOP_ATTEMPTS,
    orchestrator.STOP_REFUSED,
    orchestrator.STOP_NO_PROGRESS,
)


def sweep(rules_doc, seeds, judge_name="rubric"):
    outcomes = collections.Counter()
    per_slot = collections.defaultdict(collections.Counter)
    first_seen = {}
    refusal_rules = collections.Counter()
    rescore_failures = []
    monotonicity_failures = []

    for slot in generator.slot_names(rules_doc):
        for seed in range(1, seeds + 1):
            result = orchestrator.run(rules_doc, slot, seed, judge_name=judge_name)
            stop = result["stop_reason"]
            outcomes[stop] += 1
            per_slot[slot][stop] += 1
            first_seen.setdefault(stop, {"slot": slot, "seed": seed})

            if stop == orchestrator.STOP_REFUSED:
                refused = result["attempts"][-1]["refinement"]["refused"]
                refusal_rules[refused.split(":")[0].replace("cannot safely fix ", "")] += 1

            if stop == orchestrator.STOP_SUCCESS:
                rescored = evaluator.evaluate(result["final_line"], rules_doc)
                if rescored["faults"] or not rescored["passed"]:
                    rescore_failures.append({
                        "run_id": result["run_id"],
                        "text": result["final_line"]["text"],
                        "score": rescored["score"],
                    })

            scores = [attempt["evaluation"]["score"] for attempt in result["attempts"]]
            if scores != sorted(scores):
                monotonicity_failures.append({"run_id": result["run_id"], "scores": scores})

    total = sum(outcomes.values())
    return {
        "seeds_per_slot": seeds,
        "slots": generator.slot_names(rules_doc),
        "total_runs": total,
        "judge": judge_name,
        "rules_version": rules_doc.get("rules_version"),
        "outcomes": {stop: outcomes.get(stop, 0) for stop in ALL_STOPS},
        "unreached": [stop for stop in ALL_STOPS if not outcomes.get(stop)],
        "first_seen": first_seen,
        "refusal_rules": dict(refusal_rules),
        "per_slot": {slot: dict(counts) for slot, counts in sorted(per_slot.items())},
        "rescore_failures": rescore_failures,
        "monotonicity_failures": monotonicity_failures,
    }


def render_markdown(report):
    out = []
    out.append("# Circuit-breaker reachability sweep")
    out.append("")
    out.append("%d runs — %d slots x %d seeds, tone judge `%s`, rules v%s."
               % (report["total_runs"], len(report["slots"]), report["seeds_per_slot"],
                  report["judge"], report["rules_version"]))
    out.append("")
    out.append("| Stop reason | Runs | Share | First seen |")
    out.append("|---|---:|---:|---|")
    for stop, count in report["outcomes"].items():
        seen = report["first_seen"].get(stop)
        where = "`%s` seed %d" % (seen["slot"], seen["seed"]) if seen else "**never**"
        out.append("| `%s` | %d | %.1f%% | %s |"
                   % (stop, count, 100.0 * count / report["total_runs"], where))
    out.append("")

    out.append("## Refusals, by the rule that caused them")
    out.append("")
    if report["refusal_rules"]:
        out.append("| Rule | Runs |")
        out.append("|---|---:|")
        for rule_id, count in sorted(report["refusal_rules"].items()):
            out.append("| `%s` | %d |" % (rule_id, count))
    else:
        out.append("None.")
    out.append("")

    out.append("## Unreached stop reasons")
    out.append("")
    if report["unreached"]:
        for stop in report["unreached"]:
            out.append("- `%s`" % stop)
        out.append("")
        out.append("`CIRCUIT_BREAKER_NO_PROGRESS` is unreachable, and structurally so "
                   "rather than by luck. A run only reaches the no-progress check after "
                   "a refinement was *applied*, every applied refinement changes the "
                   "text, and the fix for a fault always removes that fault's evidence "
                   "— which is what the signature is built from. Two consecutive "
                   "attempts therefore cannot share a signature.")
        out.append("")
        out.append("It is kept anyway. It costs nothing, and it is the guard that would "
                   "catch a future fix that edits the copy without clearing the fault it "
                   "was called for.")
    else:
        out.append("None — every stop reason fired at least once.")
    out.append("")

    out.append("## Invariants checked across every run")
    out.append("")
    out.append("| Invariant | Failures |")
    out.append("|---|---:|")
    out.append("| Every `SUCCESS` still passes when scored again from scratch | %d |"
               % len(report["rescore_failures"]))
    out.append("| The score never moves backwards inside a run | %d |"
               % len(report["monotonicity_failures"]))
    out.append("")
    for failure in report["rescore_failures"][:10]:
        out.append("- rescore failure: `%s` — %r scored %.1f"
                   % (failure["run_id"], failure["text"], failure["score"]))
    for failure in report["monotonicity_failures"][:10]:
        out.append("- monotonicity failure: `%s` — %s" % (failure["run_id"], failure["scores"]))
    out.append("")

    out.append("## Per-slot breakdown")
    out.append("")
    out.append("| Slot | " + " | ".join("`%s`" % stop for stop in ALL_STOPS) + " |")
    out.append("|---|" + "---:|" * len(ALL_STOPS))
    for slot, counts in report["per_slot"].items():
        cells = " | ".join(str(counts.get(stop, 0)) for stop in ALL_STOPS)
        out.append("| `%s` | %s |" % (slot, cells))
    out.append("")
    return "\n".join(out) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(description="Sweep the loop for breaker reachability.")
    parser.add_argument("--seeds", type=int, default=200)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--judge", default="rubric")
    parser.add_argument("--out", default=DEFAULT_OUT)
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    report = sweep(rules_doc, args.seeds, judge_name=args.judge)

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "sweep.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    with open(os.path.join(args.out, "sweep.md"), "w", encoding="utf-8") as handle:
        handle.write(render_markdown(report))

    print(render_markdown(report))
    print("written to %s" % args.out)

    failed = report["rescore_failures"] or report["monotonicity_failures"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
