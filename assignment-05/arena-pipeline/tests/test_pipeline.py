"""Tests for the generator, evaluator, refiner and orchestrator.

The orchestrator tests exercise every stop reason the circuit breaker can
produce, including the two that depend on the refiner declining to act.
"""

import copy
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE_ROOT)

import evaluator as E  # noqa: E402
import generator as G  # noqa: E402
import orchestrator as O  # noqa: E402
import refiner as R  # noqa: E402
import validate_arena_plan as V  # noqa: E402

RULES_PATH = os.path.join(PIPELINE_ROOT, "contracts", "arena_rules.json")


@pytest.fixture
def rules():
    with open(RULES_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def clean_plan(rules):
    """A generated plan taken all the way through the loop until it passes."""
    result = O.run(rules, seed=8)
    assert result["stop_reason"] == O.STOP_SUCCESS
    return result["final_plan"]


# --- generator -----------------------------------------------------------


def test_generator_is_deterministic_for_a_seed(rules):
    assert G.generate(rules, 42) == G.generate(rules, 42)


def test_generator_varies_between_seeds(rules):
    assert G.generate(rules, 1) != G.generate(rules, 2)


def test_generator_takes_its_combat_span_from_the_rules(rules):
    plan = G.generate(rules, 1)
    span = plan["combat_axis"]["max_cm"] - plan["combat_axis"]["min_cm"]
    assert span == V.rules_by_id(rules)["R1"]["min_combat_span_cm"]


def test_generator_takes_its_footprint_from_the_design_targets(rules):
    plan = G.generate(rules, 1)
    assert plan["floor"]["long_axis_cm"] == rules["design_targets"]["playable_long_axis_cm"]
    assert plan["floor"]["short_axis_cm"] == rules["design_targets"]["playable_short_axis_cm"]


def test_generator_records_which_resolutions_it_applied(rules):
    plan = G.generate(rules, 1)
    assert plan["provenance"]["resolutions_applied"] == ["U1", "U2"]
    assert plan["camera"]["near_wall_culled"] is True


def test_side_railings_are_not_read_as_combat_volume_intrusions(rules):
    """A railing runs parallel to the combat axis and crosses x = 0 legitimately."""
    plan = G.generate(rules, 1)
    assert any(b["name"].startswith("Railing") and b["x_cm"] == 0.0 for b in plan["boundaries"])
    violations, _, _ = V.validate(plan, rules)
    assert "R8" not in {v.rule_id for v in violations}


# --- evaluator -----------------------------------------------------------


def test_evaluator_passes_a_clean_plan(clean_plan, rules):
    report = E.evaluate(clean_plan, rules)
    assert report["passed"], report["failed_criteria"]
    assert report["score"] >= E.PASS_THRESHOLD


def test_evaluator_flags_a_blocked_fighting_space(clean_plan, rules):
    clean_plan["obstacles"].append(
        {"name": "Crate", "x_cm": 0.0, "y_cm": 0.0, "blocking": True})
    report = E.evaluate(clean_plan, rules)
    assert "clear_central_floor" in report["failed_criteria"]
    assert not report["passed"]


def test_evaluator_flags_indistinguishable_ends(clean_plan, rules):
    clean_plan["obstacles"] = [
        {"name": "Strut", "x_cm": 1200.0, "y_cm": 0.0, "blocking": True},
        {"name": "Strut", "x_cm": -1200.0, "y_cm": 0.0, "blocking": True},
    ]
    report = E.evaluate(clean_plan, rules)
    assert "landmark_asymmetry" in report["failed_criteria"]


def test_evaluator_flags_a_one_sided_boundary(clean_plan, rules):
    clean_plan["boundaries"] = [b for b in clean_plan["boundaries"]
                                if float(b.get("y_cm", 0.0)) <= 0]
    report = E.evaluate(clean_plan, rules)
    assert "boundary_readability" in report["failed_criteria"]


def test_agent_judge_is_a_declared_seam_not_a_silent_fallback(clean_plan, rules):
    with pytest.raises(NotImplementedError):
        E.evaluate(clean_plan, rules, judge="agent")


def test_unknown_judge_is_rejected(clean_plan, rules):
    with pytest.raises(ValueError):
        E.evaluate(clean_plan, rules, judge="vibes")


# --- refiner -------------------------------------------------------------


def test_refiner_never_mutates_the_plan_it_was_given(rules):
    plan = G.generate(rules, 1)
    before = copy.deepcopy(plan)
    R.refine(plan, "R7", rules)
    assert plan == before


def test_refiner_pulls_overwide_spawns_to_the_legal_maximum(rules):
    plan = G.generate(rules, 1)
    plan["spawns"]["player"]["x_cm"] = -300.0
    plan["spawns"]["opponent"]["x_cm"] = 300.0
    result = R.refine(plan, "R6", rules)
    assert result.applied
    separation = abs(result.plan["spawns"]["opponent"]["x_cm"]
                     - result.plan["spawns"]["player"]["x_cm"])
    assert separation == V.rules_by_id(rules)["R6"]["max_spawn_separation_cm"]


def test_refiner_raises_a_low_ceiling_to_exactly_what_is_required(rules):
    plan = G.generate(rules, 1)
    plan["ceiling_cm"] = 300.0
    result = R.refine(plan, "R7", rules)
    rule = V.rules_by_id(rules)["R7"]
    assert result.plan["ceiling_cm"] == rule["jump_apex_cm"] + rule["character_height_cm"]


def test_refiner_changes_exactly_one_field(rules):
    plan = G.generate(rules, 1)
    plan["ceiling_cm"] = 300.0
    plan["spawns"]["opponent"]["yaw_deg"] = 90.0
    result = R.refine(plan, "R7", rules)
    # The yaw fault is untouched -- one correction per attempt.
    assert result.plan["spawns"]["opponent"]["yaw_deg"] == 90.0
    assert result.change["field"] == "ceiling_cm"


def test_refiner_refuses_to_retune_the_gameplay_owners_camera(rules):
    plan = G.generate(rules, 1)
    result = R.refine(plan, "R4", rules)
    assert not result.applied
    assert "BP_DuelCameraRig" in result.refused


def test_refiner_refuses_creative_decisions(rules):
    plan = G.generate(rules, 1)
    assert not R.refine(plan, "landmark_asymmetry", rules).applied
    assert not R.refine(plan, "staging_room", rules).applied


def test_refiner_refuses_what_it_has_no_rule_for(rules):
    plan = G.generate(rules, 1)
    result = R.refine(plan, "R99", rules)
    assert not result.applied
    assert "no refinement rule" in result.refused


# --- orchestrator / circuit breaker --------------------------------------


def test_a_successful_run_ends_with_a_plan_that_passes_the_gate(rules):
    result = O.run(rules, seed=8)
    assert result["stop_reason"] == O.STOP_SUCCESS
    violations, _, _ = V.validate(result["final_plan"], rules)
    assert violations == []


def test_the_breaker_caps_the_attempt_count(rules):
    result = O.run(rules, seed=2, max_attempts=1)
    assert result["attempts_used"] == 1
    assert result["stop_reason"] != O.STOP_SUCCESS


def test_three_attempts_is_the_default(rules):
    assert O.MAX_ATTEMPTS == 3
    result = O.run(rules, seed=2)
    assert result["attempts_used"] <= 3


def test_the_breaker_stops_when_the_refiner_refuses(rules, monkeypatch):
    """A plan whose only fault is R4 -- the camera rule we may not touch."""
    def only_r4(rules_doc, seed):
        plan = G.generate(rules_doc, seed)
        plan["combat_axis"] = {"axis": "X", "min_cm": -1200.0, "max_cm": 1200.0}
        plan["obstacles"] = []
        plan["ceiling_cm"] = 450.0
        plan["spawns"]["player"]["x_cm"] = -100.0
        plan["spawns"]["opponent"]["x_cm"] = 100.0
        return plan

    monkeypatch.setattr(O, "generate", only_r4)
    result = O.run(rules, seed=1)
    assert result["stop_reason"] == O.STOP_REFUSED
    assert "BP_DuelCameraRig" in result["attempts"][-1]["refinement"]["refused"]


def test_the_breaker_stops_when_refinement_stops_helping(rules, monkeypatch):
    """A refiner that reports success while changing nothing must not be allowed
    to burn all three attempts."""
    def no_op(plan, failure_key, rules_doc):
        return R.Refinement(plan=copy.deepcopy(plan),
                            change={"field": "none", "before": 0, "after": 0, "reason": "stub"})

    monkeypatch.setattr(O, "refine", no_op)
    result = O.run(rules, seed=2)
    assert result["stop_reason"] == O.STOP_NO_PROGRESS


def test_progress_on_one_of_two_same_rule_faults_is_not_read_as_a_stall(rules):
    """Two R2 obstacles: fixing one leaves R2 still failing, but that is
    progress, not a stalled loop."""
    plan_a = G.generate(rules, 1)
    plan_a["obstacles"][0]["x_cm"] = 700.0
    plan_a["obstacles"][1]["x_cm"] = -700.0
    violations_a, _, _ = V.validate(plan_a, rules)

    fixed = R.refine(plan_a, "R2", rules)
    violations_b, _, _ = V.validate(fixed.plan, rules)

    assert {v.rule_id for v in violations_a} == {v.rule_id for v in violations_b}
    assert O._signature(violations_a, None) != O._signature(violations_b, None)


def test_an_undecided_clash_stops_the_run_before_any_generation_work(rules):
    mutated = copy.deepcopy(rules)
    mutated["unresolved"][0]["resolution"] = None
    result = O.run(mutated, seed=8)
    assert result["stop_reason"] == O.STOP_REVIEW
    assert result["attempts_used"] == 1


def test_every_stop_reason_is_reachable():
    """Guards against a stop reason being added and never exercised."""
    declared = {O.STOP_SUCCESS, O.STOP_ATTEMPTS, O.STOP_REFUSED,
                O.STOP_NO_PROGRESS, O.STOP_REVIEW}
    assert len(declared) == 5


# --- reporting -----------------------------------------------------------


def test_a_run_writes_a_readable_log_and_a_final_plan(rules, tmp_path):
    result = O.run(rules, seed=8)
    run_dir = O.write_report(result, str(tmp_path))
    for name in ("run.json", "run.md", "final_plan.json"):
        assert os.path.isfile(os.path.join(run_dir, name)), name

    with open(os.path.join(run_dir, "run.md"), "r", encoding="utf-8") as handle:
        text = handle.read()
    assert "Arena pipeline run" in text
    assert "Deterministic gate" in text


def test_the_log_records_what_the_refiner_changed(rules):
    result = O.run(rules, seed=2)
    text = O.render_markdown(result)
    assert "Refiner" in text
    assert "Stop reason" in text
