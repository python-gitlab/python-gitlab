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
   * - ``api_version``
     - ``4``
     - The API version to use to make queries. Only ``4`` is available since 1.5.0.
   * - ``per_page``
     - Integer between 1 and 100
     - The number of items to return in listing queries. GitLab limits the
       value at 100.

You must define the ``url`` in each GitLab server section.

.. warning::

   If the GitLab server you are using redirects requests from http to https,
   make sure to use the ``https://`` protocol in the ``url`` definition.

Only one of ``private_token``, ``oauth_token`` or ``job_token`` should be
defined. If neither are defined an anonymous request will be sent to the Gitlab
server, with very limited permissions.

.. list-table:: GitLab server options
   :header-rows: 1

   * - Option
     - Description
   * - ``url``
     - URL for the GitLab server
   * - ``private_token``
     - Your user token. Login/password is not supported. Refer to `the official
       documentation`_pat to learn how to obtain a token.
   * - ``oauth_token``
     - An Oauth token for authentication. The Gitlab server must be configured
       to support this authentication method.
   * - ``job_token``
     - Your job token. See `the official  documentation`_job-token to learn how to obtain a token.
   * - ``api_version``
     - GitLab API version to use. Only ``4`` is available since 1.5.0.
   * - ``http_username``
     - Username for optional HTTP authentication
   * - ``http_password``
     - Password for optional HTTP authentication

.. _pat: https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html
.. _job-token: https://docs.gitlab.com/ce/api/jobs.html#get-job-artifacts

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

    **Notice:**

        The `PyYAML package <https://pypi.org/project/PyYAML/>`_ is required to use the yaml output option.
        You need to install it separately using ``pip install PyYAML``

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

List values are comma-separated:

.. code-block:: console

   $ gitlab issue list --labels foo,bar

Reading values from files
-------------------------

You can make ``gitlab`` read values from files instead of providing them on the
command line. This is handy for values containing new lines for instance:

.. code-block:: console

   $ cat > /tmp/description << EOF
   This is the description of my project.

   It is obviously the best project around
   EOF
   $ gitlab project create --name SuperProject --description @/tmp/description

Enabling shell autocompletion
============================

To get autocompletion, you'll need to install the package with the extra
"autocompletion":

.. code-block:: console

    pip install python_gitlab[autocompletion]


Add the appropriate command below to your shell's config file so that it is run on
startup. You will likely have to restart or re-login for the autocompletion to
start working.

Bash
----

.. code-block:: console

   eval "$(register-python-argcomplete gitlab)"

tcsh
----

.. code-block:: console

   eval `register-python-argcomplete --shell tcsh gitlab`

fish
----

.. code-block:: console

   register-python-argcomplete --shell fish gitlab | .

Zsh
---

.. warning::

    Zsh autocompletion support is broken right now in the argcomplete python
    package. Perhaps it will be fixed in a future release of argcomplete at
    which point the following instructions will enable autocompletion in zsh.

To activate completions for zsh you need to have bashcompinit enabled in zsh:

.. code-block:: console

   autoload -U bashcompinit
   bashcompinit

Afterwards you can enable completion for gitlab:

.. code-block:: console

   eval "$(register-python-argcomplete gitlab)"
