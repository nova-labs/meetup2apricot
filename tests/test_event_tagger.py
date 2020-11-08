"""Test the event tagger."""

from meetup2apricot.event_tagger import EventTagger
from .sample_apricot_json import EXPECTED_TAGS, EXPECTED_FREE_TAGS
from .sample_codes_to_tags import SAMPLE_CODES_TO_TAGS
import pytest

@pytest.fixture()
def event_tagger():
   return EventTagger(SAMPLE_CODES_TO_TAGS, EXPECTED_TAGS)

def test_tag_code_none(event_tagger):
    """Test tagging a missing accounting code."""
    assert event_tagger.tag_code(None) == EXPECTED_TAGS

def test_tag_code_one(event_tagger):
    """Test tagging a code with one tag."""
    assert event_tagger.tag_code("AV") == ["audio-visual"] + EXPECTED_TAGS

def test_tag_code_multiple(event_tagger):
    """Test tagging a code with multiple tags."""
    assert event_tagger.tag_code("AC") == ["arts-and-crafts", "the-studio"] + EXPECTED_TAGS

def test_tag_code_unknown(event_tagger):
    """Test tagging an unknown accounting code."""
    assert event_tagger.tag_code("XY") == EXPECTED_TAGS

def test_tag_event(event_tagger, free_meetup_event):
    """Test tagging an event."""
    assert event_tagger.tag_event(free_meetup_event) == EXPECTED_FREE_TAGS

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
