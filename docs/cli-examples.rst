############
CLI examples
############

.. seealso::

      For a complete list of objects and actions available, see :doc:`/cli-objects`.

CI Lint
-------

Lint a CI YAML configuration from a string:

.. note:: 

   To see output, you will need to use the ``-v``/``--verbose`` flag.

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

Lint a project's CI YAML configuration:

.. code-block:: console

   $ gitlab --verbose project-ci-lint create --project-id group/my-project --content @.gitlab-ci.yml

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

   $ gitlab project list --all

List all projects of a group:

.. code-block:: console

   $ gitlab group-project list --all --group-id 1

List all projects of a group and its subgroups:

.. code-block:: console

   $ gitlab group-project list --all --include-subgroups true --group-id 1

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

Deploy tokens
-------------

Create a deploy token for a project:

.. code-block:: console

   $ gitlab -v project-deploy-token create --project-id 2 \
        --name bar --username root --expires-at "2021-09-09" --scopes "read_repository"

List deploy tokens for a group:

.. code-block:: console

   $ gitlab -v group-deploy-token list --group-id 3

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

Artifacts
---------

Download the artifacts zip archive of a job:

.. code-block:: console

   $ gitlab project-job artifacts --id 10 --project-id 1 > artifacts.zip

Other
-----

Use sudo to act as another user (admin only):

.. code-block:: console

   $ gitlab project create --name user_project1 --sudo username

List values are comma-separated:

.. code-block:: console

   $ gitlab issue list --labels foo,bar