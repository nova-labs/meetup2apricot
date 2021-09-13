=======
History
=======

~~~~~~~~~~~~~~
Future History
~~~~~~~~~~~~~~

* Update tags and member-only status of existing events.

~~~~~~~~~~~~~~
Recent History
~~~~~~~~~~~~~~

Next Release
------------------

* Make "Add new guests to contacts list only if email entered" the default for Wild Apricot events.

1.10.0 (2021-08-18)
------------------

* Upload event photos to Wild Apricot via WEBDAV.

1.9.0 (2021-08-10)
------------------

* Add registration restrictions based on price.
* Make guest registration policy configurable.

1.8.1 (2021-04-09)
------------------

* Provide only 1 instructor/host slot in Wild Apricot.

1.8.0 (2021-04-05)
------------------

* Ignore Meetup registrations. Provide 2 instructor/host slots in Wild Apricot.

1.7.0 (2021-03-25)
------------------

* Add --transfer command line option to transfer selected Meetup events.
* Allow multiple Meetup event IDs with a --skip command line option.

1.6.0 (2021-03-24)
------------------

* Add --skip command line option to skip Meetup events.

1.5.1 (2021-02-21)
------------------

* Turn off event waitlist.

1.5.0 (2021-02-19)
------------------

* Select Meetup events to download by listing their IDs on the command line.

1.4.1 (2021-02-11)
------------------

* Add accounting code from title to list of event tags.
* Rename "Meetup RSVP" registration type to "Instructor/Host".
* Disable guest registration due to COVID-19.
* Report and limit oversubscribed Meetup events.
* Add -m flag to show Meetup event IDs in reports.

1.4.0 (2020-11-29)
------------------

* Make event registration type member level restrictions configurable.
* Show end time without date when end data matches start date.
* List downloaded photos at the end of a report.

1.3.2 (2020-11-23)
------------------

* Add registrations limit to Wild Apricot events.
* Work around imghdr bug of not recognizing some jpeg images.

1.3.1 (2020-11-22)
------------------

* Label availability counts in reports.

1.3.0 (2020-11-21)
------------------

* Report added events, regristration types, and photos.

1.2.2 (2020-11-20)
------------------

* For "members only" events, restrict registrations instead of event visibility.
* Document how to run meetup2apricot.

1.2.1 (2020-11-18)
------------------

* Detect photo file type by inspection; Meetup always claims jpeg.

1.2.0 (2020-11-18)
------------------

* Restrict registrations for events labeled members only.
* Show Meetup's "how to find us" as extra info for registrants.
* Accept multiple accounting codes from event title.
* Tag featured events.
* Limit processed events by latest start date.

1.1.0 (2020-11-17)
------------------

* Handle changes to Meetup event IDs.
* Throttle Meetup API requests based on response headers.
* Add dry run capability.
* Improve documentation.

1.0.3 (2020-11-13)
------------------

* Link to documentation at readthedocs.io.

1.0.2 (2020-11-13)
------------------

* Improve documentation.
* Improve installation.

1.0.1 (2020-11-10)
------------------

* Reformat source code with black for PEP 8 conformance.
* Correct style, import, and other issues reported by flake8 for PEP 8 conformance.

1.0.0 (2020-11-08)
------------------

* Turn on waitlist with manual processing.
* Collect guest counts, but no personal information.
* Throttle Wild Apricot requests.
* Allow members to see the list of event registrants.

0.2.0 (2020-11-08)
------------------

* Tag events based on accounting code.

0.1.1 (2020-11-08)
------------------

* Restrict event payments to online only.
* Apply a configurable list of tags to all Wild Apricot events.

0.1.0 (2020-11-08)
------------------

* Copy events from Meetup to Wild Apricot.
* Add capacity limited event reservation types to Wild Apricot.
* Download photos from Meetup to local directory.

0.0.1 (2020-10-28)
------------------

* Setup basic project files.

0.0.0 (2020-10-26)
------------------

* A good start.
