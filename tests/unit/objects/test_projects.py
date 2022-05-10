"""
GitLab API: https://docs.gitlab.com/ce/api/projects.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    Project,
    ProjectFork,
    ProjectUser,
    StarredProject,
    UserProject,
)

project_content = {"name": "name", "id": 1}
languages_content = {
    "python": 80.00,
    "ruby": 99.99,
    "CoffeeScript": 0.01,
}
user_content = {
    "name": "first",
    "id": 1,
    "state": "active",
}
forks_content = [
    {
        "id": 1,
    },
]
import_content = {
    "id": 1,
    "name": "project",
    "import_status": "scheduled",
}


@pytest.fixture
def resp_get_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1",
            json=project_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_user_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/projects",
            json=[project_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_starred_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/starred_projects",
            json=[project_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_users():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/users",
            json=[user_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_forks():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/forks",
            json=forks_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_languages():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/languages",
            json=languages_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects",
            json=[project_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_import_bitbucket_server():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/import/bitbucket_server",
            json=import_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_transfer_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/transfer",
            json=project_content,
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.json_params_matcher({"namespace": "test-namespace"})
            ],
        )
        yield rsps


def test_get_project(gl, resp_get_project):
    data = gl.projects.get(1)
    assert isinstance(data, Project)
    assert data.name == "name"
    assert data.id == 1


def test_list_projects(gl, resp_list_projects):
    projects = gl.projects.list()
    assert isinstance(projects[0], Project)
    assert projects[0].name == "name"


def test_import_bitbucket_server(gl, resp_import_bitbucket_server):
    res = gl.projects.import_bitbucket_server(
        bitbucket_server_project="project",
        bitbucket_server_repo="repo",
        bitbucket_server_url="url",
        bitbucket_server_username="username",
        personal_access_token="token",
        new_name="new_name",
        target_namespace="namespace",
    )
    assert res["id"] == 1
    assert res["name"] == "project"
    assert res["import_status"] == "scheduled"


def test_list_user_projects(user, resp_user_projects):
    user_project = user.projects.list()[0]
    assert isinstance(user_project, UserProject)
    assert user_project.name == "name"
    assert user_project.id == 1


def test_list_user_starred_projects(user, resp_starred_projects):
    starred_projects = user.starred_projects.list()[0]
    assert isinstance(starred_projects, StarredProject)
    assert starred_projects.name == "name"
    assert starred_projects.id == 1


def test_list_project_users(project, resp_list_users):
    user = project.users.list()[0]
    assert isinstance(user, ProjectUser)
    assert user.id == 1
    assert user.name == "first"
    assert user.state == "active"


@pytest.mark.skip(reason="missing test")
def test_create_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_create_user_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_update_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_fork_project(gl):
    pass


def test_list_project_forks(project, resp_list_forks):
    fork = project.forks.list()[0]
    assert isinstance(fork, ProjectFork)
    assert fork.id == 1


@pytest.mark.skip(reason="missing test")
def test_star_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_unstar_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_list_project_starrers(gl):
    pass


def test_get_project_languages(project, resp_list_languages):
    python = project.languages().get("python")
    ruby = project.languages().get("ruby")
    coffee_script = project.languages().get("CoffeeScript")
    assert python == 80.00
    assert ruby == 99.99
    assert coffee_script == 00.01


@pytest.mark.skip(reason="missing test")
def test_archive_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_unarchive_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_remove_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_restore_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_upload_file(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_share_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_delete_shared_project_link(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_create_forked_from_relationship(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_delete_forked_from_relationship(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_search_projects_by_name(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_project_housekeeping(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_get_project_push_rules(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_create_project_push_rule(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_update_project_push_rule(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_delete_project_push_rule(gl):
    pass


def test_transfer_project(project, resp_transfer_project):
    project.transfer("test-namespace")


def test_transfer_project_deprecated_warns(project, resp_transfer_project):
    with pytest.warns(DeprecationWarning):
        project.transfer_project("test-namespace")


@pytest.mark.skip(reason="missing test")
def test_project_pull_mirror(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_project_snapshot(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_import_github(gl):
    pass
