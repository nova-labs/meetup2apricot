"""Sample JSON-ready data for testing."""

EXPECTED_FREE_PHOTO_NAME = "TEST_ETL_AC_Mending_Monday_2020-11-09"

EXPECTED_FREE_PHOTO_PATH = (
    f"/resources/Pictures/EventAnnouncements/{EXPECTED_FREE_PHOTO_NAME}"
)

EXPECTED_TAGS = ["meetup", "test"]

EXPECTED_FREE_TAGS = ["arts-and-crafts", "the-studio", "meetup", "test"]

EXPECTED_FREE_DESCRIPTION_HTML = (
    f'<p><img src="{EXPECTED_FREE_PHOTO_PATH}" '
    'alt="" title="" border="0"></p>'
    "<p>Mending Mondays is an opportunity to gather "
    "to restore ripped seams, etc.</p><p>Nova Labs previously announced this "
    "event on <a "
    'href="https://www.meetup.com/NOVA-Makers/events/pfsbvrybcpbmb/">'
    "Meetup.com</a>.</p>"
)

EXPECTED_FREE_EVENT_JSON = {
    "Name": "AC: Mending Monday (Test Event)",
    "EventType": "Regular",
    "StartDate": "2020-11-09 19:00-05:00",
    "StartTimeSpecified": True,
    "EndDate": "2020-11-09 21:00-05:00",
    "EndTimeSpecified": True,
    "Location": "Online event",
    "RegistrationEnabled": True,
    "Tags": EXPECTED_FREE_TAGS,
    "Details": {
        "DescriptionHtml": EXPECTED_FREE_DESCRIPTION_HTML,
        "AccessControl": {
            "AccessLevel": "Public",
            "AvailableForAnyLevel": True,
            "AvailableForAnyGroup": True,
        },
        "PaymentMethod": "OnlineOnly",
        "IsWaitlistEnabled": True,
        "WaitlistSettings": {
            "WaitlistType": "Manual",
            "InformationToCollect": "ContactInformation",
        },
        "AttendeesDisplaySettings": {
            "VisibleTo": "Members",
            "ShowPendingAttendees": False,
        },
    },
}

EXPECTED_PAID_DESCRIPTION_HTML = (
    "<p>Get information about how to manage multiple cameras, set up OBS, and run "
    "smoother streaming for that great online class or steaming experience. Ask "
    "about which equipment to buy and how to set up with your current equipment for "
    "the best effect.</p> <p>**Refund and Events Policy: <a "
    'href="https://www.nova-labs.org/class-and-event-policies/" '
    'class="linkified">https://www.nova-labs.org/class-and-event-policies/</a></p> '
    "<p>Nova Labs previously announced this event on <a "
    'href="https://www.meetup.com/NOVA-Makers/events/274139316/">Meetup.com</a>.</p>'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
