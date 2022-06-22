############
Environments
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectEnvironment`
  + :class:`gitlab.v4.objects.ProjectEnvironmentManager`
  + :attr:`gitlab.v4.objects.Project.environments`

* GitLab API: https://docs.gitlab.com/ce/api/environments.html

Examples
--------

List environments for a project::

    environments = project.environments.list()

Create an environment for a project::

    environment = project.environments.create({'name': 'production'})

Retrieve a specific environment for a project::

    environment = project.environments.get(112)

Update an environment for a project::

    environment.external_url = 'http://foo.bar.com'
    environment.save()

Delete an environment for a project::

    environment = project.environments.delete(environment_id)
    # or
    environment.delete()

Stop an environment::

    environment.stop()

To manage protected environments, see :doc:`/gl_objects/protected_environments`.
