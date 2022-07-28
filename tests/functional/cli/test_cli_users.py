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
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
