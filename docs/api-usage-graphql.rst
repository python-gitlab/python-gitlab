############################
Using the GraphQL API (beta)
############################

python-gitlab provides basic support for executing GraphQL queries and mutations.

.. danger::

   The GraphQL client is experimental and only provides basic support.
   It does not currently support pagination, obey rate limits,
   or attempt complex retries. You can use it to build simple queries and mutations.

   It is currently unstable and its implementation may change. You can expect a more
   mature client in one of the upcoming versions.

The ``gitlab.GraphQL`` class
==================================

As with the REST client, you connect to a GitLab instance by creating a ``gitlab.GraphQL`` object:

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
