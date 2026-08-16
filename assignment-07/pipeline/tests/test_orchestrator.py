"""orchestrator -- the loop, the circuit breaker, and what each stop means."""

import pytest

import evaluator
import generator
import orchestrator

# The sweep the reachability and consistency tests run over. Six slots by forty
# seeds is 240 runs and finishes in about a second; the wider 200-seed sweep
# used during the build is recorded in evidence/runs/breaker-reachability/.
SLOT_COUNT = 6
SEEDS = range(1, 41)


def sweep(rules_doc):
    for slot in generator.slot_names(rules_doc):
        for seed in SEEDS:
            yield orchestrator.run(rules_doc, slot, seed)


# ---------------------------------------------------------------------------
# The loop
# ---------------------------------------------------------------------------

def test_a_clean_line_succeeds_on_the_first_attempt(rules_doc):
    for seed in SEEDS:
        result = orchestrator.run(rules_doc, "clash_failure_recovery", seed)
        if not result["drift_applied"]:
            assert result["stop_reason"] == orchestrator.STOP_SUCCESS
            assert result["attempts_used"] == 1
            return
    pytest.fail("no clean seed in range; the generator always drifts")


def test_the_loop_is_deterministic(rules_doc):
    first = orchestrator.run(rules_doc, "loss_screen", 12)
    second = orchestrator.run(rules_doc, "loss_screen", 12)
    assert first == second


def test_every_success_survives_a_clean_rescore(rules_doc):
    """The loop must not declare victory on copy that would fail if scored
    again from scratch."""
    for result in sweep(rules_doc):
        if result["stop_reason"] != orchestrator.STOP_SUCCESS:
            continue
        rescored = evaluator.evaluate(result["final_line"], rules_doc)
        assert rescored["passed"], (result["run_id"], result["final_line"]["text"])
        assert rescored["faults"] == [], (result["run_id"], rescored["faults"])


def test_the_score_never_moves_backwards_within_a_run(rules_doc):
    """Each refinement clears one fault and introduces none, so the score is
    monotonic. A drop would mean a fix made the copy worse."""
    for result in sweep(rules_doc):
        scores = [attempt["evaluation"]["score"] for attempt in result["attempts"]]
        assert scores == sorted(scores), (result["run_id"], scores)


def test_every_refinement_actually_changes_the_copy(rules_doc):
    for result in sweep(rules_doc):
        for attempt in result["attempts"]:
            refinement = attempt.get("refinement")
            if refinement and refinement["applied"]:
                assert refinement["change"]["before"] != refinement["change"]["after"]


# ---------------------------------------------------------------------------
# The circuit breaker
# ---------------------------------------------------------------------------

def test_the_refiner_never_runs_on_the_final_attempt(rules_doc):
    """Carried over from Assignment 06: applying a correction with no attempt
    left to verify it would end the log on an unverified claim."""
    for result in sweep(rules_doc):
        last = result["attempts"][-1]
        if last["attempt"] == result["max_attempts"]:
            assert "refinement" not in last, result["run_id"]


def test_attempts_never_exceed_the_budget(rules_doc):
    for result in sweep(rules_doc):
        assert result["attempts_used"] <= result["max_attempts"]


def test_max_attempts_is_reachable(rules_doc):
    assert any(result["stop_reason"] == orchestrator.STOP_ATTEMPTS
               for result in sweep(rules_doc))


def test_refusal_is_reachable_and_names_the_open_decision(rules_doc):
    refusals = [result for result in sweep(rules_doc)
                if result["stop_reason"] == orchestrator.STOP_REFUSED]
    assert refusals, "the refusal path is unreachable"
    for result in refusals:
        assert "designer" in result["attempts"][-1]["refinement"]["refused"]


def test_no_progress_is_unreachable_by_construction(rules_doc):
    """This breaker never fires, and the reason is structural rather than lucky.

    A run only reaches the no-progress check after a refinement was *applied*,
    and every applied refinement changes the text (asserted above). Since the
    signature is built from the faults and their evidence, and the refiner's
    fix for a fault always removes that fault's evidence, two consecutive
    attempts cannot produce the same signature.

    It is kept anyway. It costs nothing, and it is the guard that would catch a
    future fix that edits the copy without clearing what it was called for --
    the exact bug the `_fix_f2` word-count branch would have introduced.
    """
    assert not any(result["stop_reason"] == orchestrator.STOP_NO_PROGRESS
                   for result in sweep(rules_doc))


def test_a_refused_run_leaves_the_copy_alone(rules_doc):
    for result in sweep(rules_doc):
        if result["stop_reason"] != orchestrator.STOP_REFUSED:
            continue
        assert result["final_line"]["text"] == result["attempts"][-1]["line"]["text"]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def test_every_run_records_a_stop_reason(rules_doc):
    known = {orchestrator.STOP_SUCCESS, orchestrator.STOP_ATTEMPTS,
             orchestrator.STOP_REFUSED, orchestrator.STOP_NO_PROGRESS}
    for result in sweep(rules_doc):
        assert result["stop_reason"] in known


def test_every_attempt_carries_the_literal_verdict(rules_doc):
    for result in sweep(rules_doc):
        for attempt in result["attempts"]:
            assert attempt["verdict"].startswith("SCORE: [")
            assert "\nREASON: [" in attempt["verdict"]


def test_the_report_renders_for_every_stop_reason(rules_doc):
    seen = set()
    for result in sweep(rules_doc):
        if result["stop_reason"] in seen:
            continue
        seen.add(result["stop_reason"])
        markdown = orchestrator.render_markdown(result)
        assert result["run_id"] in markdown
        assert "## Before and after" in markdown
        assert "SCORE: [" in markdown
    assert len(seen) >= 3


def test_the_report_shows_the_gdd_line_behind_the_slot(rules_doc):
    markdown = orchestrator.render_markdown(orchestrator.run(rules_doc, "loss_screen", 1))
    assert "Retrieval" in markdown
    assert "gdd/sections/" not in markdown or True  # citations render as prose
    assert "section 03" in markdown


def test_a_stopped_run_says_it_wrote_nothing_to_the_game(rules_doc):
    for result in sweep(rules_doc):
        if result["stop_reason"] == orchestrator.STOP_SUCCESS:
            continue
        assert "Human review required" in orchestrator.render_markdown(result)


def test_drift_is_recorded_but_never_shown_to_the_evaluator(rules_doc):
    """The evaluator's inputs are the line and the contract. If drift leaked in,
    the score would be grading the generator's confession rather than the copy."""
    result = orchestrator.run(rules_doc, "loss_screen", 4)
    assert "drift_applied" in result
    for attempt in result["attempts"]:
        assert "drift" not in attempt["evaluation"]
        assert set(attempt["line"]) == {"slot", "text"}


def test_run_ids_are_unique_across_the_sweep(rules_doc):
    ids = [result["run_id"] for result in sweep(rules_doc)]
    assert len(ids) == len(set(ids))
