"""
GitLab API: https://docs.gitlab.com/ce/api/projects.html
"""

import pytest


from gitlab.v4.objects import Project
from httmock import urlmatch, response, with_httmock

from .mocks import headers


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects/1", method="get")
def resp_get_project(url, request):
    content = '{"name": "name", "id": 1}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_project)
def test_get_project(gl):
    data = gl.projects.get(1)
    assert isinstance(data, Project)
    assert data.name == "name"
    assert data.id == 1


@pytest.mark.skip(reason="missing test")
def test_list_projects(gl):
    pass


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
