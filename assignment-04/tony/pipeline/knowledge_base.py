"""Manifest-driven retrieval over Assignment #04's curated knowledge base.

Parses each approved knowledge-base file into heading-based chunks, restricts
candidates per output to the files retrieval-manifest.md names for it, scores
every eligible chunk against the output's query with a deterministic lexical
overlap count, and returns both the full candidate list and the selected
top-K (score > 0) chunks. No embeddings, no network calls - fully
reproducible from the same inputs every time.
"""

import re
from dataclasses import dataclass
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
PIPELINE_DIR = _THIS_FILE.parent
TONY_DIR = PIPELINE_DIR.parent
ASSIGNMENT_DIR = TONY_DIR.parent
PROJECT_ROOT = ASSIGNMENT_DIR.parent
KNOWLEDGE_BASE_DIR = ASSIGNMENT_DIR / "shared" / "knowledge-base"

DEFAULT_TOP_K = 4

_HEADING_RE = re.compile(r"^##\s+(.*\S)\s*$")
_TOKEN_RE = re.compile(r"[a-z0-9]+")

_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are",
    "was", "were", "be", "been", "being", "with", "that", "this", "it", "its",
    "as", "by", "at", "from", "into", "than", "then", "so", "but", "not",
    "no", "do", "does", "did", "if", "when", "what", "which", "who", "how",
    "why", "describe", "give", "write", "name", "without",
})


@dataclass(frozen=True)
class Chunk:
    source_file: str
    heading: str
    body: str
    index: int


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: int
    matched_tokens: tuple


# Selection-reason labels recorded per chunk in RetrievalResult.selected,
# parallel to RetrievalResult.selection_reasons. A chunk is "lexical" when
# the top-K score cutoff alone put it there, "required" when only a pin
# added it (it fell outside the lexical top-K), and "lexical+required" when
# both independently would have selected it.
SELECTED_BY_LEXICAL = "lexical"
SELECTED_BY_REQUIRED = "required"
SELECTED_BY_BOTH = "lexical+required"


@dataclass(frozen=True)
class RetrievalResult:
    slug: str
    query: str
    eligible_files: tuple
    candidates: tuple  # every scored chunk, sorted best-first, deterministic tie-break
    selected: tuple    # lexical top-K (score > 0) plus any required pins
    selection_reasons: tuple = ()  # parallel to `selected`: SELECTED_BY_* per chunk
    required_chunks: tuple = ()    # (source_file, heading) pins requested for this retrieval
    top_k: int = DEFAULT_TOP_K


def parse_markdown_chunks(text, source_file):
    """Split markdown into level-2 ('## ') heading chunks.

    Text before the first such heading (title + intro) is not a chunk -
    retrieval only ever needs named sections, which is exactly what the
    manifest cites.
    """
    chunks = []
    current_heading = None
    current_lines = []
    index = 0

    def flush():
        nonlocal current_heading, current_lines, index
        if current_heading is not None:
            body = "\n".join(current_lines).strip()
            chunks.append(Chunk(
                source_file=source_file,
                heading=current_heading,
                body=body,
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
    """Deterministic lexical overlap: count of distinct query tokens present
    in the chunk's heading+body. Returns (score, matched_tokens_sorted)."""
    chunk_tokens = set(tokenize(chunk.heading + " " + chunk.body))
    matched = sorted(set(query_tokens) & chunk_tokens)
    return len(matched), tuple(matched)


def load_chunks_for_files(eligible_files, kb_dir=KNOWLEDGE_BASE_DIR):
    """Read and parse only the files named in eligible_files - chunks from
    any other file are never candidates."""
    chunks = []
    for filename in eligible_files:
        path = Path(kb_dir) / filename
        text = path.read_text(encoding="utf-8")
        chunks.extend(parse_markdown_chunks(text, filename))
    return chunks


def _reason_for(key, lexical_keys, required_key_set):
    in_lexical = key in lexical_keys
    in_required = key in required_key_set
    if in_lexical and in_required:
        return SELECTED_BY_BOTH
    if in_required:
        return SELECTED_BY_REQUIRED
    return SELECTED_BY_LEXICAL


def retrieve(slug, query, eligible_files, kb_dir=KNOWLEDGE_BASE_DIR, top_k=DEFAULT_TOP_K,
             required_chunks=()):
    """Run one manifest-driven retrieval pass and return the full evidence trail.

    required_chunks is a tuple of (source_file, heading) pairs that must be
    present in the returned `selected` set regardless of lexical score - this
    pins safety-critical context (e.g. restoration-gap caveats) that a flat
    top-K score cutoff would otherwise drop. A required chunk already present
    in the lexical top-K is not duplicated; ordering is deterministic: the
    lexical top-K first (score desc, file, index, as before), then any
    required-only chunks appended in the exact order the caller declared them.
    """
    chunks = load_chunks_for_files(eligible_files, kb_dir=kb_dir)
    query_tokens = tokenize(query)

    scored = []
    for chunk in chunks:
        score, matched = score_chunk(query_tokens, chunk)
        scored.append(ScoredChunk(chunk=chunk, score=score, matched_tokens=matched))

    # Deterministic ordering: score desc, then file name, then original
    # position - never dependent on dict/set iteration order.
    candidates = tuple(sorted(
        scored,
        key=lambda sc: (-sc.score, sc.chunk.source_file, sc.chunk.index),
    ))
    by_key = {(sc.chunk.source_file, sc.chunk.heading): sc for sc in candidates}

    lexical_selected = tuple(sc for sc in candidates if sc.score > 0)[:top_k]
    lexical_keys = {(sc.chunk.source_file, sc.chunk.heading) for sc in lexical_selected}

    required_keys = tuple(required_chunks)
    required_key_set = set(required_keys)

    required_only = []
    seen = set()
    for key in required_keys:
        if key in lexical_keys or key in seen:
            continue
        if key not in by_key:
            raise ValueError(
                "Required chunk not found among eligible chunks for {!r}: {}".format(
                    slug, key
                )
            )
        seen.add(key)
        required_only.append(by_key[key])

    selected = lexical_selected + tuple(required_only)
    selection_reasons = tuple(
        _reason_for((sc.chunk.source_file, sc.chunk.heading), lexical_keys, required_key_set)
        for sc in selected
    )

    return RetrievalResult(
        slug=slug,
        query=query,
        eligible_files=tuple(eligible_files),
        candidates=candidates,
        selected=selected,
        selection_reasons=selection_reasons,
        required_chunks=required_keys,
        top_k=top_k,
    )


# ---------------------------------------------------------------------------
# The three confirmed outputs (Tony-approved 2026-07-28, see
# assignment-04/shared/knowledge-base/retrieval-manifest.md).
# ---------------------------------------------------------------------------

OUTPUTS = [
    {
        "slug": "vanguard-telegraph-pack",
        "title": "Crimson Vanguard Telegraph and Readability Pack",
        "query": (
            "Name Crimson Vanguard's four authored attacks A-D and describe a "
            "readable telegraph for each, consistent with its stated range, "
            "purpose, and readability requirement."
        ),
        "eligible_files": ("vanguard-telegraphs.md", "core-canon.md"),
        "allowed_to_create": (
            "A short name per attack (A-D) consistent with its stated range/purpose.",
            "One or two lines of telegraph/announcer-readable flavor text per "
            "attack, consistent with the stated readability requirement and "
            "behavioral intent.",
            "Tone-consistent narrative language for the six-state cycle, so "
            "long as all six states and their order are preserved.",
        ),
        "must_not_invent": (
            "A fifth attack, a renamed/merged attack, or a phase-exclusive attack.",
            "Any new timing number, or a restated number that differs from "
            "the ranges in vanguard-telegraphs.md.",
            "Any implication that attack selection is learned, adaptive, or "
            "runtime-generated.",
            "A backstory for Crimson Vanguard or Project Valor-7.",
        ),
    },
    {
        "slug": "impact-window-beat-pack",
        "title": "Echo/Nova Impact Window Cinematic Beat Pack",
        "query": (
            "Describe Echo's and Nova's cinematic bursts on a successful "
            "Impact Window, differentiated by combat identity, without "
            "implying automatic success or altering the meter gain or "
            "response-time values."
        ),
        "eligible_files": ("impact-window-cinematics.md", "core-canon.md"),
        # Pinned per the 2026-07-28 audit: the lexical top-4 for this
        # output's query cut both restoration-caveat chunks (scored 5 and 3,
        # below the top-4 cutoff of 10/9/7/6), so the generator never saw the
        # guardrail context and wrote unhedged restoration certainty that the
        # critic's Rule 6 then failed to catch. Required regardless of score.
        "required_chunks": (
            (
                "impact-window-cinematics.md",
                "The restoration rule (why every cinematic beat must \"hand back\" cleanly)",
            ),
            (
                "impact-window-cinematics.md",
                "OPEN — restoration gaps flagged by inspection, not yet corrected",
            ),
        ),
        "allowed_to_create": (
            "Separate short burst descriptions for Echo and Nova expressing "
            "each fighter's stated identity and accent color.",
            "Distinct flavor for the wider first (onboarding) window versus a "
            "standard window, preserving the one stated mechanical difference "
            "(response time).",
        ),
        "must_not_invent": (
            "Any burst that plays without the player succeeding at the input.",
            "A burst duration outside 1-3 seconds, or a response time other "
            "than 0.75 s (first) / 0.35-0.50 s (standard).",
            "A burst that implies rival AI, camera, or gameplay state does "
            "not cleanly return afterward - the restoration gaps are OPEN, "
            "not resolved.",
            "A meter gain value other than the ones in impact-window-cinematics.md.",
        ),
        "extra_constraints": (
            "Describe the burst ending with a return to combat, but do not "
            "assert specific rival-AI, camera-ownership, montage-cleanup, or "
            "gameplay-state restoration behavior that is still marked OPEN.",
        ),
    },
    {
        "slug": "shattered-ring-reaction-pack",
        "title": "Shattered Ring Environmental Reaction Pack",
        "query": (
            "Describe how the Shattered Ring's central floor, far doorway, "
            "and wall surfaces visibly react to a major impact, as "
            "presentation only, without adding gameplay hazards."
        ),
        "eligible_files": ("shattered-ring-reactions.md", "core-canon.md"),
        "allowed_to_create": (
            "Short descriptive flavor for how the floor, doorway, or wall "
            "surfaces visibly respond to a major impact (light flicker, "
            "dust, structural creak, surface scuffing) - visible but controlled.",
            "Language explicitly framing this as presentation only (an "
            "M5/Phase 2 authored pass), not a Phase 1 gameplay system.",
        ),
        "must_not_invent": (
            "Any hazard, damage volume, destructible object, or physics "
            "object that could affect the duel - none exist in Phase 1.",
            "A second arena, an alternate version of the Ring, or any "
            "off-screen location.",
            "Any description drawn from GDD pages 10-14 (image reference "
            "sheets, no extractable text).",
            "A history or origin for the Shattered Ring.",
        ),
    },
]


def get_output(slug):
    for output in OUTPUTS:
        if output["slug"] == slug:
            return output
    raise KeyError("Unknown output slug: {}".format(slug))
