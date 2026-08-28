"""
Second-storey detail pass for the octagon arena. Payload for the Unreal MCP
ProgrammaticToolset -- see build_octagon_arena.py for why running this with
plain `python` raises NameError on execute_tool.

Runs ON TOP of an arena already built by build_octagon_arena.py. Additive except
for one deliberate removal: the gallery slabs on the two truss facets, because
the reference shows the gallery stopping at the truss wall.

Facet layout (yaw degrees, facet index i = yaw / 45):

      i=3 slope   i=2 flat   i=1 slope
                 (+Y, behind camera)
    i=4 TRUSS  <---- fight axis X ---->  i=0 TRUSS
       (-X)                                (+X)
      i=5 slope   i=6 flat   i=7 slope
                 (-Y, camera sees this)
"""

import json
import math

# =============================================================================
# PARAMETERS
# =============================================================================

# --- Must match the shell that was built --------------------------------------
APOTHEM_CM = 1590.0               # centre to wall face
PANEL_WIDTH_CM = 1367.2           # width of one facet
WALL_THICKNESS_CM = 40.0
WALL_HEIGHT_CM = 1200.0
GALLERY_UNDERSIDE_CM = 550.0
GALLERY_SLAB_CM = 60.0
GALLERY_OVERHANG_CM = 450.0

# --- Which facets get what ----------------------------------------------------
TRUSS_FACETS = [0, 4]             # tall solid wall, gallery interrupted
FLAT_PARAPET_FACETS = [2, 6]      # full-height gallery, level parapet
# Facets adjacent to a truss facet get the descending stepped parapet.

# --- Parapet ------------------------------------------------------------------
PARAPET_HEIGHT_CM = 120.0         # project placeholder railing_height_cm
PARAPET_THICKNESS_CM = 30.0
PARAPET_STEPS = 4                 # steps in each descending run
PARAPET_STEP_DROP_CM = 30.0       # height lost per step toward the truss wall

# --- X-braced truss panel (derived from Ref-Arena 1.jpg, PROPOSED) ------------
TRUSS_PANEL_WIDTH_CM = 900.0
TRUSS_PANEL_SILL_CM = 690.0
TRUSS_PANEL_HEAD_CM = 1050.0
TRUSS_PANEL_DEPTH_CM = 20.0       # how far it stands proud of the wall face
TRUSS_BRACE_THICKNESS_CM = 40.0
PLACE_TRUSS_PANEL = True
PLACE_TRUSS_BRACES = True

# --- Build behaviour ----------------------------------------------------------
REMOVE_GALLERY_ON_TRUSS_FACETS = True
PLACE_PARAPETS = True
ACTOR_PREFIX = "ArenaOct_"
OUTLINER_FOLDER = "ArenaOctagon"
UNIT_CUBE_ASSET = "/Engine/BasicShapes/Cube"
UNIT_CUBE_SIZE_CM = 100.0
CENTRE = {"x": 0.0, "y": 0.0, "z": 0.0}

# Lvl_DuelGraybox came off this list on 2026-08-27 for G07 -- see the note in
# build_octagon_arena.py. Checkpoint: Lvl_DuelGraybox_CP01_PreOctagon.
PROTECTED_LEVEL_NAMES = ["Lvl_ThirdPerson"]
DRY_RUN = False

# =============================================================================


def _call(tool, payload):
    return execute_tool(tool, json.dumps(payload))


def get_current_level():
    return _call("editor_toolset.toolsets.scene.SceneTools.get_current_level", {})["returnValue"]


def actors_in_folder(folder):
    return _call("editor_toolset.toolsets.scene.SceneTools.get_actors_in_folder",
                 {"folder_path": folder, "recursive": True})["returnValue"]


def get_label(actor):
    return _call("editor_toolset.toolsets.actor.ActorTools.get_label",
                 {"actor": actor})["returnValue"]


def remove_actor(actor):
    return _call("editor_toolset.toolsets.scene.SceneTools.remove_from_scene",
                 {"actor": actor})["returnValue"]


def spawn_cube(name, loc, rot, scale_cm):
    xform = {"location": {"x": loc[0], "y": loc[1], "z": loc[2]},
             "rotation": {"pitch": rot[0], "yaw": rot[1], "roll": rot[2]},
             "scale": {"x": scale_cm[0] / UNIT_CUBE_SIZE_CM,
                       "y": scale_cm[1] / UNIT_CUBE_SIZE_CM,
                       "z": scale_cm[2] / UNIT_CUBE_SIZE_CM}}
    return _call("editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
                 {"asset_path": UNIT_CUBE_ASSET, "name": name, "xform": xform,
                  "snap_to_ground": False})["returnValue"]


def set_folder(actor, folder):
    return _call("editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
                 {"actor": actor, "folder_path": folder})


def save_all():
    return _call("editor_toolset.toolsets.asset.AssetTools.save_assets",
                 {"asset_paths": []})["returnValue"]


# --- Frame helpers ------------------------------------------------------------

def facet_yaw(i):
    return i * 45.0


def radial(theta_deg):
    t = math.radians(theta_deg)
    return (math.cos(t), math.sin(t))


def tangent(theta_deg):
    """+local Y for a cube at this yaw: counterclockwise, i.e. increasing yaw."""
    t = math.radians(theta_deg)
    return (-math.sin(t), math.cos(t))


def place(name, theta, radius, along, z, scale, roll=0.0):
    """Place a cube in a facet's local frame: radius out, `along` tangential."""
    rx, ry = radial(theta)
    tx, ty = tangent(theta)
    loc = (CENTRE["x"] + radius * rx + along * tx,
           CENTRE["y"] + radius * ry + along * ty,
           CENTRE["z"] + z)
    a = spawn_cube(name, loc, (0.0, theta, roll), scale)
    set_folder(a, OUTLINER_FOLDER)
    return a


def truss_side_sign(i):
    """+1 if the nearest truss facet lies counterclockwise (+local Y), else -1."""
    best = None
    for t in TRUSS_FACETS:
        d = (facet_yaw(t) - facet_yaw(i) + 180.0) % 360.0 - 180.0
        if best is None or abs(d) < abs(best):
            best = d
    return 1.0 if best > 0 else -1.0


# --- Build steps --------------------------------------------------------------

def remove_truss_facet_galleries():
    """The gallery stops at the truss wall, so those two slabs come out."""
    targets = set("%sGallery_%d" % (ACTOR_PREFIX, i) for i in TRUSS_FACETS)
    removed = []
    for a in actors_in_folder(OUTLINER_FOLDER):
        lbl = get_label(a)
        if lbl in targets and remove_actor(a):
            removed.append(lbl)
    return removed


def build_truss_panels():
    placed = []
    inner_face = APOTHEM_CM - WALL_THICKNESS_CM / 2.0
    height = TRUSS_PANEL_HEAD_CM - TRUSS_PANEL_SILL_CM
    mid_z = (TRUSS_PANEL_HEAD_CM + TRUSS_PANEL_SILL_CM) / 2.0
    brace_len = math.hypot(TRUSS_PANEL_WIDTH_CM, height)
    brace_roll = math.degrees(math.atan2(height, TRUSS_PANEL_WIDTH_CM))

    for i in TRUSS_FACETS:
        theta = facet_yaw(i)
        if PLACE_TRUSS_PANEL:
            placed.append(place(
                "%sTrussPanel_%d" % (ACTOR_PREFIX, i), theta,
                inner_face - TRUSS_PANEL_DEPTH_CM / 2.0, 0.0, mid_z,
                (TRUSS_PANEL_DEPTH_CM, TRUSS_PANEL_WIDTH_CM, height)))
        if PLACE_TRUSS_BRACES:
            for k, roll in enumerate((brace_roll, -brace_roll)):
                placed.append(place(
                    "%sTrussBrace_%d_%d" % (ACTOR_PREFIX, i, k), theta,
                    inner_face - TRUSS_PANEL_DEPTH_CM - TRUSS_BRACE_THICKNESS_CM / 2.0,
                    0.0, mid_z,
                    (TRUSS_BRACE_THICKNESS_CM, brace_len, TRUSS_BRACE_THICKNESS_CM),
                    roll=roll))
    return placed


def build_parapets():
    placed = []
    deck_top = GALLERY_UNDERSIDE_CM + GALLERY_SLAB_CM
    inner_edge = APOTHEM_CM - GALLERY_OVERHANG_CM
    par_radius = inner_edge + PARAPET_THICKNESS_CM / 2.0

    for i in range(8):
        if i in TRUSS_FACETS:
            continue
        theta = facet_yaw(i)

        if i in FLAT_PARAPET_FACETS:
            placed.append(place(
                "%sParapet_%d" % (ACTOR_PREFIX, i), theta, par_radius, 0.0,
                deck_top + PARAPET_HEIGHT_CM / 2.0,
                (PARAPET_THICKNESS_CM, PANEL_WIDTH_CM, PARAPET_HEIGHT_CM)))
            continue

        # Descending run: tallest at the end away from the truss wall.
        sign = truss_side_sign(i)
        seg = PANEL_WIDTH_CM / PARAPET_STEPS
        for j in range(PARAPET_STEPS):
            h = PARAPET_HEIGHT_CM - j * PARAPET_STEP_DROP_CM
            if h <= 0.0:
                continue
            # j = 0 is the far end from the truss wall.
            along = -sign * (PANEL_WIDTH_CM / 2.0 - (j + 0.5) * seg)
            placed.append(place(
                "%sParapetStep_%d_%d" % (ACTOR_PREFIX, i, j), theta,
                par_radius, along, deck_top + h / 2.0,
                (PARAPET_THICKNESS_CM, seg, h)))
    return placed


def _build():
    level = get_current_level()
    report = {"level": level, "removed": [], "placed": 0, "actors": []}

    level_name = level.rsplit("/", 1)[-1]
    if level_name in PROTECTED_LEVEL_NAMES:
        report["status"] = "REFUSED"
        report["reason"] = "'%s' matches protected level name." % level
        return report

    if DRY_RUN:
        report["status"] = "DRY_RUN"
        return report

    if REMOVE_GALLERY_ON_TRUSS_FACETS:
        report["removed"] = remove_truss_facet_galleries()

    placed = []
    placed += build_truss_panels()
    if PLACE_PARAPETS:
        placed += build_parapets()

    report["placed"] = len(placed)
    report["saved"] = save_all()
    report["status"] = "BUILT"
    return report


_RESULT = _build()


def run():
    return _RESULT
