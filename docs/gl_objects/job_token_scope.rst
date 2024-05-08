#####################
CI/CD job token scope
#####################

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectJobTokenScope`
  + :class:`gitlab.v4.objects.ProjectJobTokenScopeManager`
  + :attr:`gitlab.v4.objects.Project.job_token_scope`

* GitLab API: https://docs.gitlab.com/ee/api/project_job_token_scopes.html

Examples
--------

.. warning::

   The GitLab API does **not** return any data when saving or updating
   the job token scope settings. You need to call ``refresh()`` (or ``get()``
   a new object) as shown below to get the latest state.

Get a project's CI/CD job token access settings::

    scope = project.job_token_scope.get()
    print(scope.inbound_enabled)
    # True

Update the job token scope settings::

    scope.enabled = False
    scope.save()

.. warning::

   As you can see above, the attributes you receive from and send to the GitLab API
   are not consistent. GitLab returns ``inbound_enabled`` and ``outbound_enabled``,
   but expects ``enabled``, which only refers to the inbound scope. This is important
   when accessing and updating these attributes.

Or update the job token scope settings directly::

    project.job_token_scope.update(new_data={"enabled": True})

Refresh the current state of job token scope::

    scope.refresh()
    print(scope.inbound_enabled)
    # False

Get a project's CI/CD job token inbound allowlist::

    allowlist = scope.allowlist.list()

Add a project to the project's inbound allowlist::

    allowed_project = scope.allowlist.create({"target_project_id": 42})

Remove a project from the project's inbound allowlist::

    allowed_project.delete()
    # or directly using a project ID
    scope.allowlist.delete(42)

.. warning::

   Similar to above, the ID attributes you receive from the create and list
   APIs are not consistent (in create() the id is returned as ``source_project_id`` whereas list() returns as ``id``). To safely retrieve the ID of the allowlisted project
   regardless of how the object was created, always use its ``.get_id()`` method.

Using ``.get_id()``::

    resp = allowlist.create({"target_project_id": 2})
    allowlist_id = resp.get_id()

    allowlists = project.allowlist.list()
    for allowlist in allowlists:
      allowlist_id == allowlist.get_id()

Get a project's CI/CD job token inbound groups allowlist::

    allowlist = scope.groups_allowlist.list()

Add a project to the project's inbound groups allowlist::

    allowed_project = scope.groups_allowlist.create({"target_project_id": 42})

Remove a project from the project's inbound agroups llowlist::

    allowed_project.delete()
    # or directly using a Group ID
    scope.groups_allowlist.delete(42)

.. warning::

   Similar to above, the ID attributes you receive from the create and list
   APIs are not consistent. To safely retrieve the ID of the allowlisted group
   regardless of how the object was created, always use its ``.get_id()`` method.

