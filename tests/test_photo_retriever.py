"""Test the photo retriever."""

from meetup2apricot.photo_retriever import (
    PhotoRetriever,
    make_photo_retriever,
    make_session,
)
import requests


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


def test_get(tmp_path, mocker):
    """Test getting and storing a file."""
    file_path = tmp_path / "bar.txt"
    sample_url = "http://example.com/foo.txt"
    sample_bytes = bytes("Quick brown fox", "utf-8")
    mock_response = mocker.Mock()
    mock_response.content = sample_bytes
    mock_session = mocker.Mock()
    mock_session.get = mocker.Mock(return_value=mock_response)
    photo_retriever = PhotoRetriever(tmp_path, mock_session)
    photo_retriever.get(sample_url, file_path)
    assert file_path.open("rb").read() == sample_bytes


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
