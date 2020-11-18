"""Test generating the Wild Apricot API."""

from meetup2apricot.apricot_api import ApricotApi
from meetup2apricot.http_response_error import ApricotApiError
from meetup2apricot.throttle import Throttle
from .sample_apricot_json import EXPECTED_FREE_EVENT_JSON
from requests_toolbelt.utils import dump
import json
import os
import pytest


@pytest.fixture(scope="module")
def apricot_throttle():
    """Return a Wild Apricot throttle: 100 requests per 60 seconds."""
    return Throttle(100, 60)


@pytest.fixture()
def apricot_api(apricot_session, apricot_throttle):
    """Return a Wild Apricot API."""
    account_id = os.getenv("APRICOT_ACCOUNT_ID")
    if not account_id:
        pytest.skip("Define environment variable APRICOT_ACCOUNT_ID")
    return ApricotApi(account_id, apricot_session, apricot_throttle)


def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent=4, sort_keys=True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file=f)


def save_response(response, path):
    """Save an HTTP response to the path."""
    with path.with_suffix(".txt").open("w") as f:
        data = dump.dump_response(response)
        print(data.decode("utf-8"), file=f)


def test_bad_status(apricot_api):
    """Test raising a Wild Apricot API error for a bad HTTP response status."""
    bad_about_url = ApricotApi.api_url + "/x"
    with pytest.raises(ApricotApiError, match=r".*HTTP status is \d+, not ok.*"):
        apricot_api.get_response(bad_about_url)


# These tests retrieve and save data from Wild Apricot to aid development.
# Provide required environment variables to run these tests.


def test_get_api_versions(module_file_path, apricot_api):
    """Save response from a "api versions" request to Wild Apricot."""
    apricot_json = apricot_api.get_json(ApricotApi.api_url)
    save_json(apricot_json, module_file_path)


def test_get_accounts(module_file_path, apricot_api):
    """Save response with account list."""
    apricot_json = apricot_api.get_json(ApricotApi.api_url + "/v2.2/accounts/")
    save_json(apricot_json, module_file_path)


def test_get_event_response(module_file_path, apricot_api):
    """Save response from an "event id" request to Wild Apricot."""
    event_id = os.getenv("APRICOT_EVENT_ID")
    if not event_id:
        pytest.skip("Define environment variable APRICOT_EVENT_ID")
    apricot_json = apricot_api.get_event(event_id)
    save_json(apricot_json, module_file_path)


@pytest.mark.skip("Avoid adding test events to live system.")
def test_add_event_free(module_file_path, apricot_api):
    """Save response from adding a free event to Wild Apricot."""
    response = apricot_api.add_event(EXPECTED_FREE_EVENT_JSON)
    with module_file_path.open("wt") as response_file:
        response_file.write(f"{response:d}\n")


# These tests mock the Wild Apricot session and check that the appropriate
# parameters reach the right URL.


def test_add_event(mocker):
    """Test posting parameters when adding an event."""
    sample_event = {"name": "Sample Event", "start_date": "2020-11-02 19:00"}
    expected_url = "https://api.wildapricot.org/v2.2/accounts/123/events"
    mock_response = mocker.Mock()
    mock_response.content = "4567"
    apricot_api = ApricotApi("123", None, None)
    apricot_api.post = mocker.Mock(return_value=mock_response)
    response = apricot_api.add_event(sample_event)
    assert response == 4567
    apricot_api.post.assert_called_once_with(expected_url, json=sample_event)


def test_add_registration_type(mocker):
    """Test posting parameters when adding an event registration type."""
    sample_registration_type = {"name": "RSVP"}
    expected_url = (
        "https://api.wildapricot.org/v2.2/accounts/123/EventRegistrationTypes"
    )
    mock_response = mocker.Mock()
    mock_response.content = "4567"
    apricot_api = ApricotApi("123", None, None)
    apricot_api.post = mocker.Mock(return_value=mock_response)
    response = apricot_api.add_registration_type(sample_registration_type)
    assert response == 4567
    apricot_api.post.assert_called_once_with(
        expected_url, json=sample_registration_type
    )


# These tests check that dry runs return values.


def test_add_event_dry_run():
    """Test that an add event dry run returns a value without contacting Wild
    Apricot."""
    sample_event = {}
    apricot_api = ApricotApi("123", None, None)
    apricot_api.dryrun = True
    assert apricot_api.add_event(sample_event) == 12345


def test_add_registration_type_dry_run():
    """Test that an add event registration type dry run returns a value without
    contacting Wild Apricot."""
    sample_registration_type = {}
    apricot_api = ApricotApi("123", None, None)
    apricot_api.dryrun = True
    assert apricot_api.add_registration_type(sample_registration_type) == 98765


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
