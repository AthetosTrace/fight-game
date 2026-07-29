# Crimson Vanguard — State Loop, Attacks, and Telegraphs

Facts about the authored rival AI relevant to writing attack names,
telegraph/announcer copy, and any AI-flavor text. **The GDD gives range,
purpose, and a readability requirement for each attack — no names, no
choreography prose, no telegraph copy.** That absence is a real content gap;
do not fill it with numbers or mechanics, only with names/flavor text
consistent with the facts below.

## The six-state loop (authored, deterministic — never LLM-driven)

State flow, in this order, always: **Idle / Reposition → Select Attack →
Telegraph → Active Attack → Recover → Return to Neutral**.

| State | Purpose | Phase 1 duration | Phase 2 duration | Exit condition |
|---|---|---|---|---|
| Idle / Reposition | Face the selected fighter, maintain armored pressure | 0.60–1.20 s | 0.35–0.80 s | Valid range and line |
| Select Attack | Choose one of four authored attacks by range and cooldown | 0.10–0.20 s | 0.10–0.20 s | Attack selected |
| Telegraph | Show committed pose, warning lights, sound, readable direction | 0.55–0.95 s | 0.40–0.75 s | Telegraph completes |
| Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s (unchanged) | Active frames end |
| Recover | Expose a deliberate punish opening after the committed strike | 0.45–0.90 s | 0.35–0.75 s | Recovery completes |
| Return to Neutral | Clear attack flags, restore valid locomotion | 0.10–0.20 s | 0.10–0.20 s | Neutral restored |

All timing ranges are **provisional, pending playtest** — never state a
number as final in generated copy.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Crimson Vanguard —
Authored Rival AI", state flow table); `project-brief.md`, "Crimson Vanguard
— authored rival AI (GDD §04)".*

## Behavioral intent (tone reference for telegraph/announcer copy)

Crimson Vanguard advances as a large armored threat: attacks are **committed
rather than random**, propulsion closes short gaps explosively, gauntlets
communicate force, and every major offense exposes a clear recovery opening.
Armor and scale may intensify presentation but do not remove readable
counterplay.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Behavioral intent").*

## The four authored attacks (no names in the GDD — this is the gap)

| Attack | Range / purpose | Readability requirement |
|---|---|---|
| **A** | Close-range committed gauntlet force | Distinct wind-up and punishable recovery |
| **B** | Committed forward-pressure sequence | Visible first beat and stable tracking limit |
| **C** | Armored reach and space control | Clear body direction and visible active range |
| **D** | Short propulsion-assisted approach | Thruster cue before movement; **no hidden full-arena snap** |

**Exactly four attacks exist. No fifth attack, no alternate move set, no
per-phase-exclusive attack may appear in generated content.**

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Four-attack course
set"); `project-brief.md`, "The four authored attacks".*

## Phase 2 escalation (same four attacks, re-timed — never a new moveset)

Begins when Crimson Vanguard reaches **50% health**. The phase change is
committed on Return to Neutral, then signaled **once** with stronger thruster
output, warning lights, sound, and armor-energy presentation. Uses the
**same four authored attacks — no transformation rig and no second move
set.**

| Parameter | Phase 1 | Phase 2 |
|---|---|---|
| Reposition delay | 0.60–1.20 s | 0.35–0.80 s |
| Forward pressure | Measured advances | More frequent advances, shorter hesitation |
| Attack weighting | Balanced authored selection | More aggressive close-range and gap-closing weight |
| Presentation | Readable red-orange systems | Stronger thruster, warning-light, sound, armor-energy cues |
| Attack set | Four authored attacks | Same four authored attacks |

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 6 ("Phase 2 escalation");
`project-brief.md`, "Phase 2 escalation (REVISED)".*

## Telegraph mechanics (for anchoring announcer/telegraph copy to real windows)

Each attack montage carries, in order: `ANS_Telegraph` (pose hold + warning
lights, no hitbox), `ANS_ActiveHit` (the hitbox trace window), `ANS_Recover`
(the punish opening), and `ANS_CounterWindow` (overlaps late telegraph/early
active — the legal counter read). Attack B additionally locks tracking at a
fixed point ("stable tracking limit"); Attack D's travel is hard-capped by
data (no hidden full-arena snap).

*Source: `design-brief.md`, "5.1 The three windows are Anim Notify States...",
"5.3 Attacks A–D are data, not four graphs".*
