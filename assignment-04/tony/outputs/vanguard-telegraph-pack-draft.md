# Crimson Vanguard — Telegraph and Readability Pack

*Offline design reference only. Not shipped game code, not shipped dialogue.*

## The six-state loop

Crimson Vanguard's behavior runs on a fixed, authored cycle — a deterministic state machine, never a learning or runtime-adaptive system. The order never changes:

**Idle / Reposition → Select Attack → Telegraph → Active Attack → Recover → Return to Neutral**

- **Idle / Reposition.** Crimson Vanguard holds its line, facing the player under armored pressure, closing or holding range until it has valid range and line to commit. This state reacts deterministically to range and cooldown — a fixed, authored rule set, not a learned response to the player's habits.
- **Select Attack.** One of the four authored attacks (A–D) is chosen by an authored rule keyed to current range and cooldown. This selection is conditional, not adaptive: the same range and cooldown state always produces the same authored choice.
- **Telegraph.** Crimson Vanguard shows a committed pose, warning-light buildup, and directional sound cueing before it acts — the moment the player is meant to read.
- **Active Attack.** The chosen attack's authored movement, gauntlet force, hitbox, reach, or propulsion executes.
- **Recover.** A deliberate, exposed opening follows every committed strike — the punish opportunity the player earns by reading the telegraph correctly.
- **Return to Neutral.** Attack flags clear and locomotion restores, closing the loop back to Idle / Reposition.

Every duration above belongs to the human designer and is provisional pending playtest; none is restated with new values here.

## The four authored attacks

*Exactly four attacks exist: A, B, C, D. No fifth attack, no renamed or merged attack, and no phase-exclusive attack appears anywhere in this pack.*

### Attack A — Close-range committed gauntlet force
**Proposed working name (new authored content, pending designer review, not an established GDD fact): "Fault Line"**

Readability requirement: a distinct wind-up and a punishable recovery.

Playtest readability shorthand (internal designer-facing copy for use during playtesting — not shipped dialogue): "Watch the gauntlet load — the moment it commits, the counterattack window opens."

### Attack B — Committed forward-pressure sequence
**Proposed working name (new authored content, pending designer review, not an established GDD fact): "Advance Line"**

Readability requirement: a visible first beat and a stable tracking limit.

Playtest readability shorthand (internal designer-facing copy for use during playtesting — not shipped dialogue): "First beat is the tell — track the limit, don't outrun it."

### Attack C — Armored reach and space control
**Proposed working name (new authored content, pending designer review, not an established GDD fact): "Bulwark Reach"**

Readability requirement: clear body direction and visible active range.

Playtest readability shorthand (internal designer-facing copy for use during playtesting — not shipped dialogue): "Body tells you the line — active range is wide, so respect it before you close."

### Attack D — Short propulsion-assisted approach
**Proposed working name (new authored content, pending designer review, not an established GDD fact): "Thruster Snap"**

Readability requirement: a thruster cue before movement, with no hidden full-arena snap.

Playtest readability shorthand (internal designer-facing copy for use during playtesting — not shipped dialogue): "Thruster flares first — the approach is short, never a surprise cross-arena hit."

## Phase 2 escalation

At 50% health, Crimson Vanguard's phase change commits on Return to Neutral and is signaled once with stronger thruster output, warning lights, sound, and armor-energy presentation. The same four authored attacks carry forward — no fifth attack, no transformation, no second move set. Attack weighting shifts toward more aggressive close-range and gap-closing selection, and reposition delay shortens — both still fixed, authored responses to range and cooldown, not learned or player-pattern-adaptive behavior. Exact durations remain the designer's provisional numbers and are not restated here.

## Note on authored reactivity

Crimson Vanguard is not "non-reactive." Its Idle/Reposition and Select Attack states respond to range and cooldown by design — that is conditional authored logic, executed the same way every time a given condition recurs. What never happens is learning from player behavior, adapting across playthroughs, or any runtime call to a model. The distinction is deterministic condition-checking versus learning — only the latter is out of scope.