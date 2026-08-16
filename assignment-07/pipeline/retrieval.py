"""Retrieval stage -- prove every rule against the GDD text on disk.

Assignment 06's retrieval layer scored A#04's knowledge-base chunks. This one
does something narrower and stricter, because the claims here are different in
kind: a style rule asserts *what the GDD says*, and the cheapest way for that
to be wrong is for nobody to check.

So each rule and each slot in the contract carries a `gdd_source` string naming
a section, a page, and -- in single quotes -- the wording it relies on. This
module resolves the section to its file under `gdd/sections/`, finds that
wording, and returns the line it found. A rule whose quoted wording is not in
the file it cites comes back `verified: false`, and there is a test that fails
the build when any rule does.

That makes the citations load-bearing rather than decorative. It also means the
run report can show, side by side: the slot asked for, the GDD line behind it,
and the copy produced.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GDD_DIR = os.path.join(REPO_ROOT, "gdd", "sections")

_SECTION_RE = re.compile(r"section\s*(\d{1,2})", re.IGNORECASE)
_PAGE_RE = re.compile(r"pages?\s*([\d\-]+)", re.IGNORECASE)
_QUOTED_RE = re.compile(r"'([^']{8,})'")

# The extracted GDD normalises a few characters the PDF carried; comparisons
# have to normalise the same way or a correct citation reads as a miss.
_NORMALISE = {
    "’": "'", "‘": "'",
    "“": '"', "”": '"',
    "–": "-", "—": "-",
    " ": " ",
}


def _normalise(text):
    for source, target in _NORMALISE.items():
        text = text.replace(source, target)
    return re.sub(r"\s+", " ", text).strip().lower()


def section_file(section_number, gdd_dir=None):
    """The `gdd/sections/NN-*.md` file for a section number, or None."""
    directory = gdd_dir or DEFAULT_GDD_DIR
    if not os.path.isdir(directory):
        return None
    prefix = "%02d-" % int(section_number)
    for name in sorted(os.listdir(directory)):
        if name.startswith(prefix) and name.endswith(".md"):
            return os.path.join(directory, name)
    return None


def verify_citation(gdd_source, gdd_dir=None):
    """Resolve one `gdd_source` string against the extracted GDD.

    Returns a dict carrying the section, the page, the wording the citation
    claims, whether that wording is present, and the line it was found on.
    """
    section_match = _SECTION_RE.search(gdd_source)
    page_match = _PAGE_RE.search(gdd_source)
    quotes = _QUOTED_RE.findall(gdd_source)

    record = {
        "citation": gdd_source,
        "section": int(section_match.group(1)) if section_match else None,
        "page": page_match.group(1) if page_match else None,
        "quoted": quotes,
        "verified": False,
        "found_in": None,
        "excerpt": None,
    }

    if record["section"] is None or not quotes:
        # Contract entries that cite a repo document rather than a GDD section
        # (the open-values list does this) are out of scope for verification.
        return record

    path = section_file(record["section"], gdd_dir=gdd_dir)
    if path is None or not os.path.isfile(path):
        return record

    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    record["found_in"] = os.path.relpath(path, REPO_ROOT).replace("\\", "/")

    # Match against the whole section, flattened. The extracted GDD is a PDF
    # dump, so authored sentences wrap mid-clause and a line-by-line search
    # would miss quotes that are genuinely present. Flattening once and
    # searching that is the only way a citation spanning a wrap can verify.
    flattened_lines = [_normalise(line) for line in lines]
    document = " ".join(flattened_lines)

    for quote in quotes:
        needle = _normalise(quote)
        offset = document.find(needle)
        if offset == -1:
            continue
        record["verified"] = True
        record["excerpt"] = _excerpt_for(lines, flattened_lines, offset, len(needle))
        return record
    return record


def _excerpt_for(lines, flattened_lines, offset, length):
    """The authored line(s) a verified quote occupies.

    `offset` is a character position in the flattened join, so the line it
    belongs to is found by walking the same cumulative widths the join used --
    one space between entries. Anchoring on a word instead would land on the
    wrong line whenever the quote opens with a common word.
    """
    cursor = 0
    start_line = end_line = None
    for index, flattened in enumerate(flattened_lines):
        line_start = cursor
        line_end = cursor + len(flattened)
        if start_line is None and line_end > offset:
            start_line = index
        if line_start < offset + length:
            end_line = index
        cursor = line_end + 1  # the single space the join inserted
        if start_line is not None and line_start >= offset + length:
            break

    if start_line is None:
        return None
    selected = [lines[i].strip() for i in range(start_line, (end_line or start_line) + 1)]
    return " ".join(part for part in selected if part)


def applicable_rules(rules_doc, slot):
    """Rule ids that govern this slot, in contract order.

    A rule applies to every slot unless it names an `applies_to_slots` list.
    """
    applicable = []
    for rule in rules_doc["rules"]:
        scoped = rule.get("applies_to_slots")
        if scoped is None or slot in scoped:
            applicable.append(rule["id"])
    return applicable


def for_slot(rules_doc, slot, gdd_dir=None):
    """Everything the run report needs to show what the GDD said about a slot."""
    spec = rules_doc["slots"][slot]
    rule_ids = applicable_rules(rules_doc, slot)
    by_id = {rule["id"]: rule for rule in rules_doc["rules"]}

    return {
        "slot": slot,
        "moment": spec["moment"],
        "slot_citation": verify_citation(spec["gdd_source"], gdd_dir=gdd_dir),
        "rules_in_force": rule_ids,
        "rule_citations": [
            dict(verify_citation(by_id[rule_id]["gdd_source"], gdd_dir=gdd_dir),
                 rule_id=rule_id, title=by_id[rule_id]["title"])
            for rule_id in rule_ids
        ],
    }


def verify_all(rules_doc, gdd_dir=None):
    """Every citation in the contract that names a GDD section. Used by tests."""
    records = []
    for slot, spec in sorted(rules_doc["slots"].items()):
        record = verify_citation(spec["gdd_source"], gdd_dir=gdd_dir)
        record["source"] = "slot:%s" % slot
        records.append(record)
    for rule in rules_doc["rules"]:
        record = verify_citation(rule["gdd_source"], gdd_dir=gdd_dir)
        record["source"] = "rule:%s" % rule["id"]
        records.append(record)
    return records
