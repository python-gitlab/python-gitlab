"""
GitLab API: https://docs.gitlab.com/ce/api/groups.html
"""

import pytest

from httmock import response, urlmatch, with_httmock

import gitlab
from .mocks import *  # noqa


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/groups/1", method="get")
def resp_get_group(url, request):
    content = '{"name": "name", "id": 1, "path": "path"}'
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/groups", method="post")
def resp_create_group(url, request):
    content = '{"name": "name", "id": 1, "path": "path"}'
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/groups/import", method="post",
)
def resp_create_import(url, request):
    """Mock for Group import tests.

    GitLab does not respond with import status for group imports.
    """

    content = """{
    "message": "202 Accepted"
    }"""
    content = content.encode("utf-8")
    return response(202, content, headers, None, 25, request)


@with_httmock(resp_get_group)
def test_get_group(gl):
    data = gl.groups.get(1)
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == "name"
    assert data.path == "path"
    assert data.id == 1


@with_httmock(resp_create_group)
def test_create_group(gl):
    name, path = "name", "path"
    data = gl.groups.create({"name": name, "path": path})
    assert isinstance(data, gitlab.v4.objects.Group)
    assert data.name == name
    assert data.path == path


@with_httmock(resp_create_export)
def test_create_group_export(group):
    export = group.exports.create()
    assert export.message == "202 Accepted"


@pytest.mark.skip("GitLab API endpoint not implemented")
@with_httmock(resp_create_export)
def test_refresh_group_export_status(group):
    export = group.exports.create()
    export.refresh()
    assert export.export_status == "finished"


@with_httmock(resp_create_export, resp_download_export)
def test_download_group_export(group):
    export = group.exports.create()
    download = export.download()
    assert isinstance(download, bytes)
    assert download == binary_content


@with_httmock(resp_create_import)
def test_import_group(gl):
    group_import = gl.groups.import_group("file", "api-group", "API Group")
    assert group_import["message"] == "202 Accepted"


@pytest.mark.skip("GitLab API endpoint not implemented")
@with_httmock(resp_create_import)
def test_refresh_group_import_status(group):
    group_import = group.imports.get()
    group_import.refresh()
    assert group_import.import_status == "finished"
