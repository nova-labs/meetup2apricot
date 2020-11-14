"""Tests for Meetup API"""

from meetup2apricot.meetup_api import MeetupEventsRetriever, start_requests_session
from meetup2apricot.throttle import Throttle, OpenThrottle
import os
import json
import logging
import requests
from requests_toolbelt.utils import dump
import pytest


MEETUP_EVENTS_WANTED = 199

SAMPLE_STATUS_RESPONSE_HEADERS = {
    "X-RateLimit-Limit": 30,
    "X-RateLimit-Remaining": 29,
    "X-RateLimit-Reset": 10,
}


@pytest.fixture()
def meetup_event_retriever():
    """Return a Meetup events retriever configured to connect to Meetup.com."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    return MeetupEventsRetriever(requests, OpenThrottle(), group_name, MEETUP_EVENTS_WANTED)


def save_response(response, path):
    """Save an HTTP response to the path."""
    with path.with_suffix(".txt").open("w") as f:
        data = dump.dump_response(response)
        print(data.decode("utf-8"), file=f)


def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent=4, sort_keys=True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file=f)


def test_build_url_none():
    """Test building a URL with no additional path segments."""
    retriever = MeetupEventsRetriever(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url() == "https://api.meetup.com/"


def test_build_url_one():
    """Test building a URL with one additional path segment."""
    retriever = MeetupEventsRetriever(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url("events") == "https://api.meetup.com/events"


def test_build_url_two():
    """Test building a URL with two additional path segments."""
    retriever = MeetupEventsRetriever(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url("events", "1234") == "https://api.meetup.com/events/1234"


def test_request_params():
    """Test building a request parameter dictionary."""
    retriever = MeetupEventsRetriever(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    expected_params = {
        "page": MEETUP_EVENTS_WANTED,
        "fields": "series,featured_photo",
        "scroll": "recent_past",
    }
    assert retriever.request_params() == expected_params


def test_retrieve_status_request_interaction(meetup_event_retriever, mocker):
    """Test the interaction with Requests when retrieving Meetup's API status."""
    sample_response = mocker.Mock()
    sample_response.headers = SAMPLE_STATUS_RESPONSE_HEADERS
    mocker.patch.object(requests, "get", return_value=sample_response)
    response = meetup_event_retriever.retrieve_status()
    requests.get.assert_called_once_with("https://api.meetup.com/status")


def test_retrieve_status_response(module_file_path, meetup_event_retriever, caplog):
    """Save the response from a status request to Meetup."""
    caplog.set_level(logging.INFO)
    response = meetup_event_retriever.retrieve_status()
    save_response(response, module_file_path)


def test_retrieve_events_response(module_file_path, meetup_event_retriever):
    """Save response from an events request to Meetup."""
    response_json = meetup_event_retriever.retrieve_events_json()
    save_json(response_json, module_file_path)


def test_retrieve_events_response_one(module_file_path, meetup_event_retriever):
    """Save response from an individual event request to Meetup."""
    event_id = os.getenv("MEETUP_EVENT_ID")
    if not event_id:
        pytest.skip("Define environment variable MEETUP_EVENT_ID")
    response_json = meetup_event_retriever.retrieve_events_json(event_id)
    save_json(response_json, module_file_path)


def test_make_meetup_api_throttle(meetup_event_retriever, mocker):
    """Test making a throttle from Meetup API response header data."""
    sample_response = mocker.Mock()
    sample_response.headers = SAMPLE_STATUS_RESPONSE_HEADERS
    throttle = meetup_event_retriever.make_meetup_api_throttle(sample_response)
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 10


def test_start_requests_session_user_agent():
    """Test starting a requests session with a user agent."""
    session = start_requests_session("Test 1")
    assert type(session) == requests.Session
    assert session.headers["User-Agent"] == "Test 1"


def test_start_requests_session_no_user_agent():
    """Test starting a requests session with a user agent."""
    session = start_requests_session()
    assert type(session) == requests.Session


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
