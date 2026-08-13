"""Retrieval must be reproducible and must carry GDD citations forward.

A retrieval trail that cannot be reproduced is not evidence, and a retrieved
fact with no citation is indistinguishable from an invented one.
"""

import os

import pytest

import retrieval

KB_FILES = ("vanguard-telegraphs.md", "core-canon.md")
QUERY = "Crimson Vanguard four authored attacks readability telegraph phase 2"


class TestChunkParsing:
    def test_level_two_headings_become_chunks(self):
        text = "# Title\nintro\n\n## First\nbody one\n\n## Second\nbody two\n"
        chunks = retrieval.parse_markdown_chunks(text, "f.md")
        assert [c.heading for c in chunks] == ["First", "Second"]

    def test_text_before_the_first_heading_is_not_a_chunk(self):
        text = "# Title\nintro text\n\n## Only\nbody\n"
        chunks = retrieval.parse_markdown_chunks(text, "f.md")
        assert len(chunks) == 1
        assert "intro text" not in chunks[0].body

    def test_citation_is_extracted_from_the_source_line(self):
        text = "## H\nbody\n\n*Source: `gdd/x.md`, Page 5 (\"Thing\").*\n"
        chunk = retrieval.parse_markdown_chunks(text, "f.md")[0]
        assert "Page 5" in chunk.citation
        assert chunk.gdd_pages == (5,)

    def test_a_chunk_with_no_source_line_has_no_citation(self):
        chunk = retrieval.parse_markdown_chunks("## H\njust body\n", "f.md")[0]
        assert chunk.citation is None
        assert chunk.gdd_pages == ()


class TestRetrieval:
    def test_every_knowledge_base_file_exists(self):
        for name in KB_FILES:
            assert os.path.isfile(os.path.join(retrieval.DEFAULT_KB_DIR, name))

    def test_retrieval_is_deterministic(self):
        first = retrieval.retrieve(QUERY, KB_FILES)
        second = retrieval.retrieve(QUERY, KB_FILES)
        assert [s.chunk.key for s in first] == [s.chunk.key for s in second]
        assert [s.score for s in first] == [s.score for s in second]

    def test_results_are_ordered_by_descending_score(self):
        scores = [s.score for s in retrieval.retrieve(QUERY, KB_FILES)]
        assert scores == sorted(scores, reverse=True)

    def test_only_eligible_files_are_candidates(self):
        selected = retrieval.retrieve(QUERY, ("core-canon.md",))
        assert {s.chunk.source_file for s in selected} == {"core-canon.md"}

    def test_zero_score_chunks_are_not_selected(self):
        selected = retrieval.retrieve("zzzz nonsense token", KB_FILES)
        assert selected == ()

    def test_required_chunks_are_pinned_regardless_of_score(self):
        pin = ("core-canon.md", "Scope lock (do not exceed in generated content)")
        selected = retrieval.retrieve(
            "thruster propulsion", KB_FILES, top_k=1, required_chunks=(pin,))
        assert pin in [s.chunk.key for s in selected]

    def test_a_required_chunk_already_selected_is_not_duplicated(self):
        pin = ("vanguard-telegraphs.md", "Phase 2 escalation (same four attacks, "
                                         "re-timed — never a new moveset)")
        selected = retrieval.retrieve(QUERY, KB_FILES, required_chunks=(pin,))
        keys = [s.chunk.key for s in selected]
        assert keys.count(pin) <= 1

    def test_an_unknown_required_chunk_raises(self):
        with pytest.raises(ValueError):
            retrieval.retrieve(QUERY, KB_FILES,
                               required_chunks=(("core-canon.md", "No Such Heading"),))

    def test_a_missing_knowledge_base_file_raises(self):
        with pytest.raises(IOError):
            retrieval.retrieve(QUERY, ("does-not-exist.md",))

    def test_selected_chunks_carry_gdd_citations(self):
        selected = retrieval.retrieve(QUERY, KB_FILES)
        citations = retrieval.citations_for(selected)
        assert citations
        assert all("gdd/ascendant-impact-gdd" in c for c in citations)

    def test_citations_are_deduplicated_in_order(self):
        selected = retrieval.retrieve(QUERY, KB_FILES)
        citations = retrieval.citations_for(selected)
        assert len(citations) == len(set(citations))
