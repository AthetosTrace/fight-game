# FINISH PLAN — Ascendant Impact

**Written 2026-09-02.** This is the only plan file. Everything left to do on this
project is a numbered step below. When a step is done, tick its box and add one line
under **Log**. Nothing else in this repo tells you what to build.

**The goal:** a duel a stranger can open, play, win, and lose — that looks like a game
rather than a gray box. Not the full GDD. That version is deferred and is not coming
back before this ships.

---

## Status

Change a row's status as work lands. `start-session.ps1` reads this table to tell you
what is next, so it is the one place that has to stay honest.

| Step | What | Status |
|---|---|---|
| 1 | Prove the packaged build launches | `todo` |
| 2 | Win, lose, and restart | `todo` |
| 3 | Vanguard's second attack | `todo` |
| 4 | The anti-kite attack | `todo` |
| 5 | Balance until it is a fight | `todo` |
| 6 | Research the art assets | `todo` |
| 7 | Apply the character art | `todo` |
| 8 | Arena lighting and materials | `todo` |
| 9 | Title screen and controls | `todo` |
| 10 | Audio minimum | `todo` |
| 11 | Package and publish the playable link | `todo` |
| 12 | Assignment 10 submission | `todo` |

Statuses: `todo` · `in-progress` · `done` · `cut`

---

## The four problems this plan exists to fix

Named by Adrian, in his words:

1. **Can't win** — the Vanguard hits 0 HP, ragdolls, and nothing happens. Forever.
2. **Can't lose** — same in reverse. No fail state, no restart.
3. **Backing up wins every time** — the Vanguard is slower than you, so you kite him.
4. **Only one NPC attack** — one telegraphed strike on repeat.

Steps 2–5 close all four. Everything after that is presentation and shipping.

---

## Standing rules for this plan

- **Never commit Blueprint or Unreal binary assets.** No `.uasset`, no `.umap`, no
  `Content/` binaries, ever, in any commit made by an agent. They are LFS-tracked
  binaries that git cannot merge, and a bad merge silently loses a side. Commit code,
  docs, config and scripts only. If assets changed and need committing, **Adrian does
  it by hand.** An agent that stages a `.uasset` has broken this rule.
- **One editor at a time.** The MCP binds `127.0.0.1:8000` and the port has one owner.
- **Checkpoint before geometry.** Duplicate the level into
  `/Game/AscendantImpact/Maps/Checkpoints/` before changing approved geometry.
- **Every number is provisional** until Adrian plays it. An agent proposes values; it
  never settles one.
- **Nothing in this plan requires the Ascension Meter, Impact Windows, the Final Clash,
  Phase 2, a second arena, or a second playable character.** If a step seems to need one
  of those, the step is wrong — stop and ask.

---

# PHASE 1 — Make it a game you can actually finish

Nothing here is optional. At the end of Phase 1 the duel has a beginning and an end.

## Step 1 — Prove the packaged build launches

**Why first:** it has been packaged many times and **never once double-clicked.** If the
`.exe` is broken, everything built after this is built on sand. It is also the cheapest
step in the plan.

**Editor:** no. **Roughly:** 30 minutes.

1. Package Windows Shipping from the editor (Platforms → Windows → Package Project).
2. Find the output `.exe` and run it from Explorer, not from the editor.
3. Walk, jump, punch. Confirm the octagon renders and the Vanguard reacts.
4. Note the launch time and the build size. The last build was **647 MB**.

**Done when:** the `.exe` runs standalone, shows the octagon, and accepts input.
**If it fails:** stop the plan and fix it here. This is the gate.

---

## Step 2 — Win, lose, and restart

**This is the single most important step in the plan.** It closes problems 1 and 2, and
it is what turns a tech demo into a game.

**Editor:** yes, with MCP. **Roughly:** the largest gameplay task here.

1. **Checkpoint first** — duplicate `Lvl_DuelGraybox` to `Lvl_DuelGraybox_CP_PreMatchLoop`.
2. Decide where match state lives. `BP_DuelKnockoutCoordinator` already detects both
   knockouts and is the natural owner. **Record the choice and the alternative you
   rejected** — Step 12 has to report one architectural decision and its alternative.
3. **Round start.** A brief "Round 1 — Fight" beat before input unlocks, with both
   fighters frozen for the count so the player is not hit before they have their bearings.
4. **End detection.** On either fighter reaching 0: stop the mover and the attack driver,
   let the ragdoll play, then show the result — **"YOU WIN"** or **"YOU LOSE"**.
5. **Fix the post-knockout collision bug (`X7`) here.** The QA agent found it and it
   reproduced on every seed: `StopMover` disables the mover's tick, which also stops
   `ApplyConstraints`, so the arena clamp and the 78 cm minimum separation stop being
   enforced. Measured: separation **50.6 cm against a 69 cm capsule contact**. It was
   invisible on the flat test plane. **In the octagon it means the player who just won
   walks through the ramps and truss walls.** Keep constraints running after a knockout.
6. **Restart.** A key that resets both fighters to full health and their spawn points
   without leaving the level. Re-enable the mover, driver and constraints.

**Done when:** you can win, you can lose, the result is on screen, restart works from
both outcomes, and after a knockout neither body escapes the arena.

---

## Step 3 — Give the Vanguard a second attack

Closes problem 4. He currently has one strike on a 2.5–4 s cooldown.

**Editor:** yes. **Depends on:** Step 2.

A **close-range punish** — faster than the existing strike, shorter reach, used when the
player is inside the current attack range. The point is that standing next to him stops
being free.

1. Extend `BP_VanguardBasicAttackDriver` with a second attack branch. Keep the same
   int-state flow — idle / windup / strike / recovery — so the telegraph and the
   interrupt-on-hit-react behaviour carry over for free.
2. **Give it a visually distinct telegraph.** The player has to be able to tell the two
   apart before impact, or the variety does not read as variety.
3. Pick between the two by range, not at random. Random reads as noise.
4. Provisional values only. Adrian tunes them in Step 5.

**Done when:** the Vanguard uses both attacks, picks by range, each is telegraphed
differently, and both are dodgeable.

**Note — the DataTable route is deliberately skipped.** `DT_VanguardAttacks` was paused,
and the assignment's pipeline points are already earned by the arena generator. Build the
attacks directly on the driver. It is faster and costs nothing on the grade.

---

## Step 4 — The anti-kite attack

Closes problem 3, and it is the difference between a fight and a chore.

**Editor:** yes. **Depends on:** Step 3.

Right now the Vanguard's top speed is below the player's, so walking backwards wins every
time and the duel cannot be lost. He needs one **advancing** move that covers ground.

1. A lunge or dash strike that closes distance, used when the player has been holding
   beyond his preferred range.
2. **The correct answer must be jumping over it or moving toward it — never backing up.**
   Verify both by playing it, not by reading the graph.
3. Add a short cooldown so it cannot be spammed into a stun-lock.

**Done when:** retreating in a straight line no longer wins, and there is a readable,
learnable answer a first-time player can find.

---

## Step 5 — Balance until it is a fight

**Editor:** yes, in PIE. **Depends on:** Steps 2–4. **This step is Adrian's, not an agent's.**

**Target: the player wins roughly 60–70% of matches.** Losing sometimes is the point.

1. Play ten full matches. Write down the result of each one.
2. Tune, in this order: Vanguard damage, then his attack cooldowns, then his movement
   speed, then player health.
3. Change **one value at a time** and replay. Two at once tells you nothing.
4. Record the final values in the Log so they survive a rebuild.

**Done when:** you lose at least three of ten, and the losses feel like your mistake
rather than the game's.

**Phase 1 ends here. From this point the game is finishable and everything else is polish.**

---

# PHASE 2 — Make it look like a game

Read this before starting: **recolouring is explicitly not enough.** The requirement is
real art assets brought in and placed on top of what exists, which Adrian then refines by
hand over the last days.

## Step 6 — RESEARCH FIRST — stop and do this before touching the editor

**This step is a reminder to Adrian: we agreed to do the research pass here.**
Do not start Step 7 until it is done. It is the difference between a real visual upgrade
and another gray box with different colours.

**Editor:** no. **This is a research step, and the agent does the research.**

What needs answering — with links, licences and file sizes — before anything is downloaded:

1. **Characters.** What free, rigged, game-ready humanoid characters suit a cyber-fantasy
   martial-arts duel and retarget onto the existing skeleton without re-rigging. The
   leading candidates are **Epic's Paragon character packs** (free, AAA-quality, fully
   rigged, with complete animation sets), **Mixamo** (free rigged characters and a large
   free animation library), and the **Fab free tier**. Paragon is the strongest lead —
   those are finished AAA fighters, and one of them standing in for Crimson Vanguard is a
   different game visually.
2. **Retargeting.** Exactly how a new skeletal mesh is swapped onto
   `BP_ThirdPersonCharacter` and `BP_VanguardProxy` in UE 5.8 — IK Rig and IK Retargeter,
   step by step — and what breaks when proportions differ. **The Vanguard sits at 1.1
   uniform scale**, so a taller mesh changes his reach and his collision capsule. That
   must be checked against combat spacing.
3. **Arena materials and lighting.** What free material and lighting packs would make the
   octagon read as an industrial arena. The interior is flat-lit today, the gallery
   overhangs read as dark bands, and the old template floor plane's ±2000 corners stick
   out past the 3180 cm octagon like a floating island.
4. **Effects.** Free hit-impact VFX, plus a usable sound set — hit, whiff, knockout, and
   an arena ambience bed.
5. **Cost and licence.** Everything must be **$0** and licensed for a submitted course
   build. Where nothing free exists, name the gap and propose a free fallback. **Never
   assume a purchase.**

**Done when:** a short written shortlist exists — asset name, source, licence, size, and
the exact import steps — and Adrian has picked from it.

---

## Step 7 — Apply the character art

**Editor:** yes. **Depends on:** Step 6. **Checkpoint the level first.**

1. Import the chosen meshes and animations.
2. Retarget onto the existing skeleton so all current animation and montage logic keeps
   working. **Do not rebuild the combat logic to suit a mesh** — the mesh serves the
   working game, not the other way round.
3. Swap the player mesh and the Vanguard mesh.
4. **Re-check combat spacing immediately.** Capsule sizes, the 78 cm minimum separation,
   attack reach and the ±650 arena clamp are all tuned to the current proportions.
5. Re-run Step 5's ten matches. If the feel moved, retune.

**Done when:** both fighters are recognisably characters rather than mannequins, and the
fight plays the way it did before the swap.

---

## Step 8 — Arena lighting and materials

**Editor:** yes. Cuttable under time pressure, but the cheapest visual win in the plan.

1. Light the interior properly. Kill the dark bands under the gallery overhangs.
2. Fix the template floor plane's corners sticking out past the octagon.
3. Apply industrial materials to the walls, gallery and truss.
4. Take fresh screenshots for the submission.

---

## Step 9 — Title screen and controls

**Editor:** yes. **Required for the "playable in 2 minutes without instructions" gate.**

A stranger opening the `.exe` must know what to do without being told.

1. A title screen with the game's name and a Start control.
2. **A controls list on screen** — move, jump, attack. This is what makes the two-minute
   rule pass.
3. Return to title from the result screen.

---

## Step 10 — Audio minimum

**Editor:** yes. **First to cut if time runs out.**

Four sounds: hit connects, attack whiffs, knockout, and an arena ambience loop. Silence
reads as broken to a first-time player more than bad audio does.

---

# PHASE 3 — Ship it

## Step 11 — Package and publish the playable link

**Editor:** yes, then no. **Worth 2.0 points, and it gates the entire assignment.**

**A broken or missing link caps the whole assignment at 50% regardless of everything else
in it.**

1. Final package, Windows Shipping.
2. **Test the `.exe` on its own** the way Step 1 did. Then, if at all possible, have
   someone who has never seen it open it cold and play. Watch where they get stuck.
3. Zip the build folder. **Keep the `.exe` and its sibling data folders together** — a
   zip missing them will not run on anyone else's machine.
4. Upload to **itch.io** as a downloadable Windows build. Leave "This file will be played
   in the browser" **unticked** — it is a native build, not web.
5. Fill in the itch page: title, a short description, a screenshot from Step 8, and the
   controls from Step 9.
6. Set the page to **public**, then **open the link in a private browser window** and
   download it as a stranger would. A draft page 404s for everyone but you, and that is a
   broken link by the rubric.

**Size warning:** the last build was **647 MB**. Check that against itch.io's upload
limit before starting — above the browser limit it needs their `butler` CLI tool.

**Done when:** the link is public, and a download from a logged-out browser produces a
build that runs.

---

## Step 12 — Assignment 10 submission

**Editor:** no. Everything below is read from the assignment PDF at the repo root.

**Deliverable 1 — Playable Link.** The itch.io URL from Step 11.

**Deliverable 2 — Pipeline source and engine integration.**
- The GitHub repository link.
- **A video of the pipeline running and generating output.** Nobody has recorded this
  yet. Screen-record `game/Tools/ArenaPipeline/` generating the octagon into the level.
- A description of how agent output lands in the engine without manual reformatting.

**Deliverable 3 — Pipeline audit and cost analysis, one page.**
- What the pipeline produced that is **in the playable build**. The octagon arena is the
  strong answer: generated by `game/Tools/ArenaPipeline/`, merged into `Lvl_DuelGraybox`,
  and therefore in the cook. Evidence and screenshots are already committed under
  `game/reports/arena/`.
- What manual steps remain, and what it would take to eliminate them.
- One architectural decision you would now make differently, and the specific alternative.
- **Actual run cost — calculated, not estimated.** The real token counts are in
  `ascendant-dm/transcripts/*/run.json`. Do not re-estimate them; the rubric requires it
  calculated from the actual run.
- The most expensive pipeline step, and whether this is sustainable for a solo dev.
- A before/after mid-project cost reduction, with token counts.

**How to turn it in:** the assignment wants links, not files — the itch.io URL, the GitHub
URL, and the video URL. Tag the submitted state so it is preserved:

```
git tag -a assignment-10-submission -m "Assignment 10 submitted state"
git push origin assignment-10-submission
```

**Done when:** all three deliverables are submitted and the playable link has been
verified from a logged-out browser.

---

## Cut order, if time runs short

Cut whole steps, never half-build one:

**Step 10** (audio) → **Step 8** (arena lighting) → **Step 4** (anti-kite attack).

**Steps 1, 2, 11 and 12 are not cuttable.** Step 2 is the game; Steps 11 and 12 are the
grade; Step 1 protects both.

---

## Log

- 2026-09-02 — plan written. Replaces `SHIP-PLAN.md`, `sprint/PLAN.md`, `sprint/BOARD.md`
  and `sprint/HANDOFF.md`, all of which planned to a ship date that has passed. The
  Assignment 10 requirements above are read from the PDF at the repo root, not inferred.
