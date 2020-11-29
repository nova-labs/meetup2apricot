"""Tests event restriction loaders."""

from meetup2apricot.event_restriction_loader import (
    EventRestrictionLoader,
    EventRestriction,
)
from meetup2apricot.exceptions import InvalidRestrictionPattern
from meetup2apricot.member_level_manager import MemberLevel, MemberLevelManager
import re
import pytest


MEMBER_LEVEL_1 = MemberLevel(Id=111, Url="http://example.com/111")
MEMBER_LEVEL_2 = MemberLevel(Id=222, Url="http://example.com/222")
MEMBER_LEVEL_3 = MemberLevel(Id=333, Url="http://example.com/333")

ALL_LEVELS = [MEMBER_LEVEL_1, MEMBER_LEVEL_2, MEMBER_LEVEL_3]

SAMPLE_ALL_LEVELS_RESTRICTION_JSON = {
    "name": "Members Only",
    "pattern": "members[ -]*only",
}

SAMPLE_NAMED_LEVELS_RESTRICTION_JSON = {
    "name": "Key Members Only",
    "pattern": "key +members +only",
    "levels": ["Key", "Family"],
}

SAMPLE_ALL_LEVELS_RESTRICTION = EventRestriction(
    name="Members Only",
    pattern=re.compile("members[ -]*only", re.IGNORECASE),
    member_levels=ALL_LEVELS,
)

SAMPLE_NAMED_LEVELS_RESTRICTION = EventRestriction(
    name="Key Members Only",
    pattern=re.compile("key +members +only", re.IGNORECASE),
    member_levels=[MEMBER_LEVEL_1, MEMBER_LEVEL_3],
)


@pytest.fixture()
def member_level_manager():
    """Return a member level manager with most levels."""
    named_levels = {
        "Key": MEMBER_LEVEL_1,
        "Associate": MEMBER_LEVEL_2,
        "Family": MEMBER_LEVEL_3,
    }
    return MemberLevelManager(ALL_LEVELS, named_levels)


@pytest.fixture()
def event_restriction_loader(member_level_manager):
    """Return an event restriction loader."""
    return EventRestrictionLoader(member_level_manager)


def test_compile_pattern_valid():
    """Test compiling a valid regex pattern."""
    loader = EventRestrictionLoader(None)
    pattern = EventRestrictionLoader.compile_pattern("valid")
    assert pattern.search("valid")


def test_compile_pattern_invalid():
    """Test compiling an invalid regex pattern."""
    expected_message_pattern = r"Event restriction pattern '\[' is invalid: unterminated character set at position 0"
    with pytest.raises(InvalidRestrictionPattern, match=expected_message_pattern):
        pattern = EventRestrictionLoader.compile_pattern("[")


@pytest.mark.parametrize(
    "raw_level_list, expected_level_list",
    [
        ("attendee", ["attendee"]),
        (["key", "family"], ["key", "family"]),
        ([], []),
        ("", []),
        (None, []),
    ],
)
def test_clean_level_names(raw_level_list, expected_level_list):
    """Test cleaning a list of member level names."""
    assert (
        EventRestrictionLoader.clean_level_names(raw_level_list) == expected_level_list
    )


def test_lookup_member_levels_empty(event_restriction_loader):
    """Test looking up an empty list of member level names."""
    assert event_restriction_loader.lookup_member_levels([]) == ALL_LEVELS


def test_lookup_member_levels_list(event_restriction_loader):
    """Test looking up an empty list of member level names."""
    level_names = ["Family", "Key"]
    expected_levels = [MEMBER_LEVEL_3, MEMBER_LEVEL_1]
    assert event_restriction_loader.lookup_member_levels(level_names) == expected_levels


def test_load_restriction_all(event_restriction_loader):
    """Test loading a restriction that allows all member levels."""
    restriction = event_restriction_loader.load_restriction(
        SAMPLE_ALL_LEVELS_RESTRICTION_JSON
    )
    assert restriction == SAMPLE_ALL_LEVELS_RESTRICTION


def test_load_restriction_named(event_restriction_loader):
    """Test loading a restriction that namedows named member levels."""
    restriction = event_restriction_loader.load_restriction(
        SAMPLE_NAMED_LEVELS_RESTRICTION_JSON
    )
    assert restriction == SAMPLE_NAMED_LEVELS_RESTRICTION


def test_load(event_restriction_loader):
    """Test loading a list of restrictions."""
    restrictions = event_restriction_loader.load(
        [SAMPLE_NAMED_LEVELS_RESTRICTION_JSON, SAMPLE_ALL_LEVELS_RESTRICTION_JSON]
    )
    assert restrictions == [
        SAMPLE_NAMED_LEVELS_RESTRICTION,
        SAMPLE_ALL_LEVELS_RESTRICTION,
    ]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
