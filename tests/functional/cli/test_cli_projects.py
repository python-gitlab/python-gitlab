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
    ret = ret = script_runner.run(*cmd)
    assert ret.success
