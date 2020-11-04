"""Test the Meetup to Wild Apricot event adaptor."""

from meetup2apricot.meetup_event import MeetupEvent
from meetup2apricot.meetup_to_apricot_event_adaptor import MeetupToApricotEventAdaptor
from datetime import datetime
import pytest

@pytest.fixture()
def free_event_adaptor(free_meetup_event_json):
    meetup_event = MeetupEvent(free_meetup_event_json)
    return MeetupToApricotEventAdaptor(meetup_event)

@pytest.fixture()
def paid_event_adaptor(paid_meetup_event_json):
    meetup_event = MeetupEvent(paid_meetup_event_json)
    return MeetupToApricotEventAdaptor(meetup_event)

def test_name(free_event_adaptor):
    """Test returning the event title."""
    assert free_event_adaptor.name == "AC: Mending Monday"

def test_event_type(free_event_adaptor):
    """Test returning a flag that indicates if event is simple (RSVP) or
    regular. Enum: [ Reqular, RSVP ] """
    assert free_event_adaptor.event_type == "Regular"

def test_start_date(free_event_adaptor):
    """Test returning the date and time when the event is scheduled to
    start. If no time offset is specified, counts as UTC and will be
    converted into event timezone."""
    assert free_event_adaptor.start_date == datetime.fromisoformat("2020-11-09 19:00 -05:00")

def test_start_time_specified(free_event_adaptor):
    """Test returning a flag that indicates if event start time is
    specified. False means that StartDate contains only date component."""
    assert free_event_adaptor.start_time_specified == True

def test_end_date(free_event_adaptor):
    """Test returning the date and time when the event is scheduled to end.
    Could be empty. If no time offset is specified, counts as UTC and will
    be converted into event timezone."""
    assert free_event_adaptor.end_date == datetime.fromisoformat("2020-11-09 21:00 -05:00")

def test_end_time_specified(free_event_adaptor):
    """Test returning a flag that indicates if event end time is specified.
    False means that EndDate contains only date component."""
    assert free_event_adaptor.end_time_specified == True

def test_location_online(free_event_adaptor):
    """Test returning the location when the event is online."""
    assert free_event_adaptor.location == "Online event"

def test_location_address(paid_event_adaptor):
    """Test returning the location when the event has a street address."""
    assert paid_event_adaptor.location == "Nova Labs Inc., 1916 Isaac Newton Square W, Reston, VA 20190"

def test_registration_enabled(free_event_adaptor):
    """Test returning a flag that indicates that registration to this event
    is enabled."""
    assert free_event_adaptor.registration_enabled == True

def test_registrations_limit_none(free_event_adaptor):
    """Test returning the maximum number of registrations for this
    event, which has no limit."""
    assert free_event_adaptor.registrations_limit == None

def test_registrations_limit_set(paid_event_adaptor):
    """Test returning the maximum number of registrations for this
    event, which has a set limit."""
    assert paid_event_adaptor.registrations_limit == 6

def test_access_level(free_event_adaptor):
    """Test returning an enum that indicates the event accessability.
    Enum: [ Public, AdminOnly, Restricted ] """
    assert free_event_adaptor.access_level == "Public"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
