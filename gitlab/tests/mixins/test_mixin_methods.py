import pytest

from httmock import HTTMock, response, urlmatch  # noqa

from gitlab import base
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    GetWithoutIdMixin,
    ListMixin,
    RefreshMixin,
    SaveMixin,
    SetMixin,
    UpdateMixin,
)


class FakeObject(base.RESTObject):
    pass


class FakeManager(base.RESTManager):
    _path = "/tests"
    _obj_cls = FakeObject


def test_get_mixin(gl):
    class M(GetMixin, FakeManager):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests/42", method="get")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = mgr.get(42)
        assert isinstance(obj, FakeObject)
        assert obj.foo == "bar"
        assert obj.id == 42


def test_refresh_mixin(gl):
    class O(RefreshMixin, FakeObject):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests/42", method="get")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = FakeManager(gl)
        obj = O(mgr, {"id": 42})
        res = obj.refresh()
        assert res is None
        assert obj.foo == "bar"
        assert obj.id == 42


def test_get_without_id_mixin(gl):
    class M(GetWithoutIdMixin, FakeManager):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"foo": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = mgr.get()
        assert isinstance(obj, FakeObject)
        assert obj.foo == "bar"
        assert not hasattr(obj, "id")


def test_list_mixin(gl):
    class M(ListMixin, FakeManager):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '[{"id": 42, "foo": "bar"},{"id": 43, "foo": "baz"}]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        # test RESTObjectList
        mgr = M(gl)
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


def test_list_other_url(gl):
    class M(ListMixin, FakeManager):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/others", method="get")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '[{"id": 42, "foo": "bar"}]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj_list = mgr.list(path="/others", as_list=False)
        assert isinstance(obj_list, base.RESTObjectList)
        obj = obj_list.next()
        assert obj.id == 42
        assert obj.foo == "bar"
        with pytest.raises(StopIteration):
            obj_list.next()


def test_create_mixin_missing_attrs(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = (("foo",), ("bar", "baz"))

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._check_missing_create_attrs(data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._check_missing_create_attrs(data)
    assert "foo" in str(error.value)


def test_create_mixin(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = (("foo",), ("bar", "baz"))
        _update_attrs = (("foo",), ("bam",))

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="post")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = mgr.create({"foo": "bar"})
        assert isinstance(obj, FakeObject)
        assert obj.id == 42
        assert obj.foo == "bar"


def test_create_mixin_custom_path(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = (("foo",), ("bar", "baz"))
        _update_attrs = (("foo",), ("bam",))

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/others", method="post")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = mgr.create({"foo": "bar"}, path="/others")
        assert isinstance(obj, FakeObject)
        assert obj.id == 42
        assert obj.foo == "bar"


def test_update_mixin_missing_attrs(gl):
    class M(UpdateMixin, FakeManager):
        _update_attrs = (("foo",), ("bar", "baz"))

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._check_missing_update_attrs(data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._check_missing_update_attrs(data)
    assert "foo" in str(error.value)


def test_update_mixin(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = (("foo",), ("bar", "baz"))
        _update_attrs = (("foo",), ("bam",))

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests/42", method="put")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "baz"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        server_data = mgr.update(42, {"foo": "baz"})
        assert isinstance(server_data, dict)
        assert server_data["id"] == 42
        assert server_data["foo"] == "baz"


def test_update_mixin_no_id(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = (("foo",), ("bar", "baz"))
        _update_attrs = (("foo",), ("bam",))

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="put")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"foo": "baz"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        server_data = mgr.update(new_data={"foo": "baz"})
        assert isinstance(server_data, dict)
        assert server_data["foo"] == "baz"


def test_delete_mixin(gl):
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
        mgr = M(gl)
        mgr.delete(42)


def test_save_mixin(gl):
    class M(UpdateMixin, FakeManager):
        pass

    class O(SaveMixin, base.RESTObject):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests/42", method="put")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"id": 42, "foo": "baz"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = O(mgr, {"id": 42, "foo": "bar"})
        obj.foo = "baz"
        obj.save()
        assert obj._attrs["foo"] == "baz"
        assert obj._updated_attrs == {}


def test_set_mixin(gl):
    class M(SetMixin, FakeManager):
        pass

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests/foo", method="put")
    def resp_cont(url, request):
        headers = {"Content-Type": "application/json"}
        content = '{"key": "foo", "value": "bar"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        mgr = M(gl)
        obj = mgr.set("foo", "bar")
        assert isinstance(obj, FakeObject)
        assert obj.key == "foo"
        assert obj.value == "bar"
