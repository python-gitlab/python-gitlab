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

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

from gitlab import *  # noqa
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


class TestObjectMixinsAttributes(unittest.TestCase):
    def test_access_request_mixin(self):
        class O(AccessRequestMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, 'approve'))

    def test_subscribable_mixin(self):
        class O(SubscribableMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, 'subscribe'))
        self.assertTrue(hasattr(obj, 'unsubscribe'))

    def test_todo_mixin(self):
        class O(TodoMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, 'todo'))

    def test_time_tracking_mixin(self):
        class O(TimeTrackingMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, 'time_stats'))
        self.assertTrue(hasattr(obj, 'time_estimate'))
        self.assertTrue(hasattr(obj, 'reset_time_estimate'))
        self.assertTrue(hasattr(obj, 'add_spent_time'))
        self.assertTrue(hasattr(obj, 'reset_spent_time'))


class TestMetaMixins(unittest.TestCase):
    def test_retrieve_mixin(self):
        class M(RetrieveMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, 'list'))
        self.assertTrue(hasattr(obj, 'get'))
        self.assertFalse(hasattr(obj, 'create'))
        self.assertFalse(hasattr(obj, 'update'))
        self.assertFalse(hasattr(obj, 'delete'))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)

    def test_crud_mixin(self):
        class M(CRUDMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, 'get'))
        self.assertTrue(hasattr(obj, 'list'))
        self.assertTrue(hasattr(obj, 'create'))
        self.assertTrue(hasattr(obj, 'update'))
        self.assertTrue(hasattr(obj, 'delete'))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)
        self.assertIsInstance(obj, CreateMixin)
        self.assertIsInstance(obj, UpdateMixin)
        self.assertIsInstance(obj, DeleteMixin)

    def test_no_update_mixin(self):
        class M(NoUpdateMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, 'get'))
        self.assertTrue(hasattr(obj, 'list'))
        self.assertTrue(hasattr(obj, 'create'))
        self.assertFalse(hasattr(obj, 'update'))
        self.assertTrue(hasattr(obj, 'delete'))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)
        self.assertIsInstance(obj, CreateMixin)
        self.assertNotIsInstance(obj, UpdateMixin)
        self.assertIsInstance(obj, DeleteMixin)


class FakeObject(base.RESTObject):
    pass


class FakeManager(base.RESTManager):
    _path = '/tests'
    _obj_cls = FakeObject


class TestMixinMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab("http://localhost", private_token="private_token",
                         api_version=4)

    def test_get_mixin(self):
        class M(GetMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests/42',
                  method="get")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.get(42)
            self.assertIsInstance(obj, FakeObject)
            self.assertEqual(obj.foo, 'bar')
            self.assertEqual(obj.id, 42)

    def test_get_without_id_mixin(self):
        class M(GetWithoutIdMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests',
                  method="get")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.get()
            self.assertIsInstance(obj, FakeObject)
            self.assertEqual(obj.foo, 'bar')
            self.assertFalse(hasattr(obj, 'id'))

    def test_list_mixin(self):
        class M(ListMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests',
                  method="get")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '[{"id": 42, "foo": "bar"},{"id": 43, "foo": "baz"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            # test RESTObjectList
            mgr = M(self.gl)
            obj_list = mgr.list(as_list=False)
            self.assertIsInstance(obj_list, base.RESTObjectList)
            for obj in obj_list:
                self.assertIsInstance(obj, FakeObject)
                self.assertIn(obj.id, (42, 43))

            # test list()
            obj_list = mgr.list(all=True)
            self.assertIsInstance(obj_list, list)
            self.assertEqual(obj_list[0].id, 42)
            self.assertEqual(obj_list[1].id, 43)
            self.assertIsInstance(obj_list[0], FakeObject)
            self.assertEqual(len(obj_list), 2)

    def test_list_other_url(self):
        class M(ListMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/others',
                  method="get")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '[{"id": 42, "foo": "bar"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj_list = mgr.list(path='/others', as_list=False)
            self.assertIsInstance(obj_list, base.RESTObjectList)
            obj = obj_list.next()
            self.assertEqual(obj.id, 42)
            self.assertEqual(obj.foo, 'bar')
            self.assertRaises(StopIteration, obj_list.next)

    def test_get_from_list_mixin(self):
        class M(GetFromListMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests',
                  method="get")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '[{"id": 42, "foo": "bar"},{"id": 43, "foo": "baz"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.get(42)
            self.assertIsInstance(obj, FakeObject)
            self.assertEqual(obj.foo, 'bar')
            self.assertEqual(obj.id, 42)

            self.assertRaises(GitlabGetError, mgr.get, 44)

    def test_create_mixin_get_attrs(self):
        class M1(CreateMixin, FakeManager):
            pass

        class M2(CreateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        mgr = M1(self.gl)
        required, optional = mgr.get_create_attrs()
        self.assertEqual(len(required), 0)
        self.assertEqual(len(optional), 0)

        mgr = M2(self.gl)
        required, optional = mgr.get_create_attrs()
        self.assertIn('foo', required)
        self.assertIn('bar', optional)
        self.assertIn('baz', optional)
        self.assertNotIn('bam', optional)

    def test_create_mixin_missing_attrs(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))

        mgr = M(self.gl)
        data = {'foo': 'bar', 'baz': 'blah'}
        mgr._check_missing_create_attrs(data)

        data = {'baz': 'blah'}
        with self.assertRaises(AttributeError) as error:
            mgr._check_missing_create_attrs(data)
        self.assertIn('foo', str(error.exception))

    def test_create_mixin(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests',
                  method="post")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.create({'foo': 'bar'})
            self.assertIsInstance(obj, FakeObject)
            self.assertEqual(obj.id, 42)
            self.assertEqual(obj.foo, 'bar')

    def test_create_mixin_custom_path(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/others',
                  method="post")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.create({'foo': 'bar'}, path='/others')
            self.assertIsInstance(obj, FakeObject)
            self.assertEqual(obj.id, 42)
            self.assertEqual(obj.foo, 'bar')

    def test_update_mixin_get_attrs(self):
        class M1(UpdateMixin, FakeManager):
            pass

        class M2(UpdateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        mgr = M1(self.gl)
        required, optional = mgr.get_update_attrs()
        self.assertEqual(len(required), 0)
        self.assertEqual(len(optional), 0)

        mgr = M2(self.gl)
        required, optional = mgr.get_update_attrs()
        self.assertIn('foo', required)
        self.assertIn('bam', optional)
        self.assertNotIn('bar', optional)
        self.assertNotIn('baz', optional)

    def test_update_mixin_missing_attrs(self):
        class M(UpdateMixin, FakeManager):
            _update_attrs = (('foo',), ('bar', 'baz'))

        mgr = M(self.gl)
        data = {'foo': 'bar', 'baz': 'blah'}
        mgr._check_missing_update_attrs(data)

        data = {'baz': 'blah'}
        with self.assertRaises(AttributeError) as error:
            mgr._check_missing_update_attrs(data)
        self.assertIn('foo', str(error.exception))

    def test_update_mixin(self):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests/42',
                  method="put")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"id": 42, "foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            server_data = mgr.update(42, {'foo': 'baz'})
            self.assertIsInstance(server_data, dict)
            self.assertEqual(server_data['id'], 42)
            self.assertEqual(server_data['foo'], 'baz')

    def test_update_mixin_no_id(self):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (('foo',), ('bar', 'baz'))
            _update_attrs = (('foo',), ('bam', ))

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests',
                  method="put")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            server_data = mgr.update(new_data={'foo': 'baz'})
            self.assertIsInstance(server_data, dict)
            self.assertEqual(server_data['foo'], 'baz')

    def test_delete_mixin(self):
        class M(DeleteMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests/42',
                  method="delete")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = ''
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            mgr.delete(42)

    def test_save_mixin(self):
        class M(UpdateMixin, FakeManager):
            pass

        class O(SaveMixin, RESTObject):
            pass

        @urlmatch(scheme="http", netloc="localhost", path='/api/v4/tests/42',
                  method="put")
        def resp_cont(url, request):
            headers = {'Content-Type': 'application/json'}
            content = '{"id": 42, "foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = O(mgr, {'id': 42, 'foo': 'bar'})
            obj.foo = 'baz'
            obj.save()
            self.assertEqual(obj._attrs['foo'], 'baz')
            self.assertDictEqual(obj._updated_attrs, {})
