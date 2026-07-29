"""Tests for tools/validate_vanguard_attack_csv.py.

Positive fixture: a CSV that satisfies the contract end to end.
Negative fixtures: one CSV per rule the validator is required to catch,
per CLAUDE_CODE_OVERNIGHT_WORK_ORDER_V2.md Task 4.
"""

import csv
import os
import sys
import tempfile
import unittest

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import validate_vanguard_attack_csv as validator  # noqa: E402


HEADER = validator.CONTRACT_HEADERS


def _row(
    name="Row_A",
    attack_id="A",
    display_working_name="Fault Line (proposed)",
    status="Prototype",
    enabled="true",
    intended_range="Close-range committed gauntlet force",
    purpose="Close-range committed gauntlet force",
    telegraph_req="Distinct wind-up and punishable recovery",
    tracking_rule="",
    active_desc="Authored gauntlet-force hitbox trace during the committed active window",
    recovery_req="Deliberate exposed opening after the committed strike",
    phase2_usage="Same attack, re-timed via Phase 2 parameters - no new moveset",
    montage="",
    telegraph_vfx="",
    telegraph_audio="",
    hit_socket="",
    notes="",
):
    return {
        "Name": name,
        "AttackId": attack_id,
        "DisplayWorkingName": display_working_name,
        "ImplementationStatus": status,
        "EnabledForSelection": enabled,
        "IntendedRange": intended_range,
        "GameplayPurpose": purpose,
        "TelegraphRequirement": telegraph_req,
        "TrackingRule": tracking_rule,
        "ActiveDescription": active_desc,
        "RecoveryRequirement": recovery_req,
        "Phase2Usage": phase2_usage,
        "MontageAsset": montage,
        "TelegraphVfxAsset": telegraph_vfx,
        "TelegraphAudioAsset": telegraph_audio,
        "HitTraceSocket": hit_socket,
        "Notes": notes,
    }


def _valid_rows():
    return [
        _row(),
        _row(
            name="Row_B",
            attack_id="B",
            display_working_name="Advance Line (proposed)",
            status="Planned",
            enabled="false",
            intended_range="Committed forward-pressure sequence",
            purpose="Committed forward-pressure sequence",
            telegraph_req="Visible first beat and stable tracking limit",
            tracking_rule="Body/tracking locks at a fixed point once the active window begins",
            active_desc="Multi-beat authored forward-pressure sequence",
            recovery_req="Deliberate exposed opening after the committed sequence completes",
        ),
        _row(
            name="Row_C",
            attack_id="C",
            display_working_name="Bulwark Reach (proposed)",
            status="Planned",
            enabled="false",
            intended_range="Armored reach and space control",
            purpose="Armored reach and space control",
            telegraph_req="Clear body direction and visible active range",
            tracking_rule="Body direction locks before the active window",
            active_desc="Wide authored active-range hitbox trace",
            recovery_req="Deliberate exposed opening after the committed strike",
        ),
        _row(
            name="Row_D",
            attack_id="D",
            display_working_name="Thruster Snap (proposed)",
            status="Planned",
            enabled="false",
            intended_range="Short propulsion-assisted approach",
            purpose="Short propulsion-assisted approach",
            telegraph_req="Thruster cue before movement; no hidden full-arena snap",
            active_desc="Thruster-cued propulsion movement hard-capped by data",
            recovery_req="Deliberate exposed opening after the propulsion approach completes",
            notes="Max travel distance is OPEN (design-brief Q13) and must not be invented here",
        ),
    ]


def _write_csv(rows, path, header=None):
    header = header or HEADER
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in header})


class TempCsvTestCase(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self._tmpdir.name, "DT_VanguardAttacks.csv")

    def tearDown(self):
        self._tmpdir.cleanup()

    def write(self, rows, header=None):
        _write_csv(rows, self.path, header=header)


class TestPositiveFixture(TempCsvTestCase):
    def test_valid_csv_passes(self):
        self.write(_valid_rows())
        errors = validator.validate(self.path)
        self.assertEqual(errors, [], msg=f"Unexpected errors: {errors}")

    def test_phase2usage_digit_is_not_a_false_positive(self):
        # Regression test: "Phase 2" inside Phase2Usage must not trip the
        # numeric-value check.
        self.write(_valid_rows())
        errors = validator.validate(self.path)
        self.assertFalse(
            any("Phase2Usage" in e for e in errors),
            msg=f"Phase2Usage incorrectly flagged: {errors}",
        )

    def test_question_id_citation_is_not_a_false_positive(self):
        # Regression test: "Q13" inside Notes is a citation, not an invented
        # numeric gameplay value.
        self.write(_valid_rows())
        errors = validator.validate(self.path)
        self.assertFalse(
            any("Notes" in e for e in errors),
            msg=f"Notes incorrectly flagged: {errors}",
        )


class TestNegativeFixtures(TempCsvTestCase):
    def test_missing_file_fails(self):
        errors = validator.validate(os.path.join(self._tmpdir.name, "does_not_exist.csv"))
        self.assertTrue(errors)
        self.assertIn("not found", errors[0])

    def test_wrong_headers_fail(self):
        bad_header = HEADER[:-1]  # drop the last column
        self.write(_valid_rows(), header=bad_header)
        errors = validator.validate(self.path)
        self.assertTrue(any("headers" in e.lower() for e in errors))

    def test_wrong_row_count_fails(self):
        rows = _valid_rows()[:3]
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("Expected exactly 4 rows" in e for e in errors))

    def test_ids_not_exactly_a_b_c_d_fails(self):
        rows = _valid_rows()
        rows[3]["AttackId"] = "E"
        rows[3]["Name"] = "Row_E"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("AttackId" in e for e in errors))

    def test_more_than_one_enabled_fails(self):
        rows = _valid_rows()
        rows[1]["EnabledForSelection"] = "true"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("More than one attack is enabled" in e for e in errors))

    def test_attack_a_disabled_fails(self):
        rows = _valid_rows()
        rows[0]["EnabledForSelection"] = "false"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("Attack A must be EnabledForSelection=true" in e for e in errors)
            or any("No attack is enabled" in e for e in errors)
        )

    def test_b_c_or_d_enabled_fails(self):
        rows = _valid_rows()
        rows[0]["EnabledForSelection"] = "false"
        rows[2]["EnabledForSelection"] = "true"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("Only Attack A may be enabled" in e for e in errors)
        )

    def test_unsupported_status_fails(self):
        rows = _valid_rows()
        rows[1]["ImplementationStatus"] = "InProgress"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("unsupported ImplementationStatus" in e for e in errors))

    def test_required_field_blank_fails(self):
        rows = _valid_rows()
        rows[0]["GameplayPurpose"] = ""
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("GameplayPurpose' is blank" in e for e in errors))

    def test_duplicate_ids_fail(self):
        rows = _valid_rows()
        rows[3]["AttackId"] = "A"
        rows[3]["Name"] = "Row_A"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("Duplicate AttackId" in e for e in errors)
            or any("AttackId set must be exactly" in e for e in errors)
        )

    def test_duplicate_names_fail(self):
        rows = _valid_rows()
        rows[1]["Name"] = "Row_A"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("does not match expected" in e for e in errors)
            or any("Duplicate row Name" in e for e in errors)
        )

    def test_fifth_attack_language_fails(self):
        rows = _valid_rows()
        rows[3]["Notes"] = "Do not confuse this with a fifth attack under any circumstance"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("scope-expansion" in e for e in errors))

    def test_runtime_learning_language_fails(self):
        rows = _valid_rows()
        rows[0]["Notes"] = "Crimson Vanguard learns from the player's patterns over time"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("runtime-learning" in e for e in errors))

    def test_scope_expansion_language_fails(self):
        rows = _valid_rows()
        rows[0]["Notes"] = "This attack is also usable in multiplayer PvP matches"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(any("scope-expansion" in e for e in errors))

    def test_numeric_value_in_forbidden_field_fails(self):
        rows = _valid_rows()
        rows[0]["IntendedRange"] = "Close range, deals 45 damage within 150cm"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("contains a numeric value" in e and "IntendedRange" in e for e in errors)
        )

    def test_invented_asset_path_fails(self):
        rows = _valid_rows()
        rows[0]["MontageAsset"] = "/Game/AscendantImpact/Rival/AM_Vanguard_AttackA"
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("MontageAsset" in e and "must remain blank" in e for e in errors)
        )


class TestMaxLengthEnforcement(TempCsvTestCase):
    """Proves every field in VANGUARD_ATTACK_ROW_CONTRACT.md §2 has its max
    length enforced by validator.MAX_LENGTHS, per row contract."""

    def test_display_working_name_over_limit_fails(self):
        rows = _valid_rows()
        rows[0]["DisplayWorkingName"] = "X" * (
            validator.MAX_LENGTHS["DisplayWorkingName"] + 1
        )
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any(
                "DisplayWorkingName" in e and "exceeds max length" in e
                for e in errors
            ),
            msg=f"Expected a DisplayWorkingName length violation, got: {errors}",
        )

    def test_phase2usage_over_limit_fails(self):
        rows = _valid_rows()
        rows[1]["Phase2Usage"] = "X" * (validator.MAX_LENGTHS["Phase2Usage"] + 1)
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("Phase2Usage" in e and "exceeds max length" in e for e in errors),
            msg=f"Expected a Phase2Usage length violation, got: {errors}",
        )

    def test_recovery_requirement_over_limit_fails(self):
        rows = _valid_rows()
        rows[0]["RecoveryRequirement"] = "X" * (
            validator.MAX_LENGTHS["RecoveryRequirement"] + 1
        )
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any(
                "RecoveryRequirement" in e and "exceeds max length" in e
                for e in errors
            ),
            msg=f"Expected a RecoveryRequirement length violation, got: {errors}",
        )

    def test_tracking_rule_over_limit_fails(self):
        rows = _valid_rows()
        rows[1]["TrackingRule"] = "X" * (validator.MAX_LENGTHS["TrackingRule"] + 1)
        self.write(rows)
        errors = validator.validate(self.path)
        self.assertTrue(
            any("TrackingRule" in e and "exceeds max length" in e for e in errors),
            msg=f"Expected a TrackingRule length violation, got: {errors}",
        )

    def test_every_contract_field_enforces_its_max_length(self):
        # One field over its limit at a time, across every column the
        # contract defines a max length for — not just the fields the
        # review report happened to catch.
        for field, limit in validator.MAX_LENGTHS.items():
            with self.subTest(field=field):
                rows = _valid_rows()
                rows[0][field] = "X" * (limit + 1)
                path = os.path.join(self._tmpdir.name, f"over_{field}.csv")
                _write_csv(rows, path)
                errors = validator.validate(path)
                self.assertTrue(
                    any(
                        f"'{field}'" in e and "exceeds max length" in e
                        for e in errors
                    ),
                    msg=f"Expected a max-length violation for {field}, got: {errors}",
                )

    def test_free_text_field_at_exact_limit_does_not_trip_length_check(self):
        # Fields constrained to exact enum/id/boolean values or forced blank
        # can't be padded to their character limit without also failing an
        # unrelated rule, so this boundary check is scoped to genuine
        # free-text fields.
        free_text_fields = [
            "DisplayWorkingName",
            "IntendedRange",
            "GameplayPurpose",
            "TelegraphRequirement",
            "TrackingRule",
            "ActiveDescription",
            "RecoveryRequirement",
            "Phase2Usage",
            "Notes",
        ]
        for field in free_text_fields:
            with self.subTest(field=field):
                limit = validator.MAX_LENGTHS[field]
                rows = _valid_rows()
                rows[0][field] = "X" * limit
                path = os.path.join(self._tmpdir.name, f"exact_{field}.csv")
                _write_csv(rows, path)
                errors = validator.validate(path)
                self.assertFalse(
                    any(
                        f"'{field}'" in e and "exceeds max length" in e
                        for e in errors
                    ),
                    msg=(
                        f"Field {field} at exactly its limit ({limit}) was "
                        f"incorrectly flagged: {errors}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
