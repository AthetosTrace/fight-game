"""Orchestrator -- generate, gate, evaluate, refine, stop.

    attempt 1..N:
        generate (first attempt) or take the refined row
        deterministic gate  -> violations? refine one field, retry
        evaluator           -> criteria failed? refine one field, retry
        both clean          -> SUCCESS

The circuit breaker stops the loop on any of:

    * MAX_ATTEMPTS reached
    * the refiner refuses -- a decision that belongs to the designer
    * no progress -- the same failure signature two attempts running

Two details carried over from the arena pipeline because they earned their
keep:

**No-progress is measured on the failure detail, not the rule id.** Clearing
one of two G6 fields leaves G6 still failing; that is progress, and a
rule-id-only comparison would misread it as a stalled loop.

**The refiner only runs when an attempt remains to verify it.** Applying a
correction on the final attempt and exiting would end the log on an unverified
claim, which is worse than stopping one step earlier.

Every attempt is written to evidence/runs/<run-id>/ as JSON plus a readable
Markdown log. Nothing here touches Unreal or writes to the shipped CSV.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from generator import DEFAULT_RULES, generate  # noqa: E402
from evaluator import evaluate, gate  # noqa: E402
from refiner import refine  # noqa: E402

MAX_ATTEMPTS = 3
ASSIGNMENT_ROOT = os.path.dirname(HERE)
DEFAULT_REPORT_ROOT = os.path.join(ASSIGNMENT_ROOT, "evidence", "runs")

STOP_SUCCESS = "SUCCESS"
STOP_ATTEMPTS = "CIRCUIT_BREAKER_MAX_ATTEMPTS"
STOP_REFUSED = "HUMAN_REVIEW_REFINER_REFUSED"
STOP_NO_PROGRESS = "CIRCUIT_BREAKER_NO_PROGRESS"


def _signature(violations, evaluation):
    """A fingerprint of this attempt's failures, finer-grained than rule ids."""
    if violations:
        return tuple(sorted((v.rule_id, str(v.field), str(v.actual)) for v in violations))
    if evaluation is not None:
        return tuple(sorted(
            (c["criterion"], round(c["score"], 3)) for c in evaluation["criteria"]
            if not c["passed"]))
    return ()


def _next_failure(violations, evaluation):
    """Which failure the refiner works on, and the violation behind it."""
    if violations:
        return violations[0].rule_id, violations[0]
    if evaluation is not None and evaluation["failed_criteria"]:
        return evaluation["failed_criteria"][0], None
    return None, None


def run(rules_doc, attack_id, seed, max_attempts=MAX_ATTEMPTS, kb_dir=None):
    """Run the loop. Returns a run record; writes nothing."""
    generation = generate(rules_doc, attack_id, seed, kb_dir=kb_dir)
    row = generation["row"]

    attempts = []
    last_signature = None
    stop_reason = None

    for attempt_no in range(1, max_attempts + 1):
        record = {"attempt": attempt_no, "row": dict(row)}

        violations = gate(row, rules_doc)
        record["violations"] = [v.as_dict() for v in violations]

        evaluation = None
        if not violations:
            evaluation = evaluate(row, rules_doc)
            record["evaluation"] = evaluation

        if not violations and evaluation["passed"]:
            record["outcome"] = STOP_SUCCESS
            attempts.append(record)
            stop_reason = STOP_SUCCESS
            break

        failure_key, violation = _next_failure(violations, evaluation)
        record["failure_key"] = failure_key

        signature = _signature(violations, evaluation)
        if signature == last_signature:
            record["outcome"] = STOP_NO_PROGRESS
            attempts.append(record)
            stop_reason = STOP_NO_PROGRESS
            break
        last_signature = signature

        if attempt_no == max_attempts:
            record["outcome"] = STOP_ATTEMPTS
            attempts.append(record)
            stop_reason = STOP_ATTEMPTS
            break

        refinement = refine(row, failure_key, rules_doc, violation=violation)
        record["refinement"] = refinement.as_dict()
        if not refinement.applied:
            record["outcome"] = STOP_REFUSED
            attempts.append(record)
            stop_reason = STOP_REFUSED
            break

        record["outcome"] = "REFINED"
        attempts.append(record)
        row = refinement.row

    return {
        "run_id": "attack%s-seed%d" % (attack_id, seed),
        "attack_id": attack_id,
        "seed": seed,
        "rules_version": rules_doc.get("rules_version"),
        "content_type": rules_doc.get("content_type"),
        "max_attempts": max_attempts,
        "attempts_used": len(attempts),
        "stop_reason": stop_reason,
        "drift_applied": generation["drift_applied"],
        "retrieval": generation["retrieval"],
        "final_row": row if stop_reason == STOP_SUCCESS else attempts[-1]["row"],
        "attempts": attempts,
    }


def render_markdown(result):
    out = []
    out.append("# Vanguard attack row run `%s`" % result["run_id"])
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Content type | %s |" % result["content_type"])
    out.append("| Attack | %s |" % result["attack_id"])
    out.append("| Seed | `%s` |" % result["seed"])
    out.append("| Rules | v%s |" % result["rules_version"])
    out.append("| Attempts used | %d of %d |" % (result["attempts_used"], result["max_attempts"]))
    out.append("| Stop reason | **%s** |" % result["stop_reason"])
    out.append("")

    out.append("## Retrieval — what the generator read")
    out.append("")
    out.append("GDD citations behind this row:")
    out.append("")
    for citation in result["retrieval"]["gdd_citations"]:
        out.append("- %s" % citation)
    out.append("")
    out.append("| Chunk | Score |")
    out.append("|---|---|")
    for chunk in result["retrieval"]["selected"]:
        out.append("| `%s` :: %s | %d |" % (
            chunk["source_file"], chunk["heading"], chunk["score"]))
    out.append("")

    if result["drift_applied"]:
        out.append("## Drift the generator introduced")
        out.append("")
        out.append("Seeded, so this is reproducible. The evaluator does not see this list.")
        out.append("")
        for drift in result["drift_applied"]:
            out.append("- `%s` — %s" % (drift["operator"], drift["effect"]))
        out.append("")
    else:
        out.append("## Drift the generator introduced")
        out.append("")
        out.append("None — this seed produced a clean row.")
        out.append("")

    for record in result["attempts"]:
        out.append("## Attempt %d — %s" % (record["attempt"], record["outcome"]))
        out.append("")
        if record["violations"]:
            out.append("Deterministic gate: **%d violation(s)**" % len(record["violations"]))
            out.append("")
            for violation in record["violations"]:
                out.append("- `%s` %s%s — expected %s, got `%s`" % (
                    violation["rule_id"], violation["message"],
                    " (`%s`)" % violation["field"] if violation["field"] else "",
                    violation["expected"], violation["actual"]))
            out.append("")
        else:
            out.append("Deterministic gate: **passed**")
            out.append("")
        if record.get("evaluation"):
            evaluation = record["evaluation"]
            out.append("Evaluator: **SCORE %.2f / 100**, threshold %.0f — %s" % (
                evaluation["score"], evaluation["threshold"],
                "passed" if evaluation["passed"] else "failed"))
            out.append("")
            out.append("| Criterion | Score | Weight | Passed | REASON |")
            out.append("|---|---|---|---|---|")
            for criterion in evaluation["criteria"]:
                out.append("| `%s` | %.2f | %d | %s | %s |" % (
                    criterion["criterion"], criterion["score"], criterion["weight"],
                    "yes" if criterion["passed"] else "**no**", criterion["reason"]))
            out.append("")
        if record.get("refinement"):
            refinement = record["refinement"]
            if refinement["applied"]:
                change = refinement["change"]
                out.append("Refiner changed **one** field: `%s`" % change["field"])
                out.append("")
                out.append("- before: `%s`" % change["before"])
                out.append("- after: `%s`" % change["after"])
                out.append("- why: %s" % change["reason"])
            else:
                out.append("Refiner **refused**: %s" % refinement["refused"])
            out.append("")

    if result["stop_reason"] != STOP_SUCCESS:
        out.append("---")
        out.append("")
        out.append("## Human review required")
        out.append("")
        out.append("This run stopped with `%s`. The pipeline did not guess a value, "
                   "did not write to `data/unreal/DT_VanguardAttacks.csv`, and did not "
                   "touch any Unreal asset." % result["stop_reason"])
        out.append("")
    return "\n".join(out) + "\n"


def to_csv_row(row, headers):
    """Render one row in DT_VanguardAttacks.csv column order."""
    import csv
    import io
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="")
    writer.writerow([row.get(header, "") for header in headers])
    return buffer.getvalue()


def write_report(result, rules_doc, report_root):
    run_dir = os.path.join(report_root, result["run_id"])
    os.makedirs(run_dir, exist_ok=True)
    with open(os.path.join(run_dir, "run.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    with open(os.path.join(run_dir, "run.md"), "w", encoding="utf-8") as handle:
        handle.write(render_markdown(result))
    if result["stop_reason"] == STOP_SUCCESS:
        headers = rules_doc["contract"]["headers"]
        with open(os.path.join(run_dir, "final_row.csv"), "w", encoding="utf-8") as handle:
            handle.write(",".join(headers) + "\n")
            handle.write(to_csv_row(result["final_row"], headers) + "\n")
    return run_dir


def main(argv):
    parser = argparse.ArgumentParser(
        description="Run the Vanguard attack row pipeline end to end.")
    parser.add_argument("--attack", default="A", choices=("A", "B", "C", "D"))
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--max-attempts", type=int, default=MAX_ATTEMPTS)
    parser.add_argument("--report-root", default=DEFAULT_REPORT_ROOT)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args(argv)

    try:
        with open(args.rules, "r", encoding="utf-8") as handle:
            rules_doc = json.load(handle)
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    result = run(rules_doc, args.attack, args.seed, max_attempts=args.max_attempts)

    print(render_markdown(result))
    if not args.no_report:
        run_dir = write_report(result, rules_doc, args.report_root)
        print("report written to %s" % run_dir)

    if result["stop_reason"] == STOP_SUCCESS:
        return 0
    if result["stop_reason"] == STOP_REFUSED:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
