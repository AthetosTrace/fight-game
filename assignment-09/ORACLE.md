# The Oracle — what "broken" means in *Ascendant Impact*

**Written 2026-08-24, before any driving code**, per sprint task `Q01` step 1.

An adversarial agent is only as good as its definition of failure. This document is that
definition. It is derived entirely from **measured constants in
`game/docs/agent/PROTOTYPE_BLACKBOARD.md`** — values read out of the live editor across
fifteen milestones — and every invariant cites the section it came from.

**Why not the GDD.** On 2026-08-23 the designer of record cut ship scope (**D1–D4**,
`design/decisions.md`). The Ascension Meter, Impact Windows and the Final Clash are
deferred whole; health zero wins the duel. Testing against the GDD's combat economy would
be testing a game that is not being built.

---

## 1. The system under test

| Actor | Role | Blackboard |
|---|---|---|
| `BP_ThirdPersonCharacter` | player — move, jump, punch, take damage | §16.1, §22, §23 |
| `BP_VanguardProxy` | rival — health, hit-react, ragdoll | §7, §18 |
| `BP_VanguardDuelMover` | **sole authority for all fighter position constraints** | §12, §14.1, §15.2, §22 |
| `BP_VanguardBasicAttackDriver` | one telegraphed strike, windup → strike → recovery | §16, §17.1 |
| `BP_DuelKnockoutCoordinator` | KO detection, movement stop, ragdoll | §18, §19 |
| `BP_DuelCameraRig` | 2.5D framing, mutual facing | §11, §14.2 |
| `UI_DuelHUD` | both health bars | §17.2 |

## 2. Measured constants

Every number here was read from the live editor and recorded with its milestone. **None of
them is changed by this agent.**

### Arena and spacing

| Constant | Value | Source |
|---|---|---|
| `CombatAxisMin` / `CombatAxisMax` | **−650 / +650** | §14.1 |
| Max legal separation | 1300 cm | §14.1 |
| `MinimumAxisSeparation` | **78** | §15.2 |
| Player capsule radius / half-height | 35 / 90 | §15.1 |
| Vanguard capsule radius / half-height | 34 / 88 | §15.1 |
| **Capsule contact distance** | **69 cm** center-to-center | §15.1 |
| `PreferredDistance` | 180 | §15.2 |
| `RangeDeadZone` | 45 → retreat under 135, advance beyond 225 | §15.2 |
| `RetreatSpeedScale` | 0.5 (~150 cm/s vs player 600) | §15.2 |
| Vanguard jog | 300 cm/s | §15.2 |

### Side ownership and crossing

| Constant | Value | Source |
|---|---|---|
| `CurrentSideSign` | ±1 (+1 = Vanguard right) | §22 |
| `SideDeadzone` | **20** | §22 |
| `CrossingMinRelativeHeight` | **50** | §22 |
| `bCrossingActive` | false at rest | §22 |
| `JumpZVelocity` / `GravityScale` / `AirControl` | **820 / 1.9 / 0.35** | §23 |
| Jump apex rise / airtime | 180 cm / 0.89–0.92 s | §23 |
| Vanguard capsule top (1.1 stature) | 176 cm | §22 |
| Crossing window | 0.6–0.7 s | §23 |

### Attack driver

| Constant | Value | Source |
|---|---|---|
| `AttackRange` (combat-axis separation gate) | **240** | §16.3, §16.4 |
| `WindupDuration` | **1.1 s** | §17.1 |
| `StrikeImpactDelay` | 0.3 s | §16.3 |
| `StrikeDuration` / `RecoveryDuration` | 0.6 / 1.0 | §16.3 |
| `AttackCooldownMin` / `Max` | **2.5 / 4.0** | §16.3 |
| `AttackDecisionChance` | 0.65 | §16.3 |
| `RetryDelay` / `InitialAttackDelay` | 0.6 / 1.5 | §16.3 |
| `ImpactForwardOffset` / `ImpactRadius` | 100 / 90 | §16.3 |
| **Max reach** (100 + 90 + player 35) | **225 cm** | §16.2 |
| `ImpactDepthTolerance` | **55 cm** | §17.1 |
| `AttackDamage` | 10 | §16.3 |
| Player punch overlap | forward × 120, radius 110 | §22 |
| Player punch damage | 10 | §22 test G |

### Health and knockout

| Constant | Value | Source |
|---|---|---|
| Player `MaxHealth` | 100 | §16.1 |
| Vanguard `Health` max | 100 (hardcoded in two places) | §17.2, §17.7 |
| `ImpactToRagdollDelay` | 0.2 s | §19 |
| KO one-shot flags | `bVanguardKO` / `bPlayerKO` | §18.1 |
| Ground plane | Z = 0 (traces at X −500/0/+500 all hit exactly 0) | §22 |

---

## 3. The invariants

Severity: **S1** would make the build unshippable · **S2** is a real defect a player would
hit · **S3** is a robustness or fairness concern.

### B — Boundary

| ID | Invariant | Detection | Sev |
|---|---|---|---|
| **B1** | Both fighters stay inside `[CombatAxisMin, CombatAxisMax]` = ±650 on the combat axis. | Sample both X. Violation if `abs(x) > 650 + tol` persists beyond `correction_frames`. §14.1 says corrections are gentle and land within roughly one frame of movement. | S1 |
| **B2** | Axis separation never drops below `MinimumAxisSeparation` 78 for longer than the correction window. | Separation under 78 sustained. §15.3 measured a floor of 85 under sustained pursuit. | S2 |
| **B3** | **Capsules never interpenetrate**: separation ≥ 69 cm. | Hard physical bound (35 + 34). §15.3 records that overlap below 69 never occurred. Stronger than B2 and never legal, crossing included. | S1 |
| **B4** | The Vanguard stays within its authored depth lane. | Read the lane bound from the mover CDO rather than hardcoding it; violation is Y outside that clamp. §12, §14.1. | S2 |
| **B5** | While `bCrossingActive` is false, the sign of (vanX − playerX) equals `CurrentSideSign`. | The ordering rule. §22 rewrote `ApplyConstraints` to be side-aware around exactly this. | S2 |

### S — Stuck states

| ID | Invariant | Detection | Sev |
|---|---|---|---|
| **S1** | **Every crossing closes.** `bCrossingActive` returns to false once the player is grounded. | True while grounded beyond `stuck_seconds` → violation. §22: "deactivate on first grounded frame". | S1 |
| **S2** | The mover is never left locked while the driver is idle. | `bExternalMovementLocked` true while `AttackState == 0` beyond a cycle. §16.1 locks during windup/strike/recovery and unlocks on finish **or cancel** — a cancel path that skips the unlock deadlocks movement. | S1 |
| **S3** | **The Vanguard never parks legally outside its own attack range.** | Axis separation ≤ `AttackRange` 240 continuously while `AttackState` stays 0 past `AttackCooldownMax` plus several `RetryDelay` rolls. | S1 |
| **S4** | A ragdoll never settles below the floor plane. | Mesh Z below 0 after `ImpactToRagdollDelay`. §22 establishes ground at exactly Z 0. | S2 |
| **S5** | The duel always remains progressable — at least one fighter can still lose health. | Both fighters alive, neither able to damage the other, sustained. | S1 |

> **S3 is a pre-registered regression, not a hypothesis.** It happened during §16: the range
> gate used 2D distance ≤ 190 while the mover legally holds axis separation up to 225, so
> after its first strike the Vanguard settled at 209 and never attacked again. The fix moved
> the gate to combat-axis separation ≤ 240. Any change to the hold band or the gate can
> reopen it, which is exactly why it is checked every run.

### X — Exploits

| ID | Invariant | Detection | Sev |
|---|---|---|---|
| **X1** | No damage event lands on a KO'd fighter. | Health changes after the KO flag sets. §18.1 disables the capsule specifically to prevent this. | S2 |
| **X2** | Punch cadence cannot outrun the `bIsAttacking` re-entry guard. | Damage events per second above what the guard and montage length permit. §18.1. | S2 |
| **X3** | **Collision-ignore never leaks past a knockout.** | `bCrossingActive` true after either KO flag sets. §22 added `StopMover` → `SetCrossingCollisionEnabled(false)` for this; §22 test I verified it once. | S2 |
| **X4** | Jump-over cannot push either fighter out of bounds. | During a crossing the player's X clamp relaxes to the full arena and min-separation is suspended (§22). Land inside min-sep repeatedly and watch whether the Vanguard is pushed through `CombatAxisMax`. §22 test E clamped correctly once; this probes it hard. | S1 |
| **X5** | A KO'd player deals no damage. | Vanguard health changes while `bPlayerKO` is true. §18.1 sets `bIsAttacking=true` permanently. | S2 |
| **X6** | **The Vanguard is not cancel-locked out of every attack it starts.** | Fraction of started attacks that reach `PerformImpactCheck` under continuous player punching. §17.1 widened the interrupt window to *any* player hit from telegraph start until impact — that is `WindupDuration` 1.1 + `StrikeImpactDelay` 0.3 = **1.4 s of cancellable time per attack**, against a 2.5–4.0 s cooldown that a cancel **rerolls in full**. | S2 |

| **X7** | **Position constraints stay enforced after a knockout.** | Any of B1, B3 or B5 violated while either KO flag is set. `StopMover` disables the mover tick and `ApplyConstraints` runs on it (§18.1, §14.1). | S1 |

> **X7 was found empirically on 2026-08-24 (seed 7) and formalized afterwards.** B1, B3 and
> B5 caught the symptoms; X7 names the shared cause. It is recorded this way rather than
> implying it was predicted. It **exceeds K6** — K6 accepts a survivor acting freely after a
> KO, not leaving the arena or passing through the other fighter's capsule.

> **X6 is the strongest design-level candidate in this oracle.** It is not a coding error —
> §17.1 widened the interrupt window deliberately, for fairness. The question it raises is
> whether a player who simply punches on a loop can deny the Vanguard *every* attack it ever
> begins, since each cancel rerolls the whole cooldown. If so, the fix is a design decision
> (a cancel that rerolls only part of the cooldown, a post-cancel grace, or an uncancellable
> late windup) and belongs to the designer of record — **this agent reports it and does not
> resolve it.**

### L — Logic violations

| ID | Invariant | Detection | Sev |
|---|---|---|---|
| **L1** | Health stays within `[0, max]` for both fighters. | §16.1 clamps with `Max(0, h−d)`; §17.2 relies on 0–1 bar values. | S1 |
| **L2** | **Both fighters are never KO'd.** | `bVanguardKO` and `bPlayerKO` both true. Nothing resolves a double KO. | S1 |
| **L3** | Side sign flips **exactly once** per crossing. | Count flips between crossing open and close. §22/§23 verified exactly one per crossing across many trials; more than one is the deadzone bug returning. | S2 |
| **L4** | A cancelled attack applies no damage. | Damage event after `CancelAttack`. §16.2, §17.1. | S1 |
| **L5** | **Exactly one damage event per strike.** | Guarded by `bImpactDone` (§16.2). Two events from one strike doubles the damage budget. | S1 |
| **L6** | Damage magnitude is exactly 10 in both directions. | Any health step that is not 10. §16.3, §22 test G. | S2 |
| **L7** | A KO'd fighter's health does not recover mid-match. | Health above 0 after its KO flag set. | S2 |
| **L8** | *(gated on `G05`)* A KO reaches a stated result. | Currently **KNOWN-OPEN** — see K1. Becomes live once the match loop lands. | S1 |

---

## 4. Known limitations — pre-registered, and NOT reportable as discoveries

The blackboard documents these as intentional, deferred, or accepted. They are written down
**before the first run** so that no run can pass one off as a finding. A finding matching a
`K` entry is filed as `KNOWN` and excluded from the headline count.

| ID | Known limitation | Source | Status |
|---|---|---|---|
| **K1** | **No victory/defeat resolution after a KO.** The survivor walks, jumps and punches the air freely; the loser stays down. | §18.4 | `G05` closes it |
| **K2** | Same-frame punch-vs-impact trade, ~1 frame wide. | §17.1, §17.7 | accepted |
| **K3** | The ragdolled mesh can drift from its capsule; the camera frames capsules. | §18.4 | graybox-accepted |
| **K4** | Telegraph "!" yaw is fixed to the `+Y` camera side. | §16.7, §17.7 | one value, deferred |
| **K5** | Vanguard max health hardcoded as 100 in both its graph and the HUD divisor. | §17.7 | deferred |
| **K6** | Post-KO the surviving player can act freely. | §18.4 | intentional, pending `G05` |
| **K7** | Ragdoll settle depends on template physics assets; no per-bone tuning, no impulse. | §19 | deferred knob |
| **K8** | Player boundary behaviour is walk-in-place at the edge — no input suppression. | §14.1 | deliberate (would require touching `Move`) |
| **K9** | Template jump/fall/land timing was authored for slower arcs than `GravityScale` 1.9; foot-skate persists. | §21, §23 | flagged for the animation pass |

---

## 5. Harness parameters — not design values

These belong to the QA harness and govern **detection only**. Changing one changes how
sensitive the agent is, never how the game behaves. They are listed separately so no reader
mistakes them for tuning values, and so a finding can be reproduced exactly.

| Parameter | Purpose |
|---|---|
| `sample_hz` | how often live state is read |
| `correction_frames` | frames a clamp is allowed to correct within before a boundary breach counts |
| `position_tolerance_cm` | slack on position comparisons, absorbing sampling jitter |
| `stuck_seconds` | how long a state must persist to count as stuck |
| `seed` | the RNG seed — **recorded with every finding so any run reproduces** |

**Measured floor, 2026-08-24:** each `execute_tool` inside the editor costs ~0.29 s on the
game thread and a sample needs seven, so the achieved interval is **2.0–2.3 s** however low
`sample_hz` is set. Every timing-based invariant — `S1`, `S3`, `L3`, `L5`, `X6` — is
therefore **gated on an interval the harness never reached, and suppressed rather than
guessed at.** Those invariants are *untested*, not passed. The position-based invariants
(`B1`, `B3`, `B5`, `X7`) compare coordinates within a single sample and are unaffected.

**The project rule stands: no agent changes a number, and no agent resolves a value the
project records as OPEN or PROVISIONAL.** Every constant in §2 is provisional and pending
playtest. This agent measures them; it never edits them and it never proposes a value in
place of one.

---

## 6. Backends, and the honesty rule

The same oracle runs behind two backends, and **every finding records which one produced
it.**

- **`sim`** — an offline model of §2's constants. Runs with no editor. It can exercise
  every invariant that is a consequence of the authored rules, and it is how the agent and
  the oracle are developed and regression-tested.
- **`pie`** — the live editor over Unreal MCP at `127.0.0.1:8000`, driving real input where
  it can (Slate `Click` fires `IA_Attack`; `PressKey "SpaceBar"` jumps) and scripted
  repositioning where it cannot.

**A `sim` finding is a finding about the authored rules, not proof of a runtime defect**,
and it is labelled that way in the report. Assignment 09's Findings criterion asks for a
real bug in the real game, so `sim` findings are the hypothesis list that makes the `pie`
run productive — never a substitute for it.

`Q02` step 4 adds the other half of the honesty rule: a finding caused by the harness
repositioning something impossibly is a **harness artefact**, not a game bug, and claiming
it as one is worse than finding nothing.
