"""Wild Apricot event registration types for free and paid registrations."""

from .exceptions import NoRestrictionsMatchError


class EventRegistrationType:

    """Holds data needed to add event registration types to Wild Apricot."""

    def __init__(
        self,
        event_id,
        name,
        price,
        maximum_registrants_count,
        max_reg_count_desc="available",
        is_enabled=True,
        description="",
        availability="Everyone",
        guest_registration_policy="Disabled",
        **more_attributes,
    ):
        """Initialize with parameters for the Wild Apricot API."""
        self.event_id = event_id
        self.name = name
        self.price = price
        self.maximum_registrants_count = maximum_registrants_count
        self.max_reg_count_desc = max_reg_count_desc
        self.is_enabled = is_enabled
        self.description = description
        self.availability = availability
        self.more_attributes = more_attributes
        self.guest_registration_policy = guest_registration_policy

    @property
    def display_count(self):
        """Return the maximum registrants count formatted for reporting."""
        if self.maximum_registrants_count is None:
            return "unlimited"
        else:
            return f"{self.maximum_registrants_count:d} {self.max_reg_count_desc}"

    def for_json(self):
        """Structure this event registration type into dictionaries and lists
        suitable for conversion to JSON."""
        return {
            "EventId": self.event_id,
            "Name": self.name,
            "IsEnabled": self.is_enabled,
            "Description": self.description,
            "BasePrice": self.price,
            "GuestPrice": self.price,
            "Availability": self.availability,
            "MaximumRegistrantsCount": self.maximum_registrants_count,
            "GuestRegistrationPolicy": self.guest_registration_policy,
            "UnavailabilityPolicy": "ShowDisabled",
            "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
            "CancellationDaysBeforeEvent": 2,
            "IsWaitlistEnabled": False,
        } | self.more_attributes


class EventRegistrationTypeMaker:

    """Makes various event registration types."""

    def __init__(self, event_restrictions):
        """Initialize with a list of event restrictions."""
        self.event_restrictions = event_restrictions

    def make_meetup_type(self, event_id, maximum_registrants_count):
        """Make an event registration type for existing Meetup RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="Instructor/Host",
            is_enabled=False,
            description="RSVPs on Meetup",
            price=0.0,
            maximum_registrants_count=maximum_registrants_count,
            max_reg_count_desc="available",
        )

    def make_apricot_type(
        self, event_id, maximum_registrants_count, price, event_title
    ):
        """Make a Wild Apricot event regirstation type appropriate for an event
        title."""
        restriction = self.choose_event_restriction(event_title, price)
        if restriction.member_levels:
            return self.make_restricted_apricot_type(
                event_id, maximum_registrants_count, price, restriction
            )
        else:
            return self.make_unrestricted_apricot_type(
                event_id, maximum_registrants_count, price, restriction
            )

    def make_unrestricted_apricot_type(
        self, event_id, maximum_registrants_count, price, restriction
    ):
        """Make an unrestricted event registration type for Wild Apricot RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name=restriction.name,
            price=price,
            maximum_registrants_count=maximum_registrants_count,
            guest_registration_policy=restriction.guest_policy,
        )

    def make_restricted_apricot_type(
        self, event_id, maximum_registrants_count, price, restriction
    ):
        """Make a restricted event registration type for Wild Apricot
        registrations."""
        member_levels_for_json = [
            level._asdict() for level in restriction.member_levels
        ]
        return EventRegistrationType(
            event_id=event_id,
            name=restriction.name,
            price=price,
            availability="MembersOnly",
            maximum_registrants_count=maximum_registrants_count,
            AvailableForMembershipLevels=member_levels_for_json,
            guest_registration_policy=restriction.guest_policy,
        )

    def choose_event_restriction(self, event_title, price):
        """Choose and return the first event restriction with a pattern that
        matches the event title and price category.  Note that the event
        restriction list ends with a default that should match all events."""
        for restriction in self.event_restrictions:
            if restriction.pattern.search(event_title) and restriction.matches_price(
                price
            ):
                return restriction
        message = f"Bug: No restrictions match {event_title=!r} {price=}"
        raise NoRestrictionsMatchError(message)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
