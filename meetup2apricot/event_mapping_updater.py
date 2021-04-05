"""Updates the mapping of Meetup event IDs to Wild Apricot event IDs."""


class EventMappingUpdater:

    """Updates mappings of Meetup event IDs to Wild Apricot event IDs by
    removing outdated events, correcting Meetup event IDs, and adding skipped
    Meetup event IDs."""

    def __init__(self, meetup_event_retriever, earliest_start_time, skip_meetup_ids):
        """Initialize with a Meetup event retriever, an earliest start time for
        event retention, and a list of skipped Meetup event IDs."""
        self.meetup_event_retriever = meetup_event_retriever
        self.earliest_start_time = earliest_start_time
        self.skip_meetup_ids = skip_meetup_ids

    def update_event_mapping(self, event_mapping):
        """Update a mapping of Meetup IDs to Wild Apricot event IDs and start
        times. Remove outdated events. Verify and correct Meetup IDs. Return
        the updated mapping."""
        cleansed_events = self.clean_event_mapping(event_mapping)
        skipped_events = self.skipped_event_ids_and_times()
        cleansed_events.update(skipped_events)
        return cleansed_events

    def clean_event_mapping(self, event_mapping):
        """Clean a an event mapping.  Remove outdated events. Verify and
        correct Meetup IDs. Return the cleansed mapping."""
        timely_events = (
            (meetup_id, apricot_event_data)
            for (meetup_id, apricot_event_data) in event_mapping.items()
            if self.is_timely(apricot_event_data)
        )
        updated_events = (
            (self.update_meetup_id(meetup_id), apricot_event_data)
            for (meetup_id, apricot_event_data) in timely_events
        )
        return {
            meetup_id: apricot_event_data
            for (meetup_id, apricot_event_data) in updated_events
            if meetup_id
        }

    def skipped_event_ids_and_times(self):
        """Return a list of (possibly updated) valid Meetup event IDs to skip
        and their start times."""
        skip_meetup_events = (
            self.get_event(meetup_id) for meetup_id in self.skip_meetup_ids
        )
        return (
            (event.meetup_id, {"start_time": event.start_time})
            for event in skip_meetup_events
            if event
        )

    def is_timely(self, apricot_event_data):
        """Given a dictionary of Wild Apricot event data including a start
        date, return true if the start date is later than the earliest start
        date."""
        return apricot_event_data["start_time"] >= self.earliest_start_time

    def update_meetup_id(self, meetup_id):
        """Return Meetup's current ID for the event with a given Meetup ID.
        Return None if the event is no longer planned."""
        meetup_event = self.get_event(meetup_id)
        if meetup_event:
            return meetup_event.meetup_id
        else:
            return None

    def get_event(self, meetup_id):
        """Return a Meetup event with the event ID or None if no current event
        is available."""
        return self.meetup_event_retriever.get_event(meetup_id)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
