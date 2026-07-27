# Framework Evaluation — Ascendant Impact

**Produced by:** framework-evaluator agent (runs after the main crew)
**Consumes:** `project-brief.md` · `design-brief.md` · `build-sequence.md` · `inspection.md` · `gdd/ascendant-impact-gdd-v0.4.md` · `CLAUDE.md`
**Date:** 2026-07-27 · **Ship date:** 2026-09-01 (**36 days remaining**)
**Gate check:** `inspection.md` reports **no violations** and an overall verdict that the
build sequence is faithful to the design brief. Not blocked; evaluation proceeds.

---

## 1. Executive recommendation

### `USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE`

The architecture already specified in `design-brief.md` — one shared `BP_PlayerFighter`
with data-driven Echo/Nova profiles, a Behavior Tree rival driven by one
`DT_VanguardAttacks` Data Table, notify-state attack windows, and custom Impact
Window / Final Clash directors — is the foundation with the highest probability of
shipping a complete, fought duel by 1 September 2026.

Concise reasoning, tied to schedule, scope, and the central promise:

- **Schedule.** 36 days remain. The approved plan is already decomposed into an
  inspected, traceable build sequence (M1-01 → M4-GATE) with no orphans and no gaps.
  Any external framework restarts that clock: learn it, verify UE 5.8 compatibility,
  strip its versus/round/multiplayer assumptions, then rebuild the boss AI, Impact
  Windows, and Final Clash on top anyway.
- **Scope.** Both viable external candidates (n00dFighter, TRUE FGE) are
  **versus-fighting-game templates** — round handling, player-vs-player spawning,
  network replication. Ascendant Impact is scope-locked to one player versus one
  deterministic authored boss with **no PvP**. The templates' core value proposition
  is the part of their architecture this game is forbidden to ship.
- **The central promise.** "Real-time martial-arts combat rewards player skill with
  brief, earned anime-style cinematic spectacle" lives in exactly the systems no
  template provides: perfect-dodge detection in the hit-resolution path, the earned
  Impact Window prompt with its onboarding prohibitions, the double-gated recoverable
  Final Clash, and the six-state readable rival. Those are custom either way. The
  approved plan builds only those; a template adds cost without removing any of them.
- **Budget.** Both external candidates are paid Fab/Marketplace products. The project
  constraint is a $0 asset budget with a human approval gate on any purchase. No
  purchase is justified by the evidence gathered here.

---

## 2. Candidate summary

### 2.1 Approved Blueprint-first custom architecture

- **What it is:** the architecture in `design-brief.md` §2–§9: one `BP_PlayerFighter`
  class (no subclasses), `DA_FighterProfile` data assets for Echo and Nova,
  `BT_CrimsonVanguard` Behavior Tree with six `BTTask_*` states, four attacks as rows
  in `DT_VanguardAttacks` with paired Phase 1/Phase 2 tuning structs, Anim Notify
  State windows (`ANS_Telegraph` / `ANS_ActiveHit` / `ANS_Recover` /
  `ANS_CounterWindow` / `ANS_ComboLink` / `ANS_IFrame` / `ANS_PerfectDodge`),
  `BP_ImpactWindowDirector`, `BP_FinalClashDirector`, and the
  `BP_PresentationSubsystem` kill-switch. Plain Blueprints; deliberately **not** GAS.
- **What is verified:** the full design exists on disk and has passed inspection —
  every build step traces, all four hard checks pass, every governed number is carried
  unchanged, and every technique used (montage sections, notify states, Behavior
  Trees, Data Tables, Enhanced Input, Gameplay Tags without GAS) is stock,
  long-supported Unreal Engine functionality present in 5.8.
- **What remains uncertain:** the design-brief's own red flags R1–R7 (animation
  sourcing, the Crimson Vanguard proxy gap, Motion Warping vs. capped root motion,
  playtest-time pressure), and the 29+ `OPEN` tuning values that only the human
  designer can set. These are execution risks, not architecture risks, and they exist
  under **every** candidate.
- **Available now:** yes — it is the plan of record, buildable through the Unreal MCP.
- **Source/project files inspected:** yes — `design-brief.md` (1,091 lines),
  `build-sequence.md`, `inspection.md` all read in full or in relevant part.

### 2.2 n00dFighter / NFTiny family

- **What it is:** `n00dFighter Template`, a **paid code plugin** on the Unreal
  Marketplace / Fab by n00dtech, presenting a **multiplayer-replicated fighting-game
  template**: damage, round handling, multiplayer spawning, active player swapping,
  intro/victory/fatality cinematics, level progression, an "Actions System," and a
  data-table database model for characters and levels. **NFTiny** is a free public
  GitHub skeleton project (`n00dtech/NFTiny`) that exists only to host the paid
  plugin — it contains setup files, not the framework itself.
- **What is verified:** the marketplace listing exists; the NFTiny GitHub repository
  exists and its own description states it is "the bare minimum project setup required
  for n00dFighterTemplate to function" — i.e., **the free repo is not usable without
  buying the plugin.**
- **What remains uncertain:** every feature claim above is **seller-stated**
  marketplace copy. **UE 5.8 compatibility is unverified** — no primary source found
  stating supported engine versions beyond "created with Unreal Engine 5." Whether its
  round/versus structure can be cleanly reduced to a single boss duel is **unknown**.
  Whether its character database supports one shared player class with data-only
  variants (vs. per-character classes) is **unknown**.
- **Available now:** the paid plugin is purchasable; purchase is not authorized and
  was not made. The free NFTiny repo is available but useless standalone.
- **Source/project files inspected:** **no.** Nothing was purchased, downloaded, or
  installed, per the evaluation rules. The listing claims "all source code" is
  included; that claim is seller-stated and unaudited.
- **Verdict preview:** **REJECTED** — see §5 and the hard-rejection rationale in §9.

### 2.3 TRUE Fighting Game Engine (TrueFGE)

- **What it is:** a **paid Blueprint product** on Fab (formerly the UE Marketplace):
  a "lightweight & powerful fighting game engine" with single-player and multiplayer
  (local + network) support, 2.5D and 3D modes ("Mortal Kombat style vs Tekken style"),
  reported as containing 21 Blueprints with network replication, combo creation, and a
  character-select system.
- **What is verified:** a Fab/Marketplace listing and an Epic Developer Community
  showcase thread exist. That is all that could be verified from primary sources.
- **What remains uncertain:** all feature claims are **seller-stated**. The
  "supports UE 5.0–5.7" figure comes from **third-party asset-aggregator sites, not
  the seller's primary listing** — confidence is at best *inferred*, and even taken at
  face value it **does not include 5.8**. "3D mode" means a Tekken-style versus
  fighter — side-tracking camera, two symmetric fighters, rounds — **not** the
  reverse third-person boss-duel framing the GDD's arena requirements specify.
  Auditability of its 21 Blueprints, its AI capability (if any) beyond a versus
  opponent, and its fit for authored six-state boss logic are all **unknown**.
- **Available now:** purchasable; purchase not authorized and not made.
- **Source/project files inspected:** **no.**
- **Verdict preview:** **REJECTED** — see §5 and §9.

### 2.4 Existing custom C++ combat scaffold

### `NOT EVALUABLE — code not supplied`

A repository-wide glob for `*.cpp`, `*.h`, `*.cs`, `*.uproject`, and `*.uplugin`
found **zero files**. This repository contains documentation, agents, and pipeline
artifacts only — no Unreal project and no C++ source. Per the evaluation rules, this
candidate cannot be scored on its merits and must not be assumed to exist. Its matrix
row is scored 1 across the board solely to reflect that adopting a nonexistent
scaffold is a blocker; those scores describe absence, not code quality.

### 2.5 Minimal hybrid

- **What it is:** the approved Blueprint-first plan, borrowing only proven isolated
  concepts from external frameworks — never inheriting a template project.
- **What is verified:** on examination, **the approved plan already embodies every
  proven external concept a hybrid would borrow.** Montage-section combo chains with
  a buffered-input notify window (`ANS_ComboLink`), notify-state-driven
  telegraph/active/recover windows, socket-swept capsule traces with a per-window
  already-hit set, data-table-driven attack definitions, and Behavior Tree task
  failsafes are the standard published Unreal melee-combat patterns; the design brief
  cites and specifies each one concretely.
- **What remains uncertain:** whether any *specific* isolated system from a paid
  template would ever be worth extracting. Doing so would require purchase and audit
  first, which the evidence does not justify.
- **Available now:** yes — it is the approved plan plus discipline.
- **Source/project files inspected:** same as 2.1.
- **Verdict preview:** viable, scores identically to 2.1 in practice, but adds a
  standing temptation to import template content mid-build. The clean statement of
  the recommendation is 2.1; the hybrid option collapses into it.

---

## 3. Comparison matrix

Scale: 1 = unacceptable / major blocker · 2 = high risk · 3 = workable with
meaningful risk · 4 = strong fit · 5 = excellent fit / lowest risk.

**BP** = approved Blueprint-first · **NF** = n00dFighter/NFTiny · **TF** = TRUE FGE ·
**CPP** = C++ scaffold (not evaluable — scores reflect nonexistence) · **HY** =
minimal hybrid.

| # | Criterion | BP | NF | TF | CPP | HY |
|---|---|---|---|---|---|---|
| 1 | Unreal Engine 5.8 compatibility | 5 | 2 | 2 | 1 | 5 |
| 2 | Third-person 3D combat suitability | 5 | 2 | 2 | 1 | 5 |
| 3 | Blueprint accessibility | 5 | 3 | 4 | 1 | 5 |
| 4 | Source-code access and auditability | 5 | 3 | 3 | 1 | 5 |
| 5 | Input buffering and combo support | 4 | 3 | 3 | 1 | 4 |
| 6 | Dodge, perfect-dodge, and counter support | 5 | 2 | 2 | 1 | 5 |
| 7 | Data-driven move authoring | 5 | 3 | 2 | 1 | 5 |
| 8 | Authored boss-AI integration | 5 | 2 | 2 | 1 | 5 |
| 9 | Impact Window integration | 5 | 2 | 2 | 1 | 5 |
| 10 | Final Clash integration | 5 | 2 | 2 | 1 | 5 |
| 11 | Animation replacement and retargeting effort | 4 | 2 | 2 | 1 | 4 |
| 12 | Camera and cinematic handoff support | 4 | 3 | 2 | 1 | 4 |
| 13 | Debugging and testability | 5 | 2 | 2 | 1 | 5 |
| 14 | Licensing and submission safety | 5 | 4 | 4 | 1 | 5 |
| 15 | Cost to the project ($0 budget) | 5 | 1 | 1 | 1 | 5 |
| 16 | Integration time | 4 | 1 | 2 | 1 | 4 |
| 17 | Risk of hidden assumptions | 4 | 1 | 1 | 1 | 4 |
| 18 | Preserves one shared Echo/Nova framework | 5 | 3 | 3 | 1 | 5 |
| 19 | Preserves the no-runtime-AI rule | 5 | 5 | 5 | 1 | 5 |
| 20 | Probability of complete duel by 1 Sept 2026 | 4 | 1 | 1 | 1 | 4 |
| | **Total (of 100)** | **94** | **47** | **46** | **20** | **94** |

Scoring notes:

- **BP #5, #11, #12, #16, #20 at 4, not 5:** the combo/buffer system, animation
  sourcing (R1/R4), the Level Sequence camera handoffs, and the overall schedule are
  real work with real risk (R1–R7). Nothing here is provided for free; it is all
  specified and buildable, which is what 4 means.
- **NF/TF #1 at 2:** no primary-source evidence of UE 5.8 support for either;
  TrueFGE's best third-party figure tops out at 5.7. Migration risk on a 36-day clock
  is high.
- **NF/TF #6, #8–#10, #13 at 2:** perfect-dodge scoring, a six-state deterministic
  boss with visible debug states, earned Impact Windows with onboarding prohibitions,
  and the double-gated recoverable Final Clash are not claimed by either listing and
  would be custom-built on top of an unaudited foreign codebase.
- **NF/TF #15 at 1:** both are paid products against a $0 budget with a human
  purchase gate. **NF/TF #17 at 1:** a replicated versus/round template repurposed
  into a single-player boss duel is the definition of hidden-assumption risk.
- **NF/TF #19 at 5:** to be fair, neither makes runtime model calls; that rule is
  safe under any candidate here.

---

## 4. Integration impact

### 4.1 Approved Blueprint-first (and the minimal hybrid, which is identical in effect)

| System | Impact |
|---|---|
| Player movement | Built on the UE 5.8 Third Person template as specified (M1-01); no change |
| Lock-on | `BP_LockOnComponent` per design-brief §4.4; no change |
| Light combo | `AM_Player_LightCombo` sections + `ANS_ComboLink`; no change |
| Dodge / perfect dodge | `AM_Player_Dodge` + nested `ANS_IFrame`/`ANS_PerfectDodge`; detection in `ResolveIncomingHit`; no change |
| Counter | `ANS_CounterWindow` on rival montages, one legal BT interrupt; no change |
| Health | One shared `BP_HealthComponent` with `MinHealthFloor`; no change |
| Echo/Nova shared framework | One `BP_PlayerFighter` + two `DA_FighterProfile` assets — the anti-fork rule is native to this candidate |
| Crimson Vanguard AI | `BT_CrimsonVanguard`, six tasks, guaranteed exits; no change |
| Four data-driven attacks | `DT_VanguardAttacks`, exactly four rows; no change |
| Ascension Meter | `BP_AscensionComponent` + `DT_MeterGains`, one write path; no change |
| Impact Windows | `BP_ImpactWindowDirector`, 0.75 s / 0.35–0.50 s widths, onboarding prohibitions; no change |
| Phase 2 | One `Select` node on `bPhase2`, commit on Return to Neutral; no change |
| Final Clash | `BP_FinalClashDirector`, double gate, two reused prompt beats, seven-step failure; no change |
| Animation pipeline | Free sources per design-brief §12 (Mannequins, Mixamo, Fab free tier); retargeting risk R1/R4 stands |
| Camera / presentation layer | `BP_PresentationSubsystem` kill-switch from M1, empty until M5; `Level Sequence` cuts for entrance and Clash |

### 4.2 n00dFighter / NFTiny

| System | Impact |
|---|---|
| Player movement | Replaced by or reconciled with the template's fighter pawn — unknown internals, audit required after purchase |
| Lock-on | Versus fighters face each other structurally; a free-movement soft lock likely conflicts with the template's facing model — rework |
| Light combo | Template combo/Actions System might be reused if auditable; fit to `ANS_ComboLink`-style authored windows unknown |
| Dodge / perfect dodge | Not a claimed feature; custom-built on top of foreign code |
| Counter | Not claimed; custom-built, and must interrupt the template's own state flow — high collision risk |
| Health | Template damage/round system must be **stripped of rounds** and reduced to one continuous duel |
| Echo/Nova shared framework | Template character database *might* support data-only variants — unknown; risk of per-character class pattern violating the single-source rule |
| Crimson Vanguard AI | Not provided as authored boss AI; the six-state BT is built from scratch and must drive a template-owned fighter pawn |
| Four data-driven attacks | Rebuilt in the template's data model or ours — either way, custom |
| Ascension Meter | Custom; must hook the template's damage events |
| Impact Windows | Custom; must pause/resume template combat state — the highest-collision integration in the list |
| Phase 2 | Custom |
| Final Clash | Template "fatality cinematics" exist but coupling to round flow unknown; the double gate, both beats, and the seven-step recovery are custom regardless |
| Animation pipeline | Template rigs/mirroring tool are its own ecosystem; our free-asset plan must be re-validated against it |
| Camera / presentation layer | Versus camera replaced with reverse third-person framing; the `BP_PresentationSubsystem` kill-switch must be imposed on template code that was never written to route through it |

### 4.3 TRUE Fighting Game Engine

Same shape as 4.2 with these differences: Blueprint-only (easier to read once
purchased, no plugin binaries), but the 3D mode is a Tekken-style versus camera —
farther from the GDD's reverse third-person arena framing than n00dFighter's generic
pawn; no boss-AI, perfect-dodge, Impact Window, or Clash claims at all; engine-version
evidence tops out at 5.7 from secondary sources. Every Ascendant-specific system in
the table above is custom on top of an unaudited versus framework.

### 4.4 Existing C++ scaffold

`NOT EVALUABLE — code not supplied.` No integration impact can be stated for code
that is not in the repository.

---

## 5. Build-versus-buy analysis

### 5.1 Approved Blueprint-first

- **Already provided (by stock UE 5.8):** Third Person template movement/camera,
  Enhanced Input, Anim Montages + sections, Anim Notify States, Behavior Tree +
  Blackboard + Gameplay Debugger, Data Tables, Gameplay Tags (no GAS), Level
  Sequences, UMG, free Mannequins/Mixamo/Fab animation sources.
- **Still custom:** everything in design-brief §4–§9 — which is precisely the game.
- **Needs replacement:** nothing.
- **Migration/integration risks:** none (no migration). Execution risks R1–R7 stand.
- **Time saved:** **high** relative to any template path — zero learning curve on
  foreign code, zero stripping, and the build sequence is already written and
  inspected.
- **Time lost:** none attributable to the foundation choice.

### 5.2 n00dFighter / NFTiny — **REJECTED**

- **Already provided (seller-stated, unaudited):** round handling, damage,
  multiplayer spawning, menus, cinNematic hooks, character database, Actions System.
- **Still custom:** six-state boss BT, four data-driven attacks with phase tuning,
  perfect dodge, counter interrupt, Impact Windows, Ascension Meter, Final Clash,
  presentation kill-switch, reverse third-person camera — i.e., every system the
  central promise depends on.
- **Needs replacement/stripping:** round flow, versus spawning, replication
  assumptions, versus camera.
- **Migration/integration risks:** **critical** — unverified 5.8 support; a paid
  plugin whose source is unaudited before purchase; hidden versus/replication
  assumptions under every system we would build on top.
- **Time saved:** **low** (menus and damage plumbing the approved plan already costs
  little to build).
- **Time lost:** **critical** — purchase-approval cycle, learning curve, stripping,
  and fighting the template's assumptions, on a 36-day clock.
- **Hard rejection conditions met:** requires more integration work than the approved
  Blueprint-first architecture; UE 5.8 compatibility unsupported by evidence with
  high migration risk; architecture is organized around versus/multiplayer play the
  prototype must not ship; core claims cannot be verified enough to justify use;
  paid product against a $0 budget without designer approval.

### 5.3 TRUE Fighting Game Engine — **REJECTED**

- **Already provided (seller-stated, unaudited):** versus fighting core, combos,
  character select, local/network multiplayer, 2.5D/3D modes.
- **Still custom:** identical list to 5.2 — all Ascendant-specific systems.
- **Needs replacement/stripping:** versus camera and round structure, replication,
  2.5D assumptions.
- **Migration/integration risks:** **critical** — best-available version evidence is
  5.0–5.7 from third-party aggregators, not the seller; nothing about it is
  verifiable without purchase.
- **Time saved:** **low.** **Time lost:** **critical.**
- **Hard rejection conditions met:** same set as 5.2.

### 5.4 Existing C++ scaffold

`NOT EVALUABLE — code not supplied.` No build-versus-buy statement is possible; no
files exist to audit.

### 5.5 Minimal hybrid

- **Already provided:** everything in 5.1, because the approved plan already uses the
  proven public patterns a hybrid would borrow (montage-section combos, notify-state
  windows, swept-socket traces, data-table attacks, BT failsafes).
- **Still custom / replacement / risks:** identical to 5.1, **plus** a standing
  process risk: "borrow one system" becomes "import template content," which
  re-opens purchase, licensing, audit, and scope questions mid-build.
- **Time saved vs. 5.1:** **low** to none. **Time lost vs. 5.1:** **low**, but
  nonzero governance overhead.
- **Conclusion:** the hybrid adds no capability the plan lacks and one risk it
  doesn't need. It collapses into the Blueprint-first recommendation.

---

## 6. Evidence ledger

All access dates are 2026-07-27, via WebSearch. Nothing was purchased, downloaded,
installed, or modified.

| # | Claim | Source | Accessed | Confidence |
|---|---|---|---|---|
| E1 | n00dFighter Template is a paid code plugin on the UE Marketplace/Fab | unrealengine.com/marketplace/en-US/product/n00dfighter-template-plugin | 2026-07-27 | verified (listing exists) |
| E2 | n00dFighter is a "fully replicated" multiplayer fighting framework with round handling, spawning, player swapping, cinematics, level progression, Actions System, data-table character database | same listing (marketplace copy) | 2026-07-27 | seller-stated |
| E3 | n00dFighter ships "pre-built binaries and all source code" | same listing | 2026-07-27 | seller-stated |
| E4 | NFTiny is a free GitHub skeleton that requires the paid n00dFighter plugin to function | github.com/n00dtech/NFTiny (repo description) | 2026-07-27 | verified |
| E5 | n00dFighter supports UE 5.8 | no primary source found; listing says only "created with Unreal Engine 5" | 2026-07-27 | **unknown** |
| E6 | TRUE Fighting Game Engine is listed on Fab (formerly UE Marketplace) | unrealengine.com/marketplace/en-US/product/true-fighting-game-engine (questions page); forums.unrealengine.com showcase thread | 2026-07-27 | verified (listing exists) |
| E7 | TrueFGE: single-player and multiplayer (local + network), 2.5D and 3D modes, combo creation, character select | listing/showcase copy | 2026-07-27 | seller-stated |
| E8 | TrueFGE contains 21 Blueprints and supports UE 5.0–5.7 | third-party asset-aggregator sites, not the seller's primary listing | 2026-07-27 | inferred (low trust) |
| E9 | TrueFGE supports UE 5.8 | no source found | 2026-07-27 | **unknown** |
| E10 | The UE Marketplace has migrated to Fab; standard Fab license terms govern purchased assets | unrealengine.com/en-US/blog/fab-epics-new-unified-content-marketplace-launches-today | 2026-07-27 | verified |
| E11 | Repository contains zero `*.cpp`, `*.h`, `*.cs`, `*.uproject`, `*.uplugin` files | repository-wide glob (reported by dispatching agent; consistent with repo contents read) | 2026-07-27 | verified |
| E12 | Behavior Tree remains fully included and supported in UE 5.8; State Tree is the newer default | design-brief §6.1 (designer agent's verified research of 2026-07-25) | 2026-07-27 | verified (internal, previously sourced) |

Nothing in this ledger treats ratings, marketing copy, video demos, or AI-generated
summaries as proof of fit. E2, E3, and E7 are load-bearing **only** for the rejection
analysis (i.e., even taken at face value, the templates do not fit); no acceptance
decision rests on a seller-stated claim.

---

## 7. Required human decisions

Only the human designer may resolve these. None are resolved here.

1. **Approve or reject the recommended foundation** (Blueprint-first custom
   architecture) before any implementation begins. `OPEN — designer decides`
2. **Whether to spend anything at all evaluating a paid template** (n00dFighter or
   TrueFGE). This evaluation recommends no purchase; the purchase decision itself is
   not this agent's to make. `OPEN — designer decides`
3. **Licensing acceptance** for any Fab/Marketplace/Mixamo asset that enters the
   build, per the rights-review gate. `OPEN — designer decides`
4. **Whether to run the §8 sandbox test**, and on which machine/branch.
   `OPEN — designer decides`
5. **All provisional timing/tuning values** — the entire design-brief §13/§14 set
   (health pools, damage, dodge windows, combo length, Clash beat widths, etc.)
   remains open regardless of foundation. `OPEN — designer decides`
6. **Echo/Nova character-specific differences** (play-rate, speed, stance additive
   values) — data-profile fields only, values unset. `OPEN — designer decides`
7. **Any future architecture replacement** (e.g., the design brief's note that GAS
   would suit a post-course expansion). Explicitly deferred; not a Phase 1 or Phase 2
   question. `OPEN — designer decides`

---

## 8. Next-step test plan

**Smallest reversible test: verify one buffered light-attack chain in a disposable
UE 5.8 sandbox.**

This is the highest-value narrow capability to prove first: it exercises the exact
mechanism (montage sections + `ANS_ComboLink` notify window + Enhanced Input) that
M1's combo, M3's Impact prompt discard rule, and the Clash beats all reuse, and it
confirms the UE 5.8 Third Person template assumptions in M1-01.

- **Environment:** a throwaway UE 5.8 project created from the Third Person template
  (Blueprint), on a disposable branch (e.g., `sandbox/combo-buffer-test`) or entirely
  outside the main repository. **The main build and `run/agent-pipeline` branch are
  not touched.**
- **Setup (sandbox only):** one montage with two named sections (`Light_01`,
  `Light_02`), one `ANS_ComboLink` notify state on `Light_01`, one `IA_LightAttack`
  Enhanced Input action, the §4.5 buffer logic (`bComboBuffered` set only inside the
  notify window, `Montage Set Next Section` at notify end).
- **Pass condition (all three, observed in PIE):**
  1. A press **inside** the `ANS_ComboLink` window chains into `Light_02`.
  2. No press → the montage ends after `Light_01` and returns to locomotion.
  3. A press **before** the window opens is discarded — it neither queues a chain
     nor plays a second attack.
- **Fail condition:** any of the three behaviors does not occur, or the 5.8 Third
  Person template lacks an assumed piece (Enhanced Input default rig, montage-section
  API behavior), in which case the finding goes back to the designer before M1
  proceeds.
- **Reversible:** the sandbox project/branch is deleted after the result is recorded;
  no main-build asset is created or modified; version-control history on the main
  branches is preserved untouched.
- **Explicitly not the test:** building the duel, the rival, the meter, or any
  milestone content. One capability, one pass/fail, then stop and report.

---

## 9. Final verdict

- **Recommended foundation:** `USE BLUEPRINT-FIRST CUSTOM ARCHITECTURE` — the
  approved plan in `design-brief.md`, executed via the inspected `build-sequence.md`.
  n00dFighter and TRUE FGE are **REJECTED** (unverified UE 5.8 support, versus/
  multiplayer-centric architecture against a no-PvP scope lock, more integration work
  than the approved plan, paid against a $0 budget, core claims unverifiable without
  purchase). The C++ scaffold is `NOT EVALUABLE — code not supplied`. The minimal
  hybrid collapses into the Blueprint-first plan.
- **Confidence:** **high** — for the *foundation choice*. The comparison is not
  close: the strongest external candidate scores 47/100 against the approved plan's
  94/100, and no seller claim, even taken at face value, changes the ordering.
- **Top three risks (all execution risks of the recommended path, already flagged as
  R1–R7 in the design brief):**
  1. **Animation sourcing and retargeting (R1/R4)** — especially the 6'10" Crimson
     Vanguard proxy, the single biggest free-asset gap.
  2. **Schedule compression (R7)** — M4 must be functionally complete around
     20 August to leave real tuning time; 36 days remain and the crew's Unreal MCP
     build phase has not started.
  3. **Open tuning values** — 29+ `OPEN` numbers (health, damage, dodge windows,
     Clash beats) need the human designer's decisions during the build, not after it;
     late answers stall milestones.
- **Immediate next action:** present this evaluation to the human designer; on
  approval, run the §8 sandbox test (one buffered light attack in a disposable
  UE 5.8 project), record pass/fail, then proceed to M1-01 on the main build via the
  Unreal MCP.
- **Approval statement:** **The human designer must approve this recommendation
  before any implementation begins.** Nothing in this document authorizes a purchase,
  a license acceptance, an installation, or a build step. Every number remains
  provisional and owned by the human designer.
