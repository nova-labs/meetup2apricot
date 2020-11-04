"""Wrap a Meetup event to appear as a Wild Apricot event."""

class MeetupToApricotEventAdaptor:

    """Adapts meetup events to provide Wild Apricot event fields."""

    def __init__(self, meetup_event):
        """Initialize with a Meetup event."""
        self._meetup_event = meetup_event

    @property
    def name(self):
        """Return the event title."""
        return self._meetup_event.name

    @property
    def event_type(self):
        """Return a flag that indicates if event is simple (RSVP) or
        regular. Enum: [ Reqular, RSVP ] """
        return "Regular"

    @property
    def start_date(self):
        """Return the date and time when the event is scheduled to start. If no
        time offset is specified, counts as UTC and will be converted into
        event timezone."""
        return self._meetup_event.start_time

    @property
    def start_time_specified(self):
        """Return a flag that indicates if event start time is specified. False
        means that StartDate contains only date component."""
        return True

    @property
    def end_date(self):
        """Return the date and time when the event is scheduled to end. Could
        be empty. If no time offset is specified, counts as UTC and will be
        converted into event timezone."""
        return self._meetup_event.end_time

    @property
    def end_time_specified(self):
        """Return a flag that indicates if event end time is specified. False
        means that EndDate contains only date component."""
        return True

    @property
    def location(self):
        """Return the location where the event will take place."""
        partial_address = ", ".join(filter(None, [
                self._meetup_event.venue.name,
                self._meetup_event.venue.address,
                self._meetup_event.venue.city,
                self._meetup_event.venue.state]))
        return " ".join(filter(None, [
                partial_address,
                self._meetup_event.venue.zipcode]))

    @property
    def registration_enabled(self):
        """Return a flag that indicates that registration to this event is
        enabled."""
        return True

    @property
    def registrations_limit(self):
        """Return the maximum number of registrations for this event."""
        return self._meetup_event.rsvp_limit

    @property
    def access_level(self):
        """Return the event accessability."""
        return "Public"

    @staticmethod
    def format_date_for_json(date):
        """Adjust the date/time to the local time zone and ormat it for JSON as
        YYYY-MM-DD HH:MM+HH:MM."""
        return date.astimezone().isoformat(sep=' ', timespec='minutes')

    def for_json(self):
        """Structure this event into dictionaries and lists suitable for
        conversion to JSON."""
        return {
                "Name": self.name,
                "EventType": self.event_type,
                "StartDate": self.format_date_for_json(self.start_date),
                "StartTimeSpecified": self.start_time_specified,
                "EndDate": self.format_date_for_json(self.end_date),
                "EndTimeSpecified": self.end_time_specified,
                "StartTimeSpecified": self.start_time_specified,
                "Location": self.location,
                "RegistrationEnabled": self.registration_enabled,
                "Details": {
                    "AccessControl": {
                        "AccessLevel": self.access_level
                        }
                    }
                }


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
