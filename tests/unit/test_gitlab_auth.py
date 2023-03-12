import pytest
import responses

from gitlab import Gitlab
from gitlab.config import GitlabConfigParser
from gitlab.oauth import PasswordCredentials


# /oauth/token endpoint might be missing correct content-type header
@pytest.fixture(params=["application/json", None])
def resp_oauth_token(gl: Gitlab, request: pytest.FixtureRequest):
    ropc_payload = {
        "username": "foo",
        "password": "bar",
        "grant_type": "password",
        "scope": "api",
    }
    ropc_response = {
        "access_token": "test-token",
        "token_type": "bearer",
        "expires_in": 7200,
    }
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=f"{gl._base_url}/oauth/token",
            status=201,
            match=[responses.matchers.json_params_matcher(ropc_payload)],
            json=ropc_response,
            content_type=request.param,
        )
        yield rsps


def test_invalid_auth_args():
    with pytest.raises(ValueError):
        Gitlab(
            "http://localhost",
            api_version="4",
            private_token="private_token",
            oauth_token="bearer",
        )
    with pytest.raises(ValueError):
        Gitlab(
            "http://localhost",
            api_version="4",
            oauth_token="bearer",
            http_username="foo",
            http_password="bar",
        )
    with pytest.raises(ValueError):
        Gitlab(
            "http://localhost",
            api_version="4",
            private_token="private_token",
            http_password="bar",
        )
    with pytest.raises(ValueError):
        Gitlab(
            "http://localhost",
            api_version="4",
            private_token="private_token",
            http_username="foo",
        )


def test_private_token_auth():
    gl = Gitlab("http://localhost", private_token="private_token", api_version="4")
    assert gl.private_token == "private_token"
    assert gl.oauth_token is None
    assert gl.job_token is None
    assert "Authorization" not in gl.headers
    assert gl.headers["PRIVATE-TOKEN"] == "private_token"
    assert "JOB-TOKEN" not in gl.headers


def test_oauth_token_auth():
    gl = Gitlab("http://localhost", oauth_token="oauth_token", api_version="4")
    assert gl.private_token is None
    assert gl.oauth_token == "oauth_token"
    assert gl.job_token is None
    assert gl.headers["Authorization"] == "Bearer oauth_token"
    assert "PRIVATE-TOKEN" not in gl.headers
    assert "JOB-TOKEN" not in gl.headers


def test_job_token_auth():
    gl = Gitlab("http://localhost", job_token="CI_JOB_TOKEN", api_version="4")
    assert gl.private_token is None
    assert gl.oauth_token is None
    assert gl.job_token == "CI_JOB_TOKEN"
    assert "Authorization" not in gl.headers
    assert "PRIVATE-TOKEN" not in gl.headers
    assert gl.headers["JOB-TOKEN"] == "CI_JOB_TOKEN"


def test_oauth_resource_password_auth(resp_oauth_token):
    oauth_credentials = PasswordCredentials("foo", "bar")
    gl = Gitlab(
        "http://localhost",
        api_version="4",
        oauth_credentials=oauth_credentials,
    )
    assert gl.oauth_token == "test-token"
    assert gl.private_token is None
    assert gl.job_token is None
    assert "Authorization" in gl.headers
    assert "PRIVATE-TOKEN" not in gl.headers


def test_oauth_resource_password_auth_with_legacy_params_warns(resp_oauth_token):
    with pytest.warns(DeprecationWarning, match="use the OAuth ROPC flow"):
        gl = Gitlab(
            "http://localhost",
            http_username="foo",
            http_password="bar",
            api_version="4",
        )
    assert gl.oauth_token == "test-token"
    assert gl.private_token is None
    assert gl.job_token is None
    assert "Authorization" in gl.headers
    assert "PRIVATE-TOKEN" not in gl.headers


@pytest.mark.parametrize(
    "options,config,expected_private_token,expected_oauth_token,expected_job_token",
    [
        (
            {
                "private_token": "options-private-token",
                "oauth_token": "options-oauth-token",
                "job_token": "options-job-token",
            },
            {
                "private_token": "config-private-token",
                "oauth_token": "config-oauth-token",
                "job_token": "config-job-token",
            },
            "options-private-token",
            None,
            None,
        ),
        (
            {
                "private_token": None,
                "oauth_token": "options-oauth-token",
                "job_token": "options-job-token",
            },
            {
                "private_token": "config-private-token",
                "oauth_token": "config-oauth-token",
                "job_token": "config-job-token",
            },
            "config-private-token",
            None,
            None,
        ),
        (
            {
                "private_token": None,
                "oauth_token": None,
                "job_token": "options-job-token",
            },
            {
                "private_token": "config-private-token",
                "oauth_token": "config-oauth-token",
                "job_token": "config-job-token",
            },
            "config-private-token",
            None,
            None,
        ),
        (
            {
                "private_token": None,
                "oauth_token": None,
                "job_token": None,
            },
            {
                "private_token": "config-private-token",
                "oauth_token": "config-oauth-token",
                "job_token": "config-job-token",
            },
            "config-private-token",
            None,
            None,
        ),
        (
            {
                "private_token": None,
                "oauth_token": None,
                "job_token": None,
            },
            {
                "private_token": None,
                "oauth_token": "config-oauth-token",
                "job_token": "config-job-token",
            },
            None,
            "config-oauth-token",
            None,
        ),
        (
            {
                "private_token": None,
                "oauth_token": None,
                "job_token": None,
            },
            {
                "private_token": None,
                "oauth_token": None,
                "job_token": "config-job-token",
            },
            None,
            None,
            "config-job-token",
        ),
    ],
)
def test_merge_auth(
    options,
    config,
    expected_private_token,
    expected_oauth_token,
    expected_job_token,
):
    cp = GitlabConfigParser()
    cp.private_token = config["private_token"]
    cp.oauth_token = config["oauth_token"]
    cp.job_token = config["job_token"]

    private_token, oauth_token, job_token = Gitlab._merge_auth(options, cp)
    assert private_token == expected_private_token
    assert oauth_token == expected_oauth_token
    assert job_token == expected_job_token
