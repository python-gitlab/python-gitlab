"""
GitLab API:
https://docs.gitlab.com/ee/api/personal_access_tokens.html
https://docs.gitlab.com/ee/api/users.html#create-a-personal-access-token
"""

import pytest
import responses

from gitlab.v4.objects import PersonalAccessToken

user_id = 1
token_id = 1
token_name = "Test Token"

token_url = "http://localhost/api/v4/personal_access_tokens"
single_token_url = f"{token_url}/{token_id}"
self_token_url = f"{token_url}/self"
user_token_url = f"http://localhost/api/v4/users/{user_id}/personal_access_tokens"

content = {
    "id": token_id,
    "name": token_name,
    "revoked": False,
    "created_at": "2020-07-23T14:31:47.729Z",
    "scopes": ["api"],
    "active": True,
    "user_id": user_id,
    "expires_at": None,
}


@pytest.fixture
def resp_create_user_personal_access_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=user_token_url,
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_personal_access_tokens():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=token_url,
            json=[content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_personal_access_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=single_token_url,
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_personal_access_token_self():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=self_token_url,
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_personal_access_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=single_token_url,
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_rotate_personal_access_token(token_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/personal_access_tokens/1/rotate",
            json=token_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_create_personal_access_token(gl, resp_create_user_personal_access_token):
    user = gl.users.get(1, lazy=True)
    access_token = user.personal_access_tokens.create(
        {"name": token_name, "scopes": "api"}
    )
    assert access_token.revoked is False
    assert access_token.name == token_name


def test_list_personal_access_tokens(gl, resp_list_personal_access_tokens):
    access_tokens = gl.personal_access_tokens.list()
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].name == token_name


def test_list_personal_access_tokens_filter(gl, resp_list_personal_access_tokens):
    access_tokens = gl.personal_access_tokens.list(user_id=user_id)
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].user_id == user_id


def test_get_personal_access_token(gl, resp_get_personal_access_token):
    access_token = gl.personal_access_tokens.get(token_id)

    assert access_token.revoked is False
    assert access_token.user_id == user_id


def test_get_personal_access_token_self(gl, resp_get_personal_access_token_self):
    access_token = gl.personal_access_tokens.get("self")

    assert access_token.revoked is False
    assert access_token.user_id == user_id


def test_delete_personal_access_token(gl, resp_delete_personal_access_token):
    access_token = gl.personal_access_tokens.get(token_id, lazy=True)
    access_token.delete()


def test_revoke_personal_access_token_by_id(gl, resp_delete_personal_access_token):
    gl.personal_access_tokens.delete(token_id)


def test_rotate_project_access_token(gl, resp_rotate_personal_access_token):
    access_token = gl.personal_access_tokens.get(1, lazy=True)
    access_token.rotate()
    assert isinstance(access_token, PersonalAccessToken)
    assert access_token.token == "s3cr3t"
