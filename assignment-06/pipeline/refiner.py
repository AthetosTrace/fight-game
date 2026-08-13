"""Refiner stage -- the smallest correction that clears one failure.

Rules this stage obeys, carried over from the arena pipeline because they held
up there:

1. One field per attempt. No batch rewrites, no regeneration.
2. Every change is recorded as a before/after diff.
3. If a fix would require deciding something the GDD leaves open, REFUSE.
4. If no rule matches the failure, REFUSE. Silence is not a correction.

The refusals here are not defensive padding -- each one names a decision that
belongs to the designer:

    G1  The attack set is GDD canon. A row asserting a fifth attack is a canon
        error, not a field that drifted, and there is no correct value to
        write.
    G5  What is deferred and what ships is the designer's roadmap.
    G7  Fixing an uncapped Attack D means choosing a travel cap. That is
        design-brief Q13, OPEN. Inventing it here is exactly the failure the
        Pre-Build Declaration named.

A refusal is a legitimate outcome. The orchestrator turns it into a
human-review stop, and the run report says which decision is waiting.
"""

import copy
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import generator  # noqa: E402
import textcheck  # noqa: E402
from evaluator import rules_by_id  # noqa: E402

# Failures we are structurally not allowed to auto-fix, and why.
REFUSALS = {
    "G1": "the authored attack set is GDD canon (section 04, page 5). A row asserting "
          "an attack outside A-D is a canon error with no correct value to write",
    "G5": "what is deferred and what ships is the scope lock (section 09, page 15), "
          "which is the designer's roadmap rather than a field correction",
    "G7": "capping Attack D's travel means choosing a maximum distance. That is "
          "design-brief Q13 and it is OPEN -- inventing it is the failure this "
          "pipeline exists to prevent",
}


class Refinement(object):
    def __init__(self, row=None, change=None, refused=None):
        self.row = row
        self.change = change
        self.refused = refused

    @property
    def applied(self):
        return self.refused is None

    def as_dict(self):
        return {"applied": self.applied, "change": self.change, "refused": self.refused}


def _change(field, before, after, reason):
    return {"field": field, "before": before, "after": after, "reason": reason}


# ---------------------------------------------------------------------------
# Gate fixes
# ---------------------------------------------------------------------------

def _fix_required(row, rules_doc, violation):
    """A blank required field is restored from the GDD facts, never guessed."""
    field = violation.field
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    if field not in canonical or not str(canonical[field]).strip():
        return None
    before = row.get(field, "")
    row[field] = canonical[field]
    return _change(field, before, row[field], "restored from the GDD attack facts")


def _fix_blank(row, rules_doc, violation):
    """An invented asset path is cleared. No asset is approved this pass."""
    field = violation.field
    before = row.get(field, "")
    row[field] = ""
    return _change(field, before, "", "cleared -- no asset path is approved yet")


def _fix_matrix(row, rules_doc, violation):
    field = violation.field
    before = row.get(field, "")
    row[field] = violation.expected
    return _change(field, before, row[field],
                   "set to the value the row contract requires this pass")


def _fix_name(row, rules_doc, violation):
    before = row.get("Name", "")
    row["Name"] = violation.expected
    return _change("Name", before, row["Name"], "aligned with the row's AttackId")


def _fix_maxlen(row, rules_doc, violation):
    """Restore the canonical wording rather than truncating mid-sentence."""
    field = violation.field
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    if field not in canonical:
        return None
    before = row.get(field, "")
    if len(str(canonical[field])) > len(str(before)):
        return None
    row[field] = canonical[field]
    return _change(field, before, row[field],
                   "restored the canonical wording, which fits the contract length")


def _fix_g3(row, rules_doc, violation):
    before = row.get("Phase2Usage", "")
    row["Phase2Usage"] = generator.PHASE2_STATEMENT
    return _change("Phase2Usage", before, row["Phase2Usage"],
                   "restored the GDD's Phase 2 statement -- same attacks, re-timed")


def _fix_g4(row, rules_doc, violation):
    """Adaptive language is replaced by the authored description for this
    attack. The Vanguard is a state machine; say so."""
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    for field in ("ActiveDescription", "TelegraphRequirement", "RecoveryRequirement", "Notes"):
        value = str(row.get(field, ""))
        if value == canonical.get(field, ""):
            continue
        if textcheck.unnegated_pattern(value, rules_by_id(rules_doc)["G4"]["forbidden_patterns"]):
            before = row[field]
            row[field] = canonical[field]
            return _change(field, before, row[field],
                           "replaced adaptive-AI language with the authored description")
    return None


def _fix_g6(row, rules_doc, violation):
    """Strip the invented number, keeping the qualitative GDD phrase."""
    field = violation.field
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    before = row.get(field, "")
    if field in canonical and canonical[field]:
        row[field] = canonical[field]
        return _change(field, before, row[field],
                       "restored the GDD's qualitative wording, dropping the invented number")
    stripped = re.sub(r"\s*\b\w*\d[\w.]*\s*\w*", "", str(before)).strip(" ;,-")
    if not stripped or stripped == before:
        return None
    row[field] = stripped
    return _change(field, before, stripped, "removed the invented numeric value")


# ---------------------------------------------------------------------------
# Evaluator-criterion fixes
# ---------------------------------------------------------------------------

def _fix_canon_fidelity(row, rules_doc, failure):
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    for field in ("IntendedRange", "GameplayPurpose", "TelegraphRequirement"):
        if str(row.get(field, "")) != canonical[field]:
            before = row.get(field, "")
            row[field] = canonical[field]
            return _change(field, before, row[field],
                           "restored the GDD wording for this attack")
    return None


def _fix_telegraph_readability(row, rules_doc, failure):
    attack_id = str(row.get("AttackId", "")).strip()
    canonical = generator.base_row(rules_doc, attack_id)
    for field in ("TelegraphRequirement", "RecoveryRequirement"):
        if str(row.get(field, "")) != canonical[field]:
            before = row.get(field, "")
            row[field] = canonical[field]
            return _change(field, before, row[field],
                           "restored the GDD readability requirement")
    return None


def _fix_phase2_consistency(row, rules_doc, failure):
    before = row.get("Phase2Usage", "")
    if before == generator.PHASE2_STATEMENT:
        return None
    row["Phase2Usage"] = generator.PHASE2_STATEMENT
    return _change("Phase2Usage", before, row["Phase2Usage"],
                   "restored the canonical Phase 2 statement")


def _fix_restraint(row, rules_doc, failure):
    """Re-caveat a working name that was asserted as canon.

    Re-adding the caveat is a mechanical restoration -- it takes nothing away
    and decides nothing. Choosing the *canon* name would be the designer's
    call, and this stage never does that.
    """
    attack_id = str(row.get("AttackId", "")).strip()
    name = str(row.get("DisplayWorkingName", "")).strip()
    if name and "proposed" not in name.lower():
        before = row["DisplayWorkingName"]
        canonical = generator.WORKING_NAMES.get(attack_id)
        row["DisplayWorkingName"] = canonical if canonical else "%s (proposed)" % name
        return _change("DisplayWorkingName", before, row["DisplayWorkingName"],
                       "re-caveated -- the GDD names no attack, so this is proposed only")

    notes = str(row.get("Notes", ""))
    if "open" not in notes.lower():
        canonical = generator.base_row(rules_doc, attack_id)
        before = notes
        row["Notes"] = canonical["Notes"]
        return _change("Notes", before, row["Notes"],
                       "restored the note flagging which values remain OPEN")
    return None


GATE_FIXES = {
    "C_REQUIRED": _fix_required,
    "C_BLANK": _fix_blank,
    "C_MATRIX": _fix_matrix,
    "C_NAME": _fix_name,
    "C_MAXLEN": _fix_maxlen,
    "G3": _fix_g3,
    "G4": _fix_g4,
    "G6": _fix_g6,
}

CRITERION_FIXES = {
    "canon_fidelity": _fix_canon_fidelity,
    "telegraph_readability": _fix_telegraph_readability,
    "phase2_consistency": _fix_phase2_consistency,
    "restraint": _fix_restraint,
}


def refine(row, failure_key, rules_doc, violation=None):
    """Apply the smallest correction for one failure. Never mutates the input."""
    if failure_key in REFUSALS:
        return Refinement(refused="cannot safely fix %s: %s" % (failure_key, REFUSALS[failure_key]))

    fix = GATE_FIXES.get(failure_key) or CRITERION_FIXES.get(failure_key)
    if fix is None:
        return Refinement(refused="no refinement rule exists for %s" % failure_key)

    candidate = copy.deepcopy(row)
    change = fix(candidate, rules_doc, violation if violation is not None else failure_key)
    if change is None:
        return Refinement(
            refused="%s reported a failure the refiner could not locate" % failure_key)
    return Refinement(row=candidate, change=change)
