"""
GitLab API: https://docs.gitlab.com/ce/api/project_import_export.html
"""

from httmock import response, urlmatch, with_httmock

from .mocks import *


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/1/export", method="get",
)
def resp_export_status(url, request):
    """Mock for Project Export GET response."""
    content = """{
      "id": 1,
      "description": "Itaque perspiciatis minima aspernatur",
      "name": "Gitlab Test",
      "name_with_namespace": "Gitlab Org / Gitlab Test",
      "path": "gitlab-test",
      "path_with_namespace": "gitlab-org/gitlab-test",
      "created_at": "2017-08-29T04:36:44.383Z",
      "export_status": "finished",
      "_links": {
        "api_url": "https://gitlab.test/api/v4/projects/1/export/download",
        "web_url": "https://gitlab.test/gitlab-test/download_export"
      }
    }
    """
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/import", method="post",
)
def resp_import_project(url, request):
    """Mock for Project Import POST response."""
    content = """{
      "id": 1,
      "description": null,
      "name": "api-project",
      "name_with_namespace": "Administrator / api-project",
      "path": "api-project",
      "path_with_namespace": "root/api-project",
      "created_at": "2018-02-13T09:05:58.023Z",
      "import_status": "scheduled"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/1/import", method="get",
)
def resp_import_status(url, request):
    """Mock for Project Import GET response."""
    content = """{
      "id": 1,
      "description": "Itaque perspiciatis minima aspernatur corporis consequatur.",
      "name": "Gitlab Test",
      "name_with_namespace": "Gitlab Org / Gitlab Test",
      "path": "gitlab-test",
      "path_with_namespace": "gitlab-org/gitlab-test",
      "created_at": "2017-08-29T04:36:44.383Z",
      "import_status": "finished"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/import/github", method="post",
)
def resp_import_github(url, request):
    """Mock for GitHub Project Import POST response."""
    content = """{
    "id": 27,
    "name": "my-repo",
    "full_path": "/root/my-repo",
    "full_name": "Administrator / my-repo"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@with_httmock(resp_import_project)
def test_import_project(gl):
    project_import = gl.projects.import_project("file", "api-project")
    assert project_import["import_status"] == "scheduled"


@with_httmock(resp_import_status)
def test_refresh_project_import_status(project):
    project_import = project.imports.get()
    project_import.refresh()
    assert project_import.import_status == "finished"


@with_httmock(resp_import_github)
def test_import_github(gl):
    base_path = "/root"
    name = "my-repo"
    ret = gl.projects.import_github("githubkey", 1234, base_path, name)
    assert isinstance(ret, dict)
    assert ret["name"] == name
    assert ret["full_path"] == "/".join((base_path, name))
    assert ret["full_name"].endswith(name)


@with_httmock(resp_create_export)
def test_create_project_export(project):
    export = project.exports.create()
    assert export.message == "202 Accepted"


@with_httmock(resp_create_export, resp_export_status)
def test_refresh_project_export_status(project):
    export = project.exports.create()
    export.refresh()
    assert export.export_status == "finished"


@with_httmock(resp_create_export, resp_download_export)
def test_download_project_export(project):
    export = project.exports.create()
    download = export.download()
    assert isinstance(download, bytes)
    assert download == binary_content
