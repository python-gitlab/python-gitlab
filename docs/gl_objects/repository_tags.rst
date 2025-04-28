########################
Registry Repository Tags
########################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRegistryTag`
  + :class:`gitlab.v4.objects.ProjectRegistryTagManager`
  + :attr:`gitlab.v4.objects.Repository.tags`

* Gitlab API: https://docs.gitlab.com/api/container_registry

Examples
--------

Get the list of repository tags in given registry::

      repositories = project.repositories.list(get_all=True)
      repository = repositories.pop()
      tags = repository.tags.list(get_all=True)

Get specific tag::
      
      repository.tags.get(id=tag_name)

Delete tag::

      repository.tags.delete(id=tag_name)
      # or
      tag = repository.tags.get(id=tag_name)
      tag.delete()

Delete tag in bulk::

      repository.tags.delete_in_bulk(keep_n=1)
      # or 
      repository.tags.delete_in_bulk(older_than="1m")
      # or 
      repository.tags.delete_in_bulk(name_regex="v.+", keep_n=2)

.. note::   

      Delete in bulk is asynchronous operation and may take a while. 
      Refer to: https://docs.gitlab.com/api/container_registry#delete-repository-tags-in-bulk 
