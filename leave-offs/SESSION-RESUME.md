# Session resume — written 2026-07-25, end of session

Not a gate file. The gate hooks only read `designer.md`, `developer.md`, and
`inspector.md`; this file is here for the next session to read first.

## Why this session ended

An **API session limit** (resets 7:20 pm America/New_York) killed the designer agent
mid-run. It had already written `design-brief.md`; it had not yet written its
leave-off. Nothing was lost — see `leave-offs/designer.md` for what the commander
verified before recording that gate.

## Where the project actually stands

| Thing | State |
|---|---|
| Milestone | **M1** — nothing built in Unreal yet |
| Phase | **Phase 1** (playable duel by 1 Sept 2026) |
| designer | **complete** — `design-brief.md`, 1090 lines |
| developer | **not run** — gate is **open**, this is the next agent |
| inspector | **not run** — gate closed until the developer completes |
| #04 pipeline | **not started** |

## Do this first, next session

1. **Run the `developer`.** Its gate is open. It consumes `design-brief.md` and
   produces `build-sequence.md`. This is the shortest path to the 3.0 Working Crew
   points on #03.
2. **Then run the `inspector`** — consumes both briefs, produces `inspection.md`.
   That closes out assignment #03 completely.
3. **Then move entirely to #04.** It is the deadline actually at risk.

## Deadlines as of the last session

Today was **25 July 2026**.

| Item | Due | Days left then |
|---|---|---|
| #03 Build an Agent Crew | 28 July 2026 | 3 |
| #04 Dynamic Content Pipeline | 30 July 2026 | 5 |
| **Game playable — Phase 1** | **1 September 2026** | 38 |

**Recompute these on session start — they are stale the moment this file is saved.**

## Decisions made this session

- **The game ships 1 September 2026, in two phases.** Phase 1 = M1–M4, a duel that
  can be fought start to finish with **some design on it**. Phase 2 = full M5 polish.
  Written into `project-brief.md`, `CLAUDE.md`, and `README.md`.
- **How Phase 1 gets a look without breaking M5 ordering:** dress the proxies. M1–M4
  may stand up free third-party meshes, animations, and set dressing from the start —
  asset selection is not a presentation pass. Tuned camera / VFX / hit-stop / sound
  stays in M5.
- **Budget is $0.** Unreal starter and template content, Fab free tier, free Quixel
  grants, Mixamo, Paragon, Game Animation Sample Project. No purchases assumed.

## Still open — needs the user

- **The three #04 content gaps are not confirmed.** `CLAUDE.md` lists the candidates:
  attack A–D names / choreography / telegraph copy · Shattered Ring history ·
  Project Valor-7 origin · the Ascension fiction · UI, announcer, and telegraph
  strings including the unfinalized short in-combat label for Crimson Vanguard.
  **Confirm three with the user before generating anything for #04.**
- **29 provisional values** await the human designer in `design-brief.md` §14. None
  block the developer — they become exposed variables.
- **Unreal MCP is not connected.** Required before build steps are executed in the
  editor, not before `build-sequence.md` is written.
