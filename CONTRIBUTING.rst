..highlight:: BashSessionLexer

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/nova-labs/meetup2apricot/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Meetup2apricot could always use more documentation, whether as part of the
official meetup2apricot docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/nova-labs/meetup2apricot/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `meetup2apricot` for local development.

1. Fork the `meetup2apricot` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/meetup2apricot.git
    $ cd meetup2apricot

3. Setup for development by creating a Python 3.0 virtual environment and
   loading it with the required Python packages::

    $ make dev

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

#. Now you can make your changes locally.
   Don't worry about exactly matching the project code style;
   the black formatter will fix everything::

    $ make black

#. Test as you make changes::

    $ make test

#. Commit your changes to git as you go::

    $ git add .
    $ git commit -m "Your description of the changes."

#. Continue making changes, formatting, testing, and committing to git.
   Track your progress with git's log command::

    $ make gitlog

#. When you're done making changes, test everything again in new virtual
   environment to check package dependency issues.
   This step also runs flake8 to check for code anomalies::
   
    $ make test-all

#. Commit your changes and push your branch to GitHub::

    $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests (that pass!).

2. Update docs to describe new, updated, and removed functionality,
   configuration, operation, etc.

Documentation
-------------

Most functions and methods should have docstrings summarizing their intent,
arguments, and return values.
Function, method, and variable names should be descriptive, not cryptic.
Local temporary variables can elucidate your code.
Prefer:

.. code-block:: python3

        photo_path = self.get_photo(meetup_event)
        event_tags = self.get_event_tags(meetup_event)
        self.add_apricot_event(meetup_event, photo_path, event_tags)

instead of:

.. code-block:: python3

        self.add_apricot_event(
            meetup_event,
            self.get_photo(meetup_event),
            self.get_event_tags(meetup_event)
        )

README.rst includes a list of major functionality.
Keep that list up-to-date.
   
HISTORY.rst shows the major changes in each release and planned future changes.
Keep that list up-to-date, moving items from the Future History section to the
Next Release section when possible.

When you add the first change to the Next Release section, uncomment the
section heading.
For example, change this:

   .. code-block:: restructuredtext
      
      .. Next Release
      .. ------------------

to:

   .. code-block:: restructuredtext

      Next Release
      ------------------

      * My new feature.

Run Sphinx to build the documentation for local review.
The *docs* make target will build an HTML version of the documentation and open
a browser::

    $ make docs

The browser will not open if you develop on a remote machine via ssh, PuTTY, etc.
Instead, run a simple web server on the HTML documentation::

    $ make docsweb

Tips
----

The makefile includes targets for common operations.
The default target is help::

    $ make

    clean                remove all build, test, coverage and Python artifacts
    clean-build          remove build artifacts
    clean-pyc            remove Python file artifacts
    clean-test           remove test and coverage artifacts
    black                reformat code to conform to PEP-8
    lint                 check style with flake8
    test                 run tests quickly with the default Python
    test-all             run tests on every Python version with tox
    coverage             check code coverage quickly with the default Python
    docs                 generate Sphinx HTML documentation, including API docs
    docsbrowse           compile the docs and view them in a local browser
    docsweb              compile the docs and serve them via the web
    servedocs            compile the docs watching for changes
    gitlog               show the Git graphical history
    release              package and upload a release
    dist                 builds source and wheel package
    install              install the package to the active Python's site-packages
    venv                 create a Python virtual environment
    production           install required Python packages for production
    dev                  install required Python packages for local development

Deploying Releases
------------------

A reminder for the maintainers on how to deploy releases.
Make sure all your pull requests and other changes are committed in the
development branch.
Working in the development branch, bump the version (major, minor, or patch).
Push the development branch to GitHub.
Merge the development branch to the main branch and tag with the release
number.
Push the main branch and the tagged branch to GitHub::

    $ git checkout development
    $ bumpversion patch
    $ git push origin development
    $ git checkout main
    $ git merge --no-ff development
    $ git tag -a v1.2.3
    $ git push origin main
    $ git push origin v1.2.3

After the release, start a new feature development branch to avoid committing
directly to the main and development branches::

    $ git checkout development
    $ git checkout -b my-new-feature
