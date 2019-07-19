.. image:: https://travis-ci.org/python-gitlab/python-gitlab.svg?branch=master
   :target: https://travis-ci.org/python-gitlab/python-gitlab

.. image:: https://badge.fury.io/py/python-gitlab.svg
   :target: https://badge.fury.io/py/python-gitlab

.. image:: https://readthedocs.org/projects/python-gitlab/badge/?version=latest
   :target: https://python-gitlab.readthedocs.org/en/latest/?badge=latest

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

* `python-requests <http://docs.python-requests.org/en/latest/>`_
* `six <https://six.readthedocs.io/>`_

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

``docker run -it --rm -e GITLAB_PRIVATE_TOKEN=<your token> -v /path/to/python-gitlab.cfg:/python-gitlab.cfg registry.gitlab.com/python-gitlab/python-gitlab:v1.8.0 <command> ...``

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

You need to install ``tox`` to run unit tests and documentation builds locally:

.. code-block:: bash

   # run the unit tests for python 2/3, and the pep8 tests:
   tox

   # run tests in one environment only:
   tox -epy35

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
   ./tools/functional_tests.sh

   # run the python API tests:
   ./tools/py_functional_tests.sh

You can also build a test environment using the following command:

.. code-block:: bash

   ./tools/build_test_env.sh

A freshly configured gitlab container will be available at
http://localhost:8080 (login ``root`` / password ``5iveL!fe``). A configuration
for python-gitlab will be written in ``/tmp/python-gitlab.cfg``.

To cleanup the environment delete the container:

.. code-block:: bash

   docker rm -f gitlab-test
