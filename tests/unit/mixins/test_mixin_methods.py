from unittest.mock import mock_open, patch

import pytest
import requests
import responses

from gitlab import base, GitlabUploadError
from gitlab import types as gl_types
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    GetWithoutIdMixin,
    ListMixin,
    RefreshMixin,
    SaveMixin,
    SetMixin,
    UpdateMethod,
    UpdateMixin,
    UploadMixin,
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
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    obj = mgr.get(42)
    assert isinstance(obj, FakeObject)
    assert obj.foo == "bar"
    assert obj.id == 42
    assert obj._lazy is False
    assert responses.assert_call_count(url, 1) is True


def test_get_mixin_lazy(gl):
    class M(GetMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests/42"

    mgr = M(gl)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            json={"id": 42, "foo": "bar"},
            status=200,
            match=[responses.matchers.query_param_matcher({})],
        )
        obj = mgr.get(42, lazy=True)
    assert isinstance(obj, FakeObject)
    assert not hasattr(obj, "foo")
    assert obj.id == 42
    assert obj._lazy is True
    # a `lazy` get does not make a network request
    assert not rsps.calls


def test_get_mixin_lazy_missing_attribute(gl):
    class FakeGetManager(GetMixin, FakeManager):
        pass

    manager = FakeGetManager(gl)
    obj = manager.get(1, lazy=True)
    assert obj.id == 1
    with pytest.raises(AttributeError) as exc:
        obj.missing_attribute
    # undo `textwrap.fill()`
    message = str(exc.value).replace("\n", " ")
    assert "'FakeObject' object has no attribute 'missing_attribute'" in message
    assert (
        "note that <class 'tests.unit.mixins.test_mixin_methods.FakeObject'> was "
        "created as a `lazy` object and was not initialized with any data."
    ) in message


@responses.activate
def test_head_mixin(gl):
    class M(GetMixin, FakeManager):
        pass

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.HEAD,
        url=url,
        headers={"X-GitLab-Header": "test"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    manager = M(gl)
    result = manager.head(42)
    assert isinstance(result, requests.structures.CaseInsensitiveDict)
    assert result["x-gitlab-header"] == "test"


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
        match=[responses.matchers.query_param_matcher({})],
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
        match=[responses.matchers.query_param_matcher({})],
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
    headers = {
        "X-Page": "1",
        "X-Next-Page": "2",
        "X-Per-Page": "1",
        "X-Total-Pages": "2",
        "X-Total": "2",
        "Link": ("<http://localhost/api/v4/tests" ' rel="next"'),
    }
    responses.add(
        method=responses.GET,
        headers=headers,
        url=url,
        json=[{"id": 42, "foo": "bar"}, {"id": 43, "foo": "baz"}],
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    # test RESTObjectList
    mgr = M(gl)
    obj_list = mgr.list(iterator=True)
    assert isinstance(obj_list, base.RESTObjectList)
    assert obj_list.current_page == 1
    assert obj_list.prev_page is None
    assert obj_list.next_page == 2
    assert obj_list.per_page == 1
    assert obj_list.total == 2
    assert obj_list.total_pages == 2
    assert len(obj_list) == 2

    for obj in obj_list:
        assert isinstance(obj, FakeObject)
        assert obj.id in (42, 43)

    # test list()
    obj_list = mgr.list(get_all=True)
    assert isinstance(obj_list, list)
    assert obj_list[0].id == 42
    assert obj_list[1].id == 43
    assert isinstance(obj_list[0], FakeObject)
    assert len(obj_list) == 2
    assert responses.assert_call_count(url, 2) is True


@responses.activate
def test_list_mixin_with_attributes(gl):
    class M(ListMixin, FakeManager):
        _types = {"my_array": gl_types.ArrayAttribute}

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.GET,
        headers={},
        url=url,
        json=[],
        status=200,
        match=[responses.matchers.query_param_matcher({"my_array[]": ["1", "2", "3"]})],
    )

    mgr = M(gl)
    mgr.list(iterator=True, my_array=[1, 2, 3])


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
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    obj_list = mgr.list(path="/others", iterator=True)
    assert isinstance(obj_list, base.RESTObjectList)
    obj = obj_list.next()
    assert obj.id == 42
    assert obj.foo == "bar"
    with pytest.raises(StopIteration):
        obj_list.next()


def test_create_mixin_missing_attrs(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._create_attrs.validate_attrs(data=data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._create_attrs.validate_attrs(data=data)
    assert "foo" in str(error.value)


@responses.activate
def test_create_mixin(gl):
    class M(CreateMixin, FakeManager):
        _create_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = gl_types.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
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
        _create_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = gl_types.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/others"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "foo": "bar"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    obj = mgr.create({"foo": "bar"}, path="/others")
    assert isinstance(obj, FakeObject)
    assert obj.id == 42
    assert obj.foo == "bar"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_create_mixin_with_attributes(gl):
    class M(CreateMixin, FakeManager):
        _types = {"my_array": gl_types.ArrayAttribute}

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.POST,
        headers={},
        url=url,
        json={},
        status=200,
        match=[responses.matchers.json_params_matcher({"my_array": [1, 2, 3]})],
    )

    mgr = M(gl)
    mgr.create({"my_array": [1, 2, 3]})


def test_update_mixin_missing_attrs(gl):
    class M(UpdateMixin, FakeManager):
        _update_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )

    mgr = M(gl)
    data = {"foo": "bar", "baz": "blah"}
    mgr._update_attrs.validate_attrs(data=data)

    data = {"baz": "blah"}
    with pytest.raises(AttributeError) as error:
        mgr._update_attrs.validate_attrs(data=data)
    assert "foo" in str(error.value)


@responses.activate
def test_update_mixin(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = gl_types.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests/42"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"id": 42, "foo": "baz"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    server_data = mgr.update(42, {"foo": "baz"})
    assert isinstance(server_data, dict)
    assert server_data["id"] == 42
    assert server_data["foo"] == "baz"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_update_mixin_uses_post(gl):
    class M(UpdateMixin, FakeManager):
        _update_method = UpdateMethod.POST

    url = "http://localhost/api/v4/tests/1"
    responses.add(
        method=responses.POST,
        url=url,
        json={},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    mgr.update(1, {})
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_update_mixin_no_id(gl):
    class M(UpdateMixin, FakeManager):
        _create_attrs = gl_types.RequiredOptional(
            required=("foo",), optional=("bar", "baz")
        )
        _update_attrs = gl_types.RequiredOptional(required=("foo",), optional=("bam",))

    url = "http://localhost/api/v4/tests"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"foo": "baz"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
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
        match=[responses.matchers.query_param_matcher({})],
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
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    obj = TestClass(mgr, {"id": 42, "foo": "bar"})
    obj.foo = "baz"
    obj.save()
    assert obj._attrs["foo"] == "baz"
    assert obj._updated_attrs == {}
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_save_mixin_without_new_data(gl):
    class M(UpdateMixin, FakeManager):
        pass

    class TestClass(SaveMixin, base.RESTObject):
        pass

    url = "http://localhost/api/v4/tests/1"
    responses.add(method=responses.PUT, url=url)

    mgr = M(gl)
    obj = TestClass(mgr, {"id": 1, "foo": "bar"})
    obj.save()

    assert obj._attrs["foo"] == "bar"
    assert responses.assert_call_count(url, 0) is True


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
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = M(gl)
    obj = mgr.set("foo", "bar")
    assert isinstance(obj, FakeObject)
    assert obj.key == "foo"
    assert obj.value == "bar"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_upload_mixin_with_filepath_and_filedata(gl):
    class TestClass(UploadMixin, FakeObject):
        _upload_path = "/tests/{id}/uploads"

    url = "http://localhost/api/v4/tests/42/uploads"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "file_name": "test.txt", "file_content": "testing contents"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = FakeManager(gl)
    obj = TestClass(mgr, {"id": 42})
    with pytest.raises(
        GitlabUploadError, match="File contents and file path specified"
    ):
        obj.upload("test.txt", "testing contents", "/home/test.txt")


@responses.activate
def test_upload_mixin_without_filepath_nor_filedata(gl):
    class TestClass(UploadMixin, FakeObject):
        _upload_path = "/tests/{id}/uploads"

    url = "http://localhost/api/v4/tests/42/uploads"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "file_name": "test.txt", "file_content": "testing contents"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = FakeManager(gl)
    obj = TestClass(mgr, {"id": 42})
    with pytest.raises(GitlabUploadError, match="No file contents or path specified"):
        obj.upload("test.txt")


@responses.activate
def test_upload_mixin_with_filedata(gl):
    class TestClass(UploadMixin, FakeObject):
        _upload_path = "/tests/{id}/uploads"

    url = "http://localhost/api/v4/tests/42/uploads"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "file_name": "test.txt", "file_content": "testing contents"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = FakeManager(gl)
    obj = TestClass(mgr, {"id": 42})
    res_only_data = obj.upload("test.txt", "testing contents")
    assert obj._get_upload_path() == "/tests/42/uploads"
    assert isinstance(res_only_data, dict)
    assert res_only_data["file_name"] == "test.txt"
    assert res_only_data["file_content"] == "testing contents"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_upload_mixin_with_filepath(gl):
    class TestClass(UploadMixin, FakeObject):
        _upload_path = "/tests/{id}/uploads"

    url = "http://localhost/api/v4/tests/42/uploads"
    responses.add(
        method=responses.POST,
        url=url,
        json={"id": 42, "file_name": "test.txt", "file_content": "testing contents"},
        status=200,
        match=[responses.matchers.query_param_matcher({})],
    )

    mgr = FakeManager(gl)
    obj = TestClass(mgr, {"id": 42})
    with patch("builtins.open", mock_open(read_data="raw\nfile\ndata")):
        res_only_path = obj.upload("test.txt", None, "/filepath")
    assert obj._get_upload_path() == "/tests/42/uploads"
    assert isinstance(res_only_path, dict)
    assert res_only_path["file_name"] == "test.txt"
    assert res_only_path["file_content"] == "testing contents"
    assert responses.assert_call_count(url, 1) is True
