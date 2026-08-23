# Final push — Assignments 08, 09, 10

**Strategy and scope context.** Day-to-day work runs off `BOARD.md`; read `README.md` first.
Written 2026-08-23, updated after the repo consolidation.

---

## Repo consolidation — DONE 2026-08-23

Everything now lives in **`AthetosTrace/fight-game`**. The Unreal project was
subtree-merged out of `anthonytra785/ascendant-impact-ue` into `FightGame/game/`,
preserving all 103 commits and Anthony's authorship. No fork was made.

What changed:

- `9db3306` — Git LFS enabled on `fight-game` (`*.uasset`, `*.umap`, `*.uexp`, `*.ubulk`,
  `*.fbx`, `*.wav`, `*.ogg`, `*.mp3`). GDD PDFs and assignment JPGs stay plain blobs.
- `c10937b` (in the UE repo, carried across) — the octagon arena, its two checkpoints,
  and the three tier build scripts, which had been sitting untracked.
- `7466ea8` — `git subtree add --prefix=game`. 438 LFS files, ~136 MB, zero unsmudged
  pointers.
- The 264 MB standalone UE template that sat untracked at `FightGame\FightGame\` was
  moved to `C:\Users\athet\Documents\_archive\ue-template-arenagen\` and gitignored. Its
  one unique asset, `Lvl_ArenaGen_Seed8.umap` (Assignment 05 materializer output, no OFPA
  dependencies), is preserved in the archive.

`AscendantCapstone\ascendant-impact-ue` is now a **read-only archive**. Do not work there.
Do not push there.

Pushed to `AthetosTrace/fight-game` on 2026-08-23 — `main` plus all three assignment
branches, 469 LFS objects / 150 MB. The game is no longer single-disk.

### NOT YET DONE — needs a human

- [ ] **Open `AscendantCapstone\fightgame-a10\game\AscendantImpact.uproject` in UE 5.8 and
      PIE the duel.** Nothing is migrated until it plays. First open recompiles shaders from
      scratch — the worktree starts with no DerivedDataCache — so give it time.

Deliberately deferred past 23 Aug: no editor work happened on consolidation day. Structural
risk is low, because Unreal references are `/Game/`-relative and `/Game/` resolves to
`<project>/Content/` — the whole project root moved as one unit, so every reference still
points at the same relative place. What remains unproven is engine-level: plugin loading,
absolute paths in `Config/`.

**Bundle the verification with the Phase 1 packaging smoke test.** Both need compiled
shaders and cooking reuses the DDC the editor builds, so the first editor session is:
open → PIE the duel → immediately attempt a Windows Shipping package. One shader compile,
two risks retired.

---

## Where the work happens

| Assignment | Branch | Working directory |
|---|---|---|
| 08 — Narrative Engine | `assignment-08/narrative-engine` | `AscendantCapstone\fightgame-a8` |
| 09 — Adversarial QA | `assignment-09/adversarial-qa` | `AscendantCapstone\fightgame-a9` |
| 10 — Final game | `assignment-10/final-game` | `AscendantCapstone\fightgame-a10` |

A08 and A09 are worktrees cut from main *before* the import, so neither carries `game/`.
Keep it that way — they are text-only and do not need 136 MB of assets.

All three are worktrees. The primary `C:\Users\athet\Documents\FightGame` stays on `main`
as the trunk and nobody works in it.

**Hard rule: only ever open `fightgame-a10\game\AscendantImpact.uproject`.** `main` also
carries `game/`, so a second `.uproject` exists in the primary directory. Opening it builds
a second multi-GB DerivedDataCache and puts a second editor on the same `127.0.0.1:8000`
MCP port. One editor, one project, always the a10 worktree.

**Consequence:** A09's *code* is written in parallel. A09's *runs* and A10's editor work are
serialized on the one editor. Schedule them, do not race them.

---

## Deadlines

- **A08 — Tue 25 Aug**, optional, 10 pts, standalone.
- **A09 — Thu 27 Aug**, optional, 10 pts, must run against the capstone.
- **A10 — Tue 1 Sept** per the PDF, **mandatory**. (Adrian believes 7 Sept — still
  unconfirmed. Plan to 1 Sept until it is settled in writing.)
- **Internal target: playable build live Sun 30 Aug.**

---

## The gate that decides everything

A10 Deliverable 1: *a stranger opens a link and plays within 2 minutes with no setup
instructions.* No link or a broken link caps the **entire** assignment at 50%.

UE 5.8 has no WebGL target. The only route is package Windows 64-bit Shipping → zip →
itch.io via `butler`. First packages always break. Known suspects, visible in
`game/AscendantImpact.uproject`: `ModelContextProtocol`, `MCPClientToolset`, `Terminal`,
and `AllToolsets` are enabled with **no `TargetAllowList`**. Those are editor plugins.
`ModelingToolsEditorMode` is already correctly allowlisted to Editor — copy that pattern.

Everything to date has only ever run in PIE. Nothing has been proven in a cooked build.

---

## THE SCOPE CUT — what Ascendant Impact actually ships as

The game as envisioned in the GDD is far out of reach in nine days. What exists is already
a coherent, shippable game if we stop calling it a prototype of something bigger and
commit to what it is.

### What it is

**A 2.5D boss duel in a 3D arena.** Two fighters on a constrained combat axis, moving left
and right, with a jump that crosses over the opponent and swaps sides. Fixed duel camera.
One boss. One arena. One match.

This is not a compromise imposed by the deadline — it is what the systems already enforce.
`BP_VanguardDuelMover` clamps the player to ±650 on the combat axis and holds the Vanguard
in a depth lane. `BP_DuelCameraRig` pins the camera to one arena side and never flips.
Leaning into it costs nothing and makes the build read as deliberate.

### CUT — write these into the GDD addendum as explicitly descoped

1. **Free 3D movement.** Combat stays on the constrained axis. Already true.
2. **Ascension Meter and Final Clash.** The whole Assignment 07 subject. A meter, a gated
   finisher, new UI, new state, a new montage. The single biggest cut and the right one.
3. **Combo system / multiple attacks.** One punch. A heavy is a stretch goal, not a plan.
4. **Boss phase 2.** One phase, tuned well, beats two phases tuned badly.
5. **Character roster.** One player, one boss.
6. **Story, cutscenes, narrative framing.** Assignment 08's DM agent is a separate
   deliverable and does not feed the build unless it comes free.
7. **Multiple arenas.** The octagon, and only the octagon.
8. **Animation authoring.** Template locomotion, template hit reactions, template ragdoll.
   Known foot-skate at 1.1 stature and known jump-timing mismatch at 1.9 gravity are both
   accepted and documented, not fixed.

### KEEP — the six things that make it a game

In priority order. This order is also rubric order.

1. **Match loop.** Intro → fight → KO → result screen → restart. There is currently no way
   to win, lose, or play again; someone ragdolls and nothing happens forever. **This
   outranks every art task.** A pretty build a stranger cannot finish fails the gate; an
   ugly build with a win/lose/restart passes it. *~1 day.*
2. **Balance so the boss sometimes wins.** Both fighters are 100 HP dealing 10. Player
   punch cadence has never been measured against the Vanguard's 0.65 decision chance.
   Measure first, then tune to roughly a 60–70% player win rate. *~0.5 day.*
3. **The octagon as the venue.** Worth 3 rubric points, not just looks — see below.
   *~1 day.*
4. **Title and controls screen.** "Without setup instructions" means the build teaches
   itself in ten seconds. *~0.5 day.*
5. **Minimal audio.** Hit, whiff, KO, arena ambience. Not in any rubric line, but a
   silent fighting game reads as broken inside the exact window the gate measures.
   *~0.5 day.*
6. **Packaged build on itch.io.** *~1 day, front-loaded because it will break.*

Roughly 4.5–5 days of focused work against 9 available. Feasible **if** the packaging risk
is retired in the first 48 hours rather than discovered on submission night.

### Why the octagon swap is worth 3 points

A10's *Pipeline-to-Game Connection* (3 pts) requires shipped content **traceably produced
by the pipeline**. The octagon was generated by `game/Tools/ArenaPipeline/`, with run
evidence already committed under `game/reports/arena/`. Ship on the flat graybox and that
evidence points at nothing in the build. Ship in the octagon and the connection is
demonstrable on video.

### The open geometry question A10 must close

The octagon is **1590 cm apothem** (`build_octagon_tiers.py`). The duel arena clamps the
player at **±650 cm**. So the fighters would use a 1300 cm strip in the middle of a 3180 cm
space. This is the unresolved U1 question from `ARENA_PIPELINE_FINDINGS.md` §4.2 — "is the
arena 1300 cm or 2400 cm?"

**Cheapest resolution: keep the ±650 combat bounds and centre them in the octagon.** The
surrounding space reads as arena depth and backdrop, which is exactly what an octagon
gallery is for. Widening the clamps means re-tuning spacing, camera framing, and the
Vanguard's approach behaviour — all of it re-validated. Do not widen the clamps unless the
fight visibly feels cramped, and record the decision either way.

---

## Phase plan

**Phase 0 — today (23 Aug).** Repo consolidation ✅. Human verifies the editor opens and
PIE runs. Push to origin with LFS. A10 writes the GDD cut addendum and the detailed build
plan. **No gameplay changes today.**

**Phase 1 — package early (24–25 Aug, A10).** Package `Lvl_DuelGraybox` exactly as it
stands, Windows Shipping. Not to ship it — to find what breaks while there is still a week.
Create the itch.io page, get `butler` pushing. Exit condition: a zip on itch.io that
launches, even if the game inside is still a graybox.

**Phase 2 — A08 (24–25 Aug, parallel, no editor contention).** DM agent, Python + Claude
API. JSON facts ledger driven by player *actions*, dialogue reactive to ledger state,
consistency across 5+ turns, README covering world / ledger / one surprising moment. Set it
in the Ascendant Impact world so the GDD supplies the worldbuilding for free. **First thing
that window resolves: the API key.** There is none on this machine at any scope, and A10's
cost analysis needs real token counts too.

**Phase 3 — A09 (26–27 Aug; runs serialized with A10).** Adversarial tester driving PIE
over the Unreal MCP. Not a detour — it is A10's QA pass. Hunt: arena clamp ±650, min
separation 78, side deadzone 20, crossing threshold 50, landing inside min-sep, crossings
that never close, punch-spam cadence, damage applied to a ragdolled fighter,
`bCrossingActive` collision-ignore leaking after a KO, health below 0, double knockout,
telegraph cancelled mid-windup. Output JSON with `location`, `error_type`, `game_context`.

**Phase 4 — make it a game (26–30 Aug, A10).** The six KEEP items, in order.

**Phase 5 — submission (31 Aug – 1 Sept).** Playable link, pipeline repo link, run video,
and the one-page audit: what the pipeline produced, remaining manual steps and what would
remove them, one architectural decision to change with its specific alternative, actual run
cost, most expensive step, solo-dev sustainability, before/after cost reduction.

---

## Open items needing Adrian

- [ ] Confirm the A10 due date in writing — 1 Sept or 7 Sept.
- [ ] Anthropic API key. None on this machine (process, User, or Machine scope). A08
      requires "Python using the Claude API"; A10 requires a **real** run cost, not a
      hypothesis, plus a before/after token comparison. ~$5 of credit covers it.
- [ ] Verify the migrated project opens and plays in the a10 worktree.

---

## Standing rules for every window

- PowerShell, not Git Bash — Git Bash rewrites Unreal `/Game/` paths.
- One branch touches `.uasset`/`.umap` at a time. They are binary; git cannot merge them.
  A09 is text-only for this reason; A10 owns the editor.
- Never open two Unreal editors on the same project.
- Duplicate a level to a checkpoint before changing approved geometry.
- MCP payload scripts define `run()` and must be made to **call** it, or they silently
  no-op and look like success.
- `NameError` on `execute_tool` under plain `python` is expected — those scripts only run
  inside the editor.
- PIE advances in real time between MCP calls; an idle player takes live hits.
- Compiling a Blueprint mid-PIE reinstances the pawn and kills Slate-injected input —
  restart PIE after any mid-session compile.
- `game/CLAUDE.md` and `game/AGENTS.md` came across from the old repo and still describe
  the old two-repo split and the dead never-edit rule. **A10 should reconcile them** before
  they misdirect a session.

---

## Instrument costs from the first API call

A10 wants a before/after cost-reduction comparison computed from a real run. Capture
`usage.input_tokens` and `usage.output_tokens` per call into the run JSON from the very
first call in A08. Reconstructing it later is guesswork, and the rubric says so explicitly.
