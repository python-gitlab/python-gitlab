"""
GitLab API: https://docs.gitlab.com/ce/api/bulk_imports.html
"""

import pytest
import responses

from gitlab.v4.objects import BulkImport, BulkImportAllEntity, BulkImportEntity

migration_content = {
    "id": 1,
    "status": "finished",
    "source_type": "gitlab",
    "created_at": "2021-06-18T09:45:55.358Z",
    "updated_at": "2021-06-18T09:46:27.003Z",
}
entity_content = {
    "id": 1,
    "bulk_import_id": 1,
    "status": "finished",
    "source_full_path": "source_group",
    "destination_slug": "destination_slug",
    "destination_namespace": "destination_path",
    "parent_id": None,
    "namespace_id": 1,
    "project_id": None,
    "created_at": "2021-06-18T09:47:37.390Z",
    "updated_at": "2021-06-18T09:47:51.867Z",
    "failures": [],
}


@pytest.fixture
def resp_create_bulk_import():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/bulk_imports",
            json=migration_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_list_bulk_imports():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/bulk_imports",
            json=[migration_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_bulk_import():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/bulk_imports/1",
            json=migration_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_all_bulk_import_entities():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/bulk_imports/entities",
            json=[entity_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_bulk_import_entities():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/bulk_imports/1/entities",
            json=[entity_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_bulk_import_entity():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/bulk_imports/1/entities/1",
            json=entity_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_create_bulk_import(gl, resp_create_bulk_import):
    configuration = {
        "url": gl.url,
        "access_token": "test-token",
    }
    migration_entity = {
        "source_full_path": "source",
        "source_type": "group_entity",
        "destination_slug": "destination",
        "destination_namespace": "destination",
    }
    migration = gl.bulk_imports.create(
        {
            "configuration": configuration,
            "entities": [migration_entity],
        }
    )
    assert isinstance(migration, BulkImport)
    assert migration.status == "finished"


def test_list_bulk_imports(gl, resp_list_bulk_imports):
    migrations = gl.bulk_imports.list()
    assert isinstance(migrations[0], BulkImport)
    assert migrations[0].status == "finished"


def test_get_bulk_import(gl, resp_get_bulk_import):
    migration = gl.bulk_imports.get(1)
    assert isinstance(migration, BulkImport)
    assert migration.status == "finished"


def test_list_all_bulk_import_entities(gl, resp_list_all_bulk_import_entities):
    entities = gl.bulk_import_entities.list()
    assert isinstance(entities[0], BulkImportAllEntity)
    assert entities[0].bulk_import_id == 1


def test_list_bulk_import_entities(gl, migration, resp_list_bulk_import_entities):
    entities = migration.entities.list()
    assert isinstance(entities[0], BulkImportEntity)
    assert entities[0].bulk_import_id == 1


def test_get_bulk_import_entity(gl, migration, resp_get_bulk_import_entity):
    entity = migration.entities.get(1)
    assert isinstance(entity, BulkImportEntity)
    assert entity.bulk_import_id == 1
