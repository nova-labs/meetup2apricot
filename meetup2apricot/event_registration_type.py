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
            "GuestRegistrationPolicy": "NumberOfGuests",
            "UnavailabilityPolicy": "ShowDisabled",
            "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
            "CancellationDaysBeforeEvent": 2,
            "IsWaitlistEnabled": True,
        } | self.more_attributes


class EventRegistrationTypeMaker:

    """Makes various event registration types."""

    def __init__(self, membership_levels, event_restrictions=None):
        """Initialize with a list of all membership levels and a list of event
        restrictions."""
        self.membership_levels = membership_levels
        self.event_restrictions = event_restrictions

    def make_meetup_registration_type(self, event_id, maximum_registrants_count):
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

    def make_unrestricted_apricot_registration_type(
        self, event_id, maximum_registrants_count, price
    ):
        """Make an unrestricted event registration type for Wild Apricot RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="RSVP",
            price=price,
            maximum_registrants_count=maximum_registrants_count,
        )

    def make_members_only_registration_type(
        self, event_id, maximum_registrants_count, price
    ):
        """Make an event registration type for members only RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="Members Only",
            price=price,
            availability="MembersOnly",
            maximum_registrants_count=maximum_registrants_count,
            AvailableForMembershipLevels=self.membership_levels,
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
