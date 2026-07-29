# Retrieval evidence — impact-window-beat-pack

**Query:** Describe Echo's and Nova's cinematic bursts on a successful Impact Window, differentiated by combat identity, without implying automatic success or altering the meter gain or response-time values.

**Eligible files (manifest-restricted):** impact-window-cinematics.md, core-canon.md

**Required (pinned) chunks:** impact-window-cinematics.md — The restoration rule (why every cinematic beat must "hand back" cleanly); impact-window-cinematics.md — OPEN — restoration gaps flagged by inspection, not yet corrected

## All candidate chunks (scored)

| Score | Source file | Heading | Matched tokens |
|---|---|---|---|
| 10 | impact-window-cinematics.md | Impact Windows | automatic, cinematic, combat, impact, response, s, success, successful, time, window |
| 9 | impact-window-cinematics.md | Ascension Meter | cinematic, combat, gain, impact, meter, success, successful, time, window |
| 7 | core-canon.md | Design pillars | bursts, cinematic, combat, echo, identity, impact, nova |
| 6 | core-canon.md | High concept | cinematic, combat, echo, impact, nova, time |
| 6 | impact-window-cinematics.md | Final Clash | cinematic, impact, meter, s, success, successful |
| 5 | core-canon.md | Character motivation | combat, echo, impact, meter, nova |
| 5 | core-canon.md | The three combatants | combat, echo, identity, impact, nova |
| 5 | impact-window-cinematics.md | The restoration rule (why every cinematic beat must "hand back" cleanly) | cinematic, impact, s, success, window |
| 3 | core-canon.md | Genre / mode / session / engine | echo, impact, nova |
| 3 | impact-window-cinematics.md | OPEN — restoration gaps flagged by inspection, not yet corrected | cinematic, impact, s |
| 2 | core-canon.md | Core loop | impact, s |
| 2 | core-canon.md | Scope lock (do not exceed in generated content) | combat, impact |
| 1 | core-canon.md | Hard constraint | impact |

## Selected chunks passed to the generator (lexical top-4, score > 0, plus any required pins)

### impact-window-cinematics.md — Impact Windows

Score: 10 (matched: automatic, cinematic, combat, impact, response, s, success, successful, time, window) — selected by: lexical top-4 score [lexical]

A qualifying real-time event — a perfect dodge, counter, or approved combo
milestone — opens **one short contextual timing prompt**. Success extends
the exchange into a **1–3 second choreographed burst**. Failure does **not**
auto-correct the input; the game returns immediately to normal combat.

| Window | Trigger | Provisional response time | Failure result |
|---|---|---|---|
| First Impact Window | First successful perfect dodge or counter | 0.75 s | No cinematic extension; return to combat, no extra punishment |
| Standard Impact Window | Approved skill event after cooldown | 0.35–0.50 s | No extension; return to combat |

**Onboarding rule (hard, not a suggestion):** the first window is
intentionally wider, but it still requires the player's input and must be
earned through a successful real-time defensive action. **The game does not
press the input for the player and does not convert a miss into success.**
No generated content may describe or imply an automatic/free Impact Window
success.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 3 ("Impact Windows");
`project-brief.md`, "Impact Windows (GDD §02)".*

### impact-window-cinematics.md — Ascension Meter

Score: 9 (matched: cinematic, combat, gain, impact, meter, success, successful, time, window) — selected by: lexical top-4 score [lexical]

A visible **0–100** resource earned **only through active combat decisions**.
It does not fill from waiting or elapsed time.

| Player event | Meter gain | Design intent |
|---|---|---|
| Light-combo finisher | +5 | Small reward for sustained offense |
| Perfect dodge | +12 | Reward a clean defensive read |
| Successful counter | +15 | Reward converting the opening |
| Impact Window success | +20 | Reward execution during an earned cinematic beat |
| Taking damage / waiting | +0 | Prevent passive progress |

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 3–4 ("Ascension Meter");
`project-brief.md`, "Ascension Meter (GDD §03) — PRESERVED".*

### core-canon.md — Design pillars

Score: 7 (matched: bursts, cinematic, combat, echo, identity, impact, nova) — selected by: lexical top-4 score [lexical]

1. **Skill Creates Spectacle** — readable timing and deliberate decisions earn
   the strongest visual rewards.
2. **Cinematic Rhythm** — brief camera, hit-stop, impact-frame, and VFX bursts
   punctuate combat without replacing it.
3. **Operative Identity vs. Vanguard Force** — Echo emphasizes precision and
   controlled timing; Nova emphasizes speed and aggressive momentum; Crimson
   Vanguard embodies armor, pressure, and overwhelming force.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1–2 ("Design pillars");
`project-brief.md`, "Design pillars (GDD §01)".*

### core-canon.md — High concept

Score: 6 (matched: cinematic, combat, echo, impact, nova, time) — selected by: lexical top-4 score [lexical]

> Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.

The player selects **Agent Echo** or **Agent Nova** and enters the
**Shattered Ring** to fight **Crimson Vanguard / Project Valor-7** in one
complete third-person duel.

**Central promise:** real-time martial-arts combat rewards player skill with
brief, earned anime-style cinematic spectacle.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1 ("Executive Summary");
`project-brief.md`, "The game in one line (GDD §01)".*

### impact-window-cinematics.md — The restoration rule (why every cinematic beat must "hand back" cleanly)

Score: 5 (matched: cinematic, impact, s, success, window) — selected by: required pin (outside lexical top-4) [required]

GDD implementation safeguard: **"Restore input, collision, locomotion,
lock-on, and AI state explicitly after every Impact Window and Final Clash
branch."** The build's answer is a single `RestoreCombatState()` function
called by every branch (Impact success, Impact failure, Clash success, Clash
failure) — never four separate copies. Its job is to make the control-model
promise literal: overlays *"always return control to the player"* and never
strand gameplay.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Implementation
safeguards"); `design-brief.md`, "7.5 `RestoreCombatState()` — the single
restore function".*

### impact-window-cinematics.md — OPEN — restoration gaps flagged by inspection, not yet corrected

Score: 3 (matched: cinematic, impact, s) — selected by: required pin (outside lexical top-4) [required]

The cinematic-integration-inspector found that the current plan's restore
function does **not** yet fully specify: (1) what suspends the rival's
Behavior Tree during a 1–3 s Impact burst, (2) camera-ownership return, (3)
hitbox/trace shutdown, (4) animation-state cleanup and mid-burst death, and
(5) two transient gameplay tags left out of the clear list. These are
**required corrections before M3 sign-off** — treat "every cinematic
sequence restores gameplay cleanly" as the **rule**, and these five gaps as
**known, not-yet-closed exceptions** a critic agent should watch for in any
generated content that describes a cinematic beat as if the restoration
already fully specified (e.g., do not claim the camera or rival AI provably
resumes if a generated piece implies more certainty than the plan currently
supports).

*Source: `cinematic-integration-inspection.md`, "2. Violations" (V1–V5),
"5. Cinematic handoff audit".*

