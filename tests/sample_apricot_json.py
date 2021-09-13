"""Sample JSON-ready data for testing."""

EXPECTED_FREE_PHOTO_NAME = "TEST_ETL_AC_Mending_Monday_2020-11-09"

EXPECTED_FREE_PHOTO_PATH = (
    f"/resources/Pictures/EventAnnouncements/{EXPECTED_FREE_PHOTO_NAME}"
)

EXPECTED_TAGS = ["meetup", "test"]

EXPECTED_FREE_TAGS = ["meetup", "test", "AC", "arts-and-crafts", "the-studio"]

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
        "GuestRegistrationSettings": {
            "CreateContactMode": "CreateContactForGuestsWithEmail"
        },
        "PaymentMethod": "OnlineOnly",
        "RegistrationConfirmationExtraInfo": "How to find us: "
        "https://zoom.us/j/92758362882?pwd=a2VJOGxyOTBqelNhdjY1dGpqZStjZz09",
        "IsWaitlistEnabled": False,
        "WaitlistSettings": {
            "WaitlistType": "None",
            "InformationToCollect": "None",
        },
        "AttendeesDisplaySettings": {
            "VisibleTo": "Members",
            "ShowPendingAttendees": False,
        },
    },
    "RegistrationsLimit": None,
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

EXPECTED_PAID_EVENT_JSON = {
    "Details": {
        "AccessControl": {
            "AccessLevel": "Public",
            "AvailableForAnyGroup": True,
            "AvailableForAnyLevel": True,
        },
        "AttendeesDisplaySettings": {
            "ShowPendingAttendees": False,
            "VisibleTo": "Members",
        },
        "DescriptionHtml": EXPECTED_PAID_DESCRIPTION_HTML,
        "GuestRegistrationSettings": {
            "CreateContactMode": "CreateContactForGuestsWithEmail"
        },
        "IsWaitlistEnabled": False,
        "PaymentMethod": "OnlineOnly",
        "RegistrationConfirmationExtraInfo": "",
        "WaitlistSettings": {
            "InformationToCollect": "None",
            "WaitlistType": "None",
        },
    },
    "EndDate": "2020-11-13 21:00-05:00",
    "EndTimeSpecified": True,
    "EventType": "Regular",
    "Location": "Nova Labs Inc., 1916 Isaac Newton Square W, Reston, VA 20190",
    "Name": "AV_P: Online Instructor Training-Video equipment setup, streaming, "
    "OBS/Zoom tips (Members Only) (Test Event)",
    "RegistrationEnabled": True,
    "RegistrationsLimit": 6,
    "StartDate": "2020-11-13 19:00-05:00",
    "StartTimeSpecified": True,
    "Tags": ["meetup", "test"],
}


SAMPLE_MEMBERSHIP_LEVEL_JSON = [
    {
        "ApplicationReview": {"AdminApprovalRequired": True, "PrepayRequired": False},
        "AutomaticRecurringPayments": False,
        "Description": "Associates receive access to space during open hours. \r\n\r\n\r\n",
        "Id": 1206421,
        "MembershipFee": 0.0,
        "Name": "Associate (legacy-billing)",
        "PublicCanApply": False,
        "RenewalPeriod": {"Kind": "Never"},
        "Type": "Individual",
        "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206421",
    },
    {
        "ApplicationReview": {"AdminApprovalRequired": True, "PrepayRequired": True},
        "AutomaticRecurringPayments": False,
        "Description": "24x7 access to space\r\nPriority access to certain resources and events\r\nEligible for additional discounts for events\r\n",
        "Id": 1206426,
        "MembershipFee": 100.0,
        "Name": "Key",
        "PublicCanApply": False,
        "RenewalPeriod": {
            "Dates": [
                {"Day": 1, "Month": 1},
                {"Day": 1, "Month": 2},
                {"Day": 1, "Month": 3},
                {"Day": 1, "Month": 4},
                {"Day": 1, "Month": 5},
                {"Day": 1, "Month": 6},
                {"Day": 1, "Month": 7},
                {"Day": 1, "Month": 8},
                {"Day": 1, "Month": 9},
                {"Day": 1, "Month": 10},
                {"Day": 1, "Month": 11},
                {"Day": 1, "Month": 12},
            ],
            "Kind": "Monthly",
            "StartFromJoinDate": False,
        },
        "Type": "Individual",
        "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1206426",
    },
    {
        "ApplicationReview": {"AdminApprovalRequired": False, "PrepayRequired": True},
        "AutomaticRecurringPayments": False,
        "Description": "Temporary level used during initial migration",
        "Id": 1207614,
        "MembershipFee": 0.0,
        "Name": "NL Member",
        "PublicCanApply": False,
        "RenewalPeriod": {"Kind": "Never"},
        "Type": "Individual",
        "Url": "https://api.wildapricot.org/v2.2/accounts/335649/MembershipLevels/1207614",
    },
]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
