"""Refiner stage -- the smallest rewrite that clears one stated reason.

The rules this stage obeys are carried over from Assignment 06's refiner
because they held up there:

1. One fault per attempt. No batch rewrites, no regeneration from scratch.
2. Every change is recorded as a before/after diff with the rule that caused it.
3. If clearing the fault would require deciding something the GDD leaves open,
   REFUSE.
4. If no rule matches the fault, REFUSE. Silence is not a correction.

What is new is that the edits operate on prose rather than CSV fields, so each
fix is a text transform -- strip the praise, substitute the proper noun, drop
the sentence that contradicts the GDD -- rather than restoring a column.

The two refusals below are not defensive padding. Each names a real decision
sitting with the designer, and one of them is a genuine collision between two
rules in this very contract:

    L3  Correcting a Final Clash unlock line means stating BOTH gate conditions.
        The health half cannot be stated inside the slot's character limit
        without printing the 25% threshold -- and L4 forbids printing it,
        because section 03 marks every such value provisional. Two rules in
        this contract cannot both be satisfied here. That is a design question
        (raise the character budget, or approve the threshold as shipped copy),
        and it is the designer's to answer.

    V2  Restoring a required term that will not fit is the same problem wearing
        a different hat: the fix is a shorter name for the system, and for
        Crimson Vanguard specifically CLAUDE.md records the shorter in-combat
        UI label as an open gap. Inventing one here would settle it by accident.
"""

import argparse
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import generator  # noqa: E402
import textcheck  # noqa: E402
from evaluator import rules_by_id  # noqa: E402

DEFAULT_RULES = os.path.join(HERE, "contracts", "style_rules.json")

REFUSALS = {
    "L3": "stating both Final Clash gate conditions requires printing the 25% health "
          "threshold, which L4 forbids as a provisional value (section 03, page 3). "
          "The character budget or the threshold has to give, and that is the "
          "designer's call",
}


class Refinement(object):
    def __init__(self, line=None, change=None, refused=None):
        self.line = line
        self.change = change
        self.refused = refused

    @property
    def applied(self):
        return self.refused is None

    def as_dict(self):
        return {"applied": self.applied, "change": self.change, "refused": self.refused}


def _change(rule_id, before, after, reason):
    return {"rule_id": rule_id, "before": before, "after": after, "reason": reason}


def _tidy(text):
    """Collapse the whitespace and stray punctuation an excision leaves behind."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[\s,;:.!\-]+", "", text)
    text = re.sub(r"\s+([,;.!?])", r"\1", text)
    return text.strip()


def _recapitalise(text, shape):
    if not text:
        return text
    if shape == "banner":
        return text.upper()
    return text[0].upper() + text[1:]


def _drop_phrase(text, phrase, shape):
    """Remove one phrase and everything that was only there to carry it."""
    pattern = re.compile(r"\b%s\b[\s,;:!.\-]*" % re.escape(phrase), re.IGNORECASE)
    stripped = pattern.sub(" ", text, count=1)
    return _recapitalise(_tidy(stripped), shape)


def _drop_sentence_containing(text, phrase, shape):
    """Remove the whole sentence that carries a claim the GDD denies.

    Excising only the phrase would leave a fragment asserting half a falsehood,
    which is worse than the original: the reader still infers the wrong rule and
    the copy no longer reads as English.
    """
    parts = re.split(r"(?<=[.!?])\s+", text)
    kept = [part for part in parts if phrase.lower() not in part.lower()]
    if not kept or len(kept) == len(parts):
        return None
    return _recapitalise(_tidy(" ".join(kept)), shape)


# ---------------------------------------------------------------------------
# Tone fixes
# ---------------------------------------------------------------------------

def _fix_t1(text, spec, rules_doc, fault):
    praise = textcheck.unnegated_phrase(text, rules_by_id(rules_doc)["T1"]["forbidden_phrases"])
    if not praise:
        return None
    after = _drop_phrase(text, praise, spec["shape"])
    if not after:
        return None
    return after, "removed %r -- the spectacle is the reward, not applause" % praise


def _fix_t2(text, spec, rules_doc, fault):
    after = text
    if "!" in after:
        # A banner carries no terminal punctuation; a sentence needs its period back.
        after = after.replace("!", "." if spec["shape"] == "sentence" else "")
        after = _tidy(after)
        if spec["shape"] == "sentence" and not after.endswith("."):
            after += "."
        return _recapitalise(after, spec["shape"]), \
            "removed the exclamation marks -- the GDD's register is declarative"
    for pattern in rules_by_id(rules_doc)["T2"].get("forbidden_patterns", []):
        cleaned = re.sub(pattern, "", after)
        if cleaned != after:
            return _recapitalise(_tidy(cleaned), spec["shape"]), \
                "removed a decorative symbol the register does not use"
    return None


def _fix_t3(text, spec, rules_doc, fault):
    hedge = textcheck.unnegated_phrase(text, rules_by_id(rules_doc)["T3"]["forbidden_phrases"])
    if not hedge:
        return None
    after = _drop_phrase(text, hedge, spec["shape"])
    if not after:
        return None
    return after, "removed the hedge %r -- combat copy asserts rather than suggests" % hedge


# ---------------------------------------------------------------------------
# Vocabulary and lore fixes
# ---------------------------------------------------------------------------

def _fix_v1(text, spec, rules_doc, fault):
    """Swap the genre default back to this game's proper noun."""
    banned = fault.get("evidence")
    canon = None
    for entry in rules_by_id(rules_doc)["V1"]["substitutions"]:
        if banned and banned.lower() in [b.lower() for b in entry["banned"]]:
            canon = entry["canon"]
            break
    if canon is None:
        return None
    replacement = canon.replace("the ", "")
    pattern = re.compile(r"\b%s\b" % re.escape(banned), re.IGNORECASE)
    match = pattern.search(text)
    if match is None:
        return None
    if match.group(0).isupper():
        replacement = replacement.upper()
    after = _tidy(pattern.sub(replacement, text, count=1))
    return after, "restored the canon term %r in place of %r" % (replacement, banned)


def _fix_v2(text, spec, rules_doc, fault):
    """Restore the slot's canonical line so the named system comes back.

    Refuses when the canonical line will not fit, because the only remaining fix
    is a shorter name for the system -- an open decision, not a rewrite.
    """
    canonical = spec["canonical"]
    if len(canonical) > spec["max_chars"]:
        return None
    if canonical == text:
        return None
    return canonical, ("restored the canonical line so %r is named again"
                       % fault.get("evidence", "the slot's subject"))


def _fix_lore(text, spec, rules_doc, fault):
    """Drop the sentence carrying a claim the GDD denies."""
    hit = fault.get("evidence")
    if not hit:
        return None
    after = _drop_sentence_containing(text, hit, spec["shape"])
    if after is None:
        # The claim is the whole line, so there is nothing to keep. Fall back to
        # the canonical wording, which states the GDD's actual rule.
        after = spec["canonical"]
    if after == text:
        return None
    return after, ("removed the claim %r, which contradicts %s"
                   % (hit, rules_by_id(rules_doc)[fault["rule_id"]]["gdd_source"]))


def _fix_l4(text, spec, rules_doc, fault):
    """Strip the provisional number, keeping the qualitative statement."""
    number = fault.get("evidence")
    if not number:
        return None
    pattern = re.compile(r"[\s(\[]*%s[\s)\]]*" % re.escape(str(number)))
    after = pattern.sub(" ", text, count=1)
    after = _recapitalise(_tidy(after), spec["shape"])
    if spec["shape"] == "sentence" and after and not after.endswith("."):
        after += "."
    if after == text:
        return None
    return after, ("removed %r -- section 03 marks every meter value provisional"
                   % number)


# ---------------------------------------------------------------------------
# Format fixes
# ---------------------------------------------------------------------------

def _fix_f1(text, spec, rules_doc, fault):
    """Restore the canonical wording rather than truncating mid-clause.

    Cutting to the limit would leave copy that fits and says nothing; the
    canonical line fits *and* still carries what the slot exists to say.
    """
    canonical = spec["canonical"]
    if canonical == text or len(canonical) > spec["max_chars"]:
        return None
    return canonical, "restored the canonical wording, which fits the slot's limit"


def _fix_f2(text, spec, rules_doc, fault):
    """Two different faults wear the F2 id, and they need different repairs.

    *Wrong shape* is a re-casing job. *Right shape, too many words or sentences*
    is not -- there is no mechanical way to decide which words to drop without
    deciding what the line no longer says, so it falls back to the canonical
    wording, which is inside every count by construction.
    """
    required = spec["shape"]
    canonical = spec["canonical"]
    over_count = isinstance(fault.get("evidence"), int)

    if required == "banner" and not over_count:
        after = _tidy(text.upper()).rstrip(".")
        if after != text:
            return after, "reshaped into the all-caps HUD banner this slot requires"

    # Going the other way means re-casing prose that was shouted, and casing is
    # where proper nouns live -- restore the canonical line instead of guessing
    # which words were names.
    if canonical == text:
        return None
    if over_count:
        return canonical, ("restored the canonical wording, which fits the %s's "
                           "own count" % required)
    return canonical, "restored the canonical %s this slot requires" % required


FIXES = {
    "T1": _fix_t1,
    "T2": _fix_t2,
    "T3": _fix_t3,
    "V1": _fix_v1,
    "V2": _fix_v2,
    "L1": _fix_lore,
    "L2": _fix_lore,
    "L4": _fix_l4,
    "F1": _fix_f1,
    "F2": _fix_f2,
}


def refine(line, fault, rules_doc):
    """Apply the smallest correction for one fault. Never mutates the input."""
    rule_id = fault["rule_id"]

    if rule_id in REFUSALS:
        return Refinement(refused="cannot safely fix %s: %s" % (rule_id, REFUSALS[rule_id]))

    fix = FIXES.get(rule_id)
    if fix is None:
        return Refinement(refused="no refinement rule exists for %s" % rule_id)

    spec = rules_doc["slots"][line["slot"]]
    candidate = copy.deepcopy(line)
    result = fix(candidate["text"], spec, rules_doc, fault)

    if result is None:
        if rule_id == "V2":
            return Refinement(refused=(
                "cannot safely fix V2: naming %r inside this slot's %d-character "
                "limit needs a shorter in-combat label, which CLAUDE.md records as "
                "an open gap for Crimson Vanguard. Inventing one would settle a "
                "designer's decision by accident"
                % (fault.get("evidence", "the required term"), spec["max_chars"])))
        return Refinement(refused="%s reported a fault the refiner could not locate" % rule_id)

    after, reason = result
    before = candidate["text"]
    candidate["text"] = after
    return Refinement(line=candidate, change=_change(rule_id, before, after, reason))


def main(argv):
    parser = argparse.ArgumentParser(description="Refine one line against one fault.")
    parser.add_argument("slot")
    parser.add_argument("text")
    parser.add_argument("rule_id")
    parser.add_argument("--evidence", default=None)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    refinement = refine({"slot": args.slot, "text": args.text},
                        {"rule_id": args.rule_id, "detail": "", "evidence": args.evidence},
                        rules_doc)
    print(json.dumps(refinement.as_dict(), indent=2))
    return 0 if refinement.applied else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
