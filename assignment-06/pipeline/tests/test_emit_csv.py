"""Assembling the full table, and checking it against a referee that knows
nothing about this pipeline."""

import csv
import importlib.util
import os
import sys

import pytest

import emit_csv
import orchestrator

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(PIPELINE_DIR))
SHIPPED_VALIDATOR = os.path.join(REPO_ROOT, "tools", "validate_vanguard_attack_csv.py")

CLEAN_SEEDS = {"A": 16, "B": 16, "C": 16, "D": 16}


def _load_shipped_validator():
    """Load tools/validate_vanguard_attack_csv.py by path.

    It predates this pipeline and was written to guard the hand-authored CSV,
    which is exactly why it is worth checking against.
    """
    spec = importlib.util.spec_from_file_location("shipped_validator", SHIPPED_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestEmit:
    def test_all_four_attacks_are_emitted(self, rules_doc):
        rows, failures = emit_csv.emit(rules_doc, CLEAN_SEEDS)
        assert failures == []
        assert [row["AttackId"] for row in rows] == ["A", "B", "C", "D"]

    def test_a_failed_attack_is_reported_not_skipped_silently(self, rules_doc):
        seeds = dict(CLEAN_SEEDS)
        seeds["A"] = 3  # this seed stops for human review
        rows, failures = emit_csv.emit(rules_doc, seeds)
        assert failures
        assert failures[0][0] == "A"

    def test_no_table_is_written_when_an_attack_fails(self, rules_doc, tmp_path, capsys):
        out = str(tmp_path / "out.csv")
        code = emit_csv.main([
            "--out", out, "--seed-a", "3",
            "--seed-b", "16", "--seed-c", "16", "--seed-d", "16"])
        assert code == 2
        assert not os.path.exists(out)

    def test_the_written_table_uses_the_contract_column_order(self, rules_doc, tmp_path):
        rows, _ = emit_csv.emit(rules_doc, CLEAN_SEEDS)
        path = emit_csv.write_csv(
            rows, rules_doc["contract"]["headers"], str(tmp_path / "out.csv"))
        with open(path, encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        assert header == rules_doc["contract"]["headers"]

    def test_exactly_one_row_is_enabled(self, rules_doc):
        rows, _ = emit_csv.emit(rules_doc, CLEAN_SEEDS)
        enabled = [r["AttackId"] for r in rows if r["EnabledForSelection"] == "true"]
        assert enabled == ["A"]


@pytest.mark.skipif(not os.path.isfile(SHIPPED_VALIDATOR),
                    reason="shipped validator not present")
class TestAgainstTheShippedValidator:
    def test_the_generated_table_passes_the_shipped_validator(self, rules_doc, tmp_path):
        """The end-to-end claim: what this pipeline emits is import-ready by
        the standard that already guards the real CSV."""
        rows, _ = emit_csv.emit(rules_doc, CLEAN_SEEDS)
        path = emit_csv.write_csv(
            rows, rules_doc["contract"]["headers"], str(tmp_path / "generated.csv"))
        errors = _load_shipped_validator().validate(path)
        assert errors == []

    def test_the_shipped_validator_still_rejects_a_broken_table(self, rules_doc, tmp_path):
        """Guards against the above passing because the referee is asleep."""
        rows, _ = emit_csv.emit(rules_doc, CLEAN_SEEDS)
        rows[1]["EnabledForSelection"] = "true"  # two enabled attacks
        path = emit_csv.write_csv(
            rows, rules_doc["contract"]["headers"], str(tmp_path / "broken.csv"))
        assert _load_shipped_validator().validate(path)
