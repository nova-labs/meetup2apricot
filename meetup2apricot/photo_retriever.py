"""Retrieves photos from Meetup into local storage."""

import requests


class PhotoRetriever:

    """Retrieves photos from Meetup into local storage."""

    def __init__(self, session):
        """Initialize with a requests session."""
        self.session = session

    def get(self, photo_url, local_photo_path):
        """Get the photo from the URL and store it at the local path."""
        response = self.session.get(photo_url)
        self.assure_directory(local_photo_path)
        with local_photo_path.open('wb') as photo_file:
            photo_file.write(response.content)

    @staticmethod
    def assure_directory(file_path):
        """Asssure existence of a file's directory."""
        dir_path = file_path.parent
        if not dir_path.is_dir():
            dir_path.mkdir()


def make_session(user_agent):
    """Make a Requests session with the specified user agent."""
    session = requests.Session()
    if user_agent:
        session.headers.update({'User-Agent': user_agent})
    return session

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
