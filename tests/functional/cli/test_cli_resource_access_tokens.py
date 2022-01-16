import pytest


def test_list_project_access_tokens(gitlab_cli, project):
    cmd = ["project-access-token", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


@pytest.mark.skip(reason="Requires GitLab 14.7")
def test_list_group_access_tokens(gitlab_cli, group):
    cmd = ["group-access-token", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success
