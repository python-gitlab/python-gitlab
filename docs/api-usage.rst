############################
Getting started with the API
############################

The ``gitlab`` package provides 3 basic types:

* ``gitlab.Gitlab`` is the primary class, handling the HTTP requests. It holds
  the GitLab URL and authentication information.
* ``gitlab.GitlabObject`` is the base class for all the GitLab objects. These
  objects provide an abstraction for GitLab resources (projects, groups, and so
  on).
* ``gitlab.BaseManager`` is the base class for objects managers, providing the
  API to manipulate the resources and their attributes.

``gitlab.Gitlab`` class
=======================

To connect to a GitLab server, create a ``gitlab.Gitlab`` object:

.. code-block:: python

   import gitlab

   # private token authentication
   gl = gitlab.Gitlab('http://10.0.0.1', 'JVNSESs8EwWRx5yDxM5q')

   # or username/password authentication
   gl = gitlab.Gitlab('http://10.0.0.1', email='jdoe', password='s3cr3t')

   # make an API request to create the gl.user object. This is mandatory if you
   # use the username/password authentication.
   gl.auth()

You can also use configuration files to create ``gitlab.Gitlab`` objects:

.. code-block:: python

   gl = gitlab.Gitlab.from_config('somewhere', ['/tmp/gl.cfg'])

See the :ref:`cli_configuration` section for more information about
configuration files.


Managers
========

The ``gitlab.Gitlab`` class provides managers to access the GitLab resources.
Each manager provides a set of methods to act on the resources. The available
methods depend on the resource type. Resources are represented as
``gitlab.GitlabObject``-derived objects.

Examples:

.. code-block:: python

   # list all the projects
   projects = gl.projects.list()
   for project in projects:
       print(project)

   # get the group with id == 2
   group = gl.groups.get(2)
   for group in groups:
       print()

   # create a new user
   user_data = {'email': 'jen@foo.com', 'username': 'jen', 'name': 'Jen'}
   user = gl.users.create(user_data)
   print(user)

Some ``gitlab.GitlabObject`` classes also provide managers to access related
GitLab resources:

.. code-block:: python

   # list the issues for a project
   project = gl.projects.get(1)
   issues = project.issues.list()

Gitlab Objects
==============

You can update or delete an object when it exists as a ``GitlabObject`` object:

.. code-block:: python

   # update the attributes of a resource
   project = gl.projects.get(1)
   project.wall_enabled = False
   # don't forget to apply your changes on the server:
   project.save()

   # delete the resource
   project.delete()


Some ``GitlabObject``-derived classes provide additional methods, allowing more
actions on the GitLab resources. For example:

.. code-block:: python

   # get a tarball of the git repository
   project = gl.projects.get(1)
   project.archive()

Pagination
==========

You can use pagination to go throught long lists:

.. code-block:: python

   ten_first_groups = gl.groups.list(page=0, per_page=10)

Use the ``all`` parameter to get all the items when using listing methods:

.. code-block:: python

   all_groups = gl.groups.list(all=True)
   all_owned_projects = gl.projects.owned(all=True)

Sudo
====

If you have the administrator status, you can use ``sudo`` to act as another
user. For example:

.. code-block:: python

   p = gl.projects.create({'name': 'awesome_project'}, sudo='user1')
