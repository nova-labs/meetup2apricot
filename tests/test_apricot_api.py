"""Test generating the Wild Apricot API."""

from meetup2apricot.apricot_api import ApricotApi
from meetup2apricot.http_response_error import ApricotApiError
from requests_toolbelt.utils import dump
import json
import os
import pytest

SAMPLE_URL = "https://example.com/api"
SAMPLE_XIBO_PAGE_LENGTH = 100


@pytest.fixture()
def apricot_api(apricot_session):
    """Return a Wild Apricot API."""
    account_id = os.getenv("APRICOT_ACCOUNT_ID")
    if not account_id:
        pytest.skip("Define environment variable APRICOT_ACCOUNT_ID")
    return ApricotApi(account_id, apricot_session, SAMPLE_XIBO_PAGE_LENGTH)

def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent = 4, sort_keys = True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file = f)

def save_response(response, path):
    """Save an HTTP response to the path."""
    with path.with_suffix(".txt").open("w") as f:
        data = dump.dump_response(response)
        print(data.decode('utf-8'), file = f)

def test_bad_status(apricot_api):
    """Test raising a Wild Apricot API error for a bad HTTP response status."""
    bad_about_url = ApricotApi.api_url + "/x"
    with pytest.raises(ApricotApiError, match=r'.*HTTP status is \d+, not ok.*'):
        apricot_api.get_response(bad_about_url)

## These tests retrieve and save data from Wild Apricot to aid development.
## Provide required environment variables to run these tests.

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

## These tests from Xibo testing must be adapted or deleted.

@pytest.mark.skip(reason="Not ready to test")
def test_get_datasets_by_code_response(module_file_path, apricot_api):
    """Save response from a "dataset" request to Wild Apricot."""
    dataset_code = os.getenv("EVENT_DATASET_CODE")
    if not dataset_code:
        pytest.skip("Define environment variable EVENT_DATASET_CODE")
    apricot_json = apricot_api.get_datasets_by_code(dataset_code)
    save_json(apricot_json, module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_get_apricot_api_version(mocker):
    """Testing getting the Wild Apricot API version number."""
    apricot_api.get_about = mocker.Mock(return_value = SAMPLE_ABOUT_JSON)
    assert apricot_api.get_apricot_api_version() == "1.8.12"

@pytest.mark.skip(reason="Not ready to test")
def test_get_dataset_column_response(module_file_path, apricot_api):
    """Save response from a "dataset column" request to Wild Apricot."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    apricot_json = apricot_api.get_dataset_column_by_id(dataset_id)
    save_json(list(apricot_json), module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_get_response(module_file_path, apricot_api):
    """Save response from a "dataset data" request to Wild Apricot."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    url = apricot_api_url_builder.dataset_data_url(dataset_id)
    response = apricot_api.get_response(url, start = 100, length = 7)
    save_response(response, module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_get_dataset_data(module_file_path, apricot_api):
    """Save JSON from a "dataset data" request to Wild Apricot."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    apricot_json = apricot_api.get_dataset_data_by_id(dataset_id)
    save_json(list(apricot_json), module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_delete_row_response(module_file_path, apricot_api):
    """Save response from a "dataset data delete" request to Wild Apricot."""
    row_id = os.getenv("DELETE_ROW_ID")
    if not row_id:
        pytest.skip("Environment variable DELETE_ROW_ID is not defined")
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    response = apricot_api.delete_dataset_data_by_id(dataset_id, row_id)
    save_response(response, module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_insert_dataset_data_response(module_file_path, apricot_api):
    """Save response from a "dataset data insert" request to Wild Apricot."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    response = apricot_api.insert_dataset_data(dataset_id, SAMPLE_XIBO_EVENT_COLUMNS)
    save_response(response, module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_update_dataset_data_response(module_file_path, apricot_api):
    """Save response from a "dataset data update" request to Wild Apricot."""
    row_id = os.getenv("UPDATE_ROW_ID")
    if not row_id:
        pytest.skip("Environment variable UPDATE_ROW_ID is not defined")
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    response = apricot_api.update_dataset_data(dataset_id, row_id, SAMPLE_XIBO_EVENT_COLUMNS)
    save_response(response, module_file_path)

@pytest.mark.skip(reason="Not ready to test")
def test_get_paged_json_0(mocker):
    """Test getting 0 paged JSON results."""
    apricot_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_0)
    results = apricot_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_0
    apricot_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

@pytest.mark.skip(reason="Not ready to test")
def test_get_paged_json_1(mocker):
    """Test getting 1 paged JSON result."""
    apricot_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_1)
    results = apricot_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_1
    apricot_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

@pytest.mark.skip(reason="Not ready to test")
def test_get_paged_json_2(mocker):
    """Test getting 2 paged JSON results."""
    apricot_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_2)
    results = apricot_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_2
    apricot_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

@pytest.mark.skip(reason="Not ready to test")
def test_get_paged_json_3(mocker):
    """Test getting 3 paged JSON results, requiring two pages."""
    return_values = [SAMPLE_JSON_LIST_3, SAMPLE_JSON_LIST_0]
    expected_calls = [
        mocker.call(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH),
        mocker.call(SAMPLE_URL, start = SAMPLE_XIBO_PAGE_LENGTH, length = SAMPLE_XIBO_PAGE_LENGTH),
        ]
    apricot_api.get_json = mocker.Mock(side_effect = return_values)
    results = apricot_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_3
    assert apricot_api.get_json.call_args_list == expected_calls

@pytest.mark.skip(reason="Not ready to test")
def test_get_paged_json_4(mocker):
    """Test getting 4 paged JSON results, requiring two pages."""
    return_values = [SAMPLE_JSON_LIST_3, SAMPLE_JSON_LIST_1]
    expected_calls = [
        mocker.call(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH),
        mocker.call(SAMPLE_URL, start = SAMPLE_XIBO_PAGE_LENGTH, length = SAMPLE_XIBO_PAGE_LENGTH),
        ]
    apricot_api.get_json = mocker.Mock(side_effect = return_values)
    results = apricot_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_3 + SAMPLE_JSON_LIST_1
    assert apricot_api.get_json.call_args_list == expected_calls

    


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
