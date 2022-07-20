#####################
Registry Repositories
#####################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRegistryRepository`
  + :class:`gitlab.v4.objects.ProjectRegistryRepositoryManager`
  + :attr:`gitlab.v4.objects.Project.repositories`

* Gitlab API: https://docs.gitlab.com/ce/api/container_registry.html

Examples
--------

Get the list of container registry repositories associated with the project::

      repositories = project.repositories.list()

Get the list of all project container registry repositories in a group::

      repositories = group.registry_repositories.list()

Delete repository::

      project.repositories.delete(id=x)
      # or 
      repository = repositories.pop()
      repository.delete()
