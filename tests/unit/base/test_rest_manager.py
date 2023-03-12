from gitlab import base
from tests.unit import helpers


def test_computed_path_simple(gl):
    class MGR(base.RESTManager):
        _path = "/tests"
        _obj_cls = object

    mgr = MGR(gl)
    assert mgr._computed_path == "/tests"


def test_computed_path_with_parent(gl, fake_manager):
    class MGR(base.RESTManager):
        _path = "/tests/{test_id}/cases"
        _obj_cls = object
        _from_parent_attrs = {"test_id": "id"}

    mgr = MGR(gl, parent=helpers.FakeParent(manager=fake_manager, attrs={}))
    assert mgr._computed_path == "/tests/42/cases"


def test_path_property(gl):
    class MGR(base.RESTManager):
        _path = "/tests"
        _obj_cls = object

    mgr = MGR(gl)
    assert mgr.path == "/tests"
