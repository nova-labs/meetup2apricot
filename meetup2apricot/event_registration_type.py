"""Wild Apricot event registration types for free and paid registrations."""


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
            "GuestRegistrationPolicy": "Disabled",
            "UnavailabilityPolicy": "ShowDisabled",
            "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
            "CancellationDaysBeforeEvent": 2,
            "IsWaitlistEnabled": True,
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
            name="Meetup RSVP",
            is_enabled=False,
            description="RSVPs on Meetup",
            price=0.0,
            maximum_registrants_count=maximum_registrants_count,
            max_reg_count_desc="registered on Meetup",
        )

    def make_apricot_type(
        self, event_id, maximum_registrants_count, price, event_title
    ):
        """Make a Wild Apricot event regirstation type appropriate for an event
        title."""
        restriction = self.choose_event_restriction(event_title)
        if restriction:
            return self.make_restricted_apricot_type(
                event_id, maximum_registrants_count, price, restriction
            )
        else:
            return self.make_unrestricted_apricot_type(
                event_id, maximum_registrants_count, price
            )

    def make_unrestricted_apricot_type(
        self, event_id, maximum_registrants_count, price
    ):
        """Make an unrestricted event registration type for Wild Apricot RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="RSVP",
            price=price,
            maximum_registrants_count=maximum_registrants_count,
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
        )

    def choose_event_restriction(self, event_title):
        """Choose and return the first event restriction with a pattern that
        matches the event title. Return None if no patterns match."""
        for restriction in self.event_restrictions:
            if restriction.pattern.search(event_title):
                return restriction
        return None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
