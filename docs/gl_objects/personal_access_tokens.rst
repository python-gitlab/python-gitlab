######################
Personal Access Tokens
######################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.PersonalAccessToken`
  + :class:`gitlab.v4.objects.PersonalAcessTokenManager`
  + :attr:`gitlab.Gitlab.personal_access_tokens`
  + :class:`gitlab.v4.objects.UserPersonalAccessToken`
  + :class:`gitlab.v4.objects.UserPersonalAcessTokenManager`
  + :attr:`gitlab.Gitlab.User.personal_access_tokens`

* GitLab API:

  + https://docs.gitlab.com/ee/api/personal_access_tokens.html
  + https://docs.gitlab.com/ee/api/users.html#create-a-personal-access-token

Examples
--------

List personal access tokens::

    access_tokens = gl.personal_access_tokens.list()
    print(access_tokens[0].name)

List personal access tokens from other user_id (admin only)::

    access_tokens = gl.personal_access_tokens.list(user_id=25)

Get a personal access token by id::

    gl.personal_access_tokens.get(123)

Get the personal access token currently used::

    gl.personal_access_tokens.get("self")

Revoke a personal access token fetched via list::

    access_token = access_tokens[0]
    access_token.delete()

Revoke a personal access token by id::

    gl.personal_access_tokens.delete(123)

Revoke the personal access token currently used::

    gl.personal_access_tokens.delete("self")

Rotate a personal access token and retrieve its new value::

    token = gl.personal_access_tokens.get(42, lazy=True)
    token.rotate()
    print(token.token)
    # or directly using a token ID
    new_token_dict = gl.personal_access_tokens.rotate(42)
    print(new_token_dict)

Create a personal access token for a user (admin only)::

    user = gl.users.get(25, lazy=True)
    access_token = user.personal_access_tokens.create({"name": "test", "scopes": "api"})

.. note:: As you can see above, you can only create personal access tokens
    via the Users API, but you cannot revoke these objects directly.
    This is because the create API uses a different endpoint than the list and revoke APIs.
    You need to fetch the token via the list or get API first to revoke it.
