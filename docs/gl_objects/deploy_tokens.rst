#############
Deploy tokens
#############

Deploy tokens allow read-only access to your repository and registry images
without having a user and a password.

Deploy tokens
=============

This endpoint requires admin access.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.DeployToken`
  + :class:`gitlab.v4.objects.DeployTokenManager`
  + :attr:`gitlab.Gitlab.deploytokens`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_tokens.html

Examples
--------

Use the ``list()`` method to list all deploy tokens across the GitLab instance.

::

    # List deploy tokens
    deploy_tokens = gl.deploytokens.list()

Project deploy tokens
=====================

This endpoint requires project maintainer access or higher.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeployToken`
  + :class:`gitlab.v4.objects.ProjectDeployTokenManager`
  + :attr:`gitlab.v4.objects.Project.deploytokens`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_tokens.html#project-deploy-tokens

Examples
--------

List the deploy tokens for a project::

    deploy_tokens = project.deploytokens.list()

Get a deploy token for a project by id::

    deploy_token = project.deploytokens.get(deploy_token_id)

Create a new deploy token to access registry images of a project:

In addition to required parameters ``name`` and ``scopes``, this method accepts
the following parameters:

* ``expires_at`` Expiration date of the deploy token. Does not expire if no value is provided.
* ``username`` Username for deploy token. Default is ``gitlab+deploy-token-{n}``


::

    deploy_token = project.deploytokens.create({'name': 'token1', 'scopes': ['read_registry'], 'username':'', 'expires_at':''})
    # show its id
    print(deploy_token.id)
    # show the token value. Make sure you save it, you won't be able to access it again.
    print(deploy_token.token)

.. warning::

   With GitLab 12.9, even though ``username`` and ``expires_at`` are not required, they always have to be passed to the API.
   You can set them to empty strings, see: https://gitlab.com/gitlab-org/gitlab/-/issues/211878.
   Also, the ``username``'s value is ignored by the API and will be overridden with ``gitlab+deploy-token-{n}``,
   see: https://gitlab.com/gitlab-org/gitlab/-/issues/211963
   These issues were fixed in GitLab 12.10.

Remove a deploy token from the project::

    deploy_token.delete()
    # or
    project.deploytokens.delete(deploy_token.id)


Group deploy tokens
===================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupDeployToken`
  + :class:`gitlab.v4.objects.GroupDeployTokenManager`
  + :attr:`gitlab.v4.objects.Group.deploytokens`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_tokens.html#group-deploy-tokens

Examples
--------

List the deploy tokens for a group::

    deploy_tokens = group.deploytokens.list()

Get a deploy token for a group by id::

    deploy_token = group.deploytokens.get(deploy_token_id)

Create a new deploy token to access all repositories of all projects in a group:

In addition to required parameters ``name`` and ``scopes``, this method accepts
the following parameters:

* ``expires_at`` Expiration date of the deploy token. Does not expire if no value is provided.
* ``username`` Username for deploy token. Default is ``gitlab+deploy-token-{n}``

::

    deploy_token = group.deploytokens.create({'name': 'token1', 'scopes': ['read_repository'], 'username':'', 'expires_at':''})
    # show its id
    print(deploy_token.id)

.. warning::

   With GitLab 12.9, even though ``username`` and ``expires_at`` are not required, they always have to be passed to the API.
   You can set them to empty strings, see: https://gitlab.com/gitlab-org/gitlab/-/issues/211878.
   Also, the ``username``'s value is ignored by the API and will be overridden with ``gitlab+deploy-token-{n}``,
   see: https://gitlab.com/gitlab-org/gitlab/-/issues/211963
   These issues were fixed in GitLab 12.10.

Remove a deploy token from the group::

    deploy_token.delete()
    # or
    group.deploytokens.delete(deploy_token.id)

