"""
GitLab API: https://docs.gitlab.com/ce/api/environments.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectEnvironment, ProjectProtectedEnvironment


@pytest.fixture
def resp_get_environment():
    content = {"name": "environment_name", "id": 1, "last_deployment": "sometime"}

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/environments/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_protected_environment():
    content = {
        "name": "protected_environment_name",
        "last_deployment": "my birthday",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/protected_environments/2",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_environments(project, resp_get_environment):
    environment = project.environments.get(1)
    assert isinstance(environment, ProjectEnvironment)
    assert environment.id == 1
    assert environment.last_deployment == "sometime"
    assert environment.name == "environment_name"


def test_project_protected_environments(project, resp_get_protected_environment):
    protected_environment = project.protected_environments.get(2)
    assert isinstance(protected_environment, ProjectProtectedEnvironment)
    assert protected_environment.last_deployment == "my birthday"
    assert protected_environment.name == "protected_environment_name"
