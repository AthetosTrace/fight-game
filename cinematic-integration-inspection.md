# Cinematic Integration Inspection — Ascendant Impact

**Produced by:** cinematic-integration-inspector agent (runs last in the specialist extension)
**Audited artifacts:** `framework-evaluation.md` · `combat-integration-plan.md`
**Reference inputs:** `project-brief.md` · `design-brief.md` · `build-sequence.md` · `inspection.md` · `gdd/ascendant-impact-gdd-v0.4.md` · `CLAUDE.md`
**Date:** 2026-07-27 · **Ship date:** 2026-09-01 (**36 days remaining**)

Sources of truth: the GDD (v0.4) and the approved project brief. This inspection verifies both technical alignment and game-design alignment against the defining experience:

> Real-time martial-arts combat rewards player skill with brief, earned anime-style cinematic spectacle.

This inspection identifies violations, gaps, unsupported claims, and required corrections. It does not redesign the game and does not repair the audited artifacts.

---

## 1. Overall verdict

### `APPROVED WITH REQUIRED CHANGES`

The recommended foundation (Blueprint-first custom architecture) is sound, evidence-backed, human-approved, and preserves the defining experience. Nine of the ten hard checks pass cleanly. Hard check 7 (cinematic handoff safety) does **not** pass cleanly: several restoration steps are **assumed rather than specified**, and one ownership transition (the rival's AI during the 1–3 s Impact burst) has no documented suspension mechanism at all. These are specification defects in the audited plan, not foundation defects. They must be corrected before M3 (Impact handoff) is implemented; they do not block the approved first test, M1, or M2.

---

## 2. Violations

Hard-check results: checks 1, 2, 3, 4, 5, 6, 8, 9, 10 — **PASS** (detail in §3–§6). Check 7 — **VIOLATIONS FOUND**, listed first, then the pass summaries.

### V1 — Rival AI ownership during the Impact burst is assumed, not specified

- **Rule:** Hard check 7 — cinematic handoff safety requires explicit restoration (and therefore explicit suspension) of AI logic for **every** cinematic branch.
- **Offending section:** `combat-integration-plan.md` §3.1 rows 19 and 27; §5.1 steps 7–8 (inherited from `design-brief.md` §7.4/§7.5).
- **Evidence:** the only documented mechanism that parks `BT_CrimsonVanguard` is the `bInClash` Blackboard bool → `BTTask_WaitIndefinite` branch, which applies to the **Final Clash only**. The Impact success branch plays "a montage pair on both fighters" for the GDD's 1–3 seconds, and row 19's acceptance condition says "after either branch … the rival BT is running" — implying it was somehow not running during the burst — but **no mechanism suspends the six-state Attack Cycle during the burst**. As specified, `BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst, fight the rival's stagger montage for the montage slot, and either desync the debug state display or strand the burst.
- **Required correction:** see correction 1 (§8). Specify the rival-side ownership transition for the Impact burst explicitly (e.g., a park flag analogous to `bInClash`, or a documented rule that the burst may only play during a state that cannot start a new attack), with its release routed through `RestoreCombatState()`.
- **Blocks implementation:** blocks **M3** implementation sign-off. Does not block the sandbox test, M1, or M2.

### V2 — Camera ownership is not restored by the single restore function

- **Rule:** Hard check 7 — explicit restoration of camera ownership on every cinematic branch.
- **Offending section:** `combat-integration-plan.md` §3.1 row 27 (the `RestoreCombatState()` contents list) versus §2 principle 4 and the §10 acceptance checklist; `design-brief.md` §7.5 pseudocode upstream.
- **Evidence:** the specified `RestoreCombatState()` body restores input, collision, locomotion, tags, lock-on, time dilation, rival BT, and the prompt widget — **it contains no camera-return step.** Camera return is specified only piecemeal: Clash failure step 1 ("camera back") and §8.4's routing of `LS_FinalClash` `OnStop`/`OnFinished` into restore. Meanwhile plan §2 principle 4 and the §10 checklist claim `RestoreCombatState()` "explicitly restores … camera/time dilation" — the claim **overstates the specified function**. The Clash-success path's camera return before the Win screen rests entirely on the assumed Level Sequence finish behavior.
- **Required correction:** correction 2 (§8). Add an explicit camera-ownership restoration step (e.g., `Set View Target with Blend` back to the player's spring-arm camera) inside the single restore function so all branches inherit it, and align the §2/§10 claims with the actual spec.
- **Blocks implementation:** blocks **M3/M4** sign-off of the restore function. Does not block M1/M2.

### V3 — Hitbox/trace shutdown on restoration is assumed engine behavior

- **Rule:** Hard check 7 — explicit restoration of hitboxes.
- **Offending section:** `combat-integration-plan.md` §3.1 row 27; `design-brief.md` §7.5.
- **Evidence:** `RestoreCombatState()` never disables active attack traces or clears the per-window already-hit set. The Impact Window's most common trigger — a perfect dodge — fires **while the rival's `ANS_ActiveHit` window is open**. Trace shutdown therefore relies on `Received Notify End` firing when a montage is stopped or interrupted. That is plausible engine behavior, but it is **assumed, not specified, and not on any gate checklist**. A trace left live across the handoff produces phantom hits during or after a cinematic — a direct wound to the central promise.
- **Required correction:** correction 3 (§8). Either add an explicit "terminate all active hit traces / clear hit sets" step to restore, or specify the notify-end-on-interrupt guarantee as a tested assumption with a case on the M3-GATE checklist.
- **Blocks implementation:** blocks **M3** sign-off.

### V4 — Animation-state cleanup and the death-during-burst edge are unspecified

- **Rule:** Hard check 7 — explicit restoration of animation state; hard check 6 — no unintended punishment.
- **Offending section:** `combat-integration-plan.md` §3.1 rows 19, 22, 27; `design-brief.md` §7.5, §9.3.
- **Evidence:** explicit `Montage Stop` exists only on the Clash **failure** path (step 1). The Impact success branch assumes the burst montage pair ends naturally before restore — unstated for interruption paths. `RequestImpactWindow` refuses when "either fighter is dead," but nothing specifies what happens if the player's health reaches zero **during** a burst or Clash beat (rival damage during overlays is presumably impossible, but that presumption is also unstated). An `OnDeath` firing mid-overlay races `EndDuel(Loss)` against `RestoreCombatState()`.
- **Required correction:** correction 4 (§8). Specify montage/animation cleanup in restore (or the completion-before-restore rule per branch) and define the mid-overlay death rule.
- **Blocks implementation:** blocks **M3/M4** sign-off.

### V5 — Two transient tags are omitted from the restore clear list

- **Rule:** Hard check 7 — explicit restoration of combat state.
- **Offending section:** `combat-integration-plan.md` §3.1 row 27 (clear list: `State.Attacking/.Invulnerable/.PerfectWindow/.InImpactWindow/.Clashing`).
- **Evidence:** the registered tag set (plan §4 tag table) also contains `State.Dodging` and `State.CanCounter`. Neither is in the restore clear list. `State.CanCounter` clearing relies on the rival's `ANS_CounterWindow` notify-end firing when its montage is stopped — the same assumed behavior as V3. A stale `State.CanCounter` after a handoff yields a free counter, i.e., unearned spectacle.
- **Required correction:** correction 5 (§8). Add both tags to the clear list or document precisely why each is guaranteed clear by construction.
- **Blocks implementation:** blocks **M3** sign-off. Low effort to fix.

**No other hard violations found.** In particular: no scope expansion, no runtime AI-model calls, no marketing treated as fact, no unverified 5.8 claim accepted, the C++ scaffold correctly declared `NOT EVALUABLE — code not supplied` (the repo verifiably contains zero source files), one shared Echo/Nova framework, the six-state deterministic flow intact, all governed numbers verbatim, milestone order intact, and a genuinely reversible first test.

---

## 3. Framework-evaluation audit

| Dimension | Finding |
|---|---|
| **Candidate completeness** | PASS. Five candidates: approved Blueprint-first, n00dFighter/NFTiny, TRUE FGE, existing C++ scaffold, minimal hybrid. The realistic field for a UE 5.8 one-vs-one boss duel is covered; no plausible major candidate (e.g., GAS-based build) is missing — GAS was already ruled out with reasoning in `design-brief.md` §3, which the evaluation correctly treats as settled rather than re-litigating. |
| **Evidence quality** | PASS with one note. The §6 ledger separates **verified** / **seller-stated** / **inferred (low trust)** / **unknown** correctly. Marketing copy is load-bearing *only* for rejection ("even taken at face value, the templates do not fit") — the correct direction of inference. UE 5.8 compatibility for both templates is honestly marked **unknown**; TrueFGE's "5.0–5.7" is correctly downgraded to third-party inference. E11 (zero source files) is verified and the C++ candidate is scored as *absence*, explicitly not as code quality. **Note (non-blocking):** E12 (Behavior Tree supported in 5.8) cites the design brief's own prior research — an internal, second-hand citation. Acceptable because the claim is low-risk and stock-engine, but it is the one ledger row not independently sourced by this agent. |
| **Score consistency** | PASS with one quibble. The 94/47/46/20/94 totals follow from the row scores; the notes explain every 4 on the BP column (real R1–R7 execution risk) rather than inflating to 5. Quibble: NF/TF criterion 14 (licensing/submission safety) at 4 is generous for unpurchased, unaudited paid products — but since both are rejected on five independent hard conditions, the quibble cannot change the ordering. CPP's uniform 1s are explicitly labeled as describing nonexistence — honest. |
| **Rejection logic** | PASS. Each rejection names its hard conditions: unverified 5.8 support, versus/multiplayer architecture against a no-PvP scope lock, more integration work than the approved plan, paid against a $0 budget, unverifiable core claims. The hybrid is correctly collapsed into the recommendation rather than kept as a vague third path. |
| **Recommendation traceability** | PASS. The recommendation is the already-inspected plan of record; every claimed strength traces to `design-brief.md` sections and `inspection.md`'s zero-violation result. No seller demo, rating, or video is treated as proof of fit anywhere. |
| **Human-approval status** | PASS. The evaluation explicitly withheld authority ("The human designer must approve this recommendation before any implementation begins"). The approval record — *"APPROVED — use the Blueprint-first custom architecture recommended by framework-evaluation.md"* (2026-07-27) — is quoted in `combat-integration-plan.md` §1.2 and `leave-offs/combat-integration-architect.md`. The chain evaluated → surfaced → human approved → then planned is intact and in the right order. |

---

## 4. Integration-plan audit

All 28 systems in `combat-integration-plan.md` §3.1/§3.2 were checked against the GDD, project brief, design brief, and build sequence. Verdict per system:

| # | System | Verdict | Source decision it maps to |
|---|---|---|---|
| 1 | Third-person movement | TRACES | design-brief §1.2/M1-01; R2 (standard AnimBP, not Motion Matching) |
| 2 | Camera and lock-on | TRACES | design-brief §4.4; GDD side-on readability |
| 3 | Character selection | TRACES | GDD simplified-screen allowance; design-brief §10.1 |
| 4 | Shared Echo/Nova fighter data | TRACES | GDD SHARED PLAYER-KIT SCOPE RULE; design-brief §4.1–§4.2; color direction preserved (cyan-white ≠ costume recolor) |
| 5 | Light attack sequence | TRACES | design-brief §4.5; +5 at `AN_ComboFinisher` only |
| 6 | Input buffering | TRACES | design-brief §7.3 prohibition 2; the two opposing buffer policies are correctly kept separate (risk §8.3) |
| 7 | Dodge | TRACES | design-brief §4.6 |
| 8 | Perfect dodge | TRACES | design-brief §4.6 — detection in the damage trace, one code path |
| 9 | Counter | TRACES | design-brief §4.7/§6.5 — the one legal interrupt, routed through the sequence |
| 10 | Player health | TRACES | design-brief §4.8 |
| 11 | Rival health | TRACES | design-brief §4.8; 1 HP floor via `MinHealthFloor`; 50%/≤25% reads |
| 12 | Vanguard controller | TRACES | design-brief §6.1; no AI Perception |
| 13 | Six-state rival flow | TRACES | GDD §04 state flow, verbatim order; guaranteed-exit failsafes = the M2 gate implemented |
| 14 | Four data-driven attacks | TRACES | GDD four-attack set; design-brief §5.3 one data path; D capped — no hidden full-arena snap |
| 15 | Telegraph/Active/Recover windows | TRACES | GDD state timings verbatim; Active 0.18–0.45 s deliberately unscaled across phases |
| 16 | Hit detection/reaction | TRACES | design-brief §5.2; one `ANS_ActiveHit` class for both fighters |
| 17 | Ascension Meter | TRACES | GDD §03 verbatim (+5/+12/+15/+20/+0, 0–100, no time gain); one write path + one sanctioned exception |
| 18 | Impact Window trigger | TRACES | GDD §02 verbatim (0.75 s first, 0.35–0.50 s standard); onboarding prohibitions carried |
| 19 | Impact success/failure branches | **GAP** | Branch outcomes and numbers trace (GDD 1–3 s burst, no-punishment failure), but the rival-AI suspension during the burst is unspecified — **V1** — and mid-burst death is undefined — **V4** |
| 20 | Phase 2 at 50% | TRACES | GDD REVISED — PHASE 2: commit on Return to Neutral, signaled once, same four attacks |
| 21 | Final Clash eligibility gate | TRACES | GDD SINGLE GATE: meter 100 **AND** health ≤25%; player-initiated only |
| 22 | Final Clash success | TRACES | GDD both beats → finisher → Win; camera return partially assumed — see **V2** |
| 23 | Final Clash failure recovery | TRACES | GDD verbatim: 1 HP floor, meter 50, 3 s cooldown, return to neutral, no restart, no player death |
| 24 | Win and loss handling | TRACES | GDD encounter flow; sole loss condition is player health zero; no invented timer |
| 25 | Debug-state visibility | TRACES | GDD implementation safeguard (visible debug state names) |
| 26 | Presentation kill-switch | TRACES | GDD safeguard (separate gameplay timing from presentation) |
| 27 | Clean return to gameplay | **GAP** | The single-function design traces to the GDD's explicit-restore safeguard, but the function's specified contents omit camera ownership (**V2**), hitbox shutdown (**V3**), animation cleanup (**V4**), and two tags (**V5**); plan §2/§10 claims exceed the spec |
| 28 | Save/test/version-control boundaries | TRACES | plan-level discipline consistent with CLAUDE.md's MCP prerequisite and the reversibility principle |

**No system is UNSUPPORTED** — every claim rests on the approved documents or verified stock-UE capability, and plan §1.4 honestly tables its unverified assumptions instead of asserting them. **No system is OUT OF SCOPE** — nothing deferred (PvP, extra fighters/arenas/attacks, playable Vanguard, progression, per-fighter move sets, signature cinematics) received integration work; `BTTask_WaitIndefinite` is a parking task, not a seventh combat state; `L_CharacterSelect` is a menu level, not a second arena; the proposed burst-montage names are cosmetic and left `OPEN`.

---

## 5. Cinematic handoff audit

Walking the full handoff as specified, with every ownership transition. Legend: **P** = player/input, **C** = camera, **T** = time, **A** = animation, **X** = collision, **AI** = rival logic, **U** = UI.

1. **Qualifying gameplay event.** Perfect dodge (rival's `ANS_ActiveHit` trace lands during `State.PerfectWindow`), counter (`IA_Counter` inside `ANS_CounterWindow`), or combo milestone (`AN_ComboFinisher`). All three are earned real-time events; the trigger set is closed and matches the GDD. Ownership: everything remains gameplay-owned. **Sound.**
2. **Prompt opening.** `RequestImpactWindow` → refusal checks (window open / cooldown / `bInClash` / death) → `OpenWindow(0.75 s or 0.35–0.50 s)` → `WBP_ImpactPrompt` shown, timer set. **U** transitions to the director. **Unspecified:** what, if anything, is suspended while the window is open — the plan specifies restoration (row 27) but never the corresponding suspension for this phase. In Phase 1, presentation is empty, so presumably nothing is suspended and combat continues under the prompt; that presumption should be written down (folded into correction 1's acceptance).
3. **Player success or failure.** `IA_Impact` while open → SUCCESS; expiry → FAILURE; a pre-open press is discarded, never queued. No auto-success path exists. **Sound** — this is the onboarding rule implemented, not hoped for.
4. **Cinematic start (success only).** +20 meter; burst montage pair plays on both fighters. **A** transitions to the burst montages; **C**/**T** transitions are wrappers into `BP_PresentationSubsystem` (empty in Phase 1 — camera and time never actually leave gameplay ownership until M5 fills them, which is a virtue). **AI: VIOLATION V1 — no specified mechanism takes ownership of the rival's Behavior Tree for the 1–3 s burst.** **X**: never explicitly transferred — acceptable only if traces are guaranteed dead (V3).
5. **Hit or consequence.** The rival half of the pair is a stagger/knockback beat (vertical slice, plan §7). Damage numbers during the burst: none specified, none granted — consistent with the meter table. Mid-burst player death: **undefined (V4)**.
6. **Cinematic end.** Burst montages end naturally (success) or never started (failure). Clash paths: `LS_FinalClash` `OnFinished`/`OnStop` both route to restore (§8.4) — specified for the sequence, **assumed for camera blend-back (V2)**.
7. **Restoration.** `RestoreCombatState()` — one function, all branches, five call sites. Explicitly specified: **P** (enable input), **X** (capsules Query+Physics), locomotion (Walking mode both), combat state (five tags), lock-on, **T** (dilation → 1.0 via subsystem), **AI** (`bInClash=false`, `CurrentState=Idle_Reposition`, BT resumes), **U** (prompt hidden). **Assumed rather than specified: C (V2), hitboxes (V3), A (V4), `State.Dodging`/`State.CanCounter` (V5).** The single-function pattern is exactly right — which is why the omissions matter: fixing the spec fixes every branch at once.
8. **Return to gameplay.** Rival Attack Cycle resumes at `Idle_Reposition` with visible state names; failure returns immediately with no punishment, no meter, cooldown started — control return on a failed standard window is immediate as required.

**Conclusion:** the handoff architecture (earned trigger → closed trigger set → one director → one restore function → severable presentation) is the correct shape and preserves the control model. The five violations are all in the same place — the ownership ledger of the restore/suspend contract — and are correctable on paper before M3.

---

## 6. Vertical-slice readiness

Two proofs are proposed; both are judged **ready and genuinely reversible**.

**Proof A — the narrow first test** (framework-evaluation §8): one buffered light-attack chain in a disposable UE 5.8 Third Person project on a throwaway branch/project.
- **Required assets:** one montage with sections `Light_01`/`Light_02`, one `ANS_ComboLink`, one `IA_LightAttack` + mapping context. Nothing else.
- **Required systems:** stock UE 5.8 only.
- **Expected output:** an observed PIE result recorded pass/fail.
- **Pass:** press inside the window chains; no press ends cleanly; press before the window is **discarded**.
- **Fail:** any of the three misbehaves, or the 5.8 template lacks an assumed piece → finding goes to the designer before M1.
- **Rollback:** delete the sandbox project/branch; the main build is never touched. **This test correctly exercises the single mechanism reused by the combo, the Impact prompt discard rule, and the Clash beats** — the highest-leverage narrow capability. It is a real reversible test, not a disguised build start.

**Proof B — the vertical slice** (plan §7, at M3-GATE): Echo proxy vs. the six-state rival on Attack A — telegraph → perfect dodge (+12) → First Impact Window (0.75 s, player-pressed) → 1–3 s burst with rival stagger → `RestoreCombatState()` → live combat at meter 32, plus the failure fork (expired prompt → clean immediate return).
- **Required assets/systems:** exactly the M1–M3 output; no extra content — the slice "falls out" of the build, matching the GDD's PRESERVED gray-box milestone element for element.
- **Pass:** all eight beats in one unbroken PIE run with state names visible, plus the failure fork; **fail:** any stranded state, any auto-success, any timing change when presentation is toggled off.
- **Rollback:** the M2-GATE commit.
- **Caveat:** Proof B currently inherits V1–V5 — the slice's "clean return" beat cannot be honestly judged until the restore/suspend spec is corrected. The slice definition itself needs no change.

The plan does **not** begin by building the entire game: sandbox test → M1 → M2 → slice at M3 → M4, with gates, commits, fallbacks (§8.1–§8.8), and designer decisions at each step. Buildability check: PASS.

---

## 7. Risk ranking

| Rank | Risk | Severity | Probability | Impact | Earliest test | Fallback |
|---|---|---|---|---|---|---|
| 1 | **Schedule compression (R7/§8.8)** — 36 days; M4 must complete ~20 Aug to leave tuning time; the Unreal build phase has not started | **Critical** | High | Every provisional number ships untested; or the duel is incomplete on 1 Sept | The M1 gate date against its internal target — the first slip is the signal | The cut order is law: cuts come from asset fidelity (Mannequin proxies, cut-less Clash camera, silent build) never from M1–M4 systems |
| 2 | **Cinematic handoff restoration gaps (V1–V5)** — a stranded state or phantom hit at the heart of the central promise | **High** | Medium (each individually likely to surface in edge cases) | M3 gate failure; the defining experience breaks exactly where it is supposed to shine | Paper correction now; then interrupt-heavy cases added to the M3-GATE checklist (counter-triggered window mid-active-hit; death during burst; presentation-off toggle mid-burst) | The single-restore-function design itself — one spec fix repairs all branches; cut-less Clash camera (§8.4) removes the hardest camera transition |
| 3 | **Crimson Vanguard proxy + animation retargeting (R1/R4/§8.2)** — no verified free asset for a 6'10" armored rival; a late swap invalidates sockets, capsule, ranges | **High** | Medium-high | Weeks of retarget time, or double range-tuning if a swap lands after M4 tuning | Retarget one Mixamo/Paragon clip on a disposable branch during M1; sockets checked on the candidate skeleton | The ladder: scaled Mannequin (208 cm) + proxy gauntlet blocks + red/black material ships no matter what; Paragon swap only before M4 range tuning (Q30) |
| 4 | **Unreal MCP instability (§8.6)** — the build conduit is untested; CLAUDE.md names it a prerequisite | **Medium** | Medium | Stalled build or lost sessions; schedule bleed if large parts go manual | The first M1 session's asset-create/save round trip | Small sessions with save+commit boundaries; the build sequence already names exact editor paths for manual execution |
| 5 | **Late designer answers on OPEN values** — 29+ Q-values plus Q22 (1 HP floor permanent vs. Clash-only), which changes what the endgame is | **Medium** | Medium | Milestones stall or gates are signed against placeholder-neutral defaults; Q22 late = M4-08 rework | Batch Q22, Q10/Q24/Q25 at the M2 gate as the plan already requests | Designer-exposed variables at neutral defaults keep the build moving; but tuning debt lands on the ~10 post-M4 days |

(Ranked by expected schedule-adjusted damage; V1–V5 outrank the asset gap because the asset gap has a guaranteed-ship fallback while a stranded cinematic state fails the M3 gate outright.)

---

## 8. Required corrections

Corrections name what must change; this inspector does not rewrite the artifacts.

1. **Artifact:** `combat-integration-plan.md` — **Section:** §3.1 row 19 (and the §5.1 chain step 7). **Issue (V1):** no specified mechanism suspends `BT_CrimsonVanguard` during the 1–3 s Impact burst; only `bInClash` parking exists, and it is Clash-only. **Acceptance:** the plan names an explicit rival-ownership mechanism for the burst (park flag, or a documented can't-attack-state rule), states what is suspended when a window opens (including "nothing," if so decided), and routes its release through `RestoreCombatState()`; the mechanism appears in the M3-GATE checklist.
2. **Artifact:** `combat-integration-plan.md` — **Section:** §3.1 row 27, §2 principle 4, §10 checklist (upstream note: `design-brief.md` §7.5 has the same omission — surface to the designer, do not silently edit). **Issue (V2):** `RestoreCombatState()` spec contains no camera-ownership restoration step, yet §2/§10 claim it does. **Acceptance:** an explicit camera-return step is added to the single restore function's contents, and the §2/§10 claims match the spec exactly.
3. **Artifact:** `combat-integration-plan.md` — **Section:** §3.1 row 27 and risk §8.4. **Issue (V3):** hitbox/trace shutdown on restoration relies on assumed notify-end-on-interrupt behavior. **Acceptance:** either an explicit trace-termination/hit-set-clear step in restore, or the assumption is named, tested in the sandbox or an M2 case, and added to the M3-GATE checklist ("no trace survives a handoff").
4. **Artifact:** `combat-integration-plan.md` — **Section:** §3.1 rows 19/22/27. **Issue (V4):** animation-state cleanup is specified only on Clash failure; mid-overlay player death is undefined. **Acceptance:** each overlay branch states its montage-cleanup rule (natural completion vs. explicit stop), and a single stated rule resolves `OnDeath` during any overlay (surfaced to the designer if it needs a design decision).
5. **Artifact:** `combat-integration-plan.md` — **Section:** §3.1 row 27 clear list. **Issue (V5):** `State.Dodging` and `State.CanCounter` are registered transient tags absent from the restore clear list. **Acceptance:** both are added to the clear list, or a per-tag guarantee-of-clearance is documented.
6. **Artifact:** `framework-evaluation.md` — **Section:** §6 ledger row E12. **Issue (non-blocking):** the Behavior-Tree-in-5.8 claim is internally cited (design-brief research) rather than independently sourced in this ledger. **Acceptance:** either an independent primary source is added, or the row is annotated as inherited-internal — no other change; the recommendation does not hinge on it.

Corrections 1–5 must be accepted by the human designer before **M3** implementation is signed off. None blocks the sandbox test, M1, or M2.

---

## 9. Human approval items

Unresolved decisions, consolidated across both audited artifacts:

1. Accept or amend corrections 1–5 above (they touch the restore contract the GDD safeguard owns) — `OPEN — designer decides`
2. Run the sandbox combo-buffer test, and on which machine/branch — `OPEN — designer decides`
3. Any purchase, plugin adoption (including Motion Warping), or external code entering the course build — `OPEN — designer decides` (both plans assume none)
4. Licensing/rights acceptance for every free asset at claim time (Mannequins, Mixamo, Fab, Paragon) — `OPEN — designer decides`
5. Manual-execution fallback policy if the Unreal MCP fails — `OPEN — designer decides`
6. Acceptance of a cut-less Phase 1 Final Clash camera if the Level Sequence handoff proves fragile — `OPEN — designer decides`
7. **Q22 — whether the 1 HP floor is permanent from first eligibility or Clash-attempt-only** (the most consequential open value; needed before M4-08 is final) — `OPEN — designer decides`
8. The full design-brief §14 tuning set: Q1–Q4 health/damage economy; Q5–Q8, Q28 combo/dodge/counter windows; Q9 meter decay (none recommended); Q10–Q13, Q18, Q24–Q27 ranges, cooldowns, travel cap, footprint, failsafe margin, recover multiplier, window cooldown; Q17, Q19–Q21 Clash input binding, post-counter window, beat widths, separation distance; Q23 duel timer (none recommended) — `OPEN — designer decides`
9. Q14–Q16 Echo/Nova differentiation scalars, including whether they differ at all in Phase 1 — `OPEN — designer decides`
10. Q29 Crimson Vanguard short in-combat UI label (GDD lists it unfinalized; HUD field blank) · Q30 Paragon heavy swap and its deadline (before M4 range tuning) · Q31 whether Phase 1 ships silent — `OPEN — designer decides`
11. Burst montage pair names (cosmetic) — `OPEN — designer decides`
12. Mid-overlay death rule, if correction 4 surfaces it as a design question rather than a spec omission — `OPEN — designer decides`

---

## 10. Final recommendation

- **May implementation begin?** **Yes, conditionally.** The sandbox test, M1, and M2 may proceed on the approved foundation now. **M3 implementation may not be signed off until corrections 1–5 are accepted by the human designer** — they sit exactly on the real-time-to-cinematic handoff this game exists to prove.
- **Approved foundation:** `USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE` — as recommended by `framework-evaluation.md`, approved by the designer of record on 2026-07-27, and mapped by `combat-integration-plan.md`. This inspection confirms the recommendation is evidence-supported, scope-safe, and preserves the defining experience.
- **Approved first test:** the framework-evaluation §8 sandbox test — one buffered light-attack chain in a disposable UE 5.8 project/branch, three pass conditions, delete-on-completion. Narrow, reversible, and load-bearing for M1, M3, and the Clash beats alike.
- **Conditions before full implementation:** (1) designer acceptance of corrections 1–5 before M3; (2) Unreal MCP established per CLAUDE.md before the developer runs; (3) rights review per asset at claim time; (4) Q22 answered before M4-08 is finalized; (5) every provisional number remains the human designer's — no agent resolves one.
- **Does the six-agent submission accurately demonstrate collaboration?** **Yes.** All six artifacts exist on disk and form two real dependency chains: the core crew (designer → developer → inspector producing `design-brief.md` → `build-sequence.md` → `inspection.md`, each consuming the previous output) and the extension (framework-evaluator → combat-integration-architect → cinematic-integration-inspector producing `framework-evaluation.md` → `combat-integration-plan.md` → this document). Each downstream artifact quotes, gate-checks, and depends on its upstream — including this one, which found real defects rather than rubber-stamping, which is what independent review in a pipeline is for.

---

## Role-clarity check for Assignment 3

The three-agent extension is a **real dependency chain**, verified against the artifacts on disk:

- **Unique roles:** the framework-evaluator decides *what to build on* (candidate comparison, evidence ledger, recommendation); the combat-integration-architect decides *how every required system lands on it* (28-system matrix, architecture map, data flows, milestone contracts, risks); the cinematic-integration-inspector independently verifies *that the result still is Ascendant Impact* (ten hard checks, handoff audit, required corrections). No role overlaps another's output.
- **Defined inputs/outputs:** each agent names its consumed artifacts in its header and produces exactly one named artifact plus a leave-off; each downstream header performs a gate check on its upstream (the plan quotes the evaluation's verdict and the human approval record verbatim; this inspection audits both).
- **Removing any one agent breaks the pipeline:** without the evaluator there is no recommendation for the designer to approve and §1 of the plan has no input; without the architect there is no integration plan for this inspector to audit (`BLOCKED — required upstream artifact is missing`); without this inspector the plan's restore-contract gaps (V1–V5) would have reached implementation unchallenged.
- **Outputs are specific to Ascendant Impact:** every artifact turns on this game's actual systems and numbers — `DT_VanguardAttacks`' four rows, the 0.75 s first Impact Window, the meter-100-AND-≤25% Clash gate, the 1 HP floor, `RestoreCombatState()` — none of it is transplantable boilerplate, and none of it mentions any other project.
- **Diagram/README accuracy:** the extension can be accurately described as a strictly ordered chain `framework-evaluator → combat-integration-architect → cinematic-integration-inspector` appended after the core inspector's gate; the Mermaid diagram and README should show it exactly that way (per CLAUDE.md's hard rule, both diagrams must be updated together when the extension is drawn in).

**Rubric note for the Assignment 3 README:** Tony's extension adds three specialists that run strictly after the core designer → developer → inspector crew and form their own gated chain: the *framework-evaluator* researches and scores five candidate combat foundations for Ascendant Impact against a 20-criterion matrix and an evidence ledger, recommending the Blueprint-first custom architecture with every unverifiable seller claim marked as such; the *combat-integration-architect*, running only after that recommendation received the human designer's recorded approval, maps all 28 required duel systems — the shared Echo/Nova fighter, the six-state Crimson Vanguard loop, the four data-driven attacks, Impact Windows, and the recoverable Final Clash — onto that approved foundation with per-system acceptance conditions, risks, and milestone contracts; and the *cinematic-integration-inspector* independently audits both outputs against ten hard checks drawn from the GDD (scope lock, no runtime AI, numbers unchanged, milestone order, cinematic handoff safety, and more), producing a violations list and required corrections rather than silent fixes. Each agent consumes the previous agent's artifact, each produces exactly one, removing any one breaks the chain, and the third agent's independence is demonstrated by the fact that it found and blocked real specification gaps (rival-AI ownership during Impact bursts, camera/hitbox restoration) instead of approving its upstream unconditionally.

---

*End of cinematic integration inspection. Verdict: APPROVED WITH REQUIRED CHANGES — corrections 1–5 to the human designer before M3; the foundation, the first test, and M1–M2 may proceed.*
