"""Test fixtures."""

from meetup2apricot.oauth2_session_starter import Oauth2SessionStarter
from meetup2apricot.meetup_event import MeetupEvent
from meetup2apricot.event_tagger import EventTagger
from pathlib import Path
from .sample_meetup_json import FREE_MEETUP_EVENT_JSON, PAID_MEETUP_EVENT_JSON
from .sample_codes_to_tags import SAMPLE_CODES_TO_TAGS
from .sample_apricot_json import EXPECTED_TAGS
import os
import json
import pytest

ONE_DAY_MS = 24 * 60 * 60 * 1000
ONE_WEEK_MS = 7 * ONE_DAY_MS
ONE_YEAR_MS = 365 * ONE_DAY_MS


@pytest.fixture(scope="module")
def module_dir_path(request):
    """Assure a directory exists in this module.
    The directory name is given by the environment variable
    combining the module name and "_DIR".  For example,
    module test_foo.py will use the environment variable
    named TEST_FOO_DIR.  Return the path to the directory
    or None if the environment variable is not set."""
    module_file_path = Path(request.module.__file__)
    env_var_name = "{}_{}".format(module_file_path.stem, "DIR").upper()
    module_dir_name = os.environ.get(env_var_name)
    if not module_dir_name:
        return None
    test_dir = module_file_path.parent
    module_dir = test_dir / module_dir_name
    module_dir.mkdir(mode=0o775, exist_ok=True)
    return module_dir


@pytest.fixture()
def module_file_path(request, module_dir_path):
    """Return a path in the module's directory to a file
    named for the test function.  Skip the test if there
    is no module directory."""
    if module_dir_path is None:
        pytest.skip("No module directory for this test")
    test_name = request.function.__name__
    return module_dir_path / test_name


@pytest.fixture(scope="module")
def optional_apricot_session():
    """Return an authorized Wild Apricot API web session configured with
    environment variables. If any variables are undefined, return None."""
    apricot_token_url = os.getenv("APRICOT_TOKEN_URL")
    apricot_api_key = os.getenv("APRICOT_API_KEY")
    if None in [apricot_token_url, apricot_api_key]:
        return None
    starter = Oauth2SessionStarter(
        "APIKEY", apricot_api_key, apricot_token_url, "test_apricot_api", "auto"
    )
    return starter.start_session()


@pytest.fixture()
def apricot_session(optional_apricot_session):
    """Return an authorized Wild Apricot API web session configured with
    environment variables. If any variables are undefined, skip
    the test."""
    if not optional_apricot_session:
        pytest.skip(
            "Wild Apricot environment variables APRICOT_TOKEN_URL "
            "and APRICOT_API_KEY must be defined."
        )
    return optional_apricot_session


@pytest.fixture(scope="session")
def free_meetup_event_json():
    return json.loads(FREE_MEETUP_EVENT_JSON)


@pytest.fixture(scope="session")
def later_free_meetup_event_json(free_meetup_event_json):
    one_week_later = free_meetup_event_json["time"] + ONE_WEEK_MS
    return free_meetup_event_json | {"time": one_week_later}

@pytest.fixture(scope="session")
def much_later_free_meetup_event_json(free_meetup_event_json):
    one_year_later = free_meetup_event_json["time"] + ONE_YEAR_MS
    return free_meetup_event_json | {"time": one_year_later}


@pytest.fixture(scope="session")
def paid_meetup_event_json():
    return json.loads(PAID_MEETUP_EVENT_JSON)


@pytest.fixture()
def free_meetup_event(free_meetup_event_json):
    return MeetupEvent(free_meetup_event_json)


@pytest.fixture()
def later_free_meetup_event(later_free_meetup_event_json):
    return MeetupEvent(later_free_meetup_event_json)

@pytest.fixture()
def much_later_free_meetup_event(much_later_free_meetup_event_json):
    return MeetupEvent(much_later_free_meetup_event_json)


@pytest.fixture()
def paid_meetup_event(paid_meetup_event_json):
    return MeetupEvent(paid_meetup_event_json)


@pytest.fixture()
def event_tagger():
    return EventTagger(SAMPLE_CODES_TO_TAGS, EXPECTED_TAGS)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
