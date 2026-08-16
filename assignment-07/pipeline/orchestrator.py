"""Orchestrator -- generate, score, refine, stop.

    attempt 1..N:
        generate (first attempt) or take the refined line
        evaluate  -> SCORE + REASON
        at or above threshold -> SUCCESS
        otherwise             -> refine the first fault, retry

The circuit breaker stops the loop on any of:

    * MAX_ATTEMPTS reached
    * the refiner refuses -- a decision that belongs to the designer
    * no progress -- the same failure signature two attempts running

Two details carried over from Assignment 06 because they earned their keep
there, and both still matter on prose:

**No-progress is measured on the failure detail, not the rule id.** A line that
breaks V1 twice -- one generic noun fixed, one still standing -- is still V1,
and a rule-id-only comparison would misread that as a stalled loop.

**The refiner only runs when an attempt remains to verify it.** Applying a
rewrite on the final attempt and exiting would end the log on an unverified
claim, which is worse than stopping one step earlier.

What is different from Assignment 06: there is no gate, so there is no way for a
line to be rejected without a score. The score is the only verdict, which is
what this assignment's brief requires.

Every attempt is written to evidence/runs/<run-id>/ as JSON plus a readable
Markdown log. Nothing here writes to the game.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import judge as judge_module  # noqa: E402
from evaluator import DEFAULT_RULES, evaluate, format_verdict  # noqa: E402
from generator import generate, slot_names  # noqa: E402
from refiner import refine  # noqa: E402

MAX_ATTEMPTS = 3
ASSIGNMENT_ROOT = os.path.dirname(HERE)
DEFAULT_REPORT_ROOT = os.path.join(ASSIGNMENT_ROOT, "evidence", "runs")

STOP_SUCCESS = "SUCCESS"
STOP_ATTEMPTS = "CIRCUIT_BREAKER_MAX_ATTEMPTS"
STOP_REFUSED = "HUMAN_REVIEW_REFINER_REFUSED"
STOP_NO_PROGRESS = "CIRCUIT_BREAKER_NO_PROGRESS"


def _signature(evaluation):
    """A fingerprint of this attempt's failures, finer-grained than rule ids."""
    return tuple(sorted((fault["rule_id"], str(fault["evidence"]))
                        for fault in evaluation["faults"]))


def _next_fault(evaluation):
    """Which fault the refiner works on. Contract order, so tone before format."""
    return evaluation["faults"][0] if evaluation["faults"] else None


def run(rules_doc, slot, seed, max_attempts=MAX_ATTEMPTS, judge_name="rubric",
        gdd_dir=None):
    """Run the loop. Returns a run record; writes nothing."""
    tone_judge = judge_module.get_judge(judge_name)
    generation = generate(rules_doc, slot, seed, gdd_dir=gdd_dir)
    line = generation["line"]
    original = dict(line)

    attempts = []
    last_signature = None
    stop_reason = None

    for attempt_no in range(1, max_attempts + 1):
        record = {"attempt": attempt_no, "line": dict(line)}

        evaluation = evaluate(line, rules_doc, tone_judge)
        record["evaluation"] = evaluation
        record["verdict"] = format_verdict(evaluation)

        if evaluation["passed"]:
            record["outcome"] = STOP_SUCCESS
            attempts.append(record)
            stop_reason = STOP_SUCCESS
            break

        fault = _next_fault(evaluation)
        record["fault_worked"] = fault

        signature = _signature(evaluation)
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

        if fault is None:
            # Below threshold with no attributable fault: the score is the
            # verdict, and there is nothing for the refiner to act on.
            record["outcome"] = STOP_ATTEMPTS
            attempts.append(record)
            stop_reason = STOP_ATTEMPTS
            break

        refinement = refine(line, fault, rules_doc)
        record["refinement"] = refinement.as_dict()
        if not refinement.applied:
            record["outcome"] = STOP_REFUSED
            attempts.append(record)
            stop_reason = STOP_REFUSED
            break

        record["outcome"] = "REFINED"
        attempts.append(record)
        line = refinement.line

    # The judge is part of the run's identity once it stops being the default:
    # two runs of the same slot and seed under different tone backends are
    # different results, and writing them to one directory loses one of them.
    suffix = "" if judge_name == "rubric" else "-%s" % judge_name

    return {
        "run_id": "%s-seed%d%s" % (slot.replace("_", "-"), seed, suffix),
        "slot": slot,
        "seed": seed,
        "judge": judge_name,
        "rules_version": rules_doc.get("rules_version"),
        "content_type": rules_doc.get("content_type"),
        "max_attempts": max_attempts,
        "attempts_used": len(attempts),
        "stop_reason": stop_reason,
        "drift_applied": generation["drift_applied"],
        "retrieval": generation["retrieval"],
        "original_line": original,
        "final_line": line if stop_reason == STOP_SUCCESS else attempts[-1]["line"],
        "attempts": attempts,
    }


def render_markdown(result):
    out = []
    out.append("# Combat copy run `%s`" % result["run_id"])
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Content type | %s |" % result["content_type"])
    out.append("| Slot | `%s` |" % result["slot"])
    out.append("| Seed | `%s` |" % result["seed"])
    out.append("| Tone judge | `%s` |" % result["judge"])
    out.append("| Rules | v%s |" % result["rules_version"])
    out.append("| Attempts used | %d of %d |" % (result["attempts_used"], result["max_attempts"]))
    out.append("| Stop reason | **%s** |" % result["stop_reason"])
    out.append("")

    out.append("## Before and after")
    out.append("")
    out.append("| | Copy |")
    out.append("|---|---|")
    out.append("| **Before** | `%s` |" % result["original_line"]["text"])
    out.append("| **After** | `%s` |" % result["final_line"]["text"])
    out.append("")

    retrieval = result["retrieval"]
    out.append("## Retrieval — what the GDD says about this slot")
    out.append("")
    out.append("**Moment:** %s" % retrieval["moment"])
    out.append("")
    slot_citation = retrieval["slot_citation"]
    out.append("**Slot source:** %s" % slot_citation["citation"])
    if slot_citation["excerpt"]:
        out.append("")
        out.append("> %s" % slot_citation["excerpt"])
    out.append("")
    out.append("| Rule | Title | GDD source | Verified |")
    out.append("|---|---|---|---|")
    for citation in retrieval["rule_citations"]:
        out.append("| `%s` | %s | %s | %s |" % (
            citation["rule_id"], citation["title"], citation["citation"],
            "yes" if citation["verified"] else "**no**"))
    out.append("")

    out.append("## Drift the generator introduced")
    out.append("")
    if result["drift_applied"]:
        out.append("Seeded, so this is reproducible. The evaluator does not see this list.")
        out.append("")
        for drift in result["drift_applied"]:
            out.append("- `%s` — %s" % (drift["operator"], drift["effect"]))
    else:
        out.append("None — this seed produced a clean line.")
    out.append("")

    for record in result["attempts"]:
        out.append("## Attempt %d — %s" % (record["attempt"], record["outcome"]))
        out.append("")
        out.append("**Copy:** `%s`" % record["line"]["text"])
        out.append("")
        out.append("```")
        out.append(record["verdict"])
        out.append("```")
        out.append("")
        evaluation = record["evaluation"]
        out.append("| Criterion | Score | Weight | Backend | Reason |")
        out.append("|---|---|---|---|---|")
        for criterion in evaluation["criteria"]:
            out.append("| `%s` | %.2f | %d | %s | %s |" % (
                criterion["criterion"], criterion["score"], criterion["weight"],
                criterion["backend"] or "deterministic", criterion["reason"]))
        out.append("")
        if evaluation["faults"]:
            out.append("Faults, in the order the refiner works them:")
            out.append("")
            for fault in evaluation["faults"]:
                out.append("- `%s` — %s" % (fault["rule_id"], fault["detail"]))
            out.append("")
        if record.get("refinement"):
            refinement = record["refinement"]
            if refinement["applied"]:
                change = refinement["change"]
                out.append("Refiner worked `%s`:" % change["rule_id"])
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
        out.append("This run stopped with `%s`. The pipeline did not invent a value, "
                   "did not settle an open design question, and wrote nothing into the "
                   "game." % result["stop_reason"])
        out.append("")
    return "\n".join(out) + "\n"


def write_report(result, report_root):
    run_dir = os.path.join(report_root, result["run_id"])
    os.makedirs(run_dir, exist_ok=True)
    with open(os.path.join(run_dir, "run.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    with open(os.path.join(run_dir, "run.md"), "w", encoding="utf-8") as handle:
        handle.write(render_markdown(result))
    if result["stop_reason"] == STOP_SUCCESS:
        with open(os.path.join(run_dir, "final_line.txt"), "w", encoding="utf-8") as handle:
            handle.write(result["final_line"]["text"] + "\n")
    return run_dir


def main(argv):
    parser = argparse.ArgumentParser(
        description="Run the combat-copy style pipeline end to end.")
    parser.add_argument("--slot", required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--judge", default="rubric", choices=sorted(judge_module.BACKENDS))
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

    if args.slot not in rules_doc["slots"]:
        print("ERROR: unknown slot %r. Known slots: %s"
              % (args.slot, ", ".join(slot_names(rules_doc))), file=sys.stderr)
        return 3

    result = run(rules_doc, args.slot, args.seed,
                 max_attempts=args.max_attempts, judge_name=args.judge)

    print(render_markdown(result))
    if not args.no_report:
        run_dir = write_report(result, args.report_root)
        print("report written to %s" % run_dir)

    if result["stop_reason"] == STOP_SUCCESS:
        return 0
    if result["stop_reason"] == STOP_REFUSED:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
