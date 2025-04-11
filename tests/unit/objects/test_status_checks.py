"""
GitLab API: https://docs.gitlab.com/ee/api/status_checks.html
"""

import pytest
import responses


@pytest.fixture
def external_status_check():
    return {
        "id": 1,
        "name": "MR blocker",
        "project_id": 1,
        "external_url": "https://example.com/mr-blocker",
        "hmac": True,
        "protected_branches": [
            {
                "id": 1,
                "project_id": 1,
                "name": "main",
                "created_at": "2020-10-12T14:04:50.787Z",
                "updated_at": "2020-10-12T14:04:50.787Z",
                "code_owner_approval_required": False,
            }
        ],
    }


@pytest.fixture
def updated_external_status_check():
    return {
        "id": 1,
        "name": "Updated MR blocker",
        "project_id": 1,
        "external_url": "https://example.com/mr-blocker",
        "hmac": True,
        "protected_branches": [
            {
                "id": 1,
                "project_id": 1,
                "name": "main",
                "created_at": "2020-10-12T14:04:50.787Z",
                "updated_at": "2020-10-12T14:04:50.787Z",
                "code_owner_approval_required": False,
            }
        ],
    }


@pytest.fixture
def resp_list_external_status_checks(external_status_check):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/external_status_checks",
            json=[external_status_check],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_external_status_checks(external_status_check):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/external_status_checks",
            json=external_status_check,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_update_external_status_checks(updated_external_status_check):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/groups/1/external_status_checks",
            json=updated_external_status_check,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_external_status_checks():
    content = []

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/external_status_checks/1",
            status=204,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/external_status_checks",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_external_status_checks(gl, resp_list_external_status_checks):
    status_checks = gl.projects.get(1, lazy=True).external_status_checks.list()
    assert len(status_checks) == 1
    assert status_checks[0].name == "MR blocker"


def test_create_external_status_checks(gl, resp_create_external_status_checks):
    access_token = gl.projects.get(1, lazy=True).external_status_checks.create(
        {"name": "MR blocker", "external_url": "https://example.com/mr-blocker"}
    )
    assert access_token.name == "MR blocker"
    assert access_token.external_url == "https://example.com/mr-blocker"


def test_delete_external_status_checks(gl, resp_delete_external_status_checks):
    gl.projects.get(1, lazy=True).external_status_checks.delete(1)
    status_checks = gl.projects.get(1, lazy=True).external_status_checks.list()
    assert len(status_checks) == 0
