"""The loop and its circuit breaker -- every stop reason, deliberately."""

import json
import os

import evaluator
import generator
import orchestrator
import refiner


class TestStopReasons:
    def test_a_clean_row_succeeds_on_the_first_attempt(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=16)
        assert result["stop_reason"] == orchestrator.STOP_SUCCESS
        assert result["attempts_used"] == 1

    def test_a_drifted_row_is_refined_then_succeeds(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=2)
        assert result["stop_reason"] == orchestrator.STOP_SUCCESS
        assert result["attempts_used"] > 1

    def test_the_refiner_refusing_stops_the_loop(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=3)
        assert result["stop_reason"] == orchestrator.STOP_REFUSED

    def test_running_out_of_attempts_trips_the_breaker(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=4)
        assert result["stop_reason"] == orchestrator.STOP_ATTEMPTS
        assert result["attempts_used"] == result["max_attempts"]

    def test_no_progress_trips_the_breaker(self, rules_doc, monkeypatch):
        """A refiner that reports success while changing nothing must be
        caught. Without this guard the loop would burn every attempt on an
        identical failure and report MAX_ATTEMPTS, hiding a stuck stage."""
        def noop_refine(row, failure_key, rules_doc_, violation=None):
            return refiner.Refinement(row=dict(row), change={
                "field": "Notes", "before": "x", "after": "x", "reason": "no-op"})

        monkeypatch.setattr(orchestrator, "refine", noop_refine)
        result = orchestrator.run(rules_doc, "A", seed=1, max_attempts=6)
        assert result["stop_reason"] == orchestrator.STOP_NO_PROGRESS

    def test_no_applied_refinement_ever_leaves_the_signature_unchanged(self, rules_doc):
        """Why the guard above needs a stub, and why no real seed reaches it.

        The no-progress breaker trips only when the refiner *applies* a change
        that leaves the failure signature identical. The real refiner has no
        such path: every branch either restores a field from the canonical GDD
        facts, which always moves the signature, or it refuses, which ends the
        run as a human-review stop instead.

        This asserts that invariant directly. The full-space version is
        evidence/runs/circuit-breaker-reachability/ -- 200,000 runs, zero
        no-progress stops. If a future refiner branch ever gains a partial-fix
        path, this test fails and the guard stops being unreachable.
        """
        for attack_id in ("A", "B", "C", "D"):
            for seed in range(60):
                row = generator.generate(rules_doc, attack_id, seed)["row"]
                previous = None
                for _ in range(12):
                    violations = evaluator.gate(row, rules_doc)
                    evaluation = (evaluator.evaluate(row, rules_doc)
                                  if not violations else None)
                    if not violations and evaluation["passed"]:
                        break
                    signature = orchestrator._signature(violations, evaluation)
                    assert signature != previous, (
                        "attack %s seed %d repeated failure signature %r -- the "
                        "refiner applied a no-op" % (attack_id, seed, signature))
                    previous = signature

                    failure_key, violation = orchestrator._next_failure(
                        violations, evaluation)
                    refinement = refiner.refine(
                        row, failure_key, rules_doc, violation=violation)
                    if not refinement.applied:
                        break
                    row = refinement.row

    def test_a_successful_run_ends_on_a_verified_row(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=2)
        assert evaluator.gate(result["final_row"], rules_doc) == []
        assert evaluator.evaluate(result["final_row"], rules_doc)["passed"] is True


class TestLoopDiscipline:
    def test_the_refiner_never_runs_on_the_final_attempt(self, rules_doc):
        """Applying a correction we never re-validate would end the log on an
        unverified claim."""
        result = orchestrator.run(rules_doc, "A", seed=4)
        assert "refinement" not in result["attempts"][-1]

    def test_every_attempt_records_its_outcome(self, rules_doc):
        for seed in (2, 3, 4, 16):
            for record in orchestrator.run(rules_doc, "A", seed)["attempts"]:
                assert record["outcome"]

    def test_the_evaluator_only_runs_on_a_gate_clean_row(self, rules_doc):
        for seed in range(1, 25):
            for record in orchestrator.run(rules_doc, "A", seed)["attempts"]:
                if record["violations"]:
                    assert "evaluation" not in record

    def test_a_run_is_reproducible(self, rules_doc):
        first = orchestrator.run(rules_doc, "A", seed=4)
        second = orchestrator.run(rules_doc, "A", seed=4)
        assert first["attempts"] == second["attempts"]
        assert first["stop_reason"] == second["stop_reason"]

    def test_max_attempts_is_never_exceeded(self, rules_doc):
        for seed in range(1, 40):
            result = orchestrator.run(rules_doc, "A", seed)
            assert result["attempts_used"] <= result["max_attempts"]

    def test_a_failed_run_still_reports_its_last_row(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=3)
        assert result["final_row"] == result["attempts"][-1]["row"]


class TestSweep:
    def test_every_attack_and_seed_terminates_with_a_known_stop_reason(self, rules_doc):
        known = {
            orchestrator.STOP_SUCCESS, orchestrator.STOP_ATTEMPTS,
            orchestrator.STOP_REFUSED, orchestrator.STOP_NO_PROGRESS,
        }
        for attack_id in "ABCD":
            for seed in range(1, 30):
                assert orchestrator.run(rules_doc, attack_id, seed)["stop_reason"] in known

    def test_no_successful_run_ever_writes_an_open_value(self, rules_doc):
        """The declaration's failure case: an OPEN field filled with an
        invented value. Across the sweep, this must never happen."""
        blank_fields = rules_doc["contract"]["must_be_blank_fields"]
        for attack_id in "ABCD":
            for seed in range(1, 30):
                result = orchestrator.run(rules_doc, attack_id, seed)
                if result["stop_reason"] != orchestrator.STOP_SUCCESS:
                    continue
                for field in blank_fields:
                    assert result["final_row"][field] == ""

    def test_no_successful_run_ever_asserts_an_uncaveated_name(self, rules_doc):
        for attack_id in "ABCD":
            for seed in range(1, 30):
                result = orchestrator.run(rules_doc, attack_id, seed)
                if result["stop_reason"] != orchestrator.STOP_SUCCESS:
                    continue
                name = result["final_row"]["DisplayWorkingName"]
                assert not name or "proposed" in name.lower()


class TestReporting:
    def test_markdown_names_the_stop_reason(self, rules_doc):
        result = orchestrator.run(rules_doc, "A", seed=3)
        assert result["stop_reason"] in orchestrator.render_markdown(result)

    def test_markdown_lists_the_gdd_citations(self, rules_doc):
        markdown = orchestrator.render_markdown(orchestrator.run(rules_doc, "A", seed=16))
        assert "gdd/ascendant-impact-gdd" in markdown

    def test_markdown_reports_the_score_for_a_scored_attempt(self, rules_doc):
        markdown = orchestrator.render_markdown(orchestrator.run(rules_doc, "A", seed=16))
        assert "SCORE" in markdown

    def test_a_failed_run_says_human_review_is_required(self, rules_doc):
        markdown = orchestrator.render_markdown(orchestrator.run(rules_doc, "A", seed=3))
        assert "Human review required" in markdown

    def test_reports_are_written_to_disk(self, rules_doc, tmp_path):
        result = orchestrator.run(rules_doc, "A", seed=16)
        run_dir = orchestrator.write_report(result, rules_doc, str(tmp_path))
        assert os.path.isfile(os.path.join(run_dir, "run.json"))
        assert os.path.isfile(os.path.join(run_dir, "run.md"))
        assert os.path.isfile(os.path.join(run_dir, "final_row.csv"))

    def test_a_failed_run_emits_no_csv(self, rules_doc, tmp_path):
        result = orchestrator.run(rules_doc, "A", seed=3)
        run_dir = orchestrator.write_report(result, rules_doc, str(tmp_path))
        assert not os.path.isfile(os.path.join(run_dir, "final_row.csv"))

    def test_the_emitted_csv_uses_the_contract_column_order(self, rules_doc, tmp_path):
        result = orchestrator.run(rules_doc, "A", seed=16)
        run_dir = orchestrator.write_report(result, rules_doc, str(tmp_path))
        with open(os.path.join(run_dir, "final_row.csv"), encoding="utf-8") as handle:
            header = handle.readline().strip().split(",")
        assert header == rules_doc["contract"]["headers"]

    def test_the_run_record_is_json_serialisable(self, rules_doc):
        json.dumps(orchestrator.run(rules_doc, "A", seed=4))
