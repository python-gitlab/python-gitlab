import json

import pytest


@pytest.fixture
def feature_flag_cli(gitlab_cli, project):
    flag_name = "test_flag_cli_fixture"
    cmd = [
        "project-feature-flag",
        "create",
        "--project-id",
        str(project.id),
        "--name",
        flag_name,
    ]
    gitlab_cli(cmd)
    yield flag_name
    try:
        cmd = [
            "project-feature-flag",
            "delete",
            "--project-id",
            str(project.id),
            "--name",
            flag_name,
        ]
        gitlab_cli(cmd)
    except Exception:
        pass


def test_project_feature_flag_cli_create_delete(gitlab_cli, project):
    flag_name = "test_flag_cli_create"
    cmd = [
        "project-feature-flag",
        "create",
        "--project-id",
        str(project.id),
        "--name",
        flag_name,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    assert flag_name in ret.stdout

    cmd = [
        "project-feature-flag",
        "delete",
        "--project-id",
        str(project.id),
        "--name",
        flag_name,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success


def test_project_feature_flag_cli_create_with_strategies(gitlab_cli, project):
    flag_name = "test_flag_cli_strategies"
    strategies_json = (
        '[{"name": "userWithId", "parameters": {"userIds": "user1,user2"}}]'
    )

    cmd = [
        "project-feature-flag",
        "create",
        "--project-id",
        str(project.id),
        "--name",
        flag_name,
        "--strategies",
        strategies_json,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success

    cmd = [
        "-o",
        "json",
        "project-feature-flag",
        "get",
        "--project-id",
        str(project.id),
        "--name",
        flag_name,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    data = json.loads(ret.stdout)
    assert len(data["strategies"]) == 1
    assert data["strategies"][0]["name"] == "userWithId"


def test_project_feature_flag_cli_list(gitlab_cli, project, feature_flag_cli):
    cmd = ["project-feature-flag", "list", "--project-id", str(project.id)]
    ret = gitlab_cli(cmd)
    assert ret.success
    assert feature_flag_cli in ret.stdout


def test_project_feature_flag_cli_get(gitlab_cli, project, feature_flag_cli):
    cmd = [
        "project-feature-flag",
        "get",
        "--project-id",
        str(project.id),
        "--name",
        feature_flag_cli,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    assert feature_flag_cli in ret.stdout


def test_project_feature_flag_cli_update(gitlab_cli, project, feature_flag_cli):
    cmd = [
        "project-feature-flag",
        "update",
        "--project-id",
        str(project.id),
        "--name",
        feature_flag_cli,
        "--active",
        "false",
    ]
    ret = gitlab_cli(cmd)
    assert ret.success

    cmd = [
        "-o",
        "json",
        "project-feature-flag",
        "get",
        "--project-id",
        str(project.id),
        "--name",
        feature_flag_cli,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    data = json.loads(ret.stdout)
    assert data["active"] is False
