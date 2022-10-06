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

We enforce commit messages to be formatted using the `conventional-changelog <https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit>`_.
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
container. You need to have docker and `docker compose
<https://docs.docker.com/compose/install/>`_
installed on the test machine, and your user must have the correct permissions
to talk to the docker daemon.

To run these tests:

.. code-block:: bash

   # run the CLI tests:
   tox -e cli_func_v4

   # run the python API tests:
   tox -e api_func_v4

When developing tests it can be a little frustrating to wait for GitLab to spin
up every run. To prevent the containers from being cleaned up afterwards, pass
``--keep-containers`` to pytest, i.e.:

.. code-block:: bash

   tox -e api_func_v4 -- --keep-containers

If you then wish to test against a clean slate, you may perform a manual clean
up of the containers by running:

.. code-block:: bash

   docker compose -f tests/functional/fixtures/docker-compose.yml -p pytest-python-gitlab down -v

By default, the tests run against the latest version of the ``gitlab/gitlab-ce``
image. You can override both the image and tag by providing either the
``GITLAB_IMAGE`` or ``GITLAB_TAG`` environment variables.

This way you can run tests against different versions, such as ``nightly`` for
features in an upcoming release, or an older release (e.g. ``12.8.0-ce.0``).
The tag must match an exact tag on Docker Hub:

.. code-block:: bash

   # run tests against ``nightly`` or specific tag
   GITLAB_TAG=nightly tox -e api_func_v4
   GITLAB_TAG=12.8.0-ce.0 tox -e api_func_v4

   # run tests against the latest gitlab EE image
   GITLAB_IMAGE=gitlab/gitlab-ee tox -e api_func_v4

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

* Bumps the version in ``_version.py`` and adds an entry in ``CHANGELOG.md``,
* Commits and tags the changes, then pushes to the main branch as the ``github-actions`` user,
* Creates a release from the tag and adds the changelog entry to the release notes,
* Uploads the package as assets to the GitHub release,
* Uploads the package to PyPI using ``PYPI_TOKEN`` (configured as a secret).
