# Pipeline — how this content was generated

An **LLM-assisted authoring pipeline driven by a scoped source manifest.** No Python, no vector database, no embedding model. Retrieval is performed by reading a fixed, explicitly enumerated set of project documents and quoting from them verbatim into the generation context; grounding is enforced by a manifest that names what may be read, and by a verbatim-quotation rule that makes every claim checkable against a source line.

The pipeline is deliberately auditable rather than automated: every stage leaves a written artifact on disk, so the whole run can be re-checked by a human reading files, with no tooling required.

---

## 1. The scoped source manifest

The manifest is the retrieval boundary. **Only these files may be read**, and any claim in a generated output must trace to one of them:

| # | Source | Role | Authority |
|---|---|---|---|
| 1 | `gdd/ascendant-impact-gdd-v0.4.md` | Assignment #02 Revised GDD v0.4, 17 pages, extracted from the PDF with `pypdf` | **Source of truth.** Wins every conflict. |
| 2 | `assignment-04/shared/knowledge-base/` | The derived canon layer — `core-canon.md`, `vanguard-telegraphs.md`, `impact-window-cinematics.md`, `shattered-ring-reactions.md`, `retrieval-manifest.md` | Derived from #1. Defers to it. |
| 3 | `combat-integration-plan.md` | The 28-system integration map onto the approved Blueprint-first foundation | Approved plan of record |
| 4 | `cinematic-integration-inspection.md` | Independent audit; the five open restoration defects V1–V5 | Audit of record |
| 5 | `build-sequence.md` | Ordered editor steps M1-01 → M5-08 with real asset paths | Approved build order |
| 6 | `assignment-04/shared/critic-rules/consistency-checklist.md` | The seven shared consistency checks | Critic input |

**Two exclusions are part of the manifest, not oversights:**

- **`Ascendant_Impact_GDD_Assignment_01_Anthony.pdf` is excluded.** It is the superseded v0.1 draft in which Nova was an authored rival. In v0.4 Nova is a selectable player avatar. Citing v0.1 would inject a reversed fact.
- **GDD pages 10–14 are excluded.** They are supplied image reference sheets (character scale, arena, Echo, Nova, Crimson Vanguard) and carry **no extractable text**. No stage may guess at their contents.

The manifest is also scoped *against* the sibling capstone project: nothing from CapstoneWerewolf may be read or cited. Every output was grepped for `werewolf`/`mansion`/`scent`/`villager` and returned zero hits.

---

## 2. Stages

```
  ┌─────────────────────────────────────────────────────┐
  │ 0. SCOPE — fix the manifest; identify the gap        │
  └────────────────────────┬────────────────────────────┘
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │ 1. QUERY — write ONE question per output             │
  └────────────────────────┬────────────────────────────┘
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │ 2. RETRIEVE — read manifest sources; extract the     │
  │    passages that answer the query, VERBATIM          │
  └────────────────────────┬────────────────────────────┘
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │ 3. GENERATE — write the output with the retrieved    │
  │    text pinned in a header above the content         │
  └────────────────────────┬────────────────────────────┘
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │ 4. CRITIC — adversarial re-read against sources;     │
  │    quote claim vs. conflicting source; correct       │
  └────────────────────────┬────────────────────────────┘
                           ▼
  ┌─────────────────────────────────────────────────────┐
  │ 5. EVIDENCE — pair each retrieved chunk with the     │
  │    output line it produced, side by side             │
  └─────────────────────────────────────────────────────┘
```

### Stage 0 — Scope

Fix the manifest above. Then identify the **content gap**: what does this game specifically lack that generated content could fill, and which of those gaps is *production-support* material rather than player-facing fiction (which the sibling pack already covers). Recorded in `../README.md` §2.

### Stage 1 — Query

Each output gets exactly **one** question. One question per output is a constraint, not a formality: it is what keeps an output from sprawling into three half-documents, and it is what makes retrieval checkable — a passage either helps answer that question or it does not belong.

The three queries are printed verbatim at the top of each output file and each evidence file.

### Stage 2 — Retrieve

Read the manifest sources and extract the passages that bear on the query. Rules:

- **Verbatim only.** Passages are copied, not summarised. A summary cannot be checked against a source; a quotation can.
- **Located.** Every passage carries its file and its section, heading, or step ID.
- **Sufficient.** If the retrieved set does not answer part of the query, that part is marked `OPEN` in the output rather than filled from inference.

### Stage 3 — Generate

Each output opens with a fixed header, before any content:

```
QUERY: <the one question this output answers>
SOURCES READ: <file paths, comma separated>
RETRIEVED TEXT:
<the actual passages used, verbatim>
---
```

The retrieved text sits **in** the artifact rather than beside it. That is the pipeline's main grounding device: a reader can check any claim against the quotations at the top of the same file, without opening anything else, and a claim with no supporting quotation above it is visibly unsupported.

Generation rules, enforced at write time:

1. **Never state a number that cannot be pointed at in a source file.**
2. **Never resolve a provisional value.** Open values are named with their question tag (`OPEN — Q22`) and left open.
3. **Never exceed the scope lock.** One player, one authored rival, one arena, one shared framework, four attacks A–D, one duel with a win and a loss.
4. **Never imply runtime AI-model calls** in the shipped game.
5. **Never duplicate the sibling pack.** Player-facing telegraph copy, Impact Window beat descriptions, and environmental reaction language belong to `../../shared/knowledge-base/` and Tony's outputs; this pack is implementation-support.
6. **Distinguish quoted from derived.** (Added after the critic pass — see §4 and `../README.md` §5.)

### Stage 4 — Critic

An adversarial re-read whose stated goal is to **break** the outputs, not approve them. Two passes:

- **Checklist pass** — the seven shared checks in `consistency-checklist.md`: Nova-as-boss, runtime-AI implication, free Impact success, extra arena or fifth attack, altered governed numbers, cinematics that fail to restore, scope expansion beyond the duel.
- **Claim-by-claim pass** — for every *specific* claim, ask whether a source actually says it, or whether it was inferred and then written in the register of fact.

Findings are recorded as **claim quoted → conflicting source quoted with location → which wins and why → corrected line**, and the corrections are **applied to the output files**. Clean checks are recorded too, so the pass is auditable rather than a claim of diligence.

The checklist pass found nothing. The claim-by-claim pass found six real defects. That asymmetry is the argument for having both: the checklist catches contradictions of canon; the second pass catches over-extensions, which are not contradictions and slip straight through a checklist.

### Stage 5 — Evidence

For each output, `../retrieval-evidence/<output>.md` pairs each retrieved chunk with the generated line it produced, side by side, plus one line per source on why it was selected and what it contributed, plus every post-critic before/after. Copy only.

---

## 3. Why no code

The retrieval problem here is small and fixed: six sources, three queries, one human reviewer. A vector store would add an embedding model, a chunking strategy, and a similarity threshold — three new sources of silent error — to a corpus small enough to enumerate by hand. Worse, it would make grounding *harder* to audit: a reviewer would have to trust a similarity score instead of reading a quotation.

The manifest approach trades recall for verifiability, which is the right trade when the corpus is this size and when the failure mode that actually matters is **an unsupported claim reaching a build document**, not a missed passage.

> **Flagged for the designer, honestly:** the Assignment #04 brief states that *"Code that does not run scores 0 across all criteria. Functional code is the minimum bar, not an achievement."* This pipeline is a documented process with artifacts, not an executable program, on explicit instruction ("No Python"). If the grader reads that criterion as requiring runnable code per submission, this pack would need a scripted harness added — the manifest, queries, and rules above are already specified tightly enough to script directly. Tony's `assignment-04/tony/pipeline/` contains a Python implementation against the same shared knowledge base. **This is the designer's call, and it is worth making deliberately before submission.**

---

## 4. What changed after the critic pass

One rule was added to Stage 3 as a direct result of the critic findings, and it is the pipeline's substantive improvement rather than a cosmetic one.

**Rule 6 — distinguish quoted from derived.** Four of the six findings (F2, F3, F4, F6) were the same defect: an inference written in the same typographic register as a quotation. None was a wild invention; three were probably correct. The harm was that a document rendering `bLockTrackingAtActive = true` (sourced to build step M4-01) and `bUsesPropulsion = false` (inferred from the GDD attributing propulsion to D alone) in identical formatting teaches its reader to trust both equally — and an implementer building from it cannot tell which values they may safely change.

Every derived claim now carries a visible marker and its derivation:

> "`bUsesPropulsion` — expected **false**, `MaxTravelDistance` unused. *Derivation, not a quoted value:* the GDD attributes propulsion to **D only** ("Short propulsion-assisted approach"), so A/B/C read as non-propulsion. The row values themselves are the designer's to set."

Three registers, always visually distinct: **quoted from source** · *derived by inference, with the derivation shown* · `OPEN — designer decides`.

---

## 5. Files this pipeline produced

```
assignment-04/madion/
├── outputs/
│   ├── qa-edge-case-test-pack.md          17 tests across the five defects + all overlay branches
│   ├── animation-integration-briefs.md    one authoring brief per attack A–D
│   └── vfx-audio-cue-sheets.md            12 cue specifications with accessibility contracts
├── retrieval-evidence/
│   ├── qa-edge-case-test-pack.md          7 chunk→output pairs + 1 correction
│   ├── animation-integration-briefs.md    8 chunk→output pairs + 4 corrections
│   └── vfx-audio-cue-sheets.md            9 chunk→output pairs + 2 corrections
├── critic-evidence/
│   └── critic-report.md                   7 checklist checks + 6 findings, all corrected
├── pipeline/
│   └── README.md                          this file
└── README.md                              the submission write-up
```
