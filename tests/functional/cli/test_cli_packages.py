def test_list_project_packages(gitlab_cli, project):
    cmd = ["project-package", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_group_packages(gitlab_cli, group):
    cmd = ["group-package", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success
