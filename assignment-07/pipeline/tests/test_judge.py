"""judge -- the deterministic backend, and the contract the Claude one honours."""

import pytest
from conftest import line

import judge as judge_module


# ---------------------------------------------------------------------------
# The factory
# ---------------------------------------------------------------------------

def test_all_backends_are_registered():
    assert set(judge_module.BACKENDS) == {"rubric", "claude", "session"}


def test_unknown_backend_raises():
    with pytest.raises(KeyError):
        judge_module.get_judge("gpt")


def test_default_backend_is_the_reproducible_one(rules_doc):
    """The committed evidence has to be regenerable by anyone who clones this
    repo, so the offline backend is the default."""
    import evaluator
    evaluation = evaluator.evaluate(
        line("loss_screen", "The evaluation ends here. Crimson Vanguard still stands."),
        rules_doc)
    tone = next(c for c in evaluation["criteria"] if c["criterion"] == "tone")
    assert tone["backend"] == "rubric"


# ---------------------------------------------------------------------------
# The rubric backend
# ---------------------------------------------------------------------------

def test_rubric_passes_canonical_copy(rules_doc, rubric_judge):
    verdict = rubric_judge.score(
        line("meter_feedback_counter", "Counter landed. Ascension rising."), rules_doc)
    assert verdict.score == 1.0
    assert verdict.backend == "rubric"


@pytest.mark.parametrize("text", [
    "Nice work. Ascension rising.",
    "Counter landed. Ascension rising!",
    "Maybe counter landed.",
])
def test_rubric_penalises_off_register_copy(rules_doc, rubric_judge, text):
    verdict = rubric_judge.score(line("meter_feedback_counter", text), rules_doc)
    assert verdict.score < 1.0
    assert verdict.reason.strip()


def test_rubric_is_deterministic(rules_doc, rubric_judge):
    text = line("loss_screen", "Amazing! Maybe the boss fell!!")
    first = rubric_judge.score(text, rules_doc)
    second = rubric_judge.score(text, rules_doc)
    assert first.score == second.score
    assert first.reason == second.reason


def test_rubric_stacks_deductions(rules_doc, rubric_judge):
    one = rubric_judge.score(line("loss_screen", "Nice work. It ended."), rules_doc).score
    several = rubric_judge.score(line("loss_screen", "Nice work! Maybe it ended!"), rules_doc).score
    assert several < one


def test_score_is_clamped_to_the_unit_interval():
    assert judge_module.Verdict(-5, "r", "t").score == 0.0
    assert judge_module.Verdict(99, "r", "t").score == 1.0


def test_rubric_carries_a_fix_hint_when_it_deducts(rules_doc, rubric_judge):
    verdict = rubric_judge.score(line("loss_screen", "Nice work. It ended."), rules_doc)
    assert verdict.fix_hint


# ---------------------------------------------------------------------------
# The Claude backend -- contract only, no network
# ---------------------------------------------------------------------------

def test_claude_prompt_renders_every_placeholder(rules_doc):
    claude = judge_module.ClaudeJudge()
    prompt = claude._render_prompt(
        line("impact_window_prompt", "STRIKE NOW!"), rules_doc)
    assert "{" not in prompt and "}" not in prompt, "an unfilled placeholder survived"
    assert "STRIKE NOW!" in prompt
    assert "impact_window_prompt" in prompt


def test_claude_prompt_carries_the_tone_rules_and_their_citations(rules_doc):
    prompt = judge_module.ClaudeJudge()._render_prompt(
        line("loss_screen", "anything"), rules_doc)
    for rule_id in ("T1", "T2", "T3"):
        assert rule_id in prompt
    assert "section 01" in prompt


def test_claude_prompt_scopes_the_model_to_tone_only(rules_doc):
    """Vocabulary, lore, length, and shape are scored deterministically. If the
    prompt did not say so, the model would double-count them."""
    prompt = judge_module.ClaudeJudge()._render_prompt(
        line("loss_screen", "anything"), rules_doc)
    # The prompt is hard-wrapped, so assert against the flattened text -- a
    # sentence split across a newline is still the instruction it carries.
    flat = " ".join(prompt.split())
    assert "on tone alone" in flat
    assert "Do not deduct for those" in flat
    assert "except tone" in flat


def test_claude_uses_the_current_opus_model_id():
    assert judge_module.CLAUDE_MODEL == "claude-opus-5"


def test_claude_max_tokens_leaves_room_for_thinking():
    """Thinking is on by default on this model and `max_tokens` caps thinking
    plus response text together, so a ceiling sized for the JSON alone would
    truncate the verdict."""
    assert judge_module.CLAUDE_MAX_TOKENS >= 8000


def test_verdict_schema_is_strict_and_complete():
    schema = judge_module.VERDICT_SCHEMA
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {"score", "reason"}


def test_claude_backend_parses_a_structured_verdict(rules_doc):
    """Exercised through a stub client so the contract is tested without a key."""
    pytest.importorskip("anthropic")

    class Block(object):
        type = "text"
        text = '{"score": 0.4, "reason": "opens with praise (T1)"}'

    class Response(object):
        stop_reason = "end_turn"
        content = [Block()]

    class Messages(object):
        def create(self, **kwargs):
            assert kwargs["model"] == judge_module.CLAUDE_MODEL
            assert kwargs["output_config"]["format"]["type"] == "json_schema"
            return Response()

    class Client(object):
        messages = Messages()

    verdict = judge_module.ClaudeJudge(client=Client()).score(
        line("loss_screen", "Nice work!"), rules_doc)
    assert verdict.score == 0.4
    assert verdict.backend == "claude"
    assert "T1" in verdict.reason


def test_claude_backend_surfaces_a_refusal_rather_than_indexing_content(rules_doc):
    """A refusal returns HTTP 200 with empty content, so the stop reason has to
    be checked before reading `content[0]`."""
    pytest.importorskip("anthropic")

    class Response(object):
        stop_reason = "refusal"
        content = []

    class Messages(object):
        def create(self, **kwargs):
            return Response()

    class Client(object):
        messages = Messages()

    with pytest.raises(RuntimeError, match="declined"):
        judge_module.ClaudeJudge(client=Client()).score(
            line("loss_screen", "anything"), rules_doc)


# ---------------------------------------------------------------------------
# The session backend -- replayed Claude verdicts
# ---------------------------------------------------------------------------

def test_session_backend_replays_a_recorded_verdict(rules_doc):
    session = judge_module.get_judge("session")
    verdict = session.score(
        line("meter_feedback_counter", "Counter landed. Ascension rising."), rules_doc)
    assert verdict.score == 1.0
    assert verdict.backend == "session"


def test_session_backend_records_the_model_it_came_from():
    assert judge_module.get_judge("session").model == judge_module.CLAUDE_MODEL


def test_session_backend_refuses_to_guess(rules_doc):
    """Strict on purpose. Falling back to the rubric would silently mix a
    deterministic verdict into a run labelled model-graded, and the label would
    then be a lie for some fraction of the lines.

    This strictness earned its keep during the build: it caught an intermediate
    line in the seed-33 chain that had been recorded from a guess rather than
    from the run.
    """
    session = judge_module.get_judge("session")
    with pytest.raises(RuntimeError, match="no recorded Claude verdict"):
        session.score(line("loss_screen", "a line nobody has judged"), rules_doc)


def test_claude_catches_off_brand_copy_the_phrase_list_cannot(rules_doc, rubric_judge):
    """The argument for the pluggable judge, asserted rather than claimed.

    'Better luck next time' uses no banned word, no exclamation mark, and no
    hedge, so the rubric scores it clean. It is still consoling copy that
    attributes the outcome to luck, in a game whose fiction frames the duel as
    a combat evaluation.
    """
    session = judge_module.get_judge("session")
    off_brand = line("loss_screen", "Better luck next time. Crimson Vanguard still stands.")
    assert rubric_judge.score(off_brand, rules_doc).score == 1.0
    assert session.score(off_brand, rules_doc).score < 0.5


def test_the_two_backends_agree_on_the_canonical_lines(rules_doc, rubric_judge, slots):
    """Where a recorded verdict exists for a canonical line, the model and the
    rubric must not disagree -- a divergence there would mean one of them has
    the register wrong."""
    session = judge_module.get_judge("session")
    for slot in slots:
        canonical = line(slot, rules_doc["slots"][slot]["canonical"])
        try:
            recorded = session.score(canonical, rules_doc)
        except RuntimeError:
            continue
        assert recorded.score == rubric_judge.score(canonical, rules_doc).score == 1.0, slot


def test_claude_backend_reports_a_missing_sdk_clearly():
    claude = judge_module.ClaudeJudge()
    try:
        import anthropic  # noqa: F401
    except ImportError:
        with pytest.raises(RuntimeError, match="pip install anthropic"):
            claude._ensure_client()
    else:
        pytest.skip("the SDK is installed, so this path is unreachable here")
