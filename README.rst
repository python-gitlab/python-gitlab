python-gitlab
=============

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

.. image:: https://img.shields.io/github/license/python-gitlab/python-gitlab
   :target: https://github.com/python-gitlab/python-gitlab/blob/main/COPYING

``python-gitlab`` is a Python package providing access to the GitLab APIs.

It includes a client for GitLab's v4 REST API, synchronous and asynchronous GraphQL API
clients, as well as a CLI tool (``gitlab``) wrapping REST API endpoints.

.. _features:

Features
--------

``python-gitlab`` enables you to:

* write Pythonic code to manage your GitLab resources.
* pass arbitrary parameters to the GitLab API. Simply follow GitLab's docs
  on what parameters are available.
* use a synchronous or asynchronous client when using the GraphQL API.
* access arbitrary endpoints as soon as they are available on GitLab, by using
  lower-level API methods.
* use persistent requests sessions for authentication, proxy and certificate handling.
* handle smart retries on network and server errors, with rate-limit handling.
* flexible handling of paginated responses, including lazy iterators.
* automatically URL-encode paths and parameters where needed.
* automatically convert some complex data structures to API attribute types
* merge configuration from config files, environment variables and arguments.

Installation
------------

As of 5.0.0, ``python-gitlab`` is compatible with Python 3.9+.

Use ``pip`` to install the latest stable version of ``python-gitlab``:

.. code-block:: console

   $ pip install --upgrade python-gitlab

The current development version is available on both `GitHub.com
<https://github.com/python-gitlab/python-gitlab>`__ and `GitLab.com
<https://gitlab.com/python-gitlab/python-gitlab>`__, and can be
installed directly from the git repository:

.. code-block:: console

   $ pip install git+https://github.com/python-gitlab/python-gitlab.git

From GitLab:

.. code-block:: console

   $ pip install git+https://gitlab.com/python-gitlab/python-gitlab.git

Using the docker images
-----------------------

``python-gitlab`` provides Docker images in two flavors, based on the Alpine and Debian slim
python `base images <https://hub.docker.com/_/python>`__. The default tag is ``alpine``,
but you can explicitly use the alias (see below).

The alpine image is smaller, but you may want to use the Debian-based slim tag (currently 
based on ``-slim-bullseye``) if you are running into issues or need a more complete environment
with a bash shell, such as in CI jobs.

The images are published on the GitLab registry, for example:

* ``registry.gitlab.com/python-gitlab/python-gitlab:latest`` (latest, alpine alias)
* ``registry.gitlab.com/python-gitlab/python-gitlab:alpine`` (latest alpine)
* ``registry.gitlab.com/python-gitlab/python-gitlab:slim-bullseye`` (latest slim-bullseye)
* ``registry.gitlab.com/python-gitlab/python-gitlab:v3.2.0`` (alpine alias)
* ``registry.gitlab.com/python-gitlab/python-gitlab:v3.2.0-alpine``
* ``registry.gitlab.com/python-gitlab/python-gitlab:v3.2.0-slim-bullseye``

You can run the Docker image directly from the GitLab registry:

.. code-block:: console

   $ docker run -it --rm registry.gitlab.com/python-gitlab/python-gitlab:latest <command> ...

For example, to get a project on GitLab.com (without authentication):

.. code-block:: console

   $ docker run -it --rm registry.gitlab.com/python-gitlab/python-gitlab:latest project get --id gitlab-org/gitlab

You can also mount your own config file:

.. code-block:: console

   $ docker run -it --rm -v /path/to/python-gitlab.cfg:/etc/python-gitlab.cfg registry.gitlab.com/python-gitlab/python-gitlab:latest <command> ...

Usage inside GitLab CI
~~~~~~~~~~~~~~~~~~~~~~

If you want to use the Docker image directly inside your GitLab CI as an ``image``, you will need to override
the ``entrypoint``, `as noted in the official GitLab documentation <https://docs.gitlab.com/ee/ci/docker/using_docker_images.html#override-the-entrypoint-of-an-image>`__:

.. code-block:: yaml

   Job Name:
      image:
         name: registry.gitlab.com/python-gitlab/python-gitlab:latest
         entrypoint: [""]
      before_script:
         gitlab --version
      script:
         gitlab <command>

Building the image
~~~~~~~~~~~~~~~~~~

To build your own image from this repository, run:

.. code-block:: console

   $ docker build -t python-gitlab:latest .

Run your own image:

.. code-block:: console

   $ docker run -it --rm python-gitlab:latest <command> ...

Build a Debian slim-based image:

.. code-block:: console

   $ docker build -t python-gitlab:latest --build-arg PYTHON_FLAVOR=slim-bullseye .

Bug reports
-----------

Please report bugs and feature requests at
https://github.com/python-gitlab/python-gitlab/issues.

Gitter Community Chat
---------------------

We have a `gitter <https://gitter.im/python-gitlab/Lobby>`_ community chat
available at https://gitter.im/python-gitlab/Lobby, which you can also
directly access via the Open Chat button below.

If you have a simple question, the community might be able to help already,
without you opening an issue. If you regularly use python-gitlab, we also
encourage you to join and participate. You might discover new ideas and
use cases yourself!

Documentation
-------------

The full documentation for CLI and API is available on `readthedocs
<http://python-gitlab.readthedocs.org/en/stable/>`_.

Build the docs
~~~~~~~~~~~~~~

We use ``tox`` to manage our environment and build the documentation::

    pip install tox
    tox -e docs

Contributing
------------

For guidelines for contributing to ``python-gitlab``, refer to `CONTRIBUTING.rst <https://github.com/python-gitlab/python-gitlab/blob/main/CONTRIBUTING.rst>`_.
