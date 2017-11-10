####################
``gitlab`` CLI usage
####################

``python-gitlab`` provides a :command:`gitlab` command-line tool to interact
with GitLab servers. It uses a configuration file to define how to connect to
the servers.

.. _cli_configuration:

Configuration
=============

Files
-----

``gitlab`` looks up 2 configuration files by default:

``/etc/python-gitlab.cfg``
    System-wide configuration file

``~/.python-gitlab.cfg``
    User configuration file

You can use a different configuration file with the ``--config-file`` option.

Content
-------

The configuration file uses the ``INI`` format. It contains at least a
``[global]`` section, and a specific section for each GitLab server. For
example:

.. code-block:: ini

   [global]
   default = somewhere
   ssl_verify = true
   timeout = 5
   api_version = 3

   [somewhere]
   url = https://some.whe.re
   private_token = vTbFeqJYCY3sibBP7BZM
   api_version = 4

   [elsewhere]
   url = http://else.whe.re:8080
   private_token = CkqsjqcQSFH5FQKDccu4
   timeout = 1

The ``default`` option of the ``[global]`` section defines the GitLab server to
use if no server is explicitly specified with the ``--gitlab`` CLI option.

The ``[global]`` section also defines the values for the default connection
parameters. You can override the values in each GitLab server section.

.. list-table:: Global options
   :header-rows: 1

   * - Option
     - Possible values
     - Description
   * - ``ssl_verify``
     - ``True``, ``False``, or a ``str``
     - Verify the SSL certificate. Set to ``False`` to disable verification,
       though this will create warnings. Any other value is interpreted as path
       to a CA_BUNDLE file or directory with certificates of trusted CAs.
   * - ``timeout``
     - Integer
     - Number of seconds to wait for an answer before failing.

You must define the ``url`` in each GitLab server section.

Only one of ``private_token`` or ``oauth_token`` should be defined. If neither
are defined an anonymous request will be sent to the Gitlab server, with very
limited permissions.

.. list-table:: GitLab server options
   :header-rows: 1

   * - Option
     - Description
   * - ``url``
     - URL for the GitLab server
   * - ``private_token``
     - Your user token. Login/password is not supported. Refer to `the official
       documentation`__ to learn how to obtain a token.
   * - ``oauth_token``
     - An Oauth token for authentication. The Gitlab server must be configured
       to support this authentication method.
   * - ``api_version``
     - GitLab API version to use (``3`` or ``4``). Defaults to ``3`` for now,
       but will switch to ``4`` eventually.
   * - ``http_username``
     - Username for optional HTTP authentication
   * - ``http_password``
     - Password for optional HTTP authentication

__ https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html

CLI
===

Objects and actions
-------------------

The ``gitlab`` command expects two mandatory arguments. The first one is the
type of object that you want to manipulate. The second is the action that you
want to perform. For example:

.. code-block:: console

   $ gitlab project list

Use the ``--help`` option to list the available object types and actions:

.. code-block:: console

   $ gitlab --help
   $ gitlab project --help

Some actions require additional parameters. Use the ``--help`` option to
list mandatory and optional arguments for an action:

.. code-block:: console

   $ gitlab project create --help

Optional arguments
------------------

Use the following optional arguments to change the behavior of ``gitlab``.
These options must be defined before the mandatory arguments.

``--verbose``, ``-v``
    Outputs detail about retrieved objects. Available for legacy (default)
    output only.

``--config-file``, ``-c``
    Path to a configuration file.

``--gitlab``, ``-g``
    ID of a GitLab server defined in the configuration file.

``--output``, ``-o``
    Output format. Defaults to a custom format. Can also be ``yaml`` or ``json``.

``--fields``, ``-f``
    Comma-separated list of fields to display (``yaml`` and ``json`` output
    formats only).  If not used, all the object fields are displayed.

Example:

.. code-block:: console

   $ gitlab -o yaml -f id,permissions -g elsewhere -c /tmp/gl.cfg project list


Examples
========

List the projects (paginated):

.. code-block:: console

   $ gitlab project list

List all the projects:

.. code-block:: console

   $ gitlab project list --all

Limit to 5 items per request, display the 1st page only

.. code-block:: console

   $ gitlab project list --page 1 --per-page 5

Get a specific project (id 2):

.. code-block:: console

   $ gitlab project get --id 2

Get a specific user by id:

.. code-block:: console

   $ gitlab user get --id 3

Get a list of snippets for this project:

.. code-block:: console

   $ gitlab project-issue list --project-id 2

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

Define the status of a commit (as would be done from a CI tool for example):

.. code-block:: console

   $ gitlab project-commit-status create --project-id 2 \
       --commit-id a43290c --state success --name ci/jenkins \
       --target-url http://server/build/123 \
       --description "Jenkins build succeeded"

Use sudo to act as another user (admin only):

.. code-block:: console

   $ gitlab project create --name user_project1 --sudo username
