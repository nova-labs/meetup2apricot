"""Retrieves photos from Meetup into local storage."""

from . import dryrun
from .http_response_error import PhotoRetrieveError
import requests
import imghdr
import logging


class PhotoRetriever:

    """Retrieves photos from Meetup into local storage."""

    logger = logging.getLogger("PhotoRetriever")

    def __init__(self, local_directory, session, dryrun=False):
        """Initialize with a local directory path for storing photos, a
        requests session, and a dry run flag."""
        self.local_directory = local_directory
        self.session = session
        self.dryrun = dryrun

    @dryrun.method(value="photo.png")
    def get(self, photo_url, proposed_photo_filename):
        """Get the photo from the URL and store it with the proposed name in
        the local directory, adjusting the filename extension if needed for the
        image type. Return the actual filename."""
        proposed_photo_path = self.local_directory / proposed_photo_filename
        self.retrieve_photo(photo_url, proposed_photo_path)
        local_photo_path = self.adjust_extension(proposed_photo_path)
        proposed_photo_path.rename(local_photo_path)
        self.logger.info("get: local_photo_path=%s", local_photo_path)
        return local_photo_path.name

    def retrieve_photo(self, photo_url, photo_path):
        """Retrieve a photo from a URL and save it to a path."""
        response = self.session.get(photo_url)
        PhotoRetrieveError.check_response_status(response)
        with photo_path.open("wb") as photo_file:
            photo_file.write(response.content)

    def adjust_extension(self, photo_path):
        """Examine the image type at a photo path and adjust its filename
        extension accordingly. Return the corrected path. As of 11/22/2020,
        Python's imghdr library fails to recognize some jpeg images, returning
        None. See issue 28591, https://bugs.python.org/issue28591, opened in
        2016."""
        image_type = imghdr.what(photo_path)
        if image_type is None:
            return photo_path
        return photo_path.with_suffix(f".{image_type}")

    def assure_local_directory(self):
        """Assure that the local photo directory exists."""
        if not self.local_directory.is_dir():
            self.local_directory.mkdir()


def make_photo_retriever(local_directory, session, dryrun=False):
    """Make a photo retriever with a confirmed local directory path for
    storing photos, a requests session, and a dry run flag."""
    retriever = PhotoRetriever(local_directory, session, dryrun)
    retriever.assure_local_directory()
    return retriever


def make_session(user_agent):
    """Make a Requests session with the specified user agent."""
    session = requests.Session()
    if user_agent:
        session.headers.update({"User-Agent": user_agent})
    return session


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
