"""Test starting an OAuth2 web session."""

from meetup2apricot.oauth2_session_starter import (
    Oauth2SessionStarter,
    Oauth2SessionStarterError,
)
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MissingTokenError
import logging
import os
import pytest


def test_create_session():
    """Test that an OAuth2 session is created."""
    starter = Oauth2SessionStarter(
        "a_client_id", "a_client_secret", "a_token_url", "a_user_agent", "auto"
    )
    session = starter.create_session()
    assert isinstance(session, OAuth2Session)


def test_set_user_agent():
    """Test that the user agent header is set."""
    starter = Oauth2SessionStarter(
        "a_client_id", "a_client_secret", "a_token_url", "a_user_agent"
    )
    session = starter.create_session()
    starter.set_user_agent(session)
    assert session.headers["user-agent"] == "a_user_agent"


def test_set_user_agent_none():
    """Test that the user agent header is set to something
    even if the OAuth2 session starter user agent is None."""
    starter = Oauth2SessionStarter(
        "a_client_id", "a_client_secret", "a_token_url", None
    )
    session = starter.create_session()
    starter.set_user_agent(session)
    assert session.headers["user-agent"] is not None


def test_authorize_session(mocker):
    """Test that a token is fetched to authorize a session."""
    mock_session = mocker.Mock()
    starter = Oauth2SessionStarter(
        "a_client_id", "a_client_secret", "a_token_url", "a_user_agent"
    )
    starter.authorize_session(mock_session)
    mock_session.assert_not_called()
    mock_session.fetch_token.assert_called_once_with(
        token_url="a_token_url",
        client_id="a_client_id",
        client_secret="a_client_secret",
    )


def test_authorize_session_no_token_error(mocker):
    """Test handling a missing token error when trying to authorize a session.."""
    mock_session = mocker.Mock()
    mock_session.fetch_token = mocker.Mock(
        side_effect=MissingTokenError("Missing access token parameter")
    )
    starter = Oauth2SessionStarter(
        "a_client_id", "a_client_secret", "a_token_url", "a_user_agent"
    )
    expected_message = (
        r"Cannot start OAuth2 session. "
        r"URL=a_token_url "
        r"problem=\(missing_token\) Missing access token parameter"
    )
    with pytest.raises(Oauth2SessionStarterError, match=expected_message):
        starter.authorize_session(mock_session)


@pytest.mark.skipif(
    not os.getenv("APRICOT_TOKEN_URL"),
    reason="environment variable APRICOT_TOKEN_URL needed to test live session",
)
@pytest.mark.skipif(
    not os.getenv("APRICOT_API_KEY"),
    reason="environment variable APRICOT_API_KEY needed to test live session",
)
def test_start_session(caplog):
    """Test that a session starts with a real token provider."""
    with caplog.at_level(logging.DEBUG):
        apricot_token_url = os.getenv("APRICOT_TOKEN_URL")
        apricot_api_key = os.getenv("APRICOT_API_KEY")
        starter = Oauth2SessionStarter(
            "APIKEY", apricot_api_key, apricot_token_url, "test_start_session", "auto"
        )
        session = starter.start_session()
        assert isinstance(session, OAuth2Session)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
