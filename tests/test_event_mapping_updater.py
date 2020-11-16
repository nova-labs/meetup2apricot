"""Test event mapping updaters."""

from meetup2apricot.event_mapping_updater import EventMappingUpdater
from datetime import datetime
import pytest

SAMPLE_EARLIEST_START_TIME = datetime.fromisoformat("2020-11-06 00:00 -05:00")

MEETUP_ID_1 = "1234"
MEETUP_ID_2 = "3456"
MEETUP_ID_3 = "5678"
FREE_MEETUP_ID = "pfsbvrybcpbmb"

APRICOT_DATA_1 = {
    "wild_apricot_event": 9876,
    "start_time": datetime.fromisoformat("2020-11-01 19:30 -05:00"),
}

APRICOT_DATA_2 = {
    "wild_apricot_event": 6543,
    "start_time": datetime.fromisoformat("2020-11-09 21:00 -05:00"),
}

APRICOT_DATA_3 = {
    "wild_apricot_event": 3210,
    "start_time": datetime.fromisoformat("2020-11-12 18:00 -05:00"),
}

SAMPLE_EVENT_MAPPING = {
    MEETUP_ID_1: APRICOT_DATA_1,
    MEETUP_ID_2: APRICOT_DATA_2,
    MEETUP_ID_3: APRICOT_DATA_3,
}


@pytest.fixture
def mock_meetup_event_retriever(mocker, free_meetup_event):
    """Return a mock Meetup event retriever, which returns the free event."""
    mock_retriever = mocker.Mock()
    mock_retriever.get_event = mocker.Mock(side_effect=[free_meetup_event, None])
    return mock_retriever


@pytest.fixture
def event_mapping_updater(mock_meetup_event_retriever):
    """Return an event mapping updater for testing."""
    return EventMappingUpdater(mock_meetup_event_retriever, SAMPLE_EARLIEST_START_TIME)


def test_is_timely_early(event_mapping_updater):
    """Test is start date with an early event."""
    assert not event_mapping_updater.is_timely(APRICOT_DATA_1)


def test_is_timely_late(event_mapping_updater):
    """Test is start date with a late event."""
    assert event_mapping_updater.is_timely(APRICOT_DATA_2)


def test_update_meetup_id(event_mapping_updater):
    """Test getting an updated meetup ID."""
    assert event_mapping_updater.update_meetup_id(MEETUP_ID_1) == FREE_MEETUP_ID


def test_update_meetup_id_none(
    event_mapping_updater, mock_meetup_event_retriever, mocker
):
    """Test getting an updated meetup ID when none is available."""
    mock_meetup_event_retriever.get_event = mocker.Mock(return_value=None)
    assert event_mapping_updater.update_meetup_id(MEETUP_ID_2) == None


def test_update_event_mapping(event_mapping_updater):
    expected_mapping = {FREE_MEETUP_ID: APRICOT_DATA_2}
    assert (
        event_mapping_updater.update_event_mapping(SAMPLE_EVENT_MAPPING)
        == expected_mapping
    )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
