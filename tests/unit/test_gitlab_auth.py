import pytest
import requests
from requests import PreparedRequest

from gitlab import Gitlab
from gitlab._backends import JobTokenAuth, OAuthTokenAuth, PrivateTokenAuth
from gitlab.config import GitlabConfigParser


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
    p = PreparedRequest()
    p.prepare(url=gl.url, auth=gl._auth)
    assert gl.private_token == "private_token"
    assert gl.oauth_token is None
    assert gl.job_token is None
    assert isinstance(gl._auth, PrivateTokenAuth)
    assert gl._auth.token == "private_token"
    assert p.headers["PRIVATE-TOKEN"] == "private_token"
    assert "JOB-TOKEN" not in p.headers
    assert "Authorization" not in p.headers


def test_oauth_token_auth():
    gl = Gitlab("http://localhost", oauth_token="oauth_token", api_version="4")
    p = PreparedRequest()
    p.prepare(url=gl.url, auth=gl._auth)
    assert gl.private_token is None
    assert gl.oauth_token == "oauth_token"
    assert gl.job_token is None
    assert isinstance(gl._auth, OAuthTokenAuth)
    assert gl._auth.token == "oauth_token"
    assert p.headers["Authorization"] == "Bearer oauth_token"
    assert "PRIVATE-TOKEN" not in p.headers
    assert "JOB-TOKEN" not in p.headers


def test_job_token_auth():
    gl = Gitlab("http://localhost", job_token="CI_JOB_TOKEN", api_version="4")
    p = PreparedRequest()
    p.prepare(url=gl.url, auth=gl._auth)
    assert gl.private_token is None
    assert gl.oauth_token is None
    assert gl.job_token == "CI_JOB_TOKEN"
    assert isinstance(gl._auth, JobTokenAuth)
    assert gl._auth.token == "CI_JOB_TOKEN"
    assert p.headers["JOB-TOKEN"] == "CI_JOB_TOKEN"
    assert "PRIVATE-TOKEN" not in p.headers
    assert "Authorization" not in p.headers


def test_http_auth():
    gl = Gitlab(
        "http://localhost",
        http_username="foo",
        http_password="bar",
        api_version="4",
    )
    p = PreparedRequest()
    p.prepare(url=gl.url, auth=gl._auth)
    assert gl.private_token is None
    assert gl.oauth_token is None
    assert gl.job_token is None
    assert isinstance(gl._auth, requests.auth.HTTPBasicAuth)
    assert gl._auth.username == "foo"
    assert gl._auth.password == "bar"
    assert p.headers["Authorization"] == "Basic Zm9vOmJhcg=="
    assert "PRIVATE-TOKEN" not in p.headers
    assert "JOB-TOKEN" not in p.headers


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
