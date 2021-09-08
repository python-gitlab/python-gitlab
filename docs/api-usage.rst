############################
Getting started with the API
############################

python-gitlab only supports GitLab API v4.

``gitlab.Gitlab`` class
=======================

To connect to GitLab.com or another GitLab instance, create a ``gitlab.Gitlab`` object:

.. code-block:: python

   import gitlab

   # anonymous read-only access for public resources (GitLab.com)
   gl = gitlab.Gitlab()

   # anonymous read-only access for public resources (self-hosted GitLab instance)
   gl = gitlab.Gitlab('https://gitlab.example.com')

   # private token or personal token authentication (GitLab.com)
   gl = gitlab.Gitlab(private_token='JVNSESs8EwWRx5yDxM5q')

   # private token or personal token authentication (self-hosted GitLab instance)
   gl = gitlab.Gitlab(url='https://gitlab.example.com', private_token='JVNSESs8EwWRx5yDxM5q')

   # oauth token authentication
   gl = gitlab.Gitlab('https://gitlab.example.com', oauth_token='my_long_token_here')

   # job token authentication (to be used in CI)
   import os
   gl = gitlab.Gitlab('https://gitlab.example.com', job_token=os.environ['CI_JOB_TOKEN'])

   # Define your own custom user agent for requests
   gl = gitlab.Gitlab('https://gitlab.example.com', user_agent='my-package/1.0.0')

   # make an API request to create the gl.user object. This is mandatory if you
   # use the username/password authentication.
   gl.auth()

You can also use configuration files to create ``gitlab.Gitlab`` objects:

.. code-block:: python

   gl = gitlab.Gitlab.from_config('somewhere', ['/tmp/gl.cfg'])

See the :ref:`cli_configuration` section for more information about
configuration files.

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
   for project in group.projects.list():
       print(project)

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

python-gitlab allows to send any data to the GitLab server when making queries.
In case of invalid or missing arguments python-gitlab will raise an exception
with the GitLab server error message:

.. code-block:: python

   >>> gl.projects.list(sort='invalid value')
   ...
   GitlabListError: 400: sort does not have a valid value

You can use the ``query_parameters`` argument to send arguments that would
conflict with python or python-gitlab when using them as kwargs:

.. code-block:: python

   gl.user_activities.list(from='2019-01-01')  ## invalid

   gl.user_activities.list(query_parameters={'from': '2019-01-01'})  # OK

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

Gitlab allows to also use keyset pagination. You can supply it to your project listing,
but you can also do so globally. Be aware that GitLab then also requires you to only use supported
order options. At the time of writing, only ``order_by="id"`` works.

.. code-block:: python

   gl = gitlab.Gitlab(url, token, pagination="keyset", order_by="id", per_page=100)
   gl.projects.list()

Reference:
https://docs.gitlab.com/ce/api/README.html#keyset-based-pagination

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
https://2.python-requests.org/en/master/user/advanced/#proxies

SSL certificate verification
----------------------------

python-gitlab relies on the CA certificate bundle in the `certifi` package
that comes with the requests library.

If you need python-gitlab to use your system CA store instead, you can provide
the path to the CA bundle in the `REQUESTS_CA_BUNDLE` environment variable.

Reference:
https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification

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
https://2.python-requests.org/en/master/user/advanced/#client-side-certificates

Rate limits
-----------

python-gitlab obeys the rate limit of the GitLab server by default.  On
receiving a 429 response (Too Many Requests), python-gitlab sleeps for the
amount of time in the Retry-After header that GitLab sends back.  If GitLab
does not return a response with the Retry-After header, python-gitlab will
perform an exponential backoff.

If you don't want to wait, you can disable the rate-limiting feature, by
supplying the ``obey_rate_limit`` argument.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(all=True, obey_rate_limit=False)

If you do not disable the rate-limiting feature, you can supply a custom value
for ``max_retries``; by default, this is set to 10. To retry without bound when
throttled, you can set this parameter to -1. This parameter is ignored if
``obey_rate_limit`` is set to ``False``.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(all=True, max_retries=12)

.. warning::

   You will get an Exception, if you then go over the rate limit of your GitLab instance.

Transient errors
----------------

GitLab server can sometimes return a transient HTTP error.
python-gitlab can automatically retry in such case, when
``retry_transient_errors`` argument is set to ``True``.  When enabled,
HTTP error codes 500 (Internal Server Error), 502 (502 Bad Gateway),
503 (Service Unavailable), and 504 (Gateway Timeout) are retried.  By
default an exception is raised for these errors.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(all=True, retry_transient_errors=True)

The default ``retry_transient_errors`` can also be set on the ``Gitlab`` object
and overridden by individual API calls.

.. code-block:: python

   import gitlab
   import requests
   gl = gitlab.gitlab(url, token, api_version=4, retry_transient_errors=True)
   gl.projects.list(all=True)                               # retries due to default value
   gl.projects.list(all=True, retry_transient_errors=False) # does not retry

Timeout
-------

python-gitlab will by default use the ``timeout`` option from it's configuration
for all requests. This is passed downwards to the ``requests`` module at the
time of making the HTTP request. However if you would like to override the
global timeout parameter for a particular call, you can provide the ``timeout``
parameter to that API invocation:

.. code-block:: python

   import gitlab

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.import_github(ACCESS_TOKEN, 123456, "root", timeout=120.0)

.. _object_attributes:

Attributes in updated objects
=============================

When methods manipulate an existing object, such as with ``refresh()`` and ``save()``,
the object will only have attributes that were returned by the server. In some cases,
such as when the initial request fetches attributes that are needed later for additional
processing, this may not be desired:

.. code-block:: python

   project = gl.projects.get(1, statistics=True)
   project.statistics

   project.refresh()
   project.statistics # AttributeError

To avoid this, either copy the object/attributes before calling ``refresh()``/``save()``
or subsequently perform another ``get()`` call as needed, to fetch the attributes you want.
