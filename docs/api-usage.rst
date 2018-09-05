############################
Getting started with the API
############################

python-gitlab supports both GitLab v3 and v4 APIs.

.. note::

   To use the v3 make sure to install python-gitlab 1.4. Only the v4 API is
   documented here. See the documentation of earlier versions for the v3 API.

``gitlab.Gitlab`` class
=======================

To connect to a GitLab server, create a ``gitlab.Gitlab`` object:

.. code-block:: python

   import gitlab

   # private token or personal token authentication
   gl = gitlab.Gitlab('http://10.0.0.1', private_token='JVNSESs8EwWRx5yDxM5q')

   # oauth token authentication
   gl = gitlab.Gitlab('http://10.0.0.1', oauth_token='my_long_token_here')

   # username/password authentication (for GitLab << 10.2)
   gl = gitlab.Gitlab('http://10.0.0.1', email='jdoe', password='s3cr3t')

   # anonymous gitlab instance, read-only for public resources
   gl = gitlab.Gitlab('http://10.0.0.1')

   # make an API request to create the gl.user object. This is mandatory if you
   # use the username/password authentication.
   gl.auth()

You can also use configuration files to create ``gitlab.Gitlab`` objects:

.. code-block:: python

   gl = gitlab.Gitlab.from_config('somewhere', ['/tmp/gl.cfg'])

See the :ref:`cli_configuration` section for more information about
configuration files.

.. warning::

   If the GitLab server you are using redirects requests from http to https,
   make sure to use the ``https://`` protocol in the URL definition.

Note on password authentication
-------------------------------

The ``/session`` API endpoint used for username/password authentication has
been removed from GitLab in version 10.2, and is not available on gitlab.com
anymore. Personal token authentication is the preferred authentication method.

If you need username/password authentication, you can use cookie-based
authentication. You can use the web UI form to authenticate, retrieve cookies,
and then use a custom ``requests.Session`` object to connect to the GitLab API.
The following code snippet demonstrates how to automate this:
https://gist.github.com/gpocentek/bd4c3fbf8a6ce226ebddc4aad6b46c0a.

See `issue 380 <https://github.com/python-gitlab/python-gitlab/issues/380>`_
for a detailed discussion.

Managers
========

The ``gitlab.Gitlab`` class provides managers to access the GitLab resources.
Each manager provides a set of methods to act on the resources. The available
methods depend on the resource type.

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

You can list the mandatory and optional attributes for object creation and
update with the manager's ``get_create_attrs()`` and ``get_update_attrs()``
methods. They return 2 tuples, the first one is the list of mandatory
attributes, the second one is the list of optional attribute:

.. code-block:: python

   # v4 only
   print(gl.projects.get_create_attrs())
   (('name',), ('path', 'namespace_id', ...))

The attributes of objects are defined upon object creation, and depend on the
GitLab API itself. To list the available information associated with an object
use the ``attributes`` attribute:

.. code-block:: python

   project = gl.projects.get(1)
   print(project.attributes)

Some objects also provide managers to access related GitLab resources:

.. code-block:: python

   # list the issues for a project
   project = gl.projects.get(1)
   issues = project.issues.list()

Gitlab Objects
==============

You can update or delete a remote object when it exists locally:

.. code-block:: python

   # update the attributes of a resource
   project = gl.projects.get(1)
   project.wall_enabled = False
   # don't forget to apply your changes on the server:
   project.save()

   # delete the resource
   project.delete()

Some classes provide additional methods, allowing more actions on the GitLab
resources. For example:

.. code-block:: python

   # star a git repository
   project = gl.projects.get(1)
   project.star()

Base types
==========

The ``gitlab`` package provides some base types.

* ``gitlab.Gitlab`` is the primary class, handling the HTTP requests. It holds
  the GitLab URL and authentication information.
* ``gitlab.base.RESTObject`` is the base class for all the GitLab v4 objects.
  These objects provide an abstraction for GitLab resources (projects, groups,
  and so on).
* ``gitlab.base.RESTManager`` is the base class for v4 objects managers,
  providing the API to manipulate the resources and their attributes.

Lazy objects
============

To avoid useless API calls to the server you can create lazy objects. These
objects are created locally using a known ID, and give access to other managers
and methods.

The following example will only make one API call to the GitLab server to star
a project (the previous example used 2 API calls):

.. code-block:: python

   # star a git repository
   project = gl.projects.get(1, lazy=True)  # no API call
   project.star()  # API call

Pagination
==========

You can use pagination to iterate over long lists. All the Gitlab objects
listing methods support the ``page`` and ``per_page`` parameters:

.. code-block:: python

   ten_first_groups = gl.groups.list(page=1, per_page=10)

.. warning::

   The first page is page 1, not page 0.

By default GitLab does not return the complete list of items. Use the ``all``
parameter to get all the items when using listing methods:

.. code-block:: python

   all_groups = gl.groups.list(all=True)
   all_owned_projects = gl.projects.list(owned=True, all=True)

You can define the ``per_page`` value globally to avoid passing it to every
``list()`` method call:

.. code-block:: python

   gl = gitlab.Gitlab(url, token, per_page=50)

``list()`` methods can also return a generator object which will handle the
next calls to the API when required. This is the recommended way to iterate
through a large number of items:

.. code-block:: python

   items = gl.groups.list(as_list=False)
   for item in items:
       print(item.attributes)

The generator exposes extra listing information as received from the server:

* ``current_page``: current page number (first page is 1)
* ``prev_page``: if ``None`` the current page is the first one
* ``next_page``: if ``None`` the current page is the last one
* ``per_page``: number of items per page
* ``total_pages``: total number of pages available
* ``total``: total number of items in the list

Sudo
====

If you have the administrator status, you can use ``sudo`` to act as another
user. For example:

.. code-block:: python

   p = gl.projects.create({'name': 'awesome_project'}, sudo='user1')

Advanced HTTP configuration
===========================

python-gitlab relies on ``requests`` ``Session`` objects to perform all the
HTTP requests to the Gitlab servers.

You can provide your own ``Session`` object with custom configuration when
you create a ``Gitlab`` object.

Context manager
---------------

You can use ``Gitlab`` objects as context managers. This makes sure that the
``requests.Session`` object associated with a ``Gitlab`` instance is always
properly closed when you exit a ``with`` block:

.. code-block:: python

   with gitlab.Gitlab(host, token) as gl:
       gl.projects.list()

.. warning::

   The context manager will also close the custom ``Session`` object you might
   have used to build the ``Gitlab`` instance.

Proxy configuration
-------------------

The following sample illustrates how to define a proxy configuration when using
python-gitlab:

.. code-block:: python

   import gitlab
   import requests

   session = requests.Session()
   session.proxies = {
       'https': os.environ.get('https_proxy'),
       'http': os.environ.get('http_proxy'),
   }
   gl = gitlab.gitlab(url, token, api_version=4, session=session)

Reference:
http://docs.python-requests.org/en/master/user/advanced/#proxies

Client side certificate
-----------------------

The following sample illustrates how to use a client-side certificate:

.. code-block:: python

   import gitlab
   import requests

   session = requests.Session()
   session.cert = ('/path/to/client.cert', '/path/to/client.key')
   gl = gitlab.gitlab(url, token, api_version=4, session=session)

Reference:
http://docs.python-requests.org/en/master/user/advanced/#client-side-certificates

Rate limits
-----------

python-gitlab obeys the rate limit of the GitLab server by default.  On
receiving a 429 response (Too Many Requests), python-gitlab sleeps for the
amount of time in the Retry-After header that GitLab sends back.

If you don't want to wait, you can disable the rate-limiting feature, by
supplying the ``obey_rate_limit`` argument.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(all=True, obey_rate_limit=False)


.. warning::

   You will get an Exception, if you then go over the rate limit of your GitLab instance.
