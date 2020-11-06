"""Cache featured photos from Meetup events."""

import re
from urllib.parse import urlparse
from pathlib import PurePosixPath


class PhotoCache:

    """Caches event featured photos for upload to Wild Apricot."""

    def __init__(self, local_directory, apricot_directory):
        """Initialize with local and Wild Apricot directory paths."""
        self.local_directory = local_directory
        self.apricot_directory = apricot_directory

    def apricot_photo_path(self, meetup_event):
        """Return the Wild Apricot photo path for a Meetup event or None."""
        if meetup_event.photo_url:
            photo_file_name = self.apricot_photo_file_name(meetup_event)
            return self.apricot_directory / photo_file_name
        else:
            return None

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
