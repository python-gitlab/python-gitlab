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

* GitLab API: https://docs.gitlab.com/api/group_access_tokens

Examples
--------

List group access tokens::

    access_tokens = gl.groups.get(1, lazy=True).access_tokens.list(get_all=True)
    print(access_tokens[0].name)

Get a group access token by id::

    token = group.access_tokens.get(123)
    print(token.name)

Create group access token::

    access_token = gl.groups.get(1).access_tokens.create({"name": "test", "scopes": ["api"], "expires_at": "2023-06-06"})

Revoke a group access token::

    gl.groups.get(1).access_tokens.delete(42)
    # or
    access_token.delete()

Rotate a group access token and retrieve its new value::

    token = group.access_tokens.get(42, lazy=True)
    token.rotate()
    print(token.token)
    # or directly using a token ID
    new_token = group.access_tokens.rotate(42)
    print(new_token.token)

Self-Rotate the group access token you are using to authenticate the request and retrieve its new value::

    token = group.access_tokens.get(42, lazy=True)
    token.rotate(self_rotate=True)
    print(token.token)