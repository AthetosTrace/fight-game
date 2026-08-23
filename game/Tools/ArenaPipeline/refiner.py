"""Refiner stage -- the smallest correction that clears one failure.

Rules this stage obeys:

1. One field per attempt. No batch rewrites, no regeneration.
2. Every change is recorded as a before/after diff.
3. If a fix would require editing something we do not own, REFUSE and escalate.
   R4 is the clearest case: the only way to fix a framing failure is to retune
   BP_DuelCameraRig, which belongs to the gameplay owner. The refiner must never
   quietly "fix" that by rewriting his camera curve.
4. If no rule matches the failure, REFUSE. Silence is not a correction.

A refusal is a legitimate outcome, not an error. The orchestrator turns it into
a human-review stop.
"""

import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_arena_plan import obstacle_half_depth, rules_by_id  # noqa: E402

# Failures we are structurally not allowed to auto-fix, and why.
REFUSALS = {
    "R4": "fixing camera framing means retuning BP_DuelCameraRig "
          "(DistancePerSeparation / MaxCameraDistance), which the gameplay owner owns",
    "R8": "moving a perimeter boundary changes the arena shell, which is a creative "
          "decision rather than a measurement correction",
    "landmark_asymmetry": "which landmark distinguishes which end is a creative decision",
    "staging_room": "changing the room-to-fight-box ratio reopens resolution U1",
}


class Refinement:
    def __init__(self, plan=None, change=None, refused=None):
        self.plan = plan
        self.change = change
        self.refused = refused

    @property
    def applied(self):
        return self.refused is None

    def as_dict(self):
        return {"applied": self.applied, "change": self.change, "refused": self.refused}


def _change(field, before, after, reason):
    return {"field": field, "before": before, "after": after, "reason": reason}


def _fix_r1(plan, rule, violation):
    required = float(rule["min_combat_span_cm"])
    before = dict(plan["combat_axis"])
    half = required / 2.0
    plan["combat_axis"]["min_cm"] = -half
    plan["combat_axis"]["max_cm"] = half
    return _change("combat_axis", before, dict(plan["combat_axis"]),
                   "widened to the minimum legal combat span")


def _fix_r2(plan, rule, violation):
    margin = float(rule["min_clearance_beyond_bound_cm"])
    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    half_depth = obstacle_half_depth(plan)
    for obstacle in plan.get("obstacles", []):
        if not obstacle.get("blocking", True):
            continue
        x = float(obstacle["x_cm"])
        if axis_min <= x <= axis_max:
            continue
        gap = (axis_min - (x + half_depth) if x < axis_min
               else (x - half_depth) - axis_max)
        if gap < margin:
            before = x
            # Push the FACE to the clearance line, so the centre lands one
            # half-depth further out. Targeting the centre re-creates the very
            # violation this fix is clearing.
            target = (axis_min - margin - half_depth if x < axis_min
                      else axis_max + margin + half_depth)
            obstacle["x_cm"] = round(target, 1)
            return _change("obstacles[%s].x_cm" % obstacle.get("name"), before,
                           obstacle["x_cm"], "pushed out to the minimum clearance")
    return None


def _fix_r3(plan, rule, violation):
    expected = float(rule["floor_z_cm"])
    if abs(float(plan["floor"]["z_cm"]) - expected) > float(rule["floor_z_tolerance_cm"]):
        before = plan["floor"]["z_cm"]
        plan["floor"]["z_cm"] = expected
        return _change("floor.z_cm", before, expected, "levelled with the combat plane")

    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    for obstacle in plan.get("obstacles", []):
        if not obstacle.get("blocking", True):
            continue
        x = float(obstacle["x_cm"])
        if axis_min <= x <= axis_max:
            before = x
            half_depth = obstacle_half_depth(plan)
            target = axis_max if x >= 0 else axis_min
            sign = 1.0 if x >= 0 else -1.0
            obstacle["x_cm"] = round(target + sign * (500.0 + half_depth), 1)
            return _change("obstacles[%s].x_cm" % obstacle.get("name"), before,
                           obstacle["x_cm"], "moved out of the fighting space")
    return None


def _fix_r5(plan, rule, violation):
    camera = plan.setdefault("camera", {})
    if not camera.get("near_wall_culled", False):
        camera["near_wall_culled"] = True
        return _change("camera.near_wall_culled", False, True,
                       "near-wall culling per resolution U2")
    return None


def _fix_r6(plan, rule, violation):
    player = plan["spawns"]["player"]
    opponent = plan["spawns"].get("opponent")
    if opponent is None:
        return None  # a missing spawn is a structural fault, not a measurement

    low = float(rule["min_axis_separation_cm"])
    high = float(rule["max_spawn_separation_cm"])
    separation = abs(float(opponent["x_cm"]) - float(player["x_cm"]))
    if separation > high or separation < low:
        target = high if separation > high else low
        before = opponent["x_cm"]
        opponent["x_cm"] = round(float(player["x_cm"]) + target, 1)
        return _change("spawns.opponent.x_cm", before, opponent["x_cm"],
                       "pulled to the %s legal opening distance"
                       % ("widest" if separation > high else "closest"))

    for label, spawn, required in (
            ("player", player, float(rule["required_player_yaw_deg"])),
            ("opponent", opponent, float(rule["required_opponent_yaw_deg"]))):
        if abs(((float(spawn["yaw_deg"]) - required + 180.0) % 360.0) - 180.0) > float(
                rule["yaw_tolerance_deg"]):
            before = spawn["yaw_deg"]
            spawn["yaw_deg"] = required
            return _change("spawns.%s.yaw_deg" % label, before, required,
                           "turned to face the opponent")

    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    for label, spawn in (("player", player), ("opponent", opponent)):
        x = float(spawn["x_cm"])
        if not (axis_min <= x <= axis_max):
            before = x
            spawn["x_cm"] = round(max(axis_min, min(axis_max, x)), 1)
            return _change("spawns.%s.x_cm" % label, before, spawn["x_cm"],
                           "clamped inside the combat bounds")
    return None


def _fix_r7(plan, rule, violation):
    required = float(rule["jump_apex_cm"]) + float(rule["character_height_cm"])
    before = plan.get("ceiling_cm")
    plan["ceiling_cm"] = required
    return _change("ceiling_cm", before, required, "raised to clear a jump-over")


def _fix_clear_central_floor(plan, rule, failure):
    """Evaluator wanted more breathing room than the hard minimum."""
    margin = float(rule["min_clearance_beyond_bound_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    axis_min = float(plan["combat_axis"]["min_cm"])
    half_depth = obstacle_half_depth(plan)
    tightest, chosen = None, None
    for obstacle in plan.get("obstacles", []):
        if not obstacle.get("blocking", True):
            continue
        x = float(obstacle["x_cm"])
        gap = (axis_min - (x + half_depth) if x < axis_min
               else (x - half_depth) - axis_max)
        if tightest is None or gap < tightest:
            tightest, chosen = gap, obstacle
    if chosen is None:
        return None
    before = chosen["x_cm"]
    sign = 1.0 if float(before) >= 0 else -1.0
    bound = axis_max if sign > 0 else axis_min
    # Clamped to the end wall: on a 2400 cm long axis the annulus between the
    # clearance line and the shell is only 50 cm deep, so an unclamped push
    # would put the landmark through the wall.
    half_long = float(plan["floor"]["long_axis_cm"]) / 2.0
    target = bound + sign * (margin * 1.2 + half_depth)
    limit = sign * (half_long - half_depth)
    chosen["x_cm"] = round(min(target, limit) if sign > 0 else max(target, limit), 1)
    return _change("obstacles[%s].x_cm" % chosen.get("name"), before, chosen["x_cm"],
                   "opened up the fighting space beyond the bare minimum")


def _fix_boundary_readability(plan, rule, failure):
    boundaries = plan.setdefault("boundaries", [])
    half_short = float(plan["floor"]["short_axis_cm"]) / 2.0
    if not any(float(b.get("y_cm", 0.0)) > 0 for b in boundaries):
        boundaries.append({"name": "Railing_North", "x_cm": 0.0, "y_cm": half_short})
        return _change("boundaries", "no north boundary", "Railing_North",
                       "added the missing boundary so the edge reads from both sides")
    if not any(float(b.get("y_cm", 0.0)) < 0 for b in boundaries):
        boundaries.append({"name": "Railing_South", "x_cm": 0.0, "y_cm": -half_short})
        return _change("boundaries", "no south boundary", "Railing_South",
                       "added the missing boundary so the edge reads from both sides")
    return None


FIXES = {
    "R1": _fix_r1,
    "R2": _fix_r2,
    "R3": _fix_r3,
    "R5": _fix_r5,
    "R6": _fix_r6,
    "R7": _fix_r7,
    "clear_central_floor": _fix_clear_central_floor,
    "boundary_readability": _fix_boundary_readability,
}

# Which rule's thresholds each evaluator-criterion fix reads from.
CRITERION_RULE = {
    "clear_central_floor": "R2",
    "boundary_readability": "R2",
}


def refine(plan, failure_key, rules_doc):
    """Apply the smallest correction for one failure. Never mutates the input."""
    if failure_key in REFUSALS:
        return Refinement(refused="cannot safely fix %s: %s" % (failure_key, REFUSALS[failure_key]))

    fix = FIXES.get(failure_key)
    if fix is None:
        return Refinement(refused="no refinement rule exists for %s" % failure_key)

    lookup = rules_by_id(rules_doc)
    rule = lookup.get(CRITERION_RULE.get(failure_key, failure_key))
    if rule is None:
        return Refinement(refused="no rule data backing a fix for %s" % failure_key)

    candidate = copy.deepcopy(plan)
    change = fix(candidate, rule, failure_key)
    if change is None:
        return Refinement(refused="%s reported a failure the refiner could not locate" % failure_key)
    return Refinement(plan=candidate, change=change)
