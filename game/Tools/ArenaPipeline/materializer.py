"""Materializer stage -- turns a validated arena plan into a build manifest.

The plan the generator emits is *dimensionless*: obstacles and boundaries are
points (`x_cm`, `y_cm`), and the deterministic gate checks those points. Real
geometry has extent, so the moment a plan becomes actors in a level it acquires
faces the gate never saw. An obstacle whose centre clears the combat bound by
507 cm has a near face that does not.

This stage exists to close that hole. It:

    1. re-runs the deterministic gate, and refuses to build an invalid plan;
    2. resolves each plan element into a world-space box (a *placement*);
    3. re-checks R2, R3 and R8 against the resulting FACES rather than centres;
    4. emits a build manifest, plus the MCP script that realises it.

It writes no Unreal asset itself and imports no Unreal module -- it is a pure
CLI like the rest of the pipeline, so it stays testable without an editor. The
manifest is the reviewable artifact; the script is what gets handed to the
unreal-mcp ProgrammaticToolset against a live editor session.

Extents are NOT design decisions. They are graybox visual placeholders carried
in contracts/arena_rules.json under `materializer` with status PROPOSED, and
this stage refuses to use them without --allow-proposed, exactly as the
validator refuses to enforce a PROPOSED requirement.

Exit codes:
    0  manifest built; realised geometry passes every re-checked rule
    1  realised geometry violates a rule the dimensionless plan passed
    2  human review required (invalid plan, or PROPOSED extents without waiver)
    3  bad usage / unreadable input
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_arena_plan import (  # noqa: E402
    BINDING_STATUSES, DEFAULT_RULES, Violation, load_json, rules_by_id, validate,
)

MANIFEST_VERSION = "1.0.0"

# Roles a placement can have. Only BLOCKING_ROLES are re-checked against the
# combat volume -- a spawn marker has no collision and a floor is meant to be
# underfoot.
ROLE_FLOOR = "floor"
ROLE_CEILING = "ceiling"
ROLE_WALL = "wall"
ROLE_RAILING = "railing"
ROLE_OBSTACLE = "obstacle"
ROLE_SPAWN = "spawn"

BLOCKING_ROLES = (ROLE_WALL, ROLE_RAILING, ROLE_OBSTACLE)


class Placement:
    """One actor to be created, as a world-space axis-aligned box.

    `size_cm` is the full extent, not the half-extent. Rotation is carried for
    the spawn markers only; every graybox box is axis-aligned, which is what
    lets the face checks stay a plain interval comparison.
    """

    def __init__(self, name, role, center, size, source_asset=None,
                 source_class=None, yaw_deg=0.0, folder="", visual_only=False):
        self.name = name
        self.role = role
        self.center = center           # (x, y, z)
        self.size = size               # (sx, sy, sz)
        self.source_asset = source_asset
        self.source_class = source_class
        self.yaw_deg = yaw_deg
        self.folder = folder
        self.visual_only = visual_only

    def min_x(self):
        return self.center[0] - self.size[0] / 2.0

    def max_x(self):
        return self.center[0] + self.size[0] / 2.0

    def min_z(self):
        return self.center[2] - self.size[2] / 2.0

    def max_z(self):
        return self.center[2] + self.size[2] / 2.0

    def as_dict(self, unit_cube_size):
        entry = {
            "name": self.name,
            "role": self.role,
            "location": {"x": round(self.center[0], 2),
                         "y": round(self.center[1], 2),
                         "z": round(self.center[2], 2)},
            "rotation": {"pitch": 0.0, "yaw": round(self.yaw_deg, 2), "roll": 0.0},
            "folder": self.folder,
            "visual_only": self.visual_only,
        }
        if self.source_asset is not None:
            entry["asset_path"] = self.source_asset
            entry["size_cm"] = {"x": round(self.size[0], 2),
                                "y": round(self.size[1], 2),
                                "z": round(self.size[2], 2)}
            entry["scale"] = {"x": round(self.size[0] / unit_cube_size, 6),
                              "y": round(self.size[1] / unit_cube_size, 6),
                              "z": round(self.size[2] / unit_cube_size, 6)}
        if self.source_class is not None:
            entry["class_path"] = self.source_class
        return entry


def materializer_settings(rules_doc, allow_proposed=False):
    """Fetch the graybox extents block, honouring its approval status.

    Returns (settings, review_notes). `settings` is None when the block may not
    be used, which the caller must treat as human review, not as a failure.
    """
    review = []
    settings = rules_doc.get("materializer")
    if settings is None:
        review.append("contracts/arena_rules.json has no `materializer` block; "
                      "graybox extents are unstated and cannot be guessed")
        return None, review

    status = settings.get("status")
    if status not in BINDING_STATUSES:
        if not allow_proposed:
            review.append("materializer extents have status %s and cannot be built "
                          "without approval (pass --allow-proposed to build a "
                          "graybox anyway)" % status)
            return None, review
        review.append("materializer extents used from a %s value under "
                      "--allow-proposed; every placed actor is graybox-only and "
                      "carries no design authority" % status)
    return settings, review


def build_placements(plan, settings):
    """Resolve the dimensionless plan into world-space boxes."""
    placements = []

    long_axis = float(plan["floor"]["long_axis_cm"])
    short_axis = float(plan["floor"]["short_axis_cm"])
    floor_z = float(plan["floor"]["z_cm"])
    ceiling_z = float(plan["ceiling_cm"])

    floor_t = float(settings["floor_thickness_cm"])
    wall_t = float(settings["wall_thickness_cm"])
    rail_t = float(settings["railing_thickness_cm"])
    rail_h = float(settings["railing_height_cm"])
    # The plan's own declared footprint wins: it is what the gate measured
    # clearance against, so building to anything else would place geometry the
    # validator never saw. The contract is the fallback for older plans.
    declared = plan.get("obstacle_extents", {})
    obs_d = float(declared.get("depth_cm", settings["obstacle_depth_cm"]))
    obs_w = float(declared.get("width_cm", settings["obstacle_width_cm"]))
    obs_h = float(declared.get("height_cm", settings["obstacle_height_cm"]))
    cube = settings["unit_cube_asset"]

    # Floor: the plan states the top surface, so the slab hangs below it.
    placements.append(Placement(
        "Arena_Floor", ROLE_FLOOR,
        (0.0, 0.0, floor_z - floor_t / 2.0),
        (long_axis, short_axis, floor_t),
        source_asset=cube, folder="ArenaGen/Shell"))

    # Ceiling: R7 is a real rule, so the headroom limit is built, not implied.
    placements.append(Placement(
        "Arena_Ceiling", ROLE_CEILING,
        (0.0, 0.0, ceiling_z + floor_t / 2.0),
        (long_axis, short_axis, floor_t),
        source_asset=cube, folder="ArenaGen/Shell"))

    # Boundaries. A boundary's stated coordinate is the plane its INNER face
    # sits on, so each slab is pushed outward by half its thickness -- building
    # it centred would put half the wall inside the room.
    for boundary in plan.get("boundaries", []):
        name = boundary.get("name", "Boundary")
        axis = boundary.get("axis", "x").lower()
        if axis == "x":
            plane = float(boundary["x_cm"])
            sign = 1.0 if plane >= 0 else -1.0
            placements.append(Placement(
                name, ROLE_WALL,
                (plane + sign * wall_t / 2.0, 0.0, floor_z + ceiling_z / 2.0),
                (wall_t, short_axis, ceiling_z),
                source_asset=cube, folder="ArenaGen/Shell"))
        else:
            plane = float(boundary["y_cm"])
            sign = 1.0 if plane >= 0 else -1.0
            placements.append(Placement(
                name, ROLE_RAILING,
                (0.0, plane + sign * rail_t / 2.0, floor_z + rail_h / 2.0),
                (long_axis, rail_t, rail_h),
                source_asset=cube, folder="ArenaGen/Shell"))

    # Obstacles. The plan gives a centre only; the graybox box is centred on it.
    for obstacle in plan.get("obstacles", []):
        placements.append(Placement(
            obstacle.get("name", "Obstacle"), ROLE_OBSTACLE,
            (float(obstacle["x_cm"]), float(obstacle["y_cm"]), floor_z + obs_h / 2.0),
            (obs_d, obs_w, obs_h),
            source_asset=cube, folder="ArenaGen/Landmarks",
            visual_only=not obstacle.get("blocking", True)))

    # Spawns. Non-colliding markers -- these are placement metadata, not shell.
    spawns = plan.get("spawns", {})
    for label, class_path in (("player", settings["player_start_class"]),
                              ("opponent", settings["opponent_marker_class"])):
        spawn = spawns.get(label)
        if spawn is None:
            continue
        placements.append(Placement(
            "Spawn_%s" % label.capitalize(), ROLE_SPAWN,
            (float(spawn["x_cm"]), float(spawn["y_cm"]), float(spawn["z_cm"])),
            (0.0, 0.0, 0.0),
            source_class=class_path, yaw_deg=float(spawn["yaw_deg"]),
            folder="ArenaGen/Spawns", visual_only=True))

    return placements


def recheck_realised(placements, plan, rules_doc):
    """Re-run the extent-sensitive rules against realised faces.

    R1, R4, R5, R6 and R7 are unaffected by extent -- they constrain spans,
    camera maths and spawn points, none of which gain faces here. R2, R3 and R8
    all compare geometry to the combat bounds, and all three were checked
    against centres.
    """
    out = []
    lookup = rules_by_id(rules_doc)
    axis_min = float(plan["combat_axis"]["min_cm"])
    axis_max = float(plan["combat_axis"]["max_cm"])
    margin = float(lookup["R2"]["min_clearance_beyond_bound_cm"])

    for placement in placements:
        if placement.role not in BLOCKING_ROLES or placement.visual_only:
            continue

        near = placement.min_x()
        far = placement.max_x()

        # A railing runs parallel to the combat axis and legitimately spans it,
        # exactly as R8's axis semantics allow for the dimensionless case.
        if placement.role == ROLE_RAILING:
            continue

        # R3 / R8: does any face reach into the fighting space?
        if near <= axis_max and far >= axis_min:
            rule_id = "R8" if placement.role == ROLE_WALL else "R3"
            out.append(Violation(
                rule_id,
                "realised geometry '%s' overlaps the combat volume once given "
                "extent" % placement.name,
                "outside [%.1f, %.1f]" % (axis_min, axis_max),
                "spans [%.1f, %.1f]" % (near, far)))
            continue

        # R2: clearance is measured to the nearest face, not the centre.
        if placement.role == ROLE_OBSTACLE:
            gap = axis_min - far if far < axis_min else near - axis_max
            if gap < margin:
                out.append(Violation(
                    "R2",
                    "realised obstacle '%s' crowds the combat bound once given "
                    "extent (centre clears, near face does not)" % placement.name,
                    ">= %.1f cm clearance" % margin,
                    "%.1f cm" % gap))

    return out


def interpenetrations(placements):
    """Boxes that share volume. A warning, not a violation -- a landmark set
    flush into its end wall is legitimate graybox, but silent overlap is not."""
    notes = []
    boxes = [p for p in placements if p.role in
             (ROLE_WALL, ROLE_RAILING, ROLE_OBSTACLE)]
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            overlap = []
            for axis in range(3):
                a_min = a.center[axis] - a.size[axis] / 2.0
                a_max = a.center[axis] + a.size[axis] / 2.0
                b_min = b.center[axis] - b.size[axis] / 2.0
                b_max = b.center[axis] + b.size[axis] / 2.0
                overlap.append(min(a_max, b_max) - max(a_min, b_min))
            if all(o > 0.0 for o in overlap):
                notes.append("'%s' and '%s' interpenetrate by %.1f x %.1f x %.1f cm"
                             % (a.name, b.name, overlap[0], overlap[1], overlap[2]))
    return notes


def build_manifest(plan, rules_doc, allow_proposed=False):
    """Full stage. Returns a manifest dict; never touches Unreal."""
    review = []
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "plan_id": plan.get("plan_id"),
        "seed": plan.get("seed"),
        "rules_version": rules_doc.get("rules_version"),
        "generated_by": "Tools/ArenaPipeline/materializer.py",
        "level_path": None,
        "placements": [],
        "realised_violations": [],
        "interpenetrations": [],
        "human_review": review,
    }

    # Refuse to build a plan that never passed the dimensionless gate.
    violations, plan_review, decisions = validate(plan, rules_doc,
                                                  allow_proposed=allow_proposed)
    manifest["decisions_pending_confirmation"] = decisions
    if violations:
        review.append("plan fails the deterministic gate and will not be built: %s"
                      % "; ".join(str(v) for v in violations))
        return manifest
    review.extend(plan_review)

    settings, extent_review = materializer_settings(rules_doc, allow_proposed)
    review.extend(extent_review)
    if settings is None:
        return manifest

    placements = build_placements(plan, settings)
    realised = recheck_realised(placements, plan, rules_doc)

    manifest["placements"] = [p.as_dict(float(settings["unit_cube_size_cm"]))
                              for p in placements]
    manifest["realised_violations"] = [v.as_dict() for v in realised]
    manifest["interpenetrations"] = interpenetrations(placements)
    manifest["extents_source"] = settings.get("source")
    manifest["extents_status"] = settings.get("status")
    return manifest


def render_mcp_script(manifest, level_path):
    """Emit the ProgrammaticToolset script that realises the manifest.

    Generated rather than hand-written so the level can only ever contain what
    the manifest says it contains.
    """
    payload = json.dumps(manifest["placements"], indent=2)
    return '''import json

PLACEMENTS = json.loads(r"""%s""")

LEVEL_PATH = "%s"


def add_from_asset(asset_path, name, xform):
    return execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
        json.dumps({"asset_path": asset_path, "name": name, "xform": xform}))["returnValue"]


def add_from_class(class_path, name, xform):
    return execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class",
        json.dumps({"actor_type": {"refPath": class_path}, "name": name,
                    "xform": xform}))["returnValue"]


def set_folder(actor, folder_path):
    execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
        json.dumps({"actor": actor, "folder_path": folder_path}))


def run():
    created = []
    failed = []
    for entry in PLACEMENTS:
        xform = {"location": entry["location"], "rotation": entry["rotation"]}
        if "scale" in entry:
            xform["scale"] = entry["scale"]
        try:
            if "asset_path" in entry:
                actor = add_from_asset(entry["asset_path"], entry["name"], xform)
            else:
                actor = add_from_class(entry["class_path"], entry["name"], xform)
            if entry.get("folder"):
                set_folder(actor, entry["folder"])
            created.append(entry["name"])
        except RuntimeError as exc:
            failed.append({"name": entry["name"], "error": str(exc)})
    execute_tool("editor_toolset.toolsets.asset.AssetTools.save_assets",
                 json.dumps({"asset_paths": []}))
    return {"level": LEVEL_PATH, "created": created, "failed": failed,
            "count": len(created)}
''' % (payload, level_path)


def render_markdown(manifest):
    out = []
    out.append("# Arena build manifest `%s`" % manifest.get("plan_id"))
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Seed | `%s` |" % manifest.get("seed"))
    out.append("| Rules | v%s |" % manifest.get("rules_version"))
    out.append("| Extents status | %s |" % manifest.get("extents_status"))
    out.append("| Placements | %d |" % len(manifest["placements"]))
    out.append("| Realised violations | %d |" % len(manifest["realised_violations"]))
    out.append("")

    if manifest["human_review"]:
        out.append("**Human review / waivers:**")
        out.append("")
        for note in manifest["human_review"]:
            out.append("- %s" % note)
        out.append("")

    if manifest["realised_violations"]:
        out.append("## Realised-geometry violations")
        out.append("")
        out.append("These rules passed against the dimensionless plan and fail once "
                   "the geometry has extent.")
        out.append("")
        for violation in manifest["realised_violations"]:
            out.append("- `%s` %s (expected %s, got %s)" % (
                violation["rule_id"], violation["message"],
                violation["expected"], violation["actual"]))
        out.append("")

    if manifest["interpenetrations"]:
        out.append("## Interpenetration warnings")
        out.append("")
        for note in manifest["interpenetrations"]:
            out.append("- %s" % note)
        out.append("")

    if manifest["placements"]:
        out.append("## Placements")
        out.append("")
        out.append("| Actor | Role | Location (cm) | Size (cm) |")
        out.append("|---|---|---|---|")
        for entry in manifest["placements"]:
            location = "%.0f, %.0f, %.0f" % (entry["location"]["x"],
                                             entry["location"]["y"],
                                             entry["location"]["z"])
            if "size_cm" in entry:
                size = "%.0f x %.0f x %.0f" % (entry["size_cm"]["x"],
                                               entry["size_cm"]["y"],
                                               entry["size_cm"]["z"])
            else:
                size = "marker"
            out.append("| `%s` | %s | %s | %s |" % (
                entry["name"], entry["role"], location, size))
        out.append("")
    return "\n".join(out) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(
        description="Turn a validated arena plan into an Unreal build manifest.")
    parser.add_argument("plan", help="path to the arena plan JSON")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--allow-proposed", action="store_true",
                        help="build using PROPOSED graybox extents")
    parser.add_argument("--level-path",
                        default="/Game/AscendantImpact/Maps/Lvl_ArenaGen",
                        help="content path of the level the script will target")
    parser.add_argument("--out-dir", help="write manifest.json, manifest.md and "
                                          "build_level.py here")
    parser.add_argument("--json", action="store_true",
                        help="print the manifest as JSON instead of Markdown")
    args = parser.parse_args(argv)

    try:
        plan = load_json(args.plan, "arena plan")
        rules_doc = load_json(args.rules, "arena rules")
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    manifest = build_manifest(plan, rules_doc, allow_proposed=args.allow_proposed)
    manifest["level_path"] = args.level_path

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(render_markdown(manifest))

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        with open(os.path.join(args.out_dir, "manifest.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2)
        with open(os.path.join(args.out_dir, "manifest.md"), "w",
                  encoding="utf-8") as handle:
            handle.write(render_markdown(manifest))
        if manifest["placements"] and not manifest["realised_violations"]:
            with open(os.path.join(args.out_dir, "build_level.py"), "w",
                      encoding="utf-8") as handle:
                handle.write(render_mcp_script(manifest, args.level_path))
        print("manifest written to %s" % args.out_dir)

    if manifest["realised_violations"]:
        return 1
    if not manifest["placements"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
