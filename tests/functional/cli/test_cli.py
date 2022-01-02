import json

import pytest
import responses

from gitlab import __version__, config


@pytest.fixture
def resp_get_project():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="https://gitlab.com/api/v4/projects/1",
            json={"name": "name", "path": "test-path", "id": 1},
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_main_entrypoint(script_runner, gitlab_config):
    ret = script_runner.run("python", "-m", "gitlab", "--config-file", gitlab_config)
    assert ret.returncode == 2


def test_version(script_runner):
    ret = script_runner.run("gitlab", "--version")
    assert ret.stdout.strip() == __version__


@pytest.mark.script_launch_mode("inprocess")
def test_defaults_to_gitlab_com(script_runner, resp_get_project, monkeypatch):
    with monkeypatch.context() as m:
        # Ensure we don't pick up any config files that may already exist in the local
        # environment.
        m.setattr(config, "_DEFAULT_FILES", [])
        # Runs in-process to intercept requests to gitlab.com
        ret = script_runner.run("gitlab", "project", "get", "--id", "1")
    assert ret.success
    assert "id: 1" in ret.stdout


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
