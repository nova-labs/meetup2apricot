"""Wild Apricot event registration types for free and paid registrations."""


class EventRegistrationType:

    """Holds data needed to add event registration types to Wild Apricot."""

    def __init__(
        self, event_id, name, is_enabled, description, price, maximum_registrants_count
    ):
        """Initialize with parameters from thw Wild Apricot API."""
        self.event_id = event_id
        self.name = name
        self.is_enabled = is_enabled
        self.description = description
        self.price = price
        self.maximum_registrants_count = maximum_registrants_count

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
            "Availability": "Everyone",
            "MaximumRegistrantsCount": self.maximum_registrants_count,
            "GuestRegistrationPolicy": "NumberOfGuests",
            "UnavailabilityPolicy": "ShowDisabled",
            "CancellationBehaviour": "AllowUpToPeriodBeforeEvent",
            "CancellationDaysBeforeEvent": 2,
            "IsWaitlistEnabled": True,
        }


class EventRegistrationTypeMaker:

    """Makes various event registration types."""

    def __init__(self, membership_levels):
        """Initialize with a list of all membership levels."""
        self.membership_levels = membership_levels

    def make_meetup_registration_type(self, event_id, maximum_registrants_count):
        """Make an event registration type for existing Meetup RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="Meetup RSVP",
            is_enabled=False,
            description="RSVPs on Meetup",
            price=0.0,
            maximum_registrants_count=maximum_registrants_count,
        )

    def make_apricot_registration_type(
        self, event_id, maximum_registrants_count, price
    ):
        """Make an event registration type for Wild Apricot RSVPs."""
        return EventRegistrationType(
            event_id=event_id,
            name="RSVP",
            is_enabled=True,
            description="",
            price=price,
            maximum_registrants_count=maximum_registrants_count,
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
