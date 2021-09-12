"""
GitLab API:
https://docs.gitlab.com/ee/api/personal_access_tokens.html
https://docs.gitlab.com/ee/api/users.html#create-a-personal-access-token
"""

import pytest
import responses

user_id = 1
token_id = 1
token_name = "Test Token"

token_url = "http://localhost/api/v4/personal_access_tokens"
single_token_url = f"{token_url}/{token_id}"
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
def resp_personal_access_token(no_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url=token_url,
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url=single_token_url,
            json=no_content,
            content_type="application/json",
            status=204,
        )
        yield rsps


def test_create_personal_access_token(gl, resp_create_user_personal_access_token):
    user = gl.users.get(1, lazy=True)
    access_token = user.personal_access_tokens.create(
        {"name": token_name, "scopes": "api"}
    )
    assert access_token.revoked is False
    assert access_token.name == token_name


def test_list_personal_access_tokens(gl, resp_personal_access_token):
    access_tokens = gl.personal_access_tokens.list()
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].name == token_name


def test_list_personal_access_tokens_filter(gl, resp_personal_access_token):
    access_tokens = gl.personal_access_tokens.list(user_id=user_id)
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].user_id == user_id


def test_revoke_personal_access_token(gl, resp_personal_access_token):
    access_token = gl.personal_access_tokens.list(user_id=user_id)[0]
    access_token.delete()
    assert resp_personal_access_token.assert_call_count(single_token_url, 1)


def test_revoke_personal_access_token_by_id(gl, resp_personal_access_token):
    gl.personal_access_tokens.delete(token_id)
    assert resp_personal_access_token.assert_call_count(single_token_url, 1)
