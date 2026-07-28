# Retrieval Manifest — Three Confirmed Outputs

Maps each of Tony's three confirmed Assignment #04 outputs to the query
pattern the pipeline should retrieve against, the exact knowledge files and
sections to pull, what unrelated context must be excluded, and the boundary
between what the generator may create and what it must never invent.

**Status: CONFIRMED with the user on 2026-07-28.** The three outputs are:

1. Crimson Vanguard Telegraph and Readability Pack
2. Echo/Nova Impact Window Cinematic Beat Pack
3. Shattered Ring Environmental Reaction Pack

---

## Output 1 — Crimson Vanguard Telegraph and Readability Pack

**What it is:** short names and telegraph/announcer-readable descriptions
for the four authored Crimson Vanguard attacks (A–D), grounded in each
attack's range/purpose and readability requirement.

**Likely retrieval queries:**
- "Name Crimson Vanguard's close-range gauntlet attack and describe its telegraph."
- "What should the telegraph for the forward-pressure sequence (attack B) look and read like?"
- "Give attack C a readable identity tied to its armored-reach purpose."
- "Describe the thruster telegraph for attack D consistent with 'no hidden full-arena snap.'"

**Exact knowledge files to retrieve:**
- `vanguard-telegraphs.md`
- `core-canon.md`

**Relevant sections / chunks:**
- `vanguard-telegraphs.md` → "The six-state loop", "Behavioral intent",
  "The four authored attacks (no names in the GDD — this is the gap)",
  "Phase 2 escalation", "Telegraph mechanics"
- `core-canon.md` → "The three combatants" (Crimson Vanguard row only — for
  material family / energy-VFX / readability-target flavor), "Hard
  constraint" (to keep any "intent" language authored/deterministic, never
  adaptive)

**Unrelated context to exclude:**
- `impact-window-cinematics.md` in full — meter gains, Impact Window
  widths, and Final Clash gate numbers have no bearing on naming or
  describing an attack telegraph.
- `shattered-ring-reactions.md` in full — arena facts are not attack facts.
- Echo/Nova rows of the combatants table beyond what's needed to keep them
  out of this pack entirely — this output is Crimson Vanguard only.

**The generator is allowed to create:**
- A short name per attack (A–D) consistent with its stated range/purpose.
- One or two lines of telegraph/announcer-readable flavor text per attack,
  consistent with the stated readability requirement and behavioral intent.
- Tone-consistent language describing the six-state cycle in narrative form
  (e.g., for a bestiary-style readout), so long as all six states and their
  order are preserved.

**The generator must not invent:**
- A fifth attack, a renamed/merged attack, or a phase-exclusive attack —
  exactly four attacks (A–D), unchanged across both phases.
- Any new timing number, or a restated number that differs from the ranges
  in `vanguard-telegraphs.md`.
- Any implication that attack selection is learned, adaptive, or
  runtime-generated — selection is authored/weighted, not intelligent.
- A backstory for Crimson Vanguard or Project Valor-7 — that is out of
  scope for this pack (no origin-fiction output was confirmed).

---

## Output 2 — Echo/Nova Impact Window Cinematic Beat Pack

**What it is:** short descriptions of the 1–3 second choreographed bursts
that play on Impact Window success, differentiated by which fighter
(Echo or Nova) is performing them, consistent with each fighter's combat
identity.

**Likely retrieval queries:**
- "Describe Echo's cinematic burst on a successful perfect-dodge Impact Window."
- "Describe Nova's cinematic burst on a successful counter Impact Window."
- "What does the first (onboarding) Impact Window burst look like versus a standard one?"
- "Write flavor text for the +20 meter gain moment without implying auto-success."

**Exact knowledge files to retrieve:**
- `impact-window-cinematics.md`
- `core-canon.md`

**Relevant sections / chunks:**
- `impact-window-cinematics.md` → "Impact Windows", "Ascension Meter", "The
  restoration rule", "OPEN — restoration gaps flagged by inspection, not yet
  corrected"
- `core-canon.md` → "The three combatants" (Echo and Nova rows — combat
  identity, movement, energy/VFX, readability target, for differentiating
  the two fighters' burst flavor), "Design pillars" (Skill Creates
  Spectacle, Cinematic Rhythm)

**Unrelated context to exclude:**
- `vanguard-telegraphs.md` in full — Crimson Vanguard's attack-state timing
  is not relevant to describing the player-side cinematic beat.
- `shattered-ring-reactions.md` in full — arena facts are not cinematic-beat
  facts.
- Crimson Vanguard's row in the combatants table beyond what's needed to
  keep the rival out of the player-focused burst description (the burst is
  about Echo/Nova, not the rival's presentation).

**The generator is allowed to create:**
- Separate short burst descriptions for Echo and Nova, each expressing that
  fighter's stated identity (precision/controlled vs. speed/aggressive
  momentum) and accent color (Echo's orange; Nova's cyan-white — reserved
  for combat energy/telegraphs, not a costume recolor).
- Distinct flavor for the wider first (onboarding) window versus a standard
  window, so long as the only stated mechanical difference (response time)
  is preserved and not altered.

**The generator must not invent:**
- Any burst that plays without the player having succeeded at the input —
  no automatic or free Impact Window success, ever.
- A burst duration outside the stated 1–3 second range, or a response time
  other than 0.75 s (first) / 0.35–0.50 s (standard).
- A burst that implies the rival's AI, camera, or gameplay state does not
  cleanly return afterward — see the OPEN restoration gaps; do not claim
  more certainty about restoration than the source specifies.
- A meter gain value other than the ones in `impact-window-cinematics.md`.

---

## Output 3 — Shattered Ring Environmental Reaction Pack

**What it is:** short descriptions of the arena's visible-but-controlled
reaction during major impacts, consistent with the GDD's environmental
reaction requirement and the hard Phase 1 rule that no gameplay hazards
exist.

**Likely retrieval queries:**
- "Describe how the Shattered Ring visibly reacts to a major impact."
- "Write environmental reaction flavor for the central combat floor without adding hazards."
- "What does the arena do when Crimson Vanguard lands a committed gauntlet strike nearby?"

**Exact knowledge files to retrieve:**
- `shattered-ring-reactions.md`
- `core-canon.md`

**Relevant sections / chunks:**
- `shattered-ring-reactions.md` → "Status", "Functional requirements (the
  only textual facts the GDD gives)", "Build-side notes (Phase 1 vs. Phase
  2 — not fiction, but constrains tone)"
- `core-canon.md` → "Design pillars" (Cinematic Rhythm — brief impact
  punctuation without replacing combat), "Hard constraint" (reaction must
  stay presentation, never a gameplay-affecting system)

**Unrelated context to exclude:**
- `vanguard-telegraphs.md` in full — attack-state timing is not arena
  reaction.
- `impact-window-cinematics.md` in full — meter/Clash mechanics are not
  arena facts.
- Echo/Nova/Crimson Vanguard combat-identity rows beyond the one line
  needed to keep reaction descriptions fighter-agnostic (the arena reacts
  to "a major impact," not to a specific fighter's kit).

**The generator is allowed to create:**
- Short descriptive flavor for how the central floor, far doorway, or wall
  surfaces visibly respond to a major impact (light flicker, dust,
  structural creak, surface scuffing) — visible but controlled.
- Language explicitly framing this as **presentation only** (an M5 /
  Phase 2 authored pass), not a Phase 1 gameplay system.

**The generator must not invent:**
- Any hazard, damage volume, destructible object, or physics object that
  could affect the duel — the Phase 1 hard rule is that none exist.
- A second arena, an alternate version of the Ring, or any off-screen
  location.
- Any description of the arena's appearance drawn from GDD pages 10–14 —
  those are image reference sheets with no extractable text and must never
  be cited or inferred from.
- A history or origin for the Shattered Ring — that is out of scope for
  this pack (no lore/history output was confirmed).

---

## Shared exclusion rule for all three outputs

No retrieval for any output may pull governed numeric values (timing
ranges, meter gains, health thresholds, Clash gate numbers) into generated
prose as if they were newly authored or changeable. Numbers may be quoted
verbatim as grounding context; they may never be restated as altered,
rounded, or newly invented values.
