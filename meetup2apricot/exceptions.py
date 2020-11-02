"""Descriptive exceptions."""


class JsonConversionError(Exception):

    """Raised when JSON conversion fails."""


class MissingEnvVarError(Exception):
    """Raisded when an expected environment variable is missing."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
