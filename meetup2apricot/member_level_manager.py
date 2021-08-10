"""Provides complete and partial lists of member levels."""

from .exceptions import UnknownMemberLevelName
from collections import namedtuple

# Member level fields names correspond to Wild Apricot API JSON keys.
MemberLevel = namedtuple("MemberLevel", "Id Url")


class MemberLevelManager:

    """Provides complete and partial lists of member levels."""

    def __init__(self, named_levels=None):
        """Initialize, optionally with a list of all member levels and a mapping of level
        names to member levels for testing."""
        self._named_levels = named_levels or {}

    def add_level(self, name, level):
        """Add a named level."""
        self._named_levels[name] = level

    def named_level(self, name):
        """Return the named member level."""
        if name in self._named_levels:
            return self._named_levels[name]
        else:
            raise UnknownMemberLevelName(f"Unknown member level name {name!r}")

    def named_levels(self, names):
        """Given a list of member level names, return a list of corresponding
        member levels."""
        return [self.named_level(name) for name in names]


def make_member_level_manager(json_member_levels):
    """Make a member level manager from Wild Apricot's JSON structured member levels."""
    manager = MemberLevelManager()
    for level in json_member_levels:
        manager.add_level(level["Name"], MemberLevel(level["Id"], level["Url"]))
    return manager


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
