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

You can contribute to the project in multiple ways:

* Write documentation
* Implement features
* Fix bugs
* Add unit and functional tests
* Everything else you can think of

Development workflow
--------------------

Before contributing, please make sure you have `pre-commit <https://pre-commit.com>`_
installed and configured. This will help automate adhering to code style and commit
message guidelines described below:

.. code-block:: bash

  cd python-gitlab/
  pip3 install --user pre-commit
  pre-commit install -t pre-commit -t commit-msg --install-hooks

Please provide your patches as GitHub pull requests. Thanks!

Commit message guidelines
-------------------------

We enforce commit messages to be formatted using the `conventional-changelog <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines>`_.
This leads to more readable messages that are easy to follow when looking through the project history.

Code-Style
----------

We use black as code formatter, so you'll need to format your changes using the
`black code formatter
<https://github.com/python/black>`_. Pre-commit hooks will validate/format your code
when committing. You can then stage any changes ``black`` added if the commit failed.

To format your code according to our guidelines before committing, run:

.. code-block:: bash

  cd python-gitlab/
  pip3 install --user black
  black .

Running unit tests
------------------

Before submitting a pull request make sure that the tests and lint checks still succeed with
your change. Unit tests and functional tests run in GitHub Actions and
passing checks are mandatory to get merge requests accepted.

Please write new unit tests with pytest and using `responses
<https://github.com/getsentry/responses/>`_.
An example can be found in ``tests/unit/objects/test_runner.py``

You need to install ``tox`` (``pip3 install tox``) to run tests and lint checks locally:

.. code-block:: bash

   # run unit tests using your installed python3, and all lint checks:
   tox -s

   # run unit tests for all supported python3 versions, and all lint checks:
   tox

   # run tests in one environment only:
   tox -epy38

   # build the documentation, the result will be generated in
   # build/sphinx/html/
   tox -edocs

Running integration tests
-------------------------

Integration tests run against a running gitlab instance, using a docker
container. You need to have docker installed on the test machine, and your user
must have the correct permissions to talk to the docker daemon.

To run these tests:

.. code-block:: bash

   # run the CLI tests:
   tox -e cli_func_v4

   # run the python API tests:
   tox -e py_func_v4

By default, the tests run against the latest version of the ``gitlab/gitlab-ce``
image. You can override both the image and tag by providing either the
``GITLAB_IMAGE`` or ``GITLAB_TAG`` environment variables.

This way you can run tests against different versions, such as ``nightly`` for
features in an upcoming release, or an older release (e.g. ``12.8.0-ce.0``).
The tag must match an exact tag on Docker Hub:

.. code-block:: bash

   # run tests against `nightly` or specific tag
   GITLAB_TAG=nightly tox -e py_func_v4
   GITLAB_TAG=12.8.0-ce.0 tox -e py_func_v4

   # run tests against the latest gitlab EE image
   GITLAB_IMAGE=gitlab/gitlab-ee tox -e py_func_v4

A freshly configured gitlab container will be available at
http://localhost:8080 (login ``root`` / password ``5iveL!fe``). A configuration
for python-gitlab will be written in ``/tmp/python-gitlab.cfg``.

To cleanup the environment delete the container:

.. code-block:: bash

   docker rm -f gitlab-test
   docker rm -f gitlab-runner-test

Releases
--------

A release is automatically published once a month on the 28th if any commits merged
to the main branch contain commit message types that signal a semantic version bump
(``fix``, ``feat``, ``BREAKING CHANGE:``).

Additionally, the release workflow can be run manually by maintainers to publish urgent
fixes, either on GitHub or using the ``gh`` CLI with ``gh workflow run release.yml``.

**Note:** As a maintainer, this means you should carefully review commit messages
used by contributors in their pull requests. If scopes such as ``fix`` and ``feat``
are applied to trivial commits not relevant to end users, it's best to squash their
pull requests and summarize the addition in a single conventional commit.
This avoids triggering incorrect version bumps and releases without functional changes.

The release workflow uses `python-semantic-release
<https://python-semantic-release.readthedocs.io>`_ and does the following:

* Bumps the version in ``__version__.py`` and adds an entry in ``CHANGELOG.md``,
* Commits and tags the changes, then pushes to the main branch as the ``github-actions`` user,
* Creates a release from the tag and adds the changelog entry to the release notes,
* Uploads the package as assets to the GitHub release,
* Uploads the package to PyPI using ``PYPI_TOKEN`` (configured as a secret).
