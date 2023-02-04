################
Lower-level APIs
################

``python-gitlab``'s API levels provide different degrees of convenience, control and stability.

Main interface - ``Gitlab``, managers and objects
=================================================

As shown in previous sections and examples, the high-level API interface wraps GitLab's API
endpoints and makes them available from the ``Gitlab`` instance via managers that create
objects you can manipulate.

This is what most users will want to use, as it covers most of GitLab's API endpoints, and
allows you to write idiomatic Python code when interacting with the API.

Lower-level API - HTTP methods
==============================

.. danger::

   At this point, python-gitlab will no longer take care of URL-encoding and other transformations
   needed to correctly pass API parameter types. You have to construct these correctly yourself.

   However, you still benefit from many of the client's :ref:`features` such as authentication,
   requests and retry handling.

.. important::

   If you've found yourself at this section because of an endpoint not yet implemented in
   the library - please consider opening a pull request implementing the resource or at
   least filing an issue so we can track progress.

   High-quality pull requests for standard endpoints that pass CI and include unit tests and
   documentation are easy to review, and can land quickly with monthly releases. If you ask,
   we can also trigger a new release, so you and everyone benefits from the contribution right away!

Managers and objects call specific HTTP methods to fetch or send data to the server. These methods
can be invoked directly to access endpoints not currently implemented by the client. This essentially
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
* ``http_patch()``
* ``http_delete()``
* ``http_list()`` (a wrapper around ``http_get`` handling pagination, including with lazy generators)
* ``http_head()`` (only returns the header dictionary)

Lower-lower-level API - HTTP requests
=====================================

.. important::

    This is mostly intended for internal use in python-gitlab and may have a less stable interface than
    higher-level APIs. To lessen the chances of a change to the interface impacting your code, we
    recommend using keyword arguments when calling the interfaces.

At the lowest level, HTTP methods call ``http_request()``, which performs the actual request and takes
care of details such as timeouts, retries, and handling rate-limits.

This method can be invoked directly to or customize this behavior for a single request, or to call custom
HTTP methods not currently implemented in the library - while still making use of all of the client's
options and authentication methods.

For example, if for whatever reason you want to fetch allowed methods for an endpoint at runtime:

.. code-block:: python

    >>> gl = gitlab.Gitlab(private_token=private_token)
    >>>
    >>> response = gl.http_request(verb="OPTIONS", path="/projects")
    >>> response.headers["Allow"]
    'OPTIONS, GET, POST, HEAD'

Or get the total number of a user's events with a customized HEAD request:

.. code-block:: python

    >>> response = gl.http_request(
            verb="HEAD",
            path="/events",
            query_params={"sudo": "some-user"},
            timeout=10
        )
    >>> response.headers["X-Total"]
    '123'
