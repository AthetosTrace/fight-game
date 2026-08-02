# GDD v0.4 — index

Source of truth: **`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf`**,
Assignment #02 Revised, **v0.4, 2026-07-24, 17 pages**.

`Ascendant_Impact_GDD_Assignment_01_Anthony.pdf` is the superseded v0.1 draft and must
never be cited. Its major reversal: Nova was an authored rival in v0.1 and is a
**selectable player avatar** in v0.4.

## How to cite this document

**Cite `gdd/sections/` for authored text. Cite `gdd/reference/` for the image sheets.**
Both record the PDF pages they came from, so a citation can always be traced back.

## `gdd/sections/` — authored text, one file per numbered section

Split on the document's own section numbering rather than on page breaks, so a
citation can be narrower than a page. Text is **verbatim**; the only removal is the
repeating two-line page header. Table text sits in PDF extraction order, so a row's
cells may not land on one line.

| File | Section | Pages | Covers |
|---|---|---|---|
| `00-front-matter.md` | — | 1 | Title block: author, version 0.4, engine/platform, revision-marker key |
| `01-executive-summary.md` | 01 | 1–2 | High concept, scope lock, genre/mode/session/engine, design pillars 1–3, character motivation |
| `02-real-time-combat-and-selectable-player-roster.md` | 02 | 2–3 | Control model, the six-step core loop, Echo/Nova roster and heights, shared player-kit scope rule, Impact Windows and their response times, onboarding rule |
| `03-ascension-meter-final-clash-and-encounter-flow.md` | 03 | 3–4 | Meter definition and all five gain values, Final Clash single gate, Clash success/failure resolution, failed-Clash recovery, encounter flow beats |
| `04-crimson-vanguard-authored-rival-ai.md` | 04 | 5–6 | Runtime AI boundary, the six-state flow with **all Phase 1 / Phase 2 timing ranges**, behavioral intent, the four-attack course set, Phase 2 escalation parameters |
| `05-gray-box-vertical-slice-and-technical-milestones.md` | 05 | 6–7 | Gray-box milestone definition, **milestones M1–M5** with required proof and gates, implementation safeguards |
| `06-ai-assisted-development-architecture.md` | 06 | 7 | Human approval gate, allowed support vs course-build boundary per area, **no runtime LLM** rule |
| `07-character-readability-scale-and-opening-flow.md` | 07 | 8–9 | Three-way readability comparison table, colour direction, **character scale (5'8" / 6'0" / 6'10")**, fair-reach requirement, selection and opening flow, concept-video placeholder |
| `08-visual-assets-and-official-version-1-arena.md` | 08 | 9–14 | Official arena direction, the five arena requirements, and the captions of the five supplied reference sheets — **the sheets themselves are recovered in `gdd/reference/`** |
| `09-course-scope-lock-and-future-expansion.md` | 09 | 15 | Scope lock, what is included, deferred future scope, definition of done |
| `10-revision-log-and-open-design-decisions.md` | 10 | 16–17 | v0.4 revision log by section, provisional design decisions for playtesting, central promise |

## `gdd/reference/` — recovers pages 10 to 14

**Pages 10 through 14 are supplied image reference sheets and carry no extractable
text beyond a one-line caption.** They were unreadable to every agent on this project
until 2026-08-02. They are now recovered.

**How.** `pdftoppm`/poppler is absent on this machine, so the Read tool cannot render
PDF pages. Instead each page's embedded JPEG was pulled straight out of the PDF's
`/XObject` resources with `pypdf` and viewed directly. All five images are shared
across the document's resource dictionary; the content stream of each page names
exactly one, giving a clean 1:1 mapping.

| File | Page | XObject | Pixels | Recovers |
|---|---|---|---|---|
| `page-10-character-scale-reference.md` | 10 | `/Im798` | 1448×1086 | Three-figure height line-up against a measured ruler — 5'8" / 6'0" / **6'10" (208 cm)** — plus silhouette, costume and colour for all three |
| `page-11-established-arena-reference.md` | 11 | `/Im807` | 1448×1086 | Shattered Ring, three rendered angles plus a legend: concrete/steel/orange material family, skylight shadow bars, far doorway, mezzanine ring, clear central floor |
| `page-12-agent-echo.md` | 12 | `/Im814` | 1376×1554 | Echo turnaround, front/back/side, 12 named callouts, **3-swatch palette** |
| `page-13-agent-nova.md` | 13 | `/Im823` | 1376×1498 | Nova turnaround, front/back/side, 12 named callouts, **4-swatch palette** including the light-grey helmet cap |
| `page-14-crimson-vanguard.md` | 14 | `/Im832` | 1784×1786 | Vanguard technical board — head/optics, chest core, gauntlet, back thrusters, orthographic views, action vignettes, system stats, and the only in-world prose about the rival |

**Every file in `gdd/reference/` describes an image. It does not quote authored text.**
Each says so at the top, quotes the labels printed inside its image exactly, and marks
anything unclear as **AMBIGUOUS**. Authored GDD text outranks any description in these
files. No agent may guess at anything a file marks ambiguous.

- **`OPEN-QUESTION-IMPACT.md`** — what the recovered sheets say about the open
  questions in `design-brief.md` §14, and the new questions they raise.

## `gdd/ascendant-impact-gdd-v0.4.md` — the original page dump

Kept, unchanged. It is one file split "Page 1" through "Page 17", so nothing in it can
be cited more narrowly than a page, and its pages 10–14 hold only
`[IMAGE REFERENCE SHEET: ... no extractable text; see the PDF]` placeholders.

It stays because `.claude/hooks/entry_gate.py` requires it on disk before the designer
may spawn, and existing artifacts cite it. **Prefer `gdd/sections/` and
`gdd/reference/` for all new work.**

## Re-extracting

If the PDF is ever revised, regenerate everything: `pypdf` is installed and works,
`pdftoppm` is not. Re-run the section split, re-extract the page images, and re-read
the sheets — a revised sheet may say something different.
