"""Test member level managers."""

from meetup2apricot.exceptions import UnknownMemberLevelName
from meetup2apricot.member_level_manager import (
    MemberLevel,
    MemberLevelManager,
    make_member_level_manager,
)
from .sample_apricot_json import SAMPLE_MEMBERSHIP_LEVEL_JSON
import pytest


MEMBER_LEVEL_1 = MemberLevel(Id=111, Url="http://example.com/111")
MEMBER_LEVEL_2 = MemberLevel(Id=222, Url="http://example.com/222")
MEMBER_LEVEL_3 = MemberLevel(Id=333, Url="http://example.com/333")
MEMBER_LEVEL_4 = MemberLevel(Id=444, Url="http://example.com/444")

ALL_LEVELS = [MEMBER_LEVEL_1, MEMBER_LEVEL_2, MEMBER_LEVEL_3, MEMBER_LEVEL_4]

SAMPLE_KEY_MEMBER = MemberLevel(
    Id=1206426,
    Url="https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206426",
)

EXPECTED_SAMPLE_LEVELS = [
    MemberLevel(
        Id=1206421,
        Url="https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206421",
    ),
    SAMPLE_KEY_MEMBER,
    MemberLevel(
        Id=1207614,
        Url="https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1207614",
    ),
]


@pytest.fixture()
def member_level_manager():
    """Return a member level manager with most levels."""
    named_levels = {
        "Key": MEMBER_LEVEL_1,
        "Associate": MEMBER_LEVEL_2,
        "Family": MEMBER_LEVEL_3,
    }
    return MemberLevelManager(named_levels)


def test_named_level(member_level_manager):
    """Test getting a named level."""
    assert member_level_manager.named_level("Associate") == MEMBER_LEVEL_2


def test_named_level_missing(member_level_manager):
    """Test getting a named level."""
    expected_message_pattern = "Unknown member level name 'Attendee'"
    with pytest.raises(UnknownMemberLevelName, match=expected_message_pattern):
        member_level_manager.named_level("Attendee")


def test_named_levels(member_level_manager):
    """Test getting a list of named levels."""
    assert member_level_manager.named_levels(["Associate", "Key"]) == [
        MEMBER_LEVEL_2,
        MEMBER_LEVEL_1,
    ]


def test_add_level(member_level_manager):
    """Test adding a level."""
    member_level_manager.add_level("Attendee", MEMBER_LEVEL_4)
    assert member_level_manager.named_level("Attendee") == MEMBER_LEVEL_4


def test_make_member_level_manager():
    """Test making a member level manager."""
    manager = make_member_level_manager(SAMPLE_MEMBERSHIP_LEVEL_JSON)
    assert manager.named_level("Key") == SAMPLE_KEY_MEMBER


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
