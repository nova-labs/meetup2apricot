"""Test the photo retriever."""

from meetup2apricot.photo_retriever import (
    PhotoRetriever,
    make_photo_retriever,
    make_session,
)
from pathlib import Path
import inspect
import requests
import shutil
import pytest

SAMPLE_PHOTO_FILENAME = "dot.png"


@pytest.fixture()
def sample_photo_path():
    """Return the path to a sample image file."""
    test_file_path = Path(inspect.getsourcefile(test_assure_directory_exists))
    return test_file_path.parent / SAMPLE_PHOTO_FILENAME


def test_assure_directory_exists(tmp_path):
    """Test assuring a directory that exists."""
    photo_retriever = PhotoRetriever(tmp_path, None)
    photo_retriever.assure_local_directory()
    assert tmp_path.is_dir()


def test_assure_directory_new(tmp_path):
    """Test assuring a new directory."""
    dir_path = tmp_path / "blat"
    photo_retriever = PhotoRetriever(dir_path, None)
    photo_retriever.assure_local_directory()
    assert dir_path.is_dir()


def test_get(tmp_path, sample_photo_path, mocker):
    """Test getting and storing a file."""
    sample_url = "http://example.com/foo.txt"
    sample_bytes = sample_photo_path.open("rb").read()
    mock_response = mocker.Mock()
    mock_response.content = sample_bytes
    mock_session = mocker.Mock()
    mock_session.get = mocker.Mock(return_value=mock_response)
    photo_retriever = PhotoRetriever(tmp_path, mock_session)
    assert photo_retriever.get(sample_url, "foo.jpg") == "foo.png"
    assert (tmp_path / "foo.png").open("rb").read() == sample_bytes


def test_retrieve_photo(tmp_path, mocker):
    """Test retrieving and storing a file."""
    file_path = tmp_path / "bar.txt"
    sample_url = "http://example.com/foo.txt"
    sample_bytes = bytes("Quick brown fox", "utf-8")
    mock_response = mocker.Mock()
    mock_response.content = sample_bytes
    mock_session = mocker.Mock()
    mock_session.get = mocker.Mock(return_value=mock_response)
    photo_retriever = PhotoRetriever(tmp_path, mock_session)
    photo_retriever.retrieve_photo(sample_url, file_path)
    assert file_path.open("rb").read() == sample_bytes


@pytest.mark.parametrize(
    "proposed_photo_name,corrected_photo_name",
    [
        ("foo.png", "foo.png"),
        ("bar.jpg", "bar.png"),
    ],
)
def test_adjust_extension(
    proposed_photo_name, corrected_photo_name, tmp_path, sample_photo_path
):
    """Test adjusting the extension of a photo with the correct file
    extension."""
    working_photo_path = tmp_path / proposed_photo_name
    expected_photo_path = tmp_path / corrected_photo_name
    shutil.copyfile(sample_photo_path, working_photo_path)
    photo_retriever = PhotoRetriever(tmp_path, None, False)
    corrected_path = photo_retriever.adjust_extension(working_photo_path)
    assert corrected_path == expected_photo_path


def test_make_photo_retriever(tmp_path, mocker):
    """Test making a photo retriever with a new local directory."""
    dir_path = tmp_path / "foo"
    mock_session = mocker.Mock()
    photo_retriever = make_photo_retriever(dir_path, mock_session, True)
    assert dir_path.is_dir()
    assert photo_retriever.session == mock_session
    assert photo_retriever.dryrun


def test_make_session():
    """Test making a session with a user agent."""
    session = make_session("foo")
    assert type(session) == requests.Session
    assert session.headers["User-Agent"] == "foo"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
