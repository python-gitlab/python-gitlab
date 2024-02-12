import datetime


def test_create_user_impersonation_token_with_scopes(gitlab_cli, user):
    cmd = [
        "user-impersonation-token",
        "create",
        "--user-id",
        user.id,
        "--name",
        "test-token",
        "--scopes",
        "api,read_user",
        "--expires-at",
        datetime.date.today().isoformat(),
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_user_projects(gitlab_cli, user):
    cmd = ["user-project", "list", "--user-id", user.id]
    ret = gitlab_cli(cmd)

    assert ret.success
