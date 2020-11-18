"""Retrieves Meetup events by ID."""

from .meetup_event import MeetupEvent


class MeetupEventRetriever:

    """Retrieves events by ID from cache or Meetup API."""

    def __init__(self, meetup_api, meetup_events):
        """Initialize with a Meetup API interface and a list of Meetup events."""
        self.meetup_api = meetup_api
        self.events_by_id = {event.meetup_id: event for event in meetup_events}

    def get_event(self, meetup_id):
        """Return a Meetup event with the event ID or None if no current event
        is available."""
        if meetup_id not in self.events_by_id:
            self.events_by_id[meetup_id] = self.retrieve_event(meetup_id)
        return self.events_by_id[meetup_id]

    def retrieve_event(self, meetup_id):
        """Retrieve a Meetup event by ID from Meetup. Return the event or None
        if it is cancelled or unavailable."""
        event_json = self.meetup_api.retrieve_event_json(meetup_id)
        if not event_json:
            return None
        event = MeetupEvent(event_json)
        if event.status == "cancelled":
            return None
        return event


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
