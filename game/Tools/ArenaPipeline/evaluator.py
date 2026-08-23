"""Evaluator stage -- game-specific judgement of a plan that already passed the
deterministic gate.

The deterministic validator answers "is this legal?". The evaluator answers "is
this a good duel arena?" -- readability, orientation, staging room. Those are
criteria the measured rules cannot express.

Two backends behind one interface:

  heuristic  (default) a scored rubric. Offline, deterministic, reproducible,
             needs no API key. This is what runs in tests and in reports.
  agent      an LLM judge. Not implemented yet; the seam exists so it can be
             added without changing the orchestrator.

Criteria come from gdd/reference/page-11-established-arena-reference.md in the
design repo. This stage judges graybox layout only. Whether the result *feels*
like the Shattered Ring is the gameplay owner's creative approval, not ours.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_arena_plan import DEFAULT_RULES, load_json, rules_by_id  # noqa: E402

PASS_THRESHOLD = 70.0


class CriterionResult:
    def __init__(self, key, score, weight, passed, note, fix_hint=None):
        self.key = key
        self.score = score
        self.weight = weight
        self.passed = passed
        self.note = note
        self.fix_hint = fix_hint

    def as_dict(self):
        return {
            "criterion": self.key,
            "score": round(self.score, 3),
            "weight": self.weight,
            "passed": self.passed,
            "note": self.note,
            "fix_hint": self.fix_hint,
        }


def _clear_central_floor(plan, lookup):
    """The reference sheet: 'the central floor is completely clear'."""
    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    margin = float(lookup["R2"]["min_clearance_beyond_bound_cm"])
    intruders = 0
    tightest = None
    for obstacle in plan.get("obstacles", []):
        if not obstacle.get("blocking", True):
            continue
        x = float(obstacle["x_cm"])
        gap = axis_min - x if x < axis_min else x - axis_max if x > axis_max else 0.0
        if gap <= 0.0:
            intruders += 1
        tightest = gap if tightest is None else min(tightest, gap)

    if intruders:
        return CriterionResult("clear_central_floor", 0.0, 30, False,
                               "%d blocking object(s) inside the fighting space" % intruders,
                               "move them beyond the combat bound")
    if tightest is None:
        return CriterionResult("clear_central_floor", 1.0, 30, True, "no blocking geometry at all")
    # Full marks at 2x the required margin; linear below that.
    score = min(1.0, tightest / (margin * 2.0))
    return CriterionResult("clear_central_floor", score, 30, score >= 0.5,
                           "tightest blocking object sits %.0f cm beyond the bound" % tightest,
                           "increase landmark offset from the combat bound")


def _landmark_asymmetry(plan, lookup):
    """The two ends must be tellable apart -- doorway end vs truss end. Without
    that the player cannot orient after a jump-over side switch."""
    names_pos = {o["name"] for o in plan.get("obstacles", []) if float(o["x_cm"]) > 0}
    names_neg = {o["name"] for o in plan.get("obstacles", []) if float(o["x_cm"]) < 0}
    if not names_pos or not names_neg:
        return CriterionResult("landmark_asymmetry", 0.0, 25, False,
                               "one end of the arena has no landmark at all", None)
    if names_pos == names_neg:
        return CriterionResult("landmark_asymmetry", 0.0, 25, False,
                               "both ends carry identical landmarks", None)
    return CriterionResult("landmark_asymmetry", 1.0, 25, True,
                           "ends are distinguishable: %s vs %s"
                           % (sorted(names_pos), sorted(names_neg)))


def _boundary_readability(plan, lookup):
    """Orange railings sit on the boundary line in the reference -- the player
    must be able to see where the edge is from either side."""
    boundaries = plan.get("boundaries", [])
    has_north = any(float(b.get("y_cm", 0.0)) > 0 for b in boundaries)
    has_south = any(float(b.get("y_cm", 0.0)) < 0 for b in boundaries)
    ends = sum(1 for b in boundaries if float(b.get("y_cm", 0.0)) == 0.0)
    score = (0.4 if has_north else 0.0) + (0.4 if has_south else 0.0) + (0.2 if ends >= 2 else 0.0)
    passed = score >= 0.8
    missing = []
    if not has_north:
        missing.append("north side")
    if not has_south:
        missing.append("south side")
    return CriterionResult("boundary_readability", score, 25, passed,
                           "missing boundary on %s" % ", ".join(missing) if missing
                           else "boundary readable on both long sides",
                           "add a boundary element on the missing side" if missing else None)


def _staging_room(plan, lookup):
    """The Final Clash needs room outside the fight box. Score the ratio of the
    room's long axis to the combat span."""
    long_axis = float(plan["floor"]["long_axis_cm"])
    span = float(plan["combat_axis"]["max_cm"]) - float(plan["combat_axis"]["min_cm"])
    ratio = long_axis / span if span else 0.0
    # 1.0 = no staging room at all; 1.85 (the designed 2400/1300) = full marks.
    score = max(0.0, min(1.0, (ratio - 1.0) / 0.85))
    return CriterionResult("staging_room", score, 20, score >= 0.5,
                           "room is %.2fx the combat span" % ratio,
                           "widen the arena long axis relative to the combat span")


CRITERIA = (_clear_central_floor, _landmark_asymmetry, _boundary_readability, _staging_room)


def evaluate_heuristic(plan, rules_doc):
    lookup = rules_by_id(rules_doc)
    results = [criterion(plan, lookup) for criterion in CRITERIA]
    total_weight = sum(r.weight for r in results)
    score = sum(r.score * r.weight for r in results) / total_weight * 100.0
    return {
        "judge": "heuristic",
        "score": round(score, 2),
        "threshold": PASS_THRESHOLD,
        "passed": score >= PASS_THRESHOLD and all(r.passed for r in results),
        "criteria": [r.as_dict() for r in results],
        "failed_criteria": [r.key for r in results if not r.passed],
    }


def evaluate(plan, rules_doc, judge="heuristic"):
    if judge == "heuristic":
        return evaluate_heuristic(plan, rules_doc)
    if judge == "agent":
        raise NotImplementedError(
            "the LLM judge backend is not built yet -- run with judge='heuristic'")
    raise ValueError("unknown judge backend: %s" % judge)


def main(argv):
    parser = argparse.ArgumentParser(description="Evaluate an arena plan.")
    parser.add_argument("plan")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--judge", default="heuristic", choices=("heuristic", "agent"))
    args = parser.parse_args(argv)

    try:
        plan = load_json(args.plan, "arena plan")
        rules_doc = load_json(args.rules, "arena rules")
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    try:
        report = evaluate(plan, rules_doc, judge=args.judge)
    except NotImplementedError as exc:
        print("HUMAN REVIEW: %s" % exc, file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
