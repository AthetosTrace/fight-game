"""Reachability sweep -- which stop reasons can real generator output actually produce?

The committed single-seed runs under evidence/runs/ each show one stop reason
firing. This tool answers the complementary question: across *every* row the
generator can build, which stop reasons fire and which never do?

It reports two things per attack:

  * **Drift coverage** -- how many distinct drift-operator combinations the seed
    range produced, and the seed at which the last new one appeared. If that
    seed is well inside the range, the sweep has saturated the generator's
    reachable output space rather than merely sampling it.

  * **Stop-reason tally** -- how many runs ended in each stop reason.

Run it:

    python assignment-06/pipeline/sweep_reachability.py --seeds 25000

Writes evidence/runs/circuit-breaker-reachability/sweep.json and sweep.md.
Nothing here writes to data/unreal/DT_VanguardAttacks.csv or touches Unreal.
"""

import argparse
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from generator import DEFAULT_RULES, generate  # noqa: E402
from orchestrator import run  # noqa: E402

ASSIGNMENT_ROOT = os.path.dirname(HERE)
DEFAULT_OUT = os.path.join(
    ASSIGNMENT_ROOT, "evidence", "runs", "circuit-breaker-reachability")

ATTACKS = ("A", "B", "C", "D")


def sweep(rules_doc, seeds, budgets, attacks=ATTACKS):
    """Run every attack across `seeds` seeds, at each attempt budget in `budgets`.

    Two budgets are reported because they answer different questions. The
    shipped budget shows what the pipeline actually does in production. The
    widened budget removes MAX_ATTEMPTS as a confound, so that any run still
    not resolving is genuinely stuck rather than merely out of tries.
    """
    tallies = {budget: Counter() for budget in budgets}
    coverage = {}
    no_progress_hits = []

    for attack_id in attacks:
        first_seen = {}
        for seed in range(seeds):
            generation = generate(rules_doc, attack_id, seed)
            key = tuple(sorted(d["operator"] for d in generation["drift_applied"]))
            if key not in first_seen:
                first_seen[key] = seed

            for budget in budgets:
                result = run(rules_doc, attack_id, seed, max_attempts=budget)
                tallies[budget][result["stop_reason"]] += 1
                if result["stop_reason"] == "CIRCUIT_BREAKER_NO_PROGRESS":
                    no_progress_hits.append(
                        {"attack_id": attack_id, "seed": seed, "max_attempts": budget})

        coverage[attack_id] = {
            "distinct_drift_combinations": len(first_seen),
            "last_new_combination_seed": max(first_seen.values()),
            "saturation_margin_seeds": seeds - 1 - max(first_seen.values()),
        }

    return {
        "seeds_per_attack": seeds,
        "attacks": list(attacks),
        "budgets": list(budgets),
        "total_runs": sum(sum(t.values()) for t in tallies.values()),
        "stop_reason_tally_by_budget": {
            str(budget): dict(tally) for budget, tally in tallies.items()},
        "no_progress_hits": no_progress_hits,
        "drift_coverage": coverage,
    }


def render_markdown(result):
    out = []
    out.append("# Circuit-breaker reachability sweep")
    out.append("")
    out.append("Which stop reasons can the generator's output actually produce?")
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Seeds per attack | %d |" % result["seeds_per_attack"])
    out.append("| Attacks | %s |" % ", ".join(result["attacks"]))
    out.append("| Attempt budgets | %s |" % ", ".join(
        str(b) for b in result["budgets"]))
    out.append("| **Total runs** | **%d** |" % result["total_runs"])
    out.append("")

    out.append("## Stop reasons observed")
    out.append("")
    out.append("Two budgets, because they answer different questions. Budget 3 is what")
    out.append("the pipeline ships with. The widened budget removes MAX_ATTEMPTS as a")
    out.append("confound, so a run that still does not resolve is genuinely stuck")
    out.append("rather than merely out of tries.")
    out.append("")
    all_reasons = ["SUCCESS", "HUMAN_REVIEW_REFINER_REFUSED",
                   "CIRCUIT_BREAKER_MAX_ATTEMPTS", "CIRCUIT_BREAKER_NO_PROGRESS"]
    header = "| Stop reason | " + " | ".join(
        "budget %s" % b for b in result["budgets"]) + " |"
    out.append(header)
    out.append("|---" * (len(result["budgets"]) + 1) + "|")
    for reason in all_reasons:
        cells = []
        for budget in result["budgets"]:
            count = result["stop_reason_tally_by_budget"][str(budget)].get(reason, 0)
            cells.append("**0**" if count == 0 else str(count))
        out.append("| `%s` | %s |" % (reason, " | ".join(cells)))
    out.append("")

    out.append("## Did the sweep cover the whole reachable space?")
    out.append("")
    out.append("Drift is seeded, so the generator has a finite set of reachable")
    out.append("outputs. If the last *new* drift combination appears far inside the")
    out.append("seed range, the sweep saturated that space rather than sampling it.")
    out.append("")
    out.append("| Attack | Distinct drift combinations | Last new one at seed | Margin |")
    out.append("|---|---|---|---|")
    for attack_id in result["attacks"]:
        cov = result["drift_coverage"][attack_id]
        out.append("| %s | %d | %d | %d seeds |" % (
            attack_id, cov["distinct_drift_combinations"],
            cov["last_new_combination_seed"], cov["saturation_margin_seeds"]))
    out.append("")

    hits = result["no_progress_hits"]
    out.append("## Finding")
    out.append("")
    if hits:
        out.append("`CIRCUIT_BREAKER_NO_PROGRESS` fired on %d run(s), first at "
                   "attack %s seed %d (budget %d)." % (
                       len(hits), hits[0]["attack_id"], hits[0]["seed"],
                       hits[0]["max_attempts"]))
    else:
        out.append("**`CIRCUIT_BREAKER_NO_PROGRESS` never fires on generator output.**")
        out.append("")
        out.append("Not a sampling gap -- it is structural. The no-progress guard trips")
        out.append("only when the refiner *applies* a change that leaves the failure")
        out.append("signature identical. The refiner has no such path: every branch")
        out.append("either restores a field from the canonical GDD facts, which always")
        out.append("moves the signature, or it refuses, which ends the run as")
        out.append("`HUMAN_REVIEW_REFINER_REFUSED` instead. A no-op-but-applied")
        out.append("refinement does not exist, so the guard cannot be reached from here.")
        out.append("")
        out.append("`test_no_applied_refinement_ever_leaves_the_signature_unchanged`")
        out.append("asserts that invariant directly, and the guard keeps its unit")
        out.append("coverage through a stubbed stalling refiner.")
        out.append("")
        out.append("The guard stays. It is cheap, and it is the correct protection if a")
        out.append("future refiner branch ever gains a partial-fix path. But the six")
        out.append("single-seed runs should not be read as proving it fires, and this")
        out.append("sweep is the reason that claim is not made.")
    out.append("")

    out.append("## Reproduce")
    out.append("")
    out.append("```bash")
    out.append("python assignment-06/pipeline/sweep_reachability.py --seeds %d"
               % result["seeds_per_attack"])
    out.append("```")
    out.append("")
    return "\n".join(out) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seeds", type=int, default=25000,
                        help="seeds per attack (default 25000, saturates the space)")
    parser.add_argument("--budgets", type=int, nargs="+", default=(3, 12),
                        help="attempt budgets to sweep (default: 3 shipped, 12 widened)")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    result = sweep(rules_doc, args.seeds, tuple(args.budgets))
    print(render_markdown(result))

    if not args.no_report:
        os.makedirs(args.out, exist_ok=True)
        with open(os.path.join(args.out, "sweep.json"), "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
        with open(os.path.join(args.out, "sweep.md"), "w", encoding="utf-8") as handle:
            handle.write(render_markdown(result))
        print("report written to %s" % args.out)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
