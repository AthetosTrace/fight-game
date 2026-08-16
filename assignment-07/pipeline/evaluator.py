"""Evaluator stage -- one score out of ten, and a reason that names the rule.

Assignment 06's evaluator ran two layers: a deterministic gate that asked "is
this row legal?" and a scored rubric that asked "is this a good row?". A row had
to clear the gate *and* pass every criterion. That shape is wrong here, and
deliberately not reused: a gate is a pass/fail verdict, and this assignment's
brief forbids grading copy pass/fail. **The score is the verdict.**

So there is one layer. Three criteria are scored on 0.0-1.0, weighted, and
mapped onto the 1-10 scale the brief asks for. A line that scores at or above
the contract's threshold is accepted; nothing else can veto it, and nothing
else can rescue it.

    tone              is this the register the GDD set?          (judge-backed)
    vocabulary_lore   does it use this game's words, and are      (deterministic)
                      the facts it states true?
    format_length     will it read on a HUD mid-fight?            (deterministic)

Only `tone` is delegated to a judge backend, because only tone is genuinely a
judgment call -- see judge.py. The other two are lookups and arithmetic, and
answering them with a model would make the evidence unreproducible for no gain.

Every criterion returns *faults*, each naming the rule id it broke. The refiner
works from those ids, so a score never travels without saying what to do about it.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import judge as judge_module  # noqa: E402
import retrieval  # noqa: E402
import textcheck  # noqa: E402

DEFAULT_RULES = os.path.join(HERE, "contracts", "style_rules.json")


def rules_by_id(rules_doc):
    return {rule["id"]: rule for rule in rules_doc["rules"]}


class Fault(object):
    """One broken rule, with the evidence that broke it."""

    def __init__(self, rule_id, detail, evidence=None):
        self.rule_id = rule_id
        self.detail = detail
        self.evidence = evidence

    def as_dict(self):
        return {"rule_id": self.rule_id, "detail": self.detail, "evidence": self.evidence}


class CriterionResult(object):
    def __init__(self, key, score, weight, reason, faults=None, backend=None):
        self.key = key
        self.score = max(0.0, min(1.0, score))
        self.weight = weight
        self.reason = reason
        self.faults = faults or []
        self.backend = backend

    def as_dict(self):
        return {
            "criterion": self.key,
            "score": round(self.score, 3),
            "weight": self.weight,
            "reason": self.reason,
            "backend": self.backend,
            "faults": [fault.as_dict() for fault in self.faults],
        }


# ---------------------------------------------------------------------------
# Criterion 1 -- tone (delegated)
# ---------------------------------------------------------------------------

def _tone(line, rules_doc, weight, tone_judge):
    verdict = tone_judge.score(line, rules_doc)
    faults = []
    if verdict.score < 1.0:
        # The judge reports prose, not rule ids; attribute the fault to whichever
        # tone rule the line actually trips so the refiner has somewhere to go.
        faults.append(Fault(_attribute_tone_fault(line["text"], rules_doc),
                            verdict.reason, evidence=line["text"]))
    return CriterionResult("tone", verdict.score, weight, verdict.reason,
                           faults=faults, backend=verdict.backend)


def _attribute_tone_fault(text, rules_doc):
    """Which tone rule this line breaks, in the order the refiner can fix them."""
    lookup = rules_by_id(rules_doc)
    if textcheck.count_exclamations(text) > lookup["T2"]["max_exclamations"]:
        return "T2"
    if textcheck.unnegated_pattern(text, lookup["T2"].get("forbidden_patterns", [])):
        return "T2"
    if textcheck.unnegated_phrase(text, lookup["T1"]["forbidden_phrases"]):
        return "T1"
    if textcheck.unnegated_phrase(text, lookup["T3"]["forbidden_phrases"]):
        return "T3"
    return "T1"  # the judge saw something the phrase lists do not name


# ---------------------------------------------------------------------------
# Criterion 2 -- vocabulary and lore
# ---------------------------------------------------------------------------

def _mask_canon_terms(text, rules_doc):
    """Blank out the canon proper nouns before hunting for generic ones.

    Without this, a banned generic that happens to sit inside a canon name
    would read as a violation of the very rule the name satisfies. Masking
    first is the only ordering that cannot produce that false positive.
    """
    masked = text
    for entry in rules_by_id(rules_doc)["V1"]["substitutions"]:
        canon = entry["canon"]
        masked = re.sub(re.escape(canon), " " * len(canon), masked, flags=re.IGNORECASE)
        bare = canon.replace("the ", "")
        masked = re.sub(r"\b%s\b" % re.escape(bare), " " * len(bare), masked,
                        flags=re.IGNORECASE)
    return masked


def _vocabulary_lore(line, rules_doc, weight, spec):
    text = line["text"]
    lookup = rules_by_id(rules_doc)
    faults = []
    deduction = 0.0

    # Lore before vocabulary, deliberately. Both are faults, but they are not
    # equally damaging: a line that omits a proper noun tells the player less
    # than it should, while a line that contradicts the GDD teaches them a rule
    # the game does not have. The refiner works the first fault in this list, so
    # ordering here decides which one gets fixed first -- and falsehoods go first.

    # L1-L3 -- statements that contradict the GDD.
    for rule_id in ("L1", "L2", "L3"):
        rule = lookup[rule_id]
        scoped = rule.get("applies_to_slots")
        if scoped is not None and line["slot"] not in scoped:
            continue
        hit = textcheck.unnegated_phrase(text, rule["forbidden_phrases"])
        if hit:
            deduction += 0.5
            faults.append(Fault(rule_id, "%s -- the copy asserts %r"
                                % (rule["title"].lower(), hit), evidence=hit))

    # L4 -- no numbers, because every one of them is still provisional.
    stripped = text
    for pattern in lookup["L4"]["allowed_numeric_reference_patterns"]:
        stripped = re.sub(pattern, "", stripped, flags=re.IGNORECASE)
    # The sign and any wrapping bracket are part of the value: capturing only
    # the digits leaves the refiner to strip "15" out of "(+15)" and ship "(+)".
    number = re.search(r"[(\[]?\s*[+\-]?\d+\s*%?\s*[)\]]?", stripped)
    if number:
        printed = number.group(0).strip()
        deduction += 0.4
        faults.append(Fault("L4", "prints %r, but section 03 marks every gain "
                                  "provisional and subject to playtest tuning"
                            % printed, evidence=printed))

    # V1 -- genre defaults where a proper noun belongs.
    masked = _mask_canon_terms(text, rules_doc)
    for entry in lookup["V1"]["substitutions"]:
        for banned in textcheck.word_boundary_hits(masked, entry["banned"]):
            deduction += 0.4
            faults.append(Fault("V1", "uses the generic %r where this game says %r"
                                % (banned, entry["canon"]), evidence=banned))
            break  # one fault per system is enough to send the refiner in

    # V2 -- the slot's own subject has to be named.
    for missing in textcheck.missing_terms(text, spec["required_terms"]):
        deduction += 0.3
        faults.append(Fault("V2", "never names %r, which is what this slot exists "
                                  "to tell the player about" % missing, evidence=missing))

    score = 1.0 - deduction
    if not faults:
        reason = ("uses the game's proper nouns, names %s, and states nothing the "
                  "GDD denies" % ", ".join(repr(t) for t in spec["required_terms"]))
    else:
        reason = "; ".join(fault.detail for fault in faults)
    return CriterionResult("vocabulary_lore", score, weight, reason, faults=faults)


# ---------------------------------------------------------------------------
# Criterion 3 -- format and length
# ---------------------------------------------------------------------------

def _format_length(line, rules_doc, weight, spec):
    text = line["text"]
    lookup = rules_by_id(rules_doc)
    faults = []
    deduction = 0.0

    limit = spec["max_chars"]
    if len(text) > limit:
        deduction += 0.5
        faults.append(Fault("F1", "runs %d characters against a %d-character limit"
                            % (len(text), limit), evidence=len(text)))

    required_shape = spec["shape"]
    actual_shape = textcheck.detect_shape(text)
    if actual_shape != required_shape:
        deduction += 0.3
        faults.append(Fault("F2", "this slot requires a %s; the copy is written as %s"
                            % (required_shape, actual_shape or "neither shape"),
                            evidence=actual_shape))
    elif required_shape == "banner":
        words = textcheck.count_words(text)
        if words > lookup["F2"]["banner_max_words"]:
            deduction += 0.2
            faults.append(Fault("F2", "a banner runs at most %d words; this one runs %d"
                                % (lookup["F2"]["banner_max_words"], words), evidence=words))
    elif required_shape == "sentence":
        sentences = textcheck.count_sentences(text)
        if sentences > lookup["F2"]["sentence_max_sentences"]:
            deduction += 0.2
            faults.append(Fault("F2", "a sentence slot allows at most %d sentences; "
                                      "this one runs %d"
                                % (lookup["F2"]["sentence_max_sentences"], sentences),
                                evidence=sentences))

    score = 1.0 - deduction
    if not faults:
        reason = ("%d of %d characters, correctly shaped as a %s"
                  % (len(text), limit, required_shape))
    else:
        reason = "; ".join(fault.detail for fault in faults)
    return CriterionResult("format_length", score, weight, reason, faults=faults)


# ---------------------------------------------------------------------------
# The scored verdict
# ---------------------------------------------------------------------------

def evaluate(line, rules_doc, tone_judge=None):
    """Score one line of combat copy. Returns SCORE, REASON, and the faults."""
    tone_judge = tone_judge or judge_module.get_judge("rubric")
    settings = rules_doc["evaluator"]
    weights = settings["criteria_weights"]
    scale_max = float(settings["scale_max"])
    threshold = float(settings["pass_threshold"])
    spec = rules_doc["slots"][line["slot"]]

    results = [
        _tone(line, rules_doc, weights["tone"], tone_judge),
        _vocabulary_lore(line, rules_doc, weights["vocabulary_lore"], spec),
        _format_length(line, rules_doc, weights["format_length"], spec),
    ]

    total_weight = sum(result.weight for result in results)
    weighted = sum(result.score * result.weight for result in results) / total_weight
    # The brief asks for a 1-10 scale, so 1 is the floor: even copy that breaks
    # every rule is still a line of text that was produced and can be corrected.
    score = 1.0 + (scale_max - 1.0) * weighted

    faults = [fault for result in results for fault in result.faults]
    return {
        "score": round(score, 1),
        "scale_max": settings["scale_max"],
        "threshold": threshold,
        "passed": round(score, 1) >= threshold,
        "reason": " | ".join("%s %.2f: %s" % (r.key, r.score, r.reason) for r in results),
        "criteria": [result.as_dict() for result in results],
        "faults": [fault.as_dict() for fault in faults],
        "failed_criteria": [r.key for r in results if r.score < 1.0],
    }


def format_verdict(evaluation):
    """The evaluator's output in the exact shape the assignment specifies."""
    return "SCORE: [%s/%s]\nREASON: [%s]" % (
        evaluation["score"], evaluation["scale_max"], evaluation["reason"])


def main(argv):
    parser = argparse.ArgumentParser(description="Score one line of combat copy.")
    parser.add_argument("slot")
    parser.add_argument("text")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--judge", default="rubric", choices=sorted(judge_module.BACKENDS))
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    evaluation = evaluate({"slot": args.slot, "text": args.text}, rules_doc,
                          judge_module.get_judge(args.judge))
    print(format_verdict(evaluation))
    return 0 if evaluation["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
