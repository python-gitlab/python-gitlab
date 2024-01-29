"""
GitLab API: https://docs.gitlab.com/ee/api/container_registry.html
"""

import re

import pytest
import responses

from gitlab.v4.objects import ProjectRegistryRepository, RegistryRepository

repositories_content = [
    {
        "id": 1,
        "name": "",
        "path": "group/project",
        "project_id": 9,
        "location": "gitlab.example.com:5000/group/project",
        "created_at": "2019-01-10T13:38:57.391Z",
        "cleanup_policy_started_at": "2020-01-10T15:40:57.391Z",
    },
    {
        "id": 2,
        "name": "releases",
        "path": "group/project/releases",
        "project_id": 9,
        "location": "gitlab.example.com:5000/group/project/releases",
        "created_at": "2019-01-10T13:39:08.229Z",
        "cleanup_policy_started_at": "2020-08-17T03:12:35.489Z",
    },
]


@pytest.fixture
def resp_list_registry_repositories():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/(groups|projects)/1/registry/repositories"
            ),
            json=repositories_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_registry_repository():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/registry/repositories/1",
            json=repositories_content[0],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_registry_repository():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/registry/repositories/1",
            status=204,
        )
        yield rsps


def test_list_group_registry_repositories(group, resp_list_registry_repositories):
    repositories = group.registry_repositories.list()
    assert isinstance(repositories[0], ProjectRegistryRepository)
    assert repositories[0].id == 1


def test_list_project_registry_repositories(project, resp_list_registry_repositories):
    repositories = project.repositories.list()
    assert isinstance(repositories[0], ProjectRegistryRepository)
    assert repositories[0].id == 1


def test_delete_project_registry_repository(project, resp_delete_registry_repository):
    project.repositories.delete(1)


def test_get_registry_repository(gl, resp_get_registry_repository):
    repository = gl.registry_repositories.get(1)
    assert isinstance(repository, RegistryRepository)
    assert repository.id == 1
