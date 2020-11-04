"""Sample JSON-ready data for testing."""

EXPECTED_DESCRIPTION_HTML = "<p>Mending Mondays is an opportunity to gather " \
"to restore ripped seams, etc.</p><p>Nova Labs previously announced this " \
"event on <a " \
'href="https://www.meetup.com/NOVA-Makers/events/pfsbvrybcpbmb/">Meetup.com</a>.</p>'

EXPECTED_FREE_EVENT_JSON = {
    "Name": "TEST-ETL: AC: Mending Monday",
    "EventType": "Regular",
    "StartDate": "2020-11-09 19:00-05:00",
    "StartTimeSpecified": True,
    "EndDate": "2020-11-09 21:00-05:00",
    "EndTimeSpecified": True,
    "Location": "Online event",
    "RegistrationEnabled": True,
    "Details": {
        "DescriptionHtml": EXPECTED_DESCRIPTION_HTML,
        "AccessControl": {
            "AccessLevel": "Public"
            }
        }
    }

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
