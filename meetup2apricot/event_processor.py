"""Process Meetup events by creating and uploading Wild Apricot events, by
downloading Meetup photos for manual uploading to Wild Apricot, and by tracking
events and photos already seen."""

from .meetup_to_apricot_event_adaptor import MeetupToApricotEventAdaptor
import pickle

class EventProcessor:

    """Processes Meetup events into Wild Apricot events."""

    def __init__(self, cutoff_time, known_events, photo_cache, apricot_api):
        """Initialize with a cutoff time, a datetime before which events will
        be ignored; a dictionary of previously processed known events (indexed
        by Meetup event ID); a photo cache; and a Wild Apricot API
        interface."""
        self.cutoff_time = cutoff_time
        self.known_events = known_events
        self.photo_cache = photo_cache
        self.apricot_api = apricot_api

    def process(self, meetup_event):
        """Process a meetup event."""
        if self.can_ignore_event(meetup_event):
            return
        photo_name = self.get_photo(meetup_event)
        apricot_event_id = self.add_apricot_event(meetup_event, photo_name)
        self.record_event(meetup_event, apricot_event_id)

    def can_ignore_event(self, meetup_event):
        """Return true if a Meetup event can be ignored; false otherwise."""
        return meetup_event.start_time < self.cutoff_time \
            or meetup_event.meetup_id in self.known_events

    def get_photo(self, meetup_event):
        """Get an available photo for a meetup event, if it hasn't been
        downloaded before.  Return the photo name if it was ever downloaded or
        None."""
        return self.photo_cache.cache_photo(meetup_event)

    def add_apricot_event(self, meetup_event, photo_name):
        """Add the event to Wild Apricot."""
        apricot_event = MeetupToApricotEventAdaptor(meetup_event, photo_name)
        apricot_event_json = apricot_event.for_json()
        return self.apricot_api.add_event(apricot_event_json)

    def record_event(self, meetup_event, apricot_event_id):
        """Record the known event to ignore in the future."""
        self.known_events[meetup_event.meetup_id] = {
            "wild_apricot_event": apricot_event_id,
            "start_time": meetup_event.start_time
            }

    def persist(self, path):
        """Persist cache to a file."""
        with path.open("wb") as f:
            pickle.dump(self.known_events, f)


def make_event_processor(cache_path, cutoff_time, photo_cache, apricot_api):
    """Initialize with a file caching a dictionary of previously processed
    known events (indexed by Meetup event ID); a cutoff time, the datetime
    before which events will be ignored; a photo cache; and a Wild Apricot API
    interface."""
    if cache_path.exists():
        with cache_path.open("rb") as f:
            known_events = pickle.load(f)
    else:
        known_events = {}
    return EventProcessor(cutoff_time, known_events, photo_cache, apricot_api)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
