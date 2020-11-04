"""Provide event fields from a Meetup event JSON response."""

from datetime import datetime, timezone
from collections import namedtuple

# Meetup event JSON field names
DESCRIPTION_KEY = "description"
DURATION_KEY = "duration"
FIND_US_KEY = "how_to_find_us"
LINK_KEY = "link"
MEETUP_ID_KEY = "id"
NAME_KEY = "name"
RSVP_LIMIT_KEY = "rsvp_limit"
START_TIME_KEY = "time"
VENUE_KEY = "venue"
VENUE_NAME_KEY = "name"
VENUE_ADDRESS_KEY = "address_1"
VENUE_CITY_KEY = "city"
VENUE_STATE_KEY = "state"
VENUE_ZIPCODE_KEY = "zip"

# Default event length
THREE_HOURS_MSEC = 3 * 60 * 60 * 1000
DEFAULT_DURATION = THREE_HOURS_MSEC


MeetupVenue = namedtuple("MeetupVenue", "name address city state zipcode")


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
    def description(self):
        """Return the HTML description."""
        return self.event_json[DESCRIPTION_KEY]

    @property
    def link(self):
        """Return the link to the Meetup.com event."""
        return self.event_json[LINK_KEY]

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
        venue = self.event_json.get(VENUE_KEY, {})
        return MeetupVenue(
            name=venue.get(VENUE_NAME_KEY, ""),
            address=venue.get(VENUE_ADDRESS_KEY, ""),
            city=venue.get(VENUE_CITY_KEY, ""),
            state=venue.get(VENUE_STATE_KEY, ""),
            zipcode=venue.get(VENUE_ZIPCODE_KEY, ""))

    @property
    def find_us(self):
        """Return the find us."""
        return self.event_json.get(FIND_US_KEY, "")

    @property
    def rsvp_limit(self):
        """Return the maximum number of RSVPs allowed or None if unlimited."""
        return self.event_json.get(RSVP_LIMIT_KEY, None)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
