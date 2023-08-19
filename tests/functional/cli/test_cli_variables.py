import copy

import pytest
import responses

from gitlab.const import DEFAULT_URL


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


def test_list_project_variables_with_path(gitlab_cli, project):
    cmd = ["project-variable", "list", "--project-id", project.path_with_namespace]
    ret = gitlab_cli(cmd)

    assert ret.success


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_list_project_variables_with_path_url_check(script_runner, resp_get_project):
    resp_get_project_variables = copy.deepcopy(resp_get_project)
    resp_get_project_variables.update(
        url=f"{DEFAULT_URL}/api/v4/projects/project%2Fwith%2Fa%2Fnamespace/variables"
    )
    resp_get_project_variables.update(json=[])

    responses.add(**resp_get_project_variables)
    ret = script_runner.run(
        [
            "gitlab",
            "project-variable",
            "list",
            "--project-id",
            "project/with/a/namespace",
        ]
    )
    assert ret.success
