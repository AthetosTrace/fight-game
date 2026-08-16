"""The tone judge -- two backends behind one interface.

Tone is the one criterion in this style guide that is genuinely a judgment
call. Vocabulary and lore are lookups: either the copy says "Ascension Meter"
or it says "super meter", and either it contradicts GDD 03 or it does not.
Length and shape are arithmetic. But "does this sound like Ascendant Impact"
is the kind of question a language model answers better than a regex.

So the tone criterion is pluggable, and both backends are real:

    rubric   Deterministic. Scores the markers that Pillar 1 and the GDD's
             high-concept register actually forbid -- congratulation, hype
             punctuation, hedging. Runs offline, needs no key, and gives every
             test in this suite a fixed answer to assert against.

    claude   Calls Claude with the evaluator prompt in prompts/evaluator.md and
             reads back a scored verdict. Better at the cases a phrase list
             cannot reach -- copy that is off-brand without using any banned
             word.

`rubric` is the default because the committed evidence has to be reproducible:
a run report nobody can regenerate is not evidence. `claude` is what the
assignment's own action plan describes, and the prompt it uses is a submitted
deliverable in its own right.

Both return the same `Verdict`, so the evaluator does not know or care which
one answered.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import textcheck  # noqa: E402

PROMPTS_DIR = os.path.join(HERE, "prompts")

# Claude Opus 5. Thinking is on by default on this model and `max_tokens` caps
# thinking plus response text together, so the ceiling is generous even though
# the verdict itself is a few dozen tokens.
CLAUDE_MODEL = "claude-opus-5"
CLAUDE_MAX_TOKENS = 16000

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {
            "type": "number",
            "description": "Tone score from 0.0 (fully off-brand) to 1.0 (fully on-brand).",
        },
        "reason": {
            "type": "string",
            "description": "One sentence naming which tone rule was violated and how, or confirming the line is clean.",
        },
    },
    "required": ["score", "reason"],
    "additionalProperties": False,
}


class Verdict(object):
    def __init__(self, score, reason, backend, fix_hint=None):
        self.score = max(0.0, min(1.0, float(score)))
        self.reason = reason
        self.backend = backend
        self.fix_hint = fix_hint

    def as_dict(self):
        return {
            "score": round(self.score, 3),
            "reason": self.reason,
            "backend": self.backend,
            "fix_hint": self.fix_hint,
        }


def load_prompt(name):
    with open(os.path.join(PROMPTS_DIR, name), "r", encoding="utf-8") as handle:
        return handle.read()


def _rule(rules_doc, rule_id):
    for rule in rules_doc["rules"]:
        if rule["id"] == rule_id:
            return rule
    raise KeyError(rule_id)


# ---------------------------------------------------------------------------
# Backend 1 -- the deterministic rubric
# ---------------------------------------------------------------------------

class RubricJudge(object):
    """Scores tone from the markers the GDD's own register forbids.

    Deductions are weighted by how far each marker moves the line off-brand.
    Congratulation is the heaviest because it contradicts a design pillar
    rather than a style preference: Pillar 1 makes the spectacle the reward, so
    copy that hands out praise has changed what the game rewards.
    """

    name = "rubric"

    def score(self, line, rules_doc):
        text = line["text"]
        faults = []
        deduction = 0.0

        t1 = _rule(rules_doc, "T1")
        praise = textcheck.unnegated_phrase(text, t1["forbidden_phrases"])
        if praise:
            deduction += 0.5
            faults.append("congratulates the player (%r) -- Pillar 1 makes the "
                          "spectacle the reward, not applause" % praise)

        t2 = _rule(rules_doc, "T2")
        exclamations = textcheck.count_exclamations(text)
        if exclamations > t2["max_exclamations"]:
            deduction += 0.3
            faults.append("uses %d exclamation mark(s); the GDD's register allows %d"
                          % (exclamations, t2["max_exclamations"]))
        if textcheck.unnegated_pattern(text, t2.get("forbidden_patterns", [])):
            deduction += 0.2
            faults.append("contains an emoji or decorative symbol")

        t3 = _rule(rules_doc, "T3")
        hedge = textcheck.unnegated_phrase(text, t3["forbidden_phrases"])
        if hedge:
            deduction += 0.3
            faults.append("hedges (%r) where combat copy must assert" % hedge)

        if not faults:
            return Verdict(1.0, "clipped, declarative, and claims no reward the "
                                "player did not earn", self.name)
        return Verdict(1.0 - deduction, "; ".join(faults), self.name,
                       fix_hint="strip the praise, punctuation, and hedging; state what happened")


# ---------------------------------------------------------------------------
# Backend 2 -- Claude
# ---------------------------------------------------------------------------

class ClaudeJudge(object):
    """Sends the line and the tone rules to Claude and reads back a verdict.

    The prompt is `prompts/evaluator.md`, which is a submitted deliverable --
    the assignment asks for the evaluator's prompt, not only its output.
    """

    name = "claude"

    def __init__(self, model=CLAUDE_MODEL, client=None):
        self.model = model
        self._client = client

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        try:
            import anthropic
        except ImportError:
            raise RuntimeError(
                "the claude judge needs the Anthropic SDK: python -m pip install anthropic")
        try:
            self._client = anthropic.Anthropic()
        except Exception as exc:  # missing credentials surface here
            raise RuntimeError("could not construct an Anthropic client: %s" % exc)
        return self._client

    def _render_prompt(self, line, rules_doc):
        tone_rules = [_rule(rules_doc, rule_id) for rule_id in ("T1", "T2", "T3")]
        rendered = []
        for rule in tone_rules:
            rendered.append("- **%s (%s)** %s\n  GDD: %s"
                            % (rule["id"], rule["title"], rule["statement"], rule["gdd_source"]))
        spec = rules_doc["slots"][line["slot"]]
        return load_prompt("evaluator.md").format(
            tone_rules="\n".join(rendered),
            slot=line["slot"],
            moment=spec["moment"],
            text=line["text"],
        )

    def score(self, line, rules_doc):
        import anthropic

        client = self._ensure_client()
        prompt = self._render_prompt(line, rules_doc)
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=CLAUDE_MAX_TOKENS,
                output_config={
                    "effort": "medium",
                    "format": {"type": "json_schema", "schema": VERDICT_SCHEMA},
                },
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.NotFoundError as exc:
            raise RuntimeError("model %r not available: %s" % (self.model, exc))
        except anthropic.RateLimitError as exc:
            raise RuntimeError("rate limited by the Claude API: %s" % exc)
        except anthropic.APIStatusError as exc:
            raise RuntimeError("Claude API error %s: %s" % (exc.status_code, exc))
        except anthropic.APIConnectionError as exc:
            raise RuntimeError("could not reach the Claude API: %s" % exc)

        # A refusal returns HTTP 200 with an empty or partial content list, so
        # the stop reason has to be checked before indexing into content.
        if response.stop_reason == "refusal":
            raise RuntimeError("Claude declined to score this line")

        text = next((block.text for block in response.content if block.type == "text"), None)
        if text is None:
            raise RuntimeError("Claude returned no text block to parse")

        payload = json.loads(text)
        return Verdict(payload["score"], payload["reason"], self.name,
                       fix_hint="apply the evaluator's reason to the line")


# ---------------------------------------------------------------------------
# Backend 3 -- recorded Claude verdicts
# ---------------------------------------------------------------------------

VERDICTS_PATH = os.path.join(HERE, "verdicts", "claude_session.json")


class SessionJudge(object):
    """Replays tone verdicts Claude Opus 5 actually produced for these lines.

    The `claude` backend above is the live path, and it cannot be exercised
    without an API key -- which means it cannot produce committed evidence that
    someone else can regenerate. This backend closes that gap from the other
    side: the verdicts in verdicts/claude_session.json were produced by Claude
    Opus 5 reading the rendered output of prompts/evaluator.md, and replaying
    them makes a model-graded run reproducible offline.

    It is deliberately **strict**. Falling back to the rubric on a miss would
    silently mix a deterministic verdict into a run labelled model-graded, and
    the label would then be a lie for some fraction of the lines.
    """

    name = "session"

    def __init__(self, path=VERDICTS_PATH):
        with open(path, "r", encoding="utf-8") as handle:
            document = json.load(handle)
        self.model = document["model"]
        self._recorded = {
            (entry["slot"], entry["text"]): entry for entry in document["verdicts"]
        }

    def score(self, line, rules_doc):
        entry = self._recorded.get((line["slot"], line["text"]))
        if entry is None:
            raise RuntimeError(
                "no recorded Claude verdict for %s / %r -- record one in %s or run "
                "with --judge rubric" % (line["slot"], line["text"], VERDICTS_PATH))
        return Verdict(entry["score"], entry["reason"], self.name,
                       fix_hint="apply the evaluator's reason to the line")


BACKENDS = {"rubric": RubricJudge, "claude": ClaudeJudge, "session": SessionJudge}


def get_judge(name):
    try:
        return BACKENDS[name]()
    except KeyError:
        raise KeyError("unknown judge backend %r; choose from %s"
                       % (name, ", ".join(sorted(BACKENDS))))
