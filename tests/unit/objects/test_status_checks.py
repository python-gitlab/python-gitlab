"""
GitLab API: https://docs.gitlab.com/ee/api/status_checks.html
"""

import pytest
import responses

mr_content = {
    "id": 1,
    "iid": 1,
    "project_id": 1,
    "title": "test1",
    "description": "fixed login page css paddings",
    "state": "merged",
    "sha": "somerandomstring",
    "merged_by": {
        "id": 87854,
        "name": "Douwe Maan",
        "username": "DouweM",
        "state": "active",
        "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
        "web_url": "https://gitlab.com/DouweM",
    },
    "reviewers": [
        {
            "id": 2,
            "name": "Sam Bauch",
            "username": "kenyatta_oconnell",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
            "web_url": "http://gitlab.example.com//kenyatta_oconnell",
        }
    ],
}

external_status_checks_content = [
    {
        "id": 2,
        "name": "Service 2",
        "external_url": "https://gitlab.example.com/test-endpoint-2",
        "status": "pending",
    },
    {
        "id": 1,
        "name": "Service 1",
        "external_url": "https://gitlab.example.com/test-endpoint-1",
        "status": "pending",
    },
]


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


@pytest.fixture
def resp_list_merge_requests_status_checks():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1",
            json=mr_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/status_checks",
            json=external_status_checks_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_merge_requests_status_checks_set_value():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1",
            json=mr_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/status_checks",
            json=external_status_checks_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/1/status_check_responses",
            json={"status": "passed"},
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


def test_get_merge_request_external_status_checks(
    gl, resp_list_merge_requests_status_checks
):
    merge_request = gl.projects.get(1, lazy=True).mergerequests.get(1)
    external_status_checks = merge_request.external_status_checks.list()
    assert len(external_status_checks) == 2


def test_get_merge_request_external_status_checks_set_value(
    gl, resp_list_merge_requests_status_checks_set_value
):
    merge_request = gl.projects.get(1, lazy=True).mergerequests.get(1)
    external_status_checks = merge_request.external_status_checks.list()

    assert len(external_status_checks) == 2
    for external_status_check in external_status_checks:
        if external_status_check.name == "Service 2":
            response = merge_request.external_status_check_response.update(
                {
                    "external_status_check_id": external_status_check.id,
                    "status": "passed",
                    "sha": merge_request.sha,
                }
            )
            response["status"] == "passed"
