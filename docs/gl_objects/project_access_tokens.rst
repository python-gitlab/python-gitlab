#####################
Project Access Tokens
#####################

Get a list of project access tokens

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectAccessToken`
  + :class:`gitlab.v4.objects.ProjectAccessTokenManager`
  + :attr:`gitlab.Gitlab.project_access_tokens`

* GitLab API: https://docs.gitlab.com/ee/api/project_access_tokens.html

Examples
--------

List project access tokens::

    access_tokens = gl.projects.get(1, lazy=True).access_tokens.list()
    print(access_tokens[0].name)

Get a project access token by id::

    token = project.access_tokens.get(123)
    print(token.name)

Create project access token::

    access_token = gl.projects.get(1).access_tokens.create({"name": "test", "scopes": ["api"], "expires_at": "2023-06-06"})

Revoke a project access tokens::

    gl.projects.get(1).access_tokens.delete(42)
    # or
    access_token.delete()
