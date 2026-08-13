"""Every gate rule and every scored criterion, fired deliberately.

The most important test in this file is
`test_an_uncaveated_working_name_passes_the_gate` — it proves the two layers
are actually doing different jobs, which is the whole argument for having two.
"""

import pytest

import evaluator


def _ids(violations):
    return sorted({v.rule_id for v in violations})


class TestContractGate:
    def test_the_canonical_row_is_clean(self, row_a, rules_doc):
        assert evaluator.gate(row_a, rules_doc) == []

    def test_a_missing_column_fails_the_schema(self, row_a, rules_doc):
        del row_a["Notes"]
        assert "C_SCHEMA" in _ids(evaluator.gate(row_a, rules_doc))

    def test_an_extra_column_fails_the_schema(self, row_a, rules_doc):
        row_a["Invented"] = "x"
        assert "C_SCHEMA" in _ids(evaluator.gate(row_a, rules_doc))

    def test_a_schema_failure_stops_further_checks(self, row_a, rules_doc):
        del row_a["Notes"]
        assert _ids(evaluator.gate(row_a, rules_doc)) == ["C_SCHEMA"]

    def test_a_blank_required_field_is_caught(self, row_a, rules_doc):
        row_a["GameplayPurpose"] = ""
        assert "C_REQUIRED" in _ids(evaluator.gate(row_a, rules_doc))

    def test_an_overlong_field_is_caught(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "x" * 200
        assert "C_MAXLEN" in _ids(evaluator.gate(row_a, rules_doc))

    def test_an_invented_asset_path_is_caught(self, row_a, rules_doc):
        row_a["MontageAsset"] = "/Game/Anything/MM_Attack_A"
        assert "C_BLANK" in _ids(evaluator.gate(row_a, rules_doc))

    def test_a_mismatched_row_name_is_caught(self, row_a, rules_doc):
        row_a["Name"] = "Row_Z"
        assert "C_NAME" in _ids(evaluator.gate(row_a, rules_doc))

    def test_an_unsupported_status_is_caught(self, row_a, rules_doc):
        row_a["ImplementationStatus"] = "Complete"
        assert "C_STATUS" in _ids(evaluator.gate(row_a, rules_doc))

    def test_a_non_boolean_enabled_flag_is_caught(self, row_a, rules_doc):
        row_a["EnabledForSelection"] = "TRUE"
        assert "C_BOOL" in _ids(evaluator.gate(row_a, rules_doc))

    def test_enabling_a_planned_attack_is_caught(self, rules_doc):
        import generator
        row = generator.base_row(rules_doc, "C")
        row["EnabledForSelection"] = "true"
        assert "C_MATRIX" in _ids(evaluator.gate(row, rules_doc))

    def test_disabling_the_prototype_attack_is_caught(self, row_a, rules_doc):
        row_a["EnabledForSelection"] = "false"
        assert "C_MATRIX" in _ids(evaluator.gate(row_a, rules_doc))


class TestGddGate:
    def test_g1_rejects_an_attack_id_outside_the_set(self, row_a, rules_doc):
        row_a["AttackId"] = "E"
        assert "G1" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g1_rejects_a_fifth_attack_reference(self, row_a, rules_doc):
        row_a["Notes"] = "Pairs with the fifth attack in Phase 2."
        assert "G1" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g1_allows_denying_a_fifth_attack(self, row_a, rules_doc):
        row_a["Notes"] = "There is no fifth attack."
        assert "G1" not in _ids(evaluator.gate(row_a, rules_doc))

    def test_g3_rejects_an_upgraded_moveset(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Phase 2 grants an upgraded moveset"
        assert "G3" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g4_rejects_adaptive_language(self, row_a, rules_doc):
        row_a["ActiveDescription"] = "Adapts to the player in real time"
        assert "G4" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g4_allows_denying_adaptive_language(self, row_a, rules_doc):
        row_a["Notes"] = "Authored state machine; it never adapts to the player."
        assert "G4" not in _ids(evaluator.gate(row_a, rules_doc))

    def test_g5_rejects_deferred_scope(self, row_a, rules_doc):
        row_a["Notes"] = "Also used by the second boss in the additional arena."
        assert "G5" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g6_rejects_an_invented_number(self, row_a, rules_doc):
        row_a["IntendedRange"] = "Close-range committed gauntlet force within 250 cm"
        assert "G6" in _ids(evaluator.gate(row_a, rules_doc))

    def test_g6_allows_a_phase_reference(self, row_a, rules_doc):
        row_a["Notes"] = "Re-timed in Phase 2."
        assert "G6" not in _ids(evaluator.gate(row_a, rules_doc))

    def test_g6_allows_an_open_question_citation(self, row_a, rules_doc):
        row_a["Notes"] = "Travel cap is OPEN (design-brief Q13)."
        assert "G6" not in _ids(evaluator.gate(row_a, rules_doc))

    def test_g7_accepts_the_canonical_attack_d_row(self, row_d, rules_doc):
        assert "G7" not in _ids(evaluator.gate(row_d, rules_doc))

    def test_g7_rejects_a_full_arena_snap(self, row_d, rules_doc):
        row_d["ActiveDescription"] = "Instant close from anywhere via a full-arena snap"
        assert "G7" in _ids(evaluator.gate(row_d, rules_doc))

    def test_g7_requires_a_thruster_cue(self, row_d, rules_doc):
        # Both describing fields must lose the cue. Attack D's GDD readability
        # requirement states the thruster cue itself, so a row that still
        # carries it genuinely does declare one.
        row_d["ActiveDescription"] = "Moves forward quickly"
        row_d["TelegraphRequirement"] = "Approaches the player"
        row_d["Notes"] = "Approved metadata only."
        assert "G7" in _ids(evaluator.gate(row_d, rules_doc))

    def test_g7_accepts_a_cue_stated_only_in_the_telegraph_field(self, row_d, rules_doc):
        row_d["ActiveDescription"] = "Propulsion movement hard-capped by data"
        assert "G7" not in _ids(evaluator.gate(row_d, rules_doc))

    def test_g7_ignores_a_thruster_in_the_working_name(self, row_d, rules_doc):
        """'Thruster Snap' is a name, not a telegraph."""
        row_d["ActiveDescription"] = "Moves forward quickly"
        row_d["TelegraphRequirement"] = "Approaches the player"
        row_d["Notes"] = "Approved metadata only."
        assert "Thruster" in row_d["DisplayWorkingName"]
        assert "G7" in _ids(evaluator.gate(row_d, rules_doc))

    def test_g7_does_not_apply_to_other_attacks(self, row_a, rules_doc):
        row_a["ActiveDescription"] = "Uses a full-arena snap"
        assert "G7" not in _ids(evaluator.gate(row_a, rules_doc))


class TestScoredEvaluator:
    def test_the_canonical_row_passes_with_a_score(self, row_a, rules_doc):
        report = evaluator.evaluate(row_a, rules_doc)
        assert report["passed"] is True
        assert report["score"] == pytest.approx(100.0)

    def test_every_criterion_reports_a_score_and_a_reason(self, row_a, rules_doc):
        for criterion in evaluator.evaluate(row_a, rules_doc)["criteria"]:
            assert isinstance(criterion["score"], float)
            assert criterion["reason"]

    def test_the_report_carries_a_combined_reason(self, row_a, rules_doc):
        assert evaluator.evaluate(row_a, rules_doc)["reason"]

    def test_an_uncaveated_working_name_passes_the_gate(self, row_a, rules_doc):
        """The two layers do different jobs. 'Fault Line' is a legal string
        that would import cleanly -- and it asserts canon the GDD never
        granted. The gate cannot see that; the evaluator must."""
        row_a["DisplayWorkingName"] = "Fault Line"
        assert evaluator.gate(row_a, rules_doc) == []

    def test_an_uncaveated_working_name_fails_the_evaluator(self, row_a, rules_doc):
        row_a["DisplayWorkingName"] = "Fault Line"
        report = evaluator.evaluate(row_a, rules_doc)
        assert report["passed"] is False
        assert "restraint" in report["failed_criteria"]

    def test_a_high_score_still_fails_if_one_criterion_fails(self, row_a, rules_doc):
        row_a["DisplayWorkingName"] = "Fault Line"
        report = evaluator.evaluate(row_a, rules_doc)
        assert report["score"] > report["threshold"]
        assert report["passed"] is False

    def test_a_blank_working_name_is_restrained(self, row_a, rules_doc):
        row_a["DisplayWorkingName"] = ""
        assert evaluator.evaluate(row_a, rules_doc)["passed"] is True

    def test_canon_fidelity_falls_when_the_gdd_wording_drifts(self, row_a, rules_doc):
        row_a["IntendedRange"] = "Some punchy melee thing"
        report = evaluator.evaluate(row_a, rules_doc)
        assert "canon_fidelity" in report["failed_criteria"]

    def test_telegraph_readability_needs_a_cue(self, row_a, rules_doc):
        row_a["TelegraphRequirement"] = "It happens"
        row_a["RecoveryRequirement"] = "It ends"
        report = evaluator.evaluate(row_a, rules_doc)
        assert "telegraph_readability" in report["failed_criteria"]

    def test_phase2_consistency_needs_the_same_moveset_claim(self, row_a, rules_doc):
        row_a["Phase2Usage"] = "Used in Phase 2"
        report = evaluator.evaluate(row_a, rules_doc)
        assert "phase2_consistency" in report["failed_criteria"]

    def test_scores_are_bounded(self, row_a, rules_doc):
        report = evaluator.evaluate(row_a, rules_doc)
        assert 0.0 <= report["score"] <= 100.0


class TestRulesContract:
    def test_every_gdd_rule_cites_the_gdd(self, rules_doc):
        for rule in rules_doc["rules"]:
            assert "GDD v0.4 section" in rule["source"], rule["id"]

    def test_no_gdd_rule_cites_the_prototype_blackboard(self, rules_doc):
        """A5's rules traced to measured implementation. These must not."""
        for rule in rules_doc["rules"]:
            assert "PROTOTYPE_BLACKBOARD" not in rule["source"], rule["id"]

    def test_every_gdd_rule_names_a_page(self, rules_doc):
        for rule in rules_doc["rules"]:
            assert "page" in rule["source"].lower(), rule["id"]

    def test_every_rule_id_is_unique(self, rules_doc):
        ids = [rule["id"] for rule in rules_doc["rules"]]
        assert len(ids) == len(set(ids))

    def test_every_open_value_states_why(self, rules_doc):
        for entry in rules_doc["open_values"]:
            assert entry["why"]
            assert entry["source"]
