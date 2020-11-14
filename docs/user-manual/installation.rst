.. highlight:: console

============
Installation
============

Download Source
---------------

The sources for meetup2apricot can be downloaded from the `Github repo`_.

You can either clone the public repository::

    $ git clone git://github.com/nova-labs/meetup2apricot
    $ cd meetup2apricot

Or you can download the `zip file`_ and unzip it::

    $ curl -OL https://github.com/nova-labs/meetup2apricot/tarball/master
    $ unzip main.zip
    $ cd meetup2apricot-main

Install Meetup2apricot
----------------------

Once you have a copy of the source, you can install it with::

    $ make install

:program:`Make` will create a Python virtual environment, if neccessary;
install the required Python packages; and install meetup2python.

.. _Github repo: https://github.com/nova-labs/meetup2apricot
.. _zip file: https://github.com/nova-labs/meetup2apricot/archive/main.zip
