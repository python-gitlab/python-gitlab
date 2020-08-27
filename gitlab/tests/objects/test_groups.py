"""
GitLab API: https://docs.gitlab.com/ce/api/groups.html
"""

import pytest
import responses

import gitlab


@pytest.fixture
def resp_groups():
    content = {"name": "name", "id": 1, "path": "path"}

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_import(accepted_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/import",
            json=accepted_content,
            content_type="application/json",
            status=202,
        )
        yield rsps


def test_get_group(gl, resp_groups):
    data = gl.groups.get(1)
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == "name"
    assert data.path == "path"
    assert data.id == 1


def test_create_group(gl, resp_groups):
    name, path = "name", "path"
    data = gl.groups.create({"name": name, "path": path})
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == name
    assert data.path == path


def test_create_group_export(group, resp_export):
    export = group.exports.create()
    assert export.message == "202 Accepted"


@pytest.mark.skip("GitLab API endpoint not implemented")
def test_refresh_group_export_status(group, resp_export):
    export = group.exports.create()
    export.refresh()
    assert export.export_status == "finished"


def test_download_group_export(group, resp_export, binary_content):
    export = group.exports.create()
    download = export.download()
    assert isinstance(download, bytes)
    assert download == binary_content


def test_import_group(gl, resp_create_import):
    group_import = gl.groups.import_group("file", "api-group", "API Group")
    assert group_import["message"] == "202 Accepted"


@pytest.mark.skip("GitLab API endpoint not implemented")
def test_refresh_group_import_status(group, resp_groups):
    group_import = group.imports.get()
    group_import.refresh()
    assert group_import.import_status == "finished"
