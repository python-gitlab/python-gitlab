import time

import pytest

import gitlab


@pytest.fixture
def bulk_import_enabled(gl: gitlab.Gitlab):
    settings = gl.settings.get()
    bulk_import_default = settings.bulk_import_enabled

    settings.bulk_import_enabled = True
    settings.save()

    # todo: why so fussy with feature flag timing?
    time.sleep(5)
    get_settings = gl.settings.get()
    assert get_settings.bulk_import_enabled is True

    yield settings

    settings.bulk_import_enabled = bulk_import_default
    settings.save()


# https://github.com/python-gitlab/python-gitlab/pull/2790#pullrequestreview-1873617123
@pytest.mark.xfail(reason="Bulk Imports to be worked on in a follow up")
def test_bulk_imports(gl, group, bulk_import_enabled):
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
