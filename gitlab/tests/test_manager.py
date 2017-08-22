# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

from gitlab import *  # noqa
from gitlab.v3.objects import BaseManager  # noqa


class FakeChildObject(GitlabObject):
    _url = "/fake/%(parent_id)s/fakechild"
    requiredCreateAttrs = ['name']
    requiredUrlAttrs = ['parent_id']


class FakeChildManager(BaseManager):
    obj_cls = FakeChildObject


class FakeObject(GitlabObject):
    _url = "/fake"
    requiredCreateAttrs = ['name']
    managers = [('children', FakeChildManager, [('parent_id', 'id')])]


class FakeObjectManager(BaseManager):
    obj_cls = FakeObject


class TestGitlabManager(unittest.TestCase):
    def setUp(self):
        self.gitlab = Gitlab("http://localhost", private_token="private_token",
                             email="testuser@test.com",
                             password="testpassword", ssl_verify=True)

    def test_set_parent_args(self):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/fake",
                  method="POST")
        def resp_create(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"id": 1, "name": "name"}'.encode("utf-8")
            return response(201, content, headers, None, 5, request)

        mgr = FakeChildManager(self.gitlab)
        args = mgr._set_parent_args(name="name")
        self.assertEqual(args, {"name": "name"})

        with HTTMock(resp_create):
            o = FakeObjectManager(self.gitlab).create({"name": "name"})
            args = o.children._set_parent_args(name="name")
            self.assertEqual(args, {"name": "name", "parent_id": 1})

    def test_constructor(self):
        self.assertRaises(AttributeError, BaseManager, self.gitlab)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/fake/1",
                  method="get")
        def resp_get(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"id": 1, "name": "fake_name"}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get):
            mgr = FakeObjectManager(self.gitlab)
            fake_obj = mgr.get(1)
            self.assertEqual(fake_obj.id, 1)
            self.assertEqual(fake_obj.name, "fake_name")
            self.assertEqual(mgr.gitlab, self.gitlab)
            self.assertEqual(mgr.args, [])
            self.assertEqual(mgr.parent, None)

            self.assertIsInstance(fake_obj.children, FakeChildManager)
            self.assertEqual(fake_obj.children.gitlab, self.gitlab)
            self.assertEqual(fake_obj.children.parent, fake_obj)
            self.assertEqual(len(fake_obj.children.args), 1)

            fake_child = fake_obj.children.get(1)
            self.assertEqual(fake_child.id, 1)
            self.assertEqual(fake_child.name, "fake_name")

    def test_get(self):
        mgr = FakeObjectManager(self.gitlab)
        FakeObject.canGet = False
        self.assertRaises(NotImplementedError, mgr.get, 1)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/fake/1",
                  method="get")
        def resp_get(url, request):
            headers = {'content-type': 'application/json'}
            content = '{"id": 1, "name": "fake_name"}'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get):
            FakeObject.canGet = True
            mgr = FakeObjectManager(self.gitlab)
            fake_obj = mgr.get(1)
            self.assertIsInstance(fake_obj, FakeObject)
            self.assertEqual(fake_obj.id, 1)
            self.assertEqual(fake_obj.name, "fake_name")

    def test_list(self):
        mgr = FakeObjectManager(self.gitlab)
        FakeObject.canList = False
        self.assertRaises(NotImplementedError, mgr.list)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/fake",
                  method="get")
        def resp_get(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"id": 1, "name": "fake_name1"},'
                       '{"id": 2, "name": "fake_name2"}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get):
            FakeObject.canList = True
            mgr = FakeObjectManager(self.gitlab)
            fake_list = mgr.list()
            self.assertEqual(len(fake_list), 2)
            self.assertIsInstance(fake_list[0], FakeObject)
            self.assertEqual(fake_list[0].id, 1)
            self.assertEqual(fake_list[0].name, "fake_name1")
            self.assertIsInstance(fake_list[1], FakeObject)
            self.assertEqual(fake_list[1].id, 2)
            self.assertEqual(fake_list[1].name, "fake_name2")

    def test_create(self):
        mgr = FakeObjectManager(self.gitlab)
        FakeObject.canCreate = False
        self.assertRaises(NotImplementedError, mgr.create, {'name': 'name'})

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/fake",
                  method="post")
        def resp_post(url, request):
            headers = {'content-type': 'application/json'}
            data = '{"name": "fake_name"}'
            content = '{"id": 1, "name": "fake_name"}'.encode("utf-8")
            return response(201, content, headers, data, 5, request)

        with HTTMock(resp_post):
            FakeObject.canCreate = True
            mgr = FakeObjectManager(self.gitlab)
            fake_obj = mgr.create({'name': 'fake_name'})
            self.assertIsInstance(fake_obj, FakeObject)
            self.assertEqual(fake_obj.id, 1)
            self.assertEqual(fake_obj.name, "fake_name")

    def test_project_manager_owned(self):
        mgr = ProjectManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/owned", method="get")
        def resp_get_all(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "name1", "id": 1}, '
                       '{"name": "name2", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_all):
            data = mgr.owned()
            self.assertEqual(type(data), list)
            self.assertEqual(2, len(data))
            self.assertEqual(type(data[0]), Project)
            self.assertEqual(type(data[1]), Project)
            self.assertEqual(data[0].name, "name1")
            self.assertEqual(data[1].name, "name2")
            self.assertEqual(data[0].id, 1)
            self.assertEqual(data[1].id, 2)

    def test_project_manager_all(self):
        mgr = ProjectManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost",
                  path="/api/v3/projects/all", method="get")
        def resp_get_all(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "name1", "id": 1}, '
                       '{"name": "name2", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_all):
            data = mgr.all()
            self.assertEqual(type(data), list)
            self.assertEqual(2, len(data))
            self.assertEqual(type(data[0]), Project)
            self.assertEqual(type(data[1]), Project)
            self.assertEqual(data[0].name, "name1")
            self.assertEqual(data[1].name, "name2")
            self.assertEqual(data[0].id, 1)
            self.assertEqual(data[1].id, 2)

    def test_project_manager_search(self):
        mgr = ProjectManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/projects",
                  query="search=foo", method="get")
        def resp_get_all(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "foo1", "id": 1}, '
                       '{"name": "foo2", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_all):
            data = mgr.list(search='foo')
            self.assertEqual(type(data), list)
            self.assertEqual(2, len(data))
            self.assertEqual(type(data[0]), Project)
            self.assertEqual(type(data[1]), Project)
            self.assertEqual(data[0].name, "foo1")
            self.assertEqual(data[1].name, "foo2")
            self.assertEqual(data[0].id, 1)
            self.assertEqual(data[1].id, 2)

    def test_user_manager_search(self):
        mgr = UserManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/users",
                  query="search=foo", method="get")
        def resp_get_search(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "foo1", "id": 1}, '
                       '{"name": "foo2", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_search):
            data = mgr.search('foo')
            self.assertEqual(type(data), list)
            self.assertEqual(2, len(data))
            self.assertEqual(type(data[0]), User)
            self.assertEqual(type(data[1]), User)
            self.assertEqual(data[0].name, "foo1")
            self.assertEqual(data[1].name, "foo2")
            self.assertEqual(data[0].id, 1)
            self.assertEqual(data[1].id, 2)

    def test_user_manager_get_by_username(self):
        mgr = UserManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/users",
                  query="username=foo", method="get")
        def resp_get_username(url, request):
            headers = {'content-type': 'application/json'}
            content = '[{"name": "foo", "id": 1}]'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_username):
            data = mgr.get_by_username('foo')
            self.assertEqual(type(data), User)
            self.assertEqual(data.name, "foo")
            self.assertEqual(data.id, 1)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/users",
                  query="username=foo", method="get")
        def resp_get_username_nomatch(url, request):
            headers = {'content-type': 'application/json'}
            content = '[]'.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_username_nomatch):
            self.assertRaises(GitlabGetError, mgr.get_by_username, 'foo')

    def test_group_manager_search(self):
        mgr = GroupManager(self.gitlab)

        @urlmatch(scheme="http", netloc="localhost", path="/api/v3/groups",
                  query="search=foo", method="get")
        def resp_get_search(url, request):
            headers = {'content-type': 'application/json'}
            content = ('[{"name": "foo1", "id": 1}, '
                       '{"name": "foo2", "id": 2}]')
            content = content.encode("utf-8")
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_get_search):
            data = mgr.search('foo')
            self.assertEqual(type(data), list)
            self.assertEqual(2, len(data))
            self.assertEqual(type(data[0]), Group)
            self.assertEqual(type(data[1]), Group)
            self.assertEqual(data[0].name, "foo1")
            self.assertEqual(data[1].name, "foo2")
            self.assertEqual(data[0].id, 1)
            self.assertEqual(data[1].id, 2)
