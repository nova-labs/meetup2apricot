"""Test the photo cache."""

from meetup2apricot.photo_cache import PhotoCache
from meetup2apricot.meetup_event import MeetupEvent
from datetime import datetime
from pathlib import Path, PurePosixPath
import pytest

SAMPLE_DATE = datetime.fromisoformat("2020-11-09 18:30 -05:00")
SAMPLE_APRICOT_DIRECTORY = PurePosixPath("/resources/photos")
SAMPLE_LOCAL_DIRECTORY = Path("/var/tmp/photos")

@pytest.fixture()
def photo_cache():
    """Return a photo cache."""
    return PhotoCache(SAMPLE_LOCAL_DIRECTORY, SAMPLE_APRICOT_DIRECTORY)

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

def test_apricot_photo_file_name(free_meetup_event_json, photo_cache):
    """Test formatting a Wild Apricot photo file name for a Meetup event."""
    meetup_event = MeetupEvent(free_meetup_event_json)
    assert photo_cache.apricot_photo_file_name(meetup_event) == "TEST_ETL_AC_Mending_Monday_2020-11-09.jpeg"

def test_apricot_photo_path(photo_cache):
    """Test building a path to a Wild Apricot photo."""
    assert photo_cache.apricot_photo_path("photo.jpg") == PurePosixPath("/resources/photos/photo.jpg")

def test_local_photo_path(photo_cache):
    """Test building a path to a local photo."""
    assert photo_cache.local_photo_path("photo.jpg") == Path("/var/tmp/photos/photo.jpg")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
