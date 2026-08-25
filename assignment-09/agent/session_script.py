"""Builds the in-editor sampling script.

The agent's behaviour loop runs INSIDE the editor through
ProgrammaticToolset.execute_tool_script. That matters for two reasons:

1. Sampling from outside costs ~7 MCP round trips per snapshot (~2.3s), which is
   far too coarse for a 1.1s windup or a 0.6-0.7s crossing window. Inside, the
   whole series is gathered in one call.
2. PIE advances in real time between MCP calls, so an outside loop spends most of
   its wall clock waiting rather than acting - and the Vanguard KOs an idle
   player in about 40 seconds.

The sandbox allows only {math, copy, json, datetime, time, re} plus
execute_tool(). No general Python.
"""

from __future__ import annotations

import json

# Phases the agent cycles through. Each entry is (name, seconds, action).
# Actions are what real input injection can actually reach: LMB fires IA_Attack
# via Slate Click on the editor window, SpaceBar reaches Enhanced Input.
DEFAULT_PLAN = [
    ("baseline_idle", 6.0, "none"),
    ("punch_loop", 22.0, "punch"),
    ("jump_cross", 10.0, "jump"),
    ("punch_loop", 16.0, "punch"),
    ("jump_punch_mix", 10.0, "mix"),
    ("idle_tail", 6.0, "none"),
]

SCRIPT_TEMPLATE = '''
import json, time

ACTORS = {actors}
FIELDS = {fields}
DYNAMIC = {dynamic}
PLAN = {plan}
DT = {dt}
WINDOW_REF = {window_ref!r}
SEED = {seed}

def _props(ref, names):
    out = execute_tool(
        "editor_toolset.toolsets.object.ObjectTools.get_properties",
        json.dumps({{"instance": {{"refPath": ref}}, "properties": names}}))
    val = out["returnValue"] if isinstance(out, dict) and "returnValue" in out else out
    if isinstance(val, str):
        try:
            val = json.loads(val)
        except Exception:
            return {{}}
    return val if isinstance(val, dict) else {{}}

def _loc(ref):
    got = _props(ref, ["rootComponent"])
    comp = got.get("rootComponent") or {{}}
    rp = comp.get("refPath") if isinstance(comp, dict) else None
    if not rp:
        return (None, None, None)
    got = _props(rp, ["relativeLocation"])
    loc = got.get("relativeLocation") or {{}}
    if not isinstance(loc, dict):
        return (None, None, None)
    return (loc.get("x"), loc.get("y"), loc.get("z"))

def _click():
    try:
        execute_tool("SlateInspectorToolset.SlateInspectorToolset.Click",
                     json.dumps({{"ref": WINDOW_REF, "button": "left"}}))
        return True
    except Exception:
        return False

def _key(k):
    try:
        execute_tool("SlateInspectorToolset.SlateInspectorToolset.PressKey",
                     json.dumps({{"key": k}}))
        return True
    except Exception:
        return False

def _root(ref):
    got = _props(ref, ["rootComponent"])
    comp = got.get("rootComponent") or {{}}
    return comp.get("refPath") if isinstance(comp, dict) else None

def run():
    t0 = time.time()
    ROOTS = {{}}
    for role in ("player", "vanguard"):
        if role in ACTORS:
            ROOTS[role] = _root(ACTORS[role])
    samples = []
    actions = []
    rng = SEED
    tick = 0

    for phase_name, phase_secs, action in PLAN:
        phase_end = time.time() + phase_secs
        while time.time() < phase_end:
            tick += 1
            rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF
            did = "none"
            if action == "punch":
                did = "punch" if _click() else "punch_failed"
            elif action == "jump":
                did = "jump" if _key("SpaceBar") else "jump_failed"
            elif action == "mix":
                if rng % 3 == 0:
                    did = "jump" if _key("SpaceBar") else "jump_failed"
                else:
                    did = "punch" if _click() else "punch_failed"

            row = {{"t": round(time.time() - t0, 3), "phase": phase_name,
                    "action": did, "tick": tick}}
            for role, ref in ACTORS.items():
                if role in DYNAMIC:
                    vals = _props(ref, DYNAMIC[role])
                    for k, v in vals.items():
                        row[role + "." + k] = v
            for role in ("player", "vanguard"):
                rp = ROOTS.get(role)
                if rp:
                    got = _props(rp, ["relativeLocation"])
                    loc = got.get("relativeLocation") or {{}}
                    if isinstance(loc, dict):
                        row[role + ".x"] = loc.get("x")
                        row[role + ".y"] = loc.get("y")
                        row[role + ".z"] = loc.get("z")
            samples.append(row)
            actions.append(did)

            slack = DT - (time.time() - t0 - (samples[-1]["t"]))
            if slack > 0:
                time.sleep(min(slack, DT))

    return {{"samples": samples, "ticks": tick,
             "duration_s": round(time.time() - t0, 2), "seed": SEED}}
'''


# Only these change during a duel. Everything else in SAMPLE_FIELDS is CDO
# tuning, read once by the runner and verified against ORACLE.md section 2.
DYNAMIC_FIELDS = {
    "player": ["currentHealth", "bIsAttacking"],
    "vanguard": ["health"],
    "mover": ["currentSideSign", "bCrossingActive", "bExternalMovementLocked",
              "movementIntent"],
    "driver": ["attackState", "stateTimer", "cooldownRemaining", "bImpactDone"],
    "knockout": ["bPlayerKO", "bVanguardKO", "bPlayerRagdolled",
                 "bVanguardRagdolled"],
}


def build_script(
    actors: dict[str, str],
    fields: dict[str, list[str]],
    plan: list[tuple[str, float, str]] | None = None,
    dt: float = 0.35,
    window_ref: str = "w1",
    seed: int = 1,
) -> str:
    """Render the in-editor behaviour loop."""
    return SCRIPT_TEMPLATE.format(
        actors=json.dumps(actors),
        fields=json.dumps(fields),
        dynamic=json.dumps(DYNAMIC_FIELDS),
        plan=json.dumps([list(p) for p in (plan or DEFAULT_PLAN)]),
        dt=dt,
        window_ref=window_ref,
        seed=seed,
    )
