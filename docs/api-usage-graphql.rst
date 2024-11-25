############################
Using the GraphQL API (beta)
############################

python-gitlab provides basic support for executing GraphQL queries and mutations,
providing both a synchronous and asynchronous client.

.. danger::

   The GraphQL client is experimental and only provides basic support.
   It does not currently support pagination, obey rate limits,
   or attempt complex retries. You can use it to build simple queries and mutations.

   It is currently unstable and its implementation may change. You can expect a more
   mature client in one of the upcoming versions.

The ``gitlab.GraphQL`` and ``gitlab.AsyncGraphQL`` classes
==========================================================

As with the REST client, you connect to a GitLab instance by creating a ``gitlab.GraphQL``
(for synchronous code) or ``gitlab.AsyncGraphQL`` instance (for asynchronous code):

.. code-block:: python

   import gitlab

   # anonymous read-only access for public resources (GitLab.com)
   gq = gitlab.GraphQL()

   # anonymous read-only access for public resources (self-hosted GitLab instance)
   gq = gitlab.GraphQL('https://gitlab.example.com')

   # personal access token or OAuth2 token authentication (GitLab.com)
   gq = gitlab.GraphQL(token='glpat-JVNSESs8EwWRx5yDxM5q')

   # personal access token or OAuth2 token authentication (self-hosted GitLab instance)
   gq = gitlab.GraphQL('https://gitlab.example.com', token='glpat-JVNSESs8EwWRx5yDxM5q')

   # or the async equivalents
   async_gq = gitlab.AsyncGraphQL()
   async_gq = gitlab.AsyncGraphQL('https://gitlab.example.com')
   async_gq = gitlab.AsyncGraphQL(token='glpat-JVNSESs8EwWRx5yDxM5q')
   async_gq = gitlab.AsyncGraphQL('https://gitlab.example.com', token='glpat-JVNSESs8EwWRx5yDxM5q')
  
Sending queries
===============

Get the result of a query:

.. code-block:: python

    query = """{
        query {
          currentUser {
            name
          }
        }
    """

    result = gq.execute(query)

Get the result of a query using the async client:

.. code-block:: python

    query = """{
        query {
          currentUser {
            name
          }
        }
    """

    result = await async_gq.execute(query)
