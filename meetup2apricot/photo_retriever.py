"""Retrieves photos from Meetup into local storage."""

from . import dryrun
import requests
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

    @dryrun.method()
    def get(self, photo_url, local_photo_path):
        """Get the photo from the URL and store it at the local path."""
        response = self.session.get(photo_url)
        with local_photo_path.open("wb") as photo_file:
            photo_file.write(response.content)
        self.logger.info("get: local_photo_path=%s", local_photo_path)

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
