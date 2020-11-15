"""Retrieve events from Meetup and add the to Wild Apricot."""

from .meetup_event import MeetupEvent


class Meetup2Apricot:

    """Downloads Meetup events into Wild Apricot."""

    def __init__(self, meetup_api, photo_cache, event_processor):
        """Initialize with a Meetup API, a photo cache, and an event
        processor."""
        self.meetup_api = meetup_api
        self.photo_cache = photo_cache
        self.event_processor = event_processor

    def run(self):
        """Run the Meetup to Wild Apricot conversion."""
        meetup_events = self.retreive_meetup_events()
        self.add_apricot_events(meetup_events)
        self.event_processor.persist()
        self.photo_cache.persist()

    def retreive_meetup_events(self):
        """Return a list of Meetup events to convert."""
        json_events = self.meetup_api.retrieve_events_json()
        return [MeetupEvent(event) for event in json_events]

    def add_apricot_events(self, meetup_events):
        """Add Meetup events to Wild Apricot."""
        for event in meetup_events:
            self.event_processor.process(event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
