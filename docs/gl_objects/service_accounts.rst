################
Service Accounts
################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ServiceAccount`
  + :class:`gitlab.v4.objects.ServiceAccountManager`
  + :class:`gitlab.v4.objects.GroupServiceAccount`
  + :class:`gitlab.v4.objects.GroupServiceAccountManager`
  + :class:`gitlab.v4.objects.GroupServiceAccountAccessToken`
  + :class:`gitlab.v4.objects.GroupServiceAccountAccessTokenManager`
  + :class:`gitlab.v4.objects.ProjectServiceAccount`
  + :class:`gitlab.v4.objects.ProjectServiceAccountManager`
  + :class:`gitlab.v4.objects.ProjectServiceAccountAccessToken`
  + :class:`gitlab.v4.objects.ProjectServiceAccountAccessTokenManager`

* GitLab API: https://docs.gitlab.com/api/service_accounts/

Instance service accounts
-------------------------

List instance service accounts::

    accounts = gl.service_accounts.list()

Create an instance service account::

    sa = gl.service_accounts.create({})
    # with optional attributes
    sa = gl.service_accounts.create({"name": "my-bot", "username": "my-bot", "email": "my-bot@example.com"})

Update an instance service account::

    gl.service_accounts.update(sa.id, {"name": "renamed-bot"})
    # or via the object
    sa.name = "renamed-bot"
    sa.save()

Group service accounts
----------------------

List group service accounts::

    accounts = group.service_accounts.list()

Create a group service account::

    sa = group.service_accounts.create({})
    # with optional attributes
    sa = group.service_accounts.create({"name": "ci-bot", "username": "ci-bot"})

Update a group service account::

    group.service_accounts.update(sa.id, {"name": "renamed-bot"})
    # or via the object
    sa.name = "renamed-bot"
    sa.save()

Delete a group service account::

    group.service_accounts.delete(sa.id)
    # or via the object
    sa.delete()

Group service account personal access tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List tokens for a group service account::

    tokens = sa.access_tokens.list()

Create a token for a group service account::

    token = sa.access_tokens.create({
        "name": "ci-token",
        "scopes": ["api"],
        "expires_at": "2026-01-01",
    })
    print(token.token)

Rotate a token::

    token.rotate()
    print(token.token)
    # or directly using a token ID
    new_token = sa.access_tokens.rotate(token.id)
    print(new_token["token"])

Revoke a token::

    sa.access_tokens.delete(token.id)
    # or via the object
    token.delete()

Project service accounts
------------------------

List project service accounts::

    accounts = project.service_accounts.list()

Create a project service account::

    sa = project.service_accounts.create({})
    # with optional attributes
    sa = project.service_accounts.create({"name": "ci-bot", "username": "ci-bot"})

Update a project service account::

    project.service_accounts.update(sa.id, {"name": "renamed-bot"})
    # or via the object
    sa.name = "renamed-bot"
    sa.save()

Delete a project service account::

    project.service_accounts.delete(sa.id)
    # or via the object
    sa.delete()

Project service account personal access tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List tokens for a project service account::

    tokens = sa.access_tokens.list()

Create a token for a project service account::

    token = sa.access_tokens.create({
        "name": "ci-token",
        "scopes": ["read_repository"],
        "expires_at": "2026-01-01",
    })
    print(token.token)

Rotate a token::

    token.rotate()
    print(token.token)
    # or directly using a token ID
    new_token = sa.access_tokens.rotate(token.id)
    print(new_token["token"])

Revoke a token::

    sa.access_tokens.delete(token.id)
    # or via the object
    token.delete()
