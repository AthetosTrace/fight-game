# Core Canon — Ascendant Impact

Concise reference for the game's high concept, characters, and setting. Facts
only — no invented lore. Every chunk below cites its source file and heading
so retrieval can quote it directly.

## High concept

> Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.

The player selects **Agent Echo** or **Agent Nova** and enters the
**Shattered Ring** to fight **Crimson Vanguard / Project Valor-7** in one
complete third-person duel.

**Central promise:** real-time martial-arts combat rewards player skill with
brief, earned anime-style cinematic spectacle.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1 ("Executive Summary");
`project-brief.md`, "The game in one line (GDD §01)".*

## Genre / mode / session / engine

| Genre | Player mode | Target session | Engine / platform |
|---|---|---|---|
| Third-person action fighter | 1 player vs. authored AI; Echo or Nova selectable | 3–5 minutes | Unreal Engine 5.8 / PC |

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1 ("Executive Summary").*

## Character motivation

Echo and Nova are **Ascendant operatives** entering the Shattered Ring to
survive a **live combat evaluation** against Project Valor-7, an armored
Vanguard unit "designed to push enhanced fighters beyond their operational
limits."

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1–2 ("Executive Summary" /
character motivation note); `project-brief.md`, "The game in one line (GDD §01)".*

**OPEN / not defined by the GDD:** what "Ascendant operative" means as an
in-world program or institution, and what the Ascension Meter represents
in-fiction. The GDD gives the meter numbers only, no explanation. Do not
invent an origin for either without flagging it as new fiction pending
designer approval.

## Design pillars

1. **Skill Creates Spectacle** — readable timing and deliberate decisions earn
   the strongest visual rewards.
2. **Cinematic Rhythm** — brief camera, hit-stop, impact-frame, and VFX bursts
   punctuate combat without replacing it.
3. **Operative Identity vs. Vanguard Force** — Echo emphasizes precision and
   controlled timing; Nova emphasizes speed and aggressive momentum; Crimson
   Vanguard embodies armor, pressure, and overwhelming force.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1–2 ("Design pillars");
`project-brief.md`, "Design pillars (GDD §01)".*

## The three combatants

| | Agent Echo | Agent Nova | Crimson Vanguard |
|---|---|---|---|
| Height | 6'0" / 183 cm | 5'8" / 173 cm | 6'10" |
| Combat identity | Precision, controlled timing | Speed, aggressive momentum | Armor, pressure, overwhelming force |
| Movement | Deliberate spacing and counters | Fast lateral rhythm, forward intent | Committed advances, short propulsion |
| Silhouette | Lean, upright technical striker | Compact, agile layered profile | Substantially broader armored mass |
| Material family | Matte black and charcoal technical suit | Black, charcoal, orange, light-gray helmet cap | Red armor over black structure |
| Energy / VFX | Controlled orange accents | Cyan-white combat energy or selected telegraphs (**not a costume recolor**) | Red-orange systems and warning lights |
| Role | Selectable player avatar | Selectable player avatar | **Sole authored AI rival / boss** |
| Readability target | Exact timing, clear counter intent | Momentum without visual noise | Threatening reach, obvious tells and recovery |

**Governed fact, do not confuse:** Nova is a **selectable player avatar**,
not the AI opponent. Crimson Vanguard / Project Valor-7 is the **sole**
authored AI rival. (Nova was an authored rival in the superseded v0.1 draft —
that is reversed in v0.4 and must never be cited.)

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 8 ("Character Readability
Comparison"); `project-brief.md`, "The two playable fighters (GDD §02, §07)".*

## Core loop

1. **READ** — read Crimson Vanguard's telegraph
2. **RESPOND** — attack, dodge, or counter
3. **BUILD** — earn Ascension energy
4. **IMPACT** — choose the timing input
5. **ESCALATE** — adapt to Phase 2
6. **CLASH** — attempt the Final Clash

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 2 ("Core loop");
`project-brief.md`, "Core loop (GDD §02)".*

## Scope lock (do not exceed in generated content)

One player, one authored AI opponent, one official arena, one shared
player-combat framework, four authored rival attacks (A–D), one complete
duel with win and loss outcomes. Deferred and never to appear in content:
PvP, unique per-fighter move sets, a playable Crimson Vanguard, additional
arenas, additional fighters, transformations, story chapters, multiplayer,
progression.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 15 ("Course Scope Lock &
Future Expansion"); `project-brief.md`, "SCOPE LOCK (GDD §01, §09) — do not
exceed".*

## Hard constraint

The shipped game makes **no runtime AI-model calls**. Crimson Vanguard is
deterministic authored Unreal gameplay AI — a state machine / Behavior Tree.
No learning, no dynamically generated attacks or choreography.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("REVISED — RUNTIME AI
BOUNDARY"); `project-brief.md`, "Hard constraint — no runtime AI-model calls
(GDD §04, §06)".*
