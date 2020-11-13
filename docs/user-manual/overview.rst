========
Overview
========

.. figure:: /images/diagrams/Meetup2Apricot-Architecture.png
   :align: center
   :alt: Diagram of dataflow from Metup to Wild Apricot through meetup2apricot
   :name: meetup2apricot-event-data-flow

   Meetup2apricot retrieves event data and photos from Meetup, transforms the
   data, and adds events and registration types to Wild Apricot.
   Administrators later manually upload the photos to Wild Apricot.

:program:`Meetup2apricot` is a command line program that retrieves event
descriptions from Meetup and adds them to Wild Apricot.
Meetup2apricot also downloads featured event photos from Meetup for manual
upload to Wild Apricot.
:numref:`Figure %s <meetup2apricot-event-data-flow>` shows event data flow from
Meetup to Wild Apricot.

Preparation
-----------

Meetup2apricot run on any computer running Linux or a similar operating system.
An administrator will need some basic computer skills to install and configure
meetup2apricot.
See :doc:`prerequisites` for a description of the computing and skills
requirements.

Meetup2apricot accesses the Xibo :abbr:`API(application programming interface)`
as a distinct authorized application.  See :doc:`apricot-application-setup` for
instructions about adding and authorizing this application.

Installation
------------

Meetup2apricot can be installed with standard Python package tools.
A makefile automates the installation.
See :doc:`installation`.

Configuration
-------------

Meetup2apricot gets its configuration from environment variables.
The configuration includes:

- Meetup :abbr:`API(application programming interface)` settings
- Wild Apricot API credentials
- Date/time thresholds for event conversion
- Event tagging
- Paths to local and remote files and directories

The :ref:`meetup2apricot man page <meetup2apricot-environment>` defines the
configuration environment variables.
:doc:`configuration` explains the environment variables in more detail.
An annotated example configuration script, :github-raw:`/data/run_sample.env`,
provides a starting point for customization.

Logging
-------

Meetup2apricot can log its activity to a named file, standard output, or both.
:ref:`Command line options <meetup2apricot-options>` control the message levels to
log and where to send the logs.
