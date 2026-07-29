# Impact Windows, Ascension Meter, and Final Clash — Cinematic Rules

Facts governing every brief cinematic beat in the duel: what triggers one,
how long it lasts, what it costs, and — critically — the restoration rule
that keeps every cinematic beat from stranding gameplay. Use this file when
generating any content that describes or names a cinematic burst, a win/loss
moment, or UI copy tied to these systems.

## Impact Windows

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

## Ascension Meter

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

## Final Clash

**Single gate — both must be true:** Ascension Meter full at **100** AND
Crimson Vanguard's health at or below **25%**. If only one condition is met,
the Clash stays locked until the other is met. The player **chooses** to
initiate with a contextual input during neutral or after a successful
counter — it never auto-triggers.

| Outcome | Rule | Return state |
|---|---|---|
| Success | Complete both timing beats; finishing sequence defeats Crimson Vanguard, ends the duel | Win screen |
| Failure | Separate both fighters; preserve current health with Crimson Vanguard held at a **1 HP floor**; reduce meter to **50**; apply a **3-second** re-trigger cooldown | Return to Neutral; rebuild meter and try again |

**Failed Clash recovery (hard rule):** a failed Final Clash does **not**
restart the duel, does **not** kill the player automatically, and does not
leave either fighter in a cinematic state. It is a meter setback with a
recoverable path back to victory.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 4 ("Ascension Meter, Final
Clash & Encounter Flow"); `project-brief.md`, "Final Clash (GDD §03)".*

## The restoration rule (why every cinematic beat must "hand back" cleanly)

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

## OPEN — restoration gaps flagged by inspection, not yet corrected

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
