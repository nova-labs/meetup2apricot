"""Test the Meetup to Wild Apricot event adaptor."""

from meetup2apricot.meetup_event import MeetupEvent
from meetup2apricot.meetup_to_apricot_event_adaptor import MeetupToApricotEventAdaptor
from .sample_apricot_json import (
    EXPECTED_FREE_EVENT_JSON,
    EXPECTED_FREE_DESCRIPTION_HTML,
    EXPECTED_FREE_PHOTO_PATH,
    EXPECTED_TAGS,
    EXPECTED_FREE_TAGS,
    EXPECTED_PAID_DESCRIPTION_HTML,
    EXPECTED_PAID_EVENT_JSON,
)
from datetime import datetime
import pytest


@pytest.fixture()
def free_event_adaptor(free_meetup_event_json):
    meetup_event = MeetupEvent(free_meetup_event_json)
    return MeetupToApricotEventAdaptor(
        meetup_event, EXPECTED_FREE_PHOTO_PATH, EXPECTED_FREE_TAGS
    )


@pytest.fixture()
def paid_event_adaptor(paid_meetup_event_json):
    meetup_event = MeetupEvent(paid_meetup_event_json)
    return MeetupToApricotEventAdaptor(meetup_event, None, EXPECTED_TAGS)


def test_name(free_event_adaptor):
    """Test returning the event title."""
    assert free_event_adaptor.name == "AC: Mending Monday (Test Event)"


def test_description_html_photo(free_event_adaptor):
    """Test returning the full HTML event description with a photo."""
    assert free_event_adaptor.description_html == EXPECTED_FREE_DESCRIPTION_HTML


def test_description_html_no_photo(paid_event_adaptor):
    """Test returning the full HTML event description with a no photo."""
    assert paid_event_adaptor.description_html == EXPECTED_PAID_DESCRIPTION_HTML


def test_event_type(free_event_adaptor):
    """Test returning a flag that indicates if event is simple (RSVP) or
    regular. Enum: [ Reqular, RSVP ]"""
    assert free_event_adaptor.event_type == "Regular"


def test_start_date(free_event_adaptor):
    """Test returning the date and time when the event is scheduled to
    start. If no time offset is specified, counts as UTC and will be
    converted into event timezone."""
    assert free_event_adaptor.start_date == datetime.fromisoformat(
        "2020-11-09 19:00 -05:00"
    )


def test_start_time_specified(free_event_adaptor):
    """Test returning a flag that indicates if event start time is
    specified. False means that StartDate contains only date component."""
    assert free_event_adaptor.start_time_specified


def test_end_date(free_event_adaptor):
    """Test returning the date and time when the event is scheduled to end.
    Could be empty. If no time offset is specified, counts as UTC and will
    be converted into event timezone."""
    assert free_event_adaptor.end_date == datetime.fromisoformat(
        "2020-11-09 21:00 -05:00"
    )


def test_end_time_specified(free_event_adaptor):
    """Test returning a flag that indicates if event end time is specified.
    False means that EndDate contains only date component."""
    assert free_event_adaptor.end_time_specified


def test_location_online(free_event_adaptor):
    """Test returning the location when the event is online."""
    assert free_event_adaptor.location == "Online event"


def test_location_address(paid_event_adaptor):
    """Test returning the location when the event has a street address."""
    assert (
        paid_event_adaptor.location
        == "Nova Labs Inc., 1916 Isaac Newton Square W, Reston, VA 20190"
    )


def test_registration_enabled(free_event_adaptor):
    """Test returning a flag that indicates that registration to this event
    is enabled."""
    assert free_event_adaptor.registration_enabled


def test_registrations_limit_none(free_event_adaptor):
    """Test returning the maximum number of registrations for this
    event, which has no limit."""
    assert free_event_adaptor.registrations_limit is None


def test_registrations_limit_set(paid_event_adaptor):
    """Test returning the maximum number of registrations for this
    event, which has a set limit."""
    assert paid_event_adaptor.registrations_limit == 6


def test_access_level(free_event_adaptor):
    """Test returning an enum that indicates the event accessability.
    Enum: [ Public, AdminOnly, Restricted ]"""
    assert free_event_adaptor.access_level == "Public"


def test_for_json_free(free_event_adaptor):
    """Test converting the free event into dictionaries and lists suitable for
    conversion to JSON."""
    assert free_event_adaptor.for_json() == EXPECTED_FREE_EVENT_JSON


def test_for_json_paid(paid_event_adaptor):
    """Test converting the paid event into dictionaries and lists suitable for
    conversion to JSON."""
    assert paid_event_adaptor.for_json() == EXPECTED_PAID_EVENT_JSON


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
