"""Test the photo retriever."""

from meetup2apricot.photo_retriever import PhotoRetriever, make_session
from pathlib import Path
import requests
import pytest

def test_assure_directory_exists(tmpdir):
    """Test assuring a directory that exists."""
    tmpdir_path = Path(tmpdir)
    file_path = tmpdir_path / "foo.bar"
    PhotoRetriever.assure_directory(file_path)
    assert tmpdir_path.is_dir()

def test_assure_directory_new(tmpdir):
    """Test assuring a new directory."""
    tmpdir_path = Path(tmpdir)
    file_path = tmpdir_path / "blat/foo.bar"
    PhotoRetriever.assure_directory(file_path)
    assert (tmpdir_path / "blat").is_dir()

def test_get(tmpdir, mocker):
    """Test getting and storing a file."""
    tmpdir_path = Path(tmpdir)
    file_path = tmpdir_path / "bar.txt"
    sample_url = "http://example.com/foo.txt"
    sample_bytes = bytes("Quick brown fox", 'utf-8') 
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
