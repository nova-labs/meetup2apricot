"""Loads event restrictions from a configuration list.

A configuration list contains JSON objects converted to Python dicts with these keys:

    name: the event registration type name such as RSVP.

    pattern: a regex pattern to find within the event name.

    levels: a member level name such as Associate or a list of such names. If
    omitted, all member levels are selected.
"""

from .exceptions import InvalidRestrictionPattern
from collections import namedtuple
import re

# Each restriction object contains an event registration type name, a regex
# pattern to search for in an event name, and a list of names of member levels
# allowed to register.

EventRestriction = namedtuple("EventRestriction", "name pattern member_levels")


class EventRestrictionLoader:

    """Loads event restrictions from a list, compiling title patterns, and
    validating member levels."""

    def __init__(self, member_level_manager):
        """Initialize with a member level manager."""
        self.member_level_manager = member_level_manager

    def load(self, restriction_list):
        """Load restrictions from a list of restriction JSON objects, typically
        from the environment configuration.  Return a list of EventRestriction
        objects."""
        return [self.load_restriction(restriction) for restriction in restriction_list]

    def load_restriction(self, restriction):
        """Load a restriction JSON object, typically from the environment
        configuration.  Return an EventRestriction object."""
        name = restriction["name"]
        pattern = self.compile_pattern(restriction["pattern"])
        level_names = self.clean_level_names(restriction.get("levels", []))
        member_levels = self.lookup_member_levels(level_names)
        return EventRestriction(name, pattern, member_levels)

    def lookup_member_levels(self, level_names):
        """Given a list of member level names, return a corresponding list of
        member levels. If the level name list is empty, return all member
        levels."""
        if level_names:
            return self.member_level_manager.named_levels(level_names)
        else:
            return self.member_level_manager.all_levels()

    @staticmethod
    def compile_pattern(pattern):
        """Compile a title patten. Return the compiled pattern."""
        try:
            return re.compile(pattern, re.IGNORECASE)
        except re.error as err:
            message = f"Event restriction pattern {pattern!r} is invalid: {err}"
            raise InvalidRestrictionPattern(message) from err

    @staticmethod
    def clean_level_names(raw_level_names):
        """Give a list of member level names, an individual member level name,
        or None, return a possibly empty list of member level names."""
        if not raw_level_names:
            return []
        if type(raw_level_names) == str:
            return [raw_level_names]
        return raw_level_names


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
