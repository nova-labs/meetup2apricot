"""Cache featured photos from Meetup events."""

import re
import pickle
from urllib.parse import urlparse
from pathlib import PurePosixPath


class PhotoCache:

    """Caches event featured photos for upload to Wild Apricot."""

    def __init__(
        self,
        local_directory,
        apricot_directory,
        urls_to_paths,
        photo_retriever,
        cache_path,
    ):
        """Initialize with local and Wild Apricot directory paths, an initial
        mapping of Meetup photo URLs to Wild Apricot photo paths, a photo
        retriever, and a path to the cache file."""
        self.local_directory = local_directory
        self.apricot_directory = apricot_directory
        self.urls_to_paths = urls_to_paths
        self.photo_retriever = photo_retriever
        self.cache_path = cache_path

    def cache_photo(self, meetup_event):
        """Cache a Meetup event's photo for copying to Wild Apricot and return
        it's Wild Apricot path."""
        if meetup_event.photo_url not in self.urls_to_paths:
            self.get_meetup_photo_for_apricot(meetup_event)
        return self.urls_to_paths[meetup_event.photo_url]

    def get_meetup_photo_for_apricot(self, meetup_event):
        """Get a Meetup photo for Wild Apricot."""
        apricot_photo_name = self.apricot_photo_file_name(meetup_event)
        self.urls_to_paths[meetup_event.photo_url] = self.apricot_photo_path(
            apricot_photo_name
        )
        local_photo_path = self.local_photo_path(apricot_photo_name)
        self.photo_retriever.get(meetup_event.photo_url, local_photo_path)

    def apricot_photo_path(self, photo_file_name):
        """Return a photo's Wild Apricot URL path."""
        return self.apricot_directory / photo_file_name

    def local_photo_path(self, photo_file_name):
        """Return a photo's local path."""
        return self.local_directory / photo_file_name

    def apricot_photo_file_name(self, meetup_event):
        """Return the Wild Apricot photo file name for a Meetup event."""
        file_name = self.apricot_photo_name(meetup_event.name, meetup_event.start_time)
        extension = PurePosixPath(urlparse(meetup_event.photo_url).path).suffix
        return file_name + extension

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


def make_photo_cache(cache_path, local_directory, apricot_directory, photo_retriever):
    """Initialize with path to a file caching mapping of Meetup photo URLs to
    Wild Apricot photo paths, local and Wild Apricot directory paths, and a
    photo retriever."""
    if not local_directory.is_dir():
        local_directory.mkdir()
    if cache_path.exists():
        with cache_path.open("rb") as f:
            urls_to_paths = pickle.load(f)
    else:
        urls_to_paths = {None: None}
    return PhotoCache(
        local_directory, apricot_directory, urls_to_paths, photo_retriever, cache_path
    )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
