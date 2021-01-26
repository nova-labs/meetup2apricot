"""Test Wild Apricot event registration types."""

from meetup2apricot.event_registration_type import EventRegistrationTypeMaker
from meetup2apricot.event_restriction_loader import EventRestriction
from meetup2apricot.member_level_manager import MemberLevel
import re
import pytest

MEMBER_LEVEL_1 = MemberLevel(Id=111, Url="http://example.com/111")
MEMBER_LEVEL_2 = MemberLevel(Id=222, Url="http://example.com/222")

ALL_LEVELS = [MEMBER_LEVEL_1, MEMBER_LEVEL_2]

SAMPLE_MEMBER_LEVELS_JSON = [
    {"Id": 111, "Url": "http://example.com/111"},
    {"Id": 222, "Url": "http://example.com/222"},
]

SAMPLE_ALL_LEVELS_RESTRICTION = EventRestriction(
    name="Members Only",
    pattern=re.compile("members[ -]*only", re.IGNORECASE),
    member_levels=ALL_LEVELS,
)

SAMPLE_NAMED_LEVELS_RESTRICTION = EventRestriction(
    name="Key Members Only",
    pattern=re.compile("key +members +only", re.IGNORECASE),
    member_levels=[MEMBER_LEVEL_2],
)

EXPECTED_APRICOT_JSON = {
    "Availability": "Everyone",
    "BasePrice": 78.9,
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "Description": "",
    "EventId": 12345,
    "GuestPrice": 78.9,
    "GuestRegistrationPolicy": "Disabled",
    "IsEnabled": True,
    "IsWaitlistEnabled": True,
    "MaximumRegistrantsCount": 6,
    "Name": "RSVP",
    "UnavailabilityPolicy": "ShowDisabled",
}

EXPECTED_MEETUP_JSON = {
    "Availability": "Everyone",
    "BasePrice": 0.0,
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "Description": "RSVPs on Meetup",
    "EventId": 12345,
    "GuestPrice": 0.0,
    "GuestRegistrationPolicy": "Disabled",
    "IsEnabled": False,
    "IsWaitlistEnabled": True,
    "MaximumRegistrantsCount": 6,
    "Name": "Instructor/Host",
    "UnavailabilityPolicy": "ShowDisabled",
}

EXPECTED_MEMBERS_ONLY_JSON = {
    "Availability": "MembersOnly",
    "AvailableForMembershipLevels": SAMPLE_MEMBER_LEVELS_JSON,
    "BasePrice": 78.9,
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "Description": "",
    "EventId": 12345,
    "GuestPrice": 78.9,
    "GuestRegistrationPolicy": "Disabled",
    "IsEnabled": True,
    "IsWaitlistEnabled": True,
    "MaximumRegistrantsCount": 6,
    "Name": "Members Only",
    "UnavailabilityPolicy": "ShowDisabled",
}


@pytest.fixture()
def event_registration_type_maker():
    """Return an event registration type maker."""
    restrictions = [SAMPLE_NAMED_LEVELS_RESTRICTION, SAMPLE_ALL_LEVELS_RESTRICTION]
    return EventRegistrationTypeMaker(restrictions)


def test_make_unrestricted_apricot_type_for_json(
    event_registration_type_maker,
):
    """Test converting an unrestricted Wild Apricot RSVP event registration
    type into dictionaries and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_unrestricted_apricot_type(
        12345, 6, 78.9
    )
    assert reg_type.for_json() == EXPECTED_APRICOT_JSON


def test_make_meetup_type_for_json(event_registration_type_maker):
    """Test converting a Meetup RSBP event registration type into dictionaries
    and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_meetup_type(12345, 6)
    assert reg_type.for_json() == EXPECTED_MEETUP_JSON


def test_make_restricted_apricot_type_for_json(event_registration_type_maker):
    """Test converting a restricted Wild Apricot event registration type into
    dictionaries and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_restricted_apricot_type(
        12345, 6, 78.9, SAMPLE_ALL_LEVELS_RESTRICTION
    )
    assert reg_type.for_json() == EXPECTED_MEMBERS_ONLY_JSON


def test_choose_event_restriction_no_match(event_registration_type_maker):
    """Test choosing an event restriction when no pattern matches the event title."""
    event_title = "Mending Monday"
    restriction = event_registration_type_maker.choose_event_restriction(event_title)
    assert restriction is None


def test_choose_event_restriction_first_match(event_registration_type_maker):
    """Test choosing an event restriction when no pattern matches the event title."""
    event_title = "Mending Monday (Members Only)"
    restriction = event_registration_type_maker.choose_event_restriction(event_title)
    assert restriction == SAMPLE_ALL_LEVELS_RESTRICTION


def test_make_apricot_type_unrestricted(event_registration_type_maker):
    """Test creating an unrerstricted Wild Apricot event registration type in
    dictionaries and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_apricot_type(
        12345, 6, 78.9, "Mending Monday"
    )
    assert reg_type.for_json() == EXPECTED_APRICOT_JSON


def test_make_apricot_type_restricted(event_registration_type_maker):
    """Test creating a rerstricted Wild Apricot event registration type in
    dictionaries and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_apricot_type(
        12345, 6, 78.9, "Mending Monday (Members Only)"
    )
    assert reg_type.for_json() == EXPECTED_MEMBERS_ONLY_JSON


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
