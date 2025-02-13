"""
GitLab API: https://docs.gitlab.com/ee/api/status_checks.html
"""

import pytest
import responses


@pytest.fixture
def member_roles():
    return {
        "id": 2,
        "name": "Custom role",
        "description": "Custom guest that can read code",
        "group_id": None,
        "base_access_level": 10,
        "admin_cicd_variables": False,
        "admin_compliance_framework": False,
        "admin_group_member": False,
        "admin_merge_request": False,
        "admin_push_rules": False,
        "admin_terraform_state": False,
        "admin_vulnerability": False,
        "admin_web_hook": False,
        "archive_project": False,
        "manage_deploy_tokens": False,
        "manage_group_access_tokens": False,
        "manage_merge_request_settings": False,
        "manage_project_access_tokens": False,
        "manage_security_policy_link": False,
        "read_code": True,
        "read_runners": False,
        "read_dependency": False,
        "read_vulnerability": False,
        "remove_group": False,
        "remove_project": False,
    }


@pytest.fixture
def create_member_role():
    return {
        "id": 3,
        "name": "Custom webhook manager role",
        "description": "Custom reporter that can manage webhooks",
        "group_id": None,
        "base_access_level": 20,
        "admin_cicd_variables": False,
        "admin_compliance_framework": False,
        "admin_group_member": False,
        "admin_merge_request": False,
        "admin_push_rules": False,
        "admin_terraform_state": False,
        "admin_vulnerability": False,
        "admin_web_hook": True,
        "archive_project": False,
        "manage_deploy_tokens": False,
        "manage_group_access_tokens": False,
        "manage_merge_request_settings": False,
        "manage_project_access_tokens": False,
        "manage_security_policy_link": False,
        "read_code": False,
        "read_runners": False,
        "read_dependency": False,
        "read_vulnerability": False,
        "remove_group": False,
        "remove_project": False,
    }


@pytest.fixture
def resp_list_member_roles(member_roles):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/member_roles",
            json=[member_roles],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_member_roles(create_member_role):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/member_roles",
            json=create_member_role,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_member_roles():
    content = []

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/member_roles/1",
            status=204,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/member_roles",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_group_member_roles(member_roles):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/member_roles",
            json=[member_roles],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_group_member_roles(create_member_role):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/member_roles",
            json=create_member_role,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_group_member_roles():
    content = []

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/member_roles/1",
            status=204,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/member_roles",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_member_roles(gl, resp_list_member_roles):
    member_roles = gl.member_roles.list()
    assert len(member_roles) == 1
    assert member_roles[0].name == "Custom role"


def test_create_member_roles(gl, resp_create_member_roles):
    member_role = gl.member_roles.create(
        {
            "name": "Custom webhook manager role",
            "base_access_level": 20,
            "description": "Custom reporter that can manage webhooks",
            "admin_web_hook": True,
        }
    )
    assert member_role.name == "Custom webhook manager role"
    assert member_role.base_access_level == 20


def test_delete_member_roles(gl, resp_delete_member_roles):
    gl.member_roles.delete(1)
    member_roles_after_delete = gl.member_roles.list()
    assert len(member_roles_after_delete) == 0


def test_list_group_member_roles(gl, resp_list_group_member_roles):
    member_roles = gl.groups.get(1, lazy=True).member_roles.list()
    assert len(member_roles) == 1


def test_create_group_member_roles(gl, resp_create_group_member_roles):
    member_role = gl.groups.get(1, lazy=True).member_roles.create(
        {
            "name": "Custom webhook manager role",
            "base_access_level": 20,
            "description": "Custom reporter that can manage webhooks",
            "admin_web_hook": True,
        }
    )
    assert member_role.name == "Custom webhook manager role"
    assert member_role.base_access_level == 20


def test_delete_group_member_roles(gl, resp_delete_group_member_roles):
    gl.groups.get(1, lazy=True).member_roles.delete(1)
    member_roles_after_delete = gl.groups.get(1, lazy=True).member_roles.list()
    assert len(member_roles_after_delete) == 0
