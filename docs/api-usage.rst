##################
Using the REST API
##################

python-gitlab currently only supports v4 of the GitLab REST API.

``gitlab.Gitlab`` class
=======================

To connect to GitLab.com or another GitLab instance, create a ``gitlab.Gitlab`` object:

.. hint::

   You can use different types of tokens for authenticated requests against the GitLab API.
   You will most likely want to use a resource (project/group) access token or a personal
   access token.

   For the full list of available options and how to obtain these tokens, please see
   https://docs.gitlab.com/ee/api/rest/authentication.html.

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
   # bear in mind the limitations of the API endpoints it supports:
   # https://docs.gitlab.com/ee/ci/jobs/ci_job_token.html
   import os
   gl = gitlab.Gitlab('https://gitlab.example.com', job_token=os.environ['CI_JOB_TOKEN'])

   # Define your own custom user agent for requests
   gl = gitlab.Gitlab('https://gitlab.example.com', user_agent='my-package/1.0.0')

   # make an API request to create the gl.user object. This is not required but may be useful
   # to validate your token authentication. Note that this will not work with job tokens.
   gl.auth()

   # Enable "debug" mode. This can be useful when trying to determine what
   # information is being sent back and forth to the GitLab server.
   # Note: this will cause credentials and other potentially sensitive
   # information to be printed to the terminal.
   gl.enable_debug()

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

GitLab has long removed password-based basic authentication. You can currently still use the
`resource owner password credentials <https://docs.gitlab.com/ee/api/oauth2.html#resource-owner-password-credentials-flow>`_
flow to obtain an OAuth token.

However, we do not recommend this as it will not work with 2FA enabled, and GitLab is removing
ROPC-based flows without client IDs in a future release. We recommend you obtain tokens for
automated workflows as linked above or obtain a session cookie from your browser.

For a python example of password authentication using the ROPC-based OAuth2
flow, see `this Ansible snippet <https://github.com/ansible-collections/community.general/blob/1c06e237c8100ac30d3941d5a3869a4428ba2974/plugins/module_utils/gitlab.py#L86-L92>`_.

Managers
========

The ``gitlab.Gitlab`` class provides managers to access the GitLab resources.
Each manager provides a set of methods to act on the resources. The available
methods depend on the resource type.

Examples:

.. code-block:: python

   # list all the projects
   projects = gl.projects.list(iterator=True)
   for project in projects:
       print(project)

   # get the group with id == 2
   group = gl.groups.get(2)
   for project in group.projects.list(iterator=True):
       print(project)

.. warning::
   Calling ``list()`` without any arguments will by default not return the complete list
   of items. Use either the ``get_all=True`` or ``iterator=True`` parameters to get all the
   items when using listing methods. See the :ref:`pagination` section for more
   information.

.. code-block:: python

   # create a new user
   user_data = {'email': 'jen@foo.com', 'username': 'jen', 'name': 'Jen'}
   user = gl.users.create(user_data)
   print(user)

.. note:: 
   python-gitlab attempts to sync the required, optional, and mutually exclusive attributes
   for resource creation and update with the upstream API.
   
   You are encouraged to follow upstream API documentation for each resource to find these -
   each resource documented here links to the corresponding upstream resource documentation
   at the top of the page.

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
   issues = project.issues.list(get_all=True)

python-gitlab allows to send any data to the GitLab server when making queries.
In case of invalid or missing arguments python-gitlab will raise an exception
with the GitLab server error message:

.. code-block:: python

   >>> gl.projects.list(sort='invalid value')
   ...
   GitlabListError: 400: sort does not have a valid value

.. _conflicting_parameters:

Conflicting Parameters
======================

You can use the ``query_parameters`` argument to send arguments that would
conflict with python or python-gitlab when using them as kwargs:

.. code-block:: python

   gl.user_activities.list(from='2019-01-01', iterator=True)  ## invalid

   gl.user_activities.list(query_parameters={'from': '2019-01-01'}, iterator=True)  # OK

.. _objects:

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

You can print a Gitlab Object. For example:

.. code-block:: python

   project = gl.projects.get(1)
   print(project)

   # Or in a prettier format.
   project.pprint()

   # Or explicitly via ``pformat()``. This is equivalent to the above.
   print(project.pformat())

You can also extend the object if the parameter isn't explicitly listed. For example,
if you want to update a field that has been newly introduced to the Gitlab API, setting
the value on the object is accepted:

.. code-block:: python

   issues = project.issues.list(state='opened')
   for issue in issues:
      issue.my_super_awesome_feature_flag = "random_value"
      issue.save()

As a dictionary
---------------

You can get a dictionary representation copy of the Gitlab Object. Modifications made to
the dictionary will have no impact on the GitLab Object.

* ``asdict()`` method. Returns a dictionary representation of the Gitlab object.
* ``attributes`` property. Returns a dictionary representation of the Gitlab
   object. Also returns any relevant parent object attributes.

.. code-block:: python

   project = gl.projects.get(1)
   project_dict = project.asdict()

   # Or a dictionary representation also containing some of the parent attributes
   issue = project.issues.get(1)
   attribute_dict = issue.attributes

   # The following will return the same value
   title = issue.title
   title = issue.attributes["title"]

.. hint::

   This can be used to access attributes that clash with python-gitlab's own methods or managers.
   Note that:

   ``attributes`` returns the parent object attributes that are defined in
   ``object._from_parent_attrs``. For example, a ``ProjectIssue`` object will have a
   ``project_id`` key in the dictionary returned from ``attributes`` but ``asdict()`` will not.

As JSON
-------

You can get a JSON string represenation of the Gitlab Object. For example:

.. code-block:: python

   project = gl.projects.get(1)
   print(project.to_json())
   # Use arguments supported by ``json.dump()``
   print(project.to_json(sort_keys=True, indent=4))

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

``head()`` methods
========================

All endpoints that support ``get()`` and ``list()`` also support a ``head()`` method.
In this case, the server responds only with headers and not the response JSON or body.
This allows more efficient API calls, such as checking repository file size without
fetching its content.

.. note::

   In some cases, GitLab may omit specific headers. See more in the :ref:`pagination` section.

.. code-block:: python

   # See total number of personal access tokens for current user
   gl.personal_access_tokens.head()
   print(headers["X-Total"])

   # See returned content-type for project GET endpoint
   headers = gl.projects.head("gitlab-org/gitlab")
   print(headers["Content-Type"])

.. _pagination:

Pagination
==========

You can use pagination to iterate over long lists. All the Gitlab objects
listing methods support the ``page`` and ``per_page`` parameters:

.. code-block:: python

   ten_first_groups = gl.groups.list(page=1, per_page=10)

.. warning::

   The first page is page 1, not page 0.

By default GitLab does not return the complete list of items. Use the ``get_all``
parameter to get all the items when using listing methods:

.. code-block:: python

   all_groups = gl.groups.list(get_all=True)

   all_owned_projects = gl.projects.list(owned=True, get_all=True)

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

``list()`` methods can also return a generator object, by passing the argument
``iterator=True``, which will handle the next calls to the API when required. This
is the recommended way to iterate through a large number of items:

.. code-block:: python

   items = gl.groups.list(iterator=True)
   for item in items:
       print(item.attributes)

The generator exposes extra listing information as received from the server:

* ``current_page``: current page number (first page is 1)
* ``prev_page``: if ``None`` the current page is the first one
* ``next_page``: if ``None`` the current page is the last one
* ``per_page``: number of items per page
* ``total_pages``: total number of pages available. This may be a ``None`` value.
* ``total``: total number of items in the list. This may be a ``None`` value.

.. note::

   For performance reasons, if a query returns more than 10,000 records, GitLab
   does not return the ``total_pages`` or ``total`` headers.  In this case,
   ``total_pages`` and ``total`` will have a value of ``None``.

   For more information see:
   https://docs.gitlab.com/ee/user/gitlab_com/index.html#pagination-response-headers

.. note::
   Prior to python-gitlab 3.6.0 the argument ``as_list`` was used instead of
   ``iterator``.  ``as_list=False`` is the equivalent of ``iterator=True``.

.. note::
   If ``page`` and ``iterator=True`` are used together, the latter is ignored.

Sudo
====

If you have the administrator status, you can use ``sudo`` to act as another
user. For example:

.. code-block:: python

   p = gl.projects.create({'name': 'awesome_project'}, sudo='user1')

.. warning::
   When using ``sudo``, its usage is not remembered. If you use ``sudo`` to
   retrieve an object and then later use ``save()`` to modify the object, it
   will not use ``sudo``.  You should use ``save(sudo='user1')`` if you want to
   perform subsequent actions as the  user.

Updating with ``sudo``
----------------------

An example of how to ``get`` an object (using ``sudo``), modify the object, and
then ``save`` the object (using ``sudo``):

.. code-block:: python

   group = gl.groups.get('example-group')
   notification_setting = group.notificationsettings.get(sudo='user1')
   notification_setting.level = gitlab.const.NOTIFICATION_LEVEL_GLOBAL
   # Must use 'sudo' again when doing the save.
   notification_setting.save(sudo='user1')


Logging
=======

To enable debug logging from the underlying ``requests`` and ``http.client`` calls,
you can use ``enable_debug()`` on your ``Gitlab`` instance. For example:

.. code-block:: python

   import os
   import gitlab

   gl = gitlab.Gitlab(private_token=os.getenv("GITLAB_TOKEN"))
   gl.enable_debug()

By default, python-gitlab will mask the token used for authentication in logging output.
If you'd like to debug credentials sent to the API, you can disable masking explicitly:

.. code-block:: python

   gl.enable_debug(mask_credentials=False)

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
