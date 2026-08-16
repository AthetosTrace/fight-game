# Assignment 07 — Pre-Build Declaration

**Game:** *Ascendant Impact* — cinematic 1v1 cyber-fantasy action fighter, Unreal Engine 5.8, PC.
**Author:** AthetosTrace · **Submitted before any style-guide code was written.**

---

**01. What content type does this agent govern?**

Player-facing combat copy — the words the player actually reads during the duel:
Impact Window prompts, Ascension Meter feedback, the Phase 2 transition callout, the
Final Clash unlock prompt, the failed-Clash recovery line, and the win/loss screens.
Nothing in Assignments #04–#06 produced a single line of it.

**02. What specific rules from the GDD must every line satisfy?**

Three constraint types, each citing the GDD.

- **Tone** — §01, page 1, Pillar 1 "Skill Creates Spectacle": readable timing and
  deliberate decisions *earn* the strongest rewards. Copy that celebrates progress the
  player did not earn contradicts the pillar. The GDD's own high-concept line sets the
  register: *"Choose an Ascendant operative. Survive one complete duel. Earn the
  spectacle."*
- **Vocabulary and lore** — §01 page 1 and §03 pages 3–4 fix the proper nouns
  (Ascension Meter, Impact Window, Final Clash, Shattered Ring, Ascendant operative,
  Crimson Vanguard / Project Valor-7) and the facts behind them: the meter is earned
  only through active combat decisions and never fills from waiting or elapsed time;
  a failed Final Clash does not restart the duel.
- **Formatting and length** — §07, pages 8–9 makes readability the standard for what
  the player must parse mid-fight. On-screen prompts carry hard character limits and a
  fixed line shape.

**03. What does a failure look like — concretely, in this game's terms?**

A prompt reading "ULTIMATE READY!!" instead of naming the Final Clash. A meter tooltip
saying the bar fills over time, which §03 explicitly denies. A recovery line telling the
player the duel is restarting after a failed Clash, which §03 explicitly denies. A line
that cheers a player who is losing. A prompt too long to read during Phase 2 pressure.
Shipped, each one either teaches the player a rule the game does not have, or breaks the
voice the GDD established.

---

*Every rule above traces to a GDD section and page. No rule cites
`PROTOTYPE_BLACKBOARD.md`, and no rule invents lore the GDD leaves open — the Shattered
Ring's history and Project Valor-7's origin stay undefined, and this agent never needs
them.*
