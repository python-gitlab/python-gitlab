######################
Protected environments
######################

You can list and manage protected environments in a project.

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectProtectedEnvironment`
  + :class:`gitlab.v4.objects.ProjectProtectedEnvironmentManager`
  + :attr:`gitlab.v4.objects.Project.protected_environment`

* GitLab API: https://docs.gitlab.com/ee/api/protected_environments.html

Examples
--------

Get the list of protected environments for a project::

    p_environments = project.protected_environments.list()

Get a single protected environment::

    p_environments = project.protected_environments.get('production')

Protect an existing environment::

    p_environment = project.protected_environments.create(
        {
            'name': 'production',
            'deploy_access_levels': [
                {'access_level': 40}
            ],
        }
    )


Unprotect a protected environment::

    p_environment = project.protected_environments.delete('production')
    # or
    p_environment.delete()
