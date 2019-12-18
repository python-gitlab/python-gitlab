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
from httmock import HTTMock, urlmatch, response  # noqa


headers = {"content-type": "application/json"}


class TestProjectSnippets(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version=4,
        )

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
            snippets = self.gl.projects.get(1, lazy=True).snippets.list()
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
            snippet = self.gl.projects.get(1, lazy=True).snippets.get(1)
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
            snippet = self.gl.projects.get(1, lazy=True).snippets.create(
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
