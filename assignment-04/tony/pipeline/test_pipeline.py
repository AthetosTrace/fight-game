"""Unit tests for Assignment #04's content pipeline.

Everything here is offline: no Claude CLI process is ever really invoked and
no network call is made. subprocess.run is mocked wherever llm_client's CLI
plumbing is exercised.

Run with:
    python -m unittest assignment-04/tony/pipeline/test_pipeline.py -v
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import critic_rules  # noqa: E402
import knowledge_base  # noqa: E402
import llm_client  # noqa: E402
import pipeline  # noqa: E402


# ---------------------------------------------------------------------------
# knowledge_base: heading parsing, eligible-file restriction, scoring, top-K
# ---------------------------------------------------------------------------

class ParseMarkdownChunksTests(unittest.TestCase):
    SAMPLE = """\
# Title Line Is Not A Chunk

Intro paragraph, also not a chunk.

## First Heading

Body line one.
Body line two.

## Second Heading

Only one body line.
"""

    def test_splits_on_level_two_headings(self):
        chunks = knowledge_base.parse_markdown_chunks(self.SAMPLE, "sample.md")
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].heading, "First Heading")
        self.assertEqual(chunks[1].heading, "Second Heading")

    def test_preamble_before_first_heading_is_dropped(self):
        chunks = knowledge_base.parse_markdown_chunks(self.SAMPLE, "sample.md")
        joined = " ".join(c.body for c in chunks)
        self.assertNotIn("Intro paragraph", joined)

    def test_body_text_and_source_file_are_captured(self):
        chunks = knowledge_base.parse_markdown_chunks(self.SAMPLE, "sample.md")
        self.assertIn("Body line one.", chunks[0].body)
        self.assertIn("Body line two.", chunks[0].body)
        self.assertEqual(chunks[0].source_file, "sample.md")
        self.assertEqual(chunks[1].body, "Only one body line.")

    def test_chunk_index_is_sequential(self):
        chunks = knowledge_base.parse_markdown_chunks(self.SAMPLE, "sample.md")
        self.assertEqual([c.index for c in chunks], [0, 1])


class ScoringAndTopKTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.kb_dir = Path(self.tmpdir.name)

        (self.kb_dir / "eligible.md").write_text(
            "# Eligible File\n\n"
            "## Telegraph Timing\n\n"
            "The gauntlet attack telegraph shows a committed pose and warning lights.\n\n"
            "## Unrelated Section\n\n"
            "This section is about arena doorways and framing, not attacks.\n",
            encoding="utf-8",
        )
        (self.kb_dir / "ineligible.md").write_text(
            "# Ineligible File\n\n"
            "## Telegraph Timing\n\n"
            "This file also mentions telegraph and gauntlet but must never be "
            "retrieved for this output.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_eligible_files_restrict_candidates(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query="gauntlet telegraph attack",
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=4,
        )
        sources = {sc.chunk.source_file for sc in result.candidates}
        self.assertEqual(sources, {"eligible.md"})
        self.assertNotIn("ineligible.md", sources)

    def test_scoring_is_deterministic_and_reproducible(self):
        kwargs = dict(
            slug="test-output",
            query="gauntlet telegraph attack",
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=4,
        )
        first = knowledge_base.retrieve(**kwargs)
        second = knowledge_base.retrieve(**kwargs)
        self.assertEqual(
            [(sc.chunk.heading, sc.score) for sc in first.candidates],
            [(sc.chunk.heading, sc.score) for sc in second.candidates],
        )

    def test_higher_overlap_chunk_ranks_first(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query="gauntlet telegraph attack",
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=4,
        )
        self.assertEqual(result.candidates[0].chunk.heading, "Telegraph Timing")

    def test_top_k_limits_selected_count(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query="gauntlet telegraph attack arena doorway framing",
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=1,
        )
        self.assertLessEqual(len(result.selected), 1)

    def test_zero_score_chunks_are_excluded_from_selected_but_kept_in_candidates(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query="gauntlet telegraph attack",
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=4,
        )
        zero_score_headings = {
            sc.chunk.heading for sc in result.candidates if sc.score == 0
        }
        selected_headings = {sc.chunk.heading for sc in result.selected}
        self.assertTrue(
            zero_score_headings,
            "fixture should include an unrelated, zero-score chunk",
        )
        self.assertFalse(zero_score_headings & selected_headings)
        # The zero-score chunk must still be visible in the full evidence trail.
        self.assertIn(
            "Unrelated Section", {sc.chunk.heading for sc in result.candidates}
        )

# ---------------------------------------------------------------------------
# knowledge_base: required (pinned) chunks - audit-fix coverage
# ---------------------------------------------------------------------------

class RequiredChunksTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.kb_dir = Path(self.tmpdir.name)
        self.query = (
            "gauntlet telegraph attack readable range purpose crimson vanguard "
            "authored four"
        )
        (self.kb_dir / "eligible.md").write_text(
            "# Eligible File\n\n"
            "## High Score Heading\n\n"
            "gauntlet telegraph attack readable range purpose crimson vanguard "
            "authored four\n\n"
            "## Low Score Required Heading\n\n"
            "This section barely overlaps with the query at all, just one "
            "relevant token: telegraph.\n\n"
            "## Zero Score Heading\n\n"
            "Nothing relevant here whatsoever, completely unrelated content.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_required_chunk_included_outside_top_k(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query=self.query,
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=1,
            required_chunks=(("eligible.md", "Low Score Required Heading"),),
        )
        selected_headings = [sc.chunk.heading for sc in result.selected]
        self.assertIn("Low Score Required Heading", selected_headings)
        # Confirms it truly fell outside the lexical top-1 cut.
        lexical_only = knowledge_base.retrieve(
            slug="test-output", query=self.query, eligible_files=("eligible.md",),
            kb_dir=self.kb_dir, top_k=1,
        )
        self.assertNotIn(
            "Low Score Required Heading",
            [sc.chunk.heading for sc in lexical_only.selected],
        )

    def test_required_chunk_reason_is_required_when_outside_top_k(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query=self.query,
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=1,
            required_chunks=(("eligible.md", "Low Score Required Heading"),),
        )
        headings = [sc.chunk.heading for sc in result.selected]
        idx = headings.index("Low Score Required Heading")
        self.assertEqual(result.selection_reasons[idx], knowledge_base.SELECTED_BY_REQUIRED)

    def test_required_chunk_dedup_when_already_in_top_k(self):
        result = knowledge_base.retrieve(
            slug="test-output",
            query=self.query,
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=4,
            required_chunks=(("eligible.md", "High Score Heading"),),
        )
        headings = [sc.chunk.heading for sc in result.selected]
        self.assertEqual(headings.count("High Score Heading"), 1)
        idx = headings.index("High Score Heading")
        self.assertEqual(result.selection_reasons[idx], knowledge_base.SELECTED_BY_BOTH)

    def test_selected_ordering_is_deterministic_with_required_chunks(self):
        kwargs = dict(
            slug="test-output",
            query=self.query,
            eligible_files=("eligible.md",),
            kb_dir=self.kb_dir,
            top_k=1,
            required_chunks=(("eligible.md", "Low Score Required Heading"),),
        )
        first = knowledge_base.retrieve(**kwargs)
        second = knowledge_base.retrieve(**kwargs)
        self.assertEqual(
            [sc.chunk.heading for sc in first.selected],
            [sc.chunk.heading for sc in second.selected],
        )
        self.assertEqual(first.selection_reasons, second.selection_reasons)
        # Lexical top-K always precedes the required-only tail.
        self.assertEqual(
            [sc.chunk.heading for sc in first.selected],
            ["High Score Heading", "Low Score Required Heading"],
        )

    def test_missing_required_chunk_raises(self):
        with self.assertRaises(ValueError):
            knowledge_base.retrieve(
                slug="test-output",
                query=self.query,
                eligible_files=("eligible.md",),
                kb_dir=self.kb_dir,
                top_k=1,
                required_chunks=(("eligible.md", "Nonexistent Heading"),),
            )


class ImpactWindowRequiredChunksIntegrationTests(unittest.TestCase):
    """Verifies the real pipeline config for impact-window-beat-pack pins
    both restoration-caveat headings the 2026-07-28 audit found missing."""

    def test_impact_window_output_config_pins_both_restoration_headings(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        headings = {heading for (_source, heading) in output_cfg.get("required_chunks", ())}
        self.assertTrue(any("restoration rule" in h.lower() for h in headings))
        self.assertTrue(
            any(h.startswith("OPEN") and "restoration gaps" in h.lower() for h in headings)
        )

    def test_impact_window_retrieval_selects_both_required_headings(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        selected_keys = {(sc.chunk.source_file, sc.chunk.heading) for sc in result.selected}
        for key in output_cfg["required_chunks"]:
            self.assertIn(key, selected_keys)

    def test_impact_window_prompt_carries_the_new_generation_constraint(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        prompt = pipeline.build_generation_prompt(output_cfg, result)
        self.assertIn("still marked OPEN", prompt)
        self.assertIn("camera-ownership", prompt)

    def test_impact_window_prompt_forbids_unsupported_weapons_and_equipment(self):
        # 2026-07-28 grounding pass: the retrieved canon never establishes a
        # weapon/gear for Echo or Nova, so the prompt must explicitly forbid
        # inventing one (the earlier draft invented "blade angle").
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        prompt = pipeline.build_generation_prompt(output_cfg, result)
        self.assertIn("weapon", prompt.lower())
        self.assertIn("gear", prompt.lower())
        self.assertIn("armor feature", prompt.lower())

    def test_impact_window_prompt_anchors_echo_and_nova_to_supported_identities(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        prompt = pipeline.build_generation_prompt(output_cfg, result)
        self.assertIn("precision and controlled timing", prompt)
        self.assertIn("speed and aggressive momentum", prompt)

    def test_impact_window_prompt_requires_neutral_combat_wording(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        prompt = pipeline.build_generation_prompt(output_cfg, result)
        for term in ("guard angle", "body angle", "strike line", "stance", "momentum"):
            self.assertIn(term, prompt)
        self.assertIn("blade angle", prompt)  # named only as the forbidden phrasing
        self.assertIn("never 'blade angle'", prompt)


class VanguardPromptGroundingTests(unittest.TestCase):
    """2026-07-28 grounding pass: the four attack names are new authored
    proposals (the GDD only gives A-D range/purpose), so the prompt must
    require proposed-name labeling, ban an implied announcer/dialogue
    system, and ban the word 'countertext'."""

    def _prompt(self):
        output_cfg = knowledge_base.get_output("vanguard-telegraph-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        return pipeline.build_generation_prompt(output_cfg, result)

    def test_prompt_requires_proposed_name_labeling(self):
        prompt = self._prompt()
        self.assertIn("proposed working name", prompt)
        self.assertIn("new authored content", prompt)
        self.assertIn("pending designer review", prompt)
        self.assertIn("not an established GDD fact", prompt)

    def test_prompt_uses_playtest_readability_shorthand_label(self):
        prompt = self._prompt()
        self.assertIn("Playtest readability shorthand", prompt)

    def test_prompt_forbids_announcer_or_shipped_dialogue_system(self):
        prompt = self._prompt()
        self.assertIn("announcer system", prompt)
        self.assertIn("voice-over system", prompt)
        self.assertIn("never ", prompt)
        self.assertTrue(
            "shipped dialogue" in prompt or "ships in the game" in prompt
        )

    def test_prompt_prohibits_countertext(self):
        prompt = self._prompt()
        self.assertIn("countertext", prompt)
        self.assertIn("counterplay", prompt)
        self.assertIn("counterattack", prompt)
        self.assertIn("punish opportunity", prompt)
        # It must be named only as the forbidden word, with alternatives
        # required - never presented as an allowed term on its own.
        self.assertIn("Never write the word 'countertext'", prompt)


class AuditGroundingPromptConstraintTests(unittest.TestCase):
    """2026-07-28 human grounding audit (post-generation review): three
    generated sentences overreached what the retrieved context supports -
    an invented armor weak point, an overly broad 'never reactive' claim
    for Crimson Vanguard, and burst-duration wording that implied the
    player controls how long the burst lasts. These tests prove the
    generation prompts now carry general grounding rules against that
    class of drift, not just a ban on the exact flagged sentences."""

    def _impact_prompt(self):
        output_cfg = knowledge_base.get_output("impact-window-beat-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        return pipeline.build_generation_prompt(output_cfg, result)

    def _vanguard_prompt(self):
        output_cfg = knowledge_base.get_output("vanguard-telegraph-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        return pipeline.build_generation_prompt(output_cfg, result)

    def test_both_task_prompts_carry_the_new_semantic_constraints(self):
        impact_prompt = self._impact_prompt()
        vanguard_prompt = self._vanguard_prompt()
        self.assertIn("GROUNDING AUDIT CONSTRAINTS", impact_prompt)
        self.assertIn("GROUNDING AUDIT CONSTRAINTS", vanguard_prompt)
        # And each output's block is specific to its own drift, not a
        # copy-pasted shared block.
        self.assertIn("armor weak point", impact_prompt.lower())
        self.assertNotIn("armor weak point", vanguard_prompt.lower())
        self.assertIn("never reactive", vanguard_prompt.lower())
        self.assertNotIn("never reactive", impact_prompt.lower())

    def test_impact_prompt_distinguishes_earning_burst_from_controlling_duration(self):
        prompt = self._impact_prompt()
        self.assertIn("succeeds at the impact window input", prompt.lower())
        self.assertIn("earns the burst", prompt.lower())
        self.assertIn(
            "determines, controls, sets, or varies", prompt.lower()
        )
        self.assertIn("how long the burst lasts", prompt.lower())

    def test_impact_prompt_forbids_weak_points_but_allows_earned_opening_language(self):
        prompt = self._impact_prompt()
        for forbidden in (
            "armor weak point", "vulnerable armor location",
            "damage multiplier", "exposed component",
            "momentary structural weakness",
        ):
            self.assertIn(forbidden, prompt.lower())
        # The forbidding language must be paired with an explicit permission
        # for grounded phrasing - not a blanket ban on describing openings.
        self.assertIn("earned opening", prompt.lower())
        self.assertIn("punishable recovery", prompt.lower())
        self.assertIn("clean strike line", prompt.lower())
        self.assertIn(
            "none of that implies or requires an armor weak point",
            prompt.lower(),
        )

    def test_impact_prompt_preserves_governed_values_alongside_new_constraints(self):
        # The new constraints must be additive - the pre-existing
        # response-time/meter-gain/equipment/restoration-gap guardrails stay
        # in the prompt unchanged.
        prompt = self._impact_prompt()
        self.assertIn("0.75", prompt)
        self.assertIn("still marked OPEN", prompt)
        self.assertIn("weapon", prompt.lower())
        self.assertIn("gear", prompt.lower())

    def test_vanguard_prompt_distinguishes_deterministic_response_from_learning(self):
        prompt = self._vanguard_prompt()
        self.assertIn("deterministic", prompt.lower())
        self.assertIn("range and cooldown", prompt.lower())
        self.assertIn("not learning", prompt.lower())
        self.assertIn("player-pattern adaptation", prompt.lower())
        self.assertIn("runtime-model behavior", prompt.lower())

    def test_vanguard_prompt_forbids_never_reactive_style_wording(self):
        prompt = self._vanguard_prompt()
        self.assertIn("never reactive", prompt.lower())
        self.assertIn("non-reactive", prompt.lower())
        self.assertIn("does not respond to combat conditions", prompt.lower())
        # Named only as forbidden phrasing, paired with the reason it's false.
        self.assertIn("those claims are false", prompt.lower())

    def test_vanguard_prompt_preserves_existing_constraints_alongside_new_ones(self):
        # The new deterministic-response constraints must be additive - the
        # pre-existing proposed-name, playtest-shorthand, dialogue, scope,
        # and timing constraints stay in the prompt unchanged.
        prompt = self._vanguard_prompt()
        self.assertIn("proposed working name", prompt)
        self.assertIn("Playtest readability shorthand", prompt)
        self.assertIn("announcer system", prompt)
        self.assertIn("countertext", prompt)


class ShatteredRingRequiredChunkIntegrationTests(unittest.TestCase):
    """Verifies the real pipeline config for shattered-ring-reaction-pack
    pins the 'Build-side notes' chunk the 2026-07-28 grounding pass found
    was the only source directly supporting the Phase 1/Phase 2 build-status
    language this output uses."""

    BUILD_SIDE_HEADING = (
        "Build-side notes (Phase 1 vs. Phase 2 — not fiction, but "
        "constrains tone)"
    )

    def test_shattered_ring_config_pins_the_build_side_notes_heading(self):
        output_cfg = knowledge_base.get_output("shattered-ring-reaction-pack")
        headings = {heading for (_source, heading) in output_cfg.get("required_chunks", ())}
        self.assertIn(self.BUILD_SIDE_HEADING, headings)

    def test_shattered_ring_retrieval_selects_the_required_heading(self):
        output_cfg = knowledge_base.get_output("shattered-ring-reaction-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        selected_keys = {(sc.chunk.source_file, sc.chunk.heading) for sc in result.selected}
        for key in output_cfg["required_chunks"]:
            self.assertIn(key, selected_keys)

    def test_shattered_ring_required_heading_is_marked_required_not_lexical(self):
        # Confirms the pin is load-bearing: the heading falls outside the
        # lexical top-K on its own and is only present because of the pin.
        output_cfg = knowledge_base.get_output("shattered-ring-reaction-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        key = ("shattered-ring-reactions.md", self.BUILD_SIDE_HEADING)
        idx = [
            (sc.chunk.source_file, sc.chunk.heading) for sc in result.selected
        ].index(key)
        self.assertEqual(
            result.selection_reasons[idx], knowledge_base.SELECTED_BY_REQUIRED
        )

    def test_shattered_ring_retrieval_is_deterministic_with_the_pin(self):
        output_cfg = knowledge_base.get_output("shattered-ring-reaction-pack")
        kwargs = dict(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        first = knowledge_base.retrieve(**kwargs)
        second = knowledge_base.retrieve(**kwargs)
        self.assertEqual(
            [sc.chunk.heading for sc in first.selected],
            [sc.chunk.heading for sc in second.selected],
        )
        self.assertEqual(first.selection_reasons, second.selection_reasons)

    def test_shattered_ring_prompt_omits_unsupported_m4_stability_gate_claim(self):
        # The generated output previously claimed M4 stability gates M5
        # presentation work - that claim is not supported by anything in
        # this pack's eligible files, so the prompt must instruct the
        # generator to omit it rather than invent support for it.
        output_cfg = knowledge_base.get_output("shattered-ring-reaction-pack")
        result = knowledge_base.retrieve(
            slug=output_cfg["slug"],
            query=output_cfg["query"],
            eligible_files=output_cfg["eligible_files"],
            required_chunks=output_cfg.get("required_chunks", ()),
        )
        prompt = pipeline.build_generation_prompt(output_cfg, result)
        self.assertIn("M4", prompt)
        self.assertIn("not established by the retrieved arena facts", prompt)
        self.assertIn("build-side production status", prompt)


class RetrievalEvidenceRenderingTests(unittest.TestCase):
    def test_render_shows_selection_reason_for_required_and_lexical_chunks(self):
        result = knowledge_base.RetrievalResult(
            slug="demo",
            query="demo query",
            eligible_files=("a.md",),
            candidates=(),
            selected=(
                knowledge_base.ScoredChunk(
                    chunk=knowledge_base.Chunk("a.md", "Lexical Heading", "body one", 0),
                    score=5, matched_tokens=("demo",),
                ),
                knowledge_base.ScoredChunk(
                    chunk=knowledge_base.Chunk("a.md", "Required Heading", "body two", 1),
                    score=0, matched_tokens=(),
                ),
            ),
            selection_reasons=(
                knowledge_base.SELECTED_BY_LEXICAL,
                knowledge_base.SELECTED_BY_REQUIRED,
            ),
            required_chunks=(("a.md", "Required Heading"),),
            top_k=1,
        )
        rendered = pipeline.render_retrieval_evidence(result)
        self.assertIn("Lexical Heading", rendered)
        self.assertIn("Required Heading", rendered)
        self.assertIn(knowledge_base.SELECTED_BY_LEXICAL, rendered)
        self.assertIn(knowledge_base.SELECTED_BY_REQUIRED, rendered)
        self.assertIn("Required (pinned) chunks:", rendered)


# ---------------------------------------------------------------------------
# critic_rules: all seven detectors, positive + negative, and the fixture
# ---------------------------------------------------------------------------

class CriticRuleTests(unittest.TestCase):
    def test_rule_1_positive_nova_as_boss(self):
        text = "Nova stands as the game's authored rival and final boss for this duel."
        result = critic_rules.check_rule_1_nova_as_boss(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 1)

    def test_rule_1_negative_nova_correctly_described(self):
        text = (
            "Nova is a selectable player avatar, not the boss; Crimson Vanguard "
            "is the sole AI opponent."
        )
        self.assertIsNone(critic_rules.check_rule_1_nova_as_boss(text))

    def test_rule_2_positive_runtime_learning(self):
        text = "Crimson Vanguard learns from the player and adapts its attacks in real time."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negative_deterministic_language(self):
        text = "An authored state machine selects among four fixed attacks by range and cooldown."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_false_positive_protection_adapt_to_phase_2(self):
        text = "The core loop asks the player to escalate and adapt to Phase 2 once it begins."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_false_positive_protection_adapt_to_phase_2_alongside_vanguard(self):
        # Confirms the new adaptive-phrase additions don't collaterally catch
        # the canonical, one-time-authored-escalation phrasing even when
        # Crimson Vanguard and "Phase 2" appear in the same sentence.
        text = (
            "Crimson Vanguard commits to its same four authored attacks and "
            "simply adapts to Phase 2 once health crosses 50%, with no new tools."
        )
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_positive_tracks_the_players_patterns(self):
        text = "Crimson Vanguard tracks the player's patterns and reacts accordingly."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_tracks_player_patterns(self):
        text = "Crimson Vanguard tracks player patterns across the whole duel."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_least_anticipated(self):
        text = "Crimson Vanguard favors whichever attack has been least anticipated."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_predicts_the_players_habits(self):
        text = "Crimson Vanguard predicts the player's habits before it ever strikes."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_studies_the_players_behavior(self):
        text = "Crimson Vanguard studies the player's behavior between exchanges."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    # -- 2026-07-28 audit fix: Rule 2 negation-awareness ---------------------

    def test_rule_2_false_positive_protection_authored_deterministic_no_runtime_calls(self):
        # The exact canon-correct sentence the audit found incorrectly
        # flagged - "no runtime model calls" and "no ... adaptive selection"
        # are each negated within their own comma-separated clause.
        text = (
            "Authored, deterministic AI behavior — no runtime model calls, "
            "no learned or adaptive selection."
        )
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_does_not_learn_from_player(self):
        text = "Crimson Vanguard does not learn from the player."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_never_adapts_at_runtime(self):
        text = "The boss never adapts its attacks at runtime."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_no_adaptive_selection(self):
        text = "There is no adaptive selection."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_cannot_predict_habits(self):
        text = "The system cannot predict the player's habits."
        # Prove this sentence genuinely contains a Rule 2 trigger occurrence
        # first - otherwise a None result below would be indistinguishable
        # from "nothing matched" rather than "negation correctly suppressed
        # a real match".
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("predict the player's habits", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_positive_can_predict_the_players_habits(self):
        text = "The system can predict the player's habits."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("predict the player's habits", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_learns_from_the_player_bare(self):
        text = "Crimson Vanguard learns from the player."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_adapts_its_attacks_at_runtime(self):
        text = "The boss adapts its attacks at runtime."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_uses_adaptive_selection(self):
        text = "The AI uses adaptive selection."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_predicts_the_players_habits_bare(self):
        text = "The system predicts the player's habits."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_tracks_the_players_patterns_bare(self):
        text = "The boss tracks the player's patterns."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negation_in_one_clause_does_not_hide_violation_in_another(self):
        # "no fixed order" is a real, canon-correct negation, but it lives in
        # a different clause than the affirmative "it learns from the
        # player" - the negation must not launder that second clause.
        text = "The system has no fixed order, and it learns from the player."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("learns from the player", result.matched_sentence.lower())

    def test_rule_2_negation_in_one_sentence_does_not_hide_violation_in_next(self):
        # Same idea across a sentence boundary rather than a clause boundary.
        text = (
            "The boss does not use random attacks. It adapts to the player "
            "at runtime."
        )
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("adapts to the player at runtime", result.matched_sentence.lower())

    # -- 2026-07-28 audit fix (revised): negation scoped to the trigger -----
    # occurrence itself, not the whole comma/semicolon clause, so unrelated
    # negation earlier in a clause can no longer launder an affirmative
    # trigger later in that same clause.

    def test_rule_2_unrelated_negation_before_and_does_not_suppress_trigger(self):
        text = "The boss does not use random attacks and adapts to the player at runtime."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_unrelated_negation_before_but_does_not_suppress_trigger(self):
        text = "The system is not random but learns from the player."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negated_first_clause_does_not_suppress_but_clause(self):
        text = "The boss does not learn from the player but adapts its attacks at runtime."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negative_compound_denial_across_or(self):
        # A single negation governing two verb phrases joined by "or" must
        # still pass - "or" is not treated as a hard boundary the way
        # "and"/"but" are, since negation naturally distributes across it.
        # Both "learn from the player" and "adapt at runtime" are real
        # trigger phrases (see the base-form additions below), so this
        # proves the negation logic actually suppressed two genuine
        # matches - it is not passing because nothing matched.
        text = "The boss does not learn from the player or adapt at runtime."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    # -- 2026-07-28 audit fix (second revision): base-form triggers, and ----
    # every occurrence of a trigger phrase (not just the first) is checked.

    def test_rule_2_positive_base_form_can_learn_from_the_player(self):
        text = "The boss can learn from the player."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_base_form_can_adapt_at_runtime(self):
        text = "The boss can adapt at runtime."
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negative_base_form_cannot_learn_from_the_player(self):
        text = "The boss cannot learn from the player."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_never_adapts_at_runtime_bare(self):
        text = "The boss never adapts at runtime."
        # Same non-vacuous proof as above: confirm the trigger genuinely
        # matches before asserting negation suppressed it.
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adapts at runtime", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_positive_adapts_at_runtime_bare(self):
        text = "The boss adapts at runtime."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adapts at runtime", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negated_first_occurrence_does_not_hide_later_affirmative_occurrence(self):
        # Same trigger phrase, twice: the first occurrence is negated by
        # "never", but "but later" starts a fresh affirmative clause with a
        # second, unnegated occurrence of the exact same phrase. Relying on
        # str.find() (first occurrence only) would wrongly stop at the
        # negated first hit and miss this.
        text = (
            "The boss never adapts to the player at runtime but later "
            "adapts to the player at runtime."
        )
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_negated_first_occurrence_of_different_phrase_family_does_not_hide_later_one(self):
        text = (
            "The system does not use adaptive selection but its backup "
            "mode uses adaptive selection."
        )
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    # -- 2026-07-28 audit fix (list-level governing-negation revision): a
    # leading quantified negator ("nothing below implies") or a negated
    # assertion predicate ("the text does not claim") governs every Rule 2
    # trigger coordinated as its object, across commas and "or"/"nor", the
    # same way Rule 4's list-negation fix governs Rule 4's arena/attack
    # triggers. This is the exact false positive the fix targets, plus its
    # generalizations. -------------------------------------------------------

    def test_rule_2_negative_nothing_below_implies_enumeration(self):
        # The exact false-positive sentence from the audit: "nothing below
        # implies" governs all three comma/"or"-joined list items, including
        # the final "a runtime model call", even though the governing
        # phrase itself follows an unrelated introductory clause joined by
        # an em dash (not one of the recognized assertion boundaries).
        text = (
            "Crimson Vanguard is deterministic authored logic (state "
            "machine / Behavior Tree) — nothing below implies "
            "learning, adaptation, or a runtime model call."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("runtime model call", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_nothing_here_suggests_enumeration(self):
        text = (
            "Nothing here suggests adaptive selection, player-pattern "
            "tracking, or runtime model calls."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIn("runtime model call", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_none_of_this_describes_enumeration(self):
        text = (
            "None of this describes Crimson Vanguard that learns from the "
            "player, adapts at runtime, or calls an AI model."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("learns from the player", matched_phrases)
        self.assertIn("adapts at runtime", matched_phrases)
        self.assertIn("calls an ai model", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_text_does_not_claim_enumeration(self):
        text = (
            "The text does not claim Crimson Vanguard learns from the "
            "player, adapts at runtime, or calls an AI model."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("learns from the player", matched_phrases)
        self.assertIn("adapts at runtime", matched_phrases)
        self.assertIn("calls an ai model", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_design_never_implies_enumeration(self):
        text = (
            "The design never implies adaptive selection, runtime "
            "generation, or player-pattern prediction."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_section_cannot_suggest_enumeration(self):
        text = (
            "This section cannot suggest the boss learns from the player "
            "or adapts at runtime."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("learns from the player", matched_phrases)
        self.assertIn("adapts at runtime", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_positive_list_negation_stops_at_but(self):
        text = "Nothing below is random, but Crimson Vanguard learns from the player."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("learns from the player", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_list_negation_stops_at_semicolon(self):
        text = "Nothing here implies learning; Phase 2 uses adaptive selection."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)

    def test_rule_2_positive_negated_predicate_stops_at_but(self):
        text = "The text does not describe Phase 1, but Phase 2 adapts at runtime."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adapts at runtime", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("adapts at runtime", result.matched_sentence.lower())

    def test_rule_2_positive_negated_predicate_stops_at_yet(self):
        text = (
            "The design never implies runtime generation, yet the boss "
            "predicts the player's habits."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("predicts the player's habits", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("predicts the player's habits", result.matched_sentence.lower())

    def test_rule_2_positive_negated_predicate_stops_at_and(self):
        # A comma-plus-"and" that opens a fresh clause with its own subject
        # ("Crimson Vanguard") and predicate ("learns") is a genuine
        # assertion boundary, not the Oxford-comma list ending - so the
        # first "runtime model call" is governed by "does not claim" but
        # the second clause's "learns from the player" is not.
        text = (
            "The text does not claim runtime model calls, and Crimson "
            "Vanguard learns from the player."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("runtime model call", matched_phrases)
        self.assertIn("learns from the player", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("learns from the player", result.matched_sentence.lower())

    def test_rule_2_positive_unrelated_not_does_not_suppress_later_trigger(self):
        # Proves requirement #4: an earlier, unrelated "not" ("is not
        # random") is not a governing negator paired with an assertion verb,
        # and must never blanket-suppress a later, real trigger occurrence.
        text = "The system is not random and adapts at runtime."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adapts at runtime", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("adapts at runtime", result.matched_sentence.lower())

    def test_rule_2_positive_list_negation_same_trigger_negated_then_flagged(self):
        # Repeated-trigger test: the first "runtime model call" sits inside
        # the "Nothing below implies ..." clause and is governed by it, but
        # the identical phrase recurs after "but", in a fresh clause with no
        # governing negator of its own, and that occurrence must still be
        # flagged.
        text = (
            "Nothing below implies runtime model calls, but Phase 2 makes "
            "runtime model calls."
        )
        occurrences = critic_rules._rule2_all_occurrences(text.lower())
        matched_phrases = {phrase for _, phrase in occurrences}
        self.assertIn("runtime model call", matched_phrases)
        self.assertGreaterEqual(
            sum(1 for _, phrase in occurrences if phrase == "runtime model call"), 2
        )
        # Direct proof the first occurrence alone is suppressed: taken on
        # its own (before "but"), the governing negation covers it.
        first_clause_alone = "Nothing below implies runtime model calls."
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(first_clause_alone))
        # The full sentence must still be flagged - only the second,
        # post-"but" occurrence can be the cause, since the first is proven
        # suppressed above.
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("runtime model call", result.matched_sentence.lower())

    # -- 2026-07-28 audit fix (bare-"and" assertion-boundary revision): a
    # bare "and" (no preceding comma) is a boundary only when an explicit
    # new subject phrase - not just a bare article/list modifier - stands
    # between it and the next Rule 2 trigger. -------------------------------

    def test_rule_2_negative_does_not_claim_bare_and_coordinated_triggers(self):
        # Both triggers are directly coordinated objects of "does not
        # claim" - the bare "and" has nothing but whitespace before the
        # second trigger, so it must not split.
        text = "The text does not claim adaptive selection and runtime model calls."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIn("runtime model call", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_nothing_here_suggests_bare_and_coordinated_triggers(self):
        text = "Nothing here suggests adaptive selection and runtime model calls."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIn("runtime model call", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_negative_does_not_claim_bare_and_shared_subject_predicates(self):
        # "Crimson Vanguard" is the shared subject of both coordinated verb
        # phrases ("learns ... and adapts ..."); the second trigger begins
        # immediately after the bare "and", so it must not split.
        text = (
            "The text does not claim Crimson Vanguard learns from the "
            "player and adapts at runtime."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("learns from the player", matched_phrases)
        self.assertIn("adapts at runtime", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_2_runtime_learning(text))

    def test_rule_2_positive_does_not_claim_bare_and_new_subject_flags(self):
        # The false-negative hole this fix closes: "Crimson Vanguard learns
        # from the player" is an explicit new subject+predicate after the
        # bare "and", not a coordinated object of "does not claim" - it must
        # split and flag.
        text = (
            "The text does not claim adaptive selection and Crimson "
            "Vanguard learns from the player."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIn("learns from the player", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("learns from the player", result.matched_sentence.lower())

    def test_rule_2_positive_never_implies_bare_and_new_subject_flags(self):
        text = (
            "The design never implies runtime generation and the boss "
            "predicts the player's habits."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("predicts the player's habits", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("predicts the player's habits", result.matched_sentence.lower())

    def test_rule_2_positive_nothing_here_suggests_bare_and_new_subject_flags(self):
        text = "Nothing here suggests runtime model calls and Phase 2 adapts at runtime."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("runtime model call", matched_phrases)
        self.assertIn("adapts at runtime", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("adapts at runtime", result.matched_sentence.lower())

    def test_rule_2_positive_cannot_suggest_bare_and_new_subject_flags(self):
        text = (
            "This section cannot suggest adaptive selection and the system "
            "tracks the player's patterns."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule2_all_occurrences(text.lower())
        }
        self.assertIn("adaptive selection", matched_phrases)
        self.assertIn("tracks the player's patterns", matched_phrases)
        result = critic_rules.check_rule_2_runtime_learning(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 2)
        self.assertIn("tracks the player's patterns", result.matched_sentence.lower())

    def test_rule_3_positive_free_impact_window(self):
        text = "The first Impact Window automatically succeeds without player input."
        result = critic_rules.check_rule_3_free_impact_window(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 3)

    def test_rule_3_negative_requires_input(self):
        text = "The Impact Window opens only after a correctly timed perfect dodge or counter."
        self.assertIsNone(critic_rules.check_rule_3_free_impact_window(text))

    def test_rule_3_negative_false_positive_nothing_presses_or_converts(self):
        # The exact canon-correct sentence the 2026-07-28 audit found
        # incorrectly flagged - "nothing" negates both trigger phrases in
        # the same sentence.
        text = (
            "Nothing about this window presses the input for the player or "
            "converts a miss into a success."
        )
        self.assertIsNone(critic_rules.check_rule_3_free_impact_window(text))

    def test_rule_3_negative_does_not_press_the_input(self):
        text = "The game does not press the input for the player."
        self.assertIsNone(critic_rules.check_rule_3_free_impact_window(text))

    def test_rule_3_negative_miss_never_converted(self):
        text = "A miss is never converted into success."
        self.assertIsNone(critic_rules.check_rule_3_free_impact_window(text))

    def test_rule_3_positive_presses_the_input_for_the_player(self):
        text = "The game presses the input for the player."
        result = critic_rules.check_rule_3_free_impact_window(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 3)

    def test_rule_3_positive_miss_converts_into_success(self):
        text = "A miss converts into success."
        result = critic_rules.check_rule_3_free_impact_window(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 3)

    def test_rule_3_positive_automatically_succeeds(self):
        text = "The Impact Window automatically succeeds."
        result = critic_rules.check_rule_3_free_impact_window(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 3)

    def test_rule_3_positive_holding_the_input_guarantees_success(self):
        text = "Holding the input guarantees success."
        result = critic_rules.check_rule_3_free_impact_window(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 3)

    def test_rule_4_positive_fifth_attack(self):
        text = "Crimson Vanguard unleashes Attack E, a devastating finisher unseen until Phase 2."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_second_arena(self):
        text = "The duel briefly continues in a second arena beyond the Shattered Ring."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)

    def test_rule_4_negative_four_authored_attacks(self):
        text = "Attack A and Attack B are two of the four authored attacks used in both phases."
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    # -- 2026-07-28 audit fix: Rule 4 arena/attack trigger-local negation ----

    def test_rule_4_negative_false_positive_functional_requirements_sentence(self):
        # The exact canon-correct sentence the audit found incorrectly
        # flagged - "no second space", "no alternate version of the Ring",
        # and "nothing off-screen" are each a denial, not an assertion.
        text = (
            "No reaction is described for anything beyond the central floor, "
            "the far doorway, and the surrounding walls/ceiling rig already "
            "specified in the arena's functional requirements — no second "
            "space, no alternate version of the Ring, nothing off-screen."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("alternate version of the ring", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_no_second_space_or_alternate_version(self):
        text = "There is no second space or alternate version of the Ring."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("alternate version of the ring", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_duel_never_leaves_shattered_ring(self):
        text = "The duel never leaves Shattered Ring."
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_no_additional_arena_introduced(self):
        text = "No additional arena is introduced."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("additional arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_no_fifth_attack(self):
        text = "Crimson Vanguard has no fifth attack."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("fifth attack", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_positive_second_space(self):
        text = "The duel shifts to a second space."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_alternate_version_of_the_ring(self):
        text = "Phase 2 uses an alternate version of the Ring."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_second_arena_opens(self):
        text = "A second arena opens after the Impact Window."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_gains_a_fifth_attack(self):
        text = "Crimson Vanguard gains a fifth attack."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_new_rival_attack(self):
        text = "Phase 2 introduces a new rival attack."
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_negated_first_occurrence_does_not_hide_later_alternate_ring(self):
        # "no second space" is correctly negated, but the "but" clause that
        # follows starts a fresh, independently-true (and violating)
        # statement - relying on whole-sentence negation would wrongly clear
        # this whole sentence.
        text = (
            "There is no second space at first, but Phase 2 uses an "
            "alternate version of the Ring."
        )
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("alternate version of the ring", result.matched_sentence.lower())

    def test_rule_4_negated_fifth_attack_does_not_hide_later_second_arena(self):
        text = (
            "Crimson Vanguard has no fifth attack, but the duel moves to a "
            "second arena."
        )
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("second arena", result.matched_sentence.lower())

    def test_rule_4_unrelated_negation_does_not_hide_second_space_after_semicolon(self):
        text = (
            "The duel does not leave through the doorway; instead, a second "
            "space opens beneath the arena."
        )
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("second space", result.matched_sentence.lower())

    # -- 2026-07-28 audit fix (list-negation revision): a leading "None" /
    # "Nothing" / "Neither" / "No <subject>" must govern every Rule 4
    # trigger later in the same enumerated list, across commas and
    # "or"/"nor", but must stop at a true assertion boundary. -------------

    def test_rule_4_negative_none_constitute_enumeration(self):
        # The exact false positive from the audit: the leading "None"
        # governs all three comma/"or"-joined list items, including the
        # final "an alternate arena state".
        text = (
            "None constitute a destructible object, a damage volume, or an "
            "alternate arena state."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("alternate arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_none_of_these_effects_enumeration(self):
        text = (
            "None of these effects creates a second arena, an alternate "
            "arena, or another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("alternate arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_no_reaction_introduces_enumeration(self):
        text = (
            "No reaction introduces a second space, alternate arena, or "
            "off-screen location."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("alternate arena", matched_phrases)
        self.assertIn("off-screen location", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_neither_nor_creates_alternate_arena(self):
        text = (
            "Neither the lighting cue nor the debris reaction creates an "
            "alternate arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("alternate arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    # -- 2026-07-28 audit fix (bare-"and" revision): a bare coordinating
    # "and" (no preceding comma) coordinates two objects of the same
    # governed verb/negator and must NOT act as an assertion boundary - only
    # a comma-plus-"and" splits off a fresh, independently-true clause. -----

    def test_rule_4_negative_none_governs_both_sides_of_bare_and(self):
        # The exact false positive from the follow-up audit: a bare "and"
        # (no comma) coordinates two objects of "creates", both still under
        # "None"'s scope.
        text = "None of these effects creates a second arena and another arena."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_no_reaction_governs_both_sides_of_bare_and(self):
        text = (
            "No reaction introduces a second space and an alternate arena "
            "effect."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("alternate arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_neither_nor_second_arena_another_arena(self):
        text = "Neither cue creates a second arena nor another arena."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_positive_list_negation_stops_at_but(self):
        text = (
            "None are destructible, but Phase 2 introduces an alternate "
            "arena state."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("alternate arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_list_negation_stops_at_semicolon(self):
        text = "Nothing changes at first; later, a second arena opens."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)

    def test_rule_4_positive_list_negation_stops_at_but_no_additional_arena(self):
        text = (
            "No additional arena appears during Phase 1, but Phase 2 uses "
            "an alternate version of the Ring."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("additional arena", matched_phrases)
        self.assertIn("alternate version of the ring", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("alternate version of the ring", result.matched_sentence.lower())

    def test_rule_4_positive_list_negation_stops_at_and(self):
        text = (
            "No reaction introduces a second space, and Phase 2 opens "
            "another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("another arena", result.matched_sentence.lower())

    def test_rule_4_positive_list_negation_same_trigger_negated_then_flagged(self):
        # Proves list-negation is scoped per assertion segment, not per
        # trigger phrase: the first "alternate arena state" sits inside the
        # "None constitute ..." segment and is governed by it, but the
        # identical phrase recurs after "but", in a fresh segment that
        # opens with no negator of its own, and that occurrence must still
        # be flagged.
        text = (
            "None constitute an alternate arena state, but Phase 2 uses an "
            "alternate arena state."
        )
        occurrences = critic_rules._rule4_all_occurrences(text.lower())
        matched_phrases = {phrase for _, phrase in occurrences}
        self.assertIn("alternate arena", matched_phrases)
        self.assertGreaterEqual(
            sum(1 for _, phrase in occurrences if phrase == "alternate arena"), 2
        )
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("alternate arena", result.matched_sentence.lower())

    # -- 2026-07-28 audit fix (negated-governing-predicate revision): a
    # negated governing predicate ("does not describe", "does not add",
    # "never introduces", "cannot open", ...) at the start of an assertion
    # segment must govern every Rule 4 trigger coordinated as its object,
    # across commas and "or"/"nor", the same way a leading list negator
    # ("None", "No <subject>") already does. -----------------------------

    def test_rule_4_negative_does_not_describe_second_arena_or_alternate_ring(self):
        # The exact false positive from the follow-up audit: "does not
        # describe" governs all three commas/"or"-joined objects, including
        # the Oxford-comma-ending "or any location beyond what's on screen".
        text = (
            "It does not describe a second arena, an alternate version of "
            "the Ring, or any location beyond what's on screen."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("alternate version of the ring", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_does_not_add_second_space_or_off_screen(self):
        text = (
            "The pack does not add a second space, another arena, or an "
            "off-screen location."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIn("off-screen location", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_never_introduces_second_arena_alternate_or_another(self):
        text = (
            "The text never introduces a second arena, an alternate arena, "
            "or another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("alternate arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_cannot_open_second_arena_or_alternate_ring(self):
        text = (
            "The design cannot open a second arena or an alternate version "
            "of the Ring."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("alternate version of the ring", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_negative_does_not_describe_oxford_comma_ending(self):
        # The Oxford-comma-ending case: "an alternate arena, and another
        # arena" is the last coordinated object of "does not describe", not
        # a fresh clause - the trailing ", and" must not be treated as an
        # assertion boundary here.
        text = (
            "It does not describe a second arena, an alternate arena, and "
            "another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("alternate arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        self.assertIsNone(critic_rules.check_rule_4_extra_arena_or_attack(text))

    def test_rule_4_positive_negated_predicate_stops_at_but(self):
        text = (
            "It does not describe a second arena, but Phase 2 opens "
            "another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("another arena", result.matched_sentence.lower())

    def test_rule_4_positive_negated_predicate_stops_at_semicolon(self):
        text = "It does not describe a second arena; later, another arena opens."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("another arena", result.matched_sentence.lower())

    def test_rule_4_positive_negated_predicate_stops_at_and(self):
        text = (
            "It does not describe a second arena, and Phase 2 opens "
            "another arena."
        )
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second arena", matched_phrases)
        self.assertIn("another arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("another arena", result.matched_sentence.lower())

    def test_rule_4_positive_does_not_add_stops_at_but(self):
        text = "The pack does not add hazards, but it introduces an alternate arena."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("alternate arena", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("alternate arena", result.matched_sentence.lower())

    def test_rule_4_positive_unrelated_not_does_not_suppress_later_trigger(self):
        # Proves requirement #3: an earlier, unrelated "not" ("is not
        # random") is not a negated governing predicate and must never
        # blanket-suppress a later, real trigger occurrence.
        text = "The text is not random and introduces a second space."
        matched_phrases = {
            phrase for _, phrase in critic_rules._rule4_all_occurrences(text.lower())
        }
        self.assertIn("second space", matched_phrases)
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("second space", result.matched_sentence.lower())

    def test_rule_4_positive_negated_predicate_same_trigger_negated_then_flagged(self):
        # Proves the negated-governing-predicate scope is per assertion
        # segment, not per trigger phrase: the first "alternate arena" sits
        # inside the "does not describe ..." segment and is governed by it,
        # but the identical phrase recurs after "but", in a fresh segment
        # with no negated predicate of its own, and that occurrence must
        # still be flagged.
        text = (
            "It does not describe an alternate arena, but Phase 2 uses an "
            "alternate arena."
        )
        occurrences = critic_rules._rule4_all_occurrences(text.lower())
        matched_phrases = {phrase for _, phrase in occurrences}
        self.assertIn("alternate arena", matched_phrases)
        self.assertGreaterEqual(
            sum(1 for _, phrase in occurrences if phrase == "alternate arena"), 2
        )
        result = critic_rules.check_rule_4_extra_arena_or_attack(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 4)
        self.assertIn("alternate arena", result.matched_sentence.lower())

    def test_rule_5_positive_altered_meter_gain(self):
        text = "A perfect dodge grants +9 meter, rewarding a clean defensive read."
        result = critic_rules.check_rule_5_altered_numbers(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 5)

    def test_rule_5_negative_correct_meter_gain(self):
        text = "A perfect dodge grants +12 meter, rewarding a clean defensive read."
        self.assertIsNone(critic_rules.check_rule_5_altered_numbers(text))

    def test_rule_5_negative_no_number_claimed(self):
        text = "A perfect dodge feels satisfying and opens a clean counter window."
        self.assertIsNone(critic_rules.check_rule_5_altered_numbers(text))

    def test_rule_6_positive_no_restoration(self):
        text = (
            "After the burst, the camera never returns and the rival AI stays "
            "paused indefinitely."
        )
        result = critic_rules.check_rule_6_restoration_failure(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 6)

    def test_rule_6_negative_clean_return(self):
        text = "After the burst, control, camera, and rival AI all return cleanly to live combat."
        self.assertIsNone(critic_rules.check_rule_6_restoration_failure(text))

    def test_rule_7_positive_multiplayer_reference(self):
        text = "A future multiplayer mode lets two players duel Crimson Vanguard together."
        result = critic_rules.check_rule_7_scope_expansion(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.rule_number, 7)

    def test_rule_7_negative_labeled_deferred(self):
        text = "Multiplayer is deferred future scope, out of the current build."
        self.assertIsNone(critic_rules.check_rule_7_scope_expansion(text))

    def test_run_critic_returns_all_hits(self):
        text = "Nova stands as the game's final boss, and multiplayer is fully supported."
        violations = critic_rules.run_critic(text)
        rule_numbers = {v.rule_number for v in violations}
        self.assertIn(1, rule_numbers)
        self.assertIn(7, rule_numbers)

    def test_regression_fixture_exists_and_is_nonempty(self):
        self.assertTrue(critic_rules.REGRESSION_FIXTURE_TEXT.strip())
        self.assertTrue(critic_rules.REGRESSION_FIXTURE_TITLE.strip())

    def test_regression_fixture_trips_only_rule_2(self):
        violations = critic_rules.run_critic(critic_rules.REGRESSION_FIXTURE_TEXT)
        rule_numbers = [v.rule_number for v in violations]
        self.assertEqual(rule_numbers, [2])

    def test_regression_fixture_matched_sentence_is_in_fixture_text(self):
        violations = critic_rules.run_critic(critic_rules.REGRESSION_FIXTURE_TEXT)
        self.assertIn(violations[0].matched_sentence, critic_rules.REGRESSION_FIXTURE_TEXT)

    def test_verify_correction_passes_on_clean_text(self):
        clean_text = "An authored state machine selects among four fixed attacks by range and cooldown."
        self.assertEqual(critic_rules.verify_correction(clean_text), [])

    def test_verify_correction_raises_on_still_violating_text(self):
        still_bad = "Crimson Vanguard still tracks the player's patterns during the fight."
        with self.assertRaises(critic_rules.CorrectionValidationError):
            critic_rules.verify_correction(still_bad)


# ---------------------------------------------------------------------------
# pipeline.apply_corrections: post-correction re-verification (audit fix)
# ---------------------------------------------------------------------------

class ApplyCorrectionsRevalidationTests(unittest.TestCase):
    """Assignment #04 audit fix: an LLM-produced correction must be re-checked
    against all seven rules before it is accepted. A correction that still
    violates a rule (original problem persists, or a new one was introduced)
    must fail loudly, never be silently written out as a valid final."""

    def _draft_and_violations(self):
        draft_text = (
            "Crimson Vanguard learns from the player and adapts its attacks "
            "in real time during the fight."
        )
        violations = critic_rules.run_critic(draft_text)
        self.assertEqual([v.rule_number for v in violations], [2])
        return draft_text, violations

    @patch("pipeline.llm_client.call_claude")
    def test_rejects_correction_that_still_violates_a_rule(self, mock_call):
        draft_text, violations = self._draft_and_violations()
        # The "fix" swaps one adaptive phrase for another new one added by
        # this same audit - still a rule 2 violation.
        mock_call.return_value = (
            "Crimson Vanguard still tracks the player's patterns and reacts "
            "in real time during the fight."
        )
        with self.assertRaises(critic_rules.CorrectionValidationError):
            pipeline.apply_corrections(draft_text, violations, model="sonnet")
        # Real-output corrections must still go through Claude - only the
        # controlled regression fixture skips the call.
        mock_call.assert_called_once()

    @patch("pipeline.llm_client.call_claude")
    def test_accepts_correction_that_is_actually_clean(self, mock_call):
        draft_text, violations = self._draft_and_violations()
        mock_call.return_value = (
            "An authored state machine selects among four fixed attacks by "
            "range and cooldown during the fight."
        )
        corrected_text, corrections = pipeline.apply_corrections(
            draft_text, violations, model="sonnet"
        )
        self.assertNotIn("learns from the player", corrected_text)
        self.assertEqual(len(corrections), 1)
        # A clean correction must not raise, and run_critic on the result
        # confirms it truly is clean (belt-and-suspenders on the fixture).
        self.assertEqual(critic_rules.run_critic(corrected_text), [])
        mock_call.assert_called_once()

    @patch("pipeline.llm_client.call_claude")
    def test_no_final_written_when_correction_still_invalid(self, mock_call):
        # finalize_output must not reach its atomic_write_text calls when
        # apply_corrections raises - simulated here by asserting the
        # exception propagates past finalize_output rather than returning.
        draft_text, violations = self._draft_and_violations()
        mock_call.return_value = "Crimson Vanguard tracks player patterns in real time."
        output_cfg = {"slug": "unit-test-slug", "title": "Unit Test Output"}
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(pipeline, "CRITIC_EVIDENCE_DIR", Path(tmp) / "critic"), \
                 patch.object(pipeline, "OUTPUTS_DIR", Path(tmp) / "outputs"):
                with self.assertRaises(critic_rules.CorrectionValidationError):
                    pipeline.finalize_output(output_cfg, draft_text, violations, model="sonnet")
                self.assertFalse((Path(tmp) / "critic" / "unit-test-slug.md").exists())
                self.assertFalse((Path(tmp) / "outputs" / "unit-test-slug-final.md").exists())


# ---------------------------------------------------------------------------
# pipeline.run_regression_fixture: controlled rule-#2 fixture uses a fixed,
# non-Claude correction (2026-07-28 audit fix)
# ---------------------------------------------------------------------------

class RegressionFixtureTests(unittest.TestCase):
    """The controlled Rule 2 regression fixture must never depend on a live
    Claude rewrite - the correction is a fixed, canon-safe literal, always
    re-verified against all seven rules rather than accepted on faith."""

    def test_planted_fixture_still_triggers_exactly_rule_2(self):
        violations = critic_rules.run_critic(critic_rules.REGRESSION_FIXTURE_TEXT)
        self.assertEqual([v.rule_number for v in violations], [2])
        self.assertEqual(
            violations[0].matched_sentence,
            critic_rules.REGRESSION_FIXTURE_FLAGGED_SENTENCE,
        )

    def test_fixed_corrected_fixture_passes_all_seven_rules(self):
        self.assertEqual(
            critic_rules.run_critic(critic_rules.REGRESSION_FIXTURE_CORRECTED_TEXT),
            [],
        )
        # verify_correction must not raise on the fixed correction.
        self.assertEqual(
            critic_rules.verify_correction(critic_rules.REGRESSION_FIXTURE_CORRECTED_TEXT),
            [],
        )

    def test_fixed_correction_fails_clearly_if_it_ever_stops_passing(self):
        # Simulates the fixed correction drifting out of sync with the rules
        # (e.g. a future rule addition catching it) - must fail loudly via
        # CorrectionValidationError, never pass silently.
        drifted_correction = (
            critic_rules.REGRESSION_FIXTURE_CORRECTED_TEXT
            + " It also tracks the player's patterns between exchanges."
        )
        with self.assertRaises(critic_rules.CorrectionValidationError):
            critic_rules.verify_correction(drifted_correction)

    @patch("pipeline.llm_client.call_claude")
    def test_controlled_fixture_path_does_not_call_claude(self, mock_call):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(pipeline, "CRITIC_EVIDENCE_DIR", Path(tmp) / "critic"):
                pipeline.run_regression_fixture()
        mock_call.assert_not_called()

    def test_controlled_fixture_returns_the_fixed_corrected_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(pipeline, "CRITIC_EVIDENCE_DIR", Path(tmp) / "critic"):
                corrected_text = pipeline.run_regression_fixture()
        self.assertEqual(corrected_text, critic_rules.REGRESSION_FIXTURE_CORRECTED_TEXT)

    def test_controlled_fixture_evidence_contains_before_rule_and_after(self):
        with tempfile.TemporaryDirectory() as tmp:
            critic_dir = Path(tmp) / "critic"
            with patch.object(pipeline, "CRITIC_EVIDENCE_DIR", critic_dir):
                pipeline.run_regression_fixture()
            evidence_text = (critic_dir / "regression-fixture.md").read_text(encoding="utf-8")

        self.assertIn("CONTROLLED REGRESSION FIXTURE", evidence_text)
        self.assertIn(critic_rules.REGRESSION_FIXTURE_FLAGGED_SENTENCE, evidence_text)
        self.assertIn("Rule 2", evidence_text)
        self.assertIn(critic_rules.REGRESSION_FIXTURE_CORRECTED_SENTENCE, evidence_text)


# ---------------------------------------------------------------------------
# llm_client: CLI invocation shape, response parsing, mocked failures
# ---------------------------------------------------------------------------

class BuildCommandTests(unittest.TestCase):
    def test_command_shape_matches_approved_invocation(self):
        command = llm_client.build_command("claude", "sonnet")
        self.assertEqual(
            command,
            [
                "claude", "-p", "--model", "sonnet", "--tools", "",
                "--output-format", "text", "--no-session-persistence",
            ],
        )

    def test_command_never_includes_bare(self):
        command = llm_client.build_command("claude", "sonnet")
        self.assertNotIn("--bare", command)

    def test_command_requests_text_output_format(self):
        command = llm_client.build_command("claude", "sonnet")
        idx = command.index("--output-format")
        self.assertEqual(command[idx + 1], "text")


class CallClaudeMockedSubprocessTests(unittest.TestCase):
    def _mock_completed(self, returncode=0, stdout="", stderr=""):
        return subprocess.CompletedProcess(
            args=["claude"], returncode=returncode, stdout=stdout, stderr=stderr
        )

    @patch("llm_client.subprocess.run")
    def test_successful_plain_text_response(self, mock_run):
        mock_run.return_value = self._mock_completed(stdout="hello world")
        text = llm_client.call_claude("prompt", executable="fake-claude")
        self.assertEqual(text, "hello world")
        self.assertEqual(mock_run.call_args.kwargs.get("shell"), False)
        self.assertEqual(mock_run.call_args.kwargs.get("input"), "prompt")

    @patch("llm_client.subprocess.run")
    def test_multiline_markdown_response_is_preserved(self, mock_run):
        markdown = "# Heading\n\n- item one\n- item two\n\n```\ncode block\n```"
        mock_run.return_value = self._mock_completed(stdout=markdown)
        text = llm_client.call_claude("prompt", executable="fake-claude")
        self.assertEqual(text, markdown)

    @patch("llm_client.subprocess.run")
    def test_surrounding_whitespace_is_stripped(self, mock_run):
        mock_run.return_value = self._mock_completed(stdout="\n\n  hello world  \n\n")
        text = llm_client.call_claude("prompt", executable="fake-claude")
        self.assertEqual(text, "hello world")

    @patch("llm_client.subprocess.run")
    def test_empty_stdout_raises_parse_error(self, mock_run):
        mock_run.return_value = self._mock_completed(stdout="   \n  \n")
        with self.assertRaises(llm_client.ClaudeResponseParseError):
            llm_client.call_claude("prompt", executable="fake-claude")

    @patch("llm_client.subprocess.run")
    def test_nonzero_exit_raises_cli_error(self, mock_run):
        mock_run.return_value = self._mock_completed(returncode=1, stderr="boom")
        with self.assertRaises(llm_client.ClaudeCLIError):
            llm_client.call_claude("prompt", executable="fake-claude")

    @patch("llm_client.subprocess.run")
    def test_auth_failure_pattern_raises_auth_error(self, mock_run):
        mock_run.return_value = self._mock_completed(
            returncode=1, stderr="Error: not authenticated. Please log in."
        )
        with self.assertRaises(llm_client.ClaudeAuthError):
            llm_client.call_claude("prompt", executable="fake-claude")

    @patch("llm_client.subprocess.run")
    def test_timeout_raises_timeout_error(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["claude"], timeout=5)
        with self.assertRaises(llm_client.ClaudeTimeoutError):
            llm_client.call_claude("prompt", executable="fake-claude", timeout=5)

    @patch("llm_client.subprocess.run")
    def test_file_not_found_raises_not_found_error(self, mock_run):
        mock_run.side_effect = FileNotFoundError("no such file")
        with self.assertRaises(llm_client.ClaudeNotFoundError):
            llm_client.call_claude("prompt", executable="fake-claude")

    @patch("llm_client.subprocess.run")
    def test_prompt_passed_via_stdin_not_argv(self, mock_run):
        mock_run.return_value = self._mock_completed(stdout="ok")
        secret_prompt = "prompt with special chars ; & | $(rm -rf) `backticks`"
        llm_client.call_claude(secret_prompt, executable="fake-claude")
        called_args = mock_run.call_args[0][0]
        self.assertNotIn(secret_prompt, called_args)
        self.assertEqual(mock_run.call_args.kwargs["input"], secret_prompt)

    @patch("llm_client.subprocess.run")
    def test_unicode_prompt_and_response_use_utf8_not_default_codepage(self, mock_run):
        unicode_prompt = (
            "Describe the telegraph -> impact window for Echo/Nova: "
            "“strike—dodge—counter.”"
        )
        unicode_reply = "Echo/Nova telegraph -> impact window: “clean read.”"
        mock_run.return_value = self._mock_completed(stdout=unicode_reply)

        text = llm_client.call_claude(unicode_prompt, executable="fake-claude")

        self.assertEqual(text, unicode_reply)
        self.assertEqual(mock_run.call_args.kwargs.get("input"), unicode_prompt)
        self.assertEqual(mock_run.call_args.kwargs.get("encoding"), "utf-8")
        self.assertEqual(mock_run.call_args.kwargs.get("text"), True)


if __name__ == "__main__":
    unittest.main()
