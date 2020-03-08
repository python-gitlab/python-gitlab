import unittest
import gitlab
import os
import pickle
import tempfile
import json
import unittest
import requests
from gitlab import *  # noqa
from gitlab.v4.objects import *  # noqa
from httmock import HTTMock, urlmatch, response, with_httmock  # noqa


headers = {"content-type": "application/json"}
binary_content = b"binary content"


class TestProject(unittest.TestCase):
    """Base class for GitLab Project tests"""

    def setUp(self):
        self.gl = Gitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version=4,
        )
        self.project = self.gl.projects.get(1, lazy=True)


class TestProjectSnippets(TestProject):
    def test_list_project_snippets(self):
        title = "Example Snippet Title"
        visibility = "private"

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/projects/1/snippets",
            method="get",
        )
        def resp_list_snippet(url, request):
            content = """[{
            "title": "%s",
            "description": "More verbose snippet description",
            "file_name": "example.txt",
            "content": "source code with multiple lines",
            "visibility": "%s"}]""" % (
                title,
                visibility,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        with HTTMock(resp_list_snippet):
            snippets = self.project.snippets.list()
            self.assertEqual(len(snippets), 1)
            self.assertEqual(snippets[0].title, title)
            self.assertEqual(snippets[0].visibility, visibility)

    def test_get_project_snippets(self):
        title = "Example Snippet Title"
        visibility = "private"

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/projects/1/snippets/1",
            method="get",
        )
        def resp_get_snippet(url, request):
            content = """{
            "title": "%s",
            "description": "More verbose snippet description",
            "file_name": "example.txt",
            "content": "source code with multiple lines",
            "visibility": "%s"}""" % (
                title,
                visibility,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        with HTTMock(resp_get_snippet):
            snippet = self.project.snippets.get(1)
            self.assertEqual(snippet.title, title)
            self.assertEqual(snippet.visibility, visibility)

    def test_create_update_project_snippets(self):
        title = "Example Snippet Title"
        visibility = "private"

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/projects/1/snippets",
            method="put",
        )
        def resp_update_snippet(url, request):
            content = """{
            "title": "%s",
            "description": "More verbose snippet description",
            "file_name": "example.txt",
            "content": "source code with multiple lines",
            "visibility": "%s"}""" % (
                title,
                visibility,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/projects/1/snippets",
            method="post",
        )
        def resp_create_snippet(url, request):
            content = """{
            "title": "%s",
            "description": "More verbose snippet description",
            "file_name": "example.txt",
            "content": "source code with multiple lines",
            "visibility": "%s"}""" % (
                title,
                visibility,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        with HTTMock(resp_create_snippet, resp_update_snippet):
            snippet = self.project.snippets.create(
                {
                    "title": title,
                    "file_name": title,
                    "content": title,
                    "visibility": visibility,
                }
            )
            self.assertEqual(snippet.title, title)
            self.assertEqual(snippet.visibility, visibility)
            title = "new-title"
            snippet.title = title
            snippet.save()
            self.assertEqual(snippet.title, title)
            self.assertEqual(snippet.visibility, visibility)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/1/export", method="post",
)
def resp_create_export(url, request):
    """Common mock for Project Export tests"""
    content = """{
    "message": "202 Accepted"
    }"""
    content = content.encode("utf-8")
    return response(202, content, headers, None, 25, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/1/export", method="get",
)
def resp_export_status(url, request):
    """mock for Project Export GET response"""
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
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/export/download",
    method="get",
)
def resp_download_export(url, request):
    headers = {"content-type": "application/octet-stream"}
    content = binary_content
    return response(200, content, headers, None, 25, request)


class TestProjectExport(TestProject):
    @with_httmock(resp_create_export)
    def test_create_project_export(self):
        export = self.project.exports.create()
        self.assertEqual(export.message, "202 Accepted")

    @with_httmock(resp_create_export, resp_export_status)
    def test_refresh_project_export_status(self):
        export = self.project.exports.create()
        export.refresh()
        self.assertEqual(export.export_status, "finished")

    @with_httmock(resp_create_export, resp_download_export)
    def test_download_project_export(self):
        export = self.project.exports.create()
        download = export.download()
        self.assertIsInstance(download, bytes)
        self.assertEqual(download, binary_content)
