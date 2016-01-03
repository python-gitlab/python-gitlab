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

You can use a different configuration file with the :option:`--config-file`
option.

Content
-------

The configuration file uses the ``INI`` format. It contains at least a
``[global]`` section, and a new section for each GitLab server. For example:

.. code-block:: ini

   [global]
   default = somewhere
   ssl_verify = true
   timeout = 5

   [somewhere]
   url = https://some.whe.re
   private_token = vTbFeqJYCY3sibBP7BZM

   [elsewhere]
   url = http://else.whe.re:8080
   private_token = CkqsjqcQSFH5FQKDccu4
   timeout = 1

The ``default`` option of the ``[global]`` section defines the GitLab server to
use if no server is explitly specified with the :option:`--gitlab` CLI option.

The ``[global]`` section also defines the values for the default connexion
parameters. You can override the values in each GitLab server section.

.. list-table:: Global options
   :header-rows: 1

   * - Option
     - Possible values
     - Description
   * - ``ssl_verify``
     - ``True`` or ``False``
     - Verify the SSL certificate. Set to ``False`` if your SSL certificate is
       auto-signed.
   * - ``timeout``
     - Integer
     - Number of seconds to wait for an answer before failing.

You must define the ``url`` and ``private_token`` in each GitLab server
section.

.. list-table:: GitLab server options
   :header-rows: 1

   * - Option
     - Description
   * - ``url``
     - URL for the GitLab server
   * - ``private_token``
     - Your user token. Login/password is not supported.

CLI
===

Objects and actions
-------------------

The ``gitlab`` command expects two mandatory arguments. This first one is the
type of object that you want to manipulate. The second is the action that you
want to perform. For example:

.. code-block:: console

   $ gitlab project list

Use the :option:`--help` option to list the available object types and actions:

.. code-block:: console

   $ gitlab --help
   $ gitlab project --help

Some actions require additional parameters. Use the :option:`--help` option to
list mandatory and optional arguments for an action:

.. code-block:: console

   $ gitlab project create --help

Optional arguments
------------------

Use the following optional arguments to change the behavior of ``gitlab``.
These options must be defined before the mandatory arguments.

``--verbose``, ``-v``
    Outputs detail about retrieved objects.

``--config-file``, ``-c``
    Path to a configuration file.

``--gitlab``, ``-g``
    ID of a GitLab server defined in the configuration file.

Example:

.. code-block:: console

   $ gitlab -v -g elsewhere -c /tmp/gl.cfg project list
