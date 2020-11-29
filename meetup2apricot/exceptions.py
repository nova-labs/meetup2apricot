"""Descriptive exceptions."""


class InvalidRestrictionPattern(Exception):
    """Raised when an event restriction title pattern cannot be compiled."""


class JsonConversionError(Exception):

    """Raised when JSON conversion fails."""


class MissingEnvVarError(Exception):
    """Raised when an expected environment variable is missing."""


class UnknownMemberLevelName(Exception):
    """Raised when an unknown member level name is requested."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
