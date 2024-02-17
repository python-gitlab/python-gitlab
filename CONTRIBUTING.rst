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

Before contributing, install `tox <https://tox.wiki/>`_ and `pre-commit <https://pre-commit.com>`_:

.. code-block:: bash

  pip3 install --user tox pre-commit
  cd python-gitlab/
  pre-commit install -t pre-commit -t commit-msg --install-hooks

This will help automate adhering to code style and commit message guidelines described below.

If you don't like using ``pre-commit``, feel free to skip installing it, but please **ensure all your
commit messages and code pass all default tox checks** outlined below before pushing your code.

When you're ready or if you'd like to get feedback, please provide your patches as Pull Requests on GitHub.

Commit message guidelines
-------------------------

We enforce commit messages to be formatted using the `Conventional Commits <https://www.conventionalcommits.org/>`_.
This creates a clearer project history, and automates our `Releases`_ and changelog generation. Examples:

* Bad:   ``Added support for release links``
* Good:  ``feat(api): add support for release links``

* Bad:   ``Update documentation for projects``
* Good:  ``docs(projects): update example for saving project attributes``

Coding Style
------------

We use `black <https://github.com/python/black/>`_ and `isort <https://pycqa.github.io/isort/>`_
to format our code, so you'll need to make sure you use it when committing.

Pre-commit hooks will validate and format your code, so you can then stage any changes done if the commit failed.

To format your code according to our guidelines before committing, run:

.. code-block:: bash

  cd python-gitlab/
  tox -e black,isort

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

   # run unit tests using all python3 versions available on your system, and all lint checks:
   tox

   # run unit tests in one python environment only (useful for quick testing during development):
   tox -e py311

   # build the documentation - the result will be generated in build/sphinx/html/:
   tox -e docs

   # List all available tox environments
   tox list

   # "label" based tests. These use the '-m' flag to tox

   # run all the linter checks:
   tox -m lint

   # run only the unit tests:
   tox -m unit

   # run the functional tests. This is very time consuming:
   tox -m func

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
   tox -e api_func_v4

When developing tests it can be a little frustrating to wait for GitLab to spin
up every run. To prevent the containers from being cleaned up afterwards, pass
``--keep-containers`` to pytest, i.e.:

.. code-block:: bash

   tox -e api_func_v4 -- --keep-containers

If you then wish to test against a clean slate, you may perform a manual clean
up of the containers by running:

.. code-block:: bash

   docker-compose -f tests/functional/fixtures/docker-compose.yml -p pytest-python-gitlab down -v

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

Rerunning failed CI workflows
-----------------------------

* Ask the maintainers to add the ``ok-to-test`` label on the PR
* Post a comment in the PR
   ``/rerun-all`` - rerun all failed workflows

   ``/rerun-workflow <workflow name>`` - rerun a specific failed workflow

The functionality is provided by ``rerun-action <https://github.com/marketplace/actions/rerun-actions>``

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
