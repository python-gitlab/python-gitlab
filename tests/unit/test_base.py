# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Gauvain Pocentek <gauvain@pocentek.net>
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

import pickle
import unittest

from gitlab import base


class FakeGitlab(object):
    pass


class FakeObject(base.RESTObject):
    pass


class FakeManager(base.RESTManager):
    _obj_cls = FakeObject
    _path = "/tests"


class TestRESTManager(unittest.TestCase):
    def test_computed_path_simple(self):
        class MGR(base.RESTManager):
            _path = "/tests"
            _obj_cls = object

        mgr = MGR(FakeGitlab())
        self.assertEqual(mgr._computed_path, "/tests")

    def test_computed_path_with_parent(self):
        class MGR(base.RESTManager):
            _path = "/tests/%(test_id)s/cases"
            _obj_cls = object
            _from_parent_attrs = {"test_id": "id"}

        class Parent(object):
            id = 42

        mgr = MGR(FakeGitlab(), parent=Parent())
        self.assertEqual(mgr._computed_path, "/tests/42/cases")

    def test_path_property(self):
        class MGR(base.RESTManager):
            _path = "/tests"
            _obj_cls = object

        mgr = MGR(FakeGitlab())
        self.assertEqual(mgr.path, "/tests")


class TestRESTObject(unittest.TestCase):
    def setUp(self):
        self.gitlab = FakeGitlab()
        self.manager = FakeManager(self.gitlab)

    def test_instanciate(self):
        obj = FakeObject(self.manager, {"foo": "bar"})

        self.assertDictEqual({"foo": "bar"}, obj._attrs)
        self.assertDictEqual({}, obj._updated_attrs)
        self.assertEqual(None, obj._create_managers())
        self.assertEqual(self.manager, obj.manager)
        self.assertEqual(self.gitlab, obj.manager.gitlab)

    def test_pickability(self):
        obj = FakeObject(self.manager, {"foo": "bar"})
        original_obj_module = obj._module
        pickled = pickle.dumps(obj)
        unpickled = pickle.loads(pickled)
        self.assertIsInstance(unpickled, FakeObject)
        self.assertTrue(hasattr(unpickled, "_module"))
        self.assertEqual(unpickled._module, original_obj_module)
        pickled2 = pickle.dumps(unpickled)

    def test_attrs(self):
        obj = FakeObject(self.manager, {"foo": "bar"})

        self.assertEqual("bar", obj.foo)
        self.assertRaises(AttributeError, getattr, obj, "bar")

        obj.bar = "baz"
        self.assertEqual("baz", obj.bar)
        self.assertDictEqual({"foo": "bar"}, obj._attrs)
        self.assertDictEqual({"bar": "baz"}, obj._updated_attrs)

    def test_get_id(self):
        obj = FakeObject(self.manager, {"foo": "bar"})
        obj.id = 42
        self.assertEqual(42, obj.get_id())

        obj.id = None
        self.assertEqual(None, obj.get_id())

    def test_custom_id_attr(self):
        class OtherFakeObject(FakeObject):
            _id_attr = "foo"

        obj = OtherFakeObject(self.manager, {"foo": "bar"})
        self.assertEqual("bar", obj.get_id())

    def test_update_attrs(self):
        obj = FakeObject(self.manager, {"foo": "bar"})
        obj.bar = "baz"
        obj._update_attrs({"foo": "foo", "bar": "bar"})
        self.assertDictEqual({"foo": "foo", "bar": "bar"}, obj._attrs)
        self.assertDictEqual({}, obj._updated_attrs)

    def test_create_managers(self):
        class ObjectWithManager(FakeObject):
            _managers = (("fakes", "FakeManager"),)

        obj = ObjectWithManager(self.manager, {"foo": "bar"})
        obj.id = 42
        self.assertIsInstance(obj.fakes, FakeManager)
        self.assertEqual(obj.fakes.gitlab, self.gitlab)
        self.assertEqual(obj.fakes._parent, obj)

    def test_equality(self):
        obj1 = FakeObject(self.manager, {"id": "foo"})
        obj2 = FakeObject(self.manager, {"id": "foo", "other_attr": "bar"})
        self.assertEqual(obj1, obj2)

    def test_equality_custom_id(self):
        class OtherFakeObject(FakeObject):
            _id_attr = "foo"

        obj1 = OtherFakeObject(self.manager, {"foo": "bar"})
        obj2 = OtherFakeObject(self.manager, {"foo": "bar", "other_attr": "baz"})
        self.assertEqual(obj1, obj2)

    def test_inequality(self):
        obj1 = FakeObject(self.manager, {"id": "foo"})
        obj2 = FakeObject(self.manager, {"id": "bar"})
        self.assertNotEqual(obj1, obj2)

    def test_inequality_no_id(self):
        obj1 = FakeObject(self.manager, {"attr1": "foo"})
        obj2 = FakeObject(self.manager, {"attr1": "bar"})
        self.assertNotEqual(obj1, obj2)
