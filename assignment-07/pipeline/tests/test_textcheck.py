"""textcheck -- negation handling and the prose measurements."""

import pytest

import textcheck


# ---------------------------------------------------------------------------
# Negation
# ---------------------------------------------------------------------------

def test_plain_assertion_is_found():
    assert textcheck.unnegated_phrase("The duel restarts.", ["restarts"]) == "restarts"


def test_denied_phrase_is_not_a_hit():
    """The canonical failed-Clash line denies the very thing it names."""
    text = "A failed Final Clash does not restart the duel."
    assert textcheck.unnegated_phrase(text, ["restart the duel"]) is None


def test_never_denies():
    assert textcheck.unnegated_phrase("It never fills over time.", ["fills over time"]) is None


def test_contraction_denies():
    assert textcheck.unnegated_phrase("It doesn't restart.", ["restart"]) is None


def test_and_opens_a_fresh_clause():
    """'and' is a hard boundary: the denial does not reach past it."""
    text = "It does not restart and the duel restarts"
    assert textcheck.unnegated_phrase(text, ["the duel restarts"]) == "the duel restarts"


def test_sentence_end_splits_clauses():
    text = "It does not restart the duel. The duel restarts."
    assert textcheck.unnegated_phrase(text, ["the duel restarts"]) == "the duel restarts"


def test_negated_first_mention_does_not_hide_a_later_one():
    text = "Not over time, over time"
    assert textcheck.unnegated_phrase(text, ["over time"]) == "over time"


def test_unnegated_pattern_respects_negation():
    assert textcheck.unnegated_pattern("no 25% threshold", [r"\d+%"]) is None
    assert textcheck.unnegated_pattern("25% threshold", [r"\d+%"]) == r"\d+%"


def test_matching_is_case_insensitive():
    assert textcheck.unnegated_phrase("THE DUEL RESTARTS", ["the duel restarts"])


# ---------------------------------------------------------------------------
# Term presence
# ---------------------------------------------------------------------------

def test_missing_terms_reports_only_absent_ones():
    assert textcheck.missing_terms("Ascension rising", ["ascension", "clash"]) == ["clash"]


def test_missing_terms_empty_when_all_present():
    assert textcheck.missing_terms("Final Clash ready", ["final clash"]) == []


def test_word_boundary_hits_does_not_match_inside_a_word():
    assert textcheck.word_boundary_hits("ultimate", ["ult"]) == []
    assert textcheck.word_boundary_hits("use your ult", ["ult"]) == ["ult"]


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("no marks", 0),
    ("one!", 1),
    ("two!!", 2),
])
def test_count_exclamations(text, expected):
    assert textcheck.count_exclamations(text) == expected


def test_count_words_ignores_punctuation_only_tokens():
    """A banner separator is typography, not a word the reader parses."""
    assert textcheck.count_words("PHASE 2 - CRIMSON VANGUARD PRESSES HARDER") == 6


def test_count_words_counts_alphanumeric_tokens():
    assert textcheck.count_words("Counter landed. Ascension rising.") == 4


def test_count_sentences_floors_at_one():
    assert textcheck.count_sentences("No terminator here") == 1
    assert textcheck.count_sentences("") == 0


def test_count_sentences_counts_terminators():
    assert textcheck.count_sentences("One. Two. Three.") == 3


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------

def test_banner_is_all_caps_without_a_period():
    assert textcheck.detect_shape("IMPACT WINDOW - STRIKE NOW") == "banner"


def test_sentence_is_cased_prose_ending_in_a_period():
    assert textcheck.detect_shape("Counter landed. Ascension rising.") == "sentence"


def test_all_caps_with_a_period_is_neither_shape():
    """Shouted prose is not a sentence, and the period disqualifies the banner.

    Without this, every all-caps line ending in a period passed the shape rule
    and reached SUCCESS looking like copy no HUD would ever show.
    """
    assert textcheck.detect_shape("THE CLASH BROKE. REBUILD ASCENSION.") is None


def test_lowercase_opening_is_neither_shape():
    assert textcheck.detect_shape("impact window - strike now") is None


def test_empty_text_has_no_shape():
    assert textcheck.detect_shape("   ") is None


def test_digits_and_punctuation_do_not_break_all_caps():
    assert textcheck.is_all_caps("PHASE 2 - GO")
