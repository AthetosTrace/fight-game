"""Assignment #04 content pipeline: Context Retriever -> Content Generator ->
Consistency Critic, for Ascendant Impact.

Single entry point, no Claude Code agents, no project hooks - plain Python
using the local knowledge_base/critic_rules/llm_client modules. The Claude
Code CLI is invoked in tool-less, non-interactive mode purely as a text
generator; this script owns every file read and write itself.

Usage:
    python assignment-04/tony/pipeline/pipeline.py [--model sonnet]

Exits 0 on success, non-zero on any failure (preflight, generation, or I/O).
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import critic_rules  # noqa: E402
import knowledge_base  # noqa: E402
import llm_client  # noqa: E402

TONY_DIR = knowledge_base.TONY_DIR
OUTPUTS_DIR = TONY_DIR / "outputs"
RETRIEVAL_EVIDENCE_DIR = TONY_DIR / "retrieval-evidence"
CRITIC_EVIDENCE_DIR = TONY_DIR / "critic-evidence"


class PipelineError(Exception):
    """Raised for any pipeline-level failure that should abort with a message."""


def atomic_write_text(path, content, encoding="utf-8"):
    """Write content to path via a same-directory temp file + os.replace, so a
    crash mid-write never leaves a half-written final artifact."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            handle.write(content)
        os.replace(tmp_name, str(path))
    except Exception:
        try:
            os.remove(tmp_name)
        except OSError:
            pass
        raise


_SELECTION_REASON_LABELS = {
    knowledge_base.SELECTED_BY_LEXICAL: "lexical top-{k} score",
    knowledge_base.SELECTED_BY_REQUIRED: "required pin (outside lexical top-{k})",
    knowledge_base.SELECTED_BY_BOTH: "lexical top-{k} score + required pin",
}


# ---------------------------------------------------------------------------
# 2026-07-28 human grounding audit: prompt-side reinforcement.
#
# Distinct from knowledge_base.OUTPUTS' per-output "extra_constraints" (which
# encode what the retrieved chunks do and don't support), these are general
# grounding rules the generator drifted on across drafts - keyed by slug so
# they attach to the output where the drift actually happened, but phrased
# as standing rules rather than as a ban on the exact sentences that were
# caught. Applied in build_generation_prompt() regardless of what
# knowledge_base.py declares for a given output.
# ---------------------------------------------------------------------------
_AUDIT_GROUNDING_CONSTRAINTS = {
    "impact-window-beat-pack": (
        "Do not invent an armor weak point, a vulnerable armor location, a "
        "damage multiplier, an exposed component, or any momentary "
        "structural weakness for Crimson Vanguard, unless that exact detail "
        "is explicitly present in the grounding context above - the "
        "retrieved canon establishes armor, a readable opening, and a "
        "punishable recovery, never a weak point or a momentary "
        "vulnerability.",
        "Grounded wording is fine and encouraged here: you may describe "
        "striking during an earned opening, a punishable recovery, or a "
        "clean strike line - none of that implies or requires an armor "
        "weak point.",
        "State plainly that the 1-3 second burst occurs after the player "
        "succeeds at the Impact Window input - success earns the burst.",
        "Never write or imply that the player's input determines, "
        "controls, sets, or varies how long the burst lasts - earning the "
        "burst and sizing its duration are not the same thing, and only "
        "the former is true.",
    ),
    "vanguard-telegraph-pack": (
        "Describe Crimson Vanguard's attack selection as deterministic, "
        "authored, non-learning, and never runtime-adaptive.",
        "Explicitly acknowledge that this same authored selection logic "
        "may respond deterministically to range and cooldown - reacting to "
        "range/cooldown by a fixed, authored rule is conditional authored "
        "logic, not learning, and must not be denied.",
        "Never write broad claims that Crimson Vanguard is 'never "
        "reactive', 'non-reactive', or does not respond to combat "
        "conditions - those claims are false, since it does react, "
        "deterministically, to range and cooldown.",
        "Keep the distinction explicit: authored conditional behavior "
        "(fixed rules reacting to range/cooldown) is not the same as "
        "learning, player-pattern adaptation, or runtime-model behavior - "
        "only the latter three are forbidden.",
    ),
}


def render_retrieval_evidence(result):
    lines = []
    lines.append("# Retrieval evidence — {}".format(result.slug))
    lines.append("")
    lines.append("**Query:** {}".format(result.query))
    lines.append("")
    lines.append("**Eligible files (manifest-restricted):** {}".format(
        ", ".join(result.eligible_files)
    ))
    lines.append("")
    if result.required_chunks:
        lines.append("**Required (pinned) chunks:** {}".format(
            "; ".join(
                "{} — {}".format(source_file, heading)
                for source_file, heading in result.required_chunks
            )
        ))
        lines.append("")
    lines.append("## All candidate chunks (scored)")
    lines.append("")
    lines.append("| Score | Source file | Heading | Matched tokens |")
    lines.append("|---|---|---|---|")
    for sc in result.candidates:
        lines.append("| {} | {} | {} | {} |".format(
            sc.score, sc.chunk.source_file, sc.chunk.heading,
            ", ".join(sc.matched_tokens) if sc.matched_tokens else "(none)",
        ))
    lines.append("")
    lines.append(
        "## Selected chunks passed to the generator "
        "(lexical top-{k}, score > 0, plus any required pins)".format(k=result.top_k)
    )
    lines.append("")
    if not result.selected:
        lines.append("_No chunk scored above zero and no chunk was pinned for this query._")
    for sc, reason in zip(result.selected, result.selection_reasons):
        lines.append("### {} — {}".format(sc.chunk.source_file, sc.chunk.heading))
        lines.append("")
        reason_label = _SELECTION_REASON_LABELS[reason].format(k=result.top_k)
        lines.append("Score: {} (matched: {}) — selected by: {} [{}]".format(
            sc.score, ", ".join(sc.matched_tokens) if sc.matched_tokens else "(none)",
            reason_label, reason,
        ))
        lines.append("")
        lines.append(sc.chunk.body)
        lines.append("")
    return "\n".join(lines) + "\n"


def build_generation_prompt(output_cfg, retrieval_result):
    grounding = "\n\n".join(
        "### {} — {}\n{}".format(sc.chunk.source_file, sc.chunk.heading, sc.chunk.body)
        for sc in retrieval_result.selected
    )
    allowed = "\n".join("- {}".format(item) for item in output_cfg["allowed_to_create"])
    forbidden = "\n".join("- {}".format(item) for item in output_cfg["must_not_invent"])

    extra_constraints = output_cfg.get("extra_constraints", ())
    extra_block = ""
    if extra_constraints:
        extra_block = "\n\nADDITIONAL CONSTRAINTS FOR THIS OUTPUT:\n" + "\n".join(
            "- {}".format(item) for item in extra_constraints
        )

    audit_constraints = _AUDIT_GROUNDING_CONSTRAINTS.get(output_cfg["slug"], ())
    audit_block = ""
    if audit_constraints:
        audit_block = (
            "\n\nGROUNDING AUDIT CONSTRAINTS (human review, 2026-07-28):\n"
            + "\n".join("- {}".format(item) for item in audit_constraints)
        )

    return (
        "You are drafting a short piece of authored game content for the Unreal "
        "Engine 5.8 action fighter Ascendant Impact, for use as offline design "
        "reference only (this text never ships as runtime game code).\n\n"
        "OUTPUT: {title}\n\n"
        "GROUNDING CONTEXT (retrieved from the approved knowledge base — treat as "
        "fact, do not contradict it):\n{grounding}\n\n"
        "YOU MAY CREATE:\n{allowed}\n\n"
        "YOU MUST NEVER INVENT:\n{forbidden}{extra}{audit}\n\n"
        "Every timing/tuning number is provisional and belongs to the human "
        "designer — quote governed numbers verbatim if you reference them at "
        "all, never alter or round them. Crimson Vanguard is deterministic "
        "authored logic (state machine / Behavior Tree) — never describe it as "
        "learning, adapting, or calling a model at runtime. Write the output now "
        "as plain prose/markdown, with no meta-commentary about these "
        "instructions.".format(
            title=output_cfg["title"], grounding=grounding, allowed=allowed,
            forbidden=forbidden, extra=extra_block, audit=audit_block,
        )
    )


def build_correction_prompt(violation, context_hint):
    return (
        "Rewrite ONLY the sentence below to fix one specific problem. Return "
        "just the corrected sentence, nothing else — no preamble, no quotes, "
        "no explanation.\n\n"
        "SENTENCE TO FIX:\n{sentence}\n\n"
        "PROBLEM: {explanation}\n\n"
        "REQUIRED CORRECTION: {instruction}\n\n"
        "CONTEXT (do not contradict): {hint}".format(
            sentence=violation.matched_sentence,
            explanation=violation.explanation,
            instruction=violation.correction_instruction,
            hint=context_hint,
        )
    )


_CORRECTION_CONTEXT_HINT = (
    "Ascendant Impact, Unreal Engine 5.8 cinematic 1v1 action fighter; Crimson "
    "Vanguard is deterministic authored AI; scope is one player, one arena, "
    "one authored rival, four fixed attacks A-D."
)


def apply_corrections(draft_text, violations, model):
    corrected_text = draft_text
    corrections = []
    for violation in violations:
        prompt = build_correction_prompt(violation, _CORRECTION_CONTEXT_HINT)
        corrected_sentence = llm_client.call_claude(prompt, model=model).strip()
        if violation.matched_sentence in corrected_text:
            corrected_text = corrected_text.replace(
                violation.matched_sentence, corrected_sentence, 1
            )
        corrections.append((violation, corrected_sentence))

    # Never accept an LLM correction on faith: re-run all seven deterministic
    # rules against the fully-corrected text. If anything still fires (the
    # original problem persists, or the rewrite introduced a new one), fail
    # loudly here rather than letting a caller write out an invalid final.
    critic_rules.verify_correction(corrected_text)

    return corrected_text, corrections


def render_critic_evidence(label, violations, corrections, is_fixture=False):
    lines = []
    header = "# Critic evidence — {}".format(label)
    if is_fixture:
        header += "  \n**CONTROLLED REGRESSION FIXTURE — NOT A REAL GENERATED OUTPUT**"
    lines.append(header)
    lines.append("")

    flagged_rule_numbers = {v.rule_number for v in violations}

    lines.append("## Per-rule results (all seven checked)")
    lines.append("")
    lines.append("| Rule | Status |")
    lines.append("|---|---|")
    for rule_number in range(1, 8):
        status = "FLAGGED" if rule_number in flagged_rule_numbers else "clean"
        lines.append("| {} | {} |".format(rule_number, status))
    lines.append("")

    if not violations:
        lines.append(
            "No violation detected against any of the seven consistency rules. "
            "The draft is preserved unchanged as the final output."
        )
        return "\n".join(lines) + "\n"

    for violation, corrected_sentence in corrections:
        lines.append("## Rule {} — {}".format(violation.rule_number, violation.rule_name))
        lines.append("")
        lines.append("**Before (flagged):**")
        lines.append("> {}".format(violation.matched_sentence))
        lines.append("")
        lines.append("**Why it's flagged:** {}".format(violation.explanation))
        lines.append("")
        lines.append("**Ground truth:** {}".format(violation.citation))
        lines.append("")
        lines.append("**After (corrected):**")
        lines.append("> {}".format(corrected_sentence))
        lines.append("")
    return "\n".join(lines) + "\n"


def run_output(output_cfg, model):
    retrieval_result = knowledge_base.retrieve(
        slug=output_cfg["slug"],
        query=output_cfg["query"],
        eligible_files=output_cfg["eligible_files"],
        required_chunks=output_cfg.get("required_chunks", ()),
    )
    atomic_write_text(
        RETRIEVAL_EVIDENCE_DIR / "{}.md".format(output_cfg["slug"]),
        render_retrieval_evidence(retrieval_result),
    )

    prompt = build_generation_prompt(output_cfg, retrieval_result)
    draft_text = llm_client.call_claude(prompt, model=model)
    atomic_write_text(
        OUTPUTS_DIR / "{}-draft.md".format(output_cfg["slug"]),
        draft_text,
    )

    violations = critic_rules.run_critic(draft_text)
    return draft_text, violations


def finalize_output(output_cfg, draft_text, violations, model):
    if violations:
        final_text, corrections = apply_corrections(draft_text, violations, model)
    else:
        final_text, corrections = draft_text, []

    atomic_write_text(
        CRITIC_EVIDENCE_DIR / "{}.md".format(output_cfg["slug"]),
        render_critic_evidence(output_cfg["title"], violations, corrections),
    )
    atomic_write_text(
        OUTPUTS_DIR / "{}-final.md".format(output_cfg["slug"]),
        final_text,
    )
    return final_text


def run_regression_fixture():
    """Run the controlled rule-#2 regression fixture end to end.

    Unlike apply_corrections (used for real generated drafts), this never
    calls Claude: the fixture's planted violation always maps to the same
    fixed, canon-safe correction, hand-authored and re-verified against all
    seven deterministic rules on every run. If that fixed correction ever
    stops passing (a rule drifted, or the fixture text changed underneath
    it), this fails loudly via CorrectionValidationError rather than writing
    out stale or invalid evidence.
    """
    fixture_text = critic_rules.REGRESSION_FIXTURE_TEXT
    violations = critic_rules.run_critic(fixture_text)
    rule_numbers = [v.rule_number for v in violations]
    if rule_numbers != [2]:
        # Defensive only - the fixture is designed to always trip exactly
        # rule #2, nothing more and nothing less.
        raise PipelineError(
            "Regression fixture must trip exactly rule #2; got rule(s) {} "
            "instead. The fixture or the detectors have drifted out of sync "
            "and need review.".format(rule_numbers)
        )

    corrected_text = critic_rules.REGRESSION_FIXTURE_CORRECTED_TEXT
    critic_rules.verify_correction(corrected_text)

    corrections = [(violations[0], critic_rules.REGRESSION_FIXTURE_CORRECTED_SENTENCE)]
    atomic_write_text(
        CRITIC_EVIDENCE_DIR / "regression-fixture.md",
        render_critic_evidence(
            critic_rules.REGRESSION_FIXTURE_TITLE,
            violations, corrections, is_fixture=True,
        ),
    )
    return corrected_text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", default=None,
        help="Model alias for both generation and critic-correction calls "
             "(default: {} or ${}).".format(llm_client.DEFAULT_MODEL, llm_client.MODEL_ENV_VAR),
    )
    args = parser.parse_args(argv)
    model = args.model or os.environ.get(llm_client.MODEL_ENV_VAR) or llm_client.DEFAULT_MODEL

    print("Preflight: checking Claude Code CLI install + auth ...")
    ok, message = llm_client.preflight(model=model)
    if not ok:
        print("FAIL: {}".format(message), file=sys.stderr)
        return 1
    print("PASS: {}".format(message))

    drafts = {}
    all_violations = {}
    try:
        for output_cfg in knowledge_base.OUTPUTS:
            print("Retrieving + generating: {}".format(output_cfg["slug"]))
            draft_text, violations = run_output(output_cfg, model)
            drafts[output_cfg["slug"]] = draft_text
            all_violations[output_cfg["slug"]] = violations

        any_real_violation = any(all_violations.values())

        for output_cfg in knowledge_base.OUTPUTS:
            slug = output_cfg["slug"]
            print("Critiquing + finalizing: {}".format(slug))
            finalize_output(output_cfg, drafts[slug], all_violations[slug], model)

        if not any_real_violation:
            print(
                "All three natural drafts passed clean — running the controlled "
                "regression fixture to demonstrate the critic."
            )
            run_regression_fixture()
        else:
            print(
                "At least one natural draft was flagged and corrected — "
                "regression fixture skipped (not needed)."
            )

    except llm_client.ClaudeClientError as exc:
        print("FAIL (Claude CLI): {}".format(exc), file=sys.stderr)
        return 1
    except critic_rules.CorrectionValidationError as exc:
        print("FAIL (critic correction still invalid): {}".format(exc), file=sys.stderr)
        return 1
    except PipelineError as exc:
        print("FAIL (pipeline): {}".format(exc), file=sys.stderr)
        return 1
    except OSError as exc:
        print("FAIL (file I/O): {}".format(exc), file=sys.stderr)
        return 1

    print("Done. See outputs/, retrieval-evidence/, and critic-evidence/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
