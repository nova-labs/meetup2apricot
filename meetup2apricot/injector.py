from .apricot_api import ApricotApi
from .event_processor import make_event_processor
from .event_tagger import make_event_tagger
from .exceptions import JsonConversionError, MissingEnvVarError
from .http_response_error import HttpResponseError
from .logging_application import LoggingApplication
from .logging_context import LoggingContext
from .logging_setup_manager import LoggingSetupManager
from .meetup2apricot import Meetup2Apricot
from .meetup_api import MeetupEventsRetriever
from .oauth2_session_starter import Oauth2SessionStarter, Oauth2SessionStarterError
from .photo_cache import make_photo_cache
from .photo_retriever import PhotoRetriever, make_session
from .throttle import Throttle
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


def inject_enter_logging_application_scope(application_scope):
    """Return a function configured by an application scope that provides a
    processor configured by an application scope and a notional logging
    application scope."""

    def enter():
        return inject_meetup2apricot(application_scope)

    return enter


def inject_no_trace_exceptions():
    """Return a tuple listing exception classes that need no traceback."""
    return (
        HttpResponseError,
        JsonConversionError,
        MissingEnvVarError,
        Oauth2SessionStarterError,
    )


def inject_meetup2apricot(application_scope):
    """Return a Meetup events retriever configured by an application scope."""
    return Meetup2Apricot(
        meetup_events_retriever=inject_meetup_events_retriever(application_scope),
        photo_cache=inject_photo_cache(application_scope),
        event_processor=inject_event_processor(application_scope),
    )


def inject_meetup_events_retriever(application_scope):
    """Return a Meetup events retriever configured by an application scope."""
    return MeetupEventsRetriever(
        group_url_name=application_scope.meetup_group_url_name,
        events_wanted=application_scope.meetup_events_wanted,
    )


def inject_event_processor(application_scope):
    """Return an event processor configured by an application scope."""
    return make_event_processor(
        cache_path=application_scope.event_cache_file,
        cutoff_time=application_scope.earliest_event_start_time,
        photo_cache=inject_photo_cache(application_scope),
        apricot_api=inject_apricot_api(application_scope),
        event_tagger=inject_event_tagger(application_scope),
    )


def inject_photo_cache(application_scope):
    """Return a photo cache configured by an application scope."""
    return application_scope.photo_cache(inject_photo_cache_provider(application_scope))


def inject_photo_cache_provider(application_scope):
    """Return a function that provides an photo cache configured by an
    application session scope."""

    def get():
        return make_photo_cache(
            cache_path=application_scope.photo_cache_file,
            local_directory=application_scope.photo_directory,
            apricot_directory=application_scope.apricot_photo_directory,
            photo_retriever=inject_photo_retriever(application_scope),
        )

    return get


def inject_photo_retriever(application_scope):
    """Return a photo retriever configured by an application scope."""
    return PhotoRetriever(inject_http_session(application_scope))


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
