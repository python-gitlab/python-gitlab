#####################
Registry Repositories
#####################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRegistryRepository`
  + :class:`gitlab.v4.objects.ProjectRegistryRepositoryManager`
  + :attr:`gitlab.v4.objects.Project.registries`

* Gitlab API: https://docs.gitlab.com/ce/api/container_registry.html

Examples
--------

Get the list of container registry repositories associated with the project::

      registries = project.registries.list()

Delete repository::

      project.registries.delete(id=x)
      # or 
      registry = registries.pop()
      registry.delete()
