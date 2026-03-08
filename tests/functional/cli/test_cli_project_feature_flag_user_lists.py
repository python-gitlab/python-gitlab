import json

import pytest


@pytest.fixture
def user_list_cli(gitlab_cli, project, user):
    list_name = "cli_test_list_fixture"
    cmd = [
        "-o",
        "json",
        "project-feature-flag-user-list",
        "create",
        "--project-id",
        str(project.id),
        "--name",
        list_name,
        "--user-xids",
        str(user.id),
    ]
    ret = gitlab_cli(cmd)
    data = json.loads(ret.stdout)
    iid = str(data["iid"])

    yield iid

    try:
        cmd = [
            "project-feature-flag-user-list",
            "delete",
            "--project-id",
            str(project.id),
            "--iid",
            iid,
        ]
        gitlab_cli(cmd)
    except Exception:
        pass


def test_project_feature_flag_user_list_cli_create_delete(gitlab_cli, project, user):
    list_name = "cli_test_list_create"

    cmd = [
        "-o",
        "json",
        "project-feature-flag-user-list",
        "create",
        "--project-id",
        str(project.id),
        "--name",
        list_name,
        "--user-xids",
        str(user.id),
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    data = json.loads(ret.stdout)
    assert data["name"] == list_name
    assert str(user.id) in data["user_xids"]
    iid = str(data["iid"])

    cmd = [
        "project-feature-flag-user-list",
        "delete",
        "--project-id",
        str(project.id),
        "--iid",
        iid,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success


def test_project_feature_flag_user_list_cli_list(gitlab_cli, project, user_list_cli):
    cmd = [
        "-o",
        "json",
        "project-feature-flag-user-list",
        "list",
        "--project-id",
        str(project.id),
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    data = json.loads(ret.stdout)
    assert any(item["name"] == "cli_test_list_fixture" for item in data)


def test_project_feature_flag_user_list_cli_get(gitlab_cli, project, user_list_cli):
    cmd = [
        "-o",
        "json",
        "project-feature-flag-user-list",
        "get",
        "--project-id",
        str(project.id),
        "--iid",
        user_list_cli,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    data = json.loads(ret.stdout)
    assert data["name"] == "cli_test_list_fixture"


def test_project_feature_flag_user_list_cli_update(gitlab_cli, project, user_list_cli):
    new_name = "cli_updated_list"
    cmd = [
        "project-feature-flag-user-list",
        "update",
        "--project-id",
        str(project.id),
        "--iid",
        user_list_cli,
        "--name",
        new_name,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
