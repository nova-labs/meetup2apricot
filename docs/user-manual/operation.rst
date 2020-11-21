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

To monitor the progress of meetup2apricot use the verbose option
(:option:`-v <meetup2apricot -v>`), as described in :doc:`logging`::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -v )

Dry Runs
--------

*Dry run* mode lets you preview changes.
When you run meetup2apricot in dry run mode, no events will be added to Wild
Apricot and no photos will be downloaded from Meetup.
Use the dry run option (:option:`-n <meetup2apricot -n>`) with the verbose
option (:option:`-v <meetup2apricot -v>`) to see the proposed changes::

    $ ( . meetup2apricot.env && $(MEETUP2APRICOT) -n -v )

Run on a Schedule
-----------------

Schedule meetup2apricot with `cron`_ to run on a schedule.
Add the ``MEETUP2APRICOT`` environment variable and the scheduled commands to
``crontab``, cron's configuration file.
The example cron job was written for the bash shell, so specify that shell if
necessary.
The warning option (:option:`-w <meetup2apricot -w>`) reports warning and error
messages to the standard error output; cron can send these results via email.
For example, to run meetup2apricot every hour on the half hour::

    SHELL=/bin/bash
    MEETUP2APRICOT=/home/joel/.virtualenvs/meetup2apricot/bin/meetup2apricot
    30 * * * * . meetup2apricot.env && $(MEETUP2APRICOT) -w

.. _cron: https://en.wikipedia.org/wiki/Cron
.. _path: https://en.wikipedia.org/wiki/PATH_(variable)
