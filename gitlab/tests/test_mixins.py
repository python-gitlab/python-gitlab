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
import pytest


class TestObjectMixinsAttributes(unittest.TestCase):
    def test_access_request_mixin(self):
        class O(AccessRequestMixin):
            pass

        obj = O()
        assert hasattr(obj, "approve")

    def test_subscribable_mixin(self):
        class O(SubscribableMixin):
            pass

        obj = O()
        assert hasattr(obj, "subscribe")
        assert hasattr(obj, "unsubscribe")

    def test_todo_mixin(self):
        class O(TodoMixin):
            pass

        obj = O()
        assert hasattr(obj, "todo")

    def test_time_tracking_mixin(self):
        class O(TimeTrackingMixin):
            pass

        obj = O()
        assert hasattr(obj, "time_stats")
        assert hasattr(obj, "time_estimate")
        assert hasattr(obj, "reset_time_estimate")
        assert hasattr(obj, "add_spent_time")
        assert hasattr(obj, "reset_spent_time")

    def test_set_mixin(self):
        class O(SetMixin):
            pass

        obj = O()
        assert hasattr(obj, "set")

    def test_user_agent_detail_mixin(self):
        class O(UserAgentDetailMixin):
            pass

        obj = O()
        assert hasattr(obj, "user_agent_detail")


class TestMetaMixins(unittest.TestCase):
    def test_retrieve_mixin(self):
        class M(RetrieveMixin):
            pass

        obj = M()
        assert hasattr(obj, "list")
        assert hasattr(obj, "get")
        assert not hasattr(obj, "create")
        assert not hasattr(obj, "update")
        assert not hasattr(obj, "delete")
        assert isinstance(obj, ListMixin)
        assert isinstance(obj, GetMixin)

    def test_crud_mixin(self):
        class M(CRUDMixin):
            pass

        obj = M()
        assert hasattr(obj, "get")
        assert hasattr(obj, "list")
        assert hasattr(obj, "create")
        assert hasattr(obj, "update")
        assert hasattr(obj, "delete")
        assert isinstance(obj, ListMixin)
        assert isinstance(obj, GetMixin)
        assert isinstance(obj, CreateMixin)
        assert isinstance(obj, UpdateMixin)
        assert isinstance(obj, DeleteMixin)

    def test_no_update_mixin(self):
        class M(NoUpdateMixin):
            pass

        obj = M()
        assert hasattr(obj, "get")
        assert hasattr(obj, "list")
        assert hasattr(obj, "create")
        assert not hasattr(obj, "update")
        assert hasattr(obj, "delete")
        assert isinstance(obj, ListMixin)
        assert isinstance(obj, GetMixin)
        assert isinstance(obj, CreateMixin)
        assert not isinstance(obj, UpdateMixin)
        assert isinstance(obj, DeleteMixin)


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

    def test_get_mixin(self):
        class M(GetMixin, FakeManager):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/42", method="get"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.get(42)
            assert isinstance(obj, FakeObject)
            assert obj.foo == "bar"
            assert obj.id == 42

    def test_refresh_mixin(self):
        class O(RefreshMixin, FakeObject):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/42", method="get"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = FakeManager(self.gl)
            obj = O(mgr, {"id": 42})
            res = obj.refresh()
            assert res is None
            assert obj.foo == "bar"
            assert obj.id == 42

    def test_get_without_id_mixin(self):
        class M(GetWithoutIdMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.get()
            assert isinstance(obj, FakeObject)
            assert obj.foo == "bar"
            assert not hasattr(obj, "id")

    def test_list_mixin(self):
        class M(ListMixin, FakeManager):
            pass

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '[{"id": 42, "foo": "bar"},{"id": 43, "foo": "baz"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            # test RESTObjectList
            mgr = M(self.gl)
            obj_list = mgr.list(as_list=False)
            assert isinstance(obj_list, base.RESTObjectList)
            for obj in obj_list:
                assert isinstance(obj, FakeObject)
                assert obj.id in (42, 43)

            # test list()
            obj_list = mgr.list(all=True)
            assert isinstance(obj_list, list)
            assert obj_list[0].id == 42
            assert obj_list[1].id == 43
            assert isinstance(obj_list[0], FakeObject)
            assert len(obj_list) == 2

    def test_list_other_url(self):
        class M(ListMixin, FakeManager):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/others", method="get"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '[{"id": 42, "foo": "bar"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj_list = mgr.list(path="/others", as_list=False)
            assert isinstance(obj_list, base.RESTObjectList)
            obj = obj_list.next()
            assert obj.id == 42
            assert obj.foo == "bar"
            with pytest.raises(StopIteration):
                obj_list.next()

    def test_create_mixin_get_attrs(self):
        class M1(CreateMixin, FakeManager):
            pass

        class M2(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        mgr = M1(self.gl)
        required, optional = mgr.get_create_attrs()
        assert len(required) == 0
        assert len(optional) == 0

        mgr = M2(self.gl)
        required, optional = mgr.get_create_attrs()
        assert "foo" in required
        assert "bar" in optional
        assert "baz" in optional
        assert "bam" not in optional

    def test_create_mixin_missing_attrs(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))

        mgr = M(self.gl)
        data = {"foo": "bar", "baz": "blah"}
        mgr._check_missing_create_attrs(data)

        data = {"baz": "blah"}
        with pytest.raises(AttributeError) as error:
            mgr._check_missing_create_attrs(data)
        assert "foo" in str(error.value)

    def test_create_mixin(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests", method="post"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.create({"foo": "bar"})
            assert isinstance(obj, FakeObject)
            assert obj.id == 42
            assert obj.foo == "bar"

    def test_create_mixin_custom_path(self):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/others", method="post"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.create({"foo": "bar"}, path="/others")
            assert isinstance(obj, FakeObject)
            assert obj.id == 42
            assert obj.foo == "bar"

    def test_update_mixin_get_attrs(self):
        class M1(UpdateMixin, FakeManager):
            pass

        class M2(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        mgr = M1(self.gl)
        required, optional = mgr.get_update_attrs()
        assert len(required) == 0
        assert len(optional) == 0

        mgr = M2(self.gl)
        required, optional = mgr.get_update_attrs()
        assert "foo" in required
        assert "bam" in optional
        assert "bar" not in optional
        assert "baz" not in optional

    def test_update_mixin_missing_attrs(self):
        class M(UpdateMixin, FakeManager):
            _update_attrs = (("foo",), ("bar", "baz"))

        mgr = M(self.gl)
        data = {"foo": "bar", "baz": "blah"}
        mgr._check_missing_update_attrs(data)

        data = {"baz": "blah"}
        with pytest.raises(AttributeError) as error:
            mgr._check_missing_update_attrs(data)
        assert "foo" in str(error.value)

    def test_update_mixin(self):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/42", method="put"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            server_data = mgr.update(42, {"foo": "baz"})
            assert isinstance(server_data, dict)
            assert server_data["id"] == 42
            assert server_data["foo"] == "baz"

    def test_update_mixin_no_id(self):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="put")
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            server_data = mgr.update(new_data={"foo": "baz"})
            assert isinstance(server_data, dict)
            assert server_data["foo"] == "baz"

    def test_delete_mixin(self):
        class M(DeleteMixin, FakeManager):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/42", method="delete"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = ""
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            mgr.delete(42)

    def test_save_mixin(self):
        class M(UpdateMixin, FakeManager):
            pass

        class O(SaveMixin, RESTObject):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/42", method="put"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"id": 42, "foo": "baz"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = O(mgr, {"id": 42, "foo": "bar"})
            obj.foo = "baz"
            obj.save()
            assert obj._attrs["foo"] == "baz"
            assert obj._updated_attrs == {}

    def test_set_mixin(self):
        class M(SetMixin, FakeManager):
            pass

        @urlmatch(
            scheme="http", netloc="localhost", path="/api/v4/tests/foo", method="put"
        )
        def resp_cont(url, request):
            headers = {"Content-Type": "application/json"}
            content = '{"key": "foo", "value": "bar"}'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            mgr = M(self.gl)
            obj = mgr.set("foo", "bar")
            assert isinstance(obj, FakeObject)
            assert obj.key == "foo"
            assert obj.value == "bar"
