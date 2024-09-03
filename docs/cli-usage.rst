#############
Using the CLI
#############

``python-gitlab`` provides a :command:`gitlab` command-line tool to interact
with GitLab servers.

This is especially convenient for running quick ad-hoc commands locally, easily
interacting with the API inside GitLab CI, or with more advanced shell scripting
when integrating with other tooling.

.. _cli_configuration:

Configuration
=============

``gitlab`` allows setting configuration options via command-line arguments,
environment variables, and configuration files.

For a complete list of global CLI options and their environment variable
equivalents, see :doc:`/cli-objects`.

With no configuration provided, ``gitlab`` will default to unauthenticated
requests against `GitLab.com <https://gitlab.com>`__.

With no configuration but running inside a GitLab CI job, it will default to
authenticated requests using the current job token against the current instance
(via ``CI_SERVER_URL`` and ``CI_JOB_TOKEN`` environment variables).

.. warning::
   Please note the job token has very limited permissions and can only be used
   with certain endpoints. You may need to provide a personal access token instead.

When you provide configuration, values are evaluated with the following precedence:

1. Explicitly provided CLI arguments,
2. Environment variables,
3. Configuration files:

   a. explicitly defined config files:

      i. via the ``--config-file`` CLI argument,
      ii. via the ``PYTHON_GITLAB_CFG`` environment variable,

   b. user-specific config file,
   c. system-level config file,

4. Environment variables always present in CI (``CI_SERVER_URL``, ``CI_JOB_TOKEN``).

Additionally, authentication will take the following precedence
when multiple options or environment variables are present:

1. Private token,
2. OAuth token,
3. CI job token.


Configuration files
-------------------

``gitlab`` looks up 3 configuration files by default:

The ``PYTHON_GITLAB_CFG`` environment variable
    An environment variable that contains the path to a configuration file.

``/etc/python-gitlab.cfg``
    System-wide configuration file

``~/.python-gitlab.cfg``
    User configuration file

You can use a different configuration file with the ``--config-file`` option.

.. warning::
    If the ``PYTHON_GITLAB_CFG`` environment variable is defined and the target
    file exists, it will be the only configuration file parsed by ``gitlab``.  

    If the environment variable is defined and the target file cannot be accessed,
    ``gitlab`` will fail explicitly.

Configuration file format
-------------------------

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
   private_token = helper: path/to/helper.sh
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
   * - ``user_agent``
     - ``str``
     - A string defining a custom user agent to use when ``gitlab`` makes requests.

You must define the ``url`` in each GitLab server section.

.. warning::

   Note that a url that results in 301/302 redirects will raise an error,
   so it is highly recommended to use the final destination in the ``url`` field.
   For example, if the GitLab server you are using redirects requests from http
   to https, make sure to use the ``https://`` protocol in the URL definition.

   A URL that redirects using 301/302 (rather than 307/308) will most likely
   `cause malformed POST and PUT requests <https://github.com/psf/requests/blob/c45a4dfe6bfc6017d4ea7e9f051d6cc30972b310/requests/sessions.py#L324-L332>`_.

   python-gitlab will therefore raise a ``RedirectionError`` when it encounters
   a redirect which it believes will cause such an error, to avoid confusion
   between successful GET and failing POST/PUT requests on the same instance.

Only one of ``private_token``, ``oauth_token`` or ``job_token`` should be
defined. If neither are defined an anonymous request will be sent to the Gitlab
server, with very limited permissions.

We recommend that you use `Credential helpers`_ to securely store your tokens.

.. list-table:: GitLab server options
   :header-rows: 1

   * - Option
     - Description
   * - ``url``
     - URL for the GitLab server. Do **NOT** use a URL which redirects.
   * - ``private_token``
     - Your user token. Login/password is not supported. Refer to `the
       official documentation
       <https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html>`__
       to learn how to obtain a token.
   * - ``oauth_token``
     - An Oauth token for authentication. The Gitlab server must be configured
       to support this authentication method.
   * - ``job_token``
     - Your job token. See `the official documentation
       <https://docs.gitlab.com/ce/api/jobs.html#get-job-artifacts>`__
       to learn how to obtain a token.
   * - ``api_version``
     - GitLab API version to use. Only ``4`` is available since 1.5.0.

Credential helpers
------------------

For all configuration options that contain secrets (for example,
``personal_token``, ``oauth_token``, ``job_token``), you can specify
a helper program to retrieve the secret indicated by a ``helper:``
prefix. This allows you to fetch values from a local keyring store
or cloud-hosted vaults such as Bitwarden. Environment variables are
expanded if they exist and ``~`` expands to your home directory.

It is expected that the helper program prints the secret to standard output.
To use shell features such as piping to retrieve the value, you will need
to use a wrapper script; see below.

Example for a `keyring <https://github.com/jaraco/keyring>`_ helper:

.. code-block:: ini

   [global]
   default = somewhere
   ssl_verify = true
   timeout = 5

   [somewhere]
   url = http://somewhe.re
   private_token = helper: keyring get Service Username
   timeout = 1

Example for a `pass <https://www.passwordstore.org>`_ helper with a wrapper script:

.. code-block:: ini

   [global]
   default = somewhere
   ssl_verify = true
   timeout = 5

   [somewhere]
   url = http://somewhe.re
   private_token = helper: /path/to/helper.sh
   timeout = 1

In ``/path/to/helper.sh``:

.. code-block:: bash

    #!/bin/bash
    pass show path/to/credentials | head -n 1

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

.. important::

        The `PyYAML package <https://pypi.org/project/PyYAML/>`_ is required to use the yaml output option.
        You need to install it explicitly using ``pip install python-gitlab[yaml]``

``--fields``, ``-f``
    Comma-separated list of fields to display (``yaml`` and ``json`` output
    formats only).  If not used, all the object fields are displayed.

Example:

.. code-block:: console

   $ gitlab -o yaml -f id,permissions -g elsewhere -c /tmp/gl.cfg project list

.. _cli_from_files:

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

It you want to explicitly pass an argument starting with ``@``,  you can escape it using ``@@``:

.. code-block:: console
  
   $ gitlab project-tag list --project-id somenamespace/myproject
   ...
   name: @at-started-tag
   ...
   $ gitlab project-tag delete --project-id somenamespace/myproject --name '@@at-started-tag'


Enabling shell autocompletion
=============================

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

   eval ``register-python-argcomplete --shell tcsh gitlab``

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
