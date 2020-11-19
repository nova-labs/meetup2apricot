"""Process Meetup events by creating and uploading Wild Apricot events, by
downloading Meetup photos for manual uploading to Wild Apricot, and by tracking
events and photos already seen."""

from . import dryrun
from .meetup_to_apricot_event_adaptor import MeetupToApricotEventAdaptor
import pickle
import logging


class EventProcessor:

    """Processes Meetup events into Wild Apricot events."""

    logger = logging.getLogger("EventProcessor")

    def __init__(
        self,
        earliest_start_time,
        latest_start_time,
        known_events,
        photo_cache,
        event_registration_type_maker,
        apricot_api,
        cache_path,
        event_tagger,
        dryrun=False,
    ):
        """Initialize with the earliest and latest event start times, a
        dictionary of previously processed known events (indexed by Meetup
        event ID), a photo cache, an event registration type maker, a Wild
        Apricot API interface, a path to the cache file; an event tagger, and a
        dry run flag."""
        self.earliest_start_time = earliest_start_time
        self.latest_start_time = latest_start_time
        self.known_events = known_events
        self.photo_cache = photo_cache
        self.event_registration_type_maker = event_registration_type_maker
        self.apricot_api = apricot_api
        self.cache_path = cache_path
        self.event_tagger = event_tagger
        self.dryrun = dryrun

    def process(self, meetup_event):
        """Process a meetup event."""
        if self.can_ignore_event(meetup_event):
            return
        photo_path = self.get_photo(meetup_event)
        event_tags = self.get_event_tags(meetup_event)
        apricot_event_id = self.add_apricot_event(meetup_event, photo_path, event_tags)
        self.add_event_registration_types(meetup_event, apricot_event_id)
        self.record_event(meetup_event, apricot_event_id)

    def can_ignore_event(self, meetup_event):
        """Return true if a Meetup event can be ignored; false otherwise."""
        return (
            meetup_event.start_time < self.earliest_start_time
            or meetup_event.start_time > self.latest_start_time
            or meetup_event.meetup_id in self.known_events
        )

    def get_photo(self, meetup_event):
        """Get an available photo for a meetup event, if it hasn't been
        downloaded before.  Return the photo path if it was ever downloaded or
        None."""
        return self.photo_cache.cache_photo(meetup_event)

    def get_event_tags(self, meetup_event):
        """Get Wild Apricot event tags for a meetup event."""
        return self.event_tagger.tag_event(meetup_event)

    def add_apricot_event(self, meetup_event, photo_path, event_tags):
        """Add the event to Wild Apricot."""
        apricot_event = MeetupToApricotEventAdaptor(
            meetup_event, photo_path, event_tags
        )
        apricot_event_json = apricot_event.for_json()
        apricot_event_id = self.apricot_api.add_event(apricot_event_json)
        self.logger.info(
            "add_apricot_event: meetup_id=%s apricot_id=%d title=%r start_time=%s",
            meetup_event.meetup_id,
            apricot_event_id,
            meetup_event.name,
            meetup_event.start_time,
        )
        return apricot_event_id

    def add_event_registration_types(self, meetup_event, apricot_event_id):
        """Add event registration types for a Wild Apricot event based on a
        Meetup event."""
        reg_types = self.choose_registration_types(meetup_event, apricot_event_id)
        for reg_type in reg_types:
            self.apricot_api.add_registration_type(reg_type.for_json())
            self.log_add_event_registration_type(apricot_event_id, reg_type)

    def choose_registration_types(self, meetup_event, apricot_event_id):
        """Choose event registration types for a Wild Apricot event based on a
        Meetup event."""
        meetup_count = meetup_event.yes_rsvp_count
        if meetup_event.rsvp_limit:
            apricot_count = meetup_event.rsvp_limit - meetup_count
        else:
            apricot_count = None
        return [
            self.event_registration_type_maker.make_meetup_registration_type(
                apricot_event_id, meetup_event.yes_rsvp_count
            ),
            self.event_registration_type_maker.make_apricot_registration_type(
                apricot_event_id, apricot_count, meetup_event.fee_amount
            ),
        ]

    def log_add_event_registration_type(self, apricot_event_id, reg_type):
        """Log adding an event registration type for a Wild Apricot event."""
        if reg_type.maximum_registrants_count is None:
            display_count = "unlimited"
        else:
            display_count = f"{reg_type.maximum_registrants_count:d}"
        self.logger.info(
            "add_event_registration_types: apricot_id=%d "
            "maximum_registrants_count=%s price=%.2f name=%r",
            apricot_event_id,
            display_count,
            reg_type.price,
            reg_type.name,
        )

    def record_event(self, meetup_event, apricot_event_id):
        """Record the known event to ignore in the future."""
        self.known_events[meetup_event.meetup_id] = {
            "wild_apricot_event": apricot_event_id,
            "start_time": meetup_event.start_time,
        }

    @dryrun.method()
    def persist(self):
        """Persist cache to a file."""
        with self.cache_path.open("wb") as f:
            pickle.dump(self.known_events, f)


def load_cached_event_mapping(cache_path):
    """Return a mapping of Meetup event IDs to Wild Apricot event details,
    either loaded from a cache file or initialized to a default."""
    if cache_path.exists():
        with cache_path.open("rb") as f:
            return pickle.load(f)
    else:
        return {}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
