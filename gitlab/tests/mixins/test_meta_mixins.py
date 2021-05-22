from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    NoUpdateMixin,
    RetrieveMixin,
    UpdateMixin,
)


def test_retrieve_mixin():
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


def test_crud_mixin():
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


def test_no_update_mixin():
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
