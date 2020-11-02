"""Provide event fields from a Meetup event JSON response."""

from datetime import datetime, timezone

# Meetup event JSON field names
DURATION_KEY = "duration"
FIND_US_KEY = "how_to_find_us"
MEETUP_ID_KEY = "id"
NAME_KEY = "name"
START_TIME_KEY = "time"
VENUE_KEY = "venue"
VENUE_NAME_KEY = "name"

# Default event length
THREE_HOURS_MSEC = 3 * 60 * 60 * 1000
DEFAULT_DURATION = THREE_HOURS_MSEC

class MeetupEvent:

    """Wraps a Meetup event JSON response."""

    def __init__(self, event_json):
        """Iniitialize with event JSON from Meetup."""
        self.event_json = event_json

    @property
    def meetup_id(self):
        """Return the meetup id."""
        return self.event_json[MEETUP_ID_KEY]

    @property
    def name(self):
        """Return the name."""
        return self.event_json[NAME_KEY]

    @property
    def start_time_epoch_ms(self):
        """Return the start time epoch ms."""
        return self.event_json[START_TIME_KEY]

    @property
    def start_time(self):
        """Return the start time."""
        return datetime.fromtimestamp(
                self.start_time_epoch_ms / 1000,
                tz=timezone.utc)

    @property
    def duration(self):
        """Return the duration."""
        return self.event_json.get(DURATION_KEY, DEFAULT_DURATION)

    @property
    def end_time(self):
        """Return the end time."""
        return datetime.fromtimestamp(
                (self.start_time_epoch_ms + self.duration) / 1000,
                tz=timezone.utc)

    @property
    def venue(self):
        """Return the venue."""
        return self.event_json.get(VENUE_KEY, {VENUE_NAME_KEY: ""})

    @property
    def venue_name(self):
        """Return the venue name."""
        return self.venue[VENUE_NAME_KEY]

    @property
    def find_us(self):
        """Return the find us."""
        return self.event_json.get(FIND_US_KEY, "")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
