"""
GitLab API: https://docs.gitlab.com/ce/api/deploy_tokens.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import ProjectDeployToken

from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/deploy_tokens",
    method="post",
)
def resp_deploy_token_create(url, request):
    content = """{
    "id": 1,
    "name": "test_deploy_token",
    "username": "custom-user",
    "expires_at": "2022-01-01T00:00:00.000Z",
    "token": "jMRvtPNxrn3crTAGukpZ",
    "scopes": [ "read_repository" ]}"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_deploy_token_create)
def test_deploy_tokens(gl):
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
