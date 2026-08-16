"""Shared fixtures. The pipeline is a flat package reached by path, matching
Assignment 06's layout so both suites run the same way from the repo root."""

import json
import os
import sys

import pytest

PIPELINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

RULES_PATH = os.path.join(PIPELINE, "contracts", "style_rules.json")


@pytest.fixture(scope="session")
def rules_doc():
    with open(RULES_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="session")
def slots(rules_doc):
    return sorted(rules_doc["slots"])


@pytest.fixture
def rubric_judge():
    import judge
    return judge.get_judge("rubric")


def line(slot, text):
    return {"slot": slot, "text": text}
