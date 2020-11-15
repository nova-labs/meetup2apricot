"""Test Meetup event retrievers."""

from meetup2apricot.meetup_event_retriever import MeetupEventRetriever

import pytest

CACHED_EVENT_ID = "pfsbvrybcpbmb"
CANCELLED_EVENT_ID = "1234"
MISSING_EVENT_ID = "7890"
UNCACHED_EVENT_ID = "4567"


@pytest.fixture
def sample_meetup_events(free_meetup_event):
    """Return a list of sample Meetup events."""
    return [free_meetup_event]


@pytest.fixture
def mock_meetup_api(mocker):
    """Return a mock meetup API, which should be augmented for each test."""
    return mocker.Mock()


@pytest.fixture
def meetup_event_retriever(mock_meetup_api, sample_meetup_events):
    """Return a Meetup event retriever configured with sample data."""
    return MeetupEventRetriever(mock_meetup_api, sample_meetup_events)


def test_get_event_cached(meetup_event_retriever, free_meetup_event):
    """Test getting a cached Meetup event."""
    assert meetup_event_retriever.get_event(CACHED_EVENT_ID) == free_meetup_event


def test_get_event_cancelled(meetup_event_retriever, mock_meetup_api, mocker):
    """Test getting a cancelled Meetup event."""
    cancelled_json = {"status": "cancelled"}
    mock_meetup_api.retrieve_event_json = mocker.Mock(return_value=cancelled_json)
    assert meetup_event_retriever.get_event(CANCELLED_EVENT_ID) == None
    mock_meetup_api.retrieve_event_json.assert_called_once_with(CANCELLED_EVENT_ID)


def test_get_event_missing(meetup_event_retriever, mock_meetup_api, mocker):
    """Test getting a missing Meetup event from the Meetup API."""
    mock_meetup_api.retrieve_event_json = mocker.Mock(return_value=None)
    assert meetup_event_retriever.get_event(MISSING_EVENT_ID) == None
    mock_meetup_api.retrieve_event_json.assert_called_once_with(MISSING_EVENT_ID)


def test_get_event_uncached(
    meetup_event_retriever,
    mock_meetup_api,
    paid_meetup_event_json,
    paid_meetup_event,
    mocker,
):
    """Test getting an uncached Meetup event from the Meetup API."""
    mock_meetup_api.retrieve_event_json = mocker.Mock(
        return_value=paid_meetup_event_json
    )
    meetup_event = meetup_event_retriever.get_event(UNCACHED_EVENT_ID)
    assert meetup_event.meetup_id == paid_meetup_event.meetup_id
    assert meetup_event.name == paid_meetup_event.name
    mock_meetup_api.retrieve_event_json.assert_called_once_with(UNCACHED_EVENT_ID)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
