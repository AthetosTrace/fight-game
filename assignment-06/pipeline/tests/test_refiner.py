"""One field per attempt, a recorded diff, and a refusal when the fix is not
ours to make."""

import pytest

import evaluator
import generator
import refiner


class TestFixes:
    def test_a_blank_required_field_is_restored_from_the_gdd(self, row_a, rules_doc):
        row_a["GameplayPurpose"] = ""
        violation = [v for v in evaluator.gate(row_a, rules_doc)
                     if v.rule_id == "C_REQUIRED"][0]
        result = refiner.refine(row_a, "C_REQUIRED", rules_doc, violation=violation)
        assert result.applied
        facts = rules_doc["gdd_attack_facts"]["A"]
        assert result.row["GameplayPurpose"] == facts["range_purpose"]

    def test_an_invented_asset_path_is_cleared(self, row_a, rules_doc):
        row_a["MontageAsset"] = "/Game/Anything/MM_Attack_A"
        violation = [v for v in evaluator.gate(row_a, rules_doc)
                     if v.rule_id == "C_BLANK"][0]
        result = refiner.refine(row_a, "C_BLANK", rules_doc, violation=violation)
        assert result.applied
        assert result.row["MontageAsset"] == ""

    def test_an_invented_number_is_replaced_by_the_gdd_wording(self, row_a, rules_doc):
        row_a["IntendedRange"] = "Close-range committed gauntlet force within 250 cm"
        violation = [v for v in evaluator.gate(row_a, rules_doc) if v.rule_id == "G6"][0]
        result = refiner.refine(row_a, "G6", rules_doc, violation=violation)
        assert result.applied
        assert "250" not in result.row["IntendedRange"]
        assert evaluator.gate(result.row, rules_doc) == []

    def test_an_upgraded_phase2_claim_is_restored(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Phase 2 grants an upgraded moveset"
        result = refiner.refine(row_a, "G3", rules_doc)
        assert result.applied
        assert result.row["Phase2Usage"] == generator.PHASE2_STATEMENT

    def test_adaptive_language_is_replaced(self, row_a, rules_doc):
        row_a["ActiveDescription"] = "Adapts to the player in real time"
        result = refiner.refine(row_a, "G4", rules_doc)
        assert result.applied
        assert evaluator.gate(result.row, rules_doc) == []

    def test_a_mismatched_row_name_is_aligned(self, row_a, rules_doc):
        row_a["Name"] = "Row_Z"
        violation = [v for v in evaluator.gate(row_a, rules_doc) if v.rule_id == "C_NAME"][0]
        result = refiner.refine(row_a, "C_NAME", rules_doc, violation=violation)
        assert result.applied
        assert result.row["Name"] == "Row_A"

    def test_a_wrong_enabled_flag_is_corrected(self, rules_doc):
        row = generator.base_row(rules_doc, "C")
        row["EnabledForSelection"] = "true"
        violation = [v for v in evaluator.gate(row, rules_doc) if v.rule_id == "C_MATRIX"][0]
        result = refiner.refine(row, "C_MATRIX", rules_doc, violation=violation)
        assert result.applied
        assert result.row["EnabledForSelection"] == "false"

    def test_an_uncaveated_name_is_recaveated(self, row_a, rules_doc):
        row_a["DisplayWorkingName"] = "Fault Line"
        result = refiner.refine(row_a, "restraint", rules_doc)
        assert result.applied
        assert "proposed" in result.row["DisplayWorkingName"].lower()

    def test_recaveating_keeps_the_proposed_name_itself(self, row_a, rules_doc):
        """Re-adding the caveat decides nothing. Choosing the canon name would,
        and this stage never does that."""
        row_a["DisplayWorkingName"] = "Fault Line"
        result = refiner.refine(row_a, "restraint", rules_doc)
        assert "Fault Line" in result.row["DisplayWorkingName"]

    def test_drifted_canon_wording_is_restored(self, row_a, rules_doc):
        row_a["IntendedRange"] = "Some punchy melee thing"
        result = refiner.refine(row_a, "canon_fidelity", rules_doc)
        assert result.applied
        assert result.row["IntendedRange"] == \
            rules_doc["gdd_attack_facts"]["A"]["range_purpose"]

    def test_a_broken_telegraph_is_restored(self, row_a, rules_doc):
        row_a["TelegraphRequirement"] = "It happens"
        result = refiner.refine(row_a, "telegraph_readability", rules_doc)
        assert result.applied
        assert evaluator.evaluate(result.row, rules_doc)["passed"] is True


class TestRefusals:
    @pytest.mark.parametrize("rule_id", ["G1", "G5", "G7"])
    def test_designer_decisions_are_refused(self, row_a, rules_doc, rule_id):
        result = refiner.refine(row_a, rule_id, rules_doc)
        assert not result.applied
        assert result.refused

    def test_the_refusal_names_the_reason(self, row_a, rules_doc):
        result = refiner.refine(row_a, "G7", rules_doc)
        assert "Q13" in result.refused

    def test_an_unknown_failure_is_refused_rather_than_guessed(self, row_a, rules_doc):
        result = refiner.refine(row_a, "G_NONEXISTENT", rules_doc)
        assert not result.applied
        assert "no refinement rule exists" in result.refused

    def test_a_failure_the_refiner_cannot_locate_is_refused(self, row_a, rules_doc):
        # Nothing is actually wrong, so the restraint fix has nothing to do.
        result = refiner.refine(row_a, "restraint", rules_doc)
        assert not result.applied
        assert "could not locate" in result.refused


class TestDiscipline:
    def test_the_input_row_is_never_mutated(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Phase 2 grants an upgraded moveset"
        before = dict(row_a)
        refiner.refine(row_a, "G3", rules_doc)
        assert row_a == before

    def test_exactly_one_field_changes_per_refinement(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Phase 2 grants an upgraded moveset"
        result = refiner.refine(row_a, "G3", rules_doc)
        changed = [k for k in row_a if row_a[k] != result.row[k]]
        assert changed == ["Phase2Usage"]

    def test_every_refinement_records_a_before_and_after(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Phase 2 grants an upgraded moveset"
        change = refiner.refine(row_a, "G3", rules_doc).change
        assert change["field"] and change["reason"]
        assert change["before"] != change["after"]

    def test_every_refusal_is_backed_by_a_documented_reason(self, rules_doc):
        for rule_id, reason in refiner.REFUSALS.items():
            assert len(reason) > 40, rule_id
