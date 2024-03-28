import datetime


def test_list_project_access_tokens(gitlab_cli, project):
    cmd = ["project-access-token", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_project_access_token_with_scopes(gitlab_cli, project):
    cmd = [
        "project-access-token",
        "create",
        "--project-id",
        project.id,
        "--name",
        "test-token",
        "--scopes",
        "api,read_repository",
        "--expires-at",
        datetime.date.today().isoformat(),
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_group_access_tokens(gitlab_cli, group):
    cmd = ["group-access-token", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_group_access_token_with_scopes(gitlab_cli, group):
    cmd = [
        "group-access-token",
        "create",
        "--group-id",
        group.id,
        "--name",
        "test-token",
        "--scopes",
        "api,read_repository",
        "--expires-at",
        datetime.date.today().isoformat(),
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
