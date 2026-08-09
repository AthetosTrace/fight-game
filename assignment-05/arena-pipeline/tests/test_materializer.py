"""Tests for the materializer stage.

The stage exists because the plan is dimensionless and the level is not. Most
of these tests are therefore about the gap between a centre and a face: that
the re-check catches what the deterministic gate structurally cannot, and that
the generator now reserves the footprint so the two agree.
"""

import copy
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE_ROOT)

import generator as G  # noqa: E402
import materializer as M  # noqa: E402
import orchestrator as O  # noqa: E402
import validate_arena_plan as V  # noqa: E402

RULES_PATH = os.path.join(PIPELINE_ROOT, "contracts", "arena_rules.json")


@pytest.fixture
def rules():
    with open(RULES_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def clean_plan(rules):
    result = O.run(rules, seed=8)
    assert result["stop_reason"] == O.STOP_SUCCESS
    return result["final_plan"]


# --- approval gating -----------------------------------------------------


def test_proposed_extents_are_refused_without_a_waiver(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=False)
    assert manifest["placements"] == []
    assert any("PROPOSED" in note for note in manifest["human_review"])


def test_proposed_extents_build_under_a_waiver_but_say_so(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    assert manifest["placements"]
    assert any("allow-proposed" in note for note in manifest["human_review"])


def test_missing_extents_block_is_review_not_a_guess(rules, clean_plan):
    stripped = copy.deepcopy(rules)
    del stripped["materializer"]
    manifest = M.build_manifest(clean_plan, stripped, allow_proposed=True)
    assert manifest["placements"] == []
    assert any("cannot be guessed" in note for note in manifest["human_review"])


def test_an_invalid_plan_is_never_built(rules, clean_plan):
    broken = copy.deepcopy(clean_plan)
    broken["combat_axis"]["max_cm"] = 100.0  # fails R1
    manifest = M.build_manifest(broken, rules, allow_proposed=True)
    assert manifest["placements"] == []
    assert any("deterministic gate" in note for note in manifest["human_review"])


# --- the centre-versus-face gap ------------------------------------------


def test_r2_is_measured_to_the_near_face(rules, clean_plan):
    """The regression this stage was built for.

    An obstacle centre 507.7 cm beyond the bound clears R2 on paper; given the
    declared depth its near face is only 482.7 cm out. Both the gate and the
    realised re-check must object -- they measure the same edge now.
    """
    plan = copy.deepcopy(clean_plan)
    plan["obstacles"][0]["x_cm"] = 1157.7

    violations, _, _ = V.validate(plan, rules, allow_proposed=True)
    gate = [v for v in violations if v.rule_id == "R2"]
    assert len(gate) == 1
    assert "482.7" in str(gate[0])

    manifest = M.build_manifest(plan, rules, allow_proposed=True)
    assert any("deterministic gate" in note for note in manifest["human_review"])


def test_a_plan_declaring_no_footprint_keeps_point_semantics(rules, clean_plan):
    """Archived and hand-written plans predate the footprint field."""
    plan = copy.deepcopy(clean_plan)
    del plan["obstacle_extents"]
    plan["obstacles"][0]["x_cm"] = 1157.7
    violations, _, _ = V.validate(plan, rules, allow_proposed=True)
    assert not [v for v in violations if v.rule_id == "R2"]


def test_declared_footprint_drives_the_placed_box(rules, clean_plan):
    """The materializer must build what the gate measured, not what the
    contract happens to say."""
    plan = copy.deepcopy(clean_plan)
    plan["obstacle_extents"]["height_cm"] = 275.0
    manifest = M.build_manifest(plan, rules, allow_proposed=True)
    obstacle = [p for p in manifest["placements"]
                if p["role"] == M.ROLE_OBSTACLE][0]
    assert obstacle["size_cm"]["z"] == pytest.approx(275.0)


def test_generated_plans_survive_the_face_recheck(rules):
    """The generator must reserve the footprint it knows the plan will acquire.

    Swept rather than spot-checked: the two defects this stage found were both
    seed-dependent, and seed 8 happened to be clean for each of them.
    """
    checked = 0
    for seed in range(1, 51):
        result = O.run(rules, seed=seed)
        if result["stop_reason"] != O.STOP_SUCCESS:
            continue
        checked += 1
        manifest = M.build_manifest(result["final_plan"], rules, allow_proposed=True)
        assert manifest["realised_violations"] == [], (
            "seed %d passed the gate but its realised geometry does not: %s"
            % (seed, manifest["realised_violations"]))
        assert manifest["interpenetrations"] == [], (
            "seed %d places geometry inside other geometry: %s"
            % (seed, manifest["interpenetrations"]))
    assert checked >= 30, "sweep covered only %d seeds; it is not proving much" % checked


def test_generator_declares_the_footprint_it_reserved(rules):
    plan = G.generate(rules, 8)
    assert plan["obstacle_extents"]["depth_cm"] == pytest.approx(
        float(rules["materializer"]["obstacle_depth_cm"]))


def test_generator_reserves_the_obstacle_half_depth(rules):
    plan = G.generate(rules, 8)
    half_depth = V.obstacle_half_depth(plan)
    bound = float(plan["combat_axis"]["max_cm"])
    margin = float(V.rules_by_id(rules)["R2"]["min_clearance_beyond_bound_cm"])
    for obstacle in plan["obstacles"]:
        near_face = abs(float(obstacle["x_cm"])) - half_depth
        assert near_face - bound >= margin - 1e-6


def test_obstacles_stay_inside_the_side_railings(rules):
    plan = G.generate(rules, 8)
    half_width = float(rules["materializer"]["obstacle_width_cm"]) / 2.0
    limit = float(plan["floor"]["short_axis_cm"]) / 2.0
    for obstacle in plan["obstacles"]:
        assert abs(float(obstacle["y_cm"])) + half_width <= limit + 1e-6


# --- placement geometry --------------------------------------------------


def test_floor_top_lands_on_the_combat_plane(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    floor = [p for p in manifest["placements"] if p["role"] == M.ROLE_FLOOR][0]
    top = floor["location"]["z"] + floor["size_cm"]["z"] / 2.0
    assert top == pytest.approx(float(clean_plan["floor"]["z_cm"]))


def test_wall_inner_face_sits_on_the_declared_boundary_plane(rules, clean_plan):
    """A wall built centred on its plane would put half its thickness inside
    the room, quietly shrinking the arena."""
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    walls = {p["name"]: p for p in manifest["placements"] if p["role"] == M.ROLE_WALL}
    for boundary in clean_plan["boundaries"]:
        if boundary.get("axis") != "x":
            continue
        wall = walls[boundary["name"]]
        plane = float(boundary["x_cm"])
        inner = wall["location"]["x"] - (wall["size_cm"]["x"] / 2.0
                                         if plane >= 0 else -wall["size_cm"]["x"] / 2.0)
        assert inner == pytest.approx(plane)


def test_ceiling_underside_matches_the_planned_headroom(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    ceiling = [p for p in manifest["placements"] if p["role"] == M.ROLE_CEILING][0]
    underside = ceiling["location"]["z"] - ceiling["size_cm"]["z"] / 2.0
    assert underside == pytest.approx(float(clean_plan["ceiling_cm"]))


def test_spawn_markers_carry_the_planned_yaw(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    spawns = {p["name"]: p for p in manifest["placements"]
              if p["role"] == M.ROLE_SPAWN}
    assert spawns["Spawn_Player"]["rotation"]["yaw"] == pytest.approx(
        float(clean_plan["spawns"]["player"]["yaw_deg"]))
    assert spawns["Spawn_Opponent"]["rotation"]["yaw"] == pytest.approx(
        float(clean_plan["spawns"]["opponent"]["yaw_deg"]))


def test_railings_are_not_treated_as_combat_volume_intrusions(rules, clean_plan):
    """A side railing runs parallel to the combat axis and spans x = 0 by
    design -- R8's axis semantics, carried through to the realised check."""
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    assert not [v for v in manifest["realised_violations"]
                if "Railing" in v["message"]]


def test_scale_is_derived_from_the_unit_cube(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    unit = float(rules["materializer"]["unit_cube_size_cm"])
    for entry in manifest["placements"]:
        if "scale" not in entry:
            continue
        for axis in ("x", "y", "z"):
            assert entry["scale"][axis] == pytest.approx(
                entry["size_cm"][axis] / unit)


def test_clean_plan_places_no_interpenetrating_geometry(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    assert manifest["interpenetrations"] == []


# --- emitted build script ------------------------------------------------


def test_build_script_is_emitted_and_covers_every_placement(rules, clean_plan):
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    script = M.render_mcp_script(manifest, "/Game/ArenaTools/Maps/Lvl_Test")
    compile(script, "build_level.py", "exec")  # must be valid Python
    for entry in manifest["placements"]:
        assert entry["name"] in script
    assert "/Game/ArenaTools/Maps/Lvl_Test" in script


def test_build_script_only_touches_the_arenatools_namespace(rules, clean_plan):
    """The asset boundary is enforced in code, not just documented."""
    manifest = M.build_manifest(clean_plan, rules, allow_proposed=True)
    script = M.render_mcp_script(manifest, "/Game/ArenaTools/Maps/Lvl_Test")
    for forbidden in ("/Game/ThirdPerson", "/Game/Variant_Combat",
                      "/Game/AscendantImpact", "Lvl_DuelGraybox", "BP_Vanguard"):
        assert forbidden not in script
