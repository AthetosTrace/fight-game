"""The negation-aware matcher. Assignment #04's hardest-won lesson: the
canonical Vanguard row denies the very phrase it names."""

import textcheck


class TestNegation:
    def test_the_canonical_attack_d_wording_is_not_a_violation(self):
        # This is the shipped CSV's own wording. A naive substring check
        # flags it; that is the bug this module exists to prevent.
        text = "Thruster-cued propulsion movement hard-capped by data (never a full-arena snap)"
        assert textcheck.unnegated_phrase(text, ["full-arena snap"]) is None

    def test_an_actual_assertion_is_caught(self):
        text = "Instant close to the player from anywhere via a full-arena snap"
        assert textcheck.unnegated_phrase(text, ["full-arena snap"]) == "full-arena snap"

    def test_no_prefix_denies(self):
        assert textcheck.unnegated_phrase("There is no fifth attack", ["fifth attack"]) is None

    def test_and_is_a_hard_boundary(self):
        # "and" opens a fresh, independently-true statement, so the earlier
        # negation must not launder the later assertion.
        text = "no second arena and the fifth attack lands in phase 2"
        assert textcheck.unnegated_phrase(text, ["fifth attack"]) == "fifth attack"

    def test_or_distributes_negation(self):
        text = "no fifth attack or second arena appears"
        assert textcheck.unnegated_phrase(text, ["second arena"]) is None

    def test_a_negated_first_mention_does_not_hide_a_later_assertion(self):
        text = "never a full-arena snap. Uses a full-arena snap in phase 2"
        assert textcheck.unnegated_phrase(text, ["full-arena snap"]) == "full-arena snap"

    def test_matching_is_case_insensitive(self):
        assert textcheck.unnegated_phrase("A FIFTH ATTACK exists", ["fifth attack"])


class TestPatterns:
    def test_adaptive_language_is_caught(self):
        pattern = r"\badapts?\s+to\s+the\s+player\b"
        assert textcheck.unnegated_pattern("It adapts to the player", [pattern]) == pattern

    def test_denied_adaptive_language_is_not_caught(self):
        pattern = r"\badapts?\s+to\s+the\s+player\b"
        assert textcheck.unnegated_pattern("It never adapts to the player", [pattern]) is None


class TestPositiveChecks:
    def test_contains_any_ignores_negation(self):
        # Positive requirements ask whether a term is present at all.
        assert textcheck.contains_any("no thruster cue", ["thruster"]) is True

    def test_first_present_returns_the_first_match(self):
        assert textcheck.first_present("a punishable recovery", ["punishable", "recovery"]) \
            == "punishable"

    def test_first_present_returns_none_when_absent(self):
        assert textcheck.first_present("nothing here", ["thruster"]) is None
