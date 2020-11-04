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
    assert meetup_event.name == "TEST-ETL: AC: Mending Monday"

def test_start_time(free_meetup_event_json):
    """Test getting the start time from Meetup event JSON."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert meetup_event.start_time == datetime.fromisoformat("2020-11-09 19:00 -05:00")

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



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
