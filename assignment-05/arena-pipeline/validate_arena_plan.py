"""Deterministic validator for an Ascendant Impact arena plan.

Checks an arena plan JSON against contracts/arena_rules.json before any agent
evaluation runs. Exits 0 if the plan passes every rule, exits 1 and prints every
violation found otherwise. This script invents nothing -- every threshold it
enforces is sourced from a project document, and it refuses to treat a PROPOSED
design value as an approved requirement.

Exit codes:
    0  plan passed every applicable rule
    1  one or more rule violations
    2  human review required (unresolved input, or a PROPOSED value was needed
       and --allow-proposed was not passed)
    3  bad usage / unreadable input
"""

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES = os.path.join(HERE, "contracts", "arena_rules.json")

# Statuses that may be enforced as hard requirements without a human waiver.
BINDING_STATUSES = ("MEASURED", "APPROVED", "DERIVED")


class Violation:
    """A single failed check. Ordered by rule id for stable report output."""

    def __init__(self, rule_id, message, expected=None, actual=None):
        self.rule_id = rule_id
        self.message = message
        self.expected = expected
        self.actual = actual

    def as_dict(self):
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "expected": self.expected,
            "actual": self.actual,
        }

    def __str__(self):
        detail = ""
        if self.expected is not None or self.actual is not None:
            detail = " (expected %s, got %s)" % (self.expected, self.actual)
        return "%s: %s%s" % (self.rule_id, self.message, detail)


def load_json(path, label):
    if not os.path.isfile(path):
        raise IOError("%s not found: %s" % (label, path))
    with open(path, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except ValueError as exc:
            raise IOError("%s is not valid JSON: %s" % (label, exc))


def rules_by_id(rules_doc):
    return {rule["id"]: rule for rule in rules_doc.get("rules", [])}


def _obstacles(plan):
    return [o for o in plan.get("obstacles", []) if o.get("blocking", True)]


def obstacle_half_depth(plan):
    """Half the along-axis footprint the plan reserves for each obstacle.

    Clearance in R2's source is a distance between the combat bound and real
    environment geometry, and geometry has faces. A plan that declares no
    footprint degrades to the historical point behaviour (half-depth 0), which
    keeps hand-written and archived plans valid.
    """
    return float(plan.get("obstacle_extents", {}).get("depth_cm", 0.0)) / 2.0


def _span(combat_axis):
    return float(combat_axis["max_cm"]) - float(combat_axis["min_cm"])


def check_r1_combat_span(plan, rule):
    """Combat axis must be wide enough for the maximum legal separation."""
    span = _span(plan["combat_axis"])
    required = float(rule["min_combat_span_cm"])
    if span < required:
        return [Violation("R1", "combat axis span is too narrow for max legal separation",
                          ">= %.1f cm" % required, "%.1f cm" % span)]
    return []


def check_r2_clearance(plan, rule):
    """Blocking geometry must sit clear of the combat bounds.

    Measured to the obstacle's NEAR FACE, not its centre. A centre-based check
    passes geometry whose face is already inside the clearance band, and the
    error is exactly one half-depth -- invisible on paper, real in the level.
    """
    out = []
    margin = float(rule["min_clearance_beyond_bound_cm"])
    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    half_depth = obstacle_half_depth(plan)
    for obstacle in _obstacles(plan):
        x = float(obstacle["x_cm"])
        if axis_min <= x <= axis_max:
            continue  # handled by R3 as an in-volume violation
        gap = (axis_min - (x + half_depth) if x < axis_min
               else (x - half_depth) - axis_max)
        if gap < margin:
            out.append(Violation(
                "R2",
                "obstacle '%s' crowds the combat bound" % obstacle.get("name", "<unnamed>"),
                ">= %.1f cm clearance" % margin, "%.1f cm" % gap))
    return out


def check_r3_flat_floor(plan, rule):
    """Floor sits at Z=0 and nothing blocks the fighting space."""
    out = []
    expected_z = float(rule["floor_z_cm"])
    tolerance = float(rule["floor_z_tolerance_cm"])
    actual_z = float(plan["floor"]["z_cm"])
    if abs(actual_z - expected_z) > tolerance:
        out.append(Violation("R3", "floor top is not level with the combat plane",
                             "%.1f +/- %.1f cm" % (expected_z, tolerance), "%.1f cm" % actual_z))

    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    for obstacle in _obstacles(plan):
        if axis_min <= float(obstacle["x_cm"]) <= axis_max:
            out.append(Violation(
                "R3",
                "blocking obstacle '%s' sits inside the combat volume" % obstacle.get("name", "<unnamed>"),
                "clear combat volume", "x = %.1f cm" % float(obstacle["x_cm"])))
    return out


def camera_distance_for_separation(separation_cm, rule):
    """Reproduces BP_DuelCameraRig's distance curve: base + k*S, clamped."""
    raw = float(rule["base_camera_distance_cm"]) + float(rule["distance_per_separation"]) * separation_cm
    return max(float(rule["min_camera_distance_cm"]),
               min(float(rule["max_camera_distance_cm"]), raw))


def check_r4_camera_framing(plan, rule):
    """At worst-case separation both fighters must still be on screen."""
    separation = _span(plan["combat_axis"])
    distance = camera_distance_for_separation(separation, rule)
    half_width = distance * float(rule["half_width_per_distance"])
    needed = separation / 2.0 + float(rule["fighter_body_margin_cm"])
    if half_width < needed:
        return [Violation("R4", "camera cannot frame both fighters at maximum separation",
                          ">= %.1f cm half-width" % needed, "%.1f cm" % half_width)]
    return []


def required_camera_depth(plan, r4_rule, r5_rule):
    """How far back the camera sits at the plan's worst-case separation."""
    distance = camera_distance_for_separation(_span(plan["combat_axis"]), r4_rule)
    return distance * math.cos(math.radians(float(r5_rule["side_angle_deg"])))


def check_r5_camera_corridor(plan, rule, r4_rule=None):
    """No blocking gameplay geometry in the corridor, and the shell must either
    contain the camera or be flagged cullable (resolution U2)."""
    out = []
    if r4_rule is not None:
        needed = required_camera_depth(plan, r4_rule, rule)
        available = float(plan["floor"]["short_axis_cm"]) / 2.0
        culled = plan.get("camera", {}).get("near_wall_culled", False)
        if available < needed and not culled:
            out.append(Violation(
                "R5",
                "floor is too shallow for the camera pull-back and the near wall is not "
                "flagged cullable (set camera.near_wall_culled)",
                ">= %.1f cm depth" % needed, "%.1f cm" % available))

    for obstacle in _obstacles(plan):
        if obstacle.get("in_camera_corridor", False):
            out.append(Violation("R5", "obstacle '%s' occludes the camera corridor"
                                 % obstacle.get("name", "<unnamed>"), "clear corridor", "occluded"))
    return out


def check_r6_spawns(plan, rule):
    """Two spawns, on the floor, facing each other, legally separated."""
    out = []
    spawns = plan.get("spawns", {})
    player = spawns.get("player")
    opponent = spawns.get("opponent")
    if not player or not opponent:
        return [Violation("R6", "plan must define both a player and an opponent spawn",
                          "2 spawns", "%d" % len(spawns))]

    separation = abs(float(opponent["x_cm"]) - float(player["x_cm"]))
    low = float(rule["min_axis_separation_cm"])
    high = float(rule["max_spawn_separation_cm"])
    if separation < low:
        out.append(Violation("R6", "spawns are closer than the minimum axis separation",
                             ">= %.1f cm" % low, "%.1f cm" % separation))
    elif separation > high:
        out.append(Violation("R6", "spawns are further apart than the approved opening distance",
                             "<= %.1f cm" % high, "%.1f cm" % separation))

    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    for label, spawn in (("player", player), ("opponent", opponent)):
        x = float(spawn["x_cm"])
        if not (axis_min <= x <= axis_max):
            out.append(Violation("R6", "%s spawn is outside the combat bounds" % label,
                                 "[%.1f, %.1f]" % (axis_min, axis_max), "%.1f cm" % x))

    tolerance = float(rule["yaw_tolerance_deg"])
    for label, spawn, required in (
            ("player", player, float(rule["required_player_yaw_deg"])),
            ("opponent", opponent, float(rule["required_opponent_yaw_deg"]))):
        yaw = float(spawn["yaw_deg"])
        if abs(((yaw - required + 180.0) % 360.0) - 180.0) > tolerance:
            out.append(Violation("R6", "%s spawn does not face the opponent" % label,
                                 "%.1f deg" % required, "%.1f deg" % yaw))
    return out


def check_r7_headroom(plan, rule):
    """Jump-over side switching must clear overhead geometry."""
    needed = float(rule["jump_apex_cm"]) + float(rule["character_height_cm"])
    ceiling = plan.get("ceiling_cm")
    if ceiling is None:
        return [Violation("R7", "plan does not state a ceiling height",
                          ">= %.1f cm" % needed, "unstated")]
    if float(ceiling) < needed:
        return [Violation("R7", "not enough headroom for a jump-over",
                          ">= %.1f cm" % needed, "%.1f cm" % float(ceiling))]
    return []


def check_r8_boundary(plan, rule):
    """Perimeter geometry must enclose, never intrude on, the combat volume.

    Only boundaries that face along the combat axis are constrained by it. A side
    railing runs parallel to the combat axis and legitimately crosses x = 0, so it
    is not an intrusion. Boundaries declare this with `axis`; absent, "x" is
    assumed, which is the conservative reading.
    """
    out = []
    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    for boundary in plan.get("boundaries", []):
        if boundary.get("axis", "x").lower() != "x":
            continue
        x = float(boundary["x_cm"])
        if axis_min <= x <= axis_max:
            out.append(Violation("R8", "boundary '%s' intrudes into the combat volume"
                                 % boundary.get("name", "<unnamed>"),
                                 "outside [%.1f, %.1f]" % (axis_min, axis_max), "%.1f cm" % x))
    return out


CHECKS = {
    "R1": check_r1_combat_span,
    "R2": check_r2_clearance,
    "R3": check_r3_flat_floor,
    "R4": check_r4_camera_framing,
    "R5": check_r5_camera_corridor,
    "R6": check_r6_spawns,
    "R7": check_r7_headroom,
    "R8": check_r8_boundary,
}

REQUIRED_PLAN_KEYS = ("schema_version", "floor", "combat_axis", "spawns")


def validate(plan, rules_doc, allow_proposed=False):
    """Run every rule.

    Returns (violations, human_review_reasons, decisions).

    `review` means the pipeline cannot safely proceed and must stop.
    `decisions` are clashes we resolved ourselves and are carrying forward
    pending the gameplay owner's confirmation -- reported, but not blocking.
    """
    review = []
    decisions = []
    violations = []

    missing = [key for key in REQUIRED_PLAN_KEYS if key not in plan]
    if missing:
        return ([Violation("SCHEMA", "plan is missing required keys: %s" % ", ".join(missing))],
                review, decisions)

    for item in rules_doc.get("unresolved", []):
        resolution = item.get("resolution")
        if resolution is None:
            review.append("UNRESOLVED %s: %s (owner: %s, blocks: %s)" % (
                item["id"], item["question"], item.get("owner", "?"),
                ", ".join(item.get("blocks", [])) or "none"))
        elif resolution.get("status") == "PENDING_CONFIRMATION":
            decisions.append("%s resolved by us, awaiting %s: %s" % (
                item["id"], resolution.get("confirm_with", "the owner"), resolution["decision"]))

    lookup = rules_by_id(rules_doc)
    for rule_id, check in sorted(CHECKS.items()):
        rule = lookup.get(rule_id)
        if rule is None:
            review.append("rule %s is referenced by the validator but absent from the rules file" % rule_id)
            continue
        status = rule.get("status")
        if status not in BINDING_STATUSES:
            if not allow_proposed:
                review.append("rule %s has status %s and cannot be enforced without approval "
                              "(pass --allow-proposed to evaluate it anyway)" % (rule_id, status))
                continue
            review.append("rule %s enforced from a %s value under --allow-proposed" % (rule_id, status))
        if rule_id == "R5":
            violations.extend(check(plan, rule, lookup.get("R4")))
        else:
            violations.extend(check(plan, rule))

    return (violations, review, decisions)


def main(argv):
    parser = argparse.ArgumentParser(description="Validate an Ascendant Impact arena plan.")
    parser.add_argument("plan", help="path to the arena plan JSON")
    parser.add_argument("--rules", default=DEFAULT_RULES, help="path to arena_rules.json")
    parser.add_argument("--allow-proposed", action="store_true",
                        help="enforce rules whose source value is still PROPOSED")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args(argv)

    try:
        plan = load_json(args.plan, "arena plan")
        rules_doc = load_json(args.rules, "arena rules")
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    violations, review, decisions = validate(plan, rules_doc, allow_proposed=args.allow_proposed)

    if args.json:
        print(json.dumps({
            "plan": os.path.basename(args.plan),
            "rules_version": rules_doc.get("rules_version"),
            "passed": not violations,
            "violations": [v.as_dict() for v in violations],
            "human_review": review,
            "decisions_pending_confirmation": decisions,
        }, indent=2))
    else:
        print("arena plan: %s" % args.plan)
        print("rules      : v%s" % rules_doc.get("rules_version"))
        if decisions:
            print("\nDECIDED BY US, PENDING CONFIRMATION (%d):" % len(decisions))
            for note in decisions:
                print("  - %s" % note)
        if review:
            print("\nHUMAN REVIEW REQUIRED (%d):" % len(review))
            for note in review:
                print("  - %s" % note)
        if violations:
            print("\nFAILED (%d violation%s):" % (len(violations), "" if len(violations) == 1 else "s"))
            for violation in violations:
                print("  - %s" % violation)
        else:
            print("\nPASSED: no rule violations.")

    if violations:
        return 1
    if review:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
