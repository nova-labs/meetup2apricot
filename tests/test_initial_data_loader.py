"""Test the initial data loader."""

from meetup2apricot.initial_data_loader import InitialDataLoader
from .sample_apricot_json import SAMPLE_MEMBERSHIP_LEVEL_JSON
import pytest


@pytest.fixture()
def mock_apricot_api(mocker):
    """Return a mock Wild Apricot API, which should be augmented for each test."""
    return mocker.Mock()


@pytest.fixture()
def mock_meetup_api(mocker):
    """Return a mock meetup API, which should be augmented for each test."""
    return mocker.Mock()


@pytest.fixture()
def initial_data_loader(mock_apricot_api, mock_meetup_api):
    """Return an initial data loader with mock APIs and no support functions."""
    return InitialDataLoader(
        meetup_api=mock_meetup_api,
        apricot_api=mock_apricot_api,
        event_mapping_provider=None,
        photo_urls_provider=None,
        enter_initial_data_scope=None,
    )


@pytest.mark.skip("interface changed")
def test_retrieve_membership_levels(initial_data_loader, mock_apricot_api, mocker):
    """Test retrieving a list of membership levels."""
    mock_apricot_api.get_membership_levels = mocker.Mock(
        return_value=SAMPLE_MEMBERSHIP_LEVEL_JSON
    )
    expected_levels = [
        {
            "Id": 1206421,
            "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206421",
        },
        {
            "Id": 1206426,
            "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206426",
        },
        {
            "Id": 1207614,
            "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1207614",
        },
    ]
    levels = initial_data_loader.retrieve_membership_levels()
    assert levels == expected_levels
    assert mock_apricot_api.get_membership_levels.called_once_with()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
