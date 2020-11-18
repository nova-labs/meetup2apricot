"""Tests for Meetup API"""

from meetup2apricot.meetup_api import MeetupApi
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

SAMPLE_GROUP_NAME = "Nova-Labs"


@pytest.fixture()
def meetup_api():
    """Return a Meetup API configured to connect to Meetup.com."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    return MeetupApi(requests, OpenThrottle(), group_name, MEETUP_EVENTS_WANTED)


@pytest.fixture()
def mock_session(mocker):
    """Return a mock session."""
    mock_session = mocker.Mock()
    return mock_session


@pytest.fixture()
def meetup_api_mock_session(mock_session):
    """Return a Meetup API with a mock session."""
    return MeetupApi(
        mock_session, OpenThrottle(), SAMPLE_GROUP_NAME, MEETUP_EVENTS_WANTED
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
def meetup_api_for_status(mock_session_for_status):
    """Return a Meetup API mocked to return a status response."""
    return MeetupApi(
        mock_session_for_status, OpenThrottle(), SAMPLE_GROUP_NAME, MEETUP_EVENTS_WANTED
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
    retriever = MeetupApi(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url() == "https://api.meetup.com/"


def test_build_url_one():
    """Test building a URL with one additional path segment."""
    retriever = MeetupApi(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url("events") == "https://api.meetup.com/events"


def test_build_url_two():
    """Test building a URL with two additional path segments."""
    retriever = MeetupApi(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    assert retriever.build_url("events", "1234") == "https://api.meetup.com/events/1234"


def test_request_params():
    """Test building a request parameter dictionary."""
    retriever = MeetupApi(None, None, "foo_name", MEETUP_EVENTS_WANTED)
    expected_params = {
        "page": MEETUP_EVENTS_WANTED,
        "fields": "featured_photo",
        "scroll": "recent_past",
    }
    assert retriever.request_params() == expected_params


def test_retrieve_status_request_interaction(
    meetup_api_for_status, mock_session_for_status
):
    """Test the interaction with Requests when retrieving Meetup's API status."""
    response = meetup_api_for_status.retrieve_status()
    mock_session_for_status.get.assert_called_once_with("https://api.meetup.com/status")


def test_retrieve_status_response(module_file_path, meetup_api):
    """Save the response from a status request to Meetup."""
    response = meetup_api.retrieve_status()
    save_response(response, module_file_path)


def test_retrieve_events_response(module_file_path, meetup_api):
    """Save response from an events request to Meetup."""
    response_json = meetup_api.retrieve_events_json()
    save_json(response_json, module_file_path)


def test_retrieve_events_response_one(module_file_path, meetup_api):
    """Save response from an individual event request to Meetup."""
    event_id = os.getenv("MEETUP_EVENT_ID")
    if not event_id:
        pytest.skip("Define environment variable MEETUP_EVENT_ID")
    response_json = meetup_api.retrieve_events_json(event_id)
    save_json(response_json, module_file_path)


def test_make_throttle(meetup_api, mocker):
    """Test making a throttle from Meetup API response header data."""
    sample_response = mocker.Mock()
    sample_response.headers = SAMPLE_STATUS_RESPONSE_HEADERS
    throttle = meetup_api.make_throttle(sample_response)
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 10


def test_make_meetup_api_throttle(meetup_api_for_status):
    """Test the making a throttle."""
    throttle = meetup_api_for_status.make_meetup_api_throttle()
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 10


def test_retrieve_event_interaction(mock_session, meetup_api_mock_session):
    """Test interaction with Requests when requesting an event."""
    meetup_api_mock_session.retrieve_event_json("12345")
    mock_session.get.assert_called_once_with(
        "https://api.meetup.com/Nova-Labs/events/12345"
    )


def test_retrieve_event_success(mock_session, meetup_api_mock_session, mocker):
    """Test retrieving an existing event from Meetup."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json = mocker.Mock(return_value="foo")
    mock_session.get = mocker.Mock(return_value=mock_response)
    assert meetup_api_mock_session.retrieve_event_json("12345") == "foo"


def test_retrieve_event_not_found(mock_session, meetup_api_mock_session, mocker):
    """Test retrieving a missing event from Meetup."""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_session.get = mocker.Mock(return_value=mock_response)
    assert meetup_api_mock_session.retrieve_event_json("12345") == None


def test_retrieve_event(module_file_path, meetup_api):
    """Save response from an individual event request to Meetup."""
    event_id = os.getenv("MEETUP_EVENT_ID")
    if not event_id:
        pytest.skip("Define environment variable MEETUP_EVENT_ID")
    response_json = meetup_api.retrieve_event_json(event_id)
    save_json(response_json, module_file_path)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
