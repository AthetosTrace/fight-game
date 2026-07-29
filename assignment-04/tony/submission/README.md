# Assignment 4 — Dynamic Content Pipeline

## What the pipeline generated

1. **Crimson Vanguard Telegraph and Readability Pack** — names the four
   authored attacks (A–D) as proposed working names ("Fault Line," "Advance
   Line," "Bulwark Reach," "Thruster Snap"), pairs each with its readability
   requirement, and adds internal playtest-facing telegraph shorthand. This
   fills a gap the GDD names directly: the four attacks have range and
   purpose but no names, choreography, or telegraph copy.
2. **Echo/Nova Impact Window Cinematic Beat Pack** — describes how a
   successful Impact Window plays out differently for Echo (precise,
   controlled) versus Nova (fast, aggressive) at both the 0.75 s onboarding
   window and the tightened 0.35–0.50 s standard window, without touching
   meter values or response times. This gives the two playable fighters a
   distinct cinematic identity the GDD specifies systemically but never
   describes in prose.
3. **Shattered Ring Environmental Reaction Pack** — drafts presentation-only
   reaction language (scuffing, flicker, dust, creak) for the arena's floor,
   doorway, and walls during major impacts, explicitly deferred to M5/Phase 2
   and explicitly not adding any hazard or gameplay object. This is useful
   because Shattered Ring is specified only as a functional space with no
   reaction fiction attached.

All three target real, GDD-named gaps rather than generic content, and all
three are useful directly to design/build work: attack names and telegraph
copy for the developer and animator, cinematic identity language for the
Impact Window handoff, and reaction language staged for the M5 pass without
getting ahead of it.

## Does it sound like the game?

Yes, on balance. All three final packs read in the game's painterly
cyber-fantasy martial-arts register — controlled, technical language for
Echo, momentum-forward language for Nova, armored/industrial language for
Crimson Vanguard and the Ring — and consistently frame spectacle as
**earned**, never automatic, which is the GDD's central promise. Every pack
stays inside the one-duel, one-arena, four-attack scope lock and repeatedly
declines to invent facts the GDD doesn't support (no arena history, no
Vanguard origin, no fifth attack).

That said, getting here required real human grounding review — just not on
these final drafts. Earlier generation runs contained tone drift and
unsupported specifics that the seven deterministic rules do not check for
(see "What the critic and human review caught" below); a human caught those
issues, and those findings drove the retrieval and prompt improvements
described later in this README. Those earlier, problematic runs were
discarded. In the final run, made with those improvements already in place,
all three natural drafts passed all seven deterministic critic rules
cleanly and each is preserved unchanged as the final output. The current
`-draft.md` files in `outputs/` are raw generation artifacts from that
successful final run — they are not before/after evidence of the earlier
human corrections, since no correction was needed on this run.

## RAG implementation

The pipeline restricts retrieval to a small, per-content-type manifest of
knowledge-base files (e.g. `vanguard-telegraphs.md` + `core-canon.md` for the
Vanguard pack) so it can never pull from an out-of-scope document. Each
eligible file is parsed into **heading-based chunks**, and every chunk is
scored against the query by **lexical token overlap** — shared word count
between the query and the chunk's heading/body. The **top four
positive-scoring chunks** are passed to the generator as retrieved context.

On top of that, specific **canon-critical chunks can be pinned** — forced
into the generator's context even when they fall outside the lexical top
four, because the pipeline flags them as required for a given content type
regardless of query wording. The three important pinned chunks used in this
run:

- **Impact Window restoration rule** — the `RestoreCombatState()` safeguard
  requiring input/collision/locomotion/lock-on/AI state to be restored after
  every Impact Window and Final Clash branch.
- **Open restoration gaps pending M3 sign-off** — the cinematic-integration
  inspector's five unresolved restoration items, pinned so no generated beat
  overclaims certainty the plan doesn't yet support.
- **Shattered Ring build-side Phase 1 vs. Phase 2 constraints** — the rule
  that environmental reaction is deferred to M5 and Phase 1 has no hazards,
  damage volumes, or physics objects.

Each file in `retrieval-evidence/` is the side-by-side proof for one content
pack: the exact query, the full scored candidate table (source file,
heading, matched tokens), which chunks were selected and why (lexical top-4
vs. required pin), and the full retrieved text that was handed to the
generator — directly comparable against the final output in `outputs/`.

## Consistency loop

All three natural generated drafts passed all seven deterministic critic
rules in the final run — no rule fired against any of the three real
outputs. Because no natural draft failed, the pipeline separately ran a
**deliberately planted controlled regression fixture** to demonstrate that
the consistency loop actually catches and corrects a violation when one
exists. That fixture is **not a real generated output** — it exists only to
prove the mechanism works.

**Before:**
> "Over the course of the fight, Crimson Vanguard learns from the player's
> patterns and adapts its attacks in real time, favoring whichever of its
> four strikes the fight has shown to be least anticipated."

**After:**
> "Crimson Vanguard uses an authored state machine to select among four
> fixed attacks by range and cooldown; it does not learn from the player or
> adapt at runtime."

Rule 2 caught the runtime-learning claim ("learns from the player's
patterns," "adapts... in real time") and restored the canon requirement,
grounded in `core-canon.md`'s hard constraint, that Crimson Vanguard is
deterministic authored logic with no runtime model calls. See
`critic-evidence/regression-fixture.md` for the full per-rule table and the
before/after pair.

## What the critic and human review caught

**Deterministic critic (seven rules, checked against all three real drafts
and the fixture, final run):**
- Rule 2 — runtime learning/adaptation language
- Incorrect automatic Impact Window success (bypassing the earned-input
  requirement)
- Extra attacks (a fifth attack) or second-arena implications
- Unsupported meter values, scope expansion, and the remaining canon breaks
  covered by the seven rules

In the final run, all three natural drafts passed all seven rules cleanly.
Only Rule 2 fired, and only against the deliberately planted controlled
regression fixture — see `critic-evidence/` for the per-pack, per-rule
results.

**Human grounding review, on earlier discarded generation runs, caught
prompt drift the seven deterministic rules do not check for:**
- An unsupported claim that Crimson Vanguard had a momentary armor weak
  point
- Wording that described Vanguard as never reactive, when authored selection
  does deterministically respond to range and cooldown
- Wording that could imply player input controls the 1–3 second cinematic
  duration, rather than merely earning it
- Proposed attack names needed to be explicitly labeled as new authored
  working names, not established GDD facts
- Announcer-style language needed to be reframed as internal playtest
  readability shorthand, not shipped dialogue
- Unresolved cinematic restoration details needed explicit caveats rather
  than being described as already fully specified

None of these six items were caught by the deterministic critic — they
surfaced only when a human read the earlier, discarded drafts. Those
findings are what drove the retrieval and prompt changes in the next
section; the final run's drafts, produced after those changes, did not
contain these issues and needed no further correction.

## Concrete prompt and retrieval improvements

- Flat lexical top-four retrieval did not always surface canon-critical
  caveats (the restoration rule, the open restoration gaps, the Phase 1/2
  arena constraint) when they scored below the top four on raw word overlap.
- **Required chunk pinning was added** so those restoration and build-side
  constraint chunks are always included regardless of lexical score.
- The **Impact Window prompt** now forbids unsupported weapons, equipment,
  armor weak points, or exposed components, and forbids unsupported
  restoration claims; it also explicitly distinguishes **earning** a burst
  from **controlling its duration**.
- The **Vanguard prompt** now requires proposed attack names to be labeled
  as working names, requires telegraph copy to read as internal playtest
  shorthand with no announcer or shipped-dialogue implication, and requires
  a clear distinction between deterministic range/cooldown response and
  runtime learning.
- The **Shattered Ring prompt** now forbids hazards, interactive terrain,
  invented lore, and unsupported milestone-gating claims.

## How to run

```
py -3 -m unittest assignment-04/tony/pipeline/test_pipeline.py -v
py -3 assignment-04/tony/pipeline/pipeline.py
```

The final test suite contains **175 passing tests**.

## Final artifact locations

- `assignment-04/tony/outputs/`
- `assignment-04/tony/retrieval-evidence/`
- `assignment-04/tony/critic-evidence/`

The `-final.md` files in `outputs/` are the graded deliverables. In this
final run, each draft passed all seven deterministic rules and its final
copy is identical to it; the `-draft.md` files are raw generation artifacts
from that successful run, not before/after evidence of human correction —
the corrections driven by human grounding review were made to earlier,
discarded runs before this final run was produced.
