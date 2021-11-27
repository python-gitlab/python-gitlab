"""
Some test cases are run in-process to intercept requests to gitlab.com
and example servers.
"""

import copy
import json

import pytest
import responses

from gitlab import __version__, config
from gitlab.const import DEFAULT_URL

PRIVATE_TOKEN = "glpat-abc123"
CI_JOB_TOKEN = "ci-job-token"
CI_SERVER_URL = "https://gitlab.example.com"


def test_main_entrypoint(script_runner, gitlab_config):
    ret = script_runner.run("python", "-m", "gitlab", "--config-file", gitlab_config)
    assert ret.returncode == 2


def test_version(script_runner):
    ret = script_runner.run("gitlab", "--version")
    assert ret.stdout.strip() == __version__


def test_config_error_with_help_prints_help(script_runner):
    ret = script_runner.run("gitlab", "-c", "invalid-file", "--help")
    assert ret.stdout.startswith("usage:")
    assert ret.returncode == 0


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_defaults_to_gitlab_com(script_runner, resp_get_project, monkeypatch):
    responses.add(**resp_get_project)
    monkeypatch.setattr(config, "_DEFAULT_FILES", [])
    ret = script_runner.run("gitlab", "project", "get", "--id", "1")
    assert ret.success
    assert "id: 1" in ret.stdout


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_uses_ci_server_url(monkeypatch, script_runner, resp_get_project):
    monkeypatch.setenv("CI_SERVER_URL", CI_SERVER_URL)
    monkeypatch.setattr(config, "_DEFAULT_FILES", [])
    resp_get_project_in_ci = copy.deepcopy(resp_get_project)
    resp_get_project_in_ci.update(url=f"{CI_SERVER_URL}/api/v4/projects/1")

    responses.add(**resp_get_project_in_ci)
    ret = script_runner.run("gitlab", "project", "get", "--id", "1")
    assert ret.success


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_uses_ci_job_token(monkeypatch, script_runner, resp_get_project):
    monkeypatch.setenv("CI_JOB_TOKEN", CI_JOB_TOKEN)
    monkeypatch.setattr(config, "_DEFAULT_FILES", [])
    resp_get_project_in_ci = copy.deepcopy(resp_get_project)
    resp_get_project_in_ci.update(
        match=[responses.matchers.header_matcher({"JOB-TOKEN": CI_JOB_TOKEN})],
    )

    responses.add(**resp_get_project_in_ci)
    ret = script_runner.run("gitlab", "project", "get", "--id", "1")
    assert ret.success


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_private_token_overrides_job_token(
    monkeypatch, script_runner, resp_get_project
):
    monkeypatch.setenv("GITLAB_PRIVATE_TOKEN", PRIVATE_TOKEN)
    monkeypatch.setenv("CI_JOB_TOKEN", CI_JOB_TOKEN)

    resp_get_project_with_token = copy.deepcopy(resp_get_project)
    resp_get_project_with_token.update(
        match=[responses.matchers.header_matcher({"PRIVATE-TOKEN": PRIVATE_TOKEN})],
    )

    # CLI first calls .auth() when private token is present
    resp_auth_with_token = copy.deepcopy(resp_get_project_with_token)
    resp_auth_with_token.update(url=f"{DEFAULT_URL}/api/v4/user")

    responses.add(**resp_get_project_with_token)
    responses.add(**resp_auth_with_token)
    ret = script_runner.run("gitlab", "project", "get", "--id", "1")
    assert ret.success


def test_env_config_missing_file_raises(script_runner, monkeypatch):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", "non-existent")
    ret = script_runner.run("gitlab", "project", "list")
    assert not ret.success
    assert ret.stderr.startswith("Cannot read config from PYTHON_GITLAB_CFG")


def test_arg_config_missing_file_raises(script_runner):
    ret = script_runner.run(
        "gitlab", "--config-file", "non-existent", "project", "list"
    )
    assert not ret.success
    assert ret.stderr.startswith("Cannot read config from file")


def test_invalid_config(script_runner):
    ret = script_runner.run("gitlab", "--gitlab", "invalid")
    assert not ret.success
    assert not ret.stdout


def test_invalid_config_prints_help(script_runner):
    ret = script_runner.run("gitlab", "--gitlab", "invalid", "--help")
    assert ret.success
    assert ret.stdout


def test_invalid_api_version(script_runner, monkeypatch, fixture_dir):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", str(fixture_dir / "invalid_version.cfg"))
    ret = script_runner.run("gitlab", "--gitlab", "test", "project", "list")
    assert not ret.success
    assert ret.stderr.startswith("Unsupported API version:")


def test_invalid_auth_config(script_runner, monkeypatch, fixture_dir):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", str(fixture_dir / "invalid_auth.cfg"))
    ret = script_runner.run("gitlab", "--gitlab", "test", "project", "list")
    assert not ret.success
    assert "401" in ret.stderr


def test_fields(gitlab_cli, project_file):
    cmd = "-o", "json", "--fields", "default_branch", "project", "list"

    ret = gitlab_cli(cmd)
    assert ret.success

    content = json.loads(ret.stdout.strip())
    assert ["default_branch" in item for item in content]
