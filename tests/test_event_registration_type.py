"""Test Wild Apricot event registration types."""

from meetup2apricot.event_registration_type import EventRegistrationTypeMaker
import pytest

SAMPLE_MEMBER_LEVELS = [
    {"Id": 222, "Url": "http://example.com/222"},
    {"Id": 333, "Url": "http://example.com/333"},
    {"Id": 444, "Url": "http://example.com/444"},
]

EXPECTED_APRICOT_JSON = {
    "Availability": "Everyone",
    "BasePrice": 78.9,
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "Description": "",
    "EventId": 12345,
    "GuestPrice": 78.9,
    "GuestRegistrationPolicy": "NumberOfGuests",
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
    "GuestRegistrationPolicy": "NumberOfGuests",
    "IsEnabled": False,
    "IsWaitlistEnabled": True,
    "MaximumRegistrantsCount": 6,
    "Name": "Meetup RSVP",
    "UnavailabilityPolicy": "ShowDisabled",
}

EXPECTED_MEMBERS_ONLY_JSON = {
    "Availability": "MembersOnly",
    "AvailableForMembershipLevels": SAMPLE_MEMBER_LEVELS,
    "BasePrice": 78.9,
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "Description": "",
    "EventId": 12345,
    "GuestPrice": 78.9,
    "GuestRegistrationPolicy": "NumberOfGuests",
    "IsEnabled": True,
    "IsWaitlistEnabled": True,
    "MaximumRegistrantsCount": 6,
    "Name": "Members Only",
    "UnavailabilityPolicy": "ShowDisabled",
}


@pytest.fixture()
def event_registration_type_maker():
    """Return an event registration type maker."""
    return EventRegistrationTypeMaker(SAMPLE_MEMBER_LEVELS)


def test_make_unrestricted_apricot_registration_type_for_json(
    event_registration_type_maker,
):
    """Test converting an unrestricted Wild Apricot RSVP event registration
    type into dictionaries and lists suitable for conversion to JSON."""
    reg_type = (
        event_registration_type_maker.make_unrestricted_apricot_registration_type(
            12345, 6, 78.9
        )
    )
    assert reg_type.for_json() == EXPECTED_APRICOT_JSON


def test_make_meetup_registration_type_for_json(event_registration_type_maker):
    """Test converting a Meetup RSBP event registration type into dictionaries
    and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_meetup_registration_type(12345, 6)
    assert reg_type.for_json() == EXPECTED_MEETUP_JSON


def test_make_members_only_registration_type_for_json(event_registration_type_maker):
    """Test converting a members only RSVP event registration type into
    dictionaries and lists suitable for conversion to JSON."""
    reg_type = event_registration_type_maker.make_members_only_registration_type(
        12345, 6, 78.9
    )
    assert reg_type.for_json() == EXPECTED_MEMBERS_ONLY_JSON


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
