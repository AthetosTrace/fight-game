"""Assemble a full DT_VanguardAttacks.csv from four pipeline runs.

The pipeline generates one row at a time. This stage runs it for A, B, C and D
and writes the complete table -- but only if all four runs reached SUCCESS. A
partial table is not a table; if any attack stopped for human review, this
stage writes nothing and says which one.

The output is then checkable by `tools/validate_vanguard_attack_csv.py`, the
validator that already guards the shipped CSV. That validator was written
before this pipeline existed and knows nothing about it, which is what makes
it a fair referee.

This stage never writes to data/unreal/DT_VanguardAttacks.csv. The Unreal-side
DataTable route is PAUSED pending the gameplay owner, so output goes to the
assignment's evidence folder and stops there.
"""

import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from generator import DEFAULT_RULES  # noqa: E402
import orchestrator  # noqa: E402

ASSIGNMENT_ROOT = os.path.dirname(HERE)
DEFAULT_OUT = os.path.join(ASSIGNMENT_ROOT, "evidence", "generated_DT_VanguardAttacks.csv")


def emit(rules_doc, seeds, max_attempts=orchestrator.MAX_ATTEMPTS):
    """Run all four attacks. Returns (rows, failures)."""
    rows = []
    failures = []
    for attack_id in ("A", "B", "C", "D"):
        result = orchestrator.run(
            rules_doc, attack_id, seeds[attack_id], max_attempts=max_attempts)
        if result["stop_reason"] != orchestrator.STOP_SUCCESS:
            failures.append((attack_id, seeds[attack_id], result["stop_reason"]))
            continue
        rows.append(result["final_row"])
    return rows, failures


def write_csv(rows, headers, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(header, "") for header in headers])
    return path


def main(argv):
    parser = argparse.ArgumentParser(description="Emit a full generated attack table.")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed-a", type=int, default=16)
    parser.add_argument("--seed-b", type=int, default=16)
    parser.add_argument("--seed-c", type=int, default=16)
    parser.add_argument("--seed-d", type=int, default=16)
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    seeds = {"A": args.seed_a, "B": args.seed_b, "C": args.seed_c, "D": args.seed_d}
    rows, failures = emit(rules_doc, seeds)

    if failures:
        print("HUMAN REVIEW — no table written. These attacks did not reach SUCCESS:",
              file=sys.stderr)
        for attack_id, seed, reason in failures:
            print("  attack %s (seed %d): %s" % (attack_id, seed, reason), file=sys.stderr)
        return 2

    path = write_csv(rows, rules_doc["contract"]["headers"], args.out)
    print("wrote %d rows to %s" % (len(rows), path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
