"""Samples of Meetup event JSON."""

FREE_MEETUP_EVENT_JSON = """
    {
        "created": 1594000624000,
        "date_in_series_pattern": true,
        "description": "<p>Mending Mondays is an opportunity to gather to restore ripped seams, etc.</p> ",
        "duration": 7200000,
        "featured_photo": {
            "base_url": "https://secure.meetupstatic.com",
            "highres_link": "https://secure.meetupstatic.com/photos/event/6/b/4/9/highres_491187465.jpeg",
            "id": 491187465,
            "photo_link": "https://secure.meetupstatic.com/photos/event/6/b/4/9/600_491187465.jpeg",
            "thumb_link": "https://secure.meetupstatic.com/photos/event/6/b/4/9/thumb_491187465.jpeg",
            "type": "event"
        },
        "group": {
            "country": "us",
            "created": 1333912341000,
            "id": 3629072,
            "join_mode": "open",
            "lat": 38.959999084472656,
            "localized_location": "Reston, VA",
            "lon": -77.33999633789062,
            "name": "NOVA Labs",
            "region": "en_US",
            "state": "VA",
            "timezone": "US/Eastern",
            "urlname": "NOVA-Makers",
            "who": "Makers"
        },
        "how_to_find_us": "https://zoom.us/j/92758362882?pwd=a2VJOGxyOTBqelNhdjY1dGpqZStjZz09",
        "id": "pfsbvrybcpbmb",
        "is_online_event": true,
        "link": "https://www.meetup.com/NOVA-Makers/events/pfsbvrybcpbmb/",
        "local_date": "2020-11-09",
        "local_time": "19:00",
        "member_pay_fee": false,
        "name": "TEST-ETL: AC: Mending Monday",
        "series": {
            "description": "Every 2 weeks on Monday",
            "id": 44165671,
            "start_date": 1594008000000,
            "template_event_id": 0,
            "weekly": {
                "days_of_week": [
                    1
                ],
                "interval": 2
            }
        },
        "status": "upcoming",
        "time": 1604966400000,
        "updated": 1594000624000,
        "utc_offset": -18000000,
        "venue": {
            "country": "",
            "id": 26906060,
            "localized_country_name": "",
            "name": "Online event",
            "repinned": false
        },
        "visibility": "public",
        "waitlist_count": 0,
        "yes_rsvp_count": 3
    }
"""

PAID_MEETUP_EVENT_JSON = r"""
    {
        "created": 1603512050000,
        "date_in_series_pattern": false,
        "description": "<p>Get information about how to manage multiple cameras, set up OBS, and run smoother streaming for that great online class or steaming experience. Ask about which equipment to buy and how to set up with your current equipment for the best effect.</p> <p>**Refund and Events Policy: <a href=\"https://www.nova-labs.org/class-and-event-policies/\" class=\"linkified\">https://www.nova-labs.org/class-and-event-policies/</a></p> ",
        "duration": 7200000,
        "fee": {
            "accepts": "wepay",
            "amount": 20.0,
            "currency": "USD",
            "description": "",
            "label": "Price",
            "required": true
        },
        "group": {
            "country": "us",
            "created": 1333912341000,
            "id": 3629072,
            "join_mode": "open",
            "lat": 38.959999084472656,
            "localized_location": "Reston, VA",
            "lon": -77.33999633789062,
            "name": "NOVA Labs",
            "region": "en_US",
            "state": "VA",
            "timezone": "US/Eastern",
            "urlname": "NOVA-Makers",
            "who": "Makers"
        },
        "id": "274139316",
        "is_online_event": false,
        "link": "https://www.meetup.com/NOVA-Makers/events/274139316/",
        "local_date": "2020-11-13",
        "local_time": "19:00",
        "member_pay_fee": false,
        "name": "Test-ETL: AV_P: Online Instructor Training-Video equipment setup, streaming, OBS/Zoom tips",
        "rsvp_limit": 6,
        "status": "upcoming",
        "time": 1605312000000,
        "updated": 1603676407000,
        "utc_offset": -18000000,
        "venue": {
            "address_1": "1916 Isaac Newton Square W",
            "city": "Reston",
            "country": "us",
            "id": 27015523,
            "lat": 38.95444107055664,
            "localized_country_name": "USA",
            "lon": -77.33830261230469,
            "name": "Nova Labs Inc.",
            "repinned": false,
            "state": "VA",
            "zip": "20190"
        },
        "visibility": "public",
        "waitlist_count": 0,
        "yes_rsvp_count": 2
    }
"""
