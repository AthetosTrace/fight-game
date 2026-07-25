"""Exit gate. SubagentStop hook covering our three agents.

Reads agent_type from stdin and runs the shared check on that agent. If its
leave-off is not complete, writes the reason to stderr and exits 2 — that blocks
the stop and hands the reason back to the agent so it goes and writes one.

Agents that are not ours are ignored, so this hook needs no matcher.

One-shot guard: an agent that fails this check twice is let through with a warning
instead of hanging forever. Failure counts are kept in a small per-agent state file
and reset the moment the agent passes.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_leaveoff import check_complete, project_root  # noqa: E402

OURS = {"designer", "developer", "inspector"}
MAX_FAILURES = 2  # On the 2nd failure, let the agent through with a warning.


def state_dir():
    d = os.path.join(project_root(), ".claude", "hooks", ".state")
    os.makedirs(d, exist_ok=True)
    return d


def read_count(agent):
    path = os.path.join(state_dir(), "exit_guard_" + agent + ".count")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return int(handle.read().strip() or "0")
    except (OSError, ValueError):
        return 0


def write_count(agent, value):
    path = os.path.join(state_dir(), "exit_guard_" + agent + ".count")
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(str(value))
    except OSError:
        pass


def clear_count(agent):
    path = os.path.join(state_dir(), "exit_guard_" + agent + ".count")
    try:
        os.remove(path)
    except OSError:
        pass


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    agent = (
        payload.get("agent_type")
        or payload.get("subagent_type")
        or (payload.get("tool_input", {}) or {}).get("subagent_type")
    )
    if agent not in OURS:
        sys.exit(0)  # Not one of ours — don't interfere.

    ok, reason = check_complete(agent)
    if ok:
        clear_count(agent)
        sys.exit(0)

    # Failed. Count it, and apply the one-shot guard.
    count = read_count(agent) + 1
    write_count(agent, count)

    if count >= MAX_FAILURES:
        clear_count(agent)
        print(
            "WARNING: {} failed the exit gate {} times ({}). Letting it through "
            "to avoid hanging - its leave-off is NOT complete.".format(agent, count, reason),
            file=sys.stderr,
        )
        sys.exit(0)

    print(
        "{} cannot stop yet: {}. Write leave-offs/{}.md with 'status: complete' "
        "(status line last) and the artifact on disk, then finish.".format(
            agent, reason, agent
        ),
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
