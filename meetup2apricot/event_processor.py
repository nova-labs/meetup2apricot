"""Process Meetup events by creating and uploading Wild Apricot events, by
downloading Meetup photos for manual uploading to Wild Apricot, and by tracking
events and photos already seen."""

class EventProcessor:

    """Processes Meetup events into Wild Apricot events."""

    def __init__(self, cutoff_time, known_events):
        """Initialize with a cutoff time, a datetime before which events will
        be ignored; a dictionary of previously processed known events (indexed
        by Meetup event ID)."""
        self.cutoff_time = cutoff_time
        self.known_events = known_events

    def process(self, meetup_event):
        """Process a meetup event."""
        if self.can_ignore_event(meetup_event):
            return
        photo_name = self.get_photo(meetup_event)
        self.add_apricot_event(meetup_event, photo_name)

    def can_ignore_event(self, meetup_event):
        """Return true if a Meetup event can be ignored; false otherwise."""
        return meetup_event.start_time < self.cutoff_time \
            or meetup_event.meetup_id in self.known_events

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
