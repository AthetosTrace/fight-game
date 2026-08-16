"""retrieval -- the citations have to be real, or the style guide is decorative.

The test that matters here is `test_every_citation_verifies`. A style rule
asserts what the GDD says, and the cheapest way for that to be wrong is for
nobody to check. This suite checks.
"""

import os

import retrieval


def test_every_citation_verifies(rules_doc):
    """Every rule and slot citing a GDD section must quote it verbatim.

    This failed on the first run of the build: six slot citations and eight
    rules quoted wording that was close but not what the PDF extraction
    actually contains. The rules were right; the quotes were paraphrased.
    """
    failures = [record for record in retrieval.verify_all(rules_doc)
                if not record["verified"]]
    assert not failures, "unverified citations: %s" % [
        (f["source"], f["quoted"]) for f in failures]


def test_every_citation_names_a_section_and_page(rules_doc):
    for record in retrieval.verify_all(rules_doc):
        assert record["section"] is not None, record["source"]
        assert record["page"] is not None, record["source"]


def test_no_rule_cites_the_prototype_blackboard(rules_doc):
    """Assignment 06 asserted this and it holds here for the same reason:
    PROTOTYPE_BLACKBOARD.md records measured implementation, not design. A
    style rule sourced from it would encode what the build happens to do
    rather than what the designer decided."""
    blob = str(rules_doc).lower()
    assert "prototype_blackboard" not in blob


def test_excerpt_lands_on_the_authored_line(rules_doc):
    """The excerpt must contain the quote, not merely sit near it."""
    for record in retrieval.verify_all(rules_doc):
        assert record["excerpt"], record["source"]
        flattened = retrieval._normalise(record["excerpt"])
        assert any(retrieval._normalise(q) in flattened for q in record["quoted"]), \
            "%s excerpt does not contain its own quote" % record["source"]


def test_citations_resolve_to_files_under_gdd_sections(rules_doc):
    for record in retrieval.verify_all(rules_doc):
        assert record["found_in"].startswith("gdd/sections/"), record["source"]


def test_unknown_section_does_not_verify():
    record = retrieval.verify_citation("section 99, page 1 - 'nothing here'")
    assert record["verified"] is False


def test_citation_without_a_quote_does_not_verify():
    """A citation with nothing quoted cannot be checked, so it must not claim
    to have been."""
    record = retrieval.verify_citation("section 03, page 3 - no quoted wording")
    assert record["verified"] is False


def test_section_file_lookup_is_zero_padded():
    path = retrieval.section_file(3)
    assert path is not None
    assert os.path.basename(path).startswith("03-")


def test_applicable_rules_respects_slot_scoping(rules_doc):
    """L3 is scoped to the Final Clash slot and must not govern the others."""
    assert "L3" in retrieval.applicable_rules(rules_doc, "final_clash_unlock")
    assert "L3" not in retrieval.applicable_rules(rules_doc, "loss_screen")


def test_for_slot_reports_the_moment_and_every_rule(rules_doc, slots):
    for slot in slots:
        record = retrieval.for_slot(rules_doc, slot)
        assert record["moment"]
        assert record["slot_citation"]["verified"]
        assert record["rules_in_force"]
        assert len(record["rule_citations"]) == len(record["rules_in_force"])


def test_normalise_folds_the_pdf_punctuation():
    """The extraction carries curly quotes and en-dashes; a citation written
    with plain ASCII must still match."""
    assert retrieval._normalise("don’t — stop") == retrieval._normalise("don't - stop")
