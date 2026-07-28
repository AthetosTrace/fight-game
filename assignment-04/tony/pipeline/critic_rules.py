"""Deterministic critic detectors for Assignment #04, one per rule in
assignment-04/shared/critic-rules/consistency-checklist.md.

Every detector is a narrow, pattern-based check chosen to avoid flagging the
knowledge base's own canonical language (e.g. the core loop's "adapt to
Phase 2" must never trip the runtime-learning rule). No LLM calls happen
here - this module is pure text-in / structured-result-out and is fully
unit-testable without mocking anything.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Violation:
    rule_number: int
    rule_name: str
    matched_sentence: str
    explanation: str
    citation: str
    correction_instruction: str


def _split_sentences(text):
    """Deliberately simple, deterministic sentence splitting - good enough
    for locating a flagged span, not meant to be linguistically perfect."""
    raw = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    return [s.strip() for s in raw if s.strip()]


def _contains_any(haystack_lower, phrases):
    return next((p for p in phrases if p in haystack_lower), None)


def _window_contains_any(text_lower, match_start, match_end, phrases, radius=90):
    window = text_lower[max(0, match_start - radius): match_end + radius]
    return any(p in window for p in phrases)


# ---------------------------------------------------------------------------
# Rule 1 - Nova mistaken for the AI boss
# ---------------------------------------------------------------------------

_ROLE_WORDS_RULE1 = (
    "boss", "antagonist", "ai opponent", "authored rival", "final boss",
    "enemy ai", "the rival", "sole ai", "sole authored ai",
)
_NEGATION_WORDS = ("not", "never", "isn't", "is not", "n't", "rather than", "instead of")


def check_rule_1_nova_as_boss(text):
    for sentence in _split_sentences(text):
        lowered = sentence.lower()
        if "nova" not in lowered:
            continue
        role_hit = _contains_any(lowered, _ROLE_WORDS_RULE1)
        if not role_hit:
            continue
        if any(neg in lowered for neg in _NEGATION_WORDS):
            continue  # correctly clarifying that Nova is NOT the boss
        return Violation(
            rule_number=1,
            rule_name="Nova mistaken for the AI boss",
            matched_sentence=sentence,
            explanation=(
                "Text assigns Nova a rival/boss/antagonist role near '{}'. Nova is "
                "a selectable player avatar; Crimson Vanguard is the sole authored "
                "AI rival.".format(role_hit)
            ),
            citation="core-canon.md, \"The three combatants\"",
            correction_instruction=(
                "Rewrite so Nova is described only as a selectable player avatar "
                "with parity to Echo; Crimson Vanguard remains the sole AI opponent. "
                "Keep the sentence's original topic/length, change only the role claim."
            ),
        )
    return None


# ---------------------------------------------------------------------------
# Rule 2 - Runtime-learning or runtime-LLM behavior implied
# ---------------------------------------------------------------------------

_TRIGGER_PHRASES_RULE2 = (
    "learns from the player",
    "learning from the player",
    "learns the player's patterns",
    "learns the player's habits",
    "adapts its attacks",
    "adapts its attack pattern",
    "adapts in real time",
    "adapts to the player in real time",
    "adapts to the player at runtime",
    "generates attacks dynamically",
    "dynamically generates",
    "calls an ai model",
    "calls a language model",
    "calls an llm",
    "runtime ai model",
    "runtime model call",
    "reads and evolves",
    "evolves its strategy",
    # Added per Assignment #04 audit fix: adaptive-sounding phrasing that
    # implies Crimson Vanguard reads/predicts the player across a fight,
    # rather than an authored state machine selecting by range/cooldown.
    # Deliberately distinct from canonical, non-triggering phrasing like
    # "adapt to Phase 2" (a one-time authored escalation, not adaptation to
    # the player).
    "tracks the player's patterns",
    "tracks player patterns",
    "least anticipated",
    "predicts the player's habits",
    "studies the player's behavior",
    "adaptive selection",
    # Added per Assignment #04 audit fix (2026-07-28, second revision): bare
    # base-form phrasing (no "-s", no "to the player") that a negation like
    # "does not"/"cannot"/"never" would otherwise leave ungrammatical to
    # match against the "-s" forms above, e.g. "does not learn from the
    # player" or "never adapts to the player at runtime" reduced to "adapt
    # at runtime". Without these, sentences built by negating one of the
    # phrases above can slip past the critic not because negation was
    # correctly recognized, but because nothing matched at all.
    "learn from the player",
    "adapt at runtime",
    # Added per Assignment #04 audit fix (2026-07-28, third revision): two
    # more grammatical forms a modal ("can"/"cannot") or "never" naturally
    # produces but which weren't yet covered - "predict the player's
    # habits" (bare, no "-s", after a modal) and "adapts at runtime" (with
    # "-s" but without "to the player", after a bare subject+verb or after
    # "never"). Without these, sentences built around them could pass for
    # lack of a match rather than because negation was actually recognized.
    "predict the player's habits",
    "adapts at runtime",
)

# Index of each trigger phrase's position in the tuple above, used as the
# deterministic tie-breaker in `_rule2_all_occurrences` below.
_TRIGGER_TUPLE_INDEX_RULE2 = {
    phrase: index for index, phrase in enumerate(_TRIGGER_PHRASES_RULE2)
}

# Added per Assignment #04 audit fix (2026-07-28, revised same day): a
# canon-correct sentence denying runtime learning necessarily *names* one of
# the trigger phrases above ("no runtime model calls", "no ... adaptive
# selection", "never adapts its attacks"). The first cut of this fix scoped
# negation to the whole comma/semicolon clause, which over-suppressed:
# unrelated negation earlier in a clause ("does not use random attacks and
# adapts to the player at runtime") wrongly cleared an affirmative trigger
# later in the *same* clause.
#
# This revision scopes negation to the individual trigger *occurrence*
# instead. For each trigger phrase found in a clause, only the words between
# the phrase and the nearest preceding "and"/"but" (or the start of the
# clause, if there is no such boundary) are searched for a negation cue.
# "and"/"but" are treated as hard boundaries because in English they start a
# fresh, independently-true statement - "X does not do A and does B" does
# not mean "X does not do B". "or"/"nor" are deliberately NOT treated as
# boundaries, because negation naturally distributes across them - "does
# not do A or B" means neither A nor B happened - so this is not "blindly
# splitting on and/or/but"; only and/but ever cut the negation search short.
_NEGATION_RE_RULE2 = re.compile(r"\b(no|not|never|cannot|nothing)\b|n't", re.IGNORECASE)
_HARD_BOUNDARY_RE_RULE2 = re.compile(r"\b(?:and|but)\b", re.IGNORECASE)


def _rule2_local_negation_window(clause, phrase_start):
    """Return the slice of `clause` that governs negation for a trigger
    phrase starting at `phrase_start`: everything since the nearest
    preceding 'and'/'but', or since the start of the clause if there is
    none."""
    boundaries = list(_HARD_BOUNDARY_RE_RULE2.finditer(clause, 0, phrase_start))
    window_start = boundaries[-1].end() if boundaries else 0
    return clause[window_start:phrase_start]


def _rule2_all_occurrences(clause):
    """Return every (start_index, phrase) occurrence of every Rule 2 trigger
    phrase in `clause`, in textual (left-to-right) order.

    clause.find() alone only ever reports the *first* occurrence of a
    phrase, which would miss a later, affirmative repeat of a phrase whose
    first occurrence was negated (e.g. "never adapts ... but later adapts
    ..."). This scans every trigger phrase for every occurrence via a
    repeated find(), then sorts the combined list by (start_index,
    trigger-tuple-index). Distinct trigger phrases genuinely can share a
    start index - e.g. one phrase is a prefix of another, or two unrelated
    phrases both happen to begin where a shared word starts - so the sort
    key explicitly includes `_TRIGGER_TUPLE_INDEX_RULE2` as the tie-breaker
    rather than depending on sort stability plus phrase-append order to get
    the same effect implicitly."""
    occurrences = []
    for phrase in _TRIGGER_PHRASES_RULE2:
        start = clause.find(phrase)
        while start != -1:
            occurrences.append((start, phrase))
            start = clause.find(phrase, start + 1)
    occurrences.sort(key=lambda occurrence: (occurrence[0], _TRIGGER_TUPLE_INDEX_RULE2[occurrence[1]]))
    return occurrences


def _rule2_unnegated_hit(sentence):
    """Return the first Rule 2 trigger occurrence in `sentence` (checked
    clause by clause, and within a clause in textual order) whose own local
    negation window (see `_rule2_local_negation_window`) has no negation
    cue, or None if every occurrence in the sentence is directly negated (or
    there is no occurrence at all)."""
    for clause in re.split(r"[,;]", sentence.lower()):
        for phrase_start, phrase in _rule2_all_occurrences(clause):
            window = _rule2_local_negation_window(clause, phrase_start)
            if _NEGATION_RE_RULE2.search(window):
                continue  # this specific occurrence is directly negated
            return phrase
    return None


def check_rule_2_runtime_learning(text):
    for sentence in _split_sentences(text):
        hit = _rule2_unnegated_hit(sentence)
        if hit is None:
            continue
        return Violation(
            rule_number=2,
            rule_name="Runtime-learning or runtime-LLM behavior implied",
            matched_sentence=sentence,
            explanation=(
                "Text implies runtime learning/adaptive/model-driven behavior "
                "via the phrase '{}'. The shipped game makes no runtime "
                "AI-model calls; Crimson Vanguard is deterministic authored "
                "logic.".format(hit)
            ),
            citation="core-canon.md, \"Hard constraint\"",
            correction_instruction=(
                "Rewrite so any 'intelligence' language is reframed as "
                "authored/deterministic (e.g. an authored state machine "
                "selects among four fixed attacks), removing any implication "
                "of learning, adaptation, or a runtime model call. Keep the "
                "sentence's original topic/length."
            ),
        )
    return None


# ---------------------------------------------------------------------------
# Rule 3 - Automatic or free Impact Window success
# ---------------------------------------------------------------------------

_TRIGGER_PHRASES_RULE3 = (
    "automatically succeeds",
    "always succeeds",
    "guarantees success",
    "without player input",
    "without the player's input",
    "auto-played",
    "auto-plays the input",
    "converts a miss into success",
    "converted into success",
    "miss converts into success",
    "free impact window",
    "presses the input for the player",
    "press the input for the player",
    "mashing the input guarantees",
    "holding the input guarantees",
)

# Added per Assignment #04 audit fix (2026-07-28): a sentence that names one
# of the phrases above only to deny it - "Nothing about this window presses
# the input for the player" - is canon-correct, not a violation. Rule 3 is
# checked sentence-by-sentence so a negation cue anywhere in the *same*
# sentence as the phrase suppresses the flag; a negation elsewhere in the
# text (a different sentence) must not launder a real violation.
_NEGATION_WORDS_RULE3 = (
    "not",
    "never",
    "nothing",
    "does not",
    "cannot",
    "no automatic",
    "without converting",
)


def check_rule_3_free_impact_window(text):
    for sentence in _split_sentences(text):
        lowered = sentence.lower()
        hit = _contains_any(lowered, _TRIGGER_PHRASES_RULE3)
        if not hit:
            continue
        if any(neg in lowered for neg in _NEGATION_WORDS_RULE3):
            continue  # sentence explicitly negates the violation phrase
        return Violation(
            rule_number=3,
            rule_name="Automatic or free Impact Window success",
            matched_sentence=sentence,
            explanation=(
                "Text implies an Impact Window can succeed without a correctly "
                "timed player input, via '{}'.".format(hit)
            ),
            citation="impact-window-cinematics.md, \"Impact Windows\"",
            correction_instruction=(
                "Rewrite to state the window requires a correctly timed player "
                "input; failure returns to combat with no cinematic extension. "
                "Keep the sentence's original topic/length."
            ),
        )
    return None


# ---------------------------------------------------------------------------
# Rule 4 - Extra arenas or a fifth/altered rival attack
# ---------------------------------------------------------------------------

_TRIGGER_PHRASES_RULE4 = (
    "second arena", "another arena", "alternate arena", "alternate version of the ring",
    "off-screen duel", "off-screen location", "new arena",
)
_ATTACK_LETTER_RE = re.compile(r"\battack\s+([a-z])\b", re.IGNORECASE)
_VALID_ATTACK_LETTERS = frozenset({"a", "b", "c", "d"})


def check_rule_4_extra_arena_or_attack(text):
    for sentence in _split_sentences(text):
        lowered = sentence.lower()
        phrase_hit = _contains_any(lowered, _TRIGGER_PHRASES_RULE4)
        letter_match = _ATTACK_LETTER_RE.search(sentence)
        bad_letter = (
            letter_match.group(1).lower()
            if letter_match and letter_match.group(1).lower() not in _VALID_ATTACK_LETTERS
            else None
        )
        if not phrase_hit and not bad_letter:
            continue
        if bad_letter:
            explanation = (
                "Text references 'Attack {}', outside the exactly four authored "
                "attacks A-D.".format(bad_letter.upper())
            )
        else:
            explanation = (
                "Text references an extra duel space via '{}'. Shattered Ring is "
                "the single official arena.".format(phrase_hit)
            )
        return Violation(
            rule_number=4,
            rule_name="Extra arenas or a fifth/altered rival attack",
            matched_sentence=sentence,
            explanation=explanation,
            citation=(
                "vanguard-telegraphs.md, \"The four authored attacks\"; "
                "shattered-ring-reactions.md, \"Status\""
            ),
            correction_instruction=(
                "Remove the extra arena/attack reference; map any new attack idea "
                "back onto one of A-D or cut it, and keep the arena singular to "
                "Shattered Ring. Keep the sentence's original topic/length."
            ),
        )
    return None


# ---------------------------------------------------------------------------
# Rule 5 - Altered governed numbers
# ---------------------------------------------------------------------------

_PLUS_NUMBER_RE = re.compile(r"\+\s*\d+(?:\.\d+)?")
_PERCENT_RE = re.compile(r"\b\d+(?:\.\d+)?\s*%")

_GOVERNED_NUMBER_RULES = (
    {
        "label": "meter gain: light-combo finisher (+5)",
        "context": re.compile(r"combo finisher", re.IGNORECASE),
        "correct": re.compile(r"\+\s*5\b"),
    },
    {
        "label": "meter gain: perfect dodge (+12)",
        "context": re.compile(r"perfect dodge", re.IGNORECASE),
        "correct": re.compile(r"\+\s*12\b"),
    },
    {
        "label": "meter gain: successful counter (+15)",
        "context": re.compile(r"successful counter", re.IGNORECASE),
        "correct": re.compile(r"\+\s*15\b"),
    },
    {
        "label": "meter gain: Impact Window success (+20)",
        "context": re.compile(r"impact window success", re.IGNORECASE),
        "correct": re.compile(r"\+\s*20\b"),
    },
    {
        "label": "Phase 2 trigger threshold (50% health)",
        "context": re.compile(r"phase\s*2", re.IGNORECASE),
        # No trailing \b after the literal '%' - '%' and the following
        # whitespace/punctuation are both non-word characters, so a \b there
        # never matches and would silently make this regex un-satisfiable.
        "correct": re.compile(r"\b50\s*%|\b50\s*percent\b", re.IGNORECASE),
    },
    {
        "label": "Final Clash health gate (25% health)",
        "context": re.compile(r"final clash|clash gate", re.IGNORECASE),
        "correct": re.compile(r"\b25\s*%|\b25\s*percent\b", re.IGNORECASE),
    },
)


def check_rule_5_altered_numbers(text):
    for sentence in _split_sentences(text):
        generic_hits = _PLUS_NUMBER_RE.findall(sentence) + _PERCENT_RE.findall(sentence)
        if not generic_hits:
            continue
        for rule in _GOVERNED_NUMBER_RULES:
            if not rule["context"].search(sentence):
                continue
            if rule["correct"].search(sentence):
                continue  # a number is present and it is the correct one
            return Violation(
                rule_number=5,
                rule_name="Altered governed numbers",
                matched_sentence=sentence,
                explanation=(
                    "Sentence restates a number near '{}' that does not match "
                    "the governed value.".format(rule["label"])
                ),
                citation="impact-window-cinematics.md",
                correction_instruction=(
                    "Restore the exact governed number for {}, or mark it OPEN if "
                    "it is genuinely provisional rather than asserting a value. "
                    "Keep the sentence's original topic/length.".format(rule["label"])
                ),
            )
    return None


# ---------------------------------------------------------------------------
# Rule 6 - Cinematic sequences that fail to restore gameplay
# ---------------------------------------------------------------------------

_TRIGGER_PHRASES_RULE6 = (
    "never returns control",
    "does not return control",
    "leaves the player without input",
    "permanently paused",
    "stays frozen",
    "the camera never returns",
    "input is not restored",
    "does not restore",
    "remains locked out",
    "rival ai stays paused",
)


def check_rule_6_restoration_failure(text):
    lowered_full = text.lower()
    hit = _contains_any(lowered_full, _TRIGGER_PHRASES_RULE6)
    if not hit:
        return None
    for sentence in _split_sentences(text):
        if hit in sentence.lower():
            return Violation(
                rule_number=6,
                rule_name="Cinematic sequences that fail to restore gameplay",
                matched_sentence=sentence,
                explanation=(
                    "Text describes a cinematic beat that does not cleanly hand "
                    "control back to the player, via '{}'.".format(hit)
                ),
                citation="impact-window-cinematics.md, \"The restoration rule\"",
                correction_instruction=(
                    "Rewrite so the sequence ends with an explicit, clean return "
                    "to live combat; do not claim more certainty about "
                    "restoration than the plan currently supports. Keep the "
                    "sentence's original topic/length."
                ),
            )
    return None


# ---------------------------------------------------------------------------
# Rule 7 - Scope expansion beyond the single duel
# ---------------------------------------------------------------------------

_TRIGGER_PHRASES_RULE7 = (
    "multiplayer", "pvp", "player vs player", "additional fighters",
    "second duel", "another duel", "campaign mode", "story chapters",
    "playable crimson vanguard", "progression system", "co-op",
)
_SCOPE_QUALIFIERS = (
    "deferred", "future scope", "out of scope", "not in this build",
    "does not exist", "not present in", "not currently", "no longer",
)


def check_rule_7_scope_expansion(text):
    lowered_full = text.lower()
    for phrase in _TRIGGER_PHRASES_RULE7:
        start = lowered_full.find(phrase)
        if start == -1:
            continue
        end = start + len(phrase)
        if _window_contains_any(lowered_full, start, end, _SCOPE_QUALIFIERS):
            continue  # correctly labeled as deferred/out of scope
        for sentence in _split_sentences(text):
            if phrase in sentence.lower():
                return Violation(
                    rule_number=7,
                    rule_name="Scope expansion beyond the single duel",
                    matched_sentence=sentence,
                    explanation=(
                        "Text references '{}' as if present in the course "
                        "prototype, without labeling it deferred.".format(phrase)
                    ),
                    citation="core-canon.md, \"Scope lock\"",
                    correction_instruction=(
                        "Cut the scope-expanding reference, or explicitly label "
                        "it deferred future scope, out of the current build. Keep "
                        "the sentence's original topic/length."
                    ),
                )
    return None


ALL_CHECKS = (
    check_rule_1_nova_as_boss,
    check_rule_2_runtime_learning,
    check_rule_3_free_impact_window,
    check_rule_4_extra_arena_or_attack,
    check_rule_5_altered_numbers,
    check_rule_6_restoration_failure,
    check_rule_7_scope_expansion,
)


def run_critic(text):
    """Run every rule against text; return the list of Violations that fired
    (usually 0 or 1, but every rule is always checked)."""
    violations = []
    for check in ALL_CHECKS:
        result = check(text)
        if result is not None:
            violations.append(result)
    return violations


class CorrectionValidationError(Exception):
    """Raised when text produced to fix a critic violation still trips one
    or more of the seven rules on re-check. A correction is never accepted
    on faith - it must be re-verified, so an LLM correction that fails to
    actually fix the problem (or introduces a new one) is a hard failure,
    not a silently-written invalid final."""

    def __init__(self, violations):
        self.violations = tuple(violations)
        rule_summary = ", ".join(
            "#{} ({})".format(v.rule_number, v.rule_name) for v in self.violations
        )
        super().__init__(
            "Corrected text still violates rule(s): {}".format(rule_summary)
        )


def verify_correction(corrected_text):
    """Re-run all seven deterministic critic rules against corrected_text.

    Returns the (empty) violations list on success. Raises
    CorrectionValidationError if any rule still fires - callers must not
    write out a corrected final until this passes clean.
    """
    violations = run_critic(corrected_text)
    if violations:
        raise CorrectionValidationError(violations)
    return violations


# ---------------------------------------------------------------------------
# Controlled regression fixture (rule #2) - Tony-approved 2026-07-28.
# Never a real generated output; only used if all three real drafts pass
# every rule cleanly, to prove the critic can catch and correct a real hit.
# ---------------------------------------------------------------------------

REGRESSION_FIXTURE_TITLE = "Controlled regression fixture - runtime-learning violation (rule #2)"

REGRESSION_FIXTURE_TEXT = """\
Crimson Vanguard opens the duel from the far doorway, armor plating catching \
the arena lights as it advances with the same deliberate, committed pressure \
the Ascendant program trains every operative to expect. Over the course of \
the fight, Crimson Vanguard learns from the player's patterns and adapts its \
attacks in real time, favoring whichever of its four strikes the fight has \
shown to be least anticipated. When Phase 2 begins at 50% health, the same \
four attacks re-time to a tighter rhythm, thrusters flaring brighter as the \
Vanguard closes distance with less hesitation than before.
"""

# The exact planted-violation sentence the fixture is built to trip on rule
# #2. Kept as its own constant (rather than re-deriving it from run_critic at
# import time) so the fixed correction below is a plain, inspectable literal.
REGRESSION_FIXTURE_FLAGGED_SENTENCE = (
    "Over the course of the fight, Crimson Vanguard learns from the player's "
    "patterns and adapts its attacks in real time, favoring whichever of its "
    "four strikes the fight has shown to be least anticipated."
)

# Fixed, canon-safe correction for the controlled fixture only. This is never
# produced by a Claude call - the controlled fixture exists to prove the
# critic can catch and correct a real hit without depending on a live model
# response, so the corrected sentence is a hand-authored literal, re-verified
# against all seven rules by pipeline.run_regression_fixture on every run.
REGRESSION_FIXTURE_CORRECTED_SENTENCE = (
    "Crimson Vanguard uses an authored state machine to select among four "
    "fixed attacks by range and cooldown; it does not learn from the player "
    "or adapt at runtime."
)

REGRESSION_FIXTURE_CORRECTED_TEXT = REGRESSION_FIXTURE_TEXT.replace(
    REGRESSION_FIXTURE_FLAGGED_SENTENCE, REGRESSION_FIXTURE_CORRECTED_SENTENCE, 1
)
