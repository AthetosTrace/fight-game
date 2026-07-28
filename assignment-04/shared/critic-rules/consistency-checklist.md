# Consistency Checklist — Critic Agent

The critic agent runs against every generated output before it is shown as
final. Each check names a specific failure mode, how to detect it, and the
required correction. This checklist is the minimum bar for Assignment #04's
Consistency Checking criterion — the critic must catch and **show the
correction for** at least one real hit from this list, not merely claim it
checked.

## 1. Nova mistaken for the AI boss

**Detect:** generated text assigns Nova the role of authored rival, AI
opponent, "boss," or antagonist, or describes her as anything other than a
selectable player avatar alongside Echo.
**Why it's wrong:** Crimson Vanguard / Project Valor-7 is the sole authored
AI rival. Nova was an authored rival only in the superseded v0.1 draft.
**Correction:** rewrite so Nova is a selectable player avatar (parity with
Echo); Crimson Vanguard remains the sole AI opponent.
*Ground truth: `core-canon.md`, "The three combatants"; `gdd/ascendant-impact-gdd-v0.4.md` Page 8, Page 16 (Revision log).*

## 2. Runtime-learning or runtime-LLM behavior implied

**Detect:** generated text describes Crimson Vanguard (or any fighter) as
learning from the player, adapting via a model, generating attacks
dynamically, calling an AI/LLM at runtime, or otherwise implies shipped
runtime AI-model behavior.
**Why it's wrong:** the shipped game makes no runtime AI-model calls.
Crimson Vanguard is deterministic authored logic (state machine / Behavior
Tree) with a weighted-but-authored attack selection.
**Correction:** rewrite so any "intelligence" language is reframed as
authored/deterministic (e.g., "reads the fight" → "authored state machine
selects among four fixed attacks").
*Ground truth: `core-canon.md`, "Hard constraint"; `gdd/ascendant-impact-gdd-v0.4.md` Page 5, Page 7.*

## 3. Automatic or free Impact Window success

**Detect:** generated text implies an Impact Window succeeds without player
input, that mashing/holding the input guarantees success, that a miss is
converted to success, or that the prompt can be "auto-played."
**Why it's wrong:** the onboarding rule is explicit — the game does not
press the input for the player and does not convert a miss into success,
even on the wider first window.
**Correction:** rewrite to state the window requires a correctly timed
player input; failure returns to combat with no cinematic extension.
*Ground truth: `impact-window-cinematics.md`, "Impact Windows"; `gdd/ascendant-impact-gdd-v0.4.md` Page 3.*

## 4. Extra arenas or a fifth/altered rival attack

**Detect:** generated text introduces a second arena, an arena variant, an
off-screen duel location, a fifth Crimson Vanguard attack, a merged/renamed
attack that isn't one of A–D, or a phase-exclusive attack.
**Why it's wrong:** SCOPE LOCK fixes one official arena (Shattered Ring) and
exactly four authored attacks, unchanged across both phases.
**Correction:** remove the extra arena/attack; map any new attack idea back
onto one of A–D or cut it entirely.
*Ground truth: `shattered-ring-reactions.md`, "Status"; `vanguard-telegraphs.md`, "The four authored attacks"; `gdd/ascendant-impact-gdd-v0.4.md` Page 15.*

## 5. Altered governed numbers

**Detect:** any generated text restates a governed timing range, meter gain,
health threshold, or Clash gate value with a different number than the
knowledge base carries, or presents an OPEN/provisional value as final and
fixed.
**Why it's wrong:** every number in the GDD is carried through unchanged and
is the human designer's alone to set; provisional values must stay marked
provisional.
**Correction:** restore the exact governed number, or if the value is OPEN,
mark it OPEN rather than asserting a number.
*Ground truth: `impact-window-cinematics.md`; `design-brief.md` §13 (Provisional values table).*

## 6. Cinematic sequences that fail to restore gameplay

**Detect:** generated text describes an Impact Window burst or Final Clash
beat that leaves the player without input, leaves the rival AI permanently
paused, skips returning camera/collision/locomotion, or otherwise implies a
cinematic beat that doesn't hand control back to the player.
**Why it's wrong:** every cinematic overlay must explicitly restore input,
collision, locomotion, lock-on, and AI state — overlays never replace the
main combat loop and always return control to the player.
**Correction:** rewrite so the described sequence ends with an explicit,
clean return to live combat; do not claim more certainty about restoration
than the plan currently specifies (see the OPEN restoration gaps noted in
`impact-window-cinematics.md`).
*Ground truth: `impact-window-cinematics.md`, "The restoration rule" and "OPEN — restoration gaps"; `cinematic-integration-inspection.md` §2, §5.*

## 7. Scope expansion beyond the single duel

**Detect:** generated text references PvP, multiplayer, a playable Crimson
Vanguard, additional fighters, campaign/story progression, multiple duels,
or any deferred future-scope item as if it exists in the course prototype.
**Why it's wrong:** the prototype is one player, one authored AI opponent,
one arena, one duel with a win and a loss outcome — everything else is
deferred future scope and must never be designed or implied as present.
**Correction:** cut the scope-expanding reference; if the idea has merit,
label it explicitly as deferred future scope, out of the current build.
*Ground truth: `core-canon.md`, "Scope lock"; `gdd/ascendant-impact-gdd-v0.4.md` Page 15.*

---

## Process note

For every generated output, the critic must show its check results as
**before / flagged issue / after (corrected)** — a claim of "checked, no
issues" without the retrieved-context comparison does not satisfy the
Assignment #04 Consistency Checking criterion, which requires the
correction to be **shown, not claimed**.
