import unittest

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


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.gl = gitlab.Gitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version=4,
        )

    @with_httmock(resp_get_group)
    def test_get_group(self):
        data = self.gl.groups.get(1)
        self.assertIsInstance(data, gitlab.v4.objects.Group)
        self.assertEqual(data.name, "name")
        self.assertEqual(data.path, "path")
        self.assertEqual(data.id, 1)

    @with_httmock(resp_create_group)
    def test_create_group(self):
        name, path = "name", "path"
        data = self.gl.groups.create({"name": name, "path": path})
        self.assertIsInstance(data, gitlab.v4.objects.Group)
        self.assertEqual(data.name, name)
        self.assertEqual(data.path, path)


class TestGroupExport(TestGroup):
    def setUp(self):
        super(TestGroupExport, self).setUp()
        self.group = self.gl.groups.get(1, lazy=True)

    @with_httmock(resp_create_export)
    def test_create_group_export(self):
        export = self.group.exports.create()
        self.assertEqual(export.message, "202 Accepted")

    @unittest.skip("GitLab API endpoint not implemented")
    @with_httmock(resp_create_export)
    def test_refresh_group_export_status(self):
        export = self.group.exports.create()
        export.refresh()
        self.assertEqual(export.export_status, "finished")

    @with_httmock(resp_create_export, resp_download_export)
    def test_download_group_export(self):
        export = self.group.exports.create()
        download = export.download()
        self.assertIsInstance(download, bytes)
        self.assertEqual(download, binary_content)


class TestGroupImport(TestGroup):
    @with_httmock(resp_create_import)
    def test_import_group(self):
        group_import = self.gl.groups.import_group("file", "api-group", "API Group")
        self.assertEqual(group_import["message"], "202 Accepted")

    @unittest.skip("GitLab API endpoint not implemented")
    @with_httmock(resp_create_import)
    def test_refresh_group_import_status(self):
        group_import = self.group.imports.get()
        group_import.refresh()
        self.assertEqual(group_import.import_status, "finished")
