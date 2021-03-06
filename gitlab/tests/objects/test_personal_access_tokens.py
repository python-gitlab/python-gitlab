"""
GitLab API: https://docs.gitlab.com/ee/api/personal_access_tokens.html
"""

import pytest
import responses


@pytest.fixture
def resp_list_personal_access_token():
    content = [
        {
            "id": 4,
            "name": "Test Token",
            "revoked": False,
            "created_at": "2020-07-23T14:31:47.729Z",
            "scopes": ["api"],
            "active": True,
            "user_id": 24,
            "expires_at": None,
        }
    ]

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/personal_access_tokens",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_personal_access_tokens(gl, resp_list_personal_access_token):
    access_tokens = gl.personal_access_tokens.list()
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].name == "Test Token"


def test_list_personal_access_tokens_filter(gl, resp_list_personal_access_token):
    access_tokens = gl.personal_access_tokens.list(user_id=24)
    assert len(access_tokens) == 1
    assert access_tokens[0].revoked is False
    assert access_tokens[0].user_id == 24
