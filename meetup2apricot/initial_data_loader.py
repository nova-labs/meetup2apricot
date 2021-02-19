"""Loads initial data from caches and Meetup to prepare for event conversino."""

from .meetup_event import MeetupEvent
from .scope_cache import ScopeCache


class InitialDataScope:

    """Initial data scope provides data loaded once at the beginning of a run."""

    def __init__(
        self,
        upcoming_meetup_events,
        membership_levels,
        photo_urls_to_paths,
        meetup_to_apricot_event_mapping,
    ):
        """Initialize with data loaded from Meetup and caches."""
        self.upcoming_meetup_events = upcoming_meetup_events
        self.membership_levels = membership_levels
        self.photo_urls_to_paths = photo_urls_to_paths
        self.meetup_to_apricot_event_mapping = meetup_to_apricot_event_mapping
        self._photo_cache_cache = ScopeCache()

    def photo_cache(self, photo_cache_provider):
        """Return a cached photo cache or one provided by a provider."""
        return self._photo_cache_cache.get(photo_cache_provider)


class InitialDataLoader:

    """Loads cached event and photo data. Downloads upcoming Meetup events.
    Runs the Meetup to Wild Apricot event conversion."""

    def __init__(
        self,
        meetup_api,
        apricot_api,
        event_mapping_provider,
        photo_urls_provider,
        enter_initial_data_scope,
    ):
        """Initialize with Meetup and Wild Apricot APIs and functions to
        provide cached event and photo data and to enter the initial data
        scope."""
        self.meetup_api = meetup_api
        self.apricot_api = apricot_api
        self.event_mapping_provider = event_mapping_provider
        self.photo_urls_provider = photo_urls_provider
        self.enter_initial_data_scope = enter_initial_data_scope

    def run(self):
        """Run the Meetup to Wild Apricot conversion."""
        upcoming_meetup_events = self.retreive_upcoming_meetup_events()
        membership_levels = self.retrieve_membership_levels()
        event_mapping = self.event_mapping_provider()
        photo_urls_to_paths = self.photo_urls_provider()
        self.convert_events(
            upcoming_meetup_events,
            membership_levels,
            photo_urls_to_paths,
            event_mapping,
        )

    def retreive_upcoming_meetup_events(self):
        """Return a list of upcoming Meetup events to convert."""
        json_events = self.meetup_api.retrieve_events_json()
        return [MeetupEvent(event) for event in json_events]

    def retrieve_membership_levels(self):
        """Return a list of Wild Apricot membership levels."""
        return self.apricot_api.get_membership_levels()

    def convert_events(
        self,
        upcoming_meetup_events,
        membership_levels,
        photo_urls_to_paths,
        event_mapping,
    ):
        """Convert Meetup events to Wild Apricot events using some initial data."""
        initial_data_scope = InitialDataScope(
            upcoming_meetup_events,
            membership_levels,
            photo_urls_to_paths,
            event_mapping,
        )
        processor = self.enter_initial_data_scope(initial_data_scope)
        processor.run()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
