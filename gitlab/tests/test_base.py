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

from gitlab import base
import pytest


class FakeGitlab(object):
    pass


class FakeObject(base.RESTObject):
    pass


class FakeManager(base.RESTManager):
    _obj_cls = FakeObject
    _path = "/tests"


@pytest.fixture
def fake_gitlab():
    return FakeGitlab()


@pytest.fixture
def fake_manager(fake_gitlab):
    return FakeManager(fake_gitlab)


class TestRESTManager:
    def test_computed_path_simple(self):
        class MGR(base.RESTManager):
            _path = "/tests"
            _obj_cls = object

        mgr = MGR(FakeGitlab())
        assert mgr._computed_path == "/tests"

    def test_computed_path_with_parent(self):
        class MGR(base.RESTManager):
            _path = "/tests/%(test_id)s/cases"
            _obj_cls = object
            _from_parent_attrs = {"test_id": "id"}

        class Parent(object):
            id = 42

        mgr = MGR(FakeGitlab(), parent=Parent())
        assert mgr._computed_path == "/tests/42/cases"

    def test_path_property(self):
        class MGR(base.RESTManager):
            _path = "/tests"
            _obj_cls = object

        mgr = MGR(FakeGitlab())
        assert mgr.path == "/tests"


class TestRESTObject:
    def test_instantiate(self, fake_gitlab, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "bar"})

        assert {"foo": "bar"} == obj._attrs
        assert {} == obj._updated_attrs
        assert obj._create_managers() is None
        assert fake_manager == obj.manager
        assert fake_gitlab == obj.manager.gitlab

    def test_picklability(self, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "bar"})
        original_obj_module = obj._module
        pickled = pickle.dumps(obj)
        unpickled = pickle.loads(pickled)
        assert isinstance(unpickled, FakeObject)
        assert hasattr(unpickled, "_module")
        assert unpickled._module == original_obj_module
        pickle.dumps(unpickled)

    def test_attrs(self, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "bar"})

        assert "bar" == obj.foo
        with pytest.raises(AttributeError):
            getattr(obj, "bar")

        obj.bar = "baz"
        assert "baz" == obj.bar
        assert {"foo": "bar"} == obj._attrs
        assert {"bar": "baz"} == obj._updated_attrs

    def test_get_id(self, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "bar"})
        obj.id = 42
        assert 42 == obj.get_id()

        obj.id = None
        assert obj.get_id() is None

    def test_custom_id_attr(self, fake_manager):
        class OtherFakeObject(FakeObject):
            _id_attr = "foo"

        obj = OtherFakeObject(fake_manager, {"foo": "bar"})
        assert "bar" == obj.get_id()

    def test_update_attrs(self, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "bar"})
        obj.bar = "baz"
        obj._update_attrs({"foo": "foo", "bar": "bar"})
        assert {"foo": "foo", "bar": "bar"} == obj._attrs
        assert {} == obj._updated_attrs

    def test_update_attrs_deleted(self, fake_manager):
        obj = FakeObject(fake_manager, {"foo": "foo", "bar": "bar"})
        obj.bar = "baz"
        obj._update_attrs({"foo": "foo"})
        assert {"foo": "foo"} == obj._attrs
        assert {} == obj._updated_attrs

    def test_dir_unique(self, fake_manager):
        obj = FakeObject(fake_manager, {"manager": "foo"})
        assert len(dir(obj)) == len(set(dir(obj)))

    def test_create_managers(self, fake_gitlab, fake_manager):
        class ObjectWithManager(FakeObject):
            _managers = (("fakes", "FakeManager"),)

        obj = ObjectWithManager(fake_manager, {"foo": "bar"})
        obj.id = 42
        assert isinstance(obj.fakes, FakeManager)
        assert obj.fakes.gitlab == fake_gitlab
        assert obj.fakes._parent == obj

    def test_equality(self, fake_manager):
        obj1 = FakeObject(fake_manager, {"id": "foo"})
        obj2 = FakeObject(fake_manager, {"id": "foo", "other_attr": "bar"})
        assert obj1 == obj2

    def test_equality_custom_id(self, fake_manager):
        class OtherFakeObject(FakeObject):
            _id_attr = "foo"

        obj1 = OtherFakeObject(fake_manager, {"foo": "bar"})
        obj2 = OtherFakeObject(fake_manager, {"foo": "bar", "other_attr": "baz"})
        assert obj1 == obj2

    def test_inequality(self, fake_manager):
        obj1 = FakeObject(fake_manager, {"id": "foo"})
        obj2 = FakeObject(fake_manager, {"id": "bar"})
        assert obj1 != obj2

    def test_inequality_no_id(self, fake_manager):
        obj1 = FakeObject(fake_manager, {"attr1": "foo"})
        obj2 = FakeObject(fake_manager, {"attr1": "bar"})
        assert obj1 != obj2
