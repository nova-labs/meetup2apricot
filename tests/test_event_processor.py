"""Test the event processor."""

from meetup2apricot.event_processor import EventProcessor
from datetime import datetime
import pytest


CUTOFF_TIME = datetime.fromisoformat("2020-11-10 00:00 -05:00")

KNOWN_EVENTS = {"274139316": "2020-11-13 19:00 -05:00"}

@pytest.fixture()
def event_processor():
    return EventProcessor(
        cutoff_time = CUTOFF_TIME,
        known_events = KNOWN_EVENTS
        )

def test_can_ignore_event_past(event_processor, free_meetup_event):
    """Test that an event before the cutoff time can be ignored."""
    assert event_processor.can_ignore_event(free_meetup_event)

def test_can_ignore_event_future_new(event_processor, later_free_meetup_event):
    """Test that an unseen event after the cutoff time can not be ignored."""
    assert not event_processor.can_ignore_event(later_free_meetup_event)

def test_can_ignore_event_seen(event_processor, paid_meetup_event):
    """Test that a previously seen event can be ignored."""
    assert event_processor.can_ignore_event(paid_meetup_event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
