from .apricot_api import ApricotApi
from .event_mapping_updater import EventMappingUpdater
from .event_processor import EventProcessor, load_cached_event_mapping
from .event_tagger import make_event_tagger
from .exceptions import JsonConversionError, MissingEnvVarError
from .http_response_error import HttpResponseError
from .initial_data_loader import InitialDataLoader
from .logging_application import LoggingApplication
from .logging_context import LoggingContext
from .logging_setup_manager import LoggingSetupManager
from .meetup2apricot import Meetup2Apricot
from .meetup_api import MeetupApi
from .meetup_event_retriever import MeetupEventRetriever
from .oauth2_session_starter import Oauth2SessionStarter, Oauth2SessionStarterError
from .photo_cache import PhotoCache, load_cached_photo_urls
from .photo_retriever import make_photo_retriever, make_session
from .throttle import Throttle, OpenThrottle
from requests_toolbelt import user_agent


APRICOT_TOKEN_URL = "https://oauth.wildapricot.org/auth/token"


def inject_logging_application(application_scope):
    """Return a logging application configured by an application scope."""
    return LoggingApplication(
        inject_logging_context(application_scope),
        inject_enter_logging_application_scope(application_scope),
    )


def inject_logging_context(application_scope):
    """Return a logging context configured by an application scope."""
    return LoggingContext(
        app_name=application_scope.app_name,
        description=application_scope.version,
        logging_setup_manager=inject_logging_setup_manager(application_scope),
        no_trace_exceptions=inject_no_trace_exceptions(),
    )


def inject_logging_setup_manager(application_scope):
    """Return a logging setup manager configured by an application scope."""
    return LoggingSetupManager(
        log_level=application_scope.log_level,
        filename=application_scope.logfile,
        verbose=application_scope.verbose,
        warnings=application_scope.warnings,
    )


def inject_no_trace_exceptions():
    """Return a tuple listing exception classes that need no traceback."""
    return (
        HttpResponseError,
        JsonConversionError,
        MissingEnvVarError,
        Oauth2SessionStarterError,
    )


def inject_enter_logging_application_scope(application_scope):
    """Return a function configured by an application scope that provides a
    processor configured by an application scope and a notional logging
    application scope."""

    def enter():
        return inject_initial_data_loader(application_scope)

    return enter


def inject_initial_data_loader(application_scope):
    """Inject an initial data loader configured by an application scope."""
    return InitialDataLoader(
        meetup_api=inject_meetup_api(application_scope),
        event_mapping_provider=inject_event_mapping_provider(application_scope),
        photo_urls_provider=inject_photo_urls_provider(application_scope),
        enter_initial_data_scope=inject_enter_initial_data_scope(application_scope),
    )


def inject_event_mapping_provider(application_scope):
    """Inject a function configured by an application scope that provides cached
    event mappings."""

    def get():
        return load_cached_event_mapping(application_scope.event_cache_file)

    return get


def inject_photo_urls_provider(application_scope):
    """Inject a function configured by an application scope that provides
    cached mappings of Meetup photo URLs to Wild Apricot photo paths."""

    def get():
        return load_cached_photo_urls(application_scope.photo_cache_file)

    return get


def inject_enter_initial_data_scope(application_scope):
    """Return a function configured by an application scope that provides a
    processor configured by an application scope and an initial data scope."""

    def enter(initial_data_scope):
        return inject_meetup2apricot(application_scope, initial_data_scope)

    return enter


def inject_meetup2apricot(application_scope, initial_data_scope):
    """Return a Meetup to Wild Apricot processor configured by application and
    initial data scopes."""
    return Meetup2Apricot(
        meetup_events=initial_data_scope.meetup_events,
        initial_event_mapping=initial_data_scope.meetup_to_apricot_event_mapping,
        photo_cache=inject_photo_cache(application_scope, initial_data_scope),
        event_mapping_updater=inject_event_mapping_updater(
            application_scope, initial_data_scope
        ),
        event_processor_provider=inject_event_processor_provider(
            application_scope, initial_data_scope
        ),
    )


def inject_meetup_api(application_scope):
    """Return a Meetup API configured by an application scope."""
    return application_scope.meetup_api(inject_meetup_api_provider(application_scope))


def inject_meetup_api_provider(application_scope):
    """Return function that provides a Meetup API configured by an application
    scope."""

    def get():
        return MeetupApi(
            session=inject_http_session(application_scope),
            throttle=inject_meetup_throttle(application_scope),
            group_url_name=application_scope.meetup_group_url_name,
            events_wanted=application_scope.meetup_events_wanted,
        )

    return get


def inject_meetup_throttle(application_scope):
    """Return a throttle for Meetup API access configured by an application
    scope."""
    return inject_meetup_api_for_status(application_scope).make_meetup_api_throttle()


def inject_meetup_api_for_status(application_scope):
    """Return a Meetup API configured by an application scope for one status
    request."""
    return MeetupApi(
        session=inject_http_session(application_scope),
        throttle=OpenThrottle(),
        group_url_name=application_scope.meetup_group_url_name,
        events_wanted=application_scope.meetup_events_wanted,
    )


def inject_event_processor_provider(application_scope, initial_data_scope):
    """Return a function that provides an event processor configured by an
    event mapping and by application and initial data scopes."""

    def get(event_mapping):
        return EventProcessor(
            earliest_start_time=application_scope.earliest_event_start_time,
            latest_start_time=application_scope.latest_event_start_time,
            known_events=event_mapping,
            photo_cache=inject_photo_cache(application_scope, initial_data_scope),
            apricot_api=inject_apricot_api(application_scope),
            cache_path=application_scope.event_cache_file,
            event_tagger=inject_event_tagger(application_scope),
            dryrun=application_scope.dryrun,
        )

    return get


def inject_photo_cache(application_scope, initial_data_scope):
    """Return a photo cache configured by application and initial data scopes."""
    return initial_data_scope.photo_cache(
        inject_photo_cache_provider(application_scope, initial_data_scope)
    )


def inject_photo_cache_provider(application_scope, initial_data_scope):
    """Return a function that provides an photo cache configured by application
    and initial data scopes."""

    def get():
        return PhotoCache(
            apricot_directory=application_scope.apricot_photo_directory,
            urls_to_paths=initial_data_scope.photo_urls_to_paths,
            photo_retriever=inject_photo_retriever(application_scope),
            cache_path=application_scope.photo_cache_file,
            dryrun=application_scope.dryrun,
        )

    return get


def inject_photo_retriever(application_scope):
    """Return a photo retriever configured by an application scope."""
    return make_photo_retriever(
        local_directory=application_scope.photo_directory,
        session=inject_http_session(application_scope),
        dryrun=application_scope.dryrun,
    )


def inject_event_mapping_updater(application_scope, initial_data_scope):
    """Return an event mapping updater configured by application and initial
    data scopes."""
    return EventMappingUpdater(
        meetup_event_retriever=inject_meetup_event_retriever(
            application_scope, initial_data_scope
        ),
        earliest_start_time=application_scope.earliest_event_start_time,
    )


def inject_meetup_event_retriever(application_scope, initial_data_scope):
    """Return a Meetup event retriever configured by application and initial
    data scopes."""
    return MeetupEventRetriever(
        meetup_api=inject_meetup_api(application_scope),
        meetup_events=initial_data_scope.meetup_events,
    )


def inject_http_session(application_scope):
    """Return a Requests HTTP session configured by an application scope."""
    return make_session(inject_user_agent(application_scope))


def inject_apricot_api(application_scope):
    """Return a Wild Apricot API interface configured by an application
    scope."""
    return ApricotApi(
        account_id=application_scope.apricot_account_number,
        session=inject_apricot_oauth_session(application_scope),
        throttle=inject_apricot_throttle(application_scope),
        dryrun=application_scope.dryrun,
    )


def inject_apricot_oauth_session(application_scope):
    """Return an OAuth session for Wild Apricot configured by an application
    scope."""
    return inject_apricot_oauth_session_starter(application_scope).start_session()


def inject_apricot_oauth_session_starter(application_scope):
    """Return an OAuth session starter for Wild Apricot configured by an
    application scope."""
    return Oauth2SessionStarter(
        client_id="APIKEY",
        client_secret=application_scope.apricot_api_key,
        token_url=APRICOT_TOKEN_URL,
        user_agent=inject_user_agent(application_scope),
        scope="auto",
    )


def inject_user_agent(application_scope):
    """Return the user agent string for web requests configured by an
    application scope."""
    return user_agent(application_scope.app_name, application_scope.version)


def inject_apricot_throttle(application_scope):
    """Return a throttle for Wild Apricot web requests configured by an
    application scope."""
    return Throttle(rate=100, time_span=60)


def inject_event_tagger(application_scope):
    """Return an event tagger configured by an application scope."""
    return make_event_tagger(
        application_scope.codes_to_tags, application_scope.all_event_tags
    )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
