"""Test the event reports and the reporter."""

from meetup2apricot.event_registration_type import EventRegistrationTypeMaker
from meetup2apricot.meetup_to_apricot_event_adaptor import MeetupToApricotEventAdaptor
from meetup2apricot.reporter import EventReport, Reporter, NullReporter, make_reporter
from .sample_apricot_json import EXPECTED_FREE_PHOTO_PATH, EXPECTED_FREE_TAGS
from datetime import datetime
import io
import pytest

EXPECTED_FREE_EVENT_NAME = "AC: Mending Monday (Test Event)\n"
EXPECTED_FREE_EVENT_DATES = "    2020-11-09 19:00 to 21:00\n"
EXPECTED_LONGER_FREE_EVENT_DATES = "    2020-11-09 19:00 to 2020-11-10 01:00\n"

EXPECTED_FREE_EVENT_REPORT = EXPECTED_FREE_EVENT_NAME + EXPECTED_FREE_EVENT_DATES
EXPECTED_LONGER_FREE_EVENT_REPORT = (
    EXPECTED_FREE_EVENT_NAME + EXPECTED_LONGER_FREE_EVENT_DATES
)

EXPECTED_MEETUP_RSVP_FREE = "    Meetup RSVP    $  0.00   0 registered on Meetup\n"
EXPECTED_MEMBERS_ONLY_FREE = "    Members Only   $125.00   6 available\n"


@pytest.fixture()
def output():
    """Return a string output stream."""
    return io.StringIO()


@pytest.fixture()
def free_apricot_event(free_meetup_event):
    """Return a free Wild Apricot event."""
    return MeetupToApricotEventAdaptor(
        free_meetup_event, EXPECTED_FREE_PHOTO_PATH, EXPECTED_FREE_TAGS
    )


@pytest.fixture()
def longer_free_apricot_event(longer_free_meetup_event):
    """Return a longer free Wild Apricot event."""
    return MeetupToApricotEventAdaptor(
        longer_free_meetup_event, EXPECTED_FREE_PHOTO_PATH, EXPECTED_FREE_TAGS
    )


@pytest.fixture()
def event_report():
    """Return an empty event report."""
    return EventReport()


@pytest.fixture()
def reporter(output):
    """Return a reporter that writes to a string."""
    return Reporter(output)


@pytest.fixture()
def event_registration_type_maker():
    """Return an event registration type maker."""
    return EventRegistrationTypeMaker([])


def test_report_event(event_report, free_apricot_event, output):
    """Test reporting on an event."""
    event_report.add_event(free_apricot_event)
    event_report.report_event(output)
    assert output.getvalue() == EXPECTED_FREE_EVENT_REPORT


def test_report_event_longer(event_report, longer_free_apricot_event, output):
    """Test reporting on an event."""
    event_report.add_event(longer_free_apricot_event)
    event_report.report_event(output)
    assert output.getvalue() == EXPECTED_LONGER_FREE_EVENT_REPORT


def test_report_registration_type_rsvp(
    event_report, event_registration_type_maker, output
):
    """Test reporting on an RSVP event registration type."""
    reg_type = event_registration_type_maker.make_apricot_registration_type(
        event_id=12345, maximum_registrants_count=None, price=25.0
    )
    event_report.report_registration_type(output, reg_type)
    assert output.getvalue() == "    RSVP           $ 25.00   unlimited\n"


def test_report_registration_type_meetup(
    event_report, event_registration_type_maker, output
):
    """Test reporting on a Meetup event registration type."""
    reg_type = event_registration_type_maker.make_meetup_registration_type(
        event_id=12345, maximum_registrants_count=0
    )
    event_report.report_registration_type(output, reg_type)
    assert output.getvalue() == EXPECTED_MEETUP_RSVP_FREE


def test_report_registration_type_members_only(
    event_report, event_registration_type_maker, output
):
    """Test reporting on a Meetup event registration type."""
    reg_type = event_registration_type_maker.make_members_only_registration_type(
        event_id=12345, maximum_registrants_count=6, price=125.0
    )
    event_report.report_registration_type(output, reg_type)
    assert output.getvalue() == EXPECTED_MEMBERS_ONLY_FREE


def test_report_registration_types(event_report, event_registration_type_maker, output):
    """Test reporting on a multiple event registration types."""
    reg_type_1 = event_registration_type_maker.make_meetup_registration_type(
        event_id=12345, maximum_registrants_count=0
    )
    reg_type_2 = event_registration_type_maker.make_members_only_registration_type(
        event_id=12345, maximum_registrants_count=6, price=125.0
    )
    event_report.add_registration_type(reg_type_1)
    event_report.add_registration_type(reg_type_2)
    event_report.report_registration_types(output)
    assert output.getvalue() == EXPECTED_MEETUP_RSVP_FREE + EXPECTED_MEMBERS_ONLY_FREE


def test_report(reporter, free_apricot_event, event_registration_type_maker, output):
    """Test reporting an event, its photo, and its registration types."""
    reg_type_1 = event_registration_type_maker.make_meetup_registration_type(
        event_id=12345, maximum_registrants_count=0
    )
    reg_type_2 = event_registration_type_maker.make_members_only_registration_type(
        event_id=12345, maximum_registrants_count=6, price=125.0
    )
    reporter.report_event(free_apricot_event)
    reporter.report_photo_name("sample.jpg")
    reporter.report_registration_type(reg_type_1)
    reporter.report_registration_type(reg_type_2)
    reporter.report()
    assert (
        output.getvalue()
        == EXPECTED_FREE_EVENT_REPORT
        + EXPECTED_MEETUP_RSVP_FREE
        + EXPECTED_MEMBERS_ONLY_FREE
        + "\n"
    )


def test_report_no_photo(
    reporter, free_apricot_event, event_registration_type_maker, output
):
    """Test reporting an event without a photo and its registration types."""
    reg_type_1 = event_registration_type_maker.make_meetup_registration_type(
        event_id=12345, maximum_registrants_count=0
    )
    reg_type_2 = event_registration_type_maker.make_members_only_registration_type(
        event_id=12345, maximum_registrants_count=6, price=125.0
    )
    reporter.report_event(free_apricot_event)
    reporter.report_registration_type(reg_type_1)
    reporter.report_registration_type(reg_type_2)
    reporter.report()
    assert (
        output.getvalue()
        == EXPECTED_FREE_EVENT_REPORT
        + EXPECTED_MEETUP_RSVP_FREE
        + EXPECTED_MEMBERS_ONLY_FREE
        + "\n"
    )


def test_report_downloads(reporter, output):
    """Test reporting downloaded photos in sorted order."""
    reporter.report_photo_name("photo2.jpg")
    reporter.report_photo_name("photo1.png")
    reporter.report_downloads()
    assert output.getvalue() == "photo1.png\nphoto2.jpg\n"


def test_null_reporter(free_apricot_event, event_registration_type_maker, output):
    """Test reporting an event, its photo, and its registration types to the null reporter."""
    reporter = NullReporter()
    reg_type_1 = event_registration_type_maker.make_meetup_registration_type(
        event_id=12345, maximum_registrants_count=0
    )
    reg_type_2 = event_registration_type_maker.make_members_only_registration_type(
        event_id=12345, maximum_registrants_count=6, price=125.0
    )
    reporter.report_event(free_apricot_event)
    reporter.report_photo_name("sample.jpg")
    reporter.report_registration_type(reg_type_1)
    reporter.report_registration_type(reg_type_2)
    reporter.report()


def test_make_reporter():
    """Test making a reporter with a true report flag."""
    reporter = make_reporter(True)
    assert type(reporter) == Reporter


def test_make_reporter_null():
    """Test making a reporter with a false report flag."""
    reporter = make_reporter(False)
    assert type(reporter) == NullReporter


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
