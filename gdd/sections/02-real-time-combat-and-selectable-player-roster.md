# Section 02 — Real-Time Combat & Selectable Player Roster

> **Source:** `Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` v0.4 (2026-07-24), **page 2–3**.
> Text is verbatim from the PDF. The repeating two-line page header was
> removed as page furniture; nothing else was altered, reordered, or reflowed.
> Table text appears in PDF extraction order, so a row's cells may not sit on
> one line.

---

The duel is an action-combat game with short earned timing prompts, not a sequence of QTE 
scenes.
PRESERVED — CONTROL MODEL  Movement, lock-on, light attacks, dodge, perfect dodge, counter, health, 
spacing, and opponent reads occur in real time. Impact Windows and the Final Clash are brief authored 
overlays triggered by gameplay performance. They never replace the main combat loop, never auto-play 
an entire fight, and always return control to the player.
Core loop
1. READ 2. RESPOND 3. BUILD 4. IMPACT 5. ESCALATE 6. CLASH
Read Crimson 
Vanguard’s 
telegraph.
Attack, dodge, or 
counter.
Earn Ascension 
energy.
Choose the timing 
input. Adapt to Phase 2. Attempt the Final 
Clash.
Selectable roster
FIGHTER COMBAT IDENTITY PROTOTYPE EXPRESSION
Agent Echo — 6'0" / 183 cm Lean precision striker Controlled spacing, deliberate movement, perfect-dodge timing, 
counters, restrained orange accents.
Agent Nova — 5'8" / 173 cm Agile pressure striker Faster visual rhythm, lateral movement, aggressive momentum, 
preserved costume palette, cyan-white combat energy.
NEW — SHARED PLAYER-KIT SCOPE RULE  Echo and Nova are selected before the duel and share the same 
prototype framework: movement, lock-on, light attack sequence, dodge, perfect dodge, counter, health, 
Ascension Meter, Impact Windows, and Final Clash. Their initial differences are animation presentation, 
stance and movement personality, VFX language, timing flavor, and character introduction. Fully unique 
move sets, separate balance systems, and extensive character-specific cinematics are deferred until the 
base duel is stable. One signature cinematic variation may be considered only after that foundation is 
approved.
Impact Windows
A qualifying real-time event—such as a perfect dodge, counter, or approved combo milestone—can open one 
short contextual timing prompt. Success extends the exchange into a 1–3 second choreographed burst. 
Failure does not auto-correct the input; the game returns immediately to normal combat.
WINDOW TRIGGER PROVISIONAL RESPONSE 
TIME FAILURE RESULT
First Impact Window First successful perfect dodge or 
counter 0.75 seconds No cinematic extension; return to 
combat with no extra punishment
Standard Impact 
Window Approved skill event after cooldown 0.35–0.50 seconds No extension; return to combat
PRESERVED — ONBOARDING RULE  The first Impact Window is intentionally wider, but it still requires the 
player’s input and must be earned through a successful real-time defensive action. The game does not 
press the input for the player and does not convert a miss into success.
