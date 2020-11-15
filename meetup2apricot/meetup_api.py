"""Access Meetup API to download events."""

from .http_response_error import MeetupApiError
from .throttle import make_throttle
import requests


class MeetupEventsRetriever:

    """Retrieves events and other data from Meetup via their API."""

    api_utilization_ratio = 2 / 3

    def __init__(self, session, throttle, group_url_name, events_wanted):
        """Initialize with a Requests session, a throttle, a Meetup group URL
        name, and the number of events wanted from Meetup."""
        self.session = session
        self.throttle = throttle
        self.group_url_name = group_url_name
        self.events_wanted = events_wanted

    def retrieve_status(self):
        """Retrieve the status of the Meetup API."""
        self.throttle.throttle()
        url = self.build_url("status")
        response = self.session.get(url)
        MeetupApiError.check_response_status(response)
        return response

    def retrieve_events_json(self, *path_segments, **kwargs):
        """Retrieve the JSON event list, adding path segments to the URL and
        keyword arguments to the usual request parameters."""
        self.throttle.throttle()
        url = self.build_url(self.group_url_name, "events", *path_segments)
        params = self.request_params()
        params.update(kwargs)
        response = self.session.get(url, params=params)
        MeetupApiError.check_response_status(response)
        return response.json()

    def build_url(self, *path_segments):
        """Build a Meetup API URL from any number of path segments."""
        path = "/".join(path_segments)
        return f"https://api.meetup.com/{path}"

    def request_params(self):
        """Return a dictionary of request parameters."""
        return {
            "page": self.events_wanted,
            "fields": "featured_photo",
            "scroll": "recent_past",
        }

    def make_throttle(self, requests_response):
        """Make a throttle based on a Meetup API Request response."""
        rate = int(requests_response.headers["X-RateLimit-Limit"])
        time_span = int(requests_response.headers["X-RateLimit-Reset"])
        return make_throttle(rate, time_span, self.api_utilization_ratio, "Meetup API")

    def make_meetup_api_throttle(self):
        """Make a Meetup status request and return a throttle configured with
        the rate limits contained in Meetup's response."""
        response = self.retrieve_status()
        return self.make_throttle(response)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
