.. highlight:: console

=========
Operation
=========

:program:`Meetup2apricot` is a command line program with options for
conveniently running from a shell session or a cron job.

Before You Start
----------------

Before running meetup2apricot, authorize meetup2apricot in Wild Apricot,
install meetup2apricot, and configure environment variables, and locate the
meetup2apricot executable program.

Meetup2apricot requires authorization to access the Wild Apricot API.
See :doc:`apricot-application-authorization` for details.

Install meetup2apricot as described in :doc:`installation`.

You must configure several environment variables as described in
:doc:`configuration`.
The examples below assume that the annotated example script,
:github-raw:`/data/run_sample.env`, has been copied to local file
``meetup2apricot.env`` and configured as needed.

Your computer's shell (bash, powershell, etc.) will find meetup2apricot on its
`path`_ if you have an activated Python virtual environment.
Otherwise, use make's *which* target to locate the meetup2apricot executable.
For example::

    $ make which
    ...
    /home/joel/.virtualenvs/meetup2apricot/bin/meetup2apricot   

For convenience, define an environment variable with that path::

    $ export MEETUP2APRICOT=/home/joel/.virtualenvs/meetup2apricot/bin/meetup2apricot

Run on the Command Line
-----------------------

Run meetup2apricot on the command line when new Meetup events are added.
Supply your configured environment variables by sourcing your configuration
script.
Use a subshell to isolate and protect sensitive configuration information.
For example::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) )

To monitor the progress of meetup2apricot use the report option
(:option:`-r <meetup2apricot -r>`) to report
added events, registration types, and photos::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -r )

    GO: New Member Orientation/Onboarding
        2020-11-29 16:00 to 2020-11-29 18:00
        Downloaded GO_New_Member_Orientation_2020-11-10.jpeg
        Instructor/Host   $  0.00   2 available
        RSVP              $  0.00   unlimited 

    BL_G: Blacksmithing Open Office Hours and Practice Session (Members ONLY)
        2020-12-02 18:30 to 2020-12-02 20:30
        Instructor/Host   $  0.00   2 available
        Members Only      $ 15.00   7 available


Dry Runs
--------

*Dry run* mode lets you preview changes.
When you run meetup2apricot in dry run mode, no events will be added to Wild
Apricot and no photos will be downloaded from Meetup.
Use the dry run option (:option:`-n <meetup2apricot -n>`) with the report
option (:option:`-r <meetup2apricot -r>`) to see the proposed changes::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -n -r )


Selecting Events
----------------

Meetup2apricot can transfer selected events from Meetup and add them to Wild
Apricot.
This need can arise occasionally when some other upcoming Meetup events need
correction or when a future event must open to registration early.

Use the Meetup IDs option (:option:`-m <meetup2apricot -m>`) 
in conjunction with the dry run option (:option:`-n <meetup2apricot -n>`)
and the report option (:option:`-r <meetup2apricot -r>`)
to see Meetup event IDs along with the proposed changes::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -m -n -r )

    276466635: AC_P: Digitizing for CNC Machine Embroidery
        2021-03-04 19:00 to 21:00
        Instructor/Host   $  0.00   2 available
        RSVP              $120.00   unlimited

    276381033: MW_S: CNC Mill Sign Off Class
        2021-03-06 12:00 to 17:00
        Instructor/Host   $  0.00   2 available
        RSVP              $300.00   4 available

    276412113: AC_S: Industrial Sewing Machine Red Tool Sign Off (members only)
        2021-03-09 18:30 to 21:00
        Instructor/Host   $  0.00   2 available
        Members Only      $ 65.00   4 available

Use the transfer option (:option:`-t <meetup2apricot -t>`) with the selected
Meetup event IDs to transfer only those events from Meetup to Wild Apricot.
For example, to select only the Arts and Crafts (AC) events::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -r -t 276466635 276412113 )

    AC_P: Digitizing for CNC Machine Embroidery
        2021-03-04 19:00 to 21:00
        Instructor/Host   $  0.00   2 available
        RSVP              $120.00   unlimited

    AC_S: Industrial Sewing Machine Red Tool Sign Off (members only)
        2021-03-09 18:30 to 21:00
        Instructor/Host   $  0.00   2 available
        Members Only      $ 65.00   4 available

Skipping Events
---------------

Meetup2apricot can permanently skip downloading selected events from Meetup.
This need can arise when an administrator creates a Wild Apricot version of an
event before meetup2apricot has downloaded the event.

As in the previous example, use the Meetup IDs option
(:option:`-m <meetup2apricot -m>`) in conjunction with the dry run option
(:option:`-n <meetup2apricot -n>`) and the report option
(:option:`-r <meetup2apricot -r>`) to see Meetup event IDs along with the
proposed changes::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -m -n -r )

    276466635: AC_P: Digitizing for CNC Machine Embroidery
        2021-03-04 19:00 to 21:00
        Instructor/Host   $  0.00   2 available
        RSVP              $120.00   unlimited

    276381033: MW_S: CNC Mill Sign Off Class
        2021-03-06 12:00 to 17:00
        Instructor/Host   $  0.00   2 available
        RSVP              $300.00   4 available

    276412113: AC_S: Industrial Sewing Machine Red Tool Sign Off (members only)
        2021-03-09 18:30 to 21:00
        Instructor/Host   $  0.00   2 available
        Members Only      $ 65.00   4 available

Suppose that the arts and crafts steward created a Wild Apricot events for the
embroidery and sewing classes.
Use the skip option (:option:`-s <meetup2apricot -s>`) with the Meetup event
IDs to skip those events::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -r -s 276466635 276412113 )

    MW_S: CNC Mill Sign Off Class
        2021-03-06 12:00 to 17:00
        Instructor/Host   $  0.00   2 available
        RSVP              $300.00   4 available

When the meetup2apricot command specifies both selected and skipped events, the
two options interact.
First the Meetup download is limited to the selected events; other events will
be available for later downloads.
Then skipped events, whether selected or not, will be permanently skipped.

For example, an administrator may create a Meetup event to "hold the date" for
a multi-event special day still in the planning stage.
The "hold the date" event (Meetup ID 12345) should never be downloaded to Wild Apricot.
This command limits the transfer to that event and permanently skips the event::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -r -t 12345 -s 12345 )

Run on a Schedule
-----------------

Schedule meetup2apricot with `cron`_ to run on a schedule.
Add the ``MEETUP2APRICOT`` environment variable and the scheduled commands to
``crontab``, cron's configuration file.
This example cron job runs meetup2apricot every hour on the half hour::

    SHELL=/bin/bash
    MEETUP2APRICOT=/home/joel/.virtualenvs/meetup2apricot/bin/meetup2apricot
    30 * * * * . meetup2apricot.env && $(MEETUP2APRICOT) -r -w

In the example, the  warning option (:option:`-w <meetup2apricot -w>`) reports
warning and error messages to the standard error output.
The report option (:option:`-r <meetup2apricot -r>`) reports added events,
registration types, and photos to standard output.
Cron will send these results via email.
If there are no warnings and no added events, cron will not send an email.

The example was written for the bash shell, so specify that shell if necessary.

.. _cron: https://en.wikipedia.org/wiki/Cron
.. _path: https://en.wikipedia.org/wiki/PATH_(variable)
