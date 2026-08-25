# Assignment 09 — An Adversarial QA Agent for *Ascendant Impact*

**Game:** *Ascendant Impact* — a cinematic one-versus-one cyber-fantasy martial-arts
action fighter. Unreal Engine 5.8, PC, Blueprint-only.
**Author:** AthetosTrace · **Repo:** `AthetosTrace/fight-game`
**Run date:** 2026-08-24, against the live editor over Unreal MCP.

An agent that runs inside the game and actively tries to break it. It cycles
behaviours, samples duel state from the running PIE session, and reports every
violation of a written oracle as structured JSON and CSV.

**It found a real, reproducible, S1 defect that lets the player walk out of the arena.**

---

## What it tests, and why not the GDD

On 2026-08-23 the designer of record cut ship scope (**D1–D4**, recorded in
`design/decisions.md`). The Ascension Meter, Impact Windows and the Final Clash are
**deferred whole**; health zero now wins the duel. An oracle built on the GDD's combat
economy would be testing a game nobody is building.

So every invariant is derived from a **measured constant in
`game/docs/agent/PROTOTYPE_BLACKBOARD.md`** — a value read out of the live editor across
fifteen milestones — and cites the section it came from.

**The agent verified those constants against the live build before testing anything.**
All 23 checkable values matched exactly — `CombatAxisMin/Max` ±650, `MinimumAxisSeparation`
78, `WindupDuration` 1.1, `AttackCooldownMin/Max` 2.5/4.0, `ImpactDepthTolerance` 55, and
the rest. Zero mismatches. The blackboard is accurate, and the oracle rests on real values.

---

## Run it

```bash
# the editor must be open on Lvl_DuelGraybox with the MCP server started:
#   ModelContextProtocol.StartServer      (bAutoStartServer defaults to false)

python assignment-09/agent/agent.py --seed 7 --dt 0.2 --out evidence/runs/live-seed7
```

```
assignment-09/
├── PRE-BUILD-DECLARATION.md      committed before any agent code
├── ORACLE.md                     what "broken" means — written before the driving code
├── agent/
│   ├── contracts/oracle.json     25 invariants + 9 known limitations, as data
│   ├── mcp_client.py             JSON-RPC over the plugin's Streamable-HTTP transport
│   ├── pie_backend.py            resolves duel actors, samples state, injects input
│   ├── session_script.py         the behaviour loop, rendered to run INSIDE the editor
│   ├── oracle_checks.py          the oracle, executable — one checker per invariant
│   └── agent.py                  run entry point, triage, report emission
└── evidence/runs/                three runs: report.json, report.csv, samples.csv
```

## What "broken" means — the strategy

The oracle was written and committed **before any driving code**, per sprint task `Q01`.
Four classes, 25 invariants, severity-rated:

| Class | Examples |
|---|---|
| **Boundary** | fighter leaves ±650 · capsules interpenetrate below 69 cm · side ordering inverts |
| **Stuck** | a crossing that never closes · mover locked with the driver idle · the Vanguard parked outside its own attack range |
| **Exploit** | damage onto a KO'd fighter · collision-ignore leaking past a knockout · a cancel loop denying every attack |
| **Logic** | health outside `[0, max]` · both fighters KO'd · two damage events from one strike |

Two invariants are **pre-registered regressions, not hypotheses** — `S3` is the §16.4 bug
where the Vanguard settled at 209 cm and never attacked again, and `X3` is the crossing
collision-ignore leak that §22 added `StopMover → SetCrossingCollisionEnabled(false)` to fix.

Nine **known limitations** were written down before the first run — no victory state after
a KO, the ~1-frame trade window, ragdoll-to-capsule drift — so no run could pass an
accepted behaviour off as a discovery.

---

## What the agent found

Three runs (seeds 7, 21, 3), 35 samples each, ~78 s of duel per run.

| Invariant | Sev | Runs | What it is |
|---|---|---|---|
| **X7** | S1 | **3/3** | Position constraints stop being enforced after a knockout |
| **B3** | S1 | **3/3** | Capsule interpenetration — separation down to **0.2 cm** against a 69 cm contact distance |
| **B1** | S1 | 2/3 | Player outside the arena at **x = 689.4** (bound is 650) |
| **B5** | S2 | 2/3 | Side ordering inverted — `CurrentSideSign` says right, the Vanguard is left |

All four are one causal chain.

### The headline: a knockout switches off every position constraint

`BP_VanguardDuelMover.ApplyConstraints` is, in the blackboard's own words (§14.1), *"the
single authority for all fighter position constraints"* — arena bounds, minimum
separation, side ordering, depth lane. On knockout,
`BP_DuelKnockoutCoordinator.StopMover` calls `SetActorTickEnabled(false)` on the mover
(§18.1).

**`ApplyConstraints` runs on that tick.** Disabling the mover disables every constraint in
the game at once.

The measured before-and-after, from `live-seed21/samples.csv`:

```
   t   action    plyX    vanX     sep   vanHP   vKO
45.33   punch    572.0   650.0    78.0     10   False     <- constraint holding, exactly 78
48.33   punch    602.5   650.0    47.5      0    True     <- KO fires; separation collapses
50.66   punch    691.3   650.0    41.3      0    True     <- player 41 cm outside the arena
57.00   punch    691.3   650.0    41.3      0    True
63.33   punch    691.3   650.0    41.3      0    True
```

Separation sits pinned at **exactly 78.0** — `MinimumAxisSeparation` — for as long as the
Vanguard is alive. The instant `bVanguardKO` flips true it collapses to 47.5, and the
player walks to **x = 691.3**, past a bound of 650, and stays there.

### How the agent got there

Punch-spam. Each punch advances the player, and the min-separation rule pushes the Vanguard
ahead of it, so a looping punch **walks the Vanguard into the arena wall**, pins it at
`CombatAxisMax` where it cannot retreat (§14.1 suppresses retreat within 5 cm of the
bound), kills it there — and then the constraints vanish and the player strolls out through
the corpse.

### This is not the accepted limitation K6

`K6` accepts that after a KO the surviving player can walk, jump and punch freely. It does
**not** accept leaving the arena or passing through the other fighter's capsule. §15.3
recorded that overlap below 69 cm *never occurred* in validation. It occurs now, at 0.2 cm.

### Why it matters for the ship

Sprint task `G07` (octagon swap) carries the acceptance criterion **"no geometry the player
can get stuck on or escape through."** That cannot be met while a knockout disables
containment. `G05` (match loop) is the natural fix site: whatever ends the match must keep
constraints alive, or re-assert them, after the KO.

**The agent does not propose the fix.** Whether constraints move off the mover tick, or the
coordinator re-asserts them, or the match loop freezes both fighters, is an architecture
decision — and every value in this project is the designer of record's.

---

## Were we surprised?

**Yes, twice.**

**The bug was in the shutdown path, not the combat.** We expected to break the fight — the
telegraph, the dodge window, the damage budget. Instead the fight held up well: damage was
exactly 10 every time, min-separation held at exactly 78 under sustained punch pressure,
health never left `[0, 100]`, and no double-KO occurred. What broke was **the code that
runs when the fight ends.** Fifteen milestones of validation all tested a *live* duel;
nobody had adversarially tested the seconds *after* one.

**The strongest hypothesis in the oracle never fired.** `X6` predicted the Vanguard would be
cancel-locked — 1.4 s of cancellable windup against a 2.5–4.0 s cooldown that a cancel
rerolls in full. It stayed silent. Not because it is wrong, but because the harness cannot
resolve it (below), and because a punch-spamming player kills the Vanguard in about ten
seconds — faster than the exploit needs to matter. **`X6` is unproven, and it is written up
here as unproven.**

The third surprise was smaller and about us: **the first run reported six defects and two
were our own fault.** Sampling at a 2.7 s interval, the agent "saw" the Vanguard idle for
15 s while the player's health dropped 90→80→70 — it was attacking the whole time, and the
entire 2.7 s attack cycle fell between samples. That produced a false `S3` (the stall
regression) and a false `L5` (two damage events in one strike). Both were traced, both were
suppressed by making timing checks require a sample interval fine enough to resolve them,
and **neither appears in the final report.**

---

## Harness limits, stated plainly

- **Sample rate floors at ~2.0–2.3 s.** Each `execute_tool` inside the editor costs ~0.29 s
  on the game thread, and a sample needs seven. That cannot resolve a 1.1 s windup or a
  0.6–0.7 s crossing window, so **every timing-based invariant is suppressed rather than
  guessed at** — `S1`, `S3`, `L3`, `L5`, `X6` are all gated on an interval the harness never
  achieved. They are untested, not passed.
- **The position-based findings are immune to this.** `B1`, `B3`, `B5` and `X7` compare
  coordinates within a single sample. Sample rate cannot manufacture a player at x = 691.3.
- **Input injection reaches LMB and SpaceBar only.** Slate `Click` on the editor window
  fires `IA_Attack`; `PressKey "SpaceBar"` reaches Enhanced Input. There is no key-hold, so
  **sustained WASD locomotion is not injectable** and directional boundary probing was not
  performed. The out-of-bounds finding came from punch-driven advance, not steering.
- **No scripted repositioning was used.** Every finding came from real injected input and
  observed state. Nothing was teleported into place, so no finding is a harness artefact of
  that kind.

## Provenance

The agent is read-only over gameplay: it samples properties and injects input. It never
edits an asset, never writes a design value, and never resolves anything the project records
as OPEN or PROVISIONAL. Every constant it checks against remains provisional and pending
playtest.

`X7` was **found empirically and formalized afterwards** — `B1`, `B3` and `B5` caught the
symptoms on seed 7, and `X7` was added to name the shared cause and confirm it on further
seeds. The contract records that discovery order rather than implying it was predicted.
