"""Excepctions that raise when responses contain HTTP errors."""

from requests.exceptions import HTTPError
from requests_toolbelt.utils import dump
import logging


class HttpResponseError(Exception):

    """Raised when HTTP response status is not ok."""

    logger = logging.getLogger("HttpResponseError")

    @classmethod
    def check_response_status(cls, response):
        """Raise this exception if the response status is not ok."""
        try:
            response.raise_for_status()
        except HTTPError as err:
            data = dump.dump_response(response)
            cls.logger.info("Unexpected HTTP response\n{}".format(data.decode("utf-8")))
            message = "HTTP status is {:d}, not ok".format(response.status_code)
            raise cls(message) from err


class MeetupApiError(HttpResponseError):

    """Raised when a Meetup HTTP response status is not ok."""

    logger = logging.getLogger("MeetupApiError")


class ApricotApiError(HttpResponseError):

    """Raised when a Wild Apricot HTTP response status is not ok."""

    logger = logging.getLogger("ApricotApiError")


class PhotoRetrieveError(HttpResponseError):

    """Raised when a photo cannot be downloaded from Meetup."""

    logger = logging.getLogger("PhotoRetrieveError")


class PhotoUploadError(HttpResponseError):

    """Raised when a photo upload to Wild Apricot HTTP response status is not ok."""

    logger = logging.getLogger("PhotoUploadError")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
