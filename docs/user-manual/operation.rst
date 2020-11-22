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
        Meetup RSVP    $  0.00   2 registered on Meetup
        RSVP           $  0.00   unlimited 
    
    BL_G: Blacksmithing Open Office Hours and Practice Session (Members ONLY)
        2020-12-02 18:30 to 2020-12-02 20:30
        Meetup RSVP    $  0.00   1 registered on Meetup
        Members Only   $ 15.00   7 available


Dry Runs
--------

*Dry run* mode lets you preview changes.
When you run meetup2apricot in dry run mode, no events will be added to Wild
Apricot and no photos will be downloaded from Meetup.
Use the dry run option (:option:`-n <meetup2apricot -n>`) with the report
option (:option:`-r <meetup2apricot -r>`) to see the proposed changes::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -n -r )

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
