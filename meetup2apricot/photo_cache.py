"""Cache featured photos from Meetup events."""

from . import dryrun
import re
import pickle
from urllib.parse import urlparse
from pathlib import PurePosixPath


class PhotoCache:

    """Caches event featured photos for upload to Wild Apricot."""

    def __init__(
        self,
        apricot_directory,
        urls_to_paths,
        photo_retriever,
        photo_uploader,
        cache_path,
        reporter,
        dryrun=False,
    ):
        """Initialize a Wild Apricot directory path, an initial mapping of
        Meetup photo URLs to Wild Apricot photo paths, a photo retriever, a
        photo uploader, a path to the cache file, a reporter, and a dry run
        flag."""
        self.apricot_directory = apricot_directory
        self.urls_to_paths = urls_to_paths
        self.photo_retriever = photo_retriever
        self.photo_uploader = photo_uploader
        self.cache_path = cache_path
        self.reporter = reporter
        self.dryrun = dryrun

    def cache_photo(self, meetup_event):
        """Cache a Meetup event's photo for copying to Wild Apricot and return
        it's Wild Apricot path."""
        if meetup_event.photo_url not in self.urls_to_paths:
            self.copy_meetup_photo_to_apricot(meetup_event)
        return self.urls_to_paths[meetup_event.photo_url]

    def copy_meetup_photo_to_apricot(self, meetup_event):
        """Copy a Meetup photo to Wild Apricot."""
        proposed_photo_name = self.apricot_photo_file_name(meetup_event)
        apricot_photo_name = self.photo_retriever.get(
            meetup_event.photo_url, proposed_photo_name
        )
        self.urls_to_paths[meetup_event.photo_url] = self.apricot_photo_path(
            apricot_photo_name
        )
        self.reporter.report_photo_name(apricot_photo_name)

    def apricot_photo_path(self, photo_file_name):
        """Return a photo's Wild Apricot URL path."""
        return self.apricot_directory / photo_file_name

    def apricot_photo_file_name(self, meetup_event):
        """Return the Wild Apricot photo file name for a Meetup event."""
        file_name = self.apricot_photo_name(meetup_event.name, meetup_event.start_time)
        extension = PurePosixPath(urlparse(meetup_event.photo_url).path).suffix
        return file_name + extension

    @dryrun.method()
    def persist(self):
        """Persist cache to a file."""
        with self.cache_path.open("wb") as f:
            pickle.dump(self.urls_to_paths, f)

    @staticmethod
    def apricot_photo_name(name, date):
        """Choose a descriptive photo name for Wild Apricot."""
        alpha_numeric_name = re.sub("[^A-Za-z0-9_]", "_", name + "_")
        tighter_name = re.sub("__+", "_", alpha_numeric_name)
        shorter_name = re.sub("[^_]*$", "", tighter_name[:31])
        return f"{shorter_name}{date:%Y-%m-%d}"


def load_cached_photo_urls(cache_path):
    """Return a mapping of Meetup photo URLs to Wild Apricot photo paths,
    either loaded from a cache file or initialized to a default."""
    if cache_path.exists():
        with cache_path.open("rb") as f:
            return pickle.load(f)
    else:
        return {None: None}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
