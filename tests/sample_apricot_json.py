"""Sample JSON-ready data for testing."""

EXPECTED_FREE_PHOTO_NAME = "TEST_ETL_AC_Mending_Monday_2020-11-09"

EXPECTED_FREE_PHOTO_PATH = f"/resources/Pictures/EventAnnouncements/{EXPECTED_FREE_PHOTO_NAME}"

EXPECTED_TAGS = ["meetup", "test"]

EXPECTED_FREE_DESCRIPTION_HTML = \
f"<p><img src=\"{EXPECTED_FREE_PHOTO_PATH}\" " \
"alt=\"\" title=\"\" border=\"0\"></p>" \
"<p>Mending Mondays is an opportunity to gather " \
"to restore ripped seams, etc.</p><p>Nova Labs previously announced this " \
"event on <a " \
'href="https://www.meetup.com/NOVA-Makers/events/pfsbvrybcpbmb/">Meetup.com</a>.</p>'

EXPECTED_FREE_EVENT_JSON = {
    "Name": "AC: Mending Monday (Test Event)",
    "EventType": "Regular",
    "StartDate": "2020-11-09 19:00-05:00",
    "StartTimeSpecified": True,
    "EndDate": "2020-11-09 21:00-05:00",
    "EndTimeSpecified": True,
    "Location": "Online event",
    "RegistrationEnabled": True,
    "Tags": EXPECTED_TAGS,
    "Details": {
        "DescriptionHtml": EXPECTED_FREE_DESCRIPTION_HTML,
        "AccessControl": {
            "AccessLevel": "Public"
            },
        "PaymentMethod": "OnlineOnly"
        }
    }

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
