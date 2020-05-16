.. image:: https://travis-ci.org/python-gitlab/python-gitlab.svg?branch=master
   :target: https://travis-ci.org/python-gitlab/python-gitlab

.. image:: https://badge.fury.io/py/python-gitlab.svg
   :target: https://badge.fury.io/py/python-gitlab

.. image:: https://readthedocs.org/projects/python-gitlab/badge/?version=latest
   :target: https://python-gitlab.readthedocs.org/en/latest/?badge=latest

.. image:: https://codecov.io/github/python-gitlab/python-gitlab/coverage.svg?branch=master
    :target: https://codecov.io/github/python-gitlab/python-gitlab?branch=master

.. image:: https://img.shields.io/pypi/pyversions/python-gitlab.svg
   :target: https://pypi.python.org/pypi/python-gitlab

.. image:: https://img.shields.io/gitter/room/python-gitlab/Lobby.svg
   :target: https://gitter.im/python-gitlab/Lobby
   
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

Python GitLab
=============

``python-gitlab`` is a Python package providing access to the GitLab server API.

It supports the v4 API of GitLab, and provides a CLI tool (``gitlab``).

Installation
============

Requirements
------------

python-gitlab depends on:

* `python-requests <https://2.python-requests.org/en/latest/>`_

Install with pip
----------------

.. code-block:: console

   pip install python-gitlab


Using the python-gitlab docker image
====================================

How to build
------------

``docker build -t python-gitlab:TAG .``

How to use
----------

``docker run -it --rm -e GITLAB_PRIVATE_TOKEN=<your token> -v /path/to/python-gitlab.cfg:/python-gitlab.cfg python-gitlab <command> ...``

or run it directly from the upstream image:

``docker run -it --rm -e GITLAB_PRIVATE_TOKEN=<your token> -v /path/to/python-gitlab.cfg:/python-gitlab.cfg registry.gitlab.com/python-gitlab/python-gitlab:latest <command> ...``

To change the GitLab URL, use `-e GITLAB_URL=<your url>`

Bring your own config file:
``docker run -it --rm -v /path/to/python-gitlab.cfg:/python-gitlab.cfg -e GITLAB_CFG=/python-gitlab.cfg python-gitlab <command> ...``


Bug reports
===========

Please report bugs and feature requests at
https://github.com/python-gitlab/python-gitlab/issues.


Documentation
=============

The full documentation for CLI and API is available on `readthedocs
<http://python-gitlab.readthedocs.org/en/stable/>`_.

Build the docs
--------------
You can build the documentation using ``sphinx``::

    pip install sphinx
    python setup.py build_sphinx


Contributing
============

You can contribute to the project in multiple ways:

* Write documentation
* Implement features
* Fix bugs
* Add unit and functional tests
* Everything else you can think of

We enforce commit messages to be formatted using the `conventional-changelog <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines>`_.
This leads to more readable messages that are easy to follow when looking through the project history.

Please provide your patches as github pull requests. Thanks!

Code-Style
----------

We use black as code formatter, so you'll need to format your changes using the
`black code formatter
<https://github.com/python/black>`_.

Just run

.. code-block:: bash

  cd python-gitlab/
  pip3 install --user black
  black .
  
to format your code according to our guidelines.

Running unit tests
------------------

Before submitting a pull request make sure that the tests still succeed with
your change. Unit tests and functional tests run using the travis service and
passing tests are mandatory to get merge requests accepted.

We're currently in a restructing phase for the unit tests. If you're changing existing
tests, feel free to keep the current format. Otherwise please write new tests with pytest and
using `responses<https://github.com/getsentry/responses>`_. An example for new tests can be found in
tests/objects/test_runner.py

You need to install ``tox`` to run unit tests and documentation builds locally:

.. code-block:: bash

   # run the unit tests for all supported python3 versions, and the pep8 tests:
   tox

   # run tests in one environment only:
   tox -epy38

   # build the documentation, the result will be generated in
   # build/sphinx/html/
   tox -edocs

Running integration tests
-------------------------

Two scripts run tests against a running gitlab instance, using a docker
container. You need to have docker installed on the test machine, and your user
must have the correct permissions to talk to the docker daemon.

To run these tests:

.. code-block:: bash

   # run the CLI tests:
   tox -e cli_func_v4

   # run the python API tests:
   tox -e py_func_v4

By default, the tests run against the ``gitlab/gitlab-ce:latest`` image. You can
override both the image and tag with the ``-i`` and ``-t`` options, or by providing
either the ``GITLAB_IMAGE`` or ``GITLAB_TAG`` environment variables.

This way you can run tests against different versions, such as ``nightly`` for
features in an upcoming release, or an older release (e.g. ``12.8.0-ce.0``).
The tag must match an exact tag on Docker Hub:

.. code-block:: bash

   # run tests against `nightly` or specific tag
   ./tools/py_functional_tests.sh -t nightly
   ./tools/py_functional_tests.sh -t 12.8.0-ce.0

   # run tests against the latest gitlab EE image
   ./tools/py_functional_tests.sh -i gitlab/gitlab-ee

   # override tags with environment variables
   GITLAB_TAG=nightly ./tools/py_functional_tests.sh

You can also build a test environment using the following command:

.. code-block:: bash

   ./tools/build_test_env.sh

A freshly configured gitlab container will be available at
http://localhost:8080 (login ``root`` / password ``5iveL!fe``). A configuration
for python-gitlab will be written in ``/tmp/python-gitlab.cfg``.

To cleanup the environment delete the container:

.. code-block:: bash

   docker rm -f gitlab-test
