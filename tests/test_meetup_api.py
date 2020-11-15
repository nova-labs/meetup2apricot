"""Tests for Meetup API"""

from meetup2apricot.meetup_api import MeetupEventsRetriever
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
    return MeetupEventsRetriever(
        requests, OpenThrottle(), group_name, MEETUP_EVENTS_WANTED
    )


@pytest.fixture()
def mock_session_for_status(mocker):
    """Return a mock session the returns status responses."""
    sample_response = mocker.Mock()
    sample_response.headers = SAMPLE_STATUS_RESPONSE_HEADERS
    mock_session = mocker.Mock()
    mock_session.get = mocker.Mock(return_value=sample_response)
    return mock_session


@pytest.fixture()
def meetup_event_retriever_for_status(mock_session_for_status):
    """Return a Meetup events retriever mocked to return a status response."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    return MeetupEventsRetriever(
        mock_session_for_status, OpenThrottle(), group_name, MEETUP_EVENTS_WANTED
    )


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
        "fields": "featured_photo",
        "scroll": "recent_past",
    }
    assert retriever.request_params() == expected_params


def test_retrieve_status_request_interaction(
    meetup_event_retriever_for_status, mock_session_for_status
):
    """Test the interaction with Requests when retrieving Meetup's API status."""
    response = meetup_event_retriever_for_status.retrieve_status()
    mock_session_for_status.get.assert_called_once_with("https://api.meetup.com/status")


def test_retrieve_status_response(module_file_path, meetup_event_retriever):
    """Save the response from a status request to Meetup."""
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


def test_make_throttle(meetup_event_retriever, mocker):
    """Test making a throttle from Meetup API response header data."""
    sample_response = mocker.Mock()
    sample_response.headers = SAMPLE_STATUS_RESPONSE_HEADERS
    throttle = meetup_event_retriever.make_throttle(sample_response)
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 10


def test_make_meetup_api_throttle(meetup_event_retriever_for_status):
    """Test the interaction with Requests when retrieving Meetup's API status."""
    throttle = meetup_event_retriever_for_status.make_meetup_api_throttle()
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 10


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
