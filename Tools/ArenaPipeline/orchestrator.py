"""Orchestrator -- generate, validate, evaluate, refine, stop.

    attempt 1..N:
        generate (first attempt) or take the refined plan
        deterministic gate      -> violations? refine and retry
        evaluator               -> criteria failed? refine and retry
        both clean              -> SUCCESS

The circuit breaker stops the loop on any of:

    * MAX_ATTEMPTS reached
    * the refiner refuses (a fix we are not allowed or able to make)
    * no progress -- the same failure signature two attempts running

Every attempt is written to reports/arena/<run-id>/ as JSON plus a readable
Markdown log. Nothing here touches Unreal.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_arena_plan import DEFAULT_RULES, load_json, validate  # noqa: E402
from generator import generate  # noqa: E402
from evaluator import evaluate  # noqa: E402
from refiner import refine  # noqa: E402

MAX_ATTEMPTS = 3
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_REPORT_ROOT = os.path.join(REPO_ROOT, "reports", "arena")

STOP_SUCCESS = "SUCCESS"
STOP_ATTEMPTS = "CIRCUIT_BREAKER_MAX_ATTEMPTS"
STOP_REFUSED = "HUMAN_REVIEW_REFINER_REFUSED"
STOP_NO_PROGRESS = "CIRCUIT_BREAKER_NO_PROGRESS"
STOP_REVIEW = "HUMAN_REVIEW_REQUIRED"


def _failure_keys(violations, evaluation):
    """Which rules/criteria failed -- used to choose what the refiner works on."""
    keys = sorted({v.rule_id for v in violations})
    if not keys and evaluation is not None:
        keys = sorted(evaluation["failed_criteria"])
    return keys


def _signature(violations, evaluation):
    """A detailed fingerprint of this attempt's failures.

    Deliberately finer-grained than the rule ids: fixing one of two R2 obstacles
    is real progress even though R2 still fails, and a rule-id-only signature
    would misread that as a stalled loop.
    """
    if violations:
        return tuple(sorted((v.rule_id, v.message, str(v.actual)) for v in violations))
    if evaluation is not None:
        return tuple(sorted(
            (c["criterion"], round(c["score"], 3)) for c in evaluation["criteria"]
            if not c["passed"]))
    return ()


def run(rules_doc, seed, max_attempts=MAX_ATTEMPTS, judge="heuristic"):
    """Run the loop. Returns a run record; writes nothing."""
    attempts = []
    plan = generate(rules_doc, seed)
    last_signature = None
    stop_reason = None

    for attempt_no in range(1, max_attempts + 1):
        record = {"attempt": attempt_no, "plan": plan}

        violations, review, decisions = validate(plan, rules_doc)
        record["violations"] = [v.as_dict() for v in violations]
        record["human_review"] = review
        record["decisions_pending_confirmation"] = decisions

        if review:
            record["outcome"] = STOP_REVIEW
            attempts.append(record)
            stop_reason = STOP_REVIEW
            break

        evaluation = None
        if not violations:
            try:
                evaluation = evaluate(plan, rules_doc, judge=judge)
            except NotImplementedError as exc:
                record["outcome"] = STOP_REVIEW
                record["human_review"] = [str(exc)]
                attempts.append(record)
                stop_reason = STOP_REVIEW
                break
            record["evaluation"] = evaluation

        if not violations and evaluation["passed"]:
            record["outcome"] = STOP_SUCCESS
            attempts.append(record)
            stop_reason = STOP_SUCCESS
            break

        signature = _signature(violations, evaluation)
        failure_keys = _failure_keys(violations, evaluation)
        record["failure_keys"] = failure_keys

        if signature == last_signature:
            record["outcome"] = STOP_NO_PROGRESS
            attempts.append(record)
            stop_reason = STOP_NO_PROGRESS
            break
        last_signature = signature

        # Only refine if an attempt remains to verify the result. Applying a
        # correction we never re-validate would end the log on an unverified
        # claim, which is worse than stopping one step earlier.
        if attempt_no == max_attempts:
            record["outcome"] = STOP_ATTEMPTS
            attempts.append(record)
            stop_reason = STOP_ATTEMPTS
            break

        refinement = refine(plan, failure_keys[0], rules_doc)
        record["refinement"] = refinement.as_dict()
        if not refinement.applied:
            record["outcome"] = STOP_REFUSED
            attempts.append(record)
            stop_reason = STOP_REFUSED
            break

        record["outcome"] = "REFINED"
        attempts.append(record)
        plan = refinement.plan
    else:
        stop_reason = STOP_ATTEMPTS

    return {
        "run_id": "seed%d" % seed,
        "seed": seed,
        "judge": judge,
        "rules_version": rules_doc.get("rules_version"),
        "max_attempts": max_attempts,
        "attempts_used": len(attempts),
        "stop_reason": stop_reason,
        "final_plan": attempts[-1]["plan"] if stop_reason != STOP_SUCCESS else plan,
        "attempts": attempts,
    }


def render_markdown(result):
    out = []
    out.append("# Arena pipeline run `%s`" % result["run_id"])
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Seed | `%s` |" % result["seed"])
    out.append("| Rules | v%s |" % result["rules_version"])
    out.append("| Judge | %s |" % result["judge"])
    out.append("| Attempts used | %d of %d |" % (result["attempts_used"], result["max_attempts"]))
    out.append("| Stop reason | **%s** |" % result["stop_reason"])
    out.append("")

    for record in result["attempts"]:
        out.append("## Attempt %d -- %s" % (record["attempt"], record["outcome"]))
        out.append("")
        if record["decisions_pending_confirmation"]:
            out.append("Decisions carried forward, pending confirmation:")
            out.append("")
            for note in record["decisions_pending_confirmation"]:
                out.append("- %s" % note)
            out.append("")
        if record["human_review"]:
            out.append("**Human review required:**")
            out.append("")
            for note in record["human_review"]:
                out.append("- %s" % note)
            out.append("")
        if record["violations"]:
            out.append("Deterministic gate: **%d violation(s)**" % len(record["violations"]))
            out.append("")
            for violation in record["violations"]:
                out.append("- `%s` %s (expected %s, got %s)" % (
                    violation["rule_id"], violation["message"],
                    violation["expected"], violation["actual"]))
            out.append("")
        else:
            out.append("Deterministic gate: **passed**")
            out.append("")
        if record.get("evaluation"):
            evaluation = record["evaluation"]
            out.append("Evaluator (`%s`): **%.2f / 100**, threshold %.0f -- %s" % (
                evaluation["judge"], evaluation["score"], evaluation["threshold"],
                "passed" if evaluation["passed"] else "failed"))
            out.append("")
            out.append("| Criterion | Score | Weight | Passed | Note |")
            out.append("|---|---|---|---|---|")
            for criterion in evaluation["criteria"]:
                out.append("| `%s` | %.2f | %d | %s | %s |" % (
                    criterion["criterion"], criterion["score"], criterion["weight"],
                    "yes" if criterion["passed"] else "**no**", criterion["note"]))
            out.append("")
        if record.get("refinement"):
            refinement = record["refinement"]
            if refinement["applied"]:
                change = refinement["change"]
                out.append("Refiner changed **one** field: `%s` `%s` -> `%s` (%s)" % (
                    change["field"], change["before"], change["after"], change["reason"]))
            else:
                out.append("Refiner **refused**: %s" % refinement["refused"])
            out.append("")

    if result["stop_reason"] != STOP_SUCCESS:
        out.append("---")
        out.append("")
        out.append("## Human review required")
        out.append("")
        out.append("This run stopped with `%s`. The pipeline did not guess a value "
                   "and did not modify any Unreal asset." % result["stop_reason"])
        out.append("")
    return "\n".join(out) + "\n"


def write_report(result, report_root):
    run_dir = os.path.join(report_root, result["run_id"])
    os.makedirs(run_dir, exist_ok=True)
    with open(os.path.join(run_dir, "run.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    with open(os.path.join(run_dir, "run.md"), "w", encoding="utf-8") as handle:
        handle.write(render_markdown(result))
    with open(os.path.join(run_dir, "final_plan.json"), "w", encoding="utf-8") as handle:
        json.dump(result["final_plan"], handle, indent=2)
    return run_dir


def main(argv):
    parser = argparse.ArgumentParser(description="Run the arena pipeline end to end.")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--max-attempts", type=int, default=MAX_ATTEMPTS)
    parser.add_argument("--judge", default="heuristic", choices=("heuristic", "agent"))
    parser.add_argument("--report-root", default=DEFAULT_REPORT_ROOT)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args(argv)

    try:
        rules_doc = load_json(args.rules, "arena rules")
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    result = run(rules_doc, args.seed, max_attempts=args.max_attempts, judge=args.judge)

    print(render_markdown(result))
    if not args.no_report:
        run_dir = write_report(result, args.report_root)
        print("report written to %s" % run_dir)

    if result["stop_reason"] == STOP_SUCCESS:
        return 0
    if result["stop_reason"] in (STOP_REVIEW, STOP_REFUSED):
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
