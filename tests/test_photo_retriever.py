"""Test the photo retriever."""

from meetup2apricot.photo_retriever import PhotoRetriever, make_session
import requests


def test_assure_directory_exists(tmp_path):
    """Test assuring a directory that exists."""
    file_path = tmp_path / "foo.bar"
    PhotoRetriever.assure_directory(file_path)
    assert tmp_path.is_dir()


def test_assure_directory_new(tmp_path):
    """Test assuring a new directory."""
    file_path = tmp_path / "blat/foo.bar"
    PhotoRetriever.assure_directory(file_path)
    assert (tmp_path / "blat").is_dir()


def test_get(tmp_path, mocker):
    """Test getting and storing a file."""
    file_path = tmp_path / "bar.txt"
    sample_url = "http://example.com/foo.txt"
    sample_bytes = bytes("Quick brown fox", "utf-8")
    mock_response = mocker.Mock()
    mock_response.content = sample_bytes
    mock_session = mocker.Mock()
    mock_session.get = mocker.Mock(return_value=mock_response)
    photo_retriever = PhotoRetriever(mock_session)
    photo_retriever.get(sample_url, file_path)
    assert file_path.open("rb").read() == sample_bytes


def test_make_session():
    """Test making a session with a user agent."""
    session = make_session("foo")
    assert type(session) == requests.Session
    assert session.headers["User-Agent"] == "foo"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
