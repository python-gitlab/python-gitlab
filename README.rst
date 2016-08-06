.. image:: https://travis-ci.org/gpocentek/python-gitlab.svg?branch=master
   :target: https://travis-ci.org/gpocentek/python-gitlab

Python GitLab
=============

``python-gitlab`` is a Python package providing access to the GitLab server API.

It supports the v3 api of GitLab, and provides a CLI tool (``gitlab``).

Installation
============

Requirements
------------

python-gitlab depends on:

* `python-requests <http://docs.python-requests.org/en/latest/>`_
* `six <https://pythonhosted.org/six/>`_

Install with pip
----------------

.. code-block:: console

   pip install python-gitlab

Bug reports
===========

Please report bugs and feature requests at
https://github.com/gpocentek/python-gitlab/issues.


Documentation
=============

The full documentation for CLI and API is available on `readthedocs
<http://python-gitlab.readthedocs.org/en/stable/>`_.


Contributing
============

You can contribute to the project in multiple ways:

* Write documentation
* Implement features
* Fix bugs
* Add unit and functional tests
* Everything else you can think of

Provide your patches as github pull requests. Thanks!

Running unit tests
------------------

Before submitting a pull request make sure that the tests still succeed with
your change. Unit tests will run using the travis service and passing tests are
mandatory.

You need to install ``tox`` to run unit tests and documentation builds:

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

To cleanup the environement delete the container:

.. code-block:: bash

   docker rm -f gitlab-test
