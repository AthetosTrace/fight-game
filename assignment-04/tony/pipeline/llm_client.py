"""Claude Code CLI wrapper for Assignment #04's content pipeline.

Invokes the already-installed `claude` CLI in non-interactive, tool-less mode
as the generation/critique backend. No API keys, no third-party SDKs -
standard library only. The prompt always goes in via stdin, never shell
interpolation, and the subprocess call always uses shell=False.

Standalone use (mirrors .claude/hooks/check_leaveoff.py's own pattern):
    py -3 assignment-04/tony/pipeline/llm_client.py --check
"""

import argparse
import os
import shutil
import subprocess
import sys

DEFAULT_MODEL = "sonnet"
DEFAULT_TIMEOUT_S = 120
PREFLIGHT_TIMEOUT_S = 30
MODEL_ENV_VAR = "CLAUDE_PIPELINE_MODEL"

_AUTH_FAILURE_MARKERS = (
    "not authenticated",
    "not logged in",
    "unauthorized",
    "authentication",
    "please log in",
    "please run",
    "login required",
    "invalid api key",
    "credentials",
)


class ClaudeClientError(Exception):
    """Base class for every error this wrapper raises."""


class ClaudeNotFoundError(ClaudeClientError):
    """The `claude` executable could not be located on PATH."""


class ClaudeAuthError(ClaudeClientError):
    """The CLI call failed in a way that looks like an authentication problem."""


class ClaudeTimeoutError(ClaudeClientError):
    """The CLI call did not finish within the allotted timeout."""


class ClaudeCLIError(ClaudeClientError):
    """The CLI exited non-zero for a reason other than authentication."""


class ClaudeResponseParseError(ClaudeClientError):
    """A successful CLI call returned empty or whitespace-only stdout."""


def find_claude_executable():
    """Locate the Claude Code CLI executable. Raises ClaudeNotFoundError if absent."""
    exe = shutil.which("claude") or shutil.which("claude.cmd")
    if not exe:
        raise ClaudeNotFoundError(
            "Could not find the 'claude' executable on PATH (checked 'claude' "
            "and 'claude.cmd'). Install/verify the Claude Code CLI and retry."
        )
    return exe


def build_command(executable, model):
    """Build the exact, fixed argument list. No shell, no interpolation."""
    return [
        executable,
        "-p",
        "--model", model,
        "--tools", "",
        "--output-format", "text",
        "--no-session-persistence",
    ]


def _looks_like_auth_failure(*texts):
    combined = " ".join(t or "" for t in texts).lower()
    return any(marker in combined for marker in _AUTH_FAILURE_MARKERS)


def call_claude(prompt, model=None, timeout=DEFAULT_TIMEOUT_S, executable=None):
    """Run one non-interactive, tool-less Claude Code CLI call and return its text.

    The prompt is passed via stdin (input=), never as a shell-interpolated
    argument, and the call always uses shell=False.
    """
    resolved_model = model or os.environ.get(MODEL_ENV_VAR) or DEFAULT_MODEL
    exe = executable or find_claude_executable()
    command = build_command(exe, resolved_model)

    try:
        proc = subprocess.run(
            command,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError as exc:
        raise ClaudeNotFoundError(
            "The 'claude' executable could not be run: {}".format(exc)
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise ClaudeTimeoutError(
            "Claude CLI call timed out after {}s.".format(timeout)
        ) from exc

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    if proc.returncode != 0:
        if _looks_like_auth_failure(stderr, stdout):
            raise ClaudeAuthError(
                "Claude CLI exited {} in a way that looks like an authentication "
                "failure. stderr: {!r}. Run `claude` interactively once to "
                "(re)authenticate, then retry.".format(proc.returncode, stderr.strip())
            )
        raise ClaudeCLIError(
            "Claude CLI exited with status {}. stderr: {!r}".format(
                proc.returncode, stderr.strip()
            )
        )

    text = stdout.strip()
    if not text:
        raise ClaudeResponseParseError(
            "Claude CLI exited successfully but stdout was empty or "
            "whitespace-only. stderr: {!r}".format(stderr.strip())
        )

    return text


def preflight(model=None, timeout=PREFLIGHT_TIMEOUT_S):
    """Verify the CLI is installed and authenticated with one real call.

    Returns (ok: bool, message: str).
    """
    try:
        exe = find_claude_executable()
    except ClaudeNotFoundError as exc:
        return False, str(exc)

    try:
        call_claude(
            "Reply with the single word OK.",
            model=model,
            timeout=timeout,
            executable=exe,
        )
    except ClaudeClientError as exc:
        return False, str(exc)

    return True, "Claude CLI found at '{}' and responded successfully.".format(exe)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Preflight check: is the Claude Code CLI installed and authenticated?"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run the preflight check (this is also the default action).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model alias to use for the check (default: {} or ${}).".format(
            DEFAULT_MODEL, MODEL_ENV_VAR
        ),
    )
    args = parser.parse_args(argv)

    ok, message = preflight(model=args.model)
    print(("PASS: " if ok else "FAIL: ") + message)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
