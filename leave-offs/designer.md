---
agent: designer
status: complete
artifact: design-brief.md
date: 2026-07-25
recorded_by: commander
---

# Designer leave-off

`design-brief.md` is on disk and complete — 1090 lines, 16 sections, ending with a
closing statement rather than a truncation.

## Provenance — read this before trusting the status line

The designer agent was **killed by an API session limit** after it finished writing
`design-brief.md` but **before** it wrote this leave-off. The artifact survived; the
gate record did not. The commander verified the artifact directly and recorded this
file, rather than re-running a 99 KB research job that had already succeeded.

**What the commander verified before writing `status: complete`:**

| Check | Result |
|---|---|
| Artifact on disk, not truncated | 1090 lines, closes with "End of design brief" |
| All required sections present | 16 sections, §0 through §15 plus Sources |
| Phase 1 cut line present | §1 — what ships on 1 September |
| Free-asset sourcing present | §12 — $0 budget |
| Provisional-values table present | §13 — 57 rows |
| Wrong-project contamination | **0 hits** for werewolf / mansion / scent / villager |
| Numbers unchanged from the GDD | §13.1 — all 28 carried values match (0.75 s, 0.35–0.50 s, +5/+12/+15/+20/+0, meter 100, CV ≤25 %, 1 HP floor, meter→50, 3 s cooldown, Phase 2 at 50 %, all six state ranges, all three heights) |
| Provisional values resolved on its own authority | **None** — 29 open values routed to §14 as questions |

The inspector will re-check all of this independently at the end of the chain. If it
disagrees with any line above, **the inspector is right and this file is wrong.**

## What the brief contains

§0 how to read it · §1 Phase 1 cut line · §2 architecture · §3 framework decision
(plain Blueprints, **not** GAS) · §4 the one shared player-combat framework ·
§5 attack authoring, telegraph readability, hit detection · §6 the six-state rival
model · §7 Impact Windows and the meter handoff · §8 Phase 2 re-timing through one
data path · §9 the Final Clash · §10 encounter flow and arena · §11 milestone
contents M1–M5 · §12 free-asset sourcing · §13 provisional-values table ·
§14 29 questions for the human designer · §15 constraint compliance · Sources.

## Handoff to the developer

The developer's gate is now **open**. It consumes `design-brief.md` and produces
`build-sequence.md`.

**Carry forward into the developer run:**
- Ship date **1 September 2026**. M1–M4 are Phase 1; M5 is Phase 2 and must not be
  interleaved.
- Every number in §13 is the human designer's. The developer implements them as
  exposed variables and **changes none of them**.
- The 29 open questions in §14 are **not** the developer's to answer either. They
  become exposed variables left at whatever the designer sets.
- Unreal MCP must be connected before the developer's steps can actually be executed
  in the editor. Writing the sequence does not require it; running it does.
