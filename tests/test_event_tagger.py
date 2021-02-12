"""Test the event tagger."""

from meetup2apricot.event_tagger import (
    clean_tag_list,
    clean_codes_to_tags,
    make_event_tagger,
)
from .sample_apricot_json import EXPECTED_TAGS, EXPECTED_FREE_TAGS
import pytest

RAW_CODES_TO_TAGS = {
    "WW": "woodworking",
    "AC": ["arts-and-crafts", "the-studio"],
    "ZZ": None,
}

EXPECTED_CODES_TO_TAGS = {
    "AC": ["arts-and-crafts", "the-studio"],
    "WW": ["woodworking"],
    "ZZ": [],
}


def test_tag_code_none(event_tagger):
    """Test tagging a missing accounting code."""
    assert event_tagger.tag_code(None) == []


def test_tag_code_one(event_tagger):
    """Test tagging a code with one tag."""
    assert event_tagger.tag_code("AV") == ["audio-visual"]


def test_tag_code_multiple(event_tagger):
    """Test tagging a code with multiple tags."""
    assert event_tagger.tag_code("AC") == ["arts-and-crafts", "the-studio"]


def test_tag_code_unknown(event_tagger):
    """Test tagging an unknown accounting code."""
    assert event_tagger.tag_code("XY") == []


def test_tag_codes_none(event_tagger):
    """Test tagging an empty list of accounting codes."""
    assert event_tagger.tag_codes([]) == []


def test_tag_codes_one(event_tagger):
    """Test tagging a list of accounting codes with one code, which has one
    tag."""
    assert event_tagger.tag_codes(["AV"]) == ["AV", "audio-visual"]


def test_tag_codes_multiple(event_tagger):
    """Test tagging a list of accounting codes with one code, which has
    multiple tags."""
    assert event_tagger.tag_codes(["AC"]) == [
        "AC",
        "arts-and-crafts",
        "the-studio",
    ]


def test_tag_codes_multiple_multiple(event_tagger):
    """Test tagging a list of accounting codes, which have multiple tags, some
    in common."""
    assert event_tagger.tag_codes(["AC", "BIO"]) == [
        "AC_BIO",
        "arts-and-crafts",
        "the-studio",
        "biology",
        "the-studio",
    ]


def test_tag_event(event_tagger, free_meetup_event):
    """Test tagging an event."""
    assert event_tagger.tag_event(free_meetup_event) == EXPECTED_FREE_TAGS


def test_tag_event_featured(event_tagger, paid_meetup_event):
    """Test tagging an event."""
    expected_tags = ["featured"] + EXPECTED_TAGS + ["AV_P", "audio-visual"]
    assert event_tagger.tag_event(paid_meetup_event) == expected_tags


@pytest.mark.parametrize(
    "raw_tags, expected_tags",
    [
        ("woodworking", ["woodworking"]),
        (["arts-and-crafts", "the-studio"], ["arts-and-crafts", "the-studio"]),
        ([], []),
        ("", []),
        (None, []),
    ],
)
def test_clean_tag_list(raw_tags, expected_tags):
    """Test cleaning a list of tags."""
    assert clean_tag_list(raw_tags) == expected_tags


@pytest.mark.parametrize(
    "code, expected_tags",
    [("WW", ["woodworking"]), ("AC", ["arts-and-crafts", "the-studio"]), ("ZZ", [])],
)
def test_codes_to_tags(code, expected_tags):
    """Test cleaning a codes to tags mapping."""
    codes_to_tags = clean_codes_to_tags(RAW_CODES_TO_TAGS)
    assert codes_to_tags[code] == expected_tags


def test_make_event_tagger():
    """Test making an event tagger."""
    event_tagger = make_event_tagger(RAW_CODES_TO_TAGS, EXPECTED_TAGS)
    assert event_tagger.codes_to_tags == EXPECTED_CODES_TO_TAGS
    assert event_tagger.all_event_tags == EXPECTED_TAGS


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
