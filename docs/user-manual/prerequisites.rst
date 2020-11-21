=============
Prerequisites
=============

Computing Environment
---------------------

- Linux or maybe Windows
- Internet
- Python 3.9

:program:`Meetup2apricot` was developed, tested, and run on computers with
Ubuntu, a Linux operating system.
Meetup2apricot has no dependencies on Ubuntu or Linux; it should run on Windows,
macOS, Raspberry Pi, or anywhere Python is available.

Meetup2apricot requires an internet connection to access Meetup and Wild Apricot.

Meetup2apricot requires local storage to hold downloaded photos and two small
data files.

Meetup2apricot was coded with the Python programming language.
Python must be installed to run meetup2apricot.
Meetup2apricot was developed and tested successfully with Python 3.9.

Skills Needed
-------------

- Run commands from Linux shell
- Familiarity with :program:`make` and Python virtual environments
- Edit configuration files
- Access Wild Apricot as administrator

You must be able to run commands on your computer.
On Linux, you can use a terminal window to enter commands.
On Windows, you can use a command or PowerShell window.
From a remote computer, you can connect via ssh to run commands.

`Make`_ automates building, testing, and installing software by tracking
dependencies and executing commands listed in a makefile.
Meetup2apricot includes a makefile containing commands to build a virtual
environment, load the necessary Python packages, and install meetup2apricot.
You should be familiar with running make and understanding its output.

Meetup2apricot has dependencies on several other Python packages.
The Python Packaging Authority recommends creating a Python virtual environment
to keep meetup2apricot and its dependencies from conflicting with other Python
packages.
(See "`Installing packages using pip and virtual environments`_" for deep
backroundnot needed to run meetup2apricot.)
You should be familiar with the concepts of Python virtual environments.

You must be able to use a text editor to edit configuration files.

You must have administrative access to Wild Apricot to upload photos and to
review and edit events.

.. _`Installing packages using pip and virtual environments`: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
.. _`Make`: https://en.wikipedia.org/wiki/Make_(software)
