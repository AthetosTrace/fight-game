"""Generator stage -- produces an arena plan from the sourced rules.

Parametric and seeded: the same seed always produces the same plan, so any run
in a report can be reproduced exactly. The generator invents no requirements; it
reads its targets from contracts/arena_rules.json.

It deliberately samples some parameters from ranges wider than the legal ones.
A generator that could only emit valid plans would make the validator, refiner
and circuit breaker untestable -- and would not resemble a real generator.
"""

import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_arena_plan import DEFAULT_RULES, load_json, rules_by_id  # noqa: E402

SCHEMA_VERSION = "1.0.0"

# Sampling ranges. Slightly wider than the legal bands on purpose -- see the
# module docstring. Tuned so a typical seed needs one or two corrections, which
# is what a three-attempt circuit breaker is sized for.
SPAWN_SEPARATION_RANGE_CM = (200.0, 420.0)   # legal: [78, 350]
OBSTACLE_OFFSET_RANGE_CM = (470.0, 650.0)    # legal: >= 500 beyond the bound
CEILING_CHOICES_CM = (380.0, 450.0, 450.0, 520.0)   # legal: >= 388

# The plan is dimensionless, but the geometry it becomes is not. An obstacle
# whose CENTRE clears the combat bound by 500 cm has a near face that does not,
# so the sampled offset is measured to the near face and the centre is pushed
# out by the graybox half-depth. Without this the materializer's face re-check
# rejects plans the deterministic gate passed. See materializer.py.
DEFAULT_OBSTACLE_DEPTH_CM = 0.0
DEFAULT_OBSTACLE_WIDTH_CM = 0.0

LANDMARKS = (
    ("Doorway_Frame", 1),      # +X end, the Vanguard entrance from GDD section 08
    ("Truss_Panel", -1),       # -X end, the X-braced landmark from the reference sheet
    ("Mezzanine_Strut_A", 1),
    ("Mezzanine_Strut_B", -1),
)


def generate(rules_doc, seed):
    """Build one arena plan. Deterministic for a given seed."""
    rng = random.Random(seed)
    lookup = rules_by_id(rules_doc)
    targets = rules_doc["design_targets"]

    long_axis = float(targets["playable_long_axis_cm"])
    short_axis = float(targets["playable_short_axis_cm"])
    combat_span = float(lookup["R1"]["min_combat_span_cm"])
    half_combat = combat_span / 2.0
    half_long = long_axis / 2.0

    separation = round(rng.uniform(*SPAWN_SEPARATION_RANGE_CM), 1)
    player_x = round(-separation / 2.0, 1)
    opponent_x = round(separation / 2.0, 1)

    # Reserve the graybox footprint the materializer will give these landmarks,
    # so the plan is legal both as points and as boxes.
    extents = rules_doc.get("materializer", {})
    half_depth = float(extents.get("obstacle_depth_cm", DEFAULT_OBSTACLE_DEPTH_CM)) / 2.0
    half_width = float(extents.get("obstacle_width_cm", DEFAULT_OBSTACLE_WIDTH_CM)) / 2.0

    # The far face must stay inside the end wall, and the near face must clear
    # the combat bound. On a 2400 cm long axis those two limits meet almost
    # exactly -- the annulus is only 50 cm deep -- so this clamp is load-bearing.
    max_center = half_long - half_depth
    max_y = max(0.0, short_axis / 2.0 - half_width)

    # Landmarks sharing an end also share an X plane -- the annulus is far too
    # shallow to stagger them in depth -- so their Y bands are partitioned
    # rather than sampled independently. Drawing both from the full range put
    # one landmark inside the other on roughly three seeds in five.
    per_side_total = {}
    for _, side in LANDMARKS:
        per_side_total[side] = per_side_total.get(side, 0) + 1
    per_side_index = {}

    obstacles = []
    for name, side in LANDMARKS:
        slot = per_side_index.get(side, 0)
        per_side_index[side] = slot + 1
        band = (2.0 * max_y) / per_side_total[side]
        low = -max_y + slot * band + half_width
        high = -max_y + (slot + 1) * band - half_width
        if high < low:  # band too narrow to jitter within; centre it
            low = high = (low + high) / 2.0

        offset = round(rng.uniform(*OBSTACLE_OFFSET_RANGE_CM), 1)
        x = side * min(half_combat + offset + half_depth, max_center)
        obstacles.append({
            "name": name,
            "x_cm": round(x, 1),
            "y_cm": round(rng.uniform(low, high), 1),
            "blocking": True,
            "in_camera_corridor": False,
        })

    return {
        "schema_version": SCHEMA_VERSION,
        "plan_id": "gen-seed%d" % seed,
        "seed": seed,
        "generated_by": "Tools/ArenaPipeline/generator.py",
        "provenance": {
            "floor_footprint": targets["source"],
            "combat_span": lookup["R1"]["source"],
            "resolutions_applied": ["U1", "U2"],
        },
        "floor": {
            "long_axis_cm": long_axis,
            "short_axis_cm": short_axis,
            "z_cm": float(lookup["R3"]["floor_z_cm"]),
        },
        "combat_axis": {
            "axis": "X",
            "min_cm": -half_combat,
            "max_cm": half_combat,
        },
        "ceiling_cm": rng.choice(CEILING_CHOICES_CM),
        # Declared on the plan so the validator, refiner and materializer all
        # measure clearance against the same footprint. Graybox values -- see
        # the `materializer` block in contracts/arena_rules.json.
        "obstacle_extents": {
            "depth_cm": half_depth * 2.0,
            "width_cm": half_width * 2.0,
            "height_cm": float(extents.get("obstacle_height_cm", 0.0)),
            "status": extents.get("status", "PROPOSED"),
        },
        "camera": {
            # Resolution U2: the shell is shallower than the camera pull-back,
            # so the near wall is culled rather than the arena being widened.
            "near_wall_culled": True,
        },
        "spawns": {
            "player": {"x_cm": player_x, "y_cm": 0.0, "z_cm": 94.0, "yaw_deg": 0.0},
            "opponent": {"x_cm": opponent_x, "y_cm": 0.0, "z_cm": 90.0, "yaw_deg": 180.0},
        },
        "obstacles": obstacles,
        "boundaries": [
            {"name": "Wall_DoorwayEnd", "axis": "x", "x_cm": half_long},
            {"name": "Wall_TrussEnd", "axis": "x", "x_cm": -half_long},
            # Side railings run parallel to the combat axis, so they cross x = 0
            # legitimately -- see R8's axis semantics.
            {"name": "Railing_North", "axis": "y", "x_cm": 0.0, "y_cm": short_axis / 2.0},
            {"name": "Railing_South", "axis": "y", "x_cm": 0.0, "y_cm": -short_axis / 2.0},
        ],
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Generate an Ascendant Impact arena plan.")
    parser.add_argument("--seed", type=int, default=1, help="deterministic seed")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--out", help="write the plan here instead of stdout")
    args = parser.parse_args(argv)

    try:
        rules_doc = load_json(args.rules, "arena rules")
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    plan = generate(rules_doc, args.seed)
    text = json.dumps(plan, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print("wrote %s" % args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
