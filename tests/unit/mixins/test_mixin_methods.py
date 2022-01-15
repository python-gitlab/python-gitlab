import pytest
import responses

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


@responses.activate
def test_get_mixin(gl):
    class M(GetMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.GET,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = mgr.get(42)
    assert isinstance(obj, FakeObject)
    assert obj.foo == "bar"
    assert obj.id == 42
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_refresh_mixin(gl):
    class TestClass(RefreshMixin, FakeObject):
        pass

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.GET,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = FakeManager(gl)
    obj = TestClass(mgr, {"id": 42})
    res = obj.refresh()
    assert res is None
    assert obj.foo == "bar"
    assert obj.id == 42
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_get_without_id_mixin(gl):
    class M(GetWithoutIdMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.GET,
        url=url,
        json={"foo": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = mgr.get()
    assert isinstance(obj, FakeObject)
    assert obj.foo == "bar"
    assert not hasattr(obj, "id")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_list_mixin(gl):
    class M(ListMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.GET,
        url=url,
        json=[{"id": 42, "foo": "bar"}, {"id": 43, "foo": "baz"}],
        status=200,
        match_querystring=True,
    )

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
    assert responses.assert_call_count(url, 2) is True


@responses.activate
def test_list_other_url(gl):
    class M(ListMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/others"
    responses.add(
        method=responses.GET,
        url=url,
        json=[{"id": 42, "foo": "bar"}],
        status=200,
        match_querystring=True,
    )

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
        _create_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._check_missing_create_attrs(data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._check_missing_create_attrs(data)
    assert "foo" in str(error.value)


@responses.activate
def test_create_mixin(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = base.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = mgr.create({"foo": "bar"})
    assert isinstance(obj, FakeObject)
    assert obj.id == 42
    assert obj.foo == "bar"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_create_mixin_custom_path(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = base.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/others"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = mgr.create({"foo": "bar"}, path="/others")
    assert isinstance(obj, FakeObject)
    assert obj.id == 42
    assert obj.foo == "bar"
    assert responses.assert_call_count(url, 1) is True


def test_update_mixin_missing_attrs(gl):
    class M(UpdateMixin, FakeManager):
        _update_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._check_missing_update_attrs(data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._check_missing_update_attrs(data)
    assert "foo" in str(error.value)


@responses.activate
def test_update_mixin(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = base.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"id": 42, "foo": "baz"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    server_data = mgr.update(42, {"foo": "baz"})
    assert isinstance(server_data, dict)
    assert server_data["id"] == 42
    assert server_data["foo"] == "baz"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_update_mixin_no_id(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = base.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = base.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"foo": "baz"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    server_data = mgr.update(new_data={"foo": "baz"})
    assert isinstance(server_data, dict)
    assert server_data["foo"] == "baz"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_delete_mixin(gl):
    class M(DeleteMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.DELETE,
        url=url,
        json="",
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    mgr.delete(42)
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_save_mixin(gl):
    class M(UpdateMixin, FakeManager):
        pass

    class TestClass(SaveMixin, base.RESTObject):
        pass

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"id": 42, "foo": "baz"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = TestClass(mgr, {"id": 42, "foo": "bar"})
    obj.foo = "baz"
    obj.save()
    assert obj._attrs["foo"] == "baz"
    assert obj._updated_attrs == {}
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_set_mixin(gl):
    class M(SetMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests/foo"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"key": "foo", "value": "bar"},
        status=200,
        match_querystring=True,
    )

    mgr = M(gl)
    obj = mgr.set("foo", "bar")
    assert isinstance(obj, FakeObject)
    assert obj.key == "foo"
    assert obj.value == "bar"
    assert responses.assert_call_count(url, 1) is True
