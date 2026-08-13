"""Negation-aware phrase matching, shared by the evaluator and the refiner.

Assignment #04 learned this the hard way: the canonical Vanguard row says
"never a full-arena snap", and a naive substring check flags that as asserting
a full-arena snap. The GDD's own wording denies the thing it names, so any
rule built from forbidden phrases must be able to tell an assertion from a
denial.

The scope is deliberately narrow -- negation is checked against the words
immediately governing the matched phrase, back to the nearest "and"/"but" or
the start of the clause. "and"/"but" are hard boundaries because they open a
fresh, independently-true statement; "or"/"nor" are not, because negation
distributes across them ("no fifth attack or second arena" denies both).
"""

import re

_NEGATION_RE = re.compile(r"\b(no|not|never|cannot|nothing|without)\b|n't", re.IGNORECASE)
_HARD_BOUNDARY_RE = re.compile(r"\b(?:and|but)\b", re.IGNORECASE)

# Clause boundaries. Sentence-enders matter as much as commas: "never a
# full-arena snap. Uses a full-arena snap" denies the first mention and
# asserts the second, and a splitter that ignored the period would let the
# denial launder the assertion. The pipe is how callers separate CSV fields
# (see FIELD_SEPARATOR) -- negation in one field must never reach into
# another.
FIELD_SEPARATOR = "\n"
_CLAUSE_SPLIT_RE = re.compile(r"[,;.!?\n|]")


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
    """Return the first phrase asserted (not denied) in `text`, or None.

    Phrases are matched case-insensitively.
    """
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
    """True if any term appears at all. Used for positive requirements
    (a telegraph cue must be present), where negation is not the question."""
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def first_present(text, terms):
    lowered = text.lower()
    for term in terms:
        if term.lower() in lowered:
            return term
    return None
