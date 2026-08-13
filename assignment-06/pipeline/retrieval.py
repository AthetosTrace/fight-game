"""Retrieval over the curated, GDD-cited knowledge base.

Assignment #04 built a manifest-driven retrieval layer whose every chunk ends
in a `*Source: gdd/... Page N*` line. Assignment #05's arena pipeline never
called it -- its rules trace to PROTOTYPE_BLACKBOARD.md, which is measured
implementation, not design. This module is the join: the generator below
grounds each field it writes in a retrieved chunk, and carries that chunk's
GDD page citation forward into the run report.

Deterministic lexical scoring. No embeddings, no network calls, no API key --
the same choice Assignment #04 made, for the same reason: a retrieval trail
that cannot be reproduced is not evidence.

Adapted from assignment-04/tony/pipeline/knowledge_base.py.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_KB_DIR = os.path.join(
    REPO_ROOT, "assignment-04", "shared", "knowledge-base")

DEFAULT_TOP_K = 3

_HEADING_RE = re.compile(r"^##\s+(.*\S)\s*$")
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_SOURCE_RE = re.compile(r"\*Source:\s*(.+?)\*", re.DOTALL)
_GDD_PAGE_RE = re.compile(r"Page\s+(\d+)")

_STOPWORDS = frozenset("""
a an and are as at be by for from has have in is it its of on or that the to
with must may not no this these those which what when where how
""".split())


class Chunk(object):
    """One level-2 markdown section of a knowledge-base file."""

    def __init__(self, source_file, heading, body, index):
        self.source_file = source_file
        self.heading = heading
        self.body = body
        self.index = index

    @property
    def key(self):
        return (self.source_file, self.heading)

    @property
    def citation(self):
        """The chunk's own `*Source: ...*` line, verbatim, or None.

        This is what makes a retrieved fact traceable to the GDD rather than
        merely plausible.
        """
        match = _SOURCE_RE.search(self.body)
        if not match:
            return None
        return " ".join(match.group(1).split())

    @property
    def gdd_pages(self):
        """GDD page numbers named in this chunk's source line."""
        citation = self.citation
        if not citation:
            return ()
        return tuple(int(page) for page in _GDD_PAGE_RE.findall(citation))

    def as_dict(self):
        return {
            "source_file": self.source_file,
            "heading": self.heading,
            "citation": self.citation,
            "gdd_pages": list(self.gdd_pages),
        }


class ScoredChunk(object):
    def __init__(self, chunk, score, matched_tokens):
        self.chunk = chunk
        self.score = score
        self.matched_tokens = matched_tokens

    def as_dict(self):
        record = self.chunk.as_dict()
        record["score"] = self.score
        record["matched_tokens"] = list(self.matched_tokens)
        return record


def parse_markdown_chunks(text, source_file):
    """Split markdown into level-2 ('## ') heading chunks.

    Text before the first such heading is title/intro, never a chunk --
    retrieval only ever needs named sections.
    """
    chunks = []
    current_heading = None
    current_lines = []
    index = 0

    def flush():
        nonlocal current_heading, current_lines, index
        if current_heading is not None:
            chunks.append(Chunk(
                source_file=source_file,
                heading=current_heading,
                body="\n".join(current_lines).strip(),
                index=index,
            ))
            index += 1
        current_lines = []

    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            flush()
            current_heading = match.group(1)
        elif current_heading is not None:
            current_lines.append(line)
    flush()
    return chunks


def tokenize(text):
    return [tok for tok in _TOKEN_RE.findall(text.lower()) if tok not in _STOPWORDS]


def score_chunk(query_tokens, chunk):
    """Distinct query tokens present in the chunk's heading + body."""
    chunk_tokens = set(tokenize(chunk.heading + " " + chunk.body))
    matched = sorted(set(query_tokens) & chunk_tokens)
    return len(matched), tuple(matched)


def load_chunks(eligible_files, kb_dir=DEFAULT_KB_DIR):
    """Parse only the named files. Chunks from any other file are never
    candidates -- the manifest decides eligibility, not the scorer."""
    chunks = []
    for filename in eligible_files:
        path = os.path.join(kb_dir, filename)
        if not os.path.isfile(path):
            raise IOError("knowledge-base file not found: %s" % path)
        with open(path, "r", encoding="utf-8") as handle:
            chunks.extend(parse_markdown_chunks(handle.read(), filename))
    return chunks


def retrieve(query, eligible_files, kb_dir=DEFAULT_KB_DIR, top_k=DEFAULT_TOP_K,
             required_chunks=()):
    """One retrieval pass. Returns the selected chunks, best first.

    `required_chunks` pins (source_file, heading) pairs that must appear
    regardless of lexical score -- a flat top-K would otherwise drop the
    safety-critical canon (the hard constraint, the scope lock) that keeps a
    generated row inside the GDD.
    """
    chunks = load_chunks(eligible_files, kb_dir=kb_dir)
    query_tokens = tokenize(query)

    scored = [ScoredChunk(chunk, *score_chunk(query_tokens, chunk))
              for chunk in chunks]

    # Deterministic: score desc, then file, then original position. Never
    # dependent on dict or set iteration order.
    candidates = sorted(
        scored, key=lambda sc: (-sc.score, sc.chunk.source_file, sc.chunk.index))
    by_key = {sc.chunk.key: sc for sc in candidates}

    selected = [sc for sc in candidates if sc.score > 0][:top_k]
    selected_keys = {sc.chunk.key for sc in selected}

    for key in required_chunks:
        if key in selected_keys:
            continue
        if key not in by_key:
            raise ValueError("required chunk not found among eligible chunks: %s" % (key,))
        selected.append(by_key[key])
        selected_keys.add(key)

    return tuple(selected)


def citations_for(selected):
    """The distinct GDD citations behind a retrieval, in selection order."""
    seen = []
    for scored in selected:
        citation = scored.chunk.citation
        if citation and citation not in seen:
            seen.append(citation)
    return tuple(seen)
