"""
Some test cases are run in-process to intercept requests to gitlab.com
and example servers.
"""

import copy
import json

import pytest
import responses
import yaml

from gitlab import __version__, config
from gitlab.const import DEFAULT_URL

PRIVATE_TOKEN = "glpat-abc123"
CI_JOB_TOKEN = "ci-job-token"
CI_SERVER_URL = "https://gitlab.example.com"


def test_main_entrypoint(script_runner, gitlab_config):
    ret = script_runner.run(["python", "-m", "gitlab", "--config-file", gitlab_config])
    assert ret.returncode == 2


def test_version(script_runner):
    ret = script_runner.run(["gitlab", "--version"])
    assert ret.stdout.strip() == __version__


def test_config_error_with_help_prints_help(script_runner):
    ret = script_runner.run(["gitlab", "-c", "invalid-file", "--help"])
    assert ret.stdout.startswith("usage:")
    assert ret.returncode == 0


def test_resource_help_prints_actions_vertically(script_runner):
    ret = script_runner.run(["gitlab", "project", "--help"])
    assert "    list                List the GitLab resources\n" in ret.stdout
    assert "    get                 Get a GitLab resource\n" in ret.stdout
    assert ret.returncode == 0


def test_resource_help_prints_actions_vertically_only_one_action(script_runner):
    ret = script_runner.run(["gitlab", "event", "--help"])
    assert "  {list}      Action to execute on the GitLab resource.\n"
    assert "    list      List the GitLab resources\n" in ret.stdout
    assert ret.returncode == 0


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_defaults_to_gitlab_com(script_runner, resp_get_project, monkeypatch):
    responses.add(**resp_get_project)
    monkeypatch.setattr(config, "_DEFAULT_FILES", [])
    ret = script_runner.run(["gitlab", "project", "get", "--id", "1"])
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
    ret = script_runner.run(["gitlab", "project", "get", "--id", "1"])
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
    ret = script_runner.run(["gitlab", "project", "get", "--id", "1"])
    assert ret.success


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_does_not_auth_on_skip_login(
    monkeypatch, script_runner, resp_get_project, resp_current_user
):
    monkeypatch.setenv("GITLAB_PRIVATE_TOKEN", PRIVATE_TOKEN)
    monkeypatch.setattr(config, "_DEFAULT_FILES", [])

    resp_user = responses.add(**resp_current_user)
    resp_project = responses.add(**resp_get_project)
    ret = script_runner.run(["gitlab", "--skip-login", "project", "get", "--id", "1"])
    assert ret.success
    assert resp_user.call_count == 0
    assert resp_project.call_count == 1


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
    resp_auth_with_token["json"].update(username="user", web_url=f"{DEFAULT_URL}/user")

    responses.add(**resp_get_project_with_token)
    responses.add(**resp_auth_with_token)
    ret = script_runner.run(["gitlab", "project", "get", "--id", "1"])
    assert ret.success


def test_env_config_missing_file_raises(script_runner, monkeypatch):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", "non-existent")
    ret = script_runner.run(["gitlab", "project", "list"])
    assert not ret.success
    assert ret.stderr.startswith("Cannot read config from PYTHON_GITLAB_CFG")


def test_arg_config_missing_file_raises(script_runner):
    ret = script_runner.run(
        ["gitlab", "--config-file", "non-existent", "project", "list"]
    )
    assert not ret.success
    assert ret.stderr.startswith("Cannot read config from file")


def test_invalid_config(script_runner):
    ret = script_runner.run(["gitlab", "--gitlab", "invalid"])
    assert not ret.success
    assert not ret.stdout


def test_invalid_config_prints_help(script_runner):
    ret = script_runner.run(["gitlab", "--gitlab", "invalid", "--help"])
    assert ret.success
    assert ret.stdout


def test_invalid_api_version(script_runner, monkeypatch, fixture_dir):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", str(fixture_dir / "invalid_version.cfg"))
    ret = script_runner.run(["gitlab", "--gitlab", "test", "project", "list"])
    assert not ret.success
    assert ret.stderr.startswith("Unsupported API version:")


def test_invalid_auth_config(script_runner, monkeypatch, fixture_dir):
    monkeypatch.setenv("PYTHON_GITLAB_CFG", str(fixture_dir / "invalid_auth.cfg"))
    ret = script_runner.run(["gitlab", "--gitlab", "test", "project", "list"])
    assert not ret.success
    assert "401" in ret.stderr


format_matrix = [
    ("json", json.loads),
    ("yaml", yaml.safe_load),
]


@pytest.mark.parametrize("format,loader", format_matrix)
def test_cli_display(gitlab_cli, project, format, loader):
    cmd = ["-o", format, "project", "get", "--id", project.id]

    ret = gitlab_cli(cmd)
    assert ret.success

    content = loader(ret.stdout.strip())
    assert content["id"] == project.id


@pytest.mark.parametrize("format,loader", format_matrix)
def test_cli_fields_in_list(gitlab_cli, project_file, format, loader):
    cmd = [
        "-o",
        format,
        "--fields",
        "default_branch",
        "project",
        "list",
    ]

    ret = gitlab_cli(cmd)
    assert ret.success

    content = loader(ret.stdout.strip())
    assert ["default_branch" in item for item in content]


def test_cli_display_without_fields_warns(gitlab_cli, project):
    cmd = ["project-ci-lint", "get", "--project-id", project.id]

    ret = gitlab_cli(cmd)
    assert ret.success

    assert "No default fields to show" in ret.stdout
    assert "merged_yaml" not in ret.stdout


def test_cli_does_not_print_token(gitlab_cli, gitlab_token):
    ret = gitlab_cli(["--debug", "current-user", "get"])
    assert ret.success

    assert gitlab_token not in ret.stdout
    assert gitlab_token not in ret.stderr
    assert "[MASKED]" in ret.stderr
