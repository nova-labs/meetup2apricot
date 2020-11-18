"""Test the event processor."""

from meetup2apricot.event_processor import EventProcessor, load_cached_event_mapping
from datetime import datetime
from .sample_apricot_json import (
    EXPECTED_FREE_PHOTO_PATH,
    EXPECTED_FREE_EVENT_JSON,
    EXPECTED_TAGS,
    EXPECTED_FREE_TAGS,
)
import pickle
import pytest


EARLIEST_START_TIME = datetime.fromisoformat("2020-11-10 00:00 -05:00")
LATEST_START_TIME = datetime.fromisoformat("2020-12-31 23:59 -05:00")

KNOWN_EVENTS = {
    "274139316": {
        "wild_apricot_event": "4041234",
        "start_time": "2020-11-13 19:00 -05:00",
    }
}

EXPECTED_APRICOT_EVENT_ID = 43210987

EXPECTED_REGISTRATION_TYPE_ID = 76543

CACHE_FILE_NAME = "event_processor.pickle"

EXPECTED_MEETUP_RSVP_TYPE_FOR_FREE = {
    "EventId": EXPECTED_APRICOT_EVENT_ID,
    "Name": "Meetup RSVP",
    "IsEnabled": False,
    "Description": "RSVPs on Meetup",
    "BasePrice": 0.0,
    "GuestPrice": 0.0,
    "Availability": "Everyone",
    "MaximumRegistrantsCount": 3,
    "GuestRegistrationPolicy": "NumberOfGuests",
    "UnavailabilityPolicy": "ShowDisabled",
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "IsWaitlistEnabled": True,
}

EXPECTED_RSVP_TYPE_FOR_FREE = {
    "EventId": EXPECTED_APRICOT_EVENT_ID,
    "Name": "RSVP",
    "IsEnabled": True,
    "Description": "",
    "BasePrice": 0.0,
    "GuestPrice": 0.0,
    "Availability": "Everyone",
    "MaximumRegistrantsCount": None,
    "GuestRegistrationPolicy": "NumberOfGuests",
    "UnavailabilityPolicy": "ShowDisabled",
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "IsWaitlistEnabled": True,
}

EXPECTED_MEETUP_RSVP_TYPE_FOR_PAID = {
    "EventId": 7890,
    "Name": "Meetup RSVP",
    "IsEnabled": False,
    "Description": "RSVPs on Meetup",
    "BasePrice": 0.0,
    "GuestPrice": 0.0,
    "Availability": "Everyone",
    "MaximumRegistrantsCount": 2,
    "GuestRegistrationPolicy": "NumberOfGuests",
    "UnavailabilityPolicy": "ShowDisabled",
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "IsWaitlistEnabled": True,
}

EXPECTED_RSVP_TYPE_FOR_PAID = {
    "EventId": 7890,
    "Name": "RSVP",
    "IsEnabled": True,
    "Description": "",
    "BasePrice": 20.0,
    "GuestPrice": 20.0,
    "Availability": "Everyone",
    "MaximumRegistrantsCount": 4,
    "GuestRegistrationPolicy": "NumberOfGuests",
    "UnavailabilityPolicy": "ShowDisabled",
    "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
    "CancellationDaysBeforeEvent": 2,
    "IsWaitlistEnabled": True,
}


@pytest.fixture()
def mock_photo_cache(mocker):
    """Mock a photo cache, which implements a "cache_photo" method."""
    mock_photo_cache = mocker.Mock()
    mock_photo_cache.cache_photo = mocker.Mock(return_value="foo.jpg")
    return mock_photo_cache


@pytest.fixture()
def mock_apricot_api(mocker):
    """Mock a Wild Apricot API interface."""
    mock_apricot_api = mocker.Mock()
    mock_apricot_api.add_event = mocker.Mock(return_value=EXPECTED_APRICOT_EVENT_ID)
    mock_apricot_api.add_registration_type = mocker.Mock(
        return_value=EXPECTED_REGISTRATION_TYPE_ID
    )
    return mock_apricot_api


@pytest.fixture()
def event_processor(mock_photo_cache, mock_apricot_api, tmp_path, event_tagger):
    return EventProcessor(
        earliest_start_time=EARLIEST_START_TIME,
        latest_start_time=LATEST_START_TIME,
        known_events=KNOWN_EVENTS.copy(),
        photo_cache=mock_photo_cache,
        apricot_api=mock_apricot_api,
        cache_path=tmp_path / CACHE_FILE_NAME,
        event_tagger=event_tagger,
    )


def test_can_ignore_event_past(event_processor, free_meetup_event):
    """Test that an event before the earliest start time can be ignored."""
    assert event_processor.can_ignore_event(free_meetup_event)


def test_can_ignore_event_future_new(event_processor, later_free_meetup_event):
    """Test that an unseen event after the earliest start time can not be
    ignored."""
    assert not event_processor.can_ignore_event(later_free_meetup_event)

def test_can_ignore_event_far_future(event_processor, much_later_free_meetup_event):
    """Test that an unseen event after the latest start time can be ignored."""
    assert event_processor.can_ignore_event(much_later_free_meetup_event)


def test_can_ignore_event_seen(event_processor, paid_meetup_event):
    """Test that a previously seen event can be ignored."""
    assert event_processor.can_ignore_event(paid_meetup_event)


def test_get_photo(event_processor, free_meetup_event, mock_photo_cache):
    """Test getting a photo and it's Wild Apricot path."""
    assert event_processor.get_photo(free_meetup_event) == "foo.jpg"
    mock_photo_cache.cache_photo.assert_called_once_with(free_meetup_event)


def test_add_apricot_event(event_processor, free_meetup_event, mock_apricot_api):
    """Test adding a Wild Apricot event."""
    assert (
        event_processor.add_apricot_event(
            free_meetup_event, EXPECTED_FREE_PHOTO_PATH, EXPECTED_FREE_TAGS
        )
        == EXPECTED_APRICOT_EVENT_ID
    )
    mock_apricot_api.add_event.assert_called_once_with(EXPECTED_FREE_EVENT_JSON)


def test_add_event_registration_types_unlimited(
    event_processor, free_meetup_event, mock_apricot_api, mocker
):
    """Test adding registration types for a Wild Apricot event with unlimited
    capacity."""
    expected_calls = [
        mocker.call(EXPECTED_MEETUP_RSVP_TYPE_FOR_FREE),
        mocker.call(EXPECTED_RSVP_TYPE_FOR_FREE),
    ]
    event_processor.add_event_registration_types(
        free_meetup_event, EXPECTED_APRICOT_EVENT_ID
    )
    mock_apricot_api.add_registration_type.assert_has_calls(expected_calls)


def test_add_event_registration_types_limited(
    event_processor, paid_meetup_event, mock_apricot_api, mocker
):
    """Test adding registration types for a Wild Apricot event with limited
    capacity."""
    expected_calls = [
        mocker.call(EXPECTED_MEETUP_RSVP_TYPE_FOR_PAID),
        mocker.call(EXPECTED_RSVP_TYPE_FOR_PAID),
    ]
    event_processor.add_event_registration_types(paid_meetup_event, 7890)
    mock_apricot_api.add_registration_type.assert_has_calls(expected_calls)


def test_record_event(event_processor, free_meetup_event):
    """Test recording a known event."""
    assert free_meetup_event.meetup_id not in event_processor.known_events
    event_processor.record_event(free_meetup_event, EXPECTED_APRICOT_EVENT_ID)
    assert event_processor.known_events[free_meetup_event.meetup_id] == {
        "wild_apricot_event": EXPECTED_APRICOT_EVENT_ID,
        "start_time": free_meetup_event.start_time,
    }


def test_process_skip(event_processor, free_meetup_event):
    """Test processing an event to skip."""
    event_processor.process(free_meetup_event)
    assert free_meetup_event.meetup_id not in event_processor.known_events


def test_process(event_processor, later_free_meetup_event, mock_apricot_api, mocker):
    """Test processing an event."""
    expected_calls = [
        mocker.call(EXPECTED_MEETUP_RSVP_TYPE_FOR_FREE),
        mocker.call(EXPECTED_RSVP_TYPE_FOR_FREE),
    ]
    event_processor.process(later_free_meetup_event)
    assert event_processor.known_events[later_free_meetup_event.meetup_id] == {
        "wild_apricot_event": EXPECTED_APRICOT_EVENT_ID,
        "start_time": later_free_meetup_event.start_time,
    }
    mock_apricot_api.add_registration_type.assert_has_calls(expected_calls)


def test_persist(event_processor, tmp_path):
    """Test persisting the event processor."""
    event_processor.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    with data_path.open("rb") as data_file:
        cached_data = pickle.load(data_file)
    assert cached_data == KNOWN_EVENTS


def test_load_cached_event_mapping(event_processor, tmp_path):
    """Test loading cached data."""
    event_processor.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    known_events = load_cached_event_mapping(data_path)
    assert known_events == KNOWN_EVENTS


def test_make_load_cached_event_mapping_no_prior(tmp_path):
    """Test loading cached data with no prior cached data."""
    data_path = tmp_path / "event_processor.pickle"
    known_events = load_cached_event_mapping(data_path)
    assert known_events == {}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
