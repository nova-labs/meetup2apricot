r"""A regex pattern that can be tested for equality with some result.

From "Assert that str matches regex in pytest" by Ihor Kalnytskyi
https://kalnytskyi.com/howto/assert-str-matches-regex-in-pytest/

Example usage:

assert foo == PytestRegex('\d+')
"""

import re


class PytestRegex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        """Initialize with a regex pattern and flags."""
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        """Return true if the actual value matches the regex pattern; false
        otherwise."""
        return bool(self._regex.match(actual))

    def __repr__(self):
        """Return the regex pattern as the string representation."""
        return self._regex.pattern


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
