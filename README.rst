.. image:: https://github.com/python-gitlab/python-gitlab/workflows/Test/badge.svg
   :target: https://github.com/python-gitlab/python-gitlab/actions

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

For guidelines for contributing to ``python-gitlab``, refer to `CONTRIBUTING.rst <https://github.com/python-gitlab/python-gitlab/blob/master/CONTRIBUTING.rst>`_.
