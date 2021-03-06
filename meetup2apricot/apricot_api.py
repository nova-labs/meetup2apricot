"""Access Apricot API to insert events."""

from . import dryrun
from .http_response_error import ApricotApiError
import logging


class ApricotApi:

    """Hides details of accessing the Apricot API."""

    logger = logging.getLogger("ApricotApi")
    api_url = "https://api.wildapricot.org"
    api_version = "v2.2"
    api_base_url = f"{api_url}/{api_version}"

    def __init__(self, account_id, session, throttle, dryrun=False):
        """Initialize with a Wild Appricot account ID, an OAuth2 session to the
        Apricot server, a throttle to slow large numbers of requests, and a dry
        run flag."""
        self.account_id = account_id
        self.session = session
        self.throttle = throttle
        self.dryrun = dryrun

    def get_response(self, url, **payload):
        """Request a URL and return the response."""
        self.throttle.throttle()
        response = self.session.get(url, params=payload)
        ApricotApiError.check_response_status(response)
        return response

    def get_json(self, url, **payload):
        """Request a URL and return the JSON result."""
        response = self.get_response(url, **payload)
        return response.json()

    def delete(self, url, **payload):
        """Request deletion at a URL and return the response."""
        self.throttle.throttle()
        response = self.session.delete(url, params=payload)
        ApricotApiError.check_response_status(response)
        return response

    def post(self, url, json=None, **payload):
        """Request posting at a URL and return the response."""
        self.throttle.throttle()
        response = self.session.post(url, json=json, data=payload)
        ApricotApiError.check_response_status(response)
        return response

    def put(self, url, **payload):
        """Request puting at a URL and return the response."""
        self.throttle.throttle()
        response = self.session.put(url, data=payload)
        ApricotApiError.check_response_status(response)
        return response

    # Wild Apricot functions

    def get_event(self, event_id):
        """Get the JSON description of an event."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/events/{event_id}"
        return self.get_json(url)

    def get_membership_levels(self):
        """Get the JSON list of membership levels."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/membershiplevels"
        return self.get_json(url)

    @dryrun.method(value=12345)
    def add_event(self, event):
        """Insert an event into Wild Apricot."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/events"
        return int(self.post(url, json=event).content)

    @dryrun.method(value=2468)
    def clone_event(self, event_id, title_prefix):
        """Clone a Wild Apricot event, setting a title prefix. Return the new
        event number."""
        url = f"{self.api_base_url}/rpc/{self.account_id}/CloneEvent"
        request = {"EventId": event_id, "TitlePrefix": title_prefix}
        return int(self.post(url, json=request).content)

    @dryrun.method(value=98765)
    def add_registration_type(self, registration_type):
        """Insert an event registration type into Wild Apricot."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/EventRegistrationTypes"
        return int(self.post(url, json=registration_type).content)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
