.. highlight:: Bash

=====================================
Wild Apricot Appliction Authorization
=====================================

Wild Apricot authenticates client applications such as meetup2apricot with OAuth2.
The client application, meetup2apricot, needs an :abbr:`API(application
programming interface)` key.
When a Wild Apricot administrator adds or edits an authorized application, Wild
Apricot reveals the API key as described in `Authorizing External
Applications`_.
Experienced Wild Apricot administrators can follow this outline:

1. Authorize a new server application.
2. Name the application.
3. Copy the API key into the meetup2apricot configuration file
4. Save the new authorized application.

Authorize an Application in Wild Apricot
----------------------------------------

In the Wild Apricot web administration settings, view authorized applications as shown in
:numref:`Figure %s <administration-settings-menu>`.

.. figure:: /images/screenshots/GlobalSettingsforAuthorizedApplications.png
   :align: center
   :alt: Screenshot showing the Wild Apricot administration settings menu
   :name: administration-settings-menu

   Click :guilabel:`Settings` (1) in the administration menu to display a settings menu.
   Click :guilabel:`Authorized (2) applications` to display the list of authorized applications.

Confirm that ``meetup2apricot`` is not among the authorized applications.
Start the authorization process as shown in
:numref:`Figure %s <authorized-applications-list>`.

.. figure:: /images/screenshots/AuthorizeApplicationButton.png
   :align: center
   :alt: Screenshot showing the list of authorized applications
   :name: authorized-applications-list

   Click :guilabel:`Authorized application` (1) to begin the authorization process.

Select the server application type, which is appropriate for meetup2apricot, as shown in
:numref:`Figure %s <authorization-type-choice>`.

.. figure:: /images/screenshots/ServerApplicationContinue.png
   :align: center
   :alt: Screenshot showing choices for application type
   :name: authorization-type-choice

   Select :guilabel:`Server application` (1), the authorization needed for meetup2apricot.
   Click :guilabel:`Continue` (2) to advance to the next form.

Fill in the application details form as shown in
:numref:`Figure %s <authorized-details-form>`.
Copy the API key for the meetup2apricot configuration file.
Save the new authorized application.

.. figure:: /images/screenshots/ApricotApplicationDetails.png
   :align: center
   :alt: Screenshot showing the application details form
   :name: authorized-details-form

   Enter an application name (1).
   Copy the API key (2).
   Select :guilabel:`Full access` (3) to allow meetup2apricot to add and change events.
   Click :guilabel:`Save` (4) to save the application authorization.

Configure the API Key
---------------------

Save the API key copied from the application details in meetup2apricot
configuration environment variable :envvar:`APRICOT_API_KEY` as described in
the :ref:`configuration guide <wild-apricot-api-credentials>`.
The API key copied from :numref:`Figure %s <authorized-details-form>` would
appear as follows in the environment configuration file::

   # Wild Apricot API key
   export APRICOT_API_KEY='vpxda1mz3y3vj58ryqtuqrt33q2ed0'

.. _`Authorizing External Applications`: https://gethelp.wildapricot.com/en/articles/180
