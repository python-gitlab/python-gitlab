##############
Advanced usage
##############

Using a custom session
----------------------

python-gitlab relies on ``requests.Session`` objects to perform all the
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

   import os
   import gitlab
   import requests

   session = requests.Session()
   session.proxies = {
       'https': os.environ.get('https_proxy'),
       'http': os.environ.get('http_proxy'),
   }
   gl = gitlab.gitlab(url, token, api_version=4, session=session)

Reference:
https://requests.readthedocs.io/en/latest/user/advanced/#proxies

SSL certificate verification
----------------------------

python-gitlab relies on the CA certificate bundle in the `certifi` package
that comes with the requests library.

If you need python-gitlab to use your system CA store instead, you can provide
the path to the CA bundle in the `REQUESTS_CA_BUNDLE` environment variable.

Reference:
https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification

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
https://requests.readthedocs.io/en/latest/user/advanced/#client-side-certificates

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
   gl.projects.list(get_all=True, obey_rate_limit=False)

If you do not disable the rate-limiting feature, you can supply a custom value
for ``max_retries``; by default, this is set to 10. To retry without bound when
throttled, you can set this parameter to -1. This parameter is ignored if
``obey_rate_limit`` is set to ``False``.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(get_all=True, max_retries=12)

.. warning::

   You will get an Exception, if you then go over the rate limit of your GitLab instance.

Transient errors
----------------

GitLab server can sometimes return a transient HTTP error.
python-gitlab can automatically retry in such case, when
``retry_transient_errors`` argument is set to ``True``.  When enabled,
HTTP error codes 500 (Internal Server Error), 502 (502 Bad Gateway),
503 (Service Unavailable), and 504 (Gateway Timeout) are retried. It will retry until reaching
the `max_retries` value. By default, `retry_transient_errors` is set to `False` and an exception
is raised for these errors.

.. code-block:: python

   import gitlab
   import requests

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.list(get_all=True, retry_transient_errors=True)

The default ``retry_transient_errors`` can also be set on the ``Gitlab`` object
and overridden by individual API calls.

.. code-block:: python

   import gitlab
   import requests
   gl = gitlab.gitlab(url, token, api_version=4, retry_transient_errors=True)
   gl.projects.list(get_all=True)                               # retries due to default value
   gl.projects.list(get_all=True, retry_transient_errors=False) # does not retry

Timeout
-------

python-gitlab will by default use the ``timeout`` option from its configuration
for all requests. This is passed downwards to the ``requests`` module at the
time of making the HTTP request. However if you would like to override the
global timeout parameter for a particular call, you can provide the ``timeout``
parameter to that API invocation:

.. code-block:: python

   import gitlab

   gl = gitlab.gitlab(url, token, api_version=4)
   gl.projects.import_github(ACCESS_TOKEN, 123456, "root", timeout=120.0)
