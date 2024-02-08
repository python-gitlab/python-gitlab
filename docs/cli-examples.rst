############
CLI examples
############

.. seealso::

      For a complete list of objects and actions available, see :doc:`/cli-objects`.

CI Lint
-------

**ci-lint has been Removed in Gitlab 16, use project-ci-lint instead**

Lint a CI YAML configuration from a string:

.. note::

   To see output, you will need to use the ``-v``/``--verbose`` flag.

   To exit with non-zero on YAML lint failures instead, use the ``validate``
   subcommand shown below.

.. code-block:: console

   $ gitlab --verbose ci-lint create --content \
     "---
     test:
       script:
         - echo hello
     "

Lint a CI YAML configuration from a file (see :ref:`cli_from_files`):

.. code-block:: console

   $ gitlab --verbose ci-lint create --content @.gitlab-ci.yml

Validate a CI YAML configuration from a file (lints and exits with non-zero on failure):

.. code-block:: console

   $ gitlab ci-lint validate --content @.gitlab-ci.yml

Project CI Lint
---------------

Lint a project's CI YAML configuration:

.. code-block:: console

   $ gitlab --verbose project-ci-lint create --project-id group/my-project --content @.gitlab-ci.yml

Validate a project's CI YAML configuration (lints and exits with non-zero on failure):

.. code-block:: console

   $ gitlab project-ci-lint validate --project-id group/my-project --content @.gitlab-ci.yml

Lint a project's current CI YAML configuration:

.. code-block:: console

   $ gitlab --verbose project-ci-lint get --project-id group/my-project

Lint a project's current CI YAML configuration on a specific branch:

.. code-block:: console

   $ gitlab --verbose project-ci-lint get --project-id group/my-project --ref my-branch

Projects
--------

List the projects (paginated):

.. code-block:: console

   $ gitlab project list

List all the projects:

.. code-block:: console

   $ gitlab project list --get-all

List all projects of a group:

.. code-block:: console

   $ gitlab group-project list --get-all --group-id 1

List all projects of a group and its subgroups:

.. code-block:: console

   $ gitlab group-project list --get-all --include-subgroups true --group-id 1

Limit to 5 items per request, display the 1st page only

.. code-block:: console

   $ gitlab project list --page 1 --per-page 5

Get a specific project (id 2):

.. code-block:: console

   $ gitlab project get --id 2

Users
-----

Get a specific user by id:

.. code-block:: console

   $ gitlab user get --id 3

Create a user impersonation token (admin-only):

.. code-block:: console

   gitlab user-impersonation-token create --user-id 2 --name test-token --scopes api,read_user

Deploy tokens
-------------

Create a deploy token for a project:

.. code-block:: console

   $ gitlab -v project-deploy-token create --project-id 2 \
        --name bar --username root --expires-at "2021-09-09" --scopes "api,read_repository"

List deploy tokens for a group:

.. code-block:: console

   $ gitlab -v group-deploy-token list --group-id 3

Personal access tokens
----------------------

List the current user's personal access tokens (or all users' tokens, if admin):

.. code-block:: console

   $ gitlab -v personal-access-token list

Revoke a personal access token by id:

.. code-block:: console

   $ gitlab personal-access-token delete --id 1

Revoke the personal access token currently used:

.. code-block:: console

   $ gitlab personal-access-token delete --id self

Create a personal access token for a user (admin only):

.. code-block:: console

   $ gitlab -v user-personal-access-token create --user-id 2 \
        --name personal-access-token --expires-at "2023-01-01" --scopes "api,read_repository"

Resource access tokens
----------------------

Create a project access token:

.. code-block:: console

   $ gitlab -v project-access-token create --project-id 2 \
        --name project-token --expires-at "2023-01-01" --scopes "api,read_repository"

List project access tokens:

.. code-block:: console

   $ gitlab -v project-access-token list --project-id 3

Revoke a project access token:

.. code-block:: console

   $ gitlab project-access-token delete --project-id 3 --id 1

Create a group access token:

.. code-block:: console

   $ gitlab -v group-access-token create --group-id 2 \
        --name group-token --expires-at "2022-01-01" --scopes "api,read_repository"

List group access tokens:

.. code-block:: console

   $ gitlab -v group-access-token list --group-id 3

Revoke a group access token:

.. code-block:: console

   $ gitlab group-access-token delete --group-id 3 --id 1

Packages
--------

List packages for a project:

.. code-block:: console

   $ gitlab -v project-package list --project-id 3

List packages for a group:

.. code-block:: console

   $ gitlab -v group-package list --group-id 3

Get a specific project package by id:

.. code-block:: console

   $ gitlab -v project-package get --id 1 --project-id 3

Delete a specific project package by id:

.. code-block:: console

   $ gitlab -v project-package delete --id 1 --project-id 3

Upload a generic package to a project:

.. code-block:: console

   $ gitlab generic-package upload --project-id 1 --package-name hello-world \
        --package-version v1.0.0 --file-name hello.tar.gz --path /path/to/hello.tar.gz

Download a project's generic package:

.. code-block:: console

   $ gitlab generic-package download --project-id 1 --package-name hello-world \
        --package-version v1.0.0 --file-name hello.tar.gz > /path/to/hello.tar.gz

Issues
------

Get a list of issues for this project:

.. code-block:: console

   $ gitlab project-issue list --project-id 2

Snippets
--------

Delete a snippet (id 3):

.. code-block:: console

   $ gitlab project-snippet delete --id 3 --project-id 2

Update a snippet:

.. code-block:: console

   $ gitlab project-snippet update --id 4 --project-id 2 \
       --code "My New Code"

Create a snippet:

.. code-block:: console

   $ gitlab project-snippet create --project-id 2
   Impossible to create object (Missing attribute(s): title, file-name, code)
   $ # oops, let's add the attributes:
   $ gitlab project-snippet create --project-id 2 --title "the title" \
       --file-name "the name" --code "the code"

Commits
-------

Get a specific project commit by its SHA id:

.. code-block:: console

   $ gitlab project-commit get --project-id 2 --id a43290c

Get the signature (e.g. GPG or x509) of a signed commit:

.. code-block:: console

   $ gitlab project-commit signature --project-id 2 --id a43290c

Define the status of a commit (as would be done from a CI tool for example):

.. code-block:: console

   $ gitlab project-commit-status create --project-id 2 \
       --commit-id a43290c --state success --name ci/jenkins \
       --target-url http://server/build/123 \
       --description "Jenkins build succeeded"

Get the merge base for two or more branches, tags or commits:

.. code-block:: console

    gitlab project repository-merge-base --id 1 --refs bd1324e2f,main,v1.0.0

Artifacts
---------

Download the artifacts zip archive of a job:

.. code-block:: console

   $ gitlab project-job artifacts --id 10 --project-id 1 > artifacts.zip

Runners
-------

List owned runners:

.. code-block:: console

   $ gitlab runner list

List owned runners with a filter:

.. code-block:: console

   $ gitlab runner list --scope active

List all runners in the GitLab instance (specific and shared):

.. code-block:: console

   $ gitlab runner-all list

Get a runner's details:

.. code-block:: console

   $ gitlab -v runner get --id 123

Other
-----

Use sudo to act as another user (admin only):

.. code-block:: console

   $ gitlab project create --name user_project1 --sudo username

List values are comma-separated:

.. code-block:: console

   $ gitlab issue list --labels foo,bar