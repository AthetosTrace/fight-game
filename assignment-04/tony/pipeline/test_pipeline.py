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
