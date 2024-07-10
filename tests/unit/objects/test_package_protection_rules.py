"""
GitLab API: https://docs.gitlab.com/ee/api/project_packages_protection_rules.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectPackageProtectionRule

protected_package_content = {
    "id": 1,
    "project_id": 7,
    "package_name_pattern": "v*",
    "package_type": "npm",
    "minimum_access_level_for_push": "maintainer",
}


@pytest.fixture
def resp_list_protected_packages():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/packages/protection/rules",
            json=[protected_package_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_protected_package():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/packages/protection/rules",
            json=protected_package_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_protected_package():
    updated_content = protected_package_content.copy()
    updated_content["package_name_pattern"] = "abc*"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/projects/1/packages/protection/rules/1",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_protected_package():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/packages/protection/rules/1",
            status=204,
        )
        yield rsps


def test_list_project_protected_packages(project, resp_list_protected_packages):
    protected_package = project.package_protection_rules.list()[0]
    assert isinstance(protected_package, ProjectPackageProtectionRule)
    assert protected_package.package_type == "npm"


def test_create_project_protected_package(project, resp_create_protected_package):
    protected_package = project.package_protection_rules.create(
        {
            "package_name_pattern": "v*",
            "package_type": "npm",
            "minimum_access_level_for_push": "maintainer",
        }
    )
    assert isinstance(protected_package, ProjectPackageProtectionRule)
    assert protected_package.package_type == "npm"


def test_update_project_protected_package(project, resp_update_protected_package):
    updated = project.package_protection_rules.update(
        1, {"package_name_pattern": "abc*"}
    )
    assert updated["package_name_pattern"] == "abc*"


def test_delete_project_protected_package(project, resp_delete_protected_package):
    project.package_protection_rules.delete(1)
