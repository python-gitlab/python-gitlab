"""
GitLab API: https://docs.gitlab.com/ce/api/projects.html
"""

from unittest.mock import mock_open, patch

import pytest
import responses

from gitlab import exceptions
from gitlab.const import DEVELOPER_ACCESS, SEARCH_SCOPE_ISSUES
from gitlab.v4.objects import (
    Project,
    ProjectFork,
    ProjectUser,
    StarredProject,
    UserProject,
)
from gitlab.v4.objects.projects import ProjectStorage

project_content = {"name": "name", "id": 1}
project_with_owner_content = {
    "name": "name",
    "id": 1,
    "owner": {"id": 1, "username": "owner_username", "name": "owner_name"},
}
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
project_forked_from_content = {
    "name": "name",
    "id": 2,
    "forks_count": 0,
    "forked_from_project": {"id": 1, "name": "name", "forks_count": 1},
}
project_starrers_content = {
    "starred_since": "2019-01-28T14:47:30.642Z",
    "user": {
        "id": 1,
        "name": "name",
    },
}
upload_file_content = {
    "alt": "filename",
    "url": "/uploads/66dbcd21ec5d24ed6ea225176098d52b/filename.png",
    "full_path": "/namespace/project/uploads/66dbcd21ec5d24ed6ea225176098d52b/filename.png",
    "markdown": "![dk](/uploads/66dbcd21ec5d24ed6ea225176098d52b/filename.png)",
}
share_project_content = {
    "id": 1,
    "project_id": 1,
    "group_id": 1,
    "group_access": 30,
    "expires_at": None,
}
push_rules_content = {"id": 1, "deny_delete_tag": True}
search_issues_content = [
    {
        "id": 1,
        "iid": 1,
        "project_id": 1,
        "title": "Issue",
    }
]
pipeline_trigger_content = {
    "id": 1,
    "iid": 1,
    "project_id": 1,
    "ref": "main",
    "status": "created",
    "source": "trigger",
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
def resp_create_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_create_user_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/user/1",
            json=project_with_owner_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_fork_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/fork",
            json=project_forked_from_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_get_project_storage():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/storage",
            json={"project_id": 1, "disk_path": "/disk/path"},
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_user_projects():
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
def resp_star_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/star",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_unstar_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/unstar",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_list_project_starrers():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/starrers",
            json=[project_starrers_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_starred_projects():
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


@pytest.fixture
def resp_archive_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/archive",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_unarchive_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/unarchive",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_project(accepted_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1",
            json=accepted_content,
            content_type="application/json",
            status=202,
        )
        yield rsps


@pytest.fixture
def resp_upload_file_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/uploads",
            json=upload_file_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_share_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/share",
            json=share_project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_unshare_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/share/1",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_create_fork_relation():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/2/fork/1",
            json=project_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_fork_relation():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/2/fork",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_trigger_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/trigger/pipeline",
            json=pipeline_trigger_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_search_project_resources_by_name():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/search?scope=issues&search=Issue",
            json=search_issues_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_start_housekeeping():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/housekeeping",
            json={},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_list_push_rules_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_push_rules_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_push_rules_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_push_rules_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/push_rule",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_restore_project(created_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/restore",
            json=created_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_start_pull_mirroring_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/mirror/pull",
            json={},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_pull_mirror_details_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/mirror/pull",
            json={
                "id": 101486,
                "last_error": None,
                "last_successful_update_at": "2020-01-06T17:32:02.823Z",
                "last_update_at": "2020-01-06T17:32:02.823Z",
                "last_update_started_at": "2020-01-06T17:31:55.864Z",
                "update_status": "finished",
                "url": "https://*****:*****@gitlab.com/gitlab-org/security/gitlab.git",
            },
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_snapshot_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/snapshot",
            content_type="application/x-tar",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_artifact():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/jobs/artifacts/ref_name/raw/artifact_path?job=job",
            content_type="application/x-tar",
            status=200,
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


def test_list_user_projects(user, resp_list_user_projects):
    user_project = user.projects.list()[0]
    assert isinstance(user_project, UserProject)
    assert user_project.name == "name"
    assert user_project.id == 1


def test_list_user_starred_projects(user, resp_list_starred_projects):
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


def test_create_project(gl, resp_create_project):
    project = gl.projects.create({"name": "name"})
    assert project.id == 1
    assert project.name == "name"


def test_create_user_project(user, resp_create_user_project):
    user_project = user.projects.create({"name": "name"})
    assert user_project.id == 1
    assert user_project.name == "name"
    assert user_project.owner
    assert user_project.owner.get("id") == user.id
    assert user_project.owner.get("name") == "owner_name"
    assert user_project.owner.get("username") == "owner_username"


def test_update_project(project, resp_update_project):
    project.snippets_enabled = 1
    project.save()


def test_fork_project(project, resp_fork_project):
    fork = project.forks.create({})
    assert fork.id == 2
    assert fork.name == "name"
    assert fork.forks_count == 0
    assert fork.forked_from_project
    assert fork.forked_from_project.get("id") == project.id
    assert fork.forked_from_project.get("name") == "name"
    assert fork.forked_from_project.get("forks_count") == 1


def test_list_project_forks(project, resp_list_forks):
    fork = project.forks.list()[0]
    assert isinstance(fork, ProjectFork)
    assert fork.id == 1


def test_star_project(project, resp_star_project):
    project.star()


def test_unstar_project(project, resp_unstar_project):
    project.unstar()


@pytest.mark.skip(reason="missing test")
def test_list_project_starrers(project, resp_list_project_starrers):
    pass


def test_get_project_languages(project, resp_list_languages):
    python = project.languages().get("python")
    ruby = project.languages().get("ruby")
    coffee_script = project.languages().get("CoffeeScript")
    assert python == 80.00
    assert ruby == 99.99
    assert coffee_script == 00.01


def test_get_project_storage(project, resp_get_project_storage):
    storage = project.storage.get()
    assert isinstance(storage, ProjectStorage)
    assert storage.disk_path == "/disk/path"


def test_archive_project(project, resp_archive_project):
    project.archive()


def test_unarchive_project(project, resp_unarchive_project):
    project.unarchive()


def test_delete_project(project, resp_delete_project):
    project.delete()


def test_upload_file(project, resp_upload_file_project):
    project.upload("filename.png", "raw\nfile\ndata")


def test_upload_file_with_filepath(project, resp_upload_file_project):
    with patch("builtins.open", mock_open(read_data="raw\nfile\ndata")):
        project.upload("filename.png", None, "/filepath")


def test_upload_file_without_filepath_nor_filedata(project):
    with pytest.raises(
        exceptions.GitlabUploadError, match="No file contents or path specified"
    ):
        project.upload("filename.png")


def test_upload_file_with_filepath_and_filedata(project):
    with pytest.raises(
        exceptions.GitlabUploadError, match="File contents and file path specified"
    ):
        project.upload("filename.png", "filedata", "/filepath")


def test_share_project(project, group, resp_share_project):
    project.share(group.id, DEVELOPER_ACCESS)


def test_delete_shared_project_link(project, group, resp_unshare_project):
    project.unshare(group.id)


def test_trigger_pipeline_project(project, resp_trigger_pipeline):
    project.trigger_pipeline("MOCK_PIPELINE_TRIGGER_TOKEN", "main")


def test_create_forked_from_relationship(
    project, another_project, resp_create_fork_relation
):
    another_project.create_fork_relation(project.id)


def test_delete_forked_from_relationship(another_project, resp_delete_fork_relation):
    another_project.delete_fork_relation()


def test_search_project_resources_by_name(
    project, resp_search_project_resources_by_name
):
    issue = project.search(SEARCH_SCOPE_ISSUES, "Issue")[0]
    assert issue
    assert issue.get("title") == "Issue"


def test_project_housekeeping(project, resp_start_housekeeping):
    project.housekeeping()


def test_list_project_push_rules(project, resp_list_push_rules_project):
    pr = project.pushrules.get()
    assert pr
    assert pr.deny_delete_tag


def test_create_project_push_rule(project, resp_create_push_rules_project):
    project.pushrules.create({"deny_delete_tag": True})


def test_update_project_push_rule(
    project,
    resp_update_push_rules_project,
):
    pr = project.pushrules.get()
    pr.deny_delete_tag = False
    pr.save()


def test_delete_project_push_rule(project, resp_delete_push_rules_project):
    pr = project.pushrules.get()
    pr.delete()


def test_transfer_project(project, resp_transfer_project):
    project.transfer("test-namespace")


def test_project_pull_mirror(project, resp_start_pull_mirroring_project):
    project.mirror_pull()


def test_project_pull_mirror_details(project, resp_pull_mirror_details_project):
    details = project.mirror_pull_details()
    assert details["last_error"] is None
    assert details["update_status"] == "finished"


def test_project_restore(project, resp_restore_project):
    project.restore()


def test_project_snapshot(project, resp_snapshot_project):
    tar_file = project.snapshot()
    assert isinstance(tar_file, bytes)
