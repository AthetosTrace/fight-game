# Assignment 09 — Pre-Build Declaration

**Game:** *Ascendant Impact* — cinematic 1v1 cyber-fantasy action fighter, Unreal Engine 5.8, PC.
**Author:** AthetosTrace · **Submitted before any adversarial-agent code was written.**

---

**01. What does this agent test, and against what?**

The **live graybox duel** as it exists in `game/` — fifteen validated milestones of it —
not the GDD, and not `design-brief.md`. On 2026-08-23 the designer of record cut ship
scope (**D1–D4**, recorded in `design/decisions.md`): the Ascension Meter, Impact Windows
and the Final Clash are **deferred whole**, and health zero now wins the duel. An agent
built against those systems would be testing a game nobody is making.

So every invariant below is drawn from a **measured constant in
`game/docs/agent/PROTOTYPE_BLACKBOARD.md`** — a value someone read out of the live editor
and wrote down with its milestone — and cites the section it came from.

**02. What does "broken" mean, concretely, in this game's terms?**

Four classes, defined in full in [`ORACLE.md`](ORACLE.md) and encoded in
[`agent/contracts/oracle.json`](agent/contracts/oracle.json).

- **Boundary (B)** — a fighter leaves the ±650 combat axis, capsules interpenetrate below
  the 69 cm contact distance, or the side-ordering rule inverts while no crossing is active.
- **Stuck (S)** — a crossing that never closes, a mover left locked with the attack driver
  idle, a ragdoll below the floor plane, or the Vanguard parked legally outside its own
  attack range and never striking again.
- **Exploit (X)** — damage landing on a KO'd fighter, collision-ignore leaking past a
  knockout, punch cadence outrunning the re-entry guard, or a cancel loop that denies the
  Vanguard every attack it ever starts.
- **Logic (L)** — health outside `[0, max]`, both fighters KO'd with no resolution, a
  cancelled attack that still deals damage, or more than one damage event per strike.

**03. What does a failure look like — concretely?**

The Vanguard settles at 209 cm axis separation, inside its legal hold band but outside a
190 cm attack gate, and never attacks again for the rest of the match. *That one already
happened* — §16.4 failure 1 — and it is pre-registered here as a regression check rather
than discovered fresh.

A player lands from a jump-over inside the 78 cm minimum separation and the overlap
resolution pushes the Vanguard through `CombatAxisMax`. A punch thrown on the same frame
the strike impact fires trades both ways. `bCrossingActive` stays true after a knockout
because `StopMover` ran before the crossing cleared, and the two capsules ignore each other
for the rest of the session.

**04. What this agent will not claim**

`ORACLE.md` §4 pre-registers **nine known, accepted limitations** — no victory state after a
KO, the ~1-frame trade window, ragdoll-to-capsule drift, and the rest. They are documented
in the blackboard as intentional or deferred. **Reporting one of them as a discovery would
be worse than finding nothing**, so they are written down *before* the first run, and any
finding that matches one is filed as `KNOWN` and excluded from the headline count.

The harness also owns its own detection thresholds — sample cadence, how many frames a
clamp is allowed to correct within, how long counts as stuck. Those are **harness
parameters, not design values.** This agent changes no number in the game, and a value the
project records as OPEN or PROVISIONAL stays that way.

---

*Every invariant cites `PROTOTYPE_BLACKBOARD.md` by section, because the blackboard is the
only document that describes the game that actually exists. Where the GDD and the live
build disagree about what is built, the build wins — the GDD still wins about what the game
**is**, and deferring a feature is not redesigning it.*
