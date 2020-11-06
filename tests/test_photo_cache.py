"""Test the photo cache."""

from meetup2apricot.photo_cache import PhotoCache
from datetime import datetime
import pytest

SAMPLE_DATE = datetime.fromisoformat("2020-11-09 18:30 -05:00")

def test_name_for_apricot_short():
    """Test converting a short Meetup name to a Wild Apricot photo name."""
    assert PhotoCache.name_for_apricot("AC: Mending Monday", SAMPLE_DATE) == "AC_Mending_Monday_2020-11-09"

def test_name_for_apricot_long():
    """Test converting a long Meetup name to a Wild Apricot photo name."""
    long_name = "WW_M: *Ladies only* Intro to the Woodshop & Yellow Tools Sign off"
    expected_name = "WW_M_Ladies_only_Intro_to_the_2020-11-09"
    assert PhotoCache.name_for_apricot(long_name, SAMPLE_DATE) == expected_name

def test_name_for_apricot_very_long():
    """Test converting a very long Meetup name to a Wild Apricot photo name."""
    long_name = "EL_M: Soldering Station 101 - Learn SMD soldering, desoldering, reflow Sign off"
    expected_name = "EL_M_Soldering_Station_101_2020-11-09"
    assert PhotoCache.name_for_apricot(long_name, SAMPLE_DATE) == expected_name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
