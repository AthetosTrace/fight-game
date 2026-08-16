"""generator -- canonical lines, and drift that is reproducible."""

import pytest

import evaluator
import generator


def test_every_slot_has_a_canonical_line(rules_doc, slots):
    for slot in slots:
        line = generator.base_line(rules_doc, slot)
        assert line["slot"] == slot
        assert line["text"].strip()


def test_every_canonical_line_scores_a_clean_ten(rules_doc, slots, rubric_judge):
    """The contract's own examples must pass the contract.

    This caught a real defect: `phase2_callout`'s canonical banner was being
    counted as seven words because the dash separator counted as one, so the
    slot's own reference line failed the rule it was written to illustrate.
    """
    for slot in slots:
        evaluation = evaluator.evaluate(generator.base_line(rules_doc, slot),
                                        rules_doc, rubric_judge)
        assert evaluation["score"] == 10.0, (slot, evaluation["reason"])
        assert evaluation["faults"] == [], (slot, evaluation["faults"])


def test_every_canonical_line_fits_its_own_limit(rules_doc, slots):
    for slot in slots:
        spec = rules_doc["slots"][slot]
        assert len(spec["canonical"]) <= spec["max_chars"], slot


def test_every_canonical_line_names_its_required_terms(rules_doc, slots):
    for slot in slots:
        spec = rules_doc["slots"][slot]
        lowered = spec["canonical"].lower()
        for term in spec["required_terms"]:
            assert term.lower() in lowered, (slot, term)


def test_generation_is_deterministic(rules_doc):
    first = generator.generate(rules_doc, "loss_screen", 7)
    second = generator.generate(rules_doc, "loss_screen", 7)
    assert first["line"] == second["line"]
    assert first["drift_applied"] == second["drift_applied"]


def test_different_seeds_reach_different_lines(rules_doc):
    texts = {generator.generate(rules_doc, "loss_screen", seed)["line"]["text"]
             for seed in range(1, 40)}
    assert len(texts) > 1


def test_drift_is_reported_with_an_operator_and_an_effect(rules_doc):
    for seed in range(1, 30):
        result = generator.generate(rules_doc, "clash_failure_recovery", seed)
        for drift in result["drift_applied"]:
            assert drift["operator"] in dict(generator.DRIFT_OPERATORS)
            assert drift["effect"].strip()


def test_some_seed_produces_a_clean_line(rules_doc):
    """A generator that always drifted would make a passing score unreachable,
    and the evaluator would never be shown to accept anything."""
    assert any(not generator.generate(rules_doc, "clash_failure_recovery", seed)["drift_applied"]
               for seed in range(1, 40))


def test_most_seeds_produce_drift(rules_doc):
    """The mirror of the previous test: a generator that never drifted would
    make the evaluator ceremonial."""
    drifted = sum(1 for seed in range(1, 40)
                  if generator.generate(rules_doc, "clash_failure_recovery", seed)["drift_applied"])
    assert drifted > 20


def test_drift_actually_changes_the_text(rules_doc):
    for seed in range(1, 40):
        result = generator.generate(rules_doc, "impact_window_prompt", seed)
        if result["drift_applied"]:
            assert result["line"]["text"] != rules_doc["slots"]["impact_window_prompt"]["canonical"]


def test_generation_carries_verified_retrieval(rules_doc, slots):
    for slot in slots:
        result = generator.generate(rules_doc, slot, 1)
        assert result["retrieval"]["slot_citation"]["verified"]


def test_unknown_slot_raises(rules_doc):
    with pytest.raises(KeyError):
        generator.base_line(rules_doc, "no_such_slot")


def test_slot_names_are_sorted(rules_doc):
    assert generator.slot_names(rules_doc) == sorted(rules_doc["slots"])
