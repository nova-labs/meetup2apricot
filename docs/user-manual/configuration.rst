.. highlight:: Bash

=============
Configuration
=============

As recommended in `The Twelve-Factor App`_,
meetup2apricot gets its configuration from environment variables.
The :ref:`meetup2apricot man page <meetup2apricot-environment>` defines the
configuration environment variables.
The configuration includes:

- Meetup :abbr:`API(application programming interface)` settings
- Wild Apricot API credentials
- Date/time thresholds for event conversion
- Event tagging
- Paths to local and remote files and directories

On Linux, a configuration shell script is a common way to provide environment
variables.
An annotated example configuration script, :github-raw:`/data/run_sample.env`,
provides a starting point for customization.
This file also is included with the downloaded or cloned source files in the
``/data`` directory.
Customize a copy with a different name.

The configuration script includes sensitive authorization data, so allow access only
to the user running meetup2apricot.
(The sample configuration script contains no sensitive data.)

For example, this chmod command gives the user read and write permissions, and
removes permissions from group members and other users:

.. code-block:: console

   $ chmod u=rw,go-rwx run.env

.. _`meetup-com-api-settings`:

Meetup API Settings
-----------------------

Meetup2apricot requests events for a specific Meetup group.
The Meetup API use a computer-friendly group :abbr:`URL(Uniform Resource
Locator)` name instead of the actual group name.
Locate the group URL name in a web browser address line, as shown in
:numref:`Figure %s <meetup-url-name>`.
Environment variable :envvar:`MEETUP_GROUP_URL_NAME` provides the URL group
name.

.. figure:: /images/screenshots/meetup-url-name.png
   :alt: Screenshot of a web browser address line with the Meetup URL group
         name circled within the URL
   :name: meetup-url-name
   :align: center

   The Meetup group URL name, "NOVA-Makers" circled in red, is the last
   part of the group's Meetup URL.

By default, the Meetup API returns data about the next 200 upcoming events.
In early November 2020, when conversions began, this provided almost a year of
future events, mostly repeated events automatically scheduled by Meetup.
Experiments determined that 100 upcoming events would provide about 60 days of
events.

Rather than rely on the Meetup default, environment variable
:envvar:`MEETUP_EVENTS_WANTED` specifies the number of upcoming events wanted
from Meetup.

.. _`wild-apricot-api-credentials`:

Wild Apricot API Credentials
----------------------------

Wild Apricot authenticates client applications with OAuth2.
The client application, meetup2apricot, needs an API key.
When a Wild Apricot administrator adds or edits an application, Wild Apricot
reveals the API key as described in `Authorizing External Applications`_.
The environment variable :envvar:`APRICOT_API_KEY` provides the necessary
credential to meetup2apricot.

.. _`wild-apricot-paths`:

Wild Apricot Paths
------------------

Several Wild Apricot API requests include Nova Labs' account number in the URL.
The environment variable :envvar:`APRICOT_ACCOUNT_NUMBER` provides the account
number to meetup2apricot.

Event photos will be uploaded to a subdirectory in the Wild Apricot web site
static resources area.
The environment variable :envvar:`APRICOT_PHOTO_DIRECTORY` specifies the path
to that subdirectory.
For example, specify this directory path for the event announcements photos
folder shown in :numref:`Figure %s <wild_apricot_photo_resources>`::

   export APRICOT_PHOTO_DIRECTORY='/resources/Pictures/EventAnnouncements'

.. figure:: /images/screenshots/ApricotFiles.png
   :alt: Wild Apricot's web file browser showing a folder hierarchy and a list
         of photos
   :name: wild_apricot_photo_resources
   :align: center

   Within the Settings/Files section of the Wild Apricot web administration
   interface (1), a directory tree shows
   ``/resources/Pictures/EventAnnouncements`` (2) containing event photos (3).

Local Paths
-----------

Event photos will be downloaded from Meetup into a local directory for
inspection and for later uploading to Wild Apricot.
The environment variable :envvar:`PHOTO_DIRECTORY` specifies the path
to that directory.

Meetup2apricot saves some information between runs about events and photos
previously processed.
:numref:`Table %s <cache_files_env_vars>` lists the related environment
variables and their purpose.

.. tabularcolumns:: |L|L|

.. _cache_files_env_vars:

.. table:: Environment Variables for Cache Files
   :align: center

   +-----------------------------+-------------------------------------------------+
   | Environment Variable        | Purpose                                         |
   +=============================+=================================================+
   | :envvar:`EVENT_CACHE_FILE`  | Path to cache file containing event information |
   +-----------------------------+-------------------------------------------------+
   | :envvar:`PHOTO_CACHE_FILE`  | Path to cache file containing photo information |
   +-----------------------------+-------------------------------------------------+

Event Tags
----------

Wild Apricot events can be tagged to aid searching and filtering.
For example, the Wild Apricot event list could be filtered by the *woodworking*
tag to prepare a list of upcoming wordworking classes.

Meetup2apricot can apply specified tags to all events copied from Meetup to
Wild Apricot.
Some possible tags might be *new,* to indicate new events; *meetup,* to
indicate events from meetup; and *review,* to indicate events requiring review
by an administrator.
Environment variable :envvar:`ALL_EVENT_TAGS` specifies a JSON formatted list
of tags to apply to all events.

Meetup2apricot can translate accounting codes from event titles into Wild
Apricot event tags.
Environment variable :envvar:`CODES_TO_TAGS` specifies a JSON formatted object
with accounting codes as keys and tags as values.
Tag values may be individual strings or a list of strings.
For example::

      export CODES_TO_TAGS='{
          "3D": "3d-printing",
          "AC": "arts-and-crafts",
          "EL": "electronics",
          "RO": ["electronics", "3d-printing"],
          "SL": "3d-printing",
          }'

Meetup2apricot would extract accounting code *RO* from event title "RO: Robot
Group Meetup" and use the ``CODES_TO_TAGS`` mapping to apply tags *electronics*
and *3d-printing* to the event.

.. _`Authorizing External Applications`: https://gethelp.wildapricot.com/en/articles/180
.. _`The Twelve-Factor App`: https://12factor.net/config
