.. image:: https://github.com/python-gitlab/python-gitlab/workflows/Test/badge.svg
   :target: https://github.com/python-gitlab/python-gitlab/actions

.. image:: https://badge.fury.io/py/python-gitlab.svg
   :target: https://badge.fury.io/py/python-gitlab

.. image:: https://readthedocs.org/projects/python-gitlab/badge/?version=latest
   :target: https://python-gitlab.readthedocs.org/en/latest/?badge=latest

.. image:: https://codecov.io/github/python-gitlab/python-gitlab/coverage.svg?branch=main
    :target: https://codecov.io/github/python-gitlab/python-gitlab?branch=main

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

Using the docker image
======================

You can run the Docker image directly from the GitLab registry:

.. code-block:: console

   $ docker run -it --rm registry.gitlab.com/python-gitlab/python-gitlab:latest <command> ...

For example, to get a project on GitLab.com (without authentication):

.. code-block:: console

   $ docker run -it --rm registry.gitlab.com/python-gitlab/python-gitlab:latest project get --id gitlab-org/gitlab

You can also mount your own config file:

.. code-block:: console

   $ docker run -it --rm -v /path/to/python-gitlab.cfg:/etc/python-gitlab.cfg registry.gitlab.com/python-gitlab/python-gitlab:latest <command> ...

Building the image
------------------

To build your own image from this repository, run:

.. code-block:: console

   $ docker build -t python-gitlab:latest .

Run your own image:

.. code-block:: console

   $ docker run -it --rm -v python-gitlab:latest <command> ...

Bug reports
===========

Please report bugs and feature requests at
https://github.com/python-gitlab/python-gitlab/issues.

Gitter Community Chat
=====================

There is a `gitter <https://gitter.im/python-gitlab/Lobby>`_ community chat
available at https://gitter.im/python-gitlab/Lobby

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

For guidelines for contributing to ``python-gitlab``, refer to `CONTRIBUTING.rst <https://github.com/python-gitlab/python-gitlab/blob/main/CONTRIBUTING.rst>`_.
