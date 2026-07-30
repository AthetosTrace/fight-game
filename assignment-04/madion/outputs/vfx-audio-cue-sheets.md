QUERY: For every gameplay event in Ascendant Impact that must be communicated to the player — each Vanguard telegraph, perfect dodge, Impact Window success and failure, Phase 2 escalation, and Final Clash success and failure — what cue fires, where does it play, when must it start and stop, what is it for, how does it change in Phase 2, how is it cleaned up after interruption, and how does it stay readable for a player who cannot rely on color or on sound?
SOURCES READ: gdd/ascendant-impact-gdd-v0.4.md, combat-integration-plan.md, build-sequence.md, cinematic-integration-inspection.md, assignment-04/shared/knowledge-base/core-canon.md
RETRIEVED TEXT:

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("State flow and provisional timing") ---
"Telegraph | Show committed pose, warning lights, sound, and readable direction | 0.55–0.95 s | 0.40–0.75 s | Telegraph completes"
"Active Attack | Apply authored movement, gauntlet force, hitbox, reach, or short propulsion | 0.18–0.45 s | 0.18–0.45 s | Active frames end"
"Recover | Expose a deliberate punish opening after the committed strike | 0.45–0.90 s | 0.35–0.75 s | Recovery completes"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Behavioral intent") ---
"Armor and scale may intensify presentation, but they do not remove readable counterplay."

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 5 ("Four-attack course set") ---
"Authored attack A | Close-range committed gauntlet force | Distinct wind-up and punishable recovery"
"Authored attack B | Committed forward-pressure sequence | Visible first beat and stable tracking limit"
"Authored attack C | Armored reach and space control | Clear body direction and visible active range"
"Authored attack D | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3 ("Impact Windows") ---
"A qualifying real-time event—such as a perfect dodge, counter, or approved combo milestone—can open one short contextual timing prompt. Success extends the exchange into a 1–3 second choreographed burst. Failure does not auto-correct the input; the game returns immediately to normal combat."
"First Impact Window | First successful perfect dodge or counter | 0.75 seconds | No cinematic extension; return to combat with no extra punishment"
"Standard Impact Window | Approved skill event after cooldown | 0.35–0.50 seconds | No extension; return to combat"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3 ("Ascension Meter") ---
"Perfect dodge +12 | Successful counter +15 | Impact Window success +20 | Taking damage / waiting +0"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 4 ("Encounter flow") ---
"Phase 2 | Begins at 50% Crimson Vanguard health; same attacks, stronger pressure | Apply learned reads under stress"
"Climax | Meter 100 + Crimson Vanguard health ≤25% | Player chooses the Final Clash attempt"

--- from `gdd/ascendant-impact-gdd-v0.4.md`, Page 3–4 ("Final Clash resolution") ---
"Failure | Separate both fighters; preserve current health with Crimson Vanguard held at a 1 HP floor; reduce meter to 50; apply a 3-second re-trigger cooldown. | Return to Neutral; rebuild meter and try again"
"PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player automatically, or leave either fighter in a cinematic state."

--- from `combat-integration-plan.md` §2 principle 5 ("Presentation is severable") ---
"All hit-stop, camera shake, VFX, sound, and time dilation route through `BP_PresentationSubsystem` wrappers that early-return when `bPresentationEnabled` is false. Gameplay timing is driven by montage playback and `Set Timer by Event`, never through a presentation call, so disabling presentation cannot change a frame window. The subsystem is wired (empty) in M1 so all M5 work lands without touching gameplay code. M5 remains last."

--- from `combat-integration-plan.md` §3.1 row 26 ---
"`BP_PresentationSubsystem`: `bPresentationEnabled` + the ONLY legal wrappers (`RequestHitStop`, `RequestCameraShake`, `RequestVFX`, `RequestSound`, `RequestTimeDilation`), each early-returning when disabled; hard rule: the five raw engine calls appear in exactly this one asset; wired empty in M1, filled only in M5"

--- from `build-sequence.md` M2-13 (`ANS_Telegraph` behaviour) ---
"Begin: `Set Blackboard CurrentState = Telegraph`, `RequestVFX` warning lights (empty in Phase 1), set emissive **red-orange** telegraph color, broadcast `OnTelegraphStart(AttackID)`; End: clear color."

--- from `build-sequence.md` M4-01 (per-attack readability) ---
"**D** (short propulsion-assisted approach) — thruster cue in `ANS_Telegraph`; root motion (or Motion Warping, **R5**) travel **hard-capped at `MaxTravelDistance`**"

--- from `combat-integration-plan.md` §3.1 row 20 (Phase 2) ---
"one-shot `OnPhase2Committed` signal guarded by `bPhase2` (Phase 1 realization: emissive change + brief pause; authored VFX/sound M5)"

--- from `combat-integration-plan.md` §3.1 row 21 (Clash gate) ---
"`WBP_HUD` shows two honest gate indicators; `IA_FinalClash` accepted only in neutral or the post-counter window (`OPEN` Q19); never auto-triggers"

--- from `combat-integration-plan.md` §6 M5 ---
"fill the already-wired `BP_PresentationSubsystem` wrappers (hit-stop/time-dilation, camera shake + choreography, authored Niagara, sound + mix); arena environmental reaction (still no hazards); final character treatment"

--- from `combat-integration-plan.md` §9 item 17 ---
"Q29 Crimson Vanguard's short in-combat UI label (GDD lists it unfinalized; HUD field stays blank) · Q30 Paragon heavy swap and its deadline (before M4 range tuning) · **Q31 whether Phase 1 ships silent**"

--- from `cinematic-integration-inspection.md` §2 (V2) ---
"the specified `RestoreCombatState()` body restores input, collision, locomotion, tags, lock-on, time dilation, rival BT, and the prompt widget — **it contains no camera-return step.**"

--- from `assignment-04/shared/knowledge-base/core-canon.md`, "The three combatants" ---
"Agent Echo | Energy / VFX: Controlled orange accents"
"Agent Nova | Energy / VFX: Cyan-white combat energy or selected telegraphs (**not a costume recolor**)"
"Crimson Vanguard | Energy / VFX: Red-orange systems and warning lights | Readability target: Threatening reach, obvious tells and recovery"

--- from `assignment-04/shared/knowledge-base/core-canon.md`, "Design pillars" ---
"**Cinematic Rhythm** — brief camera, hit-stop, impact-frame, and VFX bursts punctuate combat without replacing it."

---

# VFX and Audio Cue Sheets — Ascendant Impact

## Status and scope

**Every authored VFX and sound asset in this document is M5 work — Phase 2 of the project, after 1 September.** In Phase 1 the `BP_PresentationSubsystem` wrappers are **wired but empty**, so these cues resolve to no-ops. That is deliberate and structural: plan §2 principle 5 puts all hit-stop, camera shake, VFX, sound, and time dilation behind wrappers that early-return when `bPresentationEnabled` is false, "so disabling presentation cannot change a frame window."

This document is therefore a **specification to fill against**, not a description of anything that exists. Its value now is that it names every cue slot, its trigger, its stop condition, and its cleanup rule *before* M5 begins, so the presentation pass has a checklist instead of a blank page — and so no cue gets authored in a way that would move a gameplay frame.

**No asset names are invented here.** Where an asset does not exist, the entry names the **cue slot** and its required behaviour. The only concrete identifiers used are ones already approved upstream: the five subsystem wrappers (`RequestHitStop`, `RequestCameraShake`, `RequestVFX`, `RequestSound`, `RequestTimeDilation`), the notify states, the widgets, and the Blackboard keys. Actual Niagara system and sound cue names are `OPEN — designer decides` at M5.

**Two hard rules every entry obeys:**
1. **A cue may never drive gameplay timing.** Gameplay timing comes from montage playback and `Set Timer by Event`. A cue reads state; it never gates it. Toggling `bPresentationEnabled` off must change zero measured windows (verified by QA-KS-01 in this directory's test pack).
2. **The five raw engine calls appear in exactly one asset** — `BP_PresentationSubsystem`. No entry below authorises a direct `Spawn Emitter`, `Play Sound`, `Client Start Camera Shake`, `Set Global Time Dilation`, or hit-stop call anywhere else.

### Accessibility principle, applied to every entry

**No critical cue may be color-only or sound-only.** Two independent reasons make this a requirement rather than a nicety:

- **Color-only fails on color vision deficiency.** The Vanguard's entire telegraph language is "red-orange systems and warning lights" against "red armor over black structure." A red-orange flash on red armor is the single worst-case combination for a player with protanopia or deuteranopia — and the telegraph is the game's core read. Every telegraph therefore carries **shape, motion, or pose** as its primary channel, with color as reinforcement only.
- **Sound-only may not exist at all.** **Q31 — whether Phase 1 ships silent — is `OPEN — designer decides`.** A build that ships silent loses every audio-only cue entirely. So audio is never the sole carrier of anything the player must react to.

Every entry below states its **primary channel** (which must be non-color and non-audio), plus reinforcing channels.

### Intensity scale used throughout

Relative labels only — no invented durations or magnitudes.

| Label | Meaning |
|---|---|
| **subtle** | perceptible without drawing the eye off the fight |
| **moderate** | clearly noticeable, does not obscure the fighters |
| **strong** | commands attention for a beat |
| **peak** | the loudest moment in the duel; reserved, used at most a few times per match |

---

## Group 1 — Vanguard telegraph cues

All four share this frame. Differences follow per attack.

**Common trigger:** `ANS_Telegraph` Begin, which sets `CurrentState = Telegraph`, calls `RequestVFX` for warning lights, sets the emissive **red-orange** telegraph color, and broadcasts `OnTelegraphStart(AttackID)`.
**Common stop:** `ANS_Telegraph` End clears the color. The cue **must** stop no later than the moment active frames begin — a telegraph cue still running during the hit is a lie about state.
**Common Phase 2 change:** the telegraph *window* shortens from **0.55–0.95 s** to **0.40–0.75 s**. The cue does not become a different cue; it has less time. Every telegraph cue must remain fully readable at the Phase 2 lower bound. That is the acceptance bar, not the Phase 1 bound.
**Common cleanup:** on counter interrupt, `Montage Stop` fires and notify-end must clear the emissive and kill any looping element. **Note V3/V5:** notify-end-on-interrupt is *assumed, not specified* upstream — so any looping telegraph element authored at M5 must **also** be cleared by `BTTask_ReturnToNeutral` as a backstop, not by notify-end alone.

---

### CUE-TEL-A — Attack A telegraph (close-range committed gauntlet force)

| Field | Specification |
|---|---|
| **Triggering event** | `ANS_Telegraph` Begin on `AM_Vanguard_AttackA`; `OnTelegraphStart(A)` |
| **Where it plays** | Gauntlet sockets (both hands) for the charge element; rival mesh emissive for the warning color; **no** camera effect, **no** UI element |
| **Starts** | First frame of `ANS_Telegraph` |
| **MUST stop by** | `ANS_Telegraph` End — i.e. before `ANS_ActiveHit` Begin. Hard boundary. |
| **Readability purpose** | Sell "distinct wind-up." A is the attack the player learns the fight on; its tell must be the most legible in the set. |
| **Intensity** | **moderate**, building. A is frequent; a peak cue here would exhaust the player. |
| **Phase 2 change** | Same cue, compressed window (0.40–0.75 s). No new element. |
| **Primary channel (non-color, non-audio)** | **The held gauntlet pose.** Attack A's wind-up is a body-shape read — pose held long enough to be identified from silhouette alone. |
| **Reinforcing** | red-orange gauntlet emissive; charge-up audio |
| **Cleanup on interruption** | Emissive cleared and charge element killed on `Montage Stop`; backstopped by Return to Neutral. No orphan looping emitter on the gauntlet sockets. |
| **Accessibility** | Passes: identifiable with color removed (pose) and with audio removed (pose + motion). Verify by playtesting with a greyscale filter and with sound muted. |

---

### CUE-TEL-B — Attack B telegraph (committed forward-pressure sequence)

| Field | Specification |
|---|---|
| **Triggering event** | `ANS_Telegraph` Begin on `AM_Vanguard_AttackB`; `OnTelegraphStart(B)` |
| **Where it plays** | Rival mesh emissive; a directional element oriented along the committed advance line; **floor** element optional to mark the advance path |
| **Starts** | First frame of `ANS_Telegraph` |
| **MUST stop by** | `ANS_Telegraph` End. Note B has **multiple `ANS_ActiveHit` beats** — the telegraph cue stops before the *first* beat and does not re-fire between beats. |
| **Readability purpose** | Sell "visible first beat." The player must know B has started, and that more beats are coming, from the first beat. |
| **Intensity** | **moderate** |
| **Phase 2 change** | Compressed window. **Watch:** B's beats are the dodge opportunities; if a Phase 2 cue overlaps into the beat gaps it will visually hide them. Beat gaps must stay visually clean in both phases. |
| **Primary channel** | **Forward-lean pose plus advance direction.** The commitment to a direction is the read. |
| **Reinforcing** | emissive; directional audio |
| **Cleanup on interruption** | A counter can only land on beat 1 (the counter window sits at late telegraph / early active). On interrupt, clear emissive and any floor/path element. Per-beat elements authored at M5 must each clear independently — an orphan beat element after a counter is the predicted failure. |
| **Accessibility** | Passes: pose and direction carry it. **Do not** encode "how many beats remain" in color alone — if that information is surfaced at all, use a countable visual (discrete marks) or omit it. |

---

### CUE-TEL-C — Attack C telegraph (armored reach and space control)

| Field | Specification |
|---|---|
| **Triggering event** | `ANS_Telegraph` Begin on `AM_Vanguard_AttackC`; `OnTelegraphStart(C)` |
| **Where it plays** | Rival mesh emissive; **the threatened space** — a floor or volumetric indication of reach, oriented by body direction; reach-limb socket |
| **Starts** | First frame of `ANS_Telegraph`. **Must be live before `ANS_TrackingLock` ends**, since C's facing locks *before* active frames — the direction becomes readable at the lock, and the cue must be showing it by then. |
| **MUST stop by** | `ANS_Telegraph` End |
| **Readability purpose** | Sell **both** GDD obligations: "clear body direction" **and** "visible active range." C is the only attack whose cue must communicate *space*, not just timing. |
| **Intensity** | **moderate to strong** — C's threat is spatial and needs footprint legibility |
| **Phase 2 change** | Compressed window. Spatial information must resolve inside 0.40–0.75 s; a slow-blooming range indicator that only reads at 0.95 s **fails Phase 2**. Author against the Phase 2 lower bound. |
| **Primary channel** | **Body orientation plus a geometric footprint** — shape, not hue. A floor decal or outline whose *extent* is the information. |
| **Reinforcing** | emissive; reach audio |
| **Cleanup on interruption** | The floor/space element is the highest orphan risk in the set — it is not attached to a socket and may outlive the montage. Must be explicitly destroyed on `Montage Stop` **and** at Return to Neutral. |
| **Accessibility** | Passes only if the range indication is shape-based. A red-tinted floor area is a **fail** — the cue would be competing with the Vanguard's own red-orange warning language on the mesh directly in front of it, and hue alone cannot separate the two for a protanopic player. Use an outline, hatch, or edge. *(The Shattered Ring's own palette is not specified by the GDD — it is described functionally as an "industrial" arena with a central floor and far doorway. Do not author against an assumed arena color.)* |

---

### CUE-TEL-D — Attack D telegraph (short propulsion-assisted approach)

| Field | Specification |
|---|---|
| **Triggering event** | `ANS_Telegraph` Begin on `AM_Vanguard_AttackD`; `OnTelegraphStart(D)`. The **thruster cue lives inside `ANS_Telegraph`** per M4-01. |
| **Where it plays** | Thruster/propulsion sockets (back, legs — dependent on the chosen proxy skeleton, **verify sockets exist**); rival mesh emissive |
| **Starts** | First frame of `ANS_Telegraph` — and critically **before any root-motion frame**. The GDD requirement is "thruster cue **before movement**." |
| **MUST stop by** | `ANS_Telegraph` End. The thrust visual may continue into the active window only if authored as a separate active-phase element; the *telegraph* cue itself stops. |
| **Readability purpose** | Give the player the one beat of warning that distance is about to stop protecting them. This is the highest-stakes telegraph in the game: D closes a gap explosively. |
| **Intensity** | **strong** — D punishes the player for a spacing read they thought was safe; the warning must earn that |
| **Phase 2 change** | Compressed window means **less warning before the same lunge**. This is the most dangerous Phase 2 compression in the set. The thruster cue must be unmistakable at **0.40 s**. If it is not, that is a finding for the designer, not something to tune around. |
| **Primary channel** | **Propulsion body pose plus the pre-movement beat itself** — the fact that the rival visibly loads before travelling. |
| **Reinforcing** | thruster emissive; thruster audio (strong, but never the only channel — Q31 may remove it entirely) |
| **Cleanup on interruption** | A counter at the start of the lunge stops a montage **mid-root-motion**. Thruster elements must die immediately; a thruster still emitting on a stationary rival reads as an attack still incoming. Clear on `Montage Stop` and at Return to Neutral. |
| **Accessibility** | Passes: the load-and-launch pose carries it without color or sound. **Do not** rely on a thruster glow as the primary tell. |

---

## Group 2 — Player defensive cues

### CUE-DEF-PERFECT — Perfect dodge

| Field | Specification |
|---|---|
| **Triggering event** | The rival's `ANS_ActiveHit` trace lands while the player holds `State.PerfectWindow` — detected in `BP_CombatComponent.ResolveIncomingHit`. Damage resolves to 0 and the meter gains **+12**. |
| **Where it plays** | Player mesh / player-centred; a brief camera response via `RequestCameraShake`; `RequestHitStop` for the punctuation beat; **`WBP_HUD`** meter bar for the +12 |
| **Starts** | The frame `ResolveIncomingHit` classifies the hit as a perfect dodge |
| **MUST stop by** | Before the Impact Window prompt opens, so it never competes with the prompt for attention. The prompt is the thing the player must act on next. |
| **Readability purpose** | Confirm the highest-skill defensive read in the game landed. This cue is the reward that teaches the mechanic — a player who cannot tell a perfect dodge from an ordinary dodge cannot learn it. |
| **Intensity** | **strong**. Deliberately louder than an ordinary dodge, which grants **no meter** (plan §3.2 row 8: "ordinary dodge grants no meter"). Whether an ordinary dodge carries any cue at all is `OPEN — designer decides` — no source says it has none. The requirement here is only that the two are unmistakably distinguishable, because that contrast is what teaches the mechanic. |
| **Phase 2 change** | No change. The window itself is unchanged by phase; the cue should feel identical so the player's learned read stays valid under pressure. |
| **Primary channel** | **Hit-stop plus the meter bar moving.** Time-based and positional, not color, not audio. |
| **Reinforcing** | player accent VFX — **Echo: controlled orange; Nova: cyan-white combat energy** (per core-canon, and explicitly *not* a costume recolor); camera shake; audio sting |
| **Cleanup on interruption** | Short and self-terminating by design; must not survive into the Impact burst. If the player dies on the same frame (edge case in QA-V4-02), the cue must not outlive `EndDuel`. |
| **Accessibility** | Passes: hit-stop is felt, and the meter delta is a numeric/positional change. **The Echo-orange / Nova-cyan distinction must never be load-bearing** — it is flavour, and the two are separable by hue only, which fails on CVD. |

---

## Group 3 — Impact Window cues

### CUE-IW-OPEN — Impact Window prompt opens

*Not in the originally requested list, but the success and failure cues below are meaningless without it — the prompt is what the player responds to. Included and flagged.*

| Field | Specification |
|---|---|
| **Triggering event** | `BP_ImpactWindowDirector.RequestImpactWindow()` accepted → `OpenWindow()`. First window **0.75 s**; standard window **0.35–0.50 s**. |
| **Where it plays** | **`WBP_ImpactPrompt`** (UI) is the carrier. Optional subtle world/camera framing. |
| **Starts** | The frame the window opens — **not before**. A cue that anticipates the window would function as a pre-open input tell and edges toward the buffering the GDD forbids. |
| **MUST stop by** | The frame the window closes, by success or by expiry. A prompt visible after the window closed will produce presses that are correctly discarded and feel broken. |
| **Readability purpose** | Communicate *that* a window is open and *how much time remains*. The GDD's onboarding rule requires the player's own input — so the prompt must make the deadline legible, since the game "does not press the input for the player." |
| **Intensity** | **strong** — it is a call to action under a sub-second deadline |
| **Phase 2 change** | None inherent. Window widths do not change by phase; the first-versus-standard distinction (0.75 s vs 0.35–0.50 s) is what varies, and the prompt must make the *remaining time* readable in both. |
| **Primary channel** | **A depleting shape** — a radial or linear timer whose geometry shows time left. Not a color shift, not a beep. |
| **Reinforcing** | color; audio tick |
| **Cleanup on interruption** | Hidden by `RestoreCombatState()` on every branch (this *is* in the specified restore list). Also hidden if either fighter dies mid-window. |
| **Accessibility** | Passes: geometry carries time. **A prompt that only changes color as time runs out is a fail.** The wider first window at 0.75 s is the onboarding affordance and must be visibly wider, not just longer-lived. |

---

### CUE-IW-SUCCESS — Impact Window succeeded

| Field | Specification |
|---|---|
| **Triggering event** | `IA_Impact` pressed while `bWindowOpen` → SUCCESS. Meter **+20**. The **1–3 s** choreographed burst begins (montage pair on both fighters). |
| **Where it plays** | Both fighters (burst montage pair); camera via `RequestCameraShake` and, at M5, choreography; `RequestHitStop` and `RequestTimeDilation` for the impact frame; `WBP_HUD` for +20 |
| **Starts** | The frame SUCCESS resolves |
| **MUST stop by** | **Before `RestoreCombatState()` completes.** Nothing from this cue may survive into live gameplay. The burst is 1–3 s (GDD); no cue element may outlast it. |
| **Readability purpose** | This is the game's central promise delivered: "real-time martial-arts combat rewards player skill with brief, earned anime-style cinematic spectacle." It must feel earned, and — per the Cinematic Rhythm pillar — must "punctuate combat without replacing it." |
| **Intensity** | **peak** for the burst's opening frames, decaying. The loudest recurring moment in the duel. |
| **Phase 2 change** | No change specified. The burst stays within 1–3 s in both phases. |
| **Primary channel** | **Hit-stop, time dilation, and the montage pair itself** — motion and timing. |
| **Reinforcing** | VFX, camera shake, audio, +20 on the meter bar |
| **Cleanup on interruption** | **The highest-risk cleanup in the document.** Open defects V1 (no specified rival-AI suspension during the burst), V2 (no camera-return step in restore), and V4 (montage cleanup unspecified on interruption paths) all land here. Every element must be explicitly terminated at restore, and **time dilation must return to 1.0** — that step *is* specified in restore; the camera return is not. Author accordingly and do not assume restore cleans up after you. |
| **Accessibility** | Passes: motion and timing carry it. Since this is the reward moment, ensure it is distinguishable from CUE-IW-FAIL **without** audio — a silent build (Q31) must still make success and failure unmistakably different. |

---

### CUE-IW-FAIL — Impact Window failed (expired)

| Field | Specification |
|---|---|
| **Triggering event** | The window timer expires with no `IA_Impact` press. Per the GDD: "No cinematic extension; return to combat with no extra punishment," and the game "returns immediately to normal combat." |
| **Where it plays** | `WBP_ImpactPrompt` dismissal only. **No** camera effect, **no** hit-stop, **no** time dilation, **no** world VFX. |
| **Starts** | The frame the window expires |
| **MUST stop by** | Immediately — within the prompt's dismissal. Control returns **immediately**; a lingering failure cue would read as a punishment the GDD forbids. |
| **Readability purpose** | Tell the player the window closed, and **nothing else**. Meter gained nothing (**+0** for waiting). This cue's job is to be honest and get out of the way. |
| **Intensity** | **subtle**. Deliberately the quietest cue in the document. |
| **Phase 2 change** | None. |
| **Primary channel** | **The prompt's disappearance** — the absence itself is the information. |
| **Reinforcing** | at most a soft dismissal; **no** negative sting |
| **Cleanup on interruption** | Trivially short. Prompt hidden by `RestoreCombatState()`. |
| **Accessibility** | Passes: prompt removal is positional. **Design warning:** do not author a "failure" flourish. A punishing red flash or harsh sting would contradict "no extra punishment" — the cue would *be* the punishment even though no mechanical penalty exists. Failure must feel neutral, not scolding. |

---

## Group 4 — Phase 2 escalation

### CUE-P2-ESCALATE — Phase 2 committed

| Field | Specification |
|---|---|
| **Triggering event** | One-shot `OnPhase2Committed`, guarded by `bPhase2`. Set pending at rival health **≤ 50%**, but **committed only inside `BTTask_ReturnToNeutral`** — never mid-telegraph, never mid-active. |
| **Where it plays** | Rival mesh (emissive change); brief pause beat; `WBP_HUD` if a phase indicator exists |
| **Starts** | The frame Phase 2 commits at Return to Neutral — **not** the frame health crossed 50% |
| **MUST stop by** | Before the next `Telegraph` begins. The escalation cue must never overlap a telegraph — it would compete with the read the whole game depends on. |
| **Readability purpose** | Tell the player the rules of pressure just changed: "same attacks, stronger pressure." The player's learned reads remain valid but their timing budget shrank. |
| **Intensity** | **strong**, once. **Fires exactly once per duel** — the one-shot guard is a hard requirement, and a repeating escalation cue is a defect (QA-P2-01 counts occurrences). |
| **Phase 2 change** | This *is* the Phase 2 cue. The **persistent** change afterwards is the rival's altered emissive state — a standing condition, not a repeated event. |
| **Primary channel** | **The pause beat plus a silhouette or emissive-state change that persists.** The pause is temporal; the persistent state change is verifiable at a glance at any later moment. |
| **Reinforcing** | audio escalation sting; HUD indicator |
| **Cleanup on interruption** | The transient beat self-terminates. The **persistent** state must survive every subsequent overlay and restore — a rival that visually reverts to Phase 1 appearance after an Impact burst is a bug, since `bPhase2` never reverts. Verify the persistent element is not cleared by `RestoreCombatState()`. |
| **Accessibility** | Passes: the pause is temporal and the persistent change should include a non-hue component (brightness, pattern, or added element), because "red armor becomes differently-red" is invisible on CVD. Since Phase 2 is a **standing** condition, a player must be able to answer "am I in Phase 2?" at any time without color. |

**Phase 1 realization note:** plan §3.1 row 20 specifies the Phase 1 realization as "emissive change + brief pause," with "authored VFX/sound M5." So this is the one cue in this document that has *any* Phase 1 presence — and even that is a material parameter change, not authored VFX.

---

## Group 5 — Final Clash cues

### CUE-FC-ELIGIBLE — Final Clash becomes available

*Also not in the originally requested list, but success and failure both require the player to have initiated — and initiation requires knowing eligibility. Included and flagged.*

| Field | Specification |
|---|---|
| **Triggering event** | `EvaluateClashGate()` returns true: Meter **100** AND rival health **≤ 25%** AND no cooldown AND not `bInClash`. |
| **Where it plays** | `WBP_HUD` — **two honest gate indicators**, one per condition |
| **Starts** | When both conditions hold |
| **MUST stop by** | When either condition stops holding, or on initiation |
| **Readability purpose** | The GDD's single gate is an **AND**: "If one condition is met first, the Clash remains locked until the other is met." The HUD must show *which* condition is outstanding — one combined indicator would hide that and mislead the player into waiting for the wrong thing. |
| **Intensity** | **moderate** while pending per-condition; **strong** at the moment both land |
| **Phase 2 change** | Eligibility is reachable only in Phase 2 territory by construction (≤25% health is past the 50% Phase 2 threshold). No separate variant. |
| **Primary channel** | **Two discrete, separately-legible indicators** whose filled/unfilled state is positional. |
| **Reinforcing** | color; an eligibility sting |
| **Cleanup on interruption** | Must clear on initiation and on cooldown. **After a failed Clash the indicators must honestly re-lock** — meter drops to **50**, so the meter condition is false again and must read false. |
| **Accessibility** | Passes if filled/unfilled is a shape or fill state. Two indicators distinguished only by hue is a **fail**. Note the HUD's Vanguard short label field stays **blank** (`OPEN — Q29`) — do not author a cue that depends on a label that does not exist. |

---

### CUE-FC-SUCCESS — Final Clash succeeded

| Field | Specification |
|---|---|
| **Triggering event** | Both timing beats hit → finisher → rival health to 0 → `EndDuel(Win)` |
| **Where it plays** | Both fighters; `LS_FinalClash` (one camera cut in Phase 1, full choreography at M5-07); peak camera and time-dilation work; `WBP_Result` Win state |
| **Starts** | On the second successful beat |
| **MUST stop by** | **Before the Win screen appears** — plan §3.1 row 22 requires `RestoreCombatState()` to run *before* the result screen. No cue element may persist under `WBP_Result`. |
| **Readability purpose** | The duel's climax and the payoff for the whole meter economy. The single most-earned moment in the game. |
| **Intensity** | **peak**, and the highest peak in the duel — reachable at most once per match. |
| **Phase 2 change** | N/A — only reachable in the endgame. |
| **Primary channel** | **The finisher choreography and the rival's defeat** — unambiguous motion. |
| **Reinforcing** | camera cut, peak VFX, audio, Win screen |
| **Cleanup on interruption** | `LS_FinalClash` `OnStop` **and** `OnFinished` both route to restore. **V2 applies directly:** restore contains no camera-return step, so a Clash-success camera return currently rests on assumed Level Sequence finish behaviour. Note also the plan's §8.4 fallback — if the sequence handoff proves fragile, the Phase 1 fallback is **no camera cut at all**, which "loses nothing gameplay-tests care about." Author so the cue survives that fallback. |
| **Accessibility** | Passes: motion and the Win screen carry it. |

---

### CUE-FC-FAILURE — Final Clash failed

| Field | Specification |
|---|---|
| **Triggering event** | Any beat missed → the seven-step recovery: stop montages/sequence and camera back → separate fighters → preserve health → rival at **1 HP floor** → meter to **50** → **3 s** cooldown → `RestoreCombatState()`. |
| **Where it plays** | Both fighters (separation); `WBP_HUD` for the meter drop to 50 and the re-locked gate indicators; camera returns to gameplay |
| **Starts** | The frame the beat is missed |
| **MUST stop by** | Before control returns. The GDD is explicit: a failed Clash "does not … leave either fighter in a cinematic state." |
| **Readability purpose** | Communicate three things without lying about any: the attempt failed; **the duel continues**; the setback is the meter, not the player's life. The GDD calls it "a meaningful meter setback" that "preserves a recoverable path to victory." |
| **Intensity** | **moderate** — and this is a deliberate judgement, not a hedge. A **peak** failure cue would read as a death or a defeat, which is exactly what the GDD forbids: no restart, no automatic player death. The cue must feel like a lost opportunity, not a catastrophe. |
| **Phase 2 change** | N/A. |
| **Primary channel** | **The visible separation of the fighters plus the meter bar dropping to 50.** Both are positional. |
| **Reinforcing** | subdued audio; camera return |
| **Cleanup on interruption** | Every element must clear before the 3 s cooldown ends, so the player has clean vision when control returns. **`State.Clashing` must be cleared and `bInClash` set false** — a lingering Clash cue over live gameplay is the stranded-cinematic-state failure the inspection is most concerned about. |
| **Accessibility** | Passes: separation and the meter drop are both non-color, non-audio. **Do not** signal failure by color-shifting the HUD alone. |
| **1 HP floor — UNRESOLVED** | **Q22 is open**: whether the floor is permanent from first eligibility or Clash-attempt-only. The inspection calls it "the most consequential open value." **No cue in this document depicts the floor**, because a cue that visually announces "the rival cannot die yet" would be wrong under one reading and right under the other. If the designer resolves Q22 toward *permanent*, a persistent low-health indication may become desirable; if *Clash-only*, it must not exist. **Deferred to the designer — do not author a floor cue until Q22 is answered.** |

---

## Cue index

| Cue | Trigger | Intensity | Phase 2 differs | Milestone |
|---|---|---|---|---|
| CUE-TEL-A | `ANS_Telegraph` on Attack A | moderate | window shortens | M2 slot / M5 authored |
| CUE-TEL-B | `ANS_Telegraph` on Attack B | moderate | window shortens | M4 slot / M5 authored |
| CUE-TEL-C | `ANS_Telegraph` on Attack C | moderate–strong | window shortens | M4 slot / M5 authored |
| CUE-TEL-D | `ANS_Telegraph` on Attack D | strong | window shortens — least warning | M4 slot / M5 authored |
| CUE-DEF-PERFECT | perfect dodge in `ResolveIncomingHit` | strong | no | M3 slot / M5 authored |
| CUE-IW-OPEN | window opens | strong | no | M3 slot / M5 authored |
| CUE-IW-SUCCESS | `IA_Impact` inside window | peak | no | M3 slot / M5 authored |
| CUE-IW-FAIL | window expires | subtle | no | M3 slot / M5 authored |
| CUE-P2-ESCALATE | `OnPhase2Committed` | strong, once | is the change | M4 (partial in Phase 1) / M5 |
| CUE-FC-ELIGIBLE | both gate conditions true | moderate–strong | n/a | M4 slot / M5 authored |
| CUE-FC-SUCCESS | both beats hit | peak | n/a | M4 slot / M5 authored |
| CUE-FC-FAILURE | a beat missed | moderate | n/a | M4 slot / M5 authored |

## Accessibility summary — the primary channel of every cue

Every entry's primary channel is non-color and non-audio, so a build that ships silent (Q31) or a player with color vision deficiency loses nothing critical.

| Cue | Primary channel | Type |
|---|---|---|
| CUE-TEL-A | held gauntlet pose | shape |
| CUE-TEL-B | forward-lean pose + advance direction | shape / motion |
| CUE-TEL-C | body orientation + geometric footprint | shape |
| CUE-TEL-D | load-and-launch pose before movement | motion |
| CUE-DEF-PERFECT | hit-stop + meter delta | timing / position |
| CUE-IW-OPEN | depleting geometric timer | shape |
| CUE-IW-SUCCESS | hit-stop, time dilation, montage pair | timing / motion |
| CUE-IW-FAIL | prompt disappearance | position |
| CUE-P2-ESCALATE | pause beat + persistent non-hue state change | timing / shape |
| CUE-FC-ELIGIBLE | two discrete fill-state indicators | shape / position |
| CUE-FC-SUCCESS | finisher choreography | motion |
| CUE-FC-FAILURE | fighter separation + meter drop to 50 | position |

**Two combinations flagged as forbidden:**
- **Red-orange on red armor as a primary telegraph channel.** The Vanguard is "red armor over black structure" with "red-orange systems and warning lights." That pairing is the worst case for CVD, and the telegraph is the core read. Color reinforces; pose carries.
- **Echo-orange versus Nova-cyan as load-bearing information.** These are flavour accents distinguished by hue alone. Fine as identity; never as a cue a player must decode.

## Open values this document does not resolve

| Tag | Value | Affects |
|---|---|---|
| **Q31** | whether Phase 1 ships silent | every audio channel — the reason audio is never primary |
| **Q22** | 1 HP floor permanent vs. Clash-attempt-only | CUE-FC-FAILURE — no floor cue authored until answered |
| Q29 | Vanguard short in-combat UI label (HUD field blank) | CUE-FC-ELIGIBLE |
| Q30 | Paragon heavy swap | all socket-attached cues — sockets must be re-verified after any swap |
| — | all Niagara system and sound cue asset names | every entry — `OPEN` at M5 |
| — | whether the Phase 1 Clash ships cut-less (plan §8.4) | CUE-FC-SUCCESS |

## What this document does not do

- It does not author or name a single asset. Cue slots and required behaviour only.
- It does not schedule any of this into M1–M4. Authored VFX and sound are **M5**, behind a stable M4. The one exception is the Phase 2 emissive change and pause, which plan §3.1 row 20 already places in Phase 1.
- It does not permit a cue to affect gameplay timing. All five wrappers early-return when presentation is disabled, and QA-KS-01 verifies zero timing drift.
- It does not duplicate the player-facing Impact Window beat descriptions or environmental reaction language already in `assignment-04/shared/knowledge-base/`. This is the cue-level technical contract: trigger, location, start, stop, cleanup, accessibility.
- It does not add arena hazards. Plan §6 M5 keeps environmental reaction hazard-free.
- It does not resolve a provisional value.
