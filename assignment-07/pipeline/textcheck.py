"""Negation-aware phrase matching plus the prose measurements this pipeline needs.

The negation half is adapted from assignment-06/pipeline/textcheck.py, which
adapted it in turn from the arena pipeline. It earned its keep there and the
problem it solves is worse in prose than it was in CSV fields: player-facing
copy denies things constantly. The canonical failed-Clash line says the duel
does *not* restart, and a naive substring check flags that as claiming the duel
restarts. Any rule built from forbidden phrases has to tell an assertion from a
denial.

The scope is deliberately narrow -- negation is checked against the words
immediately governing the matched phrase, back to the nearest "and"/"but" or the
start of the clause. "and"/"but" are hard boundaries because they open a fresh,
independently-true statement; "or"/"nor" are not, because negation distributes
across them.

The prose measurements below are new. Assignment 06 measured CSV fields, where
"too long" was the only shape question. Copy has a visual grammar -- a HUD
banner and a sentence of prose are different objects -- so this module also
counts words, sentences, and exclamation marks, and decides which shape a line
is wearing.
"""

import re

_NEGATION_RE = re.compile(r"\b(no|not|never|cannot|nothing|without)\b|n't", re.IGNORECASE)
_HARD_BOUNDARY_RE = re.compile(r"\b(?:and|but)\b", re.IGNORECASE)
_CLAUSE_SPLIT_RE = re.compile(r"[,;.!?\n]")

_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")
_WORD_RE = re.compile(r"[^\s]+")


# ---------------------------------------------------------------------------
# Negation-aware matching (adapted from assignment-06)
# ---------------------------------------------------------------------------

def _local_negation_window(clause, phrase_start):
    """The slice of `clause` that governs negation for a phrase at
    `phrase_start`: everything since the nearest preceding 'and'/'but'."""
    boundaries = list(_HARD_BOUNDARY_RE.finditer(clause, 0, phrase_start))
    start = boundaries[-1].end() if boundaries else 0
    return clause[start:phrase_start]


def _occurrences(clause, phrases):
    """Every (start, phrase) occurrence, left to right. Scans every phrase for
    every occurrence -- a negated first mention must never hide a later,
    affirmative repeat."""
    found = []
    for phrase in phrases:
        start = clause.find(phrase)
        while start != -1:
            found.append((start, phrase))
            start = clause.find(phrase, start + 1)
    found.sort(key=lambda item: (item[0], item[1]))
    return found


def unnegated_phrase(text, phrases):
    """Return the first phrase asserted (not denied) in `text`, or None."""
    lowered = text.lower()
    wanted = [p.lower() for p in phrases]
    for clause in re.split(_CLAUSE_SPLIT_RE, lowered):
        for start, phrase in _occurrences(clause, wanted):
            if _NEGATION_RE.search(_local_negation_window(clause, start)):
                continue  # this occurrence is denied, not asserted
            return phrase
    return None


def unnegated_pattern(text, patterns):
    """Same, for regex patterns. Returns the first pattern asserted, or None."""
    lowered = text.lower()
    for clause in re.split(_CLAUSE_SPLIT_RE, lowered):
        for pattern in patterns:
            for match in re.finditer(pattern, clause, re.IGNORECASE):
                if _NEGATION_RE.search(_local_negation_window(clause, match.start())):
                    continue
                return pattern
    return None


def contains_any(text, terms):
    """True if any term appears at all. Used for positive requirements, where
    negation is not the question."""
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def missing_terms(text, terms):
    """Which of `terms` are absent. The positive half of the vocabulary rule."""
    lowered = text.lower()
    return [term for term in terms if term.lower() not in lowered]


def first_present(text, terms):
    lowered = text.lower()
    for term in terms:
        if term.lower() in lowered:
            return term
    return None


def word_boundary_hits(text, terms):
    """Every term present as a whole word, in contract order.

    Substring matching is wrong for the vocabulary rule: "the ring" is a banned
    generic, but "Shattered Ring" is the canon name and contains it. Word
    boundaries alone are not enough either, so callers pair this with a check
    that the canon term is not what produced the match.
    """
    hits = []
    for term in terms:
        pattern = r"\b%s\b" % re.escape(term.lower())
        if re.search(pattern, text.lower()):
            hits.append(term)
    return hits


# ---------------------------------------------------------------------------
# Prose measurements
# ---------------------------------------------------------------------------

def count_exclamations(text):
    return text.count("!")


def count_words(text):
    """Words a reader actually parses.

    Punctuation-only tokens do not count. A HUD banner separator -- the dash in
    "PHASE 2 - CRIMSON VANGUARD PRESSES HARDER" -- is typography, not a word,
    and counting it costs the line a word it never spent.
    """
    return len([token for token in _WORD_RE.findall(text.strip())
                if any(char.isalnum() for char in token)])


def count_sentences(text):
    """Sentences, counted by terminator. A line with no terminator still holds
    one sentence's worth of content, so the floor is 1 for any non-empty text."""
    stripped = text.strip()
    if not stripped:
        return 0
    parts = [p for p in _SENTENCE_SPLIT_RE.split(stripped) if p.strip()]
    return max(1, len(parts))


def is_all_caps(text):
    """True when the text carries no lowercase letters. Digits, punctuation and
    spaces are transparent -- a banner may contain them."""
    return not any(char.islower() for char in text)


def ends_with_period(text):
    return text.strip().endswith(".")


def starts_capitalised(text):
    stripped = text.strip()
    if not stripped:
        return False
    for char in stripped:
        if char.isalpha():
            return char.isupper()
    return True  # no letters at all: nothing to get wrong


def detect_shape(text):
    """Which shape this line is actually wearing: 'banner', 'sentence', or None.

    The contract names the shape a slot *requires*; this reports what was
    written, so the evaluator can say which one it got instead.

    All-caps disqualifies a line from being a sentence, and it is not enough on
    its own to make it a banner. Without that first clause, shouted prose with a
    period ("THE CLASH BROKE. REBUILD ASCENSION.") reads as a well-formed
    sentence and the shape rule passes something no HUD would show.
    """
    stripped = text.strip()
    if not stripped:
        return None
    shouted = is_all_caps(stripped)
    if shouted:
        return "banner" if not ends_with_period(stripped) else None
    if starts_capitalised(stripped) and ends_with_period(stripped):
        return "sentence"
    return None
