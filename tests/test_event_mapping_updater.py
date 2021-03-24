"""Test event mapping updaters."""

from meetup2apricot.event_mapping_updater import EventMappingUpdater
from datetime import datetime
import pytest

SAMPLE_EARLIEST_START_TIME = datetime.fromisoformat("2020-11-06 00:00 -05:00")

MEETUP_ID_1 = "1234"
MEETUP_ID_2 = "3456"
FREE_MEETUP_ID = "pfsbvrybcpbmb"
PAID_MEETUP_ID = "274139316"
PREV_FREE_MEETUP_ID = "abcde"

APRICOT_DATA_1 = {
    "wild_apricot_event": 4321,
    "start_time": datetime.fromisoformat("2020-11-01 19:30 -05:00"),
}

APRICOT_DATA_2 = {
    "wild_apricot_event": 6543,
    "start_time": datetime.fromisoformat("2020-11-07 18:00 -05:00"),
}

FREE_EVENT_APRICOT_DATA = {
    "wild_apricot_event": 8765,
    "start_time": datetime.fromisoformat("2020-11-09 21:00 -05:00"),
}

SAMPLE_EVENT_MAPPING = {
    MEETUP_ID_1: APRICOT_DATA_1,
    MEETUP_ID_2: APRICOT_DATA_2,
    FREE_MEETUP_ID: FREE_EVENT_APRICOT_DATA,
}


class MeetupEventRetrieverFake:

    """Returns free and paid Meetup events from several IDs."""

    def __init__(self, free_meetup_event, paid_meetup_event):
        """Initialize with free and paid Meetup events."""
        self.events = {
            free_meetup_event.meetup_id: free_meetup_event,
            PREV_FREE_MEETUP_ID: free_meetup_event,
            paid_meetup_event.meetup_id: paid_meetup_event,
        }

    def get_event(self, meetup_event_id):
        """Fake getting and returning a Meetup event by its ID."""
        return self.events.get(meetup_event_id, None)


@pytest.fixture
def fake_meetup_event_retriever(free_meetup_event, paid_meetup_event):
    """Return a fake Meetup event retriever for testing."""
    return MeetupEventRetrieverFake(free_meetup_event, paid_meetup_event)


@pytest.fixture
def event_mapping_updater(fake_meetup_event_retriever):
    """Return an event mapping updater for testing."""
    return EventMappingUpdater(
        fake_meetup_event_retriever,
        SAMPLE_EARLIEST_START_TIME,
        [],  # TODO provide skip Meetup event IDs
    )


def test_is_timely_early(event_mapping_updater):
    """Test is start date with an early event."""
    assert not event_mapping_updater.is_timely(APRICOT_DATA_1)


def test_is_timely_late(event_mapping_updater):
    """Test is start date with a late event."""
    assert event_mapping_updater.is_timely(APRICOT_DATA_2)


def test_update_meetup_id(event_mapping_updater):
    """Test getting an updated meetup ID."""
    assert event_mapping_updater.update_meetup_id(PREV_FREE_MEETUP_ID) == FREE_MEETUP_ID


def test_update_meetup_id_unchanged(event_mapping_updater):
    """Test getting an unchanged meetup ID."""
    assert event_mapping_updater.update_meetup_id(PAID_MEETUP_ID) == PAID_MEETUP_ID


def test_update_meetup_id_none(event_mapping_updater):
    """Test getting an updated meetup ID when none is available."""
    assert event_mapping_updater.update_meetup_id(MEETUP_ID_2) == None


def test_update_event_mapping(event_mapping_updater):
    expected_mapping = {FREE_MEETUP_ID: FREE_EVENT_APRICOT_DATA}
    assert (
        event_mapping_updater.update_event_mapping(SAMPLE_EVENT_MAPPING)
        == expected_mapping
    )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
