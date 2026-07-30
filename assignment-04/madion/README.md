# Assignment 04 — Production-Support Content Pipeline for *Ascendant Impact*

**Author:** AthetosTrace · **Game:** Ascendant Impact (Unreal Engine 5.8, PC, one-versus-one cyber-fantasy action fighter)
**Branch:** `assignment4/madion-production-pipeline` · **Opened as a PR for review, not merged.**

This is **my own** Assignment 04 submission, separate from my teammate Anthony's `assignment-04/tony/`. Both read the same shared knowledge base at `assignment-04/shared/`; the generated content is deliberately non-overlapping. His is player-facing; mine is implementation-support.

---

## 1. Knowledge base and provenance

**The knowledge base is the game's actual GDD and its direct downstream artifacts. Nothing here is placeholder lore.**

| Source | What it is | Provenance |
|---|---|---|
| `gdd/ascendant-impact-gdd-v0.4.md` | **Source of truth.** Assignment #02 Revised GDD, v0.4, dated 2026-07-24, 17 pages | Extracted with `pypdf` from `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf`, which cannot be opened by the Read tool on this machine (poppler absent). The extracted markdown is the copy every agent and every stage of this pipeline consults. |
| `assignment-04/shared/knowledge-base/` | The derived canon layer: `core-canon.md`, `vanguard-telegraphs.md`, `impact-window-cinematics.md`, `shattered-ring-reactions.md`, `retrieval-manifest.md` | Anthony's extension of the GDD. Every chunk cites its source file and heading. Defers to the GDD on conflict. |
| `combat-integration-plan.md` | The 28-system integration map onto the approved Blueprint-first foundation | Produced by the `combat-integration-architect` agent, after the human designer approved the framework recommendation on 2026-07-27 |
| `cinematic-integration-inspection.md` | Independent audit — ten hard checks, verdict `APPROVED WITH REQUIRED CHANGES`, five open defects V1–V5 | Produced by the `cinematic-integration-inspector` agent |
| `build-sequence.md` | Ordered editor steps M1-01 → M5-08, with real Unreal asset paths and Blueprint node names | Produced by the `developer` agent |
| `assignment-04/shared/critic-rules/consistency-checklist.md` | Seven named consistency checks | Anthony's critic rules, reused |

**Two deliberate exclusions.** `Ascendant_Impact_GDD_Assignment_01_Anthony.pdf` is the **superseded** v0.1 draft, in which Nova was an authored rival — reversed in v0.4, where Nova is a selectable player avatar. It is never cited. GDD **pages 10–14** are supplied image reference sheets with no extractable text; no stage guesses at their contents.

**Cross-project contamination: zero.** This repository also relates to a separate capstone (CapstoneWerewolf). All three outputs were grepped for `werewolf`, `mansion`, `scent`, and `villager` — no hits.

---

## 2. The gap being filled, and why these three content types

### Where this game is genuinely thin

The GDD is **dense on systems and deliberately sparse on authored specifics**. It fixes every number, every state, and every rule — and then stops. That produces two different kinds of gap, and they need different content:

- **Fiction gaps** — the arena has no history, Project Valor-7 has no origin, "Ascendant operative" and the Ascension fiction are undefined, and there are no UI or announcer strings.
- **Production-support gaps** — the systems are specified but nothing tells a tester how to prove them, tells an animator what a montage must satisfy, or tells a presentation pass what a cue must do.

**Anthony's pack fills the player-facing side** — telegraph readability, Impact Window cinematic beats, environmental reactions. Duplicating that would have been the easy and worthless move.

**My gap statement: this game is thin on the material that turns an approved plan into a buildable, verifiable one.** Three specifics, each traceable to a named line in the sources:

1. **Nothing converts the five open restoration defects into repeatable tests.** `cinematic-integration-inspection.md` returned `APPROVED WITH REQUIRED CHANGES` with V1–V5 open, and states corrections 1–5 "must be accepted by the human designer before **M3** implementation is signed off." The corrections are edits to a document. **Nothing on disk proves the behaviour.** The inspection itself flags this: Proof B "currently inherits V1–V5 — the slice's 'clean return' beat cannot be honestly judged until the restore/suspend spec is corrected."
2. **Four attack montages must be authored and none exists.** `AM_Vanguard_AttackA` is created at M2-13, B/C/D at M4-01. The GDD gives each attack a purpose and a one-line readability requirement — and nothing else. No document tells an animator what the montage owes the Behavior Tree, where hit detection turns on and off, or what must survive an interruption.
3. **Every VFX and sound cue slot is empty by design, with no specification to fill.** `BP_PresentationSubsystem` is "wired empty in M1, filled only in M5." M5 is the presentation pass — and it currently has a kill-switch, five wrapper names, and a blank page.

### Why these three, and why now

| Output | Fills | Why it is the right thing to generate |
|---|---|---|
| `qa-edge-case-test-pack.md` | gap 1 | **The highest-value of the three.** V1–V5 sit exactly on the real-time-to-cinematic handoff the game exists to prove, and they are ranked risk #2 of 5 in the inspection. A paper correction is not a fix. This is also the only output usable *immediately* — the tests can be run at the M2 gate. |
| `animation-integration-briefs.md` | gap 2 | Animation is named the schedule's tightest resource (R1) and the Vanguard proxy the single biggest free-asset gap (R4). A brief written **before** authoring costs nothing; a montage re-authored after a gate failure costs days the 1 September date does not have. |
| `vfx-audio-cue-sheets.md` | gap 3 | M5 is Phase 2 and must stay behind a stable M4 — so writing the spec now is the *only* M5 work that does not violate milestone order. Specifying a cue is not authoring one. |

All three are **implementation-support, not fiction**, so they add zero new canon and cannot contradict the GDD by invention — only by misquotation, which is what the critic pass hunts.

---

## 3. Retrieval, with one worked example

The pipeline is an **LLM-assisted authoring workflow over a scoped source manifest** — six enumerated sources, one question per output, verbatim quotation as the grounding device. No vector store, no embeddings. Full description: [`pipeline/README.md`](pipeline/README.md).

Each output pins its retrieval **inside** the artifact, above the content:

```
QUERY: <the one question this output answers>
SOURCES READ: <file paths, comma separated>
RETRIEVED TEXT:
<the actual passages used, verbatim>
---
```

That is the whole trick: a reader checks any claim against the quotations at the top of the same file, and a claim with no supporting quotation above it is visibly unsupported.

### Worked example — query → retrieved chunk → generated output

**QUERY** (from `qa-edge-case-test-pack.md`):

> How does a tester prove, repeatably and in PIE, that the five open cinematic-restoration defects (V1–V5) are fixed and that every overlay branch — failed Impact Window, failed Final Clash, death mid-overlay, repeated triggers, boss Behavior Tree resume — returns Ascendant Impact to a valid combat state?

**RETRIEVED CHUNK** — `cinematic-integration-inspection.md` §2, defect V1, quoted verbatim:

> "**Evidence:** the only documented mechanism that parks `BT_CrimsonVanguard` is the `bInClash` Blackboard bool → `BTTask_WaitIndefinite` branch, which applies to the **Final Clash only**. The Impact success branch plays "a montage pair on both fighters" for the GDD's 1–3 seconds, and row 19's acceptance condition says "after either branch … the rival BT is running" — implying it was somehow not running during the burst — but **no mechanism suspends the six-state Attack Cycle during the burst**. As specified, `BTTask_SelectAttack`/`BTTask_Telegraph` can fire mid-burst, fight the rival's stagger montage for the montage slot, and either desync the debug state display or strand the burst."

**SECOND RETRIEVED CHUNK** — `cinematic-integration-inspection.md` §8, correction 1, which constrains what the test may assume:

> "**Acceptance:** the plan names an explicit rival-ownership mechanism for the burst (park flag, or a documented can't-attack-state rule), states what is suspended when a window opens (including "nothing," if so decided), and routes its release through `RestoreCombatState()`; the mechanism appears in the M3-GATE checklist."

**GENERATED OUTPUT** — test QA-V1-01, excerpted:

> **Steps**
> 1. Let the rival enter `Telegraph` on Attack A. Confirm the drawn state reads `Telegraph`.
> 2. Dodge so the rival's `ANS_ActiveHit` trace lands while `State.PerfectWindow` is active — a perfect dodge. Confirm damage 0 and meter +12.
> 3. The First Impact Window opens at **0.75 s** (GDD). Press `IA_Impact` inside it.
> 4. During the resulting **1–3 s** burst (GDD), watch the drawn state string and the Blackboard continuously. Do not press any input.
>
> **Expected result** — Throughout step 4 the rival is playing its half of the burst montage pair and its Attack Cycle is **not** progressing. `CurrentState` does not advance into `SelectAttack` or `Telegraph` at any point during the burst.
>
> **Note on the flag name.** The inspection's correction 1 accepts either "a park flag analogous to `bInClash`, or a documented rule that the burst may only play during a state that cannot start a new attack." Which mechanism ships is `OPEN — designer decides`. This test does not assume a name: read whichever mechanism the corrected plan names. If neither exists yet, the test fails at step 4 by definition.
>
> **Fail criteria (any one)** — The state string advances mid-burst. / The stagger beat is visibly interrupted or replaced. / The two debug views disagree at any frame. / The rival attacks the player during the burst.

**What the retrieval did, concretely.** The first chunk supplied the exact failure mode to test for — `SelectAttack`/`Telegraph` firing mid-burst — so the test's fail criteria are the inspection's own predicted symptoms rather than invented ones. The second chunk supplied a constraint that changed the test's shape: because correction 1 permits *either* a park flag *or* a can't-attack-state rule, a test asserting a specific flag name would fail a correct build. So the test reads whichever mechanism ships and asserts the observable behaviour instead. Retrieval did not just supply facts here — it prevented a wrong test.

Full side-by-side pairing for all three outputs, plus every post-critic before/after, is in [`retrieval-evidence/`](retrieval-evidence/) — 24 chunk-to-output pairs total.

---

## 4. What the critic caught

Full report with all quotations: [`critic-evidence/critic-report.md`](critic-evidence/critic-report.md).

The critic ran two passes. **The seven shared checks in `consistency-checklist.md` all passed** — no Nova-as-boss, no runtime-AI implication, no free Impact success, no fifth attack or second arena, no altered governed number, no overclaimed restoration, no scope expansion. The clean results are recorded individually so the pass is auditable rather than asserted.

**The second pass — claim-by-claim, asking whether a source actually says each specific thing — found six real defects. All six were corrected in the output files. None was invented.**

| # | Defect | Winner | Correction |
|---|---|---|---|
| **F1** | Attack A's recover called "**longest of the four**" attacks | Source. M2-13 says "longest recover window **on the montage**" — an intra-montage comparison. At M2, B/C/D do not exist yet, so a cross-attack ranking cannot be the meaning. | "**the longest of the three windows on A's own montage** (M2-13)" |
| **F2** | Attack C asserted to hold "**the longest of the four**" range bands | Source. The GDD gives C "armored reach" but **never ranks the bands**. Possibly inverted: D is a gap-closer, implying D operates at distance C may not cover. | Ranking removed; now states the GDD "does not rank the four range bands against each other" |
| **F3** | Attack B given a "mid band" and "forward travel across the beats" | Source. Neither the GDD nor M4-01 states B's band, distance, or travel. Real risk: `MaxTravelDistance` is **D's** field, so unmeasured B travel inherits D's failure mode with none of its guardrails. | Both marked as unsourced; travel now labelled an inference and routed to the designer |
| **F4** | `bUsesPropulsion = false` stated as settled for A, B, C | Source, on authority. The inference is almost certainly right — the GDD attributes propulsion to D alone — but no source states the row values, and plan §2 principle 8 says "No agent … resolves a provisional value." | Each now reads "expected **false**" with the derivation shown and authority returned to the designer |
| **F5** | Meter expected value stated flatly as **32** | Source. Plan §7 states 32 inside a scripted slice starting from meter 0. QA-V1-01 is runnable at any time. **A tester running a prior test first would record a false failure.** | Now "starting value + 12 + 20 … equals 32 **only if the run begins at meter 0**", plus a new precondition to record the starting value |
| **F6a** | A "**red-orange arena palette**" invented for Shattered Ring | Source. The GDD describes the arena **functionally with no colors** — "industrial", central floor, far doorway. Red-orange belongs to Crimson Vanguard. I transplanted the character's palette onto the arena. | Reasoning rebuilt on the sourced fact (the cue competes with the *Vanguard's* red-orange on the mesh); explicit note not to author against an assumed arena color |
| **F6b** | Ordinary dodge asserted to have "**no cue**" | Source, half. "No meter" is quotable (plan §3.2 row 8). "No cue" is unsourced — asserting an absence is still asserting. | "no meter" kept and cited; cue existence marked `OPEN — designer decides` |

### The pattern, which matters more than any single finding

**Four of six — F2, F3, F4, F6 — are the same defect: inference presented in the same register as sourced fact.** Not one was a wild invention; three are probably correct. The failure was epistemic and typographic: a document that renders `bLockTrackingAtActive = true` (sourced) and `bUsesPropulsion = false` (inferred) in identical formatting trains its reader to trust both equally, and an implementer cannot tell which values they may safely change.

**F1 and F5 are a second pattern: a source claim carried out of the scope that made it true.** "Longest recover on the montage" became longest of four. "Meter shows 32" in a fresh scripted slice became a flat expected value in a test runnable at any time.

**Both patterns are invisible to the shared checklist, which passed cleanly.** The checklist catches contradictions of canon. Neither pattern is a contradiction — they are over-extensions. That is the argument for running a second adversarial pass and not stopping at a checklist.

---

## 5. Self-assessment, and the one concrete change that improved game fit

### Honest assessment

**What worked.** Pinning retrieved text *inside* each artifact rather than beside it was the single highest-leverage decision. It made the critic pass mechanical instead of interpretive: comparing a claim to a quotation twenty lines above it needs no judgement, so the six findings were found by reading rather than by intuition. Anchoring to `cinematic-integration-inspection.md` also meant the outputs address problems the project **actually has** and had already documented, rather than problems I imagined for it.

**What was weakest, and why.** The four F2/F3/F4/F6-class findings all trace to one habit: writing confidently in a document meant to be authoritative. The GDD is sparse by design, and filling its silences with plausible detail is exactly the failure mode this pipeline exists to prevent. It got past generation and was only caught adversarially — which means the *generation* rules were insufficient, not merely that the critic was diligent. F5 is the one I would call a genuine near-miss: it would not have produced a wrong build, it would have produced a **wrong bug report**, which is worse in a way that is easy to underrate.

**Voice.** These are technical documents, so the target voice is the project's own build-document register — clipped, numbered, GDD-quoting, `OPEN — designer decides` where a value is unresolved. That register was inherited by quoting it directly. Where I judge the fit weakest is that the outputs are *long*; a tester at a milestone gate under schedule pressure may want a one-page checklist, and the gate-assignment table is a partial concession to that but not a full answer.

**Scope discipline.** Zero scope violations: four attacks throughout, one arena, no PvP, no per-fighter move sets, no runtime AI, M5 kept behind M4, and not one provisional value resolved — including Q22, which was the strongest temptation, since asserting either reading of the 1 HP floor would have made QA-FC-01 shorter and cleaner.

### The one concrete change that improved game fit

**Rule 6 was added to the generation stage: every claim must declare whether it is quoted, derived, or open — and derived claims must show their derivation.**

This is a prompt/process change, made *because* of finding F4, and applied back across all three outputs. Before, the pipeline had five generation rules, all about what may not be said (no unsourced numbers, no resolved provisionals, no scope expansion, no runtime AI, no duplication of the sibling pack). Every one is a prohibition — and prohibitions caught nothing here, because none of the six findings **violated** one. F4 stated no wrong number; it stated a probably-right value with borrowed authority.

Before, after F4 was applied:

> **Before:** "`bUsesPropulsion` = **false**. `MaxTravelDistance` unused."
>
> **After:** "`bUsesPropulsion` — expected **false**, `MaxTravelDistance` unused. *Derivation, not a quoted value:* the GDD attributes propulsion to **D only** ("Short propulsion-assisted approach"), so A/B/C read as non-propulsion. The row values themselves are the designer's to set."

Three registers, always visually distinct: **quoted from source** · *derived by inference, with the derivation shown* · `OPEN — designer decides`.

**Why this improves game fit specifically.** *Ascendant Impact*'s governing constraint is not a lore bible — it is that **the human designer owns every rule and number, and every timing value is provisional pending playtest.** A generated document that blurs quoted and derived values quietly takes authority the designer never delegated. Rule 6 makes the boundary of that authority visible on every line, which is what makes these documents safe to build from: an implementer can see at a glance which values are the GDD's, which are my reading, and which are still the designer's to set.

---

## Files

```
assignment-04/madion/
├── README.md                              this file
├── outputs/
│   ├── qa-edge-case-test-pack.md          17 tests · V1–V5 + every overlay branch
│   ├── animation-integration-briefs.md    one authoring brief per attack A–D
│   └── vfx-audio-cue-sheets.md            12 cue specs with accessibility contracts
├── retrieval-evidence/                    24 chunk→output pairs + all corrections
├── critic-evidence/critic-report.md       7 checks + 6 findings, all corrected
├── pipeline/README.md                     manifest, five stages, why no code
└── submission/                            (reserved)
```

**Nothing in this pack enters the Unreal build without human review and explicit designer approval.** This is offline authoring tooling; it lives outside the game's scope lock, and the shipped build still makes no runtime AI-model calls.
