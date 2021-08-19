"""Test the photo uploader."""
from meetup2apricot.photo_uploader import PhotoUploader, make_photo_uploader_session
from meetup2apricot.http_response_error import PhotoUploadError
from pathlib import Path, PurePosixPath
import inspect
import logging
import os
import requests
from requests.auth import HTTPDigestAuth
import shutil
import pytest

SAMPLE_PNG_FILENAME = "dot.png"
SAMPLE_MISSING_PHOTO_FILENAME = "foo.ppng"
SAMPLE_APRICOT_DIRECTORY = "/resource/photos"
SAMPLE_APRICOT_DIRECTORY_PATH = PurePosixPath(SAMPLE_APRICOT_DIRECTORY)
SAMPLE_BASE_URL = "https://apricot.com"
EXPECTED_APRICOT_PHOTO_PATH = SAMPLE_APRICOT_DIRECTORY_PATH / SAMPLE_PNG_FILENAME
EXPECTED_URL = SAMPLE_BASE_URL + str(EXPECTED_APRICOT_PHOTO_PATH)


@pytest.fixture()
def testcase_dir_path():
    """Return the path to the directory containing tests and test dat files."""
    return Path(inspect.getsourcefile(test_upload_photo)).parent


@pytest.fixture()
def sample_photo_path(testcase_dir_path):
    """Return the path to a sample image file."""
    return testcase_dir_path / SAMPLE_PNG_FILENAME


def test_upload_photo(testcase_dir_path, sample_photo_path, mocker):
    """Test uploading a photo."""
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock
    mock_session = mocker.Mock()
    mock_session.put = mocker.Mock(return_value=mock_response)
    photo_uploader = PhotoUploader(
        local_directory=testcase_dir_path,
        apricot_base_url=SAMPLE_BASE_URL,
        apricot_directory=SAMPLE_APRICOT_DIRECTORY_PATH,
        session=mock_session,
    )
    apricot_photo_path = photo_uploader.upload_photo(SAMPLE_PNG_FILENAME)
    assert apricot_photo_path == EXPECTED_APRICOT_PHOTO_PATH
    mock_session.put.assert_called_once()
    (url,) = mock_session.put.call_args.args
    assert url == EXPECTED_URL
    kwargs = mock_session.put.call_args.kwargs
    open_file = kwargs["data"]
    assert open_file.read() == open(sample_photo_path, "rb").read()
    headers = kwargs["headers"]
    assert headers == {"Content-type": "image/png"}


def test_upload_photo_cannot_open(testcase_dir_path, sample_photo_path, mocker):
    """Test uploading a photo that cannot be opened."""
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock
    mock_session = mocker.Mock()
    mock_session.put = mocker.Mock(return_value=mock_response)
    photo_uploader = PhotoUploader(
        local_directory=testcase_dir_path,
        apricot_base_url=SAMPLE_BASE_URL,
        apricot_directory=SAMPLE_APRICOT_DIRECTORY_PATH,
        session=mock_session,
    )
    with pytest.raises(PhotoUploadError):
        apricot_photo_path = photo_uploader.upload_photo(SAMPLE_MISSING_PHOTO_FILENAME)


def test_make_photo_uploader_session():
    """Test making a photo uploader session."""
    session = make_photo_uploader_session(
        username="foo", password="bar", user_agent="blat"
    )
    assert type(session) == requests.Session
    assert session.auth == HTTPDigestAuth("foo", "bar")
    assert session.headers["User-Agent"] == "blat"


# These tests save data to Wild Apricot to aid development.
# Provide required environment variables to run these tests.


def test_upload_photo_to_wild_apricot(testcase_dir_path, sample_photo_path, caplog):
    """Test uploading a photo to Wild Apricot."""
    caplog.set_level(logging.INFO)
    apricot_photo_username = os.getenv("APRICOT_PHOTO_USERNAME")
    apricot_photo_password = os.getenv("APRICOT_PHOTO_PASSWORD")
    apricot_photo_base_url = os.getenv("APRICOT_PHOTO_BASE_URL")
    apricot_photo_directory = os.getenv("APRICOT_PHOTO_DIRECTORY")
    if not (
        apricot_photo_username
        and apricot_photo_password
        and apricot_photo_base_url
        and apricot_photo_directory
    ):
        pytest.skip(
            "Wild Apricot environment variables APRICOT_PHOTO_USERNAME, "
            "APRICOT_PHOTO_PASSWORD, APRICOT_PHOTO_BASE_URL, and "
            "APRICOT_PHOTO_DIRECTORY must be defined."
        )
    session = make_photo_uploader_session(
        apricot_photo_username, apricot_photo_password, "test_photo_uploader"
    )
    photo_uploader = PhotoUploader(
        local_directory=testcase_dir_path,
        apricot_base_url=apricot_photo_base_url,
        apricot_directory=PurePosixPath(apricot_photo_directory),
        session=session,
    )
    photo_uploader.upload_photo(SAMPLE_PNG_FILENAME)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
