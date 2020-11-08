"""Application scope holds command line arguments and environment variables
needed by the application."""


from .scope_cache import ScopeCache
from . import __version__
from datetime import datetime
from pathlib import Path, PurePosixPath
import logging

APP_NAME = "meetup2apricot"


class ApplicationScope:

    """Application scope provides configuration values."""

    def __init__(self, args, env_vars):
        """Initialize with parsed command line arguments and a careful
        environment variable dictionary."""
        self._args = args
        self._env_vars = env_vars
        self._photo_cache_cache = ScopeCache()

    @property
    def app_name(self):
        return APP_NAME

    @property
    def apricot_account_number(self):
        return self._env_vars["APRICOT_ACCOUNT_NUMBER"]

    @property
    def apricot_api_key(self):
        return self._env_vars["APRICOT_API_KEY"]

    @property
    def apricot_photo_directory(self):
        return PurePosixPath(self._env_vars["APRICOT_PHOTO_DIRECTORY"])

    @property
    def debug(self):
        return self._args.debug

    @property
    def earliest_event_start_time(self):
        return datetime.fromisoformat(
            self._env_vars["EARLIEST_EVENT_START_TIME"])

    @property
    def event_cache_file(self):
        return Path(self._env_vars["EVENT_CACHE_FILE"])

    @property
    def logfile(self):
        return self._args.logfile

    @property
    def log_level(self):
        return logging.DEBUG if self.debug else logging.INFO

    @property
    def meetup_events_wanted(self):
        return self._env_vars["MEETUP_EVENTS_WANTED"]

    @property
    def meetup_group_url_name(self):
        return self._env_vars["MEETUP_GROUP_URL_NAME"]

    def photo_cache(self, photo_cache_provider):
        return self._photo_cache_cache.get(photo_cache_provider)

    @property
    def photo_cache_file(self):
        return Path(self._env_vars["PHOTO_CACHE_FILE"])

    @property
    def photo_directory(self):
        return Path(self._env_vars["PHOTO_DIRECTORY"])

    @property
    def verbose(self):
        return self._args.verbose

    @property
    def version(self):
        return __version__

    @property
    def warnings(self):
        return self._args.warnings


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
