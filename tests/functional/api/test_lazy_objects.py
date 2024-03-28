import time

import pytest

import gitlab


@pytest.fixture
def lazy_project(gl, project):
    assert "/" in project.path_with_namespace
    return gl.projects.get(project.path_with_namespace, lazy=True)


def test_lazy_id(project, lazy_project):
    assert isinstance(lazy_project.id, str)
    assert isinstance(lazy_project.id, gitlab.utils.EncodedId)
    assert lazy_project.id == gitlab.utils.EncodedId(project.path_with_namespace)


def test_refresh_after_lazy_get_with_path(project, lazy_project):
    lazy_project.refresh()
    assert lazy_project.id == project.id


def test_save_after_lazy_get_with_path(project, lazy_project):
    lazy_project.description = "A new description"
    lazy_project.save()
    assert lazy_project.id == project.id
    assert lazy_project.description == "A new description"


def test_delete_after_lazy_get_with_path(gl, group):
    project = gl.projects.create({"name": "lazy_project", "namespace_id": group.id})
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)
    lazy_project = gl.projects.get(project.path_with_namespace, lazy=True)
    lazy_project.delete()


def test_list_children_after_lazy_get_with_path(gl, lazy_project):
    lazy_project.mergerequests.list()
