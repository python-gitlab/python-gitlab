"""
GitLab API: https://docs.gitlab.com/ee/api/project_job_token_scopes.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectJobTokenScope
from gitlab.v4.objects.job_token_scope import (
    AllowlistGroupManager,
    AllowlistProjectManager,
)

job_token_scope_content = {
    "inbound_enabled": True,
    "outbound_enabled": False,
}

project_allowlist_content = [
    {
        "id": 4,
        "description": "",
        "name": "Diaspora Client",
        "name_with_namespace": "Diaspora / Diaspora Client",
        "path": "diaspora-client",
        "path_with_namespace": "diaspora/diaspora-client",
        "created_at": "2013-09-30T13:46:02Z",
        "default_branch": "main",
        "tag_list": ["example", "disapora client"],
        "topics": ["example", "disapora client"],
        "ssh_url_to_repo": "git@gitlab.example.com:diaspora/diaspora-client.git",
        "http_url_to_repo": "https://gitlab.example.com/diaspora/diaspora-client.git",
        "web_url": "https://gitlab.example.com/diaspora/diaspora-client",
        "avatar_url": "https://gitlab.example.com/uploads/project/avatar/4/uploads/avatar.png",
        "star_count": 0,
        "last_activity_at": "2013-09-30T13:46:02Z",
        "namespace": {
            "id": 2,
            "name": "Diaspora",
            "path": "diaspora",
            "kind": "group",
            "full_path": "diaspora",
            "parent_id": "",
            "avatar_url": "",
            "web_url": "https://gitlab.example.com/diaspora",
        },
    }
]

project_allowlist_created_content = {
    "target_project_id": 2,
    "project_id": 1,
}

groups_allowlist_content = [
    {
        "id": 4,
        "web_url": "https://gitlab.example.com/groups/diaspora/diaspora-group",
        "name": "namegroup",
    }
]

group_allowlist_created_content = {
    "target_group_id": 4,
    "project_id": 1,
}


@pytest.fixture
def resp_get_job_token_scope():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/job_token_scope",
            json=job_token_scope_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_allowlist():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/job_token_scope/allowlist",
            json=project_allowlist_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_add_to_allowlist():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/job_token_scope/allowlist",
            json=project_allowlist_created_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_groups_allowlist():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/job_token_scope/groups_allowlist",
            json=groups_allowlist_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_add_to_groups_allowlist():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/job_token_scope/groups_allowlist",
            json=group_allowlist_created_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_patch_job_token_scope():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/projects/1/job_token_scope",
            status=204,
            match=[responses.matchers.json_params_matcher({"enabled": False})],
        )
        yield rsps


@pytest.fixture
def job_token_scope(project, resp_get_job_token_scope):
    return project.job_token_scope.get()


def test_get_job_token_scope(project, resp_get_job_token_scope):
    scope = project.job_token_scope.get()
    assert isinstance(scope, ProjectJobTokenScope)
    assert scope.inbound_enabled is True


def test_refresh_job_token_scope(job_token_scope, resp_get_job_token_scope):
    job_token_scope.refresh()
    assert job_token_scope.inbound_enabled is True


def test_save_job_token_scope(job_token_scope, resp_patch_job_token_scope):
    job_token_scope.enabled = False
    job_token_scope.save()


def test_update_job_token_scope(project, resp_patch_job_token_scope):
    project.job_token_scope.update(new_data={"enabled": False})


def test_get_projects_allowlist(job_token_scope, resp_get_allowlist):
    allowlist = job_token_scope.allowlist
    assert isinstance(allowlist, AllowlistProjectManager)

    allowlist_content = allowlist.list()
    assert isinstance(allowlist_content, list)
    assert allowlist_content[0].get_id() == 4


def test_add_project_to_allowlist(job_token_scope, resp_add_to_allowlist):
    allowlist = job_token_scope.allowlist
    assert isinstance(allowlist, AllowlistProjectManager)

    resp = allowlist.create({"target_project_id": 2})
    assert resp.get_id() == 2


def test_get_groups_allowlist(job_token_scope, resp_get_groups_allowlist):
    allowlist = job_token_scope.groups_allowlist
    assert isinstance(allowlist, AllowlistGroupManager)

    allowlist_content = allowlist.list()
    assert isinstance(allowlist_content, list)
    assert allowlist_content[0].get_id() == 4


def test_add_group_to_allowlist(job_token_scope, resp_add_to_groups_allowlist):
    allowlist = job_token_scope.groups_allowlist
    assert isinstance(allowlist, AllowlistGroupManager)

    resp = allowlist.create({"target_group_id": 4})
    assert resp.get_id() == 4
