"""Test the event processor."""

from meetup2apricot.event_processor import EventProcessor, make_event_processor
from datetime import datetime
from .sample_apricot_json import EXPECTED_FREE_PHOTO_NAME, EXPECTED_FREE_EVENT_JSON 
import pickle
import pytest


CUTOFF_TIME = datetime.fromisoformat("2020-11-10 00:00 -05:00")

KNOWN_EVENTS = {
    "274139316": {
        "wild_apricot_event": "4041234",
        "start_time": "2020-11-13 19:00 -05:00"
        }
    }

EXPECTED_APRICOT_EVENT_ID = "43210987"

CACHE_FILE_NAME = "event_processor.pickle"

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
    return mock_apricot_api

@pytest.fixture()
def event_processor(mock_photo_cache, mock_apricot_api, tmp_path):
    return EventProcessor(
        cutoff_time = CUTOFF_TIME,
        known_events = KNOWN_EVENTS.copy(),
        photo_cache = mock_photo_cache,
        apricot_api = mock_apricot_api,
        cache_path = tmp_path / CACHE_FILE_NAME
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

def test_get_photo(event_processor, free_meetup_event, mock_photo_cache):
    """Test getting a photo and it's Wild Apricot name."""
    assert event_processor.get_photo(free_meetup_event) == "foo.jpg"
    mock_photo_cache.cache_photo.assert_called_once_with(free_meetup_event)

def test_add_apricot_event(event_processor, free_meetup_event, mock_apricot_api):
    """Test adding a Wild Apricot event."""
    assert event_processor.add_apricot_event(free_meetup_event, EXPECTED_FREE_PHOTO_NAME) == EXPECTED_APRICOT_EVENT_ID
    mock_apricot_api.add_event.assert_called_once_with(EXPECTED_FREE_EVENT_JSON)

def test_record_event(event_processor, free_meetup_event):
    """Test recording a known event."""
    assert free_meetup_event.meetup_id not in event_processor.known_events
    event_processor.record_event(free_meetup_event, EXPECTED_APRICOT_EVENT_ID)
    assert event_processor.known_events[free_meetup_event.meetup_id] == {
            "wild_apricot_event": EXPECTED_APRICOT_EVENT_ID,
            "start_time": free_meetup_event.start_time
            }

def test_process_skip(event_processor, free_meetup_event):
    """Test processing an event to skip."""
    event_processor.process(free_meetup_event)
    assert free_meetup_event.meetup_id not in event_processor.known_events

def test_process(event_processor, later_free_meetup_event):
    """Test processing an event."""
    event_processor.process(later_free_meetup_event)
    assert event_processor.known_events[later_free_meetup_event.meetup_id] == {
            "wild_apricot_event": EXPECTED_APRICOT_EVENT_ID,
            "start_time": later_free_meetup_event.start_time
            }

def test_persist(event_processor, tmp_path):
    """Test persisting the event processor."""
    event_processor.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    with data_path.open('rb') as data_file:
        cached_data = pickle.load(data_file)
    assert cached_data == KNOWN_EVENTS 

def test_make_event_processor(event_processor, tmp_path, mock_photo_cache,
        mock_apricot_api):
    """Test making an event processor from cached data."""
    event_processor.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    another_event_processor = make_event_processor(data_path, CUTOFF_TIME,
            mock_photo_cache, mock_apricot_api)
    assert another_event_processor.cutoff_time == CUTOFF_TIME
    assert another_event_processor.known_events == KNOWN_EVENTS
    assert another_event_processor.photo_cache == mock_photo_cache
    assert another_event_processor.apricot_api == mock_apricot_api

def test_make_event_processor_no_prior(tmp_path, mock_photo_cache,
        mock_apricot_api):
    """Test making an event processor with no prior cached data."""
    data_path = tmp_path / "event_processor.pickle"
    another_event_processor = make_event_processor(data_path, CUTOFF_TIME,
            mock_photo_cache, mock_apricot_api)
    assert another_event_processor.cutoff_time == CUTOFF_TIME
    assert another_event_processor.known_events == {}
    assert another_event_processor.photo_cache == mock_photo_cache
    assert another_event_processor.apricot_api == mock_apricot_api

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
