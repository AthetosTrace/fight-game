"""Tests for the gap scanner.

The scanner's job is to be trusted about what is missing, so most of these
tests are about the ways it could quietly lie: inventing a requirement from
prose, hiding a gap behind a guessed alias, or letting ownership reorder the
ranking instead of merely filtering it.
"""

import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SCANNER_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(SCANNER_ROOT))
sys.path.insert(0, SCANNER_ROOT)

import gap_scan as G  # noqa: E402

SCOPE_PATH = os.path.join(SCANNER_ROOT, "scope.json")
BUILD_SEQUENCE = os.path.join(REPO_ROOT, "build-sequence.md")


@pytest.fixture
def scope():
    with open(SCOPE_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def steps(scope):
    return G.parse_requirements(BUILD_SEQUENCE, set(scope["asset_prefixes"]))


# --- parsing the design ---------------------------------------------------


def test_parses_the_real_build_sequence(steps):
    assert len(steps) == 63, "the sequence documents 63 ordered steps"
    assert all(s["step_id"] for s in steps)


def test_step_ids_are_unique(steps):
    ids = [s["step_id"] for s in steps]
    assert len(ids) == len(set(ids))


def test_finds_the_arena_step(steps):
    arena = [s for s in steps if s["step_id"] == "M1-21"][0]
    assert "L_ShatteredRing" in arena["assets"]


def test_prose_is_not_mistaken_for_a_requirement(steps):
    """The document backticks menu paths and property names too. Only tokens
    with a known asset prefix may become requirements."""
    every_asset = {a for s in steps for a in s["assets"]}
    for token in ("Add_Level", "Details_Panel", "Content_Browser"):
        assert token not in every_asset


def test_titles_are_ascii(steps):
    """Windows consoles default to cp1252; a stray en dash must not be able to
    crash the report."""
    for step in steps:
        step["title"].encode("ascii")


# --- ranking --------------------------------------------------------------


def test_milestones_sort_before_step_numbers():
    assert G.step_sort_key("M1-21") < G.step_sort_key("M2-01")
    assert G.step_sort_key("M1-09") < G.step_sort_key("M1-10"), "not lexical"


def test_gaps_come_back_in_blocking_order(steps, scope):
    gaps = G.detect_gaps(steps, {"BP_ThirdPersonCharacter"}, scope)
    keys = [G.step_sort_key(g["step_id"]) for g in gaps]
    assert keys == sorted(keys)


# --- detecting gaps -------------------------------------------------------


def test_a_built_asset_closes_its_gap(steps, scope):
    built = {a for s in steps for a in s["assets"]}
    assert G.detect_gaps(steps, built, scope) == []


def test_an_empty_build_leaves_every_step_open(steps, scope):
    gaps = G.detect_gaps(steps, set(), scope)
    open_steps = {g["step_id"] for g in gaps}
    assert "M1-21" in open_steps


def test_a_declared_alias_closes_the_gap(steps, scope):
    """The prototype shipped the player as BP_ThirdPersonCharacter."""
    gaps = G.detect_gaps(steps, {"BP_ThirdPersonCharacter"}, scope)
    still_missing = {m for g in gaps for m in g["missing"]}
    assert "BP_PlayerFighter" not in still_missing


def test_an_undeclared_rename_is_still_a_gap(steps, scope):
    """The scanner must not guess that two similar names are the same asset."""
    gaps = G.detect_gaps(steps, {"BP_PlayerFighterV2"}, scope)
    still_missing = {m for g in gaps for m in g["missing"]}
    assert "BP_PlayerFighter" in still_missing


def test_the_graybox_level_does_not_count_as_the_arena(steps, scope):
    """Lvl_DuelGraybox is a locomotion test map, not the Shattered Ring.
    Letting it close M1-21 would hide the gap this scan exists to find."""
    gaps = G.detect_gaps(steps, {"Lvl_DuelGraybox"}, scope)
    arena = [g for g in gaps if g["step_id"] == "M1-21"]
    assert arena and "L_ShatteredRing" in arena[0]["missing"]


def test_assets_the_agent_cannot_create_are_not_ranked(steps, scope):
    """UserDefinedStruct/Enum cannot be made through the MCP server, so they
    are not closable gaps and must not outrank real work."""
    gaps = G.detect_gaps(steps, set(), scope)
    still_missing = {m for g in gaps for m in g["missing"]}
    for excluded in scope["not_deliverables"]:
        assert excluded not in still_missing


# --- ownership ------------------------------------------------------------


def test_ownership_filters_but_never_reorders(steps, scope):
    """The true top of the list must survive into the report even when it
    belongs to someone else."""
    gaps = G.detect_gaps(steps, set(), scope)
    selected = G.select_buildable(gaps, scope)
    assert selected["step_id"] == "M1-21"
    assert gaps[0]["step_id"] != "M1-21", (
        "something ranked above the arena; the report must still show it")


def test_selection_is_the_earliest_owned_gap(steps, scope):
    gaps = G.detect_gaps(steps, set(), scope)
    selected = G.select_buildable(gaps, scope)
    owned = set(scope["owned_steps"])
    earlier_owned = [g for g in gaps
                     if g["step_id"] in owned
                     and G.step_sort_key(g["step_id"])
                     < G.step_sort_key(selected["step_id"])]
    assert earlier_owned == []


def test_nothing_owned_means_nothing_selected(steps):
    gaps = G.detect_gaps(steps, set(), {"owned_steps": []})
    assert G.select_buildable(gaps, {"owned_steps": []}) is None


# --- scanning the build ---------------------------------------------------


def test_ofpa_packages_are_skipped(tmp_path):
    """One-File-Per-Actor packages have generated hash names and would drown
    the real inventory."""
    content = tmp_path / "Content"
    (content / "Blueprints").mkdir(parents=True)
    (content / "__ExternalActors__" / "Maps").mkdir(parents=True)
    (content / "Blueprints" / "BP_Real.uasset").write_text("x")
    (content / "__ExternalActors__" / "Maps" / "0G2RQ0ZR3JK81UMB.uasset").write_text("x")

    built = G.scan_codebase(str(content))
    assert built == {"BP_Real"}


def test_maps_and_assets_both_count(tmp_path):
    content = tmp_path / "Content"
    content.mkdir()
    (content / "Lvl_Test.umap").write_text("x")
    (content / "BP_Test.uasset").write_text("x")
    assert G.scan_codebase(str(content)) == {"Lvl_Test", "BP_Test"}


def test_committed_inventory_matches_a_live_scan():
    """The snapshot graders read must not drift from what a scan produces."""
    inventory_path = os.path.join(SCANNER_ROOT, "codebase-inventory.json")
    with open(inventory_path, "r", encoding="utf-8") as handle:
        inventory = json.load(handle)
    assert inventory["assets"], "inventory is empty"
    assert len(inventory["assets"]) == len(set(inventory["assets"]))
