# Ship plan — Ascendant Impact, 23 Aug → 1 Sept 2026

**Written 2026-08-23. Nine days to ship.** This is the operational plan for the
final stretch. It supersedes the milestone status in the root `CLAUDE.md`, which
is stale by fifteen build milestones.

**Partner status:** Anthony is unresponsive. The user (AthetosTrace) is now sole
commander and designer of record. Every call below that touches design is theirs
and was made on 2026-08-23.

---

## 1. Where the build actually is

The Unreal project is in-tree at `game/` (subtree, 2026-08-23, Git LFS). Fifteen
milestones are complete and validated in PIE. Milestone detail lives in
`game/docs/agent/PROTOTYPE_BLACKBOARD.md`.

**Working today**

- Player: movement, jump-over with dynamic side switching, punch (10 dmg,
  `MM_Attack_01`), health 100, hit-react, camera shake, ragdoll death.
- Vanguard: range-band AI mover with hysteresis and depth wander, directional
  locomotion (`ABP_VanguardLocomotion`), **one** telegraphed strike
  (1.1 s "!" windup, 10 dmg, 2.5–4 s cooldown, 0.65 fire chance, interruptible
  before impact, depth-dodgeable at 55 cm), health 100, ragdoll KO.
- 2.5D duel camera rig, arena bounds ±650, mutual facing.
- `UI_DuelHUD` — both health bars, timer-driven, interpolated.
- `BP_DuelKnockoutCoordinator` — either fighter at 0 HP falls and stays down.
- Octagon arena blockout `Lvl_ArenaOctagon` — two-tier gallery, truss walls,
  script-generated from `Tools/ArenaPipeline/build_octagon_*.py`.

**The two real gaps, named plainly**

1. **The player wins nearly every time.** Punch has no recovery cost and there is
   no dodge, block or counter. Mashing LMB ten times ends the fight. Nothing in
   the game asks the player to read anything.
2. **The Vanguard has one move forever.** No variety, no phase change, no punish
   of player recovery, no pressure.

Neither is a tuning problem. Both are missing systems, and both are on the
critical path to "somewhat playable".

**Also missing:** win/loss resolution (at 0 HP a body drops and nothing happens),
restart, round timer. Everything is gray prototype material. The project default
map is still the stock UE template level.

---

## 2. Decisions made 2026-08-23 (designer of record)

| # | Decision | Consequence |
|---|---|---|
| **D1** | **Health-zero wins the duel.** Ascension Meter, Impact Window and Final Clash are **deferred future scope**. | **Amends Q22**, previously marked settled and binding ("the Final Clash is the only way to win"). Releases constraints C1/C2/C3 and retires open item 64. `MinHealthFloor` stays 0 — no gate. |
| **D2** | The Vanguard gets **three attacks**. Phase 2 is **optional**, taken only if the calendar allows. | Scopes `AGENTS.md`'s "only Attack A is enabled" rule to the **paused DataTable route**, which is where it was aimed. The graybox driver may carry three attacks. All values remain provisional and pending playtest. |
| **D3** | Character look = **material-instance recolor** as the guaranteed floor. A free Fab/Mixamo character swap is **optional**, attempted only if the duel is finished early. Preferred, not vital. | Arena materials and lighting proceed regardless — `CLAUDE.md` permits dressing proxies with free assets during M1–M4. |
| **D4** | The `DT_VanguardAttacks` / `S_VanguardAttackDef` DataTable route **stays paused permanently** for this ship. | Anthony's signed approval packet and the missing countersignature are **moot for the ship** — the route it authorizes is not being taken. The V1–V5 cinematic-restore corrections likewise stop being a ship blocker, because there is no cinematic restore to correct. |

D1 and D2 must be written into `design/decisions.md` as recorded amendments
before the work starts, so no later agent re-litigates them.

---

## 3. The plan — three tracks

Track 1 is the critical path. Track 2 runs in any gap and never touches combat
Blueprints. Track 3 is the one thing most likely to be left too late.

### Track 1 — make the fight a fight

| # | Task | Acceptance | Est |
|---|---|---|---|
| **T1** | **Fight-end resolution + restart.** Victory/Defeat panel on `UI_DuelHUD`, duel ends, R restarts. | At 0 HP either way, a result appears within 2 s and R produces a clean fresh duel with all flags reset. | 0.5 d |
| **T2** | **Player attack commitment.** Punch gains recovery frames and a 3-hit string (`MM_Attack_01/02/03`). Mashing commits you to whiff recovery. | Continuous mashing at range leaves measurable punish windows. Landing all three costs more than one punch but risks more. | 0.5 d |
| **T3** | **Player dodge with i-frames.** Directional dash on `MM_Dash` (already in Content), ~0.28 s invulnerability, cooldown. | A correctly timed dodge beats every Vanguard attack. A mistimed one gets hit. Dodge cannot be spammed to cross the arena. | 0.75 d |
| **T4** | **Vanguard three-attack set.** Fast jab (short telegraph, short range, low dmg) · mid swing (today's strike) · heavy (long telegraph, high dmg, long punish window). Range-gated weighted selection with a no-repeat rule. | Three visually and temporally distinct telegraphs. Selection depends on distance. The same attack never fires three times running. | 1.0 d |
| **T5** | **Pressure and punish.** Shorter and more variable cooldowns, closes distance decisively, and attacks into the player's recovery frames. | Standing still loses. Mashing loses. Reading and dodging wins. | 0.5 d |
| **T6** | **Balance pass.** Health and damage tuned so a mashing player loses and a reading player wins comfortably but not automatically. | Ten hand-played duels; the outcome is not a foregone conclusion in either direction. Numbers stay provisional. | 0.5 d |
| **T7** | *Optional* — **Phase 2** at ≤50% Vanguard health: telegraph and cooldown scale factors. | Visible behavioural change at the threshold. | 0.5 d |
| **T8** | *Optional* — **round timer**, 3–5 min, with a time-out result. | Duel resolves on the clock as well as on health. | 0.25 d |

**T1 → T6 is the definition of playable.** Everything after T6 is upside.

### Track 2 — styling, in descending value per hour

| # | Task | Why this order | Est |
|---|---|---|---|
| **S1** | **Move the duel into `Lvl_ArenaOctagon`.** Verify ±650 combat bounds and spawns inside the octagon, migrate the duel actors, set it as `GameDefaultMap` and `EditorStartupMap`. | The arena already exists and is unused. Biggest look change available for the least work. | 0.5 d |
| **S2** | **Lighting + post-process.** Directional + sky + fog, arena spot rig, bloom, colour grade, vignette. | Highest visual return per hour in the entire plan. A lit gray box stops reading as a gray box. | 0.5 d |
| **S3** | **Arena material pass.** Real materials on floor / truss / gallery / accent, driven back through the build script. | The arena is script-generated, so a material pass is a parameter change and a re-run, not hand-placement. | 0.5 d |
| **S4** | **Character recolor.** Material instances — crimson and dark for the Vanguard, cyan-white for Echo. | Two distinct fighters for two hours of work and zero rig risk. | 0.25 d |
| **S5** | **Feel pass (M5).** Hit-stop on impact, camera push-in on heavy hits, hit and whiff sounds. **Only after T6.** | Cheapest perceived-quality gain in the project — and it is the tuned work that `CLAUDE.md` gates behind a stable complete duel. | 0.5 d |
| **S6** | *Optional* — **Fab/Mixamo character swap.** Research a free licensed humanoid, retarget onto the existing ABP and dynamic-montage path. | Preferred but not vital, and retargeting can break the validated animation path. Attempt only from a finished duel. | 1.0 d |

S1–S4 are **asset dressing**, which `CLAUDE.md` explicitly permits during M1–M4:
"Picking a proxy asset is asset selection, not a presentation pass." S5 is the
tuned M5 work and waits for a stable duel.

### Track 3 — shipping

| # | Task | Est |
|---|---|---|
| **P1** | **Packaging spike — run it on 24 Aug, not on 31 Aug.** This project has never been packaged. The default map is wrong, and `ModelContextProtocol` is an Editor-only plugin. First-package failures in UE 5.8 routinely cost a day. Find the breakage while there is time to absorb it. | 0.5 d |
| **P2** | Final package, full playtest, gameplay capture, submission. | 0.5 d |

---

## 4. The calendar

| Date | Work | Milestone |
|---|---|---|
| **Sun 23 Aug** | Planning. Record D1 and D2 in `design/decisions.md`. Truth-pass the root `CLAUDE.md`. | — |
| **Mon 24 Aug** | **T1** fight-end + restart · **T2** attack commitment · **P1** packaging spike | first real win/loss |
| **Tue 25 Aug** | **T3** dodge + i-frames | **counterplay exists — defensible floor** |
| **Wed 26 Aug** | **T4** three-attack set | the fight stops repeating |
| **Thu 27 Aug** | **T5** pressure + **T6** balance | **PLAYABLE — complete duel, both outcomes, honestly contested** |
| **Fri 28 Aug** | **S1** arena swap · **S2** lighting + post | the game stops looking like a prototype |
| **Sat 29 Aug** | **S3** arena materials · **S4** character recolor | visual identity |
| **Sun 30 Aug** | **S5** feel pass · optional **T7** Phase 2 | polish |
| **Mon 31 Aug** | Buffer. Optional **S6** character swap or **T8** timer. **P2** package + capture. | shippable |
| **Tue 1 Sept** | Submit. | **SHIP** |

**Answers to the two questions this plan was written for:**

- **How fast to playable — 27 August, four working days from now.** There is a
  defensible floor two days earlier: after T3 on 25 August the game has win/loss
  resolution, an attack that costs something, and a dodge that rewards reading.
- **When styling starts — 28 August for the full pass, and any earlier gap for
  S1–S4**, because arena and material dressing is asset selection and does not
  wait on M4. Fastest order is lighting → arena materials → character recolor,
  which is strictly descending return per hour. Only the feel pass (S5) is
  genuinely gated on a stable duel.

Three optional items (T7 Phase 2, T8 timer, S6 character swap) are the release
valve. If any day slips, they are what gets cut — in that order, S6 last because
it is the one the designer of record wants most.

---

## 5. Risks, in order of how much they would cost

| Risk | Mitigation |
|---|---|
| **First package fails and eats a day.** Never packaged; wrong default map; Editor-only plugin enabled. | **P1 on 24 August.** Do not defer this. |
| **Retargeting a Fab/Mixamo character breaks the animation path** that fifteen milestones validated. | S6 is optional and last. The recolor (S4) is the guaranteed floor and ships regardless. |
| **Balance is subjective and can absorb unlimited time.** | T6 is timeboxed to half a day and ten hand-played duels. Values stay provisional; perfect is not the bar. |
| **One `.uasset` edited from two branches at once** — binary, unmergeable, always loses a side. | One branch touches assets at a time. Already the standing rule in `.gitattributes`. |
| **Agents re-litigate D1 or D2** because Q22 is recorded as settled and binding. | Write both amendments into `design/decisions.md` **before** the first build task starts. |
| **Editor open in more than one place** while MCP agents are working. | Single editor session. Confirmed working practice as of 2026-08-23. |
