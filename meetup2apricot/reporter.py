"""Reports added events, registration types, and photos."""

import sys


class EventReport:

    """Details about one event for reporting."""

    def __init__(self):
        """Initialize with no Wild Apricot event, photo name, or registration
        types."""
        self.apricot_event = None
        self.photo_name = None
        self.registration_types = []

    def add_event(self, apricot_event):
        """Add a Wild Apricot event to the report."""
        self.apricot_event = apricot_event

    def add_registration_type(self, registration_type):
        """Add an event registration type to the report."""
        self.registration_types.append(registration_type)

    def add_photo_name(self, photo_name):
        """Add a photo name to the report."""
        self.photo_name = photo_name

    def report_event(self, output):
        """Report an event to an output stream."""
        output.write(
            f"{self.apricot_event.name}\n"
            f"    {self.apricot_event.start_date:%Y-%m-%d %H:%M} "
            f"to {self.apricot_event.end_date:%Y-%m-%d %H:%M}\n"
        )

    def report_photo_name(self, output):
        """Report a photo name to an output stream."""
        if self.photo_name:
            output.write(f"    Downloaded {self.photo_name}\n")

    def report_registration_type(self, output, reg_type):
        """Report an event registration type to an output stream."""
        output.write(
            f"    {reg_type.name:<12}   ${reg_type.price:6,.2f}"
            f"   {reg_type.display_count}\n"
        )

    def report_registration_types(self, output):
        """Report all event registration types to an output stream."""
        for reg_type in self.registration_types:
            self.report_registration_type(output, reg_type)

    def report(self, output):
        """Report an event and associated data to an output stream."""
        self.report_event(output)
        self.report_photo_name(output)
        self.report_registration_types(output)


class Reporter:

    """Reports added events, registration types, and photos to an output
    stream."""

    def __init__(self, output):
        """Initialize with an output stream (an open file, stdout, etc.)."""
        self.output = output
        self.event_report = EventReport()

    def report_event(self, apricot_event):
        """Add an event to the report."""
        self.event_report.add_event(apricot_event)

    def report_registration_type(self, registration_type):
        """Add an event registration type to the report."""
        self.event_report.add_registration_type(registration_type)

    def report_photo_name(self, photo_name):
        """Add a photo name to the report."""
        self.event_report.add_photo_name(photo_name)

    def report(self):
        """Report an event and associated data to an output stream."""
        self.event_report.report(self.output)
        self.event_report = EventReport()


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


def make_reporter(report_flag):
    """Make a real or null reporter depending on the report flag."""
    if report_flag:
        return Reporter(sys.stdout)
    else:
        return NullReporter()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
