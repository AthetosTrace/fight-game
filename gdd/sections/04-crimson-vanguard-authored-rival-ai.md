# Section 04 — Crimson Vanguard — Authored Rival AI

> **Source:** `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` v0.4 (2026-07-24), **page 5–6**.
> Text is verbatim from the PDF. The repeating two-line page header was
> removed as page furniture; nothing else was altered, reordered, or reflowed.
> Table text appears in PDF extraction order, so a row's cells may not sit on
> one line.

---

A compact state machine or Behavior Tree controls readable, testable armored pressure.
REVISED — RUNTIME AI BOUNDARY  Crimson Vanguard is controlled by authored Unreal gameplay AI. The 
packaged duel makes no runtime LLM calls, does not learn from the player, and does not generate attacks 
or choreography dynamically.
State flow and provisional timing
Idle / Reposition  →  Select Attack  →  Telegraph  →  Active Attack  →  Recover  →  Return to Neutral
STATE PURPOSE PHASE 1 PHASE 2 EXIT CONDITION
Idle / Reposition Face the selected fighter and maintain armored 
pressure 0.60–1.20 s 0.35–0.80 s Valid range and line
Select Attack Choose one of four authored attacks by range and 
cooldown 0.10–0.20 s 0.10–0.20 s Attack selected
Telegraph Show committed pose, warning lights, sound, and 
readable direction 0.55–0.95 s 0.40–0.75 s Telegraph completes
Active Attack Apply authored movement, gauntlet force, hitbox, 
reach, or short propulsion 0.18–0.45 s 0.18–0.45 s Active frames end
Recover Expose a deliberate punish opening after the 
committed strike 0.45–0.90 s 0.35–0.75 s Recovery completes
Return to Neutral Clear attack flags and restore valid locomotion 0.10–0.20 s 0.10–0.20 s Neutral restored
Behavioral intent. Crimson Vanguard advances as a large armored threat: attacks are committed rather than 
random, propulsion closes short gaps explosively, gauntlets communicate force, and every major offense 
exposes a clear recovery opening. Armor and scale may intensify presentation, but they do not remove 
readable counterplay.
Four-attack course set
AUTHORED ATTACK RANGE / PURPOSE READABILITY REQUIREMENT
Authored attack A Close-range committed gauntlet force Distinct wind-up and punishable recovery
Authored attack B Committed forward-pressure sequence Visible first beat and stable tracking limit
Authored attack C Armored reach and space control Clear body direction and visible active range
Authored attack D Short propulsion-assisted approach Thruster cue before movement; no hidden full-arena 
snap
Phase 2 escalation
REVISED — PHASE 2  Phase 2 begins when Crimson Vanguard reaches 50% health. The phase change is 
committed on Return to Neutral, then signaled once with stronger thruster output, warning lights, sound, 
and armor-energy presentation. It uses the same four authored attacks—no transformation rig and no 
second move set.
PARAMETER PHASE 1 PHASE 2
Reposition delay 0.60–1.20 s 0.35–0.80 s
Forward pressure Measured advances More frequent advances and shorter hesitation
Attack weighting Balanced authored selection More aggressive close-range and gap-closing weight
Presentation Readable red-orange systems Stronger thruster, warning-light, sound, and armor-
energy cues
Attack set Four authored attacks Same four authored attacks
