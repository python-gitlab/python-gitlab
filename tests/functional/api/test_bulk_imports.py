def test_bulk_imports(gl, group):
    destination = f"{group.full_path}-import"
    configuration = {
        "url": gl.url,
        "access_token": gl.private_token,
    }
    migration_entity = {
        "source_full_path": group.full_path,
        "source_type": "group_entity",
        "destination_slug": destination,
        "destination_namespace": destination,
    }
    created_migration = gl.bulk_imports.create(
        {
            "configuration": configuration,
            "entities": [migration_entity],
        }
    )

    assert created_migration.source_type == "gitlab"
    assert created_migration.status == "created"

    migration = gl.bulk_imports.get(created_migration.id)
    assert migration == created_migration

    migration.refresh()
    assert migration == created_migration

    migrations = gl.bulk_imports.list()
    assert migration in migrations

    all_entities = gl.bulk_import_entities.list()
    entities = migration.entities.list()
    assert isinstance(entities, list)
    assert entities[0] in all_entities

    entity = migration.entities.get(entities[0].id)
    assert entity == entities[0]

    entity.refresh()
    assert entity.created_at == entities[0].created_at
