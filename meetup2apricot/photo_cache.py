"""Cache featured photos from Meetup events."""

import re
from urllib.parse import urlparse
from pathlib import PurePosixPath


class PhotoCache:

    """Caches event featured photos for upload to Wild Apricot."""

    def __init__(self, local_directory, apricot_directory, urls_to_paths,
                photo_retriever):
        """Initialize with local and Wild Apricot directory paths, an initial
        mapping of Meetup photo URLs to Wild Apricot photo paths and a photo
        retriever."""
        self.local_directory = local_directory
        self.apricot_directory = apricot_directory
        self.urls_to_paths = urls_to_paths
        self.photo_retriever = photo_retriever

    def cache_photo(self, meetup_event):
        """Cache a Meetup event's photo for copying to Wild Apricot and return
        it's Wild Apricot path."""
        if meetup_event.photo_url not in self.urls_to_paths:
            self.get_meetup_photo_for_apricot(meetup_event)
        return self.urls_to_paths[meetup_event.photo_url]

    def get_meetup_photo_for_apricot(self, meetup_event):
        """Get a Meetup photo for Wild Apricot."""
        apricot_photo_name = self.apricot_photo_file_name(meetup_event)
        self.urls_to_paths[meetup_event.photo_url] = \
            self.apricot_photo_path(apricot_photo_name)
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
        file_name = self.apricot_photo_name(
                meetup_event.name,
                meetup_event.start_time)
        extension = PurePosixPath(urlparse(meetup_event.photo_url).path).suffix
        return file_name + extension

    @staticmethod
    def apricot_photo_name(name, date):
        """Choose a descriptive photo name for Wild Apricot."""
        alpha_numeric_name = re.sub("[^A-Za-z0-9_]", "_", name + "_")
        tighter_name = re.sub("__+", "_", alpha_numeric_name)
        shorter_name = re.sub("[^_]*$", "", tighter_name[:31])
        return f"{shorter_name}{date:%Y-%m-%d}"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
