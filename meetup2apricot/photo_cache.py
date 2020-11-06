"""Cache featured photos from Meetup events."""

import re


class PhotoCache:

    """Caches event featured photos for upload to Wild Apricot."""

    def __init__(self, local_directory, apricot_directory):
        """Initialize with local and Wild Apricot directory paths."""
        self.local_directory = local_directory
        self.apricot_directory = apricot_directory

    @staticmethod
    def name_for_apricot(name, date):
        """Choose a descriptive photo name for Wild Apricot."""
        alpha_numeric_name = re.sub("[^A-Za-z0-9_]", "_", name + "_")
        tighter_name = re.sub("__+", "_", alpha_numeric_name)
        shorter_name = re.sub("[^_]*$", "", tighter_name[:31])
        return f"{shorter_name}{date:%Y-%m-%d}"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
