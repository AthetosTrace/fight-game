# Retrieval evidence — shattered-ring-reaction-pack

**Query:** Describe how the Shattered Ring's central floor, far doorway, and wall surfaces visibly react to a major impact, as presentation only, without adding gameplay hazards.

**Eligible files (manifest-restricted):** shattered-ring-reactions.md, core-canon.md

**Required (pinned) chunks:** shattered-ring-reactions.md — Build-side notes (Phase 1 vs. Phase 2 — not fiction, but constrains tone)

## All candidate chunks (scored)

| Score | Source file | Heading | Matched tokens |
|---|---|---|---|
| 12 | shattered-ring-reactions.md | Functional requirements (the only textual facts the GDD gives) | adding, central, doorway, far, floor, gameplay, hazards, impact, major, only, ring, shattered |
| 6 | shattered-ring-reactions.md | OPEN — no history exists (a named content gap) | doorway, far, floor, ring, s, shattered |
| 4 | core-canon.md | High concept | central, impact, ring, shattered |
| 4 | core-canon.md | Character motivation | impact, only, ring, shattered |
| 3 | shattered-ring-reactions.md | Status | impact, ring, shattered |
| 3 | shattered-ring-reactions.md | Build-side notes (Phase 1 vs. Phase 2 — not fiction, but constrains tone) | hazards, ring, shattered |
| 2 | core-canon.md | Core loop | impact, s |
| 2 | core-canon.md | Hard constraint | gameplay, impact |
| 1 | core-canon.md | Genre / mode / session / engine | impact |
| 1 | core-canon.md | Design pillars | impact |
| 1 | core-canon.md | The three combatants | impact |
| 1 | core-canon.md | Scope lock (do not exceed in generated content) | impact |

## Selected chunks passed to the generator (lexical top-4, score > 0, plus any required pins)

### shattered-ring-reactions.md — Functional requirements (the only textual facts the GDD gives)

Score: 12 (matched: adding, central, doorway, far, floor, gameplay, hazards, impact, major, only, ring, shattered) — selected by: lexical top-4 score [lexical]

| Arena requirement | Version 1 function |
|---|---|
| Central combat floor | Open, readable space for spacing, lock-on, dodges, counters, Final Clash staging |
| Far doorway | Dedicated Crimson Vanguard entrance axis |
| Reverse third-person framing | Clear camera position behind the selected fighter |
| Side-on readability | Readable silhouettes and attack direction during lateral exchanges |
| Environmental reaction | Visible but controlled reaction during major impacts, **without adding gameplay hazards** |

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 9 ("Official arena
direction" table); `project-brief.md`, "The arena — Shattered Ring (GDD
§08)".*

### shattered-ring-reactions.md — OPEN — no history exists (a named content gap)

Score: 6 (matched: doorway, far, floor, ring, s, shattered) — selected by: lexical top-4 score [lexical]

The GDD gives Shattered Ring no backstory, no in-world explanation for why
this industrial space hosts combat evaluations, and no name origin. Any
generated lore for Shattered Ring is **new fiction**, not extracted fact —
it must be flagged as such and must not contradict the functional
requirements above (e.g., it cannot imply the floor is anything but open and
readable, or that the far doorway serves any purpose other than the rival's
entrance axis).

*Source: `CLAUDE.md`, "Where this game is genuinely thin — candidate content
gaps for Content Fit."*

### core-canon.md — High concept

Score: 4 (matched: central, impact, ring, shattered) — selected by: lexical top-4 score [lexical]

> Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.

The player selects **Agent Echo** or **Agent Nova** and enters the
**Shattered Ring** to fight **Crimson Vanguard / Project Valor-7** in one
complete third-person duel.

**Central promise:** real-time martial-arts combat rewards player skill with
brief, earned anime-style cinematic spectacle.

*Source: `gdd/ascendant-impact-gdd-v0.4.md`, Page 1 ("Executive Summary");
`project-brief.md`, "The game in one line (GDD §01)".*

### core-canon.md — Character motivation

Score: 4 (matched: impact, only, ring, shattered) — selected by: lexical top-4 score [lexical]

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

### shattered-ring-reactions.md — Build-side notes (Phase 1 vs. Phase 2 — not fiction, but constrains tone)

Score: 3 (matched: hazards, ring, shattered) — selected by: required pin (outside lexical top-4) [required]

Environmental reaction is **deferred to M5 / Phase 2**. The Phase 1
requirement that survives is the negative one: the arena contains **no
hazards, no damage volumes, and no physics objects that can affect the
duel.** Any generated arena flavor text must not describe hazards, traps, or
interactive terrain — none exist and none are planned for Phase 1.

*Source: `design-brief.md`, "10.2 Shattered Ring — Phase 1 arena spec".*

