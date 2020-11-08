"""Test Wild Apricot event registration types."""

from meetup2apricot.event_registration_type import \
    make_meetup_registration_type, make_apricot_registration_type

import pytest

EXPECTED_APRICOT_JSON = {
    'Availability': 'Everyone',
    'BasePrice': 78.9,
    'CancellationBehaviour': 'AllowUpToPeriodBeforeEvent',
    'CancellationDaysBeforeEvent': 2,
    'Description': '',
    'EventId': 12345,
    'GuestPrice': 78.9,
    'GuestRegistrationPolicy': 'CollectContactDetails',
    'IsEnabled': True,
    'IsWaitlistEnabled': False,
    'MaximumRegistrantsCount': 6,
    'Name': 'RSVP',
    'UnavailabilityPolicy': 'ShowDisabled'
    }

EXPECTED_MEETUP_JSON = {
    'Availability': 'Everyone',
    'BasePrice': 0.0,
    'CancellationBehaviour': 'AllowUpToPeriodBeforeEvent',
    'CancellationDaysBeforeEvent': 2,
    'Description': 'RSVPs on Meetup',
    'EventId': 12345,
    'GuestPrice': 0.0,
    'GuestRegistrationPolicy': 'CollectContactDetails',
    'IsEnabled': False,
    'IsWaitlistEnabled': False,
    'MaximumRegistrantsCount': 6,
    'Name': 'Meetup RSVP',
    'UnavailabilityPolicy': 'ShowDisabled'
    }


def test_make_apricot_registration_type_for_json():
    """Test converting a Wild Apricot RSVP event registration type into
    dictionaries and lists suitable for conversion to JSON."""
    reg_type = make_apricot_registration_type(12345, 6, 78.9)
    assert reg_type.for_json() == EXPECTED_APRICOT_JSON

def test_make_meetup_registration_type_for_json():
    """Test converting a Meetup RSBP event registration type into dictionaries
    and lists suitable for conversion to JSON."""
    reg_type = make_meetup_registration_type(12345, 6)
    assert reg_type.for_json() == EXPECTED_MEETUP_JSON

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
