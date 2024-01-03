"""
GitLab API: https://docs.gitlab.com/ee/api/project_access_tokens.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectAccessToken


@pytest.fixture
def resp_list_project_access_token(token_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/access_tokens",
            json=[token_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_project_access_token(token_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/access_tokens/1",
            json=token_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_project_access_token(token_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/access_tokens",
            json=token_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_revoke_project_access_token():
    content = [
        {
            "user_id": 141,
            "scopes": ["api"],
            "name": "token",
            "expires_at": "2021-01-31",
            "id": 42,
            "active": True,
            "created_at": "2021-01-20T22:11:48.151Z",
            "revoked": False,
        }
    ]

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/access_tokens/42",
            status=204,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/access_tokens",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_rotate_project_access_token(token_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/access_tokens/1/rotate",
            json=token_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_access_tokens(gl, resp_list_project_access_token):
    access_tokens = gl.projects.get(1, lazy=True).access_tokens.list()
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].name == "token"


def test_get_project_access_token(project, resp_get_project_access_token):
    access_token = project.access_tokens.get(1)
    assert isinstance(access_token, ProjectAccessToken)
    assert access_token.revoked is False
    assert access_token.name == "token"


def test_create_project_access_token(gl, resp_create_project_access_token):
    access_tokens = gl.projects.get(1, lazy=True).access_tokens.create(
        {"name": "test", "scopes": ["api"]}
    )
    assert access_tokens.revoked is False
    assert access_tokens.user_id == 141
    assert access_tokens.expires_at == "2021-01-31"


def test_revoke_project_access_token(
    gl, resp_list_project_access_token, resp_revoke_project_access_token
):
    gl.projects.get(1, lazy=True).access_tokens.delete(42)
    access_token = gl.projects.get(1, lazy=True).access_tokens.list()[0]
    access_token.delete()


def test_rotate_project_access_token(project, resp_rotate_project_access_token):
    access_token = project.access_tokens.get(1, lazy=True)
    access_token.rotate()
    assert isinstance(access_token, ProjectAccessToken)
    assert access_token.token == "s3cr3t"
