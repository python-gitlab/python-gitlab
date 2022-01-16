##########
API levels
##########

python-gitlab works in three API layers, with different levels of convenience and control.

High-level API - ``Gitlab`` managers and objects
================================================

As shown in previous sections and examples, the high-level API interface wraps GitLab's API
endpoints and makes them available from the ``Gitlab`` instance via managers that create
objects you can manipulate.

This is what most users will want to use, as it covers most of GitLab's API endpoints, and
allows you to write idiomatic Python code when interacting with the API.

Mid-level API - HTTP methods
============================

.. danger::

   At this point and lower, python-gitlab will no longer take care of URL-encoding and other
   transformations needed to correctly pass API parameter types. You have to construct these yourself.

.. important::

   If you've found yourself at this section because of an endpoint not yet implemented in
   the library - please consider opening a pull request implementing the resource or at
   least filing an issue so we can track progress.

   High-quality pull requests for standard endpoints that pass CI and include unit tests and
   documentation are easy to review, and can land quickly with monthly releases. If you ask,
   we can also trigger a new release, so you and everyone benefits from the contribution right away!

Managers and objects call specific HTTP methods to fetch or send data to the server. These methods
can be invoked directly to access endpoints not currently implemented by python-gitlab. This essentially
gives you some level of usability for any endpoint the moment it is available on your GitLab instance.

These methods can be accessed directly via the ``Gitlab`` instance (e.g. ``gl.http_get()``), or via an
object's manager (e.g. ``project.manager.gitlab.http_get()``), if the ``Gitlab`` instance is not available
in the current context.

For example, if you'd like to access GitLab's `undocumented latest pipeline endpoint
<https://gitlab.com/gitlab-org/gitlab/-/blob/5e2a61166d2a033d3fd1eb4c09d896ed19a57e60/lib/api/ci/pipelines.rb#L97>`__,
you can do so by calling ``http_get()`` with the path to the endpoint:

.. code-block:: python

    >>> gl = gitlab.Gitlab(private_token=private_token)
    >>>
    >>> pipeline = gl.http_get("/projects/gitlab-org%2Fgitlab/pipelines/latest")
    >>> pipeline["id"]
    449070256

The available methods are:

* ``http_get()``
* ``http_post()``
* ``http_put()``
* ``http_delete()``
* ``http_list()`` (a wrapper around ``http_get`` handling pagination, including with lazy generators)

Low-level API - HTTP requests
=============================

At the lowest level, these HTTP methods call ``http_request()``, which performs the actual request.

Although mostly designed for internal use in python-gitlab, this method can be invoked directly to
call custom HTTP methods not currently implemented in the library - while still making use of all
of the client's options and authentication methods.

If, for whatever reason, you want to fetch allowed methods for an endpoint at runtime:

.. code-block:: python

    >>> gl = gitlab.Gitlab(private_token=private_token)
    >>>
    >>> response = gl.http_request("OPTIONS", "/projects")
    >>> response.headers["Allow"]
    'OPTIONS, GET, POST, HEAD'

Check a file's size or if it exists in a project without fetching its entire content:

.. code-block:: python

    >>> gl = gitlab.Gitlab(private_token=private_token)
    >>> file_path = "/projects/gitlab-org%2Fgitlab/repository/files/Dangerfile"
    >>>
    >>> response = gl.http_request("HEAD", file_path, ref="master")
    >>> response.headers["x-gitlab-size"]
    '1548'
