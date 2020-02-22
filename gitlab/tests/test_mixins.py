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

import unittest

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
        self.assertTrue(hasattr(obj, "approve"))

    def test_subscribable_mixin(self):
        class O(SubscribableMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, "subscribe"))
        self.assertTrue(hasattr(obj, "unsubscribe"))

    def test_todo_mixin(self):
        class O(TodoMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, "todo"))

    def test_time_tracking_mixin(self):
        class O(TimeTrackingMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, "time_stats"))
        self.assertTrue(hasattr(obj, "time_estimate"))
        self.assertTrue(hasattr(obj, "reset_time_estimate"))
        self.assertTrue(hasattr(obj, "add_spent_time"))
        self.assertTrue(hasattr(obj, "reset_spent_time"))

    def test_set_mixin(self):
        class O(SetMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, "set"))

    def test_user_agent_detail_mixin(self):
        class O(UserAgentDetailMixin):
            pass

        obj = O()
        self.assertTrue(hasattr(obj, "user_agent_detail"))


class TestMetaMixins(unittest.TestCase):
    def test_retrieve_mixin(self):
        class M(RetrieveMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, "list"))
        self.assertTrue(hasattr(obj, "get"))
        self.assertFalse(hasattr(obj, "create"))
        self.assertFalse(hasattr(obj, "update"))
        self.assertFalse(hasattr(obj, "delete"))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)

    def test_crud_mixin(self):
        class M(CRUDMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, "get"))
        self.assertTrue(hasattr(obj, "list"))
        self.assertTrue(hasattr(obj, "create"))
        self.assertTrue(hasattr(obj, "update"))
        self.assertTrue(hasattr(obj, "delete"))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)
        self.assertIsInstance(obj, CreateMixin)
        self.assertIsInstance(obj, UpdateMixin)
        self.assertIsInstance(obj, DeleteMixin)

    def test_no_update_mixin(self):
        class M(NoUpdateMixin):
            pass

        obj = M()
        self.assertTrue(hasattr(obj, "get"))
        self.assertTrue(hasattr(obj, "list"))
        self.assertTrue(hasattr(obj, "create"))
        self.assertFalse(hasattr(obj, "update"))
        self.assertTrue(hasattr(obj, "delete"))
        self.assertIsInstance(obj, ListMixin)
        self.assertIsInstance(obj, GetMixin)
        self.assertIsInstance(obj, CreateMixin)
        self.assertNotIsInstance(obj, UpdateMixin)
        self.assertIsInstance(obj, DeleteMixin)


class FakeObject(base.RESTObject):
    pass


class FakeManager(base.RESTManager):
    _path = "/tests"
    _obj_cls = FakeObject


class TestMixinMethods(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(
            "http://localhost", private_token="private_token", api_version=4
        )

    def test_create_mixin_get_attrs(self):
        class M1(CreateMixin, FakeManager):
            pass

        class M2(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        mgr = M1(self.gl)
        required, optional = mgr.get_create_attrs()
        self.assertEqual(len(required), 0)
        self.assertEqual(len(optional), 0)

        mgr = M2(self.gl)
        required, optional = mgr.get_create_attrs()
        self.assertIn("foo", required)
        self.assertIn("bar", optional)
        self.assertIn("baz", optional)
        self.assertNotIn("bam", optional)

    def test_create_mixin_missing_attrs(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))

        mgr = M(self.gl)
        data = {"foo": "bar", "baz": "blah"}
        mgr._check_missing_create_attrs(data)

        data = {"baz": "blah"}
        with self.assertRaises(AttributeError) as error:
            mgr._check_missing_create_attrs(data)
        self.assertIn("foo", str(error.exception))

    def test_update_mixin_get_attrs(self):
        class M1(UpdateMixin, FakeManager):
            pass

        class M2(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        mgr = M1(self.gl)
        required, optional = mgr.get_update_attrs()
        self.assertEqual(len(required), 0)
        self.assertEqual(len(optional), 0)

        mgr = M2(self.gl)
        required, optional = mgr.get_update_attrs()
        self.assertIn("foo", required)
        self.assertIn("bam", optional)
        self.assertNotIn("bar", optional)
        self.assertNotIn("baz", optional)

    def test_update_mixin_missing_attrs(self):
        class M(UpdateMixin, FakeManager):
            _update_attrs = (("foo",), ("bar", "baz"))

        mgr = M(self.gl)
        data = {"foo": "bar", "baz": "blah"}
        mgr._check_missing_update_attrs(data)

        data = {"baz": "blah"}
        with self.assertRaises(AttributeError) as error:
            mgr._check_missing_update_attrs(data)
        self.assertIn("foo", str(error.exception))
