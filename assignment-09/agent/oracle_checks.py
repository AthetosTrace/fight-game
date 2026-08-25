"""The oracle, executable.

Each checker consumes the snapshot stream and yields findings. The definitions
live in ORACLE.md and contracts/oracle.json; this module is the code that
enforces them, one function per invariant id so the two stay legible together.

Nothing here edits the game. A checker observes and reports.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Iterable

CONTRACT_PATH = os.path.join(os.path.dirname(__file__), "contracts", "oracle.json")

ERROR_TYPES = {
    "boundary": "boundary_break",
    "stuck": "stuck_state",
    "exploit": "exploit",
    "logic": "logic_violation",
}


@dataclass
class Finding:
    """One oracle violation, in the shape Assignment 09 asks for."""

    finding_id: str
    invariant_id: str
    location: str
    error_type: str
    game_context: str
    seed: int
    backend: str
    repro: str
    severity: str = "S2"
    classification: str = "DEFECT"
    invariant: str = ""
    evidence: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def load_contract(path: str = CONTRACT_PATH) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


class Oracle:
    """Runs every invariant over a run's snapshot stream."""

    def __init__(self, contract: dict, seed: int, backend: str) -> None:
        self.contract = contract
        self.seed = seed
        self.backend = backend
        self.params = contract["harness_parameters"]
        self.invariants = {inv["id"]: inv for inv in contract["invariants"]}
        self.findings: list[Finding] = []
        self._seen: set[tuple[str, str]] = set()
        self._counter = 0

        consts = contract["constants"]
        self.axis_min = consts["arena"]["combat_axis_min"]["value"]
        self.axis_max = consts["arena"]["combat_axis_max"]["value"]
        self.ground_z = consts["arena"]["ground_plane_z"]["value"]
        self.min_sep = consts["spacing"]["minimum_axis_separation"]["value"]
        self.contact = consts["spacing"]["capsule_contact_distance"]["value"]
        self.attack_range = consts["attack_driver"]["attack_range"]["value"]
        self.cooldown_max = consts["attack_driver"]["attack_cooldown_max"]["value"]
        self.retry_delay = consts["attack_driver"]["retry_delay"]["value"]
        self.damage = consts["attack_driver"]["attack_damage"]["value"]
        self.punch_damage = consts["player"]["punch_damage"]["value"]

        self.tol = self.params["position_tolerance_cm"]
        self.stuck_s = self.params["stuck_seconds"]

        # episode state
        self._crossing_open_t: float | None = None
        self._crossing_flips = 0
        self._idle_in_range_since: float | None = None
        self._locked_idle_since: float | None = None
        self._attack_episodes: list[dict] = []
        self._episode: dict | None = None
        self._breach: dict[str, float] = {}
        # Median interval actually achieved, set by the runner. Timing-based
        # checks (S3, L5) are suppressed when sampling is too coarse to resolve
        # a 1.1s windup or a 2.7s attack cycle - reporting those would be a
        # harness artefact, not a defect.
        self.sample_dt: float = 0.35

    # ---- emission ------------------------------------------------------

    def _emit(
        self,
        inv_id: str,
        location: str,
        context: str,
        repro: str,
        evidence: dict,
        dedupe: str | None = None,
    ) -> None:
        key = (inv_id, dedupe or "")
        if key in self._seen:
            return
        self._seen.add(key)
        inv = self.invariants.get(inv_id, {})
        self._counter += 1
        known = inv.get("known_limitation")
        self.findings.append(
            Finding(
                finding_id=f"F{self._counter:03d}",
                invariant_id=inv_id,
                location=location,
                error_type=ERROR_TYPES.get(inv.get("class", ""), "logic_violation"),
                game_context=context,
                seed=self.seed,
                backend=self.backend,
                repro=repro,
                severity=inv.get("severity", "S2"),
                classification="KNOWN" if known else "DEFECT",
                invariant=inv.get("statement", ""),
                evidence=evidence,
            )
        )

    # ---- the run -------------------------------------------------------

    def observe(self, prev, cur, action: str = "") -> None:
        """Feed one snapshot (with its predecessor) through every checker."""
        self._boundary(prev, cur)
        self._stuck(prev, cur)
        self._logic(prev, cur)
        self._exploit(prev, cur)
        self._episodes(prev, cur, action)

    # ---- B: boundary ---------------------------------------------------

    def _boundary(self, prev, cur) -> None:
        for who, x in (("player", cur.player_x), ("vanguard", cur.vanguard_x)):
            if x is None:
                continue
            if x > self.axis_max + self.tol or x < self.axis_min - self.tol:
                first = self._breach.setdefault(f"B1:{who}", cur.t)
                if cur.t - first >= self.stuck_s:
                    self._emit(
                        "B1",
                        "BP_VanguardDuelMover.ApplyConstraints",
                        f"{who} at x={x:.1f}, outside [{self.axis_min}, {self.axis_max}] "
                        f"for {cur.t - first:.1f}s; sep={cur.separation}",
                        f"seed={self.seed}; drive {who} toward the bound and hold",
                        {"actor": who, "x": x, "held_s": round(cur.t - first, 2)},
                        dedupe=who,
                    )
            else:
                self._breach.pop(f"B1:{who}", None)

        sep = cur.separation
        if sep is None:
            return
        if sep < self.contact - self.tol:
            self._emit(
                "B3",
                "BP_VanguardDuelMover.ApplyConstraints",
                f"capsule interpenetration: separation {sep:.1f} < contact {self.contact}; "
                f"crossing={cur.crossing_active}, side={cur.side_sign}",
                f"seed={self.seed}; close to contact range and press",
                {"separation": sep, "crossing": cur.crossing_active},
            )
        elif sep < self.min_sep - self.tol and not cur.crossing_active:
            first = self._breach.setdefault("B2", cur.t)
            if cur.t - first >= self.stuck_s:
                self._emit(
                    "B2",
                    "BP_VanguardDuelMover.ApplyConstraints",
                    f"separation {sep:.1f} below MinimumAxisSeparation {self.min_sep} "
                    f"for {cur.t - first:.1f}s while not crossing",
                    f"seed={self.seed}; walk into the Vanguard and hold",
                    {"separation": sep, "held_s": round(cur.t - first, 2)},
                )
        else:
            self._breach.pop("B2", None)

        # B5 - ordering must match the recorded side while not crossing
        if (
            not cur.crossing_active
            and cur.side_sign in (1, -1)
            and cur.player_x is not None
            and cur.vanguard_x is not None
            and abs(cur.vanguard_x - cur.player_x) > self.tol
        ):
            actual = 1 if cur.vanguard_x > cur.player_x else -1
            if actual != cur.side_sign:
                first = self._breach.setdefault("B5", cur.t)
                if cur.t - first >= self.stuck_s:
                    self._emit(
                        "B5",
                        "BP_VanguardDuelMover.UpdateSideOwnership",
                        f"ordering inverted: CurrentSideSign={cur.side_sign} but "
                        f"vanguard is {'right' if actual > 0 else 'left'} "
                        f"(player {cur.player_x:.1f}, vanguard {cur.vanguard_x:.1f})",
                        f"seed={self.seed}; jump over and land inside the deadzone",
                        {"side_sign": cur.side_sign, "actual": actual},
                    )
            else:
                self._breach.pop("B5", None)

    # ---- S: stuck ------------------------------------------------------

    def _stuck(self, prev, cur) -> None:
        # S2 - mover locked while the driver is idle
        if cur.movement_locked and cur.attack_state == 0:
            if self._locked_idle_since is None:
                self._locked_idle_since = cur.t
            elif cur.t - self._locked_idle_since >= self.stuck_s:
                self._emit(
                    "S2",
                    "BP_VanguardDuelMover.SetExternalMovementLocked",
                    f"mover locked with AttackState=idle for "
                    f"{cur.t - self._locked_idle_since:.1f}s - movement deadlock",
                    f"seed={self.seed}; interrupt a windup repeatedly",
                    {"held_s": round(cur.t - self._locked_idle_since, 2)},
                )
        else:
            self._locked_idle_since = None

        # S3 - in range, idle, past the cooldown ceiling, still not attacking
        sep = cur.separation
        in_range = sep is not None and sep <= self.attack_range
        alive = not (cur.player_ko or cur.vanguard_ko)
        losing = (
            prev is not None
            and prev.player_health is not None
            and cur.player_health is not None
            and cur.player_health < prev.player_health
        )
        if losing:
            # Damage proves the driver is cycling even if every sample caught
            # state 0. Coarse sampling hides a 2.7s attack cycle completely.
            self._idle_in_range_since = None
        elif in_range and alive and cur.attack_state == 0:
            if self._idle_in_range_since is None:
                self._idle_in_range_since = cur.t
            else:
                held = cur.t - self._idle_in_range_since
                ceiling = self.cooldown_max + 4 * self.retry_delay
                if held >= ceiling * 2 and self.sample_dt <= 1.0:
                    self._emit(
                        "S3",
                        "BP_VanguardBasicAttackDriver.TryStartAttack",
                        f"Vanguard idle {held:.1f}s at separation {sep:.1f} "
                        f"(<= AttackRange {self.attack_range}), well past cooldown "
                        f"ceiling {ceiling:.1f}s - the 16.4 stall regression",
                        f"seed={self.seed}; hold inside the hold band without attacking",
                        {"held_s": round(held, 2), "separation": sep},
                    )
        else:
            self._idle_in_range_since = None

        # S4 - ragdoll below the floor
        for who, z, ragdolled in (
            ("player", cur.player_z, cur.player_ragdolled),
            ("vanguard", cur.vanguard_z, cur.vanguard_ragdolled),
        ):
            if ragdolled and z is not None and z < self.ground_z - 50:
                self._emit(
                    "S4",
                    "BP_DuelKnockoutCoordinator.ApplyRagdoll",
                    f"{who} ragdoll settled at z={z:.1f}, below the floor plane "
                    f"{self.ground_z}",
                    f"seed={self.seed}; KO {who} near the arena bound",
                    {"actor": who, "z": z},
                    dedupe=who,
                )

    # ---- L: logic ------------------------------------------------------

    def _logic(self, prev, cur) -> None:
        ph, vh = cur.player_health, cur.vanguard_health
        pmax = cur.player_max_health or 100

        if ph is not None and (ph < 0 or ph > pmax):
            self._emit(
                "L1", "BP_ThirdPersonCharacter.HandleDamage",
                f"player health {ph} outside [0, {pmax}]",
                f"seed={self.seed}", {"health": ph},
            )
        if vh is not None and (vh < 0 or vh > 100):
            self._emit(
                "L1", "BP_VanguardProxy",
                f"vanguard health {vh} outside [0, 100]",
                f"seed={self.seed}", {"health": vh},
            )

        if cur.player_ko and cur.vanguard_ko:
            self._emit(
                "L2", "BP_DuelKnockoutCoordinator",
                f"both fighters KO'd at t={cur.t}s - nothing in the build resolves "
                f"a double knockout",
                f"seed={self.seed}; trade the killing blows in the same window",
                {"t": cur.t},
            )

        if prev is None:
            return

        # L6 - damage magnitude
        for who, before, after, expect, loc in (
            ("player", prev.player_health, ph, self.damage,
             "BP_VanguardBasicAttackDriver.PerformImpactCheck"),
            ("vanguard", prev.vanguard_health, vh, self.punch_damage,
             "BP_ThirdPersonCharacter attack chain"),
        ):
            if before is None or after is None or after >= before:
                continue
            step = before - after
            if abs(step - expect) > 0.01 and abs(step % expect) > 0.01:
                self._emit(
                    "L6", loc,
                    f"{who} health stepped {before} -> {after} ({step}), "
                    f"not the authored {expect}",
                    f"seed={self.seed}", {"before": before, "after": after, "step": step},
                    dedupe=f"{who}:{step}",
                )

        # L7 - a KO'd fighter recovering
        if prev.player_ko and cur.player_ko and ph and ph > 0:
            self._emit(
                "L7", "BP_DuelKnockoutCoordinator",
                f"player health recovered to {ph} after KO",
                f"seed={self.seed}", {"health": ph},
            )
        if prev.vanguard_ko and cur.vanguard_ko and vh and vh > 0:
            self._emit(
                "L7", "BP_DuelKnockoutCoordinator",
                f"vanguard health recovered to {vh} after KO",
                f"seed={self.seed}", {"health": vh},
            )

    # ---- X: exploits ---------------------------------------------------

    def _exploit(self, prev, cur) -> None:
        if prev is None:
            return

        # X1 - damage onto a KO'd fighter
        if prev.vanguard_ko and cur.vanguard_ko:
            if (prev.vanguard_health or 0) > (cur.vanguard_health or 0):
                self._emit(
                    "X1", "BP_DuelKnockoutCoordinator (capsule NoCollision)",
                    f"vanguard took damage after KO: "
                    f"{prev.vanguard_health} -> {cur.vanguard_health}",
                    f"seed={self.seed}; punch the corpse", {},
                )
        if prev.player_ko and cur.player_ko:
            if (prev.player_health or 0) > (cur.player_health or 0):
                self._emit(
                    "X1", "BP_DuelKnockoutCoordinator (capsule NoCollision)",
                    f"player took damage after KO: "
                    f"{prev.player_health} -> {cur.player_health}",
                    f"seed={self.seed}", {},
                )

        # X3 - crossing collision-ignore leaking past a knockout
        if (cur.player_ko or cur.vanguard_ko) and cur.crossing_active:
            self._emit(
                "X3", "BP_DuelKnockoutCoordinator.StopMover",
                f"bCrossingActive still true after KO "
                f"(playerKO={cur.player_ko}, vanguardKO={cur.vanguard_ko}) - "
                f"the mutual IgnoreActorWhenMoving never cleared",
                f"seed={self.seed}; KO a fighter during an active crossing",
                {"t": cur.t},
            )

        # X7 - constraints must survive a knockout.
        # StopMover disables the mover tick, and ApplyConstraints runs on it, so
        # bounds / min-separation / ordering all stop at once. Found empirically
        # on 2026-08-24 seed 7; B1, B3 and B5 catch the symptoms, this names the
        # shared cause.
        if cur.player_ko or cur.vanguard_ko:
            sep = cur.separation
            broke = []
            if cur.player_x is not None and not (
                self.axis_min - self.tol <= cur.player_x <= self.axis_max + self.tol
            ):
                broke.append(f"player x={cur.player_x:.1f} outside bounds")
            if sep is not None and sep < self.contact - self.tol:
                broke.append(f"separation {sep:.1f} < capsule contact {self.contact}")
            if broke:
                self._emit(
                    "X7",
                    "BP_DuelKnockoutCoordinator.StopMover -> "
                    "BP_VanguardDuelMover.ApplyConstraints",
                    f"after KO (player={cur.player_ko}, vanguard={cur.vanguard_ko}) "
                    f"position constraints are no longer enforced: {'; '.join(broke)}. "
                    f"crossing={cur.crossing_active}, side={cur.side_sign}",
                    f"seed={self.seed}; punch the Vanguard to the arena bound, KO it "
                    f"there, then keep walking forward into and past the body",
                    {"player_x": cur.player_x, "vanguard_x": cur.vanguard_x,
                     "separation": sep, "player_ko": cur.player_ko,
                     "vanguard_ko": cur.vanguard_ko},
                )

        # X5 - a KO'd player still dealing damage
        if cur.player_ko and (prev.vanguard_health or 0) > (cur.vanguard_health or 0):
            self._emit(
                "X5", "BP_DuelKnockoutCoordinator (bIsAttacking latch)",
                f"vanguard lost health while the player was KO'd: "
                f"{prev.vanguard_health} -> {cur.vanguard_health}",
                f"seed={self.seed}", {},
            )

    # ---- attack episodes: L3, L5, S1, X6 -------------------------------

    def _episodes(self, prev, cur, action: str) -> None:
        if prev is None:
            return

        # crossing episode -> S1, L3
        if cur.crossing_active and not prev.crossing_active:
            self._crossing_open_t = cur.t
            self._crossing_flips = 0
        if cur.crossing_active and prev.side_sign != cur.side_sign:
            self._crossing_flips += 1
        if cur.crossing_active and self._crossing_open_t is not None:
            if cur.t - self._crossing_open_t >= self.stuck_s and self.sample_dt <= 0.3:
                self._emit(
                    "S1", "BP_VanguardDuelMover.UpdateCrossingState",
                    f"crossing has stayed open {cur.t - self._crossing_open_t:.1f}s "
                    f"(airtime is 0.89-0.92s) - it never closed",
                    f"seed={self.seed}; jump over and land",
                    {"open_s": round(cur.t - self._crossing_open_t, 2)},
                )
        if prev.crossing_active and not cur.crossing_active:
            if self._crossing_flips != 1 and self.sample_dt <= 0.3:
                self._emit(
                    "L3", "BP_VanguardDuelMover.UpdateSideOwnership",
                    f"side sign flipped {self._crossing_flips} times during one "
                    f"crossing; exactly one is required",
                    f"seed={self.seed}; jump over and land inside the deadzone",
                    {"flips": self._crossing_flips},
                    dedupe=str(self._crossing_flips),
                )
            self._crossing_open_t = None

        # attack episode -> L5, X6
        if cur.attack_state == 1 and prev.attack_state in (0, 3):
            self._episode = {
                "start_t": cur.t,
                "damage_events": 0,
                "reached_strike": False,
                "player_punched": False,
                "vanguard_health_at_start": cur.vanguard_health,
            }
        if self._episode is not None:
            if cur.attack_state == 2:
                self._episode["reached_strike"] = True
            if action == "punch":
                self._episode["player_punched"] = True
            if (
                prev.player_health is not None
                and cur.player_health is not None
                and cur.player_health < prev.player_health
            ):
                self._episode["damage_events"] += 1
            ended = cur.attack_state in (0, 3) and prev.attack_state in (1, 2)
            if ended:
                ep = self._episode
                ep["end_t"] = cur.t
                ep["landed"] = ep["damage_events"] > 0
                self._attack_episodes.append(ep)
                if ep["damage_events"] > 1 and self.sample_dt <= 0.5:
                    self._emit(
                        "L5", "BP_VanguardBasicAttackDriver.PerformImpactCheck",
                        f"{ep['damage_events']} damage events in one strike - "
                        f"the bImpactDone guard did not hold",
                        f"seed={self.seed}", {"events": ep["damage_events"]},
                    )
                self._episode = None

    # ---- end-of-run analysis ------------------------------------------

    def finalize(self, punching: bool) -> None:
        """X6 - the cancel-lock ratio, judged over the whole run."""
        eps = self._attack_episodes
        if not punching or len(eps) < 4:
            return
        landed = sum(1 for e in eps if e.get("landed"))
        ratio = landed / len(eps)
        if ratio <= 0.05:
            self._emit(
                "X6", "BP_VanguardBasicAttackDriver (health-drop cancel, states 1 and 2)",
                f"under continuous player punching the Vanguard started {len(eps)} "
                f"attacks and landed {landed} ({ratio:.0%}). Each cancel rerolls the "
                f"full 2.5-4.0s cooldown while only 1.4s of windup is cancellable, so "
                f"a looping punch denies the attack indefinitely",
                f"seed={self.seed}; stand in range and punch on a loop for the run",
                {"attacks_started": len(eps), "attacks_landed": landed,
                 "land_ratio": round(ratio, 3)},
            )
