def test_list_instance_variables(gitlab_cli, gl):
    cmd = ["variable", "list"]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_group_variables(gitlab_cli, group):
    cmd = ["group-variable", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_project_variables(gitlab_cli, project):
    cmd = ["project-variable", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success
