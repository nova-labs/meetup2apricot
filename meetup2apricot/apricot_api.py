"""Access Apricot API to insert events."""

from .http_response_error import ApricotApiError
import logging


class ApricotApi:

    """Hides details of accessing the Apricot API."""

    logger = logging.getLogger("ApricotApi")
    api_url = "https://api.wildapricot.org"
    api_version = "v2.2"
    api_base_url = f"{api_url}/{api_version}"

    def __init__(self, account_id, session):
        """Initialize with a Wild Appricot account ID and an OAuth2 session to
        the Apricot server."""
        self.account_id = account_id
        self.session = session

    def get_response(self, url, **payload):
        """Request a URL and return the response."""
        response = self.session.get(url, params=payload)
        ApricotApiError.check_response_status(response)
        return response

    def get_json(self, url, **payload):
        """Request a URL and return the JSON result."""
        response = self.get_response(url, **payload)
        return response.json()

    def delete(self, url, **payload):
        """Request deletion at a URL and return the response."""
        response = self.session.delete(url, params=payload)
        ApricotApiError.check_response_status(response)
        return response

    def post(self, url, json=None, **payload):
        """Request posting at a URL and return the response."""
        response = self.session.post(url, json=json, data=payload)
        ApricotApiError.check_response_status(response)
        return response

    def put(self, url, **payload):
        """Request puting at a URL and return the response."""
        response = self.session.put(url, data=payload)
        ApricotApiError.check_response_status(response)
        return response

## Wild Apricot functions

    def get_event(self, event_id):
        """Get the JSON description of an event."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/events/{event_id}"
        return self.get_json(url)

    def add_event(self, event):
        """Insert an event into Wild Apricot."""
        url = f"{self.api_base_url}/accounts/{self.account_id}/events"
        return self.post(url, json=event)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
