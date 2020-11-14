=======
Logging
=======

:program:`Meetup2apricot` logs its activity to a log file and optionally to the
console *(stderr).*
Command line flags control which log messages should be directed to which
destinations.

Log Destinations
----------------

By default, meetup2apricot writes log messages to file :file:`meetup2apricot.log` in
the current directory.
Logs are rotated daily; five days of logs are retained.

The :option:`-l <meetup2apricot -l>` option can specify an alternate path to the
log file.
The :option:`-v <meetup2apricot -v>` option adds console output.
The :option:`-w <meetup2apricot -w>` option, intended for cron jobs, adds
console output and limits the console log level to warnings and errors.
In the rare situation when ``meetup2apricot -w`` reports a warning or error,
cron will send an email.

:numref:`Table %s <log-output>` summarizes the impact of the :option:`-l
<meetup2apricot -l>`, :option:`-v <meetup2apricot -v>`, and :option:`-w
<meetup2apricot -w>` flags on log destination.

.. tabularcolumns:: |L|C|C|C|C|

.. _log-output:

.. table:: Selection of Log Destination by Command Line Flags
   :align: center

   +----------------------------+---------+---------+---------+------------+
   | Log Destination            | Default | -v      | -w      | -l logfile |
   +============================+=========+=========+=========+============+
   | Console Log Output         |         | \+      | \+      |            |
   +----------------------------+---------+---------+---------+------------+
   | :file:`meetup2apricot.log` | ✔       |         |         |            |
   +----------------------------+---------+---------+---------+------------+
   | Specified :file:`logfile`  |         |         |         | ✔          |
   +----------------------------+---------+---------+---------+------------+


Log Levels
----------

By default, meetup2apricot logs only info, warning, and error messages.
The :option:`-d <meetup2apricot -d>` option adds debug level messages, which help
software developers.
As described above, the :option:`-w <meetup2apricot -w>` option adds console
output and limits the console log level to warnings and errors.
:numref:`Table %s <log-levels>` summarizes the log levels and the impact of the
:option:`-d <meetup2apricot -d>` and :option:`-w <meetup2apricot -w>` flags.

.. tabularcolumns:: |L|L|C|C|C|

.. _log-levels:

.. table:: Selection of Log Level by Command Line Flags
   :align: center

   +-----------+---------------------+---------+---------+---------+
   | Log Level | Reports             | Default | -d      | -w      |
   +===========+=====================+=========+=========+=========+
   | Error     | Failures            | ✔       | ✔       | ✔       |
   +-----------+---------------------+---------+---------+---------+
   | Warning   | Abnormal conditions | ✔       | ✔       | ✔       |
   +-----------+---------------------+---------+---------+---------+
   | Info      | Routine operations  | ✔       | ✔       |         |
   +-----------+---------------------+---------+---------+---------+
   | Debug     | Developer details   |         | ✔       |         |
   +-----------+---------------------+---------+---------+---------+

