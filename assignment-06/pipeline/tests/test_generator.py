"""The generator must be canon-faithful before drift, and reproducible after."""

import pytest

import evaluator
import generator

ATTACKS = ("A", "B", "C", "D")


class TestBaseRow:
    @pytest.mark.parametrize("attack_id", ATTACKS)
    def test_the_base_row_passes_the_gate_cleanly(self, rules_doc, attack_id):
        row = generator.base_row(rules_doc, attack_id)
        assert evaluator.gate(row, rules_doc) == []

    @pytest.mark.parametrize("attack_id", ATTACKS)
    def test_the_base_row_passes_the_evaluator(self, rules_doc, attack_id):
        row = generator.base_row(rules_doc, attack_id)
        assert evaluator.evaluate(row, rules_doc)["passed"] is True

    @pytest.mark.parametrize("attack_id", ATTACKS)
    def test_fields_come_from_the_gdd_facts(self, rules_doc, attack_id):
        row = generator.base_row(rules_doc, attack_id)
        facts = rules_doc["gdd_attack_facts"][attack_id]
        assert row["IntendedRange"] == facts["range_purpose"]
        assert row["TelegraphRequirement"] == facts["readability_requirement"]

    @pytest.mark.parametrize("attack_id", ATTACKS)
    def test_working_names_are_always_caveated(self, rules_doc, attack_id):
        row = generator.base_row(rules_doc, attack_id)
        assert "proposed" in row["DisplayWorkingName"].lower()

    def test_only_attack_a_is_enabled(self, rules_doc):
        enabled = [a for a in ATTACKS
                   if generator.base_row(rules_doc, a)["EnabledForSelection"] == "true"]
        assert enabled == ["A"]

    @pytest.mark.parametrize("attack_id", ATTACKS)
    def test_no_asset_path_is_invented(self, rules_doc, attack_id):
        row = generator.base_row(rules_doc, attack_id)
        for field in rules_doc["contract"]["must_be_blank_fields"]:
            assert row[field] == ""

    def test_an_unknown_attack_is_rejected(self, rules_doc):
        with pytest.raises(ValueError):
            generator.generate(rules_doc, "E", seed=1)


class TestDrift:
    def test_generation_is_reproducible_for_a_seed(self, rules_doc):
        first = generator.generate(rules_doc, "A", seed=4)
        second = generator.generate(rules_doc, "A", seed=4)
        assert first["row"] == second["row"]
        assert first["drift_applied"] == second["drift_applied"]

    def test_different_seeds_can_produce_different_rows(self, rules_doc):
        rows = {tuple(sorted(generator.generate(rules_doc, "A", seed=s)["row"].items()))
                for s in range(1, 20)}
        assert len(rows) > 1

    def test_zero_drift_rate_reproduces_the_base_row(self, rules_doc):
        result = generator.generate(rules_doc, "A", seed=4, drift_rate=0.0)
        assert result["row"] == generator.base_row(rules_doc, "A")
        assert result["drift_applied"] == []

    def test_drift_is_reported_with_its_operator(self, rules_doc):
        result = generator.generate(rules_doc, "A", seed=4)
        assert result["drift_applied"]
        for entry in result["drift_applied"]:
            assert entry["operator"]
            assert entry["effect"]

    def test_snap_drift_only_applies_to_attack_d(self, rules_doc):
        for attack_id in ("A", "B", "C"):
            for seed in range(1, 40):
                ops = [d["operator"]
                       for d in generator.generate(rules_doc, attack_id, seed)["drift_applied"]]
                assert "snap_travel" not in ops


class TestRetrievalEvidence:
    def test_every_generation_carries_gdd_citations(self, rules_doc):
        result = generator.generate(rules_doc, "A", seed=1)
        assert result["retrieval"]["gdd_citations"]

    def test_the_hard_constraint_chunk_is_always_retrieved(self, rules_doc):
        result = generator.generate(rules_doc, "B", seed=7)
        headings = [c["heading"] for c in result["retrieval"]["selected"]]
        assert "Hard constraint" in headings

    def test_the_scope_lock_chunk_is_always_retrieved(self, rules_doc):
        result = generator.generate(rules_doc, "B", seed=7)
        headings = [c["heading"] for c in result["retrieval"]["selected"]]
        assert any(h.startswith("Scope lock") for h in headings)
