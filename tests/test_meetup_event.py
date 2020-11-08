"""Test event fields from a Meetup event JSON response."""

from meetup2apricot.meetup_event import MeetupEvent, MeetupVenue 
from datetime import datetime
import json
import pytest

def test_duration(free_meetup_event_json):
    """Test getting the duration from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.duration == 7200000

def test_end_time(free_meetup_event_json):
    """Test getting the end time from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.end_time == datetime.fromisoformat("2020-11-09 21:00 -05:00")

def test_find_us(free_meetup_event_json):
    """Test getting the find us from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.find_us == "https://zoom.us/j/92758362882?pwd=a2VJOGxyOTBqelNhdjY1dGpqZStjZz09"

def test_meetup_id(free_meetup_event_json):
    """Test getting the meetup ID from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.meetup_id == "pfsbvrybcpbmb"

def test_name(free_meetup_event_json):
    """Test getting the name from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.name == "AC: Mending Monday (Test Event)"

def test_start_time(free_meetup_event_json):
    """Test getting the start time from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.start_time == datetime.fromisoformat("2020-11-09 19:00 -05:00")

def test_later_start_time(later_free_meetup_event_json):
    """Test getting the start time from Meetup event JSON."""
    meetup_event = MeetupEvent(later_free_meetup_event_json)
    assert meetup_event.start_time == datetime.fromisoformat("2020-11-16 19:00 -05:00")

def test_venue_online(free_meetup_event_json):
    """Test getting the online venue from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    expected_venue = MeetupVenue("Online event", "", "", "", "")
    assert meetup_event.venue == expected_venue

def test_venue_address(paid_meetup_event_json):
    """Test getting the venue address from Meetup event JSON."""
    meetup_event = MeetupEvent(paid_meetup_event_json)
    expected_venue = MeetupVenue("Nova Labs Inc.", "1916 Isaac Newton Square W", "Reston", "VA", "20190")
    assert meetup_event.venue == expected_venue

def test_photo_url(free_meetup_event_json):
    """Test getting the highest resolution featured photo URL."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.photo_url == "https://secure.meetupstatic.com/photos/event/6/b/4/9/highres_491187465.jpeg"

def test_photo_url_missing(paid_meetup_event_json):
    """Test getting the missing highest resolution featured photo URL."""
    meetup_event = MeetupEvent(paid_meetup_event_json)
    assert meetup_event.photo_url is None

def test_fee_amount_free(free_meetup_event):
    """Test getting the fee amount from a free event."""
    assert free_meetup_event.fee_amount == 0.0

def test_fee_amount_paid(paid_meetup_event):
    """Test getting the fee amount from a paid event."""
    assert paid_meetup_event.fee_amount == 20.0

def test_yes_rsvp_count(paid_meetup_event):
    """Test getting the yes RSVP count."""
    assert paid_meetup_event.yes_rsvp_count == 2

def test_accounting_code(free_meetup_event):
    """Test getting the accounting code."""
    assert free_meetup_event.accounting_code == "AC"

def test_accounting_code_underscore(paid_meetup_event):
    """Test getting only the first part of an accounting code with an
    underscore."""
    assert paid_meetup_event.accounting_code == "AV"

def test_accounting_code_missing():
    """Test getting a missing accounting code."""
    meetup_event = MeetupEvent({"name": "NO code in event name"})
    assert meetup_event.accounting_code is None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
