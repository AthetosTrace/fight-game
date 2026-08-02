# Section 05 — Gray-Box Vertical Slice & Technical Milestones

> **Source:** `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` v0.4 (2026-07-24), **page 6–7**.
> Text is verbatim from the PDF. The repeating two-line page header was
> removed as page furniture; nothing else was altered, reordered, or reflowed.
> Table text appears in PDF extraction order, so a row's cells may not sit on
> one line.

---

Validate the complete gameplay contract before expanding presentation.
PRESERVED — GRAY-BOX MILESTONE  The first vertical slice uses proxy Echo or Nova, proxy Crimson Vanguard, 
the official arena footprint, one authored rival attack, one player defensive response, one Impact 
Window, meter gain, and a clean return to neutral. It proves the real-time-to-cinematic handoff before 
final characters, VFX, or expanded choreography.
MILESTONE REQUIRED PROOF GATE
M1 — Combat gray box Movement, lock-on, light sequence, dodge, perfect dodge, counter, 
health
Playable loop with selected 
proxy
M2 — Rival state loop All six AI states and one Crimson Vanguard attack complete without 
deadlock
Returns to Neutral every 
attempt
M3 — Impact handoff Earned prompt, success/failure branches, restored control No forced success or stranded 
cinematic state
M4 — Complete duel Meter, Phase 2, Final Clash, failure recovery, win/loss Start-to-finish course 
prototype
M5 — Presentation pass Approved character treatment, arena reaction, camera, VFX, sound Only after M4 is stable
Implementation safeguards
 Use authored state-machine or Behavior Tree logic with visible debug state names and deterministic 
recovery paths.
 Separate gameplay timing from cinematic presentation so hit-stop, camera, and VFX can be disabled 
during diagnosis.
 Restore input, collision, locomotion, lock-on, and AI state explicitly after every Impact Window and 
Final Clash branch.
 Validate both selectable avatars against the same collision, targeting, reach, and arena-boundary 
tests.
 Treat all timing ranges, meter values, and health thresholds as provisional until validated through 
playtesting and finalized by the designer.
