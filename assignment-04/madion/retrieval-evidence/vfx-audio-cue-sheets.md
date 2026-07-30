# Retrieval Evidence — `vfx-audio-cue-sheets.md`

Copy only. Full generated output: `../outputs/vfx-audio-cue-sheets.md`.

---

## QUERY

> For every gameplay event in Ascendant Impact that must be communicated to the player — each Vanguard telegraph, perfect dodge, Impact Window success and failure, Phase 2 escalation, and Final Clash success and failure — what cue fires, where does it play, when must it start and stop, what is it for, how does it change in Phase 2, how is it cleaned up after interruption, and how does it stay readable for a player who cannot rely on color or on sound?

---

## SOURCES SELECTED — why each, and what it contributed

| Source | Why selected | What it contributed |
|---|---|---|
| `gdd/ascendant-impact-gdd-v0.4.md` | Source of truth for what each cue must communicate and for the rules a cue must not contradict | the telegraph state's own definition ("warning lights, sound, and readable direction"); the four attacks' readability requirements; window widths and the 1–3 s burst; the "no extra punishment" failure rule; the Clash failure rules; Phase 2 at 50%; the "armor and scale may intensify presentation, but they do not remove readable counterplay" line |
| `combat-integration-plan.md` | Defines the only legal mechanism through which any cue may fire, and the M5 gating | §2 principle 5 presentation severability; §3.1 row 26 the five wrappers and the kill-switch; row 20 the Phase 1 emissive-change-plus-pause realization; row 21 the two honest gate indicators; §6 M5 contents; §9 item 17 Q31 |
| `build-sequence.md` | Supplies the exact notify-level hook each cue attaches to | M2-13 `ANS_Telegraph` Begin/End behaviour including the red-orange emissive and `OnTelegraphStart`; M4-01 the thruster cue living inside `ANS_Telegraph` |
| `cinematic-integration-inspection.md` | The restoration defects determine what "MUST stop" and "cleanup" can honestly claim | V2 (no camera-return step in restore) — used in CUE-IW-SUCCESS and CUE-FC-SUCCESS cleanup rows |
| `assignment-04/shared/knowledge-base/core-canon.md` | Anthony's derived layer; the per-character VFX language and the Cinematic Rhythm pillar in citable form | Echo "controlled orange accents"; Nova "cyan-white combat energy … **not a costume recolor**"; Vanguard "red-orange systems and warning lights" over "red armor over black structure"; the Cinematic Rhythm pillar |

---

## RETRIEVED TEXT → GENERATED OUTPUT, side by side

### Pair 1 — presentation severability, which gates the whole document

**RETRIEVED** (`combat-integration-plan.md` §2 principle 5):
> "All hit-stop, camera shake, VFX, sound, and time dilation route through `BP_PresentationSubsystem` wrappers that early-return when `bPresentationEnabled` is false. Gameplay timing is driven by montage playback and `Set Timer by Event`, never through a presentation call, so disabling presentation cannot change a frame window. The subsystem is wired (empty) in M1 so all M5 work lands without touching gameplay code. M5 remains last."

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 26):
> "the ONLY legal wrappers (`RequestHitStop`, `RequestCameraShake`, `RequestVFX`, `RequestSound`, `RequestTimeDilation`), each early-returning when disabled; hard rule: the five raw engine calls appear in exactly this one asset; wired empty in M1, filled only in M5"

**GENERATED** (status and scope, plus the two hard rules):
> "**Every authored VFX and sound asset in this document is M5 work — Phase 2 of the project, after 1 September.** In Phase 1 the `BP_PresentationSubsystem` wrappers are **wired but empty**, so these cues resolve to no-ops."
>
> "**1. A cue may never drive gameplay timing.** Gameplay timing comes from montage playback and `Set Timer by Event`. A cue reads state; it never gates it. Toggling `bPresentationEnabled` off must change zero measured windows"
>
> "**2. The five raw engine calls appear in exactly one asset** — `BP_PresentationSubsystem`. No entry below authorises a direct `Spawn Emitter`, `Play Sound`, `Client Start Camera Shake`, `Set Global Time Dilation`, or hit-stop call anywhere else."

---

### Pair 2 — the telegraph hook

**RETRIEVED** (`build-sequence.md` M2-13, `ANS_Telegraph`):
> "Begin: `Set Blackboard CurrentState = Telegraph`, `RequestVFX` warning lights (empty in Phase 1), set emissive **red-orange** telegraph color, broadcast `OnTelegraphStart(AttackID)`; End: clear color."

**RETRIEVED** (`gdd` Page 5, state table):
> "Telegraph | Show committed pose, warning lights, sound, and readable direction | 0.55–0.95 s | 0.40–0.75 s | Telegraph completes"

**GENERATED** (Group 1 common frame):
> "**Common trigger:** `ANS_Telegraph` Begin, which sets `CurrentState = Telegraph`, calls `RequestVFX` for warning lights, sets the emissive **red-orange** telegraph color, and broadcasts `OnTelegraphStart(AttackID)`.
> **Common stop:** `ANS_Telegraph` End clears the color. The cue **must** stop no later than the moment active frames begin — a telegraph cue still running during the hit is a lie about state.
> **Common Phase 2 change:** the telegraph *window* shortens from **0.55–0.95 s** to **0.40–0.75 s**. The cue does not become a different cue; it has less time. Every telegraph cue must remain fully readable at the Phase 2 lower bound. That is the acceptance bar, not the Phase 1 bound."

---

### Pair 3 — D's thruster cue must precede movement

**RETRIEVED** (`gdd` Page 5): "Authored attack D | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap"

**RETRIEVED** (`build-sequence.md` M4-01): "**D** … thruster cue in `ANS_Telegraph`"

**GENERATED** (CUE-TEL-D):
> "| **Starts** | First frame of `ANS_Telegraph` — and critically **before any root-motion frame**. The GDD requirement is "thruster cue **before movement**." |"
>
> "| **Phase 2 change** | Compressed window means **less warning before the same lunge**. This is the most dangerous Phase 2 compression in the set. The thruster cue must be unmistakable at **0.40 s**. If it is not, that is a finding for the designer, not something to tune around. |"

---

### Pair 4 — the failure cue must not punish

**RETRIEVED** (`gdd` Page 3, Impact Windows):
> "Failure does not auto-correct the input; the game returns immediately to normal combat."
> "First Impact Window | … | 0.75 seconds | No cinematic extension; return to combat with no extra punishment"

**RETRIEVED** (`gdd` Page 3–4, meter table): "Taking damage / waiting +0"

**GENERATED** (CUE-IW-FAIL):
> "| **Where it plays** | `WBP_ImpactPrompt` dismissal only. **No** camera effect, **no** hit-stop, **no** time dilation, **no** world VFX. |
> | **MUST stop by** | Immediately — within the prompt's dismissal. Control returns **immediately**; a lingering failure cue would read as a punishment the GDD forbids. |
> | **Intensity** | **subtle**. Deliberately the quietest cue in the document. |
> | **Primary channel** | **The prompt's disappearance** — the absence itself is the information. |"
>
> "| **Accessibility** | … **Design warning:** do not author a "failure" flourish. A punishing red flash or harsh sting would contradict "no extra punishment" — the cue would *be* the punishment even though no mechanical penalty exists. Failure must feel neutral, not scolding. |"

---

### Pair 5 — Phase 2's Phase 1 realization

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 20):
> "one-shot `OnPhase2Committed` signal guarded by `bPhase2` (Phase 1 realization: emissive change + brief pause; authored VFX/sound M5)"

**RETRIEVED** (`gdd` Page 4, Encounter flow): "Phase 2 | Begins at 50% Crimson Vanguard health; same attacks, stronger pressure | Apply learned reads under stress"

**GENERATED** (CUE-P2-ESCALATE):
> "| **Starts** | The frame Phase 2 commits at Return to Neutral — **not** the frame health crossed 50% |
> | **Intensity** | **strong**, once. **Fires exactly once per duel** — the one-shot guard is a hard requirement, and a repeating escalation cue is a defect (QA-P2-01 counts occurrences). |"
>
> "| **Cleanup on interruption** | The transient beat self-terminates. The **persistent** state must survive every subsequent overlay and restore — a rival that visually reverts to Phase 1 appearance after an Impact burst is a bug, since `bPhase2` never reverts. |"
>
> "**Phase 1 realization note:** plan §3.1 row 20 specifies the Phase 1 realization as "emissive change + brief pause," with "authored VFX/sound M5." So this is the one cue in this document that has *any* Phase 1 presence"

---

### Pair 6 — the two honest gate indicators

**RETRIEVED** (`gdd` Page 3, Final Clash unlock rule):
> "REVISED — SINGLE GATE  The Final Clash becomes available only when BOTH conditions are true: Ascension Meter is full at 100 AND Crimson Vanguard's health is at or below 25%. If one condition is met first, the Clash remains locked until the other is met."

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 21): "`WBP_HUD` shows two honest gate indicators … never auto-triggers"

**GENERATED** (CUE-FC-ELIGIBLE):
> "| **Readability purpose** | The GDD's single gate is an **AND**: "If one condition is met first, the Clash remains locked until the other is met." The HUD must show *which* condition is outstanding — one combined indicator would hide that and mislead the player into waiting for the wrong thing. |"
>
> "| **Cleanup on interruption** | Must clear on initiation and on cooldown. **After a failed Clash the indicators must honestly re-lock** — meter drops to **50**, so the meter condition is false again and must read false. |"

---

### Pair 7 — the Clash failure cue's intensity, argued from the GDD

**RETRIEVED** (`gdd` Page 4):
> "PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player automatically, or leave either fighter in a cinematic state. It creates a meaningful meter setback, restores valid combat states, and preserves a recoverable path to victory."

**GENERATED** (CUE-FC-FAILURE):
> "| **Readability purpose** | Communicate three things without lying about any: the attempt failed; **the duel continues**; the setback is the meter, not the player's life. The GDD calls it "a meaningful meter setback" that "preserves a recoverable path to victory." |
> | **Intensity** | **moderate** — and this is a deliberate judgement, not a hedge. A **peak** failure cue would read as a death or a defeat, which is exactly what the GDD forbids: no restart, no automatic player death. The cue must feel like a lost opportunity, not a catastrophe. |
> | **Primary channel** | **The visible separation of the fighters plus the meter bar dropping to 50.** Both are positional. |"

---

### Pair 8 — Q22 forces the absence of a floor cue

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 23): "CV `MinHealthFloor = 1` (Q22 open: permanent vs Clash-only)"

**GENERATED** (CUE-FC-FAILURE, final row):
> "| **1 HP floor — UNRESOLVED** | **Q22 is open**: whether the floor is permanent from first eligibility or Clash-attempt-only. The inspection calls it "the most consequential open value." **No cue in this document depicts the floor**, because a cue that visually announces "the rival cannot die yet" would be wrong under one reading and right under the other. If the designer resolves Q22 toward *permanent*, a persistent low-health indication may become desirable; if *Clash-only*, it must not exist. **Deferred to the designer — do not author a floor cue until Q22 is answered.** |"

---

### Pair 9 — the accessibility constraint, derived from two independent source facts

**RETRIEVED** (`assignment-04/shared/knowledge-base/core-canon.md`, "The three combatants"):
> "Crimson Vanguard | … Material family: Red armor over black structure | Energy / VFX: Red-orange systems and warning lights"
> "Agent Echo | Energy / VFX: Controlled orange accents"
> "Agent Nova | Energy / VFX: Cyan-white combat energy or selected telegraphs (**not a costume recolor**)"

**RETRIEVED** (`combat-integration-plan.md` §9 item 17): "**Q31 whether Phase 1 ships silent**"

**GENERATED** (accessibility principle):
> "- **Color-only fails on color vision deficiency.** The Vanguard's entire telegraph language is "red-orange systems and warning lights" against "red armor over black structure." A red-orange flash on red armor is the single worst-case combination for a player with protanopia or deuteranopia — and the telegraph is the game's core read. Every telegraph therefore carries **shape, motion, or pose** as its primary channel, with color as reinforcement only.
> - **Sound-only may not exist at all.** **Q31 — whether Phase 1 ships silent — is `OPEN — designer decides`.** A build that ships silent loses every audio-only cue entirely. So audio is never the sole carrier of anything the player must react to."

**GENERATED** (the two forbidden combinations):
> "- **Red-orange on red armor as a primary telegraph channel.** … Color reinforces; pose carries.
> - **Echo-orange versus Nova-cyan as load-bearing information.** These are flavour accents distinguished by hue alone. Fine as identity; never as a cue a player must decode."

---

## POST-CRITIC CORRECTIONS APPLIED TO THIS OUTPUT

Finding F6 in `../critic-evidence/critic-report.md`.

### F6a — an invented arena palette

**RETRIEVED** (`gdd/ascendant-impact-gdd-v0.4.md` Page 9, "Official arena direction") — the arena is described **functionally, with no colors**:
> "The established industrial Shattered Ring arena is locked as the official Version 1 environment."
> "Central combat floor | Open, readable space for spacing, lock-on, dodges, counters, and Final Clash staging"
> "Far doorway | Dedicated Crimson Vanguard entrance axis"

**BEFORE:** "A red-tinted floor area is a **fail** — it becomes invisible against a red-orange arena palette for a protanopic player."

**AFTER:** "A red-tinted floor area is a **fail** — the cue would be competing with the Vanguard's own red-orange warning language on the mesh directly in front of it, and hue alone cannot separate the two for a protanopic player. Use an outline, hatch, or edge. *(The Shattered Ring's own palette is not specified by the GDD — it is described functionally as an 'industrial' arena with a central floor and far doorway. Do not author against an assumed arena color.)*"

### F6b — an asserted absence

**RETRIEVED** (`combat-integration-plan.md` §3.2 row 8): "ordinary dodge grants no meter" — nothing about cues.

**BEFORE:** "Deliberately louder than an ordinary dodge, which gets **no** cue and **no** meter."

**AFTER:** "Deliberately louder than an ordinary dodge, which grants **no meter** (plan §3.2 row 8: 'ordinary dodge grants no meter'). Whether an ordinary dodge carries any cue at all is `OPEN — designer decides` — no source says it has none. The requirement here is only that the two are unmistakably distinguishable, because that contrast is what teaches the mechanic."
