"""Test the photo cache."""

from meetup2apricot.photo_cache import PhotoCache, load_cached_photo_urls
from meetup2apricot.reporter import NullReporter
from datetime import datetime
from pathlib import Path, PurePosixPath, PosixPath
import pickle
import pytest

SAMPLE_DATE = datetime.fromisoformat("2020-11-09 18:30 -05:00")
SAMPLE_APRICOT_DIRECTORY = PurePosixPath("/resources/photos")
CACHE_FILE_NAME = "photo_cache.pickle"
INITIAL_CACHE = {
    None: None,
    "http://example.com/photo/1234.jpg": "/resources/mending.jpg",
}


@pytest.fixture()
def mock_photo_retriever(mocker):
    """Mock a photo retriever, which implements a "get" method."""
    mock_photo_retriever = mocker.Mock()
    mock_photo_retriever.get = mocker.Mock()
    return mock_photo_retriever

@pytest.fixture()
def mock_photo_uploader(mocker):
    """Mock a photo uploader, which implements an "upload_photo" method."""
    mock_photo_uploader = mocker.Mock()
    mock_photo_uploader.upload_photo = mocker.Mock()
    return mock_photo_uploader


@pytest.fixture()
def photo_cache(mock_photo_retriever, tmp_path):
    """Return a photo cache."""
    return PhotoCache(
        apricot_directory=SAMPLE_APRICOT_DIRECTORY,
        urls_to_paths=INITIAL_CACHE.copy(),
        photo_retriever=mock_photo_retriever,
        photo_uploader=mock_photo_uploader,
        cache_path=tmp_path / CACHE_FILE_NAME,
        reporter=NullReporter(),
    )


def test_apricot_photo_name_short():
    """Test converting a short Meetup name to a Wild Apricot photo name."""
    assert (
        PhotoCache.apricot_photo_name("AC: Mending Monday", SAMPLE_DATE)
        == "AC_Mending_Monday_2020-11-09"
    )


def test_apricot_photo_name_long():
    """Test converting a long Meetup name to a Wild Apricot photo name."""
    long_name = "WW_M: *Ladies only* Intro to the Woodshop & Yellow Tools Sign off"
    expected_name = "WW_M_Ladies_only_Intro_to_the_2020-11-09"
    assert PhotoCache.apricot_photo_name(long_name, SAMPLE_DATE) == expected_name


def test_apricot_photo_name_very_long():
    """Test converting a very long Meetup name to a Wild Apricot photo name."""
    long_name = (
        "EL_M: Soldering Station 101 - Learn SMD soldering, "
        "desoldering, reflow Sign off"
    )
    expected_name = "EL_M_Soldering_Station_101_2020-11-09"
    assert PhotoCache.apricot_photo_name(long_name, SAMPLE_DATE) == expected_name


def test_apricot_photo_file_name(free_meetup_event, photo_cache):
    """Test formatting a Wild Apricot photo file name for a Meetup event."""
    assert (
        photo_cache.apricot_photo_file_name(free_meetup_event)
        == "AC_Mending_Monday_Test_Event_2020-11-09.jpeg"
    )


def test_apricot_photo_path(photo_cache):
    """Test building a path to a Wild Apricot photo."""
    assert photo_cache.apricot_photo_path("photo.jpg") == PurePosixPath(
        "/resources/photos/photo.jpg"
    )


def test_cache_photo_none(photo_cache, paid_meetup_event, mock_photo_retriever):
    """Test caching the photo for a later Meetup event without a photo."""
    assert photo_cache.cache_photo(paid_meetup_event) is None
    mock_photo_retriever.get.assert_not_called()


def test_cache_photo_later(
    photo_cache, later_free_meetup_event, mock_photo_retriever, mocker
):
    """Test caching the photo for a later Meetup event."""
    expected_apricot_path = PurePosixPath(
        "/resources/photos/AC_Mending_Monday_Test_Event_2020-11-16.jpeg"
    )
    expected_photo_name = "AC_Mending_Monday_Test_Event_2020-11-16.jpeg"

    mock_photo_retriever.get = mocker.Mock(return_value=expected_photo_name)
    assert photo_cache.cache_photo(later_free_meetup_event) == expected_apricot_path
    mock_photo_retriever.get.assert_called_once_with(
        later_free_meetup_event.photo_url, expected_photo_name
    )


def test_cache_photo_share(
    photo_cache,
    free_meetup_event,
    later_free_meetup_event,
    mock_photo_retriever,
    mocker,
):
    """Test caching the photos for Meetup events that share photos."""
    expected_apricot_path = PurePosixPath(
        "/resources/photos/AC_Mending_Monday_Test_Event_2020-11-09.jpeg"
    )
    expected_photo_name = "AC_Mending_Monday_Test_Event_2020-11-09.jpeg"

    mock_photo_retriever.get = mocker.Mock(return_value=expected_photo_name)
    assert photo_cache.cache_photo(free_meetup_event) == expected_apricot_path
    assert photo_cache.cache_photo(later_free_meetup_event) == expected_apricot_path
    mock_photo_retriever.get.assert_called_once_with(
        later_free_meetup_event.photo_url, expected_photo_name
    )


def test_persist(photo_cache, tmp_path):
    """Test persisting the photo cache."""
    photo_cache.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    with data_path.open("rb") as data_file:
        cached_data = pickle.load(data_file)
    assert cached_data == INITIAL_CACHE


def test_load_cached_photo_urls(photo_cache, tmp_path):
    """Test loading cached photo data."""
    photo_cache.persist()
    data_path = tmp_path / CACHE_FILE_NAME
    urls_to_paths = load_cached_photo_urls(data_path)
    assert urls_to_paths == INITIAL_CACHE


def test_load_cached_photo_urls_no_prior(tmp_path):
    """Test loading cached data with no prior cached data."""
    data_path = tmp_path / CACHE_FILE_NAME
    urls_to_paths = load_cached_photo_urls(data_path)
    assert urls_to_paths == {None: None}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
