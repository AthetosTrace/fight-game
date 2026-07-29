"""Deterministic validator for data/unreal/DT_VanguardAttacks.csv.

Checks the CSV against docs/unreal/VANGUARD_ATTACK_ROW_CONTRACT.md before any
human review or Unreal import. Exits 0 if the file passes every check, exits
1 and prints every violation found otherwise. This script invents nothing —
it only checks that no one else did either.
"""

import csv
import os
import re
import sys

CONTRACT_HEADERS = [
    "Name",
    "AttackId",
    "DisplayWorkingName",
    "ImplementationStatus",
    "EnabledForSelection",
    "IntendedRange",
    "GameplayPurpose",
    "TelegraphRequirement",
    "TrackingRule",
    "ActiveDescription",
    "RecoveryRequirement",
    "Phase2Usage",
    "MontageAsset",
    "TelegraphVfxAsset",
    "TelegraphAudioAsset",
    "HitTraceSocket",
    "Notes",
]

REQUIRED_FIELDS = [
    "Name",
    "AttackId",
    "ImplementationStatus",
    "EnabledForSelection",
    "IntendedRange",
    "GameplayPurpose",
    "TelegraphRequirement",
    "ActiveDescription",
    "RecoveryRequirement",
    "Phase2Usage",
]

# Must stay blank in this pass — no assets/sockets are approved yet.
MUST_BE_BLANK_FIELDS = [
    "MontageAsset",
    "TelegraphVfxAsset",
    "TelegraphAudioAsset",
    "HitTraceSocket",
]

# Per-field max character length, from VANGUARD_ATTACK_ROW_CONTRACT.md §2
# ("Max length" column). Every contract header must have an entry here.
MAX_LENGTHS = {
    "Name": 40,
    "AttackId": 1,
    "DisplayWorkingName": 40,
    "ImplementationStatus": 12,
    "EnabledForSelection": 5,
    "IntendedRange": 80,
    "GameplayPurpose": 80,
    "TelegraphRequirement": 120,
    "TrackingRule": 100,
    "ActiveDescription": 120,
    "RecoveryRequirement": 100,
    "Phase2Usage": 80,
    "MontageAsset": 200,
    "TelegraphVfxAsset": 200,
    "TelegraphAudioAsset": 200,
    "HitTraceSocket": 40,
    "Notes": 300,
}

# Free-text fields that must never carry an invented numeric game value
# (damage, range in cm, cooldown, travel cap, exact timing) in this pass.
# Phase2Usage is intentionally excluded: it is required to state that the
# attack carries into "Phase 2" unchanged, and that governed phrase
# legitimately contains a digit.
NO_NUMERIC_FIELDS = [
    "IntendedRange",
    "GameplayPurpose",
    "TelegraphRequirement",
    "TrackingRule",
    "ActiveDescription",
    "RecoveryRequirement",
    "Notes",
]

# Digits inside these governed/citation patterns are not invented gameplay
# measurements — they are phase references, open-question IDs, section
# references, or milestone names. Strip them before scanning for a leftover
# digit that would indicate an invented number (damage, cooldown, cm range,
# travel cap, exact timing).
ALLOWED_NUMERIC_REFERENCE_PATTERNS = [
    r"\bphase\s*[12]\b",        # "Phase 1" / "Phase 2"
    r"\bq\d{1,3}\b",            # design-brief open-question IDs, e.g. "Q13"
    r"§\d{1,3}(\.\d+)?",        # section references, e.g. "§14", "§5.3"
    r"\bm[1-5]\b",              # milestone references, e.g. "M2", "M4"
]

ALLOWED_ATTACK_IDS = ["A", "B", "C", "D"]
ALLOWED_STATUSES = ["Prototype", "Planned"]
ALLOWED_BOOLEANS = ["true", "false"]

RUNTIME_LEARNING_PATTERNS = [
    r"\blearns?\s+from\b",
    r"\badapts?\s+(in\s+real\s+time|at\s+runtime|to\s+the\s+player|dynamically)\b",
    r"\bmachine\s+learning\b",
    r"\bneural\s+network\b",
    r"\bllm\b",
    r"\bruntime\s+ai\b",
    r"\bgenerates?\s+attacks?\s+dynamically\b",
    r"\bself[- ]improv\w*\b",
    r"\bmodel\s+call\b",
    r"\blearn(ed|ing)?\s+the\s+player\b",
]

SCOPE_EXPANSION_PATTERNS = [
    r"\bfifth\s+attack\b",
    r"\bsecond\s+arena\b",
    r"\bpvp\b",
    r"\bmultiplayer\b",
    r"\bplayable\s+crimson\s+vanguard\b",
    r"\bcampaign\b",
    r"\badditional\s+arenas?\b",
    r"\badditional\s+fighters?\b",
    r"\bsecond\s+boss\b",
    r"\btransformation\b",
    r"\bstory\s+chapters?\b",
    r"\battack\s+e\b",
]


def _matches_any(patterns, text):
    lowered = text.lower()
    for pattern in patterns:
        if re.search(pattern, lowered, re.IGNORECASE):
            return pattern
    return None


def _strip_allowed_numeric_references(text):
    masked = text
    for pattern in ALLOWED_NUMERIC_REFERENCE_PATTERNS:
        masked = re.sub(pattern, "", masked, flags=re.IGNORECASE)
    return masked


def load_rows(path):
    """Returns (header, rows, errors). rows is None if the file is unreadable."""
    if not os.path.isfile(path):
        return None, None, [f"CSV file not found: {path}"]

    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        raw_rows = list(reader)

    if not raw_rows:
        return None, None, ["CSV file is empty (no header row)"]

    header = raw_rows[0]
    data_rows = raw_rows[1:]
    dict_rows = []
    for i, row in enumerate(data_rows):
        if len(row) != len(header):
            return header, None, [
                f"Row {i + 2} has {len(row)} fields, expected {len(header)} "
                f"(matching the header column count)"
            ]
        dict_rows.append(dict(zip(header, row)))

    return header, dict_rows, []


def validate(path):
    errors = []

    header, rows, load_errors = load_rows(path)
    if load_errors:
        return load_errors
    if rows is None:
        return errors or ["Unknown CSV load failure"]

    if header != CONTRACT_HEADERS:
        errors.append(
            "CSV headers do not match VANGUARD_ATTACK_ROW_CONTRACT.md.\n"
            f"  Expected: {CONTRACT_HEADERS}\n"
            f"  Found:    {header}"
        )
        # Header mismatch makes per-field checks unreliable; stop here.
        return errors

    if len(rows) != 4:
        errors.append(f"Expected exactly 4 rows, found {len(rows)}")
        # Row-count failure alone is fatal to the rest of the identity checks.
        return errors

    seen_ids = []
    seen_names = []
    enabled_rows = []

    for idx, row in enumerate(rows):
        row_label = f"Row {idx + 2} (Name={row.get('Name', '')!r})"

        # Required fields non-blank.
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                errors.append(f"{row_label}: required field '{field}' is blank")

        # Per-field max length, from VANGUARD_ATTACK_ROW_CONTRACT.md §2.
        for field in CONTRACT_HEADERS:
            value = row.get(field, "")
            limit = MAX_LENGTHS.get(field)
            if limit is not None and len(value) > limit:
                errors.append(
                    f"{row_label}: field '{field}' exceeds max length {limit} "
                    f"(found length {len(value)}: '{value}')"
                )

        # AttackId validity.
        attack_id = row.get("AttackId", "").strip()
        if attack_id not in ALLOWED_ATTACK_IDS:
            errors.append(
                f"{row_label}: AttackId '{attack_id}' is not one of "
                f"{ALLOWED_ATTACK_IDS}"
            )
        else:
            seen_ids.append(attack_id)

        # Row name.
        name = row.get("Name", "").strip()
        if name:
            seen_names.append(name)
        if attack_id in ALLOWED_ATTACK_IDS and name != f"Row_{attack_id}":
            errors.append(
                f"{row_label}: Name '{name}' does not match expected "
                f"'Row_{attack_id}' for AttackId '{attack_id}'"
            )

        # ImplementationStatus.
        status = row.get("ImplementationStatus", "").strip()
        if status not in ALLOWED_STATUSES:
            errors.append(
                f"{row_label}: unsupported ImplementationStatus '{status}' "
                f"(allowed: {ALLOWED_STATUSES})"
            )

        # EnabledForSelection.
        enabled_raw = row.get("EnabledForSelection", "").strip()
        if enabled_raw not in ALLOWED_BOOLEANS:
            errors.append(
                f"{row_label}: EnabledForSelection '{enabled_raw}' must be "
                f"exactly 'true' or 'false'"
            )
        elif enabled_raw == "true":
            enabled_rows.append(attack_id)

        # Attack A must be Prototype+enabled; B/C/D must be Planned+disabled.
        if attack_id == "A":
            if status == "Planned":
                errors.append(f"{row_label}: Attack A must not be 'Planned' (disabled)")
            if enabled_raw == "false":
                errors.append(f"{row_label}: Attack A must be EnabledForSelection=true")
        elif attack_id in ("B", "C", "D"):
            if status != "Planned":
                errors.append(
                    f"{row_label}: Attack {attack_id} must have "
                    f"ImplementationStatus=Planned, found '{status}'"
                )
            if enabled_raw != "false":
                errors.append(
                    f"{row_label}: Attack {attack_id} must have "
                    f"EnabledForSelection=false"
                )

        # Fields that must remain blank in this pass (no invented assets).
        for field in MUST_BE_BLANK_FIELDS:
            value = row.get(field, "").strip()
            if value:
                errors.append(
                    f"{row_label}: field '{field}' must remain blank in this "
                    f"pass (found '{value}') — no asset path may be invented "
                    f"before approval"
                )

        # No invented numeric values in fields required to stay unspecified.
        # Governed references (Phase 1/2, Q<n>, §<n>, M1-M5) are masked out
        # first so a legitimate citation doesn't read as an invented number.
        for field in NO_NUMERIC_FIELDS:
            value = row.get(field, "")
            masked_value = _strip_allowed_numeric_references(value)
            if re.search(r"\d", masked_value):
                errors.append(
                    f"{row_label}: field '{field}' contains a numeric value "
                    f"('{value}'), which must remain unspecified in this pass"
                )

        # Forbidden language checks across every field's text.
        full_text = " ".join(row.get(field, "") for field in header)
        learning_hit = _matches_any(RUNTIME_LEARNING_PATTERNS, full_text)
        if learning_hit:
            errors.append(
                f"{row_label}: runtime-learning language detected "
                f"(pattern: {learning_hit})"
            )
        scope_hit = _matches_any(SCOPE_EXPANSION_PATTERNS, full_text)
        if scope_hit:
            errors.append(
                f"{row_label}: forbidden scope-expansion language detected "
                f"(pattern: {scope_hit})"
            )

    # Cross-row checks.
    if len(set(seen_ids)) != len(seen_ids):
        errors.append(f"Duplicate AttackId values found: {seen_ids}")
    if set(seen_ids) != set(ALLOWED_ATTACK_IDS):
        errors.append(
            f"AttackId set must be exactly {set(ALLOWED_ATTACK_IDS)}, "
            f"found {set(seen_ids)}"
        )
    if len(set(seen_names)) != len(seen_names):
        errors.append(f"Duplicate row Name values found: {seen_names}")
    if len(enabled_rows) > 1:
        errors.append(
            f"More than one attack is enabled for selection: {enabled_rows}"
        )
    elif len(enabled_rows) == 1 and enabled_rows[0] != "A":
        errors.append(
            f"Only Attack A may be enabled for selection; found "
            f"'{enabled_rows[0]}' enabled instead"
        )
    elif len(enabled_rows) == 0:
        errors.append("No attack is enabled for selection; Attack A must be enabled")

    return errors


def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(
        "data", "unreal", "DT_VanguardAttacks.csv"
    )
    errors = validate(path)

    if errors:
        print(f"FAIL — {len(errors)} violation(s) found in {path}:\n")
        for i, error in enumerate(errors, start=1):
            print(f"{i}. {error}")
        return 1

    print(f"PASS — {path} satisfies the Vanguard attack row contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
