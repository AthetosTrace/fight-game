"""The adversarial QA agent - run entry point.

Restarts PIE, drives the in-editor behaviour loop, feeds every sample through
the oracle, and writes a structured report another developer can act on.

    py -3 agent.py --seed 7 --out ../evidence/runs/live-seed7

The agent is read-only over gameplay state. It injects input and samples
properties. It never edits an asset and never writes a design value.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time

from mcp_client import McpClient, McpError
from oracle_checks import Oracle, load_contract
from pie_backend import PieBackend, SAMPLE_FIELDS, Snapshot
from session_script import DEFAULT_PLAN, build_script

PROGRAMMATIC = "editor_toolset.toolsets.programmatic.ProgrammaticToolset"


def row_to_snapshot(row: dict) -> Snapshot:
    """Flatten one in-editor sample row into the oracle's Snapshot shape."""
    get = row.get
    return Snapshot(
        t=get("t", 0.0),
        player_health=get("player.currentHealth"),
        player_max_health=get("player.maxHealth"),
        vanguard_health=get("vanguard.health"),
        player_x=get("player.x"), player_y=get("player.y"), player_z=get("player.z"),
        vanguard_x=get("vanguard.x"), vanguard_y=get("vanguard.y"),
        vanguard_z=get("vanguard.z"),
        attack_state=get("driver.attackState"),
        state_timer=get("driver.stateTimer"),
        cooldown_remaining=get("driver.cooldownRemaining"),
        impact_done=get("driver.bImpactDone"),
        side_sign=get("mover.currentSideSign"),
        crossing_active=get("mover.bCrossingActive"),
        movement_locked=get("mover.bExternalMovementLocked"),
        movement_intent=get("mover.movementIntent"),
        is_attacking=get("player.bIsAttacking"),
        player_ko=get("knockout.bPlayerKO"),
        vanguard_ko=get("knockout.bVanguardKO"),
        player_ragdolled=get("knockout.bPlayerRagdolled"),
        vanguard_ragdolled=get("knockout.bVanguardRagdolled"),
    )


def run_session(seed: int, out_dir: str, dt: float, plan=None) -> dict:
    contract = load_contract()
    client = McpClient()
    backend = PieBackend(client)

    print("restarting PIE for a clean duel ...")
    backend.stop_pie()
    time.sleep(2.0)
    backend.start_pie(warmup=2.5)
    actors = backend.resolve()
    print(f"  resolved {len(actors)} duel actors")

    tuning = backend.tuning()

    script = build_script(
        actors={k: v for k, v in actors.items() if k in SAMPLE_FIELDS},
        fields=SAMPLE_FIELDS,
        plan=plan or DEFAULT_PLAN,
        dt=dt,
        seed=seed,
    )

    total = sum(p[1] for p in (plan or DEFAULT_PLAN))
    print(f"running the behaviour loop in-editor (~{total:.0f}s of duel) ...")
    started = time.time()
    client.timeout = total + 180
    raw = client.call_tool(
        "execute_tool_script", {"script": script}, toolset_name=PROGRAMMATIC
    )
    wall = time.time() - started

    payload = json.loads(raw)
    result = payload.get("returnValue", payload)
    if isinstance(result, str):
        result = json.loads(result)
    samples = result.get("samples", [])
    print(f"  {len(samples)} samples over {result.get('duration_s')}s "
          f"(wall {wall:.1f}s)")

    oracle = Oracle(contract, seed=seed, backend="pie")
    # The editor decides how fast it can actually service the sampling loop, and
    # it varies a lot between runs. Timing-based checks are only trustworthy when
    # the interval can resolve a 1.1s windup, so hand the oracle what we really
    # achieved rather than what we asked for.
    times = [row.get("t", 0.0) for row in samples]
    gaps = sorted(b - a for a, b in zip(times, times[1:])) or [dt]
    observed_dt = gaps[len(gaps) // 2]
    oracle.sample_dt = observed_dt
    print(f"  median sample interval {observed_dt:.2f}s (requested {dt:.2f}s)")

    prev = None
    punched = False
    for row in samples:
        snap = row_to_snapshot(row)
        action = row.get("action", "")
        if action == "punch":
            punched = True
        oracle.observe(prev, snap, action=action)
        prev = snap
    oracle.finalize(punching=punched)

    os.makedirs(out_dir, exist_ok=True)
    write_reports(out_dir, oracle, samples, result, tuning, seed, dt, plan,
                  observed_dt=observed_dt)
    return {"findings": oracle.findings, "samples": samples, "result": result}


def write_reports(out_dir, oracle, samples, result, tuning, seed, dt, plan,
                  observed_dt=None) -> None:
    observed_dt = dt if observed_dt is None else observed_dt
    findings = [f.to_dict() for f in oracle.findings]
    defects = [f for f in findings if f["classification"] == "DEFECT"]

    report = {
        "run": {
            "seed": seed,
            "backend": "pie",
            "level": "/Game/AscendantImpact/Maps/Lvl_DuelGraybox",
            "sample_count": len(samples),
            "duration_s": result.get("duration_s"),
            "sample_dt_requested_s": dt,
            "sample_dt_observed_s": round(observed_dt, 3),
            "plan": [list(p) for p in (plan or DEFAULT_PLAN)],
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        },
        "summary": {
            "findings_total": len(findings),
            "defects": len(defects),
            "known": len(findings) - len(defects),
            "by_severity": {
                sev: sum(1 for f in defects if f["severity"] == sev)
                for sev in ("S1", "S2", "S3")
            },
        },
        "live_tuning_verified": tuning,
        "findings": findings,
    }

    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    cols = ["finding_id", "invariant_id", "error_type", "severity",
            "classification", "location", "game_context", "repro", "seed",
            "backend"]
    with open(os.path.join(out_dir, "report.csv"), "w", encoding="utf-8",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for row in findings:
            writer.writerow(row)

    # The raw series - what makes a finding defensible if it is questioned.
    if samples:
        keys = sorted({k for row in samples for k in row})
        with open(os.path.join(out_dir, "samples.csv"), "w", encoding="utf-8",
                  newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(samples)

    print(f"\nwrote {out_dir}/report.json, report.csv, samples.csv")


def main() -> None:
    ap = argparse.ArgumentParser(description="Ascendant Impact adversarial QA agent")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--dt", type=float, default=0.35)
    ap.add_argument("--out", default="../evidence/runs/live")
    args = ap.parse_args()

    try:
        outcome = run_session(args.seed, args.out, args.dt)
    except McpError as exc:
        print(f"\nMCP error: {exc}")
        raise SystemExit(2)

    findings = outcome["findings"]
    defects = [f for f in findings if f.classification == "DEFECT"]
    print(f"\n{len(defects)} defect(s), {len(findings) - len(defects)} known")
    for f in findings:
        mark = "!" if f.classification == "DEFECT" else "-"
        print(f" {mark} [{f.invariant_id} {f.severity}] {f.location}")
        print(f"     {f.game_context}")


if __name__ == "__main__":
    main()
