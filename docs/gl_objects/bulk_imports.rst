#########################
Migrations (Bulk Imports)
#########################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.BulkImport`
  + :class:`gitlab.v4.objects.BulkImportManager`
  + :attr:`gitlab.Gitlab.bulk_imports`
  + :class:`gitlab.v4.objects.BulkImportAllEntity`
  + :class:`gitlab.v4.objects.BulkImportAllEntityManager`
  + :attr:`gitlab.Gitlab.bulk_import_entities`
  + :class:`gitlab.v4.objects.BulkImportEntity`
  + :class:`gitlab.v4.objects.BulkImportEntityManager`
  + :attr:`gitlab.v4.objects.BulkImport.entities`

* GitLab API: https://docs.gitlab.com/ee/api/bulk_imports.html

Examples
--------

.. note::

    Like the project/group imports and exports, this is an asynchronous operation and you
    will need to refresh the state from the server to get an accurate migration status. See
    :ref:`project_import_export` in the import/export section for more details and examples.

Start a bulk import/migration of a group and wait for completion::

    # Create the migration
    configuration = {
        "url": "https://gitlab.example.com",
        "access_token": private_token,
    }
    entity = {
        "source_full_path": "source_group",
        "source_type": "group_entity",
        "destination_slug": "imported-group",
        "destination_namespace": "imported-namespace",
    }
    migration = gl.bulk_imports.create(
        {
            "configuration": configuration,
            "entities": [entity],
        }
    )

    # Wait for the 'finished' status
    while migration.status != "finished":
        time.sleep(1)
        migration.refresh()

List all migrations::

    gl.bulk_imports.list()

List the entities of all migrations::

    gl.bulk_import_entities.list()

Get a single migration by ID::

    migration = gl.bulk_imports.get(123)

List the entities of a single migration::

    entities = migration.entities.list()

Get a single entity of a migration by ID::

    entity = migration.entities.get(123)

Refresh the state of a migration or entity from the server::

    migration.refresh()
    entity.refresh()

    print(migration.status)
    print(entity.status)
