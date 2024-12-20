"""
GitLab API: https://docs.gitlab.com/ee/api/container_repository_protection_rules.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectRegistryRepositoryProtectionRule

protected_registry_content = {
    "id": 1,
    "project_id": 7,
    "repository_path_pattern": "test/image",
    "minimum_access_level_for_push": "maintainer",
    "minimum_access_level_for_delete": "maintainer",
}


@pytest.fixture
def resp_list_protected_registries():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/registry/repository/protection/rules",
            json=[protected_registry_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_protected_registry():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/registry/repository/protection/rules",
            json=protected_registry_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_protected_registry():
    updated_content = protected_registry_content.copy()
    updated_content["repository_path_pattern"] = "abc*"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/projects/1/registry/repository/protection/rules/1",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_protected_registries(project, resp_list_protected_registries):
    protected_registry = project.registry_repository_protection_rules.list()[0]
    assert isinstance(protected_registry, ProjectRegistryRepositoryProtectionRule)
    assert protected_registry.repository_path_pattern == "test/image"


def test_create_project_protected_registry(project, resp_create_protected_registry):
    protected_registry = project.registry_repository_protection_rules.create(
        {
            "repository_path_pattern": "test/image",
            "minimum_access_level_for_push": "maintainer",
        }
    )
    assert isinstance(protected_registry, ProjectRegistryRepositoryProtectionRule)
    assert protected_registry.repository_path_pattern == "test/image"


def test_update_project_protected_registry(project, resp_update_protected_registry):
    updated = project.registry_repository_protection_rules.update(
        1, {"repository_path_pattern": "abc*"}
    )
    assert updated["repository_path_pattern"] == "abc*"
