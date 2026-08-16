"""Generator stage -- build a canon-faithful line, then drift it on purpose.

A generator that always emitted perfect copy would make the evaluator
ceremonial. So this stage builds the line the GDD supports for a slot, then
applies **seeded drift**: the nine ways player-facing copy for this game
actually goes wrong.

The drift catalogue is not invented. Each operator is a real habit that a
writer -- or a language model asked for "punchy fighting-game copy" -- brings
to the page by default:

    tone_congratulate    congratulate the player, because UI copy usually does
    tone_exclaim         punch it up with exclamation marks
    tone_hedge           soften into a suggestion
    vocab_genericise     reach for the genre word instead of this game's word
    vocab_strip_subject  write around the system instead of naming it
    lore_meter_over_time assume the meter charges, because meters usually do
    lore_clash_restart   assume failure means starting over, because it usually does
    lore_single_gate     assume a full meter is the unlock, because it usually is
    lore_invent_number   print the number, because numbers feel concrete
    format_overlong      write past the limit, because prose wants room
    format_shape_break   swap the HUD banner for a sentence, or the reverse

Drift is seeded, so every defect is reproducible and traceable to the operator
that introduced it. **The evaluator never sees which operators fired.**
"""

import argparse
import copy
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import retrieval  # noqa: E402

DEFAULT_RULES = os.path.join(HERE, "contracts", "style_rules.json")


# ---------------------------------------------------------------------------
# The canonical line
# ---------------------------------------------------------------------------

def slot_spec(rules_doc, slot):
    try:
        return rules_doc["slots"][slot]
    except KeyError:
        raise KeyError("no slot %r in the style contract" % slot)


def base_line(rules_doc, slot):
    """The line this slot's GDD source supports, before any drift."""
    return {"slot": slot, "text": slot_spec(rules_doc, slot)["canonical"]}


def slot_names(rules_doc):
    return sorted(rules_doc["slots"])


def _rule(rules_doc, rule_id):
    for rule in rules_doc["rules"]:
        if rule["id"] == rule_id:
            return rule
    raise KeyError(rule_id)


# ---------------------------------------------------------------------------
# Drift operators
#
# Each takes (text, spec, rules_doc, rng) and returns (new_text, effect) or
# None when it does not apply to this slot's line.
# ---------------------------------------------------------------------------

def _tone_congratulate(text, spec, rules_doc, rng):
    praise = rng.choice(["Nice work! ", "Great job -- ", "Awesome! ", "Well done! "])
    return praise + text, "prepended praise the player did not earn"


def _tone_exclaim(text, spec, rules_doc, rng):
    if text.endswith("."):
        return text[:-1] + "!", "swapped the terminal period for an exclamation mark"
    return text + "!", "appended an exclamation mark"


def _tone_hedge(text, spec, rules_doc, rng):
    hedge = rng.choice(["Maybe ", "You might want to ", "Try to "])
    lowered = text[0].lower() + text[1:] if text else text
    return hedge + lowered, "softened a direct instruction into a suggestion"


def _vocab_genericise(text, spec, rules_doc, rng):
    """Replace a canon proper noun with the genre-default word for it."""
    lowered = text.lower()
    candidates = []
    for entry in _rule(rules_doc, "V1")["substitutions"]:
        canon = entry["canon"]
        bare = canon.replace("the ", "")
        if bare.lower() in lowered:
            candidates.append((bare, entry["banned"]))
    if not candidates:
        return None
    bare, banned = rng.choice(candidates)
    replacement = rng.choice(banned)
    start = lowered.find(bare.lower())
    # Preserve the surrounding case convention: a banner stays shouted.
    swapped = replacement.upper() if text[start:start + len(bare)].isupper() else replacement
    new_text = text[:start] + swapped + text[start + len(bare):]
    return new_text, "replaced the canon term %r with the generic %r" % (bare, replacement)


def _vocab_strip_subject(text, spec, rules_doc, rng):
    """Write around the system instead of naming it."""
    for term in spec["required_terms"]:
        lowered = text.lower()
        start = lowered.find(term.lower())
        if start == -1:
            continue
        replacement = "it" if not text[start:start + len(term)].isupper() else "IT"
        new_text = (text[:start] + replacement + text[start + len(term):])
        return new_text, "replaced the named system %r with a pronoun" % term
    return None


def _lore_meter_over_time(text, spec, rules_doc, rng):
    if "ascension" not in text.lower():
        return None
    claim = rng.choice([
        " It fills over time.",
        " Ascension builds passively.",
        " Wait for your meter to charge.",
    ])
    return text.rstrip() + claim, "claimed the meter fills without active combat (denied by GDD 03 p3)"


def _lore_clash_restart(text, spec, rules_doc, rng):
    if "clash" not in text.lower():
        return None
    claim = rng.choice([
        " The duel restarts.",
        " Start over from the beginning.",
        " The fight resets.",
    ])
    return text.rstrip() + claim, "claimed a failed Clash restarts the duel (denied by GDD 03 p4)"


def _lore_single_gate(text, spec, rules_doc, rng):
    if spec.get("shape") is None or "final clash" not in text.lower():
        return None
    return "METER FULL - CLASH READY", "presented a full meter alone as the Final Clash unlock"


def _lore_invent_number(text, spec, rules_doc, rng):
    number = rng.choice(["+15", "+20", "100", "25%"])
    if text.endswith("."):
        return text[:-1] + " (%s)." % number, "printed a provisional tuning value as shipped copy"
    return text + " %s" % number, "printed a provisional tuning value as shipped copy"


def _format_overlong(text, spec, rules_doc, rng):
    padding = (" Read the telegraph, commit to the counter, and keep the "
               "pressure on Crimson Vanguard through the whole exchange.")
    return text.rstrip() + padding, "padded the line past its readability limit"


def _format_shape_break(text, spec, rules_doc, rng):
    if spec["shape"] == "banner":
        sentence = text.capitalize()
        if not sentence.endswith("."):
            sentence += "."
        return sentence, "wrote a sentence where the HUD requires a banner"
    return text.upper().rstrip("."), "wrote a banner where the slot requires a sentence"


DRIFT_OPERATORS = (
    ("tone_congratulate", _tone_congratulate),
    ("tone_exclaim", _tone_exclaim),
    ("tone_hedge", _tone_hedge),
    ("vocab_genericise", _vocab_genericise),
    ("vocab_strip_subject", _vocab_strip_subject),
    ("lore_meter_over_time", _lore_meter_over_time),
    ("lore_clash_restart", _lore_clash_restart),
    ("lore_single_gate", _lore_single_gate),
    ("lore_invent_number", _lore_invent_number),
    ("format_overlong", _format_overlong),
    ("format_shape_break", _format_shape_break),
)

# How many operators a seed may fire. Weighted toward one or two so runs stay
# readable, but 0 is reachable -- a clean line is a legitimate outcome and the
# evaluator has to be able to pass one.
_DRIFT_COUNTS = (0, 1, 1, 1, 2, 2, 2, 3, 3)


def generate(rules_doc, slot, seed, gdd_dir=None):
    """Build a line for `slot`, drift it under `seed`, and report both."""
    spec = slot_spec(rules_doc, slot)
    line = base_line(rules_doc, slot)
    rng = random.Random(seed)

    order = list(DRIFT_OPERATORS)
    rng.shuffle(order)
    wanted = rng.choice(_DRIFT_COUNTS)

    applied = []
    text = line["text"]
    for name, operator in order:
        if len(applied) >= wanted:
            break
        result = operator(text, spec, rules_doc, rng)
        if result is None:
            continue  # this operator has nothing to bite on in this line
        text, effect = result
        applied.append({"operator": name, "effect": effect})

    line["text"] = text
    return {
        "slot": slot,
        "line": line,
        "drift_applied": applied,
        "retrieval": retrieval.for_slot(rules_doc, slot, gdd_dir=gdd_dir),
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Generate one line of combat copy.")
    parser.add_argument("--slot", required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    print(json.dumps(generate(rules_doc, args.slot, args.seed), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
