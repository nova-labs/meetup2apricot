"""Access Meetup API to download events."""

from .http_response_error import MeetupApiError
import requests


class MeetupEventsRetriever:
    def __init__(self, group_url_name, events_wanted):
        """Initialize with a Meetup group URL name and the number of events
        wanted from Meetup."""
        self.group_url_name = group_url_name
        self.events_wanted = events_wanted

    def retrieve_events_json(self, **kwargs):
        """Retrieve the JSON event list, adding keyword arguments to the usual
        request parameters."""
        url = self.build_url()
        params = self.request_params()
        params.update(kwargs)
        response = requests.get(url, params=params)
        MeetupApiError.check_response_status(response)
        return response.json()

    def build_url(self):
        """Build a Meetup API URL to download events."""
        return "https://api.meetup.com/{}/events".format(self.group_url_name)

    def request_params(self):
        """Return a dictionary of request parameters."""
        return {
            "page": self.events_wanted,
            "fields": "series,featured_photo",
            "scroll": "recent_past",
        }


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
