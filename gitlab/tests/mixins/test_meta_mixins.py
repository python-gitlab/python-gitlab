from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    NoUpdateMixin,
    UpdateMixin,
    RetrieveMixin,
)


def test_retrieve_mixin():
    class M(RetrieveMixin):
        def __init__(self):
            ...

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
        def __init__(self):
            ...

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
        def __init__(self):
            ...

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
