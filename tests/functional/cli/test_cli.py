import json

from gitlab import __version__


def test_main_entrypoint(script_runner, gitlab_config):
    ret = script_runner.run("python", "-m", "gitlab", "--config-file", gitlab_config)
    assert ret.returncode == 2


def test_version(script_runner):
    ret = script_runner.run("gitlab", "--version")
    assert ret.stdout.strip() == __version__


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
