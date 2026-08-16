"""evaluator -- the score is the verdict, and the reason names the rule."""

import re

import pytest
from conftest import line

import evaluator


# ---------------------------------------------------------------------------
# Output shape -- the assignment specifies this literally
# ---------------------------------------------------------------------------

def test_verdict_uses_the_required_score_and_reason_format(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(line("loss_screen", "Nice work! it wins!!"),
                                    rules_doc, rubric_judge)
    verdict = evaluator.format_verdict(evaluation)
    assert re.match(r"^SCORE: \[\d+(\.\d+)?/10\]\nREASON: \[.+\]$", verdict, re.DOTALL)


def test_reason_is_never_empty(rules_doc, rubric_judge, slots):
    for slot in slots:
        spec = rules_doc["slots"][slot]
        evaluation = evaluator.evaluate(line(slot, spec["canonical"]), rules_doc, rubric_judge)
        assert evaluation["reason"].strip()


def test_score_is_on_a_one_to_ten_scale(rules_doc, rubric_judge):
    worst = evaluator.evaluate(
        line("impact_window_prompt",
             "Awesome!! Maybe try the super meter, it fills over time (+20) and the duel restarts"),
        rules_doc, rubric_judge)
    assert 1.0 <= worst["score"] <= 10.0
    assert worst["score"] < 5.0


def test_a_clean_line_scores_ten(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("impact_window_prompt", "IMPACT WINDOW - STRIKE NOW"), rules_doc, rubric_judge)
    assert evaluation["score"] == 10.0
    assert evaluation["passed"]


# ---------------------------------------------------------------------------
# The score is the only gate
# ---------------------------------------------------------------------------

def test_pass_is_decided_by_the_score_alone(rules_doc, rubric_judge):
    """Assignment 06 required a clean gate *and* every criterion to pass. That
    is a binary verdict and this brief forbids one, so `passed` here is derived
    from the score and nothing else can veto it."""
    evaluation = evaluator.evaluate(
        line("loss_screen", "The evaluation ends here. Crimson Vanguard still stands."),
        rules_doc, rubric_judge)
    assert evaluation["passed"] is (evaluation["score"] >= evaluation["threshold"])


def test_severity_is_ordered_by_score(rules_doc, rubric_judge):
    """A lore break has to cost more than a stray word, or the score carries no
    information beyond pass/fail."""
    stray_word = evaluator.evaluate(
        line("phase2_callout", "PHASE 2 - CRIMSON VANGUARD PRESSES HARDER NOW OK"),
        rules_doc, rubric_judge)["score"]
    lore_break = evaluator.evaluate(
        line("meter_feedback_counter", "Ascension fills over time."),
        rules_doc, rubric_judge)["score"]
    assert lore_break < stray_word


def test_threshold_rejects_any_single_fault(rules_doc, rubric_judge):
    """The cheapest possible fault must still fail. Otherwise copy ships with a
    known defect and a passing grade."""
    evaluation = evaluator.evaluate(
        line("final_clash_unlock", "FINAL CLASH READY - COMMIT."), rules_doc, rubric_judge)
    assert evaluation["faults"]
    assert not evaluation["passed"]


# ---------------------------------------------------------------------------
# Tone
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,rule", [
    ("Nice work. Ascension rising.", "T1"),
    ("Counter landed. Ascension rising!", "T2"),
    ("Maybe counter. Ascension rising.", "T3"),
])
def test_tone_faults_are_attributed_to_the_right_rule(rules_doc, rubric_judge, text, rule):
    evaluation = evaluator.evaluate(line("meter_feedback_counter", text),
                                    rules_doc, rubric_judge)
    assert rule in [fault["rule_id"] for fault in evaluation["faults"]]


def test_tone_criterion_reports_its_backend(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("loss_screen", "The evaluation ends here. Crimson Vanguard still stands."),
        rules_doc, rubric_judge)
    tone = next(c for c in evaluation["criteria"] if c["criterion"] == "tone")
    assert tone["backend"] == "rubric"


def test_denied_praise_is_not_a_tone_fault(rules_doc, rubric_judge):
    """Negation awareness has to survive into the scored criterion, not just
    the matcher it is built on."""
    evaluation = evaluator.evaluate(
        line("loss_screen", "This was not great work. Crimson Vanguard still stands."),
        rules_doc, rubric_judge)
    assert "T1" not in [fault["rule_id"] for fault in evaluation["faults"]]


# ---------------------------------------------------------------------------
# Vocabulary and lore
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("slot,text,rule", [
    ("meter_feedback_counter", "Counter landed. The super meter rises.", "V1"),
    ("impact_window_prompt", "QTE - STRIKE NOW", "V1"),
    ("loss_screen", "The evaluation ends here. The boss still stands.", "V1"),
    ("meter_feedback_counter", "Counter landed. It rises.", "V2"),
    ("meter_feedback_counter", "Counter landed. Ascension fills over time.", "L1"),
    ("clash_failure_recovery", "The Clash broke. Start over from the beginning.", "L2"),
    ("meter_feedback_counter", "Counter landed. Ascension rising +15.", "L4"),
])
def test_vocabulary_and_lore_faults(rules_doc, rubric_judge, slot, text, rule):
    evaluation = evaluator.evaluate(line(slot, text), rules_doc, rubric_judge)
    assert rule in [fault["rule_id"] for fault in evaluation["faults"]], evaluation["reason"]


def test_canon_names_are_not_read_as_generic_terms(rules_doc, rubric_judge):
    """Masking the canon nouns before hunting generics is what stops a proper
    noun from tripping the rule that requires it."""
    evaluation = evaluator.evaluate(
        line("loss_screen", "The evaluation ends here. Crimson Vanguard still stands."),
        rules_doc, rubric_judge)
    assert "V1" not in [fault["rule_id"] for fault in evaluation["faults"]]


def test_phase_two_is_an_allowed_number(rules_doc, rubric_judge):
    """L4 forbids provisional tuning values, not the name of a phase."""
    evaluation = evaluator.evaluate(
        line("phase2_callout", "PHASE 2 - CRIMSON VANGUARD PRESSES HARDER"),
        rules_doc, rubric_judge)
    assert "L4" not in [fault["rule_id"] for fault in evaluation["faults"]]


def test_l3_only_applies_to_the_final_clash_slot(rules_doc, rubric_judge):
    text = "Meter full - clash ready"
    scoped = evaluator.evaluate(line("final_clash_unlock", text), rules_doc, rubric_judge)
    assert "L3" in [fault["rule_id"] for fault in scoped["faults"]]
    other = evaluator.evaluate(line("phase2_callout", text), rules_doc, rubric_judge)
    assert "L3" not in [fault["rule_id"] for fault in other["faults"]]


def test_lore_faults_are_ordered_before_vocabulary_faults(rules_doc, rubric_judge):
    """The refiner works the first fault, so a falsehood must outrank a missing
    name -- copy that states a rule the game does not have is worse than copy
    that names nothing."""
    evaluation = evaluator.evaluate(
        line("meter_feedback_counter", "It fills over time."), rules_doc, rubric_judge)
    ids = [fault["rule_id"] for fault in evaluation["faults"]]
    assert "L1" in ids and "V2" in ids
    assert ids.index("L1") < ids.index("V2")


# ---------------------------------------------------------------------------
# Format and length
# ---------------------------------------------------------------------------

def test_over_length_is_a_fault(rules_doc, rubric_judge):
    spec = rules_doc["slots"]["impact_window_prompt"]
    text = "IMPACT WINDOW - STRIKE NOW RIGHT NOW WITHOUT ANY DELAY AT ALL"
    assert len(text) > spec["max_chars"]
    evaluation = evaluator.evaluate(line("impact_window_prompt", text), rules_doc, rubric_judge)
    assert "F1" in [fault["rule_id"] for fault in evaluation["faults"]]


def test_wrong_shape_is_a_fault(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("impact_window_prompt", "Impact window - strike now."), rules_doc, rubric_judge)
    assert "F2" in [fault["rule_id"] for fault in evaluation["faults"]]


def test_banner_word_count_is_enforced(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("phase2_callout", "PHASE 2 CRIMSON VANGUARD PRESSES VERY MUCH HARDER NOW"),
        rules_doc, rubric_judge)
    assert "F2" in [fault["rule_id"] for fault in evaluation["faults"]]


def test_sentence_count_is_enforced(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("clash_failure_recovery", "The Clash broke. Ascension holds. Go again."),
        rules_doc, rubric_judge)
    assert "F2" in [fault["rule_id"] for fault in evaluation["faults"]]


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

def test_every_fault_names_a_rule_that_exists(rules_doc, rubric_judge, slots):
    known = {rule["id"] for rule in rules_doc["rules"]}
    for slot in slots:
        for text in ("Nice work! it fills over time (+20) and the duel restarts",
                     rules_doc["slots"][slot]["canonical"]):
            evaluation = evaluator.evaluate(line(slot, text), rules_doc, rubric_judge)
            for fault in evaluation["faults"]:
                assert fault["rule_id"] in known


def test_criteria_weights_cover_every_criterion(rules_doc, rubric_judge):
    evaluation = evaluator.evaluate(
        line("loss_screen", "The evaluation ends here. Crimson Vanguard still stands."),
        rules_doc, rubric_judge)
    assert {c["criterion"] for c in evaluation["criteria"]} == \
        set(rules_doc["evaluator"]["criteria_weights"])
