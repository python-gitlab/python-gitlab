import pytest

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectRegistryProtectionRule


@pytest.fixture(scope="module", autouse=True)
def protected_registry_feature(gl: Gitlab):
    gl.features.set(name="container_registry_protected_containers", value=True)


def test_list_project_protected_registries(project: Project):
    rules = project.registry_protection_rules.list()
    assert isinstance(rules, list)


@pytest.mark.skip(reason="Not released yet")
def test_create_project_protected_registry(project: Project):
    protected_registry = project.registry_protection_rules.create(
        {
            "repository_path_pattern": "test/image",
            "minimum_access_level_for_push": "maintainer",
        }
    )
    assert isinstance(protected_registry, ProjectRegistryProtectionRule)
    assert protected_registry.repository_path_pattern == "test/image"

    protected_registry.minimum_access_level_for_push = "owner"
    protected_registry.save()
    assert protected_registry.minimum_access_level_for_push == "owner"
