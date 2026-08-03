"""Shared gate check. Answers one question: is this agent's leave-off complete?

Three checks, in order:
  1. leave-offs/<name>.md exists.
  2. It carries "status: complete" in its YAML frontmatter.
  3. The artifact path it names is really on disk.

Used by both entry_gate.py (PreToolUse) and exit_gate.py (SubagentStop).

Run standalone for a quick manual check:
    py -3 .claude/hooks/check_leaveoff.py designer
Exit 0 means open (complete). Exit 1 means closed, with the reason printed.
"""

import os
import sys


def project_root():
    """The project directory. Claude Code sets CLAUDE_PROJECT_DIR; fall back to cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def parse_frontmatter(text):
    """Return the key/value pairs from a leading '--- ... ---' YAML block.

    Deliberately dependency-free: we only need flat 'key: value' lines, so we do
    not import PyYAML (not guaranteed on this machine).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_complete(agent_name):
    """Return (ok: bool, reason: str) for one agent's leave-off."""
    root = project_root()
    leaveoff = os.path.join(root, "leave-offs", agent_name + ".md")

    # 1. File exists.
    if not os.path.isfile(leaveoff):
        return False, "leave-offs/{}.md does not exist yet".format(agent_name)

    with open(leaveoff, "r", encoding="utf-8") as handle:
        text = handle.read()
    fields = parse_frontmatter(text)

    # 2. status: complete.
    status = fields.get("status", "").lower()
    if status != "complete":
        return False, "leave-offs/{}.md status is '{}', not 'complete'".format(
            agent_name, fields.get("status", "(missing)")
        )

    # 3. Named artifact is on disk.
    artifact = fields.get("artifact", "")
    if not artifact:
        return False, "leave-offs/{}.md names no artifact".format(agent_name)
    artifact_path = artifact if os.path.isabs(artifact) else os.path.join(root, artifact)
    if not os.path.isfile(artifact_path):
        return False, "leave-offs/{}.md names artifact '{}' but it is not on disk".format(
            agent_name, artifact
        )

    return True, "leave-offs/{}.md complete (artifact '{}' present)".format(agent_name, artifact)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: py -3 check_leaveoff.py <agent-name>", file=sys.stderr)
        sys.exit(2)
    ok, reason = check_complete(sys.argv[1])
    print(reason)
    sys.exit(0 if ok else 1)
