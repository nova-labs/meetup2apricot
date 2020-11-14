.. Use only basic Restructured Text in this file so PyPi and GitHub can display it.
.. No Sphinx extensions here.

==============
Meetup2Apricot
==============

.. Start badges

.. Start description

**Meetup2apricot** is a command line program that retrieves event descriptions
from Meetup and loads them into Wild Apricot.

Meetup2apricot was developed for `Nova Labs`_, a makerspace in Reston, Virginia.
Nova Labs will transition event registrations from Meetup to Wild Apricot in
November 2020.

.. _`Nova Labs`: https://www.nova-labs.org/

.. PyPi requires an absolute image URL.
.. image:: https://raw.githubusercontent.com/nova-labs/meetup2apricot/main/docs/images/diagrams/Meetup2Apricot-Architecture.png
        :align: center
        :alt: Diagram of meetup2apricot's function showing events and photos
                retrieved by meetup2apricot from Meetup.com and transferred to
                Wild Apricot.

.. End description

Resources
---------

* Source code: https://github.com/nova-labs/meetup2apricot
* Free software: `MIT license`_

.. _`MIT license`: LICENSE


Features
--------

* Retrieves events from the Meetup API.
* Translates accounting codes into event tags to categorize events on Wild Apricot.
* Inserts events via the Wild Apricot API.
* Downloads events' featured photos from Meetup into a local directory for manual upload to Wild Apricot.
* Caches processed events and photos to avoid duplication.

Credits
-------

**Meetup2apricot** was developed by Joel Shprentz (`@jshprentz`_).

.. _`@jshprentz`: https://github.com/jshprentz
