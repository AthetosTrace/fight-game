"""Gap scanner -- reads the design, scans the build, and reports what is missing.

This is the reasoning front half of the goal-oriented agent. It answers three
questions in order, and each answer is derived from a file rather than asserted:

    1. What does the design require?   -> parse build-sequence.md
    2. What has actually been built?   -> scan the Unreal project's Content tree
    3. What is missing, and what first? -> diff the two, rank by blocking step

`build-sequence.md` is the machine-readable projection of the GDD for this
project. It was written by the developer agent from `design-brief.md`, holds 63
ordered editor steps `M1-01` through `M5-08`, and every step names the assets it
produces. That makes it the one document where "what the design requires" is
stated as identifiers a program can check, instead of prose a human must read.

Ranking is by blocking step: the lowest-numbered step that cannot execute until
the gap is closed. That rule predates these questions -- build-sequence.md was
written before most of them were asked -- so it cannot be bent to justify a
convenient order.

Ownership is applied *after* ranking, never before. The report always shows the
true top of the list, then names the highest-ranked gap this side of the project
is actually allowed to build. Hiding another owner's work from the ranking would
make the tool lie about what matters most.

Exit codes:
    0  scan completed, gaps reported
    2  nothing to rank -- no requirements parsed, or no codebase to compare
    3  bad usage / unreadable input
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCOPE = os.path.join(HERE, "scope.json")

# A step heading looks like:  ### M1-21 - Gray-box `L_ShatteredRing`
# The separator is an en or em dash in the source document. Written as escapes
# so this file stays pure ASCII and cannot break on a cp1252 machine.
STEP_HEADING = re.compile(
    "^#{2,4}\\s+(M[1-5]-\\d{2})\\s*[-–—]+\\s*(.+?)\\s*$")

# Asset identifiers are written in backticks and follow Unreal's prefix
# convention. Restricting to known prefixes keeps prose like `Details` or
# `Content` out of the requirement set.
ASSET_TOKEN = re.compile(r"`([A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+)`")

MILESTONE_ORDER = {"M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5}

# The design documents use typographic punctuation. Windows consoles default to
# cp1252, which cannot encode it, so titles are folded to ASCII on the way in
# rather than crashing the report on the way out.
ASCII_FOLD = {
    "→": "->", "←": "<-", "–": "-", "—": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "×": "x", "±": "+/-", "°": " deg",
}


def to_ascii(text):
    for char, replacement in ASCII_FOLD.items():
        text = text.replace(char, replacement)
    return text.encode("ascii", "ignore").decode("ascii")


def step_sort_key(step_id):
    """`M2-07` -> (2, 7). Sorts across milestones, not lexically."""
    milestone, number = step_id.split("-")
    return (MILESTONE_ORDER.get(milestone, 99), int(number))


def load_json(path, label):
    if not os.path.isfile(path):
        raise IOError("%s not found: %s" % (label, path))
    with open(path, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except ValueError as exc:
            raise IOError("%s is not valid JSON: %s" % (label, exc))


def parse_requirements(path, prefixes):
    """Extract the assets each build step produces.

    Returns a list of {step_id, title, assets}. Only assets whose prefix is in
    `prefixes` are kept -- the document also backticks menu paths and property
    names, and treating those as deliverables would invent requirements.
    """
    if not os.path.isfile(path):
        raise IOError("build sequence not found: %s" % path)

    steps = []
    current = None
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            heading = STEP_HEADING.match(line)
            if heading:
                current = {
                    "step_id": heading.group(1),
                    "title": to_ascii(heading.group(2).replace("`", "").strip()),
                    "assets": [],
                }
                steps.append(current)
                continue
            if current is None:
                continue
            for token in ASSET_TOKEN.findall(line):
                prefix = token.split("_", 1)[0]
                if prefix in prefixes and token not in current["assets"]:
                    current["assets"].append(token)
    return steps


def scan_codebase(content_root):
    """Every named asset that exists in the Unreal project.

    One-File-Per-Actor packages under __ExternalActors__ / __ExternalObjects__
    are per-instance data with generated hash names, not authored assets, so
    they are skipped -- counting them would drown the real inventory.
    """
    if not os.path.isdir(content_root):
        raise IOError("content root not found: %s" % content_root)

    built = set()
    for root, dirs, files in os.walk(content_root):
        dirs[:] = [d for d in dirs if not d.startswith("__External")]
        for name in files:
            stem, ext = os.path.splitext(name)
            if ext.lower() in (".uasset", ".umap"):
                built.add(stem)
    return built


def detect_gaps(steps, built, scope):
    """Diff what the design requires against what exists.

    An alias records that a required asset shipped under a different name --
    the prototype built `BP_ThirdPersonCharacter` where the sequence planned
    `BP_PlayerFighter`. Aliases must be declared with a reason; the scanner will
    not guess that two differently-named assets are the same thing.
    """
    aliases = scope.get("aliases", {})
    ignore = set(scope.get("not_deliverables", []))

    gaps = []
    for step in steps:
        missing = []
        for asset in step["assets"]:
            if asset in ignore:
                continue
            shipped_as = aliases.get(asset, {}).get("shipped_as")
            if asset in built:
                continue
            if shipped_as and shipped_as in built:
                continue
            missing.append(asset)
        if missing:
            gaps.append({
                "step_id": step["step_id"],
                "title": step["title"],
                "missing": missing,
            })
    gaps.sort(key=lambda g: step_sort_key(g["step_id"]))
    return gaps


def select_buildable(gaps, scope):
    """The highest-ranked gap this side of the project may actually build.

    Ownership is a filter applied after ranking, never a reordering. The caller
    still sees the true top of the list.
    """
    owned = set(scope.get("owned_steps", []))
    for gap in gaps:
        if gap["step_id"] in owned:
            return gap
    return None


def render_markdown(report):
    out = []
    out.append("# Gap scan")
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Requirements parsed | %d steps, %d assets |" % (
        report["steps_parsed"], report["assets_required"]))
    out.append("| Assets found in the build | %d |" % report["assets_built"])
    out.append("| Steps with something missing | %d |" % len(report["gaps"]))
    out.append("")

    selected = report.get("selected")
    if selected:
        out.append("**Selected to build: `%s` - %s**" % (
            selected["step_id"], selected["title"]))
        out.append("")
        out.append("Highest-ranked gap that falls inside this side's ownership. "
                   "Everything ranked above it belongs to the gameplay owner.")
    else:
        out.append("**Nothing selected** — no ranked gap falls inside this "
                   "side's ownership.")
    out.append("")

    out.append("## Ranked gaps")
    out.append("")
    out.append("Ranked by blocking step: the lowest-numbered build step that "
               "cannot execute until the gap is closed.")
    out.append("")
    out.append("| Rank | Step | What it produces | Missing | Ours |")
    out.append("|---|---|---|---|---|")
    owned = set(report["owned_steps"])
    for index, gap in enumerate(report["gaps"], start=1):
        out.append("| %d | `%s` | %s | %s | %s |" % (
            index, gap["step_id"], gap["title"],
            ", ".join("`%s`" % m for m in gap["missing"]),
            "yes" if gap["step_id"] in owned else "no"))
    out.append("")

    if report.get("aliases_applied"):
        out.append("## Aliases applied")
        out.append("")
        out.append("Assets the sequence planned under one name and the "
                   "prototype shipped under another.")
        out.append("")
        out.append("| Planned | Shipped as | Why |")
        out.append("|---|---|---|")
        for planned, info in sorted(report["aliases_applied"].items()):
            out.append("| `%s` | `%s` | %s |" % (
                planned, info["shipped_as"], info.get("reason", "")))
        out.append("")
    return "\n".join(out) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(
        description="Scan the design and the build, and report what is missing.")
    parser.add_argument("--build-sequence", default="build-sequence.md",
                        help="the design document to parse")
    parser.add_argument("--scan", help="path to the Unreal project root to scan")
    parser.add_argument("--inventory",
                        help="use a committed asset inventory instead of --scan")
    parser.add_argument("--write-inventory",
                        help="save the scanned inventory here for later reuse")
    parser.add_argument("--scope", default=DEFAULT_SCOPE)
    parser.add_argument("--out", help="write the markdown report here")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if not args.scan and not args.inventory:
        print("ERROR: pass --scan <unreal-project> or --inventory <file.json>",
              file=sys.stderr)
        return 3

    try:
        scope = load_json(args.scope, "scope file")
        steps = parse_requirements(args.build_sequence, set(scope["asset_prefixes"]))
        if args.scan:
            content_root = os.path.join(args.scan, "Content")
            if not os.path.isdir(content_root):
                content_root = args.scan
            built = scan_codebase(content_root)
            source = os.path.abspath(args.scan)
        else:
            inventory = load_json(args.inventory, "inventory")
            built = set(inventory["assets"])
            source = inventory.get("scanned_from", args.inventory)
    except IOError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3

    if not steps:
        print("ERROR: no build steps parsed from %s" % args.build_sequence,
              file=sys.stderr)
        return 2
    if not built:
        print("ERROR: no assets found to compare against", file=sys.stderr)
        return 2

    if args.write_inventory:
        os.makedirs(os.path.dirname(os.path.abspath(args.write_inventory)),
                    exist_ok=True)
        with open(args.write_inventory, "w", encoding="utf-8") as handle:
            json.dump({"scanned_from": source, "assets": sorted(built)},
                      handle, indent=2)

    gaps = detect_gaps(steps, built, scope)
    selected = select_buildable(gaps, scope)

    aliases_applied = {
        planned: info for planned, info in scope.get("aliases", {}).items()
        if info.get("shipped_as") in built
    }

    report = {
        "scanned_from": source,
        "build_sequence": args.build_sequence,
        "steps_parsed": len(steps),
        "assets_required": sum(len(s["assets"]) for s in steps),
        "assets_built": len(built),
        "owned_steps": scope.get("owned_steps", []),
        "gaps": gaps,
        "selected": selected,
        "aliases_applied": aliases_applied,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(render_markdown(report))
        with open(os.path.splitext(args.out)[0] + ".json", "w",
                  encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
