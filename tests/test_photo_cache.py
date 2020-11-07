"""Test the photo cache."""

from meetup2apricot.photo_cache import PhotoCache, make_photo_cache
from meetup2apricot.meetup_event import MeetupEvent
from datetime import datetime
from pathlib import Path, PurePosixPath, PosixPath
import pickle
import pytest

SAMPLE_DATE = datetime.fromisoformat("2020-11-09 18:30 -05:00")
SAMPLE_APRICOT_DIRECTORY = PurePosixPath("/resources/photos")
SAMPLE_LOCAL_DIRECTORY = Path("/var/tmp/photos")
INITIAL_CACHE = {
    None: None,
    "http://example.com/photo/1234.jpg": "/resources/mending.jpg"}

@pytest.fixture()
def mock_photo_retriever(mocker):
    """Mock a photo retriever, which implements a "get" method."""
    mock_photo_retriever = mocker.Mock()
    mock_photo_retriever.get = mocker.Mock()
    return mock_photo_retriever

@pytest.fixture()
def photo_cache(mock_photo_retriever):
    """Return a photo cache."""
    return PhotoCache(SAMPLE_LOCAL_DIRECTORY, SAMPLE_APRICOT_DIRECTORY,
        INITIAL_CACHE.copy(), mock_photo_retriever)

def test_apricot_photo_name_short():
    """Test converting a short Meetup name to a Wild Apricot photo name."""
    assert PhotoCache.apricot_photo_name("AC: Mending Monday", SAMPLE_DATE) == "AC_Mending_Monday_2020-11-09"

def test_apricot_photo_name_long():
    """Test converting a long Meetup name to a Wild Apricot photo name."""
    long_name = "WW_M: *Ladies only* Intro to the Woodshop & Yellow Tools Sign off"
    expected_name = "WW_M_Ladies_only_Intro_to_the_2020-11-09"
    assert PhotoCache.apricot_photo_name(long_name, SAMPLE_DATE) == expected_name

def test_apricot_photo_name_very_long():
    """Test converting a very long Meetup name to a Wild Apricot photo name."""
    long_name = "EL_M: Soldering Station 101 - Learn SMD soldering, desoldering, reflow Sign off"
    expected_name = "EL_M_Soldering_Station_101_2020-11-09"
    assert PhotoCache.apricot_photo_name(long_name, SAMPLE_DATE) == expected_name

def test_apricot_photo_file_name(free_meetup_event, photo_cache):
    """Test formatting a Wild Apricot photo file name for a Meetup event."""
    assert photo_cache.apricot_photo_file_name(free_meetup_event) == "TEST_ETL_AC_Mending_Monday_2020-11-09.jpeg"

def test_apricot_photo_path(photo_cache):
    """Test building a path to a Wild Apricot photo."""
    assert photo_cache.apricot_photo_path("photo.jpg") == PurePosixPath("/resources/photos/photo.jpg")

def test_local_photo_path(photo_cache):
    """Test building a path to a local photo."""
    assert photo_cache.local_photo_path("photo.jpg") == Path("/var/tmp/photos/photo.jpg")

def test_cache_photo_none(photo_cache, paid_meetup_event, mock_photo_retriever):
    """Test caching the photo for a later Meetup event without a photo."""
    assert photo_cache.cache_photo(paid_meetup_event) == None
    mock_photo_retriever.get.assert_not_called()

def test_cache_photo_later(photo_cache, later_free_meetup_event, mock_photo_retriever):
    """Test caching the photo for a later Meetup event."""
    expected_apricot_path = PurePosixPath("/resources/photos/TEST_ETL_AC_Mending_Monday_2020-11-16.jpeg")
    expected_local_path = PosixPath('/var/tmp/photos/TEST_ETL_AC_Mending_Monday_2020-11-16.jpeg')
    assert photo_cache.cache_photo(later_free_meetup_event) == expected_apricot_path
    mock_photo_retriever.get.assert_called_once_with(later_free_meetup_event.photo_url, expected_local_path)

def test_cache_photo_share(photo_cache, free_meetup_event, later_free_meetup_event, mock_photo_retriever):
    """Test caching the photos for Meetup events that share photos."""
    expected_apricot_path = PurePosixPath("/resources/photos/TEST_ETL_AC_Mending_Monday_2020-11-09.jpeg")
    expected_local_path = PosixPath('/var/tmp/photos/TEST_ETL_AC_Mending_Monday_2020-11-09.jpeg')
    assert photo_cache.cache_photo(free_meetup_event) == expected_apricot_path
    assert photo_cache.cache_photo(later_free_meetup_event) == expected_apricot_path
    mock_photo_retriever.get.assert_called_once_with(later_free_meetup_event.photo_url, expected_local_path)

def test_persist(photo_cache, tmp_path):
    """Test persisting the photo cache."""
    data_path = tmp_path / "photo_cache.pickle"
    photo_cache.persist(data_path)
    with data_path.open('rb') as data_file:
        cached_data = pickle.load(data_file)
    assert cached_data == INITIAL_CACHE

def test_make_photo_cache(tmp_path, photo_cache, mock_photo_retriever):
    """Test making a photo cache from cached data."""
    data_path = tmp_path / "photo_cache.pickle"
    photo_cache.persist(data_path)
    another_photo_cache = make_photo_cache(
        data_path,
        tmp_path,
        SAMPLE_APRICOT_DIRECTORY,
        mock_photo_retriever)
    assert another_photo_cache.urls_to_paths == INITIAL_CACHE
    assert another_photo_cache.local_directory == tmp_path
    assert another_photo_cache.apricot_directory == SAMPLE_APRICOT_DIRECTORY
    assert another_photo_cache.photo_retriever == mock_photo_retriever

def test_make_photo_cache_new_dir(tmp_path, photo_cache, mock_photo_retriever):
    """Test creating a new photo directory while making a photo cache from
    cached data."""
    data_path = tmp_path / "photo_cache.pickle"
    local_photo_directory = tmp_path / "photos"
    photo_cache.persist(data_path)
    another_photo_cache = make_photo_cache(
        data_path,
        local_photo_directory,
        SAMPLE_APRICOT_DIRECTORY,
        mock_photo_retriever)
    assert local_photo_directory.is_dir()

def test_make_photo_cache_no_prior(tmp_path, mock_photo_retriever):
    """Test making a photo cache with no prior cached data."""
    data_path = tmp_path / "photo_cache.pickle"
    another_photo_cache = make_photo_cache(
        data_path,
        tmp_path,
        SAMPLE_APRICOT_DIRECTORY,
        mock_photo_retriever)
    assert another_photo_cache.urls_to_paths == {None: None}
    assert another_photo_cache.local_directory == tmp_path
    assert another_photo_cache.apricot_directory == SAMPLE_APRICOT_DIRECTORY
    assert another_photo_cache.photo_retriever == mock_photo_retriever

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
