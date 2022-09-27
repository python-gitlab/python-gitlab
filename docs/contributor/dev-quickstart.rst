.. _dev-quickstart:

=====================
Developer Quick-Start
=====================

This is a quick walkthrough to get you started developing code for
python-gitlab.  This assumes you are already familiar with submitting code
reviews to a Github based project.

The CI (Continuous Integration) system currently runs the unit tests under
Python 3.7, 3.8, 3.9, and 3.10. It is strongly encouraged to run the unit tests
locally prior to submitting a patch.

Prepare Development System
==========================

System Prerequisites
--------------------

The following packages cover the prerequisites for a local development
environment on most current distributions. Instructions for getting set up with
non-default versions of Python and on older distributions are included below as
well.

- Ubuntu/Debian::

    sudo apt-get install python3-pip git

- RHEL/CentOS/Fedora::

    sudo dnf install python3-pip git

Python Prerequisites
--------------------

We suggest to use at least tox 3.24, if your distribution has an older version,
you can install it using pip system-wise or better per user using the --user
option that by default will install the binary under $HOME/.local/bin, so you
need to be sure to have that path in $PATH; for example::

    pip3 install tox --user

will install tox as ~/.local/bin/tox

You may need to explicitly upgrade virtualenv if you've installed the one
from your OS distribution and it is too old (tox will complain). You can
upgrade it individually, if you need to::

    pip3 install -U virtualenv --user

Running Unit Tests Locally
==========================

If you haven't already, python-gitlab source code should be pulled directly from git::

    # from your home or source directory
    cd ~
    git clone https://github.com/python-gitlab/python-gitlab
    cd python-gitlab

Running Unit and Style Tests
----------------------------

All unit tests should be run using tox. To run python-gitlab's entire test suite::

    # to run the py3 unit tests, and the style tests
    tox

To run a specific test or tests, use the "-e" option followed by the tox target
name. For example::

    # run the unit tests under py310 (Python 3.10) and also run the pep8 tests
    tox -e py310,pep8

You may pass options to the test programs using positional arguments.
To run a specific unit test, this passes the desired test
(regex string) to `pytest <https://docs.pytest.org/en/latest/>`_::

    # run tests for Python 3.8 which match the string 'test_projects'
    tox -e py310 -- -k test_projects

Additional Tox Targets
----------------------

There are several additional tox targets not included in the default list, such
as the target which builds the documentation site.   See the ``tox.ini`` file
for a complete listing of tox targets. These can be run directly by specifying
the target name::

    # generate the documentation pages locally
    tox -e docs
