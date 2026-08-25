# Ascendant Impact — Game Design Document

## Version 1.0 — FINAL DRAFT

| | |
|---|---|
| **Title** | Ascendant Impact |
| **Version** | **1.0 — final draft** (supersedes v0.4, 2026-07-24, on approval) |
| **Date** | 2026-08-17 |
| **Ship date** | **1 September 2026 — 15 days from this draft** |
| **Engine / platform** | Unreal Engine 5.8 / PC, Blueprint-first |
| **Genre / mode** | Third-person action fighter · 1 player vs. authored AI · Echo or Nova selectable |
| **Target session** | 3–5 minutes, one complete duel |
| **Central promise** | Real-time martial-arts combat rewards player skill with brief, earned anime-style cinematic spectacle |

---

## 00. How to read this document, and what authority it carries

**This is a draft, not yet the source of truth.** Until it is approved and re-issued as
the revised PDF, `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` (v0.4) remains
the source of truth and `gdd/` remains its mechanical export. Nothing in this draft has
been written back into `gdd/`, which is generated and never hand-edited
(`design/decisions.md`, rule 2).

**What v1.0 adds to v0.4.** v0.4 described a game. v1.0 describes *the same game*, plus:
what has actually been built between 2026-07-24 and today, every value that has been
researched or settled since, the honest gap between the two, and the plan that gets a
complete fought duel onto disk by 1 September.

**Nothing in v0.4's authored design has been reversed.** Scope lock, pillars, the core
loop, the meter, the double gate, the six-state rival, the four-attack set, the no-runtime-AI
rule, and the milestone order all stand exactly as written.

### Status key — every value in this document carries one

| Tag | Meaning |
|---|---|
| **LOCKED** | Authored in GDD v0.4. Not a tuning value; changing it changes what the game is. |
| **APPROVED** | Decided by the designer of record since v0.4 and recorded in `design/decisions.md`. Binding. |
| **PROPOSED** | Researched, with a recommendation on disk, **and not decided.** No agent, document, or build may treat it as canon. |
| **OPEN** | No answer yet. Named here so it is visible rather than silently filled. |
| **BUILT** | Exists and runs in the Unreal project today, with PIE evidence. |

**The single most important rule this document keeps:** a **PROPOSED** number is not a
number. It may be typed into a document, never into a Blueprint default. The designer of
record owns every one of them.

---

## 01. Executive summary

*Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.*

The player selects **Agent Echo** or **Agent Nova** and enters the **Shattered Ring** to
fight **Crimson Vanguard / Project Valor-7** in one complete third-person duel. Combat is
primarily real time: movement, attacks, dodges, perfect dodges, and counters build
Ascension energy and earn brief anime-inspired cinematic bursts, culminating in one
recoverable **Final Clash**. **LOCKED.**

**Scope lock — reaffirmed without change. LOCKED.** One player, one authored AI opponent,
one official arena, one shared player-combat framework, four authored rival attacks, one
complete duel with win and loss outcomes.

### Design pillars — LOCKED

| # | Pillar | Player-facing meaning |
|---|---|---|
| 1 | **Skill Creates Spectacle** | Readable timing and deliberate decisions earn the strongest visual rewards. |
| 2 | **Cinematic Rhythm** | Brief camera, hit-stop, impact-frame, and VFX bursts punctuate combat without replacing it. |
| 3 | **Operative Identity vs. Vanguard Force** | Echo emphasizes precision and controlled timing; Nova emphasizes speed and aggressive momentum; Crimson Vanguard embodies armor, pressure, and overwhelming force. |

**Character motivation. LOCKED.** Echo and Nova are Ascendant operatives entering the
Shattered Ring to survive a live combat evaluation against Project Valor-7, an armored
Vanguard unit designed to push enhanced fighters beyond their operational limits.

### What changed in the world since v0.4

v0.4 was written before a line of the game existed. Since then a playable graybox duel
exists in Unreal — movement, a duel camera, a telegraphed rival strike the player can
whiff or interrupt, damage, a HUD, a knockout, and a jump-over side-switch — and a full
design-research pass has produced a recommended value for nearly every blank the GDD
deliberately left. **§05 states exactly what is in the build. §12 states exactly what is
still unapproved. §10 is the plan that closes the distance.**

---

## 02. Real-time combat and the selectable player roster

*The duel is an action-combat game with short earned timing prompts, not a sequence of
QTE scenes.*

**Control model. LOCKED.** Movement, lock-on, light attacks, dodge, perfect dodge,
counter, health, spacing, and opponent reads occur in real time. Impact Windows and the
Final Clash are brief authored overlays triggered by gameplay performance. They never
replace the main combat loop, never auto-play an entire fight, and always return control
to the player.

**Core loop. LOCKED.**
`1 READ` the rival's telegraph → `2 RESPOND` attack, dodge, or counter → `3 BUILD`
Ascension energy → `4 IMPACT` choose the timing input → `5 ESCALATE` adapt to Phase 2 →
`6 CLASH` attempt the Final Clash.

### Selectable roster — LOCKED

| Fighter | Combat identity | Prototype expression |
|---|---|---|
| **Agent Echo** — 6'0" / 183 cm | Lean precision striker | Controlled spacing, deliberate movement, perfect-dodge timing, counters, restrained orange accents |
| **Agent Nova** — 5'8" / 173 cm | Agile pressure striker | Faster visual rhythm, lateral movement, aggressive momentum, preserved costume palette, cyan-white combat energy |

**Shared player-kit scope rule. LOCKED.** Echo and Nova are selected before the duel and
share the same prototype framework: movement, lock-on, light attack sequence, dodge,
perfect dodge, counter, health, Ascension Meter, Impact Windows, and Final Clash. Their
initial differences are animation presentation, stance and movement personality, VFX
language, timing flavor, and character introduction. Fully unique move sets, separate
balance systems, and extensive character-specific cinematics are deferred until the base
duel is stable.

### Player combat kit — the tuning layer

Every row below fills a blank v0.4 deliberately left open. **All PROPOSED.** They are the
first batch that must be signed, because M1 cannot be signed off without them (§12).

| System | Recommended value | Status | Home |
|---|---|---|---|
| Player max health (both fighters, identical) | **100** | PROPOSED (Q1) | `DA_TuningGlobals` |
| Light combo sections | **3** — `S_Hit1` / `S_Hit2` / `S_Finisher`, ≈1.0 s total | PROPOSED (Q5) | `AM_Player_LightCombo` |
| Light hit / finisher damage | **5** / **10**, combo total **20** | PROPOSED (Q4) | combo notify data |
| Combo input buffer | **0.25 s** (75% of a section, stated as a ratio) | PROPOSED (Q28) | `AM_Player_LightCombo` |
| Dodge invulnerability | **0.28 s**, spanning `[0.03, 0.31]` of `AM_Player_Dodge` | PROPOSED (Q6) | `ANS_IFrame` |
| **Perfect-dodge window** | **0.12 s**, `[0.03, 0.15]` — front 43% of the i-frame window | **PROPOSED · BLOCKING** (Q7) | `ANS_PerfectDodge` |
| Counter whiff lockout | **0.55 s** | PROPOSED (Q8) | `AM_Player_CounterWhiff` |
| Walk speed / strafe / backpedal | **600** / **420** / **360** uu/s, identical for both fighters | PROPOSED (Q15) | `DA_FighterProfile` |
| Dodge distance | **400 cm**, delivered by Motion Warping | PROPOSED (Q16) | `DA_FighterProfile` |
| Montage play rate (cosmetic only) | **1.000 / 1.000, identical** | PROPOSED (Q14) | `DA_FighterProfile` |
| Lock-on acquire / break / interp / aim socket | **3000 cm** / **3300 cm** / **6.0** / **140 cm at −8°** | PROPOSED (Q11) | `BP_LockOnComponent` |

**Three structural findings that travel with those numbers and are not optional:**

1. **Q14 must be renamed `CosmeticMontagePlayRate`** and restricted to a four-montage
   allowlist carrying no gameplay notify states, routed through one library node that
   `ensure()`s the montage is notify-free. Otherwise per-fighter play rate silently scales
   the i-frame and perfect-dodge windows into per-fighter difficulty. The guard must be
   **scoped to the player kit** — the rival's telegraph and recover scaling legitimately
   uses play rate, and an unscoped guard fires falsely.
2. **Q16 uses Motion Warping deliberately.** Warping changes displacement without touching
   the montage timeline that Q6 and Q7 sit on. Play rate would move both.
3. **`ANS_ActiveHit` and `ANS_ComboLink` overlap on the same section and must not be
   merged.** `bComboQueued` clears on next-section begin and on any montage interruption.
   A successful counter must never play `AM_Player_CounterWhiff`.

**Known weakness, stated plainly.** Q8's magnitude has no prior-art support — no shipped
game publishes whiffed-parry recovery frames — and it is derived purely from the GDD's own
telegraph and recover ranges. It is the weakest-sourced number in the player kit. Q8's
anti-spam intent also **fails against slow Phase 1 telegraphs (0.75–0.95 s)**; closing that
gap needs ~0.95 s of lockout, which is unplayable. It is accepted as a beginner crutch that
dies at Phase 2, and it forces a rule on §04: **do not author all four attacks near 0.95 s.**

### Impact Windows — LOCKED

A qualifying real-time event — a perfect dodge, a counter, or an approved combo milestone —
can open one short contextual timing prompt. Success extends the exchange into a **1–3
second** choreographed burst. Failure does not auto-correct the input; the game returns
immediately to normal combat.

| Window | Trigger | Response time | Failure result |
|---|---|---|---|
| **First Impact Window** | First successful perfect dodge or counter | **0.75 s** (LOCKED) | No cinematic extension; return to combat with no extra punishment |
| **Standard Impact Window** | Approved skill event after cooldown | **0.35–0.50 s** (LOCKED range) | No extension; return to combat |
| *Cooldown between windows* | — | **7.0 s**, clocked on window *close*, **first window exempt** | PROPOSED (Q26) |

**Onboarding rule. LOCKED.** The first Impact Window is intentionally wider, but it still
requires the player's input and must be earned through a successful real-time defensive
action. The game does not press the input for the player and does not convert a miss into
success. **The first-window cooldown exemption is therefore not optional** — applying the
cooldown to the first window would break this rule.

---

## 03. Ascension Meter, Final Clash, and encounter flow

### Ascension Meter — LOCKED

A visible **0–100** resource earned only through active combat decisions. It does not fill
from waiting or elapsed time.

| Player event | Meter gain | Design intent |
|---|---|---|
| Light-combo finisher | **+5** | Small reward for sustained offense |
| Perfect dodge | **+12** | Reward a clean defensive read |
| Successful counter | **+15** | Reward converting the opening |
| Impact Window success | **+20** | Reward execution during an earned cinematic beat |
| Taking damage / waiting | **+0** | Prevent passive progress |

**Meter decay: none. PROPOSED (Q9) — and constrained.** `MeterDecayRate` should not exist
as a variable at all: no Tick, no timer, no float. This is not a preference. Constraint
**C1** of the approved Q22 requires it, and it is shown falsifiably — a decay of just
**0.76 pts/s** zeroes a struggling player's income and makes the game unwinnable while the
loss condition stays live.

**What the meter actually is, corrected.** Research established that no cooldown value in
3–8 s can make the meter a genuine *second race* against the health gate: with Impact
Windows disabled entirely, twenty finishers still fill the meter in ~84 s against a health
gate at ~173 s, and every lever to halve that is closed (gains are GDD-fixed, C1 forbids
decay, the 0–100 ceiling is GDD-fixed). **The meter is an anti-passivity floor, not a
race.** Q26 = 7 s still cuts the +20 row's dominance from a ~2.25× speedup to ~1.67×.

### Final Clash unlock — LOCKED

The Final Clash becomes available only when **BOTH** conditions are true: **Ascension
Meter is full at 100 AND Crimson Vanguard's health is at or below 25%.** If one condition
is met first, the Clash remains locked until the other is met. Once eligible, the player
chooses to initiate the Clash with a contextual input during neutral or after a successful
counter.

### The 1 HP floor is permanent — APPROVED, 2026-08-02 (Q22)

**This is the one design decision carrying the designer of record's recorded approval, and
it is binding on everything downstream.**

`MinHealthFloor = 1` on the rival's `BP_HealthComponent` from `BeginPlay`, lowered to `0`
only by `ClashSuccess()` immediately before it applies lethal damage. **The Final Clash is
the only way to win the duel.** Chip damage can pin Crimson Vanguard at 1 HP forever; it can
never kill him.

Rationale: the GDD's own encounter-flow table lists exactly one win condition. Reading it
the other way requires *adding* a win condition the GDD never writes down; this reading only
widens the scope of a floor the GDD does state. It makes the double gate meaningful and
makes the meter — and therefore skill — the only route to the ending.

**Three constraints follow from Q22 and bind every answer below it:**

| | Constraint | State |
|---|---|---|
| **C1** | Q9 must resolve to *no meter decay*, or the tail becomes a dead end | Satisfied by the Q9 recommendation |
| **C2** | The HUD must show **which gate is still locked** once the health bar visibly pins | **Mandatory, not optional** — see §05 and the post-failed-Clash dead time below |
| **C3** | Q2 must be tuned so ≤25% rival health and meter 100 arrive close together | **NOT SATISFIED — OPEN, and the designer's call.** See §12, item 64 |

### Final Clash resolution — LOCKED

| Outcome | Rule | Return state |
|---|---|---|
| **Success** | Complete both timing beats; the finishing sequence defeats Crimson Vanguard and ends the duel | Win screen |
| **Failure** | Separate both fighters; preserve current health with Crimson Vanguard held at a **1 HP floor**; reduce meter to **50**; apply a **3-second** re-trigger cooldown | Return to Neutral; rebuild meter and try again |

**Failed-Clash recovery. LOCKED.** A failed Final Clash does not restart the duel, kill the
player automatically, or leave either fighter in a cinematic state. It creates a meaningful
meter setback, restores valid combat states, and preserves a recoverable path to victory.

### Final Clash execution layer — PROPOSED

| Parameter | Recommended | Status | Home |
|---|---|---|---|
| Beat-1 lead-in after initiation | **1.2 s** (band 1.0–1.3), authored as `CounterRecoveryLength + 0.6 s` | PROPOSED (Q19) | `BP_FinalClashDirector` |
| Both beat windows | **0.50 s, identical** — the top of the published 0.35–0.50 s Standard range | PROPOSED (Q20) | `BP_FinalClashDirector` |
| Separation on failure | **1200 cm** along the arena long axis, midpoint push with clamp-and-redistribute (band 1100–1300) | PROPOSED (Q21) | `BP_FinalClashDirector` |
| Clash input | **Reuse `IA_Impact`** — one action, one `IMC_Duel`, routed by a `bClashBeatOpen` bool | PROPOSED (Q17) | `IMC_Duel` |
| Retry timer | **No timer — the variable should not exist.** Under Q22 a clock converts a bounded retry loop into a hard fail. Two terminal branches, not three | PROPOSED (Q23) | `BP_DuelDirector` |

- **Q19 corrects a defect in the design brief's own range.** The brief offered 0.5–1.5 s;
  **1.5 s is unsafe** — the earliest legal Phase 2 strike after a counter is 1.30 s, so
  1.5 s would let the player Clash out of an incoming hit.
- **Q20 argues against making beat 2 tighter.** Under Q22 that makes the more expensive
  failure the more likely one. *Asura's Wrath* is the named failure mode; *Final Fantasy
  XVI*'s unfailable clash is rejected by name against the GDD's no-auto-success rule.
- **Q21 implementation:** `Teleport = true`, not sweep; `ProjectPointToNavigation` first;
  applied **under the camera cut**.

**Retry-loop verdict: acceptable, with margin — but the penalty is regressive.** One retry
costs ≈19 s (strong player) to ≈71 s (struggling player). The GDD's 3-second cooldown is
never binding; the fastest possible rebuild is 13.8 s. A competent player can fail four
times and still finish inside 5:00. The tail cannot run away, because the loss condition
bounds it — the struggling player statistically dies during their first retry.

> **The question this document most wants the designer to answer.** The practical meaning
> of Q22 plus Q20 is that a player who cannot execute the two beats **loses the duel rather
> than grinding it out**. That is defensible — it is *Sekiro*'s position — but it makes
> *"I fought well for four minutes and lost to two timing beats"* a reachable outcome. If
> that is not the intended experience, the lever is Q20's window, not the Q22 floor.

### Encounter flow — LOCKED

| Beat | Rule | Player experience |
|---|---|---|
| **Opening** | Selection, abbreviated entrance, then immediate control | Establish identity and stakes without delaying play |
| **Phase 1** | Readable armored pressure; onboarding Impact Window available | Learn Crimson Vanguard's rhythm |
| **Phase 2** | Begins at **50%** Crimson Vanguard health; same attacks, stronger pressure | Apply learned reads under stress |
| **Climax** | Meter **100** + Crimson Vanguard health **≤25%** | Player chooses the Final Clash attempt |
| **Win / Loss** | Final Clash success / selected fighter health reaches zero | Complete duel loop |

**Two economy tensions carried into playtest, unresolved:**

1. **Post-failed-Clash rebuild leaves ~15–35 s of genuinely inert damage** — the player is
   hitting a rival pinned at 1 HP while rebuilding meter. This is what makes **C2's HUD gate
   indicator mandatory.**
2. **The two-hit-and-bail player** never finishes a string, earns no meter, and can reach a
   pinned rival with an empty bar. No tuning value closes this; it is handed to the HUD, the
   onboarding Impact Window, and the combo buffer.

---

## 04. Crimson Vanguard — authored rival AI

**Runtime AI boundary. LOCKED.** Crimson Vanguard is controlled by authored Unreal gameplay
AI — a compact state machine or Behavior Tree. **The packaged duel makes no runtime LLM
calls**, does not learn from the player, and does not generate attacks or choreography
dynamically.

### State flow — LOCKED shape, LOCKED ranges

`Idle / Reposition → Select Attack → Telegraph → Active Attack → Recover → Return to Neutral`

| State | Purpose | Phase 1 | Phase 2 |
|---|---|---|---|
| Idle / Reposition | Face the selected fighter and maintain armored pressure | 0.60–1.20 s | 0.35–0.80 s |
| Select Attack | Choose one of four authored attacks by range and cooldown | 0.10–0.20 s | 0.10–0.20 s |
| Telegraph | Show committed pose, warning lights, sound, and readable direction | 0.55–0.95 s | 0.40–0.75 s |
| Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s |
| Recover | Expose a deliberate punish opening after the committed strike | 0.45–0.90 s | 0.35–0.75 s |
| Return to Neutral | Clear attack flags and restore valid locomotion | 0.10–0.20 s | 0.10–0.20 s |

**The GDD publishes these ranges per state, not per attack.** Any chosen value must fall
inside its published range, and collapsing a range to a single number on an agent's own
authority is itself a violation.

### Four-attack course set — LOCKED

| Attack | Range / purpose | Readability requirement |
|---|---|---|
| **A** | Close-range committed gauntlet force | Distinct wind-up and punishable recovery |
| **B** | Committed forward-pressure sequence | Visible first beat and stable tracking limit |
| **C** | Armored reach and space control | Clear body direction and visible active range |
| **D** | Short propulsion-assisted approach | Thruster cue before movement; **no hidden full-arena snap** |

**Working names, and their exact status.** `Fault Line` (A), `Advance Line` (B),
`Bulwark Reach` (C), `Thruster Snap` (D) were generated by the Assignment #04 pipeline and
carried into `data/unreal/DT_VanguardAttacks.csv`. They are **proposed placeholder labels,
not canon.** Only the designer may promote them.

### Per-attack tuning — 26 values, all PROPOSED (Q25), all in range

**Range compliance: 26 / 26 in range. 0 out of range. 0 GDD ranges altered or collapsed.**
Independently recomputed and confirmed by the cross-consistency inspection.

| Attack | Telegraph P1 | Telegraph P2 | Active (both) | Recover P1 | Recover P2 |
|---|---|---|---|---|---|
| **A** | 0.70 | 0.55 | 0.22 | 0.85 | 0.68 |
| **B** | 0.60 | 0.48 | 0.36 | 0.70 | 0.56 |
| **C** | 0.80 | 0.62 | 0.30 | 0.60 | 0.48 |
| **D** | 0.90 | 0.70 | **0.45** | 0.55 | 0.44 |

Duel-level: Reposition **0.90 / 0.55**, Select Attack **0.15 / 0.15**, Return to Neutral
**0.15 / 0.15**. Telegraph tracks range (close = short); Recover tracks commitment
inversely — D is shortest because D exists to set up A.

| Parameter | Phase 1 | Phase 2 | Status |
|---|---|---|---|
| Engagement bands, centre-to-centre | A **0–260** · B **90–520** · C **240–420** · D **400–840** cm | identical | PROPOSED (Q10) |
| Attack cooldowns | A 3.0 · B 3.5 · C 3.6 · D 3.8 s | A 2.5 · B 2.6 · C 2.7 · D 2.8 s | PROPOSED (Q12) |
| Damage (% of player max HP) | A **32** · B **25** · C **27** · D **18** | identical | PROPOSED (Q3) |
| Attack D travel distance | **600 cm** = 0.25 × arena long axis, finishing 240 cm from the target | identical | PROPOSED (Q13) |
| Rival max health | **1200** (band 1100–1400) | — | PROPOSED (Q2) |
| Telegraph notify offset | **0.35 s**, as `MontageLength / EffectivePlayRate + 0.35` | — | PROPOSED (Q18) |
| Recover-window damage multiplier | **1.0 — no bonus** | — | PROPOSED (Q27) |
| Rival scale | **208 cm** (82 in × 2.54, rounded as Echo's 183 and Nova's 173 are) | — | **APPROVED** (item 28) |
| Rival `MaxWalkSpeed` | — | — | **OPEN — and serious. See §12, item 49** |

**Four findings the implementation must not miss:**

1. **`ActiveSeconds` must never gain a per-phase field.** Scaling D's 0.45 s by the ~0.78
   Phase 2 ratio makes 600 cm cross at **1714 cm/s** and breaks the GDD's own no-snap rule.
   It belongs on the row, outside both phase structs. **D's Active sits on the published
   maximum and has zero upward headroom** — the validator must therefore be `Min <= Value <= Max`.
2. **Attack B's first-to-last hit notify must span ≤ 0.26 s**, or the 0.28 s i-frame window
   cannot cover the sequence and **B becomes unavoidable**.
3. **Attack B's Data Table row is *total* attack damage, split across notifies.** If B is
   authored with multiple `ANS_ActiveHit` windows each reading `Damage = 25`, it deals
   50–75% of player health in one attack and the damage budget is void. This is the most
   likely way the table silently produces a broken fight.
4. **Attack A's Phase 1 cycle is 2.97 s against a 3.0 s cooldown — 0.03 s of slack.** At
   0–90 cm, where A is the only legal attack, that is A every ~3.0 s at 32 damage:
   **10.7 dmg/s against 100 HP.** It cannot be fixed from inside the per-attack timings;
   every legal choice lands the cycle in 2.8–3.2 s. **Q12, Q25 and Q3 need one joint tuning
   session.**

**Band coverage is proved, not assumed:** contiguous over [0, 840] cm with 80 cm and 120 cm
handoff overlaps, depth ≥ 2 across the whole 100–520 cm fight zone. The single zero-coverage
region (840–2884 cm) and the single depth-1 region (520–840 cm) are **both closed by a
required advance rule** rather than by accident — which is the reposition-loop deadlock the
design brief warned about, closed deliberately. Starvation checks pass in both phases at the
fastest legal cycle, tightest slack **+0.16 s**.

### Phase 2 escalation — LOCKED

Phase 2 begins when Crimson Vanguard reaches **50% health**. The phase change is committed
on **Return to Neutral**, then signaled once with stronger thruster output, warning lights,
sound, and armor-energy presentation. It uses **the same four authored attacks — no
transformation rig and no second move set.** Only pressure parameters and presentation
change.

---

## 05. Build state and technical milestones

*Validate the complete gameplay contract before expanding presentation.*

**Gray-box milestone. LOCKED.** The first vertical slice uses proxy Echo or Nova, proxy
Crimson Vanguard, the official arena footprint, one authored rival attack, one player
defensive response, one Impact Window, meter gain, and a clean return to neutral. It proves
the real-time-to-cinematic handoff before final characters, VFX, or expanded choreography.

### Milestones — LOCKED order, with today's honest state

| # | Milestone | Required proof | Gate | **State, 2026-08-17** |
|---|---|---|---|---|
| **M1** | Combat gray box | Movement, lock-on, light sequence, dodge, perfect dodge, counter, health | Playable loop with selected proxy | **~40% — partially BUILT** |
| **M2** | Rival state loop | All six AI states and one Crimson Vanguard attack complete without deadlock | Returns to Neutral every attempt | **~35% — reduced form BUILT** |
| **M3** | Impact handoff | Earned prompt, success/failure branches, restored control | No forced success or stranded cinematic state | **Not started (design complete)** |
| **M4** | Complete duel | Meter, Phase 2, Final Clash, failure recovery, win/loss | Start-to-finish course prototype | **Not started (design complete)** |
| **M5** | Presentation pass | Approved character treatment, arena reaction, camera, VFX, sound | **Only after M4 is stable** | **Correctly locked. Phase 2 work.** |

### What is actually in the Unreal project today — BUILT

The Unreal implementation lives in `ascendant-impact-ue` (UE 5.8, Blueprint-only). Every
item below has PIE evidence recorded in `docs/agent/PROTOTYPE_BLACKBOARD.md`, compiles
clean with `warnings_as_errors=true`, and logs zero Blueprint runtime errors.

| Built | Detail |
|---|---|
| **Playable duel graybox** | `Lvl_DuelGraybox` — flat contained arena, both fighters grounded, perimeter ramps outside combat bounds |
| **Duel camera rig** | `BP_DuelCameraRig` — fixed arena-side camera, constant yaw, mutual look-at facing with an interp guard; camera cannot flip when fighters swap sides |
| **Player movement + jump** | Screen-space input, `JumpZVelocity` 820 / `GravityScale` 1.9 / `AirControl` 0.35 — apex ≈180 cm rise, ≈0.9 s airtime |
| **Jump-over and dynamic side switching** | Player can cross over the Vanguard; side ownership computed from positions with a deadzone, mutual move-ignore during the crossing, symmetric restore, no state leak on knockout |
| **Player attack → damage** | LMB punch, facing-driven overlap, 10 damage per hit, one event per swing |
| **Vanguard movement AI** | `BP_VanguardDuelMover` — advance / hold / retreat against a spacing band, in-lane depth wander, arena clamp, side-aware constraint solver |
| **One telegraphed Vanguard strike** | `BP_VanguardBasicAttackDriver` — 1.1 s wind-up, "!" telegraph, cooldowns 2.5–4.0 s, decision chance 0.65, **interruptible any time before the impact check**, 55 cm depth-dodge tolerance |
| **Duel HUD** | `UI_DuelHUD` — mirrored player/Vanguard health bars driven by authoritative health, 0.05 s timer update, interpolated settle |
| **Knockout** | Health floor at 0, ragdoll, one-shot, attacks blocked after KO, full state reset on PIE restart — both fighters |
| **Camera shake** | Separate player-hit and enemy-hit shakes, tuned restrained (no roll on player hits) |

### What is NOT in the build yet

**Player kit:** the light-combo montage and its sections, the dodge, the perfect-dodge
window, the counter, and lock-on. The current punch is a single overlap, not the 3-section
combo. **Rival:** the six named states as an explicit machine, attack selection by range
band, attacks A–D as data rows, Phase 2. **Systems:** the Ascension Meter, the HUD gate
indicator (C2), Impact Windows and the whole real-time-to-cinematic handoff, the Final
Clash and its two beats, failed-Clash recovery, win and loss end states, character
selection.

### Two divergences that must be reconciled before M2 signs off

These are real and are named here rather than discovered in September.

1. **The design architecture and the built architecture use different names and a different
   AI shape.** The design line (`build-sequence.md`, `combat-integration-plan.md`) targets
   `BP_CrimsonVanguard` driven by a Behavior Tree with six `BTTask_*` nodes reading
   `DT_VanguardAttacks`. The built line has `BP_VanguardProxy` +
   `BP_VanguardBasicAttackDriver` + `BP_VanguardDuelMover` — a timer-driven driver that
   already implements **Telegraph → Active → Recover → cooldown** and a mover that covers
   **Idle / Reposition**, with **Select Attack** absent because there is only one attack.
   **Recommendation, and it is the designer's call: keep the built driver and complete it
   into the six states rather than rebuilding on a Behavior Tree.** The state contract is
   what the GDD locks; the node graph that satisfies it is not. Rebuilding costs days the
   calendar does not have.
2. **Rival health is hardcoded to 100 in the proxy** (the HUD divides by 100 to match),
   against a proposed 1200. Nothing is broken by this today — it is a graybox default — but
   it must be replaced by `DA_TuningGlobals` before any damage tuning means anything.
3. **The arena footprint does not match the proposed one.** The built combat axis is
   ±650 cm; Q24 proposes 2400 × 1600 cm. Attack D's 600 cm travel and the Final Clash's
   1200 cm separation both assume the larger floor, so the arena has to grow before either
   can be authored honestly. Camera framing is coupled to those bounds — the rig's
   `DistancePerSeparation` and `MaxCameraDistance` must be retuned in the same pass.
4. **The attack DataTable route is PAUSED in the engine project**, pending a human unpause.
   `S_VanguardAttackDef` / `DT_VanguardAttacks` cannot be created through the MCP at all —
   user-defined structs are a manual editor step. **M2 cannot start until that pause is
   lifted and the struct is made by hand.** When it resumes, the row data imports verbatim
   from the approved CSV, and nothing marked OPEN in the source audit may be invented.

### Implementation safeguards — LOCKED

- Use authored state-machine or Behavior Tree logic with **visible debug state names** and
  deterministic recovery paths.
- **Separate gameplay timing from cinematic presentation** so hit-stop, camera, and VFX can
  be disabled during diagnosis.
- **Restore input, collision, locomotion, lock-on, and AI state explicitly** after every
  Impact Window and Final Clash branch.
- Validate both selectable avatars against the same collision, targeting, reach, and
  arena-boundary tests.
- **Treat all timing ranges, meter values, and health thresholds as provisional** until
  validated through playtesting and finalized by the designer.

### The cinematic restore contract — APPROVED (V1–V5), not yet applied

Five corrections to the cinematic handoff were approved as engineering on 2026-08-02. They
clear the one hard check the cinematic inspection failed, and **M3 does not sign off until
they are applied.**

| V | Correction |
|---|---|
| **V1** | `bInImpactBurst` as a second park key alongside `bInClash`, released only in `RestoreCombatState()`. **Nothing is suspended while a window is merely open** — combat continues under the prompt. The park flag is mandatory, not a preference: a burst can begin mid-Telegraph. |
| **V2** | `Set View Target with Blend` back to the possessed player as an **unconditional** restore step, called directly on the PlayerController, never through the presentation subsystem. |
| **V3** | All hit-window state moved off the notify object onto the combat components behind a `BPI_CombatWindows` interface, keyed by a monotonic `WindowID`; **orphan-scoped** force-close from restore and from tick. Retires the notify-end dependency entirely — `Received Notify End` is documented as unreliable under montage interruption. |
| **V4** | Per-branch montage-cleanup ledger; a single terminal `bDuelOver` rule resolves `OnDeath` during any overlay. |
| **V5** | Blind tag clear replaced with `ResyncTransientTags()` over a closed seven-tag set, reading V3's window registry. |

**A latent bug these corrections prevent, worth keeping in the document:** restore also runs
on the Impact **failure** branch, where nothing was suspended — so a blind clear of
`State.Invulnerable` / `State.PerfectWindow` **strips a player's i-frames mid-dodge** if a
window expires during that dodge. Adding `State.Dodging` to the blind clear list would have
widened the bug rather than fixing it.

---

## 06. AI-assisted development architecture

**Human approval gate. LOCKED.** Generative tools may support ideation, reference
exploration, documentation, and offline draft assets. **No generated combat behavior,
character asset, animation, VFX, sound, or text enters the build without human review,
technical validation, rights review, and explicit approval.**

| Area | Allowed support | Course-build boundary |
|---|---|---|
| Design | Brainstorming, comparison, tuning hypotheses, documentation drafts | **Designer approves all rules and numbers** |
| Visual development | Reference exploration and look-direction drafts | Human-selected assets only; no automatic final import |
| Code support | Offline implementation suggestions and debugging assistance | Reviewed source and authored Unreal runtime logic |
| **Runtime opponent** | **None** | Crimson Vanguard uses deterministic authored AI; **no runtime LLM** |
| Playable fighters | **None at runtime** | Player input controls Echo or Nova; no agent automation |

### What was actually built under this architecture

All of it is **offline authoring tooling that lives outside the game's scope lock.** None of
it ships in the packaged build, and none of it makes a runtime call.

| Tool | What it does | State |
|---|---|---|
| **The agent crew** (6 agents) | designer → developer → inspector, plus framework evaluator, combat-integration architect, cinematic-integration inspector. Hook-gated in Python: an agent cannot spawn until its upstream leave-off says `status: complete` | Ran to completion; six artifacts on disk |
| **The goal planner** | Diffs what the GDD says the game is against what `design/` records as decided, ranks the remainder by the lowest build step each item blocks, **and stops when the top item is a design question** | Built; `design/goal-plan.md` |
| **The content pipeline** (#04) | RAG over a knowledge base that *is* the extracted GDD; a critic agent enforcing seven consistency rules. Produced telegraph packs, Impact Window beat packs, arena reaction packs, animation briefs, VFX/audio cue sheets, QA edge-case packs | 175 tests pass |
| **The arena pipeline** (#05) | Generate → deterministic validate (rules R1–R8) → evaluate against four weighted criteria → refine one field at a time → three-attempt circuit breaker → Unreal materializer. **Refuses and exits rather than inventing a missing requirement** | 77 tests pass; three example runs committed |
| **The GER pipeline** (#06) | Generates the seventeen-column `DT_VanguardAttacks` rows, gated so a fifth attack, a new Phase 2 move, or an invented value for an OPEN field cannot pass | Committed with evidence |
| **The style-guide agent** (#07) | Governs player-facing combat copy — Impact prompts, meter feedback, the Phase 2 callout, the Clash unlock, the failed-Clash recovery line, the loss screen — scored, refined, and graded by a real model | 139 tests pass, 2 skipped |

**The rule that makes this safe is enforced, not promised.** Every generated value carries a
source and a status (`MEASURED` / `APPROVED` / `DERIVED` / `PROPOSED`); pipelines exit with
a request for human review rather than filling a blank. A value left **OPEN is a pass**, not
a gap to fill.

**A drafting rule that came out of #07 and belongs in the GDD:** player-facing copy prints
**no numbers**, because every meter value is provisional. The Final Clash unlock banner
therefore announces readiness rather than teaching the gate, and **must never present a full
meter alone as the unlock.**

**Optional coursework still available (#08 narrative engine, #09 adversarial QA agent)** is
tooling, not game scope. Neither is on the critical path to 1 September, and neither may add
a game feature.

---

## 07. Character readability, scale, and opening flow

*Three distinct combat identities remain legible inside one shared design family.* **LOCKED.**

| Category | Agent Echo | Agent Nova | Crimson Vanguard |
|---|---|---|---|
| Combat identity | Precision and controlled timing | Speed and aggressive momentum | Armor, pressure, overwhelming force |
| Movement | Deliberate spacing and counters | Fast lateral rhythm and forward intent | Committed advances and short propulsion |
| Silhouette | Lean, upright technical striker | Compact, agile layered profile | Substantially broader armored mass |
| Material family | Matte black and charcoal technical suit | Black, charcoal, orange, light-gray helmet cap | Red armor over black structure |
| Energy / VFX | Controlled orange accents | Cyan-white combat energy or selected telegraphs | Red-orange systems and warning lights |
| Gameplay role | Selectable player avatar | Selectable player avatar | Sole authored AI rival / boss |
| Readability target | Exact timing and clear counter intent | Momentum without visual noise | Threatening reach with obvious tells and recovery |

**Color direction. LOCKED.** Echo keeps restrained orange accents. Nova's existing black,
charcoal, orange, and light-gray costume is preserved; cyan-white is reserved for combat
energy, telegraphs, or selected VFX accents when separation is needed.

**Character scale. LOCKED, with the rival's value now APPROVED.** Nova 5'8" / 173 cm, Echo
6'0" / 183 cm, Crimson Vanguard 6'10" / **208 cm** (approved as item 28; uniform scale only,
capsule scales with the mesh). The rival is deliberately taller and substantially broader
while remaining within a scale that supports readable close-range combat. **The height
difference must not create unfair hidden reach or collision behavior**, and reach is
re-validated after any scale change. **Rival width remains unspecified — do not derive a
capsule radius from "roughly twice the shoulder width."**

### Proxy cast for Phase 1

| Role | Proxy | Status |
|---|---|---|
| Agent Echo | **Manny** (UE mannequin) | BUILT |
| Agent Nova | **Quinn** | Deferred until Echo proves the shared pipeline |
| Crimson Vanguard | Scaled mannequin at 1.1 stature today; **Paragon: Crunch** recommended (alternate: Paragon: Steel) | **PROPOSED (Q30) — and its own decide-by date of 2026-08-09 has passed. See §12.** |
| Shattered Ring | Gray-box floor, walls, one doorway axis | Partially BUILT |

**Why Crunch, if it is taken:** it wins on the two reference-sheet lines that matter for
readability — a **fully enclosed fist with no weapon** ("the hand *is* the weapon") and
**mech proportion with a small head**. Steel loses on the shield. Building the rival on
Crunch's own skeleton with Crunch's own animation cycles removes the IK-retargeting pass
from the critical path entirely: ≈1.0 day cost, offset by ≈0.5–1.0 day returned on attack
animation sourcing. **Swapping after the attack rows are authored costs 2.0–3.0 days and is
forbidden.**

### Presentation decisions — PROPOSED, all placed in M5

| Item | Decision | Status |
|---|---|---|
| Echo's faceplate | **Visor AND light** — dark visor plane plus one small indicator in the helmet position Nova's already occupies. **No gameplay-state modulation.** Under reverse third-person framing the face is off-camera for the entire duel, so it is not a viable readability channel and must not be made one | PROPOSED (item 43) |
| Energy lines | Emissive and Ascension-responsive for both fighters — one `Ascension01` scalar on the shared master material, per-fighter masks, **stepped at 50 and 100**, intensity only, no hue change. **Never the only channel; the HUD stays authoritative** | PROPOSED (item 44) |
| Fighter unit line ("SFN") | **Cannot be established and is not established.** Ship the badge as art; expose `FighterUnitLine` **blank** | PROPOSED (item 45) |
| Rival in-combat UI label | Recommend **`VALOR-7`**; **ship the field blank** until approved. `CRIMSON VANGUARD` is 16 characters against a 16-character nameplate budget with zero localization headroom | PROPOSED (Q29) |

**A readability tension that is mitigated, not removed:** Echo's orange sits next to the
rival's red-orange warning lights. The mitigating rule — **the rival owns animated emissive,
the player owns static or stepped** — makes the risk testable rather than gone.

### Character selection and opening flow — LOCKED concept, simplified build

Echo and Nova appear in a clean editorial character-selection interface; the player briefly
moves between both options; technical and equipment panels animate around the selected
fighter; the interface transitions into the established arena; the camera moves behind the
selected fighter; Crimson Vanguard enters through the far doorway; the duel begins.

**Course-build allowance. LOCKED.** The build may use a **simplified selection screen and an
abbreviated arena entrance** while preserving the same readable sequence. **This allowance is
load-bearing for 1 September** — see §10.

**Concept video:** link still pending. The document stands alone without it.

---

## 08. Visual assets and the official Version 1 arena

**The established industrial Shattered Ring arena is locked as the official Version 1
environment. LOCKED.** Alternate environment explorations do not replace it.

| Arena requirement | Version 1 function |
|---|---|
| Central combat floor | Open, readable space for spacing, lock-on, dodges, counters, and Final Clash staging |
| Far doorway | Dedicated Crimson Vanguard entrance axis |
| Reverse third-person framing | Clear camera position behind the selected fighter |
| Side-on readability | Readable silhouettes and attack direction during lateral exchanges |
| Environmental reaction | Visible but controlled reaction during major impacts, **without adding gameplay hazards** |

### Arena footprint — PROPOSED

| Parameter | Recommended | Status |
|---|---|---|
| Playable floor | **2400 × 1600 cm** (24 × 16 m), long axis = doorway axis, four 250 cm 45° chamfers | PROPOSED (Q24) |
| Stored as | `ArenaLongAxisCm` / `ArenaShortAxisCm` in `DA_TuningGlobals`, so Attack D's travel cannot drift from the floor it assumes | PROPOSED |
| Diagonal | ≈2884 cm — beyond both lock-on distances, so lock never breaks by distance in this arena | derived |
| Mezzanine | **Set dressing** — no NavMesh, no blocking volume, railings `NoCollision`, underside ignores the `Camera` channel | PROPOSED (item 18) |

The five supplied reference sheets — character scale, the established arena, Echo, Nova, and
the Crimson Vanguard technical board — are recovered and described in `gdd/reference/`.
**Authored GDD text outranks any image description, and nothing marked AMBIGUOUS in those
descriptions may be guessed at.**

### Asset sourcing and rights — the Phase 1 position

**Assets cost $0**, must be licensed for a submitted course build, and still pass human
approval and rights review. Where no free asset exists, the gap is named and a free fallback
proposed — never a purchase assumed.

- **Branding exposure is zero — APPROVED (item 20).** The swoosh appears only on the GDD's
  concept sheets, on no asset in the build or the plan. Manny and Quinn carry no branding.
  Remedy is a five-minute recorded verification when the proxies are dressed, plus a
  one-sentence constraint on final art that does not exist yet.
- **Audio: Phase 1 ships without an audio pass, and that is said here rather than
  discovered. PROPOSED (Q31).** No M1–M4 gate names audio; only M5's does. **But not
  literally silent** — a capped **6–9 one-shot cue floor at ≈0.5 day**, sequenced *after*
  M4's gate, routed through the presentation subsystem so it stays disable-able. Source:
  **Freesound filtered to CC0** (the filter is mandatory — every other licence there carries
  an attribution obligation).
- **This has an honest cost.** The GDD names sound as a Telegraph and Phase 2 channel.
  Shipping the pass in M5 means that channel is absent in Phase 1, so **pose, warning lights,
  and emissive carry the whole readability load** — which is exactly why the capped cue floor
  exists at all.
- **Gaps with no free source:** the rival's back-vane/thruster silhouette (omit in Phase 1 —
  telegraph pose plus emissive carries Attack D's cue; geometry is M5), a martial-arts strike
  set with the intended weight, character art matching the sheets, and a UI icon set (text
  and plain bars suffice).

---

## 09. Scope lock, the release cut line, and future expansion

**Scope lock — LOCKED, unchanged from v0.4.** The required prototype is complete when the
player can select Echo or Nova, enter the official arena, fight Crimson Vanguard through
both phases, earn and resolve Impact Windows, reach and retry the Final Clash, and finish
with a valid win or loss.

### Included in the course prototype — LOCKED

- One player versus one authored AI opponent.
- Two selectable player avatars using one shared core combat framework.
- One Crimson Vanguard boss with six states, four attacks, and a parameter-based Phase 2.
- One official industrial arena, one complete duel, and complete win/loss handling.
- Impact Window onboarding, Ascension Meter, Final Clash unlock, and failed-Clash recovery.
- Human approval gates and no runtime LLM-controlled fighters.

### Deferred future scope — LOCKED

Local or online PvP · unique Echo and Nova move sets, separate balance systems, or extensive
character cinematics · a playable Crimson Vanguard combat kit · multi-enemy encounters,
campaign progression, additional arenas, or extended enemy gauntlets · transformations,
second boss kits, additional characters, modes, weapons, or story chapters.

### The release cut line — NEW in v1.0, and a designer decision

Fifteen days remain. The scope lock above is what the prototype *is*; the list below is the
order in which parts of it get sacrificed if the calendar wins. **This ordering is a
recommendation and needs approval** — the first two entries cut items the scope lock names,
which makes them the designer's call and nobody else's.

| Order | Cut candidate | What is lost | What survives |
|---|---|---|---|
| 1 | **Attacks C and D** | Two of the four authored attacks | Attacks A and B cover 0–520 cm; the band coverage proof holds without C and D only if the advance rule is retuned |
| 2 | **Nova as a second selectable avatar** | Half of "two selectable avatars" | The selection screen still shows both; Echo is the playable one. This is the largest single day saving and the largest scope-lock concession |
| 3 | Attack D's propulsion travel | The gap-close identity | D authored as a short committed advance instead |
| 4 | The audio cue floor | Six to nine one-shots | Already planned as post-M4; cut costs nothing already promised for Phase 1 |
| 5 | Arena dressing beyond graybox | Visual identity | Gray-box floor, walls, and the doorway axis |
| 6 | Per-fighter timing flavor | Presentation-level identity | Identical values for both fighters — which is already the recommendation |

**Nothing on this list touches the Final Clash, the meter, the double gate, the first Impact
Window, or the win/loss outcomes.** Those five are what makes the duel a duel; if they will
not fit, the answer is to cut attacks and avatars, not the loop.

### Definition of done — LOCKED

| Area | Acceptance condition |
|---|---|
| Combat | Real-time controls remain responsive before and after every cinematic beat |
| Selection | Either avatar enters the same complete shared-framework duel |
| AI | Crimson Vanguard completes all six states and never strands the encounter |
| Phase 2 | 50% health escalation changes pressure parameters and presentation, **not the attack set** |
| Climax | Final Clash obeys **both** unlock conditions and supports recovery after failure |
| Readability | Echo, Nova, and Crimson Vanguard remain legible in motion and at combat distance |
| Scope | One complete duel runs start to finish in Unreal Engine 5.8 on PC |

---

## 10. Release plan to 1 September 2026

**Two phases, one hard date.**

| Phase | Window | Deliverable |
|---|---|---|
| **Phase 1 — the playable duel** | now → **1 Sept 2026** | A duel that can be **fought start to finish**, with *some* design on it — not a bare gray-box tech demo. **M1 → M4, then a thin presentation floor.** |
| **Phase 2 — polish** | after Phase 1 is playable | As polished as possible — graphics, VFX, camera, sound, arena reaction. **Full M5.** |

**How Phase 1 gets a look without breaking milestone order.** M5 stays gated behind a stable
M4. Phase 1 earns its visual identity by **dressing the proxies**: M1–M4 may stand up free
third-party meshes, animations, and set dressing from the start (Unreal template content,
the Fab free tier, free Quixel grants, Mixamo). **Picking a proxy asset is asset selection,
not a presentation pass.** What stays M5 is the *tuned* work — hit-stop feel, camera
choreography, VFX authoring, sound design, arena impact reaction, final character treatment.

### The critical path is approvals, not code

> **The largest single risk to shipping is not engineering. It is that ~35 researched values
> are still unapproved, and the build cannot legitimately consume any of them.** A developer
> may create the exposed variable and leave it blank; it cannot be signed off. Every day the
> approval batch waits, a day of tuning is lost at the far end, where there is no slack.

**Approve in this order** — each batch unblocks the milestone beneath it:

| Batch | Items | Unblocks |
|---|---|---|
| **1 — today** | Q1, Q4, Q5, Q28, Q6, **Q7 (BLOCKING)**, Q8, Q14, Q15, Q16, Q11 | M1 sign-off — the whole player kit |
| **2 — within 3 days** | Q2 (and **item 64 / C3** with it), Q3, Q10, Q12, Q13, Q25, Q18, Q27, **Q30 (overdue)**, Q24 | M2 — the rival, its data table, and the arena it fights in |
| **3 — within 7 days** | Q9, Q26, Q29, C2's HUD gate indicator | M3 — meter, HUD, Impact Windows |
| **4 — within 10 days** | Q17, Q19, Q20, Q21, Q23 | M4 — the Final Clash |
| **Anytime** | items 43, 44, 45, Q31 | M5 — Phase 2, after the ship date |

### The fifteen days

| Window | Target | Gate to clear |
|---|---|---|
| **Aug 17–21** (D-15 → D-11) | **Finish M1.** Light combo (3 sections + finisher), dodge with i-frames, perfect-dodge window, counter and whiff lockout, lock-on. Replace the hardcoded 100 HP with `DA_TuningGlobals`. Grow the arena to the approved footprint | Playable loop with the selected proxy — combo, dodge, perfect dodge, counter, health all live |
| **Aug 22–25** (D-10 → D-7) | **Finish M2.** Complete the existing attack driver into the six named states with visible debug names; add Select Attack by range band; author Attack A from its data row; **Attack B if and only if A's full loop passes**; wire the Phase 2 parameter swap on Return to Neutral | Six states cycle without deadlock; returns to Neutral every attempt |
| **Aug 26–28** (D-6 → D-4) | **Finish M3.** Ascension Meter component; HUD meter bar **and the C2 gate indicator**; the first (0.75 s) and standard Impact Windows; **apply V1–V5** — the restore contract is the sign-off condition, not a follow-up | Earned prompt, success **and** failure branches, control restored, no stranded cinematic state |
| **Aug 29–30** (D-3 → D-2) | **Finish M4.** The double gate; the two Clash beats; success → win screen; failure → the seven-step recovery (separate, 1 HP floor, meter 50, 3 s cooldown); loss when player health reaches zero; the simplified selection screen | **A duel that can be fought start to finish, won, and lost** |
| **Aug 31** (D-1) | **Freeze.** No new systems. Thin presentation floor only: hit-stop on the combo finisher, the existing camera shakes, telegraph emissive. Package, run the acceptance pass in §09, write the submission notes | Build on disk, runs from a cold launch |
| **Sept 1** | **Ship Phase 1** | — |
| **Sept 2 →** | **Phase 2 / M5.** Audio cue floor, character treatment, arena reaction, VFX authoring, camera choreography, the editorial selection screen | — |

**The schedule assumes the cut line in §09 is available.** If M1 is not finished by Aug 21 or
M2 by Aug 25, take cut 1 (Attacks C and D) immediately rather than compressing M3 and M4 —
those two contain everything that makes the duel readable as a *duel*, and they have the
least slack.

**Four housekeeping items with real risk attached:**

1. **The Unreal work sits on feature branches, not on `main`.** Fifteen commits of duel work
   live on `feature/agent-arena-pipeline` and its ancestors while `main` carries only the
   production baseline. Merge deliberately and early — not on August 31.
2. **The project's default map is still `Lvl_ThirdPerson`, not `Lvl_DuelGraybox`.** A
   package built today launches into the wrong level. One setting, two minutes, and it must
   not be discovered by a grader.
3. **The attack DataTable pause must be lifted this week**, and the user-defined struct
   created by hand in the editor, or M2 has nothing to read (§05).
4. **Two approvals are open and are the designer's alone:** the countersignature on
   `docs/unreal/VANGUARD_ATTACK_DATA_APPROVAL.md` (signed by Anthony Travieso on 2026-07-29
   for his branch, not countersigned here), and item 26's four canon questions about the
   Crimson Vanguard reference sheet. Neither blocks M1 or M2's Attack A.

**When the calendar and the wish list disagree, a complete fought duel on 1 September beats a
beautiful incomplete one.**

---

## 11. Revision log — v0.4 → v1.0

| Section | Change in v1.0 | Type |
|---|---|---|
| 00 | Status key added; every value in the document now carries LOCKED / APPROVED / PROPOSED / OPEN / BUILT | **New** |
| 01 | High concept, pillars, motivation, and scope lock carried forward verbatim; a paragraph added on what exists in the world since v0.4 | Preserved + extended |
| 02 | Player combat kit tuning table added (11 rows, all PROPOSED); Impact Window cooldown added; three structural implementation rules recorded | Extended |
| 03 | **Q22 recorded as APPROVED** — the 1 HP floor is permanent and the Final Clash is the only win condition, with constraints C1/C2/C3; Clash execution layer added; the meter re-characterized as an anti-passivity floor rather than a race | **Revised — first approved decision since v0.4** |
| 04 | 26 per-attack timing values added (in range, PROPOSED); bands, cooldowns, damage, travel added; rival scale **208 cm APPROVED**; four implementation findings recorded; **rival walk speed named OPEN** | Extended |
| 05 | Rewritten. Milestone table now carries real state; what is built and what is not; **three architecture divergences named**; the V1–V5 restore contract recorded as approved and unapplied | **Rewritten** |
| 06 | Rewritten around the tooling that actually exists — crew, goal planner, and four pipelines — with the no-runtime-LLM boundary reaffirmed and the no-numbers copy rule added | **Rewritten** |
| 07 | Scale value approved; proxy cast table added with the rival proxy recommendation **and its missed decision date**; four presentation decisions recorded as PROPOSED and placed in M5 | Extended |
| 08 | Arena footprint added (PROPOSED); mezzanine ruled set dressing; asset sourcing, rights, and the **audio-in-M5 position** stated explicitly with its readability cost | Extended |
| 09 | Scope lock and definition of done preserved verbatim; **release cut line added** as a new ordered list requiring approval | Preserved + **new** |
| 10 | **New section.** Two-phase release plan, approval batches on the critical path, and the fifteen-day schedule | **New** |
| 11–12 | **New sections.** This log, and the open decision register | **New** |

**Nothing in v0.4 was reversed, and nothing in this document supersedes a GDD line.** Every
value added either fills a blank v0.4 deliberately left open or is drawn from inside a range
v0.4 published. The one approved decision, Q22, interprets the scope of a floor the GDD
already states.

---

## 12. Open decision register — what must be signed before release

**35 items are PROPOSED and awaiting the designer. 1 is blocked on a human. The rest are
untouched.** Full detail lives in `TODO.md` and the nine `design/group-0*.md` dispatch files;
this is the register of what actually gates the ship date.

### Blocking or overdue

| Item | Question | Why it is here |
|---|---|---|
| **Q7 · BLOCKING** | Perfect-dodge window — 0.12 s recommended | Marked BLOCKING because it changes *what the game is*, not how it is tuned. Its repeatability is unverified: the reachability check proves the pocket's onset is reachable at ~250 ms human reaction time, not that a human can hit 0.12 s repeatably. **Playtest protocol: start at 0.15 s and tighten, never the reverse.** |
| **Q30 · OVERDUE** | Rival proxy — Paragon: Crunch | Its own recommendation set a decide-by date of **2026-08-09, which has passed.** The import must land **before the attack montages are authored**; swapping afterward costs 2.0–3.0 days and is forbidden. This is the single most time-sensitive open item. |
| **item 64 / C3** | ≤25% rival health and meter 100 do not arrive close together — meter 100 lands at ~0:40–1:25, the health gate at ~2:53 | C3 came from the one decision carrying recorded designer approval, and a dispatch may not amend an approved constraint's success criterion. **Two paths, both on the table:** accept meter-first ordering as C3's real intent and amend C3 explicitly on the record, **or** take Q2 → 1050–1100, which independently also fixes the scrappy-player ~5:24 overshoot past the 3–5 minute target. |
| **item 49** | Crimson Vanguard's `MaxWalkSpeed` is unspecified | Under the approved Q22, **a rival slower than the player can be kited forever and the duel cannot end.** Bounds exist from two directions — lower from the spacing work, upper ≈1030 uu/s from the Clash work — but the value must be set, and the Clash separation cannot be validated until it is. |
| **item 63** | V1–V5 have not been applied to the integration plan | **M3 does not sign off until they are.** M1 and M2 proceed regardless. |
| **item 26** | Four canon questions about the Crimson Vanguard reference sheet | Correctly unresolved — the transcription disclaims itself, and a low-confidence image description may not settle canon. **Blocked on a human zooming page 14.** Attack A is not blocked either way: authored §04 text outranks an image description, and a reference sheet cannot add a mechanic. |

### Approve to unblock each milestone

| Milestone | Items awaiting approval |
|---|---|
| **M1** | Q1 · Q4 · Q5 · Q28 · Q6 · **Q7** · Q8 · Q14 · Q15 · Q16 · Q11 |
| **M2** | Q2 · Q3 · Q10 · Q12 · Q13 · Q25 · Q18 · Q27 · Q24 · **Q30** · item 18 |
| **M3** | Q9 · Q26 · Q29 · item 63 (apply V1–V5) · C2's HUD gate indicator |
| **M4** | Q17 · Q19 · Q20 · Q21 · Q23 |
| **M5 / Phase 2** | Q31 · items 43, 44, 45 |

### Known-weak answers — flagged so approval is informed, not blind

| Item | Weakness |
|---|---|
| **Q8** (0.55 s whiff lockout) | No prior art exists for whiffed-parry recovery frames in any shipped game. Derived purely from the GDD's own ranges. **The weakest number in the player kit.** |
| **Q12** (attack cooldowns) | No shipped game publishes AI attack cooldowns. Derived entirely from the GDD's own state ranges. |
| **Q19** (Clash beat-1 lead) | The weakest-sourced answer in the Final Clash group — no shipped game publishes a numeric QTE window. |
| **Q25 / Q12 interaction** | Attack A's Phase 1 cycle sits 0.03 s inside its cooldown, producing 10.7 dmg/s at close range. **Needs one joint tuning session, not two separate approvals.** |
| **Q7** | Motor-timing repeatability unverified — out of research budget. |

**Three consecutive research groups reported the same finding: no shipped game publishes
per-attack boss telegraph durations, recovery durations, AI cooldowns, numeric QTE windows,
or knockback distances in world units.** Where a number here has no prior art, it says so
rather than citing something that does not exist. **These are playtest starting points, not
settled values** — which is exactly what v0.4 said they would be.

---

## Appendix A — Provisional design decisions for playtesting

Carried forward from v0.4 and still correct.

| Decision | v1.0 position |
|---|---|
| Exact combat timing and meter tuning | Keep all published timing ranges, gains, and thresholds provisional until playtest review |
| Echo / Nova timing flavor | Same mechanics and balance framework; presentation-level flavor only at first — and the recommendation is now **identical values for both** |
| Nova cyan-white application | Combat energy, telegraphs, or selected VFX — not a costume recolor — unless readability testing supports more |
| Signature cinematic variation | Deferred; consider one per fighter only after the shared base duel is stable |
| Selection and entrance fidelity | **Simplified selection screen and abbreviated arena entrance for the course build.** Load-bearing for the ship date |
| Crimson Vanguard display name | "Crimson Vanguard / Project Valor-7" formally; the shorter in-combat UI label is still open (Q29) |
| Scale, reach, and collision validation | Validate gameplay collision and hit reach only after both avatars pass the same close-range tests |
| Updated concept visualization | Link remains pending; the document stands alone without it |

---

## Appendix B — Document authority and change control

1. **The PDF is the source of truth.** Until this draft is approved and re-issued,
   `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` (v0.4) outranks this document
   and every other document in the repository.
2. **`gdd/` is generated and is never hand-edited.** To change what `gdd/` says, change the
   PDF and re-export with `pypdf` — sections, page images, and the reference-sheet
   descriptions together.
3. **Approving this draft is a real act.** It promotes every **APPROVED** row to canon,
   converts each **PROPOSED** row the designer signs into an approved value with a dated
   entry in `design/decisions.md`, and deletes the corresponding `TODO.md` item. Rows left
   PROPOSED stay PROPOSED — approving the document does **not** approve them by inclusion.
4. **No agent may promote a value, resolve a provisional number, or fill an OPEN field on
   its own authority.** It surfaces the question instead. A value left OPEN is a pass.

**Central promise — LOCKED.** *Real-time martial-arts combat rewards player skill with brief,
earned anime-style cinematic spectacle.*
