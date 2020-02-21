# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Mika Mäenpää <mika.j.maenpaa@tut.fi>,
#                    Tampere University of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
import pickle
import tempfile
import unittest

import httpx
from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

import gitlab
from gitlab import *  # noqa
from gitlab.v4.objects import *  # noqa

valid_config = b"""[global]
default = one
ssl_verify = true
timeout = 2

[one]
url = http://one.url
private_token = ABCDEF
"""


class TestSanitize(unittest.TestCase):
    def test_do_nothing(self):
        self.assertEqual(1, gitlab._sanitize(1))
        self.assertEqual(1.5, gitlab._sanitize(1.5))
        self.assertEqual("foo", gitlab._sanitize("foo"))

    def test_slash(self):
        self.assertEqual("foo%2Fbar", gitlab._sanitize("foo/bar"))

    def test_dict(self):
        source = {"url": "foo/bar", "id": 1}
        expected = {"url": "foo%2Fbar", "id": 1}
        self.assertEqual(expected, gitlab._sanitize(source))


class TestGitlabHttpMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(
            "http://localhost", private_token="private_token", api_version=4
        )

    def test_build_url(self):
        r = self.gl._build_url("http://localhost/api/v4")
        self.assertEqual(r, "http://localhost/api/v4")
        r = self.gl._build_url("https://localhost/api/v4")
        self.assertEqual(r, "https://localhost/api/v4")
        r = self.gl._build_url("/projects")
        self.assertEqual(r, "http://localhost/api/v4/projects")


class TestGitlabAuth(unittest.TestCase):
    def test_invalid_auth_args(self):
        self.assertRaises(
            ValueError,
            Gitlab,
            "http://localhost",
            api_version="4",
            private_token="private_token",
            oauth_token="bearer",
        )
        self.assertRaises(
            ValueError,
            Gitlab,
            "http://localhost",
            api_version="4",
            oauth_token="bearer",
            http_username="foo",
            http_password="bar",
        )
        self.assertRaises(
            ValueError,
            Gitlab,
            "http://localhost",
            api_version="4",
            private_token="private_token",
            http_password="bar",
        )
        self.assertRaises(
            ValueError,
            Gitlab,
            "http://localhost",
            api_version="4",
            private_token="private_token",
            http_username="foo",
        )

    def test_private_token_auth(self):
        gl = Gitlab("http://localhost", private_token="private_token", api_version="4")
        self.assertEqual(gl.private_token, "private_token")
        self.assertEqual(gl.oauth_token, None)
        self.assertEqual(gl.job_token, None)
        self.assertEqual(gl.client.auth, None)
        self.assertNotIn("Authorization", gl.headers)
        self.assertEqual(gl.headers["PRIVATE-TOKEN"], "private_token")
        self.assertNotIn("JOB-TOKEN", gl.headers)

    def test_oauth_token_auth(self):
        gl = Gitlab("http://localhost", oauth_token="oauth_token", api_version="4")
        self.assertEqual(gl.private_token, None)
        self.assertEqual(gl.oauth_token, "oauth_token")
        self.assertEqual(gl.job_token, None)
        self.assertEqual(gl.client.auth, None)
        self.assertEqual(gl.headers["Authorization"], "Bearer oauth_token")
        self.assertNotIn("PRIVATE-TOKEN", gl.headers)
        self.assertNotIn("JOB-TOKEN", gl.headers)

    def test_job_token_auth(self):
        gl = Gitlab("http://localhost", job_token="CI_JOB_TOKEN", api_version="4")
        self.assertEqual(gl.private_token, None)
        self.assertEqual(gl.oauth_token, None)
        self.assertEqual(gl.job_token, "CI_JOB_TOKEN")
        self.assertEqual(gl.client.auth, None)
        self.assertNotIn("Authorization", gl.headers)
        self.assertNotIn("PRIVATE-TOKEN", gl.headers)
        self.assertEqual(gl.headers["JOB-TOKEN"], "CI_JOB_TOKEN")

    def test_http_auth(self):
        gl = Gitlab(
            "http://localhost",
            private_token="private_token",
            http_username="foo",
            http_password="bar",
            api_version="4",
        )
        self.assertEqual(gl.private_token, "private_token")
        self.assertEqual(gl.oauth_token, None)
        self.assertEqual(gl.job_token, None)
        self.assertIsInstance(gl.client.auth, httpx.auth.BasicAuth)
        self.assertEqual(gl.headers["PRIVATE-TOKEN"], "private_token")
        self.assertNotIn("Authorization", gl.headers)


class TestGitlab(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version=4,
        )

    def _default_config(self):
        fd, temp_path = tempfile.mkstemp()
        os.write(fd, valid_config)
        os.close(fd)
        return temp_path

    def test_from_config(self):
        config_path = self._default_config()
        gitlab.Gitlab.from_config("one", [config_path])
        os.unlink(config_path)

    def test_subclass_from_config(self):
        class MyGitlab(gitlab.Gitlab):
            pass

        config_path = self._default_config()
        gl = MyGitlab.from_config("one", [config_path])
        self.assertIsInstance(gl, MyGitlab)
        os.unlink(config_path)
