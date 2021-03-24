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
        """Uptime a mapping of Meetup IDs to Wild Apricot event IDs and start
        times. Remove outdated events. Verify and correct Meetup IDs. Return
        the updated mapping."""
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

    def is_timely(self, apricot_event_data):
        """Given a dictionary of Wild Apricot event data including a start
        date, return true if the start date is later than the earliest start
        date."""
        return apricot_event_data["start_time"] >= self.earliest_start_time

    def update_meetup_id(self, meetup_id):
        """Return Meetup's current ID for the event with a given Meetup ID.
        Return None if the event is no longer planned."""
        meetup_event = self.meetup_event_retriever.get_event(meetup_id)
        if meetup_event:
            return meetup_event.meetup_id
        else:
            return None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
