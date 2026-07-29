# Retrieval evidence — vanguard-telegraph-pack

**Query:** Name Crimson Vanguard's four authored attacks A-D and describe a readable telegraph for each, consistent with its stated range, purpose, and readability requirement.

**Eligible files (manifest-restricted):** vanguard-telegraphs.md, core-canon.md

## All candidate chunks (scored)

| Score | Source file | Heading | Matched tokens |
|---|---|---|---|
| 10 | vanguard-telegraphs.md | The six-state loop (authored, deterministic — never LLM-driven) | attacks, authored, crimson, four, purpose, range, readable, s, telegraph, vanguard |
| 8 | vanguard-telegraphs.md | The four authored attacks (no names in the GDD — this is the gap) | attacks, authored, d, four, purpose, range, readability, requirement |
| 8 | vanguard-telegraphs.md | Phase 2 escalation (same four attacks, re-timed — never a new moveset) | attacks, authored, crimson, four, range, readable, s, vanguard |
| 6 | core-canon.md | Scope lock (do not exceed in generated content) | attacks, authored, crimson, d, four, vanguard |
| 6 | vanguard-telegraphs.md | Telegraph mechanics (for anchoring announcer/telegraph copy to real windows) | attacks, d, each, four, s, telegraph |
| 5 | vanguard-telegraphs.md | Behavioral intent (tone reference for telegraph/announcer copy) | attacks, crimson, readable, telegraph, vanguard |
| 4 | core-canon.md | The three combatants | authored, crimson, readability, vanguard |
| 4 | core-canon.md | Core loop | crimson, s, telegraph, vanguard |
| 4 | core-canon.md | Hard constraint | attacks, authored, crimson, vanguard |
| 3 | core-canon.md | Design pillars | crimson, readable, vanguard |
| 2 | core-canon.md | High concept | crimson, vanguard |
| 1 | core-canon.md | Genre / mode / session / engine | authored |
| 1 | core-canon.md | Character motivation | vanguard |

## Selected chunks passed to the generator (lexical top-4, score > 0, plus any required pins)

### vanguard-telegraphs.md — The six-state loop (authored, deterministic — never LLM-driven)

Score: 10 (matched: attacks, authored, crimson, four, purpose, range, readable, s, telegraph, vanguard) — selected by: lexical top-4 score [lexical]

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

### vanguard-telegraphs.md — The four authored attacks (no names in the GDD — this is the gap)

Score: 8 (matched: attacks, authored, d, four, purpose, range, readability, requirement) — selected by: lexical top-4 score [lexical]

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

### vanguard-telegraphs.md — Phase 2 escalation (same four attacks, re-timed — never a new moveset)

Score: 8 (matched: attacks, authored, crimson, four, range, readable, s, vanguard) — selected by: lexical top-4 score [lexical]

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

### core-canon.md — Scope lock (do not exceed in generated content)

Score: 6 (matched: attacks, authored, crimson, d, four, vanguard) — selected by: lexical top-4 score [lexical]

One player, one authored AI opponent, one official arena, one shared
player-combat framework, four authored rival attacks (A–D), one complete
duel with win and loss outcomes. Deferred and never to appear in content:
PvP, unique per-fighter move sets, a playable Crimson Vanguard, additional
arenas, additional fighters, transformations, story chapters, multiplayer,
progression.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 15 ("Course Scope Lock &
Future Expansion"); `project-brief.md`, "SCOPE LOCK (GDD §01, §09) — do not
exceed".*

