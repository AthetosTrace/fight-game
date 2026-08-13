import json
import os
import sys

import pytest

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPELINE_DIR)

RULES_PATH = os.path.join(PIPELINE_DIR, "contracts", "attack_rules.json")


@pytest.fixture(scope="session")
def rules_doc():
    with open(RULES_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def row_a(rules_doc):
    import generator
    return generator.base_row(rules_doc, "A")


@pytest.fixture
def row_d(rules_doc):
    import generator
    return generator.base_row(rules_doc, "D")
