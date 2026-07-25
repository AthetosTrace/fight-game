# Ascendant Impact - Game Design Document v0.4 (extracted text)

> Machine-extracted from Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf (Assignment #02 Revised, v0.4, 2026-07-24, Anthony T.).
> The PDF is the source of truth; this file exists so agents whose toolset is Read-only
> can consult the GDD, and so it can serve as the retrieval corpus for assignment #04.
> Pages 10-14 are supplied image reference sheets and carry no extractable text.



---

## Page 1

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   1
ASSIGNMENT #02  /  REVISED GAME DESIGN DOCUMENT
ASCENDANT
IMPACT
A cinematic one-versus-one cyber-fantasy martial-arts action fighter
AUTHOR VERSION ENGINE / PLATFORM
Anthony T. 0.4 - 2026-07-24 Unreal Engine 5.8 / PC
REVISION MARKERS  REVISED = feedback-driven clarification   NEW = added implementation rule or milestone
01
Executive Summary
Choose an Ascendant operative. Survive one complete duel. Earn the spectacle.
REVISED — HIGH CONCEPT  The player selects Agent Echo or Agent Nova and enters the Shattered Ring to fight 
Crimson Vanguard / Project Valor-7 in one complete third-person duel. Combat is primarily real time: 
movement, attacks, dodges, perfect dodges, and counters build Ascension energy and earn brief anime-
inspired cinematic bursts, culminating in one recoverable Final Clash.
Scope lock. The course prototype remains one player, one authored AI opponent, one official arena, one 
shared player-combat framework, four authored rival attacks, and one complete duel with win and loss 
outcomes.
GENRE PLAYER MODE TARGET SESSION ENGINE / PLATFORM
Third-person action 
fighter
1 player vs. authored AI; Echo or Nova 
selectable 3–5 minutes Unreal Engine 5.8 / PC
Design pillars
# PILLAR PLAYER-FACING MEANING
1 Skill Creates Spectacle Readable timing and deliberate decisions earn the strongest visual 
rewards.
2 Cinematic Rhythm Brief camera, hit-stop, impact-frame, and VFX bursts punctuate combat 
without replacing it.


---

## Page 2

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   2
# PILLAR PLAYER-FACING MEANING
3 Operative Identity vs. Vanguard Force
Echo emphasizes precision and controlled timing; Nova emphasizes speed 
and aggressive momentum; Crimson Vanguard embodies armor, pressure, 
and overwhelming force.
REVISED — CHARACTER MOTIVATION  Echo and Nova are Ascendant operatives entering the Shattered Ring to 
survive a live combat evaluation against Project Valor-7, an armored Vanguard unit designed to push 
enhanced fighters beyond their operational limits.
02
Real-Time Combat & Selectable Player Roster
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


---

## Page 3

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   3
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
03
Ascension Meter, Final Clash & Encounter Flow
The established meter, unlock, and failed-Clash recovery rules remain intact.
Ascension Meter
PRESERVED — METER DEFINITION  Ascension Meter is a visible 0–100 resource earned only through active 
combat decisions. It does not fill from waiting or elapsed time. Provisional gains remain subject to 
playtest tuning.
PLAYER EVENT METER GAIN DESIGN INTENT
Light-combo finisher +5 Small reward for sustained offense
Perfect dodge +12 Reward a clean defensive read
Successful counter +15 Reward converting the opening


---

## Page 4

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   4
PLAYER EVENT METER GAIN DESIGN INTENT
Impact Window success +20 Reward execution during an earned cinematic beat
Taking damage / waiting +0 Prevent passive progress
Final Clash unlock rule
REVISED — SINGLE GATE  The Final Clash becomes available only when BOTH conditions are true: Ascension 
Meter is full at 100 AND Crimson Vanguard’s health is at or below 25%. If one condition is met first, the 
Clash remains locked until the other is met. Once eligible, the player chooses to initiate the Clash with a 
contextual input during neutral or after a successful counter.
Final Clash resolution
OUTCOME RULE RETURN STATE
Success Complete both timing beats; the finishing sequence defeats Crimson 
Vanguard and ends the duel. Win screen
Failure
Separate both fighters; preserve current health with Crimson Vanguard 
held at a 1 HP floor; reduce meter to 50; apply a 3-second re-trigger 
cooldown.
Return to Neutral; rebuild meter 
and try again
PRESERVED — FAILED CLASH RECOVERY  A failed Final Clash does not restart the duel, kill the player 
automatically, or leave either fighter in a cinematic state. It creates a meaningful meter setback, restores 
valid combat states, and preserves a recoverable path to victory.
Encounter flow
BEAT PROVISIONAL RULE PLAYER EXPERIENCE
Opening Selection, abbreviated entrance, then immediate control Establish identity and stakes without delaying 
play
Phase 1 Readable armored pressure; onboarding Impact Window 
available Learn Crimson Vanguard’s rhythm
Phase 2 Begins at 50% Crimson Vanguard health; same attacks, 
stronger pressure Apply learned reads under stress
Climax Meter 100 + Crimson Vanguard health ≤25% Player chooses the Final Clash attempt
Win / Loss Final Clash success / selected fighter health reaches zero Complete duel loop


---

## Page 5

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   5
04
Crimson Vanguard — Authored Rival AI
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


---

## Page 6

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   6
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
05
Gray-Box Vertical Slice & Technical Milestones
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


---

## Page 7

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   7
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
06
AI-Assisted Development Architecture
Tools may accelerate production, but runtime behavior and creative acceptance remain 
authored and human-approved.
PRESERVED — HUMAN APPROVAL GATE  Generative tools may support ideation, reference exploration, 
documentation, and offline draft assets. No generated combat behavior, character asset, animation, VFX, 
sound, or text enters the course build without human review, technical validation, rights review, and 
explicit approval.
AREA ALLOWED SUPPORT COURSE-BUILD BOUNDARY
Design Brainstorming, comparison, tuning hypotheses, 
documentation drafts Designer approves all rules and numbers
Visual development Reference exploration and look-direction drafts Human-selected assets only; no automatic final 
import
Code support Offline implementation suggestions and 
debugging assistance
Reviewed source and authored Unreal runtime 
logic
Runtime opponent None Crimson Vanguard uses deterministic authored AI; 
no runtime LLM
Playable fighters None at runtime Player input controls Echo or Nova; no agent 
automation


---

## Page 8

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   8
07
Character Readability, Scale & Opening Flow
Three distinct combat identities remain legible inside one shared design family.
Character readability comparison
CATEGORY AGENT ECHO AGENT NOVA CRIMSON VANGUARD
Combat identity Precision and controlled timing Speed and aggressive momentum Armor, pressure, overwhelming force
Movement Deliberate spacing and counters Fast lateral rhythm and forward 
intent
Committed advances and short 
propulsion
Silhouette Lean, upright technical striker Compact, agile layered profile Substantially broader armored mass
Material family Matte black and charcoal technical 
suit
Black, charcoal, orange, light-gray 
helmet cap Red armor over black structure
Energy / VFX Controlled orange accents Cyan-white combat energy or 
selected telegraphs Red-orange systems and warning lights
Gameplay role Selectable player avatar Selectable player avatar Sole authored AI rival / boss
Readability target Exact timing and clear counter 
intent Momentum without visual noise Threatening reach with obvious tells 
and recovery
REVISED — COLOR DIRECTION  Echo keeps restrained orange accents. Nova’s existing black, charcoal, orange, 
and light-gray costume design is preserved; cyan-white is reserved for combat energy, telegraphs, or 
selected VFX accents when separation is needed. Crimson Vanguard reads through red armor, black 
structure, and red-orange systems and warning lights.
Character scale
Agent Nova stands 5'8", Agent Echo stands 6'0", and Crimson Vanguard stands 6'10". The rival is deliberately 
taller and substantially broader than either playable fighter, creating immediate threat and visual contrast 
while remaining within a scale that supports readable close-range martial-arts combat. The height difference 
must not create unfair hidden reach or collision behavior.
Character selection and opening flow
 Echo and Nova appear in a clean editorial character-selection interface.
 The player briefly moves between both options.
 Echo is selected in the current concept-video version.
 Technical and equipment panels animate around the selected fighter.
 The interface transitions into the established arena.
 The camera moves behind the selected fighter.
 Crimson Vanguard enters through the far doorway.
 The duel begins.


---

## Page 9

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   9
CONCEPT DIRECTION — OPENING PRESENTATION  The complete selection-to-arena transition describes the 
intended concept presentation. The course build may use a simplified selection screen and abbreviated 
arena entrance while preserving the same readable sequence.
CONCEPT VIDEO  Updated Concept Visualization — Link to be added.
08
Visual Assets & Official Version 1 Arena
Approved reference direction for the two selectable fighters, the boss rival, scale, and duel 
space.
Official arena direction
The established industrial Shattered Ring arena is locked as the official Version 1 environment. Alternate 
environment explorations do not replace it in the course prototype.
ARENA REQUIREMENT VERSION 1 FUNCTION
Central combat floor Open, readable space for spacing, lock-on, dodges, counters, and Final Clash staging
Far doorway Dedicated Crimson Vanguard entrance axis
Reverse third-person framing Clear camera position behind the selected fighter
Side-on readability Readable silhouettes and attack direction during lateral exchanges
Environmental reaction Visible but controlled reaction during major impacts without adding gameplay hazards


---

## Page 10

*[IMAGE REFERENCE SHEET: Character Scale Reference - no extractable text; see the PDF]*
MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   10
Character Scale Reference


---

## Page 11

*[IMAGE REFERENCE SHEET: Established Arena Reference - no extractable text; see the PDF]*
MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   11
Established Arena Reference


---

## Page 12

*[IMAGE REFERENCE SHEET: Agent Echo - Playable Precision Fighter - no extractable text; see the PDF]*
MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   12
Agent Echo — Playable Precision Fighter


---

## Page 13

*[IMAGE REFERENCE SHEET: Agent Nova - Playable Pressure Fighter - no extractable text; see the PDF]*
MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   13
Agent Nova — Playable Pressure Fighter


---

## Page 14

*[IMAGE REFERENCE SHEET: Crimson Vanguard / Project Valor-7 - Authored Boss Rival - no extractable text; see the PDF]*
MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   14
Crimson Vanguard / Project Valor-7 — Authored Boss Rival


---

## Page 15

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   15
09
Course Scope Lock & Future Expansion
Version 0.4 protects one complete duel as the course prototype.
SCOPE LOCK  The required prototype is complete when the player can select Echo or Nova, enter the official 
arena, fight Crimson Vanguard through both phases, earn and resolve Impact Windows, reach and retry 
the Final Clash, and finish with a valid win or loss. Recommendations beyond that loop are flagged as 
future scope.
Included in the course prototype
 One player versus one authored AI opponent.
 Two selectable player avatars using one shared core combat framework.
 One Crimson Vanguard boss with six states, four attacks, and a parameter-based Phase 2.
 One official industrial arena, one complete duel, and complete win/loss handling.
 Impact Window onboarding, Ascension Meter, Final Clash unlock, and failed-Clash recovery.
 Human approval gates and no runtime LLM-controlled fighters.
Deferred future scope
 Local or online PvP.
 Unique Echo and Nova move sets, separate balance systems, or extensive character cinematics.
 A playable Crimson Vanguard combat kit.
 Multi-enemy encounters, campaign progression, additional arenas, or extended enemy gauntlets.
 Transformations, second boss kits, additional characters, modes, weapons, or story chapters.
FUTURE SCOPE — NOT PART OF THE COURSE PROTOTYPE  Future PvP may allow Echo and Nova to fight each other 
or make Crimson Vanguard available as a heavyweight playable archetype, but this is outside the course 
prototype.
Definition of done
AREA ACCEPTANCE CONDITION
Combat Real-time controls remain responsive before and after every cinematic beat
Selection Either avatar enters the same complete shared-framework duel
AI Crimson Vanguard completes all six states and never strands the encounter
Phase 2 50% health escalation changes pressure parameters and presentation, not the attack set
Climax Final Clash obeys both unlock conditions and supports recovery after failure
Readability Echo, Nova, and Crimson Vanguard remain legible in motion and at combat distance
Scope One complete duel runs start to finish in Unreal Engine 5.8 on PC


---

## Page 16

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   16
10
Version 0.4 Revision Log & Open Design Decisions
Visible record of the character-structure update and the remaining decisions.
Revision log
SECTION VERSION 0.4 CHANGE STATUS
Executive Summary / Player 
Mode Nova changed from authored rival to selectable player; selection of Echo or Nova added Revised
Design Pillars / Motivation Three-way operative-and-boss contrast replaces Echo-versus-Nova conflict Revised
Core Loop / Meter / Final 
Clash All rival and health references now target Crimson Vanguard; established rules retained Revised
Rival AI / Phase 2 Crimson Vanguard became sole authored AI rival; six states, four attacks, and parameter 
escalation preserved Revised
Player Roster Shared player-kit scope rule added; unique kits and extensive cinematics deferred New
Character Readability Echo, Nova, and Crimson Vanguard comparison and cyan-white Nova combat-energy 
rule added Revised
Character Scale Supplied height reference and fair-reach/collision requirement added New
Selection / Opening Editorial selection and arena-entry concept flow added with simplified course-build 
allowance New
Visual Assets / Arena Five supplied reference sheets inserted; established industrial arena locked as Version 1 New
Future Scope PvP, multi-enemy encounters, campaigns, additional arenas, and gauntlets remain 
deferred Reaffirmed
Engine / Concept Video Engine corrected to Unreal Engine 5.8 / PC; honest concept-video placeholder added Revised


---

## Page 17

MULTI-AGENT AI FOR GAME DEVELOPMENT
ASCENDANT IMPACT  |  ASSIGNMENT #02   17
Provisional Design Decisions for Playtesting
DECISION PROVISIONAL VERSION 0.4 POSITION
Exact combat timing and meter tuning Keep all published timing ranges, gains, and thresholds provisional until playtest 
review.
Echo / Nova timing flavor Use the same mechanics and balance framework; approve only presentation-level 
timing flavor at first.
Nova cyan-white application Apply to combat energy, telegraphs, or selected VFX—not a costume recolor—unless 
later readability testing supports a broader application.
Signature cinematic variation Defer; consider one per fighter only after the shared base duel is stable.
Selection and entrance fidelity Use a simplified selection screen and abbreviated arena entrance for the course 
build.
Crimson Vanguard display name Use “Crimson Vanguard / Project Valor-7” formally; finalize the shorter in-combat UI 
label.
Scale, reach, and collision validation Validate gameplay collision and hit reach only after both avatars pass the same 
close-range tests.
Updated concept visualization Link remains pending; the document stands alone without it.
CENTRAL PROMISE  Real-time martial-arts combat rewards player skill with brief, earned anime-style 
cinematic spectacle.
