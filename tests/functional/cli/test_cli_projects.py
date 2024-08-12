import subprocess
import time

import pytest
import responses


@pytest.mark.script_launch_mode("inprocess")
@responses.activate
def test_project_registry_delete_in_bulk(
    script_runner, resp_delete_registry_tags_in_bulk
):
    responses.add(**resp_delete_registry_tags_in_bulk)
    cmd = [
        "gitlab",
        "project-registry-tag",
        "delete-in-bulk",
        "--project-id",
        "1",
        "--repository-id",
        "1",
        "--name-regex-delete",
        "^.*dev.*$",
        # TODO: remove `name` after deleting without ID is possible
        # See #849 and #1631
        "--name",
        ".*",
    ]
    ret = ret = script_runner.run(cmd)
    assert ret.success


@pytest.fixture
def project_export(project):
    export = project.exports.create()
    export.refresh()

    count = 0
    while export.export_status != "finished":
        time.sleep(0.5)
        export.refresh()
        count += 1
        if count >= 60:
            raise Exception("Project export taking too much time")

    return export


def test_project_export_download_custom_action(gitlab_config, project_export):
    """Tests custom action on ProjectManager"""
    cmd = [
        "gitlab",
        "--config-file",
        gitlab_config,
        "project-export",
        "download",
        "--project-id",
        str(project_export.id),
    ]

    export = subprocess.run(cmd, capture_output=True, check=True)
    assert export.returncode == 0


def test_project_languages_custom_action(gitlab_cli, project, project_file):
    """Tests custom action on Project/RESTObject"""
    cmd = ["project", "languages", "--id", project.id]
    ret = gitlab_cli(cmd)
    assert ret.success
