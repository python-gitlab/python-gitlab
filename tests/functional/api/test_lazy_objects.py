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


def test_delete_after_lazy_get_with_path(gl, group, wait_for_sidekiq):
    project = gl.projects.create({"name": "lazy_project", "namespace_id": group.id})
    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"
    lazy_project = gl.projects.get(project.path_with_namespace, lazy=True)
    lazy_project.delete()


def test_list_children_after_lazy_get_with_path(gl, lazy_project):
    lazy_project.mergerequests.list()
