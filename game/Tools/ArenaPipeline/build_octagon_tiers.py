"""
Two-tier gallery + diagonal wedge pass. Payload for the Unreal MCP
ProgrammaticToolset -- running it with plain `python` raises NameError on
execute_tool, which is expected.

Layers on top of build_octagon_arena.py + build_octagon_detail.py.

From ref 4.png / section.png:
  - The gallery runs at TWO levels, not one.
  - The link between them is a SOLID SLANTED SLAB of constant thickness with a
    diagonal soffit -- a stair stringer -- not a run of blocky steps.
  - The slab lands low at the truss wall and rises to the upper tier.

Facets 1, 3, 5, 7 (diagonals) carry the ramps. Facets 2 and 6 (+/-Y) gain the
upper tier for the ramps to land on. Facets 0 and 4 stay truss walls.
"""

import json
import math

# =============================================================================
# PARAMETERS
# =============================================================================

APOTHEM_CM = 1590.0
PANEL_WIDTH_CM = 1367.2
WALL_THICKNESS_CM = 40.0
GALLERY_OVERHANG_CM = 450.0
GALLERY_SLAB_CM = 60.0

TRUSS_FACETS = [0, 4]
RAMP_FACETS = [1, 3, 5, 7]        # diagonals: get the slanted wedge
UPPER_TIER_FACETS = [2, 6]        # +/-Y: gain a second gallery level

# --- Lower tier (already built) ----------------------------------------------
LOWER_UNDERSIDE_CM = 550.0
LOWER_DECK_CM = 610.0             # LOWER_UNDERSIDE + GALLERY_SLAB

# --- Upper tier (new) --------------------------------------------------------
UPPER_UNDERSIDE_CM = 890.0
UPPER_DECK_CM = 950.0
PARAPET_HEIGHT_CM = 120.0
PARAPET_THICKNESS_CM = 30.0

# --- Diagonal wedge ----------------------------------------------------------
RAMP_LOW_TOP_CM = 670.0           # top edge where it meets the truss wall
RAMP_HIGH_TOP_CM = 1070.0         # top edge where it meets the upper parapet
RAMP_BAND_CM = 200.0              # slab thickness measured vertically
RAMP_THICKNESS_CM = 30.0          # radial thickness

PLACE_RAMPS = True
PLACE_UPPER_TIER = True
REMOVE_OLD_STEPS = True

ACTOR_PREFIX = "ArenaOct_"
OUTLINER_FOLDER = "ArenaOctagon"
UNIT_CUBE_ASSET = "/Engine/BasicShapes/Cube"
UNIT_CUBE_SIZE_CM = 100.0
CENTRE = {"x": 0.0, "y": 0.0, "z": 0.0}
PROTECTED_LEVEL_NAMES = ["Lvl_ThirdPerson", "Lvl_DuelGraybox"]
DRY_RUN = False

# =============================================================================


def _call(tool, payload):
    return execute_tool(tool, json.dumps(payload))


def get_current_level():
    return _call("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]


def actors_in_folder(f):
    return _call("editor_toolset.toolsets.scene.SceneTools.get_actors_in_folder",
                 {"folder_path": f, "recursive": True})["returnValue"]


def get_label(a):
    return _call("editor_toolset.toolsets.actor.ActorTools.get_label", {"actor": a})["returnValue"]


def remove_actor(a):
    return _call("editor_toolset.toolsets.scene.SceneTools.remove_from_scene",
                 {"actor": a})["returnValue"]


def spawn_cube(name, loc, rot, scale_cm):
    xform = {"location": {"x": loc[0], "y": loc[1], "z": loc[2]},
             "rotation": {"pitch": rot[0], "yaw": rot[1], "roll": rot[2]},
             "scale": {"x": scale_cm[0] / UNIT_CUBE_SIZE_CM,
                       "y": scale_cm[1] / UNIT_CUBE_SIZE_CM,
                       "z": scale_cm[2] / UNIT_CUBE_SIZE_CM}}
    return _call("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
                 {"asset_path": UNIT_CUBE_ASSET, "name": name, "xform": xform,
                  "snap_to_ground": False})["returnValue"]


def set_folder(a, f):
    return _call("editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
                 {"actor": a, "folder_path": f})


def save_all():
    return _call("editor_toolset.toolsets.asset.AssetTools.save_assets",
                 {"asset_paths": []})["returnValue"]


def facet_yaw(i):
    return i * 45.0


def place(name, theta, radius, along, z, scale, roll=0.0):
    t = math.radians(theta)
    loc = (CENTRE["x"] + radius * math.cos(t) + along * -math.sin(t),
           CENTRE["y"] + radius * math.sin(t) + along * math.cos(t),
           CENTRE["z"] + z)
    a = spawn_cube(name, loc, (0.0, theta, roll), scale)
    set_folder(a, OUTLINER_FOLDER)
    return a


def truss_side_sign(i):
    """+1 when the nearest truss facet lies counterclockwise (+local Y)."""
    best = None
    for t in TRUSS_FACETS:
        d = (facet_yaw(t) - facet_yaw(i) + 180.0) % 360.0 - 180.0
        if best is None or abs(d) < abs(best):
            best = d
    return 1.0 if best > 0 else -1.0


def _build():
    level = get_current_level()
    report = {"level": level, "removed": [], "placed_labels": []}

    if level.rsplit("/", 1)[-1] in PROTECTED_LEVEL_NAMES:
        report["status"] = "REFUSED"
        return report
    if DRY_RUN:
        report["status"] = "DRY_RUN"
        return report

    # 1. The blocky step runs come out; the wedge replaces them.
    if REMOVE_OLD_STEPS:
        prefix = ACTOR_PREFIX + "ParapetStep_"
        for a in actors_in_folder(OUTLINER_FOLDER):
            lbl = get_label(a)
            if lbl.startswith(prefix) and remove_actor(a):
                report["removed"].append(lbl)

    labels = []
    par_radius = (APOTHEM_CM - GALLERY_OVERHANG_CM) + PARAPET_THICKNESS_CM / 2.0
    deck_radius = APOTHEM_CM - GALLERY_OVERHANG_CM / 2.0

    # 2. Upper tier for the ramps to land on.
    if PLACE_UPPER_TIER:
        for i in UPPER_TIER_FACETS:
            th = facet_yaw(i)
            n = "%sUpperGallery_%d" % (ACTOR_PREFIX, i)
            place(n, th, deck_radius, 0.0, UPPER_UNDERSIDE_CM + GALLERY_SLAB_CM / 2.0,
                  (GALLERY_OVERHANG_CM, PANEL_WIDTH_CM, GALLERY_SLAB_CM))
            labels.append(n)

            n = "%sUpperParapet_%d" % (ACTOR_PREFIX, i)
            place(n, th, par_radius, 0.0, UPPER_DECK_CM + PARAPET_HEIGHT_CM / 2.0,
                  (PARAPET_THICKNESS_CM, PANEL_WIDTH_CM, PARAPET_HEIGHT_CM))
            labels.append(n)

    # 3. The diagonal wedge: one solid slanted slab per diagonal facet.
    if PLACE_RAMPS:
        rise = RAMP_HIGH_TOP_CM - RAMP_LOW_TOP_CM
        angle = math.degrees(math.atan2(rise, PANEL_WIDTH_CM))
        length = math.hypot(PANEL_WIDTH_CM, rise)
        mid_z = (RAMP_LOW_TOP_CM + RAMP_HIGH_TOP_CM) / 2.0 - RAMP_BAND_CM / 2.0
        for i in RAMP_FACETS:
            th = facet_yaw(i)
            # Low end must be the truss end, so drop whichever side it is on.
            roll = -truss_side_sign(i) * angle
            n = "%sParapetRamp_%d" % (ACTOR_PREFIX, i)
            place(n, th, par_radius, 0.0, mid_z,
                  (RAMP_THICKNESS_CM, length, RAMP_BAND_CM), roll=roll)
            labels.append(n)

    report["placed"] = len(labels)
    report["placed_labels"] = labels
    report["ramp_angle_deg"] = round(
        math.degrees(math.atan2(RAMP_HIGH_TOP_CM - RAMP_LOW_TOP_CM, PANEL_WIDTH_CM)), 2)
    report["saved"] = save_all()
    report["status"] = "BUILT"
    return report


_RESULT = _build()


def run():
    return _RESULT
