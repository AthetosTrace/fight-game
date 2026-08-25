"""Live PIE backend - reads duel state out of a running editor over Unreal MCP.

READ-ONLY over gameplay state. The agent samples properties and injects real
input; it never edits an asset and never writes a design value. See ORACLE.md
section 5.

Property names below were discovered with ObjectTools.list_properties against a
live PIE session on 2026-08-24, not guessed. game/CLAUDE.md is emphatic that
guessed names fail silently, so every name here came off the wire.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any

from mcp_client import McpClient, McpError

SCENE = "editor_toolset.toolsets.scene.SceneTools"
OBJECT = "editor_toolset.toolsets.object.ObjectTools"
APP = "EditorToolset.EditorAppToolset"
SLATE = "SlateInspectorToolset.SlateInspectorToolset"

DUEL_LEVEL = "/Game/AscendantImpact/Maps/Lvl_DuelGraybox"

# Actor refPath fragments -> role. Matched against the PIE world.
ACTOR_KEYS = {
    "player": "BP_ThirdPersonCharacter_C_0",
    "vanguard": "BP_VanguardProxy",
    "mover": "BP_VanguardDuelMover",
    "driver": "BP_VanguardBasicAttackDriver",
    "knockout": "BP_DuelKnockoutCoordinator",
    "camera": "BP_DuelCameraRig",
    "controller": "BP_ThirdPersonPlayerController",
}

# Scalars sampled every tick, per actor role.
SAMPLE_FIELDS = {
    "player": ["currentHealth", "maxHealth", "bIsAttacking", "bDuelModeActive"],
    "vanguard": ["health"],
    "mover": [
        "combatAxisMin", "combatAxisMax", "minimumAxisSeparation",
        "preferredDistance", "rangeDeadZone", "retreatSpeedScale",
        "currentSideSign", "sideDeadzone", "crossingMinRelativeHeight",
        "bCrossingActive", "bExternalMovementLocked", "movementIntent",
        "depthLaneCenter", "depthLaneHalfWidth", "currentDepthTarget",
        "bMoverActivated",
    ],
    "driver": [
        "attackState", "stateTimer", "cooldownRemaining", "bImpactDone",
        "attackRange", "windupDuration", "strikeImpactDelay", "strikeDuration",
        "recoveryDuration", "attackCooldownMin", "attackCooldownMax",
        "attackDecisionChance", "retryDelay", "attackDamage",
        "impactForwardOffset", "impactRadius", "impactDepthTolerance",
        "windupStartVanguardHealth", "bDriverActivated",
    ],
    "knockout": [
        "bPlayerKO", "bVanguardKO", "bPlayerRagdolled", "bVanguardRagdolled",
        "playerKOTimer", "vanguardKOTimer", "impactToRagdollDelay",
    ],
}

# Attack driver state machine (blackboard 16.2).
ATTACK_STATES = {0: "idle", 1: "windup", 2: "strike", 3: "recovery"}


@dataclass
class Snapshot:
    """One sample of duel state. Everything the oracle needs, in one object."""

    t: float
    player_health: float | None = None
    player_max_health: float | None = None
    vanguard_health: float | None = None
    player_x: float | None = None
    player_y: float | None = None
    player_z: float | None = None
    vanguard_x: float | None = None
    vanguard_y: float | None = None
    vanguard_z: float | None = None
    player_falling: bool | None = None
    attack_state: int | None = None
    state_timer: float | None = None
    cooldown_remaining: float | None = None
    impact_done: bool | None = None
    side_sign: int | None = None
    crossing_active: bool | None = None
    movement_locked: bool | None = None
    movement_intent: int | None = None
    is_attacking: bool | None = None
    player_ko: bool | None = None
    vanguard_ko: bool | None = None
    player_ragdolled: bool | None = None
    vanguard_ragdolled: bool | None = None
    raw: dict = field(default_factory=dict)

    @property
    def separation(self) -> float | None:
        if self.player_x is None or self.vanguard_x is None:
            return None
        return abs(self.vanguard_x - self.player_x)

    @property
    def attack_state_name(self) -> str:
        return ATTACK_STATES.get(self.attack_state, f"unknown({self.attack_state})")

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("raw", None)
        d["separation"] = self.separation
        d["attack_state_name"] = self.attack_state_name
        return d


class PieBackend:
    """Drives and observes one PIE session."""

    name = "pie"

    def __init__(self, client: McpClient | None = None) -> None:
        self.mcp = client or McpClient()
        self.mcp.connect()
        self.actors: dict[str, str] = {}
        self._roots: dict[str, str] = {}
        self._viewport_ref: str | None = None
        self._t0 = time.time()

    # ---- raw helpers ---------------------------------------------------

    def _tool(self, name: str, args: dict | None = None, toolset: str = SCENE) -> Any:
        raw = self.mcp.call_tool(name, args or {}, toolset_name=toolset)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        value = parsed.get("returnValue", parsed) if isinstance(parsed, dict) else parsed
        # Several ObjectTools verbs double-encode their payload.
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return value

    def is_pie_running(self) -> bool:
        return bool(self._tool("IsPIERunning", {}, APP))

    def start_pie(self, warmup: float = 3.0) -> None:
        if not self.is_pie_running():
            self._tool("StartPIE", {}, APP)
            time.sleep(warmup)
        self._t0 = time.time()

    def stop_pie(self) -> None:
        if self.is_pie_running():
            self._tool("StopPIE", {}, APP)

    def current_level(self) -> str:
        return str(self._tool("get_current_level", {}, SCENE))

    # ---- actor resolution ----------------------------------------------

    def resolve(self) -> dict[str, str]:
        """Map each duel role to its PIE-world refPath."""
        found = self._tool("find_actors", {}, SCENE) or []
        paths = [a.get("refPath", "") for a in found if isinstance(a, dict)]
        pie_paths = [p for p in paths if "UEDPIE" in p] or paths

        self.actors = {}
        for role, fragment in ACTOR_KEYS.items():
            for path in pie_paths:
                if fragment in path:
                    self.actors[role] = path
                    break
        missing = set(ACTOR_KEYS) - set(self.actors)
        if {"player", "vanguard", "mover", "driver"} & missing:
            raise McpError(
                f"duel actors missing from the PIE world: {sorted(missing)}. "
                f"Is {DUEL_LEVEL} loaded and PIE running?"
            )
        return self.actors

    def _get(self, role: str, fields: list[str]) -> dict:
        path = self.actors.get(role)
        if not path or not fields:
            return {}
        try:
            return self._tool(
                "get_properties",
                {"instance": {"refPath": path}, "properties": fields},
                OBJECT,
            ) or {}
        except McpError:
            return {}

    def _location(self, role: str) -> tuple[float | None, float | None, float | None]:
        """World location via the actor's root component."""
        root = self._roots.get(role)
        if root is None:
            got = self._get(role, ["rootComponent"])
            comp = got.get("rootComponent") if isinstance(got, dict) else None
            root = comp.get("refPath") if isinstance(comp, dict) else ""
            self._roots[role] = root
        if not root:
            return (None, None, None)
        got = self._tool(
            "get_properties",
            {"instance": {"refPath": root}, "properties": ["relativeLocation"]},
            OBJECT,
        )
        loc = got.get("relativeLocation") if isinstance(got, dict) else None
        if not isinstance(loc, dict):
            return (None, None, None)
        return (loc.get("x"), loc.get("y"), loc.get("z"))

    def _is_falling(self) -> bool | None:
        got = self._get("player", ["characterMovement"])
        comp = got.get("characterMovement") if isinstance(got, dict) else None
        ref = comp.get("refPath") if isinstance(comp, dict) else None
        if not ref:
            return None
        got = self._tool(
            "get_properties",
            {"instance": {"refPath": ref}, "properties": ["movementMode"]},
            OBJECT,
        )
        mode = got.get("movementMode") if isinstance(got, dict) else None
        if mode is None:
            return None
        return str(mode).lower().endswith("falling") or mode == 3

    # ---- sampling ------------------------------------------------------

    def snapshot(self) -> Snapshot:
        if not self.actors:
            self.resolve()

        player = self._get("player", SAMPLE_FIELDS["player"])
        vanguard = self._get("vanguard", SAMPLE_FIELDS["vanguard"])
        mover = self._get("mover", SAMPLE_FIELDS["mover"])
        driver = self._get("driver", SAMPLE_FIELDS["driver"])
        ko = self._get("knockout", SAMPLE_FIELDS["knockout"])

        px, py, pz = self._location("player")
        vx, vy, vz = self._location("vanguard")

        return Snapshot(
            t=round(time.time() - self._t0, 3),
            player_health=player.get("currentHealth"),
            player_max_health=player.get("maxHealth"),
            vanguard_health=vanguard.get("health"),
            player_x=px, player_y=py, player_z=pz,
            vanguard_x=vx, vanguard_y=vy, vanguard_z=vz,
            player_falling=None,
            attack_state=driver.get("attackState"),
            state_timer=driver.get("stateTimer"),
            cooldown_remaining=driver.get("cooldownRemaining"),
            impact_done=driver.get("bImpactDone"),
            side_sign=mover.get("currentSideSign"),
            crossing_active=mover.get("bCrossingActive"),
            movement_locked=mover.get("bExternalMovementLocked"),
            movement_intent=mover.get("movementIntent"),
            is_attacking=player.get("bIsAttacking"),
            player_ko=ko.get("bPlayerKO"),
            vanguard_ko=ko.get("bVanguardKO"),
            player_ragdolled=ko.get("bPlayerRagdolled"),
            vanguard_ragdolled=ko.get("bVanguardRagdolled"),
            raw={"player": player, "vanguard": vanguard, "mover": mover,
                 "driver": driver, "knockout": ko},
        )

    def tuning(self) -> dict:
        """The live CDO values, for checking the build against ORACLE.md section 2."""
        if not self.actors:
            self.resolve()
        return {
            "mover": self._get("mover", SAMPLE_FIELDS["mover"]),
            "driver": self._get("driver", SAMPLE_FIELDS["driver"]),
            "knockout": self._get("knockout", SAMPLE_FIELDS["knockout"]),
            "player": self._get("player", SAMPLE_FIELDS["player"]),
        }

    # ---- input injection -----------------------------------------------

    def viewport_ref(self) -> str | None:
        """Slate ref for the PIE viewport, so clicks land as game input."""
        if self._viewport_ref:
            return self._viewport_ref
        snap = self.mcp.call_tool("Snapshot", {"ref": ""}, toolset_name=SLATE)
        for line in snap.splitlines():
            if "Viewport" in line and "ref=" in line:
                start = line.find("ref=") + 4
                end = line.find(" ", start)
                self._viewport_ref = line[start:end if end > start else None].strip("\"'")
                break
        return self._viewport_ref

    def punch(self) -> bool:
        """Real LMB into the PIE viewport - fires IA_Attack."""
        ref = self.viewport_ref()
        if not ref:
            return False
        self.mcp.call_tool("Click", {"ref": ref, "button": "left"}, toolset_name=SLATE)
        return True

    def press(self, key: str) -> bool:
        """Real key into Enhanced Input. Needs viewport keyboard focus."""
        self.mcp.call_tool("PressKey", {"key": key}, toolset_name=SLATE)
        return True

    def jump(self) -> bool:
        return self.press("SpaceBar")
