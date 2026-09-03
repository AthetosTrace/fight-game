# Ascendant Impact — operating rules inside the Unreal project

**Rewritten 2026-09-02.** The previous version described two separate repositories and
told agents to keep Vanguard attacks B–D disabled. Both rules are retired: there is one
repository now, and building a second and third Vanguard attack is Steps 3 and 4 of the
plan.

**The plan is `../FINISH-PLAN.md`. Do only what a numbered step in it asks for.**

## Binding rules

- **Never commit Blueprint or Unreal binary assets.** No `.uasset`, no `.umap`, no
  `Content/` binaries, in any commit an agent makes. Commit code, docs, config and
  scripts only. If assets need committing, the user does it by hand.
- **Never commit generated folders** — `Binaries/`, `DerivedDataCache/`, `Intermediate/`,
  `Saved/`, `.vs/`. They are already in `.gitignore`; keep it that way.
- **Blueprint-first. No C++.** There is no toolchain on this machine and the project
  packages only because it is genuinely Blueprint-only.
- **Do not install plugins or enable ones with Runtime modules** without explicit
  approval. Doing so silently reclassifies the project as code-based and breaks
  packaging outright.
- **Do not edit binary Unreal assets on the filesystem.** All editing goes through the
  Unreal MCP against a live editor.
- **Checkpoint before changing approved geometry** — duplicate the level into
  `/Game/AscendantImpact/Maps/Checkpoints/`.
- **Do not add scope beyond the single duel.** No Ascension Meter, Impact Windows, Final
  Clash, second character, second arena, or multiplayer. See `../CLAUDE.md`.
- **No runtime LLM or generative-NPC behaviour** in the shipped game. The Vanguard is
  deterministic authored Blueprint logic.
- **Report planned changes before modifying project architecture.**

## Validation standard

`compile_blueprint(warnings_as_errors=true)` must come back clean after every Blueprint
change, then save through MCP. Functional verification is a human PIE pass — write test
instructions rather than assuming success. Agent-driven player input does not work here.
