"""refiner -- the smallest correction, or an honest refusal."""

import pytest
from conftest import line

import evaluator
import refiner


def fault(rule_id, evidence=None):
    return {"rule_id": rule_id, "detail": "", "evidence": evidence}


def first_fault(rules_doc, judge, slot, text):
    evaluation = evaluator.evaluate(line(slot, text), rules_doc, judge)
    return evaluation["faults"][0]


# ---------------------------------------------------------------------------
# Tone fixes
# ---------------------------------------------------------------------------

def test_praise_is_removed(rules_doc):
    result = refiner.refine(line("meter_feedback_counter", "Nice work. Ascension rising."),
                            fault("T1"), rules_doc)
    assert result.applied
    assert "nice work" not in result.line["text"].lower()


def test_exclamation_becomes_a_period_in_a_sentence_slot(rules_doc):
    result = refiner.refine(line("meter_feedback_counter", "Counter landed. Ascension rising!"),
                            fault("T2"), rules_doc)
    assert result.applied
    assert "!" not in result.line["text"]
    assert result.line["text"].endswith(".")


def test_exclamation_is_dropped_outright_in_a_banner_slot(rules_doc):
    result = refiner.refine(line("impact_window_prompt", "IMPACT WINDOW - STRIKE NOW!"),
                            fault("T2"), rules_doc)
    assert result.applied
    assert not result.line["text"].endswith((".", "!"))


def test_hedge_is_removed(rules_doc):
    result = refiner.refine(
        line("meter_feedback_counter", "Maybe counter landed. Ascension rising."),
        fault("T3"), rules_doc)
    assert result.applied
    assert "maybe" not in result.line["text"].lower()


# ---------------------------------------------------------------------------
# Vocabulary and lore fixes
# ---------------------------------------------------------------------------

def test_generic_noun_is_swapped_for_the_canon_term(rules_doc):
    result = refiner.refine(
        line("meter_feedback_counter", "Counter landed. The super meter rises."),
        fault("V1", evidence="super meter"), rules_doc)
    assert result.applied
    assert "Ascension Meter" in result.line["text"]


def test_substitution_keeps_the_shouted_case_of_a_banner(rules_doc):
    result = refiner.refine(line("impact_window_prompt", "QTE - STRIKE NOW"),
                            fault("V1", evidence="qte"), rules_doc)
    assert result.applied
    assert "IMPACT WINDOW" in result.line["text"]


def test_missing_subject_restores_the_canonical_line(rules_doc):
    result = refiner.refine(line("meter_feedback_counter", "Counter landed. It rises."),
                            fault("V2", evidence="ascension"), rules_doc)
    assert result.applied
    assert "ascension" in result.line["text"].lower()


def test_a_false_claim_loses_its_whole_sentence(rules_doc):
    """Excising only the phrase would leave a fragment asserting half a
    falsehood, which is worse than the original."""
    result = refiner.refine(
        line("clash_failure_recovery",
             "The Clash broke. Return to neutral. Start over from the beginning."),
        fault("L2", evidence="start over"), rules_doc)
    assert result.applied
    assert "start over" not in result.line["text"].lower()
    assert "clash broke" in result.line["text"].lower()


def test_a_provisional_number_is_stripped_cleanly(rules_doc, rubric_judge):
    """The sign and brackets belong to the value. Stripping only the digits
    once shipped copy reading 'Ascension rising (+.'"""
    text = "Counter landed. Ascension rising (+15)."
    found = first_fault(rules_doc, rubric_judge, "meter_feedback_counter", text)
    result = refiner.refine(line("meter_feedback_counter", text), found, rules_doc)
    assert result.applied
    assert "15" not in result.line["text"]
    assert "+" not in result.line["text"]
    assert "(" not in result.line["text"]


# ---------------------------------------------------------------------------
# Format fixes
# ---------------------------------------------------------------------------

def test_over_length_restores_the_canonical_wording(rules_doc):
    spec = rules_doc["slots"]["impact_window_prompt"]
    long_text = "IMPACT WINDOW - STRIKE NOW AND KEEP STRIKING UNTIL IT ENDS"
    result = refiner.refine(line("impact_window_prompt", long_text), fault("F1"), rules_doc)
    assert result.applied
    assert len(result.line["text"]) <= spec["max_chars"]


def test_wrong_shape_is_reshaped_into_a_banner(rules_doc):
    result = refiner.refine(line("impact_window_prompt", "Impact window - strike now."),
                            fault("F2", evidence="sentence"), rules_doc)
    assert result.applied
    assert result.line["text"].isupper()
    assert not result.line["text"].endswith(".")


def test_an_over_long_banner_falls_back_to_the_canonical(rules_doc):
    """F2 carries two different faults. The word-count one has no mechanical
    repair -- dropping words means deciding what the line no longer says -- so
    it restores the canonical wording instead. Missing this branch turned every
    such run into a bogus 'refiner could not locate' refusal."""
    text = "PHASE 2 CRIMSON VANGUARD PRESSES VERY MUCH HARDER NOW"
    result = refiner.refine(line("phase2_callout", text),
                            fault("F2", evidence=9), rules_doc)
    assert result.applied
    assert result.line["text"] == rules_doc["slots"]["phase2_callout"]["canonical"]


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------

def test_l3_is_refused_because_two_rules_collide(rules_doc):
    """Stating both Final Clash gate conditions needs the 25% threshold, and L4
    forbids printing it. Neither rule is wrong; the contract cannot satisfy
    both, and that is the designer's call, not the refiner's."""
    result = refiner.refine(line("final_clash_unlock", "METER FULL - CLASH READY"),
                            fault("L3", evidence="meter full - clash ready"), rules_doc)
    assert not result.applied
    assert "L3" in result.refused
    assert "designer" in result.refused


def test_an_unknown_rule_is_refused_rather_than_guessed(rules_doc):
    result = refiner.refine(line("loss_screen", "anything"), fault("ZZ9"), rules_doc)
    assert not result.applied
    assert "no refinement rule exists" in result.refused


def test_a_fault_the_refiner_cannot_locate_is_refused(rules_doc):
    """Silence is not a correction: if the fix finds nothing to change, the
    loop has to stop rather than report success."""
    result = refiner.refine(line("meter_feedback_counter", "Counter landed. Ascension rising."),
                            fault("T1"), rules_doc)
    assert not result.applied


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

def test_refining_never_mutates_the_input(rules_doc):
    original = line("meter_feedback_counter", "Nice work. Ascension rising.")
    snapshot = dict(original)
    refiner.refine(original, fault("T1"), rules_doc)
    assert original == snapshot


def test_every_applied_change_records_a_before_and_after(rules_doc):
    result = refiner.refine(line("meter_feedback_counter", "Nice work. Ascension rising."),
                            fault("T1"), rules_doc)
    change = result.change
    assert change["before"] != change["after"]
    assert change["rule_id"] == "T1"
    assert change["reason"].strip()


def test_a_refusal_carries_no_line(rules_doc):
    result = refiner.refine(line("final_clash_unlock", "METER FULL - CLASH READY"),
                            fault("L3"), rules_doc)
    assert result.line is None
