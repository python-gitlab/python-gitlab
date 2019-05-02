########################
Registry Repository Tags
########################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRegistryTag`
  + :class:`gitlab.v4.objects.ProjectRegistryTagManager`
  + :attr:`gitlab.v4.objects.Repository.tags`

* Gitlab API: https://docs.gitlab.com/ce/api/container_registry.html

Examples
--------

Get the list of repository tags in given registry::

      registries = project.registries.list()
      registry = registries.pop()
      tags = registry.tags.list()

Get specific tag::
      
      registry.tags.get(id=tag_name)

Delete tag::

      registry.tags.delete(id=tag_name)
      # or
      tag = registry.tags.get(id=tag_name)
      tag.delete()

Delete tag in bulk::

      registry.tags.delete_in_bulk(keep_n=1)
      # or 
      registry.tags.delete_in_bulk(older_than="1m")
      # or 
      registry.tags.delete_in_bulk(name_regex="v.+", keep_n=2)

.. note::   

      Delete in bulk is asnychronous operation and may take a while. 
      Refer to: https://docs.gitlab.com/ce/api/container_registry.html#delete-repository-tags-in-bulk 
