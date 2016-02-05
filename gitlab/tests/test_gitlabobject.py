#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Mika Mäenpää <mika.j.maenpaa@tut.fi>
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
from __future__ import division
from __future__ import absolute_import

import json
try:
    import unittest
except ImportError:
    import unittest2 as unittest

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

from gitlab import *  # noqa


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects/1",
          method="get")
def resp_get_project(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"name": "name", "id": 1}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects",
          method="get")
def resp_list_project(url, request):
    headers = {'content-type': 'application/json'}
    content = '[{"name": "name", "id": 1}]'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/issues/1",
          method="get")
def resp_get_issue(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"name": "name", "id": 1}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/users/1",
          method="put")
def resp_update_user(url, request):
    headers = {'content-type': 'application/json'}
    content = ('{"name": "newname", "id": 1, "password": "password", '
               '"username": "username", "email": "email"}').encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects",
          method="post")
def resp_create_project(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"name": "testname", "id": 1}'.encode("utf-8")
    return response(201, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/2/members",
          method="post")
def resp_create_groupmember(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"access_level": 50, "id": 3}'.encode("utf-8")
    return response(201, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/projects/2/snippets/3", method="get")
def resp_get_projectsnippet(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"title": "test", "id": 3}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups/1",
          method="delete")
def resp_delete_group(url, request):
    headers = {'content-type': 'application/json'}
    content = ''.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/groups/2/projects/3",
          method="post")
def resp_transfer_project(url, request):
    headers = {'content-type': 'application/json'}
    content = ''.encode("utf-8")
    return response(201, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/groups/2/projects/3",
          method="post")
def resp_transfer_project_fail(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"message": "messagecontent"}'.encode("utf-8")
    return response(400, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/projects/2/repository/branches/branchname/protect",
          method="put")
def resp_protect_branch(url, request):
    headers = {'content-type': 'application/json'}
    content = ''.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/projects/2/repository/branches/branchname/unprotect",
          method="put")
def resp_unprotect_branch(url, request):
    headers = {'content-type': 'application/json'}
    content = ''.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost",
          path="/api/v3/projects/2/repository/branches/branchname/protect",
          method="put")
def resp_protect_branch_fail(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"message": "messagecontent"}'.encode("utf-8")
    return response(400, content, headers, None, 5, request)


class TestGitlabObject(unittest.TestCase):

    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)

    def test_json(self):
        gl_object = CurrentUser(self.gl, data={"username": "testname"})
        json_str = gl_object.json()
        data = json.loads(json_str)
        self.assertIn("id", data)
        self.assertEqual(data["username"], "testname")
        self.assertEqual(data["gitlab"]["url"], "http://localhost/api/v3")

    def test_data_for_gitlab(self):
        class FakeObj1(GitlabObject):
            _url = '/fake1'
            requiredCreateAttrs = ['create_req']
            optionalCreateAttrs = ['create_opt']
            requiredUpdateAttrs = ['update_req']
            optionalUpdateAttrs = ['update_opt']

        class FakeObj2(GitlabObject):
            _url = '/fake2'
            requiredCreateAttrs = ['create_req']
            optionalCreateAttrs = ['create_opt']

        obj1 = FakeObj1(self.gl, {'update_req': 1, 'update_opt': 1,
                                  'create_req': 1, 'create_opt': 1})
        obj2 = FakeObj2(self.gl, {'create_req': 1, 'create_opt': 1})

        obj1_data = json.loads(obj1._data_for_gitlab())
        self.assertIn('create_req', obj1_data)
        self.assertIn('create_opt', obj1_data)
        self.assertNotIn('update_req', obj1_data)
        self.assertNotIn('update_opt', obj1_data)
        self.assertNotIn('gitlab', obj1_data)

        obj1_data = json.loads(obj1._data_for_gitlab(update=True))
        self.assertNotIn('create_req', obj1_data)
        self.assertNotIn('create_opt', obj1_data)
        self.assertIn('update_req', obj1_data)
        self.assertIn('update_opt', obj1_data)

        obj1_data = json.loads(obj1._data_for_gitlab(
            extra_parameters={'foo': 'bar'}))
        self.assertIn('foo', obj1_data)
        self.assertEqual(obj1_data['foo'], 'bar')

        obj2_data = json.loads(obj2._data_for_gitlab(update=True))
        self.assertIn('create_req', obj2_data)
        self.assertIn('create_opt', obj2_data)

    def test_list_not_implemented(self):
        self.assertRaises(NotImplementedError, CurrentUser.list, self.gl)

    def test_list(self):
        with HTTMock(resp_list_project):
            data = Project.list(self.gl, id=1)
            self.assertEqual(type(data), list)
            self.assertEqual(len(data), 1)
            self.assertEqual(type(data[0]), Project)
            self.assertEqual(data[0].name, "name")
            self.assertEqual(data[0].id, 1)

    def test_get_list_or_object_with_list(self):
        with HTTMock(resp_list_project):
            gl_object = Project(self.gl, data={"name": "name"})
            data = gl_object._get_list_or_object(self.gl, id=None)
            self.assertEqual(type(data), list)
            self.assertEqual(len(data), 1)
            self.assertEqual(type(data[0]), Project)
            self.assertEqual(data[0].name, "name")
            self.assertEqual(data[0].id, 1)

    def test_get_list_or_object_with_get(self):
        with HTTMock(resp_get_project):
            gl_object = Project(self.gl, data={"name": "name"})
            data = gl_object._get_list_or_object(self.gl, id=1)
            self.assertEqual(type(data), Project)
            self.assertEqual(data.name, "name")
            self.assertEqual(data.id, 1)

    def test_get_list_or_object_cant_get(self):
        with HTTMock(resp_get_issue):
            gl_object = UserProject(self.gl, data={"name": "name"})
            self.assertRaises(NotImplementedError,
                              gl_object._get_list_or_object,
                              self.gl, id=1)

    def test_get_list_or_object_cantlist(self):
        gl_object = CurrentUser(self.gl, data={"name": "name"})
        self.assertRaises(NotImplementedError, gl_object._get_list_or_object,
                          self.gl, id=None)

    def test_get_list_or_object_create(self):
        data = {"name": "name"}
        gl_object = Project(self.gl, data=data)
        data = gl_object._get_list_or_object(Project, id=data)
        self.assertEqual(type(data), Project)
        self.assertEqual(data.name, "name")

    def test_create_cantcreate(self):
        gl_object = CurrentUser(self.gl, data={"username": "testname"})
        self.assertRaises(NotImplementedError, gl_object._create)

    def test_create(self):
        obj = Project(self.gl, data={"name": "testname"})
        with HTTMock(resp_create_project):
            obj._create()
            self.assertEqual(obj.id, 1)

    def test_create_with_kw(self):
        obj = GroupMember(self.gl, data={"access_level": 50, "user_id": 3},
                          group_id=2)
        with HTTMock(resp_create_groupmember):
            obj._create()
            self.assertEqual(obj.id, 3)
            self.assertEqual(obj.group_id, 2)
            self.assertEqual(obj.user_id, 3)
            self.assertEqual(obj.access_level, 50)

    def test_get_with_kw(self):
        with HTTMock(resp_get_projectsnippet):
            obj = ProjectSnippet(self.gl, data=3, project_id=2)
        self.assertEqual(obj.id, 3)
        self.assertEqual(obj.project_id, 2)
        self.assertEqual(obj.title, "test")

    def test_create_cantupdate(self):
        gl_object = CurrentUser(self.gl, data={"username": "testname"})
        self.assertRaises(NotImplementedError, gl_object._update)

    def test_update(self):
        obj = User(self.gl, data={"name": "testname", "email": "email",
                                  "password": "password", "id": 1,
                                  "username": "username"})
        self.assertEqual(obj.name, "testname")
        obj.name = "newname"
        with HTTMock(resp_update_user):
            obj._update()
            self.assertEqual(obj.name, "newname")

    def test_save_with_id(self):
        obj = User(self.gl, data={"name": "testname", "email": "email",
                                  "password": "password", "id": 1,
                                  "username": "username"})
        self.assertEqual(obj.name, "testname")
        obj._from_api = True
        obj.name = "newname"
        with HTTMock(resp_update_user):
            obj.save()
            self.assertEqual(obj.name, "newname")

    def test_save_without_id(self):
        obj = Project(self.gl, data={"name": "testname"})
        with HTTMock(resp_create_project):
            obj.save()
            self.assertEqual(obj.id, 1)

    def test_delete(self):
        obj = Group(self.gl, data={"name": "testname", "id": 1})
        obj._from_api = True
        with HTTMock(resp_delete_group):
            data = obj.delete()
            self.assertIs(data, True)

    def test_delete_with_no_id(self):
        obj = Group(self.gl, data={"name": "testname"})
        self.assertRaises(GitlabDeleteError, obj.delete)

    def test_delete_cant_delete(self):
        obj = CurrentUser(self.gl, data={"name": "testname", "id": 1})
        self.assertRaises(NotImplementedError, obj.delete)

    def test_set_from_dict_BooleanTrue(self):
        obj = Project(self.gl, data={"name": "testname"})
        data = {"issues_enabled": True}
        obj._set_from_dict(data)
        self.assertIs(obj.issues_enabled, True)

    def test_set_from_dict_BooleanFalse(self):
        obj = Project(self.gl, data={"name": "testname"})
        data = {"issues_enabled": False}
        obj._set_from_dict(data)
        self.assertIs(obj.issues_enabled, False)

    def test_set_from_dict_None(self):
        obj = Project(self.gl, data={"name": "testname"})
        data = {"issues_enabled": None}
        obj._set_from_dict(data)
        self.assertIsNone(obj.issues_enabled)


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)

    def test_transfer_project(self):
        obj = Group(self.gl, data={"name": "testname", "path": "testpath",
                                   "id": 2})
        with HTTMock(resp_transfer_project):
            obj.transfer_project(3)

    def test_transfer_project_fail(self):
        obj = Group(self.gl, data={"name": "testname", "path": "testpath",
                                   "id": 2})
        with HTTMock(resp_transfer_project_fail):
            self.assertRaises(GitlabTransferProjectError,
                              obj.transfer_project, 3)


class TestProjectBranch(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)
        self.obj = ProjectBranch(self.gl, data={"name": "branchname",
                                                "ref": "ref_name", "id": 3,
                                                "project_id": 2})

    def test_protect(self):
        self.assertRaises(AttributeError, getattr, self.obj, 'protected')
        with HTTMock(resp_protect_branch):
            self.obj.protect(True)
            self.assertIs(self.obj.protected, True)

    def test_protect_unprotect(self):
        self.obj.protected = True
        with HTTMock(resp_unprotect_branch):
            self.obj.protect(False)
            self.assertRaises(AttributeError, getattr, self.obj, 'protected')

    def test_protect_unprotect_again(self):
        self.assertRaises(AttributeError, getattr, self.obj, 'protected')
        with HTTMock(resp_protect_branch):
            self.obj.protect(True)
            self.assertIs(self.obj.protected, True)
        self.assertEqual(True, self.obj.protected)
        with HTTMock(resp_unprotect_branch):
            self.obj.protect(False)
            self.assertRaises(AttributeError, getattr, self.obj, 'protected')

    def test_protect_protect_fail(self):
        with HTTMock(resp_protect_branch_fail):
            self.assertRaises(GitlabProtectError, self.obj.protect)

    def test_unprotect(self):
        self.obj.protected = True
        with HTTMock(resp_unprotect_branch):
            self.obj.unprotect()
            self.assertRaises(AttributeError, getattr, self.obj, 'protected')


class TestProjectCommit(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)
        self.obj = ProjectCommit(self.gl, data={"id": 3, "project_id": 2})

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/repository/commits/3/diff",
              method="get")
    def resp_diff(self, url, request):
        headers = {'content-type': 'application/json'}
        content = '{"json": 2 }'.encode("utf-8")
        return response(200, content, headers, None, 5, request)

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/repository/commits/3/diff",
              method="get")
    def resp_diff_fail(self, url, request):
        headers = {'content-type': 'application/json'}
        content = '{"message": "messagecontent" }'.encode("utf-8")
        return response(400, content, headers, None, 5, request)

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/repository/blobs/3",
              method="get")
    def resp_blob(self, url, request):
        headers = {'content-type': 'application/json'}
        content = 'blob'.encode("utf-8")
        return response(200, content, headers, None, 5, request)

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/repository/blobs/3",
              method="get")
    def resp_blob_fail(self, url, request):
        headers = {'content-type': 'application/json'}
        content = '{"message": "messagecontent" }'.encode("utf-8")
        return response(400, content, headers, None, 5, request)

    def test_diff(self):
        with HTTMock(self.resp_diff):
            data = {"json": 2}
            diff = self.obj.diff()
            self.assertEqual(diff, data)

    def test_diff_fail(self):
        with HTTMock(self.resp_diff_fail):
            self.assertRaises(GitlabGetError, self.obj.diff)

    def test_blob(self):
        with HTTMock(self.resp_blob):
            blob = self.obj.blob("testing")
            self.assertEqual(blob, b'blob')

    def test_blob_fail(self):
        with HTTMock(self.resp_blob_fail):
            self.assertRaises(GitlabGetError, self.obj.blob, "testing")


class TestProjectSnippet(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         email="testuser@test.com", password="testpassword",
                         ssl_verify=True)
        self.obj = ProjectSnippet(self.gl, data={"id": 3, "project_id": 2})

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/snippets/3/raw",
              method="get")
    def resp_content(self, url, request):
        headers = {'content-type': 'application/json'}
        content = 'content'.encode("utf-8")
        return response(200, content, headers, None, 5, request)

    @urlmatch(scheme="http", netloc="localhost",
              path="/api/v3/projects/2/snippets/3/raw",
              method="get")
    def resp_content_fail(self, url, request):
        headers = {'content-type': 'application/json'}
        content = '{"message": "messagecontent" }'.encode("utf-8")
        return response(400, content, headers, None, 5, request)

    def test_content(self):
        with HTTMock(self.resp_content):
            data = b'content'
            content = self.obj.Content()
            self.assertEqual(content, data)

    def test_blob_fail(self):
        with HTTMock(self.resp_content_fail):
            self.assertRaises(GitlabGetError, self.obj.Content)
