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
