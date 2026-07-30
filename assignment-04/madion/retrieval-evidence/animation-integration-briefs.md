# Retrieval Evidence — `animation-integration-briefs.md`

Copy only. Full generated output: `../outputs/animation-integration-briefs.md`.

---

## QUERY

> For each of Crimson Vanguard's four authored attacks A–D, what does an animator need to deliver and what does an implementer need to wire, so the montage drives the six-state Behavior Tree correctly, activates and deactivates hit detection at the authored windows, respects its tracking and travel limits, and restores a valid combat state on every exit path including interruption?

---

## SOURCES SELECTED — why each, and what it contributed

| Source | Why selected | What it contributed |
|---|---|---|
| `gdd/ascendant-impact-gdd-v0.4.md` | The four attacks and their readability requirements exist **only** here; every other document derives from it | the four-attack table (purpose + readability requirement per attack); all six state timing bands for both phases; the behavioral-intent paragraph; the runtime AI boundary |
| `build-sequence.md` | The only source with per-attack montage authoring detail — notify layout, per-attack readability implementation, and the struct field list | M2-13 Attack A notify layout and per-notify Begin/End behaviour; M4-01 per-attack detail for B/C/D; M4-02 `ANS_TrackingLock` logic; M2-03 `S_VanguardAttackDef` fields; M2-14 the counter interrupt chain |
| `combat-integration-plan.md` | Holds the BT task chain, the trace mechanism, the failsafe rule, and the asset fallback ladder | §5.2 rival chain with per-state ownership; §3.1 row 13 six-task convention and failsafe; row 16 trace sweep and already-hit set; §8.2 the 208 cm proxy ladder; §8.5 row-versus-montage drift; §8.7 Motion Warping is not the default |
| `cinematic-integration-inspection.md` | The restoration defects directly constrain how montages may be authored — three of the five touch notify-end behaviour | V3 (trace shutdown assumed on interrupt); V4 (montage cleanup unspecified); V5 (`State.CanCounter` clearing relies on the same assumption) |
| `assignment-04/shared/knowledge-base/core-canon.md` | Anthony's derived layer; the Vanguard's physical and material description in citable form | 6'10" height, "substantially broader armored mass", red armor over black structure, red-orange systems and warning lights, readability target |

---

## RETRIEVED TEXT → GENERATED OUTPUT, side by side

### Pair 1 — the four attacks

**RETRIEVED** (`gdd/ascendant-impact-gdd-v0.4.md` Page 5, "Four-attack course set"):
> "Authored attack A | Close-range committed gauntlet force | Distinct wind-up and punishable recovery"
> "Authored attack B | Committed forward-pressure sequence | Visible first beat and stable tracking limit"
> "Authored attack C | Armored reach and space control | Clear body direction and visible active range"
> "Authored attack D | Short propulsion-assisted approach | Thruster cue before movement; no hidden full-arena snap"

**GENERATED** (the four brief headings and their readability sections):
> "## Attack A — Close-range committed gauntlet force … **Readability requirement (GDD, non-negotiable)** — "Distinct wind-up and punishable recovery.""
>
> "## Attack B — Committed forward-pressure sequence … "Visible first beat and stable tracking limit." Two distinct obligations: The **first beat must be visible** … The **tracking limit must be stable** — once committed, B does not keep re-aiming at the player. That is what makes a sequence of beats dodgeable rather than homing."
>
> "## Attack C — Armored reach and space control … "Clear body direction and visible active range." Two obligations: **Body direction must be clear before the active frames** … **The active range must be visible**"
>
> "## Attack D — Short propulsion-assisted approach … "Thruster cue before movement; no hidden full-arena snap." Two obligations, and the second is a hard structural limit"

---

### Pair 2 — Attack A notify layout

**RETRIEVED** (`build-sequence.md` M2-13):
> "Lay out on the timeline (design-brief §5.1): `[ANS_Telegraph][ANS_ActiveHit][ANS_Recover]` with `ANS_CounterWindow` overlapping late telegraph / early active."
> "**`ANS_Telegraph`** — Begin: `Set Blackboard CurrentState = Telegraph`, `RequestVFX` warning lights (empty in Phase 1), set emissive **red-orange** telegraph color, broadcast `OnTelegraphStart(AttackID)`; End: clear color."
> "**`ANS_ActiveHit`** — reuse the M1-18 class (**same class, both fighters**)."
> "**`ANS_Recover`** — Begin: `CurrentState = Recover`, raise `IncomingDamageMultiplier` (**multiplier value OPEN — §14 Q27**)"
> "**`ANS_CounterWindow`** — Begin: `bCounterable = true`, broadcast `OnCounterWindowOpen`; End: `bCounterable = false`."

**GENERATED** (shared contract, notify layout):
> "```
> |<---- ANS_Telegraph ---->|<-- ANS_ActiveHit -->|<------ ANS_Recover ------>|
>               |<--- ANS_CounterWindow --->|
>               (overlaps late telegraph / early active)
> ```"
>
> "| `ANS_ActiveHit` | **activates hit detection** — begins sweeping previous-frame → current-frame socket on the `AttackTrace` channel; opens a per-window already-hit set | **deactivates hit detection** — ends the sweep; the already-hit set closes |"
>
> "`ANS_ActiveHit` is **one class shared by both fighters** (created at M1-18, reused here). Do not author a rival-specific variant."

---

### Pair 3 — B's multiple active windows

**RETRIEVED** (`build-sequence.md` M4-01):
> "**B** (committed forward-pressure sequence) — visible first beat; **multiple separate `ANS_ActiveHit` states**, one per beat, so each beat is individually dodgeable; `ANS_TrackingLock` at a fixed point (stable tracking limit)."

**GENERATED** (Attack B, hit detection):
> "On/off **per beat**. Each `ANS_ActiveHit` state opens and closes its **own** already-hit set — that is what makes each beat independently dodgeable and prevents one dodge from eating the whole sequence, or one beat from hitting twice.
>
> The gaps between beats are not decorative: they are the dodge opportunities. If the beats merge into one continuous trace, B becomes an unavoidable multi-hit and the readability requirement fails."

**GENERATED** (Attack B, state boundaries — a scope guard derived from the six-state lock):
> "Note that **all beats live inside `BTTask_ActiveAttack`** — the multi-beat structure is montage-side, not a second BT task. Do not add a task per beat; that would fork the state model the GDD fixes at six states."

---

### Pair 4 — C's tracking lock ordering

**RETRIEVED** (`build-sequence.md` M4-01):
> "**C** (armored reach / space control) — body direction locked before active by `ANS_TrackingLock`; active-range capsule visible via the debug toggle."

**RETRIEVED** (`build-sequence.md` M4-02):
> "**Logic:** turns off the rival's rotate-to-target (facing freeze) for its duration — the "stable tracking limit" for B and C, gated by `bLockTrackingAtActive` on the row."

**GENERATED** (Attack C, root motion / facing / tracking):
> "`bLockTrackingAtActive` = **true** — body direction is locked by `ANS_TrackingLock` **before** the active window opens (M4-01). This one *is* sourced: M4-01 names B and C as the tracking-lock attacks.
>
> The ordering matters. If the lock begins at the same instant as the active window, the direction is only readable *during* the hit, which fails the requirement. The lock must precede the active frames."

---

### Pair 5 — D's travel cap

**RETRIEVED** (`build-sequence.md` M4-01):
> "**D** (short propulsion-assisted approach) — thruster cue in `ANS_Telegraph`; root motion (or Motion Warping, **R5**) travel **hard-capped at `MaxTravelDistance`** — the cap is data, **no hidden full-arena snap**."

**RETRIEVED** (`combat-integration-plan.md` §8.7):
> "the design's own R5 fallback is already the default — **root-motion montages with a hard distance cap** plus a pre-attack `Move To` reposition; Motion Warping is only attempted if the schedule holds at the M2 review, and only on a disposable branch first."

**GENERATED** (Attack D):
> "**`MaxTravelDistance` (`OPEN — Q13`) is a hard cap.** The cap is data. Travel must be measured against it, not assumed to respect it: plan §8.5 names "a D-row travel exceeding `MaxTravelDistance`" as a specific drift risk"
>
> "**Motion Warping is NOT the default.** Plan §8.7: the default is "root-motion montages with a hard distance cap plus a pre-attack `Move To` reposition." Motion Warping is R5 — optional, schedule-dependent, disposable-branch-first, and requires designer approval since it is external code. **Author for root motion.**"
>
> "2. **Measure actual travel distance across at least twenty runs from varied starting gaps.** No run exceeds `MaxTravelDistance`. This is the single check the design repeats three times."

---

### Pair 6 — the one legal interrupt

**RETRIEVED** (`build-sequence.md` M2-14):
> "`BP_VanguardCombatComponent → OnCountered` → `Montage Stop` the attack montage → set `bCounteredThisAttack = true` → the running task's `On Montage Ended` fires → task calls `Finish Execute (Success)` → the `Sequence` advances → `BTTask_Recover` reads `bCounteredThisAttack` and plays `AM_Vanguard_CounterReact`."

**RETRIEVED** (`combat-integration-plan.md` §3.1 row 13):
> "no `Abort Self`, no `Simple Parallel` aborts, no `Stop Logic`"

**GENERATED** (shared contract, interruption):
> "**The counter is the only legal mid-attack interrupt.** It must route *through* the `Sequence`, never via `Abort Self`, `Simple Parallel` aborts, or `Stop Logic` — plan §3.1 row 13 forbids all three, and §3.1 row 9 calls routing through the sequence the "deadlock defense.""
>
> "**Every attack montage must be safely stoppable at any frame.** A counter can land during late telegraph or early active — wherever `ANS_CounterWindow` is open."

---

### Pair 7 — the proxy asset ladder

**RETRIEVED** (`combat-integration-plan.md` §8.2):
> "**Fallback (ladder, cheapest first):** UE5 Mannequins on the native skeleton for both fighters (zero retargeting); Vanguard = Mannequin scaled to 208 cm + static-mesh gauntlet/shoulder proxy blocks + red/black material — ships no matter what; the Paragon heavy swap only if the schedule holds and **before** M4 range tuning."

**GENERATED** (required assets table + the scale note):
> "| Vanguard mesh | UE5 Mannequin **scaled to 208 cm** + static-mesh gauntlet/shoulder proxy blocks + red/black material | Paragon heavy swap — `OPEN — Q30`, and only **before** M4 range tuning |"
>
> "**Scale is load-bearing, not cosmetic.** The Vanguard is **6'10"** with a "substantially broader armored mass." A late mesh swap "invalidates sockets, capsule, and every range value" (plan §8.2), and every `MinRange`/`MaxRange` re-tunes twice. Q30 must be answered before M4 range tuning or the range work is done twice."

---

### Pair 8 — the restoration caveat

**RETRIEVED** (`cinematic-integration-inspection.md` §2, V3/V4/V5):
> "Trace shutdown therefore relies on `Received Notify End` firing when a montage is stopped or interrupted. That is plausible engine behavior, but it is **assumed, not specified, and not on any gate checklist**."
> "explicit `Montage Stop` exists only on the Clash **failure** path (step 1)."
> "`State.CanCounter` clearing relies on the rival's `ANS_CounterWindow` notify-end firing when its montage is stopped — the same assumed behavior as V3."

**GENERATED** (shared contract, restoration — blockquote caveat):
> "> **Caveat carried from `cinematic-integration-inspection.md` — five open defects touch this.** `RestoreCombatState()` as specified does **not** restore camera ownership (V2), does **not** terminate active hit traces or clear the already-hit set (V3), does **not** specify montage/animation cleanup on interruption paths (V4), and omits `State.Dodging` and `State.CanCounter` from its clear list (V5) … Anyone authoring these montages before that happens should assume the restore contract is still incomplete and not design around it."
>
> "**Authoring implication:** never rely on a notify firing to clear state that matters. Anything that must be true at Return to Neutral is cleared by `BTTask_ReturnToNeutral` regardless of how the montage ended."

---

## POST-CRITIC CORRECTIONS APPLIED TO THIS OUTPUT

Findings F1, F2, F3, F4 in `../critic-evidence/critic-report.md`. All four are the same class: inference stated as sourced fact.

### F1 — Attack A recover ranking

**RETRIEVED** (`build-sequence.md` M2-13):
> "Attack A = longest recover window **on the montage**"

**BEFORE:** "| Recover | 0.45–0.90 s | 0.35–0.75 s | **longest of the four** — the deliberate punish opening |"

**AFTER:** "| Recover | 0.45–0.90 s | 0.35–0.75 s | **the longest of the three windows on A's own montage** (M2-13) — the deliberate punish opening |"

### F2 — Attack C range band

**RETRIEVED** (`gdd` Page 5): "Authored attack C | Armored reach and space control | Clear body direction and visible active range" — no band, no ranking.

**BEFORE:** "Range band `OPEN — Q10`, the longest of the four."

**AFTER:** "Range band `OPEN — Q10`. The GDD gives C 'armored reach and space control' but **does not rank the four range bands against each other**; do not assume C holds the longest band until Q10 is set."

### F3 — Attack B range band and travel

**RETRIEVED** (`gdd` Page 5 + `build-sequence.md` M4-01) — neither states a band, a distance, or root-motion travel for B.

**BEFORE:** "a multi-beat advance that pressures the player across a short distance. Range band `OPEN — Q10`, mid band." / "Root motion: **forward travel across the beats** — this is 'forward-pressure.' Authored as root motion."

**AFTER:** "a multi-beat advance that pressures the player. Range band `OPEN — Q10`; the GDD does not state B's band or rank it against the others." / "Root motion: **forward travel across the beats is inferred from the GDD's 'forward-pressure' purpose, not specified upstream.** No source states that B travels, how far, or by what means."

### F4 — `bUsesPropulsion` for A, B, C

**RETRIEVED** (`build-sequence.md` M2-03): "`bUsesPropulsion` (bool)" — field listed, no per-attack value assigned.

**BEFORE:** "`bUsesPropulsion` = **false**." (three places)

**AFTER:** "`bUsesPropulsion` — expected **false**, `MaxTravelDistance` unused. *Derivation, not a quoted value:* the GDD attributes propulsion to **D only** ('Short propulsion-assisted approach'), so A/B/C read as non-propulsion. The row values themselves are the designer's to set." (and the shorter cross-references on B and C)
