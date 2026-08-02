# What the recovered sheets say about `design-brief.md` §14

Written 2026-08-02, when GDD pages 10–14 were recovered from the PDF's embedded
images for the first time. Every claim here traces to a file in `gdd/reference/`.

**Nothing in this file resolves anything.** Every open value belongs to the human
designer. This is a list of what the sheets *inform*, what they *confirm*, and where
they may *contradict* — surfaced, not settled.

---

## 1. One value the sheets actually recover

### Crimson Vanguard's height in centimetres — **208 cm**

`design-brief.md` §13.1 row 28 lists Crimson Vanguard as **6'10"** with **no cm
value**, while rows 26 and 27 give Echo 183 cm and Nova 173 cm. The gap was not a
design decision — the cm figure simply was not readable.

**Page 10 prints it: "6'10" (208 cm)".** It is GDD-published, not derived, and
consistent with the other two rows' formatting.

This is the one case in this file where a blank in the design brief can be filled from
recovered material rather than left open. **It is still the designer's call to accept
it** — but it is a transcription, not an invention.

---

## 2. Q24 — Arena playable footprint

**Status: informed, NOT resolved. No number exists.**

The arena sheet carries **no dimensions, no scale bar, and no human figure in any of
its three views**. A footprint cannot be measured from it. Anyone claiming otherwise
is guessing.

What it *does* fix, and what the build can rely on:

| Constraint | What page 11 shows |
|---|---|
| Plan shape | Broadly rectangular hall, longer than wide, corners chamfered rather than square |
| Play surface | **One flat concrete floor.** No elevation change, no stairs into play, no pits |
| Obstacles | **None.** The central floor is completely clear — no crates, columns, or props |
| Hazards | None visible, consistent with GDD §08's "without adding gameplay hazards" |
| Entrance | One bright doorway centred on the far short wall — the Vanguard entrance axis |
| Opposite end | Closed wall, landmarked by a large X-braced steel truss panel |
| Boundary | Solid concrete on all sides, with orange railings marking the floor perimeter |
| Vertical | A mezzanine ring above the floor, with **no visible route into the play space** |

**Consequences worth noting.** Q13 (Attack D max travel) is defined in the brief as a
fraction of Q24, so it stays blocked. Q10 (attack range bands) and Q21 (failed-Clash
separation distance) also depend on it. **The footprint remains the single blocking
number for that whole cluster, and the art does not unblock it.**

One thing the sheet does settle qualitatively: a **rectangular** arena means the
distance from centre to a short wall differs from centre to a long wall. Any single
"arena radius" assumption downstream is wrong.

---

## 3. Q14 / Q15 / Q16 — Echo vs Nova play-rate, walk speed, dodge distance

**Status: informed, NOT resolved — but the sheets weigh the answer.**

The brief asks whether these three scalars should differ *at all* in Phase 1, and
notes that identical is the conservative reading of the GDD and the cheaper build.

The sheets are **visual only** — no stance, no combat pose, no animation reference, no
movement note appears on either board. Both fighters are drawn in a neutral A-pose.
They therefore say nothing directly about walk speed or dodge distance.

What they *do* show is that **the differentiation budget is already substantially
spent on presentation**:

| | Echo (p.12) | Nova (p.13) |
|---|---|---|
| Palette swatches | 3 | **4** — adds "Light Grey (Helmet Cap)" |
| Helmet | Entirely black | Light-grey cap over dark visor |
| Torso | One-piece "Segmented Body Suit" | "Dual-Layer System (Jacket over Vest)" |
| Back | "Backpack Power Unit Core" + energy lines | No back unit shown |
| Legs | Close-fitting, continuous line | Cargo trousers to below the knee, then close legging |
| Carry | None | Two named thigh pouches |
| Footwear | Low-profile shoe | High-top "Designed Light Sneakers" |
| Insignia | "Unique Badge", unlettered | Circular, lettered "SFN" |

That is a genuinely different silhouette at combat distance — which is what GDD §07's
"lean, upright technical striker" versus "compact, agile layered profile" asks for, and
what §02's shared-player-kit rule says the differences should be: *"animation
presentation, stance and movement personality, VFX language, timing flavor"*.

**This strengthens the conservative reading.** The fighters already read as different
people before a single scalar is changed. Keeping play-rate, walk speed, and dodge
distance identical in Phase 1 costs the game less distinctiveness than it would have
without these sheets. **Still the designer's decision.**

---

## 4. Confirmations — things the sheets check out clean

- **Nova's cyan-white rule holds.** GDD §07 and §10 reserve cyan-white for combat
  energy, telegraphs, or selected VFX — *"not a costume recolor"*. **No cyan appears
  anywhere on Nova's sheet.** The costume palette is black / charcoal / bright orange /
  light grey. Art and rule agree.
- **"Red armor over black structure" holds.** Page 14 shows exactly that, with the
  black substructure visible at every joint.
- **Attack D's thruster cue has a physical basis.** The rear view shows large vertical
  vanes above the shoulders and louvred, amber-lit vents. The "thruster cue before
  movement" requirement has something real to key off.
- **Scale contrast reads as width, not just height.** Page 10 shows the rival at
  roughly twice the centre figure's shoulder width. GDD §07's "substantially broader"
  is understated by the height numbers alone.

---

## 5. Possible contradictions — surfaced for the designer

### 5.1 "plasma-gauntlet weapons" vs "close-range committed gauntlet force"

Page 14's UNITS DESCRIPTION panel reads, in part, *"powerful, integrated
plasma-gauntlet weapons"*. GDD §04 describes Attack A only as **"Close-range committed
gauntlet force"** with no energy component, and the sheet's own LEFT ARM / GAUNTLET
panel shows **an enclosed armored fist with no emitter, barrel, or muzzle**.

"Plasma" implies an energy weapon that the authored text does not grant and the art
does not depict. **Flagged, not resolved.**

**Confidence caveat:** that panel is printed in low-contrast grey at small size and the
transcription is explicitly low-confidence. **A human should confirm the wording
against the PDF before anyone treats this as a real contradiction.**

### 5.2 "SYSTEM STATS" map to nothing

Page 14 prints POWER 9/10, ARMOR 9/10, **MOBILITY 6/10**, SYSTEMS 7/10. **No system in
the GDD, `design-brief.md`, or `combat-integration-plan.md` consumes these.** They do
not correspond to health, damage, movement speed, or any tunable.

They are probably concept-art flavour. But they are numbers on a page in the source of
truth, and a future agent will eventually find them and try to use one. **Treat as
non-canonical until the designer says otherwise.** In particular, MOBILITY 6/10 is
**not** a movement-speed value.

### 5.3 "Crimson Valor color scheme"

The same panel uses the phrase *"Crimson Valor color scheme"*. That term appears
nowhere else in the GDD. Whether it is an in-world designation or just descriptive
prose is unknown. Same low-confidence caveat.

---

## 6. New open questions the sheets raise — not currently in §14

These are not numbered, because inventing a Q-number would imply the designer had
already logged them. They are new.

- **Is Echo's faceplate a visor or a light?** The sheet's own callout reads
  **"Visor or Light"** and does not choose. This is not an art detail — an emissive
  faceplate is a readability channel during telegraphs and Impact Windows, and it
  affects M5 VFX. Nova's sheet separately labels a "Light", so the two fighters may
  not be consistent here.
- **Are the orange energy lines emissive at runtime?** Echo's back carries
  "Integrated Energy Lines" drawn flat, with no glow. Whether they light up — and
  whether they respond to the Ascension Meter — is unstated and would be a cheap,
  strong readability win if they do.
- **What does "SFN" stand for?** It is the only readable lettering on either
  fighter, on Nova's "Unique 'SFN' Unit Insignia". The GDD never expands it. If the
  UI or announcer strings ever need a unit name, this is the thread to pull.
- **Is the mezzanine reachable?** Page 11 shows a full upper tier with no visible route
  into the play space. If it is purely set dressing, the arena's vertical volume is
  decoration and the collision boundary is simply the walls — worth confirming before
  anyone builds a blocking volume for it.
- **Footwear branding is a rights question.** Both fighters wear athletic sneakers
  carrying a swoosh-style side mark. `CLAUDE.md` requires rights review for anything
  entering a submitted course build. If the final character treatment reproduces
  real-world branding, that is a rights-review item, not a look decision.

---

## 7. Unchanged by the sheets

For completeness — these §14 questions were checked against the recovered material and
**nothing in it speaks to them**:

- **Q29 — Crimson Vanguard's short in-combat UI label.** Page 14 gives only the formal
  title treatment "CRIMSON VANGUARD | PROJECT VALOR-7". **No short form is offered
  anywhere.** Still the designer's, still to be left blank rather than invented.
- **Q3, Q10, Q12, Q13, Q25** — no damage, range, cooldown, travel, or per-attack timing
  value appears on any sheet.
- **Q22 — is the 1 HP floor permanent or Clash-only?** No art bearing on it.
- **Q26, Q27, Q28, Q19, Q20, Q21** — timing and window values; no art bearing on them.
- **Q23 — duel timer.** Nothing.
- **Q31 — silent Phase 1 build.** Nothing.

**Q30 — Paragon heavy hero for Crimson Vanguard** is the one partial exception: the
sheets do not answer it, but page 14 now gives a concrete silhouette to evaluate
candidates against — mech proportion, small head relative to torso, oversized rounded
pauldrons, back vanes, fully enclosed fists. That makes the fit assessment possible
where before it was guesswork.
