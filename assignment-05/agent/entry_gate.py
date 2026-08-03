"""Entry gate. PreToolUse hook matching Task / Agent.

Reads subagent_type from the JSON on stdin, looks up that agent's upstream
dependencies, and runs the shared check on each. If any dependency fails, prints
hookSpecificOutput with permissionDecision "deny" and the reason, so the subagent
never spawns. Otherwise stays silent and lets the spawn through.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_leaveoff import check_complete, project_root  # noqa: E402


# Upstream dependencies per agent.
#   "file"     -> a plain file must exist on disk.
#   "leaveoff" -> another agent's leave-off must be complete (shared check).
DEPS = {
    # Runs FIRST and has no upstream agent. It is the thing that decides what runs
    # next, so gating it on another agent's leave-off would deadlock the pipeline.
    # It still needs the game to exist to reason about, so the three anchor files are
    # required - the same three the designer needs. An empty list would let it spawn
    # against an empty repo and produce a confident plan about nothing.
    "goal-planner": [
        {"type": "file", "path": "project-brief.md"},
        {"type": "file", "path": "gdd/ascendant-impact-gdd-v0.4.md"},
        {"type": "file", "path": "build-sequence.md"},
    ],
    "designer": [
        {"type": "file", "path": "project-brief.md"},
        # The GDD is the source of truth. Without it the brief is unanchored, and
        # assignment #04's knowledge base has nothing real to retrieve from.
        {
            "type": "file",
            "path": "Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf",
        },
        # The extracted text. Read-only agents cannot open the PDF on this machine
        # (poppler is absent), so this is the copy they actually consult.
        {"type": "file", "path": "gdd/ascendant-impact-gdd-v0.4.md"},
    ],
    "developer": [{"type": "leaveoff", "agent": "designer"}],
    # Designer only, on purpose. Design-only sessions never run the developer, so
    # depending on the developer here would deny the inspector a spawn it must be
    # able to make. The gate enforces ORDER (nothing inspects before there is a
    # design to inspect); COVERAGE is enforced by the agent itself — see
    # `.claude/agents/inspector.md`, which requires the inspector to also verify
    # `build-sequence.md` whenever that file exists and has changed since the last
    # inspection. Do not add the developer back here.
    "inspector": [{"type": "leaveoff", "agent": "designer"}],
}


def deny(reason):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Can't parse input — don't block on our account.
        sys.exit(0)

    tool_input = payload.get("tool_input", {}) or {}
    agent = tool_input.get("subagent_type") or payload.get("subagent_type")
    if not agent:
        sys.exit(0)  # Not one of our agent spawns we can identify.

    deps = DEPS.get(agent)
    if deps is None:
        sys.exit(0)  # Unknown agent — not ours to gate.

    root = project_root()
    for dep in deps:
        if dep["type"] == "file":
            if not os.path.isfile(os.path.join(root, dep["path"])):
                deny(
                    "{} is blocked: required file '{}' does not exist yet.".format(
                        agent, dep["path"]
                    )
                )
        elif dep["type"] == "leaveoff":
            ok, reason = check_complete(dep["agent"])
            if not ok:
                deny("{} is blocked: {}.".format(agent, reason))

    sys.exit(0)  # All gates open.


if __name__ == "__main__":
    main()
