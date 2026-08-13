"""Generator stage -- produce one candidate Vanguard attack row.

Every field starts life grounded in a retrieved, GDD-cited knowledge-base
chunk (see retrieval.py). The base row is therefore canon-faithful by
construction.

It then applies *drift*. This is the honest part of the design. A generator
that always emitted a perfect row would make the evaluator ceremonial -- the
loop would never have anything to catch, and the assignment's whole premise is
that some outputs are broken and some are technically valid but wrong for the
game. Real generators drift: they over-specify a number nobody approved, they
upgrade "re-timed" into "upgraded", they drop a "(proposed)" caveat, they
reach for adaptive-AI language because that is how enemy AI is usually
described.

Drift is seeded, so every run is reproducible and every defect is traceable to
the operator that introduced it. The evaluator downstream does not know which
operators fired.
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

DEFAULT_RULES = os.path.join(HERE, "contracts", "attack_rules.json")

DRIFT_RATE = 0.25

# The knowledge-base files a Vanguard attack row may be built from, and the
# chunks pinned regardless of lexical score. Both come from Assignment #04's
# retrieval-manifest.md, Output 1 ("Crimson Vanguard Telegraph and Readability
# Pack") -- the manifest already scoped this exact content type.
ELIGIBLE_FILES = ("vanguard-telegraphs.md", "core-canon.md")
REQUIRED_CHUNKS = (
    ("core-canon.md", "Hard constraint"),
    ("core-canon.md", "Scope lock (do not exceed in generated content)"),
)

RETRIEVAL_QUERY = (
    "Crimson Vanguard attack {attack_id} range purpose readability requirement "
    "telegraph wind-up recovery tracking phase 2 authored deterministic")

# Per-attack active/recovery prose. Qualitative only -- the GDD gives no
# numbers here and this stage must not supply any.
ACTIVE_DESCRIPTIONS = {
    "A": "Authored gauntlet-force hitbox trace during the committed active window; no propulsion",
    "B": "Multi-beat authored forward-pressure sequence; each beat individually dodgeable",
    "C": "Wide authored active-range hitbox trace communicating armored reach",
    "D": "Thruster-cued propulsion movement hard-capped by data (never a full-arena snap)",
}

RECOVERY_REQUIREMENTS = {
    "A": "Deliberate exposed opening after the committed strike",
    "B": "Deliberate exposed opening after the committed sequence completes",
    "C": "Deliberate exposed opening after the committed strike",
    "D": "Deliberate exposed opening after the propulsion approach completes",
}

TRACKING_RULES = {
    "A": "",
    "B": "Body and tracking lock at a fixed point once the active window begins",
    "C": "Body direction locks before the active window so the reach direction is unambiguous",
    "D": "",
}

# Working names carried from Assignment #04's telegraph pack. Proposed, never
# canon -- the caveat is part of the value, not decoration.
WORKING_NAMES = {
    "A": "Fault Line (proposed)",
    "B": "Advance Line (proposed)",
    "C": "Bulwark Reach (proposed)",
    "D": "Thruster Snap (proposed)",
}

PHASE2_STATEMENT = "Same attack, re-timed via Phase 2 parameters - no new moveset"

NOTES = {
    "A": ("First Vanguard attack implemented this sprint; only enabled attack; all timing, "
          "damage, range, and cooldown values remain OPEN pending designer approval "
          "(see ATTACK_DATA_SOURCE_AUDIT.md)"),
    "B": "Approved metadata only; not yet implemented. Disabled for selection.",
    "C": "Approved metadata only; not yet implemented. Disabled for selection.",
    "D": ("Approved metadata only; not yet implemented. Disabled for selection. Max travel "
          "distance is OPEN (design-brief Q13) and must not be invented here."),
}


# ---------------------------------------------------------------------------
# Drift operators
# ---------------------------------------------------------------------------

def _drift_embellish_numeric(row, attack_id):
    """Over-specification: a plausible range nobody approved. Trips G6."""
    row["IntendedRange"] = row["IntendedRange"] + " within 250 cm"
    return "added an unapproved numeric range to IntendedRange"


def _drift_phase2_upgrade(row, attack_id):
    """'Re-timed' inflated into 'upgraded'. Trips G3."""
    row["Phase2Usage"] = "Phase 2 grants an upgraded moveset with a new finisher"
    return "restated Phase 2 as a new moveset"


def _drift_adaptive_language(row, attack_id):
    """The default way enemy AI gets described. Trips G4."""
    row["ActiveDescription"] = (
        "Adapts to the player in real time, selecting the least anticipated angle")
    return "described the attack as adapting to the player at runtime"


def _drift_invent_asset_path(row, attack_id):
    """A montage path that does not exist. Trips the contract's blank rule."""
    row["MontageAsset"] = "/Game/AscendantImpact/Animation/Vanguard/MM_Attack_%s" % attack_id
    return "invented a montage asset path"


def _drift_drop_name_caveat(row, attack_id):
    """The '(proposed)' caveat quietly disappears. Trips the contract."""
    row["DisplayWorkingName"] = WORKING_NAMES[attack_id].replace(" (proposed)", "")
    return "dropped the '(proposed)' caveat from the working name"


def _drift_fifth_attack(row, attack_id):
    """Canon error: an attack outside A-D. Trips G1."""
    row["Notes"] = row["Notes"] + " Pairs with the fifth attack in Phase 2."
    return "referenced a fifth attack"


def _drift_scope_creep(row, attack_id):
    """Deferred scope treated as shipped. Trips G5."""
    row["Notes"] = row["Notes"] + " Also used by the second boss in the additional arena."
    return "referenced deferred scope as if shipped"


def _drift_snap_travel(row, attack_id):
    """Attack D loses its travel cap. Trips G7."""
    if attack_id != "D":
        return None
    row["ActiveDescription"] = "Instant close to the player from anywhere via a full-arena snap"
    return "removed Attack D's travel cap and asserted a full-arena snap"


DRIFT_OPERATORS = (
    ("embellish_numeric", _drift_embellish_numeric),
    ("phase2_upgrade", _drift_phase2_upgrade),
    ("adaptive_language", _drift_adaptive_language),
    ("invent_asset_path", _drift_invent_asset_path),
    ("drop_name_caveat", _drift_drop_name_caveat),
    ("fifth_attack", _drift_fifth_attack),
    ("scope_creep", _drift_scope_creep),
    ("snap_travel", _drift_snap_travel),
)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def base_row(rules_doc, attack_id):
    """The canon-faithful row, straight from the GDD facts in the contract."""
    facts = rules_doc["gdd_attack_facts"][attack_id]
    contract = rules_doc["contract"]
    prototype = contract["prototype_attack"]
    is_prototype = attack_id == prototype

    return {
        "Name": "Row_%s" % attack_id,
        "AttackId": attack_id,
        "DisplayWorkingName": WORKING_NAMES[attack_id],
        "ImplementationStatus": "Prototype" if is_prototype else "Planned",
        "EnabledForSelection": "true" if is_prototype else "false",
        "IntendedRange": facts["range_purpose"],
        "GameplayPurpose": facts["range_purpose"],
        "TelegraphRequirement": facts["readability_requirement"],
        "TrackingRule": TRACKING_RULES[attack_id],
        "ActiveDescription": ACTIVE_DESCRIPTIONS[attack_id],
        "RecoveryRequirement": RECOVERY_REQUIREMENTS[attack_id],
        "Phase2Usage": PHASE2_STATEMENT,
        "MontageAsset": "",
        "TelegraphVfxAsset": "",
        "TelegraphAudioAsset": "",
        "HitTraceSocket": "",
        "Notes": NOTES[attack_id],
    }


def generate(rules_doc, attack_id, seed, kb_dir=None, drift_rate=DRIFT_RATE):
    """Generate one candidate row plus its retrieval and drift evidence."""
    if attack_id not in rules_doc["gdd_attack_facts"]:
        raise ValueError("no GDD facts for attack %r" % attack_id)

    kwargs = {"kb_dir": kb_dir} if kb_dir else {}
    selected = retrieval.retrieve(
        RETRIEVAL_QUERY.format(attack_id=attack_id),
        ELIGIBLE_FILES,
        required_chunks=REQUIRED_CHUNKS,
        **kwargs)

    row = base_row(rules_doc, attack_id)

    rng = random.Random(seed)
    applied = []
    for name, operator in DRIFT_OPERATORS:
        if rng.random() >= drift_rate:
            continue
        note = operator(row, attack_id)
        if note is not None:
            applied.append({"operator": name, "effect": note})

    return {
        "attack_id": attack_id,
        "seed": seed,
        "row": row,
        "retrieval": {
            "query": RETRIEVAL_QUERY.format(attack_id=attack_id),
            "eligible_files": list(ELIGIBLE_FILES),
            "selected": [sc.as_dict() for sc in selected],
            "gdd_citations": list(retrieval.citations_for(selected)),
        },
        "drift_applied": applied,
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Generate a Vanguard attack row.")
    parser.add_argument("--attack", default="A", choices=("A", "B", "C", "D"))
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--rules", default=DEFAULT_RULES)
    parser.add_argument("--out")
    args = parser.parse_args(argv)

    with open(args.rules, "r", encoding="utf-8") as handle:
        rules_doc = json.load(handle)

    result = generate(rules_doc, args.attack, args.seed)
    text = json.dumps(result, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        print("wrote %s" % args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
