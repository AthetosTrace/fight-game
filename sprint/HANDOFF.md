# Handoff — 2026-08-27

The current briefing. Read `README.md` for the protocol and `BOARD.md` for the task list;
this file is the "start here right now" note. Rewrite it when the situation changes.

---

## Starting a session that can actually do this work

The next two tasks both need the Unreal editor **and** a live MCP connection. Order matters,
because MCP servers attach at session start — a session opened before the server is listening
will not see the tools, and no amount of starting the server afterwards fixes it.

1. **Open the project** — `C:\Users\athet\Documents\FightGame\game\AscendantImpact.uproject`
2. **Start the MCP server** in the editor console:
   ```
   ModelContextProtocol.StartServer
   ```
   It does **not** auto-start. `bAutoStartServer` defaults to false. If port 8000 is dead,
   this is why.
3. **Then** open the session:
   ```
   cd C:\Users\athet\Documents\FightGame
   claude
   ```
4. **Commit before starting.** Asset reorganization is the one operation where a bad outcome
   is painful to undo by hand. A clean commit turns it into `git reset --hard`.

### The prompt to paste

> Read `sprint/README.md`, then `sprint/BOARD.md`, then
> `sprint/tasks/G16-content-reorganization.md`. Work G16, then G07. The Unreal editor is open
> and the MCP server is running. Commit before you start.

---

## G16 — reorganize Content under one root

Full detail and the exact 18-row move table are in
[`tasks/G16-content-reorganization.md`](tasks/G16-content-reorganization.md). The shape of it:

**18 of the 30 real assets move under `/Game/AscendantImpact/`.** The boss comes out of
`Variant_Combat`, the player and GameMode out of `ThirdPerson`, the arena maps out of
`ArenaTools`, `UI_LifeBar` joins `UI_DuelHUD`. Epic's **157 template files stay put** — moving
126 MB of mannequin animations is pure churn and a long re-save.

**Move only. Do not rename.** Renaming `BP_ThirdPersonCharacter` to something prettier
invalidates every reference in `PROTOTYPE_BLACKBOARD.md`, `assignment-09/ORACLE.md`, and a
dozen task files — and Assignment 09 is already submitted and tagged at
`assignment-09-submission`. Folder structure delivers the organization; renaming only buys
cosmetics. Revisit after ship.

### The three things that actually go wrong

1. **Moves must happen inside the editor.** The package path is baked into the binary, so
   moving `.uasset` files on disk corrupts references. Use
   `unreal.EditorAssetLibrary.rename_asset`.
2. **`rename_asset` leaves ObjectRedirectors** at the old paths. They work, but they are debt
   and they cook into the shipped build. Fix them up afterwards — the task carries the code.
3. **The three `.umap` moves carry OFPA external-actor folders.** `Lvl_ArenaOctagon` alone has
   43 packages under `Content/__ExternalActors__/ArenaTools/Maps/Lvl_ArenaOctagon/`, and that
   path derives from the level's package path. **Do the 15 non-map moves first, commit, then
   move the three maps separately and verify the `__ExternalActors__` folders followed before
   committing again.** If Python did not move them, `git reset --hard` and do those three by
   hand in the Content Browser, which definitely handles OFPA.

### One config line breaks, and the editor will not fix it

Asset moves fix Blueprint and level references. They never touch `.ini` files.

`game/Config/DefaultEngine.ini` →
`GlobalDefaultGameMode=/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C`
must become `/Game/AscendantImpact/Core/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C`.

All five config files were grepped on 2026-08-27. That is the only path that breaks.
`DefaultInput.ini` has no `/Game/` paths at all — Enhanced Input contexts are referenced from
the player Blueprint, not config.

### `Lvl_DuelGraybox` does not move and does not get renamed

It is `GameDefaultMap`, it is the only map currently in the cook set, and `G07` is about to
merge the octagon into it. Renaming it is a separate, optional job for after ship.

---

## G07 — the baseline Adrian asked for

Copy the octagon geometry **into** `Lvl_DuelGraybox` and delete the flat plane.

**Direction matters and it is the opposite of what this task originally said** — corrected in
`ea0fe6e`. Merging geometry into the duel level keeps three things untouched that would
otherwise all need redoing:

- **The cook set.** `GameDefaultMap` already reaches `Lvl_DuelGraybox`, and only maps reachable
  from it get cooked. The arena ships automatically, with no packaging config change.
- **The Vanguard's per-instance overrides.** Its 1.1 mesh scale and `ABP_VanguardLocomotion`
  anim class are set on the *placed instance*, not just class defaults. Re-placing the actor
  means re-applying both — the stale-instance trap the blackboard records hitting in §20, §21
  and §22.
- **PlayerStart and GameMode wiring**, already correct there.

Moving geometry is safe. Moving configured gameplay actors is where the bugs are.

After this: open the project, `EditorStartupMap` loads the level automatically, and the arena
is around the fighters. Nothing to attach, ever again.

**Not a bug:** the player not appearing until you press Play is normal Unreal. The Vanguard is
a placed actor so it shows in the editor; the player spawns from `PlayerStart` at runtime.

---

## Insist on this one acceptance check

Both tasks end with **repackage successfully**. The `G02` recipe is proven, so it is a rebuild
and not an investigation — roughly a minute. It is also the only check that catches a reorg
breaking something the Message Log stayed quiet about. Do not let it get skipped.

---

## Order after that

| Step | Task | Why |
|---|---|---|
| 1 | `G16` | One root. Know where to open and build from. |
| 2 | `G07` | Octagon merged in. The visual baseline. |
| 3 | `G03` | Run the packaged exe — built but never launched. Ten minutes. |
| 4 | `G05` | Win / lose / restart. Also fixes X7, the post-KO constraint loss. |
| 5 | `G12` → `G13` → `G14` | Attack DataTable, then attack B, then the anti-kite attack. |
| 6 | `G06` | Balance. Needs all three attacks to exist first. |
| 7 | `G04`, `G08`, `G09`, `G10`, `G11` | itch.io, title, audio, ship, submission. |

Adrian's four named problems map onto this directly: **can't win or lose** is `G05`, **backing
up wins every time** is `G14`, **only one NPC attack** is `G12`–`G14`.

---

## Where everything lives now

- **One repo, one folder.** `C:\Users\athet\Documents\FightGame`, branch `main`. No worktrees
  remain and none should be created.
- **The game** — `game/`, with `game/AscendantImpact.uproject` the only copy of the project.
- **The old `AscendantCapstone` folder is dead.** Verified 2026-08-27: `ascendant-impact-ue` is
  clean, its HEAD is exactly the commit we subtree-imported, and every tracked file in it
  already exists in this repo. Nothing unique. Ignore all 414 MB of it.
- **Assignment 08** lives outside this repo by design — `AthetosTrace/ascendant-dm`. Its
  `transcripts/*/run.json` files hold the only real token counts, which `G11` needs.
- **Assignment 09** is submitted, tagged `assignment-09-submission`, branch deleted.
