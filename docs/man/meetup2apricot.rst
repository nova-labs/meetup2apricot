.. highlight:: Bash

meetup2apricot
==============

Synopsis
--------

**meetup2apricot** [-h] [-d] [-l LOGFILE] [-m] [-n] [-r] [-s MEETUP_ID [MEETUP_ID ...]] [-t MEETUP_ID [MEETUP_ID ...]] [-v] [-w]

Description
-----------

:program:`meetup2apricot` downloads events from Meetup and 
creates events in Wild Apricot.

:program:`meetup2apricot` also downloads featured event photos from Meetup and
saves them locally for manual upload to Wild Apricot.

:program:`meetup2apricot` reads its configuration from
:ref:`environment variables <meetup2apricot-environment>`.
The :ref:`command line options <meetup2apricot-options>` control only
the message levels to log and where to send the logs.

.. _meetup2apricot-options:

Options
-------

.. program:: meetup2apricot

.. option:: -h, --help

   Show a help message and exit.

.. option:: -d, --debug

   Also log debug messages. If this option is omitted,
   log only info and higher level messages.

.. option:: -l LOGFILE, --logfile LOGFILE

   Path to logfile (default: meetup2apricot.log).

.. option:: -m, --meetup-ids

   Show Meetup event IDs in reports.

.. option:: -n, --dryrun

   Perform a dry run.
   Do not add events to Wild Apricot.
   Do not download photos from Meetup.
   Do not update event and photo data cached between runs.

.. option:: -r, --report

   Report added events, registration types, and photos to standard output.

.. option:: -s MEETUP_ID [MEETUP_ID ...], --skip MEETUP_ID [MEETUP_ID ...]

   Skip events matching the Meetup event IDs during this and subsequent runs.
   This option may be repeated.

.. option:: -t MEETUP_ID [MEETUP_ID ...], --transfer MEETUP_ID [MEETUP_ID ...]

   Transfer from Meetup to Wild Apricot only those events matching Meetup event IDs.
   When no Meetup IDs are specified, transfer all upcoming Meetup events.
   This option may be repeated.

.. option:: -v, --verbose

   Log to standard error.
   This is useful for debugging when running from the command line.

.. option:: -w, --warnings

   Log warnings and higher level messages to standard error.
   This is useful when running in cron job because cron
   will mail any standard error output.

.. _meetup2apricot-environment:

Environment
-----------

.. envvar:: ALL_EVENT_TAGS

   Tags to assign to all Wild Apricot events
   formated as a JSON list of strings.
   Some examples::

      export ALL_EVENT_TAGS='[]'
      export ALL_EVENT_TAGS='["new"]'
      export ALL_EVENT_TAGS='["new", "meetup"]'

.. envvar:: APRICOT_ACCOUNT_NUMBER

   The Wild Apricot account number.

.. envvar:: APRICOT_API_KEY

   The Wild Apricot API key.

.. envvar:: APRICOT_PHOTO_DIRECTORY

   The Wild Apricot web directory for photos.

.. envvar:: CODES_TO_TAGS

   A mapping from Nova Labs accounting codes to Wild Apricot event tags.
   Format as a JSON object with codes as keys and strings (or lists of strings)
   as values.
   For example::

      export CODES_TO_TAGS='{
          "3D": "3d-printing",
          "AC": "arts-and-crafts",
          "EL": "electronics",
          "RO": ["electronics", "3d-printing"],
          "SL": "3d-printing",
          }'

.. envvar:: EARLIEST_EVENT_START_TIME

   The start time of the earliest event to convert from Meetup to Wild Apricot.
   Use `ISO 8601`_ format including a timezone offset.
   For example::

      export EARLIEST_EVENT_START_TIME="2020-11-10 00:00 -05:00"

.. _ISO 8601: https://xkcd.com/1179/

.. envvar:: EVENT_CACHE_FILE

   The path to a Python pickle formatted cache file of event conversion
   details.

.. envvar:: EVENT_RESTRICTIONS

   Event restrictions formatted as a list of JSON objects.
   Each object optionally specifies an event restriction name, a
   case-insensitive Python regular expression to find in event titles, a price
   restriction (free or paid), and an optional member level (or list of levels).
   For example::

       export EVENT_RESTRICTIONS='[
            {
                    "name": "Green Orientation",
                    "pattern": "go:.*orientation",
                    "levels": "Associate (onboarding)"
            },
            {
                    "name": "Members Only",
                    "pattern": "members[ -]*only",
                    "price": "paid"
            }]'

The following table lists the name-value pairs within an event restriction JSON
object.
All name-value pairs are optional.

.. tabularcolumns:: |L|L|L|

.. _default_restriction_values:

.. table:: Event Restriction Name-Value Pairs
   :align: center

   +-------------+---------------------------------------------------------------------+-----------------------------+
   | Name        | Value                                                               | Default Value               |
   +=============+=====================================================================+=============================+
   | ``name``    | Event registration type name                                        | ``RSVP``                    |
   +-------------+---------------------------------------------------------------------+-----------------------------+
   | ``pattern`` | Case-insensitive regular expression to match an event title         | Match all titles            |
   +-------------+---------------------------------------------------------------------+-----------------------------+
   | ``price``   | ``free`` or ``paid``                                                | Match all prices            |
   +-------------+---------------------------------------------------------------------+-----------------------------+
   | ``levels``  | A Wild Apricot membership level or a JSON list of membership levels | Allow all membership levels |
   +-------------+---------------------------------------------------------------------+-----------------------------+

.. envvar:: LATEST_EVENT_START_TIME

   The start time of the latest event to convert from Meetup to Wild Apricot.
   Use ISO 8601 format including a timezone offset.
   For example::

      export LATEST_EVENT_START_TIME="2020-12-31 23:59 -05:00"

.. envvar:: MEETUP_EVENTS_WANTED

   The number of events to request from Meetup.

.. envvar:: MEETUP_GROUP_URL_NAME

   The group name for Meetup URLs.
   For example, in the URL https://www.meetup.com/NOVA-Makers/,
   the group name is *NOVA-Makers*.

.. envvar:: PHOTO_DIRECTORY

   A local directory for photos from Meetup.

.. envvar:: PHOTO_CACHE_FILE

   The path to a Python pickle formatted cache file of photo conversion
   details.

