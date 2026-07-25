# Project Brief — Ascendant Impact

This is the commander's seed brief and the single input the **designer** agent
consumes. It is distilled from the GDD — **`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf`**
(Assignment #02, Revised, **v0.4, 2026-07-24**, Anthony T.) — which is the **source
of truth**. `Ascendant_Impact_GDD_Assignment_01_Anthony.pdf` is the earlier draft and
is **superseded**; do not cite it. Where the two disagree, v0.4 wins.

Everything downstream must trace back to something here. Where the GDD marks a value
**PROVISIONAL**, treat it as open and pending playtest — do not resolve it by
invention. Where it marks **SCOPE LOCK** or **deferred**, treat it as a wall.

> **The human designer owns all rules and numbers.** The `designer` *agent* is a
> research-and-planning seat. It may propose, structure, and map systems onto Unreal
> concepts. It may **not** change a number, add a mechanic, or resolve a provisional
> value on its own authority.

## Delivery schedule — ship 1 September 2026, in two phases

**THE GAME MUST BE PLAYABLE ON 1 SEPTEMBER 2026.** That is the hard ship date and it
is a **calendar constraint on design complexity**, not just a note. From 25 July 2026
that is **38 days**. Any system that cannot be built and tuned inside that window is
out of scope, no matter how good it is. The designer must design to this date: prefer
the simplest realization that satisfies the GDD, and where two approaches both work,
**pick the one that ships**.

| Phase | Window | What it means | Milestones |
|---|---|---|---|
| **Phase 1 — the basic version** | now → **1 Sept 2026** | A **playable duel** that can actually be fought start to finish, **with some design on it** — it must not read as a bare gray-box tech demo | M1 → M2 → M3 → M4, then a **thin presentation floor** |
| **Phase 2 — the polish pass** | after Phase 1 is playable | Make it as polished and as good-looking as possible: graphics, VFX, camera, sound, arena reaction, character treatment | Full **M5** |

**"Some design added" — how Phase 1 satisfies it without breaking milestone order.**
M5 is still gated behind a stable M4 and must not be interleaved into M1–M4. Phase 1
gets its visual identity a different way: **the proxies themselves are dressed**.
Instead of literal gray capsules, M1–M4 may stand up **free third-party character
meshes, animations, and arena set dressing** from the start. Choosing a proxy asset is
asset selection, not a presentation pass — it costs no schedule time and gives the
Phase 1 build a look. What stays in M5 is the **tuned** work: hit-stop feel, camera
choreography, VFX authoring, sound design, arena impact reaction, final character
treatment.

**BUDGET CONSTRAINT — assets should be free.** Prefer **$0** sources: Unreal's own
starter and template content, the **Fab** free tier and free Quixel/Megascans grants,
and **Mixamo** rigs and animations. Every asset must carry a license that permits use
in a submitted course build, and it still passes the existing **human approval and
rights review gate** below. Where no free asset exists for something, **name the gap
and propose a free fallback** — do not assume a purchase.

**Priority when the calendar and the wish list disagree: a complete, fought duel on
1 September beats a beautiful incomplete one.** M4 — a duel with a win and a loss
outcome — is the thing that must exist.

## Hard constraint — no runtime AI-model calls (GDD §04, §06)

**RUNTIME AI BOUNDARY.** Crimson Vanguard is controlled by **authored Unreal gameplay
AI**. The packaged duel **makes no runtime LLM calls, does not learn from the player,
and does not generate attacks or choreography dynamically.** No agent automation
controls Echo or Nova either — player input does.

**HUMAN APPROVAL GATE.** Generative tools may support ideation, reference
exploration, documentation, and offline draft assets. **No generated combat behavior,
character asset, animation, VFX, sound, or text enters the course build without human
review, technical validation, rights review, and explicit approval.** The designer
approves all rules and numbers.

Any downstream document proposing a runtime model call, an LLM-driven opponent, or
"adaptive AI" in the shipped build is wrong on its face and must be rejected by the
inspector.

## The game in one line (GDD §01)

Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.

The player selects **Agent Echo** or **Agent Nova** and enters the **Shattered Ring**
to fight **Crimson Vanguard / Project Valor-7** in one complete third-person duel.
Combat is **primarily real time**: movement, attacks, dodges, perfect dodges, and
counters build Ascension energy and earn brief anime-inspired cinematic bursts,
culminating in **one recoverable Final Clash**.

**Central promise:** real-time martial-arts combat rewards player skill with brief,
earned anime-style cinematic spectacle.

| Genre | Player mode | Target session | Engine / platform |
|---|---|---|---|
| Third-person action fighter | 1 player vs. authored AI; Echo or Nova selectable | **3–5 minutes** | **Unreal Engine 5.8 / PC** |

**Character motivation:** Echo and Nova are Ascendant operatives entering the
Shattered Ring to survive a **live combat evaluation** against Project Valor-7, an
armored Vanguard unit designed to push enhanced fighters beyond their operational
limits.

## Design pillars (GDD §01)

1. **Skill Creates Spectacle** — readable timing and deliberate decisions earn the
   strongest visual rewards.
2. **Cinematic Rhythm** — brief camera, hit-stop, impact-frame, and VFX bursts
   punctuate combat without replacing it.
3. **Operative Identity vs. Vanguard Force** — Echo emphasizes precision and
   controlled timing; Nova emphasizes speed and aggressive momentum; Crimson Vanguard
   embodies armor, pressure, and overwhelming force.

## SCOPE LOCK (GDD §01, §09) — do not exceed

One player, one authored AI opponent, one official arena, one shared player-combat
framework, **four** authored rival attacks, one complete duel with win and loss
outcomes.

**Included in the course prototype:**
- One player versus one authored AI opponent.
- Two selectable player avatars using **one shared core combat framework**.
- One Crimson Vanguard boss with **six states, four attacks, and a parameter-based
  Phase 2**.
- One official industrial arena, one complete duel, complete win/loss handling.
- Impact Window onboarding, Ascension Meter, Final Clash unlock, failed-Clash recovery.
- Human approval gates and no runtime LLM-controlled fighters.

**Deferred future scope — name it as deferred, never build it:**
- Local or online PvP.
- Unique Echo and Nova move sets, separate balance systems, extensive character cinematics.
- A playable Crimson Vanguard combat kit.
- Multi-enemy encounters, campaign progression, additional arenas, extended gauntlets.
- Transformations, second boss kits, additional characters, modes, weapons, story chapters.

## Control model (GDD §02) — PRESERVED

Movement, lock-on, light attacks, dodge, perfect dodge, counter, health, spacing, and
opponent reads occur **in real time**. Impact Windows and the Final Clash are **brief
authored overlays triggered by gameplay performance**. They never replace the main
combat loop, never auto-play an entire fight, and **always return control to the
player**. The duel is an action-combat game with short earned timing prompts, **not a
sequence of QTE scenes**.

## Core loop (GDD §02)

1. **READ** — read Crimson Vanguard's telegraph
2. **RESPOND** — attack, dodge, or counter
3. **BUILD** — earn Ascension energy
4. **IMPACT** — choose the timing input
5. **ESCALATE** — adapt to Phase 2
6. **CLASH** — attempt the Final Clash

## The two playable fighters (GDD §02, §07)

**SHARED PLAYER-KIT SCOPE RULE (NEW in v0.4).** Echo and Nova are selected before the
duel and share the **same prototype framework**: movement, lock-on, light attack
sequence, dodge, perfect dodge, counter, health, Ascension Meter, Impact Windows, and
Final Clash. Their initial differences are **animation presentation, stance and
movement personality, VFX language, timing flavor, and character introduction**.
Fully unique move sets, separate balance systems, and extensive character-specific
cinematics are **deferred until the base duel is stable**. One signature cinematic
variation may be considered **only after** that foundation is approved.

| | **Agent Echo** | **Agent Nova** | **Crimson Vanguard** |
|---|---|---|---|
| Height | 6'0" / 183 cm | 5'8" / 173 cm | 6'10" |
| Combat identity | Precision, controlled timing | Speed, aggressive momentum | Armor, pressure, overwhelming force |
| Movement | Deliberate spacing and counters | Fast lateral rhythm, forward intent | Committed advances, short propulsion |
| Silhouette | Lean, upright technical striker | Compact, agile layered profile | Substantially broader armored mass |
| Material family | Matte black and charcoal technical suit | Black, charcoal, orange, light-gray helmet cap | Red armor over black structure |
| Energy / VFX | Controlled orange accents | Cyan-white combat energy or selected telegraphs | Red-orange systems and warning lights |
| Role | Selectable player avatar | Selectable player avatar | Sole authored AI rival / boss |
| Readability target | Exact timing, clear counter intent | Momentum without visual noise | Threatening reach, obvious tells and recovery |

**Color direction (REVISED).** Echo keeps restrained orange accents. Nova's existing
black/charcoal/orange/light-gray costume is **preserved**; **cyan-white is reserved
for combat energy, telegraphs, or selected VFX accents** when separation is needed —
it is **not a costume recolor**. Crimson Vanguard reads through red armor, black
structure, and red-orange systems and warning lights.

**Scale.** The rival is deliberately taller and substantially broader than either
fighter, creating immediate threat and visual contrast while remaining within a scale
that supports readable close-range martial-arts combat. **The height difference must
not create unfair hidden reach or collision behavior.**

## Impact Windows (GDD §02)

A qualifying real-time event — a perfect dodge, counter, or approved combo milestone —
can open **one short contextual timing prompt**. Success extends the exchange into a
**1–3 second choreographed burst**. Failure does **not** auto-correct the input; the
game returns immediately to normal combat.

| Window | Trigger | Provisional response time | Failure result |
|---|---|---|---|
| **First Impact Window** | First successful perfect dodge or counter | **0.75 s** | No cinematic extension; return to combat with **no extra punishment** |
| **Standard Impact Window** | Approved skill event after cooldown | **0.35–0.50 s** | No extension; return to combat |

**ONBOARDING RULE (PRESERVED).** The first Impact Window is intentionally wider, but
it **still requires the player's input** and must be earned through a successful
real-time defensive action. **The game does not press the input for the player and
does not convert a miss into success.**

## Ascension Meter (GDD §03) — PRESERVED

A visible **0–100** resource earned **only through active combat decisions**. It does
**not** fill from waiting or elapsed time. All gains provisional, subject to playtest.

| Player event | Meter gain | Design intent |
|---|---|---|
| Light-combo finisher | **+5** | Small reward for sustained offense |
| Perfect dodge | **+12** | Reward a clean defensive read |
| Successful counter | **+15** | Reward converting the opening |
| Impact Window success | **+20** | Reward execution during an earned cinematic beat |
| Taking damage / waiting | **+0** | Prevent passive progress |

## Final Clash (GDD §03)

**SINGLE GATE (REVISED).** Available only when **BOTH** are true: Ascension Meter is
full at **100** AND Crimson Vanguard's health is at or below **25%**. If one condition
is met first, the Clash stays **locked** until the other is met. Once eligible, the
player **chooses** to initiate with a contextual input during neutral or after a
successful counter.

| Outcome | Rule | Return state |
|---|---|---|
| **Success** | Complete **both timing beats**; the finishing sequence defeats Crimson Vanguard and ends the duel | Win screen |
| **Failure** | Separate both fighters; preserve current health with Crimson Vanguard held at a **1 HP floor**; reduce meter to **50**; apply a **3-second** re-trigger cooldown | Return to Neutral; rebuild meter and try again |

**FAILED CLASH RECOVERY (PRESERVED).** A failed Final Clash does **not** restart the
duel, kill the player automatically, or leave either fighter in a cinematic state. It
creates a meaningful meter setback, restores valid combat states, and preserves a
recoverable path to victory.

## Encounter flow (GDD §03)

| Beat | Provisional rule | Player experience |
|---|---|---|
| Opening | Selection, abbreviated entrance, then immediate control | Establish identity and stakes without delaying play |
| Phase 1 | Readable armored pressure; onboarding Impact Window available | Learn Crimson Vanguard's rhythm |
| Phase 2 | Begins at **50%** CV health; same attacks, stronger pressure | Apply learned reads under stress |
| Climax | Meter 100 + CV health ≤ 25% | Player chooses the Final Clash attempt |
| Win / Loss | Final Clash success / selected fighter health reaches zero | Complete duel loop |

## Crimson Vanguard — authored rival AI (GDD §04)

A compact **state machine or Behavior Tree** controls readable, testable armored
pressure.

**State flow:** Idle / Reposition → Select Attack → Telegraph → Active Attack →
Recover → Return to Neutral

| State | Purpose | Phase 1 | Phase 2 | Exit condition |
|---|---|---|---|---|
| Idle / Reposition | Face the selected fighter, maintain armored pressure | 0.60–1.20 s | 0.35–0.80 s | Valid range and line |
| Select Attack | Choose one of four authored attacks by range and cooldown | 0.10–0.20 s | 0.10–0.20 s | Attack selected |
| Telegraph | Show committed pose, warning lights, sound, readable direction | 0.55–0.95 s | 0.40–0.75 s | Telegraph completes |
| Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s | Active frames end |
| Recover | Expose a deliberate punish opening after the committed strike | 0.45–0.90 s | 0.35–0.75 s | Recovery completes |
| Return to Neutral | Clear attack flags, restore valid locomotion | 0.10–0.20 s | 0.10–0.20 s | Neutral restored |

**Behavioral intent.** Crimson Vanguard advances as a large armored threat: attacks
are **committed rather than random**, propulsion closes short gaps explosively,
gauntlets communicate force, and **every major offense exposes a clear recovery
opening**. Armor and scale may intensify presentation but **do not remove readable
counterplay**.

### The four authored attacks

| Attack | Range / purpose | Readability requirement |
|---|---|---|
| **A** | Close-range committed gauntlet force | Distinct wind-up and punishable recovery |
| **B** | Committed forward-pressure sequence | Visible first beat and stable tracking limit |
| **C** | Armored reach and space control | Clear body direction and visible active range |
| **D** | Short propulsion-assisted approach | Thruster cue before movement; **no hidden full-arena snap** |

### Phase 2 escalation (REVISED)

Begins when Crimson Vanguard reaches **50% health**. The phase change is **committed
on Return to Neutral**, then **signaled once** with stronger thruster output, warning
lights, sound, and armor-energy presentation. It uses the **same four authored
attacks — no transformation rig and no second move set.**

| Parameter | Phase 1 | Phase 2 |
|---|---|---|
| Reposition delay | 0.60–1.20 s | 0.35–0.80 s |
| Forward pressure | Measured advances | More frequent advances, shorter hesitation |
| Attack weighting | Balanced authored selection | More aggressive close-range and gap-closing weight |
| Presentation | Readable red-orange systems | Stronger thruster, warning-light, sound, armor-energy cues |
| Attack set | Four authored attacks | **Same** four authored attacks |

## The arena — Shattered Ring (GDD §08)

The established industrial **Shattered Ring** is **locked as the official Version 1
environment**. Alternate environment explorations do not replace it.

| Arena requirement | Version 1 function |
|---|---|
| Central combat floor | Open, readable space for spacing, lock-on, dodges, counters, Final Clash staging |
| Far doorway | Dedicated Crimson Vanguard entrance axis |
| Reverse third-person framing | Clear camera position behind the selected fighter |
| Side-on readability | Readable silhouettes and attack direction during lateral exchanges |
| Environmental reaction | Visible but controlled reaction during major impacts, **without adding gameplay hazards** |

## Selection and opening flow (GDD §07)

Editorial character-selection interface → player briefly moves between both options →
selection → technical/equipment panels animate around the selected fighter →
transition into the arena → camera moves behind the selected fighter → Crimson
Vanguard enters through the far doorway → the duel begins.

**Course-build allowance:** a **simplified selection screen and abbreviated arena
entrance** are acceptable while preserving the same readable sequence.

## Milestones — this is the build order (GDD §05)

**GRAY-BOX VERTICAL SLICE (PRESERVED).** The first vertical slice uses proxy Echo or
Nova, proxy Crimson Vanguard, the official arena footprint, **one** authored rival
attack, one player defensive response, **one** Impact Window, meter gain, and a clean
return to neutral. It proves the **real-time-to-cinematic handoff** before final
characters, VFX, or expanded choreography.

| # | Milestone | Required proof | Gate |
|---|---|---|---|
| **M1** | Combat gray box | Movement, lock-on, light sequence, dodge, perfect dodge, counter, health | Playable loop with selected proxy |
| **M2** | Rival state loop | **All six AI states and one** Crimson Vanguard attack complete without deadlock | Returns to Neutral every attempt |
| **M3** | Impact handoff | Earned prompt, success/failure branches, restored control | No forced success or stranded cinematic state |
| **M4** | Complete duel | Meter, Phase 2, Final Clash, failure recovery, win/loss | Start-to-finish course prototype |
| **M5** | Presentation pass | Approved character treatment, arena reaction, camera, VFX, sound | **Only after M4 is stable** |

No step may depend on a later milestone, and **M5 work must not be interleaved into
M1–M4.**

## Implementation safeguards (GDD §05)

- Use authored state-machine or Behavior Tree logic with **visible debug state names**
  and deterministic recovery paths.
- **Separate gameplay timing from cinematic presentation** so hit-stop, camera, and
  VFX can be disabled during diagnosis.
- **Explicitly restore** input, collision, locomotion, lock-on, and AI state after
  every Impact Window and Final Clash branch.
- Validate **both** selectable avatars against the same collision, targeting, reach,
  and arena-boundary tests.
- Treat all timing ranges, meter values, and health thresholds as **provisional**
  until validated through playtesting and finalized by the designer.

## Definition of done (GDD §09)

| Area | Acceptance condition |
|---|---|
| Combat | Real-time controls remain responsive before and after every cinematic beat |
| Selection | Either avatar enters the same complete shared-framework duel |
| AI | Crimson Vanguard completes all six states and never strands the encounter |
| Phase 2 | 50% health escalation changes pressure parameters and presentation, **not the attack set** |
| Climax | Final Clash obeys both unlock conditions and supports recovery after failure |
| Readability | Echo, Nova, and Crimson Vanguard remain legible in motion and at combat distance |
| Scope | One complete duel runs start to finish in Unreal Engine 5.8 on PC |

## Provisional decisions — open, pending playtest (GDD §10)

| Decision | v0.4 position |
|---|---|
| Exact combat timing and meter tuning | All published timing ranges, gains, and thresholds stay **provisional** until playtest review |
| Echo / Nova timing flavor | Same mechanics and balance framework; approve only **presentation-level** timing flavor at first |
| Nova cyan-white application | Combat energy, telegraphs, or selected VFX — **not** a costume recolor — unless readability testing supports more |
| Signature cinematic variation | **Deferred**; consider one per fighter only after the shared base duel is stable |
| Selection and entrance fidelity | Simplified selection screen and abbreviated arena entrance for the course build |
| Crimson Vanguard display name | Use "Crimson Vanguard / Project Valor-7" formally; **finalize the shorter in-combat UI label** |
| Scale, reach, collision validation | Validate gameplay collision and hit reach **only after** both avatars pass the same close-range tests |
| Updated concept visualization | Link **pending**; the document stands alone without it |

## What the designer agent should resolve and produce

- How the **shared player-combat framework** is realized in Unreal 5.8, and how Echo
  and Nova reskin it without forking it.
- How the **six rival states** map onto a Behavior Tree or state machine with visible
  debug state names, and how attacks **A–D** are authored as **data** rather than
  one-off graphs.
- How **Telegraph → Active Attack → Recover** windows are represented so they are
  readable by the player and retunable by the human designer without touching logic.
- How **Impact Windows** are detected and scored, including the wider first window,
  and how the five meter events hook into that.
- How **Phase 2** re-times the same four attacks through parameters, committed on
  Return to Neutral and signaled once.
- How the **Final Clash** gate, both timing beats, and failure path are structured.
- How the **separation of gameplay timing from cinematic presentation** is enforced so
  hit-stop, camera, and VFX can be disabled during diagnosis.
- What each of **M1 through M5** must contain to hit its stated gate.
- A **provisional-values table** collecting every timing/tuning number in one place
  for the human designer.
- **A Phase 1 cut line for 1 September 2026.** State plainly what is in the playable
  Phase 1 build and what is deferred to the Phase 2 polish pass, and flag any system
  in this brief that looks unlikely to be built and tuned in the remaining days.
- **A free-asset sourcing list** for the dressed Phase 1 proxies — which specific
  free sources cover Echo, Nova, Crimson Vanguard, and the Shattered Ring, and where
  no free option exists.

Anchor every decision to this brief. Leave provisional values open, treat the SCOPE
LOCK as a wall, and never propose a runtime AI-model call.
