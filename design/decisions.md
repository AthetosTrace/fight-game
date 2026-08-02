# Design decisions — the record

This file holds **one rule** and the log it governs. It is the permanent record of what
was decided; [`TODO.md`](../TODO.md) is the impermanent record of what is still open.
An item that gets answered is **deleted** from `TODO.md` and **appears here**.

---

## The rule

**1. The PDF is the source of truth.**
`Ascendant_Impact_Assignment_02_Revised_GDD_Anthony.pdf` (v0.4, 2026-07-24) outranks
every other document in this repository — this file, `project-brief.md`,
`design-brief.md`, `combat-integration-plan.md`, the assignment-04 knowledge base, and
anything said in a session. If any of them disagrees with the PDF, the PDF wins.

**2. `gdd/` is generated and is never hand-edited.**
`gdd/sections/`, `gdd/reference/`, `gdd/INDEX.md`, and
`gdd/ascendant-impact-gdd-v0.4.md` are all mechanically derived from the PDF. Editing
any of them by hand silently forks the source of truth and there is no way to detect it
afterwards. **To change what `gdd/` says, change the PDF and re-export.** If a
description in `gdd/reference/` is wrong, fix the description by re-reading the image —
never by writing in what you believe the art should show.

**3. Every answer recorded here gets a dated entry** naming:
- **what it resolves** — the `TODO.md` item number and its Q / V id, so the deletion
  from `TODO.md` is traceable;
- **the decision**, stated plainly enough to implement from;
- **who decided it and when**;
- **any GDD line it supersedes** — quoted, with its `gdd/sections/` file and PDF page.

**4. The moment an entry supersedes a GDD line, `TODO.md` gains an item** stating that
the GDD is out of date. **Clearing that item means Adrian updates the source PDF,
re-exports it, and re-extracts `gdd/`** — not editing `gdd/` and not leaving the two
out of step. Until the PDF is updated, the GDD remains the source of truth *and* is
known-stale, which is the worst state to be in silently and an acceptable state to be
in visibly.

**Superseding the GDD is a real act.** Most decisions will not do it. A decision that
merely fills a value the GDD never specified — which is what most of `TODO.md` is —
supersedes nothing. A decision that contradicts something the GDD actually says does,
and triggers rule 4.

---

## Status values

- **APPROVED** — a KIND A engineering item. A documented procedure exists and there was
  nothing to decide. It is settled and its `TODO.md` entry is deleted.
- **PROPOSED** — a KIND B design item. A designer dispatch researched it and recommends
  an answer. **It is not decided.** Its `TODO.md` entry stays open, marked PROPOSED,
  until the human designer approves or changes it. Only then is it deleted.

**Nothing supersedes the GDD yet, so rule 4 has not fired.**

## Log

### 2026-08-02 — Group 04 · spacing and arena (Q24, Q10, Q12, Q13, Q11, mezzanine)

- **Status:** **PROPOSED** — all six. The designer decides.
- **Resolves:** TODO items 17 (Q24), 22 (Q10), 23 (Q12), 24 (Q13), 10 (Q11), 18 (mezzanine) · all KIND B
- **Dispatch:** group 04 → `design/group-04-spacing-and-arena.md`

| Item | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q24 | playable floor **2400 × 1600 cm (24 × 16 m)**, long axis = doorway axis, four 250 cm 45° chamfers; also stored as `ArenaLongAxisCm`/`ArenaShortAxisCm` so Q13 cannot drift | `L_ShatteredRing` + `DA_TuningGlobals` | M1-21 |
| Q10 | bands centre-to-centre **A 0–260 · B 90–520 · C 240–420 · D 400–840** cm, identical both phases | `DT_VanguardAttacks` Min/MaxRange | M2-04 |
| Q12 | P1 **A 3.0 · B 3.5 · C 3.6 · D 3.8 s** / P2 **A 2.5 · B 2.6 · C 2.7 · D 2.8 s**, **relocated into `S_AttackPhaseTuning`** so Phase 2 re-times through the existing data path | `S_AttackPhaseTuning` | M2-04 |
| Q13 | **600 cm = 0.25 × long axis**, finishing 240 cm from the target | `DT_VanguardAttacks.MaxTravelDistance` | M2-04 |
| Q11 | acquire **3000 cm**, break **3300 cm**, interp **6.0**, aim socket **140 cm** at **−8°** — both beyond the 2884 cm diagonal so lock never breaks by distance in this arena | `BP_LockOnComponent` | M1-16 |
| 18 | mezzanine is **set dressing** — no NavMesh, no blocking volume, railings `NoCollision`, underside ignores the `Camera` channel | `L_ShatteredRing` | M1-21 |

- **Footprint:** 2400 × 1600 uu, diagonal ≈ 2884 uu, ~371.5 m² walkable. Stated as **two
  dimensions**, per the recovered arena sheet showing a rectangular hall.
- **Band coverage proof delivered:** contiguous over [0, 840] with 80 cm and 120 cm
  handoff overlaps, depth ≥ 2 across the whole 100–520 cm fight zone. Exactly one
  zero-coverage region (840–2884 cm) and one depth-1 region (520–840 cm), **both resolved
  by a required advance rule rather than by accident** — which is the `BTTask_Idle_Reposition`
  loop bug §14 warned about, closed deliberately.
- **Starvation check passes in both phases** at the fastest legal cycle; tightest slack
  **+0.16 s**. Q12's legal window is narrow: **(2.94, 3.96] s in P1**, **(2.315, 2.96] s in P2**.
- **Supports Q21 (Final Clash group):** separation **1000–1300 cm**, 1300 the guaranteed
  ceiling, **1200 the comfortable value**, pushed along the long axis rather than the
  fighters' facing.
- **Handed to Q25:** author **A and B short (0.55–0.70 s), C and D long (0.75–0.95 s)** —
  group 03's counter-spam warning made spatial. And **D's Active must sit at 0.40–0.45 s**,
  or 600 cm in 0.18 s reads as the teleport the GDD forbids.
- **Supersedes GDD:** none. Prior art from Tekken's published stage sizes (24×24 standard,
  16×24 *Midnight Siege*). Souls-like arena dimensions and per-attack AI cooldowns were
  searched for and **cited as not found rather than estimated**.

**Three more gaps with no §13.2 row and no Q number — now TODO items 49, 50, 51.** One of
them is serious: **the rival's `MaxWalkSpeed` is unspecified, and under the approved Q22
a rival slower than the player can be kited forever and the duel cannot end.**

**Q12 is the weakest-sourced item in this group** — no shipped game publishes AI attack
cooldowns, so it is derived purely from the GDD's own state ranges.

*Research note: 10/15 searches.*

### 2026-08-02 — Group 03 · defensive timing (Q6, Q7, Q8, Q26, Q27, Q28)

- **Status:** **PROPOSED** — all six. The designer decides. **Q7 is BLOCKING.**
- **Resolves:** TODO items 14 (Q6), 15 (Q7), 16 (Q8), 33 (Q26), 30 (Q27), 13 (Q28) · all KIND B
- **Dispatch:** group 03 → `design/group-03-defensive-timing.md`

| Q | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q6 | i-frames **0.28 s**, spanning `[0.03, 0.31]` of `AM_Player_Dodge` | `ANS_IFrame` | M1-19 |
| Q7 | perfect dodge **0.12 s**, `[0.03, 0.15]` — front 43% of the i-frame window | `ANS_PerfectDodge` | M1-19 |
| Q8 | whiff lockout **0.55 s** | `AM_Player_CounterWhiff` | M1-20 |
| Q26 | Impact cooldown **7.0 s**, clocked on window *close*, **first window exempt** | `BP_ImpactWindowDirector` | M3-07 |
| Q27 | recover multiplier **1.0 — no bonus** | `ANS_Recover` | M2-13 |
| Q28 | combo buffer **0.25 s = 75% of a section**, stated as a ratio | `AM_Player_LightCombo` | M1-18 |

- **Q7 rationale:** 4× SF6's 2-frame Perfect Parry, tighter than Sekiro's 12-frame deflect
  and SF3's 10-frame parry. **Front-loaded so the player must press late, into the strike.**
  Playtest protocol given: **start at 0.15 s and tighten**, never the reverse.
- **Reaction check passes at the hardest legal attack:** against a 0.40 s Phase 2
  telegraph the perfect-press window `[0.25, 0.37]` opens exactly at the ~250 ms average
  human reaction time.
- **Q26 first-window exemption is not optional** — applying the cooldown to the first
  Impact Window would break the GDD's onboarding rule.
- **Supersedes GDD:** none. All six fill blanks; every cited range is unchanged.

**Q2 = 1200 SURVIVES.** At Q27 = 1.0 the scalar is unity and group 02's derivation stands
intact. Better: effective damage becomes `20 × [f×Q27 + (1−f)]`, so **1.0 removes the
unmeasurable `f` term from the model entirely.** If the designer overrides Q27:
**1.25 → Q2 ≈ 1410** (outside group 02's 1100–1400 band); **1.5 → Q2 ≈ 1620**, and at
Q2 = 1200 a strong player reaches the gate at **1:55**, below the GDD's 3-minute floor.

**Five tensions carried forward:**
1. **Q26 cannot make the meter a real second gate — no value in 3–8 s can.** Group 02's
   framing is corrected rather than answered: the meter has four faucets and Q26 gates
   one. With Impact **disabled entirely**, 20 finishers still fill the meter in ~84 s
   against a health gate at ~173 s. Every route to halving that is closed — gains are
   GDD-fixed, C1 forbids decay, the 0–100 ceiling is GDD-fixed. **The meter is an
   anti-passivity floor, not a race.** 7 s still cuts the +20 row's dominance from a
   ~2.25× speedup to ~1.67×.
2. **Q8 anti-spam fails against slow Phase 1 telegraphs (0.75–0.95 s).** Closing it needs
   ~0.95 s of lockout — outside §14's band and unplayable. Accepted as a beginner crutch
   that dies at Phase 2. **Warning to Q25: do not author all four attacks near 0.95 s.**
3. **Q27 = 1.0 does not fix group 02's scrappy ~5:24 overshoot.** 1.25 trims ~25 s while
   also shortening the competent run — net zero. Group 02's own Q2 → 1050–1100 remains
   the only fix.
4. **Q7's repeatability is unverified.** The check proves the pocket's *onset* is
   reachable; it does not prove a human can hit 0.12 s repeatably. Motor-timing precision
   was out of research budget.
5. **Q8's magnitude has no prior-art support.** No whiffed-parry recovery frame counts
   were found in any shipped game. 0.55 s is derived purely from the GDD's own telegraph
   and recover ranges. **Named as the weakest number in the file.**

**Three defects found in `design-brief.md` §13.2 — now TODO items 46, 47, 48.** The table
has no row and no Q number for the counter's own success window, for whether a dodge
cancels the light combo, or for the total length of `AM_Player_Dodge`.

**Developer notes:** `ANS_ActiveHit` and `ANS_ComboLink` overlap on the same section and
**must not be merged**; `bComboQueued` clears on next-section begin and on any montage
interruption; a successful counter must **not** play `AM_Player_CounterWhiff`;
`BP_ImpactWindowDirector` needs a `bFirstWindowConsumed` flag that skips the cooldown
check; `BP_FinalClashDirector` must never consult that cooldown. **Three separate
warnings that Q14's `MontagePlayRate` would silently scale Q6 and Q7 into per-fighter
difficulty — Q28 is the only one of the three that scales correctly.**

*Research note: 15/15 searches, cap reached.*

### 2026-08-02 — Group 02 · combat economy (Q1, Q2, Q3, Q4, Q5)

- **Status:** **PROPOSED** — all five. The designer decides.
- **Resolves:** TODO items 2 (Q1), 3 (Q2), 21 (Q3), 11 (Q4), 12 (Q5) · all KIND B
- **Dispatch:** group 02 → `design/group-02-combat-economy.md`

| Q | Proposed | Lives in | Unblocks |
|---|---|---|---|
| Q1 | Player max health **100**, identical for both fighters | `DA_TuningGlobals` | M1-05 |
| Q2 | Vanguard max health **1200** (band 1100–1400) | `DA_TuningGlobals` | M1-05 |
| Q3 | Rival damage **A 32 · B 25 · C 27 · D 18** (% of player max HP) | `DT_VanguardAttacks.Damage` | M2-04 |
| Q4 | Light hit **5**, finisher **10** (2×), combo total **20** | `AM_Player_LightCombo` notify data | M1-17 |
| Q5 | **3** sections — `S_Hit1` / `S_Hit2` / `S_Finisher`, ~1.0 s | `AM_Player_LightCombo` | M1-17 |

- **Why Q1 = 100:** makes Q3's "percentage of player health" and the Data Table integer
  the same number, so the two can never drift.
- **Why Q5 = 3, and this is the load-bearing finding:** at GDD midpoints the rival's
  cycle leaves a non-threatening window of ~1.73 s in Phase 1 and **~1.28 s in Phase 2**.
  A 4-section combo runs ~1.33 s and **does not fit Phase 2 at all**. Q5 = 4 would also
  invalidate the Q2 derivation.
- **Q2 is derived, not picked:** 1200 puts the ≤25% gate at ~2:53 for competent play and
  ~4:29 for scrappy play, against the GDD's 3–5 minute target.
- **Supersedes GDD:** none. Every value fills a blank the GDD never specified; all fixed
  GDD numbers are cited and unchanged.

**C3 is satisfied, but not as framed** — meter 100 arrives ~0:40–1:25 while the health
gate arrives ~2:53, so they do *not* converge. The ordering is meter-first, which is the
safe direction: the player spends the tail attacking and damage still progresses. The
dangerous state (1 HP, empty meter) does not occur in normal play.

**Five open tensions carried forward, none of them settled here:**
1. **Post-failed-Clash rebuild** leaves ~15–35 s of genuinely inert damage. This makes
   **C2's HUD gate indicator mandatory, not optional.**
2. **The 2-hit-and-bail player** never finishes a string, earns no meter, and can reach a
   pinned rival with an empty bar. No number in this group can close it — handed to C2,
   the onboarding Impact Window, Q28 and Q25.
3. **Scrappy worst case overshoots to ~5:24**, past the 3–5 minute target. Either accept
   it (that player may hit the loss outcome first) or drop Q2 to ~1050–1100.
4. **Q26 makes the +20 Impact row dominant** — five Impact successes fill the meter
   outright. If the meter is to be a real second gate, the lever is **Q26**, not any GDD
   gain value. Flagged to the defensive-timing group.
5. **Attack B is a "sequence."** If authored with multiple `ANS_ActiveHit` windows each
   reading `Damage = 25`, B deals 50–75% of player health in one attack and the budget is
   void. **Proposed rule: the Data Table row is *total* attack damage, split across
   notifies.** Named as the most likely way the table silently produces a broken fight.
6. **Q27 is a direct scalar on the Q2 derivation** — at §14's upper bound of 1.5 the
   45-combo count drops toward ~30. **Q27 should be resolved before Q2 is locked.**

*Research note: 13 searches. Datamined boss HP for Sekiro and Elden Ring returned nothing
reliable, so no such figure is cited. One claim about Sekiro percentage damage is marked
unverified and is not load-bearing.*

### 2026-08-02 — Q22 · the 1 HP floor is permanent; the Final Clash is the only way to win

- **Status:** **APPROVED** — accepted as proposed by the designer of record, 2026-08-02.
  **This is now settled and binding on every downstream answer.**
- **Resolves:** TODO item 4 (Q22) · **BLOCKING** · KIND B · entry deleted from `TODO.md`
- **Dispatch:** group 01 → `design/group-01-blocking-q22.md`
- **Proposed decision:** reading **(b)**, sub-variant **(b2)** — `MinHealthFloor = 1` on
  the rival's `BP_HealthComponent` from `BeginPlay`, lowered to `0` only by
  `ClashSuccess()` immediately before it applies lethal damage.
- **Value lives in:** `HealthComponent.MinHealthFloor` (`design-brief.md` §13.2 row 50)
- **Unblocks:** M1-08 — Create the shared `BP_HealthComponent`
- **Why, in short:** the GDD's encounter-flow table lists exactly one win condition
  (Final Clash success), so reading (a) requires *adding* a win condition the GDD never
  writes down while (b) only widens the scope of a floor the GDD does state; it makes
  the double gate meaningful; it makes the meter — and therefore skill — the only route
  to the ending; and it is the cheapest, least leak-prone build.
- **Prior art cited:** Sekiro (Deathblow), Metal Gear Rising: Revengeance (Monsoon and
  Sundowner hard-stop at 10% into a mandatory QTE), Hi-Fi Rush, Sifu, God of War
  Ragnarök, Furi, Jedi: Fallen Order, Asura's Wrath as the cautionary case. Two claims
  are explicitly marked unverified in the group file.
- **Three attached conditions — carried forward as binding constraints on later groups:**
  **C1** Q9 must resolve to **no meter decay**, or the tail can become a dead end.
  **C2** the HUD must show **which gate is still locked** once the health bar visibly pins.
  **C3** Q2 must be tuned so **≤25% and meter 100 arrive close together**.
  These are not settled answers to Q9, the HUD, or Q2 — they are constraints those
  answers must satisfy.
- **Supersedes GDD:** none. This interprets the scope of the GDD's failed-Clash 1 HP
  floor; it edits no GDD number and contradicts no GDD line.
- **Developer note:** M1-08 can proceed either way — the clamp is identical. What must
  wait is the rival instance's default value and whether `BP_DuelDirector` wires a rival
  `OnDeath → EndDuel(Win)` path at all. Leave both unset rather than let a default
  silently become the design.

### Entry format

```markdown
### YYYY-MM-DD — <short title>

- **Resolves:** TODO item <n> (<Q/V id>)
- **Decision:** <the answer, stated plainly enough to implement from>
- **Decided by:** <name>
- **Supersedes GDD:** none
  <or>
- **Supersedes GDD:** "<quoted line>" — `gdd/sections/<file>.md`, PDF page <n>.
  TODO item added: GDD out of date.
```
