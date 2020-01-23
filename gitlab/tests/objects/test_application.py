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


class TestApplicationAppearance(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version="4",
        )
        self.title = "GitLab Test Instance"
        self.new_title = "new-title"
        self.description = "gitlab-test.example.com"
        self.new_description = "new-description"

    def test_get_update_appearance(self):
        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/application/appearance",
            method="get",
        )
        def resp_get_appearance(url, request):
            content = """{
            "title": "%s",
            "description": "%s",
            "logo": "/uploads/-/system/appearance/logo/1/logo.png",
            "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
            "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
            "new_project_guidelines": "Please read the FAQs for help.",
            "header_message": "",
            "footer_message": "",
            "message_background_color": "#e75e40",
            "message_font_color": "#ffffff",
            "email_header_and_footer_enabled": false}""" % (
                self.title,
                self.description,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/application/appearance",
            method="put",
        )
        def resp_update_appearance(url, request):
            content = """{
            "title": "%s",
            "description": "%s",
            "logo": "/uploads/-/system/appearance/logo/1/logo.png",
            "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
            "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
            "new_project_guidelines": "Please read the FAQs for help.",
            "header_message": "",
            "footer_message": "",
            "message_background_color": "#e75e40",
            "message_font_color": "#ffffff",
            "email_header_and_footer_enabled": false}""" % (
                self.new_title,
                self.new_description,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        with HTTMock(resp_get_appearance), HTTMock(resp_update_appearance):
            appearance = self.gl.appearance.get()
            self.assertEqual(appearance.title, self.title)
            self.assertEqual(appearance.description, self.description)
            appearance.title = self.new_title
            appearance.description = self.new_description
            appearance.save()
            self.assertEqual(appearance.title, self.new_title)
            self.assertEqual(appearance.description, self.new_description)

    def test_update_appearance(self):
        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/application/appearance",
            method="put",
        )
        def resp_update_appearance(url, request):
            content = """{
            "title": "%s",
            "description": "%s",
            "logo": "/uploads/-/system/appearance/logo/1/logo.png",
            "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
            "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
            "new_project_guidelines": "Please read the FAQs for help.",
            "header_message": "",
            "footer_message": "",
            "message_background_color": "#e75e40",
            "message_font_color": "#ffffff",
            "email_header_and_footer_enabled": false}""" % (
                self.new_title,
                self.new_description,
            )
            content = content.encode("utf-8")
            return response(200, content, headers, None, 25, request)

        with HTTMock(resp_update_appearance):
            resp = self.gl.appearance.update(
                title=self.new_title, description=self.new_description
            )
