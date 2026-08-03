# Group 08 — Asset decisions (Q30, Q31, item 20)

**Dispatched:** 2026-08-02 · **Designer dispatch, research-and-planning seat**
**Consumes:** `design-brief.md` §12.4 / §12.6 / §14 · `project-brief.md` · `CLAUDE.md` ·
`gdd/sections/05`, `gdd/sections/07` · `gdd/reference/page-10`, `page-12`, `page-13`, `page-14`
**Writes to:** this file only.

| Item | Kind | Status |
|---|---|---|
| **Q30** — Paragon heavy hero for Crimson Vanguard: yes/no, and by when | **KIND B** — design + schedule judgement | **PROPOSED** |
| **Q31** — Is a silent Phase 1 build acceptable | **KIND B** — design judgement with a GDD tension | **PROPOSED** |
| **Item 20** — Swoosh-style footwear mark on both fighter sheets | **KIND A-ish** — determinate *build action*, non-determinate legal exposure | **APPROVED for the build action; the legal question is referred to a human** |

## The two rules this whole file is written against

**1. Assets cost $0.** Unreal starter/template content, the Fab free tier, free Quixel
grants, Mixamo, Paragon, the Game Animation Sample Project. **No purchase is assumed
anywhere below.** Where no free asset was verified, the gap is named and a free fallback
is proposed. Every asset still passes the GDD's HUMAN APPROVAL GATE — rights review
included — before it enters the build. Nothing is approved by appearing here.

**2. The game ships 1 September 2026. Today is 2026-08-02 — 30 days.** Phase 1 (M1–M4)
must be a duel that can be fought start to finish, dressed with free proxy assets.
Anything that cannot be built *and tuned* in 30 days is out of scope however good it is.
**Picking a proxy asset is asset selection and is legitimate in M1–M4. Tuned presentation
is M5 and is not pulled forward by anything in this file.**

---

## Q30 — Paragon heavy hero for Crimson Vanguard

- **Kind:** KIND B — a design and schedule judgement. The designer decides.
- **Status:** **PROPOSED**
- **Unblocks build step:** **M1-23** — stand up the dressed proxies. Also gates **M2-04**
  (`DT_VanguardAttacks` rows) and **M2-05** (`BP_CrimsonVanguard` scale, item 28 = 208 cm).
- **Where it lands:** `/Game/ParagonCrunch/…` (imported pack) → referenced by
  `BP_CrimsonVanguard`'s `SkeletalMeshComponent`, its `AnimBP`, and the four attack
  montages. **Milestone: M1 (asset selection) / M2 (montage authoring).** Not M5.

### Proposed answer

**YES — take a free Paragon heavy, and make `Paragon: Crunch` the first candidate with
`Paragon: Steel` as the named alternate. Decide it by a hard date: 2026-08-09, and in any
case before `M2-04`/`M2-05` are authored.** If the swap has not landed by that date, it is
**dead for Phase 1** — ship the scaled-mannequin-plus-blocky-proxy fallback from the pulled
sprint handoff and re-open the Paragon swap as **M5** character treatment.

The recommendation is conditional on **one structural choice that is what makes it cheap**:

> **Build the rival on the Paragon character's OWN skeleton, using that pack's OWN
> animation cycles as the source for attacks A–D. Do not retarget Manny animations onto
> it.** Then there is **no `IK Retargeter` pass on the critical path at all.** The
> retargeting cost that `design-brief.md` §12.4 budgets "a full day" for only exists if
> you insist on driving a Paragon mesh with Mannequin animation.

The rival shares **no** framework with the player — the SHARED PLAYER-KIT SCOPE RULE binds
Echo and Nova to one framework and says nothing about Crimson Vanguard. So the rival is
free to sit on a foreign skeleton with a foreign `AnimBP` at zero cost to the shared
player kit. Echo (Manny) and Nova (Quinn) stay exactly where the sprint handoff put them.

### Why

**1. Crunch is the closest free match to the recovered silhouette, and it is not close.**
Judged against `gdd/reference/page-14-crimson-vanguard.md` line by line:

| Sheet requirement (page 14) | `Paragon: Crunch` | `Paragon: Steel` | Scaled Manny + blocks (fallback) |
|---|---|---|---|
| "proportion reads **mech/powered-armor rather than human**" | **Yes — a military android.** It *is* a robot | Yes — a cyborg in powered armor | No. Human proportion with boxes stuck on |
| "the head is **small relative to the torso**" | **Yes** | Partial — helmeted, more human head-to-torso | No |
| "oversized **rounded pauldrons** above and outboard of the shoulders" | Yes — heavy shoulder plating | **Yes, and rounder** | Only as attached proxy blocks |
| "**fully enclosed armored fist** … there is no visible weapon barrel, blade, or muzzle: **the hand *is* the weapon**" | **Exactly yes.** Crunch's whole kit is fists | **No — Steel carries a shield.** Removable, but it is a mesh edit and his anim set is shield-led | Neutral |
| "large vertical red **vanes** rising above the shoulders" (back thrusters) | **No — GAP** | **No — GAP** | **No — GAP** |
| "glossy **red** armor over matte dark-grey/black substructure" | Material Instance recolor | Material Instance recolor | Material Instance recolor |
| "two angular eye slots **glow amber-orange**" | Emissive parameter | Emissive parameter | Emissive parameter |
| 208 cm (item 28, APPROVED) | Uniform scale to fit | Uniform scale to fit | Uniform scale to fit |
| "substantially broader armored mass" (GDD §07) | **Yes, natively** | **Yes, natively** | Faked with attached blocks |

Crunch wins the two lines that matter most for *gameplay readability*, not just looks:
the **enclosed fist with no weapon** (Attack A is "close-range committed gauntlet force",
and Crunch has no weapon to explain away) and the **mech proportion with a small head**,
which is the whole point of the page-10 scale sheet — the rival's dominance reads as
**width, not height**.

**2. It is animation source material, not just a mesh — and that is where the days
actually are.** Each Paragon pack ships "the character model, animations, AnimBP's, skins
and FX" and, across the release, "thousands of textures, VFX and animation cycles, as
well as dialogue with hundreds of sound cues." The blocky-mannequin fallback has **no
source animation for a heavy armored attacker at all** — Mixamo has generic human punches
that will read as a person, not as 208 cm of armor. Crunch ships committed heavy strikes,
a lunge and an uppercut on the right body. **This buys back M2 time rather than spending
it.** The montage authoring work — slicing sections and placing `ANS_Telegraph`,
`ANS_ActiveHit`, `ANS_Recover` at Q25's durations — is *identical* whichever mesh is used,
so it is not a cost of this decision.

**3. The "before M4 range tuning" reason in §14 is real, and this answer tightens it.**
§14 says a late swap re-tunes every Q10 range value twice. Two clarifications the
developer needs:

- **Q10's bands are centre-to-centre**, so a mesh swap does **not** invalidate the
  *selection* bands (`A 0–260 · B 90–520 · C 240–420 · D 400–840` cm). Those are actor
  distances and are mesh-independent.
- What a mesh swap **does** invalidate is the **alignment between the band and the visible
  fist** — the hit-trace socket position, the capsule radius and half-height, and whether
  a strike that fires at 240 cm looks like it connects. That is the GDD §07 hard rule:
  *"The height difference must not create unfair hidden reach or collision behavior."*
  It is a re-validation pass, not a re-derivation.

So the deadline is **not** "before M4"; it is **before `M2-05` sets the rival's scale and
`M2-04` fills the attack rows**, because those two are what the fist alignment is measured
against. That is earlier and stricter than §14 said, and it is why a calendar date is
attached.

**4. If it slips, the fallback is genuinely fine and the decision must be allowed to die.**
The pulled sprint handoff already specifies a scaled mannequin or blocky red proxy. That
ships a fought duel. **A prettier rival is worth zero if it costs the M4 gate.** The
week-long window is the entire concession the 30-day calendar can make.

### What is explicitly NOT part of this answer

- **No `IK Retargeter` work on the critical path.** If someone starts retargeting Manny
  animation onto Crunch, the decision has changed shape and the day cost triples.
- **No back-vane / thruster geometry.** Neither candidate has it. **Named GAP.** Phase 1
  fallback: nothing, or two attached static-mesh vanes at a back socket if it costs
  minutes. Authored thruster VFX is **M5** and is already in `design-brief.md` §1.3.
- **No Paragon VFX or sound wired into the build in Phase 1.** The packs contain them; see
  Q31. Wiring and tuning them is presentation work and is **M5**.
- **Nothing about Echo or Nova changes.** Manny and Quinn stand.

### Prior art / real sources, with licence terms

| Source | What it gives | Licence, as stated by the source |
|---|---|---|
| [Paragon: Crunch — Fab](https://www.fab.com/listings/c23ee3a7-4a73-4a83-9061-30b682d269f8) | Model, animations, AnimBP, skins, FX for a **military android** built for the Omeda City military | Free. Part of the Paragon release below |
| [Paragon: Steel — Epic / Fab](https://www.unrealengine.com/marketplace/en-US/product/paragon-steel) | Model, animations, AnimBP, skins, FX for a **cyborg with a shield** | As above |
| [$17,000,000 of Paragon content for FREE — Unreal Engine](https://www.unrealengine.com/paragon) | **39 AAA characters + 1,500+ environment components** | Free to all Unreal Engine developers |
| [Final Round of Free Paragon Assets Released — Unreal Engine](https://www.unrealengine.com/en-US/blog/final-round-of-free-paragon-assets-released) | The batch that completed the 39-character roster | Free |
| [Get Paragon UE4 character and environment assets free — CG Channel](https://www.cgchannel.com/2018/09/get-free-paragon-ue4-character-and-environment-assets/) | Independent restatement of the licence | **"Free downloads … can be used in commercial projects, but are only licensed for use with Unreal Engine. You may not use the trademark PARAGON to advertise or name your game."** |
| [Free Paragon Assets Get an Update — Unreal Engine](https://www.unrealengine.com/en-US/blog/free-paragon-assets-get-an-update) | Packs updated to **include Animation Blueprints**; Epic livestream on retargeting, strafe locomotion, blendspaces, sync markers, additive animation | Free |
| [5500+ Free Retargeted Animations for UE5 — Paragon + Infinity Blade Effects (2 GB)](https://dev.epicgames.com/community/learning/tutorials/qB07/unreal-engine-5500-free-retargeted-animations-for-ue5-paragon-infinity-blade-effects-2gb-pack) | Community pack of Paragon animation **already retargeted to UE5** | **Community-published — the underlying Epic licence still governs, and this specific redistribution needs its own rights review before use.** Do not treat as pre-cleared |

**Licence consequences the rights review must record, not just note:**

1. **"Only licensed for use with Unreal Engine."** Ascendant Impact is a UE 5.8 project, so
   this is satisfied. It would not be if any Paragon asset were exported elsewhere.
2. **"You may not use the trademark PARAGON to advertise or name your game."** The
   in-combat label question (Q29, proposed `VALOR-7`) is unaffected. **No credit, splash
   screen, store text, or course submission blurb may say "Paragon".** An asset-credits
   list may name the pack factually; marketing may not.
3. The community 5500-animation repack is **third-party redistribution**. §12.1 already
   flags that Mixamo assets "may not be redistributed as standalone assets"; the same
   caution applies here. **Prefer downloading the packs from Fab directly.** Listed
   because it exists and would save time, marked because it is not automatically clean.

### Cost in days against the 30 remaining

| Path | Work | Day cost | Verdict |
|---|---|---|---|
| **A — Crunch on its own skeleton, own animations** (recommended) | Download + import pack · uniform-scale to 208 cm and measure bounds · red/black `Material Instance` + amber emissive · add hit-trace sockets to the fist bones · rebuild capsule radius/half-height · re-validate fist alignment against Q10's bands | **≈ 1.0 day**, and it **returns ≈ 0.5–1.0 day** on M2 attack-animation sourcing that the fallback would have to spend on Mixamo hunting and cleanup | **Net ≈ 0 to +0.5 days.** Affordable |
| **B — Crunch mesh driven by Manny/Mixamo animation via `IK Retargeter`** | Path A **plus** a retarget rig, chain mapping, and proportion fixes on a non-humanoid ape-proportioned robot | **+1.0 to +1.5 days** on top of A | **Do not do this.** It buys nothing the pack's own animation does not already give |
| **C — swap after `M2-04`/`M2-05` are authored** | Path A **plus** re-validating every fist-alignment and capsule check a second time, plus re-checking Q13's 600 cm travel end-distance and Q25's Active windows against a new reach | **+2.0 to +3.0 days** | **Forbidden.** This is exactly the double-tuning §14 warned about |
| **D — fallback: scaled mannequin + blocky red proxy** | Already scoped in the sprint handoff | **0 days** (already planned) | The floor. Ships regardless |

**Decision deadline, stated as a build gate rather than a vibe:** the Paragon swap must be
**imported, scaled and socketed before the first row of `DT_VanguardAttacks` is filled**.
Calendar backstop **2026-08-09**. After that, path D and the swap becomes M5.

### Open sub-questions the designer should answer with this one

- **Crunch or Steel?** Crunch on the fist criterion and the mech-proportion criterion;
  Steel on the rounded-pauldron criterion. **Crunch is recommended** because the shield is
  a mesh *and* animation problem, and because "the hand is the weapon" is a page-14 line
  about the character's whole read. Whoever decides should look at both on Fab first —
  this file judged them from published descriptions, not from opening the packs.
- **Is the missing back-vane silhouette acceptable in Phase 1?** It is a named GAP. Attack
  D's readability requirement is *"thruster cue before movement"*, and in Phase 1 that cue
  is carried by the telegraph pose and emissive, not by geometry.
- **Does the pack's own animation actually contain a usable lunge for Attack D at
  600 cm (Q13)?** Cannot be answered without opening the pack. **If not, Attack D falls
  back to Motion Warping over whatever forward animation exists**, which is what R5 and
  group 04 already assume.

---

## Q31 — Is a silent Phase 1 build acceptable?

- **Kind:** KIND B — a design judgement with a genuine GDD tension in it. The designer decides.
- **Status:** **PROPOSED**
- **Unblocks build step:** **M5-04** (the audio pass). Also determines whether an
  **audio floor** is added to M1–M4, and if so where.
- **Where it lands:** if silent — nowhere, and that is the point. If the floor is taken —
  `/Game/Audio/SFX/` `USoundWave` assets, played by `Play Sound 2D` from **existing**
  call sites: `AN_TelegraphStart`, `BP_ImpactWindowDirector.OpenWindow`,
  `ResolveIncomingHit`, the `State.PerfectWindow` branch, `OnPhase2Committed`, and
  `BP_FinalClashDirector`. **No new systems.** Milestone: **M1–M4 for the floor
  (asset selection), M5 for everything else.**

### Proposed answer

**Two answers, because the question has two halves and §14 only asked one of them.**

**(a) Yes — shipping Phase 1 without an audio *pass* is acceptable, and the designer
should say so now rather than discover it on 31 August.** No M1, M2, M3 or M4 gate names
audio. The only milestone whose GDD gate says *"sound"* is **M5**, and M5 is Phase 2. A
silent M4 is a *passing* M4 under the GDD's own table.

**(b) No — shipping *literally* silent is not the right call, and the reason is the one
this dispatch was told to address.** The GDD names sound as a channel twice, in two
load-bearing places:

> Telegraph — "Show committed pose, **warning lights, sound**, readable direction"
> — GDD §04, `gdd/sections/04-…`, PDF p.5
>
> Phase 2 — "signaled once with stronger thruster output, warning lights, **sound**, and
> armor-energy presentation" — GDD §04, PDF p.6

**Recommendation: ship Phase 1 with a named, capped audio floor of ~6–9 one-shot cues and
nothing else.** Estimated **0.5 day** total including sourcing. Everything past that —
mixing, attenuation, ambience, footsteps, music, MetaSounds, ducking, occlusion — is
**M5** and is not pulled forward by this.

### Why — and what carries the readability load if the answer is silence anyway

The honest position is that silence costs less than it first looks, **except in one
place**. Channel-by-channel, against what is already built:

| GDD moment | Channels the GDD names | Survive in a silent Phase 1 | Verdict |
|---|---|---|---|
| **Telegraph** | committed pose · warning lights · **sound** · readable direction | **3 of 4.** The committed pose is the montage's telegraph section; readable direction is body facing under lock-on; warning lights are the `ANS_Telegraph`-driven emissive scalar that already exists | **Survivable.** Group 03's reaction check is a *visual* budget — the perfect-press pocket opens at ~250 ms against a 0.40 s Phase 2 telegraph, and Q25 gives 0.55–0.95 s in Phase 1. Nothing in that math needs audio |
| **Phase 2 signal** | thruster · warning lights · **sound** · armor-energy | **3 of 4**, plus a fourth the GDD does not list: the health bar visibly crossing 50%. §8.2's Phase 1 realization is already "an emissive-intensity change plus a brief pause" | **Survivable** |
| **Impact Window prompt** | *(GDD names no channel — it is a 0.35–0.50 s UMG prompt)* | **1 of 1.** `WBP_ImpactPrompt` appearing is the *only* signal | **This is where silence actually hurts.** A 0.35 s visual-only prompt with no onset sting is the single hardest thing in the build to react to, and failing it costs the +20 row |
| **Hit connect / perfect dodge** | *(not named)* | Visual only. Hit-stop is M5, so in Phase 1 a landed hit and a whiffed hit look similar | **Real loss.** Perfect dodge is the +12 event and the skill the whole design is about |
| Footsteps, ambience, music | *(not named anywhere)* | Absent | **No loss.** Not required by any gate |

So the floor is not "add audio"; it is **buy back the two channels the visuals cannot
cover**. Ranked by value per minute of work:

| # | Cue | Call site (already exists) | Why it is on the list |
|---|---|---|---|
| **1** | **Impact Window prompt onset** | `BP_ImpactWindowDirector.OpenWindow` | Highest value in the file. 0.35–0.50 s is at the edge of a visual-only read |
| **2** | **Telegraph start** — one low mechanical charge, pitch/volume varied per attack row | `AN_TelegraphStart` | Restores the GDD-named telegraph channel with **one** asset, not four |
| **3** | **Perfect dodge success** | `State.PerfectWindow` branch | Confirms the +12 read the game is built on |
| **4–5** | **Hit connect** — player lands / player is hit | `ResolveIncomingHit` | Makes damage legible before hit-stop exists |
| **6** | **Phase 2 commit** | `OnPhase2Committed` | Restores the second GDD-named sound channel. **One-shot, guarded by `bPhase2` — it cannot double-fire** |
| **7–9** | **Clash beat open · success · failure** | `BP_FinalClashDirector` | May reuse #1 for the beats. Success/failure need to differ audibly |

**The line this stays on the correct side of.** §11.6's test is *"does it cost schedule
time and require iteration to feel right?"* Dropping a `USoundWave` into an **existing**
Blueprint node is asset selection. **Authoring a mix is M5.** Two rules keep it there:

1. **One node per call site, no new class.** No `SoundClass` hierarchy, no submix, no
   attenuation asset, no MetaSound graph, no concurrency rules in Phase 1.
2. **All nine calls route through `BP_PresentationSubsystem`** — the same kill-switch that
   §4.10 already uses for hit-stop, camera and VFX. Audio is presentation, so it must be
   disable-able during diagnosis exactly like the rest. This costs one wrapper function
   and means M5's real audio pass has a single seam to fill.

### The defect this question uncovered

**`design-brief.md` §12.1 and §12.6 both rely on UE Starter Content, and Starter Content
appears to have been removed from the engine as of UE 5.7.** §12.6's audio fallback is
written as *"Starter Content has a handful of cues"* — on a 5.8 project that fallback may
not exist. §12.1 also lists Starter Content as a source of "basic materials", which the
**arena** plan in §12.5 leans on.

**Confidence: MEDIUM.** This came from a community/forum-grade source, not from Epic
documentation, and it is stated as "removed in 5.7, migrate from an older version." It is
**not** cited here as settled. **Action: someone opens UE 5.8, makes a project with Starter
Content ticked, and confirms in five minutes.** It is cheap to check and it invalidates two
sections of the brief if true. Logged in the ledger below as a GAP with a free fallback
either way (Fab free materials, Quixel free grants) so nothing is blocked on the answer.

### Prior art / real sources, with licence terms

| Source | What it gives | Licence, as stated by the source | Fit |
|---|---|---|---|
| [Sonniss #GameAudioGDC Bundle](https://gdc.sonniss.com/) · [the licence](https://sonniss.com/gdc-bundle-license/) · [archive](https://sonniss.com/gameaudiogdc/) | **25 GB+** of professional sound-effect libraries, free every year; a **GDC 2026** bundle is live | **"Worldwide, non-exclusive, royalty-free licence to use all or any of the sound effects."** Commercial use permitted, **no attribution required**, unlimited projects, for life. **Restriction: use for AI/ML training is strictly prohibited** | **Best licence terms found.** But it is a raw *library*, not game-ready cues — 25 GB of unsorted source recordings. **Right tool for M5. Overkill and a time sink for a 9-cue floor** |
| [Freesound.org](https://freesound.org/help/faq/) | Per-sound licensed community library; advanced search **filters by licence** | **Per sound.** CC0 sounds carry **no legal attribution obligation** (linked credit "preferred, not necessary"). **Every other CC licence on the site requires crediting the author in the derivative work** | **Best fit for the floor.** Filter to **CC0 only** and record the sound ID + author per asset. Mixed licences on one site is exactly the rights-review trap |
| [50 Free Game Sounds Pack — Fab](https://www.fab.com/listings/b8cc7270-5e0c-4ef7-a277-6a1d4b69358d?lang=en) | Combat, environment, crafting, interface, guns, explosions | Free listing on Fab; Fab standard licence. **Verify the specific listing's licence at claim time** | Good floor candidate — already `.uasset`-ready for UE |
| [Fab — Sound Effects channel, Unreal Engine](https://www.fab.com/channels/unreal-engine?categories=sound-effects&listing_types=audio) | The browsable free tier | Per listing; use the `Price > Free` filter | The place to look first |
| **Paragon character packs** (see Q30) | The release includes **"dialogue with hundreds of sound cues"** and per-character FX | Same Paragon licence as Q30 — free, **UE-only**, no "PARAGON" branding in marketing | **Cross-link: if Q30 is YES, part of this gap closes for free.** Crunch ships servo/impact cues on the correct character, already in the project, already rights-reviewed as one decision |
| UE **Starter Content** cues | A handful of generic cues | Ships with the engine | **See the defect above — may not exist in 5.8.** Do not plan on it |

**Licence consequences the rights review must record:**

1. **Sonniss forbids AI/ML training use.** Trivially satisfied by the shipped game — the
   build makes no model calls at all. **But it is a live constraint on Assignment #04's
   generative pipeline: no Sonniss audio may be fed to any generative tool, offline or
   otherwise.** Worth writing down because #04 and the game share a repository.
2. **Freesound is per-sound licensed.** A CC0 filter is not optional; a single CC-BY sound
   slipped into the floor creates an attribution obligation on the whole submission.
3. **Record, per cue, the source URL, the licence name, and the author** at the moment of
   download. Retro-fitting nine attributions in late August is how a rights review fails.

### Cost in days against the 30 remaining

| Option | Work | Day cost | Verdict |
|---|---|---|---|
| **Ship silent** | none | **0 days** | Passes every M1–M4 gate. Loses two GDD-named channels and the Impact-prompt onset |
| **The 6–9 cue floor** (recommended) | Source CC0/Fab-free cues (~2 h) · import (~0.5 h) · one `Play Sound 2D` behind a `BP_PresentationSubsystem` wrapper at nine existing call sites (~1 h) · sanity listen (~0.5 h) | **≈ 0.5 day** | Buys back the Impact-prompt onset, the telegraph channel and the Phase 2 signal for half a day |
| **Anything more in Phase 1** — mix, attenuation, ambience, music, MetaSounds, footsteps | — | **1.5+ days and unbounded iteration** | **Rejected. This is M5** and pulling it forward breaks milestone order |

**Recommended sequencing so this cannot eat the schedule:** the floor is authored **after
M4's gate is met**, not before. It is on the Phase-1 side of the line, but it is the *last*
thing in Phase 1. If M4 slips, the floor is the first thing cut and the answer reverts to
"ship silent" with no rework.

### What the designer is actually being asked to say

> **"Phase 1 ships without an audio pass. That is accepted, not discovered. [Take / do not
> take] the 0.5-day nine-cue floor. All remaining audio is M5."**

One sentence, on the record, is the whole deliverable of Q31.

---

## Item 20 — Swoosh-style footwear mark on both fighter reference sheets

> **This is not legal advice and I am not qualified to give it.** What follows states the
> facts on disk, names the risk plainly, cites the case law it found, and recommends the
> **conservative build action**. The legal question itself is referred to a human. The
> recommendation below is chosen so that **it costs $0 and 0 days whether the legal
> question is ever answered or not** — which is the whole reason it can be settled now.

- **Kind:** **KIND A for the build action** — there is a determinate answer and nothing to
  design. **KIND B / referred** for the underlying legal exposure, which is not mine to
  settle and is not determinate.
- **Status:** **APPROVED — the build action.** The legal characterization is **REFERRED TO
  A HUMAN** and is not approved here.
- **Unblocks build step:** **M1-23** (stand up the dressed proxies) — as a *recorded
  verification*, not as work. And **M5-06** (final character treatment) — as a *binding
  constraint on art not yet made*.
- **Where it lands:** the **rights-review record** for M1-23, and a one-line constraint on
  the M5-06 character-art brief. **No asset changes. No file is edited. No `gdd/` file is
  touched.**

### The facts, before any opinion

1. **The mark appears in three places, and all three are the same place: the GDD's
   concept-art reference sheets.** `page-10` (both fighters, in the scale line-up),
   `page-12` (Echo, low-profile shoe), `page-13` (Nova, high-top "Designed Light
   Sneakers"). It is described in `gdd/reference/` as *"a swoosh-style side mark."*
2. **`gdd/reference/page-10` already flags it as AMBIGUOUS and unresolved by the
   document:** *"Whether that is intended branding, placeholder art, or stylistic choice is
   not stated anywhere in the document."* **Nothing in the GDD's authored text asks for a
   brand mark.** The sheets' own printed callouts describe the footwear as
   **"Custom Sole Unit with Grip"** and **"Designed Light Sneakers"** — the document's own
   language is *custom* and *designed*, not branded.
3. **The mark is on no asset in the build, and on no asset in the plan.** The proxy cast is
   **Echo → Manny**, **Nova → Quinn**, **Vanguard → scaled mannequin or Q30's Paragon
   heavy**. UE5's Manny and Quinn are stylised mannequins in a segmented bodysuit; they
   carry **no separate footwear and no third-party brand marks of any kind**. The Paragon
   candidates carry Epic's own in-fiction Omeda City design, not a real-world mark.

**Therefore: the Phase 1 build has zero footwear-branding exposure today. There is nothing
to remove.** The exposure is entirely **prospective** and arises at exactly one moment —
when bespoke character art is authored *from* the sheets. That is **M5-06**, Phase 2, after
1 September.

### The exposure, course submission versus commercial release

| | **A submitted course build** | **A commercial release** |
|---|---|---|
| Nature of use | Non-commercial, not distributed, shown to an instructor and a class | Distributed to the public, sold or monetised |
| Practical enforcement risk | **Low.** Trademark claims generally turn on use in commerce and likelihood of confusion; a coursework build is neither sold nor advertised. **Low is not zero, and "no one will notice" is not a legal position** | **Materially higher, and with an active enforcer** |
| The favourable precedent | **Rogers v. Grimaldi**, 875 F.2d 994 (2d Cir. 1989), applied to games in **AM General v. Activision Blizzard** (S.D.N.Y. 2020): depicting real trademarked objects in an expressive work is protected where the use has *"artistic relevance to the underlying work whatsoever"* and does not *"explicitly mislead as to the source or the content of the work."* Humvees in *Call of Duty* passed | Same precedent, same direction |
| **The unfavourable development** | **Jack Daniel's Properties v. VIP Products**, 599 U.S. 140 (2023): where a mark is used **as a designation of source for the alleged infringer's own goods**, the Rogers test **does not apply at all** and the court goes straight to likelihood of confusion. Rogers survives for expressive uses, but the door it sits behind narrowed | Same, and it bites harder where the item is a *product* the player sees and could want |
| **The specific enforcer** | Nike filed **intent-to-use applications in 2021 covering virtual goods including footwear for use in online virtual worlds**, has litigated virtual-sneaker cases (**Nike v. StockX**, 2022) and has pursued sneaker customisers and artists | **This is the fact that most distinguishes it from the Humvee case.** AM General had not staked out the virtual-goods class; the swoosh's owner demonstrably has |

**The unresolved question, stated honestly:** is a brand mark on a hero character's shoes
an *artistic depiction of the real world* (Rogers, likely protected) or a *virtual product
bearing a source identifier* (Jack Daniel's, straight to confusion analysis)? **This
research did not find a decided case on game costume assets either way.** That is precisely
why the build should not be the thing that finds out.

### The remedy — concrete, and it costs nothing

1. **M1–M4 — verify and record, do not change anything.** At M1-23 the rights review
   records, as a **checked** line rather than an assumption: *"Proxy meshes (Manny, Quinn,
   and the Q30 rival) carry no third-party brand marks. Verified in-editor on
   `<date>` by `<name>`."* Somebody looks at the meshes. Five minutes.
2. **M5-06 — the constraint on authored art, written into the brief now while it is free.**
   **No authored character art for Echo or Nova reproduces the swoosh-style side mark.**
   Replace it with the design language the GDD already prints on its own sheets:
   - Echo: **"Custom Sole Unit with Grip"** — the orange lug pattern with the circular
     pivot disc at the ball of the foot that `page-12`'s inset already shows.
   - Nova: **"Designed Light Sneakers"** — high-top, orange accents, pale midsole.
   - And the project's own mark where a mark is wanted: Nova's circular
     **"SFN" unit insignia** and Echo's unlettered **"Unique Badge"**. *(Item 45 already
     ships `FighterUnitLine` blank because "SFN" is unestablished — that is a mark the
     project **owns**, which is exactly why it is the right one to lean on.)*

   **This is a constraint on art that does not exist yet, not a rework of art that does.
   Applied now it costs zero. Applied after M5-06 it costs a re-texture.**
3. **Do not edit the reference sheets, and do not edit `gdd/`.** `design/decisions.md`
   rule 2 is explicit: `gdd/` is mechanically derived and hand-editing it silently forks
   the source of truth. `gdd/reference/page-13` separately warns against silently
   "correcting" anything in a sheet. **The sheets are concept art inside a submitted
   *document*; they are not assets inside a *build*, and the two questions are different.**
   If the human decides the mark should also leave the document, that is a change to the
   **PDF** followed by a re-export — rule 4 territory, and a separate decision from this
   one.
4. **One constraint on Assignment #04, because #04 and the game share a repository.** The
   #04 pipeline reads `gdd/reference/`, and those files contain the phrase *"a swoosh-style
   side mark."* In context that is a **description of an image**. It must never be
   propagated into a **generated art brief, asset spec, or costume description** as an
   instruction. Add it to the critic agent's checks: **no generated content may name,
   describe, or instruct the reproduction of a real-world brand mark on any fighter.**

### Prior art / real sources, with terms

| Source | What it establishes |
|---|---|
| [AM General v. Activision Blizzard — Technology & Marketing Law Blog](https://blog.ericgoldman.org/archives/2020/04/humvee-cant-stop-depictions-of-its-vehicles-in-the-call-of-duty-videogame-am-general-v-activision-blizzard.htm) · [Finnegan analysis](https://www.finnegan.com/en/insights/blogs/incontestable/in-legal-warfare-over-humvee-trademarks-the-first-amendment-goes-beyond-the-call-of-duty-in-dismissing-am-generals-claims.html) · [Sunstein LLP](https://www.sunsteinlaw.com/publications/ec-activision-wins-the-trademark-war-first-amendment-protects-depiction-of-humvees-in-realistic-video-games) | The two-prong **Rogers** test applied to a video game: artistic relevance + not explicitly misleading. Depicting real trademarked objects in games has succeeded |
| [Jack Daniel's Properties v. VIP Products — Davis Wright Tremaine](https://www.dwt.com/insights/2023/06/scotus-jack-daniels-trademark-rogers-test) · [Morgan Lewis](https://www.morganlewis.com/pubs/2023/06/a-win-for-trademark-owners-the-supreme-courts-ruling-in-jack-daniels-properties-inc-v-vip-products) · [Justia, 599 U.S. 140 (2023)](https://supreme.justia.com/cases/federal/us/599/22-148/) | **Rogers does not apply** where the mark is used as a **source designation for the defendant's own goods**. Rogers otherwise survives for expressive works |
| [Nike virtual-goods trademark filings — Lexology](https://www.lexology.com/library/detail.aspx?g=d8c8edfe-51ea-48aa-be06-05e8ed8e302f) · [Nike v. StockX — Katten](https://katten.com/trademark-infringement-in-the-metaverse-nike-sues-online-resale-platform-alleging) · [Bloomberg Law, sneaker artists](https://news.bloomberglaw.com/ip-law/nike-fires-warning-shot-to-sneaker-artists-with-trademark-suit) | **2021 intent-to-use filings covering virtual footwear in online virtual worlds**, plus active litigation over virtual sneakers and against customisers. The owner is present in this exact space |
| [The use of trademarks in video games in light of current case law — ROWAN LEGAL](https://rowan.legal/en/news/the-use-of-trademarks-in-video-games-in-light-of-current-case-law/) | General survey of the area |

### Cost in days against the 30 remaining

**0 days, now and at M5.** The M1-23 action is a five-minute verification that produces a
written line in the rights-review record. The M5-06 action is one sentence added to a brief
for art that has not been authored. **There is no rework, no asset change, and no schedule
impact in either direction.** That is why this one can be settled today rather than carried.

**What a human still owns:** whether the mark is acceptable in the **submitted GDD
document** (as opposed to the build), and whether the institution has its own policy on
third-party marks in coursework. Neither is answerable from this seat.

---

## The $0 asset ledger

**This is the artefact the rights review actually uses.** One row per asset class the
**Phase 1 duel (M1–M4)** needs. Every row names a free source and its licence, or is
marked **GAP** with a free fallback. **No row assumes a purchase.**

**Nothing in this table is approved by appearing in it.** The GDD's HUMAN APPROVAL GATE
requires human review, technical validation, rights review and explicit approval on each
asset before it enters the build. Availability and licence terms **must be re-confirmed at
claim time** — Fab listings change tier, and several rows below are per-listing rather than
blanket-free.

| # | Asset class | Named free source | Licence, as stated by the source | Status |
|---|---|---|---|---|
| 1 | **Player mesh — Echo** | **UE5 Mannequin `Manny`**, uniform-scaled to **183 cm** | Ships with the engine | **OK.** No branding present (item 20) |
| 2 | **Player mesh — Nova** | **UE5 Mannequin `Quinn`**, uniform-scaled to **173 cm**. *Deferred until Echo proves the shared pipeline* | Ships with the engine | **OK.** No branding present (item 20) |
| 3 | **Rival mesh — Crimson Vanguard** | **`Paragon: Crunch`** (Q30 proposed; `Paragon: Steel` alternate), uniform-scaled to **208 cm** | Free. **Licensed for use with Unreal Engine only.** **"You may not use the trademark PARAGON to advertise or name your game."** | **PROPOSED (Q30).** Deadline **2026-08-09**. Fallback below |
| 3b | **Rival mesh — fallback** | Scaled Mannequin + non-animated blocky pauldron/gauntlet static meshes on bone sockets + red/black `Material Instance` | Engine + authored | **OK.** Ships regardless |
| 4 | **Rival back-vane / thruster silhouette** | *(page-14: "large vertical red vanes rising above the shoulders")* | — | **GAP.** No free asset matches. Fallback: **omit in Phase 1**; Attack D's cue is telegraph pose + emissive. Geometry/VFX is **M5** |
| 5 | **Player locomotion animation** | UE **Third Person template** `AnimBP` + blendspaces | Ships with the engine | **OK.** Motion Matching / Game Animation Sample deliberately **not** used in Phase 1 (R2) |
| 6 | **Player combat animation** — light combo, dodge, counter | **Mixamo** (free Adobe ID), retargeted with `IK Retargeter` | Free; usable in commercial projects; **may not be redistributed as standalone assets** | **OK, with a standing GAP:** no free set has the exact martial-arts weight the design wants (§12.6). **The tightest resource in the schedule** |
| 7 | **Rival attack animation A–D** | **Crunch's own cycles** if Q30 = yes (heavy strikes, lunge, uppercut, on the right body) · **Mixamo** if Q30 = no | Paragon licence · Mixamo licence | **Conditional on Q30.** If Q30 = no this is a **GAP** — generic human punches on a 208 cm frame |
| 8 | **Game Animation Sample Project** | Epic, free | Free; **licensed for use with Unreal Engine only** | **Phase 2 / source-of-individual-clips only** (R2). Not a Phase 1 dependency |
| 9 | **Arena geometry — Shattered Ring** | **Authored in-editor**: geometry brushes / simple static meshes. **2400 × 1600 cm** (Q24), long axis = doorway axis | Authored by the team | **OK — $0 by construction.** The four functional arena requirements are met by **layout**, and layout is free |
| 10 | **Arena materials / surfaces** | **Quixel Megascans free listings on Fab** (`Price > Free`); **Fab free tier** industrial concrete / scuffed metal / painted steel | Per listing. *"What you acquire on Fab you keep forever."* The blanket free-to-everyone period has ended — **free/paid is now per-listing** | **OK, verify per listing at claim time.** Prefer lighter listings over Nanite-dense ones |
| 11 | **Arena props / set dressing** | **`Soul: City`** (free Epic content, industrial/urban) · **Fab Limited-Time Free rotation** | Free Epic content · claim-during-window, keep forever | **OK.** **Do not plan around any specific rotating freebie.** Standing recommendation: claim the weekly Fab freebies every week to 1 September |
| 12 | **UE Starter Content** (materials + the handful of audio cues §12.6 leans on) | Ships with the engine — **historically** | Ships with the engine | **GAP, MEDIUM confidence.** Search results indicate **Starter Content was removed from the engine in UE 5.7**. Source is community-grade, **not Epic documentation. Verify in five minutes by ticking Starter Content on a new 5.8 project.** If true it invalidates part of `design-brief.md` §12.1 and §12.6. Fallback: rows 10 and 13 cover both uses |
| 13 | **Character / rival materials, emissive accents, warning lights** | **Authored `Material Instance`s** on a shared master material — Echo orange, Nova preserved palette, rival red/black + amber emissive | Authored by the team | **OK — $0.** Phase 1 uses **flat emissive parameters only**. Nova must **not** be recoloured cyan (GDD §07) |
| 14 | **VFX** | Phase 1: **none authored** — emissive material parameters stand in. Paragon packs ship FX as **M5** source material | Paragon licence | **OK.** Niagara authoring is **M5** and is already deferred in §1.3 |
| 15 | **Audio — SFX** | **Baseline: silent** (Q31a). **Floor, if taken:** **Freesound.org filtered to CC0** · **`50 Free Game Sounds Pack` on Fab** · **Paragon sound cues** already in-project if Q30 = yes | **Freesound CC0: no legal attribution obligation** — *every other licence on the site requires crediting the author, so the CC0 filter is mandatory* · Fab per-listing · Paragon licence | **GAP CLOSED at floor level.** `design-brief.md` §12.6's *"no free source verified"* is **superseded** by this dispatch |
| 16 | **Audio — the M5 library** | **[Sonniss #GameAudioGDC Bundle](https://gdc.sonniss.com/)** — 25 GB+, a **GDC 2026** bundle is live | **"Worldwide, non-exclusive, royalty-free licence."** Commercial use, **no attribution required**, unlimited projects, for life. **Restriction: use for AI/ML training is strictly prohibited** | **OK for M5.** Too large and too raw for a 9-cue Phase 1 floor. **The AI/ML clause binds Assignment #04: no Sonniss audio into any generative tool** |
| 17 | **Music** | **Incompetech / Kevin MacLeod** — 2,000+ royalty-free tracks | **CC BY 4.0 — attribution is required**, naming track, Kevin MacLeod, incompetech.com, and the licence. A paid attribution-free licence exists and is **not** taken | **Not needed in Phase 1** (Q31 scopes music out). **Free option verified for M5**, with an attribution obligation that must be honoured in a credits screen |
| 18 | **UI / HUD / result screens** | **UMG**, engine-shipped fonts, plain bars and text | Ships with the engine | **OK.** GAP: **no icon set verified.** Fallback: **text labels and plain bars**, which is all the Phase 1 HUD needs. Motion-designed UI is **M5** |
| 19 | **Character art matching the reference sheets** | *(pages 12, 13, 14)* | — | **GAP, standing and unchanged from §12.6.** Proxies stand in. Real character treatment is **M5 / Phase 2**. **Item 20's constraint binds this row** |

### Gaps this dispatch could not close with a free source

| Gap | Why | Fallback that ships |
|---|---|---|
| **Rival back-vane / thruster geometry** | Neither Paragon candidate has it; no free armored-mech asset matched page 14 | Omit in Phase 1. Telegraph pose + emissive carry Attack D's cue. **M5** |
| **A martial-arts strike set with the intended weight** | Standing §12.6 gap. Mixamo is generic | Mixamo + Q25's notify timings do the *gameplay* work; the *feel* is **M5** |
| **Character art matching the sheets** | Standing §12.6 gap | Dressed proxies. **M5** |
| **UI icon set** | Not researched — out of budget | Text and plain bars. Costs nothing and reads fine |
| **UE Starter Content in 5.8** | MEDIUM-confidence removal claim, community-grade source | Rows 10 and 13. **Verify in-editor in five minutes** |

### Research budget

**12 of 15 WebSearch sources used.** Stopped with margin rather than spending the last
three on the icon set and on confirming the Starter Content removal from Epic
documentation — both are cheaper to answer by opening the editor than by searching.

### Constraint compliance

| Constraint | How this file complies |
|---|---|
| **SCOPE LOCK** | One arena, one rival, two player avatars on one framework. No extra characters, arenas, attacks or modes are proposed. Q30 swaps a **mesh**, not a design |
| **No runtime AI-model calls** | Nothing here proposes one. Two *licence* constraints on **offline** tooling are recorded: Sonniss forbids AI/ML training use, and the #04 critic must not propagate the brand-mark description into a generated art brief |
| **Milestone order** | Q30 and the ledger are **asset selection**, legitimate in M1–M4. Q31's floor is capped at nine one-shots behind the existing presentation subsystem and is sequenced **after M4's gate**. Every tuned thing — mix, VFX, camera, character treatment, back-vane geometry — is placed in **M5**. Item 20 adds a constraint to M5-06 without doing M5 work |
| **$0 / never assume a purchase** | Every row names a free source or a free fallback. Incompetech's paid attribution-free option is named and **explicitly not taken**. Five gaps are named rather than papered over |
| **Numbers unchanged** | This file changes no timing or tuning value. It cites **208 cm** (item 28, APPROVED), **183 / 173 cm**, **2400 × 1600 cm**, **600 cm** and Q25's windows as context only |
| **This is Ascendant Impact** | Echo, Nova, Crimson Vanguard / Project Valor-7, the Shattered Ring, Ascension Meter, Impact Windows, the Final Clash. No content from any other project appears |
