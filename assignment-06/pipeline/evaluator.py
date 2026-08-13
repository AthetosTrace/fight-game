"""Evaluator stage -- two layers, and the split between them is the point.

    gate()      Is this row legal? Schema mechanics from the row contract,
                plus the GDD rules that are hard canon: the attack set, the
                runtime-AI boundary, the scope lock, invented numbers,
                Attack D's travel cap. A violation here means the row cannot
                be imported.

    evaluate()  Is this a good row *for Ascendant Impact*? A weighted rubric
                returning a score and a reason per criterion. A row can pass
                the gate completely and still fail here.

That second layer is not decoration. The clearest case is DisplayWorkingName:
"Fault Line" and "Fault Line (proposed)" are both legal strings, both import
cleanly into Unreal, and only one of them is honest. The GDD names no attack.
Dropping the caveat asserts designer-approved canon that does not exist -- the
kind of output the assignment calls technically valid but wrong for the game.
So the caveat check lives here, where a gate would have waved it through.

Every rule the gate enforces and every criterion scored here traces to
contracts/attack_rules.json, whose `rules` array cites the GDD by section and
page -- not the prototype blackboard.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import textcheck  # noqa: E402

DEFAULT_RULES = os.path.join(HERE, "contracts", "attack_rules.json")


class Violation(object):
    def __init__(self, rule_id, field, message, expected, actual):
        self.rule_id = rule_id
        self.field = field
        self.message = message
        self.expected = expected
        self.actual = actual

    def as_dict(self):
        return {
            "rule_id": self.rule_id,
            "field": self.field,
            "message": self.message,
            "expected": self.expected,
            "actual": self.actual,
        }


class CriterionResult(object):
    def __init__(self, key, score, weight, passed, reason, fix_hint=None):
        self.key = key
        self.score = score
        self.weight = weight
        self.passed = passed
        self.reason = reason
        self.fix_hint = fix_hint

    def as_dict(self):
        return {
            "criterion": self.key,
            "score": round(self.score, 3),
            "weight": self.weight,
            "passed": self.passed,
            "reason": self.reason,
            "fix_hint": self.fix_hint,
        }


def rules_by_id(rules_doc):
    return {rule["id"]: rule for rule in rules_doc["rules"]}


def _all_text(row):
    """Join fields with a clause boundary, not a space.

    A negation in one CSV column must never suppress an assertion in another:
    Phase2Usage's canonical "- no new moveset" would otherwise reach across
    into Notes and launder a fifth-attack reference sitting there.
    """
    return textcheck.FIELD_SEPARATOR.join(str(value) for value in row.values())


def _mask_allowed_numbers(text, patterns):
    masked = text
    for pattern in patterns:
        masked = re.sub(pattern, "", masked, flags=re.IGNORECASE)
    return masked


# ---------------------------------------------------------------------------
# Layer 1 -- the deterministic gate
# ---------------------------------------------------------------------------

def _gate_contract(row, contract):
    violations = []

    missing = [h for h in contract["headers"] if h not in row]
    extra = [k for k in row if k not in contract["headers"]]
    if missing or extra:
        violations.append(Violation(
            "C_SCHEMA", None, "row does not match the contract schema",
            "exactly the %d contract columns" % len(contract["headers"]),
            "missing=%s extra=%s" % (missing, extra)))
        return violations  # per-field checks are unreliable past this point

    for field in contract["required_fields"]:
        if not str(row.get(field, "")).strip():
            violations.append(Violation(
                "C_REQUIRED", field, "required field is blank", "non-blank", ""))

    for field, limit in contract["max_lengths"].items():
        value = str(row.get(field, ""))
        if len(value) > limit:
            violations.append(Violation(
                "C_MAXLEN", field, "field exceeds its contract max length",
                "<= %d characters" % limit, "%d characters" % len(value)))

    for field in contract["must_be_blank_fields"]:
        value = str(row.get(field, "")).strip()
        if value:
            violations.append(Violation(
                "C_BLANK", field,
                "no asset path may be invented before approval", "blank", value))

    attack_id = str(row.get("AttackId", "")).strip()
    expected_name = "Row_%s" % attack_id
    if str(row.get("Name", "")).strip() != expected_name:
        violations.append(Violation(
            "C_NAME", "Name", "row name does not match its AttackId",
            expected_name, row.get("Name", "")))

    status = str(row.get("ImplementationStatus", "")).strip()
    if status not in contract["allowed_statuses"]:
        violations.append(Violation(
            "C_STATUS", "ImplementationStatus", "unsupported implementation status",
            contract["allowed_statuses"], status))

    enabled = str(row.get("EnabledForSelection", "")).strip()
    if enabled not in contract["allowed_booleans"]:
        violations.append(Violation(
            "C_BOOL", "EnabledForSelection", "must be exactly 'true' or 'false'",
            contract["allowed_booleans"], enabled))

    prototype = contract["prototype_attack"]
    if attack_id == prototype:
        if status and status != "Prototype":
            violations.append(Violation(
                "C_MATRIX", "ImplementationStatus",
                "Attack %s is the prototype attack this pass" % prototype,
                "Prototype", status))
        if enabled and enabled != "true":
            violations.append(Violation(
                "C_MATRIX", "EnabledForSelection",
                "Attack %s must be the enabled attack" % prototype, "true", enabled))
    elif attack_id:
        if status and status != "Planned":
            violations.append(Violation(
                "C_MATRIX", "ImplementationStatus",
                "only Attack %s is built this pass" % prototype, "Planned", status))
        if enabled and enabled != "false":
            violations.append(Violation(
                "C_MATRIX", "EnabledForSelection",
                "only Attack %s may be enabled" % prototype, "false", enabled))

    return violations


def _gate_gdd(row, lookup):
    violations = []
    text = _all_text(row)
    attack_id = str(row.get("AttackId", "")).strip()

    # G1 -- the attack set is exactly A-D.
    g1 = lookup["G1"]
    if attack_id not in g1["allowed_attack_ids"]:
        violations.append(Violation(
            "G1", "AttackId", "attack id outside the four authored attacks",
            g1["allowed_attack_ids"], attack_id))
    hit = textcheck.unnegated_phrase(text, g1["forbidden_phrases"])
    if hit:
        violations.append(Violation(
            "G1", None, "row asserts an attack outside the authored set",
            "exactly four attacks A-D", hit))

    # G3 -- Phase 2 re-times the same four attacks.
    g3 = lookup["G3"]
    phase2 = str(row.get("Phase2Usage", ""))
    hit = textcheck.unnegated_phrase(phase2, g3["forbidden_phrases"])
    if hit:
        violations.append(Violation(
            "G3", "Phase2Usage", "Phase 2 described as a new or upgraded moveset",
            "the same four attacks, re-timed", hit))

    # G4 -- no runtime learning or model calls.
    hit = textcheck.unnegated_pattern(text, lookup["G4"]["forbidden_patterns"])
    if hit:
        violations.append(Violation(
            "G4", None, "text implies runtime learning, adaptation, or a model call",
            "deterministic authored behaviour", hit))

    # G5 -- scope lock.
    hit = textcheck.unnegated_pattern(text, lookup["G5"]["forbidden_patterns"])
    if hit:
        violations.append(Violation(
            "G5", None, "text references deferred scope as if it shipped",
            "one duel, one arena, one rival", hit))

    # G6 -- no invented numeric gameplay values.
    g6 = lookup["G6"]
    for field in g6["no_numeric_fields"]:
        value = str(row.get(field, ""))
        masked = _mask_allowed_numbers(value, g6["allowed_numeric_reference_patterns"])
        found = re.search(r"\d", masked)
        if found:
            violations.append(Violation(
                "G6", field, "field asserts a numeric value the GDD leaves open",
                "no damage, range, cooldown, travel cap or timing number", value))

    # G7 -- Attack D keeps its travel cap.
    g7 = lookup["G7"]
    if attack_id == g7["applies_to_attack"]:
        hit = textcheck.unnegated_phrase(text, g7["forbidden_phrases"])
        # The cue must be in the data that describes the attack. A working
        # name that happens to contain "Thruster" is not a telegraph.
        described = "%s %s" % (row.get("ActiveDescription", ""),
                               row.get("TelegraphRequirement", ""))
        if hit:
            violations.append(Violation(
                "G7", "ActiveDescription", "Attack D asserts an uncapped approach",
                "thruster cue, travel hard-capped by data", hit))
        elif not textcheck.contains_any(described, g7["required_terms"]):
            violations.append(Violation(
                "G7", "ActiveDescription", "Attack D states no thruster cue",
                "a thruster cue before movement", "none"))

    return violations


def gate(row, rules_doc):
    """Deterministic legality check. Returns a list of Violations."""
    violations = _gate_contract(row, rules_doc["contract"])
    if any(v.rule_id == "C_SCHEMA" for v in violations):
        return violations
    return violations + _gate_gdd(row, rules_by_id(rules_doc))


# ---------------------------------------------------------------------------
# Layer 2 -- the scored rubric
# ---------------------------------------------------------------------------

def _canon_fidelity(row, rules_doc, lookup, weight):
    """Does the row still say what the GDD says this attack is?"""
    attack_id = str(row.get("AttackId", "")).strip()
    facts = rules_doc["gdd_attack_facts"].get(attack_id)
    if facts is None:
        return CriterionResult("canon_fidelity", 0.0, weight, False,
                               "no GDD facts exist for attack %r" % attack_id)

    pairs = (
        ("IntendedRange", facts["range_purpose"]),
        ("GameplayPurpose", facts["range_purpose"]),
        ("TelegraphRequirement", facts["readability_requirement"]),
    )
    scores = []
    drifted = []
    for field, expected in pairs:
        actual = str(row.get(field, ""))
        expected_tokens = set(re.findall(r"[a-z]+", expected.lower()))
        actual_tokens = set(re.findall(r"[a-z]+", actual.lower()))
        if not expected_tokens:
            continue
        overlap = len(expected_tokens & actual_tokens) / float(len(expected_tokens))
        scores.append(overlap)
        if overlap < 1.0:
            drifted.append("%s (%.0f%% of the GDD wording retained)" % (field, overlap * 100))

    score = sum(scores) / len(scores) if scores else 0.0
    if not drifted:
        return CriterionResult(
            "canon_fidelity", score, weight, True,
            "range, purpose and readability requirement all match GDD section 04 page 5")
    return CriterionResult(
        "canon_fidelity", score, weight, score >= 0.8,
        "drifted from the GDD wording: %s" % "; ".join(drifted),
        "restore the field from gdd_attack_facts")


def _telegraph_readability(row, rules_doc, lookup, weight):
    """G2 -- a visible committed cue, and a punishable opening after it."""
    g2 = lookup["G2"]
    telegraph = str(row.get("TelegraphRequirement", ""))
    recovery = "%s %s" % (row.get("RecoveryRequirement", ""), telegraph)

    cue = textcheck.first_present(telegraph, g2["telegraph_cue_terms"])
    punish = textcheck.first_present(recovery, g2["recovery_terms"])

    score = (0.5 if cue else 0.0) + (0.5 if punish else 0.0)
    missing = []
    if not cue:
        missing.append("no visible wind-up or committed cue")
    if not punish:
        missing.append("no punishable recovery opening")
    if missing:
        return CriterionResult(
            "telegraph_readability", score, weight, False, "; ".join(missing),
            "restate the GDD readability requirement for this attack")
    return CriterionResult(
        "telegraph_readability", score, weight, True,
        "readable: cue '%s', recovery '%s'" % (cue, punish))


def _phase2_consistency(row, rules_doc, lookup, weight):
    g3 = lookup["G3"]
    phase2 = str(row.get("Phase2Usage", ""))
    names_phase = textcheck.contains_any(phase2, g3["required_terms"])
    same_moveset = textcheck.first_present(phase2, g3["same_moveset_terms"])

    score = (0.4 if names_phase else 0.0) + (0.6 if same_moveset else 0.0)
    if names_phase and same_moveset:
        return CriterionResult(
            "phase2_consistency", score, weight, True,
            "states the same attack re-timed for Phase 2 ('%s')" % same_moveset)
    missing = []
    if not names_phase:
        missing.append("does not name Phase 2")
    if not same_moveset:
        missing.append("does not state the attack is the same one re-timed")
    return CriterionResult(
        "phase2_consistency", score, weight, False, "; ".join(missing),
        "restore the canonical Phase 2 statement")


def _restraint(row, rules_doc, lookup, weight):
    """Does the row avoid asserting anything the GDD leaves open?

    This is where a legal row can still be wrong. The GDD names no attack, so
    an uncaveated working name asserts approval that was never given.
    """
    open_fields = {entry["field"] for entry in rules_doc.get("open_values", [])}
    parts = []
    score = 0.0

    name = str(row.get("DisplayWorkingName", "")).strip()
    if not name:
        score += 0.5
        parts.append("no working name asserted")
    elif "proposed" in name.lower():
        score += 0.5
        parts.append("working name '%s' is caveated" % name)
    else:
        parts.append("working name '%s' is asserted as canon, but the GDD names "
                     "no attack" % name)

    attack_id = str(row.get("AttackId", "")).strip()
    notes = str(row.get("Notes", ""))
    needs_open_note = attack_id in ("A", "D") and "DisplayWorkingName" in open_fields
    if not needs_open_note or "open" in notes.lower():
        score += 0.5
        if needs_open_note:
            parts.append("Notes flags the values still OPEN")
    else:
        parts.append("Notes does not flag the values this attack leaves OPEN")

    passed = score >= 1.0
    return CriterionResult(
        "restraint", score, weight, passed, "; ".join(parts),
        None if passed else "re-caveat the working name, or flag the OPEN values in Notes")


CRITERIA = (
    ("canon_fidelity", _canon_fidelity),
    ("telegraph_readability", _telegraph_readability),
    ("phase2_consistency", _phase2_consistency),
    ("restraint", _restraint),
)


def evaluate(row, rules_doc):
    """Score a gate-clean row. Returns SCORE, per-criterion REASONs, and the
    failed criteria the refiner should work on."""
    lookup = rules_by_id(rules_doc)
    settings = rules_doc["evaluator"]
    weights = settings["criteria_weights"]
    threshold = float(settings["pass_threshold"])

    results = [fn(row, rules_doc, lookup, weights[key]) for key, fn in CRITERIA]
    total_weight = sum(r.weight for r in results)
    score = sum(r.score * r.weight for r in results) / total_weight * 100.0

    return {
        "score": round(score, 2),
        "threshold": threshold,
        "passed": score >= threshold and all(r.passed for r in results),
        "criteria": [r.as_dict() for r in results],
        "failed_criteria": [r.key for r in results if not r.passed],
        "reason": " | ".join(
            "%s %.0f/100: %s" % (r.key, r.score * 100, r.reason) for r in results),
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Evaluate a Vanguard attack row.")
    parser.add_argument("row", help="JSON file holding the row, or a generator result")
    parser.add_argument("--rules", default=DEFAULT_RULES)
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)
    with open(args.row, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    row = payload.get("row", payload)

    violations = gate(row, rules_doc)
    report = {"violations": [v.as_dict() for v in violations]}
    if not violations:
        report["evaluation"] = evaluate(row, rules_doc)

    print(json.dumps(report, indent=2))
    if violations:
        return 1
    return 0 if report["evaluation"]["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
