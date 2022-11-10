"""
GitLab API: https://docs.gitlab.com/ce/api/groups.html
"""

import re

import pytest
import responses

import gitlab
from gitlab.v4.objects import GroupDescendantGroup, GroupSubgroup
from gitlab.v4.objects.projects import GroupProject, SharedProject

content = {"name": "name", "id": 1, "path": "path"}
ldap_group_links_content = [
    {
        "cn": None,
        "group_access": 40,
        "provider": "ldapmain",
        "filter": "(memberOf=cn=some_group,ou=groups,ou=fake_ou,dc=sub_dc,dc=example,dc=tld)",
    }
]
projects_content = [
    {
        "id": 9,
        "description": "foo",
        "default_branch": "master",
        "name": "Html5 Boilerplate",
        "name_with_namespace": "Experimental / Html5 Boilerplate",
        "path": "html5-boilerplate",
        "path_with_namespace": "h5bp/html5-boilerplate",
        "namespace": {"id": 5, "name": "Experimental", "path": "h5bp", "kind": "group"},
    }
]
subgroup_descgroup_content = [
    {
        "id": 2,
        "name": "Bar Group",
        "path": "foo/bar",
        "description": "A subgroup of Foo Group",
        "visibility": "public",
        "share_with_group_lock": False,
        "require_two_factor_authentication": False,
        "two_factor_grace_period": 48,
        "project_creation_level": "developer",
        "auto_devops_enabled": None,
        "subgroup_creation_level": "owner",
        "emails_disabled": None,
        "mentions_disabled": None,
        "lfs_enabled": True,
        "default_branch_protection": 2,
        "avatar_url": "http://gitlab.example.com/uploads/group/avatar/1/bar.jpg",
        "web_url": "http://gitlab.example.com/groups/foo/bar",
        "request_access_enabled": False,
        "full_name": "Bar Group",
        "full_path": "foo/bar",
        "file_template_project_id": 1,
        "parent_id": 123,
        "created_at": "2020-01-15T12:36:29.590Z",
    },
]
push_rules_content = {
    "id": 2,
    "created_at": "2020-08-17T19:09:19.580Z",
    "commit_message_regex": "[a-zA-Z]",
    "commit_message_negative_regex": "[x+]",
    "branch_name_regex": "[a-z]",
    "deny_delete_tag": True,
    "member_check": True,
    "prevent_secrets": True,
    "author_email_regex": "^[A-Za-z0-9.]+@gitlab.com$",
    "file_name_regex": "(exe)$",
    "max_file_size": 100,
}


@pytest.fixture
def resp_groups():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_group_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/groups/1/projects(/shared)?"),
            json=projects_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_subgroups_descendant_groups():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/groups/1/(subgroups|descendant_groups)"
            ),
            json=subgroup_descgroup_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_import(accepted_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/import",
            json=accepted_content,
            content_type="application/json",
            status=202,
        )
        yield rsps


@pytest.fixture
def resp_transfer_group():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/transfer",
            json=content,
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.json_params_matcher({"group_id": "test-namespace"})
            ],
        )
        yield rsps


@pytest.fixture
def resp_list_push_rules_group():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_push_rules_group():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_push_rules_group():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_push_rules_group(no_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=push_rules_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/push_rule",
            json=no_content,
            content_type="application/json",
            status=204,
        )
        yield rsps


def test_get_group(gl, resp_groups):
    data = gl.groups.get(1)
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == "name"
    assert data.path == "path"
    assert data.id == 1


def test_create_group(gl, resp_groups):
    name, path = "name", "path"
    data = gl.groups.create({"name": name, "path": path})
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == name
    assert data.path == path


def test_create_group_export(group, resp_export):
    export = group.exports.create()
    assert export.message == "202 Accepted"


def test_list_group_projects(group, resp_list_group_projects):
    projects = group.projects.list()
    assert isinstance(projects[0], GroupProject)
    assert projects[0].path == projects_content[0]["path"]


def test_list_group_shared_projects(group, resp_list_group_projects):
    projects = group.shared_projects.list()
    assert isinstance(projects[0], SharedProject)
    assert projects[0].path == projects_content[0]["path"]


def test_list_group_subgroups(group, resp_list_subgroups_descendant_groups):
    subgroups = group.subgroups.list()
    assert isinstance(subgroups[0], GroupSubgroup)
    assert subgroups[0].path == subgroup_descgroup_content[0]["path"]


def test_list_group_descendant_groups(group, resp_list_subgroups_descendant_groups):
    descendant_groups = group.descendant_groups.list()
    assert isinstance(descendant_groups[0], GroupDescendantGroup)
    assert descendant_groups[0].path == subgroup_descgroup_content[0]["path"]


@pytest.fixture
def resp_list_ldap_group_links(no_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/ldap_group_links",
            json=ldap_group_links_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.mark.skip("GitLab API endpoint not implemented")
def test_refresh_group_export_status(group, resp_export):
    export = group.exports.create()
    export.refresh()
    assert export.export_status == "finished"


def test_download_group_export(group, resp_export, binary_content):
    export = group.exports.create()
    download = export.download()
    assert isinstance(download, bytes)
    assert download == binary_content


def test_import_group(gl, resp_create_import):
    group_import = gl.groups.import_group("file", "api-group", "API Group")
    assert group_import["message"] == "202 Accepted"


@pytest.mark.skip("GitLab API endpoint not implemented")
def test_refresh_group_import_status(group, resp_groups):
    group_import = group.imports.get()
    group_import.refresh()
    assert group_import.import_status == "finished"


def test_transfer_group(gl, resp_transfer_group):
    group = gl.groups.get(1, lazy=True)
    group.transfer("test-namespace")


def test_list_group_push_rules(group, resp_list_push_rules_group):
    pr = group.pushrules.get()
    assert pr
    assert pr.deny_delete_tag


def test_create_group_push_rule(group, resp_create_push_rules_group):
    group.pushrules.create({"deny_delete_tag": True})


def test_update_group_push_rule(
    group,
    resp_update_push_rules_group,
):
    pr = group.pushrules.get()
    pr.deny_delete_tag = False
    pr.save()


def test_delete_group_push_rule(group, resp_delete_push_rules_group):
    pr = group.pushrules.get()
    pr.delete()
