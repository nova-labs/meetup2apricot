"""Loads event restrictions from a configuration list.

A configuration list contains JSON objects converted to Python dicts with these keys:

    name: the event registration type name such as RSVP. (Default: Register)

    pattern: a regex pattern to find within the event name. (Default: match all
    event names)

    price: "free" or "paid" to match only free or paid events. (Default: match
    both free and paid events)

    levels: a member level name such as Associate or a list of such names.
    (Default: all member levels are selected)
"""

from .exceptions import InvalidPriceRestriction, InvalidRestrictionPattern
from collections import namedtuple
import re

# Each restriction object contains an event registration type name, a regex
# pattern to search for in an event name, and a list of names of member levels
# allowed to register.

EventRestriction = namedtuple(
    "EventRestriction", "name pattern match_free_events match_paid_events member_levels"
)


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
        name = restriction.get("name", "Register")
        pattern = self.compile_pattern(restriction.get("pattern", "^"))
        match_free_events, match_paid_events = self.parse_price(
            restriction.get("price", "")
        )
        level_names = self.clean_level_names(restriction.get("levels", []))
        member_levels = self.lookup_member_levels(level_names)
        return EventRestriction(
            name, pattern, match_free_events, match_paid_events, member_levels
        )

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
    def parse_price(price_restriction):
        """Parse the price restriction (free, paid, or blank) and return flags
        to match free and paid events."""
        match_free_events = True
        match_paid_events = True
        if price_restriction == "free":
            match_paid_events = False
        elif price_restriction == "paid":
            match_free_events = False
        elif price_restriction != "":
            message = f'Event price restriction "{price_restriction}" must be "free", "paid", or omitted'
            raise InvalidPriceRestriction(message)
        return match_free_events, match_paid_events

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
