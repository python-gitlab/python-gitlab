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

from __future__ import print_function

import os
import pickle
import tempfile
try:
    import unittest
except ImportError:
    import unittest2 as unittest

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa
import requests

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


class TestGitlabList(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         api_version=4)

    def test_build_list(self):
        @urlmatch(scheme='http', netloc="localhost", path="/api/v4/tests",
                  method="get")
        def resp_1(url, request):
            headers = {'content-type': 'application/json',
                       'X-Page': 1,
                       'X-Next-Page': 2,
                       'X-Per-Page': 1,
                       'X-Total-Pages': 2,
                       'X-Total': 2,
                       'Link': (
                           '<http://localhost/api/v4/tests?per_page=1&page=2>;'
                           ' rel="next"')}
            content = '[{"a": "b"}]'
            return response(200, content, headers, None, 5, request)

        @urlmatch(scheme='http', netloc="localhost", path="/api/v4/tests",
                  method='get', query=r'.*page=2')
        def resp_2(url, request):
            headers = {'content-type': 'application/json',
                       'X-Page': 2,
                       'X-Next-Page': 2,
                       'X-Per-Page': 1,
                       'X-Total-Pages': 2,
                       'X-Total': 2}
            content = '[{"c": "d"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_1):
            obj = self.gl.http_list('/tests', as_list=False)
            self.assertEqual(len(obj), 2)
            self.assertEqual(obj._next_url,
                             'http://localhost/api/v4/tests?per_page=1&page=2')
            self.assertEqual(obj.current_page, 1)
            self.assertEqual(obj.prev_page, None)
            self.assertEqual(obj.next_page, 2)
            self.assertEqual(obj.per_page, 1)
            self.assertEqual(obj.total_pages, 2)
            self.assertEqual(obj.total, 2)

            with HTTMock(resp_2):
                l = list(obj)
                self.assertEqual(len(l), 2)
                self.assertEqual(l[0]['a'], 'b')
                self.assertEqual(l[1]['c'], 'd')


class TestGitlabHttpMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         api_version=4)

    def test_build_url(self):
        r = self.gl._build_url('http://localhost/api/v4')
        self.assertEqual(r, 'http://localhost/api/v4')
        r = self.gl._build_url('https://localhost/api/v4')
        self.assertEqual(r, 'https://localhost/api/v4')
        r = self.gl._build_url('/projects')
        self.assertEqual(r, 'http://localhost/api/v4/projects')

    def test_http_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '[{"name": "project1"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            http_r = self.gl.http_request('get', '/projects')
            http_r.json()
            self.assertEqual(http_r.status_code, 200)

    def test_http_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="get")
        def resp_cont(url, request):
            content = {'Here is wh it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError,
                              self.gl.http_request,
                              'get', '/not_there')

    def test_get_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "project1"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_get('/projects')
            self.assertIsInstance(result, dict)
            self.assertEqual(result['name'], 'project1')

    def test_get_request_raw(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/octet-stream'}
            content = 'content'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_get('/projects')
            self.assertEqual(result.content.decode('utf-8'), 'content')

    def test_get_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="get")
        def resp_cont(url, request):
            content = {'Here is wh it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl.http_get, '/not_there')

    def test_get_request_invalid_data(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '["name": "project1"]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabParsingError, self.gl.http_get,
                              '/projects')

    def test_list_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json', 'X-Total': 1}
            content = '[{"name": "project1"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_list('/projects', as_list=True)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)

        with HTTMock(resp_cont):
            result = self.gl.http_list('/projects', as_list=False)
            self.assertIsInstance(result, GitlabList)
            self.assertEqual(len(result), 1)

        with HTTMock(resp_cont):
            result = self.gl.http_list('/projects', all=True)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)

    def test_list_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="get")
        def resp_cont(url, request):
            content = {'Here is why it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl.http_list, '/not_there')

    def test_list_request_invalid_data(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '["name": "project1"]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabParsingError, self.gl.http_list,
                              '/projects')

    def test_post_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "project1"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_post('/projects')
            self.assertIsInstance(result, dict)
            self.assertEqual(result['name'], 'project1')

    def test_post_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="post")
        def resp_cont(url, request):
            content = {'Here is wh it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl.http_post, '/not_there')

    def test_post_request_invalid_data(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '["name": "project1"]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabParsingError, self.gl.http_post,
                              '/projects')

    def test_put_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "project1"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_put('/projects')
            self.assertIsInstance(result, dict)
            self.assertEqual(result['name'], 'project1')

    def test_put_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="put")
        def resp_cont(url, request):
            content = {'Here is wh it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl.http_put, '/not_there')

    def test_put_request_invalid_data(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="put")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '["name": "project1"]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabParsingError, self.gl.http_put,
                              '/projects')

    def test_delete_request(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects",
                  method="delete")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = 'true'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            result = self.gl.http_delete('/projects')
            self.assertIsInstance(result, requests.Response)
            self.assertEqual(result.json(), True)

    def test_delete_request_404(self):
        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v4/not_there", method="delete")
        def resp_cont(url, request):
            content = {'Here is wh it failed'}
            return response(404, content, {}, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl.http_delete,
                              '/not_there')


class TestGitlabAuth(unittest.TestCase):
    def test_invalid_auth_args(self):
        self.assertRaises(ValueError,
                          Gitlab,
                          "http://localhost", api_version='4',
                          private_token='private_token', oauth_token='bearer')
        self.assertRaises(ValueError,
                          Gitlab,
                          "http://localhost", api_version='4',
                          oauth_token='bearer', http_username='foo',
                          http_password='bar')
        self.assertRaises(ValueError,
                          Gitlab,
                          "http://localhost", api_version='4',
                          private_token='private_token', http_password='bar')
        self.assertRaises(ValueError,
                          Gitlab,
                          "http://localhost", api_version='4',
                          private_token='private_token', http_username='foo')

    def test_private_token_auth(self):
        gl = Gitlab('http://localhost', private_token='private_token',
                    api_version='4')
        self.assertEqual(gl.private_token, 'private_token')
        self.assertEqual(gl.oauth_token, None)
        self.assertEqual(gl._http_auth, None)
        self.assertEqual(gl.headers['PRIVATE-TOKEN'], 'private_token')
        self.assertNotIn('Authorization', gl.headers)

    def test_oauth_token_auth(self):
        gl = Gitlab('http://localhost', oauth_token='oauth_token',
                    api_version='4')
        self.assertEqual(gl.private_token, None)
        self.assertEqual(gl.oauth_token, 'oauth_token')
        self.assertEqual(gl._http_auth, None)
        self.assertEqual(gl.headers['Authorization'], 'Bearer oauth_token')
        self.assertNotIn('PRIVATE-TOKEN', gl.headers)

    def test_http_auth(self):
        gl = Gitlab('http://localhost', private_token='private_token',
                    http_username='foo', http_password='bar', api_version='4')
        self.assertEqual(gl.private_token, 'private_token')
        self.assertEqual(gl.oauth_token, None)
        self.assertIsInstance(gl._http_auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(gl.headers['PRIVATE-TOKEN'], 'private_token')
        self.assertNotIn('Authorization', gl.headers)


class TestGitlab(unittest.TestCase):

    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True, api_version=4)

    def test_pickability(self):
        original_gl_objects = self.gl._objects
        pickled = pickle.dumps(self.gl)
        unpickled = pickle.loads(pickled)
        self.assertIsInstance(unpickled, Gitlab)
        self.assertTrue(hasattr(unpickled, '_objects'))
        self.assertEqual(unpickled._objects, original_gl_objects)

    def test_credentials_auth_nopassword(self):
        self.gl.email = None
        self.gl.password = None

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/session",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl._credentials_auth)

    def test_credentials_auth_notok(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/session",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"message": "message"}'.encode("utf-8")
            return response(404, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            self.assertRaises(GitlabHttpError, self.gl._credentials_auth)

    def test_auth_with_credentials(self):
        self.gl.private_token = None
        self.test_credentials_auth(callback=self.gl.auth)

    def test_auth_with_token(self):
        self.test_token_auth(callback=self.gl.auth)

    def test_credentials_auth(self, callback=None):
        if callback is None:
            callback = self.gl._credentials_auth
        token = "credauthtoken"
        id_ = 1
        expected = {"PRIVATE-TOKEN": token}

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/session",
                  method="post")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{{"id": {0:d}, "private_token": "{1:s}"}}'.format(
                id_, token).encode("utf-8")
            return response(201, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            callback()
        self.assertEqual(self.gl.private_token, token)
        self.assertDictEqual(expected, self.gl.headers)
        self.assertEqual(self.gl.user.id, id_)

    def test_token_auth(self, callback=None):
        if callback is None:
            callback = self.gl._token_auth
        name = "username"
        id_ = 1

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/user",
                  method="get")
        def resp_cont(url, request):
            headers = {'content-type': 'application/json'}
            content = '{{"id": {0:d}, "username": "{1:s}"}}'.format(
                id_, name).encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            callback()
        self.assertEqual(self.gl.user.username, name)
        self.assertEqual(self.gl.user.id, id_)
        self.assertEqual(type(self.gl.user), CurrentUser)

    def test_hooks(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/hooks/1",
                  method="get")
        def resp_get_hook(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"url": "testurl", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_hook):
            data = self.gl.hooks.get(1)
            self.assertEqual(type(data), Hook)
            self.assertEqual(data.url, "testurl")
            self.assertEqual(data.id, 1)

    def test_projects(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects/1",
                  method="get")
        def resp_get_project(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_project):
            data = self.gl.projects.get(1)
            self.assertEqual(type(data), Project)
            self.assertEqual(data.name, "name")
            self.assertEqual(data.id, 1)

    def test_groups(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/groups/1",
                  method="get")
        def resp_get_group(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"name": "name", "id": 1, "path": "path"}'
            content = content.encode('utf-8')
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_group):
            data = self.gl.groups.get(1)
            self.assertEqual(type(data), Group)
            self.assertEqual(data.name, "name")
            self.assertEqual(data.path, "path")
            self.assertEqual(data.id, 1)

    def test_issues(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/issues",
                  method="get")
        def resp_get_issue(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "name", "id": 1}, '
                       '{"name": "other_name", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_issue):
            data = self.gl.issues.list()
            self.assertEqual(data[1].id, 2)
            self.assertEqual(data[1].name, 'other_name')

    def test_users(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/users/1",
                  method="get")
        def resp_get_user(url, request):
            headers = {'content-type': 'application/json'}
            content = ('{"name": "name", "id": 1, "password": "password", '
                       '"username": "username", "email": "email"}')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_user):
            user = self.gl.users.get(1)
            self.assertEqual(type(user), User)
            self.assertEqual(user.name, "name")
            self.assertEqual(user.id, 1)

    def _default_config(self):
        fd, temp_path = tempfile.mkstemp()
        os.write(fd, valid_config)
        os.close(fd)
        return temp_path

    def test_from_config(self):
        config_path = self._default_config()
        gitlab.Gitlab.from_config('one', [config_path])
        os.unlink(config_path)

    def test_subclass_from_config(self):
        class MyGitlab(gitlab.Gitlab):
            pass
        config_path = self._default_config()
        gl = MyGitlab.from_config('one', [config_path])
        self.assertEqual(type(gl).__name__, 'MyGitlab')
        os.unlink(config_path)
