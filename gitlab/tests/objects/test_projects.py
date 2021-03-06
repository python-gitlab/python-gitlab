"""
GitLab API: https://docs.gitlab.com/ce/api/projects.html
"""

import pytest
import responses

from gitlab.v4.objects import Project


project_content = {"name": "name", "id": 1}
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


@pytest.mark.skip(reason="missing test")
def test_list_user_projects(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_list_user_starred_projects(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_list_project_users(gl):
    pass


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


@pytest.mark.skip(reason="missing test")
def test_list_project_forks(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_star_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_unstar_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_list_project_starrers(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_get_project_languages(gl):
    pass


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
def test_list_project_hooks(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_get_project_hook(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_create_project_hook(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_update_project_hook(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_delete_project_hook(gl):
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


@pytest.mark.skip(reason="missing test")
def test_transfer_project(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_project_pull_mirror(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_project_snapshot(gl):
    pass


@pytest.mark.skip(reason="missing test")
def test_import_github(gl):
    pass
