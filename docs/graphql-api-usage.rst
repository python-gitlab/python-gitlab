#####################
Using the GraphQL API
#####################

python-gitlab provides basic support for executing GraphQL queries and mutations.

.. danger::

   The GraphQL client is experimental and only provides basic support.
   It does not currently support pagination, obey rate limits,
   or attempt complex retries. You can use it to build simple queries

   It is currently unstable and its implementation may change. You can expect a more
   mature client in one of the upcoming major versions.

The ``gitlab.GraphQLGitlab`` class
==================================

As with the REST client, you connect to a GitLab instance by creating a ``gitlab.GraphQLGitlab`` object:

.. code-block:: python

   import gitlab

   # anonymous read-only access for public resources (GitLab.com)
   gl = gitlab.GraphQLGitlab()

   # anonymous read-only access for public resources (self-hosted GitLab instance)
   gl = gitlab.GraphQLGitlab('https://gitlab.example.com')

   # private token or personal token authentication (GitLab.com)
   gl = gitlab.GraphQLGitlab(private_token='JVNSESs8EwWRx5yDxM5q')

   # private token or personal token authentication (self-hosted GitLab instance)
   gl = gitlab.GraphQLGitlab(url='https://gitlab.example.com', private_token='JVNSESs8EwWRx5yDxM5q')

   # oauth token authentication
   gl = gitlab.GraphQLGitlab('https://gitlab.example.com', oauth_token='my_long_token_here')

Sending queries
===============

Get the result of a simple query:

.. code-block:: python

    query = """{
        query {
          currentUser {
            name
          }
        }
    """

    result = gl.execute(query)
