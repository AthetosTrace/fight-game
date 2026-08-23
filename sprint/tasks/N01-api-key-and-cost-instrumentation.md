---
id: N01
track: N
title: API key, and the shared cost-instrumentation helper
status: todo
assignment: 08
editor-required: false
depends-on: []
---

## Goal

A working Anthropic API key on this machine, and a small helper that records token usage
and cost on every call from the first call onward.

## Why it matters

Two things depend on this and neither has a workaround:

- **A08** requires agent code "written in Python using the Claude API."
- **A10** requires a total actual run cost "calculated from the actual content generation
  run, not a hypothesis," plus a before/after token comparison.

There is **no key on this machine** — not in the process environment, not User scope, not
Machine scope. Assignment 07 dodged this with a session-replay backend; A08 and A10 cannot.

## Preconditions

- Adrian or Omar creates a key at `console.anthropic.com`. Roughly $5 of credit covers
  everything this sprint needs.

## Steps

1. Set `ANTHROPIC_API_KEY` at User scope so it survives a reboot and is visible to every
   window. Do **not** commit it, and do not paste it into any file in the repo.
2. Confirm `.gitignore` covers whatever local env file is used.
3. Write the usage helper — small, one job: wrap a Messages API call, and append
   `{timestamp, model, step, input_tokens, output_tokens, cost_usd}` to a run JSON.
   Take pricing from the model's published rates and record which rates were used, so the
   figure can be re-derived later.
4. Smoke-test it with one trivial call. Confirm a run JSON appears with real numbers.
5. Put it somewhere both `N02` and any A10 generation run can import.

## Done when

- [ ] `ANTHROPIC_API_KEY` is set at User scope and a real API call succeeds.
- [ ] The helper writes a run JSON with per-call token counts and a cost figure.
- [ ] The pricing rates used are recorded alongside the numbers.
- [ ] No key material anywhere in the repo — checked, not assumed.

## Log

- 2026-08-23 — created. Confirmed absent at all three scopes on 2026-08-23.
