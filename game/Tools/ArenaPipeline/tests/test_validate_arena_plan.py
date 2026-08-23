"""Tests for the deterministic arena plan validator.

Every rule gets a paired test: the baseline plan passes it, and a minimally
mutated plan fails it. If a threshold in arena_rules.json changes, these tests
say exactly which rule noticed.
"""

import copy
import json
import math
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE_ROOT)

import validate_arena_plan as V  # noqa: E402

BASELINE_PATH = os.path.join(PIPELINE_ROOT, "examples", "arena_plan.baseline.json")
RULES_PATH = os.path.join(PIPELINE_ROOT, "contracts", "arena_rules.json")


@pytest.fixture
def rules():
    with open(RULES_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def plan():
    with open(BASELINE_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def rule_ids(violations):
    return sorted({v.rule_id for v in violations})


# --- baseline ------------------------------------------------------------


def test_baseline_plan_has_no_violations(plan, rules):
    violations, _, _ = V.validate(plan, rules)
    assert violations == [], "baseline should pass every rule: %s" % [str(v) for v in violations]


def test_resolved_clashes_are_reported_but_do_not_block(plan, rules):
    """U1 and U2 are decided on our side, pending Anthony's confirmation. They
    belong in `decisions`, not in the blocking `review` list."""
    _, review, decisions = V.validate(plan, rules)
    assert any(note.startswith("U1") for note in decisions)
    assert any(note.startswith("U2") for note in decisions)
    assert not any("UNRESOLVED" in note for note in review)


def test_an_undecided_clash_does_block(plan, rules):
    mutated = copy.deepcopy(rules)
    mutated["unresolved"][0]["resolution"] = None
    _, review, _ = V.validate(plan, mutated)
    assert any("UNRESOLVED U1" in note for note in review)


def test_every_resolution_records_its_reasoning_and_reversal_cost(rules):
    for item in rules["unresolved"]:
        resolution = item.get("resolution")
        if resolution is None:
            continue
        for field in ("decision", "evidence", "cost_if_reversed", "decided_by", "confirm_with"):
            assert resolution.get(field), "%s resolution must record %s" % (item["id"], field)


def test_every_validator_check_has_a_rule(rules):
    defined = {rule["id"] for rule in rules["rules"]}
    assert set(V.CHECKS) <= defined


def test_every_rule_states_a_source(rules):
    for rule in rules["rules"]:
        assert rule.get("source"), "rule %s must cite a source document" % rule["id"]
        assert rule.get("status") in (
            "MEASURED", "APPROVED", "PROPOSED", "DERIVED"), rule["id"]


# --- per-rule failures ---------------------------------------------------


def test_r1_rejects_a_combat_axis_that_is_too_narrow(plan, rules):
    plan["combat_axis"] = {"axis": "X", "min_cm": -300.0, "max_cm": 300.0}
    violations, _, _ = V.validate(plan, rules)
    assert "R1" in rule_ids(violations)


def test_r2_rejects_geometry_crowding_the_combat_bound(plan, rules):
    plan["obstacles"].append(
        {"name": "Crate", "x_cm": 800.0, "y_cm": 0.0, "blocking": True})
    violations, _, _ = V.validate(plan, rules)
    assert "R2" in rule_ids(violations)


def test_r2_ignores_non_blocking_decor(plan, rules):
    plan["obstacles"].append(
        {"name": "Decal", "x_cm": 700.0, "y_cm": 0.0, "blocking": False})
    violations, _, _ = V.validate(plan, rules)
    assert "R2" not in rule_ids(violations)


def test_r3_rejects_a_floor_that_is_not_at_the_combat_plane(plan, rules):
    plan["floor"]["z_cm"] = 200.0
    violations, _, _ = V.validate(plan, rules)
    assert "R3" in rule_ids(violations)


def test_r3_rejects_an_obstacle_inside_the_fighting_space(plan, rules):
    plan["obstacles"].append(
        {"name": "CentrePlatform", "x_cm": 0.0, "y_cm": 0.0, "blocking": True})
    violations, _, _ = V.validate(plan, rules)
    assert "R3" in rule_ids(violations)


def test_r4_rejects_a_span_the_camera_cannot_frame(plan, rules):
    # This is the designed 2400 cm long axis from group-04 Q24. It fails the
    # measured camera curve -- the concrete form of unresolved question U1.
    plan["combat_axis"] = {"axis": "X", "min_cm": -1200.0, "max_cm": 1200.0}
    violations, _, _ = V.validate(plan, rules)
    assert "R4" in rule_ids(violations)


def test_r4_camera_distance_curve_matches_the_rig(rules):
    rule = V.rules_by_id(rules)["R4"]
    assert V.camera_distance_for_separation(1300.0, rule) == pytest.approx(1490.0)
    assert V.camera_distance_for_separation(110.0, rule) == pytest.approx(538.0)
    assert V.camera_distance_for_separation(9000.0, rule) == pytest.approx(1500.0)


def test_r5_rejects_a_shallow_floor_with_an_uncullable_near_wall(plan, rules):
    # 1600 cm is the designed Shattered Ring short axis. The camera pulls back
    # ~1457 cm at max separation, so it lands outside the shell -- the concrete
    # form of U2.
    plan["floor"]["short_axis_cm"] = 1600.0
    violations, _, _ = V.validate(plan, rules)
    assert "R5" in rule_ids(violations)


def test_r5_accepts_a_shallow_floor_when_the_near_wall_is_culled(plan, rules):
    """Resolution U2: near-wall culling is the accepted answer."""
    plan["floor"]["short_axis_cm"] = 1600.0
    plan["camera"] = {"near_wall_culled": True}
    violations, _, _ = V.validate(plan, rules)
    assert "R5" not in rule_ids(violations)


def test_r5_required_depth_tracks_the_actual_span(plan, rules):
    lookup = V.rules_by_id(rules)
    depth = V.required_camera_depth(plan, lookup["R4"], lookup["R5"])
    assert depth == pytest.approx(1490.0 * math.cos(math.radians(12.0)))


def test_r5_rejects_an_occluder_in_the_camera_corridor(plan, rules):
    plan["obstacles"].append({
        "name": "Truss", "x_cm": 1300.0, "y_cm": -1400.0,
        "blocking": True, "in_camera_corridor": True})
    violations, _, _ = V.validate(plan, rules)
    assert "R5" in rule_ids(violations)


def test_r6_rejects_spawns_that_are_too_close(plan, rules):
    plan["spawns"]["opponent"]["x_cm"] = 40.0
    violations, _, _ = V.validate(plan, rules)
    assert "R6" in rule_ids(violations)


def test_r6_rejects_spawns_that_are_too_far_apart(plan, rules):
    plan["spawns"]["opponent"]["x_cm"] = 600.0
    violations, _, _ = V.validate(plan, rules)
    assert "R6" in rule_ids(violations)


def test_r6_rejects_fighters_that_do_not_face_each_other(plan, rules):
    plan["spawns"]["opponent"]["yaw_deg"] = 90.0
    violations, _, _ = V.validate(plan, rules)
    assert "R6" in rule_ids(violations)


def test_r6_rejects_a_spawn_outside_the_combat_bounds(plan, rules):
    plan["spawns"]["player"]["x_cm"] = -900.0
    violations, _, _ = V.validate(plan, rules)
    assert "R6" in rule_ids(violations)


def test_r6_requires_both_spawns(plan, rules):
    del plan["spawns"]["opponent"]
    violations, _, _ = V.validate(plan, rules)
    assert "R6" in rule_ids(violations)


def test_r7_rejects_insufficient_jump_headroom(plan, rules):
    plan["ceiling_cm"] = 300.0
    violations, _, _ = V.validate(plan, rules)
    assert "R7" in rule_ids(violations)


def test_r7_rejects_an_unstated_ceiling(plan, rules):
    del plan["ceiling_cm"]
    violations, _, _ = V.validate(plan, rules)
    assert "R7" in rule_ids(violations)


def test_r8_rejects_a_boundary_inside_the_combat_volume(plan, rules):
    plan["boundaries"].append({"name": "Rubble", "x_cm": 100.0})
    violations, _, _ = V.validate(plan, rules)
    assert "R8" in rule_ids(violations)


# --- contract discipline -------------------------------------------------


def test_missing_required_key_is_a_schema_violation(plan, rules):
    del plan["combat_axis"]
    violations, _, _ = V.validate(plan, rules)
    assert rule_ids(violations) == ["SCHEMA"]


def test_a_proposed_rule_is_not_enforced_without_approval(plan, rules):
    mutated = copy.deepcopy(rules)
    for rule in mutated["rules"]:
        if rule["id"] == "R1":
            rule["status"] = "PROPOSED"
    plan["combat_axis"] = {"axis": "X", "min_cm": -300.0, "max_cm": 300.0}

    violations, review, _ = V.validate(plan, mutated)
    assert "R1" not in rule_ids(violations)
    assert any("R1" in note and "PROPOSED" in note for note in review)


def test_a_proposed_rule_is_enforced_under_an_explicit_waiver(plan, rules):
    mutated = copy.deepcopy(rules)
    for rule in mutated["rules"]:
        if rule["id"] == "R1":
            rule["status"] = "PROPOSED"
    plan["combat_axis"] = {"axis": "X", "min_cm": -300.0, "max_cm": 300.0}

    violations, _, _ = V.validate(plan, mutated, allow_proposed=True)
    assert "R1" in rule_ids(violations)
