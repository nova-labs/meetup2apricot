"""Uploads photos to Wild Apricot from local storage."""

from . import dryrun
from .http_response_error import PhotoUploadError
import logging
from requests import Session
from requests.auth import HTTPDigestAuth
from urllib.parse import urljoin


class PhotoUploader:

    """Uploads photos via WebDAV to Wild Apricot from local storage."""

    logger = logging.getLogger("PhotoUploader")

    def __init__(
        self,
        local_directory,
        apricot_base_url,
        apricot_directory,
        session,
        dryrun=False,
    ):
        """Initialize with a local directory path for storing photos, a Wild
        Apricot base URL, a Wild Apricot directory, a requests session, and a
        dry run flag."""
        self.local_directory = local_directory
        self.apricot_base_url = apricot_base_url
        self.apricot_directory = apricot_directory
        self.session = session
        self.dryrun = dryrun

    def upload_photo(self, photo_file_name):
        """Upload a named photo file from a local directory to Wild Apricot.
        Return the path to the photo at Wild Apricot."""
        local_photo_path = self.local_directory / photo_file_name
        apricot_photo_path = self.apricot_directory / photo_file_name
        url = urljoin(self.apricot_base_url, str(apricot_photo_path))
        files = {"file": (photo_file_name, open(local_photo_path, "rb"))}
        response = self.session.put(url, files)
        PhotoUploadError.check_response_status(response)
        return apricot_photo_path


def make_photo_uploader_session(username, password, user_agent):
    """Make an HTTP session with a username, password, and user agent for
    uploading photos to Wild Apricot."""
    session = Session()
    session.auth = HTTPDigestAuth(username, password)
    if user_agent:
        session.headers.update({"User-Agent": user_agent})
    return session


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
