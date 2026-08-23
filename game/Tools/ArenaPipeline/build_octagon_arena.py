"""
Octagonal arena blockout payload for the Unreal MCP ProgrammaticToolset.

THIS IS A PAYLOAD, NOT A STANDALONE PROGRAM.
Running it with `python build_octagon_arena.py` fails with
NameError: name 'execute_tool' is not defined. That is expected and correct --
execute_tool is injected by the toolset sandbox inside the running editor.
Send the file contents as the `script` argument to
editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script.

Change any number in the PARAMETERS block and re-send to regenerate.
Everything below the PARAMETERS block is derived; no dimension is hardcoded
further down.
"""

import json
import math

# =============================================================================
# PARAMETERS -- the only numbers you should need to edit
# =============================================================================

# --- The anchor everything else is measured from -----------------------------
CHARACTER_HEIGHT_CM = 208.0

# --- Fighter clamp and clearance (drive the minimum footprint) ---------------
COMBAT_SPAN_CM = 1300.0           # total legal separation; +/- half of this
FIGHTER_CLEARANCE_CM = 500.0      # required gap: fighter -> blocking geometry

# --- Footprint --------------------------------------------------------------
CENTRE_TO_FACE_MIN_CM = 1150.0    # hard floor (= span/2 + clearance)
CENTRE_TO_FACE_USE_CM = 1200.0    # what to actually use, for margin
PANEL_WIDTH_CM = 1000.0           # width of each of the eight wall panels
PANEL_OVERLAP_CM = 50.0           # extra panel width so corners overlap, no gaps
FOOTPRINT_SQUARE_MIN_CM = 2300.0  # minimum bounding square, per side

# --- Vertical ---------------------------------------------------------------
JUMP_APEX_CM = 180.0
CEILING_CLEARANCE_MIN_CM = 388.0  # = CHARACTER_HEIGHT_CM + JUMP_APEX_CM
WALL_HEIGHT_CM = 1200.0           # derived from Ref-Arena 1.jpg at 5.79 CH
GALLERY_UNDERSIDE_CM = 550.0      # derived from Ref-Arena 1.jpg at 2.64 CH
GALLERY_OVERHANG_CM = 450.0       # how far the gallery projects inward
GALLERY_SLAB_CM = 60.0

# --- Camera containment -----------------------------------------------------
# The duel rig is runtime-spawned, so there is no instance in the level to read.
# These are read live from the Blueprint class defaults at run time; the values
# here are only the fallback if that read fails.
CONTAIN_CAMERA = True             # False = let the near wall be culled instead
CAMERA_RIG_CDO = "/Game/AscendantImpact/Camera/BP_DuelCameraRig.Default__BP_DuelCameraRig_C"
CAMERA_WALL_MARGIN_CM = 100.0     # gap between worst-case camera and wall face
FALLBACK_BASE_CAMERA_DISTANCE_CM = 450.0
FALLBACK_DISTANCE_PER_SEPARATION = 0.8
FALLBACK_MAX_CAMERA_DISTANCE_CM = 1500.0
FALLBACK_MIN_CAMERA_DISTANCE_CM = 500.0
FALLBACK_SIDE_ANGLE_DEG = 12.0

# --- Build behaviour --------------------------------------------------------
PLACE_FLOOR = False               # False = reuse the level's existing floor
PLACE_WALLS = True
PLACE_GALLERY = True
FLOOR_THICKNESS_CM = 20.0
WALL_THICKNESS_CM = 40.0
ACTOR_PREFIX = "ArenaOct_"
OUTLINER_FOLDER = "ArenaOctagon"
UNIT_CUBE_ASSET = "/Engine/BasicShapes/Cube"
UNIT_CUBE_SIZE_CM = 100.0

# --- Centring ---------------------------------------------------------------
# Rule: read the level, never blindly assume world origin. The spawns are ALWAYS
# read and reported regardless of mode, so the chosen centre can be checked
# against them.
#   "combat_axis"    -- centre on the fighter clamp centre (COMBAT_AXIS_CENTRE).
#                       The spawns mark where the fight STARTS; the clamp is
#                       where it RANGES. For a symmetric shape this is the one
#                       that reads as centred in play.
#   "spawn_midpoint" -- centre on the midpoint of the two spawns.
#   "override"       -- use CENTRE_OVERRIDE verbatim.
CENTRE_MODE = "combat_axis"
COMBAT_AXIS_CENTRE = {"x": 0.0, "y": 0.0}
PLAYER_START_CLASS = "/Script/Engine.PlayerStart"
OPPONENT_CLASS = "/Game/Variant_Combat/Blueprints/BP_VanguardProxy.BP_VanguardProxy_C"
CENTRE_OVERRIDE = None
FLOOR_TRACE_UP_CM = 500.0
FLOOR_TRACE_DOWN_CM = 500.0

# --- Safety -----------------------------------------------------------------
# Levels owned by Anthony. The build refuses to touch these; duplicate to a new
# level first and build there. Matched on LEVEL NAME, not full path, so a copy
# of a protected level parked at some other path is still caught.
PROTECTED_LEVEL_NAMES = [
    "Lvl_ThirdPerson",
    "Lvl_DuelGraybox",
]
DRY_RUN = False                   # True = compute and report, place nothing

# =============================================================================
# END PARAMETERS
# =============================================================================


def _call(tool, payload):
    return execute_tool(tool, json.dumps(payload))


def get_current_level():
    return _call("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]


def find_actors_of_class(class_path):
    return _call(
        "editor_toolset.toolsets.scene.SceneTools.find_actors",
        {"name": "", "tag": "", "collision_channels": [],
         "actor_type": {"refPath": class_path}},
    )["returnValue"]


def get_actor_transform(actor):
    return _call(
        "editor_toolset.toolsets.actor.ActorTools.get_actor_transform",
        {"actor": actor},
    )["returnValue"]


def get_properties(ref_path, names):
    raw = _call(
        "editor_toolset.toolsets.object.ObjectTools.get_properties",
        {"instance": {"refPath": ref_path}, "properties": names},
    )["returnValue"]
    return json.loads(raw)


def trace_world(start, end):
    return _call(
        "editor_toolset.toolsets.scene.SceneTools.trace_world",
        {"start": start, "end": end},
    ).get("returnValue")


def spawn_cube(name, loc, yaw, scale_cm):
    xform = {
        "location": {"x": loc[0], "y": loc[1], "z": loc[2]},
        "rotation": {"pitch": 0.0, "yaw": yaw, "roll": 0.0},
        "scale": {
            "x": scale_cm[0] / UNIT_CUBE_SIZE_CM,
            "y": scale_cm[1] / UNIT_CUBE_SIZE_CM,
            "z": scale_cm[2] / UNIT_CUBE_SIZE_CM,
        },
    }
    return _call(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
        {"asset_path": UNIT_CUBE_ASSET, "name": name, "xform": xform,
         "snap_to_ground": False},
    )["returnValue"]


def set_folder(actor, folder):
    return _call(
        "editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
        {"actor": actor, "folder_path": folder},
    )


def save_all():
    return _call(
        "editor_toolset.toolsets.asset.AssetTools.save_assets",
        {"asset_paths": []},
    )["returnValue"]


# --- Derivation --------------------------------------------------------------

def read_camera_rig():
    """Read the runtime-spawned rig's class defaults. Falls back on failure."""
    names = ["baseCameraDistance", "distancePerSeparation",
             "minCameraDistance", "maxCameraDistance", "sideAngleDegrees"]
    try:
        v = get_properties(CAMERA_RIG_CDO, names)
        return {
            "base": float(v["baseCameraDistance"]),
            "per_sep": float(v["distancePerSeparation"]),
            "min_d": float(v["minCameraDistance"]),
            "max_d": float(v["maxCameraDistance"]),
            "side_deg": float(v["sideAngleDegrees"]),
            "source": "class defaults (live read)",
        }
    except Exception as exc:
        return {
            "base": FALLBACK_BASE_CAMERA_DISTANCE_CM,
            "per_sep": FALLBACK_DISTANCE_PER_SEPARATION,
            "min_d": FALLBACK_MIN_CAMERA_DISTANCE_CM,
            "max_d": FALLBACK_MAX_CAMERA_DISTANCE_CM,
            "side_deg": FALLBACK_SIDE_ANGLE_DEG,
            "source": "PARAMETER fallback (live read failed: %s)" % exc,
        }


def worst_case_camera_radius(rig):
    """Furthest the camera ever gets from arena centre.

    Fighters are clamped to +/- COMBAT_SPAN_CM/2. For a separation s the rig
    sits at distance d = clamp(base + per_sep*s, min, max) from the fighter
    midpoint, offset by side_deg from the arena-perpendicular. The midpoint can
    itself slide to at most (half_span - s/2) off centre. Sweep s and keep the
    largest resulting radius.
    """
    half_span = COMBAT_SPAN_CM / 2.0
    ang = math.radians(rig["side_deg"])
    worst = {"radius": 0.0, "separation": 0.0, "distance": 0.0}
    steps = 261
    for i in range(steps):
        s = COMBAT_SPAN_CM * i / (steps - 1)
        d = min(max(rig["base"] + rig["per_sep"] * s, rig["min_d"]), rig["max_d"])
        midpoint_max = max(half_span - s / 2.0, 0.0)
        along = midpoint_max + d * math.sin(ang)
        perp = d * math.cos(ang)
        r = math.hypot(along, perp)
        if r > worst["radius"]:
            worst = {"radius": r, "separation": s, "distance": d,
                     "along": along, "perp": perp}
    return worst


def derive():
    rig = read_camera_rig()
    cam = worst_case_camera_radius(rig)

    spec_apothem = max(CENTRE_TO_FACE_USE_CM, CENTRE_TO_FACE_MIN_CM,
                       FOOTPRINT_SQUARE_MIN_CM / 2.0)
    camera_apothem = cam["radius"] + CAMERA_WALL_MARGIN_CM if CONTAIN_CAMERA else 0.0
    apothem = max(spec_apothem, camera_apothem)
    grown = apothem > spec_apothem + 1e-6

    min_panel = 2.0 * apothem * math.tan(math.pi / 8.0)
    panel = max(PANEL_WIDTH_CM, min_panel + PANEL_OVERLAP_CM)

    ceiling_ok = WALL_HEIGHT_CM >= CEILING_CLEARANCE_MIN_CM
    gallery_ok = GALLERY_UNDERSIDE_CM >= CEILING_CLEARANCE_MIN_CM
    gallery_inner = apothem - GALLERY_OVERHANG_CM
    gallery_to_fighter = gallery_inner - COMBAT_SPAN_CM / 2.0

    return {
        "rig": rig,
        "camera": cam,
        "apothem_cm": apothem,
        "apothem_from_spec_cm": spec_apothem,
        "apothem_from_camera_cm": camera_apothem,
        "grown_for_camera": grown,
        "flat_to_flat_cm": apothem * 2.0,
        "circumradius_cm": apothem / math.cos(math.pi / 8.0),
        "panel_width_cm": panel,
        "panel_width_min_cm": min_panel,
        "bounding_square_cm": apothem * 2.0,
        "floor_area_m2": (4.0 * apothem * min_panel) / 10000.0,
        "ceiling_clearance_ok": ceiling_ok,
        "gallery_clearance_ok": gallery_ok,
        "gallery_inner_edge_cm": gallery_inner,
        "gallery_to_fighter_bound_cm": gallery_to_fighter,
    }


def find_centre():
    """Resolve the build centre. Spawns are always read, never assumed."""
    starts = find_actors_of_class(PLAYER_START_CLASS)
    opponents = find_actors_of_class(OPPONENT_CLASS)
    if not starts or not opponents:
        raise RuntimeError(
            "Could not find spawns: %d PlayerStart, %d opponent. "
            "Refusing to fall back to world origin."
            % (len(starts), len(opponents))
        )

    a = get_actor_transform(starts[0])["location"]
    b = get_actor_transform(opponents[0])["location"]
    spawn_mid = {"x": (a["x"] + b["x"]) / 2.0, "y": (a["y"] + b["y"]) / 2.0}

    if CENTRE_MODE == "override":
        if CENTRE_OVERRIDE is None:
            raise RuntimeError("CENTRE_MODE is 'override' but CENTRE_OVERRIDE is None.")
        cx, cy = CENTRE_OVERRIDE["x"], CENTRE_OVERRIDE["y"]
        why = "CENTRE_OVERRIDE parameter"
    elif CENTRE_MODE == "spawn_midpoint":
        cx, cy = spawn_mid["x"], spawn_mid["y"]
        why = "midpoint of the two spawns"
    elif CENTRE_MODE == "combat_axis":
        cx, cy = COMBAT_AXIS_CENTRE["x"], COMBAT_AXIS_CENTRE["y"]
        why = "fighter clamp centre (spawn midpoint read as %.1f, %.1f)" % (
            spawn_mid["x"], spawn_mid["y"])
    else:
        raise RuntimeError("Unknown CENTRE_MODE %r" % CENTRE_MODE)

    # Floor Z by trace, not by assuming the spawn Z is ground level.
    top = {"x": cx, "y": cy, "z": max(a["z"], b["z"]) + FLOOR_TRACE_UP_CM}
    bottom = {"x": cx, "y": cy, "z": min(a["z"], b["z"]) - FLOOR_TRACE_DOWN_CM}
    hit = trace_world(top, bottom)
    if hit is None:
        raise RuntimeError(
            "Floor trace found nothing under (%.1f, %.1f). Refusing to guess "
            "the floor height." % (cx, cy)
        )
    cz = top["z"] - hit

    return ({"x": cx, "y": cy, "z": cz},
            "%s; spawns read at %s and %s; floor Z %.1f by trace"
            % (why, (a["x"], a["y"], a["z"]), (b["x"], b["y"], b["z"]), cz))


def build_geometry(d, centre):
    placed = []
    cx, cy, cz = centre["x"], centre["y"], centre["z"]
    apothem = d["apothem_cm"]
    panel = d["panel_width_cm"]

    if PLACE_FLOOR:
        side = d["flat_to_flat_cm"]
        a = spawn_cube(ACTOR_PREFIX + "Floor",
                       (cx, cy, cz - FLOOR_THICKNESS_CM / 2.0),
                       0.0, (side, side, FLOOR_THICKNESS_CM))
        set_folder(a, OUTLINER_FOLDER)
        placed.append(a)

    if PLACE_WALLS:
        for i in range(8):
            theta = math.radians(i * 45.0)
            a = spawn_cube(
                ACTOR_PREFIX + "Wall_%d" % i,
                (cx + apothem * math.cos(theta),
                 cy + apothem * math.sin(theta),
                 cz + WALL_HEIGHT_CM / 2.0),
                i * 45.0,
                (WALL_THICKNESS_CM, panel, WALL_HEIGHT_CM),
            )
            set_folder(a, OUTLINER_FOLDER)
            placed.append(a)

    if PLACE_GALLERY:
        radius = apothem - GALLERY_OVERHANG_CM / 2.0
        for i in range(8):
            theta = math.radians(i * 45.0)
            a = spawn_cube(
                ACTOR_PREFIX + "Gallery_%d" % i,
                (cx + radius * math.cos(theta),
                 cy + radius * math.sin(theta),
                 cz + GALLERY_UNDERSIDE_CM + GALLERY_SLAB_CM / 2.0),
                i * 45.0,
                (GALLERY_OVERHANG_CM, panel, GALLERY_SLAB_CM),
            )
            set_folder(a, OUTLINER_FOLDER)
            placed.append(a)

    return placed


def _build():
    level = get_current_level()
    d = derive()

    report = {
        "level": level,
        "character_height_cm": CHARACTER_HEIGHT_CM,
        "camera_rig_source": d["rig"]["source"],
        "camera_rig_values": {k: d["rig"][k] for k in
                              ("base", "per_sep", "min_d", "max_d", "side_deg")},
        "camera_worst_case": {
            "at_separation_cm": round(d["camera"]["separation"], 1),
            "rig_distance_cm": round(d["camera"]["distance"], 1),
            "radius_from_centre_cm": round(d["camera"]["radius"], 1),
        },
        "sizing": {
            "centre_to_face_cm": round(d["apothem_cm"], 1),
            "from_spec_cm": round(d["apothem_from_spec_cm"], 1),
            "from_camera_cm": round(d["apothem_from_camera_cm"], 1),
            "grown_for_camera": d["grown_for_camera"],
            "flat_to_flat_cm": round(d["flat_to_flat_cm"], 1),
            "centre_to_corner_cm": round(d["circumradius_cm"], 1),
            "panel_width_cm": round(d["panel_width_cm"], 1),
            "panel_width_min_cm": round(d["panel_width_min_cm"], 1),
            "bounding_square_cm": round(d["bounding_square_cm"], 1),
            "floor_area_m2": round(d["floor_area_m2"], 1),
        },
        "checks": {
            "ceiling_clearance_ok": d["ceiling_clearance_ok"],
            "gallery_underside_clears_jump": d["gallery_clearance_ok"],
            "gallery_inner_edge_cm": round(d["gallery_inner_edge_cm"], 1),
            "gallery_to_fighter_bound_cm": round(d["gallery_to_fighter_bound_cm"], 1),
        },
        "placed": 0,
        "actors": [],
    }

    level_name = level.rsplit("/", 1)[-1]
    if level_name in PROTECTED_LEVEL_NAMES:
        report["status"] = "REFUSED"
        report["reason"] = (
            "'%s' matches protected level name '%s'. Duplicate it to a level of "
            "your own and build there, or clear the name from "
            "PROTECTED_LEVEL_NAMES if you own it." % (level, level_name)
        )
        return report

    if DRY_RUN:
        report["status"] = "DRY_RUN"
        return report

    centre, centre_src = find_centre()
    report["centre"] = {k: round(v, 2) for k, v in centre.items()}
    report["centre_source"] = centre_src

    actors = build_geometry(d, centre)
    report["placed"] = len(actors)
    report["actors"] = [a["refPath"].split(".")[-1] for a in actors]
    # Empty list = save all dirty. A map-path-only save does not flush OFPA
    # actor additions to disk.
    report["saved"] = save_all()
    report["status"] = "BUILT"
    return report


# Project rule: these payloads define run() and it is never called for us, which
# produces a clean exit that builds nothing and reads as success. So the work is
# driven from module scope here, and run() just hands back the cached result --
# that way a second invocation by the host cannot double-place the geometry.
_RESULT = _build()


def run():
    return _RESULT
