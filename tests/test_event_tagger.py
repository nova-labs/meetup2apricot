"""Test the event tagger."""

from meetup2apricot.event_tagger import (
    EventTagger,
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


def test_tag_code_none(event_tagger):
    """Test tagging a missing accounting code."""
    assert event_tagger.tag_code(None) == EXPECTED_TAGS


def test_tag_code_one(event_tagger):
    """Test tagging a code with one tag."""
    assert event_tagger.tag_code("AV") == ["audio-visual"] + EXPECTED_TAGS


def test_tag_code_multiple(event_tagger):
    """Test tagging a code with multiple tags."""
    assert (
        event_tagger.tag_code("AC") == ["arts-and-crafts", "the-studio"] + EXPECTED_TAGS
    )


def test_tag_code_unknown(event_tagger):
    """Test tagging an unknown accounting code."""
    assert event_tagger.tag_code("XY") == EXPECTED_TAGS


def test_tag_event(event_tagger, free_meetup_event):
    """Test tagging an event."""
    assert event_tagger.tag_event(free_meetup_event) == EXPECTED_FREE_TAGS


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
    codes_to_tags = clean_codes_to_tags(RAW_CODES_TO_TAGS)
    assert clean_tag_list(raw_tags) == expected_tags


@pytest.mark.parametrize(
    "code, expected_tags",
    [("WW", ["woodworking"]), ("AC", ["arts-and-crafts", "the-studio"]), ("ZZ", [])],
)
def test_codes_to_tags(code, expected_tags):
    """Test cleaning a codes to tags mapping."""
    codes_to_tags = clean_codes_to_tags(RAW_CODES_TO_TAGS)
    assert codes_to_tags[code] == expected_tags


@pytest.mark.parametrize(
    "code, expected_tags",
    [
        ("WW", ["woodworking"] + EXPECTED_TAGS),
        ("AC", ["arts-and-crafts", "the-studio"] + EXPECTED_TAGS),
        ("ZZ", EXPECTED_TAGS),
    ],
)
def test_make_event_tagger(code, expected_tags):
    """Test making an event tagger."""
    event_tagger = make_event_tagger(RAW_CODES_TO_TAGS, EXPECTED_TAGS)
    assert event_tagger.tag_code(code) == expected_tags


@pytest.mark.parametrize(
    "code, expected_tags",
    [
        ("WW", ["woodworking", "foo"]),
        ("AC", ["arts-and-crafts", "the-studio", "foo"]),
        ("ZZ", ["foo"]),
    ],
)
def test_make_event_tagger_short_list(code, expected_tags):
    """Test making an event tagger with a single tag for all events."""
    event_tagger = make_event_tagger(RAW_CODES_TO_TAGS, "foo")
    assert event_tagger.tag_code(code) == expected_tags


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
