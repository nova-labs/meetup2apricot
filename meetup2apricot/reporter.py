"""Reports added events, registration types, and photos."""


class EventReport:

    """Details about one event for reporting."""

    def __init__(self, show_meetup_id):
        """Initialize with a "show Meetup event ID" flag and no Wild Apricot
        event or registration types."""
        self.show_meetup_id = show_meetup_id
        self.apricot_event = None
        self.registration_types = []

    def add_event(self, apricot_event):
        """Add a Wild Apricot event to the report."""
        self.apricot_event = apricot_event

    def add_registration_type(self, registration_type):
        """Add an event registration type to the report."""
        self.registration_types.append(registration_type)

    def report_event_name(self, output):
        """Report an event name to an output stream."""
        if self.show_meetup_id:
            output.write(f"{self.apricot_event.meetup_id}: ")
        output.write(f"{self.apricot_event.name}\n")

    def report_event_dates(self, output):
        """Report an event dates to an output stream."""
        start_date = self.apricot_event.start_date
        end_date = self.apricot_event.end_date
        start_date_format = f"    {start_date:%Y-%m-%d %H:%M} to "
        if start_date.date() == end_date.date():
            end_date_format = f"{end_date:%H:%M}\n"
        else:
            end_date_format = f"{end_date:%Y-%m-%d %H:%M}\n"
        output.write(start_date_format + end_date_format)

    def report_event(self, output):
        """Report an event to an output stream."""
        self.report_event_name(output)
        self.report_event_dates(output)

    def report_registration_type(self, output, reg_type):
        """Report an event registration type to an output stream."""
        output.write(
            f"    {reg_type.name:<15}   ${reg_type.price:6,.2f}"
            f"   {reg_type.display_count}\n"
        )

    def report_registration_types(self, output):
        """Report all event registration types to an output stream."""
        for reg_type in self.registration_types:
            self.report_registration_type(output, reg_type)

    def report(self, output):
        """Report an event and associated data to an output stream."""
        self.report_event(output)
        self.report_registration_types(output)


class Reporter:

    """Reports added events, registration types, and photos to an output
    stream."""

    def __init__(self, output, event_report_provider):
        """Initialize with an output stream (an open file, stdout, etc.) and an
        event report provider."""
        self.output = output
        self.event_report_provider = event_report_provider
        self.event_report = event_report_provider()
        self.photo_names = []

    def report_event(self, apricot_event):
        """Add an event to the report."""
        self.event_report.add_event(apricot_event)

    def report_registration_type(self, registration_type):
        """Add an event registration type to the report."""
        self.event_report.add_registration_type(registration_type)

    def report_photo_name(self, photo_name):
        """Add a photo name to the list."""
        self.photo_names.append(photo_name)

    def report(self):
        """Report an event and associated data to an output stream."""
        self.event_report.report(self.output)
        self.output.write("\n")
        self.event_report = self.event_report_provider()

    def report_downloads(self):
        """Report the list of photos downloaded."""
        self.photo_names.sort()
        for photo_name in self.photo_names:
            self.output.write(f"{photo_name}\n")


class NullReporter:

    """Ignores requests to report added events, registration types, and photos."""

    def report_event(self, apricot_event):
        """Ignore reporting an event to the report."""
        pass

    def report_registration_type(self, registration_type):
        """Ignore reporting an event registration type to the report."""
        pass

    def report_photo_name(self, photo_name):
        """Ignore reporting a photo name to the report."""
        pass

    def report(self):
        """Ignore reporting an event and associated data."""
        pass

    def report_downloads(self):
        """Ignore reporting the list of photos downloaded."""
        pass


def make_reporter(report_flag, reporter_provider):
    """Make a real or null reporter depending on the report flag."""
    if report_flag:
        return reporter_provider()
    else:
        return NullReporter()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
