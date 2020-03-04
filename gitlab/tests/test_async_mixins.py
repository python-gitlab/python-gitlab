import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import AsyncGitlab
from gitlab.base import RESTObject, RESTObjectList
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

from .test_mixins import FakeManager, FakeObject


class TestMixinMethods:
    @pytest.fixture
    def gl(self):
        return AsyncGitlab(
            "http://localhost", private_token="private_token", api_version=4
        )

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_mixin(self, gl):
        class M(GetMixin, FakeManager):
            pass

        request = respx.get(
            "http://localhost/api/v4/tests/42",
            headers={"Content-Type": "application/json"},
            content={"id": 42, "foo": "bar"},
            status_code=StatusCode.OK,
        )
        mgr = M(gl)
        obj = await mgr.get(42)
        assert isinstance(obj, FakeObject)
        assert obj.foo == "bar"
        assert obj.id == 42

    @respx.mock
    @pytest.mark.asyncio
    async def test_refresh_mixin(self, gl):
        class O(RefreshMixin, FakeObject):
            pass

        request = respx.get(
            "http://localhost/api/v4/tests/42",
            headers={"Content-Type": "application/json"},
            content={"id": 42, "foo": "bar"},
            status_code=StatusCode.OK,
        )
        mgr = FakeManager(gl)
        obj = O(mgr, {"id": 42})
        res = await obj.refresh()
        assert res is None
        assert obj.foo == "bar"
        assert obj.id == 42

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_without_id_mixin(self, gl):
        class M(GetWithoutIdMixin, FakeManager):
            pass

        request = respx.get(
            "http://localhost/api/v4/tests",
            headers={"Content-Type": "application/json"},
            content='{"foo": "bar"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj = await mgr.get()
        assert isinstance(obj, FakeObject)
        assert obj.foo == "bar"
        assert not hasattr(obj, "id")

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_mixin(self, gl):
        class M(ListMixin, FakeManager):
            pass

        request = respx.get(
            "http://localhost/api/v4/tests",
            headers={"Content-Type": "application/json"},
            content='[{"id": 42, "foo": "bar"},{"id": 43, "foo": "baz"}]',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj_list = await mgr.list(as_list=False)
        assert isinstance(obj_list, RESTObjectList)
        async for obj in obj_list:
            assert isinstance(obj, FakeObject)
            assert obj.id in (42, 43)

        obj_list = await mgr.list(all=True)
        assert isinstance(obj_list, list)
        assert obj_list[0].id == 42
        assert obj_list[1].id == 43
        assert isinstance(obj_list[0], FakeObject)
        assert len(obj_list) == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_other_url(self, gl):
        class M(ListMixin, FakeManager):
            pass

        request = respx.get(
            "http://localhost/api/v4/others",
            headers={"Content-Type": "application/json"},
            content='[{"id": 42, "foo": "bar"}]',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj_list = await mgr.list(path="/others", as_list=False)
        assert isinstance(obj_list, RESTObjectList)
        obj = await obj_list.anext()
        assert obj.id == 42
        assert obj.foo == "bar"
        with pytest.raises(StopAsyncIteration):
            await obj_list.anext()

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_mixin(self, gl):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        reqeust = respx.post(
            "http://localhost/api/v4/tests",
            headers={"Content-Type": "application/json"},
            content='{"id": 42, "foo": "bar"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj = await mgr.create({"foo": "bar"})
        assert isinstance(obj, FakeObject)
        assert obj.id == 42
        assert obj.foo == "bar"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_mixin_custom_path(self, gl):
        class M(CreateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        request = respx.post(
            "http://localhost/api/v4/others",
            headers={"Content-Type": "application/json"},
            content='{"id": 42, "foo": "bar"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj = await mgr.create({"foo": "bar"}, path="/others")
        assert isinstance(obj, FakeObject)
        assert obj.id == 42
        assert obj.foo == "bar"

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_mixin(self, gl):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        request = respx.put(
            "http://localhost/api/v4/tests/42",
            headers={"Content-Type": "application/json"},
            content='{"id": 42, "foo": "baz"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        server_data = await mgr.update(42, {"foo": "baz"})
        assert isinstance(server_data, dict)
        assert server_data["id"] == 42
        assert server_data["foo"] == "baz"

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_mixin_no_id(self, gl):
        class M(UpdateMixin, FakeManager):
            _create_attrs = (("foo",), ("bar", "baz"))
            _update_attrs = (("foo",), ("bam",))

        request = respx.put(
            "http://localhost/api/v4/tests",
            headers={"Content-Type": "application/json"},
            content='{"foo": "baz"}',
            status_code=StatusCode.OK,
        )
        mgr = M(gl)
        server_data = await mgr.update(new_data={"foo": "baz"})
        assert isinstance(server_data, dict)
        assert server_data["foo"] == "baz"

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_mixin(self, gl):
        class M(DeleteMixin, FakeManager):
            pass

        request = respx.delete(
            "http://localhost/api/v4/tests/42",
            headers={"Content-Type": "application/json"},
            content="",
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        await mgr.delete(42)

    @respx.mock
    @pytest.mark.asyncio
    async def test_save_mixin(self, gl):
        class M(UpdateMixin, FakeManager):
            pass

        class O(SaveMixin, RESTObject):
            pass

        request = respx.put(
            "http://localhost/api/v4/tests/42",
            headers={"Content-Type": "application/json"},
            content='{"id": 42, "foo": "baz"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj = O(mgr, {"id": 42, "foo": "bar"})
        obj.foo = "baz"
        await obj.save()
        assert obj._attrs["foo"] == "baz"
        assert obj._updated_attrs == {}

    @respx.mock
    @pytest.mark.asyncio
    async def test_set_mixin(self, gl):
        class M(SetMixin, FakeManager):
            pass

        request = respx.put(
            "http://localhost/api/v4/tests/foo",
            headers={"Content-Type": "application/json"},
            content='{"key": "foo", "value": "bar"}',
            status_code=StatusCode.OK,
        )

        mgr = M(gl)
        obj = await mgr.set("foo", "bar")
        assert isinstance(obj, FakeObject)
        assert obj.key == "foo"
        assert obj.value == "bar"
