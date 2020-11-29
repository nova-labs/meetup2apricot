"""Retrieve events from Meetup and add the to Wild Apricot."""


class Meetup2Apricot:

    """Downloads Meetup events into Wild Apricot."""

    def __init__(
        self,
        meetup_events,
        initial_event_mapping,
        photo_cache,
        reporter,
        event_mapping_updater,
        event_processor_provider,
    ):
        """Initialize with upcoming Meetup events, a photo cache, and an event
        mapping updater, and an event processor provider."""
        self.meetup_events = meetup_events
        self.initial_event_mapping = initial_event_mapping
        self.photo_cache = photo_cache
        self.reporter = reporter
        self.event_mapping_updater = event_mapping_updater
        self.event_processor_provider = event_processor_provider

    def run(self):
        """Run the Meetup to Wild Apricot conversion."""
        event_processor = self.setup_event_processor()
        self.add_apricot_events(event_processor)
        self.reporter.report_downloads()
        event_processor.persist()
        self.photo_cache.persist()

    def setup_event_processor(self):
        """Setup an event processor."""
        event_mapping = self.event_mapping_updater.update_event_mapping(
            self.initial_event_mapping
        )
        return self.event_processor_provider(event_mapping)

    def add_apricot_events(self, event_processor):
        """Use an event processor to add Meetup events to Wild Apricot."""
        for event in self.meetup_events:
            event_processor.process(event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
