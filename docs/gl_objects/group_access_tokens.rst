#####################
Group Access Tokens
#####################

Get a list of group access tokens

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.GroupAccessToken`
  + :class:`gitlab.v4.objects.GroupAccessTokenManager`
  + :attr:`gitlab.Gitlab.group_access_tokens`

* GitLab API: https://docs.gitlab.com/ee/api/group_access_tokens.html

Examples
--------

List group access tokens::

    access_tokens = gl.groups.get(1, lazy=True).access_tokens.list()
    print(access_tokens[0].name)

Create group access token::

    access_token = gl.groups.get(1).access_tokens.create({"name": "test", "scopes": ["api"], "expires_at": "2023-06-06"})

Revoke a group access tokens::

    gl.groups.get(1).access_tokens.delete(42)
    # or
    access_token.delete()
