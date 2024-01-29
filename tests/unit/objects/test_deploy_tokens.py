"""
GitLab API: https://docs.gitlab.com/ce/api/deploy_tokens.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectDeployToken

create_content = {
    "id": 1,
    "name": "test_deploy_token",
    "username": "custom-user",
    "expires_at": "2022-01-01T00:00:00.000Z",
    "token": "jMRvtPNxrn3crTAGukpZ",
    "scopes": ["read_repository"],
}


@pytest.fixture
def resp_deploy_token_create():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/deploy_tokens",
            json=create_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_deploy_tokens(gl, resp_deploy_token_create):
    deploy_token = gl.projects.get(1, lazy=True).deploytokens.create(
        {
            "name": "test_deploy_token",
            "expires_at": "2022-01-01T00:00:00.000Z",
            "username": "custom-user",
            "scopes": ["read_repository"],
        }
    )
    assert isinstance(deploy_token, ProjectDeployToken)
    assert deploy_token.id == 1
    assert deploy_token.expires_at == "2022-01-01T00:00:00.000Z"
    assert deploy_token.username == "custom-user"
    assert deploy_token.scopes == ["read_repository"]
