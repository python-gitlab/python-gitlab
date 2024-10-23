import pickle

import pytest

import gitlab
from gitlab import base
from tests.unit import helpers
from tests.unit.helpers import FakeManager  # noqa: F401, needed for _create_managers


def test_instantiate(gl, fake_manager):
    attrs = {"foo": "bar"}
    obj = helpers.FakeObject(fake_manager, attrs.copy())

    assert attrs == obj._attrs
    assert {} == obj._updated_attrs
    assert obj._create_managers() is None
    assert fake_manager == obj.manager
    assert gl == obj.manager.gitlab
    assert str(obj) == f"{type(obj)} => {attrs}"


def test_instantiate_non_dict(gl, fake_manager):
    with pytest.raises(gitlab.exceptions.GitlabParsingError):
        helpers.FakeObject(fake_manager, ["a", "list", "fails"])


def test_missing_attribute_does_not_raise_custom(gl, fake_manager):
    """Ensure a missing attribute does not raise our custom error message
    if the RESTObject was not created from a list"""
    obj = helpers.FakeObject(manager=fake_manager, attrs={"foo": "bar"})
    with pytest.raises(AttributeError) as excinfo:
        obj.missing_attribute
    exc_str = str(excinfo.value)
    assert "missing_attribute" in exc_str
    assert "was created via a list()" not in exc_str
    assert base._URL_ATTRIBUTE_ERROR not in exc_str


def test_missing_attribute_from_list_raises_custom(gl, fake_manager):
    """Ensure a missing attribute raises our custom error message if the
    RESTObject was created from a list"""
    obj = helpers.FakeObject(
        manager=fake_manager, attrs={"foo": "bar"}, created_from_list=True
    )
    with pytest.raises(AttributeError) as excinfo:
        obj.missing_attribute
    exc_str = str(excinfo.value)
    assert "missing_attribute" in exc_str
    assert "was created via a list()" in exc_str
    assert base._URL_ATTRIBUTE_ERROR in exc_str


def test_picklability(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "bar"})
    original_obj_module = obj._module
    pickled = pickle.dumps(obj)
    unpickled = pickle.loads(pickled)
    assert isinstance(unpickled, helpers.FakeObject)
    assert hasattr(unpickled, "_module")
    assert unpickled._module == original_obj_module
    pickle.dumps(unpickled)


def test_attrs(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "bar"})

    assert "bar" == obj.foo
    with pytest.raises(AttributeError):
        getattr(obj, "bar")

    obj.bar = "baz"
    assert "baz" == obj.bar
    assert {"foo": "bar"} == obj._attrs
    assert {"bar": "baz"} == obj._updated_attrs


def test_get_id(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "bar"})
    obj.id = 42
    assert 42 == obj.get_id()

    obj.id = None
    assert obj.get_id() is None


def test_encoded_id(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "bar"})
    obj.id = 42
    assert 42 == obj.encoded_id

    obj.id = None
    assert obj.encoded_id is None

    obj.id = "plain"
    assert "plain" == obj.encoded_id

    obj.id = "a/path"
    assert "a%2Fpath" == obj.encoded_id

    # If you assign it again it does not double URL-encode
    obj.id = obj.encoded_id
    assert "a%2Fpath" == obj.encoded_id


def test_custom_id_attr(fake_manager):
    obj = helpers.OtherFakeObject(fake_manager, {"foo": "bar"})
    assert "bar" == obj.get_id()


def test_update_attrs(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "bar"})
    obj.bar = "baz"
    obj._update_attrs({"foo": "foo", "bar": "bar"})
    assert {"foo": "foo", "bar": "bar"} == obj._attrs
    assert {} == obj._updated_attrs


def test_update_attrs_deleted(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"foo": "foo", "bar": "bar"})
    obj.bar = "baz"
    obj._update_attrs({"foo": "foo"})
    assert {"foo": "foo"} == obj._attrs
    assert {} == obj._updated_attrs


def test_dir_unique(fake_manager):
    obj = helpers.FakeObject(fake_manager, {"manager": "foo"})
    assert len(dir(obj)) == len(set(dir(obj)))


def test_create_managers(gl, fake_manager):
    class ObjectWithManager(helpers.FakeObject):
        fakes: "FakeManager"

    obj = ObjectWithManager(fake_manager, {"foo": "bar"})
    obj.id = 42
    assert isinstance(obj.fakes, helpers.FakeManager)
    assert obj.fakes.gitlab == gl
    assert obj.fakes._parent == obj


def test_equality(fake_manager):
    obj1 = helpers.FakeObject(fake_manager, {"id": "foo"})
    obj2 = helpers.FakeObject(fake_manager, {"id": "foo", "other_attr": "bar"})
    assert obj1 == obj2
    assert len(set((obj1, obj2))) == 1


def test_equality_custom_id(fake_manager):
    obj1 = helpers.OtherFakeObject(fake_manager, {"foo": "bar"})
    obj2 = helpers.OtherFakeObject(fake_manager, {"foo": "bar", "other_attr": "baz"})
    assert obj1 == obj2


def test_equality_no_id(fake_manager):
    obj1 = helpers.FakeObject(fake_manager, {"attr1": "foo"})
    obj2 = helpers.FakeObject(fake_manager, {"attr1": "bar"})
    assert not obj1 == obj2


def test_inequality(fake_manager):
    obj1 = helpers.FakeObject(fake_manager, {"id": "foo"})
    obj2 = helpers.FakeObject(fake_manager, {"id": "bar"})
    assert obj1 != obj2


def test_inequality_no_id(fake_manager):
    obj1 = helpers.FakeObject(fake_manager, {"attr1": "foo"})
    obj2 = helpers.FakeObject(fake_manager, {"attr1": "bar"})
    assert obj1 != obj2
    assert len(set((obj1, obj2))) == 2


def test_equality_with_other_objects(fake_manager):
    obj1 = helpers.FakeObject(fake_manager, {"id": "foo"})
    obj2 = None
    assert not obj1 == obj2


def test_dunder_str(fake_manager):
    fake_object = helpers.FakeObject(fake_manager, {"attr1": "foo"})
    assert str(fake_object) == (
        "<class 'tests.unit.helpers.FakeObject'> => {'attr1': 'foo'}"
    )


@pytest.mark.parametrize(
    "id_attr,repr_attr, attrs, expected_repr",
    [
        ("id", None, {"id": 1}, "<ReprObject id:1>"),
        (
            "id",
            "name",
            {"id": 1, "name": "fake"},
            "<ReprObject id:1 name:fake>",
        ),
        ("name", "name", {"name": "fake"}, "<ReprObject name:fake>"),
        ("id", "name", {"id": 1}, "<ReprObject id:1>"),
        (None, None, {}, "<ReprObject>"),
        (None, "name", {"name": "fake"}, "<ReprObject name:fake>"),
        (None, "name", {}, "<ReprObject>"),
    ],
    ids=[
        "GetMixin with id",
        "GetMixin with id and _repr_attr",
        "GetMixin with _repr_attr matching _id_attr",
        "GetMixin with _repr_attr without _repr_attr value defined",
        "GetWithoutIDMixin",
        "GetWithoutIDMixin with _repr_attr",
        "GetWithoutIDMixin with _repr_attr without _repr_attr value defined",
    ],
)
def test_dunder_repr(fake_manager, id_attr, repr_attr, attrs, expected_repr):
    class ReprObject(helpers.FakeObject):
        _id_attr = id_attr
        _repr_attr = repr_attr

    fake_object = ReprObject(fake_manager, attrs)

    assert repr(fake_object) == expected_repr


def test_pformat(fake_manager):
    fake_object = helpers.FakeObject(
        fake_manager, {"attr1": "foo" * 10, "ham": "eggs" * 15}
    )
    assert fake_object.pformat() == (
        "<class 'tests.unit.helpers.FakeObject'> => "
        "\n{'attr1': 'foofoofoofoofoofoofoofoofoofoo',\n"
        " 'ham': 'eggseggseggseggseggseggseggseggseggseggseggseggseggseggseggs'}"
    )


def test_pprint(capfd, fake_manager):
    fake_object = helpers.FakeObject(
        fake_manager, {"attr1": "foo" * 10, "ham": "eggs" * 15}
    )
    result = fake_object.pprint()
    assert result is None
    stdout, stderr = capfd.readouterr()
    assert stdout == (
        "<class 'tests.unit.helpers.FakeObject'> => "
        "\n{'attr1': 'foofoofoofoofoofoofoofoofoofoo',\n"
        " 'ham': 'eggseggseggseggseggseggseggseggseggseggseggseggseggseggseggs'}\n"
    )
    assert stderr == ""


def test_repr(fake_manager):
    attrs = {"attr1": "foo"}
    obj = helpers.FakeObject(fake_manager, attrs)
    assert repr(obj) == "<FakeObject id:None>"

    helpers.FakeObject._id_attr = None
    assert repr(obj) == "<FakeObject>"


def test_attributes_get(fake_object):
    assert fake_object.attr1 == "foo"
    result = fake_object.attributes
    assert result == {"attr1": "foo", "alist": [1, 2, 3]}


def test_attributes_shows_updates(fake_object):
    # Updated attribute value is reflected in `attributes`
    fake_object.attr1 = "hello"
    assert fake_object.attributes == {"attr1": "hello", "alist": [1, 2, 3]}
    assert fake_object.attr1 == "hello"
    # New attribute is in `attributes`
    fake_object.new_attrib = "spam"
    assert fake_object.attributes == {
        "attr1": "hello",
        "new_attrib": "spam",
        "alist": [1, 2, 3],
    }


def test_attributes_is_copy(fake_object):
    # Modifying the dictionary does not cause modifications to the object
    result = fake_object.attributes
    result["alist"].append(10)
    assert result == {"attr1": "foo", "alist": [1, 2, 3, 10]}
    assert fake_object.attributes == {"attr1": "foo", "alist": [1, 2, 3]}


def test_attributes_has_parent_attrs(fake_object_with_parent):
    assert fake_object_with_parent.attr1 == "foo"
    result = fake_object_with_parent.attributes
    assert result == {"attr1": "foo", "alist": [1, 2, 3], "test_id": "42"}


def test_to_json(fake_object):
    assert fake_object.attr1 == "foo"
    result = fake_object.to_json()
    assert result == '{"attr1": "foo", "alist": [1, 2, 3]}'


def test_asdict(fake_object):
    assert fake_object.attr1 == "foo"
    result = fake_object.asdict()
    assert result == {"attr1": "foo", "alist": [1, 2, 3]}


def test_asdict_no_parent_attrs(fake_object_with_parent):
    assert fake_object_with_parent.attr1 == "foo"
    result = fake_object_with_parent.asdict()
    assert result == {"attr1": "foo", "alist": [1, 2, 3]}
    assert "test_id" not in fake_object_with_parent.asdict()
    assert "test_id" not in fake_object_with_parent.asdict(with_parent_attrs=False)
    assert "test_id" in fake_object_with_parent.asdict(with_parent_attrs=True)


def test_asdict_modify_dict_does_not_change_object(fake_object):
    result = fake_object.asdict()
    # Demonstrate modifying the dictionary does not modify the object
    result["attr1"] = "testing"
    result["alist"].append(4)
    assert result == {"attr1": "testing", "alist": [1, 2, 3, 4]}
    assert fake_object.attr1 == "foo"
    assert fake_object.alist == [1, 2, 3]


def test_asdict_modify_dict_does_not_change_object2(fake_object):
    # Modify attribute and then ensure modifying a list in the returned dict won't
    # modify the list in the object.
    fake_object.attr1 = [9, 7, 8]
    assert fake_object.asdict() == {
        "attr1": [9, 7, 8],
        "alist": [1, 2, 3],
    }
    result = fake_object.asdict()
    result["attr1"].append(1)
    assert fake_object.asdict() == {
        "attr1": [9, 7, 8],
        "alist": [1, 2, 3],
    }


def test_asdict_modify_object(fake_object):
    # asdict() returns the updated value
    fake_object.attr1 = "spam"
    assert fake_object.asdict() == {"attr1": "spam", "alist": [1, 2, 3]}
